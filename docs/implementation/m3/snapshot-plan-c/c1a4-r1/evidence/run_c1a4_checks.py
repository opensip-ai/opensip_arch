"""C1a4 r1 candidate checks (M3-C r8 item 2 as M3-C r9 amends it; C1a plan r6, C1a4: the snapshot ledger's caps, their
lead-readable T2 margins and the constructor, with r9's classification remedies (a) and (b-prime)).

The host, security and platform suites on the base checkout and the candidate (--no-fail-fast; equal failure sets after
isolated reruns, and the new passing tests); rustfmt on the new and base-clean edited files; warning-denied all-targets
Clippy on the three crates; the focused walk, rule, census, ledger, session and sealing tests, and the 4 GiB payload
probe on the snapshot profile; the charge model --check; the vector moves (only `opensip-anchors-root-and-member`'s
prediction, by r9's -12 objects and -1,726 bytes; the session vectors byte-equal); the discovery census, workspace ledger
and snapshot census --checks over the lead-readable cache only; the census closure (exactly work_ledger.rs and
discovery_rule.rs changed, as expected) and the held-out receipt (byte-equal to the base, and stale in the regenerated
census record: the reviewed blind refresh is a separate unit); FW-01; the environment exceptions; the operability source
census; verify_design; and mutations of (a), (b-prime) and the profile, each of which must fail its focused tests. One
lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1a4'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
WK = 'crates/security/src/snapshot_walk.rs'; RULE = 'crates/security/src/custody/discovery_rule.rs'; LEDGER = 'crates/platform/src/work_ledger.rs'
MODEL = 'tools/security/snapshot_ledger_model.py'
VECTORS = 'crates/security/src/snapshot_ledger_vectors.json'; SESSION_VECTORS = 'crates/host/src/snapshot_session_vectors.json'
CENSUS_RECORD = 'crates/security/src/custody/discovery_census.json'; RECEIPT = 'crates/security/src/custody/discovery_census_held_out.json'
# The new passing tests per suite: security 3 (the multi-segment member root, the custody-state allocation pin and the
# snapshot census margin), platform 1 (C1-T27 on the snapshot profile), host none.
NEW_TESTS = {'opensip-host': 0, 'opensip-security': 3, 'opensip-platform': 1}
# The platform lib suite races under parallel test threads at base (an IO-safety abort, path_binding failures), so it
# runs serially on both sides, as D1a's lane of record and B2-b1 r2 do (supervisor-d/d1a-r1/evidence/
# base-platform-flakiness.md). Attempt 1 of this lane hit the abort on the candidate side.
SERIAL = {'opensip-platform'}
EXPECTED_CLOSURE_CHANGES = [LEDGER, RULE]
EXPECTED_MOVES = {'opensip-anchors-root-and-member': {'objects': -12, 'edges': 0, 'bytes': -1726}}
T2 = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
CARGO = [R + 'cargo', 'test', '--locked', '--offline']
FOCUSED = {
    'walk': CARGO + ['-p', 'opensip-security', '--lib', '--', 'snapshot_source', 'snapshot_walk'],
    'rule': CARGO + ['-p', 'opensip-security', '--lib', '--', 'custody::discovery_rule'],
    'census': CARGO + ['-p', 'opensip-security', '--lib', '--', 'custody::discovery_census'],
    'ledger': CARGO + ['-p', 'opensip-platform', '--lib', '--', 'work_ledger', '--test-threads=1'],
    'session': CARGO + ['-p', 'opensip-host', '--lib', '--', 'snapshot::tests', 'candidate_custody', 'snapshot_seal'],
}
PROBE = CARGO + ['-p', 'opensip-host', '--lib', '--', '--ignored', '--exact',
                 'snapshot::tests::a_four_gibibyte_stream_is_charged_only_its_buffer_and_its_read_attempts', '--test-threads=1']
MUTATIONS = [
    # (name, file, before, after, focused tests): each weakens one C1a4 rule; its focused tests must fail.
    # (a): the recorded `.opensip` classified again (the native walk then charges more than the model predicts).
    ('opensip-classified-twice', WK, "            Some((_, pruned)) => pruned,\n",
     "            Some((_, _)) => {\n                work.charge::<SnapshotStop<E>>(classify_cost(&rel))?;\n"
     "                rule::classify_path(&rel, &known, extent.member_roots).is_some()\n            }\n", 'walk'),
    # (a): the recorded classification misread (a kept `.opensip` excluded).
    ('opensip-reuse-misread', WK, "            Some((_, pruned)) => pruned,\n", "            Some((_, _)) => true,\n", 'walk'),
    # (a): the classification recorded for the wrong child.
    ('opensip-recorded-off-by-one', WK, "OpensipName::Classified { pruned } => opensip = Some((index, pruned)),",
     "OpensipName::Classified { pruned } => opensip = Some((index + 1, pruned)),", 'walk'),
    # (b-prime): a member root's segments collected again.
    ('custody-state-collects', RULE, "            && (base.is_empty() || parts[..k].iter().copied().eq(base.split('/')))\n",
     "            && (base.is_empty() || parts[..k] == base.split('/').collect::<Vec<_>>()[..])\n", 'rule'),
    # (b-prime): only a member root's first segment compared.
    ('custody-state-first-segment-only', RULE, "            && (base.is_empty() || parts[..k].iter().copied().eq(base.split('/')))\n",
     "            && (base.is_empty() || base.split('/').next() == Some(parts[0]))\n", 'rule'),
    # The profile: a cap off by a power of two, and a discovery cap borrowed.
    ('profile-edges-doubled', LEDGER, "const SNAPSHOT_EDGE_LIMIT: usize = 1 << 24;\n", "const SNAPSHOT_EDGE_LIMIT: usize = 1 << 25;\n", 'ledger'),
    ('profile-bytes-halved', LEDGER, "const SNAPSHOT_BYTE_LIMIT: usize = 1 << 33;\n", "const SNAPSHOT_BYTE_LIMIT: usize = 1 << 32;\n", 'ledger'),
    ('profile-objects-borrowed', LEDGER, "                objects: SNAPSHOT_OBJECT_LIMIT,\n", "                objects: DISCOVERY_OBJECT_LIMIT,\n", 'ledger'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1a4-check-', dir=D)); T.chmod(0o700)
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
        built = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '--no-run', '-p', 'opensip-host', '-p', 'opensip-security', '-p', 'opensip-platform'],
                               cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    rows.append(dict(name='candidate-build', exitCode=built, niceness=10)); print('candidate-build exit', built, flush=True)
    if built != 0:
        (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=False, standing='UNREVIEWED C1a4 r1 CANDIDATE CHECKS: preflight failed'), indent=2) + '\n')
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
    session_equal = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + SESSION_VECTORS], cwd=W, env=E, capture_output=True).stdout == (W / SESSION_VECTORS).read_bytes()
    vector_ok = same_ids and moves == EXPECTED_MOVES and session_equal and base_vectors['openers'] == cand_vectors['openers']
    (B / 'vector-moves.json').write_text(json.dumps(dict(sameCases=same_ids, moves=moves, expected=EXPECTED_MOVES, sessionVectorsByteEqual=session_equal,
                                                        openersEqual=base_vectors['openers'] == cand_vectors['openers'], passed=vector_ok), indent=2) + '\n')
    rows.append(dict(name='vector-moves', exitCode=0 if vector_ok else 1, niceness=10))
    # The held-out receipt is untouched, and the regenerated census record holds every held-out row stale.
    receipt_equal = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + RECEIPT], cwd=W, env=E, capture_output=True).stdout == (W / RECEIPT).read_bytes()
    record = json.loads((W / CENSUS_RECORD).read_bytes())
    held = [e for e in record['entries'] if 'status' in e and isinstance(e['status'], str) and e['status'].startswith('outstanding')]
    stale_ok = receipt_equal and held and all(e['status'] == 'outstanding: held-out (blind receipt stale)' for e in held) and record['heldOutMargin'] == 'outstanding'
    (B / 'held-out-receipt.json').write_text(json.dumps(dict(receiptByteEqualBase=receipt_equal, heldOutRows=len(held), allStale=stale_ok,
                                                             heldOutMargin=record['heldOutMargin'], standing='expected: C1a4 makes the blind receipt stale; the reviewed blind refresh is a separate unit'), indent=2) + '\n')
    rows.append(dict(name='held-out-receipt-stale-as-expected', exitCode=0 if stale_ok else 1, niceness=10))
    closure_check = ("import re,sys,subprocess,json;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);expected=" + json.dumps(sorted(EXPECTED_CLOSURE_CHANGES)) + ";print(len(closure),'closure files; hit',hit,'expected',expected);sys.exit(0 if hit==expected and len(closure)>=10 else 1)")
    cache = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2]
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '-p', 'opensip-platform', '--all-targets', '--', '-D', 'warnings']),
             *[('focused-' + k + '-tests', v) for k, v in FOCUSED.items()],
             ('payload-4gib-probe', PROBE),
             ('snapshot-ledger-model', [PY, '-I', '-B', MODEL, '--check', '--architecture', str(A), '--packages-root', str(P)]),
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
        if name == 'payload-4gib-probe' and code == 0:
            code = 0 if b'1 passed' in (B / (name + '.log')).read_bytes() else 1
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, ys, before, after, focus in MUTATIONS:
        path = W / ys; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(FOCUSED[focus], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and 'could not compile' not in out and 'test result: FAILED' in out
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=ys, focus=focus, caught=caught, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C1a4 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
