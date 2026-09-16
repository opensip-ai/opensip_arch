"""PROBE 09 (v31) — run the native checker on frozen31 and prove its digest-law enforcement is
real by mutation in a disposable verified copy:
  (a) frozen run must pass and must REPORT the measured annotation site count (siteCountLaw);
  (b) introducing an UNDECLARED retention value must make it fail and name the offending path;
  (c) removing the `derived` catalog entry (leaving the 3 uses) must also fail.
Frozen bytes are never written.
"""
import hashlib, json, os, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/nativekit')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
CHK = 'docs/coop/design-corrections/native/check_native_evidence.v2.py'
SCH = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
R = {}


def run(root, label):
    p = os.path.join(root, CHK)
    r = subprocess.run([PY, '-I', '-B', p], capture_output=True, text=True,
                       cwd=os.path.dirname(p), timeout=3600)
    out = {'returncode': r.returncode, 'stdoutBytes': len(r.stdout)}
    try:
        rep = json.loads(r.stdout)
        out['passed'] = rep.get('passed')
        out['digestLaw'] = rep.get('digestLaw')
    except Exception:
        out['stdoutTail'] = (r.stdout or '')[-800:]
    out['stderrTail'] = (r.stderr or '')[-900:]
    print('\n=== %s : rc=%d ===' % (label, r.returncode))
    print('   passed   :', out.get('passed'))
    print('   digestLaw:', json.dumps(out.get('digestLaw'))[:400])
    if r.returncode and out.get('stderrTail'):
        print('   stderr   :', out['stderrTail'][-500:])
    return out


R['frozen'] = run(SRC, 'check_native_evidence.v2.py on FROZEN31')
R['frozenReportsMeasuredSiteCount'] = (R['frozen'].get('digestLaw') or {}).get('annotationSites')
R['measuredSiteCountIs76'] = R['frozenReportsMeasuredSiteCount'] == 76

# ---- disposable verified copy ----
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
R['disposableCopied'], R['disposableVerified'] = copied, verified
print('\ndisposable copy: %d files, %d byte-equal to frozen' % (copied, verified))
assert copied == verified

ORIG = open(os.path.join(KIT, SCH), encoding='utf-8').read()

# (b) undeclared retention value at one existing site
mut = ORIG.replace('"retention": "derived",', '"retention": "conjured-from-nowhere",', 1)
assert mut != ORIG
open(os.path.join(KIT, SCH), 'w', encoding='utf-8').write(mut)
R['mutationUndeclaredRetention'] = run(KIT, 'one site given an UNDECLARED retention value')
R['undeclaredRetentionRejected'] = (R['mutationUndeclaredRetention']['returncode'] != 0
                                    or R['mutationUndeclaredRetention'].get('passed') is False)
sites = (R['mutationUndeclaredRetention'].get('digestLaw') or {}).get('undeclaredRetentionSites')
R['undeclaredRetentionNamedPaths'] = sites
print('   undeclared retention rejected:', R['undeclaredRetentionRejected'], '| named:', sites)

# (c) remove the `derived` catalog entry while its 3 uses remain
open(os.path.join(KIT, SCH), 'w', encoding='utf-8').write(ORIG)
sch = json.loads(ORIG)
del sch['x-opensip-digest-law']['retention']['derived']
open(os.path.join(KIT, SCH), 'w', encoding='utf-8').write(json.dumps(sch, indent=2) + '\n')
R['mutationCatalogEntryRemoved'] = run(KIT, '`derived` REMOVED from the catalog, 3 uses remain')
R['catalogRemovalRejected'] = (R['mutationCatalogEntryRemoved']['returncode'] != 0
                               or R['mutationCatalogEntryRemoved'].get('passed') is False)
s2 = (R['mutationCatalogEntryRemoved'].get('digestLaw') or {}).get('undeclaredRetentionSites')
R['catalogRemovalNamedPaths'] = s2
print('   catalog removal rejected:', R['catalogRemovalRejected'], '| named:', s2)

# ---- frozen untouched ----
dev = 0
for rel, f in man.items():
    q = os.path.join(SRC, rel)
    if not os.path.isfile(q) or os.path.getsize(q) != f['bytes'] or \
       hashlib.sha256(open(q, 'rb').read()).hexdigest() != f['sha256']:
        dev += 1
R['frozenDeviationsAfterProbe'] = dev
print('\nfrozen snapshot deviations after this probe:', dev)
json.dump(R, open(os.path.join(OUT, 'p09-nativechecker.json'), 'w'), indent=1)
print('wrote p09-nativechecker.json')
