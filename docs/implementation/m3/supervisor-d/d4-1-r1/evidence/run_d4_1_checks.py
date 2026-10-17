"""D4-1 candidate checks (M3-D r5 item 24; the D4 plan r2, sub-unit D4-1: components/manifest.rs, the manifest-class
excluded forms over a borrowed projection, with SD-5's order and charged work): the components suite on the base checkout
and the candidate (--no-fail-fast; equal failure sets after isolated reruns, and the new passing tests), rustfmt on the
edited files (manifest.rs and its tests new, lib.rs base-clean), the edited set exactly the three planned paths,
warning-denied all-targets Clippy on components, a workspace all-targets check, a release build of components, the
focused D4-1 tests, the environment exceptions, the operability source census with its mint audit, the census-closure
check, verify_design, and mutations, each of which must fail the focused tests (a compile failure never counts as
caught). One lane hold, nice 10, private TMPDIR. (Adapted from run_c2a3k_checks.py.)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d4-1'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
M = 'crates/components/src/manifest.rs'; MT = 'crates/components/src/manifest_tests.rs'; L = 'crates/components/src/lib.rs'
EXPECTED_EDITED = sorted([L, M, MT])
# The new passing tests: components 15 (manifest_tests.rs); no other package changes.
NEW_TESTS = {'opensip-components': 15}
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-components', '--lib', '--', 'manifest::']
MUTATIONS = [
    # (name, file, before, after): each weakens one D4-1 rule (the D4 plan r2, LD-D4-3 to LD-D4-10); the focused tests
    # must fail.
    ('ee1-arm-removed', M, '        found(form(ExcludedFormClass::Ee1, Arm::UnlistedPublisher));\n', '        {}\n'),
    ('explicit-trust-probe-skipped', M, '        && !probe(policy.explicitly_trusted, claim.provenance.publisher, work)?\n', '        && true\n'),
    ('ee3b-arm-removed', M, '            found(form(ExcludedFormClass::Ee3b, Arm::UnmatchedCapability));\n', '            {}\n'),
    ('ee3b-any-relation', M, '        if !probe(\n            policy.provider_relations,', '        if false && !probe(\n            policy.provider_relations,'),
    ('ee5a-arm-removed', M, '        found(form(ExcludedFormClass::Ee5a, arm));\n', '        drop(arm);\n'),
    ('a-only-nonempty-tree', M, '    if claim.role != Role::Analyzer && claim.commands.is_some() {\n',
     '    if claim.role != Role::Analyzer && claim.commands.is_some_and(|c| !c.is_empty()) {\n'),
    ('b-name-binding-skipped', M, '        if root.is_some_and(|r| r.name != claim.name) {\n', '        if root.is_some_and(|r| r.name != r.name) {\n'),
    ('b-root-count-skipped', M, '        if roots != 1 {\n', '        if roots > 1 {\n'),
    ('c-root-aliases-skipped', M, '    let root_aliases = root.map_or(&[][..], |r| r.aliases);\n', '    let root_aliases: &[&str] = &[];\n'),
    ('class-order-swapped', M, '    Ee1,\n    Ee2,\n    Ee3b,\n', '    Ee3b,\n    Ee2,\n    Ee1,\n'),
    ('sort-removed', M, '    while width < len {\n', '    while false && width < len {\n'),
    ('sort-comparison-uncharged', M, '            while i < mid && j < high {\n                compare(work)?;\n', '            while i < mid && j < high {\n'),
    ('duplicate-pass-removed', M, '            return Err(Refusal::Invariant(InvariantFault::DuplicateDigest));\n', '            {}\n'),
    ('duplicate-comparison-uncharged', M, '        compare(work).map_err(refusal_budget)?;\n        if claims[pair[0] as usize]', '        if claims[pair[0] as usize]'),
    ('probe-uncharged', M, '        let mid = low + (high - low) / 2;\n        compare(work)?;\n', '        let mid = low + (high - low) / 2;\n'),
    ('empty-probe-uncharged', M, '    if slice.is_empty() {\n        compare(work)?;\n', '    if slice.is_empty() {\n'),
    ('refusal-vector-under-priced', M, '        work.charge::<()>(refusal_vector_cost(k))\n', '        work.charge::<()>(refusal_vector_cost(0))\n'),
    ('vector-truncated', M, '        return Err(Refusal::Excluded(forms));\n', '        forms.truncate(1);\n        return Err(Refusal::Excluded(forms));\n'),
    ('cleared-fill-uncharged', M, '        compare(work).map_err(refusal_budget)?;\n        digests.push(', '        digests.push('),
    ('policy-order-check-removed', M, '        if pair[0] >= pair[1] {\n', '        if false && pair[0] >= pair[1] {\n'),
]
FEATURES = []
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d4-1-check-', dir=D)); T.chmod(0o700)
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
    rows.append(dict(name='rustfmt-edited', exitCode=0 if fmt_rows and all(r['baseClean'] is not False and r['candidateClean'] for r in fmt_rows) else 1, niceness=10))
    # The candidate edits exactly its three planned paths: two new files and lib.rs, which is base-clean.
    rows.append(dict(name='edited-paths-exact', exitCode=0 if edited == EXPECTED_EDITED else 1, niceness=10))
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-components', '--all-targets', '--', '-D', 'warnings']),
             ('workspace-check', [R + 'cargo', 'check', '--locked', '--offline', '--workspace', '--all-targets']),
             *FEATURES,
             ('components-release-build', [R + 'cargo', 'build', '--locked', '--offline', '--release', '-p', 'opensip-components']),
             ('focused-d4-1-tests', FOCUSED),
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
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D4-1 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
