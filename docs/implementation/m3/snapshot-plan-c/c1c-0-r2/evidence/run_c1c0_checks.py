"""C1c-0 r2 candidate checks (the mechanical rebased round in the open C1b batch) (M3-C r8 item 3; C1c plan r4, sub-unit C1c-0: the pruned-tree opener and capture_pruned, the
shared rule's read_set_path, the walk's WalkEvidence, the dependency-tree Cargo marker observation, and the read set's
authorization).

The host and security suites on the base checkout and the candidate (--no-fail-fast; equal failure sets after isolated
reruns, and the new passing tests); rustfmt on the new and base-clean edited files; warning-denied all-targets Clippy on
the two crates; the focused rule, walk and session tests; the charge model --check; the vector moves (only the member
case's prediction, by its one member-root copy; the cases' predictions otherwise equal; the session vectors' predictions
equal); the discovery census, workspace ledger and snapshot census --checks over the lead-readable cache only; the census
closure (exactly discovery_rule.rs changed, as expected); the receipt-specific record (each receipt against its accepted
baseline and current bindings, from public receipt fields only); FW-01; the environment exceptions; the operability source
census; verify_design; and the plan's C1c-0 mutations, each of which must fail its focused tests (or the model --check).
One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1c0'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
WK = 'crates/security/src/snapshot_walk.rs'; RULE = 'crates/security/src/custody/discovery_rule.rs'; RS = 'crates/security/src/snapshot_read_set.rs'; HS = 'crates/host/src/snapshot.rs'
MODEL = 'tools/security/snapshot_ledger_model.py'
VECTORS = 'crates/security/src/snapshot_ledger_vectors.json'; SESSION_VECTORS = 'crates/host/src/snapshot_session_vectors.json'
# The new passing tests per suite: security 11 (four rule tests: the full-path authorization, the dependency-tree Cargo
# root, the pruned capture's place and classify_path's outermost answer; seven walk tests: the pruned opener's charge,
# its custody split, its refusals and its replaced manifest, the walk's evidence, the Cargo marker observation and the
# authorization's charge); host 1 (the pruned capture's read-once and leftover control). Platform is untouched.
NEW_TESTS = {'opensip-host': 1, 'opensip-security': 11}
SERIAL = set()
EXPECTED_CLOSURE_CHANGES = [RULE]
# LD-C1C-13: the one member case gains its member root's copy, owned(1): one object and 1 + RECORD (128) bytes. The
# Cargo roots move: every other case's prediction is unchanged.
EXPECTED_MOVES = {'opensip-anchors-root-and-member': {'objects': 1, 'edges': 0, 'bytes': 129}}
T2 = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
CARGO = [R + 'cargo', 'test', '--locked', '--offline']
FOCUSED = {
    'walk': CARGO + ['-p', 'opensip-security', '--lib', '--', 'snapshot_source', 'snapshot_walk'],
    'rule': CARGO + ['-p', 'opensip-security', '--lib', '--', 'custody::discovery_rule'],
    'census': CARGO + ['-p', 'opensip-security', '--lib', '--', 'custody::discovery_census'],
    'session': CARGO + ['-p', 'opensip-host', '--lib', '--', 'snapshot::tests', 'candidate_custody', 'snapshot_seal'],
}
MUTATIONS = [
    # (name, file, before, after, focus): each weakens one C1c-0 rule; its focused tests (or the model) must fail.
    # LD-C1C-2: custody judged below the anchor; a symlinked component taken as a directory; the rule's VCS check dropped.
    ('custody-below-anchor', RS, "        if index < anchor\n", "        if index < usize::MAX\n", 'walk'),
    ('symlinked-component-followed', RS, "                kind: ChildKind::Directory,\n                ..\n            }\n        ) {\n            return refuse(SnapshotRefusal::NotARegularFile(path.to_owned()));",
     "                kind: ChildKind::Directory | ChildKind::Symlink,\n                ..\n            }\n        ) {\n            return refuse(SnapshotRefusal::NotARegularFile(path.to_owned()));", 'walk'),
    ('pruned-capture-vcs-unchecked', RULE, "        return PrunedCapture::Excluded(ReadSetExclusion::VcsTree);\n", "        return PrunedCapture::Anchor(anchor);\n", 'rule'),
    # LD-C1C-5: the authorization stopping at the outer node_modules, passing a nested one, checking VCS below realPath
    # only, ignoring dependency-tree or first-party Cargo roots, skipping the custody anchors.
    ('read-set-stops-at-outer-node-modules', RULE, "    if parts[base..].contains(&DEPENDENCY_TREE_SEGMENT) {\n", "    if parts.contains(&DEPENDENCY_TREE_SEGMENT) {\n", 'rule'),
    ('read-set-passes-nested-package', RULE, "    if parts[base..].contains(&DEPENDENCY_TREE_SEGMENT) {\n", "    if false {\n", 'rule'),
    ('read-set-vcs-below-only', RULE, "    if parts\n        .iter()\n        .any(|segment| VCS_TREE_SEGMENTS.contains(segment))\n    {\n        return ReadSetPath::Excluded(", "    if parts[base..]\n        .iter()\n        .any(|segment| VCS_TREE_SEGMENTS.contains(segment))\n    {\n        return ReadSetPath::Excluded(", 'rule'),
    ('read-set-dependency-cargo-ignored', RULE, " || dependency_cargo_roots.contains(&prefix)", "", 'rule'),
    ('read-set-first-party-cargo-ignored', RULE, "first_party_cargo_roots.contains(&prefix) || ", "", 'rule'),
    ('read-set-custody-anchor-skipped', RULE, "    if custody_state(&parts, member_roots).is_some() {\n        return ReadSetPath::Excluded(", "    if false {\n        return ReadSetPath::Excluded(", 'rule'),
    # LD-C1C-13: the session's retained Cargo roots dropped; a root dropped at its frame's exit; a key copied instead of
    # moved (the model's move anchor); the member-root copy uncharged.
    ('cargo-roots-not-retained', WK, "            cargo_roots: known,\n", "            cargo_roots: BTreeSet::new(),\n", 'walk'),
    ('cargo-roots-dropped-at-exit', WK, "            drop(levels.pop());\n", "            known.clear();\n            drop(levels.pop());\n", 'walk'),
    ('cargo-key-copied', WK, "            cargo_roots: known,\n", "            cargo_roots: known.clone(),\n", 'model'),
    ('member-copy-uncharged', WK, "        work.charge::<SnapshotStop<E>>(owned(member.len()))?;\n", "", 'walk'),
    # LD-C1C-6: a pruned capture read twice.
    ('pruned-capture-read-twice', HS, "        if !self.captures.contains_key(path) {\n            let source = open_pruned(", "        if true {\n            let source = open_pruned(", 'session'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1c0-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        extra = ['--', '--test-threads=1'] if pkg in SERIAL else []
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg, *extra], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    rows, comparisons = [], {}
    # Preflight: the candidate's test targets build, so a compile error ends the lane before the base suites.
    with (B / 'candidate-build.log').open('wb') as log:
        built = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '--no-run', '-p', 'opensip-host', '-p', 'opensip-security'],
                               cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    rows.append(dict(name='candidate-build', exitCode=built, niceness=10)); print('candidate-build exit', built, flush=True)
    if built != 0:
        (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=False, standing='UNREVIEWED C1c-0 r2 CANDIDATE CHECKS: preflight failed'), indent=2) + '\n')
        raise SystemExit(1)
    for pkg in NEW_TESTS:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        # A test failing on one side only is rerun alone, three times on each side: it is flaky (and not a
        # difference) only if every isolated run passes on both.
        differing = sorted(set(base['failed']) ^ set(cand['failed']))
        flaky = []
        for name in differing:
            runs = []
            for root in (P, W):
                for _ in range(3):
                    r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', pkg, '--lib', '--', '--exact', name, '--test-threads=1'], cwd=root, env=E, capture_output=True)
                    runs.append(r.returncode == 0 and b'1 passed' in r.stdout)
            (B / ('isolated-' + name.replace(':', '_') + '.json')).write_text(json.dumps(dict(test=name, runs=runs), indent=2) + '\n')
            if all(runs):
                flaky.append(name)
        comparison = dict(base=base, candidate=cand, differing=differing, flakyInIsolation=flaky, equalFailureSets=set(base['failed']) - set(flaky) == set(cand['failed']) - set(flaky), candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'] + len([f for f in flaky if f in cand['failed']]) - len([f for f in flaky if f in base['failed']]))
        comparisons[pkg] = comparison
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
        rows.append(dict(name=f'{pkg}-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] == NEW_TESTS[pkg] else 1, niceness=10))
    (B / 'test-comparison.json').write_text(json.dumps(comparisons, indent=2) + '\n')
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
    # The vector moves against the base's records (r9 section 6).
    base_vectors = json.loads(git(W, 'show', 'HEAD:' + VECTORS)); cand_vectors = json.loads((W / VECTORS).read_bytes())
    same_ids = [c['id'] for c in base_vectors['cases']] == [c['id'] for c in cand_vectors['cases']]
    moves = {x['id']: {k: y['predicted'][k] - x['predicted'][k] for k in ('objects', 'edges', 'bytes')}
             for x, y in zip(base_vectors['cases'], cand_vectors['cases']) if x['predicted'] != y['predicted']}
    base_session = json.loads(git(W, 'show', 'HEAD:' + SESSION_VECTORS)); cand_session = json.loads((W / SESSION_VECTORS).read_bytes())
    session_equal = base_session['cases'] == cand_session['cases']
    pruned = cand_vectors.get('prunedOpeners', [])
    vector_ok = same_ids and moves == EXPECTED_MOVES and session_equal and base_vectors['openers'] == cand_vectors['openers'] and len(pruned) == 3 and all(p['exact'] for p in pruned)
    (B / 'vector-moves.json').write_text(json.dumps(dict(sameCases=same_ids, moves=moves, expected=EXPECTED_MOVES, sessionPredictionsEqual=session_equal, prunedOpeners=len(pruned),
                                                        openersEqual=base_vectors['openers'] == cand_vectors['openers'], passed=vector_ok), indent=2) + '\n')
    rows.append(dict(name='vector-moves', exitCode=0 if vector_ok else 1, niceness=10))
    # LD-C1C-9 (r2, R1-RF-3): the receipt-specific record, from public receipt fields only. Each receipt is compared with
    # the batch's accepted baseline (C1a4's refresh), main's bindings (the batch so far, C1b-0's) and the candidate's
    # (C1c-0's own and the cumulative union), every changed binding named; nothing held out is read
    # (receipt_specific_record.py).
    with (B / 'receipt-specific.log').open('wb') as log:
        code = subprocess.run([PY, '-I', '-B', str(Path(__file__).parent / 'receipt_specific_record.py'), str(W), str(P), str(A), str(B / 'receipt-specific.json')],
                              cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    rows.append(dict(name='receipt-specific-record', exitCode=code, niceness=10))
    closure_check = ("import re,sys,subprocess,json;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);expected=" + json.dumps(sorted(EXPECTED_CLOSURE_CHANGES)) + ";print(len(closure),'closure files; hit',hit,'expected',expected);sys.exit(0 if hit==expected and len(closure)>=10 else 1)")
    cache = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2]
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             *[('focused-' + k + '-tests', v) for k, v in FOCUSED.items()],
             ('snapshot-ledger-model', [PY, '-I', '-B', MODEL, '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('retention-cap-evidence', [PY, '-I', '-B', str(Path(__file__).parent / 'retention_cap_evidence.py'), str(W), str(A), str(B / 'retention-cap-evidence.json')]),
             ('discovery-census', [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', *cache]),
             ('discovery-workspace-ledger', [PY, '-I', '-B', 'tools/security/discovery_workspace_ledger.py', '--check', *cache]),
             ('snapshot-ledger-census', [PY, '-I', '-B', 'tools/security/snapshot_ledger_census.py', '--check', *cache]),
             ('discovery-fw01', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('census-closure-changed-as-expected', [PY, '-I', '-B', '-c', closure_check]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, ys, before, after, focus in MUTATIONS:
        path = W / ys; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        try:
            command = [PY, '-I', '-B', MODEL, '--check', '--architecture', str(A), '--packages-root', str(P)] if focus == 'model' else FOCUSED[focus]
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(command, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and 'could not compile' not in out and ('test result: FAILED' in out or (focus == 'model' and 'Snapshot ledger model failed' in out))
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=ys, focus=focus, caught=caught, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C1c-0 r2 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
