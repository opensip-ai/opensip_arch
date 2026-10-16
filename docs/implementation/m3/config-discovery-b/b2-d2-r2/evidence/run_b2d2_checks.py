"""B2-d2 candidate checks (host framework recognition; B2-d plan r3 sections 3 and 4): the host suite on the base checkout and
the candidate (--no-fail-fast, equal failure sets, nine new passing tests), rustfmt on new and base-clean edited Rust files,
warning-denied all-targets Clippy on host, the recognition tests, the recognition and YAML vector checks against the bound
B2-d0 reference, FW-01 (the recognizers covered and pure), the environment exceptions, the operability source census,
verify_design, and twelve mutations of the recognizers (r2 adds the evidence preflight and the schema admission) (each must fail the recognition tests). One lane hold, nice 10,
private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b2d2'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
YS = 'crates/host/src/framework_recognition.rs'
NEW_TESTS = 9
YAML_TESTS = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'framework_recognition']
MUTATIONS = [
    # (name, before, after): each weakens one rule; the recognition tests must fail.
    ('state-rule-reverted', "    } else if out.iter().any(|r| !r.unresolved.is_empty()) {\n",
     "    } else if out.iter().any(|r| !r.unresolved.is_empty() && !r.entry.is_empty()) {\n"),
    ('entry-bound-per-result', "    let union: BTreeSet<&String> = out.iter().flat_map(|r| r.entry.iter()).collect();\n",
     "    let union: BTreeSet<&String> = out.iter().max_by_key(|r| r.entry.len()).into_iter().flat_map(|r| r.entry.iter()).collect();\n"),
    ('entry-bound-skipped-under-explicit', "    entry_bound(&mut out);\n", "    if inputs.explicit_entry_points.is_none() {\n        entry_bound(&mut out);\n    }\n"),
    ('explicit-empty-as-absent', "    let (state, source) = if inputs.explicit_entry_points.is_some() {\n",
     "    let (state, source) = if inputs.explicit_entry_points.is_some_and(|e| !e.is_empty()) {\n"),
    ('workspace-any-value', '                if table.get("workspace").and_then(|v| v.as_table()).is_some() {\n', '                if table.get("workspace").is_some() {\n'),
    ('tsconfig-bound-dropped', "        if raw.len() > typescript_config::MAX_CONFIG_FILE_BYTES || jsonc::parse(raw).is_err() {\n", "        if jsonc::parse(raw).is_err() {\n"),
    ('pnpm-subset-unchecked', '        if yaml_subset::parse_pnpm_packages(bytes_of("pnpm-workspace.yaml")?).is_err() {\n', '        if false {\n'),
    ('jest-config-disclosure-dropped', "                    if config.is_some() {\n", "                    if false {\n"),
    ('hints-unfiltered', "                                .filter(|n| FRAMEWORK_HINTS.contains(&n.as_str()))\n", "                                .filter(|n| !n.is_empty())\n"),
    ('evidence-preflight-dropped', "        .find(|p| inputs.paths.contains(**p) && !inputs.bytes.contains_key(**p))\n", "        .find(|_| false)\n"),
    ('schema-admission-dropped', "    schemas\n        .schema(PLAN_SCHEMA, ROW_SELECTOR)\n        .map_err(|_| RecognitionError::Shape)?\n        .admit_json(&raw, SCHEMA_BUDGET)\n        .map_err(|_| RecognitionError::Shape)?;\n",
     "    let _ = (schemas, PLAN_SCHEMA, ROW_SELECTOR, SCHEMA_BUDGET);\n"),
    ('evidence-hash-over-path', "        Ok((p.to_owned(), digest_hex(&raw_sha256(bytes_of(p)?)), field))\n", "        Ok((p.to_owned(), digest_hex(&raw_sha256(p.as_bytes())), field))\n"),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b2d2-check-', dir=D)); T.chmod(0o700)
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
    base = failures(P, 'opensip-host', 'base'); cand = failures(W, 'opensip-host', 'candidate')
    comparison = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
    print('host base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='host-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] == NEW_TESTS else 1, niceness=10)]
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '--all-targets', '--', '-D', 'warnings']),
             ('framework-recognition-tests', YAML_TESTS),
             ('framework-recognition-vectors', [PY, '-I', '-B', 'tools/host/framework_recognition_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('yaml-subset-vectors', [PY, '-I', '-B', 'tools/host/yaml_subset_vectors.py', '--check', '--architecture', str(A)]),
             ('discovery-fw01', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, before, after in MUTATIONS:
        path = W / YS; original = path.read_bytes(); text = original.decode()
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
        controls.append(dict(kind='mutation', name=name, file=YS, caught=caught, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED B2-D2 r2 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
