"""p00: regular copy of the completed readset-nesting-review.v1 work/source into this runtime's work/source.

Verifies the prior review's captured corrected files and dependencies still equal its p00 capture, copies
docs/ with shutil.copy2 (distinct inodes, st_nlink == 1, byte-equal), records a per-file hash map of the copy as the
delta baseline (receipts/baseline-file-hashes.json), and the hashes of the files this follow-up owns.
Output: receipts/p00-copy.json.
"""
import hashlib, json, shutil, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1')
PRIOR = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
OWNED = ['docs/coop/design-corrections/foundation/identity-model.v3.py',
         'docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py',
         'docs/v2/contracts/product-v1/identity-and-evidence.md',
         'docs/v2/contracts/product-v1/security-and-lifecycle.md']
prior = json.loads((PRIOR / 'receipts' / 'p00-capture.json').read_text())
out = {'standing': 'baseline copy for bounded A4 author follow-up; reference only'}
out['priorCorrectedUnchanged'] = all(sha(PRIOR / 'work/source' / r['path']) == r['captured'] for r in prior['correctedFiles'])
out['priorDependenciesUnchanged'] = all(sha(PRIOR / 'work/source' / p) == v['captured'] for p, v in prior['dependencies'].items())
out['priorReview'] = {n: sha(PRIOR / n) for n in ('review.md', 'review.json', 'correction.diff')}
dst = BASE / 'work' / 'source' / 'docs'
if dst.exists():
    raise SystemExit('refusing to overwrite ' + str(dst))
shutil.copytree(PRIOR / 'work' / 'source' / 'docs', dst, copy_function=shutil.copy2)
hashes, bad = {}, []
for p in sorted(dst.rglob('*')):
    if not p.is_file():
        continue
    rel = str(p.relative_to(BASE / 'work' / 'source'))
    s, o = p.stat(), (PRIOR / 'work' / 'source' / rel).stat()
    h = sha(p)
    if s.st_nlink != 1 or s.st_ino == o.st_ino or h != sha(PRIOR / 'work' / 'source' / rel):
        bad.append(rel)
    hashes[rel] = h
(BASE / 'receipts').mkdir(exist_ok=True)
(BASE / 'receipts' / 'baseline-file-hashes.json').write_text(json.dumps(hashes, indent=0, sort_keys=True) + '\n')
out['copy'] = {'files': len(hashes), 'problems': bad[:10], 'ok': not bad}
out['ownedBaseline'] = {p: hashes[p] for p in OWNED}
out['allOk'] = out['priorCorrectedUnchanged'] and out['priorDependenciesUnchanged'] and out['copy']['ok']
(BASE / 'receipts' / 'p00-copy.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
sys.exit(0 if out['allOk'] else 1)
