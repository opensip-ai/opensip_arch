"""C2a-3k candidate checks (M3-C r8 item 7; the C2a plan r4, sub-unit C2a-3k: the pure retained-tree verification kernel, on a
main that holds C2a-1 r1 and C2a-2 r2): the security and host suites on the base checkout and the candidate (--no-fail-fast;
equal failure sets after isolated reruns, and the new passing tests), rustfmt on the edited files (all base-clean), the
edited set exactly the three planned paths (lib.rs untouched), warning-denied all-targets Clippy on security, a workspace
all-targets check, the security features' debug checks, a release build of security, the focused C2a-1, C2a-2 and C2a-3k
tests, the environment exceptions, the operability source census with its mint audit, the census-closure check,
verify_design, and mutations, each of which must fail the focused tests (a compile failure never counts as caught).
One lane hold, nice 10, private TMPDIR. (Adapted from run_c2a2_checks.py.)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c2a3k'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
CC = 'crates/security/src/component_closure.rs'; CT = 'crates/security/src/component_closure_tests.rs'
TB = 'crates/security/src/trust/trust_bootstrap_tests.rs'
EXPECTED_EDITED = sorted([CC, CT, TB])
# The new passing tests over main (which holds C2a-1 and C2a-2): security 9 (eight C2a-3k controls in
# component_closure_tests.rs and C2-T6's kernel leg in trust_bootstrap_tests.rs); host none.
NEW_TESTS = {'opensip-security': 9, 'opensip-host': 0}
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--',
           'c2a3k_', 'c2a2_', 'component_closure', 'full_ordinary_catalog_and_component_joins_match_exact_reference']
MUTATIONS = [
    # (name, file, before, after): each weakens one C2a-3k rule (the C2a plan r4, sections 4 and 5; LD-C2A-5, LD-C2A-10);
    # the focused tests must fail.
    ('presence-check-removed', CC, '                Ordering::Greater => return Err(retention(Retention::Missing)),\n',
     '                Ordering::Greater => break slice,\n'),
    ('walk-end-accepted', CC, '            let Some((&path, &slice)) = next else {\n                return Err(retention(Retention::Missing));\n',
     '            let Some((&path, &slice)) = next else {\n                return Ok(());\n'),
    ('later-blobs-skipped', CC, '    for blob in candidate.blobs() {\n        let slice = loop {\n',
     '    for blob in candidate.blobs().take(1) {\n        let slice = loop {\n'),
    ('length-check-removed', CC, '        if u64::try_from(slice.len()) != Ok(blob.bytes()) {\n',
     '        if false && u64::try_from(slice.len()) != Ok(blob.bytes()) {\n'),
    ('blob-digest-check-removed', CC, '        if blob.sha256().as_bytes() != hex_digits(&digest) {\n',
     '        if false && blob.sha256().as_bytes() != hex_digits(&digest) {\n'),
    ('body-digest-check-removed', CC, '    if digest != candidate.manifest_digest {\n',
     '    if false && digest != candidate.manifest_digest {\n'),
    # A corrupted promised tree relabelled as absent (LD-C2A-5), and a length failure relabelled.
    ('digest-relabelled-missing', CC, '            return Err(retention(Retention::Digest));\n',
     '            return Err(retention(Retention::Missing));\n'),
    ('length-relabelled-digest', CC, '            return Err(retention(Retention::Length));\n',
     '            return Err(retention(Retention::Digest));\n'),
    # LD-C2A-10: a comparison or digest uncharged, under-priced or charged after it is made; a slice copied.
    ('length-comparison-uncharged', CC, '        work.charge(COMPARISON_COST)?;\n        if u64::try_from(slice.len())',
     '        if u64::try_from(slice.len())'),
    ('digest-charged-after', CC, '        work.charge(digest_cost(slice.len()))?;\n        let digest = raw_sha256(slice);\n',
     '        let digest = raw_sha256(slice);\n        work.charge(digest_cost(slice.len()))?;\n'),
    ('digest-under-priced', CC, '        work.charge(digest_cost(slice.len()))?;\n', '        work.charge(digest_cost(0))?;\n'),
    ('slice-copied', CC, '        let digest = raw_sha256(slice);\n', '        let digest = raw_sha256(&slice.to_vec());\n'),
    ('walk-not-advanced-on-match', CC, '                Ordering::Equal => {\n                    next = slices.next();\n                    break slice;\n',
     '                Ordering::Equal => {\n                    break slice;\n'),
]
FEATURES = [('scenario-fixtures-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'scenario-fixtures']),
            ('crash-matrix-check', [R + 'cargo', 'check', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--features', 'crash-matrix'])]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c2a3k-check-', dir=D)); T.chmod(0o700)
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
    rows.append(dict(name='rustfmt-edited', exitCode=0 if fmt_rows and all(r['baseClean'] and r['candidateClean'] for r in fmt_rows) else 1, niceness=10))
    # The candidate edits exactly its three planned paths, all base-clean; lib.rs (base-dirty) is untouched.
    rows.append(dict(name='edited-paths-exact', exitCode=0 if edited == EXPECTED_EDITED else 1, niceness=10))
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('workspace-check', [R + 'cargo', 'check', '--locked', '--offline', '--workspace', '--all-targets']),
             *FEATURES,
             ('security-release-build', [R + 'cargo', 'build', '--locked', '--offline', '--release', '-p', 'opensip-security']),
             ('focused-c2a3k-tests', FOCUSED),
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
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C2a-3k r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
