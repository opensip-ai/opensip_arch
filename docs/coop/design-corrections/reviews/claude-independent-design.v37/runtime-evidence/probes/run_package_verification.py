"""Extract a second verified exact copy and run the nonblind author package verifier against it."""
import json, subprocess, sys
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v37'
PY = '/tmp/opensip-architecture-review-env/bin/python'
SRC = BASE + '/work/source37-pkg'
p = subprocess.run([PY, '-I', '-B', BASE + '/probes/verify_archive_and_extract.py', SRC], capture_output=True, text=True)
print(p.stdout[-1500:], p.stderr[-1500:])
assert p.returncode == 0 and '"verified": true' in p.stdout
q = subprocess.run([PY, '-I', '-B', '/tmp/opensip-design-corrections/claude-author-package-successor.v14/verify-package.py',
                    '--source', SRC, '--out', BASE + '/receipts/package-verification'], capture_output=True, text=True, timeout=5400)
open(BASE + '/receipts/package-verification.stdout', 'w').write(q.stdout)
open(BASE + '/receipts/package-verification.stderr', 'w').write(q.stderr)
print('exit', q.returncode)
print(q.stdout[-3000:])
print(q.stderr[-3000:])
