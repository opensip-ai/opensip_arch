"""Invoke the supplied reference interpreter (/tmp/opensip-architecture-review-env/bin/python -I -B)
on a script under output/, echoing stdout/stderr and propagating the exit status."""
import subprocess
import sys

REF = ['/tmp/opensip-architecture-review-env/bin/python', '-I', '-B']
r = subprocess.run(REF + sys.argv[1:], capture_output=True, text=True)
out = r.stdout
if len(out) > 30000:
    out = out[:12000] + "\n...[truncated]...\n" + out[-15000:]
print(out)
if r.stderr:
    print("STDERR:", r.stderr[-8000:])
print("EXIT", r.returncode)
sys.exit(r.returncode)
