"""C2a-1 candidate checks (M3-C r8 items 7 and 8; the C2a plan r4, sub-unit C2a-1: the unadmitted closure candidate): the
security and host suites on the base checkout and the candidate (--no-fail-fast; equal failure sets after isolated reruns,
and the new passing tests), rustfmt on the edited base-clean files (lib.rs is base-dirty and append-only), warning-denied
all-targets Clippy on security, a workspace all-targets check, the security features' debug checks, a release build of
security (no test seam reaches it), the focused C2a-1 tests, the environment exceptions, the operability source census
with its mint audit, the census-closure check, verify_design, and mutations, each of which must fail the focused tests.
One lane hold, nice 10, private TMPDIR. (Adapted from run_d3a0_checks.py.)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c2a1'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
CC = 'crates/security/src/component_closure.rs'; OM = 'crates/security/src/trust_ordinary_metadata.rs'
# The new passing tests: security 14 (the C2a-1 controls; the ordinary-metadata reference test gains the bridge's
# assertions and is not new); host none.
NEW_TESTS = {'opensip-security': 14, 'opensip-host': 0}
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--',
           'component_closure', 'full_ordinary_catalog_and_component_joins_match_exact_reference']
MUTATIONS = [
    # (name, file, before, after): each weakens one C2a-1 rule (the C2a plan r4, section 5); the focused tests must fail.
    ('dir-row-projected', CC, '        if text(member(entry, "type")?)? != "file" {\n            continue;\n',
     '        if text(member(entry, "type")?)? == "symlink" {\n            continue;\n'),
    ('symlink-row-projected', CC, '        if text(member(entry, "type")?)? != "file" {\n            continue;\n',
     '        if text(member(entry, "type")?)? == "dir" {\n            continue;\n'),
    ('kind-from-role-string', CC, '    let kind = component.closure_kind();\n',
     '    let kind = if text(member(manifest, "role")?)? == "analyzer" {\n        "analyzer"\n    } else {\n        component.closure_kind()\n    };\n'),
    ('digest-over-envelope', CC, '    let manifest_digest = raw_sha256(component.body());\n',
     '    let manifest_digest = raw_sha256(component.envelope());\n'),
    ('host-platform-spelling', CC, '        .ok_or(WorkFailure::Operation(ClosureRefusal::Platform))?;\n    let mut joined = false;\n',
     '        .unwrap_or("macos-aarch64");\n    let mut joined = false;\n'),
    ('release-artifact-join-skipped', CC, '    if !joined {\n', '    if false && !joined {\n'),
    ('blob-order-unsorted', CC, '        blobs[a as usize].path.as_bytes() < blobs[b as usize].path.as_bytes()\n', '        a > b && false\n'),
    ('integer-through-string', CC, 'fn push_decimal(out: &mut Vec<u8>, n: u64) {\n',
     'fn push_decimal(out: &mut Vec<u8>, n: u64) {\n    if n > 9 {\n        out.extend_from_slice(n.to_string().as_bytes());\n        return;\n    }\n'),
    ('descriptor-through-canonical-bytes', CC, '    push_descriptor(&mut descriptor, fields, blobs, order);\n',
     '    let mut own = Vec::with_capacity(length);\n    push_descriptor(&mut own, fields, blobs, order);\n    descriptor.extend_from_slice(&opensip_identity::canonical_bytes(&opensip_identity::parse_json(&own).unwrap()).unwrap());\n'),
    ('comparison-before-charge', CC, '                work.charge(COMPARISON_COST)?;\n                if less(from[j], from[i]) {\n',
     '                let take = less(from[j], from[i]);\n                work.charge(COMPARISON_COST)?;\n                if take {\n'),
    ('uncharged-sort-unstable-by', CC,
     '    let order = merge_sort(n, work, |a, b| {\n        blobs[a as usize].path.as_bytes() < blobs[b as usize].path.as_bytes()\n    })?;\n',
     '    let mut order = Vec::with_capacity(n as usize);\n    order.extend(0..n);\n    order.sort_unstable_by(|a: &u32, b: &u32| blobs[*a as usize].path.cmp(blobs[*b as usize].path));\n'),
    ('missing-declaration-inferred', CC, '    let Some(declaration) = declaration else {\n',
     '    let Some(declaration) = declaration.or(Some(provider_protocol)) else {\n'),
    ('analyzer-guard-skipped', CC, '    if role == "analyzer" && declaration != provider_protocol {\n',
     '    if false && role == "analyzer" && declaration != provider_protocol {\n'),
    ('descriptor-guard-skipped', CC, '    if descriptor != Some(declared as i128) {\n', '    if false && descriptor != Some(declared as i128) {\n'),
    ('support-before-descriptor-guard', CC, '    if descriptor != Some(declared as i128) {\n',
     '    if declared != 1 && analyzer.is_none() {\n        return Err(protocol(\n            ProtocolKey::Unsupported,\n            ProtocolOrigin::AuthenticatedReleaseDeclaration,\n        ));\n    }\n    if descriptor != Some(declared as i128) {\n'),
    ('support-guard-skipped', CC, '    if !supported {\n', '    if false && !supported {\n'),
    ('support-numeric-union', CC, '        "toolchain" | "stdlib" | "rust-dev-llvm" | "grammar" => declared == 1,\n',
     '        "toolchain" | "stdlib" | "rust-dev-llvm" | "grammar" => declared >= 1,\n'),
    ('analyzer-cross-role-equivalence', CC, '        "analyzer" => analyzer.is_some_and(|selected| selected.major == declared),\n',
     '        "analyzer" => declared == 1 || analyzer.is_some_and(|selected| selected.major == declared),\n'),
    ('major-from-provider-protocol', CC, '        protocol_major: major,\n', '        protocol_major: provider_protocol as u64,\n'),
    ('host-bug-routed-external', CC, '            ProtocolKey::DescriptorMismatch,\n            ProtocolOrigin::HostGeneratedInternalLayer,\n',
     '            ProtocolKey::DescriptorMismatch,\n            ProtocolOrigin::AuthenticatedReleaseDeclaration,\n'),
    ('external-routed-host-bug', CC, '            ProtocolKey::DeclarationMissing,\n            ProtocolOrigin::AuthenticatedReleaseDeclaration,\n',
     '            ProtocolKey::DeclarationMissing,\n            ProtocolOrigin::HostGeneratedInternalLayer,\n'),
    ('encoding-bound-off-by-one', CC, '    if length > MAX_BYTES {\n', '    if length >= MAX_BYTES {\n'),
    ('prediction-off-by-one', CC, '    let mut len = 175usize\n', '    let mut len = 176usize\n'),
    ('duplicate-pass-removed', CC, '        if blobs[pair[0] as usize].path == blobs[pair[1] as usize].path {\n',
     '        if false && blobs[pair[0] as usize].path == blobs[pair[1] as usize].path {\n'),
    ('projection-reserved-before-charge', CC, '    work.charge(projection_cost(files))?;\n    let mut blobs = Vec::with_capacity(files);\n',
     '    let mut blobs = Vec::with_capacity(files);\n    work.charge(projection_cost(files))?;\n'),
    ('bridge-body-is-envelope', OM, '                pair.body(),\n                pair.envelope(),\n',
     '                pair.envelope(),\n                pair.envelope(),\n'),
]
FEATURES = [('scenario-fixtures-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'scenario-fixtures']),
            ('crash-matrix-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'crash-matrix'])]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c2a1-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'status', '--porcelain') == ''
    # Main moves only under the lead's lock, so it cannot move while this lane holds it. If it moved while this lane
    # waited, the worktree follows it here, only when what main changed is disjoint from the candidate's paths.
    own = set(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
    if git(P, 'rev-parse', 'HEAD') != git(W, 'rev-parse', 'HEAD'):
        moved = set(git(P, 'diff', '--name-only', git(W, 'rev-parse', 'HEAD'), git(P, 'rev-parse', 'HEAD')).splitlines())
        assert not moved & own, sorted(moved & own)
        git(W, 'checkout', '-q', '--detach', git(P, 'rev-parse', 'HEAD'))
        print('worktree moved onto main', git(W, 'rev-parse', 'HEAD'), flush=True)
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
    rows.append(dict(name='rustfmt-edited', exitCode=0 if all(r['candidateClean'] for r in fmt_rows if r['baseClean'] is not False) else 1, niceness=10))
    # The base-dirty lib.rs is append-only: the candidate begins with the base's exact bytes.
    lib_base = subprocess.run(['/usr/bin/git', 'show', 'HEAD:crates/security/src/lib.rs'], cwd=W, env=E, capture_output=True).stdout
    rows.append(dict(name='lib-rs-append-only', exitCode=0 if (W / 'crates/security/src/lib.rs').read_bytes().startswith(lib_base) else 1, niceness=10))
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('workspace-check', [R + 'cargo', 'check', '--locked', '--offline', '--workspace', '--all-targets']),
             *FEATURES,
             ('security-release-build', [R + 'cargo', 'build', '--locked', '--offline', '--release', '-p', 'opensip-security']),
             ('focused-c2a1-tests', FOCUSED),
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
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C2a-1 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
