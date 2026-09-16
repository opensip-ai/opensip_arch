"""PROBE 16 (v31) — A-6: execute the package verifier myself against frozen source31 and assess
the query semantics and limits it now asserts. Root's retained receipts are compared, not trusted."""
import hashlib, json, os, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v7'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
OUT = os.path.join(BASE, 'receipts')
WORK = os.path.join(BASE, 'disposable/verifypkg')
PY = '/tmp/opensip-architecture-review-env/bin/python'
if os.path.isdir(WORK):
    shutil.rmtree(WORK)
R = {}

cmd = [PY, '-I', '-B', os.path.join(PKG, 'verify-package.py'), '--source', SRC, '--out', WORK]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
R['returncode'] = r.returncode
R['stdout'] = r.stdout
R['stderrTail'] = (r.stderr or '')[-1500:]
print('verify-package.py rc=%d' % r.returncode)
print(r.stdout)
if r.returncode:
    print('--- stderr ---')
    print((r.stderr or '')[-1500:])

vp = os.path.join(WORK, 'verification.json')
if os.path.isfile(vp):
    v = json.load(open(vp))
    R['verification'] = v
    print('\nverification.json:')
    print('   passed              :', v.get('passed'))
    print('   sourceFilesVerified :', v.get('sourceFilesVerified'))
    print('   packageFilesVerified:', v.get('packageFilesVerified'))
    for g in v.get('groups', []):
        print('   %-26s passed=%-5s count=%s' % (g['group'], g['passed'], g['count']))
    R['queryGroupPresent'] = any(g['group'] == 'query' for g in v.get('groups', []))
    R['queryChecks'] = next((g['count'] for g in v.get('groups', []) if g['group'] == 'query'), None)
    R['allThirteenPlusQuery'] = sum(g['count'] for g in v.get('groups', [])
                                    if g['group'] != 'query') == 13

# query assessment semantics
qa = os.path.join(WORK, 'query-assessment.json')
if os.path.isfile(qa):
    q = json.load(open(qa))
    R['queryAssessment'] = q
    print('\nquery-assessment.json: passed=%s checks=%d' % (q.get('passed'), len(q.get('checks', []))))
    for c in q.get('checks', []):
        print('   -', str(c)[:150])

# compare my regenerated query outputs with the package's retained copies
qdir = os.path.join(WORK, 'query-checks')
cmp_rows = []
if os.path.isdir(qdir):
    for n in sorted(os.listdir(qdir)):
        mine = os.path.join(qdir, n)
        ship = os.path.join(PKG, 'query-checks1', n)
        row = {'file': n, 'shippedPresent': os.path.isfile(ship)}
        if row['shippedPresent']:
            row['sameBytes'] = (hashlib.sha256(open(mine, 'rb').read()).hexdigest()
                                == hashlib.sha256(open(ship, 'rb').read()).hexdigest())
        cmp_rows.append(row)
R['queryOutputComparison'] = cmp_rows
R['queryOutputsRegeneratedIdentical'] = all(c.get('sameBytes') for c in cmp_rows if c['shippedPresent'])
print('\nquery outputs vs package retained copies: %d compared, all identical: %s'
      % (len(cmp_rows), R['queryOutputsRegeneratedIdentical']))
for c in cmp_rows:
    if c['shippedPresent'] and not c.get('sameBytes'):
        print('   DIFFERS:', c['file'])

# assess root's retained source31 verification against mine
RV = '/tmp/opensip-design-corrections/author-package-final31-verification.v1'
rv = os.path.join(RV, 'verification.json')
if os.path.isfile(rv):
    root_v = json.load(open(rv))
    R['rootVerification'] = root_v
    print('\nroot retained verification: passed=%s groups=%s'
          % (root_v.get('passed'), [(g['group'], g['passed'], g['count'])
                                    for g in root_v.get('groups', [])]))
    mine_g = {g['group']: (g['passed'], g['count'], g.get('reportSha256'))
              for g in (R.get('verification') or {}).get('groups', [])}
    root_g = {g['group']: (g['passed'], g['count'], g.get('reportSha256'))
              for g in root_v.get('groups', [])}
    R['myGroupsMatchRootGroups'] = mine_g == root_g
    R['groupDifferences'] = {k: {'mine': mine_g.get(k), 'root': root_g.get(k)}
                             for k in set(mine_g) | set(root_g) if mine_g.get(k) != root_g.get(k)}
    print('my group outcomes identical to root receipts (incl. report digests):',
          R['myGroupsMatchRootGroups'])
    if R['groupDifferences']:
        print('   differences:', json.dumps(R['groupDifferences'])[:500])

json.dump(R, open(os.path.join(OUT, 'p16-verifypkg.json'), 'w'), indent=1, default=str)
print('\nwrote p16-verifypkg.json')
