"""C1a4-blind post-run gate identity (Codex C1A4B-R2-NBO-1): independent of the run's preflight, after the pinned post-run
checker. From the completed run record and the gate's product map alone, it checks that the run worktree's HEAD and
main's HEAD are the run record's productBase; that HEAD is the frozen base plus exactly one commit; and that this
commit changes exactly the gate's product-map paths, each to its candidate bytes. It writes gate-identity.json into the
post-run checks directory. Git and hashing only; it reads no store."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1a4b'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
RUN = Path('/tmp/opensip-implementation/c1a4b-run/run.json'); OUT = Path(sys.argv[1])
GATE = A / 'docs/implementation/m3/snapshot-plan-c/c1a4-blind-r2/product-map.json'
BASE = 'b7538549b727e13013f36d3b7c2e2917e767f3f2'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
run = json.loads(RUN.read_bytes()); rows = json.loads(GATE.read_bytes())['rows']
head = git(P, 'rev-parse', 'HEAD')
checks = dict(
    runRecordProductBase=run['productBase'],
    mainHeadIsRunBase=head == run['productBase'],
    worktreeHeadIsRunBase=git(W, 'rev-parse', 'HEAD') == run['productBase'],
    worktreeDetached=subprocess.run(['/usr/bin/git', 'symbolic-ref', '-q', 'HEAD'], cwd=W, env=E, capture_output=True).returncode != 0,
    parentIsFrozenBase=git(P, 'rev-parse', 'HEAD^') == BASE,
    oneCommitAfterBase=git(P, 'rev-list', '--count', BASE + '..HEAD') == '1',
    gatePathsExact=sorted(git(P, 'diff', '--name-only', BASE, 'HEAD').splitlines()) == sorted(r['path'] for r in rows),
    gateBytesExact=all(hashlib.sha256(subprocess.check_output(['/usr/bin/git', 'show', 'HEAD:' + r['path']], cwd=P, env=E)).hexdigest() == r['candidate']['sha256'] for r in rows),
    gateProductMap=dict(path=str(GATE.relative_to(A)), sha256=hashlib.sha256(GATE.read_bytes()).hexdigest()))
checks['passed'] = all(v for k, v in checks.items() if isinstance(v, bool))
(OUT / 'gate-identity.json').write_text(json.dumps(checks, indent=2) + '\n')
print(json.dumps(checks))
sys.exit(0 if checks['passed'] else 1)
