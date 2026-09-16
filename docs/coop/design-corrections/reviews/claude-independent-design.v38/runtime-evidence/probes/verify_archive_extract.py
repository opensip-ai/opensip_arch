"""Verify source38 archive SHA-256 and every member (hash+length, regular files only, exact set vs manifest),
then extract verified bytes to a fresh disposable copy DEST (refuses to reuse). usage: verify_archive_extract.py DEST"""
import hashlib, json, os, sys, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
ARC = REV + 'candidate-source.v38.tar.gz'
M38 = REV + 'candidate-subject.v38.json'
WANT_ARC = '571aad4d2038bcc02b13cfbab48d64ea1ce2255429badff5504432bb90175abd'
WANT_MAN = '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5'
DEST = sys.argv[1]
RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v38'


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
raw = open(M38, 'rb').read()
res['manifestSha256'] = hashlib.sha256(raw).hexdigest()
assert res['manifestSha256'] == WANT_MAN and res['archiveShaMatches']
man = {r['path']: r for r in rows(json.loads(raw))}
if os.path.exists(DEST):
    sys.exit('refusing to reuse ' + DEST)
os.makedirs(DEST)
seen, mism, nonreg, extra, prefix = set(), [], [], [], None
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
        if rel not in man:
            extra.append(name)
            continue
        data = t.extractfile(m).read()
        if hashlib.sha256(data).hexdigest() != man[rel]['sha256'] or ('bytes' in man[rel] and len(data) != man[rel]['bytes']):
            mism.append(rel)
            continue
        if '..' in rel.split('/') or rel.startswith('/'):
            extra.append(name)
            continue
        out = os.path.join(DEST, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'wb') as o:
            o.write(data)
        seen.add(rel)
missing = sorted(set(man) - seen)
res.update({'manifestFileCount': len(man), 'membersMatched': len(seen), 'mismatches': mism, 'missing': missing,
            'extraMembers': extra, 'nonRegularMembers': nonreg, 'leadingPrefix': prefix, 'extractedTo': DEST,
            'verified': not (mism or missing or extra or nonreg) and len(seen) == len(man)})
name = os.path.basename(DEST.rstrip('/'))
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/archive-verification.' + name + '.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'missing'} | {'missingCount': len(missing)}, indent=1))
