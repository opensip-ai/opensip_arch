"""Launch the DECLARED reference interpreter. System python3 lacks jsonschema; a wrong
invocation must never be read as a source failure."""
import subprocess, sys

PY = '/tmp/opensip-architecture-review-env/bin/python'
sys.exit(subprocess.run([PY, '-I', '-B'] + sys.argv[1:]).returncode)
