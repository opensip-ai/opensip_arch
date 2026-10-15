"""B2-a candidate checks: host and security suites (base and candidate, --no-fail-fast, equal failure sets), warning-denied
all-targets Clippy on host and security, rustfmt on base-clean and new edited files, the tools controls, the operability
census, verify_design, the reference vector check, the code mutations and the planted environment-read control. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re, sys, shutil
W = Path('/Users/sb/code/opensip-ai/opensip-b2a'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
# r2 (Codex NBO-01): every edited or new Rust file is classified; each one rustfmt-clean at base (or new) must be clean.
R_ = 'crates/security/src/custody/discovery_rule.rs'
T_R = ['test', '-p', 'opensip-security', '--lib', 'discovery_rule']
MUTATIONS = [
    (R_, T_R, 'cargo-not-outermost', "    }) && hit.as_ref().is_none_or(|h| index < h.depth())\n", "    }) && true\n"),
    (R_, T_R, 'cargo-roots-not-parent-first', "    ordered.sort_by_key(|path| (path.matches('/').count(), *path));\n", ""),
    (R_, T_R, 'opensip-any-depth', "    best.map(|k| PrunedAnchor::new(parts, k, PruneReason::OpensipCustodyState))", "    let _ = best;\n    parts\n        .iter()\n        .position(|s| *s == OPENSIP_CUSTODY_STATE)\n        .map(|k| PrunedAnchor::new(parts, k, PruneReason::OpensipCustodyState))"),
    (R_, T_R, 'opensip-not-outermost', "        Some(state) if hit.as_ref().is_none_or(|h| state.depth() < h.depth()) => Some(state),", "        Some(state) => Some(state),"),
    (R_, T_R, 'non-directory-recorded', "            recorded: kind == EntryKind::Directory && anchor.path == relpath,", "            recorded: anchor.path == relpath,"),
    (R_, T_R, 'cap-truncates', "            unit_dirs: Vec::new(),\n            pruned_trees,\n            refusal: Some(", "            unit_dirs: unit_dirs.iter().take(MAX_WORKSPACE_UNITS).cloned().collect(),\n            pruned_trees,\n            refusal: Some("),
    (R_, T_R, 'trailing-slash-kept', "    let body = spec.strip_suffix('/').unwrap_or(spec);", "    let body = spec;"),
    (R_, T_R, 'locator-root-slash', "    let base = format!(\"{}/\", selected_root.trim_end_matches('/'));", "    let base = format!(\"{selected_root}/\");"),
    (R_, T_R, 'module-does-io', "#[cfg(test)]\nmod tests {", "fn _planted() -> bool {\n    std::fs::metadata(\"/\").is_ok()\n}\n\n#[cfg(test)]\nmod tests {"),
]
COMPILE = []
PLANTED = [
    (R_, ['clippy', '-p', 'opensip-security', '--lib', '--', '-D', 'warnings'], 'planted-rule-read', "pub(crate) fn spell_root(internal_root: &str) -> &str {\n", "pub(crate) fn spell_root(internal_root: &str) -> &str {\n    let _planted = std::env::var_os(\"OPENSIP_PLANTED\");\n"),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b2a-check-', dir=D)); T.chmod(0o700)
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
    for pkg in ['opensip-security', 'opensip-host']:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        comparison[pkg] = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='host-security-base-comparison', exitCode=0 if all(c['equalFailureSets'] and c['candidateSuitesEqualBase'] and c['newPassingTests'] >= (1 if k == 'opensip-security' else 0) for k, c in comparison.items()) else 1, niceness=10)]
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines() if x.endswith('.rs'))
    def fmt_clean(path):
        return subprocess.run([R + 'rustfmt', '--edition', '2024', '--check', str(path)], env=E, capture_output=True).returncode == 0
    fmt_rows = [dict(path=x, baseClean=None if not (P / x).exists() else fmt_clean(P / x), candidateClean=fmt_clean(W / x)) for x in edited]
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    FMT = [r['path'] for r in fmt_rows if r['baseClean'] is not False]
    steps = [('rustfmt-edited', [R + 'rustfmt', '--edition', '2024', '--check', *FMT]),
             ('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('discovery-rule-vectors', [PY, '-I', '-B', 'tools/security/discovery_rule_vectors.py', '--check', '--architecture', str(A)]),
             ('configuration-tables', [PY, '-I', '-B', 'tools/tests/test_configuration_tables.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for kind, table in [('mutation', MUTATIONS), ('compile', COMPILE), ('planted', PLANTED)]:
        for rel, cargo, name, before, after in table:
            F = W / rel; original = F.read_bytes(); digest = hashlib.sha256(original).hexdigest(); text = original.decode()
            assert text.count(before) == 1, name
            F.write_text(text.replace(before, after))
            try:
                r = subprocess.run([R + 'cargo', cargo[0], '--locked', '--offline', *cargo[1:]], cwd=W, env=E, capture_output=True, text=True)
            finally:
                F.write_bytes(original)
            assert hashlib.sha256(F.read_bytes()).hexdigest() == digest
            log = r.stdout + r.stderr; (B / f'{kind}-{name}.log').write_text(log)
            if kind == 'mutation':
                failed = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', log, re.M)))
                caught = 'test result:' in log and bool(failed)
                controls.append(dict(kind=kind, name=name, file=rel, failedTests=failed, caught=caught))
            elif kind == 'compile':
                caught = r.returncode != 0 and 'error[E0283]' in log
                controls.append(dict(kind=kind, name=name, file=rel, exitCode=r.returncode, ambiguityFired='error[E0283]' in log, caught=caught))
            else:
                caught = r.returncode != 0 and 'disallowed_methods' in log
                controls.append(dict(kind=kind, name=name, file=rel, exitCode=r.returncode, lintFired='disallowed_methods' in log, caught=caught))
            print(kind, name, 'caught' if caught else 'NOT CAUGHT', flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-and-planted-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B2-a CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
