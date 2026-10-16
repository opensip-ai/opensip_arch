"""B3-b2b1 candidate checks (the D15 readers and membership decision core; M3-B r9 items 19 to 24, plan r2 amendment A2):
the security and identity suites on the base checkout and the candidate (--no-fail-fast, equal failure sets, three new passing
security tests), rustfmt on new and base-clean edited files (stdin mode), warning-denied all-targets Clippy on security and
identity, the workspace member vectors and every existing discovery vector check, the FW-01 pin, the walk-storage and census-tool
controls, the census itself (--check over the integrity-verified lead-readable T2 stores, held-out entries never opened), the
equality projection for the custody.rs closure re-pin, the identity dependency check at base and candidate (equal outcomes), the
environment exceptions, the operability source census, verify_design, and mutation controls (each patches the core and the
workspace_declarations tests must fail). One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b3b2b1'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
WD = 'crates/security/src/custody/workspace_declarations.rs'
CENSUS_JSON = 'crates/security/src/custody/discovery_census.json'; CENSUS_VECTORS = 'crates/security/src/custody/discovery_census_vectors.json'
TEST = ['test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'workspace_declarations']
GATE = TEST
ARCHIVES = '/Users/sb/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f'
IDENTITY = lambda root: [PY, '-I', '-B', 'tools/check_identity_dependencies.py', '--manifest', str(root / 'Cargo.toml'), '--target', 'aarch64-apple-darwin',
                         '--cargo', R + 'cargo', '--archives', ARCHIVES, '--policy', str(root / 'tools/identity/dependency-policy.json')]
VEC = lambda tool: [PY, '-I', '-B', 'tools/security/' + tool, '--check', '--architecture', str(A), '--packages-root', str(P)]
MUTATIONS = [
    # (name, file, before, after): the workspace_declarations tests must fail on the mutated tree.
    ('cap-off-by-one', WD, 'pub(crate) const MAX_MEMBERS: usize = 64;', 'pub(crate) const MAX_MEMBERS: usize = 63;'),
    # A forbidden lookup that changes no output (A2 r2, B3BA2-R1-RF-2): placement looks a path up before classifying it.
    ('anchor-looked-up-before-classifying', WD, '        let members: BTreeSet<String> = out.candidate.iter().cloned().collect();\n',
     '        let members: BTreeSet<String> = out.candidate.iter().cloned().collect();\n        let _ = obs.entry(&prefix)?;\n'),
    ('glob-walk-enters-anchors', WD, 'if rule::classify_path(&rel, &cargo, &none).is_some() {', 'if false && rule::classify_path(&rel, &cargo, &none).is_some() {'),
    ('patch-spec-extra-keys-allowed', WD, 'if table.len() != 1 {', 'if table.len() == 0 {'),
    ('inner-entry-linked', WD, 'if p.inner {', 'if false && p.inner {'),
    ('ambiguity-threshold', WD, 'if dirs.len() > 1 {', 'if dirs.len() > 2 {'),
    ('reader-declarer-duplicated', WD, 'if !list.contains(&declarer) {', 'if true {'),
    ('root-in-repository-subject-altered', WD, 'Some("workspace-root-inside-repository".to_owned()),', 'Some("root-inside-repository".to_owned()),'),
    ('trial-verdict-ignored', WD, 'if !trial_accepted {', 'if false && !trial_accepted {'),
    ('member-directories-unwaived', WD, 'ProjectObject::Directory, true) {\n            return Ok(Some((dir, why)));',
     'ProjectObject::Directory, false) {\n            return Ok(Some((dir, why)));'),
    ('candidate-depth-unbounded', WD, 'if parts.len() > MAX_DEPTH {', 'if parts.len() > MAX_DEPTH + 1 {'),
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
    T = Path(tempfile.mkdtemp(prefix='opensip-b3b2b1-check-', dir=D)); T.chmod(0o700)
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
    for pkg in ['opensip-security', 'opensip-identity']:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        comparison[pkg] = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    host = comparison['opensip-security']
    ident = comparison['opensip-identity']
    rows = [dict(name='security-base-comparison', exitCode=0 if host['equalFailureSets'] and host['candidateSuitesEqualBase'] and host['newPassingTests'] == 3 else 1, niceness=10),
            dict(name='identity-base-comparison', exitCode=0 if ident['equalFailureSets'] and ident['candidateSuitesEqualBase'] and ident['newPassingTests'] == 0 else 1, niceness=10)]
    # The equality projection (plan r2 section 4.2, A1-2): base and candidate census records differ only in the custody.rs
    # closure row; the held-out rows are already outstanding (stale receipt) at the base and stay so.
    projection = {}
    for rel in (CENSUS_JSON, CENSUS_VECTORS):
        base_doc = json.loads(git(P, 'show', 'HEAD:' + rel)); cand_doc = json.loads((W / rel).read_text())
        changed = diff(base_doc, cand_doc)
        held = {i for i, e in enumerate(base_doc.get('entries', [])) if e.get('status') == 'blind-census'}
        allowed = [p for p in changed if re.fullmatch(r'/closure/6/(bytes|sha256)', p)]
        held = {i for i, e in enumerate(base_doc.get('entries', [])) if e.get('status', '').startswith('outstanding: held-out')}
        stale = all(cand_doc['entries'][i]['status'] == 'outstanding: held-out (blind receipt stale)' for i in held) if 'entries' in cand_doc else True
        projection[rel] = dict(changed=changed, unallowed=sorted(set(changed) - set(allowed)), heldOutRows=sorted(held), heldOutStale=stale)
    (B / 'equality-projection.json').write_text(json.dumps(projection, indent=2) + '\n')
    rows.append(dict(name='equality-projection', exitCode=0 if all(not v['unallowed'] and v['heldOutStale'] for v in projection.values()) else 1, niceness=10))
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '-p', 'opensip-identity', '--all-targets', '--', '-D', 'warnings']),
             ('test-workspace-declarations', [R + 'cargo', *TEST, '--nocapture']),
             ('test-discovery', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'discovery_', 'git_tracking']),
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
    # The identity dependency check, at base and candidate: equal outcomes (it fails at the base: its local-source census
    # predates later identity files; this unit updates only the toml.rs pin, as toml-views-r1 did).
    ident_runs = {}
    for tag, root in (('base', P), ('candidate', W)):
        r = subprocess.run(IDENTITY(root), cwd=root, env=E, capture_output=True, text=True)
        (B / f'identity-dependencies-{tag}.log').write_text(r.stdout + r.stderr)
        ident_runs[tag] = dict(exitCode=r.returncode, output=(r.stdout + r.stderr).replace(str(root), '<root>'))
    rows.append(dict(name='identity-dependencies-equal', exitCode=0 if ident_runs['base'] == ident_runs['candidate'] else 1, niceness=10, runs=ident_runs))
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, rel, before, after in MUTATIONS:
        path = W / rel; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        try:
            r = subprocess.run([R + 'cargo', *GATE], cwd=W, env=E, capture_output=True, text=True)
            log = r.stdout + r.stderr
            compiled = 'could not compile' not in log and 'error[E' not in log
            caught = compiled and r.returncode != 0
            (B / f'mutation-{name}.log').write_text(log)
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=rel, caught=caught))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(),
        productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B3-B2B1 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
