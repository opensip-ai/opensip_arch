"""C1a2 candidate checks (M3-C r8 item 1: candidate blob custody and the capture session; C1a plan r4 as amended by the
accepted r5 and r6, C1a2 preparatory): the host, security and platform suites on the base checkout and the candidate
(--no-fail-fast; platform serially, as its lib suite is flaky in parallel at base; equal failure sets after isolated
reruns, and the new passing tests), rustfmt on the new and base-clean edited files, warning-denied all-targets Clippy on
the three crates, the focused tests, the 4 GiB stream probe, the charge model --check, the T2 census --check over the
lead-readable cache (the census records unchanged), FW-01, the environment exceptions, the operability source census, the
census-closure check (no closure file changed), verify_design, and mutations: code mutations must fail the focused tests;
model undercounts, regenerated, must fail the session control. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1a2'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
SN = 'crates/host/src/snapshot.rs'; CC = 'crates/host/src/candidate_custody.rs'; MODEL = 'tools/security/snapshot_ledger_model.py'
VECTORS = ('crates/security/src/snapshot_ledger_vectors.json', 'crates/host/src/snapshot_session_vectors.json')
# The new passing tests per suite: host 16 (custody 6, session 10), security 1 (the route control), platform 2.
NEW_TESTS = {'opensip-host': 16, 'opensip-security': 1, 'opensip-platform': 2}
SERIAL = {'opensip-platform'}
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'snapshot::tests', 'candidate_custody']
ROUTES = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'snapshot_source::route_tests', 'snapshot_walk']
ENTRY = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--lib', '--', 'custody_entry']
PROBE = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', '--ignored', '--exact',
         'snapshot::tests::a_four_gibibyte_stream_is_charged_only_its_buffer_and_its_read_attempts']
SESSION_CONTROL = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--',
                   'snapshot::tests::the_session_charges_exactly_the_models_read_and_custody_terms']
T2 = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
MUTATIONS = [
    # (name, file, before, after): each weakens one item 1 rule; the focused tests must fail.
    ('captured-path-read-again', SN, "            if let Some(capture) = captures.get_mut(source.path()) {\n",
     "            if let Some(capture) = None::<&mut Capture> {\n"),
    ('capture-change-not-refused', SN, "                if capture.stamp != Stamp::of(source.observation()) {\n", "                if false {\n"),
    ('before-sample-not-compared', SN, "    if Stamp::of(&before) != observed {\n", "    if false {\n"),
    ('after-sample-not-compared', SN, "    if after != before || total != size {\n", "    if total != size {\n"),
    ('attempt-envelope-off-by-one', SN, "        if attempts == envelope {\n", "        if attempts == envelope + 1 {\n"),
    ('buffer-uncharged', SN, "        work.charge::<ReadError>(buffer_cost())?;\n", ""),
    ('duplicate-not-resolved', CC, "        if custody.committed.contains_key(&sha256) {\n", "        if false {\n"),
    ('open-digest-not-verified', CC, "        if seen != length || RawSha256::finish(digest) != *sha256 {\n", "        if seen != length {\n"),
    ('custody-directory-not-private', CC, "        if sample.mode & 0o7777 != 0o700 || sample.uid != uid {\n", "        if sample.uid != uid {\n"),
]
# (name, before, after) on the model: each undercount, regenerated, must fail the session control.
MODEL_MUTATIONS = [
    ('model-eof-attempt-free', "        add(s['ATTEMPT'], chunks + 1)\n", "        add(s['ATTEMPT'], chunks)\n"),
    ('model-commit-sample-free', "        add(status)  # the commit's sample\n", ""),
    ('model-capture-record-free', "        add(owned(s['CAPTURE_SIZE'][0]))\n", ""),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1a2-check-', dir=D)); T.chmod(0o700)
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
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 else 0)")
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '-p', 'opensip-platform', '--all-targets', '--', '-D', 'warnings']),
             ('focused-host-tests', FOCUSED + ['--nocapture']),
             ('focused-security-tests', ROUTES),
             ('focused-platform-tests', ENTRY),
             ('four-gibibyte-probe', PROBE),
             ('snapshot-ledger-model', [PY, '-I', '-B', MODEL, '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-census', [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2]),
             ('discovery-fw01', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
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
    for name, before, after in MODEL_MUTATIONS:
        model = W / MODEL; original = model.read_bytes(); saved = [(W / v).read_bytes() for v in VECTORS]; text = original.decode()
        assert text.count(before) == 1, name
        model.write_text(text.replace(before, after))
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                g = subprocess.run([PY, '-I', '-B', MODEL, '--write', '--architecture', str(A), '--packages-root', str(P)], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
                r = subprocess.run(SESSION_CONTROL, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = g.returncode == 0 and r.returncode != 0 and 'test result: FAILED' in out
        finally:
            model.write_bytes(original)
            for v, raw in zip(VECTORS, saved): (W / v).write_bytes(raw)
        assert model.read_bytes() == original and all((W / v).read_bytes() == raw for v, raw in zip(VECTORS, saved))
        controls.append(dict(kind='model-mutation', name=name, file=MODEL, caught=caught))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C1a2 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
