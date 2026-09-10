"""p04 - Are ALL THREE limbs consistent across ALL supported effective-annotation locations?

Root's v8 counterexample was: v7 gave only the COVERAGE limb an inherited notion of "annotated"
(property / enclosing branch parent / intermediate alias $def) while RETENTION and RESIDUE still
read properties[field]['x-opensip-digest'] directly. So at exactly the newly-accepted locations a
field escaped both earlier limbs - invalid retention and missing join both admitted.

The v10 claim is that every limb now reads the SAME sightings. This probe tests the full matrix:

  locations  x  cases
  ---------     -----
  field-local        lawful joined            -> ADMIT
  intermediate alias lawful not-joined        -> ADMIT
  branch (oneOf)     invalid retention value  -> REFUSE RELATION_DIGEST_RETENTION
                     annotated, no join       -> REFUSE RELATION_DIGEST_LAW_RESIDUE
                     unannotated              -> REFUSE RELATION_DIGEST_UNANNOTATED

plus the terminal-$def blanket-exemption negative, the conflicting-annotation case, and the
identical-annotation case.
"""
import sys
sys.path.insert(0, '/tmp/opensip-design-corrections/post-reset-review.v10/probes')
import json
import harness
from jsonschema import Draft202012Validator

m = harness.load_model()
REL = 'file'

LAWFUL_NOT_JOINED = {'representation': 'raw-artifact', 'retention': 'not-joined',
                     'authority': 'hypothetical-schema-probe',
                     'reason': 'reviewer schema-only control'}
INVALID_RETENTION = {'representation': 'raw-artifact', 'retention': 'reviewer-invented-retention',
                     'authority': 'hypothetical-schema-probe'}
JOINED_PREIMAGE = {'representation': 'raw-artifact', 'retention': 'preimage',
                   'authority': 'hypothetical-schema-probe',
                   'join': 'reviewer control: claims a join'}

out = {'modelSha256': m._sha256,
       'standing': 'reviewer hypothetical schema-edit matrix; no current payload or Run claim'}


def selector_of(doc, name):
    row = doc['x-opensip-relation-registry']['relations'][name]
    return doc['$defs'][row['selector'].split('/')[-1]]


def evaluate(build, label):
    doc = harness.base_document(m)
    build(doc)
    ok = True
    try:
        Draft202012Validator.check_schema(doc)
    except Exception:
        ok = False
    verdict, cause = harness.try_closure(m, REL, doc)
    return {'label': label, 'metaschemaValid': ok, 'verdict': verdict, 'cause': cause}


# ------------------------------------------------------------------- the three annotation LOCATIONS
def loc_field(ann):
    """Annotation directly on the selector property."""
    def build(doc):
        p = {'$ref': '#/$defs/DigestHex'}
        if ann is not None:
            p['x-opensip-digest'] = ann
        selector_of(doc, REL)['properties']['probe'] = p
    return build


def loc_alias(ann):
    """Annotation on an INTERMEDIATE scalar alias $def that itself refs the governed form.
    (root's alias-positive counterexample: this was initially missed.)"""
    def build(doc):
        alias = {'$ref': '#/$defs/DigestHex'}
        if ann is not None:
            alias['x-opensip-digest'] = ann
        doc['$defs']['ProbeAlias'] = alias
        selector_of(doc, REL)['properties']['probe'] = {'$ref': '#/$defs/ProbeAlias'}
    return build


def loc_branch(ann):
    """Annotation on the PARENT of a nullable oneOf, reaching the governed branch by inheritance."""
    def build(doc):
        p = {'oneOf': [{'$ref': '#/$defs/DigestHex'}, {'type': 'null'}]}
        if ann is not None:
            p['x-opensip-digest'] = ann
        selector_of(doc, REL)['properties']['probe'] = p
    return build


LOCATIONS = {'field-local': loc_field, 'intermediate-alias': loc_alias, 'branch-parent': loc_branch}
CASES = {
    'lawful-not-joined': (LAWFUL_NOT_JOINED, 'ADMIT', None),
    'invalid-retention': (INVALID_RETENTION, 'REFUSE', 'RELATION_DIGEST_RETENTION'),
    'annotated-missing-join': (JOINED_PREIMAGE, 'REFUSE', 'RELATION_DIGEST_LAW_RESIDUE'),
    'unannotated': (None, 'REFUSE', 'RELATION_DIGEST_UNANNOTATED'),
}

matrix = {}
for lname, lbuild in LOCATIONS.items():
    for cname, (ann, expect, cause_frag) in CASES.items():
        r = evaluate(lbuild(ann), lname + ' / ' + cname)
        r['expectedVerdict'] = expect
        r['expectedCauseFragment'] = cause_frag
        r['asExpected'] = (r['verdict'] == expect and
                           (cause_frag is None or (r['cause'] and cause_frag in r['cause'])))
        matrix[lname + '/' + cname] = r
out['matrix'] = matrix
out['matrixCells'] = len(matrix)
out['matrixAllAsExpected'] = all(r['asExpected'] for r in matrix.values())
out['matrixConsistentAcrossLocations'] = {
    cname: sorted({matrix[l + '/' + cname]['verdict'] for l in LOCATIONS})
    for cname in CASES}


# -------------------------------------- terminal governed $def annotation is NOT a blanket exemption
def terminal_def_annotation(doc):
    doc['$defs']['DigestHex']['x-opensip-digest'] = LAWFUL_NOT_JOINED
    selector_of(doc, REL)['properties']['probe'] = {'$ref': '#/$defs/DigestHex'}


out['terminal_def_blanket_exemption'] = evaluate(
    terminal_def_annotation, 'annotation on the terminal governed $def must NOT cover every field')
out['terminal_def_refuses'] = (out['terminal_def_blanket_exemption']['verdict'] == 'REFUSE')


# ------------------------------------------------- conflicting vs identical annotations on one path
def conflicting(doc):
    doc['$defs']['ProbeAlias'] = {'$ref': '#/$defs/DigestHex',
                                  'x-opensip-digest': LAWFUL_NOT_JOINED}
    selector_of(doc, REL)['properties']['probe'] = {'$ref': '#/$defs/ProbeAlias',
                                                    'x-opensip-digest': JOINED_PREIMAGE}


def identical(doc):
    doc['$defs']['ProbeAlias'] = {'$ref': '#/$defs/DigestHex',
                                  'x-opensip-digest': dict(LAWFUL_NOT_JOINED)}
    selector_of(doc, REL)['properties']['probe'] = {'$ref': '#/$defs/ProbeAlias',
                                                    'x-opensip-digest': dict(LAWFUL_NOT_JOINED)}


out['conflicting_annotations'] = evaluate(conflicting, 'property and alias annotations DISAGREE')
out['identical_annotations'] = evaluate(identical, 'property and alias annotations are IDENTICAL')
out['conflictRefusesNoInventedPrecedence'] = (
    out['conflicting_annotations']['verdict'] == 'REFUSE'
    and 'RELATION_DIGEST_ANNOTATION_CONFLICT' in (out['conflicting_annotations']['cause'] or ''))
out['identicalAdmits'] = (out['identical_annotations']['verdict'] == 'ADMIT')


# ------------------------------------------- nested/array annotated location must declare not-joined
def nested_joined_claim(doc):
    selector_of(doc, REL)['properties']['probe'] = {
        'type': 'object',
        'properties': {'leaf': {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': JOINED_PREIMAGE}}}


def nested_not_joined(doc):
    selector_of(doc, REL)['properties']['probe'] = {
        'type': 'object',
        'properties': {'leaf': {'$ref': '#/$defs/DigestHex',
                                'x-opensip-digest': LAWFUL_NOT_JOINED}}}


out['nested_claims_join'] = evaluate(nested_joined_claim,
                                     'nested leaf claiming a join a join row cannot reach')
out['nested_declares_not_joined'] = evaluate(nested_not_joined,
                                             'nested leaf lawfully declaring not-joined')
out['unjoinableEnforced'] = (
    'RELATION_DIGEST_UNJOINABLE_LOCATION' in (out['nested_claims_join']['cause'] or '')
    and out['nested_declares_not_joined']['verdict'] == 'ADMIT')

out['ASSESSMENT'] = {
    'matrixCells': out['matrixCells'],
    'matrixAllAsExpected': out['matrixAllAsExpected'],
    'perCaseVerdictsAgreeAcrossAllThreeLocations': {
        k: (len(v) == 1) for k, v in out['matrixConsistentAcrossLocations'].items()},
    'terminalDefNotBlanketExemption': out['terminal_def_refuses'],
    'conflictRefuses': out['conflictRefusesNoInventedPrecedence'],
    'identicalAdmits': out['identicalAdmits'],
    'unjoinableLocationEnforced': out['unjoinableEnforced'],
    'allMetaschemaValid': all(
        r['metaschemaValid'] for r in list(matrix.values()) + [
            out['terminal_def_blanket_exemption'], out['conflicting_annotations'],
            out['identical_annotations'], out['nested_claims_join'],
            out['nested_declares_not_joined']]),
}

harness.emit(out, '/tmp/opensip-design-corrections/post-reset-review.v10/work/p04.json')
print(json.dumps(out['ASSESSMENT'], indent=2))
for k, v in sorted(matrix.items()):
    print(('OK ' if v['asExpected'] else 'XX '), k, '->', v['verdict'], (v['cause'] or '')[:80])
