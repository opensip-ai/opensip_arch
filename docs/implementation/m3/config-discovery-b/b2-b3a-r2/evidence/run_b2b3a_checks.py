"""B2-b3a candidate checks: host and security suites (base and candidate, --no-fail-fast, equal failure sets), the B1-b legacy
admission spend probe (base and candidate, equal lines), warning-denied all-targets Clippy on host and security, rustfmt on
base-clean and new edited files, the tools controls, the operability census, verify_design, both current-reference vector
checks (B2-b2's scan and B2-b3a's upward), and the code mutations. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re, sys, shutil
W = Path('/Users/sb/code/opensip-ai/opensip-b2b3a'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
# r2 (Codex NBO-01): every edited or new Rust file is classified; each one rustfmt-clean at base (or new) must be clean.
PA = 'crates/security/src/custody/project_admission.rs'; PC = 'crates/security/src/custody/project_chain.rs'; IR = 'crates/security/src/custody/installation_read.rs'
T_A = ['test', '-p', 'opensip-security', '--lib', '--', 'custody::project_admission::tests::', 'custody::discovery_scan::']
MUTATIONS = [
    (PA, T_A, 'analysis-config-in-shared-order', 'CustodyOrder::Reference\n    } else {', 'CustodyOrder::Shared\n    } else {'),
    (PC, T_A, 'reference-order-links-and-size-before-acl', '        links: 1,\n        size: 0,\n', '        links: metadata.links,\n        size: metadata.size,\n'),
    (PA, T_A, 'refused-config-row-kept-absent', 'last_row(record, |row| row.candidate = Candidate::Refused);', 'last_row(record, |row| row.candidate = Candidate::Absent);'),
    (PA, T_A, 'custody-boundary-dropped', 'Some(RowBoundary::Custody(why)),', 'None,'),
    (PA, T_A, 'config-vcs-not-probed', 'vcs_evidence(directory, uid, policy, work)?\n            } else {', 'None\n            } else {'),
    (PA, T_A, 'home-boundary-dropped', 'last_row(&mut record, |row| row.boundary = Some(RowBoundary::Home));', 'last_row(&mut record, |_| {});'),
    # r2: the link and size bounds are custody's now; `gitdir-custody-ignored` below covers them.
    (PA, T_A, 'gitdir-identity-unchecked', 'if !observation.matches(&opened) {', 'if false {'),
    (PA, T_A, 'gitdir-any-git-file-kind-read', 'ChildKind::File if marker == ".git" =>', 'ChildKind::File | ChildKind::Symlink if marker == ".git" =>'),
    (PA, T_A, 'explicit-waiver-ignored', 'let waiver = applicable_waiver(waiver, explicit);', 'let waiver: Option<&ProjectOwnerWaiver> = waiver.and(None);'),
    (PC, T_A, 'waiver-not-spelling-bound', 'waiver.filter(|w| w.explicit_root().as_os_str() == root.as_os_str())', 'waiver.filter(|_| true)'),
    (PC, T_A, 'chain-waiver-forgotten', 'owner_waived: waiver.is_some(),', 'owner_waived: false,'),
    (PA, T_A, 'config-refusal-names-the-directory', 'refused_at(record, &path.join(CONFIG_FILE), work)?;', 'refused_at(record, path, work)?;'),
    (PA, T_A, 'explicit-absent-as-root-custody', 'let refusal = if explicit {', 'let refusal = if false {'),
    # r2 (Codex B2B3A-R1-RF-1, NBO-1, NBO-2)
    (PA, T_A, 'gitdir-custody-ignored', ')) => return Ok(None),', ')) => opened.clone(),'),
    (PA, T_A, 'gitdir-bare-cr-stripped', ".or_else(|| line.strip_suffix('\\n'))", ".or_else(|| line.strip_suffix(['\\n', '\\r']))"),
    (PA, T_A, 'selection-guard-dropped', 'let path = self.refused.as_deref()?;', 'let path = self.refused.as_deref().unwrap_or(Path::new("/"));'),
    (IR, T_A, 'release-keeps-the-fence', 'let released = observation.release();', 'let released: io::Result<()> = {\n            std::mem::forget(observation);\n            Ok(())\n        };'),
]
COMPILE = []
PLANTED = []
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b2b3a-check-', dir=D)); T.chmod(0o700)
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
    def probe(root, tag):
        r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', 'b1b_legacy_spend_probe', '--', '--ignored', '--nocapture', '--test-threads=1'], cwd=root, env=E, capture_output=True, text=True)
        (B / f'legacy-probe-{tag}.log').write_text(r.stdout + r.stderr)
        # r2: the first line follows the harness's `test ... ` prefix on the same line.
        return r.returncode, re.findall(r'B1B-LEGACY:\S+', r.stdout)
    (bc, bl), (cc, cl) = probe(P, 'base'), probe(W, 'candidate')
    legacy = dict(baseExit=bc, candidateExit=cc, base=bl, candidate=cl, equal=bl == cl and len(bl) == 5)
    (B / 'legacy-probe.json').write_text(json.dumps(legacy, indent=2) + '\n'); print('legacy probe equal', legacy['equal'], flush=True)
    rows = [dict(name='legacy-admission-spend-equal', exitCode=0 if legacy['equal'] and bc == 0 and cc == 0 else 1, niceness=10)]
    rows += [dict(name='host-security-base-comparison', exitCode=0 if all(c['equalFailureSets'] and c['candidateSuitesEqualBase'] and c['newPassingTests'] >= (1 if k == 'opensip-security' else 0) for k, c in comparison.items()) else 1, niceness=10)]
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines() if x.endswith('.rs'))
    def fmt_clean(path):
        return subprocess.run([R + 'rustfmt', '--edition', '2024', '--check', str(path)], env=E, capture_output=True).returncode == 0
    fmt_rows = [dict(path=x, baseClean=None if not (P / x).exists() else fmt_clean(P / x), candidateClean=fmt_clean(W / x)) for x in edited]
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    FMT = [r['path'] for r in fmt_rows if r['baseClean'] is not False]
    steps = [('rustfmt-edited', [R + 'rustfmt', '--edition', '2024', '--check', *FMT]),
             ('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('discovery-scan-vectors', [PY, '-I', '-B', 'tools/security/discovery_scan_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-upward-vectors', [PY, '-I', '-B', 'tools/security/discovery_upward_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
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
        standing='UNREVIEWED B2-b3a CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
