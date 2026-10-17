"""D1a candidate checks (M3-D r5 items 1 to 8, the spawn primitive; D1a plan r2; unit round 4 after Codex codex-d1a-r3):
the platform suite on the base checkout and the candidate, serially (--test-threads=1: the platform lib suite at base is
flaky in parallel, evidence/base-platform-flakiness.md), with equal failure sets after isolated reruns and the new passing
tests; rustfmt on the new and base-clean edited files; warning-denied all-targets Clippy on opensip-platform; the process
tests; FW-01; the environment exceptions; the operability source census; the census-closure check (no closure file
changed); verify_design; and eighteen mutations, each of which must fail the process tests. One lane hold, nice 10,
private TMPDIR. Linux rows are not run on this host."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d1a'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
PR = 'crates/platform/src/process.rs'
NEW_TESTS = 24
YAML_TESTS = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--lib', '--', 'process_tests']
MUTATIONS = [
    # (name, file, before, after): each weakens one item 1-8 rule; the process tests must fail.
    ('setsid-dropped', PR, "        let flags = POSIX_SPAWN_SETSID\n            | libc::POSIX_SPAWN_CLOEXEC_DEFAULT as libc::c_short\n", "        let flags = libc::POSIX_SPAWN_CLOEXEC_DEFAULT as libc::c_short\n"),
    ('cloexec-default-dropped', PR, "            | libc::POSIX_SPAWN_CLOEXEC_DEFAULT as libc::c_short\n", ""),
    ('sigdef-dropped', PR, "            | libc::POSIX_SPAWN_SETSIGDEF as libc::c_short\n", ""),
    ('sigmask-dropped', PR, "            | libc::POSIX_SPAWN_SETSIGMASK as libc::c_short;\n", ";\n"),
    ('environment-key-leaked', PR, '            .map(|(k, v)| CString::new(format!("{k}={v}")))\n', '            .map(|(k, v)| CString::new(format!("{k}={v}")))\n            .chain(std::iter::once(CString::new("LEAK=1")))\n'),
    ('extra-descriptor', PR, "        let count = spec.descriptors().count();\n", "        let count = spec.descriptors().count() + 1;\n"),
    ('scratch-not-private', PR, "        check(\"fchmod\", unsafe { libc::fchmod(dir.as_raw_fd(), 0o700) })?;\n", "        check(\"fchmod\", unsafe { libc::fchmod(dir.as_raw_fd(), 0o755) })?;\n"),
    ('core-limit-kept', PR, "            limit.rlim_cur = 0;\n", "            limit.rlim_cur = limit.rlim_max;\n"),
    ('group-after-reap', PR, "            if self.reaped {\n                return Err(LaunchError::GroupAfterReap);\n", "            if false {\n                return Err(LaunchError::GroupAfterReap);\n"),
    ('nosigpipe-omitted', PR, "            check(\"fcntl(F_SETNOSIGPIPE)\", unsafe {\n                libc::fcntl(host.as_raw_fd(), F_SETNOSIGPIPE, 1)\n            })?;\n", ""),
    ('addchdir-no-fallback', PR, "            c\"posix_spawn_file_actions_addchdir_np\",\n", ""),
    # r2 (Codex codex-d1a-r1): the reap, setup-failure and sweep-protocol fixes.
    ('reap-eintr-not-retried', PR, "                Some(libc::EINTR) => continue,\n", "                Some(libc::EINTR) => return Err(error),\n"),
    ('setup-failure-root-only', PR, "            libc::killpg(process_id, libc::SIGKILL);\n            libc::kill(process_id, libc::SIGKILL);\n", "            libc::kill(process_id, libc::SIGKILL);\n"),
    ('sweep-unopened-lock-proves-death', PR, "                if fd == -1 {\n                    continue;\n                }\n", "                if fd == -1 {\n                    remove_tree(dir.as_raw_fd())?;\n                    continue;\n                }\n"),
    # r3 (Codex codex-d1a-r2, D1A-R2-RF-1): the child's own hold on its root.
    ('child-root-guard-dropped', PR, "            root_guard: Some(Arc::clone(&scratch.root)),\n", "            root_guard: None,\n"),
    # r4 (Codex codex-d1a-r3, D1A-R3-RF-1 and NBO-1).
    ('abandoned-scratch-released', PR, "                        std::mem::forget(scratch);\n", "                        drop(scratch);\n"),
    ('sweep-not-reverified', PR, "                if !same_entry(dir.as_raw_fd(), &lock, held.as_raw_fd())\n                    || !same_entry(parent, &entry, dir.as_raw_fd())\n                {\n                    continue;\n                }\n", ""),
    ('sweep-follows-links', PR, "                libc::fstatat(dir, c.as_ptr(), &mut st, libc::AT_SYMLINK_NOFOLLOW)\n", "                libc::fstatat(dir, c.as_ptr(), &mut st, 0)\n"),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d1a-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        with log.open('wb') as out:
            # Serial (attempt 3): the platform lib suite at base aborts or fails one path_binding test in about half of
            # parallel runs (an existing test concurrency race; base evidence in attempt 2), and passes serially.
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg, '--', '--test-threads=1'], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    base = failures(P, 'opensip-platform', 'base'); cand = failures(W, 'opensip-platform', 'candidate')
    # A test failing on one side only is rerun alone, three times on each side: it is flaky (and not a
    # difference) only if every isolated run passes on both.
    differing = sorted(set(base['failed']) ^ set(cand['failed']))
    flaky = []
    for name in differing:
        runs = []
        for root in (P, W):
            for _ in range(3):
                r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--lib', '--', '--exact', name], cwd=root, env=E, capture_output=True)
                runs.append(r.returncode == 0 and b'1 passed' in r.stdout)
        (B / ('isolated-' + name.replace(':', '_') + '.json')).write_text(json.dumps(dict(test=name, runs=runs), indent=2) + '\n')
        if all(runs):
            flaky.append(name)
    comparison = dict(base=base, candidate=cand, differing=differing, flakyInIsolation=flaky, equalFailureSets=set(base['failed']) - set(flaky) == set(cand['failed']) - set(flaky), candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'] + len([f for f in flaky if f in cand['failed']]) - len([f for f in flaky if f in base['failed']]))
    print('host base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='platform-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] == NEW_TESTS else 1, niceness=10)]
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
             ('process-tests', YAML_TESTS),
             ('discovery-fw01', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
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
                r = subprocess.run(YAML_TESTS, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
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
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D1a r4 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
