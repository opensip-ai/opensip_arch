"""B2-b4b3 candidate checks (the discovery caps recorded by M3-B r7 item 12, and the full margin test). The platform suite runs
one test thread at base and candidate: its library tests race on shared descriptors and the shared temp directory in
parallel (lane r1: an IO-safety abort at base, two retention races at the candidate, neither in work_ledger.rs): the security suite (base and candidate, --no-fail-fast, equal failure sets), warning-denied all-targets
Clippy on host and security, rustfmt on base-clean and new edited files, the census-tool controls, the census itself (--check over
the integrity-verified T2 stores and the vectors), the existing vector checks, the environment and FW-01 pins, the operability
census, verify_design, and the four cost-model mutations (each patches the tool, regenerates the predictions and must make the
native soundness tests fail). One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re, sys, shutil
W = Path('/Users/sb/code/opensip-ai/opensip-b2b4b3'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
TOOL = 'tools/security/discovery_census.py'; VEC = 'crates/security/src/custody/discovery_census_vectors.json'
T_S = ['test', '-p', 'opensip-security', '--lib', '--', 'discovery_census_tests::the_cost_model_bounds']
MODEL_MUTATIONS = [
    ('observation-charge-dropped', "        o, e, b = self.c['OBS']\n        self.add((o, e, b + blen(name), 0))", "        pass"),
    ('capture-edges-dropped', "        self.add(self.c['CAP'])\n        o, e = self.c['OWNED']", "        self.add((self.c['CAP'][0], 0, self.c['CAP'][2], 0))\n        o, e = self.c['OWNED']"),
    ('dot-entries-forgotten', "self.add(self.c['VISIT'], len(names) + 2)", "self.add(self.c['VISIT'], len(names))"),
    ('workspace-member-sum', "    return checked_model(c, wv, ref, slm, rule, compose(root_tree, members), label)",
     "    m = checked_model(c, wv, ref, slm, rule, root_tree, label)\n    for _, t in members:\n        x = checked_model(c, wv, ref, slm, rule, t, label)\n        m.objects += x.objects\n        m.edges += x.edges\n    return m"),
    ('scope-entry-bytes-dropped', "            self.owned(blen(rel) + self.c['ENTRY'])\n            self.observed.add(rel)", "            self.owned(blen(rel))\n            self.observed.add(rel)"),
]
WL = 'crates/platform/src/work_ledger.rs'
T_M = ['test', '-p', 'opensip-security', '--lib', '--', 'discovery_census_tests::']
MUTATIONS = [
    (WL, T_M, 'cap-not-raised', 'const DISCOVERY_OBJECT_LIMIT: usize = 1 << 22;', 'const DISCOVERY_OBJECT_LIMIT: usize = 1 << 20;'),
]
COMPILE = []
PLANTED = []
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b2b4b3-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg] + (['--', '--test-threads=1'] if pkg == 'opensip-platform' else []), cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    comparison = {}
    for pkg in ['opensip-security', 'opensip-platform']:
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
             ('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '-p', 'opensip-platform', '--all-targets', '--', '-D', 'warnings']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('discovery-scan-vectors', [PY, '-I', '-B', 'tools/security/discovery_scan_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-upward-vectors', [PY, '-I', '-B', 'tools/security/discovery_upward_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-walk-vectors', [PY, '-I', '-B', 'tools/security/discovery_walk_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-fw01-pin', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('test-census-soundness', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'discovery_census_tests', '--nocapture', '--test-threads=1']),
             ('discovery-walk-storage', [PY, '-I', '-B', 'tools/tests/test_discovery_walk_storage.py', '-v']),
             ('platform-census-sizes', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--test', 'discovery_census_sizes_tests']),
             ('discovery-census-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census.py', '-v']),
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
    for kind, table in [('mutation', MUTATIONS), ('compile', COMPILE), ('planted', PLANTED)]:
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
            elif kind == 'compile':
                caught = r.returncode != 0 and 'error[E0283]' in log
                controls.append(dict(kind=kind, name=name, file=rel, exitCode=r.returncode, ambiguityFired='error[E0283]' in log, caught=caught))
            else:
                caught = r.returncode != 0 and 'disallowed_methods' in log
                controls.append(dict(kind=kind, name=name, file=rel, exitCode=r.returncode, lintFired='disallowed_methods' in log, caught=caught))
            print(kind, name, 'caught' if caught else 'NOT CAUGHT', flush=True)
    for name, before, after in MODEL_MUTATIONS:
        F = W / TOOL; V_ = W / VEC; original, vectors = F.read_bytes(), V_.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        F.write_text(text.replace(before, after))
        try:
            g = subprocess.run([PY, '-I', '-B', TOOL, '--write', '--architecture', str(A), '--packages-root', str(P)], cwd=W, env=E, capture_output=True, text=True)
            regenerated = g.returncode == 0 and V_.read_bytes() != vectors
            r = subprocess.run([R + 'cargo', T_S[0], '--locked', '--offline', *T_S[1:]], cwd=W, env=E, capture_output=True, text=True)
        finally:
            F.write_bytes(original); V_.write_bytes(vectors)
        assert F.read_bytes() == original and V_.read_bytes() == vectors
        log = g.stdout + g.stderr + r.stdout + r.stderr; (B / f'model-mutation-{name}.log').write_text(log)
        failed = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', log, re.M)))
        caught = regenerated and 'test result:' in log and bool(failed)
        controls.append(dict(kind='model-mutation', name=name, file=TOOL, predictionsRegenerated=regenerated, failedTests=failed, caught=caught))
        print('model-mutation', name, 'caught' if caught else 'NOT CAUGHT', flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-and-planted-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B2-b4b3 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
