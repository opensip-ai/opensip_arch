"""Verify the formal frozen source42 manifest and snapshot (every member hash+length, no unlisted files), the immediate
parent41 manifest+snapshot and the last independently reviewed source40 manifest+snapshot (both still unchanged), the
declared parent chain, and the exact deltas 41->42, 40->42 and 40->41."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v42'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
B = '/tmp/opensip-design-corrections/'
SUBJ = {
    '42': (REV + 'candidate-subject.v42.json', B + 'candidate-subject.v42', 'f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307'),
    '41': (REV + 'candidate-subject.v41.json', B + 'candidate-subject.v41', None),
    '40': (REV + 'candidate-subject.v40.json', B + 'candidate-subject.v40', '3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072'),
}


def sha_file(p):
    h = hashlib.sha256()
    n = 0
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
    extra = []
    for dp, ds, fs in os.walk(root):
        for f in fs:
            rel = os.path.relpath(os.path.join(dp, f), root)
            if rel not in man:
                extra.append(rel)
    return {'mismatches': bad, 'missing': missing, 'unlisted': extra, 'verified': not (bad or missing or extra), 'members': len(man),
            'totalBytes': sum(r['bytes'] for r in man.values())}


res, rows, raw_sha, docs = {}, {}, {}, {}
for v, (mp, sp, want) in SUBJ.items():
    raw = open(mp, 'rb').read()
    raw_sha[v] = hashlib.sha256(raw).hexdigest()
    docs[v] = json.loads(raw)
    rows[v] = {r['path']: r for r in docs[v]['files']}
    res['manifest' + v] = {'path': mp, 'sha256': raw_sha[v], 'expected': want, 'matchesHeader': (raw_sha[v] == want) if want else None,
                           'declaredParent': docs[v].get('parentManifestSha256'), 'declaredFileCount': docs[v].get('fileCount'),
                           'declaredTotalBytes': docs[v].get('totalBytes'), 'snapshotRootDeclared': docs[v].get('snapshotRoot'),
                           'topKeys': {k: (x if not isinstance(x, (list, dict)) else type(x).__name__) for k, x in docs[v].items()}}
    res['snapshot' + v] = verify_tree(sp, rows[v])
res['parentChain'] = {'42declares41': docs['42']['parentManifestSha256'] == raw_sha['41'], '41declares40': docs['41']['parentManifestSha256'] == raw_sha['40']}
res['counts42'] = {'fileCount': len(rows['42']), 'totalBytes': sum(r['bytes'] for r in rows['42'].values()),
                   'matchesDeclared': len(rows['42']) == docs['42']['fileCount'] and sum(r['bytes'] for r in rows['42'].values()) == docs['42']['totalBytes'],
                   'matchesHeader': len(rows['42']) == 12913 and sum(r['bytes'] for r in rows['42'].values()) == 737766584}


def delta(a, b):
    ra, rb = rows[a], rows[b]
    changed = sorted(p for p in rb if p in ra and rb[p]['sha256'] != ra[p]['sha256'])
    added = sorted(p for p in rb if p not in ra)
    removed = sorted(p for p in ra if p not in rb)
    return {'changed': [{'path': p, 'shaA': ra[p]['sha256'], 'shaB': rb[p]['sha256'], 'bytesA': ra[p]['bytes'], 'bytesB': rb[p]['bytes']} for p in changed],
            'added': [{'path': p, 'shaB': rb[p]['sha256'], 'bytesB': rb[p]['bytes']} for p in added],
            'removed': [{'path': p, 'shaA': ra[p]['sha256'], 'bytesA': ra[p]['bytes']} for p in removed],
            'counts': {'changed': len(changed), 'added': len(added), 'removed': len(removed), 'unchanged': len(rb) - len(changed) - len(added)}}


res['delta'] = {'41to42': delta('41', '42'), '40to42': delta('40', '42'), '40to41': delta('40', '41')}
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/subject-verification.json', 'w'), indent=1)
json.dump({p: r['sha256'] for p, r in rows['42'].items()}, open(RT + '/receipts/manifest42-index.json', 'w'))
out = {k: v for k, v in res.items() if k != 'delta'}
for k in ('snapshot42', 'snapshot41', 'snapshot40'):
    out[k] = {a: (b if not isinstance(b, list) else b[:10]) for a, b in res[k].items()}
out['delta'] = {k: {'counts': d['counts'], 'changed': [c['path'] for c in d['changed']], 'added': [c['path'] for c in d['added']], 'removed': [c['path'] for c in d['removed']]}
                for k, d in res['delta'].items()}
print(json.dumps(out, indent=1))
