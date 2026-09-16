"""Verify the source42 archive SHA-256 and every member (hash+length, regular files only, exact set vs the formal
manifest), then extract verified bytes into a fresh disposable copy DEST (refuses reuse).
usage: verify_archive_extract42.py DEST"""
import hashlib, json, os, sys, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
ARC = REV + 'candidate-source.v42.tar.gz'
M42 = REV + 'candidate-subject.v42.json'
WANT_ARC = '2423c7807b489ef9af199f6eb4c44cc8a42b53160555621cf4b6a65d56fcb4c6'
WANT_MAN = 'f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307'
DEST = sys.argv[1]
RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v42'

h = hashlib.sha256()
with open(ARC, 'rb') as f:
    for c in iter(lambda: f.read(1 << 20), b''):
        h.update(c)
res = {'archive': ARC, 'archiveSha256': h.hexdigest()}
res['archiveShaMatches'] = res['archiveSha256'] == WANT_ARC
raw = open(M42, 'rb').read()
res['manifestSha256'] = hashlib.sha256(raw).hexdigest()
assert res['manifestSha256'] == WANT_MAN and res['archiveShaMatches'], res
man = {r['path']: r for r in json.loads(raw)['files']}
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
        if hashlib.sha256(data).hexdigest() != man[rel]['sha256'] or len(data) != man[rel]['bytes']:
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
