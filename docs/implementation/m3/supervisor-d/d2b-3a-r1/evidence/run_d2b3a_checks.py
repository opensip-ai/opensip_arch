"""D2b-3a candidate checks (D2b plan r3 as amendments A1 and A2 amend it: the TS2 receive side): the components,
identity and contracts suites on the base checkout and the candidate (--no-fail-fast; equal failure sets after isolated
reruns, and the new passing tests), rustfmt on the new and base-clean edited files, warning-denied all-targets Clippy on
contracts and components, the focused receiver tests, section 3's duty table against the carriers' admission list
(check_d2b3a_duty_table.py), the carriers' TS2 records against their DLV schemas (check_d2b3a_dlv_records.py; LD-D2B3-1),
the operability source census, the environment exceptions, the census-closure check, verify_design, and mutations, each
of which must fail the focused tests. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d2b3'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = A / 'docs/implementation/m3/supervisor-d/d2b-3a-r1/evidence'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
TS2 = 'crates/components/src/provider_protocol/ts2.rs'
# The new passing tests per suite: components 17 (the receiver's 16 and the embedding's 1); none elsewhere.
NEW_TESTS = {'opensip-components': 17, 'opensip-identity': 0, 'opensip-contracts': 0}
SERIAL = set()
FOCUSED = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-components', '--lib', '--', 'provider_protocol::ts2', 'schema_sources']
MUTATIONS = [
    # (name, file, before, after): each weakens one receive-side rule; the focused tests must fail.
    ('echo-member-ignored', TS2, '                    ("universeKey", &self.context.universe_key),\n', ''),
    ('commitment-reencoded', TS2,
     '        if text_of(f, "coverageCommitment") != Some(commit(domain, &received).as_str()) {\n            return Err("coverageCommitment".to_owned());\n        }\n        let frame_index',
     '        if text_of(f, "coverageCommitment") != Some(super::built_commitment(domain, &Value::Array(entries.to_vec())).as_str()) {\n            return Err("coverageCommitment".to_owned());\n        }\n        let frame_index'),
    ('stage-correlation-unchecked', TS2,
     '        let live = &self.stages[stage];\n        if text_of(f, "stageId") != Some(binding.expected_stage_id.as_str()) {',
     '        let live = &self.stages[stage];\n        if false {'),
    ('batch-counter-unchecked', TS2, '        if u64_of(f, "batchIndex") != Some(live.batches) {', '        if false {'),
    ('token-echo-unchecked', TS2, '        if field(f, "capabilities") != Some(&Value::Array(caps)) {', '        if false && field(f, "capabilities") != Some(&Value::Array(caps)) {'),
    ('runtime-descriptor-unchecked', TS2, '            .chain(&self.context.runtime_descriptor)\n', ''),
    ('piecewise-items-unchecked', TS2, '        admit_extern(item_ref, item)?;\n', ''),
    ('empty-anchor-span-admitted', TS2, '                    if !(start < end && end <= *length) {', '                    if !(start <= end && end <= *length) {'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d2b3a-check-', dir=D)); T.chmod(0o700)
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
             ('focused-receiver-tests', FOCUSED + ['--nocapture']),
             ('duty-table', [PY, '-I', '-B', str(EV / 'check_d2b3a_duty_table.py'), str(W), str(A), str(B / 'duty-table.json')]),
             ('carriers-match-dlv', [PY, '-I', '-B', str(EV / 'check_d2b3a_dlv_records.py'), str(W), str(A), str(B / 'carriers-match-dlv.json')]),
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
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D2b-3a r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
