"""Run the workflow-projection checker under the reference interpreter and summarise."""
import json, os, subprocess, sys

REF = '/tmp/opensip-architecture-review-env/bin/python'
WF = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source/docs/coop/design-corrections/workflows'
SCRIPT = os.path.join(WF, 'check-workflow-projection.v3.py')
HERE = os.path.dirname(os.path.abspath(__file__))

p = subprocess.run([REF, '-I', '-B', SCRIPT], capture_output=True, text=True, cwd=WF, timeout=900)
open(os.path.join(HERE, 'checker-stdout.json'), 'w').write(p.stdout)
if p.stderr:
    open(os.path.join(HERE, 'checker-stderr.txt'), 'w').write(p.stderr)
print('exit', p.returncode)
try:
    d = json.loads(p.stdout)
except Exception:
    print('--- stdout tail ---')
    print(p.stdout[-2000:])
    print('--- stderr tail ---')
    print(p.stderr[-4000:])
    raise SystemExit(1)

print('passed', d['passed'], 'count', d['count'], 'failed', len(d['failed']))
for f in d['failed'][:25]:
    print('  FAIL', f['id'], '|', f['detail'][:200])
print()
cw = [c for c in d['results'] if c['id'].startswith('repair-cw')]
print('repair-cw checks:', len(cw), 'ok:', sum(1 for c in cw if c['ok']))
for c in cw:
    print('  ', 'ok  ' if c['ok'] else 'FAIL', c['id'], ('| ' + c['detail'][:160]) if not c['ok'] else '')
