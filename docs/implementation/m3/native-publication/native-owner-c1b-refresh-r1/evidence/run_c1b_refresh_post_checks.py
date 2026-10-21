"""The C1b batch refresh's post-run checks, in the run worktree after the blind run (adapted from C1a4-blind's
run_c1a4b_post_checks.py; pinned in the gate package, and the run script refuses unless its bytes match): the census
tests over the composed records (the snapshot census margin test, the discovery census tests and the VCS model's
charge test), the companion's and discovery's blind controls, and verify_design. It refuses unless the run worktree is
the run's: detached at product main, main still descending from the freeze with every bound input frozen, and its
changes exactly the run's four files. One lane hold, nice 10, private TMPDIR. Reads no held-out store.

Usage: /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B <this committed path> /tmp/opensip-implementation/c1b-refresh-post"""
from pathlib import Path
import os, subprocess, tempfile, time, json, sys, hashlib
W = Path('/Users/sb/code/opensip-ai/opensip-native-owner-c1b-refresh'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = Path(__file__).resolve().parent
frozen = json.loads((EV / 'frozen-bindings.json').read_bytes())
RUN_FILES = ['crates/security/src/custody/discovery_census.json', 'crates/security/src/custody/discovery_census_held_out.json',
             'crates/security/src/snapshot_ledger_census.json', 'crates/security/src/snapshot_ledger_census_held_out.json']
run_record=json.loads(Path(sys.argv[2]).read_bytes())
assert run_record['eligibleForPostRunReview'] and run_record['freezeBase']==frozen['freezeBase']
B = Path(sys.argv[1]); B.mkdir(parents=True)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-native-owner-c1b-refresh-post-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert subprocess.run(['/usr/bin/git', 'symbolic-ref', '-q', 'HEAD'], cwd=W, env=E, capture_output=True).returncode != 0, 'the run worktree is not detached'
    assert git(W, 'rev-parse', 'HEAD') == git(P, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    assert subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=P,env=E).decode().strip()==frozen['freezeBase'], 'main moved since exact freeze'
    now = json.loads(subprocess.check_output([PY, '-I', '-B', str(EV / 'freeze_c1b_refresh.py'), '--bindings', str(W), str(A), str(P)], cwd=W, env=E))
    assert now == frozen['frozenBindings'], 'a bound input moved since the freeze'
    for root, rows in ((W, frozen['tools']), (P, frozen['tools']), (A, frozen['architectureInputs'])):
        for row in rows:
            raw=(root/row['path']).read_bytes()
            assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'], row['path']
    # Not stripped: a porcelain line's leading space is part of its status (B3-b3b's run record).
    status = subprocess.check_output(['/usr/bin/git', 'status', '--porcelain', '--untracked-files=all'], cwd=W, env=E).decode()
    changes = sorted(line[3:] for line in status.splitlines())
    assert changes == RUN_FILES, changes
    steps = [('census-tests', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'snapshot_walk::tests::the_snapshot_census', 'custody::discovery_census', 'snapshot_vcs::tests::the_observation_charges_exactly']),
             ('companion-blind-controls', [PY, '-I', '-B', 'tools/tests/test_snapshot_ledger_census_blind.py']),
             ('discovery-blind-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census_blind.py']),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    rows = []
    for name, args in steps:
        with (B / (name + '.log')).open('wb') as log:
            code = subprocess.run(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
        rows.append(dict(name=name, exitCode=code)); print(name, code, flush=True)
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), standing='C1b batch refresh POST-RUN CHECKS'), indent=2) + '\n')
finally:
    if owned: lane.rmdir()
