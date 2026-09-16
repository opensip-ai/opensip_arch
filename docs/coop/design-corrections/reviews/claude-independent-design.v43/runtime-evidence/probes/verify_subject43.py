"""Verify the formal frozen source43 manifest and snapshot (every member hash+length, no unlisted files), the immediate parent42
manifest+snapshot (still unchanged), the declared parent, and the exact 42->43 delta."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v43'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
B = '/tmp/opensip-design-corrections/'
SUBJ = {
    '43': (REV + 'candidate-subject.v43.json', B + 'candidate-subject.v43', 'db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d'),
    '42': (REV + 'candidate-subject.v42.json', B + 'candidate-subject.v42', 'f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307'),
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
res['parentChain'] = {'43declares42': docs['43']['parentManifestSha256'] == raw_sha['42']}
res['counts43'] = {'fileCount': len(rows['43']), 'totalBytes': sum(r['bytes'] for r in rows['43'].values()),
                   'matchesDeclared': len(rows['43']) == docs['43']['fileCount'] and sum(r['bytes'] for r in rows['43'].values()) == docs['43']['totalBytes'],
                   'matchesHeader': len(rows['43']) == 12913 and sum(r['bytes'] for r in rows['43'].values()) == 737769489}
ra, rb = rows['42'], rows['43']
changed = sorted(p for p in rb if p in ra and rb[p]['sha256'] != ra[p]['sha256'])
added = sorted(p for p in rb if p not in ra)
removed = sorted(p for p in ra if p not in rb)
res['delta'] = {'42to43': {
    'changed': [{'path': p, 'shaA': ra[p]['sha256'], 'shaB': rb[p]['sha256'], 'bytesA': ra[p]['bytes'], 'bytesB': rb[p]['bytes']} for p in changed],
    'added': [{'path': p, 'shaB': rb[p]['sha256'], 'bytesB': rb[p]['bytes']} for p in added],
    'removed': [{'path': p, 'shaA': ra[p]['sha256'], 'bytesA': ra[p]['bytes']} for p in removed],
    'counts': {'changed': len(changed), 'added': len(added), 'removed': len(removed), 'unchanged': len(rb) - len(changed) - len(added)}}}
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/subject-verification.json', 'w'), indent=1)
json.dump({p: r['sha256'] for p, r in rows['43'].items()}, open(RT + '/receipts/manifest43-index.json', 'w'))
out = {k: v for k, v in res.items() if k != 'delta'}
for k in ('snapshot43', 'snapshot42'):
    out[k] = {a: (b if not isinstance(b, list) else b[:10]) for a, b in res[k].items()}
out['delta'] = {'counts': res['delta']['42to43']['counts'], 'changed': changed, 'added': added, 'removed': removed}
print(json.dumps(out, indent=1))
