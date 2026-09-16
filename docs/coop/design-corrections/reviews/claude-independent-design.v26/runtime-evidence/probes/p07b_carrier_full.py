"""Probe 07b — supply the remaining runtime-root inputs the carrier validator expects,
taking each from the FROZEN snapshot's current integrated bytes (hash-verified),
then run the pinned validator."""
import hashlib, json, os, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v26'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v26/disposable/carrier-runtime'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
PY = '/tmp/opensip-architecture-review-env/bin/python'
man = {r['path']: r for r in json.load(open(MAN))['files']}

patched = os.path.join(BASE, 'scratch', 'patched')
os.makedirs(patched, exist_ok=True)
for rel in ['docs/v2/architecture/commit-recovery-plan.v1.json',
            'docs/v2/architecture/implementation-boundaries-and-build-plan.md',
            'docs/v2/contracts/product-v1/identity-and-evidence.md',
            'docs/v2/contracts/product-v1/security-and-lifecycle.md']:
    s = os.path.join(SRC, rel)
    h = hashlib.sha256(open(s, 'rb').read()).hexdigest()
    assert man[rel]['sha256'] == h, rel
    shutil.copy2(s, os.path.join(patched, os.path.basename(rel)))
    print('placed verified', os.path.basename(rel), h[:16])

rep = '/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/carrier-v3-report.json'
chk = os.path.join(SRC, 'docs/coop/design-corrections/security/check-carrier-v3.py')
r = subprocess.run([PY, '-I', '-B', chk, SRC, BASE, rep], capture_output=True, text=True, timeout=1800)
print('rc=', r.returncode, 'out=', len(r.stdout), 'err=', len(r.stderr))
print(r.stdout[-3000:])
if r.stderr:
    print('--- stderr ---')
    print(r.stderr[-2000:])
