"""Verify the source37 archive hash, compare EVERY member against the manifest, and extract a
disposable exact copy for running checkers that write reports relative to their code."""
import hashlib, json, os, sys, tarfile

ARCHIVE = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-source.v37.tar.gz'
ARCHIVE_SHA = 'f840507695e310811656a167cbef96b7e3c5ea43d400d0ecf61ef5088d659920'
MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
MANIFEST_SHA = '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v37'
DEST = sys.argv[1] if len(sys.argv) > 1 else BASE + '/work/source37'
OUT = BASE + '/receipts/archive-verification.json'

h = hashlib.sha256()
with open(ARCHIVE, 'rb') as fh:
    for ch in iter(lambda: fh.read(1 << 20), b''):
        h.update(ch)
archive_sha = h.hexdigest()
raw = open(MANIFEST, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == MANIFEST_SHA
m = json.loads(raw)
want = {f['path']: (f['sha256'], f['bytes']) for f in m['files']}
seen, bad, extra, nonregular, prefix = {}, [], [], [], None
os.makedirs(DEST, exist_ok=False)
with tarfile.open(ARCHIVE, 'r:gz') as tf:
    for mem in tf:
        name = mem.name
        if mem.isdir():
            continue
        if not mem.isfile():
            nonregular.append(name); continue
        # tolerate a single leading directory component if present
        rel = name
        if rel not in want:
            parts = rel.split('/', 1)
            if len(parts) == 2 and parts[1] in want:
                prefix = parts[0]; rel = parts[1]
        if rel.startswith('/') or '..' in rel.split('/'):
            bad.append({'member': name, 'state': 'unsafe-path'}); continue
        data = tf.extractfile(mem).read()
        d = hashlib.sha256(data).hexdigest()
        if rel not in want:
            extra.append(name); continue
        if rel in seen:
            bad.append({'member': name, 'state': 'duplicate'}); continue
        seen[rel] = True
        if (d, len(data)) != want[rel]:
            bad.append({'member': name, 'state': 'mismatch'})
        p = os.path.join(DEST, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as out:
            out.write(data)
        os.chmod(p, mem.mode & 0o755 | 0o600)
missing = sorted(set(want) - set(seen))
res = {'archive': ARCHIVE, 'archiveSha256': archive_sha, 'archiveShaMatches': archive_sha == ARCHIVE_SHA,
       'manifestSha256': MANIFEST_SHA, 'manifestFileCount': m['fileCount'], 'membersMatched': len(seen),
       'mismatches': bad, 'missing': missing, 'extraMembers': extra, 'nonRegularMembers': nonregular,
       'leadingPrefix': prefix, 'extractedTo': DEST}
res['verified'] = res['archiveShaMatches'] and not bad and not missing and not extra and len(seen) == m['fileCount']
os.makedirs(os.path.dirname(OUT), exist_ok=True)
if os.path.basename(DEST) == 'source37':
    json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items()}, indent=1)[:3000])
