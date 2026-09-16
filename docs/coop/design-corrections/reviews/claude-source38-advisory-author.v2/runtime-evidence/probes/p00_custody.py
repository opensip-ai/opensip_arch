"""p00: custody and working copy for v2.

Records SHA-256 of every file of the completed v1 work/edited tree, v1 review files, root's assessment inputs and the
source38 bytes of v1's 10 touched files (manifest-checked), then copies v1 work/edited/docs to v2 work/edited/docs as
regular files (shutil.copy2), proving distinct inodes, st_nlink == 1 and byte equality. Whole-manifest scans are not
repeated: v1 p00 verified all 12904 members; here only the touched and v1-recorded dependency files are rechecked.
Output: receipts/p00-custody.json.
"""
import hashlib, json, shutil, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v2')
V1 = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
SRC = Path('/tmp/opensip-design-corrections/candidate-subject.v38')
ROOT = Path('/tmp/opensip-design-corrections/root-source38-advisory-assessment.v1')
MAN = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
out = {'standing': 'v2 custody and regular working copy; reference only'}
out['manifestSha256'] = sha(MAN)
manifest = {r['path']: r['sha256'] for r in json.loads(MAN.read_text())['files']}
v1final = json.loads((V1 / 'receipts' / 'p04-summary.final.json').read_text())
out['v1Review'] = {n: sha(V1 / n) for n in ('review.md', 'review.json', 'proposed-edits.diff')}
out['v1ReviewMatchesRootRecorded'] = out['v1Review']['review.json'] == '1f69efb90f57f8d45905a4d398331e000bdde6bd28647d5859b0f3d7c29274b9'
checks = []
for r in v1final['touched']:
    checks.append({'path': r['path'], 'source38': sha(SRC / r['path']), 'manifest': manifest[r['path']],
                   'v1Edited': sha(V1 / 'work' / 'edited' / r['path']), 'v1Recorded': r['afterSha256']})
out['v1Touched'] = checks
out['v1TouchedOk'] = all(c['source38'] == c['manifest'] and c['v1Edited'] == c['v1Recorded'] for c in checks)
deps = [d['path'] for d in v1final['dependencies']]
out['dependenciesOk'] = all(sha(SRC / p) == manifest[p] and sha(V1 / 'work' / 'edited' / p) == manifest[p] for p in deps)
out['rootAssessment'] = {p.name: sha(p) for p in sorted(ROOT.iterdir()) if p.is_file()}
v1files = {str(p.relative_to(V1 / 'work' / 'edited')): sha(p) for p in (V1 / 'work' / 'edited' / 'docs').rglob('*') if p.is_file()}
out['v1EditedTree'] = {'files': len(v1files), 'digest': hashlib.sha256(json.dumps(sorted(v1files.items())).encode()).hexdigest()}
dst = BASE / 'work' / 'edited' / 'docs'
if dst.exists():
    raise SystemExit('refusing to overwrite ' + str(dst))
shutil.copytree(V1 / 'work' / 'edited' / 'docs', dst, copy_function=shutil.copy2)
bad = []
n = 0
for p in dst.rglob('*'):
    if not p.is_file():
        continue
    rel = str(p.relative_to(BASE / 'work' / 'edited'))
    s, o = p.stat(), (V1 / 'work' / 'edited' / rel).stat()
    if s.st_nlink != 1 or s.st_ino == o.st_ino or sha(p) != v1files.get(rel):
        bad.append(rel)
    n += 1
out['copy'] = {'files': n, 'problems': bad[:10], 'equalToV1': n == len(v1files) and not bad}
(BASE / 'receipts' / 'v1-edited-file-hashes.json').parent.mkdir(exist_ok=True)
(BASE / 'receipts' / 'v1-edited-file-hashes.json').write_text(json.dumps(v1files, indent=0, sort_keys=True) + '\n')
out['allOk'] = out['manifestSha256'] == '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5' and out['v1TouchedOk'] \
    and out['dependenciesOk'] and out['copy']['equalToV1'] and out['v1ReviewMatchesRootRecorded']
(BASE / 'receipts' / 'p00-custody.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('v1Touched',)}, indent=1))
sys.exit(0 if out['allOk'] else 1)
