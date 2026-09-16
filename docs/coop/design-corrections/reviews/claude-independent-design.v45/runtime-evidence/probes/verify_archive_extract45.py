"""Verify a frozen archive (source45 header-bound; source44 against its formal manifest) and every member (hash+length,
regular files only, exact set), then extract verified bytes into a fresh disposable copy DEST (refuses reuse).
usage: verify_archive_extract45.py VERSION DEST"""
import hashlib, json, os, sys, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
WANT = {'45': ('8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155', '9536ebe3ffe27e2a99c7e02d8338738ae3d9a62a9000af4f3e5f5ce5793b909f'),
        '44': ('e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b', 'c21d04914eaa07df967eeb945170a21d8ec8c7bc3c98573085522fab74b52bd5')}
RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v45'
version, DEST = sys.argv[1], sys.argv[2]
ARC, MAN = REV + 'candidate-source.v%s.tar.gz' % version, REV + 'candidate-subject.v%s.json' % version
want_man, want_arc = WANT[version]
h = hashlib.sha256()
with open(ARC, 'rb') as f:
    for c in iter(lambda: f.read(1 << 20), b''):
        h.update(c)
raw = open(MAN, 'rb').read()
res = {'version': version, 'archive': ARC, 'archiveSha256': h.hexdigest(), 'archiveShaMatches': h.hexdigest() == want_arc,
       'manifestSha256': hashlib.sha256(raw).hexdigest()}
assert res['manifestSha256'] == want_man and res['archiveShaMatches'], res
man = {r['path']: r for r in json.loads(raw)['files']}
if os.path.exists(DEST):
    sys.exit('refusing to reuse ' + DEST)
os.makedirs(DEST)
seen, mism, nonreg, extra, dup = set(), [], [], [], []
with tarfile.open(ARC, 'r:gz') as t:
    for m in t:
        if m.isdir():
            continue
        if not m.isfile():
            nonreg.append(m.name)
            continue
        rel = m.name
        if rel not in man or '..' in rel.split('/') or rel.startswith('/'):
            extra.append(m.name)
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
res.update({'manifestFileCount': len(man), 'membersMatched': len(seen), 'mismatches': mism, 'missingCount': len(missing), 'extraMembers': extra,
            'duplicateMembers': dup, 'nonRegularMembers': nonreg, 'extractedTo': DEST, 'verified': not (mism or missing or extra or nonreg or dup) and len(seen) == len(man)})
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/archive-verification.' + os.path.basename(DEST.rstrip('/')) + '.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
