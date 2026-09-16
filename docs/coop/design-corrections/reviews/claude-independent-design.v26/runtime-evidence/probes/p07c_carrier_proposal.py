"""Probe 07c — place exactly the proposal-overlay documents the carrier validator names,
all taken hash-verified from the frozen snapshot, then run the pinned validator."""
import hashlib, json, os, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v26'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v26/disposable/carrier-runtime'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
PY = '/tmp/opensip-architecture-review-env/bin/python'
man = {r['path']: r for r in json.load(open(MAN))['files']}
prop = os.path.join(BASE, 'scratch', 'proposal')

EXTRA = [
    'docs/v2/architecture/attempt-custody.schema.v1.json',
    'docs/v2/architecture/carrier-fault-cases.v1.json',
    'docs/v2/architecture/commit-recovery-readonly.v3.md',
]
for rel in EXTRA:
    s = os.path.join(SRC, rel)
    if not os.path.isfile(s):
        print('NOT IN FROZEN SUBJECT:', rel)
        continue
    h = hashlib.sha256(open(s, 'rb').read()).hexdigest()
    assert man[rel]['sha256'] == h, rel
    d = os.path.join(prop, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    print('placed verified', rel, h[:16])

rep = '/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/carrier-v3-report.json'
chk = os.path.join(SRC, 'docs/coop/design-corrections/security/check-carrier-v3.py')
r = subprocess.run([PY, '-I', '-B', chk, SRC, BASE, rep], capture_output=True, text=True, timeout=1800)
print('rc=', r.returncode, 'out=', len(r.stdout), 'err=', len(r.stderr))
print(r.stdout[-3000:])
if r.stderr:
    print('--- stderr ---')
    print(r.stderr[-2000:])
