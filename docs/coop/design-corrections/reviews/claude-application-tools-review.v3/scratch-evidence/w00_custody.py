"""W00: verify the v3 manifest and all 26 files; classify against the frozen v2 inputs."""
import hashlib
import json
import os

V3 = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v3'
V2 = '/tmp/opensip-design-corrections/claude-application-tools-review.v2'
EXPECT = '7e1e0165c9800c8c937b40598056a4f18fa056efaa700952dcb57711bd4fd47f'

mp = os.path.join(V3, 'input-manifest.json')
raw = open(mp, 'rb').read()
got = hashlib.sha256(raw).hexdigest()
print('manifest bytes', len(raw), '| sha256', got)
print('MANIFEST MATCH', got == EXPECT)

m = json.load(open(mp))
print('standing:', m.get('standing'))
files = m['files']
print('declared file count:', len(files))

v2m = json.load(open(os.path.join(V2, 'input-manifest.json')))
v2 = {r['path']: (r['sha256'], r['bytes']) for r in v2m['files']}

bad, unchanged, changed, new = [], [], [], []
for r in files:
    p = os.path.join(V3, 'inputs', r['path'])
    if not os.path.isfile(p):
        bad.append((r['path'], 'MISSING'))
        continue
    d = open(p, 'rb').read()
    h = hashlib.sha256(d).hexdigest()
    if h != r['sha256'] or len(d) != r['bytes']:
        bad.append((r['path'], 'DIGEST/BYTES MISMATCH'))
        continue
    if r['path'] in v2:
        (unchanged if v2[r['path']][0] == h else changed).append(r['path'])
    else:
        new.append(r['path'])

listed = {r['path'] for r in files}
top = {p.split('/')[0] for p in listed}
actual = set(os.listdir(os.path.join(V3, 'inputs')))
print('ALL 26 VERIFIED:', not bad, bad)
print('unlisted entries in inputs/:', sorted(actual - top))
print()
print('CHANGED vs v2 (%d) - full re-read required:' % len(changed))
for p in sorted(changed):
    nb = dict((r['path'], (r['sha256'], r['bytes'])) for r in files)[p]
    print('   ~ %-52s %s(%d) -> %s(%d)' % (p, v2[p][0][:10], v2[p][1], nb[0][:10], nb[1]))
print('UNCHANGED from v2 (%d) - reuse v2 full read with exact custody:' % len(unchanged))
for p in sorted(unchanged):
    print('   =', p)
print('NEW in v3 (%d):' % len(new))
for p in sorted(new):
    print('   +', p)
gone = sorted(set(v2) - listed)
print('present in v2 but NOT in v3 (%d):' % len(gone), gone)
