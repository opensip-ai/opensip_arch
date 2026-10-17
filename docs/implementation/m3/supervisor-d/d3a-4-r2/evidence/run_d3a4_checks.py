"""D3a-4 r2 candidate checks (M3-D r5 item 21's four events S-OP-2c unblocks; unit D3a-4): the components, operability
and platform (serial) suites on the base checkout (main, S-OP-2c bound) and on the candidate (--no-fail-fast; equal failure sets after
isolated reruns, and the new passing tests), rustfmt on the new and base-clean edited files, warning-denied all-targets
Clippy, a workspace all-targets check, the fixture's exact artifact and SHA-256 written beside each tree's test binary
from each build's compiler-artifact record (LD-D3A-9 r4), the focused supervisor and registry tests, the package edges
under the O1-a package policy (components gains operability), the test-fixture feature reached only from
dev-dependencies, the environment exceptions, the operability source census with the mint audit, the census-closure
check, verify_design, the base's and the candidate's supervisor tests run serially (r2), and mutations, each of which must
fail its focused tests (some across several files, with a command that must still pass). One lane hold, nice 10, private
TMPDIR."""
from pathlib import Path
import os, signal, subprocess, tempfile, time, json, re, sys, hashlib
W = Path('/Users/sb/code/opensip-ai/opensip-d3a4'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'; BASEW = P
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
SV = 'crates/components/src/supervisor.rs'; RC = 'crates/components/src/supervisor_records.rs'
RG = 'crates/operability/src/kinds/registry.rs'
PR = 'crates/platform/src/process.rs'
TESTS = {'opensip-components': 'crates/components/src/supervisor_tests.rs', 'opensip-operability': 'crates/operability/src/kinds/registry_tests.rs', 'opensip-platform': 'crates/platform/src/process_tests.rs'}
# The new passing tests: each package's candidate tests less the base's, in the one test file each unit edits.
count_tests = lambda root, rel: len(re.findall(r'^#\[test\]$', (root / rel).read_text(), re.M)) if (root / rel).exists() else 0
NEW_TESTS = {pkg: count_tests(W, rel) - count_tests(BASEW, rel) for pkg, rel in TESTS.items()}
SERIAL = {'opensip-platform'}
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-components', '--lib', '--', 'supervisor']
REGISTRY_FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-operability', '--lib', '--', 'registry', 'readback']
PLATFORM_FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--lib', '--', 'terminating_signals', '--test-threads=1']
RJ = 'crates/operability/registry-events.json'; RM = 'crates/operability/registry-events.md'
ST = 'schemas/sources/startup-v1.schema.json'; NV = 'schemas/sources/native-v2.schema.json'
P3T = 'crates/components/data/protocol3-transitions.v1.json'
def focused_for(path):
    return REGISTRY_FOCUSED if path == RG else PLATFORM_FOCUSED if path == PR else FOCUSED
def one(name, path, before, after):
    return dict(name=name, edits=[(path, before, after)], focused=focused_for(path), passes=None)
MUTATIONS = [
    # Each weakens one D3a-4 rule: every edit's `before` occurs exactly once in its file, the focused tests must fail,
    # and `passes`, when given, must still pass on the mutant.
    one('stage-change-recorded-on-every-phase', SV, "            Boundary::Phase(state) if self.last_phase != Some(state) => {\n", "            Boundary::Phase(state) => {\n"),
    one('unavailable-reason-dropped', SV, "            opensip_operability::StageTerminal::Unavailable => self.unavailable_reason,\n", "            opensip_operability::StageTerminal::Unavailable => None,\n"),
    one('crash-never-recorded', SV, "        if self.analyze_sent.is_some() {\n            self.stage_terminal(opensip_operability::StageTerminal::Crash);\n", "        if false {\n            self.stage_terminal(opensip_operability::StageTerminal::Crash);\n"),
    one('signal-member-dropped', SV, "                    opensip_platform::TerminatingSignal::of(raw).map(records::child_signal)\n", "                    opensip_platform::TerminatingSignal::of(raw).and(None)\n"),
    one('progress-since-not-measured', SV, "        Some(now.saturating_duration_since(last))\n", "        Some(Duration::ZERO)\n"),
    one('frame-counts-dropped', SV, "                Progress::FactBatch => self.fact_frames += 1,\n", "                Progress::FactBatch => {}\n"),
    one('provider-exit-given-a-signal', RG, '        teardown: Elapsed,\n    ) -> Self {\n        let (class, signal) = match exit {\n            ReapedExit::Exited => (ExitClass::Exited, None),\n',
        '        teardown: Elapsed,\n    ) -> Self {\n        let (class, signal) = match exit {\n            ReapedExit::Exited => (ExitClass::Exited, Some(Code::from_enum(ChildSignal::Sigterm))),\n'),
    one('signal-by-a-hand-number', PR, "            (libc::SIGBUS, Self::Bus),\n", "            (7, Self::Bus),\n"),
    # r2, D3A4-R1-RF-1: round 1's defect (a report moves the transition), and a schedule that ignores the last report.
    one('absence-report-resets-the-span', SV, "        self.reported = Some(now);\n", "        self.reported = Some(now);\n        self.progress = Some(now);\n"),
    one('absence-schedule-ignores-the-report', SV, "        Some(self.reported.map_or(last, |reported| reported.max(last)) + interval)\n", "        Some(last + interval)\n"),
    # r2, D3A4-R1-RF-2: round 1's defect (no terminal time once a cause exists), and no trigger fallback.
    one('terminal-time-only-without-a-cause', SV, "        self.terminal_observed.get_or_insert_with(Instant::now);\n        if self.first_cause.is_some() {\n            return;\n        }\n",
        "        if self.first_cause.is_some() {\n            return;\n        }\n        self.terminal_observed.get_or_insert_with(Instant::now);\n"),
    one('teardown-without-its-trigger-fallback', SV, "        let from = self.terminal_observed.or(self.teardown_from);\n", "        let from = self.terminal_observed;\n"),
    # r2, D3A4-R1-NBO-1: an admitted pre-Analyze terminal dropped.
    one('pre-analyze-terminal-dropped', SV, "        self.stage_terminal_recorded = true;\n", "        if self.analyze_sent.is_none() {\n            return;\n        }\n        self.stage_terminal_recorded = true;\n"),
    # r2, D3A4-R1-RF-3: a same-cardinality, same-length substitution with the references regenerated to match, so the
    # registry's own tests (and its drift test) still pass; and a member added to each table's pinned source.
    dict(name='provider-reason-substituted-with-references',
         edits=[(RG, '    PreparedOutputStale => "prepared-output-stale",\n', '    PreparedOutputStale => "prepared-output-older",\n'),
                (RJ, '"prepared-output-stale"', '"prepared-output-older"'), (RM, 'prepared-output-stale', 'prepared-output-older')],
         focused=FOCUSED, passes=REGISTRY_FOCUSED),
    one('reason-source-gains-a-member', ST, '"prepared-output-not-inert",\n            "prepared-output-stale",\n            "semantic-universe-incomplete",',
        '"prepared-output-not-inert",\n            "prepared-output-stale",\n            "prepared-output-unsigned",\n            "semantic-universe-incomplete",'),
    # The checklist's item 4 for the other two tables: StageKind substituted with its reference regenerated, and a phase
    # added to the vendored P3T list.
    dict(name='stage-kind-substituted-with-references',
         edits=[(RG, '    SemanticProvider => "semantic-provider",\n', '    SemanticProvider => "semantic-producer",\n'), (RJ, '"semantic-provider"', '"semantic-producer"'), (RM, '- `semantic-provider`\n', '- `semantic-producer`\n')],
         focused=FOCUSED, passes=REGISTRY_FOCUSED),
    one('provider-state-source-gains-a-member', P3T, '\n  "DONE",\n  "FAULT"\n ],', '\n  "DONE",\n  "FAULT",\n  "HALTED"\n ],'),
    one('terminal-source-gains-a-member', NV, '"cancelled",\n        "crash"\n      ]\n    },\n    "WorkspaceUnitV1"', '"cancelled",\n        "crash",\n        "abandoned"\n      ]\n    },\n    "WorkspaceUnitV1"'),
]
# The package edges under the O1-a package policy: components' internal edges are exactly contracts, identity and
# platform (platform also as a dev-dependency), all reached as normal edges first.
PACKAGE_EDGES = ("import json,subprocess,sys;R,PY,A,W=sys.argv[1:5];m=subprocess.run([R+'cargo','metadata','--format-version','1','--offline','--locked'],"
                 "capture_output=True,check=True,cwd=W).stdout;open(sys.argv[5],'wb').write(m);"
                 "r=subprocess.run([PY,'-I','-B','tools/check_package_edges.py','--repository',W,'--metadata',sys.argv[5],'--inventory',"
                 "A+'/'+json.load(open(W+'/design-lock.json'))['inventorySuccessors'][-1]['candidate']['path'],'--lane','host','--package-policy',"
                 "A+'/docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json','--architecture',A,'--lock','design-lock.json'],cwd=W,capture_output=True);"
                 "sys.stdout.write(r.stdout.decode()+r.stderr.decode());j=json.loads(r.stdout);"
                 "e=sorted((x['to'],x['kinds'][0]['kind'] or 'normal') for x in j['resolvedInternalEdges'] if x['from']=='opensip-components');"
                 "print(e);sys.exit(0 if j['passed'] and e==[('opensip-contracts','normal'),('opensip-identity','normal'),('opensip-operability','normal'),('opensip-platform','normal')] else 1)")
# LD-D3A-9: the test-fixture feature is reached only from components' dev-dependencies; no normal, build or target
# dependency of any manifest enables it.
FEATURE_SCOPE = ("import tomllib,sys,pathlib;W=pathlib.Path(sys.argv[1]);hits=[];bad=[]\n"
                 "for m in sorted(list(W.glob('crates/*/Cargo.toml'))+list(W.glob('apps/*/Cargo.toml'))):\n"
                 "  d=tomllib.loads(m.read_text());tables=[('',d)]+[('target.'+k,v) for k,v in d.get('target',{}).items()]\n"
                 "  for prefix,t in tables:\n"
                 "    for sec in ('dependencies','build-dependencies','dev-dependencies'):\n"
                 "      for name,dep in t.get(sec,{}).items():\n"
                 "        if isinstance(dep,dict) and 'test-fixture' in dep.get('features',[]):\n"
                 "          (hits if sec=='dev-dependencies' and m.parent.name=='components' and prefix=='' else bad).append((str(m.relative_to(W)),prefix+sec,name))\n"
                 "print('dev',hits,'other',bad);sys.exit(0 if hits and not bad else 1)")
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d3a4-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # The base is main's checkout, holding the bound S-OP-2c and the integrated D3a-3, and main is clean. Main moves only
    # under the lead's lock, so it cannot move while this lane holds it. If it moved while this lane waited, the worktree
    # follows it here, only when what main changed is disjoint from the candidate's paths.
    assert git(P, 'status', '--porcelain') == ''
    own = set(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
    if git(P, 'rev-parse', 'HEAD') != git(W, 'rev-parse', 'HEAD'):
        moved = set(git(P, 'diff', '--name-only', git(W, 'rev-parse', 'HEAD'), git(P, 'rev-parse', 'HEAD')).splitlines())
        assert not moved & own, sorted(moved & own)
        git(W, 'checkout', '-q', '--detach', git(P, 'rev-parse', 'HEAD'))
        print('worktree moved onto main', git(W, 'rev-parse', 'HEAD'), flush=True)
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD')
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
    assert fixture_record(BASEW, 'base'), 'the base builds'
    record = fixture_record(W, 'candidate')
    (B / 'fixture-record.json').write_text(json.dumps(record, indent=2) + '\n')
    rows.append(dict(name='fixture-record', exitCode=0 if record else 1, niceness=10))
    for pkg in NEW_TESTS:
        base = failures(BASEW, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        differing = sorted(set(base['failed']) ^ set(cand['failed']))
        flaky = []
        for name in differing:
            runs = []
            for root in (BASEW, W):
                for _ in range(3):
                    rr = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', pkg, '--lib', '--', '--exact', name, '--test-threads=1'], cwd=root, env=E, capture_output=True)
                    runs.append(rr.returncode == 0 and b'1 passed' in rr.stdout)
            (B / ('isolated-' + name.replace(':', '_') + '.json')).write_text(json.dumps(dict(test=name, runs=runs), indent=2) + '\n')
            if all(runs):
                flaky.append(name)
        comparison = dict(base=base, candidate=cand, differing=differing, flakyInIsolation=flaky, equalFailureSets=set(base['failed']) - set(flaky) == set(cand['failed']) - set(flaky), candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'] + len([f for f in flaky if f in cand['failed']]) - len([f for f in flaky if f in base['failed']]))
        comparisons[pkg] = comparison
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
        rows.append(dict(name=f'{pkg}-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] == NEW_TESTS[pkg] else 1, niceness=10))
    (B / 'test-comparison.json').write_text(json.dumps(comparisons, indent=2) + '\n')
    # r2: the base's parallel supervisor failures were all isolation-flaky; the same tests serially on each tree, for a
    # cleaner comparison. The candidate's run gates; the base's is recorded.
    serial_runs = {}
    for root, tag in ((BASEW, 'base'), (W, 'candidate')):
        assert fixture_record(root, tag + '-serial'), tag
        log = B / f'{tag}-supervisor-serial.log'
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-components', '--lib', '--', 'supervisor', '--test-threads=1'], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace')
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        serial_runs[tag] = dict(exitCode=code, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M))))
        print(tag, 'supervisor serial exit', code, serial_runs[tag]['passed'], 'passed', serial_runs[tag]['failedCount'], 'failed', flush=True)
    (B / 'supervisor-serial.json').write_text(json.dumps(serial_runs, indent=2) + '\n')
    rows.append(dict(name='candidate-supervisor-serial', exitCode=serial_runs['candidate']['exitCode'], niceness=10))
    edited = sorted(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
    (B / 'edited.json').write_text(json.dumps(dict(paths=edited), indent=2) + '\n')
    def fmt_clean(raw):
        rr = subprocess.run([R + 'rustfmt', '--edition', '2024', '--emit', 'stdout'], input=raw, env=E, capture_output=True)
        return rr.returncode == 0 and rr.stdout == raw
    fmt_rows = []
    for x in [x for x in edited if x.endswith('.rs')]:
        base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + x], cwd=W, env=E, capture_output=True)
        fmt_rows.append(dict(path=x, baseClean=None if base_raw.returncode else fmt_clean(base_raw.stdout), candidateClean=fmt_clean((W / x).read_bytes())))
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    rows.append(dict(name='rustfmt-edited', exitCode=0 if all(r['candidateClean'] for r in fmt_rows if r['baseClean'] is not False) else 1, niceness=10))
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-components', '-p', 'opensip-operability', '-p', 'opensip-platform', '--all-targets', '--', '-D', 'warnings']),
             ('workspace-check', [R + 'cargo', 'check', '--locked', '--offline', '--workspace', '--all-targets']),
             ('focused-supervisor-tests', FOCUSED),
             ('focused-registry-tests', REGISTRY_FOCUSED),
             ('focused-platform-tests', PLATFORM_FOCUSED),
             ('package-edges', [PY, '-I', '-B', '-c', PACKAGE_EDGES, R, PY, str(A), str(W), str(T / 'cargo-metadata.json')]),
             ('test-fixture-scope', [PY, '-I', '-B', '-c', FEATURE_SCOPE, str(W)]),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('census-closure-unchanged', [PY, '-I', '-B', '-c', closure_check]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        if name == 'focused-supervisor-tests':
            fixture_record(W, 'focused')
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    def run_logged(args, log_path):
        with log_path.open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                return child.wait(timeout=900), False
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL); return child.wait(), True
    for m in MUTATIONS:
        name = m['name']; originals = {}
        for ys, before, after in m['edits']:
            path = W / ys; originals.setdefault(path, path.read_bytes())
        timed_out = False; passes_code = None
        try:
            for ys, before, after in m['edits']:
                path = W / ys; text = path.read_text()
                assert text.count(before) == 1, (name, ys)
                path.write_text(text.replace(before, after))
            built = fixture_record(W, 'mutation-' + name)
            code, timed_out = run_logged(m['focused'], B / f'mutation-{name}.log')
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            if m['passes'] is not None:
                passes_code, passes_timed_out = run_logged(m['passes'], B / f'mutation-{name}-passes.log')
                timed_out = timed_out or passes_timed_out
            caught = built is not None and code != 0 and 'could not compile' not in out and 'test result: FAILED' in out and passes_code in (None, 0)
        finally:
            for path, original in originals.items():
                path.write_bytes(original)
        assert all(path.read_bytes() == original for path, original in originals.items())
        controls.append(dict(kind='mutation', name=name, files=[ys for ys, _, _ in m['edits']], caught=caught, timedOut=timed_out, passesExitCode=passes_code, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D3a-4 r2 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    for old in (W / 'target/debug/deps').glob('supervisor_fixture.path'):
        old.unlink()
    # The base is main's own checkout: only the record this lane wrote there is removed.
    for old in (BASEW / 'target/debug/deps').glob('supervisor_fixture.path'):
        old.unlink()
    if owned: lane.rmdir()
