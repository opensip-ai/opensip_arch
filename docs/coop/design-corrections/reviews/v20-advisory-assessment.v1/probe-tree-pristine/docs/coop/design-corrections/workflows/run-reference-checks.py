"""Verify the pinned source inventory, then run the workflows reference checker.
The review snapshot authenticates this launcher and its pin manifest externally;
this is not a hostile-host or self-authentication mechanism.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; ROOT = H.parents[3]
p = argparse.ArgumentParser(); p.add_argument('--report', required=True); a = p.parse_args()
manifest = json.loads((H / 'source-pins.v1.json').read_text()); failures = []
for item in manifest['files']:
    path = ROOT / item['path']
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        failures.append(item['path'])
if failures:
    result = {'sourcePinsValid': False, 'changedOrMissing': failures, 'checksExecuted': False, 'productQualification': False}
else:
    run = subprocess.run([sys.executable, '-I', '-B', str(H / 'check_workflows.v1.py'), '--report', str(H / 'workflows-report.v1.json')], capture_output=True, text=True, timeout=300)
    rep = H / 'workflows-report.v1.json'
    result = {'sourcePinsValid': True, 'sourceFileCount': len(manifest['files']), 'checksExecuted': True,
              'check': {'script': 'check_workflows.v1.py', 'exitCode': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr, 'reportSha256': hashlib.sha256(rep.read_bytes()).hexdigest() if rep.exists() else None},
              'passed': run.returncode == 0, 'productQualification': False}
Path(a.report).write_text(json.dumps(result, indent=2) + '\n'); print(json.dumps({k: v for k, v in result.items() if k != 'check'})); sys.exit(not result.get('passed', False))
