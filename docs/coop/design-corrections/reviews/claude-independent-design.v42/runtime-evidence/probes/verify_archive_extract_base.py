"""Verify a historical frozen archive (source40 or source41) against its formal manifest (every member hash+length, regular
files only, exact set), then extract verified bytes into a fresh disposable copy DEST (refuses reuse). Used only to import
each tree's own owner modules in old-versus-new discrimination probes.
usage: verify_archive_extract_base.py VERSION DEST"""
import hashlib, json, os, sys, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
WANT = {'40': ('3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072', 'e9980bc4d30294380c2bb3b91d2d331419db615a7b1b6f41107c7298ba249814'),
        '41': ('eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236', None)}
RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v42'
version, DEST = sys.argv[1], sys.argv[2]
ARC = REV + 'candidate-source.v%s.tar.gz' % version
MAN = REV + 'candidate-subject.v%s.json' % version
want_man, want_arc = WANT[version]
h = hashlib.sha256()
with open(ARC, 'rb') as f:
    for c in iter(lambda: f.read(1 << 20), b''):
        h.update(c)
raw = open(MAN, 'rb').read()
res = {'version': version, 'archive': ARC, 'archiveSha256': h.hexdigest(), 'archiveExpected': want_arc,
       'archiveShaMatches': (h.hexdigest() == want_arc) if want_arc else None, 'manifestSha256': hashlib.sha256(raw).hexdigest()}
assert res['manifestSha256'] == want_man and res['archiveShaMatches'] is not False, res
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
res.update({'manifestFileCount': len(man), 'membersMatched': len(seen), 'mismatches': mism, 'missingCount': len(missing),
            'extraMembers': extra, 'duplicateMembers': dup, 'nonRegularMembers': nonreg, 'extractedTo': DEST,
            'verified': not (mism or missing or extra or nonreg or dup) and len(seen) == len(man)})
json.dump(res, open(RT + '/receipts/archive-verification.base' + version + '.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
