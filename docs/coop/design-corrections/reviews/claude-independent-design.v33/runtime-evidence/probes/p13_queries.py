"""P13 — execute the package verifier against frozen33 for the 7 query checks, and compare my result
with root's named verification (evidence to assess, not authority)."""
import hashlib, json, os, shutil, subprocess

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v10'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
OUT = os.path.join(BASE, 'receipts')
WORK = os.path.join(BASE, 'disposable/verify10')
PY = '/tmp/opensip-architecture-review-env/bin/python'
ROOTV = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
         'author-package-final33-verification.v2/verification.json')
R = {}
if os.path.isdir(WORK):
    shutil.rmtree(WORK)
r = subprocess.run([PY, '-I', '-B', os.path.join(PKG, 'verify-package.py'),
                    '--source', SRC, '--out', WORK], capture_output=True, text=True, timeout=5400)
R['returncode'] = r.returncode
R['stdout'] = r.stdout[-900:]
R['stderrTail'] = (r.stderr or '')[-900:]
print('verify-package.py rc=%d' % r.returncode)
print(r.stdout[-700:])
if r.returncode:
    print('--- stderr ---')
    print((r.stderr or '')[-800:])
vp = os.path.join(WORK, 'verification.json')
R['verificationJsonEmitted'] = os.path.isfile(vp)
if R['verificationJsonEmitted']:
    v = json.load(open(vp))
    R['verification'] = v
    R['mySha256'] = hashlib.sha256(open(vp, 'rb').read()).hexdigest()
    print('\npassed=%s sourceFiles=%s packageFiles=%s'
          % (v.get('passed'), v.get('sourceFilesVerified'), v.get('packageFilesVerified')))
    for g in v.get('groups', []):
        print('   %-26s passed=%-5s count=%s' % (g['group'], g['passed'], g['count']))
    R['queryChecks'] = next((g['count'] for g in v['groups'] if g['group'] == 'query'), None)
    R['runOutcomes'] = sum(g['count'] for g in v['groups'] if g['group'] != 'query')
    R['allGroupsPassed'] = all(g['passed'] for g in v['groups'])
qa = os.path.join(WORK, 'query-assessment.json')
if os.path.isfile(qa):
    q = json.load(open(qa))
    R['queryAssessment'] = {'passed': q.get('passed'), 'checks': len(q.get('checks', []))}
    print('\nquery-assessment: passed=%s checks=%d' % (q.get('passed'), len(q.get('checks', []))))
    for c in q.get('checks', []):
        print('   - %-44s %s' % (str(c.get('name'))[:44], c.get('passed')))
if os.path.isfile(ROOTV):
    rv = json.load(open(ROOTV))
    R['rootVerificationSha256'] = hashlib.sha256(open(ROOTV, 'rb').read()).hexdigest()
    R['rootNamedSha256'] = '04d2c41f3cd1c646395349de19de0bcb5e2991b73e30040849963589720692ae'
    R['rootVerificationMatchesNamedDigest'] = R['rootVerificationSha256'] == R['rootNamedSha256']
    mine = {g['group']: (g['passed'], g['count']) for g in (R.get('verification') or {}).get('groups', [])}
    root_g = {g['group']: (g['passed'], g['count']) for g in rv.get('groups', [])}
    R['myGroupsMatchRoot'] = mine == root_g
    R['rootPassed'] = rv.get('passed')
    print('\nroot verification digest matches the named one:', R['rootVerificationMatchesNamedDigest'])
    print('my group outcomes identical to root\'s        :', R['myGroupsMatchRoot'])
    print('   (agreement is corroboration; my basis is my own execution)')
json.dump(R, open(os.path.join(OUT, 'p13-queries.json'), 'w'), indent=1, default=str)
print('\nwrote p13-queries.json')
