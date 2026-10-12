from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, statistics, sys, shutil
# SM-5 typed synthetic snapshot/plan-equivalent sealing over the remaining Rust/TS development read sets (small, large,
# very-large repositories and the three remaining overlay workspaces). Reuses the CLOSED accepted probe and control
# template from docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09 at their committed bytes, unchanged.
# Repository-only read sets, as in the closed precedent; dependency-source sets are not invented.
# A failing child is retained and reported for that workload instead of aborting the set.
os.setpriority(os.PRIO_PROCESS, 0, 10)
parent_nice = os.getpriority(os.PRIO_PROCESS, 0); assert parent_nice == 10
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'; C = Path('/Users/sb/code/.opensip-implementation-cache')
closed = A / 'docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09'
B = Path('/tmp/opensip-implementation/sm-sealing-typed-remaining-2026-10-11'); assert not B.exists(); B.mkdir()
def pin(p): raw = Path(p).read_bytes(); return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
env_git = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: env_git.pop(k, None)
closed_pins = []
for name in ['probe.py', 'control-template.json', 'run_set.py', 'audit.py']:
    committed = subprocess.check_output(['/usr/bin/git', 'show', 'HEAD:docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09/' + name], cwd=A, env=env_git)
    assert (closed / name).read_bytes() == committed
    shutil.copyfile(closed / name, B / name); closed_pins.append(dict(pin(B / name), committedPath='docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09/' + name))
sys.path.insert(0, str(P / 'tools/quality')); from corpus import manifest_document; from store import verify
raw = (A / 'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes(); assert hashlib.sha256(raw).hexdigest() == 'c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578'
m = manifest_document(raw); entries = {r['id']: r for r in m['repositories']}
ids = sorted({i for lang in ['rust', 'tsjs'] for size in ['small', 'large', 'very-large'] for i in m['counts'][lang][size]['devIds']})
assert len(ids) == 18 and all(entries[i]['heldOut'] is False for i in ids)
store = C / 't2-corpus-c8cc48e1/store'
workloads = [dict(id=i, members=[dict(root=str(store / entries[i]['treeDigest']['value']), prefix='', entry=i)]) for i in ids]
for overlay in m['workspaces']:
    if overlay['id'] == 'mr-rs-medium-serde-json' or overlay['id'].startswith('mr-py-'): continue
    assert overlay['heldOut'] is False and all(entries[i]['heldOut'] is False for i in overlay['memberIds'])
    workloads.append(dict(id=overlay['id'], members=[dict(root=str(store / entries[r['entry']]['treeDigest']['value']), prefix=r['mount'] + '/', entry=r['entry']) for r in overlay['overlay']['members']], overlayDefinition=overlay['overlay'], overlayDigest=overlay['overlayDigest'], overlayConfigurationNotCaptured=True))
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lock = D / 'opensip-lanes.lock'; owned = False
while True:
    try: lock.mkdir(); owned = True; break
    except FileExistsError: print('waiting for typed sealing measurement lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-sm-seal-remaining-', dir=D)).resolve(); T.chmod(0o700)
    env = dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T))
    for key in ['HOME', 'LANG', 'LC_ALL', 'TZ']:
        if key in os.environ: env[key] = os.environ[key]
    result = []
    for w in workloads:
        proofs = [dict(entry=member['entry'], treeVerified=verify(Path(member['root']), entries[member['entry']])) for member in w['members']]
        inp = B / (w['id'] + '-input.json'); inp.write_text(json.dumps(w, indent=2) + '\n'); runs = []; shape = None; failure = None
        for n in range(10):
            out = B / f'{w["id"]}-{n}.stdout'; err = B / f'{w["id"]}-{n}.stderr'
            with out.open('wb') as o, err.open('wb') as e:
                child = subprocess.Popen(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14', '-I', '-B', str(B / 'probe.py'), str(inp)], cwd=T, env=env, stdout=o, stderr=e)
                child_nice = os.getpriority(os.PRIO_PROCESS, child.pid); assert child_nice == 10
                _, status, usage = os.wait4(child.pid, 0); code = os.waitstatus_to_exitcode(status)
            if code != 0:
                failure = dict(ordinal=n, exitCode=code, stderr=pin(err)); print(w['id'], 'child failed', code, flush=True); break
            r = json.loads(out.read_text()); current = {k: v for k, v in r.items() if k != 'elapsedNanos'}; shape = current if shape is None else shape
            assert shape == current and r['registeredSnapshotPlanShapesPassed'] is True and err.read_bytes() == b''
            rss = int(usage.ru_maxrss); runs.append(dict(ordinal=n, observedChildNiceness=child_nice, warmup=n < 3, elapsedNanos=r['elapsedNanos'], exitCode=0, rssNative=rss, rssUnit='bytes', rssBytes=rss))
        row = dict(id=w['id'], heldOut=False, verifiedMembers=proofs, runs=runs, failure=failure, overlayConfigurationNotCaptured=w.get('overlayConfigurationNotCaptured', False))
        if failure is None:
            values = [r['elapsedNanos'] for r in runs if not r['warmup']]
            row.update(rows=shape['rows'], bytes=shape['bytes'], snapshotEquivalentDescriptorBytes=shape['snapshotEquivalentDescriptorBytes'], nonregularExcluded=len(shape['nonregularExcluded']),
                       withinSnapshot2Rows=shape['rows'] <= 100000, withinSnapshot2Descriptor=shape['snapshotEquivalentDescriptorBytes'] <= 4 << 20, withinSnapshot2TotalBytes=shape['bytes'] <= 8 << 30,
                       medianNanos=statistics.median(values), maxNanos=max(values))
            print(w['id'], row['rows'], 'rows', row['snapshotEquivalentDescriptorBytes'], 'descriptor bytes', flush=True)
        result.append(row)
        report = dict(standing='UNREVIEWED PRELIMINARY REMAINING RUST/TS DEVELOPMENT READSET TYPED SEALING; CLOSED PROBE/TEMPLATE REUSED; REPOSITORY-ONLY; NO ADMISSION', closedRecipePins=closed_pins, workloads=result,
                      host='lead macOS preliminary, not D12', ownedTMPDIR=str(T), TMPDIRMode='0700', laneHeldForEntireSet=True, nice=10, observedParentNiceness=parent_nice, HOMEUnchanged=True,
                      dependencySourceSetsIncluded=False, snapshotPlanIdentitiesAdmitted=False, SM5FigureComplete=False, SM5PlaceholderFilled=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
        (B / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
finally:
    if owned: lock.rmdir()
    assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
