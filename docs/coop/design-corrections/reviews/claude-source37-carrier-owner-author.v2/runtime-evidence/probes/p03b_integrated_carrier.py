"""Owner check-integrated-carrier.v1.py over one tree after p02b (argv[1] = tree, argv[2] = report label).

Same as p03 except that the report name carries a label, so earlier p03 reports stay preserved.
"""
import json, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
COPY, LABEL = sys.argv[1], sys.argv[2]
SRC = BASE / 'work' / COPY
report = BASE / 'receipts' / ('p03b-integrated-carrier.%s.%s.json' % (COPY, LABEL))
if report.exists():
    raise SystemExit('preserve earlier report: ' + str(report))
r = subprocess.run([sys.executable, '-I', '-B', str(SRC / 'docs/coop/design-corrections/security/check-integrated-carrier.v1.py'),
                    '--source', str(SRC), '--report', str(report)], capture_output=True, text=True, timeout=900)
print(r.stdout[-3000:])
print(r.stderr[-3000:], file=sys.stderr)
if report.exists():
    rep = json.loads(report.read_text())
    s37 = [c for c in rep.get('checks', []) if c['check'].startswith('source37')]
    print(json.dumps({'passed': rep.get('passed'), 'failed': rep.get('failed'), 'childExitCode': rep.get('childExitCode'),
                      'source37Checks': len(s37), 'source37StorageChecks': len([c for c in s37 if c['check'].startswith('source37 storage')]),
                      'failures': [c for c in rep.get('checks', []) if not c['pass']]}, indent=1))
raise SystemExit(r.returncode)
