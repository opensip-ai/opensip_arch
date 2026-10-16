"""B3-b1 candidate checks (X2 r9 item 6b; the B2-c2 recipe): the security suite on the base checkout and the candidate
(--no-fail-fast, equal failure sets, seven new passing tests), rustfmt on new and base-clean edited files (stdin mode;
git_tracking.rs is not rustfmt-clean at base and is excluded), warning-denied all-targets Clippy on security, the
git_tracking tests, the environment exceptions, the discovery census --check (its closure is untouched), the operability
source census, verify_design, and mutation controls (each patches git_tracking.rs and the git_tracking tests must fail).
One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b3b1'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
GT = 'crates/security/src/custody/git_tracking.rs'
HOST_TEST = ['test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'git_tracking']
CENSUS = [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1']
MUTATIONS = [
    # (name, file, before, after, gate): the security git_tracking tests must fail on the mutated tree.
    ('device-check-dropped', GT, '.device != device {', '.device != device && false {', 'host'),
    ('other-marker-at-member-allowed', GT, '(true, false, false) => return member_refused(MemberRefusal::VcsUnsupported("vcs-other")),', '(true, false, false) => {}', 'host'),
    ('marker-between-allowed', GT, '(false, false, false) => return member_refused(MemberRefusal::VcsUnsupported("vcs-other")),', '(false, false, false) => {}', 'host'),
    ('member-config-latches', GT, 'layout(directory, &member.spelling(), inputs, &mut ignored, config_decided, work)', 'layout(directory, &member.spelling(), inputs, &mut ignored, config, work)', 'host'),
    ('gitlinks-dropped', GT, '.filter(|e| e.mode & 0o170000 == GITLINK)', '.filter(|e| e.mode & 0o170000 == GITLINK && false)', 'host'),
    ('environment-ignored', GT, '.and_then(|verdict| verdict.map_err(|r| WorkFailure::Operation(TrackingRefusal::VcsUnsupported(r))))', '.and_then(|_verdict| Ok(()))', 'host'),
    ('precondition-always', GT, '(self.tracking == Tracking::NoRepository).then_some(NoRepository(self))', 'Some(NoRepository(self))', 'host'),
    ('linked-worktree-dropped', GT, '        if !absent(&git, linked, work)? {\n            return unsupported("linked-worktree");', '        if !absent(&git, linked, work)? && false {\n            return unsupported("linked-worktree");', 'host'),
    ('outside-volume-subject-altered', GT, 'Self::OutsideVolume => "member-outside-volume".to_owned(),', 'Self::OutsideVolume => "member-off-volume".to_owned(),', 'host'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b3b1-check-', dir=D)); T.chmod(0o700)
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
    for pkg in ['opensip-security']:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        comparison[pkg] = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    host = comparison['opensip-security']
    rows = [dict(name='security-base-comparison', exitCode=0 if host['equalFailureSets'] and host['candidateSuitesEqualBase'] and host['newPassingTests'] == 7 else 1, niceness=10)]
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines() if x.endswith('.rs'))
    def fmt_clean(raw):
        r = subprocess.run([R + 'rustfmt', '--edition', '2024', '--emit', 'stdout'], input=raw, env=E, capture_output=True)
        return r.returncode == 0 and r.stdout == raw
    fmt_rows = []
    for x in edited:
        base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + x], cwd=W, env=E, capture_output=True)
        fmt_rows.append(dict(path=x, baseClean=None if base_raw.returncode else fmt_clean(base_raw.stdout), candidateClean=fmt_clean((W / x).read_bytes())))
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    rows.append(dict(name='rustfmt-edited', exitCode=0 if all(r['candidateClean'] for r in fmt_rows if r['baseClean'] is not False) else 1, niceness=10,
                     files=[r['path'] for r in fmt_rows if r['baseClean'] is not False]))
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('test-git-tracking', [R + 'cargo', *HOST_TEST, '--nocapture']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('discovery-census-check', CENSUS),
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
            r = subprocess.run([R + 'cargo', *HOST_TEST], cwd=W, env=E, capture_output=True, text=True)
            log = r.stdout + r.stderr
            compiled = 'could not compile' not in log and 'error[E' not in log
            caught = compiled and r.returncode != 0
            (B / f'mutation-{name}.log').write_text(log)
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=rel, gate=gate, caught=caught))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(),
        productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B3-B1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
