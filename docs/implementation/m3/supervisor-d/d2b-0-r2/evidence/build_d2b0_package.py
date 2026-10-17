"""Build the D2b-0 r2 architecture package in place (round 2: the same product candidate, lane attempt 3 and the
post-rebase check, with LD-D2B0-A revised to a deferral, D2B0-R1-RF-1): exact product copies with their parent and candidate pins
(product-map.json), the preparation record, the lane evidence, the source record, the contract successor record
(LD-D2B0-6: three accepted parents, every other package file a candidate), and the subject manifest (the record and its
candidates exactly, as verify_design's contract_successor requires). The admission registry's architecture copy stays
at d2b-0-r1/admission-registry.json, which the unchanged product admission source map selects, so it is a candidate here. Usage: build_d2b0_package.py <lane dir>."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = A.parent / 'opensip-d2b0'; P = A.parent / 'opensip'
LANE = Path(sys.argv[1]); PREP = Path('/tmp/opensip-implementation/d2b0-materialization-r1')
PRE = 'docs/implementation/m3/supervisor-d/d2b-0-r2'; U = A / PRE; SUBJECT = 'docs/implementation/m3/supervisor-d/d2b-0-r2-subject.json'
COPY = 'docs/implementation/m3/supervisor-d/d2b-0-r1/admission-registry.json'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def git(root, *a): return subprocess.run(['/usr/bin/git', *a], cwd=root, env=E, capture_output=True, check=False)
def pin_bytes(path, b): return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def pin(root, path): return pin_bytes(path, (root / path).read_bytes())
def write(p, j): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(j, indent=2) + '\n')

assert json.loads((LANE / 'checks.json').read_bytes())['allPassed'], 'the lane of record must pass'
changed = sorted(git(W, 'diff', '--name-only').stdout.decode().split() + git(W, 'ls-files', '--others', '--exclude-standard').stdout.decode().split())
rows = []
for c in changed:
    t = U / 'product' / c; t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / c, t)
    base = git(W, 'show', 'HEAD:' + c)
    rows.append(dict(path=c, parent=pin_bytes(c, base.stdout) if base.returncode == 0 else None, candidate=pin(W, c), archived=pin(A, PRE + '/product/' + c)))
stale = [p.relative_to(U / 'product').as_posix() for p in (U / 'product').rglob('*') if p.is_file() and p.relative_to(U / 'product').as_posix() not in changed]
assert not stale, stale
write(U / 'product-map.json', dict(rows=rows))
shutil.copyfile(PREP / 'preparation.json', U / 'evidence/preparation.json')
ev = U / 'evidence' / LANE.name
if ev.exists(): shutil.rmtree(ev)
for p in sorted(LANE.rglob('*')):
    if p.is_file() and p.suffix in ('.log', '.json') and not any(part.endswith('-work') for part in p.relative_to(LANE).parts[:-1]):
        t = ev / p.relative_to(LANE); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
# Lane attempts 1 and 2 (void: killed, before LD-D2B0-7 and before the admission_tests count), kept as history.
for n in (1, 2):
    VOID = Path(f'/tmp/opensip-implementation/d2b0-checks-r1-void-attempt{n}'); vev = U / 'evidence' / VOID.name
    if vev.exists(): shutil.rmtree(vev)
    for p in sorted(VOID.rglob('*')):
        if p.is_file() and p.suffix in ('.log', '.json'):
            t = vev / p.relative_to(VOID); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
    shutil.copyfile(Path(str(VOID) + '.out'), vev / 'lane.out.log')
shutil.copyfile(Path(str(LANE) + '.out'), ev / 'lane.out.log')
# The post-rebase focused check on the package base (LD-D2B0-8).
PR = Path('/tmp/opensip-implementation/d2b0-postrebase-check'); prv = U / 'evidence' / PR.name
pr = json.loads((PR / 'postrebase.json').read_bytes()); assert pr['allEqual'] and pr['packageBase'] == git(W, 'rev-parse', 'HEAD').stdout.decode().strip()
if prv.exists(): shutil.rmtree(prv)
shutil.copytree(PR, prv)
lockj = json.loads((W / 'design-lock.json').read_bytes())
inventory_base = int(lockj['inventorySuccessors'][-1]['candidate']['path'].rsplit('.v', 1)[1].split('.')[0])
source = dict(productBase=git(W, 'rev-parse', 'HEAD').stdout.decode().strip(), architectureBase=git(A, 'rev-parse', 'HEAD').stdout.decode().strip(),
              inventoryBase=inventory_base, contractSuccessors=len(lockj['contractSuccessors']), productLock=pin(W, 'design-lock.json'),
              laneBase=json.loads((LANE / 'worktree-base.json').read_bytes())['productBase'], postRebaseCheck=PRE + '/evidence/d2b0-postrebase-check/postrebase.json',
              newPaths=[r['path'] for r in rows if r['parent'] is None], generatorInputsChanged=False, amendment='LD-D2B0-A',
              authorities=[pin(A, p) for p in (
                  'docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md',
                  'docs/implementation/m3/reviews/codex-d2b-plan-r3/review.json',
                  'docs/implementation/m3/native-successors-fa/fa-2/successor.json',
                  'docs/implementation/m3/native-successors-fa/fa-2/materialization-map.json',
                  'docs/implementation/m3/native-successors-fa/rust3-lim/successor.json',
                  'docs/implementation/m3/native-successors-fa/rust3-lim/materialization-map.json',
                  'docs/implementation/m3/native-publication/rust3-identity-materialization-r1/successor.json')],
              priorRounds=[dict(round=1, subjectManifest=pin(A, 'docs/implementation/m3/supervisor-d/d2b-0-r1-subject.json'),
                                review=pin(A, 'docs/implementation/m3/reviews/codex-d2b-0-r1/review.json'),
                                reviewText=pin(A, 'docs/implementation/m3/reviews/codex-d2b-0-r1/REVIEW.md'),
                                verdict='REQUIRED-FINDINGS', findings=['D2B0-R1-RF-1'], productCodeAssessment='ACCEPT-UNIT')])
write(U / 'source.json', source)
# The successor record (LD-D2B0-6). Every parent must be an accepted input of the current lock.
accepted = {}
for r in lockj['inputs']: accepted[r['path']] = r
for binding in lockj['contractSuccessors']:
    accepted[binding['record']['path']] = binding['record']
    for c in json.loads((A / binding['record']['path']).read_bytes())['candidates']: accepted[c['path']] = c
old_copy = json.loads((P / 'schemas/admission-source-map.json').read_bytes())['registryArchitectureSource']
parents = [old_copy, pin(A, 'docs/implementation/m3/native-successors-fa/fa-2/successor.json'), pin(A, 'docs/implementation/m3/native-successors-fa/rust3-lim/successor.json')]
for row in parents: assert accepted.get(row['path']) == row and pin(A, row['path']) == row, row['path']
record = U / 'successor.json'
if record.exists(): record.unlink()
assert json.loads((W / 'schemas/admission-source-map.json').read_bytes())['registryArchitectureSource'] == pin(A, COPY)
candidates = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts] + [pin(A, COPY)], key=lambda r: r['path'])
write(record, dict(schemaVersion=1, standing='PROPOSED D2b-0 admission-only materialization of the accepted FA-2 and RUST3-LIM schema sources, '
                   'with the D2b plan r3 amendment LD-D2B0-A; no generator input, generated carrier or consumer admission',
                   parents=sorted(parents, key=lambda r: r['path']), passageOverrides=[], candidates=candidates))
files = sorted(candidates + [pin(A, PRE + '/successor.json')], key=lambda r: r['path'])
write(A / SUBJECT, dict(schemaVersion=1, unit='D2B-0-r2', productBase=source['productBase'], architectureBase=source['architectureBase'], files=files))
print(len(changed), 'product files;', len(files), 'subject files;', pin(A, SUBJECT))
