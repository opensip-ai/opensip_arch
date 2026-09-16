"""P00 — verify every declared input before reading anything, and prove ancestry from my v31.

Manifest sha, archive sha AND archive equality against the snapshot, every row hash+size, no extras,
and the declared parent chain reaching the exact v31 I graded.
"""
import hashlib, io, json, os, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
MAN = os.path.join(REV, 'candidate-subject.v32.json')
ARC = os.path.join(REV, 'candidate-source.v32.tar.gz')
SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
os.makedirs(OUT, exist_ok=True)

EXP_MAN = '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2'
EXP_ARC = 'acbc2bebe2d4aa311ffb767a2f1aa32132d8b6dc2aaad8f86b7cfe9b89a35d96'
EXP_FILES, EXP_BYTES = 12898, 736666114
MY31 = 'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5'


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
R['manifestTopKeys'] = sorted(m)
R['declaredFileCount'] = len(files)
R['fileCountMatches'] = len(files) == EXP_FILES
R['declaredTotalBytes'] = sum(f['bytes'] for f in files)
R['totalBytesMatches'] = R['declaredTotalBytes'] == EXP_BYTES
R['parentManifestSha256'] = m.get('parentManifestSha256')
R['parentIsMyV31'] = m.get('parentManifestSha256') == MY31
print('files %d (%s)  bytes %d (%s)' % (len(files), R['fileCountMatches'],
                                        R['declaredTotalBytes'], R['totalBytesMatches']))
print('declared parent is the exact v31 I graded:', R['parentIsMyV31'])

# ---- every row ----
miss, badh, bads = [], [], []
total = 0
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
         missing=miss[:10], hashMismatches=badh[:10], extras=extras[:10])
R['measuredBytesMatch'] = total == EXP_BYTES
print('missing/hashbad/sizebad/extras: %d/%d/%d/%d  measuredBytes=%d (%s)'
      % (len(miss), len(badh), len(bads), len(extras), total, R['measuredBytesMatch']))

# ---- archive equality against the snapshot ----
arc_rows, arc_bad, arc_extra = 0, [], []
man_by_path = {f['path']: f for f in files}
seen_arc = set()
with tarfile.open(ARC, 'r:gz') as tf:
    for ti in tf:
        if not ti.isfile():
            continue
        arc_rows += 1
        name = ti.name
        for pre in ('./', 'candidate-subject.v32/', 'source/'):
            if name.startswith(pre):
                name = name[len(pre):]
                break
        seen_arc.add(name)
        rec = man_by_path.get(name)
        if rec is None:
            arc_extra.append(name)
            continue
        data = tf.extractfile(ti).read()
        if hashlib.sha256(data).hexdigest() != rec['sha256'] or len(data) != rec['bytes']:
            arc_bad.append(name)
R['archiveFileRows'] = arc_rows
R['archiveMismatches'] = arc_bad[:10]
R['archiveMismatchCount'] = len(arc_bad)
R['archiveNotInManifest'] = arc_extra[:10]
R['archiveMissingFromArchive'] = sorted(set(man_by_path) - seen_arc)[:10]
R['archiveEqualsManifest'] = (not arc_bad and not arc_extra
                              and not (set(man_by_path) - seen_arc))
print('archive members %d | mismatches %d | not-in-manifest %d | absent-from-archive %d'
      % (arc_rows, len(arc_bad), len(arc_extra), len(set(man_by_path) - seen_arc)))
print('archive equals manifest:', R['archiveEqualsManifest'])

R['ALL_VERIFIED'] = all([R['manifestMatchesDeclared'], R['archiveMatchesDeclared'],
                         R['fileCountMatches'], R['totalBytesMatches'], R['measuredBytesMatch'],
                         not miss, not badh, not bads, not extras,
                         R['parentIsMyV31'], R['archiveEqualsManifest']])
print('\nALL_VERIFIED:', R['ALL_VERIFIED'])
json.dump(R, open(os.path.join(OUT, 'p00-verify32.json'), 'w'), indent=1)
