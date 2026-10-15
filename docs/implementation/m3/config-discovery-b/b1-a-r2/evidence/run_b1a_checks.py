"""B1-a candidate checks: rustfmt on edited files, the generated-table and PCM-vector drift checks and their controls, host tests
(base and candidate, --no-fail-fast, equal failure sets), warning-denied all-targets Clippy, the operability source census,
verify_design on the candidate, and the resolver mutation controls. One lane hold, nice 10, private 0700 TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b1a'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
EDITED = ['crates/host/src/configuration.rs', 'crates/host/src/configuration_tests.rs', 'crates/host/src/configuration_resolver_tests.rs', 'crates/host/src/configuration_tables.rs', 'crates/host/src/lib.rs']
MUT = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/b1a/evidence/run_b1a_mutations.py')
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b1a-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    def failures(root, tag):
        log = B / f'{tag}-host-tests.log'
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', 'opensip-host'], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        config = sorted(set(re.findall(r'^test (configuration::tests::\S+) \.\.\. ok$', text, re.M)))
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results), configurationTestsPassed=config)
    base = failures(P, 'base'); cand = failures(W, 'candidate')
    comparison = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'],
                      newPassingTests=cand['passed'] - base['passed'], configurationTests=dict(base=len(base['configurationTestsPassed']), candidate=len(cand['configurationTestsPassed'])))
    (B / 'host-test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n'); print('host base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    steps = [('rustfmt-edited', [R + 'rustfmt', '--edition', '2024', '--check', *EDITED]),
             ('tables-check', [PY, '-I', '-B', 'tools/host/generate_configuration_tables.py', '--check', '--architecture', str(A), '--rustfmt', R + 'rustfmt']),
             ('vectors-check', [PY, '-I', '-B', 'tools/host/configuration_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('tools-controls', [PY, '-I', '-B', 'tools/tests/test_configuration_tables.py', '-v']),
             ('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '--all-targets', '--', '-D', 'warnings']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    rows = [dict(name='host-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] > 0 else 1, niceness=10)]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    # mutation controls inside this lane hold
    F = W / 'crates/host/src/configuration.rs'; original = F.read_bytes(); digest = hashlib.sha256(original).hexdigest()
    ns = {}; exec(MUT.read_text().split('original = ')[0].replace('OUT.mkdir(parents=True)', 'None'), ns)
    mutations = []
    for name, before, after in ns['MUTATIONS']:
        text = original.decode(); assert text.count(before) == 1, name
        F.write_text(text.replace(before, after))
        try:
            r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', 'configuration'], cwd=W, env=E, capture_output=True, text=True)
        finally:
            F.write_bytes(original)
        log = r.stdout + r.stderr; (B / f'mutation-{name}.log').write_text(log)
        failed = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', log, re.M)))
        mutations.append(dict(mutation=name, before=before.strip(), after=after.strip(), compiled='test result:' in log, failedTests=failed, caught='test result:' in log and bool(failed))); print('mutation', name, len(failed), flush=True)
    assert hashlib.sha256(F.read_bytes()).hexdigest() == digest
    (B / 'mutations.json').write_text(json.dumps(dict(rows=mutations, allCaught=all(m['caught'] for m in mutations), restoredSha256=digest), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(m['caught'] for m in mutations) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'), standing='UNREVIEWED B1-a CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
