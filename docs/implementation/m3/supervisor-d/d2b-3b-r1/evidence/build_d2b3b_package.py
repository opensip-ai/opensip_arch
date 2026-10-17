"""Build the D2b-3b r1 architecture package in place: exact product copies with their parent and candidate pins
(product-map.json), the source record, the lane evidence, and the subject manifest. Usage: build_d2b3b_package.py
<lane dir>. (Adapted from build_d2b3a_package.py.)"""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = A.parent / 'opensip-d2b3b'; P = A.parent / 'opensip'
LANE = Path(sys.argv[1])
PRE = 'docs/implementation/m3/supervisor-d/d2b-3b-r1'; U = A / PRE; SUBJECT = 'docs/implementation/m3/supervisor-d/d2b-3b-r1-subject.json'
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
def archive(lane, into):
    if into.exists(): shutil.rmtree(into)
    for p in sorted(lane.rglob('*')):
        if p.is_file() and p.suffix in ('.log', '.json') and not any(part.endswith('-work') for part in p.relative_to(lane).parts[:-1]):
            t = into / p.relative_to(lane); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
    shutil.copyfile(Path(str(lane) + '.out'), into / 'lane.out.log')
archive(LANE, U / 'evidence' / LANE.name)
# Void attempts, kept as history (none yet).
VOID = []
for n in VOID:
    v = Path(f'/tmp/opensip-implementation/d2b3b-checks-r1-void-attempt{n}'); archive(v, U / 'evidence' / v.name)
lockj = json.loads((W / 'design-lock.json').read_bytes())
inventory_base = int(lockj['inventorySuccessors'][-1]['candidate']['path'].rsplit('.v', 1)[1].split('.')[0])
source = dict(productBase=base['productBase'], architectureBase=git(A, 'rev-parse', 'HEAD').stdout.decode().strip(), inventoryBase=inventory_base,
              contractSuccessors=len(lockj['contractSuccessors']), productLock=pin(W, 'design-lock.json'),
              newPaths=[r['path'] for r in rows if r['parent'] is None], publicApiAdded=True,
              authorities=[pin(A, p) for p in (
                  'docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md',
                  'docs/implementation/m3/reviews/codex-d2b-plan-r3/review.json',
                  'docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A1.md',
                  'docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A2.md',
                  'docs/implementation/m3/supervisor-d/PROPOSAL-r5.md',
                  'docs/coop/artifacts/delivery.v2.json',
                  'docs/implementation/m1/trials/native-wire-owner-07/subject/tools/sender_ref.py',
                  'docs/implementation/m1/trials/native-wire-owner-07/subject/tools/representability.py',
                  'docs/implementation/m3/reviews/codex-d2b-3a-r1/review.json',
                  'docs/implementation/m3/supervisor-d/d2b-3a-r1-unit.json',
                  'docs/implementation/m3/supervisor-d/d3a-1-r3-unit.json',
                  'docs/implementation/m3/supervisor-d/d3a-2-r1-unit.json')],
              priorRounds=[])
write(U / 'source.json', source)
files = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts], key=lambda r: r['path'])
write(A / SUBJECT, dict(schemaVersion=1, unit='D2B-3b-r1', productBase=source['productBase'], architectureBase=source['architectureBase'], files=files))
print(len(changed), 'product files;', len(files), 'subject files;', pin(A, SUBJECT))
