"""CI-3L candidate checks (law CI r5 with amendment CI-A3 r4, accepted; component installation plan r3, unit CI-3L): the
lifecycle, platform (serially) and security suites on the base checkout and the candidate (--no-fail-fast; equal failure
sets after isolated reruns, and exactly the new passing tests), the lifetime doctest (compile_fail E0505 and its passing
twin), rustfmt on the edited files, warning-denied all-targets Clippy on the three crates, a workspace all-targets check,
the fixture features' debug checks, release builds with the fixture store and TestComponent absent from them (code
symbols, with positive controls), the package edges under the O1-a policy, the environment exceptions, the operability
source census with its mint audit, the census-closure check, CI-PT-4 (both receipts' bound inputs untouched and the
receipt files byte-equal to base), verify_design, and mutations, each of which must fail its crate's focused tests. One
lane hold, nice 10, private TMPDIR; the worktree follows main under the lock when main changed no candidate path.
(Adapted from CI-2 r2's run_ci2_checks.py.)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys, hashlib
W = Path('/Users/sb/code/opensip-ai/opensip-ci3l-takeover'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = Path(__file__).resolve().parent
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
LC = 'crates/lifecycle/src/installation.rs'; RT = 'crates/lifecycle/src/retained_tree.rs'; CT = 'crates/platform/src/component_tree.rs'
def tests_in(*files):
    base = lambda f: subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + f], cwd=W, capture_output=True).stdout.decode()
    return sum((W / f).read_text().count('#[test]\n') - base(f).count('#[test]\n') for f in files)
NEW_TESTS = {'opensip-lifecycle': tests_in('crates/lifecycle/src/installation_tests.rs', 'crates/lifecycle/src/retained_tree_tests.rs'),
             'opensip-platform': tests_in('crates/platform/src/component_tree_tests.rs'), 'opensip-security': 0}
SERIAL = {'opensip-platform'}
FOCUSED = {'lifecycle': [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-lifecycle', '--lib'],
           'platform': [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--lib', '--', 'component_tree::', '--test-threads=1']}
LSTAT_CHARGED = ('    work.charge(status_read_cost())?;\n    // SAFETY: an all-zero `stat` is a valid output buffer.\n    let mut st: libc::stat = unsafe { std::mem::zeroed() };\n'
                 '    // SAFETY: one NUL-terminated spelling the caller borrows, and a valid out\n    // pointer.\n    if unsafe { libc::lstat(path.as_ptr(), &mut st) } != 0 {\n')
LSTAT_AFTER = ('    // SAFETY: an all-zero `stat` is a valid output buffer.\n    let mut st: libc::stat = unsafe { std::mem::zeroed() };\n'
               '    // SAFETY: one NUL-terminated spelling the caller borrows, and a valid out\n    // pointer.\n    let r = unsafe { libc::lstat(path.as_ptr(), &mut st) };\n    work.charge(status_read_cost())?;\n    if r != 0 {\n')
HOP = ('                let (parent, _) = split(row.path);\n                work.charge(heap(length)).map_err(budget)?;\n'
       '                let mut joined = String::with_capacity(length);\n')
BIND = ('        let observed = match observe_path(spelling, work) {\n')
MUTATIONS = [
    # (name, focus, [(file, before, after), ...]): each weakens one CI-A3 rule.
    ('kind-check-uncharged', 'lifecycle', [(RT, '            work.charge(inst::COMPARISON).map_err(budget)?;\n            let count = if request.wants_file() {\n',
                                            '            let count = if request.wants_file() {\n')]),
    ('kind-check-skipped', 'lifecycle', [(RT, '            if count == 0 {\n                return Err(TreeReadFailure::Association);\n            }\n            Some(resolve(',
                                          '            if false && count == 0 {\n                return Err(TreeReadFailure::Association);\n            }\n            Some(resolve(')]),
    ('lookup-bound-loosened', 'lifecycle', [(RT, '                if lookups > tree.links {\n', '                if lookups > tree.links.saturating_add(1) {\n')]),
    ('hop-uncharged', 'lifecycle', [(RT, HOP, HOP.replace('                work.charge(heap(length)).map_err(budget)?;\n', ''))]),
    ('hop-allocated-before-charge', 'lifecycle', [(RT, HOP, '                let (parent, _) = split(row.path);\n                let mut joined = String::with_capacity(length);\n'
                                                            '                work.charge(heap(length)).map_err(budget)?;\n')]),
    ('reads-precharged', 'lifecycle', [(RT, '                read_verified(&file, index, length, sha256, &mut self.buffer, work, |_| {})\n',
                                        '                work.charge(inst::times(READ, envelope(length) as usize).unwrap())\n                    .map_err(budget)?;\n                read_verified(&file, index, length, sha256, &mut self.buffer, work, |_| {})\n')]),
    ('store-path-charged-per-launch', 'lifecycle', [(RT, '        work.charge(heap(length)).map_err(budget)?;\n        let mut bytes = Vec::with_capacity(length);\n',
                                                     '        work.charge(inst::store_path_cost(store.len())).map_err(budget)?;\n        work.charge(heap(length)).map_err(budget)?;\n        let mut bytes = Vec::with_capacity(length);\n')]),
    ('store-path-uncharged-at-open', 'lifecycle', [(LC, '    work.charge(store_path_cost(length))?;\n', '')]),
    ('result-charged-before-binding', 'lifecycle', [(RT, BIND, '        work.charge(launch_member_cost()).map_err(budget)?;\n' + BIND),
                                                     (RT, '        work.charge(launch_member_cost()).map_err(budget)?;\n        Ok(LaunchMember {\n', '        Ok(LaunchMember {\n')]),
    ('binding-identity-unchecked', 'lifecycle', [(RT, '        if observed.kind != kind || (observed.device, observed.inode) != (device, inode) {\n',
                                                  '        if observed.kind != kind {\n')]),
    ('lstat-io-as-binding', 'lifecycle', [(RT, '            Err(WorkFailure::Operation(PathStatusError::Io(error))) => {\n                return Err(TreeReadFailure::Io {\n                    call: "lstat",\n                    error,\n                });\n            }\n',
                                           '            Err(WorkFailure::Operation(PathStatusError::Io(_))) => {\n                return Err(TreeReadFailure::Binding);\n            }\n')]),
    ('absent-path-as-io', 'lifecycle', [(RT, '                PathStatusError::Absent | PathStatusError::NotDirectory,\n            )) => {\n                return Err(TreeReadFailure::Binding);\n',
                                         '                PathStatusError::Absent | PathStatusError::NotDirectory,\n            )) => {\n                return Err(TreeReadFailure::Io {\n                    call: "lstat",\n                    error: io::Error::other("absent"),\n                });\n')]),
    ('directory-mode-unchecked', 'lifecycle', [(RT, '                if status.mode != mode {\n', '                if false && status.mode != mode {\n')]),
    ('launch-latch-skipped', 'lifecycle', [(RT, '        if let Some(latched) = self.latched {\n            return Err(latched.failure());\n',
                                            '        if let Some(latched) = self.latched.filter(|_| false) {\n            return Err(latched.failure());\n')]),
    ('budget-not-latched', 'lifecycle', [(RT, '        if let Err(failure) = &result {\n            self.latched = Some(Latched::of(failure));\n        }\n        result\n',
                                          '        if let Err(failure) = &result\n            && !matches!(failure, TreeReadFailure::Budget(_))\n        {\n            self.latched = Some(Latched::of(failure));\n        }\n        result\n')]),
    ('pre-bound-hops-dropped', 'lifecycle', [(RT, '        .add_times(heap(q), s)?;\n', '        ;\n')]),
    ('lstat-before-charge', 'platform', [(CT, LSTAT_CHARGED, LSTAT_AFTER)]),
    ('lstat-follows-final', 'platform', [(CT, '    if unsafe { libc::lstat(path.as_ptr(), &mut st) } != 0 {\n', '    if unsafe { libc::stat(path.as_ptr(), &mut st) } != 0 {\n')]),
    ('directory-identity-uncharged', 'platform', [(CT, '    work.charge(status_read_cost())?;\n    let st = fstat(directory.as_file()).map_err(WorkFailure::Operation)?;\n',
                                                   '    let st = fstat(directory.as_file()).map_err(WorkFailure::Operation)?;\n')]),
]
FEATURES = [('security-scenario-fixtures-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'scenario-fixtures']),
            ('security-crash-matrix-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'crash-matrix']),
            ('lifecycle-scenario-fixtures-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-lifecycle', '--all-targets', '--features', 'scenario-fixtures']),
            ('lifecycle-crash-matrix-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-lifecycle', '--all-targets', '--features', 'crash-matrix'])]
PACKAGE_EDGES = ("import json,subprocess,sys;R,PY,A,W=sys.argv[1:5];m=subprocess.run([R+'cargo','metadata','--format-version','1','--offline','--locked'],"
                 "capture_output=True,check=True,cwd=W).stdout;open(sys.argv[5],'wb').write(m);"
                 "r=subprocess.run([PY,'-I','-B','tools/check_package_edges.py','--repository',W,'--metadata',sys.argv[5],'--inventory',"
                 "A+'/'+json.load(open(W+'/design-lock.json'))['inventorySuccessors'][-1]['candidate']['path'],'--lane','host','--package-policy',"
                 "A+'/docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json','--architecture',A,'--lock','design-lock.json'],cwd=W,capture_output=True);"
                 "sys.stdout.write(r.stdout.decode()+r.stderr.decode());j=json.loads(r.stdout);"
                 "e=sorted(set(x['to'] for x in j['resolvedInternalEdges'] if x['from']=='opensip-lifecycle'));"
                 "print(e);sys.exit(0 if j['passed'] and e==['opensip-identity','opensip-platform','opensip-security'] else 1)")
def symbols_check(log, crate, symbol, present):
    # The exact rlib the named build produced (its JSON artifact messages), not the newest by time: several builds
    # with different features leave rlibs side by side.
    return ("import json,subprocess,sys;libs=[f for l in open(" + repr(log) + ") if l.startswith('{') for m in [json.loads(l)] "
            "if m.get('reason')=='compiler-artifact' for f in m.get('filenames',[]) if f.endswith('.rlib') and f.rsplit('/',1)[1].removesuffix('.rlib').split('-')[0]=='lib" + crate + "'];"
            "assert len(set(libs))==1,libs;syms=subprocess.run(['/usr/bin/nm','-a',libs[0]],capture_output=True).stdout.decode(errors='replace');"
            "hit=" + repr(symbol) + " in syms;print(libs[0]," + repr(symbol) + ",hit);sys.exit(0 if hit is " + str(present) + " else 1)")
while not owned and os.environ.get("OPENSIP_LEAD_HOLDS_LANE_LOCK") != "1":
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-ci3l-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # Main may move while the lane waits: the worktree follows it once the lock is held, only when main descends from
    # the worktree's base and changed none of the candidate's paths since.
    assert git(P, 'status', '--porcelain') == ''
    main, mine = git(P, 'rev-parse', 'HEAD'), git(W, 'rev-parse', 'HEAD')
    rebased = None
    if main != mine:
        candidate = set(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
        assert subprocess.run(['/usr/bin/git', 'merge-base', '--is-ancestor', mine, main], cwd=P, env=E).returncode == 0
        assert not set(git(P, 'diff', '--name-only', mine, main).splitlines()) & candidate, 'main changed a candidate path'
        git(W, 'checkout', '-q', '--detach', main); rebased = dict(fromBase=mine, toBase=main)
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD')
    # A separate target for each checkout prevents a base image being reused as candidate evidence.
    def env_for(root):
        return dict(E, CARGO_TARGET_DIR=str(B / ('base-target' if root == P else 'candidate-target')))
    E = env_for(W)
    assert not git(W,'ls-files','--others','--exclude-standard'), 'unexpected untracked candidate source'
    source_pins = {p: hashlib.sha256((W / p).read_bytes()).hexdigest() for p in git(W, 'diff', '--name-only').splitlines()}
    assert len(source_pins)==7
    def failures(root, pkg, tag):
        build = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '--no-run', '--message-format=json', '-p', pkg], cwd=root, env=env_for(root), capture_output=True)
        (B / f'{tag}-{pkg}-artifacts.jsonl').write_bytes(build.stdout)
        (B / f'{tag}-{pkg}-build.log').write_bytes(build.stderr)
        assert build.returncode == 0, build.stderr[-5000:]
        library = pkg.replace('-', '_')
        hits = [j for line in build.stdout.splitlines() if line.startswith(b'{') for j in [json.loads(line)] if j.get('reason') == 'compiler-artifact' and j.get('target', {}).get('name') == library and j.get('profile', {}).get('test') and j.get('executable')]
        assert len(hits) == 1 and hits[0]['target']['src_path'] == str(root / ('crates/' + pkg.removeprefix('opensip-') + '/src/lib.rs')), hits
        assert hits[0]['fresh'] is False, 'first test image must be built from this checkout in its fresh target'
        binary = Path(hits[0]['executable'])
        (B / f'{tag}-{pkg}-binary.json').write_text(json.dumps(dict(path=str(binary), sha256=hashlib.sha256(binary.read_bytes()).hexdigest(), source=hits[0]['target']['src_path'], fresh=False), indent=2) + '\n')
        log = B / f'{tag}-{pkg}.log'
        extra = ['--', '--test-threads=1'] if pkg in SERIAL else []
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg, *extra], cwd=root, env=env_for(root), stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        ordinary, _, doc = text.partition('Doc-tests ')
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;', ordinary)
        docs = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;', doc)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _, _ in results), failedCount=sum(int(f) for _, _, f, _ in results), ignored=sum(int(i) for _, _, _, i in results), suites=len(results), doctestPassed=sum(int(p) for _, p, _, _ in docs), doctestFailed=sum(int(f) for _, _, f, _ in docs), doctestIgnored=sum(int(i) for _, _, _, i in docs))
    # Re-establish the independent native ABI constant on this final host/SDK.
    raw=(EV/'sizeof-stat-probe.c').read_bytes();(T/'sizeof-stat-probe.c').write_bytes(raw)
    compile_probe=subprocess.run(['/usr/bin/cc','-isysroot',E['SDKROOT'],str(T/'sizeof-stat-probe.c'),'-o',str(T/'sizeof-stat-probe')],env=E,capture_output=True);assert compile_probe.returncode==0,compile_probe.stderr
    measured=int(subprocess.check_output([str(T/'sizeof-stat-probe')],env=E,text=True).strip())
    expected_abi=int(re.search(r'const REFERENCE_NATIVE_STAT_BYTES: usize = (\d+);',(W/'crates/lifecycle/src/retained_tree_tests.rs').read_text()).group(1));assert measured==expected_abi
    (B/'native-abi-check.json').write_text(json.dumps(dict(measuredStatBytes=measured,referenceStatBytes=expected_abi,matched=True,probeSourceSha256=hashlib.sha256(raw).hexdigest(),sdk=E['SDKROOT']),indent=2)+'\n')
    rows, comparisons = [dict(name='independent-native-abi-check',exitCode=0)], {}
    for pkg in NEW_TESTS:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        differing = sorted(set(base['failed']) ^ set(cand['failed']))
        flaky = []
        for name in differing:
            runs = []
            for root in (P, W):
                for _ in range(3):
                    r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', pkg, '--lib', '--', '--exact', name, '--test-threads=1'], cwd=root, env=env_for(root), capture_output=True)
                    runs.append(r.returncode == 0 and b'1 passed' in r.stdout)
            (B / ('isolated-' + name.replace(':', '_') + '.json')).write_text(json.dumps(dict(test=name, runs=runs), indent=2) + '\n')
            if all(runs):
                flaky.append(name)
        comparison = dict(base=base, candidate=cand, differing=differing, flakyInIsolation=flaky, equalFailureSets=set(base['failed']) - set(flaky) == set(cand['failed']) - set(flaky), candidateSuitesEqualBase=cand['suites'] == base['suites'], doctestConditionsPassed=base['doctestFailed']==cand['doctestFailed']==0 and cand['doctestPassed']-base['doctestPassed']==(2 if pkg=='opensip-lifecycle' else 0), newPassingTests=cand['passed'] - base['passed'] + len([f for f in flaky if f in cand['failed']]) - len([f for f in flaky if f in base['failed']]), expectedNewTests=NEW_TESTS[pkg])
        comparisons[pkg] = comparison
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
        rows.append(dict(name=f'{pkg}-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['doctestConditionsPassed'] and comparison['newPassingTests'] == NEW_TESTS[pkg] else 1, niceness=10))
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
    lib_base = subprocess.run(['/usr/bin/git', 'show', 'HEAD:crates/security/src/lib.rs'], cwd=W, env=E, capture_output=True).stdout
    rows.append(dict(name='security-lib-rs-append-only', exitCode=0 if (W / 'crates/security/src/lib.rs').read_bytes().startswith(lib_base) else 1, niceness=10))
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-lifecycle', '-p', 'opensip-platform', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('workspace-check', [R + 'cargo', 'check', '--locked', '--offline', '--workspace', '--all-targets']),
             *FEATURES,
             ('release-build', [R + 'cargo', 'build', '--locked', '--offline', '--release', '--message-format=json', '-p', 'opensip-lifecycle', '-p', 'opensip-security']),
             ('release-fixture-store-absent', [PY, '-I', '-B', '-c', symbols_check(str(B / 'release-build.log'), 'opensip_lifecycle', '14ComponentStore7fixture', False)]),
             ('release-test-component-absent', [PY, '-I', '-B', '-c', symbols_check(str(B / 'release-build.log'), 'opensip_security', '13TestComponent3new', False)]),
             ('release-installer-present', [PY, '-I', '-B', '-c', symbols_check(str(B / 'release-build.log'), 'opensip_lifecycle', '12installation7install', True)]),
             ('lifetime-doctest', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-lifecycle', '--doc', 'retained_tree::LaunchMember']),
            ('fixture-build', [R + 'cargo', 'build', '--locked', '--offline', '--message-format=json', '-p', 'opensip-lifecycle', '--features', 'scenario-fixtures']),
             ('fixture-store-present', [PY, '-I', '-B', '-c', symbols_check(str(B / 'fixture-build.log'), 'opensip_lifecycle', '14ComponentStore7fixture', True)]),
             ('fixture-test-component-present', [PY, '-I', '-B', '-c', symbols_check(str(B / 'fixture-build.log'), 'opensip_security', '13TestComponent3new', True)]),
             ('package-edges', [PY, '-I', '-B', '-c', PACKAGE_EDGES, R, PY, str(A), str(W), str(B / 'cargo-metadata.json')]),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('census-closure-unchanged', [PY, '-I', '-B', '-c', closure_check]),
             ('receipt-inputs-unchanged', [PY, '-I', '-B', str(EV / 'receipt_inputs.py'), str(W), str(B / 'receipt-inputs.json')]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    # Final mutations ran separately on the identical seven product bytes;
    # no old/superseded r1 outcomes supply final mutation evidence.
    mutation_report=json.loads((EV/'mutations-r2/report.json').read_text())
    assert mutation_report['all24Caught'] and mutation_report['restored'] and len(mutation_report['mutations'])==24
    assert mutation_report['sourcePins']==source_pins and mutation_report['lifecycleRestoredPasses']==16 and mutation_report['platformRestoredPasses']==15
    assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==h for p,h in source_pins.items())
    (B/'controls.json').write_text(json.dumps(mutation_report,indent=2)+'\n')
    rows.append(dict(name='24-final-source-runtime-mutations-and-restored-positives',exitCode=0))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=owned, laneHeldByParentWrapper=os.environ.get("OPENSIP_LEAD_HOLDS_LANE_LOCK")=="1",
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'), rebasedBeforeLane=rebased,
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], censusModesRun=False,
        censusModesNote='No census --check/--write mode is run: they need the T2 cache, which this unit may not read. CI-PT-4 is receipt-inputs-unchanged.',
        standing='COMPLETE CORRECTED CI-3L OWNING LANE; INDEPENDENT UNIT ACCEPTANCE PENDING', sourcePins=source_pins, supersededR1Excluded=True, nativeAbiRechecked=True), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
