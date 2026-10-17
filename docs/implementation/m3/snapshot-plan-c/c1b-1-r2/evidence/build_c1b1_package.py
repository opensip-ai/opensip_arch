"""Build the C1b-1 r2 architecture package in place (adapted from C1c-0 r2's build_c1c0_package.py): exact product
copies with their parent and candidate pins (product-map.json), the preparation record, the source record, the lane
evidence (the preparation record is the lane's own), and the subject manifest. Usage: build_c1b1_package.py <lane dir>."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = A.parent / 'opensip-c1b1'; P = A.parent / 'opensip'
LANE = Path(sys.argv[1]); PREP = LANE / 'preparation.json'
PRE = 'docs/implementation/m3/snapshot-plan-c/c1b-1-r2'; U = A / PRE
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)


def git(root, *a): return subprocess.run(['/usr/bin/git', *a], cwd=root, env=E, capture_output=True, check=False)
def pin_bytes(path, b): return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def pin(root, path): return pin_bytes(path, (root / path).read_bytes())


checks = json.loads((LANE / 'checks.json').read_bytes())
assert checks['allPassed'], 'the lane of record must pass'
prep = json.loads(PREP.read_bytes()); assert prep['passed']
head, main = git(W, 'rev-parse', 'HEAD').stdout.decode().strip(), git(P, 'rev-parse', 'HEAD').stdout.decode().strip()
wb = json.loads((LANE / 'worktree-base.json').read_bytes())
assert head == checks['productBase'] == wb['productBase'] == prep['productBase'], 'the package is of the lane\'s own base'
changed = sorted(git(W, 'diff', '--name-only').stdout.decode().split() + git(W, 'ls-files', '--others', '--exclude-standard').stdout.decode().split())
assert changed == prep['changed'], (changed, prep['changed'])
for row in prep['candidates']: assert pin(W, row['path']) == row, row['path']
rows = []
for c in changed:
    t = U / 'product' / c; t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / c, t)
    base = git(W, 'show', 'HEAD:' + c)
    rows.append(dict(path=c, parent=pin_bytes(c, base.stdout) if base.returncode == 0 else None, candidate=pin(W, c), archived=pin(A, PRE + '/product/' + c)))
stale = [p.relative_to(U / 'product').as_posix() for p in (U / 'product').rglob('*') if p.is_file() and p.relative_to(U / 'product').as_posix() not in changed]
assert not stale, stale
(U / 'product-map.json').write_text(json.dumps(dict(rows=rows), indent=2) + '\n')
ev = U / 'evidence' / LANE.name
if ev.exists(): shutil.rmtree(ev)
for p in sorted(LANE.rglob('*')):
    if p.is_file() and p.suffix in ('.log', '.json') and not any(part.endswith('-work') for part in p.relative_to(LANE).parts[:-1]):
        t = ev / p.relative_to(LANE); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
out = Path(str(LANE) + '.out')
if out.exists(): (ev / 'lane.out.log').write_text(''.join(l for l in out.read_text().splitlines(True) if l != 'waiting for lane\n'))
# Earlier attempts, kept as history (each <lane dir>-void-attemptN with its .out): each stopped before any check.
for VOID in sorted(LANE.parent.glob(LANE.name + '-void-attempt*')):
    if not VOID.is_dir(): continue
    vev = U / 'evidence' / VOID.name
    if vev.exists(): shutil.rmtree(vev)
    vev.mkdir(parents=True)
    for q in sorted(VOID.rglob('*')):
        if q.is_file() and q.suffix in ('.log', '.json'):
            t2 = vev / q.relative_to(VOID); t2.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(q, t2)
    if Path(str(VOID) + '.out').exists():
        (vev / 'lane.out.log').write_text(''.join(l for l in Path(str(VOID) + '.out').read_text().splitlines(True) if l != 'waiting for lane\n'))
lockj = json.loads((W / 'design-lock.json').read_bytes())
inventory_base = int(lockj['inventorySuccessors'][-1]['candidate']['path'].rsplit('.v', 1)[1].split('.')[0])
source = dict(productBase=head, laneBase=checks['productBase'], architectureBase=git(A, 'rev-parse', 'HEAD').stdout.decode().strip(), inventoryBase=inventory_base,
              contractSuccessors=len(lockj['contractSuccessors']), productLock=pin(W, 'design-lock.json'), publicApiAdded=True,
              newPaths=[r['path'] for r in rows if r['parent'] is None],
              authorities=[pin(A, p) for p in (
                  'docs/implementation/m3/snapshot-plan-c/PROPOSAL.md',
                  'docs/implementation/m3/snapshot-plan-c/c1b/PLAN-r6.md',
                  'docs/implementation/m3/snapshot-plan-c/c1b-plan-r6-subject.json',
                  'docs/implementation/m3/reviews/codex-c1b-plan-r6/review.json',
                  'docs/implementation/m3/snapshot-plan-c/c1b/r6-evidence/vcs_term_r6.output.json',
                  'docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md',
                  'docs/implementation/m3/snapshot-plan-c/c1a-r9/evidence/option3_r2.output.json',
                  'docs/implementation/m3/config-discovery-b/b-s2/README.md',
                  'docs/implementation/m3/snapshot-plan-c/vcs-1-r1/CONTRACT.md',
                  # The open C1b batch: its accepted baseline and the bindings recorded so far.
                  'docs/implementation/m3/snapshot-plan-c/c1b-0-r2-unit.json',
                  'docs/implementation/m3/snapshot-plan-c/c1b-0-r2/evidence/census-regeneration.json',
                  'docs/implementation/m3/snapshot-plan-c/c1c-0-r2-unit.json',
                  'docs/implementation/m3/snapshot-plan-c/c1c-0-r2/evidence/c1c0-checks-r2/receipt-specific.json',
                  'docs/implementation/m3/snapshot-plan-c/c1c-0-r2/evidence/c1c0-checks-r2/retention-cap-evidence.json')],
              priorRounds=[dict(subject=pin(A, 'docs/implementation/m3/snapshot-plan-c/c1b-1-r1-subject.json'),
                                review={k: pin_bytes(k, Path('/tmp/opensip-implementation/reviews/codex-c1b-1-r1/' + k).read_bytes()) for k in ('REQUEST.md', 'REVIEW.md', 'review.json')})])
(U / 'source.json').write_text(json.dumps(source, indent=2) + '\n')
files = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts], key=lambda r: r['path'])
(A / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='C1B-1-r2', productBase=head, architectureBase=source['architectureBase'], files=files), indent=2) + '\n')
print(len(changed), 'product files;', len(files), 'subject files;', pin(A, PRE + '-subject.json'))
