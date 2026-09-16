"""PROBE 00 (v31) — verify every declared input before reading anything.

Manifest sha, archive sha, every snapshot row (hash + size), no drift, no extras, and the exact
ancestry chain 31 -> 30 -> 29 -> 28 -> 27 where 27 is the subject my prior review graded.
"""
import hashlib, json, os

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
MAN = os.path.join(REV, 'candidate-subject.v31.json')
ARC = os.path.join(REV, 'candidate-source.v31.tar.gz')
SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
os.makedirs(OUT, exist_ok=True)

EXP_MAN = 'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5'
EXP_ARC = '0a980be4067958d01f3927a63b1a8819ac63e7960f499bbb59695630b3c883e0'
EXP_FILES, EXP_BYTES = 12895, 736536507
MY27 = 'a1ae88efc4198054b11cc2533582808a88dd25e5a5cc11c2966058ce1390227a'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R = {}
R['manifestPath'] = MAN
R['manifestSha256'] = sha(MAN)
R['manifestShaMatchesDeclared'] = R['manifestSha256'] == EXP_MAN
R['archivePath'] = ARC
R['archiveExists'] = os.path.isfile(ARC)
R['archiveSha256'] = sha(ARC) if R['archiveExists'] else None
R['archiveShaMatchesDeclared'] = R['archiveSha256'] == EXP_ARC
print('manifest sha matches :', R['manifestShaMatchesDeclared'], R['manifestSha256'][:20])
print('archive  sha matches :', R['archiveShaMatchesDeclared'], str(R['archiveSha256'])[:20])

m = json.load(open(MAN))
R['manifestTopKeys'] = sorted(m)
files = m['files']
R['declaredFileCount'] = len(files)
R['declaredFileCountMatches'] = len(files) == EXP_FILES
declared_bytes = sum(f['bytes'] for f in files)
R['declaredTotalBytes'] = declared_bytes
R['declaredTotalBytesMatches'] = declared_bytes == EXP_BYTES
for k in ('parentManifestSha256', 'sha256', 'generatedAt', 'standing', 'root', 'ancestry'):
    if k in m:
        R['manifest.' + k] = m[k]
print('files declared       :', len(files), R['declaredFileCountMatches'])
print('bytes declared       :', declared_bytes, R['declaredTotalBytesMatches'])
print('manifest top keys    :', R['manifestTopKeys'])

# ---- every row verified ----
bad_hash, bad_size, missing = [], [], []
total = 0
seen = set()
for f in files:
    p = os.path.join(SRC, f['path'])
    seen.add(f['path'])
    if not os.path.isfile(p):
        missing.append(f['path'])
        continue
    st = os.path.getsize(p)
    total += st
    if st != f['bytes']:
        bad_size.append(f['path'])
        continue
    if sha(p) != f['sha256']:
        bad_hash.append(f['path'])
R['filesChecked'] = len(files)
R['measuredTotalBytes'] = total
R['measuredBytesMatchDeclared'] = total == EXP_BYTES
R['missing'] = missing[:20]
R['missingCount'] = len(missing)
R['hashMismatches'] = bad_hash[:20]
R['hashMismatchCount'] = len(bad_hash)
R['sizeMismatches'] = bad_size[:20]
R['sizeMismatchCount'] = len(bad_size)

# ---- extras on disk ----
extras = []
for dp, dn, fn in os.walk(SRC):
    for n in fn:
        rel = os.path.relpath(os.path.join(dp, n), SRC)
        if rel not in seen:
            extras.append(rel)
R['extrasOnDisk'] = extras[:20]
R['extrasOnDiskCount'] = len(extras)
print('missing / hashbad / sizebad / extras :',
      len(missing), len(bad_hash), len(bad_size), len(extras))
print('measured bytes       :', total, R['measuredBytesMatchDeclared'])

# ---- ancestry 31 -> 30 -> 29 -> 28 -> 27 ----
chain = []
cur, curname = m, 'v31'
for _ in range(6):
    parent = cur.get('parentManifestSha256')
    chain.append({'manifest': curname, 'sha256': sha(os.path.join(REV, 'candidate-subject.%s.json' % curname))
                  if os.path.isfile(os.path.join(REV, 'candidate-subject.%s.json' % curname)) else None,
                  'declaredParent': parent})
    if not parent:
        break
    # find the manifest file whose sha equals `parent`
    nxt = None
    for cand in sorted(os.listdir(REV)):
        if cand.startswith('candidate-subject.v') and cand.endswith('.json'):
            if sha(os.path.join(REV, cand)) == parent:
                nxt = cand
                break
    if nxt is None:
        chain[-1]['parentManifestFileFound'] = False
        break
    chain[-1]['parentManifestFile'] = nxt
    curname = nxt[len('candidate-subject.'):-len('.json')]
    cur = json.load(open(os.path.join(REV, nxt)))
R['ancestryChain'] = chain
print('\nancestry chain:')
for c in chain:
    print('   %-6s sha=%s parent=%s -> %s' % (c['manifest'], str(c['sha256'])[:12],
                                              str(c['declaredParent'])[:12],
                                              c.get('parentManifestFile', c.get('parentManifestFileFound'))))
names = [c['manifest'] for c in chain]
R['ancestryNames'] = names
R['reaches27'] = 'v27' in names
R['v27ShaIsTheOneIGraded'] = any(c['sha256'] == MY27 for c in chain)
print('reaches v27:', R['reaches27'], '| v27 sha is the one I graded:', R['v27ShaIsTheOneIGraded'])

R['ALL_VERIFIED'] = all([R['manifestShaMatchesDeclared'], R['archiveShaMatchesDeclared'],
                         R['declaredFileCountMatches'], R['measuredBytesMatchDeclared'],
                         not missing, not bad_hash, not bad_size, not extras,
                         R['reaches27'], R['v27ShaIsTheOneIGraded']])
print('\nALL_VERIFIED:', R['ALL_VERIFIED'])
json.dump(R, open(os.path.join(OUT, 'p00-verify31.json'), 'w'), indent=1)
