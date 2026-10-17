"""C1a4-blind post-run checks, in the run worktree after the blind run (as B3-b3b's; r2, Codex C1A4B-R1-RF-1: pinned in
the gate package, and the run script refuses unless its bytes match): the snapshot census margin test and the discovery
census tests over the composed records, the companion's and discovery's blind controls, and verify_design. It refuses
unless the run worktree is the run's: detached at product main, main the frozen base plus the gate commit only, and its
changes exactly the run's four files. One lane hold, nice 10, private TMPDIR. Reads no held-out store.

Usage: /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B <this committed path> /tmp/opensip-implementation/c1a4b-post"""
from pathlib import Path
import os, subprocess, tempfile, time, json, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1a4b'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
BASE = 'b7538549b727e13013f36d3b7c2e2917e767f3f2'  # the gate's freeze
RUN_FILES = ['crates/security/src/custody/discovery_census.json', 'crates/security/src/custody/discovery_census_held_out.json',
             'crates/security/src/snapshot_ledger_census.json', 'crates/security/src/snapshot_ledger_census_held_out.json']
B = Path(sys.argv[1]); B.mkdir(parents=True)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1a4b-post-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # The run's worktree, as the run left it: detached at main, main the freeze plus the gate commit only, and its
    # changes exactly the run's four files.
    assert subprocess.run(['/usr/bin/git', 'symbolic-ref', '-q', 'HEAD'], cwd=W, env=E, capture_output=True).returncode != 0, 'the run worktree is not detached'
    assert git(W, 'rev-parse', 'HEAD') == git(P, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    assert git(P, 'rev-parse', 'HEAD^') == BASE and git(P, 'rev-list', '--count', BASE + '..HEAD') == '1', 'main is not the freeze plus the gate commit'
    # Not stripped: a porcelain line's leading space is part of its status (B3-b3b's run record).
    status = subprocess.check_output(['/usr/bin/git', 'status', '--porcelain', '--untracked-files=all'], cwd=W, env=E).decode()
    changes = sorted(line[3:] for line in status.splitlines())
    assert changes == RUN_FILES, changes
    steps = [('census-tests', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'snapshot_walk::tests::the_snapshot_census', 'custody::discovery_census']),
             ('companion-blind-controls', [PY, '-I', '-B', 'tools/tests/test_snapshot_ledger_census_blind.py']),
             ('discovery-blind-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census_blind.py']),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    rows = []
    for name, args in steps:
        with (B / (name + '.log')).open('wb') as log:
            code = subprocess.run(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
        rows.append(dict(name=name, exitCode=code)); print(name, code, flush=True)
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), standing='C1a4-blind POST-RUN CHECKS'), indent=2) + '\n')
finally:
    if owned: lane.rmdir()
