"""Verify the source40 archive SHA-256 and every member (hash+length, regular files only, exact set vs the formal
manifest), then extract verified bytes into a fresh disposable copy DEST (refuses reuse).
usage: verify_archive_extract.py DEST"""
import hashlib, json, os, sys, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
ARC = REV + 'candidate-source.v40.tar.gz'
M40 = REV + 'candidate-subject.v40.json'
WANT_ARC = 'e9980bc4d30294380c2bb3b91d2d331419db615a7b1b6f41107c7298ba249814'
WANT_MAN = '3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072'
DEST = sys.argv[1]
RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v40'


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x


h = hashlib.sha256()
with open(ARC, 'rb') as f:
    for c in iter(lambda: f.read(1 << 20), b''):
        h.update(c)
res = {'archive': ARC, 'archiveSha256': h.hexdigest()}
res['archiveShaMatches'] = res['archiveSha256'] == WANT_ARC
raw = open(M40, 'rb').read()
res['manifestSha256'] = hashlib.sha256(raw).hexdigest()
assert res['manifestSha256'] == WANT_MAN and res['archiveShaMatches'], res
man = {r['path']: r for r in rows(json.loads(raw))}
if os.path.exists(DEST):
    sys.exit('refusing to reuse ' + DEST)
os.makedirs(DEST)
seen, mism, nonreg, extra, dup, prefix = set(), [], [], [], [], None
with tarfile.open(ARC, 'r:gz') as t:
    for m in t:
        name = m.name
        if m.isdir():
            continue
        if not m.isfile():
            nonreg.append(name)
            continue
        rel = name
        if rel not in man:
            parts = rel.split('/', 1)
            if len(parts) == 2 and parts[1] in man:
                prefix = parts[0]
                rel = parts[1]
        if rel not in man or '..' in rel.split('/') or rel.startswith('/'):
            extra.append(name)
            continue
        if rel in seen:
            dup.append(rel)
            continue
        data = t.extractfile(m).read()
        if hashlib.sha256(data).hexdigest() != man[rel]['sha256'] or ('bytes' in man[rel] and len(data) != man[rel]['bytes']):
            mism.append(rel)
            continue
        out = os.path.join(DEST, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'wb') as o:
            o.write(data)
        seen.add(rel)
missing = sorted(set(man) - seen)
res.update({'manifestFileCount': len(man), 'membersMatched': len(seen), 'mismatches': mism, 'missing': missing,
            'extraMembers': extra, 'duplicateMembers': dup, 'nonRegularMembers': nonreg, 'leadingPrefix': prefix, 'extractedTo': DEST,
            'verified': not (mism or missing or extra or nonreg or dup) and len(seen) == len(man)})
name = os.path.basename(DEST.rstrip('/'))
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/archive-verification.' + name + '.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'missing'} | {'missingCount': len(missing)}, indent=1))
