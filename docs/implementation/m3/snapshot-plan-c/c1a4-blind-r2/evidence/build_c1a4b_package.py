"""Build the C1a4-blind r2 gate package in place: exact product copies with their parent and candidate pins
(product-map.json), the source record (with the run's reviewed bytes), the lane evidence, and the subject manifest."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = Path('/Users/sb/code/opensip-ai/opensip-c1a4')
LANE = Path(sys.argv[1])
PRE = 'docs/implementation/m3/snapshot-plan-c/c1a4-blind-r2'; U = A / PRE
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)


def git(*a): return subprocess.run(['/usr/bin/git', *a], cwd=W, env=E, capture_output=True, check=False)
def pin_bytes(path, b): return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def pin(root, path): return pin_bytes(path, (root / path).read_bytes())


changed = sorted(git('diff', '--name-only').stdout.decode().split() + git('ls-files', '--others', '--exclude-standard').stdout.decode().split())
assert changed == ['crates/security/src/snapshot_ledger_census.json', 'crates/security/src/snapshot_walk_tests.rs',
                   'tools/security/snapshot_ledger_census.py', 'tools/tests/test_snapshot_ledger_census_blind.py'], changed
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
inventory_base = int(lockj['inventorySuccessors'][-1]['candidate']['path'].rsplit('.v', 1)[1].split('.')[0])
run_tools = ('tools/security/snapshot_ledger_census.py', 'tools/security/discovery_census.py', 'tools/security/discovery_member_model.py',
             'tools/security/snapshot_ledger_model.py', 'tools/security/discovery_workspace_ledger.py')
source = dict(productBase=git('rev-parse', 'HEAD').stdout.decode().strip(), architectureBase=subprocess.run(['/usr/bin/git', 'rev-parse', 'HEAD'], cwd=A, env=E, capture_output=True).stdout.decode().strip(), inventoryBase=inventory_base,
              contractSuccessors=len(lockj['contractSuccessors']), productLock=lock, publicApiAdded=False, newPaths=[r['path'] for r in rows if r['parent'] is None],
              runReviewedBytes={p: pin(W, p)['sha256'] for p in run_tools},
              authorities=[pin(A, p) for p in (
                  'docs/implementation/m3/owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md',
                  'docs/implementation/m3/config-discovery-b/b2-b4/PLAN-r6.md',
                  'docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r6.md',
                  'docs/implementation/m3/reviews/codex-c1a-plan-r6/review.json',
                  'docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md',
                  'docs/implementation/m3/reviews/codex-m3c-r9-r2/review.json',
                  'docs/implementation/m3/snapshot-plan-c/c1a4-r1-unit.json',
                  'docs/implementation/m3/reviews/codex-c1a4-r1/review.json',
                  'docs/implementation/m3/config-discovery-b/b3-b3a2-r1-unit.json',
                  'docs/implementation/m3/reviews/codex-b3b3a2-r1/review.json',
                  'docs/implementation/m3/config-discovery-b/b3-b3b-r1-unit.json',
                  'docs/implementation/m3/reviews/codex-b3b3b-r1/review.json')])
# Round 1 (Codex codex-c1a4b-r1, REQUIRED-FINDINGS, runAuthorized false): its frozen subject and the review.
source['priorRounds'] = [pin(A, p) for p in (
    'docs/implementation/m3/snapshot-plan-c/c1a4-blind-r1-subject.json',
    'docs/implementation/m3/reviews/codex-c1a4b-r1/REVIEW.md',
    'docs/implementation/m3/reviews/codex-c1a4b-r1/review.json')]
source['postRunChecker'] = pin(A, PRE + '/evidence/run_c1a4b_post_checks.py')
(U / 'source.json').write_text(json.dumps(source, indent=2) + '\n')
files = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts], key=lambda r: r['path'])
(A / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='C1A4-BLIND-r2', files=files), indent=2) + '\n')
print(len(changed), 'product files;', len(files), 'subject files')
