"""Run one of my probe scripts under the pinned review interpreter."""
import subprocess, sys
PY = '/tmp/opensip-architecture-review-env/bin/python'
r = subprocess.run([PY, '-I', '-B'] + sys.argv[1:], capture_output=True, text=True, timeout=5400)
print(r.stdout)
if r.stderr:
    print('--- stderr ---')
    print(r.stderr[-6000:])
raise SystemExit(r.returncode)
