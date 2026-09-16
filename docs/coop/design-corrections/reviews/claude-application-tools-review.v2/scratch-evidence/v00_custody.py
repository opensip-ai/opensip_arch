"""V00: verify the v2 input manifest and every input file; classify changed vs unchanged
against the v1 manifest so unchanged bytes can reuse the earlier full read with custody.
"""
import hashlib
import json
import os

V2 = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v2'
V1 = '/tmp/opensip-design-corrections/claude-application-tools-review.v1'
EXPECT = '8370a139d4ee7f449b0d39be011362618f8dfb1a17bc27b378586d16241d60a5'

mp = os.path.join(V2, 'input-manifest.json')
raw = open(mp, 'rb').read()
got = hashlib.sha256(raw).hexdigest()
print('manifest bytes', len(raw))
print('manifest sha256', got)
print('MANIFEST MATCH', got == EXPECT)

m = json.load(open(mp))
print('manifest top-level keys:', sorted(m))
files = m['files']
print('declared file count:', len(files))

v1m = json.load(open(os.path.join(V1, 'input-manifest.json')))
v1 = {r['path']: r['sha256'] for r in v1m['files']}

bad, unchanged, changed, new = [], [], [], []
for r in files:
    p = os.path.join(V2, 'inputs', r['path'])
    if not os.path.isfile(p):
        bad.append((r['path'], 'MISSING'))
        continue
    d = open(p, 'rb').read()
    h = hashlib.sha256(d).hexdigest()
    if h != r['sha256'] or len(d) != r['bytes']:
        bad.append((r['path'], 'DIGEST/BYTES MISMATCH'))
        continue
    if r['path'] in v1:
        (unchanged if v1[r['path']] == h else changed).append(r['path'])
    else:
        new.append(r['path'])

listed = {r['path'] for r in files}
actual = set(os.listdir(os.path.join(V2, 'inputs')))
print('ALL VERIFIED:', not bad, bad)
print('extra entries in inputs/:', sorted(actual - listed))
print('missing from inputs/:', sorted(listed - actual))
print()
print('UNCHANGED from v1 (%d) - reuse earlier full read with custody:' % len(unchanged))
for p in sorted(unchanged):
    print('   =', p)
print('CHANGED vs v1 (%d) - must be fully re-read:' % len(changed))
for p in sorted(changed):
    print('   ~', p, v1[p][:12], '->', dict((r['path'], r['sha256']) for r in files)[p][:12])
print('NEW in v2 (%d) - read as needed for new function:' % len(new))
for p in sorted(new):
    print('   +', p)
v1_only = sorted(set(v1) - listed)
print('present in v1 but NOT in v2 (%d):' % len(v1_only), v1_only)
