"""Probe 01 — derive the exact source26 -> source27 delta from the two frozen manifests,
independently of any author statement."""
import hashlib, json, os

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
M26 = os.path.join(REV, 'candidate-subject.v26.json')
M27 = os.path.join(REV, 'candidate-subject.v27.json')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)

b26 = open(M26, 'rb').read()
b27 = open(M27, 'rb').read()
m26, m27 = json.loads(b26), json.loads(b27)
res = {
    'manifest26Sha256': hashlib.sha256(b26).hexdigest(),
    'manifest27Sha256': hashlib.sha256(b27).hexdigest(),
    'manifest26MatchesMyReviewedSubject':
        hashlib.sha256(b26).hexdigest() == 'c9a6c26a82dbe24acfbba423360be54e45f11325576b172d75a005ec35d0ffb2',
    'declaredParentOf27': m27['parentManifestSha256'],
    'ancestryChainVerified':
        m27['parentManifestSha256'] == hashlib.sha256(b26).hexdigest(),
    'fileCount26': m26['fileCount'], 'fileCount27': m27['fileCount'],
    'totalBytes26': m26['totalBytes'], 'totalBytes27': m27['totalBytes'],
}
a = {r['path']: r for r in m26['files']}
b = {r['path']: r for r in m27['files']}
added = sorted(set(b) - set(a))
removed = sorted(set(a) - set(b))
changed = sorted(p for p in (set(a) & set(b)) if a[p]['sha256'] != b[p]['sha256'])
res['addedCount'] = len(added)
res['removedCount'] = len(removed)
res['changedCount'] = len(changed)
res['added'] = [{'path': p, 'bytes': b[p]['bytes'], 'sha256': b[p]['sha256']} for p in added]
res['removed'] = [{'path': p, 'bytes': a[p]['bytes'], 'sha256': a[p]['sha256']} for p in removed]
res['changed'] = [{'path': p,
                   'bytes26': a[p]['bytes'], 'sha26': a[p]['sha256'],
                   'bytes27': b[p]['bytes'], 'sha27': b[p]['sha256'],
                   'byteDelta': b[p]['bytes'] - a[p]['bytes']} for p in changed]
res['netBytes'] = m27['totalBytes'] - m26['totalBytes']
res['deltaTouchesReviewsTree'] = sorted(
    p for p in added + removed + changed if '/reviews/' in p)

json.dump(res, open(os.path.join(OUT, 'p01-delta.json'), 'w'), indent=1)
print('ancestry chain verified:', res['ancestryChainVerified'])
print('files 26->27: %d -> %d   bytes %d -> %d (net %+d)' % (
    res['fileCount26'], res['fileCount27'], res['totalBytes26'], res['totalBytes27'], res['netBytes']))
print('added=%d removed=%d changed=%d' % (len(added), len(removed), len(changed)))
print('\n--- ADDED ---')
for r in res['added']:
    print('  %-78s %8d  %s' % (r['path'], r['bytes'], r['sha256'][:16]))
print('\n--- REMOVED ---')
for r in res['removed']:
    print('  %-78s %8d' % (r['path'], r['bytes']))
print('\n--- CHANGED ---')
for r in res['changed']:
    print('  %-78s %+7d  %s -> %s' % (r['path'], r['byteDelta'], r['sha26'][:12], r['sha27'][:12]))
