"""PROBE 09b (v31) — corrects p09.

Two faults in p09: (1) it ran a REPORT-WRITING checker against the frozen tree (the bytes happened
to be identical so the snapshot did not drift, but a report writer belongs in the disposable copy);
(2) it treated rc=2 as enforcement without reading stderr, which is the same mistake I caught in
p06. Here every run is in a verified disposable copy, the report FILE is read, and each non-zero
exit must be attributed to the digest-law vocabulary check before it counts.
"""
import hashlib, json, os, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/nativekit2')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
CHK = 'docs/coop/design-corrections/native/check_native_evidence.v2.py'
SCH = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
REP = 'docs/coop/design-corrections/native/native-evidence-report.v2.json'
R = {'corrects': 'p09 ran a report writer against the frozen tree and read rc without stderr'}

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
assert copied == verified
print('disposable copy: %d files all byte-equal to frozen' % copied)


def run(label):
    p = os.path.join(KIT, CHK)
    r = subprocess.run([PY, '-I', '-B', p], capture_output=True, text=True,
                       cwd=os.path.dirname(p), timeout=3600)
    o = {'returncode': r.returncode,
         'stdoutTail': (r.stdout or '')[-700:], 'stderrTail': (r.stderr or '')[-900:]}
    rp = os.path.join(KIT, REP)
    if os.path.isfile(rp):
        rep = json.load(open(rp))
        o['result'] = rep.get('result')
        o['digestLaw'] = rep.get('digestLaw')
    o['exitIsCleanFailNotCrash'] = r.returncode in (0, 1)
    o['digestLawNamedTheFault'] = bool(
        o.get('digestLaw', {}).get('undeclaredRetentionSites')
        or o.get('digestLaw', {}).get('undeclaredRepresentationSites')) if o.get('digestLaw') else False
    print('\n=== %s : rc=%d ===' % (label, r.returncode))
    print('   result    :', o.get('result'))
    print('   digestLaw :', json.dumps(o.get('digestLaw'))[:420])
    print('   stdout    :', (r.stdout or '').strip().splitlines()[-2:] if r.stdout else '')
    if r.returncode not in (0, 1):
        print('   STDERR (exit not a clean FAIL):', o['stderrTail'][-600:])
    return o


ORIG = open(os.path.join(KIT, SCH), encoding='utf-8').read()
R['baseline'] = run('frozen bytes, inside the disposable copy')
dl = R['baseline'].get('digestLaw') or {}
R['measuredAnnotationSites'] = dl.get('annotationSites')
R['measuredSiteCountIs76'] = dl.get('annotationSites') == 76
R['baselineNoUndeclared'] = not dl.get('undeclaredRetentionSites') and not dl.get('undeclaredRepresentationSites')
print('\nmeasured annotationSites = %s (76: %s), baseline clean: %s'
      % (R['measuredAnnotationSites'], R['measuredSiteCountIs76'], R['baselineNoUndeclared']))

for label, mutate in (
    ('undeclared RETENTION value at one site',
     lambda t: t.replace('"retention": "derived",', '"retention": "conjured-from-nowhere",', 1)),
    ('undeclared REPRESENTATION value at one site',
     lambda t: t.replace('"representation": "h-identity",', '"representation": "invented-rep",', 1)),
):
    open(os.path.join(KIT, SCH), 'w', encoding='utf-8').write(mutate(ORIG))
    key = label.split()[1].lower()
    R['mutation_' + key] = run(label)
    o = R['mutation_' + key]
    R['rejected_' + key] = (o.get('result') == 'FAIL' and o['exitIsCleanFailNotCrash']
                            and o['digestLawNamedTheFault'])
    print('   -> rejected as a clean digest-law FAIL naming the site:', R['rejected_' + key])

# catalog entry removed while its 3 uses remain
open(os.path.join(KIT, SCH), 'w', encoding='utf-8').write(ORIG)
sch = json.loads(ORIG)
del sch['x-opensip-digest-law']['retention']['derived']
open(os.path.join(KIT, SCH), 'w', encoding='utf-8').write(json.dumps(sch, indent=2) + '\n')
R['mutation_catalogRemoval'] = run('`derived` removed from the catalog, its 3 uses remain')
o = R['mutation_catalogRemoval']
R['rejected_catalogRemoval'] = (o.get('result') == 'FAIL' and o['exitIsCleanFailNotCrash']
                                and o['digestLawNamedTheFault'])
print('   -> rejected as a clean digest-law FAIL naming the 3 sites:', R['rejected_catalogRemoval'])

dev = 0
for rel, f in man.items():
    q = os.path.join(SRC, rel)
    if not os.path.isfile(q) or os.path.getsize(q) != f['bytes'] or \
       hashlib.sha256(open(q, 'rb').read()).hexdigest() != f['sha256']:
        dev += 1
R['frozenDeviationsAfterProbe'] = dev
print('\nfrozen snapshot deviations:', dev)
json.dump(R, open(os.path.join(OUT, 'p09b-nativechecker.json'), 'w'), indent=1)
print('wrote p09b-nativechecker.json')
