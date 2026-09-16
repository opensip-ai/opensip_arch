import json, hashlib, os
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2'
R = '/Users/sb/code/opensip-ai/opensip_arch'
C = '/tmp/opensip-design-corrections/candidate-subject.v45'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()
cm = json.load(open(R + '/docs/coop/design-corrections/reviews/candidate-subject.v45.json'))
print('candidate manifest keys', list(cm.keys())[:30])
ent = None
for k, v in cm.items():
    if isinstance(v, list) and v and isinstance(v[0], dict) and 'sha256' in v[0]:
        print('list', k, len(v), list(v[0].keys()))
        ent = ent or v
cmap = {}
for e in ent:
    cmap[e['path']] = e['sha256']
bad = 0
for p, h in cmap.items():
    fp = C + '/' + p
    if not os.path.isfile(fp) or sha(fp) != h:
        bad += 1
        if bad < 10: print('SNAP BAD', p)
disk = 0; unl = []
for r, ds, fs in os.walk(C):
    for f in fs:
        disk += 1
        rel = os.path.relpath(os.path.join(r, f), C)
        if rel not in cmap: unl.append(rel)
print('snapshot entries', len(cmap), 'bad', bad, 'disk', disk, 'unlisted', unl[:10])
m = json.load(open(S + '/application-subject.v45.json'))
same = []; diff = []; absent = []
for e in m['files']:
    if e['path'] in cmap:
        (same if cmap[e['path']] == e['sha256'] else diff).append(e['path'])
    else:
        absent.append(e['path'])
print('files identical to snapshot', len(same))
print('files differing from snapshot', len(diff)); [print('  DIFF', p) for p in diff]
print('files absent from snapshot', len(absent)); [print('  ABSENT', p) for p in absent]
# live checks
livebad = []
for e in m['files']:
    fp = R + '/' + e['path']
    cur = sha(fp) if os.path.isfile(fp) else None
    if cur != e['beforeSha256']:
        livebad.append((e['path'], 'live', cur, 'before', e['beforeSha256'], 'after==live', cur == e['sha256']))
print('live != before', len(livebad)); [print('  ', x) for x in livebad[:20]]
print('activation exists', os.path.exists(R + '/docs/coop/design-corrections/application-activation.v1.json'))
for k in ['retainedManifestPath', 'retainedReviewPath']:
    print(k, os.path.exists(R + '/' + m[k]))
# before images in snapshot?
bsnap = sum(1 for e in m['beforeImages'] if cmap.get(e['path']) == e['sha256'])
print('beforeImages equal to snapshot bytes', bsnap, 'of', len(m['beforeImages']))
# new files (before None) which snapshot has
print('NEW files present in snapshot identical', sum(1 for e in m['files'] if e['beforeSha256'] is None and cmap.get(e['path']) == e['sha256']))
json.dump({'same': same, 'diff': diff, 'absent': absent}, open('/private/tmp/opensip-design-corrections/application-review.v45/probes/p03_out.json', 'w'), indent=1)
