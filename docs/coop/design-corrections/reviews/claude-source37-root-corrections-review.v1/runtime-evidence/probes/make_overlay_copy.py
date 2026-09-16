"""Disposable verified source37 copy plus exact root-correction overlay (subject-manifest.json).

1. Verify every frozen source37 file against the source37 subject manifest (SHA 245ef613...).
2. Copy the verified bytes into work/source37-overlay (fresh directory; refuses to reuse).
3. For each overlay row: base bytes must equal beforeSha256; overlay bytes (subject/) must equal sha256
   and bytes; then replace. Re-verify the whole copy = source37 manifest except the 12 overlay rows.
Reference preparation only; writes only under this runtime.
"""
import hashlib, json, os, shutil, sys

RT = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v37'
MAN37 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
DEST = RT + '/work/source37-overlay'
OUT = RT + '/receipts/overlay-copy.json'


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x
    return None


res = {'source37ManifestSha256': sha_file(MAN37)}
assert res['source37ManifestSha256'] == '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
ov_raw = open(RT + '/subject-manifest.json', 'rb').read()
res['overlayManifestSha256'] = hashlib.sha256(ov_raw).hexdigest()
assert res['overlayManifestSha256'] == 'db9b7b3f3fbec833229fbd6e0c37cdc7bfed35ffabf3b6baabf709d35b380e52'
ov = json.loads(ov_raw)
assert ov['baseManifestSha256'] == res['source37ManifestSha256']
m = rows(json.load(open(MAN37)))
listed = {r['path']: r for r in m}
bad = []
for r in m:
    p = os.path.join(SRC, r['path'])
    if not os.path.isfile(p) or sha_file(p) != r['sha256']:
        bad.append(r['path'])
extra = []
for dp, ds, fs in os.walk(SRC):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), SRC)
        if rel not in listed:
            extra.append(rel)
res['sourceVerified'] = {'entries': len(m), 'mismatchOrMissing': bad, 'unlisted': extra}
assert not bad and not extra
if os.path.exists(DEST):
    sys.exit('refusing to reuse existing ' + DEST)
os.makedirs(DEST)
for r in m:
    s = os.path.join(SRC, r['path'])
    d = os.path.join(DEST, r['path'])
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copyfile(s, d)
applied = []
for f in ov['files']:
    base = os.path.join(DEST, f['path'])
    new = os.path.join(RT, 'subject', f['path'])
    b_sha = sha_file(base)
    raw = open(new, 'rb').read()
    ok = b_sha == f['beforeSha256'] and hashlib.sha256(raw).hexdigest() == f['sha256'] and len(raw) == f['bytes']
    applied.append({'path': f['path'], 'baseEqualsBefore': b_sha == f['beforeSha256'], 'overlayVerified': ok})
    assert ok, f['path']
    with open(base, 'wb') as out:
        out.write(raw)
res['overlayApplied'] = applied
overlay_paths = {f['path']: f['sha256'] for f in ov['files']}
post_bad = []
for r in m:
    want = overlay_paths.get(r['path'], r['sha256'])
    if sha_file(os.path.join(DEST, r['path'])) != want:
        post_bad.append(r['path'])
res['postOverlayVerified'] = {'entries': len(m), 'mismatches': post_bad, 'overlayRows': len(overlay_paths)}
assert not post_bad
res['dest'] = DEST
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'overlayApplied'}, indent=1))
