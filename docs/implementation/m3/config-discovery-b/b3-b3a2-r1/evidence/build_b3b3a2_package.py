"""Build the B3-b3a2 r1 architecture package in place: exact product copies with their parent and candidate pins
(product-map.json), the source record, the lane evidence, and the subject manifest (SCOPE, RUN-PLAN and the B3-b3b run
script included)."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = Path('/Users/sb/code/opensip-ai/opensip-b3b3a2')
LANE = Path(sys.argv[1])
PRE = 'docs/implementation/m3/config-discovery-b/b3-b3a2-r1'; U = A / PRE
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)


def git(*a): return subprocess.run(['/usr/bin/git', *a], cwd=W, env=E, capture_output=True, check=False)
def pin_bytes(path, b): return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def pin(root, path): return pin_bytes(path, (root / path).read_bytes())


changed = sorted(git('diff', '--name-only').stdout.decode().split() + git('ls-files', '--others', '--exclude-standard').stdout.decode().split())
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
source = dict(productBase=git('rev-parse', 'HEAD').stdout.decode().strip(), architectureBase='abbf48fb0992b48178bf3de0aac2c42015e48b4e', inventoryBase=208,
              contractSuccessors=170, productLock=lock, publicApiAdded=False, newPaths=[r['path'] for r in rows if r['parent'] is None],
              runReviewedBytes={r['path']: r['candidate']['sha256'] for r in rows if r['path'] in ('tools/security/discovery_census.py', 'tools/security/discovery_member_model.py')},
              authorities=[pin(A, p) for p in (
                  'docs/implementation/m3/owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md',
                  'docs/implementation/m3/config-discovery-b/b2-b4/PLAN-r6.md',
                  'docs/implementation/m3/reviews/codex-b2b4c1-r2/review.json',
                  'docs/implementation/m3/reviews/codex-b2b4c3-prerun/review.json',
                  'docs/implementation/m3/reviews/codex-b2b4c3-r1/review.json',
                  'docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2.md',
                  'docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A5.md',
                  'docs/implementation/m3/reviews/codex-b3b-plan-a5-r1/review.json',
                  'docs/implementation/m3/config-discovery-b/b3-b3a1-r1/SCOPE.md',
                  'docs/implementation/m3/reviews/codex-b3b3a1-r1/review.json',
                  'docs/implementation/m3/corpus/FETCH-SPEC.md',
                  'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json')])
source['priorRounds'] = []
(U / 'source.json').write_text(json.dumps(source, indent=2) + '\n')
files = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts], key=lambda r: r['path'])
(A / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='B3-B3A2-r1', files=files), indent=2) + '\n')
print(len(changed), 'product files;', len(files), 'subject files')
