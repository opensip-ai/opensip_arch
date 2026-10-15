"""B3-a candidate checks: host and security suites (base and candidate, --no-fail-fast, equal failure sets), warning-denied
all-targets Clippy on host and security, rustfmt on base-clean and new edited files, the tools controls, the operability
census, verify_design, the SLM vector check, the code mutations, the compile-time controls and the planted environment-read
control. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re, sys, shutil
W = Path('/Users/sb/code/opensip-ai/opensip-b3a'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
# r2 (Codex NBO-01): every edited or new Rust file is classified; each one rustfmt-clean at base (or new) must be clean.
G = 'crates/security/src/grants.rs'; PC = 'crates/security/src/custody/project_chain.rs'
T_G = ['test', '-p', 'opensip-security', '--lib', 'grants']
CHECK = ['check', '-p', 'opensip-security', '--lib', '--tests']
AG = '#[derive(Debug, PartialEq, Eq)]\npub(crate) struct AuthorizedGroups {'
PR = '#[derive(Debug, PartialEq, Eq)]\npub(crate) struct PolicyRecordId(String);'
MUTATIONS = [
    (G, T_G, 'ephemeral-not-first', '    if ephemeral {', '    if ephemeral && backup == BackupClassification::BackedUp {'),
    (G, T_G, 'unknown-requires-choice', '        BackupClassification::Unknown => {\n            return StorageWriteChoice::Admit(StorageWriteBasis::UnknownDisclosed);\n        }', '        BackupClassification::Unknown => {}'),
    (G, T_G, 'record-before-flag', '    if acknowledgement.is_some() {', '    if acknowledgement.is_some() && admitted_policy.is_none() {'),
    (G, T_G, 'ci-inverted', '    StorageWriteChoice::Refuse { ci }', '    StorageWriteChoice::Refuse { ci: !ci }'),
    (G, T_G, 'record-uppercase-admitted', "(b'a'..=b'f').contains(b)", 'b.is_ascii_hexdigit()'),
    (G, T_G, 'groups-count-occurrences', '        if provenance.len() > MAX_AUTHORIZED_GROUPS {', '        if gids.len() > MAX_AUTHORIZED_GROUPS {'),
    (G, T_G, 'groups-truncate', '            return Err(GrantRefusal::TooManyGroups {\n                count: provenance.len(),\n            });', '            provenance.truncate(MAX_AUTHORIZED_GROUPS);'),
    (G, T_G, 'waiver-without-project', '            (true, None) => Err(GrantRefusal::OwnerWaiverWithoutExplicitProject),', '            (true, None) => Ok(None),'),
    (G, T_G, 'module-does-io', '#[cfg(test)]\n#[path = "grants_tests.rs"]', 'fn _planted() -> bool {\n    std::fs::metadata("/").is_ok()\n}\n\n#[cfg(test)]\n#[path = "grants_tests.rs"]'),
    # r2: r1's planted line was a function taking a record, not an impl for one, so the pin rightly ignored it.
    (PC, T_G, 'foreign-impl', "pub(crate) struct ProjectChainPolicy<'a> {", "impl crate::grants::AuthorizedGroups {\n    pub(crate) fn planted(&self) {}\n}\n\npub(crate) struct ProjectChainPolicy<'a> {"),
]
# Compile-time controls: each forbidden impl must fail the test build with the probe's ambiguity (E0283).
COMPILE = [
    (G, CHECK, 'derive-clone', AG, AG.replace('Debug,', 'Debug, Clone,')),
    (G, CHECK, 'derive-default', PR, PR.replace('Debug,', 'Debug, Default,')),
    (G, CHECK, 'impl-from-str', '/// The workflow contract', 'impl std::str::FromStr for PolicyRecordId {\n    type Err = GrantRefusal;\n    fn from_str(text: &str) -> Result<Self, GrantRefusal> {\n        Self::parse(text)\n    }\n}\n\n/// The workflow contract'),
    (G, CHECK, 'impl-from-bool', '/// An admitted storage-policy', 'impl From<bool> for BackupCustodyAcknowledgement {\n    fn from(_: bool) -> Self {\n        Self { _invocation: () }\n    }\n}\n\n/// An admitted storage-policy'),
]
PLANTED = [
    (G, ['clippy', '-p', 'opensip-security', '--lib', '--', '-D', 'warnings'], 'planted-grants-read', '    pub(crate) fn from_invocation(gids: &[u32]) -> Result<Self, GrantRefusal> {\n', '    pub(crate) fn from_invocation(gids: &[u32]) -> Result<Self, GrantRefusal> {\n        let _planted = std::env::var_os("OPENSIP_PLANTED");\n'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b3a-check-', dir=D)); T.chmod(0o700)
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
             ('storage-choice-vectors', [PY, '-I', '-B', 'tools/security/storage_choice_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
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
        standing='UNREVIEWED B3-a CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
