"""PROBE 02 (v31) — verify author package v7 (every member + its source binding) and the declared
native schema digest. Author-assisted evidence: verified, never graded from."""
import hashlib, json, os

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v7'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
EXP_AM = 'c9f632820f760245f7c9a259d28cc97839180f290f1771f51225edfb8969f258'
EXP_MAN31 = 'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5'
EXP_NATIVE = '3e37c7b7a6a620dcadc0aaed862eed242065ebd0ce9910da16faa25464f8b0b0'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R = {}
amp = os.path.join(PKG, 'artifact-manifest.json')
R['artifactManifestSha256'] = sha(amp)
R['artifactManifestMatchesDeclared'] = R['artifactManifestSha256'] == EXP_AM
am = json.load(open(amp))
rows = am['files'] if isinstance(am, dict) else am
R['declaredMembers'] = len(rows)
R['declaredMembersIs270'] = len(rows) == 270
print('artifact-manifest sha matches :', R['artifactManifestMatchesDeclared'])
print('declared members              :', len(rows), R['declaredMembersIs270'])

ok = bad = miss = 0
badrows = []
listed = set()
for r in rows:
    rel = r['path']
    listed.add(rel)
    p = os.path.join(PKG, rel)
    if not os.path.isfile(p):
        miss += 1
        badrows.append(('MISSING', rel))
        continue
    if sha(p) == r['sha256'] and os.path.getsize(p) == r.get('bytes', os.path.getsize(p)):
        ok += 1
    else:
        bad += 1
        badrows.append(('MISMATCH', rel))
extras = []
for dp, dn, fn in os.walk(PKG):
    for n in fn:
        rel = os.path.relpath(os.path.join(dp, n), PKG)
        if rel not in listed:
            extras.append(rel)
R.update(verified=ok, mismatched=bad, missing=miss, badRows=badrows[:10],
         extrasOnDisk=extras, extrasCount=len(extras))
print('members verified / mismatched / missing / extras :', ok, bad, miss, len(extras), extras[:4])

# ---- source binding ----
smp = os.path.join(PKG, 'source-manifest.json')
R['sourceManifestSha256'] = sha(smp)
R['sourceManifestEqualsFrozen31Manifest'] = R['sourceManifestSha256'] == EXP_MAN31
sm = json.load(open(smp))
smf = {f['path']: f for f in sm['files']}
man31 = {f['path']: f for f in json.load(open(
    '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'))['files']}
R['sourceManifestRows'] = len(smf)
R['sourceManifestRowsEqualFrozen31'] = len(smf) == len(man31)
diffp = [p for p in set(smf) | set(man31)
         if smf.get(p, {}).get('sha256') != man31.get(p, {}).get('sha256')]
R['sourceManifestRowDifferences'] = diffp[:10]
R['sourceManifestBindsExact31'] = not diffp
print('package source-manifest binds exact frozen31 :', R['sourceManifestBindsExact31'],
      '(rows %d)' % len(smf))

# ---- declared native schema digest ----
nat = os.path.join(SRC, 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
R['nativeSchemaSha256'] = sha(nat)
R['nativeSchemaMatchesDeclared'] = R['nativeSchemaSha256'] == EXP_NATIVE
print('native schema sha matches declared           :', R['nativeSchemaMatchesDeclared'],
      R['nativeSchemaSha256'][:20])

# ---- what does the package say about its own construction provenance ----
for n in ('source-rebuild.v1.json', 'README.md', 'source-rebinding.v2.json'):
    p = os.path.join(PKG, n)
    if os.path.isfile(p):
        R['has_' + n] = True
print('\npackage top-level entries:')
for n in sorted(os.listdir(PKG))[:60]:
    p = os.path.join(PKG, n)
    print('   %-52s %s' % (n, os.path.getsize(p) if os.path.isfile(p) else '<dir>'))

R['ALL_VERIFIED'] = all([R['artifactManifestMatchesDeclared'], R['declaredMembersIs270'],
                         bad == 0, miss == 0, R['sourceManifestBindsExact31'],
                         R['nativeSchemaMatchesDeclared']])
print('\nALL_VERIFIED:', R['ALL_VERIFIED'])
json.dump(R, open(os.path.join(OUT, 'p02-pkgverify.json'), 'w'), indent=1)
