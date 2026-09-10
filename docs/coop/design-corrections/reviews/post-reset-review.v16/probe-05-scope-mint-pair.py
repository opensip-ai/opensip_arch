#!/usr/bin/env python3
"""Probe 05 (independent): subject_scope_descriptor mint-time (relation, rung)
pair check, over ALL 17 registered pairs (positive controls) and a selected set
of unregistered pairs (negative controls).

Supersedes the mint section of probe-04, whose positive controls failed on MY
harness error (snapshotId lacked the required `snapshot2:` prefix). That failed
attempt is preserved at failed-attempt-01-probe-04-mint-wrong-prefix.result.json.
"""
import hashlib, importlib.util, itertools, json, os, sys

ROOT = '/tmp/opensip-design-corrections/post-reset-review.v16/copy-B-probes'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
DC = os.path.join(ROOT, 'docs/coop/design-corrections')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

spec = importlib.util.spec_from_file_location('rev16_native5', os.path.join(DC, 'native/native_evidence_model.v2.py'))
N = importlib.util.module_from_spec(spec)
sys.modules['rev16_native5'] = N
spec.loader.exec_module(N)

SNAP = 'snapshot2:' + 'a' * 64
UNIV = 'b' * 64
CLOS = 'closure2:' + 'c' * 64

registered = sorted((rel, rung) for rel, l in N.LADDERS.items() for rung in l)
all_rungs = sorted({r for l in N.LADDERS.values() for r in l})

rows = []
def mint(rel, rung, exp, why, subjects=('a.ts',)):
    try:
        d = N.subject_scope_descriptor(SNAP, rel, rung, UNIV, UNIV, CLOS, list(subjects))
        got, err, ident = True, None, N.subject_scope_identity(d)
    except Exception as e:
        got, err, ident = False, type(e).__name__ + ':' + str(e)[:220], None
    rows.append({'pair': f'{rel}@{rung}', 'expectedMint': exp, 'observedMint': got,
                 'agrees': got == exp, 'error': err, 'scopeIdentity': ident, 'why': why})

for rel, rung in registered:
    mint(rel, rung, True, 'registered pair: positive control, must mint')
for rel, rung in itertools.product(sorted(N.LADDERS), all_rungs):
    if (rel, rung) not in registered:
        mint(rel, rung, False, 'unregistered pair: must refuse at mint, never fall back')
# vocabulary-level negatives
mint('unresolved-edge', 'not-a-rung', False, 'rung outside the whole vocabulary')
mint('not-a-relation', 'observed', False, 'relation outside the registry')
# preserved unrelated laws must still fire
try:
    N.subject_scope_descriptor(SNAP, 'unresolved-edge', 'observed', UNIV, UNIV, CLOS, ['a.ts', 'a.ts'])
    dup = 'ADMITTED'
except Exception as e:
    dup = type(e).__name__ + ':' + str(e)[:120]
try:
    N.subject_scope_descriptor(SNAP, 'unresolved-edge', 'observed', UNIV, UNIV, CLOS, 'a.ts')
    typ = 'ADMITTED'
except Exception as e:
    typ = type(e).__name__ + ':' + str(e)[:120]

res = {
    'probe': 'probe-05-scope-mint-pair',
    'copyName': 'copy-B-probes',
    'boundSourceSha256': {'native_evidence_model.v2.py': sha256(os.path.join(DC, 'native/native_evidence_model.v2.py')),
                          'identity-schemas.v2.json': sha256(os.path.join(DC, 'foundation/identity-schemas.v2.json'))},
    'registeredPairCount': len(registered),
    'positiveControls': sum(1 for r in rows if r['expectedMint']),
    'negativeControls': sum(1 for r in rows if not r['expectedMint']),
    'cases': len(rows),
    'agree': sum(1 for r in rows if r['agrees']),
    'disagree': [r for r in rows if not r['agrees']],
    'preservedLaws': {'duplicateSubject': dup, 'nonListSubjects': typ},
    'schemaOnlyConstrainsRelationAsBoundedString': True,
    'rows': rows,
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'probe-05-scope-mint-pair.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, indent=2, sort_keys=True)[:3000])
