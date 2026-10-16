"""S10-TSC candidate checks (B-S10's and B2-c1's recipe): the identity, contracts, host and storage suites on the base
checkout and the candidate (--no-fail-fast, equal failure sets), rustfmt on base-clean edited files, warning-denied
all-targets Clippy, the operability source census, the content checker, and mutation controls (each patches one file and
must make the content checker or the host test fail). One lane hold, nice 10, private TMPDIR. The report TypeScript lane
and generate_contracts --check need the bound lock (verify_design's admission preflight) and run at integration."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-s10tsc'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
U = A / 'docs/implementation/m3/config-discovery-b/s10-tsc'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
PKGS = P / 'tools/contracts/python-packages'
CONTENT = [PY, '-I', '-B', str(U / 'evidence/check_s10_tsc.py'), '--architecture', str(A), '--product', str(W), '--packages', str(PKGS)]
HOST_TEST = ['test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'the_typescript_configuration_detail_is_admitted']
CODE = 'native.typescript-config-unresolved'
MUTATIONS = [
    # (name, file, before, after, gate): the gate must fail on the mutated tree.
    ('model-d9-code-flipped', U / 'reference/native_evidence_model.v2.py',
     f'"{CODE}": {{"class": "request-rejected", "exitCode": 2, "code": "CONFIG.INVALID"',
     f'"{CODE}": {{"class": "request-rejected", "exitCode": 2, "code": "REQUEST.PRECONDITION_FAILED"', 'content'),
    ('alias-to-config-invalid', U / 'registry/public-detail-registry.v1.json',
     '"internalCode": "native.typescript-config-malformed",\n      "publicCode": "native.typescript-config-unresolved"',
     '"internalCode": "native.typescript-config-malformed",\n      "publicCode": "CONFIG.INVALID"', 'content'),
    ('snapshot-line-record-dropped', U / 'registry/public-detail-registry.v1.json',
     '"code": "native.path-manifest-limit"', '"code": "native.path-manifest-limit-x"', 'content'),
    ('remedy-reuses-config-invalid', U / 'reference/native_evidence_model.py',
     f'    "{CODE}": "the TypeScript', f'    "{CODE}": "the configuration or selection is invalid; the TypeScript', 'content'),
    ('product-remedy-altered', W / 'crates/host/src/outcomes.rs',
     'within 32 files; or correct', 'within 33 files; or correct', 'both'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-s10tsc-check-', dir=D)); T.chmod(0o700)
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
    for pkg in ['opensip-identity', 'opensip-contracts', 'opensip-host', 'opensip-storage']:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        comparison[pkg] = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='base-comparison', exitCode=0 if all(c['equalFailureSets'] and c['candidateSuitesEqualBase'] and c['newPassingTests'] >= 0 for c in comparison.values()) and comparison['opensip-host']['newPassingTests'] == 1 else 1, niceness=10)]
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines() if x.endswith('.rs'))
    def fmt_clean(path):
        return subprocess.run([R + 'rustfmt', '--edition', '2024', '--check', str(path)], env=E, capture_output=True).returncode == 0
    fmt_rows = [dict(path=x, baseClean=None if not (P / x).exists() else fmt_clean(P / x), candidateClean=fmt_clean(W / x)) for x in edited]
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    FMT = [r['path'] for r in fmt_rows if r['baseClean'] is not False]
    steps = [('rustfmt-edited', [R + 'rustfmt', '--edition', '2024', '--check', *FMT]),
             ('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-identity', '-p', 'opensip-contracts', '-p', 'opensip-host', '-p', 'opensip-storage', '--all-targets', '--', '-D', 'warnings']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('content-check', [*CONTENT, '--work', str(B / 'content-work'), '--out', str(B / 'content-check.json')])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, path, before, after, gate in MUTATIONS:
        original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        caught = {}
        try:
            if gate in ('content', 'both'):
                r = subprocess.run([*CONTENT, '--work', str(B / f'mutation-{name}-work'), '--out', str(B / f'mutation-{name}-content.json')], cwd=W, env=E, capture_output=True, text=True)
                (B / f'mutation-{name}-content.log').write_text(r.stdout + r.stderr)
                caught['content'] = r.returncode != 0 and 'FAIL ' in r.stdout
            if gate == 'both':
                r = subprocess.run([R + 'cargo', *HOST_TEST], cwd=W, env=E, capture_output=True, text=True)
                log = r.stdout + r.stderr; (B / f'mutation-{name}-host.log').write_text(log)
                caught['host'] = 'test result:' in log and bool(re.findall(r'^test (\S+) \.\.\. FAILED$', log, re.M))
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=str(path), gates=caught, caught=bool(caught) and all(caught.values())))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(),
        productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        deferredToIntegration=['report TypeScript lane (tools/check_typescript.py --lane report)', 'tools/generate_contracts.py --check', 'verify_design with the bound lock'],
        standing='UNREVIEWED S10-TSC CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
