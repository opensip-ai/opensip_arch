"""Make a disposable exact copy of the frozen source37 snapshot and verify it against the manifest.

Usage: python -I -B make_copy.py DEST [--verify-only]
"""
import hashlib, json, os, shutil, sys

MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
EXPECTED = '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
dest = sys.argv[1]
verify_only = '--verify-only' in sys.argv
raw = open(MANIFEST, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == EXPECTED
m = json.loads(raw)
src = m['snapshotRoot']
if not verify_only:
    assert not os.path.exists(dest), dest
    shutil.copytree(src, dest, symlinks=True)
bad = []
listed = set()
for f in m['files']:
    listed.add(f['path'])
    p = os.path.join(dest, f['path'])
    if not os.path.isfile(p):
        bad.append({'path': f['path'], 'state': 'missing'}); continue
    b = open(p, 'rb').read()
    if hashlib.sha256(b).hexdigest() != f['sha256'] or len(b) != f['bytes']:
        bad.append({'path': f['path'], 'state': 'changed'})
extra = []
for d, _, fs in os.walk(dest):
    for fn in fs:
        rel = os.path.relpath(os.path.join(d, fn), dest)
        if rel not in listed:
            extra.append(rel)
res = {'dest': dest, 'manifestSha256': EXPECTED, 'files': len(m['files']), 'changedOrMissing': bad,
       'extraFiles': extra, 'exact': not bad and not extra}
print(json.dumps(res, indent=1))
