"""B1-b candidate checks: host and security suites (base and candidate, --no-fail-fast, equal failure sets), warning-denied
all-targets Clippy on host and security, rustfmt on base-clean and new edited files, the tools controls, the operability
census, verify_design, the code mutations and the planted environment-read controls. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re, sys, shutil
W = Path('/Users/sb/code/opensip-ai/opensip-b1b'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
# r2 (Codex NBO-01): every edited or new Rust file is classified; each one rustfmt-clean at base (or new) must be clean.
SEC = 'crates/security/src/custody/project_admission.rs'; MODE = 'crates/host/src/invocation_mode.rs'; READ = 'crates/security/src/custody/installation_read.rs'
MUTATIONS = [
    (SEC, ['test', '-p', 'opensip-security', '--lib', 'project_admission'], 'ci-probes-local', '        LocalCarrierPolicy::NonInteractive => None,', '        LocalCarrierPolicy::NonInteractive => Some(LocalCarrier::DirectoryAbsent),'),
    (SEC, ['test', '-p', 'opensip-security', '--lib', 'project_admission'], 'ci-ignored-local-lookup', '        LocalCarrierPolicy::NonInteractive => None,', '        LocalCarrierPolicy::NonInteractive => {\n            let _ = local_directory(root, uid, policy, work);\n            None\n        }'),
    (SEC, ['test', '-p', 'opensip-security', '--lib', 'project_admission'], 'absence-recheck-off', '    if absent {\n        Ok(())\n    } else {\n        refuse(ProjectAdmissionRefusal::Carrier(appeared))', '    if absent || true {\n        Ok(())\n    } else {\n        refuse(ProjectAdmissionRefusal::Carrier(appeared))'),
    (SEC, ['test', '-p', 'opensip-security', '--lib', 'project_admission'], 'carrier-recheck-off', '            ProjectCarrier::Captured(carrier) => same_carrier(root, carrier, work)?,', '            ProjectCarrier::Captured(_) => {}'),
    (SEC, ['test', '-p', 'opensip-security', '--lib', 'project_admission'], 'capture-rebaselines', '    if carrier_sample(file, work)? != *judged {\n        return refuse(ProjectAdmissionRefusal::Changed);\n    }\n    let metadata = judged.clone();', '    let metadata = carrier_sample(file, work)?;'),
    (READ, ['test', '-p', 'opensip-security', '--lib', 'project_admission'], 'optional-parent-sample-off', '            if capture.metadata() != metadata {', '            if capture.metadata() != metadata && false {'),
    (MODE, ['test', '-p', 'opensip-host', '--lib', 'invocation_mode'], 'mode-either-stream', '        interactive: stdin_terminal && stderr_terminal,', '        interactive: stdin_terminal || stderr_terminal,'),
]
PLANTED = [
    (MODE, ['clippy', '-p', 'opensip-host', '--lib', '--', '-D', 'warnings'], 'planted-host-read', 'pub(crate) fn observe_invocation_mode() -> InvocationModeV1 {\n', 'pub(crate) fn observe_invocation_mode() -> InvocationModeV1 {\n    let _planted = std::env::var("OPENSIP_PLANTED");\n'),
    (SEC, ['clippy', '-p', 'opensip-security', '--lib', '--', '-D', 'warnings'], 'planted-security-read', ') -> Result<ConfigCarriers, Failure> {\n    let project = match selected_config {', ') -> Result<ConfigCarriers, Failure> {\n    let _planted = std::env::var_os("OPENSIP_PLANTED");\n    let project = match selected_config {'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b1b-check-', dir=D)); T.chmod(0o700)
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
    rows = [dict(name='host-security-base-comparison', exitCode=0 if all(c['equalFailureSets'] and c['candidateSuitesEqualBase'] and c['newPassingTests'] > 0 for c in comparison.values()) else 1, niceness=10)]
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines() if x.endswith('.rs'))
    def fmt_clean(path):
        return subprocess.run([R + 'rustfmt', '--edition', '2024', '--check', str(path)], env=E, capture_output=True).returncode == 0
    fmt_rows = [dict(path=x, baseClean=None if not (P / x).exists() else fmt_clean(P / x), candidateClean=fmt_clean(W / x)) for x in edited]
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    FMT = [r['path'] for r in fmt_rows if r['baseClean'] is not False]
    # The legacy admission's charges, base against candidate (Codex B1B-R1-RF-04): the same probe file runs in a
    # copy of the base product and in the candidate; the printed charges must be equal line for line.
    base_copy = T / 'base-product'; base_copy.mkdir()
    archive = subprocess.run(['/usr/bin/git', 'archive', 'HEAD'], cwd=P, env=E, capture_output=True, check=True).stdout
    subprocess.run(['/usr/bin/tar', '-x', '-C', str(base_copy)], input=archive, check=True)
    probe = 'crates/security/src/custody/project_admission_legacy_probe_tests.rs'
    (base_copy / probe).write_bytes((W / probe).read_bytes())
    host_file = base_copy / SEC; text = host_file.read_text(); anchor = 'include!("project_admission_tests.rs");'
    assert text.count(anchor) == 1; host_file.write_text(text.replace(anchor, anchor + '\n    include!("project_admission_legacy_probe_tests.rs");'))
    def probe_lines(root, tag):
        r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', '--ignored', '--exact',
                            'custody::project_admission::tests::b1b_legacy_spend_probe', '--nocapture', '--test-threads=1'], cwd=root, env=E, capture_output=True, text=True)
        (B / f'legacy-probe-{tag}.log').write_text(r.stdout + r.stderr)
        return r.returncode, [line[line.index('B1B-LEGACY:'):] for line in r.stdout.splitlines() if 'B1B-LEGACY:' in line]
    base_code, base_lines = probe_lines(base_copy, 'base'); cand_code, cand_lines = probe_lines(W, 'candidate')
    legacy = dict(baseExit=base_code, candidateExit=cand_code, base=base_lines, candidate=cand_lines, equal=base_lines == cand_lines and len(base_lines) == 5)
    (B / 'legacy-probe.json').write_text(json.dumps(legacy, indent=2) + '\n'); print('legacy probe equal', legacy['equal'], flush=True)
    rows.append(dict(name='legacy-charges-base-equal', exitCode=0 if legacy['equal'] and base_code == 0 and cand_code == 0 else 1, niceness=10))
    shutil.rmtree(base_copy, ignore_errors=True)
    steps = [('rustfmt-edited', [R + 'rustfmt', '--edition', '2024', '--check', *FMT]),
             ('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('configuration-tables', [PY, '-I', '-B', 'tools/tests/test_configuration_tables.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for kind, table in [('mutation', MUTATIONS), ('planted', PLANTED)]:
        for rel, cargo, name, before, after in table:
            F = W / rel; original = F.read_bytes(); digest = hashlib.sha256(original).hexdigest(); text = original.decode()
            assert text.count(before) == 1, name
            F.write_text(text.replace(before, after))
            try:
                r = subprocess.run([R + 'cargo', cargo[0], '--locked', '--offline', *cargo[1:]], cwd=W, env=E, capture_output=True, text=True)
            finally:
                F.write_bytes(original)
            assert hashlib.sha256(F.read_bytes()).hexdigest() == digest
            log = r.stdout + r.stderr; (B / f'{kind}-{name}.log').write_text(log)
            if kind == 'mutation':
                failed = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', log, re.M)))
                caught = 'test result:' in log and bool(failed)
                controls.append(dict(kind=kind, name=name, file=rel, failedTests=failed, caught=caught))
            else:
                caught = r.returncode != 0 and 'disallowed_methods' in log
                controls.append(dict(kind=kind, name=name, file=rel, exitCode=r.returncode, lintFired='disallowed_methods' in log, caught=caught))
            print(kind, name, 'caught' if caught else 'NOT CAUGHT', flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-and-planted-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B1-b CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
