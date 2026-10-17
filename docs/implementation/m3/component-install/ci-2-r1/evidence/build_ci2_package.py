"""Build the CI-2+CI-3 r1 architecture package in place: exact product copies with their parent and candidate pins
(product-map.json), the source record, the lane evidence, and the subject manifest. (Adapted from build_c2a1_package.py.)
Usage: build_ci2_package.py LANE_DIR"""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = Path('/Users/sb/code/opensip-ai/opensip-ci2')
LANE = Path(sys.argv[1])
PRE = 'docs/implementation/m3/component-install/ci-2-r1'; U = A / PRE
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)


def git(*a): return subprocess.run(['/usr/bin/git', *a], cwd=W, env=E, capture_output=True, check=False)
def pin_bytes(path, b): return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def pin(root, path): return pin_bytes(path, (root / path).read_bytes())


checks = json.loads((LANE / 'checks.json').read_bytes())
assert checks['allPassed'] and checks['productBase'] == git('rev-parse', 'HEAD').stdout.decode().strip()
changed = sorted(git('diff', '--name-only').stdout.decode().split() + git('ls-files', '--others', '--exclude-standard').stdout.decode().split())
assert changed == json.loads((LANE / 'edited.json').read_bytes())['paths'], 'the candidate changed after its lane'
rows = []
for c in changed:
    t = U / 'product' / c; t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / c, t)
    base = git('show', 'HEAD:' + c)
    rows.append(dict(path=c, parent=pin_bytes(c, base.stdout) if base.returncode == 0 else None, candidate=pin(W, c), archived=pin(A, PRE + '/product/' + c)))
stale = [p.relative_to(U / 'product').as_posix() for p in (U / 'product').rglob('*') if p.is_file() and p.relative_to(U / 'product').as_posix() not in changed]
assert not stale, stale
(U / 'product-map.json').write_text(json.dumps(dict(rows=rows), indent=2) + '\n')
ev = U / 'evidence' / LANE.name
if ev.exists(): shutil.rmtree(ev)
for p in sorted(LANE.rglob('*')):
    if p.is_file() and p.suffix in ('.log', '.json', '.py') and not any(part.endswith('-work') for part in p.relative_to(LANE).parts[:-1]):
        t = ev / p.relative_to(LANE); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
lock = pin(W, 'design-lock.json')
lockj = json.loads((W / 'design-lock.json').read_bytes())
# The inventory number is derived from the lock: the last bound inventory successor.
inventory_base = int(lockj['inventorySuccessors'][-1]['candidate']['path'].rsplit('.v', 1)[1].split('.')[0])
source = dict(productBase=git('rev-parse', 'HEAD').stdout.decode().strip(), architectureBase=subprocess.run(['/usr/bin/git', 'rev-parse', 'HEAD'], cwd=A, env=E, capture_output=True).stdout.decode().strip(), inventoryBase=inventory_base,
              contractSuccessors=len(lockj['contractSuccessors']), productLock=lock, publicApiAdded=True, productionCallerAdded=False, newPaths=[r['path'] for r in rows if r['parent'] is None],
              authorities=[pin(A, p) for p in (
                  'docs/implementation/m3/component-install/PROPOSAL-r5.md',
                  'docs/implementation/m3/component-install/PROPOSAL.md',
                  'docs/implementation/m3/component-install/PLAN-r3.md',
                  'docs/implementation/m3/reviews/codex-component-install-r5/review.json',
                  'docs/implementation/m3/reviews/codex-component-install-plan-r3/review.json',
                  'docs/implementation/m3/reviews/codex-ci-1-r2/review.json',
                  'docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json')],
              priorRounds=[])
(U / 'source.json').write_text(json.dumps(source, indent=2) + '\n')
files = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts], key=lambda r: r['path'])
(A / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='CI-2-r1', files=files), indent=2) + '\n')
print(len(changed), 'product files;', len(files), 'subject files; inventory base', inventory_base)
