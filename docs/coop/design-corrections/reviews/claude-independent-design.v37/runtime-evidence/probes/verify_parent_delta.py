import hashlib, json, os, glob

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v37/receipts/parent-delta.json'
m37 = json.load(open(REV + 'candidate-subject.v37.json'))
parent = m37['parentManifestSha256']
cands = []
for p in sorted(glob.glob(REV + 'candidate-subject.v*.json')):
    b = open(p, 'rb').read()
    if hashlib.sha256(b).hexdigest() == parent:
        cands.append(p)
res = {'parentManifestSha256': parent, 'parentManifestPaths': cands}
if cands:
    m36 = json.load(open(cands[0]))
    a = {f['path']: (f['sha256'], f['bytes']) for f in m36['files']}
    b = {f['path']: (f['sha256'], f['bytes']) for f in m37['files']}
    added = sorted(set(b) - set(a))
    removed = sorted(set(a) - set(b))
    changed = sorted(p for p in set(a) & set(b) if a[p] != b[p])
    res.update({'parentFileCount': m36['fileCount'], 'parentTotalBytes': m36['totalBytes'],
                'parentSnapshotRoot': m36.get('snapshotRoot'),
                'added': added, 'removed': removed, 'changed': changed})
    # verify parent snapshot bytes if present
    root36 = m36.get('snapshotRoot')
    bad = []
    if root36 and os.path.isdir(root36):
        for f in m36['files']:
            pp = os.path.join(root36, f['path'])
            if not os.path.isfile(pp):
                bad.append(('missing', f['path'])); continue
            bb = open(pp, 'rb').read()
            if hashlib.sha256(bb).hexdigest() != f['sha256'] or len(bb) != f['bytes']:
                bad.append(('mismatch', f['path']))
        res['parentSnapshotVerified'] = not bad
        res['parentSnapshotBad'] = bad[:50]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 80 else f'{len(v)} items') for k, v in res.items()}, indent=1))
