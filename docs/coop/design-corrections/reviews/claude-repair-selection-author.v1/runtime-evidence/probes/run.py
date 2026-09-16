"""Launcher: run a probe under the reference interpreter via subprocess."""
import os, subprocess, sys

REF = '/tmp/opensip-architecture-review-env/bin/python'
HERE = os.path.dirname(os.path.abspath(__file__))
target = sys.argv[1]
if not os.path.isabs(target):
    target = os.path.join(HERE, target)
p = subprocess.run([REF, '-I', '-B', target] + sys.argv[2:], capture_output=True, text=True)
sys.stdout.write(p.stdout)
sys.stderr.write(p.stderr)
print('EXIT', p.returncode)
sys.exit(p.returncode)
