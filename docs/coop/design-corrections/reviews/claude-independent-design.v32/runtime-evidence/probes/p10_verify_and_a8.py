"""P10 — (a) execute the package verifier against frozen32 (13 outcomes + 7 query checks);
(b) inspect the A-8 evidence bundle myself: is the 29->30 native-cases difference exactly one
64-hex value, and is the failed source29 receipt preserved as a failure?"""
import hashlib, json, os, shutil, subprocess

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v8'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v32'
OUT = os.path.join(BASE, 'receipts')
WORK = os.path.join(BASE, 'disposable/verify8')
PY = '/tmp/opensip-architecture-review-env/bin/python'
BUND = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
        'independent31-advisory8-evidence.v1')
R = {}

if os.path.isdir(WORK):
    shutil.rmtree(WORK)
r = subprocess.run([PY, '-I', '-B', os.path.join(PKG, 'verify-package.py'),
                    '--source', SRC, '--out', WORK], capture_output=True, text=True, timeout=5400)
R['verifier'] = {'returncode': r.returncode, 'stdout': r.stdout[-900:],
                 'stderrTail': (r.stderr or '')[-900:]}
print('verify-package.py rc=%d' % r.returncode)
print(r.stdout[-700:])
vp = os.path.join(WORK, 'verification.json')
if os.path.isfile(vp):
    v = json.load(open(vp))
    R['verification'] = v
    print('passed=%s sourceFiles=%s packageFiles=%s'
          % (v.get('passed'), v.get('sourceFilesVerified'), v.get('packageFilesVerified')))
    for g in v.get('groups', []):
        print('   %-26s passed=%-5s count=%s' % (g['group'], g['passed'], g['count']))
    R['queryChecks'] = next((g['count'] for g in v['groups'] if g['group'] == 'query'), None)
    R['thirteenOutcomes'] = sum(g['count'] for g in v['groups'] if g['group'] != 'query')

# ---------- (b) A-8 bundle ----------
print('\n--- A-8 evidence bundle ---')
c29 = os.path.join(BUND, 'native-cases.source29.json')
c30 = os.path.join(BUND, 'native-cases.source30.json')
b29, b30 = open(c29, 'rb').read(), open(c30, 'rb').read()
R['a8'] = {'sha29': hashlib.sha256(b29).hexdigest(), 'sha30': hashlib.sha256(b30).hexdigest(),
           'bytes29': len(b29), 'bytes30': len(b30), 'sameByteCount': len(b29) == len(b30)}
j29, j30 = json.loads(b29), json.loads(b30)


def flat(o, p='$', acc=None):
    acc = {} if acc is None else acc
    if isinstance(o, dict):
        for k, v in o.items():
            flat(v, p + '/' + k, acc)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            flat(v, p + '/%d' % i, acc)
    else:
        acc[p] = o
    return acc


f29, f30 = flat(j29), flat(j30)
diff = {k: (f29.get(k), f30.get(k)) for k in set(f29) | set(f30) if f29.get(k) != f30.get(k)}
R['a8']['differingLeaves'] = len(diff)
R['a8']['differences'] = {k: {'source29': v[0], 'source30': v[1]} for k, v in list(diff.items())[:5]}
import re
R['a8']['allDifferencesAre64Hex'] = all(
    isinstance(v[0], str) and isinstance(v[1], str)
    and re.fullmatch(r'[0-9a-f]{64}', v[0]) and re.fullmatch(r'[0-9a-f]{64}', v[1])
    for v in diff.values())
R['a8']['exactlyOneReplacement'] = len(diff) == 1
print('native-cases 29 vs 30: same byte count=%s, differing leaves=%d, all 64-hex=%s'
      % (R['a8']['sameByteCount'], len(diff), R['a8']['allDifferencesAre64Hex']))
for k, v in R['a8']['differences'].items():
    print('   %s' % k)
    print('      29: %s' % v['source29'])
    print('      30: %s' % v['source30'])

# do the bundled manifests bind these bytes?
for v, path in (('29', c29), ('30', c30)):
    mp = os.path.join(BUND, 'candidate-subject.v%s.json' % v)
    mm = {f['path']: f for f in json.load(open(mp))['files']}
    key = 'docs/coop/design-corrections/native/native-cases.v2.json'
    R['a8']['manifest%sBindsTheseBytes' % v] = (
        mm.get(key, {}).get('sha256') == hashlib.sha256(open(path, 'rb').read()).hexdigest())
print('manifest-bound: 29=%s 30=%s' % (R['a8']['manifest29BindsTheseBytes'],
                                       R['a8']['manifest30BindsTheseBytes']))

# the failed source29 receipt, preserved as a failure
fr = os.path.join(BUND, 'failed-source29', 'report.json')
rep = json.load(open(fr))
R['a8']['failedReceiptTopKeys'] = sorted(rep) if isinstance(rep, dict) else '<list>'
txt = json.dumps(rep)
R['a8']['failedReceiptRecordsFailure'] = ('"passed": false' in txt.lower().replace(' ', ' ')
                                          or '"failed"' in txt or 'FAIL' in txt)
for k in ('passed', 'result', 'failed', 'status'):
    if isinstance(rep, dict) and k in rep:
        R['a8']['failedReceipt_' + k] = rep[k] if not isinstance(rep[k], (list, dict)) else len(rep[k])
fo = os.path.join(BUND, 'failed-source29', 'foundation.json')
if os.path.isfile(fo):
    f = json.load(open(fo))
    for k in ('passed', 'failed', 'status', 'result'):
        if k in f:
            R['a8']['failedFoundation_' + k] = f[k] if not isinstance(f[k], (list, dict)) else f[k]
print('\nfailed source29 receipt keys:', R['a8']['failedReceiptTopKeys'])
print('receipt records a failure   :', {k: v for k, v in R['a8'].items() if k.startswith('failed')})
sd = open(os.path.join(BUND, 'failed-source29', 'foundation.stdout'), encoding='utf-8').read()
R['a8']['failedStdout'] = sd.strip()[:400]
print('failed stdout:', sd.strip()[:300])

json.dump(R, open(os.path.join(OUT, 'p10-verify-a8.json'), 'w'), indent=1, default=str)
print('\nwrote p10-verify-a8.json')
