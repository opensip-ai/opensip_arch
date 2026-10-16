"""B2-b4c2: the blind held-out census run (B2-b4 plan r6 section 2.5; the owner decision of 2026-10-16), on the reviewed B2-b4c1
code. One lane hold, nice 10, private TMPDIR. It runs the tool with --held-out-blind exactly once; the lead sees only its one-line stdout
summary and its exit code, and stderr must be empty. Then the ordinary mode regenerates the census record from the receipt (--write)
and checks it (--check). Nothing here reads a held-out store except the reviewed blind mode itself."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b2b4c2'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'; CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
B = Path(sys.argv[1]); B.mkdir(parents=True)
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'; TOOL = 'tools/security/discovery_census.py'; RECEIPT = 'crates/security/src/custody/discovery_census_held_out.json'
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b2b4c2-blind-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/usr/bin:/bin', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == '' and git(W, 'status', '--porcelain') == ''
    assert not (W / RECEIPT).exists()
    tool = hashlib.sha256((W / TOOL).read_bytes()).hexdigest(); reviewed = hashlib.sha256((P / TOOL).read_bytes()).hexdigest(); assert tool == reviewed
    args = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]
    blind = subprocess.run([PY, '-I', '-B', TOOL, '--held-out-blind', *args], cwd=W, env=E, capture_output=True, text=True)
    (B / 'blind-stdout.txt').write_text(blind.stdout); (B / 'blind-stderr.txt').write_text(blind.stderr)
    row = dict(blindExitCode=blind.returncode, blindStdout=blind.stdout, blindStderrEmpty=blind.stderr == '', receiptWritten=(W / RECEIPT).is_file(), toolSha256=tool)
    print('blind', blind.returncode, blind.stdout.strip(), 'stderr-empty' if blind.stderr == '' else 'STDERR-NONEMPTY', flush=True)
    if blind.returncode == 0 and (W / RECEIPT).is_file():
        for mode in ('--write', '--check'):
            r = subprocess.run([PY, '-I', '-B', TOOL, mode, *args], cwd=W, env=E, capture_output=True, text=True)
            (B / f'ordinary{mode}.log').write_text(r.stdout + r.stderr); row['ordinary' + mode] = r.returncode; print(mode, r.returncode, flush=True)
    row['receipt'] = dict(path=RECEIPT, bytes=len((W / RECEIPT).read_bytes()), sha256=hashlib.sha256((W / RECEIPT).read_bytes()).hexdigest()) if (W / RECEIPT).is_file() else None
    row.update(privateTMPDIR=str(T), laneOwnedByThisProcess=True, productBase=git(P, 'rev-parse', 'HEAD'), standing='B2-b4c2 BLIND RUN RECORD')
    (B / 'run.json').write_text(json.dumps(row, indent=2) + '\n')
finally:
    if owned: lane.rmdir()
