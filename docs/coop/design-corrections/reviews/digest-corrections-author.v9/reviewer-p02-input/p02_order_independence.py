"""p02 - Is the same-path aggregation actually ORDER-INDEPENDENT, as record() claims?

record()'s own docstring states the intended law:

    "Never let an annotated sighting erase an unannotated one at the same path ... so
     admissibility cannot depend on branch order."

Implementation (identity-model.py:337-343):

    previous=seen.get(path)
    if previous is not None:
        form=previous['form'] or form
        joinable=previous['joinable'] and joinable
        annotations=previous['annotations']+[a for a in annotations if a not in previous['annotations']]
        if not previous['annotations'] or not annotations:annotations=[]
    seen[path]={...}

`annotations` is REBOUND on the merge line before it is tested. So `not annotations` is true only
when previous and incoming were BOTH empty (a no-op). The effective rule is therefore

    poison iff the FIRST-RECORDED sighting was unannotated

which is exactly a branch-order dependence, not order-independence.

This probe does not argue from source. It constructs two documents with the SAME multiset of
sightings at one path - one annotated, one unannotated - differing only in visit order, and
compares admission.
"""
import sys
sys.path.insert(0, '/tmp/opensip-design-corrections/post-reset-review.v10/probes')
import harness

m = harness.load_model()
REL = 'file'
ANN = {'representation': 'raw-artifact', 'retention': 'not-joined',
       'reason': 'reviewer probe field, deliberately not joined'}

out = {'modelSha256': m._sha256}


def selector_of(doc, name):
    row = doc['x-opensip-relation-registry']['relations'][name]
    return doc['$defs'][row['selector'].split('/')[-1]]


def run(build, label):
    doc = harness.base_document(m)
    build(doc)
    verdict, cause = harness.try_closure(m, REL, doc)
    cov = m.relation_digest_annotation_coverage(doc)
    sight = [s for s in cov['sightings'] if s['path'].startswith(REL + '.probe')]
    return {'label': label, 'verdict': verdict, 'cause': cause,
            'unannotated': cov['unannotated'],
            'probeSightings': sight}


# =============================================================== CASE A: $ref container + sibling
# A node may carry BOTH a $ref to a container def and its own `properties` - the walker follows the
# $ref first (line 358-362) and then the node's own properties (line 363+), so both land on the
# SAME path. The two arrangements below contain the identical pair of sightings; only which one the
# walker reaches first differs.

def a_unannotated_first(doc):
    """Container supplies the leaf UNANNOTATED; the local refinement annotates it."""
    doc['$defs']['ProbeContainer'] = {
        'type': 'object', 'properties': {'leaf': {'$ref': '#/$defs/DigestHex'}}}
    selector_of(doc, REL)['properties']['probe'] = {
        '$ref': '#/$defs/ProbeContainer',
        'properties': {'leaf': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ANN}}}


def a_annotated_first(doc):
    """Container supplies the leaf ANNOTATED; the local refinement leaves it unannotated.
    Same two sightings at the same path, opposite visit order."""
    doc['$defs']['ProbeContainer'] = {
        'type': 'object',
        'properties': {'leaf': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ANN}}}
    selector_of(doc, REL)['properties']['probe'] = {
        '$ref': '#/$defs/ProbeContainer',
        'properties': {'leaf': {'$ref': '#/$defs/DigestHex'}}}


out['caseA_unannotated_first'] = run(a_unannotated_first, 'container unannotated, local annotated')
out['caseA_annotated_first'] = run(a_annotated_first, 'container annotated, local unannotated')

# ======================================================= CASE B: pure key-order swap, same content
# `items` and `additionalProperties` BOTH map to path + '[]' (line 371-373). Two documents with the
# identical pair of subschemas, differing ONLY in which key is written first in the JSON object.

def b_items_first(doc):
    selector_of(doc, REL)['properties']['probe'] = {
        'items': {'$ref': '#/$defs/DigestHex'},
        'additionalProperties': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ANN},
    }


def b_addprops_first(doc):
    selector_of(doc, REL)['properties']['probe'] = {
        'additionalProperties': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ANN},
        'items': {'$ref': '#/$defs/DigestHex'},
    }


out['caseB_items_first'] = run(b_items_first, 'items(unannotated) written before additionalProperties(annotated)')
out['caseB_addprops_first'] = run(b_addprops_first, 'additionalProperties(annotated) written before items(unannotated)')

# ============================================================ CONTROLS: unambiguous single sightings
def c_only_unannotated(doc):
    selector_of(doc, REL)['properties']['probe'] = {'$ref': '#/$defs/DigestHex'}


def c_only_annotated(doc):
    selector_of(doc, REL)['properties']['probe'] = {'$ref': '#/$defs/DigestHex',
                                                    'x-opensip-digest': ANN}


out['control_only_unannotated'] = run(c_only_unannotated, 'single unannotated governed field')
out['control_only_annotated'] = run(c_only_annotated, 'single lawful annotated not-joined field')

# ===================================================================================== assessment
A_u, A_a = out['caseA_unannotated_first'], out['caseA_annotated_first']
B_i, B_a = out['caseB_items_first'], out['caseB_addprops_first']

out['ASSESSMENT'] = {
    'caseA_orderDependent': A_u['verdict'] != A_a['verdict'],
    'caseA_verdicts': [A_u['verdict'], A_a['verdict']],
    'caseB_orderDependent': B_i['verdict'] != B_a['verdict'],
    'caseB_verdicts': [B_i['verdict'], B_a['verdict']],
    'caseB_isPureKeyOrderSwap': True,
    'controlsBehaveAsDeclared': (out['control_only_unannotated']['verdict'] == 'REFUSE'
                                 and out['control_only_annotated']['verdict'] == 'ADMIT'),
    'statedRuleViolated': ('an annotated sighting DID erase an unannotated one at the same path'
                           if (A_a['verdict'] == 'ADMIT' or B_a['verdict'] == 'ADMIT')
                           else 'stated rule held'),
}

harness.emit(out, '/tmp/opensip-design-corrections/post-reset-review.v10/work/p02.json')
print(harness.json.dumps(out['ASSESSMENT'], indent=2))
print('--- caseA unannotated-first:', A_u['verdict'], A_u['cause'])
print('--- caseA annotated-first  :', A_a['verdict'], A_a['cause'])
print('--- caseB items-first      :', B_i['verdict'], B_i['cause'])
print('--- caseB addprops-first   :', B_a['verdict'], B_a['cause'])
