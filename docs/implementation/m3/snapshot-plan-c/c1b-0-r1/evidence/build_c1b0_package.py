"""Build the C1b-0 r1 architecture package in place (adapted from D2b-0b's build_d2b0b_package.py): exact product
copies with their parent and candidate pins (product-map.json; the copies of identity-v3 and the generator closure are
the accepted inputs once the unit binds), the preparation record, the lane evidence, the source record, the contract
successor record (its parents: the accepted inputs it re-pins, and B-S2's and VCS-1's records; every other package
file a candidate), and the subject manifest (the record and its candidates exactly). Usage: build_c1b0_package.py <lane dir>."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = A.parent / 'opensip-c1b0'; P = A.parent / 'opensip'
LANE = Path(sys.argv[1]); PREP = Path('/tmp/opensip-implementation/c1b0-materialization-r1')
PRE = 'docs/implementation/m3/snapshot-plan-c/c1b-0-r1'; U = A / PRE; SUBJECT = 'docs/implementation/m3/snapshot-plan-c/c1b-0-r1-subject.json'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def git(root, *a): return subprocess.run(['/usr/bin/git', *a], cwd=root, env=E, capture_output=True, check=False)
def pin_bytes(path, b): return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def pin(root, path): return pin_bytes(path, (root / path).read_bytes())
def write(p, j): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(j, indent=2) + '\n')

assert json.loads((LANE / 'checks.json').read_bytes())['allPassed'], 'the lane of record must pass'
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
shutil.copyfile(PREP / 'preparation.json', U / 'evidence/preparation.json')
shutil.copyfile(PREP / 'generation-summary.json', U / 'evidence/generation-summary.json')
ev = U / 'evidence' / LANE.name
if ev.exists(): shutil.rmtree(ev)
for p in sorted(LANE.rglob('*')):
    if p.is_file() and p.suffix in ('.log', '.json') and not any(part.endswith('-work') or part in ('generation-check', 'generate-contracts-prebind') for part in p.relative_to(LANE).parts[:-1]):
        t = ev / p.relative_to(LANE); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
shutil.copyfile(Path(str(LANE) + '.out'), ev / 'lane.out.log')
# Earlier attempts, if any, kept as history (each as <lane dir>-void-attemptN with its .out).
for VOID in sorted(LANE.parent.glob(LANE.name + '-void-attempt*')):
    if not VOID.is_dir(): continue
    vev = U / 'evidence' / VOID.name
    if vev.exists(): shutil.rmtree(vev)
    for p in sorted(VOID.rglob('*')):
        if p.is_file() and p.suffix in ('.log', '.json') and not any(part.endswith('-work') or part in ('generation-check', 'generate-contracts-prebind') for part in p.relative_to(VOID).parts[:-1]):
            t = vev / p.relative_to(VOID); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
    if Path(str(VOID) + '.out').exists(): shutil.copyfile(Path(str(VOID) + '.out'), vev / 'lane.out.log')
lockj = json.loads((W / 'design-lock.json').read_bytes())
accepted = {}
for r in lockj['inputs']: accepted[r['path']] = r
for binding in lockj['contractSuccessors']:
    accepted[binding['record']['path']] = binding['record']
    for c in json.loads((A / binding['record']['path']).read_bytes())['candidates']: accepted[c['path']] = c
def accepted_pin(product_path):
    raw = (P / product_path).read_bytes(); h = hashlib.sha256(raw).hexdigest()
    hits = [v for v in accepted.values() if v['sha256'] == h and v['bytes'] == len(raw)]; assert hits, product_path; return hits[-1]
generator_parents = [accepted_pin(p) for p in ('tools/contracts/generator-closure.json', 'tools/contracts/options.json', 'schemas/source-map.json',
                                                'schemas/sources/identity-v3.schema.json', 'schemas/admission-registry.json')]
authority = [pin(A, 'docs/implementation/m3/config-discovery-b/b-s2/successor.json'), pin(A, 'docs/implementation/m3/snapshot-plan-c/vcs-1-r1/successor.json')]
parents = sorted({r['path']: r for r in generator_parents + authority}.values(), key=lambda r: r['path'])
for row in parents: assert accepted.get(row['path']) == row and pin(A, row['path']) == row, row['path']
source = dict(productBase=base['productBase'], architectureBase=git(A, 'rev-parse', 'HEAD').stdout.decode().strip(), contractSuccessors=len(lockj['contractSuccessors']),
              productLock=pin(W, 'design-lock.json'), newPaths=[r['path'] for r in rows if r['parent'] is None], generatorInputsChanged=True,
              authorities=[pin(A, p) for p in (
                  'docs/implementation/m3/snapshot-plan-c/PROPOSAL.md',
                  'docs/implementation/m3/snapshot-plan-c/c1b/PLAN-r3.md',
                  'docs/implementation/m3/reviews/codex-c1b-plan-r3/review.json',
                  'docs/implementation/m3/config-discovery-b/b-s2/README.md',
                  'docs/implementation/m3/config-discovery-b/b-s2/successor.json',
                  'docs/implementation/m3/config-discovery-b/b-s2/schemas/identity-schemas.v3.b-s2-additions.json',
                  'docs/implementation/m3/config-discovery-b/b-s2/evidence/check_b_s2.py',
                  'docs/implementation/m3/snapshot-plan-c/vcs-1-r1/CONTRACT.md',
                  'docs/implementation/m3/snapshot-plan-c/vcs-1-r1/successor.json')],
              priorRounds=[])
write(U / 'source.json', source)
record = U / 'successor.json'
if record.exists(): record.unlink()
candidates = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts], key=lambda r: r['path'])
for path in ('tools/contracts/generator-closure.json', 'schemas/sources/identity-v3.schema.json'):
    copy = pin(A, PRE + '/product/' + path); assert {k: copy[k] for k in ('bytes', 'sha256')} == {k: pin(W, path)[k] for k in ('bytes', 'sha256')}, path
write(record, dict(schemaVersion=1, standing='PROPOSED C1b-0 materialization of M3-B successor S4 (B-S2) into the product identity-v3 source: '
                   'vcs-observation as schema 2 or 3, the re-pinned maps, registries and closure, the regenerated carriers and the evaluator member '
                   'join; opens C1b\'s census batch (C1b plan r3 LD-C1B-7); no Git read, sealing or blind refresh', parents=parents, passageOverrides=[], candidates=candidates))
files = sorted(candidates + [pin(A, PRE + '/successor.json')], key=lambda r: r['path'])
write(A / SUBJECT, dict(schemaVersion=1, unit='C1B-0-r1', productBase=source['productBase'], architectureBase=source['architectureBase'], files=files))
print(len(changed), 'product files;', len(files), 'subject files;', pin(A, SUBJECT))
