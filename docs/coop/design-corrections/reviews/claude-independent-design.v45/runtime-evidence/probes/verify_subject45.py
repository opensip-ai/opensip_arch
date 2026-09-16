"""Verify the formal frozen source45 manifest and snapshot (every member hash+length, no unlisted files), the immediate parent44
manifest+snapshot (still unchanged), the declared parent, header counts, and the exact 44->45 delta."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v45'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
B = '/tmp/opensip-design-corrections/'
SUBJ = {
    '45': (REV + 'candidate-subject.v45.json', B + 'candidate-subject.v45', '8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155'),
    '44': (REV + 'candidate-subject.v44.json', B + 'candidate-subject.v44', 'e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b'),
}


def sha_file(p):
    h, n = hashlib.sha256(), 0
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
            n += len(c)
    return h.hexdigest(), n


def verify_tree(root, man):
    bad, missing = [], []
    for p, r in man.items():
        fp = os.path.join(root, p)
        if not os.path.isfile(fp) or os.path.islink(fp):
            missing.append(p)
            continue
        h, n = sha_file(fp)
        if h != r['sha256'] or n != r['bytes']:
            bad.append(p)
    extra = [os.path.relpath(os.path.join(dp, f), root) for dp, ds, fs in os.walk(root) for f in fs if os.path.relpath(os.path.join(dp, f), root) not in man]
    return {'mismatches': bad, 'missing': missing, 'unlisted': extra, 'verified': not (bad or missing or extra), 'members': len(man),
            'totalBytes': sum(r['bytes'] for r in man.values())}


res, rows, raw_sha, docs = {}, {}, {}, {}
for v, (mp, sp, want) in SUBJ.items():
    raw = open(mp, 'rb').read()
    raw_sha[v] = hashlib.sha256(raw).hexdigest()
    docs[v] = json.loads(raw)
    rows[v] = {r['path']: r for r in docs[v]['files']}
    res['manifest' + v] = {'path': mp, 'sha256': raw_sha[v], 'expected': want, 'matchesHeader': raw_sha[v] == want,
                           'declaredParent': docs[v].get('parentManifestSha256'), 'declaredFileCount': docs[v].get('fileCount'),
                           'declaredTotalBytes': docs[v].get('totalBytes'), 'snapshotRootDeclared': docs[v].get('snapshotRoot'),
                           'topKeys': {k: (x if not isinstance(x, (list, dict)) else type(x).__name__) for k, x in docs[v].items()}}
    res['snapshot' + v] = verify_tree(sp, rows[v])
res['parentChain'] = {'45declares44': docs['45']['parentManifestSha256'] == raw_sha['44']}
res['counts45'] = {'fileCount': len(rows['45']), 'totalBytes': sum(r['bytes'] for r in rows['45'].values()),
                   'matchesDeclared': len(rows['45']) == docs['45']['fileCount'] and sum(r['bytes'] for r in rows['45'].values()) == docs['45']['totalBytes'],
                   'matchesHeader': len(rows['45']) == 12920 and sum(r['bytes'] for r in rows['45'].values()) == 738315211}
ra, rb = rows['44'], rows['45']
changed = sorted(p for p in rb if p in ra and rb[p]['sha256'] != ra[p]['sha256'])
added = sorted(p for p in rb if p not in ra)
removed = sorted(p for p in ra if p not in rb)
res['delta'] = {'44to45': {
    'changed': [{'path': p, 'shaA': ra[p]['sha256'], 'shaB': rb[p]['sha256'], 'bytesA': ra[p]['bytes'], 'bytesB': rb[p]['bytes']} for p in changed],
    'added': [{'path': p, 'shaB': rb[p]['sha256'], 'bytesB': rb[p]['bytes']} for p in added],
    'removed': [{'path': p, 'shaA': ra[p]['sha256'], 'bytesA': ra[p]['bytes']} for p in removed],
    'counts': {'changed': len(changed), 'added': len(added), 'removed': len(removed), 'unchanged': len(rb) - len(changed) - len(added)},
    'matchesHeaderCounts': (len(changed), len(added), len(removed)) == (14, 1, 0)}}
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/subject-verification.json', 'w'), indent=1)
json.dump({p: r['sha256'] for p, r in rows['45'].items()}, open(RT + '/receipts/manifest45-index.json', 'w'))
json.dump({p: r['sha256'] for p, r in rows['44'].items()}, open(RT + '/receipts/manifest44-index.json', 'w'))
out = {k: v for k, v in res.items() if k != 'delta'}
for k in ('snapshot45', 'snapshot44'):
    out[k] = {a: (b if not isinstance(b, list) else b[:10]) for a, b in res[k].items()}
out['delta'] = {'counts': res['delta']['44to45']['counts'], 'matchesHeaderCounts': res['delta']['44to45']['matchesHeaderCounts'],
                'changed': [(c['path'], c['bytesA'], c['bytesB']) for c in res['delta']['44to45']['changed']], 'added': [(a['path'], a['bytesB']) for a in res['delta']['44to45']['added']], 'removed': removed}
print(json.dumps(out, indent=1))
