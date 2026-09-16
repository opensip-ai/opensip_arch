"""Verified disposable copy of the immutable input overlay (frozen37 + 12 root files) for coauthoring.

1. Verify parent frozen37 manifest (245ef613...) and immutable overlay manifest (db9b7b3f...).
2. Verify every file of the reviewer's overlay copy: overlay rows equal sha256/bytes, all other rows equal frozen37 sha256;
   no unlisted files. Verify every frozen37 source byte for the overlay rows equals beforeSha256.
3. Copy the verified bytes into work/source37-coauthor (refuses to reuse), re-verify the copy.
4. Record the root successor's hashes for the 12 overlay rows and for the files this coauthor may touch (read-only).
Writes only under this runtime.
"""
import hashlib, json, os, shutil, sys

RT = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v1'
REVIEW = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
OVERLAY = REVIEW + '/work/source37-overlay'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v37'
MAN37 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
OVM = REVIEW + '/subject-manifest.json'
SUCC = '/tmp/opensip-design-corrections/termination-exclusivity-successor.v1/source'
DEST = RT + '/work/' + (sys.argv[1] if len(sys.argv) > 1 else 'source37-coauthor')
OUT = RT + '/receipts/' + (sys.argv[2] if len(sys.argv) > 2 else 'copy.json')
TOUCH = [
    'docs/coop/design-corrections/workflows/query_projection_model.v3.py',
    'docs/coop/design-corrections/workflows/query-projection-contract.v3.md',
    'docs/coop/design-corrections/workflows/check-query-projection.v3.py',
    'docs/coop/design-corrections/foundation/identity-model.v3.py',
    'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py',
    'docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py',
    'docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md',
]


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


res = {'parentManifestSha256': sha_file(MAN37), 'overlayManifestSha256': sha_file(OVM)}
assert res['parentManifestSha256'] == '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
assert res['overlayManifestSha256'] == 'db9b7b3f3fbec833229fbd6e0c37cdc7bfed35ffabf3b6baabf709d35b380e52'
ov = json.load(open(OVM))
assert ov['baseManifestSha256'] == res['parentManifestSha256']
m = rows(json.load(open(MAN37)))
want = {r['path']: r['sha256'] for r in m}
ovrows = {f['path']: f for f in ov['files']}
assert set(ovrows) <= set(want)
bad_before = [p for p, f in ovrows.items() if sha_file(os.path.join(FROZEN, p)) != f['beforeSha256'] or want[p] != f['beforeSha256']]
res['frozenOverlayRowsEqualBefore'] = not bad_before
assert not bad_before, bad_before
expect = dict(want)
for p, f in ovrows.items():
    expect[p] = f['sha256']
    assert os.path.getsize(os.path.join(OVERLAY, p)) == f['bytes'], p
mism = [p for p, s in expect.items() if not os.path.isfile(os.path.join(OVERLAY, p)) or sha_file(os.path.join(OVERLAY, p)) != s]
extra = []
for dp, ds, fs in os.walk(OVERLAY):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), OVERLAY)
        if rel not in expect:
            extra.append(rel)
res['inputOverlayVerified'] = {'entries': len(expect), 'mismatchOrMissing': mism, 'unlisted': extra, 'overlayRows': len(ovrows)}
assert not mism and not extra
if os.path.exists(DEST):
    sys.exit('refusing to reuse existing ' + DEST)
for p in expect:
    d = os.path.join(DEST, p)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copyfile(os.path.join(OVERLAY, p), d)
post = [p for p, s in expect.items() if sha_file(os.path.join(DEST, p)) != s]
res['copyVerified'] = {'entries': len(expect), 'mismatches': post}
assert not post
succ = {}
for p in sorted(set(ovrows) | set(TOUCH)):
    sp = os.path.join(SUCC, p)
    succ[p] = {'successorSha256': sha_file(sp) if os.path.isfile(sp) else None, 'inputSha256': expect.get(p),
               'equal': os.path.isfile(sp) and sha_file(sp) == expect.get(p), 'overlayRow': p in ovrows}
res['rootSuccessorReadOnly'] = succ
res['successorSame12'] = all(v['equal'] for p, v in succ.items() if v['overlayRow'])
res['touchInputSha256'] = {p: expect[p] for p in TOUCH}
res['dest'] = DEST
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'rootSuccessorReadOnly'}, indent=1))
print(json.dumps(succ, indent=1))
