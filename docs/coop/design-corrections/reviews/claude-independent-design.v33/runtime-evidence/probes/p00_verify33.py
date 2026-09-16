"""P00 — full custody of source33: manifest sha, archive sha AND archive-to-manifest equality,
every row hash+size, no extras, and parent32 ancestry."""
import hashlib, json, os, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
MAN = os.path.join(REV, 'candidate-subject.v33.json')
ARC = os.path.join(REV, 'candidate-source.v33.tar.gz')
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v33/receipts'
os.makedirs(OUT, exist_ok=True)
EXP_MAN = '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299'
EXP_ARC = 'a37076936fa1a124da83d7ecec7b8ebba3c5437962dd0ae857964d7a4f4114c7'
EXP_FILES, EXP_BYTES = 12899, 736764309
MY32 = '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R = {}
R['manifestSha256'] = sha(MAN)
R['manifestMatchesDeclared'] = R['manifestSha256'] == EXP_MAN
R['archiveSha256'] = sha(ARC)
R['archiveMatchesDeclared'] = R['archiveSha256'] == EXP_ARC
print('manifest sha matches:', R['manifestMatchesDeclared'])
print('archive  sha matches:', R['archiveMatchesDeclared'])

m = json.load(open(MAN))
files = m['files']
R['declaredFileCount'] = len(files)
R['fileCountMatches'] = len(files) == EXP_FILES
R['declaredTotalBytes'] = sum(f['bytes'] for f in files)
R['totalBytesMatches'] = R['declaredTotalBytes'] == EXP_BYTES
R['parentManifestSha256'] = m.get('parentManifestSha256')
R['parentIsMyV32'] = m.get('parentManifestSha256') == MY32
print('files %d (%s) bytes %d (%s)' % (len(files), R['fileCountMatches'],
                                       R['declaredTotalBytes'], R['totalBytesMatches']))
print('declared parent is the source32 I graded:', R['parentIsMyV32'])

miss, badh, bads, total = [], [], [], 0
listed = set()
for f in files:
    p = os.path.join(SRC, f['path'])
    listed.add(f['path'])
    if not os.path.isfile(p):
        miss.append(f['path'])
        continue
    st = os.path.getsize(p)
    total += st
    if st != f['bytes']:
        bads.append(f['path'])
        continue
    if sha(p) != f['sha256']:
        badh.append(f['path'])
extras = []
for dp, dn, fn in os.walk(SRC):
    for n in fn:
        rel = os.path.relpath(os.path.join(dp, n), SRC)
        if rel not in listed:
            extras.append(rel)
R.update(filesChecked=len(files), measuredTotalBytes=total, missingCount=len(miss),
         hashMismatchCount=len(badh), sizeMismatchCount=len(bads), extrasCount=len(extras),
         missing=miss[:8], hashMismatches=badh[:8], extras=extras[:8])
R['measuredBytesMatch'] = total == EXP_BYTES
print('missing/hashbad/sizebad/extras: %d/%d/%d/%d measured=%d (%s)'
      % (len(miss), len(badh), len(bads), len(extras), total, R['measuredBytesMatch']))

arc_rows, arc_bad, arc_extra = 0, [], []
by_path = {f['path']: f for f in files}
seen = set()
with tarfile.open(ARC, 'r:gz') as tf:
    for ti in tf:
        if not ti.isfile():
            continue
        arc_rows += 1
        name = ti.name
        for pre in ('./', 'candidate-subject.v33/', 'source/'):
            if name.startswith(pre):
                name = name[len(pre):]
                break
        seen.add(name)
        rec = by_path.get(name)
        if rec is None:
            arc_extra.append(name)
            continue
        data = tf.extractfile(ti).read()
        if hashlib.sha256(data).hexdigest() != rec['sha256'] or len(data) != rec['bytes']:
            arc_bad.append(name)
R['archiveFileRows'] = arc_rows
R['archiveMismatchCount'] = len(arc_bad)
R['archiveNotInManifest'] = arc_extra[:8]
R['archiveAbsentFromArchive'] = sorted(set(by_path) - seen)[:8]
R['archiveEqualsManifest'] = not arc_bad and not arc_extra and not (set(by_path) - seen)
print('archive members %d | mismatches %d | not-in-manifest %d | absent %d | equals manifest: %s'
      % (arc_rows, len(arc_bad), len(arc_extra), len(set(by_path) - seen), R['archiveEqualsManifest']))

R['ALL_VERIFIED'] = all([R['manifestMatchesDeclared'], R['archiveMatchesDeclared'],
                         R['fileCountMatches'], R['totalBytesMatches'], R['measuredBytesMatch'],
                         not miss, not badh, not bads, not extras,
                         R['parentIsMyV32'], R['archiveEqualsManifest']])
print('\nALL_VERIFIED:', R['ALL_VERIFIED'])
json.dump(R, open(os.path.join(OUT, 'p00-verify33.json'), 'w'), indent=1)
