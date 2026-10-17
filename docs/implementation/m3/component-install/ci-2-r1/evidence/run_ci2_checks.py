"""CI-2 + CI-3 candidate checks (law CI r5 items 4 to 7 with amendment CI-A2 proposed; component installation plan r3,
sub-units CI-2 and CI-3 as one package): the lifecycle, platform (serially) and security suites on the base checkout and
the candidate (--no-fail-fast; equal failure sets after isolated reruns, and exactly the new passing tests), rustfmt on
the edited base-clean files (security's lib.rs is base-dirty and append-only), warning-denied all-targets Clippy on the
three crates, a workspace all-targets check, the fixture features' debug checks, release builds with the fixture store
and TestComponent absent from them (code symbols, with positive controls), the package edges under the O1-a policy,
the environment exceptions, the operability source census with its mint audit, the census-closure check, CI-PT-4 (both
receipts' bound inputs untouched and the receipt files byte-equal to base), verify_design, and mutations, each of which
must fail its crate's focused tests. One lane hold, nice 10, private TMPDIR; the worktree follows main under the lock
when main changed no candidate path. (Adapted from run_ci1_checks.py.)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-ci2'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = Path(__file__).resolve().parent
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
LC = 'crates/lifecycle/src/installation.rs'; RT = 'crates/lifecycle/src/retained_tree.rs'; CT = 'crates/platform/src/component_tree.rs'
def tests_in(*files): return sum((W / f).read_text().count('#[test]\n') for f in files)
NEW_TESTS = {'opensip-lifecycle': tests_in('crates/lifecycle/src/installation_tests.rs', 'crates/lifecycle/src/retained_tree_tests.rs'),
             'opensip-platform': tests_in('crates/platform/src/component_tree_tests.rs'), 'opensip-security': 0}
SERIAL = {'opensip-platform'}
FOCUSED = {'lifecycle': [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-lifecycle', '--lib'],
           'platform': [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--lib', '--', 'component_tree::', '--test-threads=1']}
SORT_SECOND = '    work.charge(buffer)?;\n    let mut to = Vec::with_capacity(n);\n'
RESERVED = ('    let reserved = work.effect(WorkCost::default(), bound, |post| {\n        post.prepaid(bound, |work| {\n'
            '            transaction(store, &evidence, candidate, archive, length, work)\n        })\n    });\n')
LOST = ('            Err(WorkFailure::Operation(failure)) => {\n                return Err(WorkFailure::Operation(InstallFailure::Io(\n'
        '                    InstallIo::Publication(failure.class()),\n                )));\n            }\n')
V1_ORDER = ('    let order = charged_sort::<InstallFailure>(tree.n, work, |a, b| {\n'
            '        component_cmp(tree.row(a).path, tree.row(b).path).is_lt()\n    })?;\n')
MUTATIONS = [
    # (name, focus, [(file, before, after), ...]): each weakens one CI-2/CI-3 rule (plan r3 section 5, and the code's own).
    ('scratch-buffer-uncharged', 'lifecycle', [(LC, SORT_SECOND, '    let mut to = Vec::with_capacity(n);\n')]),
    ('comparison-charged-after', 'lifecycle', [(LC, '                work.charge(COMPARISON)?;\n                if less(from[j], from[i]) {\n',
                                                '                let take = less(from[j], from[i]);\n                work.charge(COMPARISON)?;\n                if take {\n')]),
    ('member-order-rows-left-out', 'lifecycle', [(LC, '        .add_times(index_buffer_cost(n)?, 2)?\n        .add_times(COMPARISON, sorts)?\n        // The Blobs',
                                                  '        // The Blobs')]),
    ('install-association-skipped', 'lifecycle', [(LC, '    associate(tree, &member_order, candidate, work)?;\n', '')]),
    ('bound-checked-after-acquisition', 'lifecycle', [(LC, RESERVED, '    let reserved = work.scope(|work| transaction(store, &evidence, candidate, archive, length, work));\n')]),
    ('rename-charged-twice', 'lifecycle', [(LC, '    work.effect(WorkCost::default(), postchecks, |post| {\n', '    work.effect(postchecks, postchecks, |post| {\n')]),
    ('lost-race-as-success', 'lifecycle', [(LC, LOST, '            Err(WorkFailure::Operation(_)) => return Ok(()),\n')]),
    ('v2-record-skipped', 'lifecycle', [(LC, '    check_record(stage.directory(), &bytes, &mut buffer, work).map_err(walk_failure)?;\n', '    drop(bytes);\n')]),
    ('v2-pin-skipped', 'lifecycle', [(LC, '    check_pin(stage.directory(), work).map_err(walk_failure)?;\n', '')]),
    ('extra-entry-ignored', 'lifecycle', [(LC, '        Ok(_) if names == children => Ok(()),\n', '        Ok(_) => Ok(()),\n'),
                                          (LC, 'visit_entry_names::<()>(children + 2, 1024 * (children + 2), |name| {', 'visit_entry_names::<()>(children + 999, 1024 * (children + 999), |name| {')]),
    ('directory-reentry-byte-order', 'lifecycle', [(LC, V1_ORDER, '    let order = charged_sort::<InstallFailure>(tree.n, work, |a, b| {\n        byte_less(tree.row(a).path, tree.row(b).path)\n    })?;\n')]),
    ('archive-digest-unchecked', 'lifecycle', [(LC, '                    if &hex64(&sha256)[..] != archive_digest.as_bytes() {\n',
                                                '                    if false && &hex64(&sha256)[..] != archive_digest.as_bytes() {\n')]),
    ('chunk-written-twice', 'lifecycle', [(LC, '                        chunk_write(&w.file, w.written, &buffer[from..from + chunk], work)?;\n',
                                           '                        chunk_write(&w.file, w.written, &buffer[from..from + chunk], work)?;\n                        chunk_write(&w.file, w.written, &buffer[from..from + chunk], work)?;\n')]),
    ('readdir-in-step-4', 'lifecycle', [(LC, '        ct::set_mode(level.directory.as_file(), 0o500, work)\n',
                                         '        check_listing(&level, work).map_err(walk_failure)?;\n        ct::set_mode(level.directory.as_file(), 0o500, work)\n')]),
    ('archive-read-envelope-unchecked', 'lifecycle', [(LC, '        if made == attempts {\n            return Err(admission(AdmissionRefusal::ArchiveReadAttempts));\n',
                                                       '        if false && made == attempts {\n            return Err(admission(AdmissionRefusal::ArchiveReadAttempts));\n')]),
    ('descent-uncharged', 'lifecycle', [(LC, '    work.charge(descend_cost(name.len()))?;\n', '')]),
    ('access-mode-retry-path', 'lifecycle', [(LC, 'const FINALIZE_ACCESS: Access = Access::ReadOnly;\n',
                                              'const FINALIZE_ACCESS: Access = Access::ReadOnly;\n#[allow(dead_code)]\nconst RETRY_ACCESS: Access = Access::ReadWrite;\n')]),
    ('fixture-store-unpredicated', 'lifecycle', [(LC, '    #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]\n    pub fn fixture(', '    pub fn fixture(')]),
    ('pin-file-recreated', 'lifecycle', [(RT, '        Err(WorkFailure::Operation(TreeOpenError::Absent | TreeOpenError::NotRegular)) => {\n            return Err(TreeReadFailure::Pin);\n',
                                          '        Err(WorkFailure::Operation(TreeOpenError::Absent | TreeOpenError::NotRegular)) => {\n            drop(generation.create_exclusive_regular(inst::PIN));\n            return Err(TreeReadFailure::Pin);\n')]),
    ('record-trusted', 'lifecycle', [(RT, '    inst::check_record(&generation, &expected, &mut buffer, work).map_err(TreeReadFailure::of)?;\n', '')]),
    ('association-skipped', 'lifecycle', [(RT, '    for blob in candidate.blobs() {\n', '    for blob in candidate.blobs().take(0) {\n'),
                                          (RT, '    if blobs != tree.files {\n', '    if false && blobs != tree.files {\n')]),
    ('sink-committed-unverified', 'lifecycle', [(RT, '        if result.is_err() {\n            sink.finish(false);\n', '        if result.is_err() {\n            sink.finish(true);\n')]),
    ('generation-custody-skipped', 'lifecycle', [(RT, '    match store.custody::<TreeFault>(generation.as_file(), work) {\n',
                                                  '    match Ok::<Result<(), CustodyDirectoryRefusal>, WorkFailure<TreeFault>>(Ok(())) {\n')]),
    ('symlink-followed', 'platform', [(CT, '            libc::AT_SYMLINK_NOFOLLOW,\n', '            0,\n')]),
    ('barrier-skipped', 'platform', [(CT, '    full_flush(file).map_err(WorkFailure::Operation)?;\n', '    drop(full_flush);\n')]),
    ('receipt-by-inode', 'platform', [(CT, '        std::ptr::eq(self.file, file)\n',
                                       '        self.file.metadata().map(|m| std::os::unix::fs::MetadataExt::ino(&m)).ok()\n            == file.metadata().map(|m| std::os::unix::fs::MetadataExt::ino(&m)).ok()\n')]),
    ('pin-unlock-added', 'platform', [(CT, 'impl PinLock {\n',
                                       'impl Drop for PinLock {\n    fn drop(&mut self) {\n        // SAFETY: a mutation control only.\n        unsafe { libc::flock(self.file.file.as_raw_fd(), libc::LOCK_UN) };\n    }\n}\nimpl PinLock {\n')]),
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
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-ci2-check-', dir=D)); T.chmod(0o700)
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
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        extra = ['--', '--test-threads=1'] if pkg in SERIAL else []
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg, *extra], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    rows, comparisons = [], {}
    for pkg in NEW_TESTS:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
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
        comparison = dict(base=base, candidate=cand, differing=differing, flakyInIsolation=flaky, equalFailureSets=set(base['failed']) - set(flaky) == set(cand['failed']) - set(flaky), candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'] + len([f for f in flaky if f in cand['failed']]) - len([f for f in flaky if f in base['failed']]), expectedNewTests=NEW_TESTS[pkg])
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
    controls = []
    for name, focus, edits in MUTATIONS:
        originals = {}
        try:
            for ys, before, after in edits:
                path = W / ys
                originals.setdefault(path, path.read_bytes())
                text = path.read_text()
                assert text.count(before) == 1, name
                path.write_text(text.replace(before, after))
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(FOCUSED[focus], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and 'could not compile' not in out and 'test result: FAILED' in out
        finally:
            for path, original in originals.items():
                path.write_bytes(original)
        assert all(path.read_bytes() == original for path, original in originals.items())
        controls.append(dict(kind='mutation', name=name, files=sorted({e[0] for e in edits}), caught=caught, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'), rebasedBeforeLane=rebased,
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], censusModesRun=False,
        censusModesNote='No census --check/--write mode is run: they need the T2 cache, which this unit may not read. CI-PT-4 is receipt-inputs-unchanged.',
        standing='UNREVIEWED CI-2+CI-3 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
