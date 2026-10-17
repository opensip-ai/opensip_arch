"""CI-1 candidate checks (law CI r5 item 3; component installation plan r3, sub-unit CI-1: the profile-1 archive
codec): the security suite on the base checkout and the candidate (--no-fail-fast; equal failure sets after isolated
reruns, and exactly the new passing tests), rustfmt on the edited base-clean files (lib.rs is base-dirty and
append-only), warning-denied all-targets Clippy on security, a workspace all-targets check, the security features'
debug checks (the emitter's fixture predicate), a release build of security with the emitter absent from it, the
focused CI-1 tests, PKG-AP's pin by reference, the independent fixed vector, the environment exceptions, the
operability source census with its mint audit, the census-closure check, CI-PT-4 (both receipts' bound inputs
untouched and the receipt files byte-equal to base), verify_design, and mutations, each of which must fail the focused
tests. One lane hold, nice 10, private TMPDIR. (Adapted from run_c2a1_checks.py.)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-ci1'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = Path(__file__).resolve().parent
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
AP = 'crates/security/src/archive_profile.rs'; TESTS = 'crates/security/src/archive_profile_tests.rs'
# The new passing tests: every test in the new test file (security); no other package changes.
NEW_TESTS = {'opensip-security': (W / TESTS).read_text().count('#[test]\nfn ')}
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'archive_profile::']
COMPARE = 'if b != self.expected[offset] {\n'
MUTATIONS = [
    # (name, file, before, after): each weakens one CI-1 rule (plan r3 section 5, and the codec's own); the focused
    # tests must fail.
    ('header-by-decoded-fields', AP, COMPARE, 'if b != self.expected[offset] && self.expected[offset] != 0 {\n'),
    ('typeflag-nul-accepted', AP, COMPARE, 'if b != self.expected[offset] && !(offset == 156 && b == 0) {\n'),
    ('pax-gnu-extension-accepted', AP, COMPARE, "if b != self.expected[offset] && !(offset == 156 && matches!(b, b'x' | b'g' | b'L' | b'K')) {\n"),
    ('noncanonical-uid-accepted', AP, COMPARE, 'if b != self.expected[offset] && !(108..116).contains(&offset) {\n'),
    ('chksum-unchecked', AP, '                if self.chksum_differs {\n', '                if false && self.chksum_differs {\n'),
    ('length-checked-after-reading', AP, '        if observed != self.length {\n', '        if false && observed != self.length {\n'),
    ('pad-unchecked', AP, '                if bytes.iter().any(|&b| b != 0) {\n                    return Err(ArchiveRefusal::Pad { position });\n',
     '                if false && bytes.iter().any(|&b| b != 0) {\n                    return Err(ArchiveRefusal::Pad { position });\n'),
    ('trailer-unchecked', AP, '                if bytes.iter().any(|&b| b != 0) {\n                    return Err(ArchiveRefusal::Trailer);\n',
     '                if false && bytes.iter().any(|&b| b != 0) {\n                    return Err(ArchiveRefusal::Trailer);\n'),
    ('trailing-bytes-accepted', AP, '                if !input.is_empty() {\n                    return Err(ArchiveRefusal::TrailingBytes);\n',
     '                if false && !input.is_empty() {\n                    return Err(ArchiveRefusal::TrailingBytes);\n'),
    ('file-digest-unchecked', AP, '                if file.finish() != sha256 {\n', '                if false && file.finish() != sha256 {\n'),
    ('truncation-accepted', AP, '        if self.phase != Phase::Done {\n', '        if false && self.phase != Phase::Done {\n'),
    ('chksum-nul-mask', AP, "    h[CHKSUM..CHKSUM_END].fill(b' ');\n", '    h[CHKSUM..CHKSUM_END].fill(0);\n'),
    ('name-101-accepted', AP, '            if row.path.len() > MAX_PATH_BYTES {\n', '            if row.path.len() > MAX_PATH_BYTES + 1 {\n'),
    ('link-101-accepted', AP, '                RowKind::Symlink { target } if target.len() > MAX_LINK_TARGET_BYTES => {\n',
     '                RowKind::Symlink { target } if target.len() > MAX_LINK_TARGET_BYTES + 1 => {\n'),
    ('mode-max-refused', AP, '            if row.mode > MAX_MODE {\n', '            if row.mode >= MAX_MODE {\n'),
    ('size-max-refused', AP, '                RowKind::File { length, .. } if length > MAX_SIZE => {\n',
     '                RowKind::File { length, .. } if length >= MAX_SIZE => {\n'),
    ('row-order-trusted', AP, '            if position > 0 && rows.row(position - 1).path.as_bytes() >= row.path.as_bytes() {\n',
     '            if false && position > 0 && rows.row(position - 1).path.as_bytes() >= row.path.as_bytes() {\n'),
    ('length-without-trailer', AP, '        let mut length = TRAILER as u64;\n', '        let mut length = 0u64;\n'),
    ('pad-formula-wrong', AP, '    length.div_ceil(BLOCK as u64) * BLOCK as u64\n', '    (length / BLOCK as u64 + 1) * BLOCK as u64\n'),
    ('digest-skips-trailer', AP, '                self.digest(bytes)?;\n                *input = rest;\n                if seen + take < TRAILER {\n',
     '                *input = rest;\n                if seen + take < TRAILER {\n'),
    ('emitter-blocking-factor', AP, '    out.resize(out.len() + TRAILER, 0);\n', '    out.resize((out.len() + TRAILER).div_ceil(10240) * 10240, 0);\n'),
    ('emitter-unsorted', AP, '    rows.sort_by(|a, b| a.path.as_bytes().cmp(b.path.as_bytes()));\n', '    rows.reverse();\n'),
    ('emitter-digest-unchecked', AP, ' && opensip_identity::raw_sha256(b) == sha256)', ')'),
]
FEATURES = [('scenario-fixtures-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'scenario-fixtures']),
            ('crash-matrix-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'crash-matrix'])]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-ci1-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # Main may move while the lane waits for the lock: the worktree follows it once the lock is held, only when main
    # descends from the worktree's base and changed none of the candidate's paths since.
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
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    rows, comparisons = [], {}
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
        comparison = dict(base=base, candidate=cand, differing=differing, flakyInIsolation=flaky, equalFailureSets=set(base['failed']) - set(flaky) == set(cand['failed']) - set(flaky), candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'] + len([f for f in flaky if f in cand['failed']]) - len([f for f in flaky if f in base['failed']]), expectedNewTests=NEW_TESTS[pkg])
        comparisons[pkg] = comparison
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
        rows.append(dict(name=f'{pkg}-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] == NEW_TESTS[pkg] else 1, niceness=10))
    (B / 'test-comparison.json').write_text(json.dumps(comparisons, indent=2) + '\n')
    edited = sorted(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
    (B / 'edited.json').write_text(json.dumps(dict(paths=edited), indent=2) + '\n')
    assert edited == sorted([AP, TESTS, 'crates/security/src/lib.rs', 'crates/security/src/crash_matrix_sites.rs']), edited
    def fmt_clean(raw):
        r = subprocess.run([R + 'rustfmt', '--edition', '2024', '--emit', 'stdout'], input=raw, env=E, capture_output=True)
        return r.returncode == 0 and r.stdout == raw
    fmt_rows = []
    for x in [x for x in edited if x.endswith('.rs')]:
        base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + x], cwd=W, env=E, capture_output=True)
        fmt_rows.append(dict(path=x, baseClean=None if base_raw.returncode else fmt_clean(base_raw.stdout), candidateClean=fmt_clean((W / x).read_bytes())))
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    rows.append(dict(name='rustfmt-edited', exitCode=0 if all(r['candidateClean'] for r in fmt_rows if r['baseClean'] is not False) else 1, niceness=10))
    # The base-dirty lib.rs is append-only: the candidate begins with the base's exact bytes.
    lib_base = subprocess.run(['/usr/bin/git', 'show', 'HEAD:crates/security/src/lib.rs'], cwd=W, env=E, capture_output=True).stdout
    rows.append(dict(name='lib-rs-append-only', exitCode=0 if (W / 'crates/security/src/lib.rs').read_bytes().startswith(lib_base) else 1, niceness=10))
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    # The emitter is compiled only under the fixture predicate. Item names alone are no evidence (rustc's metadata
    # records cfg-stripped items' names too), so the newest rlib's code symbols are read: the release rlib defines the
    # codec's `field_at` and no `emit`; a debug build with scenario-fixtures defines both.
    def symbols_check(profile, emit_present):
        return ("import glob,os,subprocess,sys;libs=sorted(glob.glob('target/" + profile + "/deps/libopensip_security-*.rlib'),key=os.path.getmtime);"
                "syms=subprocess.run(['/usr/bin/nm','-a',libs[-1]],capture_output=True).stdout.decode(errors='replace');"
                "codec='15archive_profile8field_at' in syms;emit='15archive_profile4emit' in syms;print(libs[-1],'codec',codec,'emit',emit);"
                "sys.exit(0 if codec and emit is " + str(emit_present) + " else 1)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('workspace-check', [R + 'cargo', 'check', '--locked', '--offline', '--workspace', '--all-targets']),
             *FEATURES,
             ('security-release-build', [R + 'cargo', 'build', '--locked', '--offline', '--release', '-p', 'opensip-security']),
             ('release-emitter-absent', [PY, '-I', '-B', '-c', symbols_check('release', False)]),
             ('fixture-build', [R + 'cargo', 'build', '--locked', '--offline', '-p', 'opensip-security', '--features', 'scenario-fixtures']),
             ('fixture-emitter-present', [PY, '-I', '-B', '-c', symbols_check('debug', True)]),
             ('focused-ci1-tests', FOCUSED),
             ('pkg-ap-pin', [PY, '-I', '-B', str(EV / 'check_pkg_ap_pin.py'), str(W), str(A), str(B / 'pkg-ap-pin.json')]),
             ('fixed-vector-independent', [PY, '-I', '-B', str(EV / 'fixed_vector.py'), str(B / 'fixed-vector.tar')]),
             ('fixed-vector-bsdtar', ['/usr/bin/tar', '-tvf', str(B / 'fixed-vector.tar')]),
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
    # The independent vector equals the one the tests pin.
    vector = json.loads((B / 'fixed-vector-independent.log').read_text().strip().splitlines()[-1])
    pinned = (W / TESTS).read_text()
    rows.append(dict(name='fixed-vector-equals-pin', exitCode=0 if f'const FIXED_VECTOR_LENGTH: usize = {vector["length"]};' in pinned and f'"{vector["sha256"]}"' in pinned else 1, niceness=10))
    controls = []
    for name, ys, before, after in MUTATIONS:
        path = W / ys; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(FOCUSED, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and 'could not compile' not in out and 'test result: FAILED' in out
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=ys, caught=caught, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'), rebasedBeforeLane=rebased,
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], censusModesRun=False,
        censusModesNote='No census --check/--write mode is run: they need the T2 cache, which this unit may not read. CI-PT-4 is receipt-inputs-unchanged.',
        standing='UNREVIEWED CI-1 r2 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
