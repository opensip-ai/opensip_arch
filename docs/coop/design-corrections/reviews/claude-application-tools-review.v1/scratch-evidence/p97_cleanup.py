"""Remove the inputs/__pycache__ directory created as a side effect of this review's
in-process imports, restoring inputs/ to exactly its delivered contents.

Strictly scoped: only a directory literally named __pycache__ directly under inputs/,
and only .pyc files inside it. No manifest-listed file is touched.
"""
import hashlib
import json
import os

BASE = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v1'
INP = os.path.join(BASE, 'inputs')
PYC = os.path.join(INP, '__pycache__')
m = json.load(open(os.path.join(BASE, 'input-manifest.json')))
listed = {r['path'] for r in m['files']}

before = {r['path']: hashlib.sha256(open(os.path.join(INP, r['path']), 'rb').read()).hexdigest()
          for r in m['files']}

removed = []
if os.path.isdir(PYC):
    for name in sorted(os.listdir(PYC)):
        p = os.path.join(PYC, name)
        assert os.path.isfile(p) and name.endswith('.pyc'), 'unexpected entry, not removing: ' + p
        os.remove(p)
        removed.append(name)
    os.rmdir(PYC)
print('removed pyc files:', len(removed))
print('pycache gone:', not os.path.exists(PYC))

after = {r['path']: hashlib.sha256(open(os.path.join(INP, r['path']), 'rb').read()).hexdigest()
         for r in m['files']}
drift = [k for k in before if before[k] != after[k]]
mismatch = [r['path'] for r in m['files']
            if after[r['path']] != r['sha256']
            or os.path.getsize(os.path.join(INP, r['path'])) != r['bytes']]
print('no drift across cleanup:', not drift, drift)
print('all 19 still match manifest sha256 + bytes:', not mismatch, mismatch)
actual = set(os.listdir(INP))
print('inputs dir now exactly the 19 listed files:', actual == listed, sorted(actual - listed))
