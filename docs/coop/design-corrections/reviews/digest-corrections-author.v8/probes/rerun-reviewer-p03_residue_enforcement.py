"""RE-RUN of an INDEPENDENT REVIEWER probe against the corrected source. NOT my construction.

Provenance: this file is post-reset-review.v9/probes/p03_residue_enforcement.py, authored by the fresh independent
reviewer (session 93403103-b133-4d69-8700-627712411137) against frozen v9. Its cases, its wording
and its judgement are theirs and are not rewritten. The ONLY change is the SUB path, which pointed
at the frozen candidate copy and now points at the working tree, so the same questions are asked of
the corrected bytes. The original file is retained unaltered in the review directory; this copy is
labelled so it can never be mistaken for the original evidence.
"""
import json, hashlib, copy, sys, importlib.util
from pathlib import Path

SUB = Path('/Users/sb/code/opensip-ai/opensip_arch')  # ADAPTED: working tree, not the frozen copy
FOUND = SUB / 'docs/coop/design-corrections/foundation'
spec = importlib.util.spec_from_file_location('identity_model_v9b', FOUND / 'identity-model.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

raw = (FOUND / 'relation-payload-schemas.v2.json').read_bytes()
d = json.loads(raw)
rows = []

def case(label, relation, mutate, expect):
    doc = copy.deepcopy(d)
    mutate(doc)
    try:
        M.relation_annotation_closure(relation, document=doc)
        got = None
    except Exception as e:
        got = str(e)
    rows.append({'case': label, 'relationAsked': relation, 'raised': got,
                 'expectToken': expect,
                 'reachedIntendedCause': bool(got and expect in got)})

case('annotated-field-with-no-join', 'file',
     lambda doc: doc['$defs']['FilePayloadV1']['properties'].__setitem__('strayDigest', {
         '$ref': '#/$defs/DigestHex',
         'x-opensip-digest': {'representation': 'raw-artifact', 'retention': 'preimage',
                              'authority': 'test', 'codec': 'test'}}),
     'RELATION_DIGEST_LAW_RESIDUE')

case('join-names-field-selector-lacks', 'file',
     lambda doc: doc['x-opensip-relation-registry']['relations']['file']['snapshotJoins'][0]
                 .__setitem__('digestField', 'noSuchField'),
     'RELATION_JOIN_FIELD_UNKNOWN')

case('retention-value-outside-declared-vocabulary', 'file',
     lambda doc: doc['$defs']['FilePayloadV1']['properties']['contentSha256']['x-opensip-digest']
                 .__setitem__('retention', 'invented-mode'),
     'RELATION_DIGEST_RETENTION')

case('clones-bodyIdentity-annotation-removed', 'clones',
     lambda doc: doc['$defs']['ClonesPayloadV1']['properties']['bodyIdentity'].pop('x-opensip-digest'),
     'RELATION_')

# THIRD LIMB: an unannotated DigestHex field added to a relation selector.
case('UNANNOTATED-digest-field-added', 'file',
     lambda doc: doc['$defs']['FilePayloadV1']['properties'].__setitem__(
         'strayBare', {'$ref': '#/$defs/DigestHex'}),
     'RELATION_')

# Does anything ELSE consume the third limb? Search the shipped sources for a sweep that
# requires every DigestHex/Sha256Text/CanonicalPath site in the relation document to be annotated.
def grep(path, needles):
    try:
        t = Path(path).read_text()
    except Exception:
        return {}
    return {n: t.count(n) for n in needles}

consumers = {
    'identity-model.py': grep(FOUND / 'identity-model.py',
                              ['x-opensip-digest', 'digest_sites', 'RELATION_DIGEST_LAW_RESIDUE',
                               'RELATION_DIGEST_ANNOTATION', 'annotated']),
    'check-identity.py': grep(FOUND / 'check-identity.py',
                              ['digest_sites', 'x-opensip-digest', 'RELATION_DIGEST',
                               'annotated-digest', 'relation_annotation_closure']),
}

# Direct question: in the REAL document, is every governed-ref field annotated?
reg = d['x-opensip-relation-registry']['relations']
payload_def_of = {r['selector'].split('/')[-1]: n for n, r in reg.items()}
unannotated = []
for defname, node in d['$defs'].items():
    if defname not in payload_def_of:
        continue
    for pname, p in (node.get('properties') or {}).items():
        rn = (p.get('$ref') or '').split('/')[-1]
        if rn in {'DigestHex', 'Sha256Text', 'CanonicalPath'} and 'x-opensip-digest' not in p:
            unannotated.append(payload_def_of[defname] + '.' + pname)

out = {
    'probe': 'p03_residue_enforcement',
    'standing': 'independent reviewer probe; design/reference only',
    'documentSha256': hashlib.sha256(raw).hexdigest(),
    'harnessCorrection': 'p02 asked the wrong relation; corrected here. Reviewer error, not a product defect.',
    'cases': rows,
    'unannotatedGovernedFieldsInRealDocument': unannotated,
    'thirdLimbConsumerSearch': consumers,
}
print(json.dumps(out, indent=1))
