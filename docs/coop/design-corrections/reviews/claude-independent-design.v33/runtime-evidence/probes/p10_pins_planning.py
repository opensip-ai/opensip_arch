"""P10 — justified reruns: all five pin ledgers were re-digested 32->33, and the planning records
changed, so pin validity and the planning groups must be re-established on 33."""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/kit33')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {'justification': 'all five pin ledgers were re-digested and the planning records changed in my derived delta'}

L = os.path.join(SRC, 'docs/coop/design-corrections/foundation/run-evaluator3-checks.py')
LED = os.path.join(SRC, 'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json')
R['launcherSha256'] = hashlib.sha256(open(L, 'rb').read()).hexdigest()
R['pinLedgerRows'] = len(json.load(open(LED))['files'])
LOUT = os.path.join(OUT, 'evaluator3-launcher33')
if os.path.isdir(LOUT):
    shutil.rmtree(LOUT)
t0 = time.time()
r = subprocess.run([PY, '-I', '-B', L, '--out', LOUT], capture_output=True, text=True, timeout=7200)
R['launcher'] = {'returncode': r.returncode, 'seconds': round(time.time() - t0, 1)}
print('evaluator3 launcher rc=%d (%.0fs) pin ledger rows=%d'
      % (r.returncode, time.time() - t0, R['pinLedgerRows']))
rep = os.path.join(LOUT, 'report.json')
if os.path.isfile(rep):
    d = json.load(open(rep))
    R['launcherReport'] = {'sourcePinsValid': d.get('sourcePinsValid'), 'passed': d.get('passed'),
                           'changedOrMissing': len(d.get('changedOrMissing', [])),
                           'children': len(d.get('checks', [])),
                           'allExitZero': all(c.get('exitCode') == 0 for c in d.get('checks', []))}
    print('   sourcePinsValid=%s passed=%s changedOrMissing=%d children=%d allExitZero=%s'
          % (d.get('sourcePinsValid'), d.get('passed'), len(d.get('changedOrMissing', [])),
             len(d.get('checks', [])), R['launcherReport']['allExitZero']))
    for c in d.get('checks', []):
        if c.get('exitCode') != 0:
            print('   NONZERO:', c.get('name'), c.get('exitCode'))

rows = []
for name, args in (('check_repository_file_inventory.py', ['--check']),
                   ('check_implementation_planning.py', ['--source', SRC, '--check'])):
    p = os.path.join(KIT, 'docs/operations', name)
    if not os.path.isfile(p):
        rows.append({'checker': name, 'error': 'absent from the disposable copy'})
        print('%-42s MISSING' % name)
        continue
    t0 = time.time()
    rr = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True,
                        cwd=KIT, timeout=3600)
    tail = (rr.stdout or '').strip().splitlines()[-1:] or ['']
    rows.append({'checker': name, 'returncode': rr.returncode, 'lastLine': tail[0][-200:],
                 'stderrTail': (rr.stderr or '')[-400:] if rr.returncode else ''})
    print('%-42s rc=%-3d %s' % (name, rr.returncode, tail[0][-110:]))
R['planningGroups'] = rows
R['allPlanningExitZero'] = all(x.get('returncode') == 0 for x in rows)
dev = sum(1 for rel, f in man.items()
          if not os.path.isfile(os.path.join(SRC, rel))
          or hashlib.sha256(open(os.path.join(SRC, rel), 'rb').read()).hexdigest() != f['sha256'])
R['frozenDeviationsAfterRuns'] = dev
print('\nfrozen33 deviations after these runs:', dev)
json.dump(R, open(os.path.join(OUT, 'p10-pins-planning.json'), 'w'), indent=1, default=str)
print('wrote p10-pins-planning.json')
