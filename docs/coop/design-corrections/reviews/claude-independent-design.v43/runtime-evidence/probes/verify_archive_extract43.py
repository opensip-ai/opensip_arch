"""Verify a frozen archive (source43 header-bound; source42 against its formal manifest) and every member (hash+length,
regular files only, exact set), then extract verified bytes into a fresh disposable copy DEST (refuses reuse).
usage: verify_archive_extract43.py VERSION DEST"""
import hashlib, json, os, sys, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
WANT = {'43': ('db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d', 'd1ff8312d6a5540a977e54cfe8e24dd4865f8b09e6c432e42fd0d651387b66fa'),
        '42': ('f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307', '2423c7807b489ef9af199f6eb4c44cc8a42b53160555621cf4b6a65d56fcb4c6')}
RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v43'
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
