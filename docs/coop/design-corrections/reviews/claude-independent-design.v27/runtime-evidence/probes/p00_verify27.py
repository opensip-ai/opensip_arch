"""Probe 00 (v27) — verify the frozen source27 snapshot completely, and the archive."""
import hashlib, json, os, time

MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v27.json'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)

mb = open(MAN, 'rb').read()
m = json.loads(mb)
root = m['snapshotRoot']
res = {
    'manifestPath': MAN,
    'manifestSha256': hashlib.sha256(mb).hexdigest(),
    'manifestBytes': len(mb),
    'expectedManifestSha256': 'a1ae88efc4198054b11cc2533582808a88dd25e5a5cc11c2966058ce1390227a',
    'parentManifestSha256': m['parentManifestSha256'],
    'parentIsTheSource26IReviewed':
        m['parentManifestSha256'] == 'c9a6c26a82dbe24acfbba423360be54e45f11325576b172d75a005ec35d0ffb2',
    'fileCountDeclared': m['fileCount'],
    'totalBytesDeclared': m['totalBytes'],
    'snapshotRoot': root,
}
res['manifestSha256Matches'] = res['manifestSha256'] == res['expectedManifestSha256']

t0 = time.time()
missing, badhash, badlen = [], [], []
total = 0
for rec in m['files']:
    fp = os.path.join(root, rec['path'])
    if not os.path.isfile(fp):
        missing.append(rec['path'])
        continue
    sz = os.path.getsize(fp)
    h = hashlib.sha256()
    with open(fp, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    total += sz
    if sz != rec['bytes']:
        badlen.append((rec['path'], sz, rec['bytes']))
    if h.hexdigest() != rec['sha256']:
        badhash.append(rec['path'])

known = {r['path'] for r in m['files']}
extra = []
for dp, dn, fn in os.walk(root):
    for n in fn:
        rel = os.path.relpath(os.path.join(dp, n), root)
        if rel not in known:
            extra.append(rel)

res.update({
    'filesChecked': len(m['files']),
    'bytesMeasured': total,
    'bytesMatchDeclared': total == m['totalBytes'],
    'missing': missing[:20], 'missingCount': len(missing),
    'hashMismatch': badhash[:20], 'hashMismatchCount': len(badhash),
    'lengthMismatch': badlen[:20], 'lengthMismatchCount': len(badlen),
    'extraOnDisk': extra[:20], 'extraOnDiskCount': len(extra),
    'elapsedSeconds': round(time.time() - t0, 1),
})

# archive
ARCH_EXPECT = 'adb78633c890eb99e3eb001d050c1fec0b77be870d18201aa732947fde827603'
cands = []
for d in ('/tmp/opensip-design-corrections',
          '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'):
    if os.path.isdir(d):
        for n in os.listdir(d):
            if 'v27' in n and (n.endswith('.tar.gz') or n.endswith('.tgz') or n.endswith('.tar')
                               or n.endswith('.zip')):
                cands.append(os.path.join(d, n))
arch = []
for c in cands:
    h = hashlib.sha256()
    with open(c, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    arch.append({'path': c, 'bytes': os.path.getsize(c), 'sha256': h.hexdigest(),
                 'matchesDeclaredArchiveSha': h.hexdigest() == ARCH_EXPECT})
res['archiveCandidates'] = arch
res['expectedArchiveSha256'] = ARCH_EXPECT

json.dump(res, open(os.path.join(OUT, 'p00-verify27.json'), 'w'), indent=1)
for k in ('manifestSha256Matches', 'parentIsTheSource26IReviewed', 'filesChecked',
          'bytesMeasured', 'bytesMatchDeclared', 'missingCount', 'hashMismatchCount',
          'lengthMismatchCount', 'extraOnDiskCount', 'elapsedSeconds'):
    print('%-32s %s' % (k, res[k]))
print('archiveCandidates:', json.dumps(arch, indent=1))
