"""PROBE 19 (v31) — independently reproduce the current relevant reference suites on source31:
the source-pinned evaluator3 launcher (16 children) and the contract/reference groups.

Report writers run inside a disposable copy whose every byte I verified against the frozen
manifest; the frozen snapshot is re-measured unchanged afterwards. Pin gates are satisfied with
frozen bytes, never bypassed. Also measures rg availability for the RES-EP13-11 correction.
"""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/suites')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {}

# ---------- evaluator3 launcher against the FROZEN tree (stdout/receipt into my own dir) ----------
L = os.path.join(SRC, 'docs/coop/design-corrections/foundation/run-evaluator3-checks.py')
LED = os.path.join(SRC, 'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json')
R['launcherSha256'] = hashlib.sha256(open(L, 'rb').read()).hexdigest()
R['pinLedgerSha256'] = hashlib.sha256(open(LED, 'rb').read()).hexdigest()
R['pinnedFiles'] = len(json.load(open(LED))['files'])
LOUT = os.path.join(OUT, 'evaluator3-launcher31')
if os.path.isdir(LOUT):
    shutil.rmtree(LOUT)
t0 = time.time()
r = subprocess.run([PY, '-I', '-B', L, '--out', LOUT], capture_output=True, text=True, timeout=7200)
R['launcher'] = {'returncode': r.returncode, 'seconds': round(time.time() - t0, 1),
                 'stdoutTail': (r.stdout or '')[-1200:], 'stderrTail': (r.stderr or '')[-900:]}
print('evaluator3 launcher rc=%d (%.0fs), pin ledger rows=%d'
      % (r.returncode, time.time() - t0, R['pinnedFiles']))
rep = os.path.join(LOUT, 'report.json')
if os.path.isfile(rep):
    d = json.load(open(rep))
    R['launcherReport'] = {'sourcePinsValid': d.get('sourcePinsValid'), 'passed': d.get('passed'),
                           'changedOrMissing': len(d.get('changedOrMissing', [])),
                           'checks': len(d.get('checks', [])),
                           'allExitZero': all(c.get('exitCode') == 0 for c in d.get('checks', []))}
    print('   sourcePinsValid=%s passed=%s changedOrMissing=%d children=%d allExitZero=%s'
          % (d.get('sourcePinsValid'), d.get('passed'), len(d.get('changedOrMissing', [])),
             len(d.get('checks', [])), R['launcherReport']['allExitZero']))
    for c in d.get('checks', []):
        if c.get('exitCode') != 0:
            print('   NONZERO:', c.get('name'), c.get('exitCode'))

# ---------- disposable copy for report-writing group checkers ----------
if os.path.isdir(KIT):
    shutil.rmtree(KIT)
copied = verified = 0
for rel in man:
    if not rel.startswith('docs/') or rel.startswith('docs/coop/design-corrections/reviews/'):
        continue
    s = os.path.join(SRC, rel)
    if not os.path.isfile(s):
        continue
    d = os.path.join(KIT, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    copied += 1
    if hashlib.sha256(open(d, 'rb').read()).hexdigest() == man[rel]['sha256']:
        verified += 1
# the three pinned review feedback files the gates require
EXC = 'docs/coop/design-corrections/reviews/'
for n in ('native-author-feedback.v1.md', 'security-author-feedback.v1.md',
          'workflows-author-feedback.v1.md'):
    rel = EXC + n
    if rel in man:
        s = os.path.join(SRC, rel)
        d = os.path.join(KIT, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        copied += 1
        if hashlib.sha256(open(d, 'rb').read()).hexdigest() == man[rel]['sha256']:
            verified += 1
R['disposableCopied'], R['disposableVerified'] = copied, verified
print('\ndisposable copy: %d files, %d byte-equal to frozen' % (copied, verified))
assert copied == verified

DCK = os.path.join(KIT, 'docs/coop/design-corrections')
JOBS = [
    ('foundation/check-identity.py', ['--report', OUT + '/identity31.json']),
    ('foundation/check-array-orders.py', ['--report', OUT + '/array-orders31.json']),
    ('foundation/check-foundation.py', ['--report', OUT + '/foundation31.json']),
    ('foundation/check-product-configuration.py', ['--report', OUT + '/product-config31.json']),
    ('foundation/check-product-quality.py', ['--report', OUT + '/product-quality31.json']),
    ('native/check_native_evidence.v2.py', []),
    ('workflows/check_workflows.v1.py', ['--report', OUT + '/workflows31.json']),
    ('security/check-security-lifecycle.v1.py', ['--report', OUT + '/security31.json']),
    ('security/check-analysis-seal-adapter.v1.py', []),
    ('security/check-integrated-carrier.v1.py', ['--source', SRC, '--report', OUT + '/carrier31.json']),
    ('check-integration.py', ['--report', OUT + '/integration31.json']),
]
rows = []
for rel, args in JOBS:
    p = os.path.join(DCK, rel)
    t0 = time.time()
    rr = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True,
                        cwd=os.path.dirname(p), timeout=5400)
    tail = (rr.stdout or '').strip().splitlines()[-1:] or ['']
    rows.append({'checker': rel, 'returncode': rr.returncode, 'seconds': round(time.time() - t0, 1),
                 'lastLine': tail[0][-200:],
                 'stderrTail': (rr.stderr or '')[-400:] if rr.returncode else ''})
    print('%-46s rc=%-3d %6.1fs  %s' % (rel, rr.returncode, time.time() - t0, tail[0][-110:]))
    if rr.returncode:
        print('   STDERR:', (rr.stderr or '')[-600:])
R['groups'] = rows
R['allGroupsExitZero'] = all(x['returncode'] == 0 for x in rows)

# ---------- rg availability, for the RES-EP13-11 correction ----------
which = shutil.which('rg')
R['rgOnPath'] = which
if which:
    rr = subprocess.run([which, '--version'], capture_output=True, text=True)
    R['rgVersion'] = (rr.stdout or '').strip().splitlines()[:1]
    R['rgInvocable'] = rr.returncode == 0
else:
    R['rgInvocable'] = False
print('\nrg on PATH: %s | invocable: %s %s' % (which, R['rgInvocable'], R.get('rgVersion')))

dev = sum(1 for rel, f in man.items()
          if not os.path.isfile(os.path.join(SRC, rel))
          or hashlib.sha256(open(os.path.join(SRC, rel), 'rb').read()).hexdigest() != f['sha256'])
R['frozenDeviationsAfterRuns'] = dev
print('frozen snapshot deviations after all runs:', dev)
json.dump(R, open(os.path.join(OUT, 'p19-suites31.json'), 'w'), indent=1, default=str)
print('\nwrote p19-suites31.json')
