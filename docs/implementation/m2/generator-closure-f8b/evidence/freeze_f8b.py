"""Freeze the F8b candidate from the prepared worktree; never touches the live product.

Copies the 9 changed product files to product/, the live verify_design.py to
reference/tools/, and rebuild-02's receipt and logs to evidence/generator-rebuild/. Then writes
materialization-map.json, successor.json (parents and candidates sorted by path) and the
subject manifest, plus the draft unit record (DRAFT-PENDING-REVIEW, not in the subject).
Candidates are every file under generator-closure-f8b/ except successor.json, PROPOSAL.md
(mutable status line) and PROPOSAL-r1.md (superseded). The accepted PROPOSAL-r2.md is one.
Usage: freeze_f8b.py WORKTREE REBUILD02_DIR"""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = Path(sys.argv[1]).resolve(strict=True); R2 = Path(sys.argv[2]).resolve(strict=True)
M = 'docs/implementation/m2'; D = M + '/generator-closure-f8b'
CHANGED = sorted(['tools/contracts/Cargo.toml', 'tools/contracts/package.json', 'tools/typescript-boundary/package.json',
                  'tools/contracts/build-receipt.json', 'tools/contracts/toolchain.json', 'tools/contracts/generator-closure.json',
                  'schemas/registry.json', 'apps/report/src/generated/report.ts', 'tools/typescript-lanes.json'])
PARENTS = sorted([M + '/existing-root-diagnostics-468a/product/apps/report/src/generated/report.ts',
                  M + '/existing-root-diagnostics-468a/product/schemas/registry.json',
                  M + '/existing-root-diagnostics-468a/product/tools/contracts/generator-closure.json',
                  M + '/native-repin-selection-v1/product/tools/contracts/build-receipt.json',
                  M + '/native-repin-selection-v1/product/tools/contracts/toolchain.json',
                  'docs/implementation/m1/generator-selection-v2/product/tools/contracts/Cargo.toml',
                  'docs/implementation/m1/generator-selection-v2/product/tools/contracts/package.json',
                  'docs/implementation/m1/bootstrap-selection-v1/product/tools/typescript-boundary/package.json',
                  M + '/typescript-closure-selection-v1/product/tools/typescript-lanes.json',
                  M + '/admission-runtime-selection-v1/product/tools/verify_design.py'])
EXCLUDED = {D + '/successor.json', D + '/PROPOSAL.md', D + '/PROPOSAL-r1.md'}
def dig(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def pin(p): return {'path': p, **dig((A / p).read_bytes())}
def save(p, v): (A / p).parent.mkdir(parents=True, exist_ok=True); (A / p).write_text(json.dumps(v, indent=2) + '\n')
def git(*a): return subprocess.check_output(['git', *a], cwd=W)
base = git('rev-parse', 'HEAD').decode().strip()
changed = sorted(git('diff', '--name-only', 'HEAD').decode().split())
assert changed in (CHANGED, sorted(CHANGED + ['design-lock.json'])), changed
assert not git('status', '--porcelain', '--untracked-files=normal').decode().count('??'), 'untracked product files'
files = []
for name in CHANGED:
    before = git('show', f'HEAD:{name}'); after = (W / name).read_bytes(); target = f'{D}/product/{name}'
    (A / target).parent.mkdir(parents=True, exist_ok=True); (A / target).write_bytes(after)
    files.append({'productPath': name, 'candidatePath': target, 'before': dig(before), 'after': dig(after)})
vd = (W / 'tools/verify_design.py').read_bytes()
assert vd == git('show', 'HEAD:tools/verify_design.py') and dig(vd)['sha256'] == 'c13d231eb755a08a33fae674426861145758c5ec136ba2cd6dd4b0f1020f8f08'
(A / D / 'reference/tools').mkdir(parents=True, exist_ok=True); (A / D / 'reference/tools/verify_design.py').write_bytes(vd)
(A / D / 'evidence/generator-rebuild').mkdir(parents=True, exist_ok=True)
for name in ('receipt.json', 'build.stdout.jsonl', 'build.stderr.log'):
    shutil.copyfile(R2 / name, A / D / 'evidence/generator-rebuild' / name)
assert (A / D / 'evidence/generator-rebuild/receipt.json').read_bytes() == (W / 'tools/contracts/build-receipt.json').read_bytes()
save(f'{D}/materialization-map.json', {'schemaVersion': 1, 'standing': 'Exact prospective development materialization for F8b; independent review, root assent and a fresh public drift check are required before selection.', 'baseProductHead': base, 'files': files})
parents = [pin(p) for p in PARENTS]
for p in parents:
    product = p['path'].split('/product/', 1)[1]
    if product != 'tools/verify_design.py':
        assert dig(git('show', f'HEAD:{product}'))['sha256'] == p['sha256'], 'parent differs from base product: ' + p['path']
    else:
        assert p['sha256'] == '2764cf7b5e3aaa7fb1722bab6714fe1eed4a350867f4cc369d0490342527325c'
paths = sorted(str(p.relative_to(A)) for p in (A / D).rglob('*') if p.is_file())
assert not any('__pycache__' in p or p.endswith('.pyc') or p.endswith('.DS_Store') for p in paths), 'stray files'
candidates = [pin(p) for p in paths if p not in EXCLUDED]
record = {'schemaVersion': 1,
          'standing': 'PROPOSED F8b generator-closure and lane-registry successor: re-pins tools/verify_design.py (pre-VD1) in the contract generator closure and the TypeScript lane registry, installs the observed rebuild-02 receipt and generator pin for license metadata in tools/contracts/Cargo.toml, licenses the three L1-excluded tooling manifests, and updates the registry closure digest and report.ts provenance; exact frozen candidate requires actual independent review and root assent.',
          'parents': parents, 'passageOverrides': [], 'candidates': candidates}
save(f'{D}/successor.json', record)
subject = {'schemaVersion': 1, 'files': sorted(candidates + [pin(f'{D}/successor.json')], key=lambda r: r['path'])}
save(f'{D}-subject.json', subject)
unit = {'schemaVersion': 1, 'unit': 'generator-closure-f8b', 'status': 'DRAFT-PENDING-REVIEW',
        'subjectManifest': pin(f'{D}-subject.json'),
        'independentReview': {'path': f'{M}/reviews/codex2-generator-closure-f8b-unit-r1/review.json', 'bytes': None, 'sha256': None},
        'rootSubstantiveAssent': False, 'requiredUnitFindings': [], 'acceptedSuccessor': pin(f'{D}/successor.json'),
        'rootAssessment': 'DRAFT. Completed by the lead after CODEX2 review: status ACCEPTED-DESIGN-UNIT, the review pin, rootSubstantiveAssent true.',
        'fullM2Complete': False, 'productQualification': False}
save(f'{D}-unit.json', unit)
print(json.dumps({'baseProductHead': base, 'mapped': len(files), 'parents': len(parents), 'candidates': len(candidates),
                  'successor': pin(f'{D}/successor.json'), 'subject': pin(f'{D}-subject.json'), 'unitDraft': pin(f'{D}-unit.json')}, indent=2))
