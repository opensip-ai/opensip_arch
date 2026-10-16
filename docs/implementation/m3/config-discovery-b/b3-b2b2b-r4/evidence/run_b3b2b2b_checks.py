"""B3-b2b2b r4 candidate checks (the native workspace observation and the D15 discovery composition; B3-b plan r2
amendments A3 and A4): the security suite on the base checkout and the candidate (--no-fail-fast, equal failure sets, the new
passing tests counted), the
host's scenario-driven discovery tests at base and candidate, rustfmt on new and base-clean edited files (stdin mode),
warning-denied all-targets Clippy on security and on security with scenario-fixtures, the composition vectors and every
discovery vector check, the FW-01 pin, the walk-storage and census-tool controls, the census (--check over the integrity-verified
lead-readable T2 stores, held-out entries never opened), the equality projection for the discovery_walk.rs and custody.rs closure
re-pins, the environment exceptions, the operability source census, verify_design, and mutation controls (each patches the
observation, the decision core or the composition, and the workspace tests must fail). One lane hold, nice 10, private
TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b3b2b2b'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
OB = 'crates/security/src/custody/workspace_observation.rs'; CO = 'crates/security/src/custody/workspace_discovery.rs'
WD = 'crates/security/src/custody/workspace_declarations.rs'; WK = 'crates/security/src/custody/discovery_walk.rs'; SC = 'crates/security/src/custody/discovery_scan.rs'
CENSUS_JSON = 'crates/security/src/custody/discovery_census.json'; CENSUS_VECTORS = 'crates/security/src/custody/discovery_census_vectors.json'
TEST = ['test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'workspace_discovery']
# r3: the decision core's mutations are judged by its own vectors too.
GATE = ['test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'workspace_', 'git_tracking']
NEW_TESTS = 14
GT = 'crates/security/src/custody/git_tracking.rs'
ARCHIVES = '/Users/sb/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f'
IDENTITY = lambda root: [PY, '-I', '-B', 'tools/check_identity_dependencies.py', '--manifest', str(root / 'Cargo.toml'), '--target', 'aarch64-apple-darwin',
                         '--cargo', R + 'cargo', '--archives', ARCHIVES, '--policy', str(root / 'tools/identity/dependency-policy.json')]
VEC = lambda tool: [PY, '-I', '-B', 'tools/security/' + tool, '--check', '--architecture', str(A), '--packages-root', str(P)]
MUTATIONS = [
    # (name, file, before, after): the workspace_discovery tests must fail on the mutated tree.
    ('acl-never-captured', OB, 'judge_entry(Some(entry), object, uid, groups, waiver) == EntryJudgment::NeedsAcl', 'false'),
    ('git-marker-missed', OB, 'found.push((marker, kind == ChildKind::Directory))', 'if marker != ".git" { found.push((marker, kind == ChildKind::Directory)) }'),
    ('listing-dropped', OB, ".map(|p| p.rsplit('/').next().unwrap_or_default().to_owned())", ".filter(|_| false).map(|p| p.rsplit('/').next().unwrap_or_default().to_owned())"),
    ('verdict-subject-dropped', OB, 'MemberVerdict::Refused(refusal) => MemberOutcome::Refused(refusal.subject()),', 'MemberVerdict::Refused(_) => MemberOutcome::Refused("member-refused".to_owned()),'),
    ('precondition-ignored', CO, 'no_repository: members.is_some(),', 'no_repository: true,'),
    ('refusal-path-unspelled', CO, 'path: Some(spelled(&root_abs, &path)),', 'path: Some(path),'),
    ('member-rows-unspelled', CO, 'path: spelled(&root_abs, &m.path),', 'path: m.path.clone(),'),
    ('declaration-paths-unspelled', CO, 'row.path = row.path.map(|p| spelled(&root_abs, &p));', ''),
    ('scope-limit-d9-altered', CO, 'code: "REQUEST.UNSATISFIABLE",', 'code: "CONFIG.INVALID",'),
    ('member-refusal-rows-dropped', CO, 'match record(walked, Vec::new(), spell_rows(declarations), false) {', 'match record(walked, Vec::new(), Vec::new(), false) {'),
    # r3 (A4-2): branch A's one walk, with its admitted members and their gitlinks.
    ('walk-without-members', CO, 'let walked = walk(&roots, &gitlinks, work)?;\n            hook("after-walk", "");', 'let walked = walk(&none, &gitlinks, work)?;\n            hook("after-walk", "");'),
    ('branch-a-walk-without-gitlinks', CO, 'let walked = walk(&roots, &gitlinks, work)?;\n            hook("after-walk", "");', 'let walked = walk(&roots, &none, work)?;\n            hook("after-walk", "");'),
    ('walk-refusal-keeps-members', CO, 'spell_rows(admitted.declarations()),\n                        false,', 'spell_rows(admitted.declarations()),\n                        true,'),
    ('walk-refusal-rows-dropped', CO, 'spell_rows(admitted.declarations()),\n                        false,', 'Vec::new(),\n                        false,'),
    # r3 (A4-2 step 1): the array gate.
    ('grammar-gate-skipped', WD, '.find(|spec| rule::normalize_explicit_root(spec).is_err())', '.find(|_| false)'),
    ('size-gate-skipped', WD, 'if inputs.array.len() > rule::MAX_WORKSPACE_UNITS {', 'if false {'),
    ('gate-path-spelled', CO, '                    path,\n                    detail: detail.to_owned(),', '                    path: path.map(|p| spelled(&root_abs, &p)),\n                    detail: detail.to_owned(),'),
    ('gate-detail-not-per-source', WD, 'Self::ConfigWorkspaceRoots => "TOO_MANY_WORKSPACE_ROOTS",', 'Self::ConfigWorkspaceRoots => "TOO_MANY_JOINS",'),
    # r2 (Codex B3B2B2B-R1-RF-1): index gitlinks.
    ('walker-gitlinks-ignored', WK, '|| self.gitlinks.contains(&rel))', ')'),
    ('core-gitlinks-ignored', SC, '(entry.vcs.is_some() || inv.gitlinks.contains(rel))', 'entry.vcs.is_some()'),
    ('links-below-gitlinks', WD, 'if p.inner || below_gitlink {', 'if p.inner {'),
    ('branch-b-walk-without-gitlinks', CO, '                    hook("before-walk", "");\n                    walk(&roots, &gitlinks, work)?', '                    hook("before-walk", "");\n                    walk(&roots, &none, work)?'),
    # r2 (RF-2, RF-3): the object bindings.
    ('binding-mismatch-ignored', OB, 'Some(seen) if !same_object(&seen, metadata) => Err(changed(rel)),', 'Some(seen) if false && !same_object(&seen, metadata) => Err(changed(rel)),'),
    ('walker-binding-ignored', WK, 'Some(seen) if !same_object(&seen, metadata) => Err(self.changed(rel)),', 'Some(seen) if false && !same_object(&seen, metadata) => Err(self.changed(rel)),'),
    # r3 (Codex B3B2B2B-R2-RF-2): every object item 6b opened is bound: the member, its ancestors and its Git evidence,
    # each comparison mutated on its own.
    ('item-6b-identities-ignored', OB, 'for (rel, metadata) in &identities {', 'for (rel, metadata) in identities.iter().filter(|_| false) {'),
    ('item-6b-ancestors-ignored', OB, 'for (rel, metadata) in &identities {', 'for (rel, metadata) in identities.iter().filter(|(rel, _)| rel.as_slice() == candidate.as_bytes() || rel.starts_with(format!("{candidate}/").as_bytes())) {'),
    ('item-6b-git-evidence-ignored', OB, 'for (rel, metadata) in &identities {', 'for (rel, metadata) in identities.iter().filter(|(rel, _)| !rel.starts_with(format!("{candidate}/").as_bytes())) {'),
    ('item-6b-member-ignored', OB, 'for (rel, metadata) in &identities {', 'for (rel, metadata) in identities.iter().filter(|(rel, _)| rel.as_slice() != candidate.as_bytes()) {'),
    # r3 (RF-3): a provider read repeated within a phase is served from the validated read.
    ('read-cache-disabled', OB, 'if let Some(kept) = self.read.get(rel) {', 'if let Some(kept) = None::<&FileBytes> {'),
    # r3 round 2 (Codex B3B2B2B-R3-RF-1, RF-2): copies and identity records are charged before they are built.
    ('kept-copy-before-charge', OB, 'if let FileBytes::Read(raw) = kept {\n        work.charge::<WorkspaceRefusal>(owned(raw.len()))?;\n    }\n    trace("copy-kept", "");\n    Ok(kept.clone())',
     'let copy = kept.clone();\n    trace("copy-kept", "");\n    if let FileBytes::Read(raw) = kept {\n        work.charge::<WorkspaceRefusal>(owned(raw.len()))?;\n    }\n    Ok(copy)'),
    ('kept-copy-uncharged', OB, '        work.charge::<WorkspaceRefusal>(owned(raw.len()))?;\n    }\n    trace("copy-kept", "");', '        let _ = raw;\n    }\n    trace("copy-kept", "");'),
    ('identity-built-before-charge', GT, '    work.charge(identity_cost(len)).map_err(member_failure)?;\n    let path = path();', '    let path = path();\n    work.charge(identity_cost(len)).map_err(member_failure)?;'),
    ('identity-uncharged', GT, '    work.charge(identity_cost(len)).map_err(member_failure)?;\n    let path = path();', '    let path = path();'),
    # r2 (RF-4): the custody-bound read.
    ('post-read-check-dropped', OB, 'if sample != judged.metadata || again.metadata != judged.metadata || again.acl != judged.acl\n        {', 'if false\n        {'),
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
    T = Path(tempfile.mkdtemp(prefix='opensip-b3b2b2b-check-', dir=D)); T.chmod(0o700)
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
    rows = [dict(name='security-base-comparison', exitCode=0 if host['equalFailureSets'] and host['candidateSuitesEqualBase'] and host['newPassingTests'] == NEW_TESTS else 1, niceness=10)]
    # The equality projection (plan r2 section 4.2, A1-2): base and candidate census records differ only in the
    # discovery_walk.rs, discovery_scan.rs and custody.rs closure rows; the held-out rows are already outstanding at the base
    # and stay so.
    projection = {}
    for rel in (CENSUS_JSON, CENSUS_VECTORS):
        base_doc = json.loads(git(P, 'show', 'HEAD:' + rel)); cand_doc = json.loads((W / rel).read_text())
        changed = diff(base_doc, cand_doc)
        held = {i for i, e in enumerate(base_doc.get('entries', [])) if e.get('status') == 'blind-census'}
        allowed = [p for p in changed if re.fullmatch(r'/closure/(0|4|6)/(bytes|sha256)', p)]
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('clippy-scenario', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--features', 'scenario-fixtures', '--all-targets', '--', '-D', 'warnings']),
             ('test-workspace-discovery', [R + 'cargo', *TEST, '--nocapture']),
             ('test-discovery-and-members', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'discovery_', 'workspace_declarations', 'git_tracking']),
             ('host-scenario-discovery', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'discovery_flag_tests']),
             ('workspace-discovery-vectors', VEC('workspace_discovery_vectors.py')),
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
        standing='UNREVIEWED B3-B2B2B r4 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
