"""p00: capture. Regular copy of the current successor source docs (minus design-corrections/reviews and __pycache__)
into work/source, then exact hashes of the three corrected files (against root correction.json), root's retained
before-files (against beforeSha256), the owner dependencies the A4 join and its controls load, and root's correction
artifacts. Every copied file is checked for a distinct inode, st_nlink == 1 and byte equality with the source at copy
time. Later steps read only this copy. Output: receipts/p00-capture.json.
"""
import hashlib, json, shutil, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1')
SRC = Path('/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source')
ROOT = Path('/tmp/opensip-design-corrections/root-source39-readset-nesting.v1')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
DC = 'docs/coop/design-corrections/'
DEPS = [DC + 'discovery-defaults.py', DC + 'foundation/check-semantic-replay.v3.py', DC + 'foundation/evaluator_semantic_fixture.v3.py',
        DC + 'foundation/evaluator_replay_model.v3.py', DC + 'foundation/identity-schemas.v3.json', DC + 'foundation/canonical.py',
        DC + 'native/native_evidence_model.v2.py', DC + 'native/native-evidence.schemas.v2.json',
        'docs/v2/contracts/product-v1/native-evidence.md', 'docs/v2/contracts/product-v1/security-and-lifecycle.md']

out = {'standing': 'capture for a bounded read-only peer review; reference only'}
corr = json.loads((ROOT / 'correction.json').read_text())
dst = BASE / 'work' / 'source' / 'docs'
if dst.exists():
    raise SystemExit('refusing to overwrite ' + str(dst))
ignore = shutil.ignore_patterns('__pycache__')


def ign(d, names):
    skip = set(ignore(d, names))
    if Path(d) == SRC / 'docs/coop/design-corrections':
        skip.add('reviews')
    return skip


pre = {p: sha(SRC / p) for p in [f['path'] for f in corr['files']] + DEPS}
shutil.copytree(SRC / 'docs', dst, ignore=ign, copy_function=shutil.copy2)
n, bad = 0, []
for p in dst.rglob('*'):
    if not p.is_file():
        continue
    rel = str(p.relative_to(BASE / 'work' / 'source'))
    s, o = p.stat(), (SRC / rel).stat()
    if s.st_nlink != 1 or s.st_ino == o.st_ino or p.read_bytes() != (SRC / rel).read_bytes():
        bad.append(rel)
    n += 1
out['copy'] = {'files': n, 'problems': bad[:10], 'ok': not bad}
rows = []
for f in corr['files']:
    rows.append({'path': f['path'], 'captured': sha(BASE / 'work/source' / f['path']), 'rootAfter': f['sha256'],
                 'rootBeforeFile': sha(ROOT / 'before-files' / f['path']), 'rootBefore': f['beforeSha256'],
                 'sourceUnchangedDuringCopy': pre[f['path']] == sha(SRC / f['path'])})
out['correctedFiles'] = rows
out['correctedFilesMatchRoot'] = all(r['captured'] == r['rootAfter'] and r['rootBeforeFile'] == r['rootBefore'] and r['sourceUnchangedDuringCopy'] for r in rows)
out['dependencies'] = {p: {'captured': sha(BASE / 'work/source' / p), 'sourceUnchangedDuringCopy': pre[p] == sha(SRC / p)} for p in DEPS}
out['rootArtifacts'] = {str(p.relative_to(ROOT)): sha(p) for p in sorted(ROOT.rglob('*')) if p.is_file()}
out['allOk'] = out['copy']['ok'] and out['correctedFilesMatchRoot'] and all(v['sourceUnchangedDuringCopy'] for v in out['dependencies'].values())
(BASE / 'receipts').mkdir(exist_ok=True)
(BASE / 'receipts' / 'p00-capture.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
sys.exit(0 if out['allOk'] else 1)
