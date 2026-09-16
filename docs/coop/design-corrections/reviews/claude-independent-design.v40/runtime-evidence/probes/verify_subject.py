"""Verify the formal frozen source40 manifest, the snapshot (every member hash+length, no unlisted files), the
parent39 formal manifest AND parent39 snapshot (still unchanged), and compute the exact 39->40 delta."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v40'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
M40 = REV + 'candidate-subject.v40.json'
M39 = REV + 'candidate-subject.v39.json'
S40 = '/tmp/opensip-design-corrections/candidate-subject.v40'
S39 = '/tmp/opensip-design-corrections/candidate-subject.v39'
WANT40 = '3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072'
WANT39 = 'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009'


def sha_file(p):
    h = hashlib.sha256()
    n = 0
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
            n += len(c)
    return h.hexdigest(), n


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x


def verify_tree(root, man):
    bad, missing = [], []
    for p, r in man.items():
        fp = os.path.join(root, p)
        if not os.path.isfile(fp) or os.path.islink(fp):
            missing.append(p)
            continue
        h, n = sha_file(fp)
        if h != r['sha256'] or ('bytes' in r and n != r['bytes']):
            bad.append(p)
    extra = []
    for dp, ds, fs in os.walk(root):
        for f in fs:
            rel = os.path.relpath(os.path.join(dp, f), root)
            if rel not in man:
                extra.append(rel)
    return {'mismatches': bad, 'missing': missing, 'unlisted': extra, 'verified': not (bad or missing or extra), 'members': len(man)}


res = {}
raw40 = open(M40, 'rb').read()
raw39 = open(M39, 'rb').read()
res['manifest40Path'] = M40
res['manifest40Sha256'] = hashlib.sha256(raw40).hexdigest()
res['manifest39Sha256'] = hashlib.sha256(raw39).hexdigest()
res['manifest40Matches'] = res['manifest40Sha256'] == WANT40
res['manifest39Matches'] = res['manifest39Sha256'] == WANT39
m40 = json.loads(raw40)
m39 = json.loads(raw39)
res['manifest40TopKeys'] = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__) for k, v in m40.items()} if isinstance(m40, dict) else None
r40 = {r['path']: r for r in rows(m40)}
r39 = {r['path']: r for r in rows(m39)}
res['fileCount40'] = len(r40)
res['totalBytes40'] = sum(r.get('bytes', 0) for r in r40.values())
res['declaredFileCount40'] = m40.get('fileCount')
res['declaredTotalBytes40'] = m40.get('totalBytes')
res['parentDeclared'] = m40.get('parentManifestSha256')
res['snapshot40'] = verify_tree(S40, r40)
res['snapshot39'] = verify_tree(S39, r39)
changed = sorted(p for p in r40 if p in r39 and r40[p]['sha256'] != r39[p]['sha256'])
added = sorted(p for p in r40 if p not in r39)
removed = sorted(p for p in r39 if p not in r40)
res['delta'] = {
    'changed': [{'path': p, 'sha39': r39[p]['sha256'], 'sha40': r40[p]['sha256'], 'bytes39': r39[p].get('bytes'), 'bytes40': r40[p].get('bytes')} for p in changed],
    'added': [{'path': p, 'sha40': r40[p]['sha256'], 'bytes40': r40[p].get('bytes')} for p in added],
    'removed': [{'path': p, 'sha39': r39[p]['sha256']} for p in removed],
    'counts': {'changed': len(changed), 'added': len(added), 'removed': len(removed), 'unchanged': len(r40) - len(changed) - len(added)},
}
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/subject-verification.json', 'w'), indent=1)
json.dump({p: r['sha256'] for p, r in r40.items()}, open(RT + '/receipts/manifest40-index.json', 'w'))
out = dict(res)
out['snapshot40'] = {k: (v if not isinstance(v, list) else v[:20]) for k, v in res['snapshot40'].items()}
out['snapshot39'] = {k: (v if not isinstance(v, list) else v[:20]) for k, v in res['snapshot39'].items()}
out['delta'] = {'counts': res['delta']['counts'], 'changed': changed, 'added': added, 'removed': removed}
print(json.dumps(out, indent=1))
