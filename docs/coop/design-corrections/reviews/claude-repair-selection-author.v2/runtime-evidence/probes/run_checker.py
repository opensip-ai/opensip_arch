"""Run the workflow-projection checker under the reference interpreter with full receipts."""
import json, os, subprocess

REF = '/tmp/opensip-architecture-review-env/bin/python'
WF = '/tmp/opensip-design-corrections/repair-selection-successor.v2/source/docs/coop/design-corrections/workflows'
SCRIPT = os.path.join(WF, 'check-workflow-projection.v3.py')
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, 'receipts'), exist_ok=True)

p = subprocess.run([REF, '-I', '-B', SCRIPT], capture_output=True, text=True, cwd=WF, timeout=1800)
json.dump({'command': [REF, '-I', '-B', SCRIPT], 'cwd': WF, 'exitCode': p.returncode,
           'stdout': p.stdout, 'stderr': p.stderr},
          open(os.path.join(HERE, 'receipts', 'check-workflow-projection.receipt.json'), 'w'), indent=2)
print('exit', p.returncode)
try:
    d = json.loads(p.stdout)
except Exception:
    print('--- stdout tail ---'); print(p.stdout[-1500:])
    print('--- stderr tail ---'); print(p.stderr[-4000:])
    raise SystemExit(1)

json.dump(d, open(os.path.join(HERE, 'checker-report.json'), 'w'), indent=2)
print('passed', d['passed'], 'count', d['count'], 'failed', len(d['failed']))
for f in d['failed'][:30]:
    print('  FAIL', f['id'], '|', f['detail'][:220])
cw = [c for c in d['results'] if c['id'].startswith('repair-cw')]
print('repair-cw:', len(cw), 'ok', sum(1 for c in cw if c['ok']))
for c in cw:
    if not c['ok']:
        print('   FAIL', c['id'], '|', c['detail'][:220])
