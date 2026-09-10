"""p03 - Harden the p02 order-dependence counterexample against every fair objection.

Objections anticipated:
  (a) "your hypothetical document is not a valid schema"      -> Draft202012Validator.check_schema
  (b) "$ref with sibling keywords is not in the language"     -> the document declares
      $schema draft/2020-12, where $ref is an ordinary applicator evaluated ALONGSIDE siblings.
      The walker itself deliberately follows the $ref and THEN the node's own keywords.
  (c) "you are demanding an unsupported future feature"       -> both colliding locations are forms
      the implementation explicitly claims to support: $ref-to-container (added in response to
      root's own counterexample) and items/additionalProperties.
  (d) "the difference is really a content difference"         -> case B swaps only JSON key order.
      Case A swaps only WHICH of the two identical locations carries the identical annotation.
  (e) "it is caught elsewhere"                                -> the closure result is reported.

Also establishes MINIMALITY/SCOPE: the shipped document has no same-path collision at all, so no
current relation, payload or Run is affected.
"""
import sys
sys.path.insert(0, '/tmp/opensip-design-corrections/post-reset-review.v10/probes')
import collections
import json
import harness
from jsonschema import Draft202012Validator

m = harness.load_model()
REL = 'file'
ANN = {'representation': 'raw-artifact', 'retention': 'not-joined',
       'authority': 'hypothetical-schema-probe',
       'reason': 'reviewer schema-only control; no runtime field or authority introduced'}

out = {'modelSha256': m._sha256,
       'standing': ('reviewer hypothetical SCHEMA-EDIT counterexample against the design/reference '
                    'guard; NOT a current payload attack, Run bypass or acceptance claim')}


def selector_of(doc, name):
    row = doc['x-opensip-relation-registry']['relations'][name]
    return doc['$defs'][row['selector'].split('/')[-1]]


def evaluate(build, label):
    doc = harness.base_document(m)
    build(doc)
    metaschema_ok, metaschema_err = True, None
    try:
        Draft202012Validator.check_schema(doc)
    except Exception as exc:
        metaschema_ok, metaschema_err = False, str(exc)[:300]
    verdict, cause = harness.try_closure(m, REL, doc)
    cov = m.relation_digest_annotation_coverage(doc)
    return {'label': label, 'metaschemaValid': metaschema_ok, 'metaschemaError': metaschema_err,
            'verdict': verdict, 'cause': cause, 'unannotated': cov['unannotated'],
            'probeSubschema': selector_of(doc, REL)['properties'].get('probe'),
            'probeDefs': {k: v for k, v in doc['$defs'].items() if k.startswith('Probe')}}


# ---------------------------------------------------------------------------- SCOPE / MINIMALITY
shipped = m.relation_digest_annotation_coverage(harness.base_document(m))
paths = [s['path'] for s in shipped['sightings']]
out['shippedScope'] = {
    'sightingPaths': paths,
    'duplicatePaths': [p for p, n in collections.Counter(paths).items() if n > 1],
    'shippedHasNoSamePathCollision': len(paths) == len(set(paths)),
    'shippedUnannotated': shipped['unannotated'],
    'note': 'no shipped relation is affected; this is a guard against future registered edits',
}

# ------------------------------------------------------------- CASE A: $ref sibling (2020-12 idiom)
def a_unannotated_first(doc):
    doc['$defs']['ProbeContainer'] = {
        'type': 'object', 'properties': {'leaf': {'$ref': '#/$defs/DigestHex'}}}
    selector_of(doc, REL)['properties']['probe'] = {
        '$ref': '#/$defs/ProbeContainer',
        'properties': {'leaf': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ANN}}}


def a_annotated_first(doc):
    doc['$defs']['ProbeContainer'] = {
        'type': 'object',
        'properties': {'leaf': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ANN}}}
    selector_of(doc, REL)['properties']['probe'] = {
        '$ref': '#/$defs/ProbeContainer',
        'properties': {'leaf': {'$ref': '#/$defs/DigestHex'}}}


out['caseA'] = {
    'unannotated_seen_first': evaluate(a_unannotated_first,
                                       'container leaf unannotated; sibling refinement annotated'),
    'annotated_seen_first': evaluate(a_annotated_first,
                                     'container leaf annotated; sibling refinement unannotated'),
}

# ------------------------------------------------------------ CASE B: PURE JSON key-order swap
def b_items_first(doc):
    selector_of(doc, REL)['properties']['probe'] = {
        'items': {'$ref': '#/$defs/DigestHex'},
        'additionalProperties': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ANN}}


def b_addprops_first(doc):
    selector_of(doc, REL)['properties']['probe'] = {
        'additionalProperties': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ANN},
        'items': {'$ref': '#/$defs/DigestHex'}}


out['caseB'] = {
    'items_written_first': evaluate(b_items_first, 'items(unannotated) key written first'),
    'addprops_written_first': evaluate(b_addprops_first,
                                       'additionalProperties(annotated) key written first'),
}
# prove the two case-B documents are byte-equal as SETS of keys and differ only in order
bi = out['caseB']['items_written_first']['probeSubschema']
ba = out['caseB']['addprops_written_first']['probeSubschema']
out['caseB_identicalContent'] = (json.dumps(bi, sort_keys=True) == json.dumps(ba, sort_keys=True))
out['caseB_differentKeyOrder'] = (list(bi.keys()) != list(ba.keys()))

# ------------------------------------------------------------------------------- POSITIVE CONTROLS
def c_unannotated_only(doc):
    doc['$defs']['ProbeContainer'] = {
        'type': 'object', 'properties': {'leaf': {'$ref': '#/$defs/DigestHex'}}}
    selector_of(doc, REL)['properties']['probe'] = {'$ref': '#/$defs/ProbeContainer'}


def c_annotated_only(doc):
    doc['$defs']['ProbeContainer'] = {
        'type': 'object',
        'properties': {'leaf': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ANN}}}
    selector_of(doc, REL)['properties']['probe'] = {'$ref': '#/$defs/ProbeContainer'}


out['controls'] = {
    'container_leaf_unannotated_only': evaluate(c_unannotated_only,
                                                'single unannotated leaf behind container ref'),
    'container_leaf_annotated_only': evaluate(c_annotated_only,
                                              'single lawful annotated leaf behind container ref'),
    'shipped_document': evaluate(lambda d: None, 'unmodified shipped document'),
}

A = out['caseA']
B = out['caseB']
out['ASSESSMENT'] = {
    'allHypotheticalDocumentsMetaschemaValid': all(
        r['metaschemaValid'] for group in (A, B, out['controls']) for r in group.values()),
    'caseA_orderDecidesAdmission': A['unannotated_seen_first']['verdict'] != A['annotated_seen_first']['verdict'],
    'caseA_verdicts': {k: v['verdict'] for k, v in A.items()},
    'caseB_orderDecidesAdmission': B['items_written_first']['verdict'] != B['addprops_written_first']['verdict'],
    'caseB_verdicts': {k: v['verdict'] for k, v in B.items()},
    'caseB_pureKeyOrderSwap': out['caseB_identicalContent'] and out['caseB_differentKeyOrder'],
    'controlsDiscriminate': (out['controls']['container_leaf_unannotated_only']['verdict'] == 'REFUSE'
                             and out['controls']['container_leaf_annotated_only']['verdict'] == 'ADMIT'
                             and out['controls']['shipped_document']['verdict'] == 'ADMIT'),
    'shippedUnaffected': out['shippedScope']['shippedHasNoSamePathCollision'],
    'recordDocstringClaim': 'Never let an annotated sighting erase an unannotated one at the same path',
    'claimHolds': not (A['annotated_seen_first']['verdict'] == 'ADMIT'
                       or B['addprops_written_first']['verdict'] == 'ADMIT'),
}

harness.emit(out, '/tmp/opensip-design-corrections/post-reset-review.v10/work/p03.json')
print(json.dumps(out['ASSESSMENT'], indent=2))
