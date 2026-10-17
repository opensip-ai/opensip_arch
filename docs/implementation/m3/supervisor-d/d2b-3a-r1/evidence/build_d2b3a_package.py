"""Build the D2b-3a r1 architecture package in place: exact product copies with their parent and candidate pins
(product-map.json), the source record, the lane evidence, and the subject manifest, which also names the proposed plan
amendment A2 (supervisor-d/d2b/PLAN-r3-A2.md) the review judges with the unit. Usage: build_d2b3a_package.py <lane dir>."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = A.parent / 'opensip-d2b3'; P = A.parent / 'opensip'
LANE = Path(sys.argv[1])
PRE = 'docs/implementation/m3/supervisor-d/d2b-3a-r1'; U = A / PRE; SUBJECT = 'docs/implementation/m3/supervisor-d/d2b-3a-r1-subject.json'
A2 = 'docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A2.md'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def git(root, *a): return subprocess.run(['/usr/bin/git', *a], cwd=root, env=E, capture_output=True, check=False)
def pin_bytes(path, b): return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def pin(root, path): return pin_bytes(path, (root / path).read_bytes())
def write(p, j): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(j, indent=2) + '\n')

checks = json.loads((LANE / 'checks.json').read_bytes()); assert checks['allPassed'], 'the lane of record must pass'
base = json.loads((LANE / 'worktree-base.json').read_bytes())
assert git(W, 'rev-parse', 'HEAD').stdout.decode().strip() == base['productBase'] == git(P, 'rev-parse', 'HEAD').stdout.decode().strip()
changed = sorted(git(W, 'diff', '--name-only').stdout.decode().split() + git(W, 'ls-files', '--others', '--exclude-standard').stdout.decode().split())
assert changed == base['candidatePaths'], (changed, base['candidatePaths'])
rows = []
for c in changed:
    t = U / 'product' / c; t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / c, t)
    b = git(W, 'show', 'HEAD:' + c)
    rows.append(dict(path=c, parent=pin_bytes(c, b.stdout) if b.returncode == 0 else None, candidate=pin(W, c), archived=pin(A, PRE + '/product/' + c)))
stale = [p.relative_to(U / 'product').as_posix() for p in (U / 'product').rglob('*') if p.is_file() and p.relative_to(U / 'product').as_posix() not in changed]
assert not stale, stale
write(U / 'product-map.json', dict(rows=rows))
ev = U / 'evidence' / LANE.name
if ev.exists(): shutil.rmtree(ev)
for p in sorted(LANE.rglob('*')):
    if p.is_file() and p.suffix in ('.log', '.json') and not any(part.endswith('-work') for part in p.relative_to(LANE).parts[:-1]):
        t = ev / p.relative_to(LANE); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
shutil.copyfile(Path(str(LANE) + '.out'), ev / 'lane.out.log')
# Attempts 1 and 2, kept as history: 1 failed warning-denied Clippy (unnecessary_fallible_conversions in build.rs,
# type_complexity on the test provenance log, explicit_counter_loop in a test), all fixed since, and passed every other
# control; 2 passed on 813d559 but was superseded before packaging when main moved to e770404 (C2a-1)
# and 01769e9 (the v223 lock).
for n in (1, 2):
    VOID = Path(f'/tmp/opensip-implementation/d2b3a-checks-r1-void-attempt{n}'); vev = U / 'evidence' / VOID.name
    if vev.exists(): shutil.rmtree(vev)
    for p in sorted(VOID.rglob('*')):
        if p.is_file() and p.suffix in ('.log', '.json') and not any(part.endswith('-work') for part in p.relative_to(VOID).parts[:-1]):
            t = vev / p.relative_to(VOID); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
    shutil.copyfile(Path(str(VOID) + '.out'), vev / 'lane.out.log')
lockj = json.loads((W / 'design-lock.json').read_bytes())
inventory_base = int(lockj['inventorySuccessors'][-1]['candidate']['path'].rsplit('.v', 1)[1].split('.')[0])
FA = 'docs/implementation/m3/native-successors-fa/'
source = dict(productBase=base['productBase'], architectureBase=git(A, 'rev-parse', 'HEAD').stdout.decode().strip(), inventoryBase=inventory_base,
              contractSuccessors=len(lockj['contractSuccessors']), productLock=pin(W, 'design-lock.json'),
              newPaths=[r['path'] for r in rows if r['parent'] is None], publicApiAdded=True, planAmendment=pin(A, A2),
              authorities=[pin(A, p) for p in (
                  'docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md',
                  'docs/implementation/m3/reviews/codex-d2b-plan-r3/review.json',
                  'docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A1.md',
                  'docs/implementation/m3/supervisor-d/PROPOSAL-r5.md',
                  'docs/coop/artifacts/delivery.v2.json',
                  'docs/coop/artifacts/fact-plane.v1.json',
                  'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json',
                  'docs/implementation/m3/supervisor-d/d2b-1-r2-unit.json',
                  'docs/implementation/m3/supervisor-d/d2b-0b-r1-unit.json')],
              priorRounds=[])
write(U / 'source.json', source)
files = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts] + [pin(A, A2)], key=lambda r: r['path'])
write(A / SUBJECT, dict(schemaVersion=1, unit='D2B-3a-r1', productBase=source['productBase'], architectureBase=source['architectureBase'], files=files))
print(len(changed), 'product files;', len(files), 'subject files;', pin(A, SUBJECT))
