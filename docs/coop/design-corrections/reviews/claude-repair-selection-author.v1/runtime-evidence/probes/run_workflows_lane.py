"""Run the historical workflows lane (check_workflows.v1.py) after the v1 model seam edit."""
import json, os, subprocess, sys

REF = '/tmp/opensip-architecture-review-env/bin/python'
WF = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source/docs/coop/design-corrections/workflows'
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, 'workflows-report.authorprobe.json')

p = subprocess.run([REF, '-I', '-B', os.path.join(WF, 'check_workflows.v1.py'), '--report', REPORT],
                   capture_output=True, text=True, cwd=WF, timeout=900)
print('exit', p.returncode)
print('stdout tail:', p.stdout[-1500:])
if p.stderr:
    print('stderr tail:', p.stderr[-2500:])
if os.path.exists(REPORT):
    d = json.load(open(REPORT))
    checks = d.get('checks') or d.get('results') or []
    failed = [c for c in checks if not c.get('ok', True)]
    print('report checks', len(checks), 'failed', len(failed))
    for f in failed[:20]:
        print('  FAIL', f.get('id'), '|', str(f.get('detail'))[:200])
