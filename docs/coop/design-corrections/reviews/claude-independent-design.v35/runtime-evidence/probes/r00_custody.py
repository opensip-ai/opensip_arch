"""R00 — full custody of frozen source35 and an INDEPENDENT 34->35 delta from the two manifests.
Root inventory, if present, is compared as inventory only."""
import glob, hashlib, json, os, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
MAN35 = os.path.join(REV, 'candidate-subject.v35.json')
MAN34 = os.path.join(REV, 'candidate-subject.v34.json')
ARC35 = os.path.join(REV, 'candidate-source.v35.tar.gz')
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v35'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
OUT = os.path.join(BASE, 'receipts')
os.makedirs(OUT, exist_ok=True)
R = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R['manifestSha256'] = sha(MAN35)
R['manifestShaMatchesDeclared'] = R['manifestSha256'] == 'eb45c22b88a428887672d729be6645abf7d4d175474313d0909c8307d7966c85'
R['archiveSha256'] = sha(ARC35)
R['archiveShaMatchesDeclared'] = R['archiveSha256'] == 'f5292e688f467c9f250f63e8dc4486cf35677e178fca15b242eb3b1be76e9781'
R['manifest34Sha256'] = sha(MAN34)
R['manifest34IsMyReviewedSource34'] = R['manifest34Sha256'] == 'bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6'
m35, m34 = json.load(open(MAN35)), json.load(open(MAN34))
R['manifestMeta'] = {k: v for k, v in m35.items() if k != 'files'}
R['parentNamedIsSource34'] = m35.get('parentManifestSha256') == R['manifest34Sha256']
print('manifest35 %s | archive35 %s | manifest34 mine %s | parent named = 34 %s' % (
    R['manifestShaMatchesDeclared'], R['archiveShaMatchesDeclared'], R['manifest34IsMyReviewedSource34'], R['parentNamedIsSource34']))
rows = {f['path']: f for f in m35['files']}
rows34 = {f['path']: f for f in m34['files']}
missing, hashbad, sizebad, total = [], [], [], 0
for p, f in rows.items():
    fp = os.path.join(SNAP, p)
    if not os.path.isfile(fp):
        missing.append(p); continue
    sz = os.path.getsize(fp); total += sz
    if sz != int(f['bytes']):
        sizebad.append(p)
    if sha(fp) != f['sha256']:
        hashbad.append(p)
extras = [os.path.relpath(os.path.join(d, fn), SNAP) for d, _, fs in os.walk(SNAP) for fn in fs
          if os.path.relpath(os.path.join(d, fn), SNAP) not in rows]
R.update(declaredFiles=len(rows), declaredTotalBytes=m35.get('totalBytes'), measuredTotalBytes=total,
         missing=len(missing), hashMismatches=len(hashbad), sizeMismatches=len(sizebad), extras=len(extras),
         badList=(missing + hashbad + sizebad + extras)[:20])
R['matchesDeclared'] = len(rows) == 12899 and total == 736823249 and m35.get('fileCount') == 12899 and m35.get('totalBytes') == 736823249
print('snapshot rows=%d bytes=%d missing=%d hash=%d size=%d extras=%d | declared 12899/736823249: %s'
      % (len(rows), total, len(missing), len(hashbad), len(sizebad), len(extras), R['matchesDeclared']))
arc_rows, arc_bad, arc_extra = 0, [], []
with tarfile.open(ARC35, 'r:gz') as t:
    for mem in t:
        if not mem.isfile():
            continue
        name = mem.name[2:] if mem.name.startswith('./') else mem.name
        if name not in rows:
            parts = name.split('/', 1)
            name = parts[1] if len(parts) == 2 and parts[1] in rows else name
        if name not in rows:
            arc_extra.append(name); continue
        arc_rows += 1
        if hashlib.sha256(t.extractfile(mem).read()).hexdigest() != rows[name]['sha256']:
            arc_bad.append(name)
R.update(archiveMemberRows=arc_rows, archiveHashMismatches=len(arc_bad), archiveExtras=arc_extra[:10],
         archiveEqualsManifest=arc_rows == len(rows) and not arc_bad and not arc_extra)
print('archive rows=%d mismatches=%d extras=%d equal=%s' % (arc_rows, len(arc_bad), len(arc_extra), R['archiveEqualsManifest']))
frz = os.path.join(REV, 'candidate-freeze.v35.json')
if os.path.isfile(frz):
    R['freeze'] = json.load(open(frz))
    R['freezeAgrees'] = (R['freeze'].get('manifestSha256') == R['manifestSha256'] and R['freeze'].get('archiveSha256') == R['archiveSha256'])
    print('freeze record agrees:', R['freezeAgrees'])
added = sorted(p for p in rows if p not in rows34)
removed = sorted(p for p in rows34 if p not in rows)
changed = sorted(p for p in rows if p in rows34 and rows[p]['sha256'] != rows34[p]['sha256'])
R['delta'] = {'added': added, 'removed': removed,
              'changed': [{'path': p, 'bytes34': int(rows34[p]['bytes']), 'bytes35': int(rows[p]['bytes']),
                           'sha34': rows34[p]['sha256'], 'sha35': rows[p]['sha256']} for p in changed],
              'counts': {'added': len(added), 'removed': len(removed), 'changed': len(changed)},
              'netBytes': total - sum(int(f['bytes']) for f in rows34.values())}
print('\nINDEPENDENT delta 34->35: added=%d removed=%d changed=%d net=%+d' % (len(added), len(removed), len(changed), R['delta']['netBytes']))
for p in added:
    print('   A ', p)
for p in removed:
    print('   R ', p)
for c in R['delta']['changed']:
    print('   M  %-88s %+d' % (c['path'], c['bytes35'] - c['bytes34']))
mine = set(added) | set(removed) | set(changed)
for cand in sorted(glob.glob(os.path.join(BASE, 'root-delta*.json')) + glob.glob(os.path.join(REV, 'root-final35-custody.v1', '*.json'))):
    try:
        d = json.load(open(cand))
    except Exception:
        continue
    paths = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'path' and isinstance(v, str):
                    paths.add(v)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(d)
    paths = {p for p in paths if p in rows or p in rows34}
    if paths:
        R.setdefault('rootInventories', {})[cand] = {'paths': len(paths), 'inMineNotRoot': sorted(mine - paths),
                                                     'inRootNotMine': sorted(paths - mine), 'agrees': paths == mine}
        print('root inventory %s agrees: %s (mine-not-root %s, root-not-mine %s)' % (
            os.path.basename(cand), paths == mine, sorted(mine - paths)[:5], sorted(paths - mine)[:5]))
json.dump(R, open(os.path.join(OUT, 'r00-custody.json'), 'w'), indent=1, default=str)
print('wrote r00-custody.json')
