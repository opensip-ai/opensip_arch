"""R00 — full custody of frozen source36 and an INDEPENDENT 35->36 delta from the two manifests.
Every manifest row is hashed in the snapshot, the snapshot is walked for extras, the archive is read member by member,
every parent35 path must be present in 36 or explicitly removed. Root inventory is compared as inventory only."""
import hashlib, json, os, tarfile

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
MAN36 = os.path.join(REV, 'candidate-subject.v36.json')
MAN35 = os.path.join(REV, 'candidate-subject.v35.json')
ARC36 = os.path.join(REV, 'candidate-source.v36.tar.gz')
ARC35 = os.path.join(REV, 'candidate-source.v35.tar.gz')
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v36'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
OUT = os.path.join(BASE, 'receipts')
PARENTS = os.path.join(BASE, 'disposable/parent35-delta-files')
os.makedirs(OUT, exist_ok=True)
R = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R['manifestSha256'] = sha(MAN36)
R['manifestShaMatchesDeclared'] = R['manifestSha256'] == 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235'
R['archiveSha256'] = sha(ARC36)
R['archiveShaMatchesDeclared'] = R['archiveSha256'] == '7db498f0b48de362eee70ff41c6e7b762d61227e6cf4b82477d1601cc8329e8f'
R['manifest35Sha256'] = sha(MAN35)
R['manifest35IsMyAcceptedSource35'] = R['manifest35Sha256'] == 'eb45c22b88a428887672d729be6645abf7d4d175474313d0909c8307d7966c85'
R['archive35Sha256'] = sha(ARC35)
R['archive35IsTheSource35IVerified'] = R['archive35Sha256'] == 'f5292e688f467c9f250f63e8dc4486cf35677e178fca15b242eb3b1be76e9781'
m36, m35 = json.load(open(MAN36)), json.load(open(MAN35))
R['manifestMeta'] = {k: v for k, v in m36.items() if k != 'files'}
R['parentNamedIsSource35'] = any(v == R['manifest35Sha256'] for k, v in m36.items() if 'parent' in k.lower() and isinstance(v, str))
print('manifest36 %s | archive36 %s | manifest35 mine %s | archive35 mine %s | parent named = 35 %s' % (
    R['manifestShaMatchesDeclared'], R['archiveShaMatchesDeclared'], R['manifest35IsMyAcceptedSource35'],
    R['archive35IsTheSource35IVerified'], R['parentNamedIsSource35']))
print('manifest meta:', R['manifestMeta'])
rows = {f['path']: f for f in m36['files']}
rows35 = {f['path']: f for f in m35['files']}
R['duplicateManifestPaths'] = len(m36['files']) - len(rows)
missing, hashbad, sizebad, total = [], [], [], 0
for p, f in rows.items():
    fp = os.path.join(SNAP, p)
    if not os.path.isfile(fp) or os.path.islink(fp):
        missing.append(p); continue
    sz = os.path.getsize(fp); total += sz
    if sz != int(f['bytes']):
        sizebad.append(p)
    if sha(fp) != f['sha256']:
        hashbad.append(p)
walked = []
for d, dirs, fs in os.walk(SNAP):
    for fn in fs:
        walked.append(os.path.relpath(os.path.join(d, fn), SNAP))
extras = sorted(p for p in walked if p not in rows)
R.update(declaredFiles=len(rows), declaredTotalBytes=m36.get('totalBytes'), declaredFileCount=m36.get('fileCount'), measuredTotalBytes=total,
         walkedFiles=len(walked), missing=len(missing), hashMismatches=len(hashbad), sizeMismatches=len(sizebad), extras=len(extras),
         badList=(missing + hashbad + sizebad + extras)[:20])
R['matchesDeclared'] = len(rows) == 12899 and total == 736854701 and len(walked) == 12899
print('snapshot rows=%d walked=%d bytes=%d missing=%d hash=%d size=%d extras=%d dupPaths=%d | declared 12899/736854701: %s'
      % (len(rows), len(walked), total, len(missing), len(hashbad), len(sizebad), len(extras), R['duplicateManifestPaths'], R['matchesDeclared']))
arc_rows, arc_bad, arc_extra, arc_seen = 0, [], [], set()
with tarfile.open(ARC36, 'r:gz') as t:
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
        arc_seen.add(name)
        if hashlib.sha256(t.extractfile(mem).read()).hexdigest() != rows[name]['sha256']:
            arc_bad.append(name)
R.update(archiveMemberRows=arc_rows, archiveDistinctRows=len(arc_seen), archiveHashMismatches=len(arc_bad), archiveExtras=arc_extra[:10],
         archiveEqualsManifest=arc_rows == len(rows) == len(arc_seen) and not arc_bad and not arc_extra)
print('archive rows=%d distinct=%d mismatches=%d extras=%d equal=%s' % (arc_rows, len(arc_seen), len(arc_bad), len(arc_extra), R['archiveEqualsManifest']))
frz = os.path.join(REV, 'candidate-freeze.v36.json')
R['freeze'] = json.load(open(frz))
R['freezeAgrees'] = (R['freeze'].get('manifestSha256') == R['manifestSha256'] and R['freeze'].get('archiveSha256') == R['archiveSha256']
                     and R['freeze'].get('fileCount') == len(rows) and R['freeze'].get('totalBytes') == total)
print('freeze record agrees:', R['freezeAgrees'])
added = sorted(p for p in rows if p not in rows35)
removed = sorted(p for p in rows35 if p not in rows)
changed = sorted(p for p in rows if p in rows35 and rows[p]['sha256'] != rows35[p]['sha256'])
R['noParentOmission'] = not removed
R['delta'] = {'added': added, 'removed': removed,
              'changed': [{'path': p, 'bytes35': int(rows35[p]['bytes']), 'bytes36': int(rows[p]['bytes']),
                           'sha35': rows35[p]['sha256'], 'sha36': rows[p]['sha256']} for p in changed],
              'counts': {'added': len(added), 'removed': len(removed), 'changed': len(changed),
                         'unchanged': sum(1 for p in rows if p in rows35 and rows[p]['sha256'] == rows35[p]['sha256'])},
              'netBytes': total - sum(int(f['bytes']) for f in rows35.values())}
print('\nINDEPENDENT delta 35->36: added=%d removed=%d changed=%d unchanged=%d net=%+d' % (
    len(added), len(removed), len(changed), R['delta']['counts']['unchanged'], R['delta']['netBytes']))
for p in added:
    print('   A ', p)
for p in removed:
    print('   R ', p)
for c in R['delta']['changed']:
    print('   M  %-88s %+d' % (c['path'], c['bytes36'] - c['bytes35']))
# parent bytes of every changed file, from the frozen35 ARCHIVE (hash-checked against the 35 manifest)
os.makedirs(PARENTS, exist_ok=True)
want = set(changed)
got = {}
with tarfile.open(ARC35, 'r:gz') as t:
    for mem in t:
        if not mem.isfile():
            continue
        name = mem.name[2:] if mem.name.startswith('./') else mem.name
        if name not in rows35:
            parts = name.split('/', 1)
            name = parts[1] if len(parts) == 2 and parts[1] in rows35 else name
        if name in want:
            b = t.extractfile(mem).read()
            assert hashlib.sha256(b).hexdigest() == rows35[name]['sha256'], name
            dst = os.path.join(PARENTS, name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'wb').write(b)
            got[name] = rows35[name]['sha256']
R['parentBytesExtractedAndVerified'] = sorted(got) == sorted(want)
mine = set(added) | set(removed) | set(changed)
rd = json.load(open(os.path.join(BASE, 'root-delta35-to36.json')))
rootp = {f['path']: (f['beforeSha256'], f['afterSha256']) for f in rd['files']}
R['rootInventory'] = {'paths': len(rootp), 'agreesOnPaths': set(rootp) == mine,
                      'agreesOnDigests': all(rootp[p] == (rows35[p]['sha256'], rows[p]['sha256']) for p in rootp if p in rows and p in rows35),
                      'inMineNotRoot': sorted(mine - set(rootp)), 'inRootNotMine': sorted(set(rootp) - mine),
                      'standing': 'inventory compared only; not acceptance evidence'}
print('root inventory agrees on paths %s and digests %s' % (R['rootInventory']['agreesOnPaths'], R['rootInventory']['agreesOnDigests']))
json.dump(R, open(os.path.join(OUT, 'r00-custody.json'), 'w'), indent=1, default=str)
print('wrote r00-custody.json')
