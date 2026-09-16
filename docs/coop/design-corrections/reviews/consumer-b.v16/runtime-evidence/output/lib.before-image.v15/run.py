"""Invoke the supplied reference interpreter (`/tmp/opensip-architecture-review-env/bin/python -I -B`)
on one of this origin's own scripts. Used because the allowed shell prefix is literal python3.

    python3 output/lib/run.py <script.py> [args...]
"""
import subprocess
import sys
import os

PY = "/tmp/opensip-architecture-review-env/bin/python"
LIB = os.path.dirname(os.path.abspath(__file__))

cmd = [PY, "-I", "-B"] + sys.argv[1:]
env = dict(os.environ)
env["PYTHONPATH"] = LIB
p = subprocess.run(cmd, env=env)
sys.exit(p.returncode)
