"""V00 — bounded verification of BOTH input sets.

Scope disclosed: I verify the exact files this bounded review reads, plus their relationship to the
frozen31 snapshot. I do NOT re-verify all 12895 frozen31 rows here; the source31 whole-design review
already did that and this pass is bounded.
"""
import hashlib, json, os

G = '/tmp/opensip-design-corrections/glob-semantics-successor.v1'
RR = '/tmp/opensip-design-corrections/root-repair-selection-author-review.v1'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v31'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
OUT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/receipts'
os.makedirs(OUT, exist_ok=True)
R = {'verificationScope': (
    'Exact inputs of this bounded pass: the 5 declared glob changes, their before-images, the glob '
    'custody/integration records, and the repair-review assessment plus its 4 captured author files. '
    'Frozen31 is used as the normative baseline and its manifest digest is re-verified, but the full '
    '12895-row sweep is NOT repeated in this bounded pass.')}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# ---- frozen31 manifest identity only ----
R['source31ManifestSha256'] = sha(MAN)
R['source31ManifestMatchesDeclared'] = (
    R['source31ManifestSha256'] == 'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5')
man = {f['path']: f for f in json.load(open(MAN))['files']}
print('source31 manifest sha matches declared:', R['source31ManifestMatchesDeclared'])

# ---- glob change set ----
cf = json.load(open(os.path.join(G, 'changed-files.json')))
R['changedFilesStanding'] = cf['standing']
R['deferredLinks'] = cf['deferredLinks']
rows = []
for f in cf['files']:
    rel = f['path']
    after = os.path.join(G, 'source', rel)
    row = {'path': rel, 'declaredSha256': f['sha256'], 'declaredBytes': f['bytes'],
           'declaredBeforeSha256': f['beforeSha256'],
           'afterPresent': os.path.isfile(after)}
    if row['afterPresent']:
        row['measuredSha256'] = sha(after)
        row['measuredBytes'] = os.path.getsize(after)
        row['afterMatchesDeclared'] = (row['measuredSha256'] == f['sha256']
                                       and row['measuredBytes'] == f['bytes'])
    fz = man.get(rel)
    row['inFrozen31'] = fz is not None
    if fz:
        row['frozen31Sha256'] = fz['sha256']
        row['beforeEqualsFrozen31'] = f['beforeSha256'] == fz['sha256']
        row['changesFrozen31Bytes'] = f['sha256'] != fz['sha256']
    else:
        row['beforeEqualsFrozen31'] = f['beforeSha256'] is None
        row['isNewFile'] = True
    rows.append(row)
R['globChanges'] = rows
print('\n--- glob change set ---')
for r in rows:
    print('%-68s after=%-5s baseOK=%-5s new=%s'
          % (r['path'][-68:], r.get('afterMatchesDeclared'), r['beforeEqualsFrozen31'],
             r.get('isNewFile', False)))
R['allAfterHashesMatch'] = all(r.get('afterMatchesDeclared') for r in rows)
R['allBeforeImagesAreFrozen31'] = all(r['beforeEqualsFrozen31'] for r in rows)
print('all after-hashes match declared      :', R['allAfterHashesMatch'])
print('every before-image equals frozen31   :', R['allBeforeImagesAreFrozen31'])

# ---- before-images directory, if present ----
bdir = None
for cand in ('before-images', 'before', 'beforeImages'):
    if os.path.isdir(os.path.join(G, cand)):
        bdir = os.path.join(G, cand)
R['beforeImagesDir'] = bdir
if bdir:
    bi = []
    for dp, dn, fn in os.walk(bdir):
        for n in fn:
            p = os.path.join(dp, n)
            rel = os.path.relpath(p, bdir)
            s = sha(p)
            match = [x['path'] for x in cf['files'] if x['beforeSha256'] == s]
            frozen = [k for k, v in man.items() if v['sha256'] == s]
            bi.append({'file': rel, 'sha256': s, 'matchesDeclaredBefore': match,
                       'matchesFrozen31Path': frozen[:2]})
    R['beforeImages'] = bi
    print('\n--- before-images (%d) ---' % len(bi))
    for x in bi:
        print('%-52s before-of=%-46s frozen31=%s' % (x['file'][-52:], x['matchesDeclaredBefore'],
                                                     bool(x['matchesFrozen31Path'])))
    R['allBeforeImagesResolveToFrozen31'] = all(x['matchesFrozen31Path'] for x in bi)

# ---- how much of source/ is just a copy of frozen31? ----
srcroot = os.path.join(G, 'source')
same = diff = extra = 0
difflist = []
for dp, dn, fn in os.walk(srcroot):
    for n in fn:
        p = os.path.join(dp, n)
        rel = os.path.relpath(p, srcroot)
        fz = man.get(rel)
        if fz is None:
            extra += 1
            difflist.append(('NOT-IN-FROZEN31', rel))
        elif sha(p) == fz['sha256']:
            same += 1
        else:
            diff += 1
            difflist.append(('DIFFERS', rel))
R['globSourceTree'] = {'filesEqualToFrozen31': same, 'filesDiffering': diff,
                       'filesNotInFrozen31': extra, 'nonIdentical': difflist}
print('\nglob source/ tree vs frozen31: %d identical, %d differing, %d not in frozen31'
      % (same, diff, extra))
for kind, rel in difflist:
    print('   %-16s %s' % (kind, rel))

# ---- custody / integration records ----
for n in ('input-custody.json', 'integration.json', 'author.py', 'checks/check-atoms.report.json'):
    p = os.path.join(G, n)
    if os.path.isfile(p):
        R.setdefault('globRecords', {})[n] = {'sha256': sha(p), 'bytes': os.path.getsize(p)}
print('\nglob records:', json.dumps(R.get('globRecords'), indent=1)[:500])

# ---- repair review input ----
names = []
for dp, dn, fn in os.walk(RR):
    for n in sorted(fn):
        p = os.path.join(dp, n)
        names.append({'path': os.path.relpath(p, RR), 'sha256': sha(p),
                      'bytes': os.path.getsize(p)})
R['repairReviewFiles'] = names
print('\n--- repair-selection review input (%d files) ---' % len(names))
for x in names:
    print('%-58s %8d  %s' % (x['path'][-58:], x['bytes'], x['sha256'][:16]))

json.dump(R, open(os.path.join(OUT, 'v00-verify.json'), 'w'), indent=1)
print('\nwrote v00-verify.json')
