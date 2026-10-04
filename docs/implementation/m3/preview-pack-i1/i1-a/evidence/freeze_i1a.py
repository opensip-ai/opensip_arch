"""Freeze the I1-a contract-successor candidate from the prepared worktree; never
touches the live product.

- Copies every changed product file except the two schema sources to
  i1-a/product/<path>. The schema sources are mapped to I1-L's accepted product
  copies (I1-L materialization-map.json), which they equal byte for byte, so
  those bytes keep one authority.
- Writes i1-a/schemas/admission-registry.json, the architecture copy that the
  product admission source map now names (registryArchitectureSource), with the
  product file's exact bytes.
- Copies the scratch phase reports and the generation summary into evidence/.
- Writes materialization-map.json, successor.json (parents and candidates sorted
  by path; no passage overrides), the subject manifest, and the draft unit
  record (DRAFT-PENDING-REVIEW; not a subject member).

Candidates are every file under i1-a/ except successor.json. Parents are the
currently selected architecture copies of the changed files' base bytes, plus
the three I1-L copies whose bytes and paths I1-a pins. The worktree may carry
the staged design-lock.json; it is outside the materialization.
Usage: freeze_i1a.py WORKTREE SCRATCH_DIR (SCRATCH_DIR holds pins-report.json,
policies-report.json and gen-candidate/summary.json)."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = Path(sys.argv[1]).resolve(strict=True); S = Path(sys.argv[2]).resolve(strict=True)
M = 'docs/implementation/m3/preview-pack-i1'; D = M + '/i1-a'; L = M + '/i1-l'
BASE = '5e25d04b3bfa85a244f5d958fe089e9626fd33fa'
CHANGED = sorted(['apps/report/src/generated/report.ts', 'crates/contracts/src/generated/evidence.rs',
                  'crates/contracts/src/generated/identity.rs', 'crates/evaluator/src/atom-registry.json',
                  'crates/host/src/schema_sources.rs', 'crates/identity/src/schema_registry.rs',
                  'schemas/admission-registry.json', 'schemas/admission-source-map.json', 'schemas/registry.json',
                  'schemas/source-map.json', 'schemas/sources/identity-v3.schema.json', 'schemas/sources/policy-v2.schema.json',
                  'tools/contracts/dependency-policy.json', 'tools/contracts/generator-closure.json',
                  'tools/identity/dependency-policy.json'])
I1L_COPIES = {'schemas/sources/identity-v3.schema.json': L + '/product/schemas/sources/identity-v3.schema.json',
              'schemas/sources/policy-v2.schema.json': L + '/product/schemas/sources/policy-v2.schema.json'}
PARENTS = sorted(['docs/implementation/m2/existing-root-diagnostics-468a/product/crates/contracts/src/generated/evidence.rs',
                  'docs/implementation/m2/existing-root-diagnostics-468a/product/crates/host/src/schema_sources.rs',
                  'docs/implementation/m2/existing-root-diagnostics-468a/product/crates/identity/src/schema_registry.rs',
                  'docs/implementation/m2/existing-root-diagnostics-468a/product/schemas/admission-source-map.json',
                  'docs/implementation/m2/existing-root-diagnostics-468a/product/schemas/source-map.json',
                  'docs/implementation/m2/existing-root-diagnostics-468a/schemas/admission-registry.json',
                  'docs/implementation/m2/generator-closure-f8b/product/apps/report/src/generated/report.ts',
                  'docs/implementation/m2/generator-closure-f8b/product/schemas/registry.json',
                  'docs/implementation/m2/generator-closure-f8b/product/tools/contracts/generator-closure.json',
                  L + '/design/workflows/schemas/policy-document.v2.schema.json',
                  L + '/product/schemas/sources/identity-v3.schema.json',
                  L + '/product/schemas/sources/policy-v2.schema.json'])
# Parent pins whose bytes are a changed file's base bytes, by product path.
SUPERSEDED = {'crates/contracts/src/generated/evidence.rs': PARENTS[0], 'crates/host/src/schema_sources.rs': PARENTS[1],
              'crates/identity/src/schema_registry.rs': PARENTS[2], 'schemas/admission-source-map.json': PARENTS[3],
              'schemas/source-map.json': PARENTS[4], 'schemas/admission-registry.json': PARENTS[5],
              'apps/report/src/generated/report.ts': PARENTS[6], 'schemas/registry.json': PARENTS[7],
              'tools/contracts/generator-closure.json': PARENTS[8]}
EXCLUDED = {D + '/successor.json'}
def dig(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def pin(p): return {'path': p, **dig((A / p).read_bytes())}
def save(p, v): (A / p).parent.mkdir(parents=True, exist_ok=True); (A / p).write_text(json.dumps(v, indent=2) + '\n')
def git(*a): return subprocess.check_output(['git', *a], cwd=W)
assert git('rev-parse', 'HEAD').decode().strip() == BASE
changed = sorted(git('diff', '--name-only', 'HEAD').decode().split())
assert changed in (CHANGED, sorted(CHANGED + ['design-lock.json'])), changed
assert '??' not in git('status', '--porcelain', '--untracked-files=normal').decode(), 'untracked product files'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', D, D + '-subject.json', D + '-unit.json'], capture_output=True, text=True, check=True).stdout
assert not tracked.strip(), 'refusing to overwrite tracked candidate paths: ' + tracked
for stale in (A / D / 'product', A / D / 'schemas'):
    if stale.exists(): shutil.rmtree(stale)
files = []
for name in CHANGED:
    before = git('show', f'HEAD:{name}'); after = (W / name).read_bytes()
    if name in I1L_COPIES:
        target = I1L_COPIES[name]
        assert (A / target).read_bytes() == after, 'product source differs from the I1-L copy: ' + name
    else:
        target = f'{D}/product/{name}'
        (A / target).parent.mkdir(parents=True, exist_ok=True); (A / target).write_bytes(after)
    if name in SUPERSEDED:
        assert dig(before) == {k: v for k, v in pin(SUPERSEDED[name]).items() if k != 'path'}, 'parent differs from base: ' + name
    files.append({'productPath': name, 'candidatePath': target, 'before': dig(before), 'after': dig(after)})
registry = (W / 'schemas/admission-registry.json').read_bytes()
(A / D / 'schemas').mkdir(parents=True, exist_ok=True); (A / D / 'schemas/admission-registry.json').write_bytes(registry)
source_map = json.loads((W / 'schemas/admission-source-map.json').read_bytes())
assert source_map['registryArchitectureSource'] == {'path': D + '/schemas/admission-registry.json', **dig(registry)}
for name in ('pins-report.json', 'policies-report.json'):
    shutil.copyfile(S / name, A / D / 'evidence' / name)
shutil.copyfile(S / 'gen-candidate/summary.json', A / D / 'evidence/generation-summary.json')
save(f'{D}/materialization-map.json', {
    'schemaVersion': 1,
    'standing': 'Exact prospective development materialization for unit I1-a (M3-I1 r2): the two product schema sources are I1-L\'s accepted copies byte for byte; every consumer pin, the generator closure, the admission registry and the generated outputs follow. Independent review, root assent and a fresh public drift check are required before selection.',
    'baseProductHead': BASE, 'files': files})
parents = [pin(p) for p in PARENTS]
paths = sorted(str(p.relative_to(A)) for p in (A / D).rglob('*') if p.is_file())
assert not any('__pycache__' in p or p.endswith('.pyc') or p.endswith('.DS_Store') for p in paths), 'stray files'
candidates = [pin(p) for p in paths if p not in EXCLUDED]
record = {'schemaVersion': 1,
          'standing': 'PROPOSED I1-a contract successor (law M3-I1 r2, unit I1-a): materializes I1-L\'s accepted policy-v2 and identity-v3 product schema copies (the appended cycle-representative member and the r2 majorLaw text), re-points the generation and admission source maps to them, and carries the admission registry, generator closure, registries, native and atom-registry pins, dependency-policy pins and regenerated contracts that follow; no passage overrides and no inventory successor. Exact frozen candidate requires actual independent review and root assent.',
          'parents': parents, 'passageOverrides': [], 'candidates': candidates}
save(f'{D}/successor.json', record)
subject = {'schemaVersion': 1, 'files': sorted(candidates + [pin(f'{D}/successor.json')], key=lambda r: r['path'])}
save(f'{D}-subject.json', subject)
unit = {'schemaVersion': 1, 'unit': 'm3-i1-a', 'status': 'DRAFT-PENDING-REVIEW',
        'subjectManifest': pin(f'{D}-subject.json'),
        'independentReview': {'path': 'docs/implementation/m3/reviews/codex2-i1a-r1/review-contract.json', 'bytes': None, 'sha256': None},
        'rootSubstantiveAssent': False, 'requiredUnitFindings': [], 'acceptedSuccessor': pin(f'{D}/successor.json'),
        'rootAssessment': 'DRAFT. Completed by the lead after CODEX2 review: status ACCEPTED-DESIGN-UNIT, the review-contract.json pin, rootSubstantiveAssent true.',
        'fullM2Complete': False, 'productQualification': False}
save(f'{D}-unit.json', unit)
print(json.dumps({'baseProductHead': BASE, 'mapped': len(files), 'parents': len(parents), 'candidates': len(candidates),
                  'successor': pin(f'{D}/successor.json'), 'subject': pin(f'{D}-subject.json'), 'unitDraft': pin(f'{D}-unit.json')}, indent=2))
