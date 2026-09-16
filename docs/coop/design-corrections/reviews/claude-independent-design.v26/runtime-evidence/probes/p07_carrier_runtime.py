"""Probe 07 — reconstruct, from verified frozen bytes only, the runtime root layout
check-carrier-v3.py expects (<runtimeRoot>/scratch/proposal/docs/coop/design-corrections/security),
then run the pinned carrier validator. No frozen byte is modified; the layout is
assembled in the disposable area and every copied file is hash-verified first."""
import hashlib, json, os, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v26'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v26/disposable/carrier-runtime'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
PY = '/tmp/opensip-architecture-review-env/bin/python'
man = {r['path']: r for r in json.load(open(MAN))['files']}

rel_sec = 'docs/coop/design-corrections/security'
dst_sec = os.path.join(BASE, 'scratch', 'proposal', rel_sec)
if os.path.isdir(BASE):
    shutil.rmtree(BASE)
os.makedirs(dst_sec, exist_ok=True)
n = 0
for f in sorted(os.listdir(os.path.join(SRC, rel_sec))):
    s = os.path.join(SRC, rel_sec, f)
    if not os.path.isfile(s):
        continue
    rel = rel_sec + '/' + f
    h = hashlib.sha256(open(s, 'rb').read()).hexdigest()
    assert man[rel]['sha256'] == h, rel
    shutil.copy2(s, os.path.join(dst_sec, f))
    n += 1
print('verified+placed security files:', n)

rep = '/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/carrier-v3-report.json'
chk = os.path.join(SRC, rel_sec, 'check-carrier-v3.py')
r = subprocess.run([PY, '-I', '-B', chk, SRC, BASE, rep], capture_output=True, text=True, timeout=1800)
print('rc=', r.returncode, 'out=', len(r.stdout), 'err=', len(r.stderr))
print(r.stdout[-2500:])
if r.stderr:
    print('--- stderr ---')
    print(r.stderr[-2500:])
