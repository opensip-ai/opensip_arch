"""Build the S10-TSC architecture package in place: exact product copies, the evidence records, the successor record
and the subject manifest. Run after the candidate checks and before (and again after) the scratch binding."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = Path('/Users/sb/code/opensip-ai/opensip-s10tsc')
D = Path('/tmp/opensip-implementation/s10-tsc')
PRE = 'docs/implementation/m3/config-discovery-b/s10-tsc'; U = A / PRE
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
PARENTS = [
    'docs/implementation/m2/continuation-diagnostics-x4tc-r1/reference/public-detail-registry.json',
    'docs/implementation/m3/snapshot-plan-c/native-metadata-missing-r1/completion/public-detail-registry.v1.json',
    'docs/implementation/m3/snapshot-plan-c/native-metadata-missing-r1/completion/design/common.schema.json',
    'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py',
    'docs/implementation/m3/native-g/rustflags-long-lint-r1/reference/native_evidence_model.v2.py',
    'docs/implementation/m3/config-discovery-b/b-s10/admission-registry.json',
    *[f'docs/implementation/m3/native-publication/native-common-materialization-r1/sources/common-v{v}.schema.json' for v in (1, 3, 4)],
]


def git(*a): return subprocess.check_output(['/usr/bin/git', *a], cwd=W, env=E).decode()
def pin(root, path): b = (root / path).read_bytes(); return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


changed = sorted(git('diff', '--name-only').split() + git('ls-files', '--others', '--exclude-standard').split())
assert not [c for c in changed if c.startswith(('tools/contracts/node_modules/', 'tools/contracts/python-packages/'))]
for c in changed:
    t = U / 'product' / c; t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / c, t)
stale = [p.relative_to(U / 'product').as_posix() for p in (U / 'product').rglob('*') if p.is_file()
         and p.relative_to(U / 'product').as_posix() not in changed]
assert not stale, stale
ev = U / 'evidence'
for n in ['preparation.json', 'generation-summary.json']:
    shutil.copyfile(D / n, ev / n)
if (D / 'checks-r1').exists():
    shutil.copyfile(D / 'checks-r1.log', ev / 'checks-r1.log')
    for p in sorted((D / 'checks-r1').rglob('*')):
        if p.is_file() and p.suffix in ('.log', '.json'):
            t = ev / 'checks-r1' / p.relative_to(D / 'checks-r1'); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
cands = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*'))
                if p.is_file() and p.name != 'successor.json' and '__pycache__' not in p.parts], key=lambda r: r['path'])
record = dict(schemaVersion=1, standing=(
    'PROPOSED S10-TSC (M3-B r8 item 14a, successor S10): the public detail registry as the union of its two accepted lines '
    'plus native.typescript-config-unresolved and its four context-free internal aliases; the closed enum design mirror; '
    'complete successor copies of both native-model files (SD-7 line 1159 applied) with one D9_MAP row (request-rejected, '
    'exit 2, CONFIG.INVALID) and one PUBLIC_ROUTE_REMEDIES entry keyed by the public detail; the product vocabulary '
    '(common v1/v3/v4, regenerated contracts), the re-pinned admission registry, and the remedy product carrier '
    '(crates/host/src/outcomes.rs). SELECTION: this unit\'s registry, design mirror and two model copies become the '
    'selected copies; every later edit of PUBLIC_ROUTE_REMEDIES, D9_MAP or the registry succeeds these, not their parents. '
    'No passage override; no TypeScript resolution, D9 class/code/exit change or qualification'),
    parents=[pin(A, p) for p in sorted(PARENTS)], passageOverrides=[], candidates=cands)
(U / 'successor.json').write_text(json.dumps(record, indent=2) + '\n')
subject = sorted(cands + [pin(A, PRE + '/successor.json')], key=lambda r: r['path'])
(A / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='S10-TSC', files=subject), indent=2) + '\n')
print(len(changed), 'product files;', len(cands), 'candidates')
