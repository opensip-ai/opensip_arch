"""Run the owner's check-integrated-carrier.v1.py against one tree (argv[1] = frozen37 | v1final | edited | hybrid-*).

Uses that tree's own validator bytes. The report path must be new; earlier reports are preserved.
"""
import json, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
COPY = sys.argv[1]
SRC = BASE / 'work' / COPY
report = BASE / 'receipts' / ('p03-integrated-carrier.' + COPY + '.json')
if report.exists():
    raise SystemExit('preserve earlier report: ' + str(report))
cmd = [sys.executable, '-I', '-B', str(SRC / 'docs/coop/design-corrections/security/check-integrated-carrier.v1.py'),
       '--source', str(SRC), '--report', str(report)]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
print(r.stdout[-3000:])
print(r.stderr[-3000:], file=sys.stderr)
if report.exists():
    rep = json.loads(report.read_text())
    s37 = [c for c in rep.get('checks', []) if c['check'].startswith('source37')]
    print(json.dumps({'passed': rep.get('passed'), 'failed': rep.get('failed'), 'childExitCode': rep.get('childExitCode'),
                      'source37Checks': len(s37),
                      'source37StorageChecks': len([c for c in s37 if c['check'].startswith('source37 storage')]),
                      'failures': [c for c in rep.get('checks', []) if not c['pass']]}, indent=1))
raise SystemExit(r.returncode)
