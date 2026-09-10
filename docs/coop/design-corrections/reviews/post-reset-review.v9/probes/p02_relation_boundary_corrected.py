"""v9 probe 02 - corrected relation payload boundary sweep + LIVE enforcement tests.

Corrects two harness assumptions in p01 (reviewer error, NOT product defects):
  (a) bodyIdentityJoin binds its field under the key 'field', not '*Field';
  (b) the not-joined reason for previousPath is stated under 'join', not 'reason'/'note'.

Then goes past declaration to enforcement: exercises relation_annotation_closure on
hypothetical mutated documents to see whether the residue rule is actually consumed,
and confirms the mutation is not made to the real module state.

Design/reference only. Qualifies nothing.
"""
import json, hashlib, copy, sys
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v9')
FOUND = SUB / 'docs/coop/design-corrections/foundation'
sys.path.insert(0, str(FOUND))
import importlib.util
spec = importlib.util.spec_from_file_location('identity_model_v9', FOUND / 'identity-model.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

raw = (FOUND / 'relation-payload-schemas.v2.json').read_bytes()
d = json.loads(raw)
reg = d['x-opensip-relation-registry']
rels = reg['relations']

# ---- (1) $ref-based enumeration: authoritative, not pattern guessing.
GOVERNED_REFS = {'DigestHex', 'Sha256Text', 'CanonicalPath'}
payload_def_of = {}
for rname, row in rels.items():
    sel = row.get('selector') or ''
    if sel.startswith('#/$defs/'):
        payload_def_of[sel.split('/')[-1]] = rname

def ref_name(p):
    r = p.get('$ref') or ''
    return r.split('/')[-1] if r.startswith('#/$defs/') else None

fields = []
for defname, node in sorted(d['$defs'].items()):
    rname = payload_def_of.get(defname)
    if rname is None:
        continue
    for pname, p in sorted((node.get('properties') or {}).items()):
        rn = ref_name(p)
        if rn not in GOVERNED_REFS:
            continue
        ann = p.get('x-opensip-digest')
        row = rels[rname]
        joined = []
        for j in (row.get('snapshotJoins') or []):
            for k, v in j.items():
                if isinstance(v, str) and v == pname and k != 'form':
                    joined.append({'join': j.get('form'), 'role': k})
        bij = row.get('bodyIdentityJoin')
        if bij:
            for k, v in bij.items():
                if isinstance(v, str) and v == pname:
                    joined.append({'join': 'bodyIdentityJoin', 'role': k})
        retention = (ann or {}).get('retention')
        has_reason = bool((ann or {}).get('join') or (ann or {}).get('reason'))
        if not ann:
            cls = 'UNGOVERNED-unannotated'
        elif joined:
            cls = 'joined'
        elif retention == 'not-joined' and has_reason:
            cls = 'declared-not-joined-with-stated-reason'
        else:
            cls = 'UNGOVERNED-annotated-but-unjoined'
        fields.append({'relation': rname, 'def': defname, 'field': pname, 'ref': rn,
                       'retention': retention, 'joinedBy': joined, 'classification': cls,
                       'authority': (ann or {}).get('authority')})

# ---- (2) Is the residue rule CONSUMED? Exercise the closure on hypothetical documents.
enforcement = []

def try_closure(label, mutate, expect_token):
    doc = copy.deepcopy(d)
    mutate(doc)
    try:
        M.relation_annotation_closure('clones', document=doc)
        got = None
    except Exception as e:
        got = str(e)
    enforcement.append({'case': label, 'raised': got, 'expectToken': expect_token,
                        'reachedIntendedCause': bool(got and expect_token in got)})

def add_annotated_unjoined(doc):
    doc['$defs']['FilePayloadV1']['properties']['strayDigest'] = {
        '$ref': '#/$defs/DigestHex',
        'x-opensip-digest': {'representation': 'raw-artifact', 'retention': 'preimage',
                             'authority': 'test', 'codec': 'test'}}

def add_unannotated_digest(doc):
    doc['$defs']['FilePayloadV1']['properties']['strayBare'] = {'$ref': '#/$defs/DigestHex'}

def join_names_missing_field(doc):
    doc['x-opensip-relation-registry']['relations']['file']['snapshotJoins'][0]['digestField'] = 'noSuchField'

try_closure('annotated-field-with-no-join', add_annotated_unjoined, 'RELATION_DIGEST_LAW_RESIDUE')
try_closure('unannotated-digest-field', add_unannotated_digest, 'RELATION_')
try_closure('join-names-field-selector-lacks', join_names_missing_field, 'RELATION_JOIN_FIELD_UNKNOWN')

# positive control: the real document must pass for every relation
positives = {}
for rname in sorted(rels):
    try:
        M.relation_annotation_closure(rname)
        positives[rname] = 'PASS'
    except Exception as e:
        positives[rname] = 'REFUSED:' + str(e)

# ---- (3) purity: did the hypothetical mutations leak into module state?
leak = None
try:
    M.relation_annotation_closure('file')
    leak = 'module-state-clean'
except Exception as e:
    leak = 'MODULE-STATE-POISONED:' + str(e)

out = {
    'probe': 'p02_relation_boundary_corrected',
    'standing': 'independent reviewer probe; design/reference only; qualifies nothing',
    'documentSha256': hashlib.sha256(raw).hexdigest(),
    'harnessCorrections': [
        'p01 classified bodyIdentity as unjoined because bodyIdentityJoin uses key "field"; reviewer harness bug, not a product defect',
        'p01 classified previousPath as reasonless because the reason is stated under "join"; reviewer harness bug, not a product defect',
    ],
    'governedFields': fields,
    'ungovernedAfterCorrection': [f for f in fields if f['classification'].startswith('UNGOVERNED')],
    'residueEnforcement': enforcement,
    'positiveClosurePerRelation': positives,
    'modulePurityAfterHypotheticals': leak,
}
print(json.dumps(out, indent=1))
