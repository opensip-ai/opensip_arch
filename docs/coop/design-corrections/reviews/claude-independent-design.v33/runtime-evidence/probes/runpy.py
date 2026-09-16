"""Declared reference interpreter."""
import subprocess, sys
sys.exit(subprocess.run(['/tmp/opensip-architecture-review-env/bin/python', '-I', '-B']
                        + sys.argv[1:]).returncode)
