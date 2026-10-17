"""C1b-2 r1 candidate checks (M3-C r8 item 4 with item 6's step 4; C1b plan r6, sub-unit C1b-2: sealing the VCS
observation). Adapted from C1b-1 r2's run_c1b1_checks.py.

The host and security suites on the base checkout and the candidate (--no-fail-fast; equal failure sets after isolated
reruns, and the new passing tests: host 6); the preparation on main (prepare_c1b2.py: the snapshot census record
regenerated; the model and the discovery census checked unchanged); rustfmt on the new and base-clean edited files;
warning-denied all-targets Clippy on the two crates; the focused sealing tests; the charge model --check with every
vector unchanged (C1b-2 adds no model term); the charge-site equality with C1b-1's derivation (the sealed record's
maximum is the model's, 1,573,798 bytes, and the charge is cross-checked against C1b-1's priced length); the discovery
census, workspace ledger and snapshot census --checks over the lead-readable cache only; no census closure file changed;
the cumulative receipt-specific record; FW-01; the environment exceptions; the operability source census; verify_design;
and the plan's four C1b-2 mutations with the self-review's two, each of which must fail its focused tests. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1b2'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = Path(__file__).resolve().parent
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
SEAL = 'crates/host/src/snapshot_seal.rs'
MODEL = 'tools/security/snapshot_ledger_model.py'
VECTORS = 'crates/security/src/snapshot_ledger_vectors.json'; SESSION_VECTORS = 'crates/host/src/snapshot_session_vectors.json'
VCS_VECTORS = 'crates/security/src/snapshot_vcs_vectors.json'
# The new passing tests: host 7 (snapshot_seal_tests.rs; the member test is replaced, not added); security none.
NEW_TESTS = {'opensip-host': 7, 'opensip-security': 0}
SERIAL = set()
EXPECTED_CLOSURE_CHANGES = []
APPEND_ONLY = []
T2 = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
CARGO = [R + 'cargo', 'test', '--locked', '--offline']
FOCUSED = {'seal': CARGO + ['-p', 'opensip-host', '--lib', '--', 'snapshot_seal']}
MUTATIONS = [
    # (name, file, [(before, after)], focus): C1b plan r6 section 5's C1b-2 mutations; each must fail the focused tests.
    ('dirty-computed-false', SEAL, [('const GIT_TAIL: &[u8] =\n    br#"","dirty":true,', 'const GIT_TAIL: &[u8] =\n    br#"","dirty":false,')], 'seal'),
    ('schema-3-for-zero-members', SEAL, [("        VcsObservation::None | VcsObservation::Unobserved => VcsRecord::None,\n",
                                          "        VcsObservation::None | VcsObservation::Unobserved if inputs.boundaries.is_some() => {\n"
                                          "            VcsRecord::Members(&[])\n        }\n"
                                          "        VcsObservation::None | VcsObservation::Unobserved => VcsRecord::None,\n")], 'seal'),
    # Discovery's record admission refuses members out of order, so the observable mutation writes them reversed.
    ('members-out-of-path-order', SEAL, [('            for (index, member) in members.iter().enumerate() {\n',
                                          '            for (index, member) in members.iter().rev().enumerate() {\n')], 'seal'),
    ('inventory-digest-recomputed', SEAL, [('    out.extend_from_slice(&hex_digits(inventory_digest));\n', '    out.extend_from_slice(&hex_digits(&raw_sha256(&out)));\n')], 'seal'),
    # The self-review (PRE-SUBMISSION-CHECKLIST items 1 and 2): the record's buffer allocated before its charge, and the
    # charge taken at the 1,573,798-byte bound instead of the record's exact length.
    ('record-allocated-before-charge', SEAL, [('    work.charge::<SealError>(owned_record(len))?;\n    let mut out = Vec::with_capacity(len);\n',
                                               '    let mut out = Vec::with_capacity(len);\n    work.charge::<SealError>(owned_record(len))?;\n')], 'seal'),
    ('record-precharged-at-bound', SEAL, [('    work.charge::<SealError>(owned_record(len))?;\n', '    work.charge::<SealError>(owned_record(1_573_798))?;\n')], 'seal'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1b2-check-', dir=D)); T.chmod(0o700)
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
        prepared = subprocess.run([PY, '-I', '-B', str(EV / 'prepare_c1b2.py'), str(B / 'preparation.json')], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    (B / 'worktree-base.json').write_text(json.dumps(dict(productBase=git(W, 'rev-parse', 'HEAD'), preparedOn=started, mainMovedWhileWaiting=moved), indent=2) + '\n')
    if prepared != 0:
        (B / 'checks.json').write_text(json.dumps(dict(rows=[dict(name='preparation', exitCode=prepared)], allPassed=False, standing='UNREVIEWED C1b-2 r1 CANDIDATE CHECKS: preparation failed'), indent=2) + '\n')
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
        (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=False, standing='UNREVIEWED C1b-2 r1 CANDIDATE CHECKS: preflight failed'), indent=2) + '\n')
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
    # No model term (LD-C1B-6): every vector file is unchanged, pins included.
    # Byte equality with HEAD, by git itself (the stripped `git show` text is not the file's bytes; void attempt 1).
    unchanged = {x: subprocess.run(['/usr/bin/git', 'diff', '--quiet', 'HEAD', '--', x], cwd=W, env=E).returncode == 0 for x in (VECTORS, SESSION_VECTORS, VCS_VECTORS)}
    (B / 'vector-moves.json').write_text(json.dumps(dict(unchanged=unchanged, passed=all(unchanged.values())), indent=2) + '\n')
    rows.append(dict(name='vector-moves', exitCode=0 if all(unchanged.values()) else 1, niceness=10))
    # The charge-site equality (C1b plan r6, the C1b-2 row): the census prices the record at the model's maximum,
    # which C1b-1's derivation priced (its recordMax), and sealing's charge is cross-checked against C1b-1's
    # `encoded_len` before it is made.
    equality = ("import importlib.util,json,sys,re,pathlib;W=pathlib.Path(sys.argv[1]);D=json.load(open(sys.argv[2]));"
                "s=importlib.util.spec_from_file_location('m',W/'tools/security/snapshot_ledger_model.py');m=importlib.util.module_from_spec(s);sys.modules['m']=m;s.loader.exec_module(m);"
                "t=importlib.util.spec_from_file_location('d',W/'tools/security/discovery_census.py');d=importlib.util.module_from_spec(t);sys.modules['discovery_census']=d;t.loader.exec_module(d);"
                "c=m.vcs_costs(W,m.snapshot_costs(W,d)[0]);mx=m.vcs_record_max(c);seal=(W/'crates/host/src/snapshot_seal.rs').read_text();"
                "cen=(W/'tools/security/snapshot_ledger_census.py').read_text();"
                "ok=mx==D['recordMax']==1573798 and 'if record_len != priced_len {' in seal and 'vcs_record = slm.vcs_record_max(slm.vcs_costs(product, c))' in cen;"
                "print(json.dumps(dict(modelRecordMax=mx,derivationRecordMax=D['recordMax'],crossChecked='if record_len != priced_len {' in seal,censusPricesModelMax=ok)));sys.exit(0 if ok else 1)")
    with (B / 'charge-site-equality.log').open('wb') as log:
        code = subprocess.run([PY, '-I', '-B', '-c', equality, str(W), str(A / 'docs/implementation/m3/snapshot-plan-c/c1b-1-r2/evidence/c1b1-checks-r2/vcs-derivation.json')],
                              cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    rows.append(dict(name='charge-site-equality', exitCode=code, niceness=10))
    # LD-C1B-7 (r3): the stale state, recorded separately and cumulatively, from public receipt fields only.
    with (B / 'receipt-specific.log').open('wb') as log:
        code = subprocess.run([PY, '-I', '-B', str(EV / 'receipt_specific_record_c1b2.py'), str(W), str(P), str(A), str(B / 'receipt-specific.json')],
                              cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    rows.append(dict(name='receipt-specific-record', exitCode=code, niceness=10))
    closure_check = ("import re,sys,subprocess,json;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);expected=" + json.dumps(sorted(EXPECTED_CLOSURE_CHANGES)) + ";print(len(closure),'closure files; hit',hit,'expected',expected);sys.exit(0 if hit==expected and len(closure)>=10 else 1)")
    cache = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2]
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             *[('focused-' + k + '-tests', v) for k, v in FOCUSED.items()],
             ('snapshot-ledger-model', [PY, '-I', '-B', MODEL, '--check', '--architecture', str(A), '--packages-root', str(P)]),
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
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C1b-2 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
