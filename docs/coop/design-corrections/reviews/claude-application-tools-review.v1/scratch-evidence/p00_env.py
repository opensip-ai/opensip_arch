"""P00: runtime/interpreter facts and existence-only check of hardcoded support paths."""
import os
import subprocess
import sys

REF = '/tmp/opensip-architecture-review-env/bin/python'
print('host python3', sys.version.split()[0], sys.executable)
print('ref exists', os.path.exists(REF))
if os.path.exists(REF):
    code = 'import sys;print(sys.version.split()[0]);import jsonschema;print("jsonschema",jsonschema.__version__)'
    r = subprocess.run([REF, '-I', '-B', '-c', code], capture_output=True, text=True)
    print('ref rc', r.returncode)
    print('ref out', r.stdout.strip().replace('\n', ' | '))
    print('ref err', r.stderr.strip()[:200])

# Existence only. No contents are read from any of these paths.
PATHS = [
    ('assemble-records.successor.v1.py:166 finalizer/catalog source',
     '/tmp/opensip-design-corrections/application-assembly.v1/files'),
    ('assemble parent', '/tmp/opensip-design-corrections/application-assembly.v1'),
    ('prepare-validation.py:5 / verify-applied.py:17 interpreter', REF),
    ('retain_public.py:334 default grok cli', '/Users/sb/.grok/bin/grok'),
    ('launch-...successor.v1.py:75 default claude cli', '/Users/sb/.local/bin/claude'),
    ('retain-...successor.v1.py:119 claude session logs', '/Users/sb/.claude/projects'),
    ('retain_public.py:76 default grok sessions root', '/Users/sb/.grok/sessions'),
]
for label, p in PATHS:
    print('exists', os.path.exists(p), '|', label, '|', p)
