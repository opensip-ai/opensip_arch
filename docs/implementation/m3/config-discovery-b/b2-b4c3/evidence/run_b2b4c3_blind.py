"""B2-b4c3: the blind held-out receipt refresh after S10-TSC's generator-closure drift (owner decision of 2026-10-16, the
mechanical blind run; Codex B3BPLAN-R1-RF-3 and NBO-1: a reviewed pre-run gate, then the run, then a post-run review). It runs
the unchanged reviewed tool's --held-out-blind exactly once in a detached worktree of product main, after removing the stale
receipt there; the lead sees only its one-line stdout summary, its exit code and the receipt (ids, verdicts and per-mille
margins only). Then the ordinary mode regenerates and checks the census record. One lane hold, nice 10, private TMPDIR.
Nothing here reads a held-out store except the reviewed blind mode itself."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b2b4c3'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'; CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
B = Path(sys.argv[1]); B.mkdir(parents=True)
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'; TOOL = 'tools/security/discovery_census.py'; RECEIPT = 'crates/security/src/custody/discovery_census_held_out.json'; CENSUS = 'crates/security/src/custody/discovery_census.json'
REVIEWED_TOOL = '6ea8a1ab7ecad60220896790df6fb07aa53d2eac7efe7e6120a441b7b75c7dfd'
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b2b4c3-blind-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/usr/bin:/bin', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == '' and git(W, 'status', '--porcelain') == ''
    tool = hashlib.sha256((W / TOOL).read_bytes()).hexdigest(); assert tool == REVIEWED_TOOL == hashlib.sha256((P / TOOL).read_bytes()).hexdigest()
    old_receipt = json.loads((W / RECEIPT).read_bytes()); old_census = (W / CENSUS).read_bytes()
    (W / RECEIPT).unlink()  # the stale receipt; the blind mode writes a fresh one
    args = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]
    blind = subprocess.run([PY, '-I', '-B', TOOL, '--held-out-blind', *args], cwd=W, env=E, capture_output=True, text=True)
    (B / 'blind-stdout.txt').write_text(blind.stdout); (B / 'blind-stderr.txt').write_text(blind.stderr)
    row = dict(blindExitCode=blind.returncode, blindStdout=blind.stdout, blindStderrEmpty=blind.stderr == '', receiptWritten=(W / RECEIPT).is_file(), toolSha256=tool)
    print('blind', blind.returncode, blind.stdout.strip(), 'stderr-empty' if blind.stderr == '' else 'STDERR-NONEMPTY', flush=True)
    if blind.returncode == 0 and (W / RECEIPT).is_file():
        for mode in ('--write', '--check'):
            r = subprocess.run([PY, '-I', '-B', TOOL, mode, *args], cwd=W, env=E, capture_output=True, text=True)
            (B / f'ordinary{mode}.log').write_text(r.stdout + r.stderr); row['ordinary' + mode] = r.returncode; print(mode, r.returncode, flush=True)
        new_receipt = json.loads((W / RECEIPT).read_bytes())
        changed_bindings = sorted(k for k in set(old_receipt['bindings']) | set(new_receipt['bindings']) if old_receipt['bindings'].get(k) != new_receipt['bindings'].get(k))
        row['comparison'] = dict(rowsEqual=old_receipt['rows'] == new_receipt['rows'], stateEqual=old_receipt['state'] == new_receipt['state'],
                                 standingEqual=old_receipt['standing'] == new_receipt['standing'], changedBindings=changed_bindings,
                                 referenceRowsChanged=sorted(x['path'] for x in new_receipt['bindings']['reference'] if x not in old_receipt['bindings']['reference']),
                                 censusRecordByteIdentical=(W / CENSUS).read_bytes() == old_census)
        print('comparison', json.dumps(row['comparison']), flush=True)
    row['receipt'] = dict(path=RECEIPT, bytes=len((W / RECEIPT).read_bytes()), sha256=hashlib.sha256((W / RECEIPT).read_bytes()).hexdigest()) if (W / RECEIPT).is_file() else None
    row.update(privateTMPDIR=str(T), laneOwnedByThisProcess=True, productBase=git(P, 'rev-parse', 'HEAD'), worktreeChanges=git(W, 'status', '--porcelain').splitlines(), standing='B2-b4c3 BLIND REFRESH RUN RECORD')
    (B / 'run.json').write_text(json.dumps(row, indent=2) + '\n')
finally:
    if owned: lane.rmdir()
