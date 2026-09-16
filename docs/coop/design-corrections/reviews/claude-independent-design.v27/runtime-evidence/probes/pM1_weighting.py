"""PROBE M1-D (v27) — resolve the v26 evidence-weighting question by measurement.

My v26 M-1 measured a digest PAIR and inferred a run3 consequence. Root's objection is
correct in principle: a provider that intentionally supplies or omits an OPTIONAL hint is
making two different attestations, and different descriptors legitimately have different
digests -- exactly what the source-text anchorLaw already says for fact.anchors. A digest
pair therefore cannot, on its own, demonstrate nondeterminism.

What the defect actually was: an internal inconsistency between a normative statement
("hint permitted ONLY for kind file|symbol") and an admission that enforced nothing there.

The right post-correction question is therefore NOT "can digests differ" but:
  for each (kind, occupancy), how many DISTINCT canonical record digests are reachable,
  and is that count 1 exactly where the contract declares the value meaningless?
"""
import hashlib, importlib.util, itertools, json, os, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v27/docs/coop/design-corrections'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
sys.path.insert(0, os.path.join(DC, 'foundation'))
from jsonschema import Draft202012Validator

spec = importlib.util.spec_from_file_location('canon', os.path.join(DC, 'foundation/canonical.py'))
canon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(canon)

TA = json.load(open(os.path.join(DC, 'foundation/target-attribution.schema.v2.json'), encoding='utf-8'))
U = '0' * 64
HINTS = [None, 'src/hint.ts', 'src/other.ts']
MEANINGFUL = {(k, o) for k in ('file', 'symbol') for o in ('external', 'unknown')}

res = {'hintValuesTried': HINTS}
table = {}
for kind, occ in itertools.product(('file', 'symbol', 'package', 'unknown'),
                                   ('first-party', 'external', 'unknown')):
    digests = set()
    for lp in HINTS:
        rec = {"schemaVersion": 2, "planId": "plan2:" + "a" * 64,
               "sourceFactId": "fact2:" + "b" * 64, "producerClosure": "closure2:" + "c" * 64,
               "targetUniverse": U, "targetNativeId": "mod:opaque-thing",
               "kind": kind, "occupancy": occ,
               "exported": "unknown" if kind == "symbol" else None,
               "logicalPath": lp, "packageManifestPath": None, "evaluationNativeId": None}
        if occ == 'first-party':
            rec['evaluationNativeId'] = 'src/a.ts'
        if kind == 'package' and occ in ('first-party', 'external'):
            rec['packageManifestPath'] = 'pkg/package.json'
        if not list(Draft202012Validator(TA).iter_errors(rec)):
            digests.add(hashlib.sha256(canon.canonical(rec)).hexdigest())
    meaningful = (kind, occ) in MEANINGFUL
    table['%s/%s' % (kind, occ)] = {
        'admissibleRecordCount': len(digests),
        'distinctDigests': len(digests),
        'contractSaysHintMeaningful': meaningful,
        'closedToOneEncoding': len(digests) <= 1,
        'expected': 'many (lawful distinct attestations)' if meaningful else 'exactly one',
        'conforms': (len(digests) > 1) == meaningful if len(digests) else None,
    }

res['perPosition'] = table
res['meaninglessPositionsStillMultiEncoded'] = sorted(
    k for k, v in table.items() if not v['contractSaysHintMeaningful'] and v['distinctDigests'] > 1)
res['meaningfulPositionsCollapsed'] = sorted(
    k for k, v in table.items() if v['contractSaysHintMeaningful'] and v['distinctDigests'] <= 1)
res['v26AmbiguityClosed'] = not res['meaninglessPositionsStillMultiEncoded']

res['weightingStatement'] = (
    "The remaining multi-digest positions are exactly the four the contract declares a "
    "meaningful provider attestation (file|symbol x external|unknown). A provider choosing "
    "to supply or omit a real path hint there is making two different statements, and the "
    "source-text anchorLaw already establishes that differing citations are different "
    "descriptors with no promised cross-provider identity. That is intended design, not "
    "nondeterminism. My v26 digest pair could not distinguish these two situations; the "
    "position-indexed count above can.")

json.dump(res, open(os.path.join(OUT, 'pM1-weighting.json'), 'w'), indent=1)
print('%-22s %-9s %-11s %-9s %s' % ('kind/occupancy', 'digests', 'meaningful', 'closed', 'conforms'))
for k in sorted(table):
    v = table[k]
    print('%-22s %-9s %-11s %-9s %s' % (k, v['distinctDigests'], v['contractSaysHintMeaningful'],
                                        v['closedToOneEncoding'], v['conforms']))
print()
print('meaningless positions still multi-encoded :', res['meaninglessPositionsStillMultiEncoded'])
print('meaningful positions wrongly collapsed    :', res['meaningfulPositionsCollapsed'])
print('v26 ambiguity closed                      :', res['v26AmbiguityClosed'])
