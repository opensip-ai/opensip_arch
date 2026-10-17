"""D2b-3b r2 candidate checks (D2b plan r3 as amendments A1 and A2 amend it: the TS2 send side and participant):
- the components, identity and contracts suites on the base checkout (main) and the candidate (--no-fail-fast; equal
  failure sets after isolated reruns, and the new passing tests), with D3a's fixture record written beside each side's
  lib test binary first (LD-D3A-9's lane step, as run_d3a2_checks.py does), so the supervisor's tests run on both;
- rustfmt on the new and base-clean edited files, and warning-denied all-targets Clippy on contracts and components;
- the focused TS2 tests;
- section 3's duty table against the carriers' admission list, with D2b-3b's builder and sender rows named
  (check_d2b3b_duty_table.py);
- the operability source census, the environment exceptions, the census-closure check and verify_design;
- mutations, each of which must fail the focused tests.
One lane hold, nice 10, private TMPDIR. (Adapted from run_d2b3a_checks.py and run_d3a2_checks.py.)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys, hashlib
W = Path('/Users/sb/code/opensip-ai/opensip-d2b3b-r2'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = A / 'docs/implementation/m3/supervisor-d/d2b-3b-r2/evidence'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
SEND = 'crates/components/src/provider_protocol/ts2/send.rs'
PART = 'crates/components/src/provider_protocol/ts2/participant.rs'
# The new passing tests per suite: components 19 (r1's 15; r2's RF-1 latching control, the spool and discard, the
# pre-Analyze boundary, and the host pipe ends); none elsewhere.
NEW_TESTS = {'opensip-components': 19, 'opensip-identity': 0, 'opensip-contracts': 0}
SERIAL = set()
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-components', '--lib', '--', 'provider_protocol::ts2']
MUTATIONS = [
    # (name, file, before, after): each weakens one send-side rule; the focused tests must fail.
    # A2-3: a limits member changed (the Hello's limits, which the TS2 HelloAck does not echo).
    ('limits-member-changed', SEND,
     '                    law.limits\n                        .iter()\n                        .map(|(n, v)| (n.clone(), Value::Unsigned(*v)))',
     '                    law.limits\n                        .iter()\n                        .map(|(n, v)| (n.clone(), Value::Unsigned(*v + u64::from(n == "maxStderrBytes"))))'),
    ('payload-digest-unchecked', SEND, '        if raw_sha256(&cbor::encode(&digest_over)) != slot.payload_sha256 {', '        if false {'),
    ('chunk-content-unchecked', SEND, '                    if &digest_hex(&RawSha256::finish(digest)) != want {',
     '                    if false && &digest_hex(&RawSha256::finish(digest)) != want {'),
    ('cancel-echo-unchecked', SEND, '        if cbor::encode(&payload) != cbor::encode(&want) {', '        if false && cbor::encode(&payload) != cbor::encode(&want) {'),
    ('cancel-before-hello', SEND, '        if !self.hello_sent() || self.cancelled || self.refused {', '        if self.cancelled || self.refused {'),
    ('budget-range-unchecked', SEND, '            if budget.iter().any(|(_, v)| *v == 0 || *v > i64::MAX as u64) {', '            if false {'),
    ('stage-ordinal-not-analyze-relative', SEND, '                ("stageOrdinal", Value::Unsigned(ordinal as u64)),',
     '                ("stageOrdinal", Value::Unsigned(ordinal as u64 + 1)),'),
    ('universe-key-not-recomputed', SEND, '                &hash_canonical_value(UNIVERSE_DOMAIN, inputs)',
     '                &hash_canonical_value("native.semantic-universe.syntax.v2", inputs)'),
    ('send-gate-removed', PART, '                Some(slot) if self.receiver.admits(&slot_frame(slot.frame)) => {', '                Some(_) => {'),
    ('host-fault-reported-as-protocol', PART, '            return ParticipantStatus::HostFault;', '            return ParticipantStatus::Fault;'),
    ('context-request-joins-unchecked', PART, '        joins(&context, &request).map_err(Ts2Refusal::Context)?;\n', ''),
    # r2: Codex D2B3B-R1-RF-1 (checklist item 7) and D3a-3's seam.
    ('source-failure-unlatched', SEND, '            Err(r) => Err(self.refuse(r)),\n        }\n    }\n\n    fn realize(',
     '            Err(r) => Err(r),\n        }\n    }\n\n    fn realize('),
    ('cancel-before-hello-unlatched', SEND, '            return Err(self.refuse(r));\n        };', '            return Err(r);\n        };'),
    ('candidate-not-spooled', PART, '                                        self.spool.push(c);\n', ''),
    ('discard-keeps-the-output', PART, '        self.spool = Spool::default();\n        self.output = None;\n', '        self.spool = Spool::default();\n'),
    ('context-boundary-dropped', PART, '                                    self.boundaries.push(Boundary::ContextVerified);\n', ''),
    ('zero-write-is-progress', PART, '                Ok(0) => self.host_fault = true,\n', ''),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d2b3b-r2-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # Main may have moved while this runner waited: the worktree follows it only if nothing that moved touches a
    # candidate path, and the candidate's bytes are unchanged by the move.
    assert git(P, 'status', '--porcelain') == ''
    head, main = git(W, 'rev-parse', 'HEAD'), git(P, 'rev-parse', 'HEAD')
    mine = sorted(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
    moved = None
    if head != main:
        theirs = set(git(P, 'diff', '--name-only', head, main).splitlines())
        assert not theirs & set(mine), sorted(theirs & set(mine))
        before = {x: (W / x).read_bytes() for x in mine}
        git(W, 'checkout', '-q', '--detach', main)
        assert {x: (W / x).read_bytes() for x in mine} == before
        moved = dict(fromHead=head, toHead=main, mainChangedPaths=sorted(theirs)); print('worktree moved onto main', main, flush=True)
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD')
    (B / 'worktree-base.json').write_text(json.dumps(dict(productBase=main, moved=moved, candidatePaths=mine), indent=2) + '\n')
    for name, ys, before, after in MUTATIONS: assert (W / ys).read_text().count(before) == 1, name
    def fixture_record(root, tag):
        """Build the components tests, then write the fixture's exact artifact and digest beside the lib test binary."""
        for old in (root / 'target/debug/deps').glob('supervisor_fixture.path'):
            old.unlink()
        r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '--no-run', '--message-format=json', '-p', 'opensip-components'], cwd=root, env=E, capture_output=True)
        (B / f'fixture-build-{tag}.log').write_bytes(r.stderr)
        if r.returncode != 0:
            return None
        fixture = lib = None
        for raw in r.stdout.splitlines():
            try: msg = json.loads(raw)
            except ValueError: continue
            if msg.get('reason') != 'compiler-artifact' or not msg.get('executable'):
                continue
            if msg['target']['name'] == 'supervisor_fixture':
                fixture = Path(msg['executable'])
            elif msg['target']['name'] == 'opensip_components' and 'lib' in msg['target']['kind'] and msg['profile']['test']:
                lib = Path(msg['executable'])
        assert fixture and lib, (fixture, lib)
        digest = hashlib.sha256(fixture.read_bytes()).hexdigest()
        record = lib.parent / 'supervisor_fixture.path'
        record.write_text(f'{fixture}\n{digest}\n')
        return dict(fixture=str(fixture), sha256=digest, record=str(record))
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        extra = ['--', '--test-threads=1'] if pkg in SERIAL else []
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg, *extra], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    rows, comparisons = [], {}
    base_record = fixture_record(P, 'base'); assert base_record, 'the base builds'
    record = fixture_record(W, 'candidate')
    (B / 'fixture-record.json').write_text(json.dumps(dict(base=base_record, candidate=record), indent=2) + '\n')
    rows.append(dict(name='fixture-record', exitCode=0 if record else 1, niceness=10))
    for pkg in NEW_TESTS:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
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
    (B / 'edited.json').write_text(json.dumps(dict(paths=mine), indent=2) + '\n')
    def fmt_clean(raw):
        r = subprocess.run([R + 'rustfmt', '--edition', '2024', '--emit', 'stdout'], input=raw, env=E, capture_output=True)
        return r.returncode == 0 and r.stdout == raw
    fmt_rows = []
    for x in [x for x in mine if x.endswith('.rs')]:
        base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + x], cwd=W, env=E, capture_output=True)
        fmt_rows.append(dict(path=x, baseClean=None if base_raw.returncode else fmt_clean(base_raw.stdout), candidateClean=fmt_clean((W / x).read_bytes())))
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    rows.append(dict(name='rustfmt-edited', exitCode=0 if all(r['candidateClean'] for r in fmt_rows if r['baseClean'] is not False) else 1, niceness=10))
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-contracts', '-p', 'opensip-components', '--all-targets', '--', '-D', 'warnings']),
             ('focused-ts2-tests', FOCUSED + ['--nocapture']),
             ('duty-table', [PY, '-I', '-B', str(EV / 'check_d2b3b_duty_table.py'), str(W), str(A), str(B / 'duty-table.json')]),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('census-closure-unchanged', [PY, '-I', '-B', '-c', closure_check]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, ys, before, after in MUTATIONS:
        path = W / ys; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(FOCUSED, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and 'could not compile' not in out and 'test result: FAILED' in out
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=ys, caught=caught, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=main,
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D2b-3b r2 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    # Only the records this lane wrote are removed, on both sides.
    for root in (W, P):
        for old in (root / 'target/debug/deps').glob('supervisor_fixture.path'):
            old.unlink()
    if owned: lane.rmdir()
