"""C1a4-blind's run: the one reviewed blind validation run of C1a plan r6 RF-3 step 3, under the C1a4-blind pre-run gate
(the owner's decision of 2026-10-16, the mechanical blind run; a reviewed pre-run gate, then the run, then a post-run
review). In a clean detached worktree of product main, after removing the stale discovery receipt there, it runs:
  1. discovery's reviewed --held-out-blind, once: the discovery receipt refreshed against the final pins;
  2. the companion's reviewed --held-out-blind, once: the companion snapshot receipt, new;
then the ordinary modes regenerate and check the discovery census record and the snapshot census record, and checks the
workspace ledger. The lead sees only each blind run's one-line stdout summary, its exit code, its stderr (which must be
empty) and the receipts (ids, verdicts and per-mille margins only). One lane hold, nice 10, private TMPDIR, PATH
/usr/bin:/bin. Nothing here reads a held-out store except the two reviewed blind modes themselves.

r2 (Codex C1A4B-R1-RF-1 and NBO-1): it refuses unless the pinned post-run checker beside it has its reviewed bytes, and
it asserts the freeze before anything is removed: main is exactly the frozen base plus one commit, the gate's, whose
changed paths and bytes are the gate's product map's; and the run worktree is detached, clean (untracked files too) and
a worktree of the product repository.

Usage: /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B <this committed path> /tmp/opensip-implementation/c1a4b-run"""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1a4b'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'; CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
B = Path(sys.argv[1]); B.mkdir(parents=True)
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
DISCOVERY = 'tools/security/discovery_census.py'; MEMBER = 'tools/security/discovery_member_model.py'
COMPANION = 'tools/security/snapshot_ledger_census.py'; MODEL = 'tools/security/snapshot_ledger_model.py'; WORKSPACE = 'tools/security/discovery_workspace_ledger.py'
D_RECEIPT = 'crates/security/src/custody/discovery_census_held_out.json'; D_CENSUS = 'crates/security/src/custody/discovery_census.json'
S_RECEIPT = 'crates/security/src/snapshot_ledger_census_held_out.json'; S_CENSUS = 'crates/security/src/snapshot_ledger_census.json'
# The bytes the C1a4-blind gate reviews: the companion tool as the gate's product map archives it, and the four tools
# the gate leaves unchanged at main's bytes. The run refuses any other.
GATE = A / 'docs/implementation/m3/snapshot-plan-c/c1a4-blind-r2/product-map.json'
# The freeze (RUN-PLAN precondition 4): main is this base plus the gate's code commit only.
BASE = 'b7538549b727e13013f36d3b7c2e2917e767f3f2'
# The architecture-side bound inputs (the corpus manifest and discovery's reference-loading sources), outside the
# product freeze: each must keep the bytes it had at the gate, which are also the committed discovery receipt's.
ARCH_PINS = {
    'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json': 'c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578',
    'docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py': '6714575ccee1474e2d7c20c4e5e9b6c95b498ad155ec1e69fc9d6ba5f3e7e32b',
    'docs/coop/design-corrections/security/security_lifecycle_model_v1.py': 'd0ef9814d27b86f10bdc1aa9a9a4781124c93c3dd92eeecdfe3090fe21d18bb9',
    'docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py': '4a104209af0ba89c76826ba7f6be4c4085f1eb7db90410f6bb731041562fdcc8',
    'docs/coop/design-corrections/foundation/canonical.py': 'd47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442',
}
# The pinned post-run checker (C1A4B-R1-RF-1): the run refuses unless it has the reviewed bytes.
POST_CHECKS = Path(__file__).resolve().parent / 'run_c1a4b_post_checks.py'
POST_CHECKS_SHA256 = 'cc0286b986b15af17dafabe8ecab849890529ffc04414eb082dc4f9b3d0fc2c3'
assert hashlib.sha256(POST_CHECKS.read_bytes()).hexdigest() == POST_CHECKS_SHA256, 'the post-run checker is not the reviewed one'
REVIEWED = {DISCOVERY: '063820607dcbb46144bb97c239c065b2ab8cb85cb1e9359422560fa03ceaffef',
            MEMBER: '582bad12d1e04e95089a7c965b6c542f10da412fb0efe22c4b4758db4cf421f1',
            MODEL: 'b985d7c8d517443b96e407d3c40a4b3ee2710f465253730fda032b084f608214',
            WORKSPACE: 'ee1d597a31d2e75c11276bfc98ac61f5c2a43f38a8722712e453d64eb38b6940'}
REVIEWED[COMPANION] = next(r['candidate']['sha256'] for r in json.loads(GATE.read_bytes())['rows'] if r['path'] == COMPANION)
# The discovery receipt's bindings expected to change since the committed receipt, against main b753854 (B3-b3b's
# lesson: every one named): `closure`, in exactly two rows (C1a4's re-pin); `reference`, in exactly one row, the
# generator closure (D2b-0b, contract successor 175); and `tool` (discovery_census.py's CLOSURE rows, C1a4). The other
# five are expected equal: limits, manifest, memberModel, rootLengths, sizes.
EXPECTED_DISCOVERY_CHANGED = ['closure', 'reference', 'tool']
EXPECTED_CLOSURE_ROWS = ['crates/platform/src/work_ledger.rs', 'crates/security/src/custody/discovery_rule.rs']
EXPECTED_REFERENCE_ROWS = ['tools/contracts/generator-closure.json']
# The companion receipt is new: all seven of its bindings are new.
EXPECTED_COMPANION_BINDINGS = ['afterWalk', 'caps', 'discovery', 'item5', 'maxUnitDepth', 'snapshotSources', 'tools']
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1a4b-blind-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/usr/bin:/bin', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == '' and git(W, 'status', '--porcelain') == ''
    # The freeze, executable (C1A4B-R1-NBO-1): main is the base plus exactly one commit, the gate's, changing exactly the
    # gate's product-map paths to its candidate bytes.
    gate_rows = json.loads(GATE.read_bytes())['rows']
    assert git(P, 'rev-parse', 'HEAD^') == BASE and git(P, 'rev-list', '--count', BASE + '..HEAD') == '1', 'main is not the freeze plus the gate commit'
    assert sorted(git(P, 'diff', '--name-only', BASE, 'HEAD').splitlines()) == sorted(r['path'] for r in gate_rows), 'the gate commit changes other paths'
    for r in gate_rows:
        blob = subprocess.check_output(['/usr/bin/git', 'show', 'HEAD:' + r['path']], cwd=P, env=E)
        assert hashlib.sha256(blob).hexdigest() == r['candidate']['sha256'], r['path']
    for rel, sha in ARCH_PINS.items():
        assert hashlib.sha256((A / rel).read_bytes()).hexdigest() == sha, rel
    # The run worktree: detached, clean with no untracked file, and a worktree of the product repository.
    assert subprocess.run(['/usr/bin/git', 'symbolic-ref', '-q', 'HEAD'], cwd=W, env=E, capture_output=True).returncode != 0, 'the run worktree is not detached'
    assert git(W, 'status', '--porcelain', '--untracked-files=all') == ''
    assert Path(git(W, 'rev-parse', '--path-format=absolute', '--git-common-dir')) == Path(git(P, 'rev-parse', '--path-format=absolute', '--git-common-dir'))
    for rel, sha in REVIEWED.items():
        assert hashlib.sha256((W / rel).read_bytes()).hexdigest() == sha == hashlib.sha256((P / rel).read_bytes()).hexdigest(), rel
    assert not (W / S_RECEIPT).exists(), 'a companion receipt already exists'
    old_d_receipt = json.loads((W / D_RECEIPT).read_bytes()); old_d_census = json.loads((W / D_CENSUS).read_bytes()); old_s_census = json.loads((W / S_CENSUS).read_bytes())
    (W / D_RECEIPT).unlink()  # the stale discovery receipt; discovery's blind mode writes a fresh one
    args = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]
    row = dict(reviewed=REVIEWED)
    blind_ok = True
    for name, tool, receipt in (('discovery', DISCOVERY, D_RECEIPT), ('companion', COMPANION, S_RECEIPT)):
        r = subprocess.run([PY, '-I', '-B', tool, '--held-out-blind', *args], cwd=W, env=E, capture_output=True, text=True)
        (B / f'{name}-blind-stdout.txt').write_text(r.stdout); (B / f'{name}-blind-stderr.txt').write_text(r.stderr)
        row[name] = dict(blindExitCode=r.returncode, blindStdout=r.stdout, blindStderrEmpty=r.stderr == '', receiptWritten=(W / receipt).is_file())
        print(name, 'blind', r.returncode, r.stdout.strip(), 'stderr-empty' if r.stderr == '' else 'STDERR-NONEMPTY', flush=True)
        blind_ok = blind_ok and r.returncode == 0 and r.stderr == '' and (W / receipt).is_file()
        if not blind_ok:
            break  # the companion is not run after a discovery failure
    if blind_ok:
        for tool, modes in ((DISCOVERY, ('--write', '--check')), (WORKSPACE, ('--check',)), (COMPANION, ('--write', '--check'))):
            for mode in modes:
                r = subprocess.run([PY, '-I', '-B', tool, mode, *args], cwd=W, env=E, capture_output=True, text=True)
                tag = Path(tool).stem + mode
                (B / f'ordinary-{tag}.log').write_text(r.stdout + r.stderr); row['ordinary-' + tag] = r.returncode; print(tag, r.returncode, flush=True)
        new_d_receipt = json.loads((W / D_RECEIPT).read_bytes()); new_d_census = json.loads((W / D_CENSUS).read_bytes())
        new_s_receipt = json.loads((W / S_RECEIPT).read_bytes()); new_s_census = json.loads((W / S_CENSUS).read_bytes())
        changed = sorted(k for k in set(old_d_receipt['bindings']) | set(new_d_receipt['bindings']) if old_d_receipt['bindings'].get(k) != new_d_receipt['bindings'].get(k))
        closure_rows = sorted(o['path'] for o, n in zip(old_d_receipt['bindings']['closure'], new_d_receipt['bindings']['closure']) if o != n)
        reference_rows = sorted(o['path'] for o, n in zip(old_d_receipt['bindings']['reference'], new_d_receipt['bindings']['reference']) if o != n)
        readable = lambda census: [e for e in census['entries'] if not isinstance(e.get('status'), str)]
        row['comparison'] = dict(
            discovery=dict(ids=[r['id'] for r in new_d_receipt['rows']] == [r['id'] for r in old_d_receipt['rows']], state=new_d_receipt['state'],
                           # No discovery charge changed (C1a4 left discovery's classify_cost and caps unchanged), so every row is expected equal.
                           rowsEqualOldReceipt=new_d_receipt['rows'] == old_d_receipt['rows'],
                           changedBindings=changed, expectedChangedBindings=EXPECTED_DISCOVERY_CHANGED, changedClosureRows=closure_rows,
                           expectedClosureRows=EXPECTED_CLOSURE_ROWS, changedReferenceRows=reference_rows, expectedReferenceRows=EXPECTED_REFERENCE_ROWS,
                           bindingsAsExpected=changed == EXPECTED_DISCOVERY_CHANGED and closure_rows == EXPECTED_CLOSURE_ROWS and reference_rows == EXPECTED_REFERENCE_ROWS,
                           censusChangedKeys=sorted(k for k in set(old_d_census) | set(new_d_census) if old_d_census.get(k) != new_d_census.get(k)),
                           leadReadableRowsEqual=readable(old_d_census) == readable(new_d_census), workspacesEqual=old_d_census['workspaces'] == new_d_census['workspaces'],
                           heldOutMargin=new_d_census['heldOutMargin'], failingEntries=new_d_census['failingEntries'], caps=new_d_census['caps']),
            companion=dict(ids=[r['id'] for r in new_s_receipt['rows']] == [r['id'] for r in old_d_receipt['rows']], state=new_s_receipt['state'],
                           bindings=sorted(new_s_receipt['bindings']), expectedBindings=EXPECTED_COMPANION_BINDINGS,
                           bindingsAsExpected=sorted(new_s_receipt['bindings']) == EXPECTED_COMPANION_BINDINGS,
                           statuses={r['id']: r['status'] for r in new_s_receipt['rows']},
                           censusChangedKeys=sorted(k for k in set(old_s_census) | set(new_s_census) if old_s_census.get(k) != new_s_census.get(k)),
                           leadReadableRowsEqual=old_s_census['entries'] == new_s_census['entries'] and old_s_census['workspaces'] == new_s_census['workspaces'],
                           heldOutMargin=new_s_census['heldOutMargin'], failing2x=new_s_census['failing2x']['snapshotProfile'], capsStatus=new_s_census['capsStatus']))
        print('comparison', json.dumps(row['comparison']), flush=True)
    row['receipts'] = {rel: (dict(path=rel, bytes=len((W / rel).read_bytes()), sha256=hashlib.sha256((W / rel).read_bytes()).hexdigest()) if (W / rel).is_file() else None)
                       for rel in (D_RECEIPT, S_RECEIPT)}
    row.update(privateTMPDIR=str(T), laneOwnedByThisProcess=True, productBase=git(P, 'rev-parse', 'HEAD'),
               worktreeChanges=sorted(git(W, 'status', '--porcelain', '--untracked-files=all').splitlines()), standing='C1a4-blind BLIND RUN RECORD')
    (B / 'run.json').write_text(json.dumps(row, indent=2) + '\n')
finally:
    if owned: lane.rmdir()
