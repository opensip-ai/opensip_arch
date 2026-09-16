"""PROBE 06 (v31) — execute the source28 ruleResults order correction on ACTUAL source, then
establish that the new branch is LOAD-BEARING by omitting it in a disposable verified copy.

Reproducing the regression, not restating root's claim:
  (a) run check-replay.v3.py against frozen31 -> must pass;
  (b) in a disposable copy whose every byte I verified against the frozen manifest, delete the
      `ruleResults` branch from identity-model.v3.ordered so it falls back to generic canonical
      member order, and re-run. If the correct-order positive then refuses, the branch is
      load-bearing and the pre-28 behaviour is reproduced.
Frozen bytes are never written.
"""
import hashlib, json, os, re, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/orderkit')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {}

CHK = 'docs/coop/design-corrections/foundation/check-replay.v3.py'

# ---------- (a) frozen run ----------
p = os.path.join(SRC, CHK)
r = subprocess.run([PY, '-I', '-B', p], capture_output=True, text=True,
                   cwd=os.path.dirname(p), timeout=3600)
R['frozenRun'] = {'returncode': r.returncode, 'stdoutTail': (r.stdout or '')[-2500:],
                  'stderrTail': (r.stderr or '')[-1500:]}
print('=== check-replay.v3.py on FROZEN31 : rc=%d ===' % r.returncode)
print((r.stdout or '')[-2500:])
if r.returncode:
    print('--- stderr ---')
    print((r.stderr or '')[-2000:])

# ---------- (b) disposable copy with the branch omitted ----------
if os.path.isdir(KIT):
    shutil.rmtree(KIT)
# FIRST RUN WAS WRONG: I copied only the foundation/native/workflows/security subdirectories, so
# docs/coop/design-corrections/discovery-defaults.py (a TOP-LEVEL member of that tree) was absent and
# the mutated run died with FileNotFoundError. That failure was my incomplete copy, not the mutation,
# and it made branchIsLoadBearing a false positive. The first run is preserved in the receipts.
# Correct rule: take the whole design-corrections tree except the large historical reviews subtree.
# SECOND RUN ALSO INCOMPLETE: docs/coop/artifacts/delivery.v4.json was still absent. Both partial
# copies are preserved. Correct rule: the whole docs/ tree minus the large historical reviews subtree.
need = set()
for rel in man:
    if rel.startswith('docs/') and not rel.startswith('docs/coop/design-corrections/reviews/'):
        need.add(rel)
copied = verified = 0
for rel in sorted(need):
    s = os.path.join(SRC, rel)
    if not os.path.isfile(s):
        continue
    d = os.path.join(KIT, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    copied += 1
    if hashlib.sha256(open(d, 'rb').read()).hexdigest() == man[rel]['sha256']:
        verified += 1
R['disposableCopied'] = copied
R['disposableVerifiedAgainstFrozen'] = verified
R['disposableAllVerified'] = copied == verified
print('\ndisposable copy: %d files, %d byte-equal to frozen manifest' % (copied, verified))
assert copied == verified

IM = os.path.join(KIT, 'docs/coop/design-corrections/foundation/identity-model.v3.py')
txt = open(IM, encoding='utf-8').read()
BRANCH = "        elif name=='ruleResults':keys=[v['ruleId'].encode('utf8') for v in value]\n"
R['branchPresentInFrozen'] = BRANCH in txt
print('ruleResults branch present in frozen bytes:', R['branchPresentInFrozen'])
assert R['branchPresentInFrozen'], 'exact branch line not found; aborting rather than guessing'
open(IM, 'w', encoding='utf-8').write(txt.replace(BRANCH, ''))
R['mutation'] = ('removed the single ruleResults branch line so the array falls through to the '
                 'generic canonical-member order, reproducing the pre-source28 reference behaviour')
print('mutation applied:', R['mutation'])

p2 = os.path.join(KIT, CHK)
r2 = subprocess.run([PY, '-I', '-B', p2], capture_output=True, text=True,
                    cwd=os.path.dirname(p2), timeout=3600)
R['mutatedRun'] = {'returncode': r2.returncode, 'stdoutTail': (r2.stdout or '')[-1500:],
                   'stderrTail': (r2.stderr or '')[-2500:]}
print('\n=== same checker with the branch OMITTED : rc=%d ===' % r2.returncode)
print((r2.stdout or '')[-1200:])
if r2.returncode:
    print('--- stderr (the reproduced regression) ---')
    print((r2.stderr or '')[-2500:])
stderr2 = r2.stderr or ''
# A non-zero exit is only evidence if it comes from the ORDER law, not from a broken copy.
R['mutatedFailedForEnvironmentReason'] = bool(
    re.search(r'FileNotFoundError|ModuleNotFoundError|ImportError', stderr2))
R['mutatedFailedOnOrderLaw'] = bool(
    re.search(r'ORDER_OR_DUPLICATE|ruleResults|ordering|AssertionError', stderr2))
R['branchIsLoadBearing'] = (r.returncode == 0 and r2.returncode != 0
                            and R['mutatedFailedOnOrderLaw']
                            and not R['mutatedFailedForEnvironmentReason'])
R['firstRunWasAFalsePositive'] = (
    'My first run reported branchIsLoadBearing=True from a FileNotFoundError caused by my own '
    'incomplete disposable copy (discovery-defaults.py omitted). That run is preserved; this '
    'result only counts a failure that names the order law.')
print('\nmutated failed for environment reason :', R['mutatedFailedForEnvironmentReason'])
print('mutated failed on the order law       :', R['mutatedFailedOnOrderLaw'])
print('frozen passes and omission fails on the LAW => branch load-bearing:',
      R['branchIsLoadBearing'])

# ---------- frozen snapshot untouched ----------
dev = 0
for rel, f in man.items():
    q = os.path.join(SRC, rel)
    if not os.path.isfile(q) or os.path.getsize(q) != f['bytes']:
        dev += 1
        continue
    if hashlib.sha256(open(q, 'rb').read()).hexdigest() != f['sha256']:
        dev += 1
R['frozenDeviationsAfterProbe'] = dev
print('frozen snapshot deviations after this probe:', dev)
json.dump(R, open(os.path.join(OUT, 'p06-replayorder.json'), 'w'), indent=1)
print('\nwrote p06-replayorder.json')
