"""Q00 — full custody of frozen source34 and an INDEPENDENT 33->34 delta derived from the two manifests.

Checks: manifest and archive digests; every manifest row against the snapshot by sha256 and size; no
extras in the snapshot; every archive member byte-equal to the manifest row; declared parent is the
source33 I reviewed; delta from manifests (root-delta33-to34.json is compared only as inventory).
"""
import hashlib, json, os, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
MAN34 = os.path.join(REV, 'candidate-subject.v34.json')
MAN33 = os.path.join(REV, 'candidate-subject.v33.json')
ARC34 = os.path.join(REV, 'candidate-source.v34.tar.gz')
FRZ34 = os.path.join(REV, 'candidate-freeze.v34.json')
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v34'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
os.makedirs(OUT, exist_ok=True)
R = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R['manifestSha256'] = sha(MAN34)
R['manifestShaMatchesDeclared'] = R['manifestSha256'] == 'bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6'
R['archiveSha256'] = sha(ARC34)
R['archiveShaMatchesDeclared'] = R['archiveSha256'] == '5c9768de78ea4454c4c4d795822fdf83bee491b7352e43e1e37317985ce45729'
R['manifest33Sha256'] = sha(MAN33)
R['manifest33IsMyReviewedSource33'] = R['manifest33Sha256'] == '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299'
print('manifest34 sha matches :', R['manifestShaMatchesDeclared'])
print('archive34 sha matches  :', R['archiveShaMatchesDeclared'])
print('manifest33 is mine     :', R['manifest33IsMyReviewedSource33'])

m34 = json.load(open(MAN34))
m33 = json.load(open(MAN33))
R['manifestTopLevelKeys'] = [k for k in m34 if k != 'files']
print('manifest34 keys:', R['manifestTopLevelKeys'])
for k in R['manifestTopLevelKeys']:
    print('   %-28s %s' % (k, json.dumps(m34[k], default=str)[:160]))
R['manifestRowKeys'] = sorted(m34['files'][0])
print('manifest row keys:', R['manifestRowKeys'])
SZ = next(k for k in ('size', 'bytes', 'sizeBytes', 'length') if k in m34['files'][0])
for f in m34['files'] + m33['files']:
    f['size'] = f[SZ]
rows = {f['path']: f for f in m34['files']}
rows33 = {f['path']: f for f in m33['files']}
R['declaredFiles'] = len(rows)
R['declaredTotalBytes'] = sum(int(f['size']) for f in rows.values())

# snapshot verification
missing, hashbad, sizebad, total = [], [], [], 0
for p, f in rows.items():
    fp = os.path.join(SNAP, p)
    if not os.path.isfile(fp):
        missing.append(p)
        continue
    sz = os.path.getsize(fp)
    total += sz
    if sz != int(f['size']):
        sizebad.append(p)
    if sha(fp) != f['sha256']:
        hashbad.append(p)
extras = []
for d, _, fs in os.walk(SNAP):
    for fn in fs:
        rel = os.path.relpath(os.path.join(d, fn), SNAP)
        if rel not in rows:
            extras.append(rel)
R.update({'filesChecked': len(rows), 'measuredTotalBytes': total, 'missing': len(missing),
          'hashMismatches': len(hashbad), 'sizeMismatches': len(sizebad), 'extras': len(extras),
          'extrasList': extras[:20], 'badList': (missing + hashbad + sizebad)[:20]})
R['matchesDeclared12899'] = len(rows) == 12899
R['matchesDeclaredBytes736798408'] = total == 736798408
print('\nsnapshot rows=%d bytes=%d missing=%d hash=%d size=%d extras=%d'
      % (len(rows), total, len(missing), len(hashbad), len(sizebad), len(extras)))
print('12,899 files / 736,798,408 bytes as declared:', R['matchesDeclared12899'], R['matchesDeclaredBytes736798408'])

# archive equality
arc_rows, arc_bad, arc_extra = 0, [], []
with tarfile.open(ARC34, 'r:gz') as t:
    for mem in t:
        if not mem.isfile():
            continue
        name = mem.name
        for pre in ('./',):
            if name.startswith(pre):
                name = name[len(pre):]
        cand = name
        if cand not in rows:
            # tolerate a single leading directory component
            parts = cand.split('/', 1)
            if len(parts) == 2 and parts[1] in rows:
                cand = parts[1]
        if cand not in rows:
            arc_extra.append(name)
            continue
        h = hashlib.sha256(t.extractfile(mem).read()).hexdigest()
        arc_rows += 1
        if h != rows[cand]['sha256']:
            arc_bad.append(cand)
R['archiveMemberRows'] = arc_rows
R['archiveHashMismatches'] = len(arc_bad)
R['archiveExtras'] = arc_extra[:20]
R['archiveEqualsManifest'] = arc_rows == len(rows) and not arc_bad and not arc_extra
print('archive rows=%d mismatches=%d extras=%d equal=%s'
      % (arc_rows, len(arc_bad), len(arc_extra), R['archiveEqualsManifest']))

# parent ancestry
frz = json.load(open(FRZ34))
R['freezeKeys'] = list(frz)
R['freeze'] = {k: (v if not isinstance(v, (list, dict)) else json.dumps(v)[:400]) for k, v in frz.items()}
print('\nfreeze34 keys:', list(frz))
for k, v in R['freeze'].items():
    print('   %-30s %s' % (k, str(v)[:200]))
blob = json.dumps(frz) + json.dumps({k: m34[k] for k in R['manifestTopLevelKeys']})
R['parentNamesSource33ManifestDigest'] = '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299' in blob
print('parent33 manifest digest named in freeze/manifest metadata:', R['parentNamesSource33ManifestDigest'])

# independent delta
added = sorted(p for p in rows if p not in rows33)
removed = sorted(p for p in rows33 if p not in rows)
changed = sorted(p for p in rows if p in rows33 and rows[p]['sha256'] != rows33[p]['sha256'])
R['delta'] = {'added': added, 'removed': removed,
              'changed': [{'path': p, 'bytes33': int(rows33[p]['size']), 'bytes34': int(rows[p]['size']),
                           'sha33': rows33[p]['sha256'], 'sha34': rows[p]['sha256']} for p in changed],
              'counts': {'added': len(added), 'removed': len(removed), 'changed': len(changed),
                         'touched': len(added) + len(removed) + len(changed)},
              'netBytes': R['declaredTotalBytes'] - sum(int(f['size']) for f in rows33.values())}
print('\nINDEPENDENT delta 33->34: added=%d removed=%d changed=%d net=%+d bytes'
      % (len(added), len(removed), len(changed), R['delta']['netBytes']))
for p in added:
    print('   A  %s' % p)
for p in removed:
    print('   R  %s' % p)
for c in R['delta']['changed']:
    print('   M  %-86s %+d' % (c['path'], c['bytes34'] - c['bytes33']))

# root inventory comparison
rd = json.load(open(os.path.join(BASE, 'root-delta33-to34.json')))
rblob = json.dumps(rd)
mine = set(added) | set(removed) | set(changed)
rootpaths = set()


def collect(o):
    if isinstance(o, str) and ('/' in o) and (o.startswith('docs/') or o.startswith('crates/') or '.' in o.split('/')[-1]):
        rootpaths.add(o)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ('path',) and isinstance(v, str):
                rootpaths.add(v)
            collect(v)
    elif isinstance(o, list):
        for v in o:
            collect(v)


collect(rd)
rootpaths = {p for p in rootpaths if p in rows or p in rows33}
R['rootInventory'] = {'rootPaths': sorted(rootpaths), 'inMineNotRoot': sorted(mine - rootpaths),
                      'inRootNotMine': sorted(rootpaths - mine), 'agrees': mine == rootpaths}
print('\nroot inventory agrees with my delta:', R['rootInventory']['agrees'],
      '| mine-not-root:', R['rootInventory']['inMineNotRoot'], '| root-not-mine:', R['rootInventory']['inRootNotMine'])
json.dump(R, open(os.path.join(OUT, 'q00-custody.json'), 'w'), indent=1, default=str)
print('wrote q00-custody.json')
