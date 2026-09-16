"""Verify the formal frozen source39 manifest, the snapshot (every member hash+length, no unlisted files), the
parent38 formal manifest AND parent38 snapshot (still unchanged), and compute the exact 38->39 delta."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v39'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
M39 = REV + 'candidate-subject.v39.json'
M38 = REV + 'candidate-subject.v38.json'
S39 = '/tmp/opensip-design-corrections/candidate-subject.v39'
S38 = '/tmp/opensip-design-corrections/candidate-subject.v38'
WANT39 = 'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009'
WANT38 = '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5'


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
raw39 = open(M39, 'rb').read()
raw38 = open(M38, 'rb').read()
res['manifest39Path'] = M39
res['manifest39Sha256'] = hashlib.sha256(raw39).hexdigest()
res['manifest38Sha256'] = hashlib.sha256(raw38).hexdigest()
res['manifest39Matches'] = res['manifest39Sha256'] == WANT39
res['manifest38Matches'] = res['manifest38Sha256'] == WANT38
m39 = json.loads(raw39)
m38 = json.loads(raw38)
res['manifest39TopKeys'] = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__) for k, v in m39.items()} if isinstance(m39, dict) else None
r39 = {r['path']: r for r in rows(m39)}
r38 = {r['path']: r for r in rows(m38)}
res['fileCount39'] = len(r39)
res['totalBytes39'] = sum(r.get('bytes', 0) for r in r39.values())
res['declaredFileCount39'] = m39.get('fileCount')
res['declaredTotalBytes39'] = m39.get('totalBytes')
res['parentDeclared'] = m39.get('parentManifestSha256')
res['snapshot39'] = verify_tree(S39, r39)
res['snapshot38'] = verify_tree(S38, r38)
changed = sorted(p for p in r39 if p in r38 and r39[p]['sha256'] != r38[p]['sha256'])
added = sorted(p for p in r39 if p not in r38)
removed = sorted(p for p in r38 if p not in r39)
res['delta'] = {
    'changed': [{'path': p, 'sha38': r38[p]['sha256'], 'sha39': r39[p]['sha256'], 'bytes38': r38[p].get('bytes'), 'bytes39': r39[p].get('bytes')} for p in changed],
    'added': [{'path': p, 'sha39': r39[p]['sha256'], 'bytes39': r39[p].get('bytes')} for p in added],
    'removed': [{'path': p, 'sha38': r38[p]['sha256']} for p in removed],
    'counts': {'changed': len(changed), 'added': len(added), 'removed': len(removed), 'unchanged': len(r39) - len(changed) - len(added)},
}
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/subject-verification.json', 'w'), indent=1)
json.dump({p: r['sha256'] for p, r in r39.items()}, open(RT + '/receipts/manifest39-index.json', 'w'))
out = dict(res)
out['snapshot39'] = {k: (v if not isinstance(v, list) else v[:20]) for k, v in res['snapshot39'].items()}
out['snapshot38'] = {k: (v if not isinstance(v, list) else v[:20]) for k, v in res['snapshot38'].items()}
out['delta'] = {'counts': res['delta']['counts'], 'changed': changed, 'added': added, 'removed': removed}
print(json.dumps(out, indent=1))
