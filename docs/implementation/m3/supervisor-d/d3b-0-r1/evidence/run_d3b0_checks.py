"""D3b-0 candidate checks (M3-D r5 items 4, 8, 16 and 18; the D3b plan r3, sub-unit D3b-0: the macOS descendant
mechanisms in process.rs, with no policy): the platform suite on the base checkout and the candidate (--no-fail-fast,
serial; equal failure sets after isolated reruns, and the six new passing tests), rustfmt on the edited base-clean files,
warning-denied all-targets Clippy on platform, a workspace all-targets check (no dependent broken), the focused D3b-0
tests, the environment exceptions, the operability source census, the census-closure check, verify_design, and
mutations, each of which must fail the focused D3b-0 tests (not a compile error). One lane hold, nice 10, private
TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d3b0'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
PR = 'crates/platform/src/process.rs'
# The new passing tests: platform 6 (the D3b-0 controls).
NEW_TESTS = {'opensip-platform': 6}
# The platform suite runs serially, as D1a's lane does: in parallel it can abort on a pre-existing IO-safety race
# (attempt 2 aborted so; attempt 1 passed in parallel).
SERIAL = {'opensip-platform'}
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--lib', '--',
           'process_tests::child_processes', 'process_tests::group_members_bounded', 'process_tests::process_identity',
           'process_tests::kill_descendant', 'process_tests::a_start_time']
MUTATIONS = [
    # (name, file, before, after): each weakens one D3b-0 mechanism; the focused D3b-0 tests must fail.
    ('count-read-as-bytes', PR, "        Ok(listing(buf, count as usize, capacity))\n",
     "        Ok(listing(buf, count as usize / std::mem::size_of::<libc::pid_t>(), capacity))\n"),
    ('exceeded-truncated', PR, "        if n > capacity {\n            return Listing::Exceeded;\n        }\n",
     "        if false {\n            return Listing::Exceeded;\n        }\n"),
    ('group-capacity-ignored', PR, "        Ok(listing(buf, n, capacity))\n", "        Ok(listing(buf, n, usize::MAX))\n"),
    ('identity-equality-skipped', PR, "            if !now.same_process(target) {\n", "            if false && !now.same_process(target) {\n"),
    # RF-4: an order filter on start times reintroduced must be caught.
    ('order-filter-reintroduced', PR, "            if !now.same_process(target) {\n",
     "            if process_identity(self.process_id)?.is_some_and(|root| {\n                (target.start_seconds, target.start_micros) < (root.start_seconds, root.start_micros)\n            }) {\n                return Ok(KillOutcome::IdentityChanged);\n            }\n            if !now.same_process(target) {\n"),
    ('root-not-refused', PR, "            if pid == self.process_id {\n", "            if false && pid == self.process_id {\n"),
    ('after-reap-not-refused', PR, "            if self.reaped {\n                return Ok(KillOutcome::Refused(Protected::AfterReap));",
     "            if false && self.reaped {\n                return Ok(KillOutcome::Refused(Protected::AfterReap));"),
    ('zombie-read-as-error', PR, "            error if filled <= 0 && error.raw_os_error() == Some(libc::ESRCH) => Ok(None),\n",
     "            error if false => Ok(None),\n"),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d3b0-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # Main may have moved while this lane queued for the lock. Inside the lock it cannot move, so the worktree moves
    # onto it here, only if every change since the worktree's base is disjoint from the candidate's paths.
    main_head, work_head = git(P, 'rev-parse', 'HEAD'), git(W, 'rev-parse', 'HEAD')
    assert git(P, 'status', '--porcelain') == ''
    if main_head != work_head:
        assert subprocess.run(['/usr/bin/git', 'merge-base', '--is-ancestor', work_head, main_head], cwd=P, env=E).returncode == 0
        candidate = set(git(W, 'diff', '--name-only').splitlines()) | set(git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
        moved = set(git(P, 'diff', '--name-only', work_head, main_head).splitlines())
        assert not candidate & moved, sorted(candidate & moved)
        git(W, 'checkout', '-q', '--detach', main_head)
        (B / 'rebased.json').write_text(json.dumps(dict(fromBase=work_head, toBase=main_head, mainChanged=sorted(moved)), indent=2) + '\n')
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD')
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        extra = ['--', '--test-threads=1'] if pkg in SERIAL else []
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg, *extra], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
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
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-platform', '--all-targets', '--', '-D', 'warnings']),
             ('workspace-check', [R + 'cargo', 'check', '--locked', '--offline', '--workspace', '--all-targets']),
             ('focused-d3b0-tests', FOCUSED + ['--test-threads=1']),
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
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D3b-0 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
