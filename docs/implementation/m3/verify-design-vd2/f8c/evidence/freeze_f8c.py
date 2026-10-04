"""Freeze the F8c candidate from the prepared worktree; never touches the live product.

The worktree is main cca4fe4 (r2; r1 used 4c761e8, whose four F8c files and tool are byte-identical)
plus VD2-a's two files (tools/verify_design.py and tools/tests/test_design_binding.py) and F8c's
four re-pinned files, with design-lock.json either HEAD's or already staged. It copies:
- the four F8c product files to product/;
- VD2-a's tools/verify_design.py to reference/tools/verify_design.py;
- VD2-a's tool diff (git diff HEAD -- tools/verify_design.py) to reference/verify_design.vd2a.diff,
  and asserts that applying it to the parent (F8b's reference copy, c13d231e) gives the candidate.
Then it writes materialization-map.json, successor.json (parents and candidates sorted by path),
the subject manifest ../f8c-subject.json and the draft unit record ../f8c-unit.json
(DRAFT-PENDING-REVIEW, not in the subject). Candidates are every file under f8c/ except
successor.json. Parents are the selected copies of the base bytes: I1-a's closure, registry
and report.ts, F8b's lane registry and F8b's reference verify_design.py; each must equal HEAD.
Usage: freeze_f8c.py WORKTREE"""
from pathlib import Path
import hashlib, json, subprocess, sys, tempfile
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = Path(sys.argv[1]).resolve(strict=True)
V = 'docs/implementation/m3/verify-design-vd2'; D = V + '/f8c'
F8B = 'docs/implementation/m2/generator-closure-f8b'; I1A = 'docs/implementation/m3/preview-pack-i1/i1-a'
CHANGED = sorted(['tools/contracts/generator-closure.json', 'schemas/registry.json',
                  'apps/report/src/generated/report.ts', 'tools/typescript-lanes.json'])
VD2A = ['tools/tests/test_design_binding.py', 'tools/verify_design.py']
PARENTS = {I1A + '/product/apps/report/src/generated/report.ts': 'apps/report/src/generated/report.ts',
           I1A + '/product/schemas/registry.json': 'schemas/registry.json',
           I1A + '/product/tools/contracts/generator-closure.json': 'tools/contracts/generator-closure.json',
           F8B + '/product/tools/typescript-lanes.json': 'tools/typescript-lanes.json',
           F8B + '/reference/tools/verify_design.py': 'tools/verify_design.py'}
EXCLUDED = {D + '/successor.json'}
def dig(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def pin(p): return {'path': p, **dig((A / p).read_bytes())}
def save(p, v): (A / p).parent.mkdir(parents=True, exist_ok=True); (A / p).write_text(json.dumps(v, indent=2) + '\n')
def git(*a): return subprocess.check_output(['git', *a], cwd=W)
base = git('rev-parse', 'HEAD').decode().strip()
assert base.startswith('cca4fe4'), base
changed = sorted(git('diff', '--name-only', 'HEAD').decode().split())
assert changed in (sorted(CHANGED + VD2A), sorted(CHANGED + VD2A + ['design-lock.json'])), changed
assert not git('status', '--porcelain', '--untracked-files=normal').decode().count('??'), 'untracked product files'
files = []
for name in CHANGED:
    before = git('show', f'HEAD:{name}'); after = (W / name).read_bytes(); target = f'{D}/product/{name}'
    (A / target).parent.mkdir(parents=True, exist_ok=True); (A / target).write_bytes(after)
    files.append({'productPath': name, 'candidatePath': target, 'before': dig(before), 'after': dig(after)})
# VD2-a's tool bytes and their provenance from the parent.
vd = (W / 'tools/verify_design.py').read_bytes(); old_vd = git('show', 'HEAD:tools/verify_design.py')
assert dig(old_vd)['sha256'] == 'c13d231eb755a08a33fae674426861145758c5ec136ba2cd6dd4b0f1020f8f08' and vd != old_vd
diff = git('diff', 'HEAD', '--', 'tools/verify_design.py')
(A / D / 'reference/tools').mkdir(parents=True, exist_ok=True)
(A / D / 'reference/tools/verify_design.py').write_bytes(vd)
(A / D / 'reference/verify_design.vd2a.diff').write_bytes(diff)
with tempfile.TemporaryDirectory() as tmp:
    (Path(tmp) / 'tools').mkdir()
    (Path(tmp) / 'tools/verify_design.py').write_bytes((A / F8B / 'reference/tools/verify_design.py').read_bytes())
    subprocess.run(['git', 'apply', str(A / D / 'reference/verify_design.vd2a.diff')], cwd=tmp, check=True)
    assert (Path(tmp) / 'tools/verify_design.py').read_bytes() == vd, 'the VD2-a diff does not turn the parent into the candidate'
save(f'{D}/materialization-map.json', {
    'schemaVersion': 1,
    'standing': 'Exact prospective development materialization for F8c; independent review, root assent and a fresh public drift check are required before selection.',
    'baseProductHead': base, 'files': files,
    'vd2aTool': {'productPath': 'tools/verify_design.py', 'candidatePath': f'{D}/reference/tools/verify_design.py',
                 'diffPath': f'{D}/reference/verify_design.vd2a.diff', 'parentPath': f'{F8B}/reference/tools/verify_design.py',
                 'before': dig(old_vd), 'after': dig(vd), 'diff': dig(diff),
                 'standing': "VD2-a's reviewed tool bytes, carried so the re-pinned rows name a selected copy; VD2-a's tests are not carried."}})
parents = [pin(p) for p in sorted(PARENTS)]
for p in parents:
    assert dig(git('show', f'HEAD:{PARENTS[p["path"]]}'))['sha256'] == p['sha256'], 'parent differs from base product: ' + p['path']
paths = sorted(str(p.relative_to(A)) for p in (A / D).rglob('*') if p.is_file())
assert not any('__pycache__' in p or p.endswith('.pyc') or p.endswith('.DS_Store') for p in paths), 'stray files'
candidates = [pin(p) for p in paths if p not in EXCLUDED]
record = {'schemaVersion': 1,
          'standing': ("PROPOSED F8c generator-closure and lane-registry successor (law VD2 r1, 'F8c'): re-pins tools/verify_design.py to VD2-a's "
                       'bytes in the contract generator closure and the TypeScript lane registry, and updates the registry closure digest and '
                       "report.ts provenance header; no rebuild, receipt or toolchain change (rebuild-02 stays selected); carries VD2-a's "
                       'tool bytes as a reference copy; exact frozen candidate requires actual independent review and root assent.'),
          'parents': parents, 'passageOverrides': [], 'candidates': candidates}
save(f'{D}/successor.json', record)
subject = {'schemaVersion': 1, 'files': sorted(candidates + [pin(f'{D}/successor.json')], key=lambda r: r['path'])}
save(f'{V}/f8c-subject.json', subject)
unit = {'schemaVersion': 1, 'unit': 'generator-closure-f8c', 'status': 'DRAFT-PENDING-REVIEW',
        'subjectManifest': pin(f'{V}/f8c-subject.json'),
        'independentReview': {'path': 'docs/implementation/m3/reviews/codex-vd2a-r2/review-contract.json', 'bytes': None, 'sha256': None},
        'rootSubstantiveAssent': False, 'requiredUnitFindings': [], 'acceptedSuccessor': pin(f'{D}/successor.json'),
        'rootAssessment': 'DRAFT. Completed by the lead after Codex review: status ACCEPTED-DESIGN-UNIT, the review pin, rootSubstantiveAssent true.',
        'fullM2Complete': False, 'productQualification': False}
save(f'{V}/f8c-unit.json', unit)
print(json.dumps({'baseProductHead': base, 'mapped': len(files), 'parents': len(parents), 'candidates': len(candidates),
                  'successor': pin(f'{D}/successor.json'), 'subject': pin(f'{V}/f8c-subject.json'), 'unitDraft': pin(f'{V}/f8c-unit.json')}, indent=2))
