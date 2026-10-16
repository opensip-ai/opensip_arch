"""B3-b2b2c candidate checks (the T2 link-map controls and the joint sweep; B3-b plan r2 section 3, amendment A3): the security
and host suites on the base checkout and the candidate (--no-fail-fast, equal failure sets, the new passing tests counted), rustfmt
on new and base-clean edited files, warning-denied all-targets Clippy on security (with and without scenario-fixtures) and host,
the T2 reconstruction tool over the integrity-verified lead-readable stores into this lane's private temporary directory and the
two lane-run T2 controls over it (never a held-out entry), the host's scenario-driven discovery tests with the joint sweep, every
discovery vector check, the FW-01 pin, the walk-storage and census-tool controls, the census (--check, unchanged: no closure file
changes), the environment exceptions, the operability source census, verify_design, and mutation controls (each patches the tool,
the decision core, the inventory or the host instrument; its gate must fail). One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys, shutil
W = Path('/Users/sb/code/opensip-ai/opensip-b3b2b2c'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
TOOL = 'tools/security/t2_link_controls.py'; WD = 'crates/security/src/custody/workspace_declarations.rs'
SC = 'crates/security/src/custody/discovery_scan.rs'; HD = 'crates/host/src/discovery.rs'
CENSUS_JSON = 'crates/security/src/custody/discovery_census.json'; CENSUS_VECTORS = 'crates/security/src/custody/discovery_census_vectors.json'
NEW_TESTS = {'opensip-security': 0, 'opensip-host': 1}  # the two T2 controls are lane-run (ignored); the joint sweep is new
T2_TESTS = ['test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', '--ignored', 't2_']
SWEEP = ['test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'the_p3_sweep_with_members']
VEC = lambda tool: [PY, '-I', '-B', 'tools/security/' + tool, '--check', '--architecture', str(A), '--packages-root', str(P)]
MUTATIONS = [
    # (name, file, before, after, gate): the gate must fail on the mutated tree.
    ('carrier-drops-a-link', TOOL, "for name in sorted(links))", "for name in sorted(links)[1:])", 't2'),
    # The Cargo carrier minus its first link, written after the cache cross-check: the controls, not the tool, must catch it.
    ('cargo-carrier-written-short', TOOL, "        write(w / path, raw, 0o644)", "        write(w / path, b'\\n'.join(raw.split(b'\\n')[:1] + raw.split(b'\\n')[2:]) if ecosystem == 'cargo' else raw, 0o644)", 't2'),
    ('npm-carrier-drops-a-link', TOOL, "doc = {'private': True, 'workspaces': sorted(links.values(), key=lambda s: s.encode())}", "doc = {'private': True, 'workspaces': sorted(links.values(), key=lambda s: s.encode())[1:]}", 't2'),
    ('provider-manifest-swapped', TOOL, "            write(w / mount / inner, raw, 0o644)", "            write(w / mount / inner, raw.replace(b'\"' + name.encode() + b'\"', b'\"x' + name.encode() + b'\"', 1), 0o644)", 't2'),
    ('npm-links-not-npm', WD, 'ecosystem: "npm",', 'ecosystem: "cargo",', 't2'),
    ('inventory-members-dropped', SC, '        member_repositories: relative_set(&prov.member_repositories)?,', '        member_repositories: relative_set(&[])?,', 'sweep'),
    ('host-member-check-dropped', HD, '            if !members.contains(parent) {', '            if false {', 'sweep'),
]
def diff(a, b, p=''):
    if type(a) is not type(b): return [p]
    if isinstance(a, dict): return [x for k in sorted(set(a) | set(b)) for x in ([p + '/' + k] if k not in a or k not in b else diff(a[k], b[k], p + '/' + k))]
    if isinstance(a, list): return [p] if len(a) != len(b) else [x for i, (u, v) in enumerate(zip(a, b)) for x in diff(u, v, f'{p}/{i}')]
    return [] if a == b else [p]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b3b2b2c-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    RECON = T / 'opensip-t2-link-controls'
    def t2_run(log_name):
        """The tool into the lane's TMPDIR, then the two lane-run controls; the reconstruction is removed afterwards."""
        if RECON.exists(): shutil.rmtree(RECON)
        with (B / log_name).open('wb') as log:
            tool = subprocess.run([PY, '-I', '-B', TOOL, '--architecture', str(A), '--t2-cache', CACHE, '--out', str(RECON)], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            if tool.returncode != 0: return tool.returncode, False
            r = subprocess.run([R + 'cargo', *T2_TESTS], cwd=W, env=E, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log.write(r.stdout)
        if RECON.exists(): shutil.rmtree(RECON)
        ran = b'test result: ok. 2 passed' in r.stdout
        return r.returncode, ran
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    comparison, rows = {}, []
    for pkg in ['opensip-security', 'opensip-host']:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        comparison[pkg] = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
        c = comparison[pkg]
        rows.append(dict(name=pkg + '-base-comparison', exitCode=0 if c['equalFailureSets'] and c['candidateSuitesEqualBase'] and c['newPassingTests'] == NEW_TESTS[pkg] else 1, niceness=10))
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    # No closure file changes: the census record and vectors equal the base.
    projection = {rel: diff(json.loads(git(P, 'show', 'HEAD:' + rel)), json.loads((W / rel).read_text())) for rel in (CENSUS_JSON, CENSUS_VECTORS)}
    (B / 'census-unchanged.json').write_text(json.dumps(projection, indent=2) + '\n')
    rows.append(dict(name='census-unchanged', exitCode=0 if not any(projection.values()) else 1, niceness=10))
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines() if x.endswith('.rs'))
    def fmt_clean(raw):
        r = subprocess.run([R + 'rustfmt', '--edition', '2024', '--emit', 'stdout'], input=raw, env=E, capture_output=True)
        return r.returncode == 0 and r.stdout == raw
    fmt_rows = []
    for x in edited:
        base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + x], cwd=W, env=E, capture_output=True)
        fmt_rows.append(dict(path=x, baseClean=None if base_raw.returncode else fmt_clean(base_raw.stdout), candidateClean=fmt_clean((W / x).read_bytes())))
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    rows.append(dict(name='rustfmt-edited', exitCode=0 if all(r['candidateClean'] for r in fmt_rows if r['baseClean'] is not False) else 1, niceness=10))
    code, ran = t2_run('t2-link-controls.log')
    rows.append(dict(name='t2-link-controls', exitCode=0 if code == 0 and ran else 1, niceness=10, ranBoth=ran))
    print('t2-link-controls', code, ran, flush=True)
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('clippy-scenario', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--features', 'scenario-fixtures', '--all-targets', '--', '-D', 'warnings']),
             ('clippy-host', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '--all-targets', '--', '-D', 'warnings']),
             ('host-scenario-discovery', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'discovery_flag_tests']),
             ('workspace-discovery-vectors', VEC('workspace_discovery_vectors.py')),
             ('workspace-member-vectors', VEC('workspace_member_vectors.py')),
             ('discovery-member-vectors', VEC('discovery_member_vectors.py')),
             ('discovery-walk-vectors', VEC('discovery_walk_vectors.py')),
             ('discovery-scan-vectors', VEC('discovery_scan_vectors.py')),
             ('discovery-upward-vectors', VEC('discovery_upward_vectors.py')),
             ('discovery-rule-vectors', [PY, '-I', '-B', 'tools/security/discovery_rule_vectors.py', '--check', '--architecture', str(A)]),
             ('discovery-fw01-pin', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('discovery-walk-storage', [PY, '-I', '-B', 'tools/tests/test_discovery_walk_storage.py', '-v']),
             ('discovery-census-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census.py', '-v']),
             ('discovery-census', [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, rel, before, after, gate in MUTATIONS:
        path = W / rel; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        try:
            if gate == 't2':
                code, _ = t2_run(f'mutation-{name}.log')
                log = (B / f'mutation-{name}.log').read_text(errors='replace')
                caught = 'could not compile' not in log and 'error[E' not in log and code != 0
            else:
                r = subprocess.run([R + 'cargo', *SWEEP], cwd=W, env=E, capture_output=True, text=True)
                log = r.stdout + r.stderr; (B / f'mutation-{name}.log').write_text(log)
                caught = 'could not compile' not in log and 'error[E' not in log and r.returncode != 0
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=rel, gate=gate, caught=caught))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        reconstructionRemoved=not RECON.exists(), heldOutStoreOpened=False,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(),
        productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B3-B2B2C r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
