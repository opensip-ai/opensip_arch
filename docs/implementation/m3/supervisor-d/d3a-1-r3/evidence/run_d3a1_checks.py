"""D3a-1 r3 candidate checks (M3-D r5 items 12 to 15, 17 and 19's normal end; the D3a plan r4, sub-unit D3a-1): the
components and platform suites on the base checkout (main, D3a-0 and D2b-2 integrated) and on the candidate (--no-fail-fast; equal failure sets after isolated
reruns, and the new passing tests), rustfmt on the new and base-clean edited files, warning-denied all-targets Clippy, a
workspace all-targets check, the fixture's exact artifact and SHA-256 written beside the test binary from each build's
compiler-artifact record (LD-D3A-9 r4: deleted first, rewritten after every build, deleted at the end), the focused
supervisor tests, the package edges under the O1-a package policy, the test-fixture feature reached only from
dev-dependencies, the environment exceptions, the operability source census, the census-closure check, verify_design,
and mutations, each of which must fail the focused supervisor tests. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, signal, subprocess, tempfile, time, json, re, sys, hashlib
W = Path('/Users/sb/code/opensip-ai/opensip-d3a1'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
SV = 'crates/components/src/supervisor.rs'; PR = 'crates/platform/src/process.rs'
# The new passing tests: components gains the supervisor tests and D2a's one r2 control (RF-6's typed detail);
# platform gains wait_ready's two controls (r1's readiness, r2's interrupted wait).
NEW_TESTS = {'opensip-components': len(re.findall(r'^#\[test\]$', (W / 'crates/components/src/supervisor_tests.rs').read_text(), re.M)) + 1,
             'opensip-platform': 2}
# The platform suite runs serially, as D1a's and D3a-0's lanes do (a pre-existing parallel IO-safety race).
SERIAL = {'opensip-platform'}
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-components', '--lib', '--', 'supervisor']
PLATFORM_FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--lib', '--', 'wait_ready', 'interrupted', '--test-threads=1']
MUTATIONS = [
    # (name, file, before, after): each weakens one D3a-1 rule (the plan's §3 list); the supervisor tests must fail.
    # r1's 'second-settlement-minted' is retired in r2: the settlement now consumes the child (RF-5), so without the
    # state guard a second settle() finds nothing to settle; the guard is defence in depth, and its control still runs.
    ('unsettled-drop-leaves-the-child', SV,
     "            if self.signal(SIGKILL) {\n                self.append(SupervisionEvent::Signalled { signal: SIGKILL });\n            }\n            let ceiling",
     "            let ceiling"),
    ('eof-hold-dropped', SV, "                // Item 13: EOF after the terminal is held for the exit.\n                self.held_eof = true;\n",
     "                self.eof_delivered = true;\n                self.deliver(ProcessEvent::Eof);\n"),
    ('zero-exit-synthesized-from-eof', SV, "                // Item 13: EOF after the terminal is held for the exit.\n                self.held_eof = true;\n",
     "                self.held_eof = true;\n                self.deliver(ProcessEvent::ZeroExit);\n"),
    ('wall-clock-unbounded', SV, "            && now >= spawned + self.waits.wall_clock\n", "            && false\n"),
    ('rust3-wait-replaced-by-ts2', SV, "        let protocol = participant.protocol_waits();\n", "        let protocol = ProtocolWaits::TS2;\n"),
    ('control-prefix-judged-after-the-body', SV, "        let target = self.body.map_or(4, |n| 4 + n);\n", "        let target = self.buf.len();\n"),
    ('control-accumulator-reset-on-wouldblock', SV,
     "            Err(e) if e.kind() == io::ErrorKind::WouldBlock => return Ok(ControlRead::Pending),\n",
     "            Err(e) if e.kind() == io::ErrorKind::WouldBlock => {\n                self.have = 0;\n                return Ok(ControlRead::Pending);\n            }\n"),
    ('liveness-taken-from-traffic', SV,
     "                    self.stderr.bytes = self.stderr.bytes.saturating_add(n as u64);\n",
     "                    self.stderr.bytes = self.stderr.bytes.saturating_add(n as u64);\n                    self.health_due = None;\n"),
    ('stderr-bytes-retained', SV,
     "                    self.stderr.bytes = self.stderr.bytes.saturating_add(n as u64);\n",
     "                    let kept = self.stderr_buf[..n].to_vec();\n                    drop(kept);\n                    self.stderr.bytes = self.stderr.bytes.saturating_add(n as u64);\n"),
    ('participant-read-twice', SV, "            self.service_data_read();\n        }\n",
     "            self.service_data_read();\n            #[cfg(test)]\n            {\n                self.seams.reads_this_turn += 1;\n                self.seams.max_reads_per_turn = self.seams.max_reads_per_turn.max(self.seams.reads_this_turn);\n            }\n            self.service_data_read();\n        }\n"),
    ('normal-end-ladder-from-t1', SV, "                self.trigger_from(Cause::Deadline, true);\n", "                self.trigger(Cause::Deadline);\n"),
    # r2 (Codex codex-d3a-1-r1).
    ('rf1-stderr-unbounded-per-turn', SV, "        for _ in 0..STDERR_READS_PER_TURN {\n", "        loop {\n"),
    ('rf2-clean-end-has-no-ceiling', SV, "            self.clean_at = Some(Instant::now());\n", ""),
    ('rf3-eintr-past-the-deadline', PR, "                if std::time::Instant::now() >= deadline {\n", "                if false {\n"),
    ('rf4-shutdown-not-deferred', SV, "        if self.deferred == Some(Deferred::Shutdown)\n            && self\n                .control\n                .observations_mut()\n                .pending_health_report\n                .is_some()\n        {\n            return;\n        }\n", ""),
    ('rf6-nonce-detail-ignored', SV, "                if refused.detail == Some(RefusalDetail::HealthNonceMismatch) {\n", "                if false {\n"),
    ('rf8-independent-death-dropped', SV, "        if self.terminal.is_none() && self.exit_independent {\n", "        if self.terminal.is_none() && self.exit_independent && self.first_cause.is_none() {\n"),
    ('rf9-confirmed-after-the-reap', SV, "        if self.ladder.is_some_and(|l| l.kill_at.is_some()) && self.reaped.is_none() {\n            self.tree_confirmed = Some(self.confirm_tree());\n        }\n", ""),
    # r3 (Codex codex-d3a-1-r2).
    # R2-RF-1: round 2's order, the unwind's kill marked only after its reap loop.
    ('r3-rf1-unwind-kill-marked-after-the-reap', SV,
     "            // The kill is marked before the first reap attempt, so each\n            // attempt captures the confirmation against the still-unreaped\n            // root, and settlement reuses the last one (r3, RF-1).\n            if let Some(ladder) = &mut self.ladder\n                && ladder.kill_at.is_none()\n            {\n                ladder.kill_at = Some(Instant::now());\n            }\n            if self.signal(SIGKILL) {\n                self.append(SupervisionEvent::Signalled { signal: SIGKILL });\n            }\n            let ceiling = Instant::now() + self.waits.reap_ceiling;\n            while Instant::now() < ceiling {\n                if self.try_reap() {\n                    break;\n                }\n                std::thread::sleep(Duration::from_millis(10));\n            }\n        }\n        self.settle();\n",
     "            if self.signal(SIGKILL) {\n                self.append(SupervisionEvent::Signalled { signal: SIGKILL });\n            }\n            let ceiling = Instant::now() + self.waits.reap_ceiling;\n            while Instant::now() < ceiling {\n                if self.try_reap() {\n                    break;\n                }\n                std::thread::sleep(Duration::from_millis(10));\n            }\n        }\n        if let Some(ladder) = &mut self.ladder\n            && ladder.kill_at.is_none()\n        {\n            ladder.kill_at = Some(Instant::now());\n        }\n        self.settle();\n"),
    # R2-RF-2: the closed check and the append in separate sections (round 2's check-then-send).
    ('r3-rf2-admission-split-from-the-close', SV,
     "        #[cfg(test)]\n        if let Some(pause) = &self.pause {\n            pause.0.wait();\n            pause.1.wait();\n        }\n        if gate.pending.len() >= TRIGGER_CAPACITY {\n",
     "        drop(gate);\n        #[cfg(test)]\n        if let Some(pause) = &self.pause {\n            pause.0.wait();\n            pause.1.wait();\n        }\n        let mut gate = self.lock();\n        if gate.pending.len() >= TRIGGER_CAPACITY {\n"),
    # R2-RF-2: the close leaving what was admitted before it queued and uncounted.
    ('r3-rf2-close-leaves-admitted-unaccounted', SV,
     "        gate.pending.clear();\n        gate.late += drained as u64;\n        drained\n",
     "        drained * 0\n"),
    # R2-NBO-1: the nonce mismatch's provenance reduced to a window expiry.
    ('r3-nbo1-provenance-dropped', SV,
     "                        LivenessMiss::NonceMismatch(refused.family),\n",
     "                        LivenessMiss::WindowExpired,\n"),
]
# Which focused run must catch each mutation: the platform's for the platform file, else the supervisor's.
def focused_for(path):
    return PLATFORM_FOCUSED if path == PR else FOCUSED
# The package edges under the O1-a package policy: components' internal edges are exactly contracts, identity and
# platform (platform also as a dev-dependency), all reached as normal edges first.
PACKAGE_EDGES = ("import json,subprocess,sys;R,PY,A,W=sys.argv[1:5];m=subprocess.run([R+'cargo','metadata','--format-version','1','--offline','--locked'],"
                 "capture_output=True,check=True,cwd=W).stdout;open(sys.argv[5],'wb').write(m);"
                 "r=subprocess.run([PY,'-I','-B','tools/check_package_edges.py','--repository',W,'--metadata',sys.argv[5],'--inventory',"
                 "A+'/'+json.load(open(W+'/design-lock.json'))['inventorySuccessors'][-1]['candidate']['path'],'--lane','host','--package-policy',"
                 "A+'/docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json','--architecture',A,'--lock','design-lock.json'],cwd=W,capture_output=True);"
                 "sys.stdout.write(r.stdout.decode()+r.stderr.decode());j=json.loads(r.stdout);"
                 "e=sorted((x['to'],x['kinds'][0]['kind'] or 'normal') for x in j['resolvedInternalEdges'] if x['from']=='opensip-components');"
                 "print(e);sys.exit(0 if j['passed'] and e==[('opensip-contracts','normal'),('opensip-identity','normal'),('opensip-platform','normal')] else 1)")
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
BASEW = None
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d3a1-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    BASEW = P
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-components', '-p', 'opensip-platform', '--all-targets', '--', '-D', 'warnings']),
             ('workspace-check', [R + 'cargo', 'check', '--locked', '--offline', '--workspace', '--all-targets']),
             ('focused-supervisor-tests', FOCUSED),
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
    for name, ys, before, after in MUTATIONS:
        path = W / ys; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        timed_out = False
        try:
            built = fixture_record(W, 'mutation-' + name)
            with (B / f'mutation-{name}.log').open('wb') as log:
                child = subprocess.Popen(focused_for(ys), cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
                try:
                    code = child.wait(timeout=900)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL); code = child.wait(); timed_out = True
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = built is not None and code != 0 and 'could not compile' not in out and 'test result: FAILED' in out
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=ys, caught=caught, timedOut=timed_out, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D3a-1 r3 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    for old in (W / 'target/debug/deps').glob('supervisor_fixture.path'):
        old.unlink()
    # The base is main's own checkout: only the record this lane wrote there is removed.
    for old in (P / 'target/debug/deps').glob('supervisor_fixture.path'):
        old.unlink()
    if owned: lane.rmdir()
