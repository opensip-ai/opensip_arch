"""The C1b batch's blind validation and refresh (C1b plan r6 LD-C1B-7): the one reviewed blind run after C1b-2's
integration, under the C1b refresh pre-run gate (the owner's standing answer: the mechanical blind run; a reviewed
pre-run gate, then the run, then a post-run review). Adapted from C1a4-blind's run_c1a4_blind.py. In a clean detached
worktree of product main, after removing both stale receipts there, it runs:
  1. discovery's reviewed --held-out-blind, once: the discovery receipt refreshed against the frozen bindings;
  2. the companion's reviewed --held-out-blind, once, only if discovery's succeeded: the companion receipt refreshed;
then the ordinary modes regenerate and check the discovery census and snapshot census records, and check the workspace
ledger. The lead sees only each blind run's one-line stdout summary, its exit code, its stderr (which must be empty)
and the receipts (ids, verdicts and per-mille margins only). One lane hold, nice 10, private TMPDIR, PATH /usr/bin:/bin.
Nothing here reads a held-out store except the two reviewed blind modes themselves, which are unchanged since their
reviews (B2-b4c, B3-b3a2; C1a4-blind).

The freeze (the gate's LD-CBR-2): main descends from the gate's freeze base, and both receipts' bindings recomputed on
main by each tool's own binding function equal the frozen bindings exactly; the five tools and the architecture-side
bound inputs keep their frozen bytes; the run refuses unless the frozen record, the freeze script and the post-run
checker beside it have their reviewed bytes.

Usage: /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B <this committed path> /tmp/opensip-implementation/c1b-refresh-run
       ... <this path> --preflight <frozen json>   (the freeze's checks against product main only: no lane, no worktree,
       no removal, no blind mode; for the gate's own self-review before the freeze is pinned)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, sys
W = Path('/Users/sb/code/opensip-ai/opensip-native-owner-c1b-refresh'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'; CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
PREFLIGHT = sys.argv[1] == '--preflight'
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
EV = Path(__file__).resolve().parent
DISCOVERY = 'tools/security/discovery_census.py'; COMPANION = 'tools/security/snapshot_ledger_census.py'; WORKSPACE = 'tools/security/discovery_workspace_ledger.py'
D_RECEIPT = 'crates/security/src/custody/discovery_census_held_out.json'; D_CENSUS = 'crates/security/src/custody/discovery_census.json'
S_RECEIPT = 'crates/security/src/snapshot_ledger_census_held_out.json'; S_CENSUS = 'crates/security/src/snapshot_ledger_census.json'
RUN_FILES = sorted([D_CENSUS, D_RECEIPT, S_CENSUS, S_RECEIPT])
# The reviewed bytes (filled by build_c1b_refresh_package.py from the frozen record; the run refuses any other).
FROZEN_SHA256 = '8343b13a845d9b85cf24163a24c54dc08699f0543a12df1e7a8b0528a9fd288f'
FREEZE_SCRIPT_SHA256 = '7ddedeb487de13a8a6b512de19e931757144b90685ca7bb6ed6a74259f0957a8'
POST_CHECKS_SHA256 = '45473c742152a614aa59e65b3f443c2ccde752775e429ca05a1b2bedbbb3d27a'
FROZEN = EV / 'frozen-bindings.json'; FREEZE_SCRIPT = EV / 'freeze_c1b_refresh.py'; POST_CHECKS = EV / 'run_c1b_refresh_post_checks.py'


def receipt_ready(name, receipt, baseline, bindings):
    if receipt.get('bindings') != bindings or receipt.get('standing') != baseline.get('standing'):
        return False
    rows=receipt.get('rows', [])
    if [r.get('id') for r in rows] != [r['id'] for r in baseline['rows']]:
        return False
    allowed={'measured'} if name=='discovery' else {'measured','over-item-5'}
    if not rows or any(r.get('status') not in allowed or r.get('integrity') is not True or r.get('population') is not True for r in rows):
        return False
    if name=='discovery':
        return receipt.get('state')=='holds (blind census)' and rows==baseline['rows']
    return receipt.get('state') in ('holds (blind census)','fails (blind census)')


def freeze_holds(root, frozen, env):
    """The freeze's checks against `root` (the run worktree, or main in preflight): main descends from the freeze
    base; the tools and the architecture-side inputs keep their frozen bytes; both receipts' bindings, recomputed by
    each tool's own binding function, equal the frozen ones; the committed receipts are the frozen ones."""
    assert subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=P,env=env).decode().strip()==frozen['freezeBase'], 'main moved since exact freeze'
    for row in frozen['tools']:
        assert hashlib.sha256((root / row['path']).read_bytes()).hexdigest() == row['sha256'] == hashlib.sha256((P / row['path']).read_bytes()).hexdigest(), row['path']
    for row in frozen['architectureInputs']:
        assert hashlib.sha256((A / row['path']).read_bytes()).hexdigest() == row['sha256'], row['path']
    now = json.loads(subprocess.check_output([PY, '-I', '-B', str(FREEZE_SCRIPT), '--bindings', str(root), str(A), str(P)], cwd=root, env=env))
    assert now == frozen['frozenBindings'], 'a bound input moved since the freeze: the gate is void'
    for name, rel in (('discovery', D_RECEIPT), ('companion', S_RECEIPT)):
        raw = (root / rel).read_bytes(); assert {'path': rel, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()} == frozen['receipts'][name]['receipt'], rel


if PREFLIGHT:
    frozen = json.loads(Path(sys.argv[2]).read_bytes()); assert frozen['passed']
    E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    assert subprocess.check_output(['/usr/bin/git', 'status', '--porcelain'], cwd=P, env=E).decode() == ''
    freeze_holds(P, frozen, E)
    print(json.dumps(dict(preflight='passed', freezeBase=frozen['freezeBase'], productMain=subprocess.check_output(['/usr/bin/git', 'rev-parse', 'HEAD'], cwd=P, env=E).decode().strip())))
    raise SystemExit(0)
gate=json.loads((A / ('docs/implementation/m3/native-publication/native-owner-c1b-refresh-r1-unit.json')).read_bytes())
assert gate['rootSubstantiveAssent'] and gate['runAuthorized'] and gate['status']=='ACCEPTED-UNIT'
review_pin=gate['independentReview'];review_raw=(A/review_pin['path']).read_bytes()
assert len(review_raw)==review_pin['bytes'] and hashlib.sha256(review_raw).hexdigest()==review_pin['sha256']
review=json.loads(review_raw);assert review['runAuthorized'] and review['verdict'] in ('ACCEPT','ACCEPT-UNIT') and not review['requiredFindings']
manifest_pin=gate['subjectManifest'];manifest_raw=(A/manifest_pin['path']).read_bytes()
assert len(manifest_raw)==manifest_pin['bytes'] and hashlib.sha256(manifest_raw).hexdigest()==manifest_pin['sha256']==review['subjectManifestSha256']
self_path=Path(__file__).resolve().relative_to(A).as_posix();self_raw=Path(__file__).read_bytes()
assert any(r['path']==self_path and r['bytes']==len(self_raw) and r['sha256']==hashlib.sha256(self_raw).hexdigest() for r in json.loads(manifest_raw)['files'])
interpreter=json.loads((EV.parent/'source.json').read_bytes())['interpreter'];py_raw=Path(PY).read_bytes()
assert interpreter['path']==PY and len(py_raw)==interpreter['bytes'] and hashlib.sha256(py_raw).hexdigest()==interpreter['sha256']
B = Path(sys.argv[1]); B.mkdir(parents=True)
for path, sha in ((FROZEN, FROZEN_SHA256), (FREEZE_SCRIPT, FREEZE_SCRIPT_SHA256), (POST_CHECKS, POST_CHECKS_SHA256)):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, ('not the reviewed bytes', path.name)
frozen = json.loads(FROZEN.read_bytes()); assert frozen['passed']
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-native-owner-c1b-refresh-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/usr/bin:/bin', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    # The run worktree: detached, clean with no untracked file, and a worktree of the product repository.
    assert subprocess.run(['/usr/bin/git', 'symbolic-ref', '-q', 'HEAD'], cwd=W, env=E, capture_output=True).returncode != 0, 'the run worktree is not detached'
    assert git(W, 'status', '--porcelain', '--untracked-files=all') == ''
    assert Path(git(W, 'rev-parse', '--path-format=absolute', '--git-common-dir')) == Path(git(P, 'rev-parse', '--path-format=absolute', '--git-common-dir'))
    # The freeze, executable: main descends from the freeze base; every bound input is the frozen one.
    freeze_holds(W, frozen, E)
    old = {rel: json.loads((W / rel).read_bytes()) for rel in RUN_FILES}
    (W / D_RECEIPT).unlink(); (W / S_RECEIPT).unlink()  # both stale; each reviewed blind mode writes its fresh one
    args = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]
    row = dict(frozen=dict(path=str(FROZEN), sha256=FROZEN_SHA256), freezeBase=frozen['freezeBase'], productMain=git(P, 'rev-parse', 'HEAD'))
    blind_ok = True
    for name, tool, receipt in (('discovery', DISCOVERY, D_RECEIPT), ('companion', COMPANION, S_RECEIPT)):
        r = subprocess.run([PY, '-I', '-B', tool, '--held-out-blind', *args], cwd=W, env=E, capture_output=True, text=True)
        (B / f'{name}-blind-stdout.txt').write_text(r.stdout); (B / f'{name}-blind-stderr.txt').write_text(r.stderr)
        row[name] = dict(blindExitCode=r.returncode, blindStdout=r.stdout, blindStderrEmpty=r.stderr == '', receiptWritten=(W / receipt).is_file())
        print(name, 'blind', r.returncode, r.stdout.strip(), 'stderr-empty' if r.stderr == '' else 'STDERR-NONEMPTY', flush=True)
        blind_ok = blind_ok and r.returncode == 0 and r.stderr == '' and (W / receipt).is_file()
        if blind_ok:
            try:
                public_receipt=json.loads((W/receipt).read_bytes())
                blind_ok=receipt_ready(name, public_receipt, old[receipt], frozen['frozenBindings'][name])
            except (ValueError,KeyError,TypeError):
                blind_ok=False
            row[name]['receiptAllowedAndExpected']=blind_ok
        if not blind_ok:
            break  # exit0 with an error row is still a failure; do not run companion

    ordinary_ok=False
    if blind_ok:
        ordinary_ok=True
        for tool, modes in ((DISCOVERY, ('--write', '--check')), (WORKSPACE, ('--check',)), (COMPANION, ('--write', '--check'))):
            for mode in modes:
                r = subprocess.run([PY, '-I', '-B', tool, mode, *args], cwd=W, env=E, capture_output=True, text=True)
                tag = Path(tool).stem + mode
                (B / f'ordinary-{tag}.log').write_text(r.stdout + r.stderr); row['ordinary-' + tag] = r.returncode; print(tag, r.returncode, flush=True)
                if r.returncode!=0:
                    ordinary_ok=False
                    break
            if not ordinary_ok:
                break
        if ordinary_ok:
            new = {rel: json.loads((W / rel).read_bytes()) for rel in RUN_FILES}
            comparison = {}
            for name, receipt, census, rows_key in (('discovery', D_RECEIPT, D_CENSUS, 'entries'), ('companion', S_RECEIPT, S_CENSUS, 'heldOutEntries')):
                o, n = old[receipt], new[receipt]
                changed = sorted(k for k in set(o['bindings']) | set(n['bindings']) if o['bindings'].get(k) != n['bindings'].get(k))
                held = [e for e in new[census][rows_key] if isinstance(e.get('status'), str) and (e['status'].startswith('outstanding') or e['status'] == 'blind-census')]
                comparison[name] = dict(
                    ids=[r['id'] for r in n['rows']] == [r['id'] for r in o['rows']], state=n['state'],
                    bindingsEqualFrozen=n['bindings'] == frozen['frozenBindings'][name],
                    changedBindings=changed, expectedChangedBindings=sorted(frozen['receipts'][name]['cumulativeDelta']),
                    bindingsAsExpected=changed == sorted(frozen['receipts'][name]['cumulativeDelta']),
                    rowsEqualOldReceipt=n['rows'] == o['rows'], statuses={r['id']: r['status'] for r in n['rows']},
                    censusChangedKeys=sorted(k for k in set(old[census]) | set(new[census]) if old[census].get(k) != new[census].get(k)),
                    renderedHeldOut=sorted({e['status'] for e in held}), heldOutMargin=new[census].get('heldOutMargin'))
            comparison['discovery'].update(failingEntries=new[D_CENSUS]['failingEntries'], caps=new[D_CENSUS]['caps'])
            comparison['companion'].update(failing2x=new[S_CENSUS]['failing2x']['snapshotProfile'], capsStatus=new[S_CENSUS]['capsStatus'])
            row['comparison'] = comparison
            print('comparison', json.dumps(comparison), flush=True)
    row['receipts'] = {rel: (dict(path=rel, bytes=len((W / rel).read_bytes()), sha256=hashlib.sha256((W / rel).read_bytes()).hexdigest()) if (W / rel).is_file() else None)
                       for rel in (D_RECEIPT, S_RECEIPT)}
    status = subprocess.check_output(['/usr/bin/git', 'status', '--porcelain', '--untracked-files=all'], cwd=W, env=E).decode()
    row.update(privateTMPDIR=str(T), laneOwnedByThisProcess=True, worktreeChanges=sorted(line[3:] for line in status.splitlines()),
               worktreeChangesExactlyTheRunsFour=sorted(line[3:] for line in status.splitlines()) == RUN_FILES, standing='C1b batch BLIND RUN RECORD')
    comparison=row.get('comparison',{})
    row['eligibleForPostRunReview']=bool(blind_ok and ordinary_ok and row['worktreeChangesExactlyTheRunsFour'] and comparison.get('discovery',{}).get('rowsEqualOldReceipt') and all(comparison.get(n,{}).get('ids') and comparison.get(n,{}).get('bindingsEqualFrozen') and comparison.get(n,{}).get('bindingsAsExpected') for n in ('discovery','companion')))
    (B / 'run.json').write_text(json.dumps(row, indent=2) + '\n')
finally:
    if owned: lane.rmdir()
