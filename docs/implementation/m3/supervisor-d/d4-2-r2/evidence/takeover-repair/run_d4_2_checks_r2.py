"""D4-2 candidate checks (M3-D r5 item 24; the D4 plan r2, sub-unit D4-2: the trust owner's admission view and the host's
R10a adapter, crates/host/src/component_admission.rs): the security and host suites on the base checkout and the
candidate (--no-fail-fast; equal failure sets after isolated reruns, and the new passing tests), rustfmt on the
edited Rust files (base-clean or new ones clean; base-dirty ones append-only), the edited set exactly the planned
paths, warning-denied all-targets Clippy on security and host, a workspace all-targets check, the security features'
debug checks, release builds of security and host, the package edges (host gains opensip-components, which the
inventory permits), the focused D4-2 tests, the environment exceptions, the operability source census with its mint
audit, the census-closure check, verify_design, and mutations, each of which must fail the focused tests (a compile
failure never counts as caught). One lane hold, nice 10, private TMPDIR. (Adapted from run_c2a3k_checks.py.)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d4-2'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
CA = 'crates/host/src/component_admission.rs'; CAT = 'crates/host/src/component_admission_tests.rs'
TAC = 'crates/security/src/trust_admitted_components.rs'; TOM = 'crates/security/src/trust_ordinary_metadata.rs'
CF = 'crates/security/src/trust/component_fixtures.rs'
EXPECTED_EDITED = sorted(['Cargo.lock', 'crates/host/Cargo.toml', 'crates/host/src/lib.rs', CA, CAT, 'crates/security/src/lib.rs',
                          'crates/security/src/crash_matrix_sites.rs',
                          'crates/security/src/trust.rs', CF, 'crates/security/src/trust/root_payload.rs',
                          'crates/security/src/trust/trust_bootstrap_tests.rs', TAC, TOM])
# Base-dirty files: only appended to.
APPEND_ONLY = ['crates/security/src/lib.rs', 'crates/security/src/trust/root_payload.rs']
# The new passing tests: security 2 (trust_bootstrap_tests.rs), host 10 (component_admission_tests.rs).
NEW_TESTS = {'opensip-security': 2, 'opensip-host': 10}
FOCUSED_SECURITY = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'd4_2', 'c2a2_', 'c2a3k_', 'component_fixtures', 'crash_matrix_sites']
FOCUSED_HOST = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'component_admission']
FOCUSED = None
MUTATIONS = [
    # (name, file, before, after, focused): each weakens one D4-2 rule; the focused tests must fail.
    ('reserved-list-not-passed', CA, '    for root in view.reserved_roots() {\n', '    for root in view.reserved_roots().take(0) {\n', 'host'),
    ('provider-table-substituted', CA, '    ("types", "checked"),\n', '    ("types", "resolved"),\n', 'host'),
    ('provenance-from-the-body', CA, '    let publisher = text(required(release, "publisher", work)?)?;\n    let source_class = source_class(text(required(release, "sourceClass", work)?)?, work)?;\n',
     '    let provenance = object(required(body, "provenance", work)?)?;\n    let publisher = text(required(provenance, "publisher", work)?)?;\n    let source_class = source_class(text(required(provenance, "sourceClass", work)?)?, work)?;\n', 'host'),
    ('explicit-trust-list-nonempty', CA, 'pub(crate) static EXPLICITLY_TRUSTED: [&str; 0] = [];\n', 'pub(crate) static EXPLICITLY_TRUSTED: [&str; 1] = ["opensip"];\n', 'host'),
    ('push-before-its-charge', CA, '        edges(work, 1)?;\n        reads.push(r);\n', '        reads.push(r);\n        edges(work, 1)?;\n', 'host'),
    ('allocation-before-its-charge', CA, "fn reserve<T>(work: &mut WorkScope<'_>, n: usize) -> Step<Vec<T>> {\n    work.charge",
     "fn reserve<T>(work: &mut WorkScope<'_>, n: usize) -> Step<Vec<T>> {\n    drop(Vec::<T>::with_capacity(n));\n    work.charge", 'host'),
    ('lookup-uncharged', CA, '    edges(work, object.len().max(1))?;\n', '', 'host'),
    ('lookup-underpriced', CA, '    edges(work, object.len().max(1))?;\n', '    edges(work, manifest::probe_reference_comparisons(object.len()))?;\n', 'host'),
    ('role-compared-before-its-charge', CA, '        edges(work, 1)?;\n        if name == spelling {\n            return Ok(role);\n',
     '        let hit = name == spelling;\n        edges(work, 1)?;\n        if hit {\n            return Ok(role);\n', 'host'),
    ('digest-decoded-wrong', CA, "        b'a'..=b'f' => Some(b - b'a' + 10),\n", "        b'a'..=b'f' => Some(b - b'a' + 11),\n", 'host'),
    ('parent-dropped', CA, '                Some(p) => Some(text(p)?),\n', '                Some(_) => None,\n', 'host'),
    ('reserved-set-rebuilt', TOM, '            &self.reserved_names,\n', '            Box::leak(Box::new(self.reserved_names.clone())),\n', 'security'),
    ('view-allocation-uncharged', TAC, '        work.charge::<()>(admission_view_cost(n))?;\n', '', 'security'),
    ('release-identity-hardcoded', CF, '            o(&o(&value)["provenance"])["sourceClass"].clone(),\n', '            V::String("first-party".to_owned()),\n', 'security'),
]
FEATURES = [('scenario-fixtures-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'scenario-fixtures']),
            ('crash-matrix-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'crash-matrix'])]
PACKAGE_EDGES = ("import json,subprocess,sys;R,PY,A,W=sys.argv[1:5];m=subprocess.run([R+'cargo','metadata','--format-version','1','--offline','--locked'],"
                 "capture_output=True,check=True,cwd=W).stdout;open(sys.argv[5],'wb').write(m);"
                 "lock=json.load(open(W+'/design-lock.json'));inv=lock['inventorySuccessors'][-1]['candidate']['path'];"
                 "r=subprocess.run([PY,'-I','-B','tools/check_package_edges.py','--repository',W,'--metadata',sys.argv[5],'--inventory',"
                 "A+'/'+inv,'--lane','host','--package-policy',"
                 "A+'/docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json','--architecture',A,'--lock','design-lock.json'],cwd=W,capture_output=True);"
                 "sys.stdout.write(r.stdout.decode()+r.stderr.decode());j=json.loads(r.stdout);"
                 "e=sorted({x['to'] for x in j['resolvedInternalEdges'] if x['from']=='opensip-host'});"
                 "print(e);sys.exit(0 if j['passed'] and 'opensip-components' in e else 1)")
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d4-2-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'status', '--porcelain') == ''
    # Reuse only the exact unchanged full-lane evidence. This worktree stays
    # on that pinned base; main's accepted platform-only advance is disjoint.
    R1 = Path('/tmp/opensip-implementation/d4-2-checks-takeover-r1')
    r1_checks = json.loads((R1 / 'checks.json').read_bytes())
    r1_comparison = json.loads((R1 / 'test-comparison.json').read_bytes())
    assert r1_checks['allPassed'] and git(W, 'rev-parse', 'HEAD') == r1_checks['productBase']
    oldmap = json.loads(Path('/tmp/opensip-implementation/codex-takeover-2026-10-17/d4-2-r1/architecture/docs/implementation/m3/supervisor-d/d4-2-r1/product-map.json').read_bytes())['rows']
    import hashlib
    changed_since_r1 = [r['path'] for r in oldmap if hashlib.sha256((W / r['path']).read_bytes()).hexdigest() != r['candidate']['sha256']]
    assert sorted(changed_since_r1) == sorted([CA, CAT]), changed_since_r1
    own = set(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
    assert own == {r['path'] for r in oldmap}
    moved = set(git(P, 'diff', '--name-only', r1_checks['productBase'], 'HEAD').splitlines())
    assert not moved & own, sorted(moved & own)
    assert subprocess.run(['/usr/bin/git','merge-base','--is-ancestor',r1_checks['productBase'],'HEAD'],cwd=P,env=E).returncode == 0
    # Format only the two changed host sources before any new execution.
    subprocess.run([R + 'rustfmt', '--edition', '2024', CA, CAT], cwd=W, env=E, check=True)
    with (B / 'preflight-focused-host.log').open('wb') as log:
        preflight = subprocess.run(FOCUSED_HOST,cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT)
    assert preflight.returncode == 0, 'focused controls must pass before full candidate execution'
    reused = dict(fullLane=str(R1),productBase=r1_checks['productBase'],changedSinceR1=sorted(changed_since_r1),securitySourceClosureUnchanged=True,baselineResultsReused=True,securityCandidateResultsReused=True,hostCandidateSuiteRunFresh=True)
    (B/'reused-evidence.json').write_text(json.dumps(reused,indent=2)+'\n')
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        if pkg == 'opensip-security' or tag == 'base':
            log.write_bytes((R1 / log.name).read_bytes())
            original = r1_comparison[pkg][tag]
            return dict(original, reusedFrom=str(R1 / log.name))
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
    rows.append(dict(name='rustfmt-edited', exitCode=0 if fmt_rows and all((r['baseClean'] is not False and r['candidateClean']) or r['path'] in APPEND_ONLY for r in fmt_rows) else 1, niceness=10))
    append_rows = []
    for x in APPEND_ONLY:
        base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + x], cwd=W, env=E, capture_output=True).stdout
        append_rows.append(dict(path=x, appendOnly=(W / x).read_bytes().startswith(base_raw) and len(base_raw) > 0, baseClean=fmt_clean(base_raw)))
    (B / 'append-only.json').write_text(json.dumps(append_rows, indent=2) + '\n')
    rows.append(dict(name='append-only-base-dirty', exitCode=0 if all(r['appendOnly'] and r['baseClean'] is False for r in append_rows) else 1, niceness=10))
    rows.append(dict(name='edited-paths-exact', exitCode=0 if edited == EXPECTED_EDITED else 1, niceness=10))
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '-p', 'opensip-host', '--all-targets', '--', '-D', 'warnings']),
             ('workspace-check', [R + 'cargo', 'check', '--locked', '--offline', '--workspace', '--all-targets']),
             *FEATURES,
             ('security-host-release-build', [R + 'cargo', 'build', '--locked', '--offline', '--release', '-p', 'opensip-security', '-p', 'opensip-host']),
             ('package-edges', [PY, '-I', '-B', '-c', PACKAGE_EDGES, R, PY, str(A), str(W), str(T / 'cargo-metadata.json')]),
             ('focused-d4-2-security-tests', FOCUSED_SECURITY),
             ('focused-d4-2-host-tests', FOCUSED_HOST),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('census-closure-unchanged', [PY, '-I', '-B', '-c', closure_check]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, ys, before, after, which in MUTATIONS:
        FOCUSED = FOCUSED_HOST if which == 'host' else FOCUSED_SECURITY
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
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(W, 'rev-parse', 'HEAD'), mainAtExecution=git(P,'rev-parse','HEAD'), reusedEvidence=reused,
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D4-2 r2 CANDIDATE CHECKS; exact pinned unchanged baseline/security evidence reused, host candidate and all mutations fresh'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
