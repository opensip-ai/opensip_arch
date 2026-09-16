"""PROBE H (v27) — remaining contract/reference groups on snapshot27.

Report-writing checkers run inside a disposable copy whose every byte I verify against the
frozen manifest first; the frozen snapshot is re-measured unchanged afterwards. Pin gates
are satisfied with frozen bytes, never bypassed."""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v27.json'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v27'
KIT = os.path.join(BASE, 'disposable/kit')
OUT = os.path.join(BASE, 'receipts')
PY = '/tmp/opensip-architecture-review-env/bin/python'
os.makedirs(OUT, exist_ok=True)
man = {r['path']: r for r in json.load(open(MAN))['files']}

# ---- build the disposable copy: all of docs/ except the huge historical reviews tree,
# ---- plus exactly the pinned review files the gates require
EXCL = 'docs/coop/design-corrections/reviews/'
NEED = [EXCL + n for n in ('native-author-feedback.v1.md', 'security-author-feedback.v1.md',
                           'workflows-author-feedback.v1.md')]
if os.path.isdir(KIT):
    shutil.rmtree(KIT)
copied = 0
for dp, dn, fn in os.walk(os.path.join(SRC, 'docs')):
    for f in fn:
        s = os.path.join(dp, f)
        rel = os.path.relpath(s, SRC)
        if rel.startswith(EXCL) and rel not in NEED:
            continue
        d = os.path.join(KIT, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        copied += 1
bad = ver = 0
for dp, dn, fn in os.walk(KIT):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, KIT)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        rec = man.get(rel)
        if rec is None or rec['sha256'] != h or rec['bytes'] != os.path.getsize(p):
            bad += 1
        else:
            ver += 1
print('disposable copy: copied=%d verifiedAgainstFrozen27=%d mismatches=%d' % (copied, ver, bad))
assert bad == 0, 'disposable copy not byte-equal to frozen27'

DCK = os.path.join(KIT, 'docs/coop/design-corrections')
JOBS = [
    ('foundation/check-identity.py', ['--report', OUT + '/identity27.json']),
    ('foundation/check-array-orders.py', ['--report', OUT + '/array-orders27.json']),
    ('foundation/check-foundation.py', ['--report', OUT + '/foundation27.json']),
    ('foundation/check-product-configuration.py', ['--report', OUT + '/product-config27.json']),
    ('foundation/check-product-quality.py', ['--report', OUT + '/product-quality27.json']),
    ('native/check_native_evidence.v2.py', []),
    ('workflows/check_workflows.v1.py', ['--report', OUT + '/workflows27.json']),
    ('security/check-security-lifecycle.v1.py', ['--report', OUT + '/security27.json']),
    ('security/check-analysis-seal-adapter.v1.py', []),
    ('security/check-integrated-carrier.v1.py', ['--source', SRC, '--report', OUT + '/integrated-carrier27.json']),
    ('check-integration.py', ['--report', OUT + '/integration27.json']),
]
rows = []
for rel, args in JOBS:
    p = os.path.join(DCK, rel)
    t0 = time.time()
    r = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True,
                       cwd=os.path.dirname(p), timeout=3600)
    tail = (r.stdout or '').strip().splitlines()[-1:] or ['']
    rows.append({'checker': rel, 'returncode': r.returncode, 'seconds': round(time.time() - t0, 1),
                 'lastLine': tail[0][-220:], 'stderrTail': (r.stderr or '')[-400:] if r.returncode else ''})
    print('%-52s rc=%-3d %6.1fs  %s' % (rel, r.returncode, time.time() - t0, tail[0][-150:]))
    if r.returncode:
        print('   STDERR:', (r.stderr or '')[-700:])

# planning checkers in --check mode only
for name, args in (('check_repository_file_inventory.py', ['--check']),
                   ('check_implementation_planning.py', ['--source', SRC, '--check'])):
    p = os.path.join(KIT, 'docs/operations', name)
    r = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True,
                       cwd=KIT, timeout=1800)
    tail = (r.stdout or '').strip().splitlines()[-1:] or ['']
    rows.append({'checker': 'operations/' + name, 'returncode': r.returncode,
                 'lastLine': tail[0][-220:]})
    print('%-52s rc=%-3d        %s' % ('operations/' + name, r.returncode, tail[0][-150:]))

# frozen snapshot must still be byte-identical
dev = 0
for rel, rec in man.items():
    p = os.path.join(SRC, rel)
    if not os.path.isfile(p) or os.path.getsize(p) != rec['bytes']:
        dev += 1
        continue
    if hashlib.sha256(open(p, 'rb').read()).hexdigest() != rec['sha256']:
        dev += 1
print('\nfrozen snapshot27 deviations after all runs:', dev)
json.dump({'disposableCopyVerified': ver, 'mismatches': bad, 'jobs': rows,
           'frozenDeviationsAfterRuns': dev},
          open(os.path.join(OUT, 'pH-groups27.json'), 'w'), indent=1)
