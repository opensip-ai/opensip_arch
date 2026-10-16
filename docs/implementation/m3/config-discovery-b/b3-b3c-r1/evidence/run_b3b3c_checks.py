"""B3-b3c candidate checks (the D15 workspace margins; B3-b plan r2 section 4.3): the security suite on the base checkout
and the candidate (--no-fail-fast, equal failure sets, one new passing test), the census record, its vectors and the
blind receipt byte-identical to the base (the census tool is untouched, so the receipt stays current), rustfmt on new and
base-clean edited Rust files, warning-denied all-targets Clippy on security (with and without scenario-fixtures), every
census test, the workspace ledger (--check over the integrity-verified lead-readable T2 stores and overlays), the census
(--check over the T2 cache), the T2 link reconstructions, the census tool's, blind receipt's and workspace ledger's
controls, the environment exceptions, the operability source census, verify_design, and four mutations (three of the
ledger tool, each caught by its controls; one of the record, caught by the Rust classification). One lane hold, nice 10,
private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b3b3c'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
LT = 'tools/security/discovery_workspace_ledger.py'; RECORD = 'crates/security/src/custody/discovery_workspace_ledger.json'
UNCHANGED = ['crates/security/src/custody/discovery_census.json', 'crates/security/src/custody/discovery_census_vectors.json',
             'crates/security/src/custody/discovery_census_held_out.json', 'tools/security/discovery_census.py', 'tools/security/discovery_member_model.py',
             'tools/security/t2_link_controls.py']
NEW_TESTS = 1
LEDGER_CONTROLS = [PY, '-I', '-B', 'tools/tests/test_discovery_workspace_ledger.py']
CLASSIFY = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'every_t2_workspace_full_ledger_is_classified_against_the_profile_limits']
T2 = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]
MUTATIONS = [
    # (name, file, before, after, control): each weakens the workspace ledger; its control must fail.
    ('members-not-repositories', LT, "        nodes[mount + '/.git'] = dict(kind='dir')\n", '        pass\n', LEDGER_CONTROLS),
    ('branch-a-dropped', LT, "BRANCHES = (('automatic', 'automatic'), ('configWorkspaceRoots', 'config-workspace-roots'))\n", "BRANCHES = (('automatic', 'automatic'),)\n", LEDGER_CONTROLS),
    ('carrier-not-rendered', LT, "        nodes[path] = dict(kind='file', size=len(raw), text=raw.decode())\n", "        nodes.pop(path, None)\n", LEDGER_CONTROLS),
    ('record-member-term-dropped', RECORD, None, None, CLASSIFY),
]
def drop_member_term(raw):
    body = json.loads(raw)
    body['workspaces'][0]['branches']['configWorkspaceRoots']['terms']['member']['edges'] = 0
    return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode()
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b3b3c-check-', dir=D)); T.chmod(0o700)
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
    base = failures(P, 'opensip-security', 'base'); cand = failures(W, 'opensip-security', 'candidate')
    comparison = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
    print('security base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='security-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] == NEW_TESTS else 1, niceness=10)]
    unchanged = {rel: subprocess.run(['/usr/bin/git', 'diff', '--quiet', 'HEAD', '--', rel], cwd=W, env=E).returncode == 0 for rel in UNCHANGED}
    (B / 'unchanged.json').write_text(json.dumps(unchanged, indent=2) + '\n')
    rows.append(dict(name='census-tool-records-and-receipt-unchanged', exitCode=0 if all(unchanged.values()) else 1, niceness=10))
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('clippy-scenario', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--features', 'scenario-fixtures', '--all-targets', '--', '-D', 'warnings']),
             ('census-tests', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'discovery_census']),
             ('workspace-ledger', [PY, '-I', '-B', LT, '--check', *T2]),
             ('discovery-census', [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', *T2]),
             ('t2-link-reconstructions', [PY, '-I', '-B', 'tools/security/t2_link_controls.py', '--architecture', str(A), '--t2-cache', CACHE, '--out', str(T / 't2-links')]),
             ('discovery-census-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census.py', '-v']),
             ('discovery-census-blind-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census_blind.py', '-v']),
             ('workspace-ledger-controls', LEDGER_CONTROLS + ['-v']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, rel, before, after, control in MUTATIONS:
        path = W / rel; original = path.read_bytes(); text = original.decode()
        if before is None:
            path.write_bytes(drop_member_term(original))
        else:
            assert text.count(before) == 1, name
            path.write_text(text.replace(before, after))
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(control, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and 'could not compile' not in out and (re.search(r'^FAILED \(', out, re.M) is not None or 'test result: FAILED' in out)
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=rel, caught=caught))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        heldOutStoreOpened=False, installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(),
        productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B3-B3C r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
