"""Owner check-integrated-carrier.v1.py over one tree (argv[1] = frozen37 | v2final | edited | hybrid-*, argv[2] = label).

Uses that tree's own validator bytes; the report name carries the label, and earlier reports are never overwritten.
"""
import json, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3')
TREE, LABEL = sys.argv[1], sys.argv[2]
SRC = BASE / 'work' / TREE
report = BASE / 'receipts' / ('p03-integrated-carrier.%s.%s.json' % (TREE, LABEL))
if report.exists():
    raise SystemExit('preserve earlier report: ' + str(report))
r = subprocess.run([sys.executable, '-I', '-B', str(SRC / 'docs/coop/design-corrections/security/check-integrated-carrier.v1.py'),
                    '--source', str(SRC), '--report', str(report)], capture_output=True, text=True, timeout=1200)
print(r.stdout[-3000:])
print(r.stderr[-3000:], file=sys.stderr)
if report.exists():
    rep = json.loads(report.read_text())
    s37 = [c for c in rep.get('checks', []) if c['check'].startswith('source37')]
    print(json.dumps({'passed': rep.get('passed'), 'failed': rep.get('failed'), 'childExitCode': rep.get('childExitCode'),
                      'source37Checks': len(s37), 'source37StorageChecks': len([c for c in s37 if c['check'].startswith('source37 storage')]),
                      'failures': [c for c in rep.get('checks', []) if not c['pass']][:60]}, indent=1))
raise SystemExit(r.returncode)
