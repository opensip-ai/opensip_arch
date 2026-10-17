"""D3a-2 r1 candidate checks (M3-D r5 item 16, and item 12's tool class, :434; the D3a plan r4, sub-unit D3a-2): the
components suite on the base checkout and on the candidate (--no-fail-fast; equal failure sets after isolated reruns, and
the new passing tests). The base is main's own checkout, which holds the integrated D3a-1 r3 (LD-D3A2-5). Then rustfmt
on the new and
base-clean edited files, warning-denied all-targets Clippy, a workspace all-targets check, the fixture's exact artifact
and SHA-256 written beside each tree's test binary from each build's compiler-artifact record (LD-D3A-9 r4: deleted
first, rewritten after every build, deleted at the end), the focused supervisor tests, the package edges under the O1-a
package policy, the test-fixture feature reached only from dev-dependencies, the environment exceptions, the
operability source census, the census-closure check, verify_design, and mutations, each of which must fail the focused
supervisor tests. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, signal, subprocess, tempfile, time, json, re, sys, hashlib
W = Path('/Users/sb/code/opensip-ai/opensip-d3a2'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'; BASEW = P
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
SV = 'crates/components/src/supervisor.rs'
TESTS = 'crates/components/src/supervisor_tests.rs'
# The new passing tests: the candidate's supervisor tests less the base's (main's, D3a-1's).
count_tests = lambda root: len(re.findall(r'^#\[test\]$', (root / TESTS).read_text(), re.M))
NEW_TESTS = {'opensip-components': count_tests(W) - count_tests(BASEW)}
SERIAL = set()
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-components', '--lib', '--', 'supervisor']
MUTATIONS = [
    # (name, file, before, after): each weakens one D3a-2 rule (the plan's §3 list, then the tool class's); the
    # supervisor tests must fail.
    ('asserted-clears-observed', SV,
     "        if observed > self.limits.resident_memory || asserted > self.limits.resident_memory {\n",
     "        if self.asserted_resident.map_or(observed, |a| a.max(asserted)) > self.limits.resident_memory {\n"),
    ('observed-memory-ignored', SV, "            .fold(0u64, u64::saturating_add);\n", "            .fold(0u64, |_, _| 0);\n"),
    ('process-count-off-by-one', SV, "        if count_on && !self.count_breached && members.len() > most {\n",
     "        if count_on && !self.count_breached && members.len() > most + 1 {\n"),
    ('ts2-response-unchecked', SV, "        if self.protocol_kind == Some(Protocol::Ts2) {\n", "        if false {\n"),
    ('scratch-walk-skipped', SV, "                        if self.class == Class::Provider && !self.scratch_within(&dir) {\n",
     "                        if false {\n"),
    ('materialization-charged-after-the-write', SV,
     "        match self.total.checked_add(bytes) {\n            Some(next) if next <= Self::LIMIT => {\n",
     "        self.total = self.total.saturating_add(bytes);\n        match Some(self.total) {\n            Some(next) if next <= Self::LIMIT => {\n"),
    ('zero-fit-unchecked', SV, "    if memory_budget_bytes < Limits::RELEASE.resident_memory {\n", "    if false {\n"),
    # The tool class (item 12, :434).
    ('tool-output-unbounded', SV, "                Ok(n) => match tool.accounting.charge(n as u64) {\n",
     "                Ok(n) => match Ok::<(), ToolOutputBound>(()) {\n"),
    ('tool-handshake-not-skipped', SV, "        if self.class == Class::Tool {\n            // No control plane: a tool skips `Handshaking` (:434). Its fd0\n",
     "        if false {\n            // No control plane: a tool skips `Handshaking` (:434). Its fd0\n"),
    ('tool-ladder-from-t1', SV, "                        t1_done: from_t2 || self.class == Class::Tool,\n", "                        t1_done: from_t2,\n"),
    ('tool-death-at-eof-unexpected', SV,
     "            Class::Tool => self.fd1_eof || self.tool.as_ref().is_some_and(|t| t.bound.is_some()),\n",
     "            Class::Tool => false,\n"),
    ('tool-wall-clock-the-providers', SV, "        wall_clock: WALL_CLOCK_TOOL,\n        ..Self::RELEASE\n", "        ..Self::RELEASE\n"),
    ('tool-process-count-the-providers', SV, "            Class::Tool => TOOL_PROCESSES,\n", "            Class::Tool => PROVIDER_PROCESSES,\n"),
    ('descriptor-set-unchecked', SV, "    if launch.spec().descriptors() != descriptors {\n", "    if false {\n"),
]
def focused_for(path):
    return FOCUSED
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
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d3a2-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # The base is main's checkout, holding the integrated D3a-1 r3 (LD-D3A2-5): the worktree sits at main, and main is clean.
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-components', '--all-targets', '--', '-D', 'warnings']),
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
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D3a-2 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    for old in (W / 'target/debug/deps').glob('supervisor_fixture.path'):
        old.unlink()
    # The base is main's own checkout: only the record this lane wrote there is removed.
    for old in (BASEW / 'target/debug/deps').glob('supervisor_fixture.path'):
        old.unlink()
    if owned: lane.rmdir()
