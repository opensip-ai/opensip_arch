"""B2-c2 candidate checks (B2-c1's recipe): the host suite on the base checkout and the candidate (--no-fail-fast, equal
failure sets, eight new passing tests), rustfmt on new and base-clean edited files (stdin mode), warning-denied
all-targets Clippy, the TypeScript configuration vectors and the B2-c1 unit vectors --check, FW-01 (with its planted
negatives), the host TypeScript configuration tests, the operability source census, verify_design, and mutation
controls: each patches one file, and the host tests (product mutations) or the vector check (tool mutations) must fail.
One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b2c2'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
TC = 'crates/host/src/typescript_config.rs'; JS = 'crates/host/src/jsonc.rs'; OUT = 'crates/host/src/outcomes.rs'; TOOL = 'tools/host/typescript_config_vectors.py'
HOST_TEST = ['test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'typescript_config', 'outcomes::tests::every_row_projects_to_its_item_10_termination']
VECTORS = [PY, '-I', '-B', TOOL, '--check', '--architecture', str(A), '--packages-root', str(P)]
MUTATIONS = [
    # (name, file, before, after, gate): the gate must fail on the mutated tree.
    ('jsconfig-default-dropped', TC, '(NodeKind::Jsconfig, None) => Some(true),', '(NodeKind::Jsconfig, None) => None,', 'host'),
    ('later-extends-loses', TC, 'allow_js = a.or(allow_js);', 'allow_js = allow_js.or(a);', 'host'),
    ('own-loses-to-base', TC, 'inherited: (own_allow_js.or(allow_js), file.check_js.or(check_js)),', 'inherited: (allow_js.or(own_allow_js), file.check_js.or(check_js)),', 'host'),
    ('checkjs-derivation-dropped', TC, 'allow_js: allow_js.unwrap_or(check_js),', 'allow_js: allow_js.unwrap_or(false),', 'host'),
    ('json-candidate-first', TC, 'spellings.push(with_json);', 'spellings.insert(0, with_json);', 'host'),
    ('nearest-node-modules-last', TC, '            Ok(out)\n', '            out.reverse();\n            Ok(out)\n', 'host'),
    ('link-skipped', TC, 'ConfigEntry::Link => {\n                    return Err(ConfigRefusal::at(ConfigRefusalKey::ExtendsUnresolved, from));\n                }', 'ConfigEntry::Link => {}', 'host'),
    ('node-bound-off-by-one', TC, 'if self.state.len() == MAX_CONFIG_NODES {', 'if self.state.len() > MAX_CONFIG_NODES {', 'host'),
    ('file-bound-off-by-one', TC, 'if bytes.len() > MAX_CONFIG_FILE_BYTES {', 'if bytes.len() >= MAX_CONFIG_FILE_BYTES {', 'host'),
    ('escape-clamped', TC, 'out.pop()?;', 'out.pop();', 'host'),
    ('uppercase-name-admitted', TC, 'byte.is_ascii_lowercase() || byte.is_ascii_digit()', 'byte.is_ascii_alphanumeric()', 'host'),
    ('empty-document-refused', TC, 'let Some(root) = document.root() else {\n        return Some(file);', 'let Some(root) = document.root() else {\n        return None;', 'host'),
    ('cycle-unchecked', TC, 'Some(Visit::OnPath) => {\n                    return Err(ConfigRefusal::at(ConfigRefusalKey::ExtendsCycle, &path));\n                }', 'Some(Visit::OnPath) => {}', 'host'),
    ('alias-row-altered', TC, '"native.typescript-config-malformed",\n        "native.typescript-config-unresolved",', '"native.typescript-config-malformed",\n        "CONFIG.INVALID",', 'host'),
    ('duplicate-key-first-wins', JS, 'Some(&at) => members[at].1 = done,', 'Some(_) => {}', 'host'),
    ('lone-low-surrogate-accepted', JS, '0xdc00..=0xdfff => return Err(self.error("lone surrogate")),', '0xdc00..=0xdfff => 0xfffd,', 'host'),
    ('bom-refused', JS, 'at: if bytes.starts_with(BOM) { BOM.len() } else { 0 },', 'at: 0,', 'host'),
    # r2 (Codex B2C2-R1-RF-2, RF-3)
    ('null-root-as-empty', TC, 'if !matches!(root, Node::Object(_)) {', 'if !matches!(root, Node::Object(_) | Node::Null) {', 'host'),
    ('edge-merge-uncounted', TC, 'self.work.edge_merges += 1;', '', 'host'),
    ('reference-null-as-empty', TOOL, 'if root is EMPTY:', 'if root is EMPTY or root is None:', 'vectors'),
    ('row-59-remedy-dropped', OUT, 'remedy: Some(REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED),\n            ..Termination::rejected(', 'remedy: None,\n            ..Termination::rejected(', 'host'),
    ('law-expectation-altered', TOOL, "f('b.json', opts(allow=True))], ok(True, False, ['b.json']))\n    case('path-escape-from-root'", "f('b.json', opts(allow=True))], ok(False, False, ['b.json']))\n    case('path-escape-from-root'", 'vectors'),
    ('reference-json-candidate-first', TOOL, "else [segments, segments[:-1] + [segments[-1] + '.json']]", "else [segments[:-1] + [segments[-1] + '.json'], segments]", 'vectors'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b2c2-check-', dir=D)); T.chmod(0o700)
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
    for pkg in ['opensip-host']:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        comparison[pkg] = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    host = comparison['opensip-host']
    rows = [dict(name='host-base-comparison', exitCode=0 if host['equalFailureSets'] and host['candidateSuitesEqualBase'] and host['newPassingTests'] == 8 else 1, niceness=10)]
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '--all-targets', '--', '-D', 'warnings']),
             ('typescript-config-vectors', VECTORS),
             ('discovery-unit-vectors', [PY, '-I', '-B', 'tools/host/discovery_unit_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-fw01', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('test-typescript-config', [R + 'cargo', *HOST_TEST, '--nocapture']),
             ('test-outcomes', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'outcomes::tests', 'invocation_tests']),
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
            if gate == 'host':
                r = subprocess.run([R + 'cargo', *HOST_TEST], cwd=W, env=E, capture_output=True, text=True)
                log = r.stdout + r.stderr
                compiled = 'could not compile' not in log and 'error[E' not in log
                caught = compiled and r.returncode != 0
            else:
                r = subprocess.run(VECTORS, cwd=W, env=E, capture_output=True, text=True)
                log = r.stdout + r.stderr
                caught = r.returncode != 0 and 'generation failed' in log
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
        standing='UNREVIEWED B2-C2 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
