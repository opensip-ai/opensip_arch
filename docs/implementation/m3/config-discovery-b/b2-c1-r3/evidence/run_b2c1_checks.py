"""B2-c1 candidate checks (the native unit instrument, crates/host/src/discovery.rs; B2-c plan r2 section 2.1): the security and
host suites (base and candidate, --no-fail-fast, equal failure sets), warning-denied all-targets Clippy on host and security,
rustfmt on base-clean and new edited files, the unit vectors --check against the bound B2-c0 reference, the FW-01 structural
check (now covering discovery.rs and discovery_export.rs), the census --check (its whole-file cost closure is unchanged), the
vector checks, the environment pins, the configuration tables, the operability census, verify_design, and the source
mutations (each patches discovery.rs and must make the host discovery tests fail). One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re, sys, copy
W = Path('/Users/sb/code/opensip-ai/opensip-b2c1'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
TOOL = 'tools/security/discovery_census.py'; CENSUS = 'crates/security/src/custody/discovery_census.json'
DISC = 'crates/host/src/discovery.rs'
T_D = ['test', '-p', 'opensip-host', '--lib', '--', 'discovery_tests']
MUTATIONS = [
    ('member-check-dropped', '            if !members.contains(parent) {', '            if false {'),
    ('ld1-filter-dropped', '.is_some_and(|a| b.is_boundary(&a.path))', '.is_some_and(|_| false)'),
    ('u9-dropped', '    if units.is_empty() && explicit_roots.is_none() && boundary_hit("", boundaries, None).is_none()', '    if false && units.is_empty() && explicit_roots.is_none() && boundary_hit("", boundaries, None).is_none()'),
    ('jsconfig-default-flipped', '"jsconfig.json" if fact.allow_js.unwrap_or(true) => "js-allowjs",', '"jsconfig.json" if fact.allow_js.unwrap_or(false) => "js-allowjs",'),
    ('alias-altered', '("native.too-many-units", "PROJECT.WORKSPACE_UNIT_LIMIT"),', '("native.too-many-units", "PROJECT.SCOPE_LIMIT"),'),
    ('cardinality-dropped', '    if requested.len() > REQUESTED_CAPABILITY_BOUND {', '    if false {'),
    ('explicit-workspace-fold-dropped', '&& workspaces.iter().any(|w| **w != dir && under_unit(&dir, w))', '&& workspaces.is_empty()'),
    ('deepest-unit-shallowest', '            .max_by(|a, b| {\n                (a.root_path.len(), std::cmp::Reverse(a.unit_ordinal))', '            .min_by(|a, b| {\n                (a.root_path.len(), std::cmp::Reverse(a.unit_ordinal))'),
    # r2 (Codex B2C1-R1-RF-1 to RF-3)
    ('mode-vocabulary-dropped', '        if !m.modes.contains(mode) {\n            return Err(SelectionFault::Key(format!(\n                "native.requested-capability-mode-unregistered:{capability}:{mode}"', '        if false {\n            return Err(SelectionFault::Key(format!(\n                "native.requested-capability-mode-unregistered:{capability}:{mode}"'),
    ('bounds-count-bytes', 'fn chars(text: &str) -> usize {\n    text.chars().count()', 'fn chars(text: &str) -> usize {\n    text.len()'),
    ('standalone-not-test-only', '#[cfg(test)]\npub(crate) mod standalone {', 'pub(crate) mod standalone {'),
    # r3 (Codex B2C1-R2-RF-1)
    ('grammar-key-spells-value', '"NATIVE_UNIT_ROOT_REPRESENTATION:{at}:{selector}:grammar"', '"NATIVE_UNIT_ROOT_REPRESENTATION:{at}:{selector}:{value}"'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b2c1-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    comparison = {}
    for pkg in ['opensip-security', 'opensip-host']:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        comparison[pkg] = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='security-base-comparison', exitCode=0 if all(c['equalFailureSets'] and c['candidateSuitesEqualBase'] and c['newPassingTests'] >= 0 for k, c in comparison.items()) else 1, niceness=10)]
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines() if x.endswith('.rs'))
    def fmt_clean(path):
        return subprocess.run([R + 'rustfmt', '--edition', '2024', '--check', str(path)], env=E, capture_output=True).returncode == 0
    fmt_rows = [dict(path=x, baseClean=None if not (P / x).exists() else fmt_clean(P / x), candidateClean=fmt_clean(W / x)) for x in edited]
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    FMT = [r['path'] for r in fmt_rows if r['baseClean'] is not False]
    steps = [('rustfmt-edited', [R + 'rustfmt', '--edition', '2024', '--check', *FMT]),
             ('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('discovery-scan-vectors', [PY, '-I', '-B', 'tools/security/discovery_scan_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-upward-vectors', [PY, '-I', '-B', 'tools/security/discovery_upward_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-walk-vectors', [PY, '-I', '-B', 'tools/security/discovery_walk_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-fw01-pin', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('test-census', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'discovery_census_tests', '--nocapture', '--test-threads=1']),
             ('discovery-walk-storage', [PY, '-I', '-B', 'tools/tests/test_discovery_walk_storage.py', '-v']),
             ('discovery-census-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census.py', '-v']),
             ('discovery-census-blind-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census_blind.py', '-v']),
             ('discovery-unit-vectors', [PY, '-I', '-B', 'tools/host/discovery_unit_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('test-discovery-units', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'discovery_tests', '--nocapture']),
             ('discovery-census', [PY, '-I', '-B', TOOL, '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]),
             ('configuration-tables', [PY, '-I', '-B', 'tools/tests/test_configuration_tables.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, before, after in MUTATIONS:
        F = W / DISC; original = F.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        F.write_text(text.replace(before, after))
        try:
            r = subprocess.run([R + 'cargo', T_D[0], '--locked', '--offline', *T_D[1:]], cwd=W, env=E, capture_output=True, text=True)
        finally:
            F.write_bytes(original)
        assert F.read_bytes() == original
        log = r.stdout + r.stderr; (B / f'mutation-{name}.log').write_text(log)
        failed = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', log, re.M)))
        caught = 'test result:' in log and bool(failed)
        controls.append(dict(kind='mutation', name=name, file=DISC, failedTests=failed, caught=caught))
        print('mutation', name, 'caught' if caught else 'NOT CAUGHT', flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), 
        productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B2-c1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
