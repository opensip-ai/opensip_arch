"""Identify the unlisted entry in inputs/ (side effect of in-process imports)."""
import json
import os

BASE = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v1'
INP = os.path.join(BASE, 'inputs')
m = json.load(open(os.path.join(BASE, 'input-manifest.json')))
listed = {r['path'] for r in m['files']}
actual = set(os.listdir(INP))
extra = sorted(actual - listed)
print('manifest-listed:', len(listed), '| actual:', len(actual))
print('unlisted entries:', extra)
for e in extra:
    p = os.path.join(INP, e)
    print(' ', e, '| isdir:', os.path.isdir(p))
    if os.path.isdir(p):
        print('   contents:', sorted(os.listdir(p)))
print('missing manifest files:', sorted(listed - actual))
