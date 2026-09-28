"""Freeze the 468a candidate from the prepared worktree; never touch the live product."""
from pathlib import Path
import hashlib, json, shutil, subprocess
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = A.parent / 'opensip-468a'
M = 'docs/implementation/m2'; D = M + '/existing-root-diagnostics-468a'
S = Path('/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/468a')
def dig(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def pin(p): return {'path': p, **dig((A / p).read_bytes())}
def save(p, v): (A / p).parent.mkdir(parents=True, exist_ok=True); (A / p).write_text(json.dumps(v, indent=2) + '\n')
base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=W, text=True).strip()
changed = subprocess.check_output(['git', 'diff', '--name-only'], cwd=W, text=True).split()
assert subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=W, text=True).count('\n') == len(changed) == 10
files = []
for name in sorted(changed):
    before = subprocess.check_output(['git', 'show', f'HEAD:{name}'], cwd=W)
    after = (W / name).read_bytes()
    target = f'{D}/product/{name}'
    (A / target).parent.mkdir(parents=True, exist_ok=True); (A / target).write_bytes(after)
    files.append({'productPath': name, 'candidatePath': target, 'before': dig(before), 'after': dig(after)})
assert (W / 'schemas/sources/common-v4.schema.json').read_bytes() == (A / D / 'schemas/common.v4.schema.json').read_bytes()
assert (W / 'schemas/admission-registry.json').read_bytes() == (A / D / 'schemas/admission-registry.json').read_bytes()
save(f'{D}/materialization-map.json', {'schemaVersion': 1, 'standing': 'Exact prospective development materialization for 468a; independent review, root assent and a fresh public drift check are required before selection.', 'baseProductHead': base, 'files': files})
shutil.copyfile(S / 'gen-candidate/summary.json', A / D / 'evidence/generation-summary.json')
overrides = json.loads((S / 'overrides.json').read_text())
parents = {o['parent']['path']: o['parent'] for o in overrides}
for p in [M + '/initial-root-binding-owner-selection-v1/schemas/common.v4.schema.json',
          M + '/initial-root-binding-owner-selection-v1/schemas/admission-registry.json',
          M + '/initial-root-binding-owner-selection-v1/reference/public-detail-registry.json',
          M + '/initial-root-binding-owner-selection-v1/diagnostic-routes.json']:
    parents[p] = pin(p)
cand_paths = sorted(str(p.relative_to(A)) for p in (A / D).rglob('*') if p.is_file() and p.name != 'successor.json')
record = {'schemaVersion': 1,
          'standing': 'PROPOSED 468a existing-root diagnostics successor: three appended common4 domain details (CORE.NO_EMBEDDED_RELEASE, INSTALLATION.ACCOUNT_REFUSED, WORK.BUDGET_EXHAUSTED), the law 468 item 6 D9 routes, law 468 item 8 golden wording, and three refreshed inventory v74 descriptions; exact frozen candidate requires actual independent review and root assent.',
          'parents': [parents[k] for k in sorted(parents)], 'passageOverrides': overrides,
          'candidates': [pin(p) for p in cand_paths]}
save(f'{D}/successor.json', record)
save(f'{D}-subject.json', {'schemaVersion': 1, 'files': sorted([pin(p) for p in cand_paths] + [pin(f'{D}/successor.json')], key=lambda r: r['path'])})
print(json.dumps({'mapped': len(files), 'candidates': len(cand_paths), 'parents': len(parents), 'overrides': len(overrides),
                  'successor': pin(f'{D}/successor.json'), 'subject': pin(f'{D}-subject.json')}, indent=2))
