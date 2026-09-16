"""Run the owner's check-integrated-carrier.v1.py against one disposable copy (argv[1] = baseline | edited).

Uses that copy's own validator bytes. The report path must be new; earlier reports are preserved.
"""
import json, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
COPY = sys.argv[1]
SRC = BASE / 'work' / COPY
report = BASE / 'receipts' / ('p03-integrated-carrier.' + COPY + '.json')
if report.exists():
    raise SystemExit('preserve earlier report: ' + str(report))
cmd = [sys.executable, '-I', '-B', str(SRC / 'docs/coop/design-corrections/security/check-integrated-carrier.v1.py'),
       '--source', str(SRC), '--report', str(report)]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
print(r.stdout[-4000:])
print(r.stderr[-4000:], file=sys.stderr)
if report.exists():
    rep = json.loads(report.read_text())
    print(json.dumps({'passed': rep.get('passed'), 'failed': rep.get('failed'), 'childExitCode': rep.get('childExitCode'),
                      'failures': [c for c in rep.get('checks', []) if not c['pass']]}, indent=1))
raise SystemExit(r.returncode)
