"""Verify LIVE source38 manifest, frozen snapshot (every member hash+length, no extras), parent37 manifest,
and compute the exact 37->38 delta (changed/added/removed/unchanged with before/after SHA-256)."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v38'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
M38 = REV + 'candidate-subject.v38.json'
M37 = REV + 'candidate-subject.v37.json'
S38 = '/tmp/opensip-design-corrections/candidate-subject.v38'
WANT38 = '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5'
WANT37 = '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'


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


res = {}
raw38 = open(M38, 'rb').read()
raw37 = open(M37, 'rb').read()
res['manifest38Sha256'] = hashlib.sha256(raw38).hexdigest()
res['manifest37Sha256'] = hashlib.sha256(raw37).hexdigest()
res['manifest38Matches'] = res['manifest38Sha256'] == WANT38
res['manifest37Matches'] = res['manifest37Sha256'] == WANT37
m38 = json.loads(raw38)
m37 = json.loads(raw37)
res['manifest38TopKeys'] = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__) for k, v in m38.items()} if isinstance(m38, dict) else None
r38 = {r['path']: r for r in rows(m38)}
r37 = {r['path']: r for r in rows(m37)}
res['fileCount38'] = len(r38)
res['totalBytes38'] = sum(r.get('bytes', 0) for r in r38.values())
bad, missing = [], []
for p, r in r38.items():
    fp = os.path.join(S38, p)
    if not os.path.isfile(fp):
        missing.append(p)
        continue
    h, n = sha_file(fp)
    if h != r['sha256'] or ('bytes' in r and n != r['bytes']):
        bad.append(p)
extra = []
for dp, ds, fs in os.walk(S38):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), S38)
        if rel not in r38:
            extra.append(rel)
res['snapshot'] = {'mismatches': bad, 'missing': missing, 'unlisted': extra, 'verified': not (bad or missing or extra)}
changed = sorted(p for p in r38 if p in r37 and r38[p]['sha256'] != r37[p]['sha256'])
added = sorted(p for p in r38 if p not in r37)
removed = sorted(p for p in r37 if p not in r38)
res['delta'] = {
    'changed': [{'path': p, 'sha37': r37[p]['sha256'], 'sha38': r38[p]['sha256'], 'bytes37': r37[p].get('bytes'), 'bytes38': r38[p].get('bytes')} for p in changed],
    'added': [{'path': p, 'sha38': r38[p]['sha256'], 'bytes38': r38[p].get('bytes')} for p in added],
    'removed': removed,
    'counts': {'changed': len(changed), 'added': len(added), 'removed': len(removed), 'unchanged': len(r38) - len(changed) - len(added)},
}
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/subject-verification.json', 'w'), indent=1)
json.dump({p: r['sha256'] for p, r in r38.items()}, open(RT + '/receipts/manifest38-index.json', 'w'))
out = dict(res)
out['delta'] = {'counts': res['delta']['counts'], 'changed': changed, 'added': added, 'removed': removed}
print(json.dumps(out, indent=1))
