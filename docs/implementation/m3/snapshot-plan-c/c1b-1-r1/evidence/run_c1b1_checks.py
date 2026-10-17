"""C1b-1 r1 candidate checks (M3-C r8 item 4; C1b plan r6, sub-unit C1b-1: the snapshot's Git reads). Adapted from
C1c-0 r2's run_c1c0_checks.py.

The security and host suites on the base checkout and the candidate (--no-fail-fast; equal failure sets after isolated
reruns, and the new passing tests); rustfmt on the new and base-clean edited files; the base-dirty files edited by
appending only; warning-denied all-targets Clippy on the two crates; the focused VCS, Git tracking and operation tests;
the charge model --check; the vector moves (the walk, opener and session predictions unchanged; the VCS vectors new);
the cap derivation from the model (vcs_derivation_c1b1.py); the discovery census, workspace ledger and snapshot census
--checks over the lead-readable cache only; the census closure (exactly git_tracking.rs changed, as expected); the
cumulative receipt-specific record (each receipt against its accepted baseline and current bindings, from public
receipt fields only); FW-01; the environment exceptions; the operability source census; verify_design; and the plan's
C1b-1 mutations, each of which must fail its focused tests. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1b1'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = Path(__file__).resolve().parent
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
VCS = 'crates/security/src/snapshot_vcs.rs'; GT = 'crates/security/src/custody/git_tracking.rs'
MODEL = 'tools/security/snapshot_ledger_model.py'
VECTORS = 'crates/security/src/snapshot_ledger_vectors.json'; SESSION_VECTORS = 'crates/host/src/snapshot_session_vectors.json'
VCS_VECTORS = 'crates/security/src/snapshot_vcs_vectors.json'
# The new passing tests: security 22 (snapshot_vcs_tests.rs); host none. Platform is untouched.
NEW_TESTS = {'opensip-host': 0, 'opensip-security': 22}
SERIAL = set()
EXPECTED_CLOSURE_CHANGES = [GT]
# Edited by appending only (base-dirty under rustfmt, C1b plan r6 section 6).
APPEND_ONLY = [GT, 'crates/security/src/lib.rs']
T2 = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
CARGO = [R + 'cargo', 'test', '--locked', '--offline']
FOCUSED = {
    'vcs': CARGO + ['-p', 'opensip-security', '--lib', '--', 'snapshot_vcs'],
    'tracking': CARGO + ['-p', 'opensip-security', '--lib', '--', 'custody::git_tracking', 'snapshot_source'],
}
JUDGE = '        git::snapshot_judge(\n            &file,\n            ProjectObject::ConfigurationFile,\n'
MUTATIONS = [
    # (name, file, [(before, after)], focus): each weakens one C1b-1 rule (C1b plan r6 section 5); its focused tests fail.
    ('symbolic-chain-followed', VCS, [('            return unsupported("symbolic-ref-chain");\n', '            return Ok(None);\n')], 'vcs'),
    ('packed-read-before-loose', VCS, [('            Ok(Head::Symbolic(target)) => match self.loose(dot_git, target, work)? {\n                Some(commit) => commit,\n                None => self.packed(dot_git, target, work)?,\n            },\n',
                                        '            Ok(Head::Symbolic(target)) => self.packed(dot_git, target, work)?,\n')], 'vcs'),
    ('unborn-taken-as-null-commit', VCS, [('            Ok(None) => unsupported("unborn-head"),\n', '            Ok(None) => Ok(CommitId([b\'0\'; COMMIT_HEX])),\n')], 'vcs'),
    ('custody-skipped-for-head', VCS, [(JUDGE, '        if reasons.custody != "head-custody" {\n' + JUDGE),
                                       ('            work,\n        )?;\n        let raw = git::snapshot_read', '            work,\n        )?;\n        }\n        let raw = git::snapshot_read')], 'vcs'),
    ('evidence-recheck-skipped', VCS, [('        if git::snapshot_metadata(dot_git.as_file(), work)? != *proof.sample() {\n',
                                        '        if git::snapshot_metadata(dot_git.as_file(), work)? != *proof.sample() && false {\n')], 'vcs'),
    ('outermost-repository-taken', GT, [('        for index in (0..=chain.path().component_count()).rev() {\n', '        for index in 0..=chain.path().component_count() {\n')], 'vcs'),
    ('a-read-uncharged', VCS, [('        work.charge::<TrackingRefusal>(parse_cost(raw.len()))?;\n', '')], 'vcs'),
    # r4: the budget refusal turned into an observation's refusal.
    ('budget-taken-as-unborn-head', VCS, [('        WorkFailure::Budget(budget) => return WorkFailure::Budget(budget),\n',
                                           '        WorkFailure::Budget(_) => VcsRefusal::Unsupported("unborn-head"),\n')], 'vcs'),
    # r6: a refused long component taken as a link; R4-RF-1: the record's member syntax miscounted.
    ('long-component-taken-as-link', VCS, [('                Err(error) if name_refused(&error) => return unsupported("ref-name"),\n', '')], 'vcs'),
    ('record-member-miscounted', VCS, [('                    .map(|m| 91 + payload_len(m.path))\n', '                    .map(|m| 90 + payload_len(m.path))\n')], 'vcs'),
    # LD-C1B-5: a member reached without its marker checks.
    ('member-markers-unchecked', GT, [('                (true, false, false) | (false, false, false) => {\n                    return Ok(Err(MemberRefusal::VcsUnsupported("vcs-other")));\n                }\n', '')], 'vcs'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1b1-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # Main may have moved while this runner waited for the lock; once the lock is held no integration can move it. The
    # worktree follows main only if nothing main changed is a candidate path (so no candidate byte is touched by the
    # move); then the preparation (prepare_c1b1.py: the closure re-pin and every generated output, by the tools' own
    # --write modes) is re-run on main inside the lane, and must pass. Anything else refuses.
    assert git(P, 'status', '--porcelain') == ''
    started, main = git(W, 'rev-parse', 'HEAD'), git(P, 'rev-parse', 'HEAD')
    assert subprocess.run(['/usr/bin/git', 'merge-base', '--is-ancestor', started, main], cwd=P, env=E).returncode == 0
    candidate = set(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
    moved = sorted(git(P, 'diff', '--name-only', started, main).splitlines()) if started != main else []
    assert not candidate & set(moved), ('main changed a candidate path while waiting: rebase by hand', sorted(candidate & set(moved)))
    if moved:
        git(W, 'checkout', '-q', '--detach', main)
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD')
    with (B / 'preparation.log').open('wb') as log:
        prepared = subprocess.run([PY, '-I', '-B', str(EV / 'prepare_c1b1.py'), str(B / 'preparation.json')], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    (B / 'worktree-base.json').write_text(json.dumps(dict(productBase=git(W, 'rev-parse', 'HEAD'), preparedOn=started, mainMovedWhileWaiting=moved), indent=2) + '\n')
    if prepared != 0:
        (B / 'checks.json').write_text(json.dumps(dict(rows=[dict(name='preparation', exitCode=prepared)], allPassed=False, standing='UNREVIEWED C1b-1 r1 CANDIDATE CHECKS: preparation failed'), indent=2) + '\n')
        raise SystemExit(1)
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        extra = ['--', '--test-threads=1'] if pkg in SERIAL else []
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg, *extra], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    rows, comparisons = [dict(name='preparation', exitCode=prepared, niceness=10)], {}
    # Preflight: the candidate's test targets build, so a compile error ends the lane before the base suites.
    with (B / 'candidate-build.log').open('wb') as log:
        built = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '--no-run', '-p', 'opensip-host', '-p', 'opensip-security'],
                               cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    rows.append(dict(name='candidate-build', exitCode=built, niceness=10)); print('candidate-build exit', built, flush=True)
    if built != 0:
        (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=False, standing='UNREVIEWED C1b-1 r1 CANDIDATE CHECKS: preflight failed'), indent=2) + '\n')
        raise SystemExit(1)
    for pkg in NEW_TESTS:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        # A test failing on one side only is rerun alone, three times on each side: it is flaky (and not a
        # difference) only if every isolated run passes on both.
        differing = sorted(set(base['failed']) ^ set(cand['failed']))
        flaky = []
        for name in differing:
            runs = []
            for root in (P, W):
                for _ in range(3):
                    r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', pkg, '--lib', '--', '--exact', name, '--test-threads=1'], cwd=root, env=E, capture_output=True)
                    runs.append(r.returncode == 0 and b'1 passed' in r.stdout)
            (B / ('isolated-' + name.replace(':', '_') + '.json')).write_text(json.dumps(dict(test=name, runs=runs), indent=2) + '\n')
            if all(runs):
                flaky.append(name)
        comparison = dict(base=base, candidate=cand, differing=differing, flakyInIsolation=flaky, equalFailureSets=set(base['failed']) - set(flaky) == set(cand['failed']) - set(flaky), candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'] + len([f for f in flaky if f in cand['failed']]) - len([f for f in flaky if f in base['failed']]))
        comparisons[pkg] = comparison
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
        rows.append(dict(name=f'{pkg}-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] == NEW_TESTS[pkg] else 1, niceness=10))
    (B / 'test-comparison.json').write_text(json.dumps(comparisons, indent=2) + '\n')
    edited = sorted(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
    (B / 'edited.json').write_text(json.dumps(dict(paths=edited), indent=2) + '\n')
    def fmt_clean(raw):
        r = subprocess.run([R + 'rustfmt', '--edition', '2024', '--emit', 'stdout'], input=raw, env=E, capture_output=True)
        return r.returncode == 0 and r.stdout == raw
    fmt_rows = []
    for x in [x for x in edited if x.endswith('.rs')]:
        base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + x], cwd=W, env=E, capture_output=True)
        fmt_rows.append(dict(path=x, baseClean=None if base_raw.returncode else fmt_clean(base_raw.stdout), candidateClean=fmt_clean((W / x).read_bytes())))
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    rows.append(dict(name='rustfmt-edited', exitCode=0 if all(r['candidateClean'] for r in fmt_rows if r['baseClean'] is not False) else 1, niceness=10))
    # The base-dirty files: each candidate is its base followed by an appended block.
    appended = []
    for x in APPEND_ONLY:
        base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + x], cwd=W, env=E, capture_output=True, check=True).stdout
        cand_raw = (W / x).read_bytes()
        appended.append(dict(path=x, baseBytes=len(base_raw), appendedBytes=len(cand_raw) - len(base_raw), appendOnly=cand_raw.startswith(base_raw) and len(cand_raw) > len(base_raw),
                             baseRustfmtClean=fmt_clean(base_raw)))
    (B / 'append-only.json').write_text(json.dumps(appended, indent=2) + '\n')
    rows.append(dict(name='base-dirty-append-only', exitCode=0 if all(r['appendOnly'] for r in appended) else 1, niceness=10))
    # The vector moves: the walk, opener and session predictions are unchanged (only the pins move); the VCS vectors are new.
    base_vectors = json.loads(git(W, 'show', 'HEAD:' + VECTORS)); cand_vectors = json.loads((W / VECTORS).read_bytes())
    base_session = json.loads(git(W, 'show', 'HEAD:' + SESSION_VECTORS)); cand_session = json.loads((W / SESSION_VECTORS).read_bytes())
    vcs_vectors = json.loads((W / VCS_VECTORS).read_bytes())
    unchanged = {k: base_vectors[k] == cand_vectors[k] for k in ('cases', 'openers', 'prunedOpeners')}
    vector_ok = all(unchanged.values()) and base_session['cases'] == cand_session['cases'] and len(vcs_vectors['cases']) == 9 and len(vcs_vectors['reach']) == 2
    (B / 'vector-moves.json').write_text(json.dumps(dict(walkPredictionsUnchanged=unchanged, sessionPredictionsUnchanged=base_session['cases'] == cand_session['cases'],
                                                        pinsMoved=base_vectors['pins'] != cand_vectors['pins'], vcsCases=len(vcs_vectors['cases']), vcsRecordMax=vcs_vectors['recordMax'],
                                                        passed=vector_ok), indent=2) + '\n')
    rows.append(dict(name='vector-moves', exitCode=0 if vector_ok else 1, niceness=10))
    # LD-C1B-7 (r3): the stale state, recorded separately and cumulatively, from public receipt fields only.
    with (B / 'receipt-specific.log').open('wb') as log:
        code = subprocess.run([PY, '-I', '-B', str(EV / 'receipt_specific_record_c1b1.py'), str(W), str(P), str(A), str(B / 'receipt-specific.json')],
                              cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    rows.append(dict(name='receipt-specific-record', exitCode=code, niceness=10))
    closure_check = ("import re,sys,subprocess,json;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);expected=" + json.dumps(sorted(EXPECTED_CLOSURE_CHANGES)) + ";print(len(closure),'closure files; hit',hit,'expected',expected);sys.exit(0 if hit==expected and len(closure)>=10 else 1)")
    cache = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2]
    derivation = B / 'vcs-derivation.json'
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             *[('focused-' + k + '-tests', v) for k, v in FOCUSED.items()],
             ('snapshot-ledger-model', [PY, '-I', '-B', MODEL, '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('vcs-derivation', [PY, '-I', '-B', '-c', 'import subprocess,sys;out=subprocess.check_output(sys.argv[1:]);open(%r,"wb").write(out)' % str(derivation),
                                 PY, '-I', '-B', str(EV / 'vcs_derivation_c1b1.py'), str(W), str(A)]),
             ('discovery-census', [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', *cache]),
             ('discovery-workspace-ledger', [PY, '-I', '-B', 'tools/security/discovery_workspace_ledger.py', '--check', *cache]),
             ('snapshot-ledger-census', [PY, '-I', '-B', 'tools/security/snapshot_ledger_census.py', '--check', *cache]),
             ('discovery-fw01', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('census-closure-changed-as-expected', [PY, '-I', '-B', '-c', closure_check]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, ys, edits, focus in MUTATIONS:
        path = W / ys; original = path.read_bytes(); text = original.decode()
        for before, after in edits:
            assert text.count(before) == 1, (name, before[:60])
            text = text.replace(before, after)
        path.write_text(text)
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(FOCUSED[focus], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and 'could not compile' not in out and 'test result: FAILED' in out
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=ys, focus=focus, caught=caught, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C1b-1 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
