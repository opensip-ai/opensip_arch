"""B3-b3b: the blind held-out run of B3-b3a2's accepted tool (B3-b plan r2 amendment A5; the owner's decision of
2026-10-16, the mechanical blind run; a reviewed pre-run gate, then the run, then a post-run review). It runs the reviewed
tool's --held-out-blind exactly once in a clean detached worktree of product main, after removing the stale walker-only
receipt there; the lead sees only its one-line stdout summary, its exit code, its stderr (which must be empty) and the
receipt (ids, verdicts and per-mille margins only). Then the ordinary mode regenerates and checks the census record. One
lane hold, nice 10, private TMPDIR. Nothing here reads a held-out store except the reviewed blind mode itself."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b3b3b'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'; CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
B = Path(sys.argv[1]); B.mkdir(parents=True)
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'; TOOL = 'tools/security/discovery_census.py'; MODEL = 'tools/security/discovery_member_model.py'
RECEIPT = 'crates/security/src/custody/discovery_census_held_out.json'; CENSUS = 'crates/security/src/custody/discovery_census.json'
# The bytes Codex's B3-b3a2 gate accepts; the run refuses any other tool or member model.
REVIEWED = {TOOL: '6e52bd5bed8599071fb595bd4050e1cad93307987107238cbfad58b1f7fc99c6',
            MODEL: '582bad12d1e04e95089a7c965b6c542f10da412fb0efe22c4b4758db4cf421f1'}
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b3b3b-blind-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/usr/bin:/bin', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == '' and git(W, 'status', '--porcelain') == ''
    for rel, sha in REVIEWED.items():
        assert hashlib.sha256((W / rel).read_bytes()).hexdigest() == sha == hashlib.sha256((P / rel).read_bytes()).hexdigest(), rel
    old_receipt = json.loads((W / RECEIPT).read_bytes()); old_census = json.loads((W / CENSUS).read_bytes())
    (W / RECEIPT).unlink()  # the stale walker-only receipt; the blind mode writes a fresh one
    args = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]
    blind = subprocess.run([PY, '-I', '-B', TOOL, '--held-out-blind', *args], cwd=W, env=E, capture_output=True, text=True)
    (B / 'blind-stdout.txt').write_text(blind.stdout); (B / 'blind-stderr.txt').write_text(blind.stderr)
    row = dict(blindExitCode=blind.returncode, blindStdout=blind.stdout, blindStderrEmpty=blind.stderr == '', receiptWritten=(W / RECEIPT).is_file(),
               reviewed=REVIEWED)
    print('blind', blind.returncode, blind.stdout.strip(), 'stderr-empty' if blind.stderr == '' else 'STDERR-NONEMPTY', flush=True)
    if blind.returncode == 0 and (W / RECEIPT).is_file():
        for mode in ('--write', '--check'):
            r = subprocess.run([PY, '-I', '-B', TOOL, mode, *args], cwd=W, env=E, capture_output=True, text=True)
            (B / f'ordinary{mode}.log').write_text(r.stdout + r.stderr); row['ordinary' + mode] = r.returncode; print(mode, r.returncode, flush=True)
        new_receipt = json.loads((W / RECEIPT).read_bytes()); new_census = json.loads((W / CENSUS).read_bytes())
        old_rows = {r['id']: r for r in old_receipt['rows']}
        # The full ledger dominates the walker, so each measured margin is expected at or below the walker-only one.
        within = {r['id']: r['status'] == 'measured' and old_rows.get(r['id'], {}).get('status') == 'measured'
                  and all(r['marginPermille'][k] <= old_rows[r['id']]['marginPermille'][k] for k in ('objects', 'edges', 'bytes'))
                  for r in new_receipt['rows']}
        changed_bindings = sorted(k for k in set(old_receipt['bindings']) | set(new_receipt['bindings']) if old_receipt['bindings'].get(k) != new_receipt['bindings'].get(k))
        census_changed = sorted(k for k in set(old_census) | set(new_census) if old_census.get(k) != new_census.get(k))
        readable_equal = [e for e in old_census['entries'] if e.get('status') is None] == [e for e in new_census['entries'] if e.get('status') is None]
        row['comparison'] = dict(ids=[r['id'] for r in new_receipt['rows']] == [r['id'] for r in old_receipt['rows']], state=new_receipt['state'],
                                 marginsWithinWalkerOnly=within, changedBindings=changed_bindings, censusChangedKeys=census_changed,
                                 leadReadableRowsEqual=readable_equal, workspacesEqual=old_census['workspaces'] == new_census['workspaces'],
                                 heldOutMargin=new_census['heldOutMargin'], failingEntries=new_census['failingEntries'], caps=new_census['caps'])
        print('comparison', json.dumps(row['comparison']), flush=True)
    row['receipt'] = dict(path=RECEIPT, bytes=len((W / RECEIPT).read_bytes()), sha256=hashlib.sha256((W / RECEIPT).read_bytes()).hexdigest()) if (W / RECEIPT).is_file() else None
    row.update(privateTMPDIR=str(T), laneOwnedByThisProcess=True, productBase=git(P, 'rev-parse', 'HEAD'), worktreeChanges=git(W, 'status', '--porcelain').splitlines(), standing='B3-b3b BLIND RUN RECORD')
    (B / 'run.json').write_text(json.dumps(row, indent=2) + '\n')
finally:
    if owned: lane.rmdir()
