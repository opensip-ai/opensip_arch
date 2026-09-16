"""v2 continuation setup: verify and copy the v1 coauthor/pristine trees and probes into this runtime.

1. Verify parent frozen37 manifest (245ef613...), immutable overlay manifest (db9b7b3f...) and every file of the
   reviewer's immutable overlay copy (overlay rows = manifest sha256/bytes, others = frozen37 sha256, no extras).
2. Snapshot every v1 runtime file hash (receipts/v1-inventory.<label>.json) so v1 immutability can be proven later.
3. Verify v1 public receipts: edit-hashes.json facts, proposed-edits.diff sha, copy receipts' manifest hashes.
4. Copy v1 work/source37-pristine and work/source37-coauthor into work/ (refuses reuse; excludes cache dirs).
   Pristine must equal the input overlay exactly; coauthor must equal it except exactly the six v1 edits, whose
   bytes must equal v1 edit-hashes afterSha256.
5. Port v1 probes by replacing only the runtime path constant; record source and ported hashes.
usage: python -I -B continue_setup.py [inventory-only LABEL]
"""
import hashlib, json, os, shutil, sys

RT = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v2'
V1 = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v1'
REVIEW = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
OVERLAY = REVIEW + '/work/source37-overlay'
MAN37 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
OVM = REVIEW + '/subject-manifest.json'
CACHE = {'__pycache__', '.pytest_cache', '.mypy_cache'}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def inventory(root):
    out = {}
    for d, ds, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = sha(p)
    return out


def write(name, value):
    os.makedirs(RT + '/receipts', exist_ok=True)
    json.dump(value, open(RT + '/receipts/' + name, 'w'), indent=1)


if len(sys.argv) == 3 and sys.argv[1] == 'inventory-only':
    inv = inventory(V1)
    prior = json.load(open(RT + '/receipts/v1-inventory.before.json'))['files']
    res = {'label': sys.argv[2], 'files': len(inv), 'equalToBefore': inv == prior,
           'changed': sorted(k for k in prior if inv.get(k) != prior[k]), 'extra': sorted(k for k in inv if k not in prior)}
    write('v1-inventory.' + sys.argv[2] + '.json', dict(res, filesHash=inv))
    print(json.dumps(res, indent=1))
    sys.exit(0 if res['equalToBefore'] else 1)


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x


res = {'parentManifestSha256': sha(MAN37), 'overlayManifestSha256': sha(OVM)}
assert res['parentManifestSha256'] == '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
assert res['overlayManifestSha256'] == 'db9b7b3f3fbec833229fbd6e0c37cdc7bfed35ffabf3b6baabf709d35b380e52'
expect = {r['path']: r['sha256'] for r in rows(json.load(open(MAN37)))}
ovrows = {f['path']: f for f in json.load(open(OVM))['files']}
for p, f in ovrows.items():
    expect[p] = f['sha256']
ov_inv = inventory(OVERLAY)
res['immutableOverlayVerified'] = {'entries': len(expect), 'mismatch': sorted(p for p in expect if ov_inv.get(p) != expect[p]),
                                   'extra': sorted(p for p in ov_inv if p not in expect)}
assert not res['immutableOverlayVerified']['mismatch'] and not res['immutableOverlayVerified']['extra']

v1_inv = inventory(V1)
write('v1-inventory.before.json', {'root': V1, 'files': v1_inv})
res['v1InventoryFiles'] = len(v1_inv)
res['v1CacheOrSessionPaths'] = sorted(p for p in v1_inv if set(p.split(os.sep)) & CACHE)

eh = json.load(open(V1 + '/receipts/edit-hashes.json'))
assert eh['inputOverlayManifestSha256'] == res['overlayManifestSha256'] and eh['parentManifestSha256'] == res['parentManifestSha256']
diff_sha = sha(V1 + '/proposed-edits.diff')
res['v1EditHashes'] = {'sha256': sha(V1 + '/receipts/edit-hashes.json'), 'proposedEditsDiffSha256Recorded': eh['proposedEditsDiffSha256'],
                       'proposedEditsDiffSha256Actual': diff_sha, 'equal': diff_sha == eh['proposedEditsDiffSha256']}
assert res['v1EditHashes']['equal']
six = {f['path']: f for f in eh['files']}
assert len(six) == 6
for p, f in six.items():
    assert f['beforeSha256'] == expect[p], p
for name in ('copy.json', 'copy-pristine.json'):
    c = json.load(open(V1 + '/receipts/' + name))
    assert c['parentManifestSha256'] == res['parentManifestSha256'] and c['overlayManifestSha256'] == res['overlayManifestSha256']
    assert not c['inputOverlayVerified']['mismatchOrMissing'] and not c['copyVerified']['mismatches']
res['v1CopyReceipts'] = {n: sha(V1 + '/receipts/' + n) for n in ('copy.json', 'copy-pristine.json')}

for label in ('source37-pristine', 'source37-coauthor'):
    src, dst = V1 + '/work/' + label, RT + '/work/' + label
    if os.path.exists(dst):
        sys.exit('refusing to reuse ' + dst)
    skipped = []
    for d, ds, fs in os.walk(src):
        for x in [x for x in ds if x in CACHE]:
            skipped.append(os.path.relpath(os.path.join(d, x), src))
            ds.remove(x)
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), src)
            os.makedirs(os.path.dirname(os.path.join(dst, rel)), exist_ok=True)
            shutil.copyfile(os.path.join(src, rel), os.path.join(dst, rel))
    inv = inventory(dst)
    want = dict(expect)
    if label == 'source37-coauthor':
        for p, f in six.items():
            want[p] = f['afterSha256']
    res[label] = {'entries': len(inv), 'skippedCacheDirs': skipped,
                  'mismatch': sorted(p for p in want if inv.get(p) != want[p]), 'extra': sorted(p for p in inv if p not in want),
                  'differsFromInput': sorted(p for p in expect if inv.get(p) != expect[p])}
    assert not res[label]['mismatch'] and not res[label]['extra'], res[label]
assert res['source37-pristine']['differsFromInput'] == []
assert res['source37-coauthor']['differsFromInput'] == sorted(six)
res['sixFiles'] = {p: {'beforeSha256': f['beforeSha256'], 'afterSha256': f['afterSha256']} for p, f in sorted(six.items())}

ported = {}
os.makedirs(RT + '/probes', exist_ok=True)
for name in ('probe_exception_identity.py', 'run_check.py', 'make_diff.py'):
    raw = open(V1 + '/probes/' + name).read()
    old = "RT = '" + V1 + "'"
    assert raw.count(old) == 1, name
    new = raw.replace(old, "RT = '" + RT + "'")
    open(RT + '/probes/' + name, 'w').write(new)
    ported[name] = {'v1Sha256': hashlib.sha256(raw.encode()).hexdigest(), 'v2Sha256': hashlib.sha256(new.encode()).hexdigest(),
                    'onlyChange': 'RT constant ' + V1 + ' -> ' + RT}
res['portedProbes'] = ported
write('continue-setup.json', res)
print(json.dumps(res, indent=1))
