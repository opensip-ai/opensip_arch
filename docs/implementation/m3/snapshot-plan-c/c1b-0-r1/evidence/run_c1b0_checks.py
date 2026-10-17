"""C1b-0 candidate checks (C1b plan r3, sub-unit C1b-0: S4's materialization): the contracts, identity, host, storage
and evaluator suites on the base checkout and the candidate (--no-fail-fast; equal failure sets after isolated reruns;
the new passing tests: host 2, evaluator 1), rustfmt on edited Rust files, warning-denied all-targets Clippy on the
edited crates, the generation determinism check (the selected pipeline re-run reproduces the worktree's outputs byte
for byte), the design preflight (verify_design refuses only the package's not-yet-accepted identity-v3 and admission-registry
copies, and passes with them accepted; the public generator entry point and the public TypeScript checker refuse for
exactly that reason), the report and generator TypeScript lanes with those copies accepted (check_c1b0_typescript.py), the discovery census, workspace ledger and
snapshot census --checks (each must PASS, LD-C1B-7's r3 rule), the stale receipt recorded separately from public fields
(the binding change is exactly the generator-closure digest), FW-01, the environment exceptions, the operability source
census, the census-closure check, and mutations, each failing its named detector. One lane hold, nice 10, private
TMPDIR. (Adapted from D2b-0b's run_d2b0b_checks.py.)"""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys, shutil, stat, hashlib
W = Path('/Users/sb/code/opensip-ai/opensip-c1b0'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = A / 'docs/implementation/m3/snapshot-plan-c/c1b-0-r1/evidence'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'; NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
GEN = '/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator'
CHILD_PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'
NEW_TESTS = {'opensip-contracts': 0, 'opensip-identity': 0, 'opensip-host': 2, 'opensip-storage': 0, 'opensip-evaluator': 1}
SERIAL = set()
T2 = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
ID3 = 'schemas/sources/identity-v3.schema.json'; REG = 'crates/identity/src/schema_registry.rs'; RL = 'crates/evaluator/src/run_links.rs'
HOST_S4 = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 's4_vcs_observation']
EVAL_JOIN = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-evaluator', '--lib', '--', 'vcs_join']
DETECTORS = {'host-s4': lambda out: HOST_S4, 'evaluator-join': lambda out: EVAL_JOIN}
def repin(root):
    """A schema mutation re-pins identity-v3's compiled SourcePin, so the semantic controls judge it, not the pin."""
    raw = (root / ID3).read_bytes(); digest = hashlib.sha256(raw).digest(); p = root / REG; text = p.read_text()
    pattern = r'(SourcePin \{\s*id: "urn:opensip:product-v1:identity:v3",\s*path: "' + re.escape(ID3) + r'",\s*bytes: )\d+(,\s*sha256: \[)[\d,\s]+(\],\s*\})'
    text, count = re.subn(pattern, lambda m: m[1] + str(len(raw)) + m[2] + ', '.join(str(v) for v in digest) + ',\n        ' + m[3], text); assert count == 1
    p.write_text(text)
MUTATIONS = [
    # (name, [(file, before, after)], detector, expected text in the detector's output, re-pin identity-v3)
    ('members-may-be-empty', [(ID3, '"members": {\n          "type": "array",\n          "minItems": 1,\n', '"members": {\n          "type": "array",\n')],
     'host-s4', 'the_s4_negatives_refuse_at_admission_and_at_the_run_closure ... FAILED', True),
    ('member-commit-pattern-relaxed', [(ID3, '"const": "git"\n        },\n        "commitId": {\n          "type": "string",\n          "pattern": "^[0-9a-f]{40}(?![\\\\s\\\\S])"\n',
                                       '"const": "git"\n        },\n        "commitId": {\n          "type": "string"\n')],
     'host-s4', 'the_s4_negatives_refuse_at_admission_and_at_the_run_closure ... FAILED', True),
    ('top-level-kind-join-dropped', [(RL, '        (text(field(vcs, "kind")?)? == "none") == (*field(vcs, "commitId")? == V::Null),\n', '        true,\n')],
     'evaluator-join', 'the_vcs_joins_read_the_top_level_and_every_member ... FAILED', False),
    ('member-join-dropped', [(RL, '                text(field(member, "kind")?)? == "git" && *field(member, "commitId")? != V::Null,\n', '                true,\n')],
     'evaluator-join', 'the_vcs_joins_read_the_top_level_and_every_member ... FAILED', False),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1b0-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # Main may have moved while this runner waited: the worktree follows it only if nothing that moved touches a
    # candidate path, and the candidate's bytes are unchanged by the move. The determinism check below re-proves the
    # generated outputs on the new base.
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
    for name, edits, _, _, _ in MUTATIONS:
        for f, before, _ in edits: assert (W / f).read_text().count(before) == 1, (name, f)
    # The TypeScript lanes' exact pinned ignored inputs (tools/typescript-boundary/node_modules), copied from main as
    # RCA-1's report check did; no install.
    lanes_reg = json.loads((W / 'tools/typescript-lanes.json').read_bytes()); copied = 0
    for row in lanes_reg['files']:
        target = W / row['path']
        if target.exists():
            raw = target.read_bytes(); assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']; continue
        assert row['path'].startswith('tools/typescript-boundary/node_modules/'), row['path']
        src = P / row['path']; st = src.lstat(); assert stat.S_ISREG(st.st_mode); raw = src.read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
        target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(raw); target.chmod(stat.S_IMODE(st.st_mode)); copied += 1
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
    # (name, args, expected exit: 0, or 'nonzero' for an expected refusal)
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-contracts', '-p', 'opensip-identity', '-p', 'opensip-host', '-p', 'opensip-evaluator', '--all-targets', '--', '-D', 'warnings'], 0),
             ('focused-host-s4', HOST_S4, 0),
             ('focused-evaluator-join', EVAL_JOIN, 0),
             ('generation-determinism', [PY, '-I', '-B', str(EV / 'run_c1b0_generation.py'), str(B / 'generation-check'), str(B / 'generation-check.json'), '--check'], 0),
             ('design-preflight', [PY, '-I', '-B', str(EV / 'check_c1b0_preflight.py'), str(B / 'design-preflight.json')], 0),
             ('generate-contracts-prebind-refusal', [PY, '-I', '-B', 'tools/generate_contracts.py', '--root', str(W), '--architecture', str(A), '--output', str(B / 'generate-contracts-prebind'),
                                                     '--node', NODE, '--generator', GEN, '--python', CHILD_PY], 'nonzero'),
             # The public TypeScript checker refuses before TypeScript runs, for exactly the pre-binding reason (the
             # package's copies are not yet accepted); the same checker with those copies accepted must pass.
             ('typescript-report-lane-prebind-refusal', [PY, '-I', '-B', 'tools/check_typescript.py', '--root', str(W), '--architecture', str(A), '--node', NODE, '--lane', 'report'], 'nonzero'),
             ('typescript-generator-lane-prebind-refusal', [PY, '-I', '-B', 'tools/check_typescript.py', '--root', str(W), '--architecture', str(A), '--node', NODE, '--lane', 'generator'], 'nonzero'),
             ('typescript-report-lane', [PY, '-I', '-B', str(EV / 'check_c1b0_typescript.py'), '--root', str(W), '--architecture', str(A), '--node', NODE, '--lane', 'report'], 0),
             # The generator lane refuses on the base too (its loader policy pins an older tools/contracts/package.json):
             # with the copies accepted, its refusal must be the base's (D2b-0b's precedent).
             ('typescript-generator-lane', [PY, '-I', '-B', str(EV / 'check_c1b0_typescript.py'), '--root', str(W), '--architecture', str(A), '--node', NODE, '--lane', 'generator'], 'nonzero'),
             ('discovery-census', [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2], 0),
             ('discovery-workspace-ledger', [PY, '-I', '-B', 'tools/security/discovery_workspace_ledger.py', '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2], 0),
             ('snapshot-ledger-census', [PY, '-I', '-B', 'tools/security/snapshot_ledger_census.py', '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2], 0),
             ('discovery-fw01', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v'], 0),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v'], 0),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)], 0),
             ('census-closure-unchanged', [PY, '-I', '-B', '-c', closure_check], 0)]
    for name, args, expected in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        ok = code == 0 if expected == 0 else code != 0
        rows.append(dict(name=name, args=args, exitCode=code, expected=expected, exitCodeAsExpected=ok, niceness=pr)); print(name, 'exit', code, 'as expected' if ok else 'UNEXPECTED', flush=True)
    # The expected refusal, for exactly its reason; and the stale receipt, recorded separately.
    refusal = (B / 'generate-contracts-prebind-refusal.log').read_text(errors='replace')
    # The generator TypeScript lane's refusal is the base's, in its reason.
    rb = subprocess.run([PY, '-I', '-B', 'tools/check_typescript.py', '--root', str(P), '--architecture', str(A), '--node', NODE, '--lane', 'generator'], cwd=P, env=E, capture_output=True)
    (B / 'typescript-generator-lane-base.log').write_bytes(rb.stdout + rb.stderr)
    reason = lambda t: sorted(l for l in t.splitlines() if 'refused' in l)
    same = rb.returncode != 0 and reason((rb.stdout + rb.stderr).decode(errors='replace')) == reason((B / 'typescript-generator-lane.log').read_text(errors='replace')) != []
    rows.append(dict(name='typescript-generator-lane-refusal-equals-base', exitCode=0 if same else 1, niceness=10))
    # Before the binding the first refusal is verify_design's, for the package's not-yet-accepted identity-v3 copy.
    PREBIND = 'generation source is not selected by accepted design'
    rows.append(dict(name='generate-contracts-refuses-only-the-unaccepted-copy', exitCode=0 if PREBIND in refusal else 1, niceness=10))
    for lane_name in ('report', 'generator'):
        text = (B / f'typescript-{lane_name}-lane-prebind-refusal.log').read_text(errors='replace')
        rows.append(dict(name=f'typescript-{lane_name}-lane-refuses-only-the-unaccepted-copy', exitCode=0 if PREBIND in text else 1, niceness=10))
    r = subprocess.run([PY, '-I', '-B', str(EV / 'check_c1b0_census_stale.py'), str(B / 'census-stale.json'), str(B / 'discovery-census.log')], cwd=W, env=E, capture_output=True)
    (B / 'census-stale.log').write_bytes(r.stdout + r.stderr)
    rows.append(dict(name='held-out-receipt-stale-recorded-closure-digest-only', exitCode=r.returncode, niceness=10))
    controls = []
    for name, edits, detector, expect, pinned in MUTATIONS:
        originals = {f: (W / f).read_bytes() for f in {f for f, _, _ in edits} | ({REG} if pinned else set())}
        for f, before, after in edits:
            text = (W / f).read_text(); assert text.count(before) == 1, (name, f); (W / f).write_text(text.replace(before, after))
        if pinned: repin(W)
        out_dir = B / f'mutation-{name}-work'
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(DETECTORS[detector](out_dir), cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and expect in out
        finally:
            for f, raw in originals.items(): (W / f).write_bytes(raw)
        for f, raw in originals.items(): assert (W / f).read_bytes() == raw
        controls.append(dict(kind='mutation', name=name, files=sorted(originals), detector=detector, expected=expect, caught=caught))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    passed = all((r['exitCodeAsExpected'] if 'exitCodeAsExpected' in r else r['exitCode'] == 0) for r in rows)
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=passed, privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        typescriptPinnedIgnoredInputsCopied=copied, installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=main,
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C1b-0 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', passed, flush=True)
finally:
    if owned: lane.rmdir()
