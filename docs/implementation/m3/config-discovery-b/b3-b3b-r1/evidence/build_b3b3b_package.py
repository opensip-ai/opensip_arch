"""Build the B3-b3b r1 post-run package in place: exact product copies of the run worktree's changes with their parent and
candidate pins (product-map.json), the run record (run.json, the blind stdout and stderr, the ordinary logs, the driver's
output), the post-run verification logs, and the subject manifest."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = Path('/Users/sb/code/opensip-ai/opensip-b3b3b')
RUN = Path('/tmp/opensip-implementation/b3b3b-run'); POST = Path('/tmp/opensip-implementation/b3b3b-post')
PRE = 'docs/implementation/m3/config-discovery-b/b3-b3b-r1'; U = A / PRE
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)


def git(*a): return subprocess.run(['/usr/bin/git', *a], cwd=W, env=E, capture_output=True, check=False)
def pin_bytes(path, b): return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def pin(root, path): return pin_bytes(path, (root / path).read_bytes())


changed = sorted(git('diff', '--name-only').stdout.decode().split() + git('ls-files', '--others', '--exclude-standard').stdout.decode().split())
assert changed == ['crates/security/src/custody/discovery_census.json', 'crates/security/src/custody/discovery_census_held_out.json'], changed
rows = []
for c in changed:
    t = U / 'product' / c; t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / c, t)
    base = git('show', 'HEAD:' + c)
    rows.append(dict(path=c, parent=pin_bytes(c, base.stdout), candidate=pin(W, c), archived=pin(A, PRE + '/product/' + c)))
(U / 'product-map.json').write_text(json.dumps(dict(rows=rows), indent=2) + '\n')
for src, name in ((RUN, 'run'), (POST, 'post-run-checks')):
    ev = U / 'evidence' / name
    if ev.exists(): shutil.rmtree(ev)
    for p in sorted(src.rglob('*')):
        if p.is_file():
            t = ev / p.relative_to(src); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
shutil.copyfile('/tmp/opensip-implementation/b3b3b-run.out', U / 'evidence/run/driver-output.log')
files = sorted([pin(A, p.relative_to(A).as_posix()) for p in sorted(U.rglob('*')) if p.is_file() and '__pycache__' not in p.parts], key=lambda r: r['path'])
gate = [pin(A, p) for p in ('docs/implementation/m3/config-discovery-b/b3-b3a2-r1-subject.json', 'docs/implementation/m3/config-discovery-b/b3-b3a2-r1-unit.json',
                            'docs/implementation/m3/config-discovery-b/b3-b3a2-r1/RUN-PLAN.md', 'docs/implementation/m3/config-discovery-b/b3-b3a2-r1/evidence/run_b3b3b_blind.py',
                            'docs/implementation/m3/reviews/codex-b3b3a2-r1/review.json')]
(A / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='B3-B3B-r1', productBase=git('rev-parse', 'HEAD').stdout.decode().strip(), gate=gate, files=files), indent=2) + '\n')
print(len(changed), 'product files;', len(files), 'subject files')
