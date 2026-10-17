"""D2b-0 candidate checks (D2b plan r3 sub-unit D2b-0, as amended by LD-D2B0-A: FA-2's and RUST3-LIM's schemas
admission-only): the identity, host, storage and evaluator suites on the base checkout and the candidate (--no-fail-fast;
equal failure sets after isolated reruns, and the new passing tests), rustfmt on the edited files, warning-denied
all-targets Clippy on identity, host and storage, the focused registry and embedding tests, the design preflight and
admission-only assertions (check_d2b0_preflight.py), the T2 census --check over the lead-readable cache (the blind
receipt stays current: no refresh), FW-01, the environment exceptions, the operability source census, the census-closure
check, and mutations, each of which must fail its named detector. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d2b0'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
EV = A / 'docs/implementation/m3/supervisor-d/d2b-0-r1/evidence'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
IR = 'crates/identity/src/schema_registry.rs'; HS = 'crates/host/src/schema_sources.rs'; SS = 'crates/storage/src/schema_sources.rs'
AM = 'schemas/admission-source-map.json'; AR = 'schemas/admission-registry.json'
# The new passing tests per suite: host 2 (successor_source_tests), none elsewhere. No new test binary.
NEW_TESTS = {'opensip-identity': 0, 'opensip-host': 2, 'opensip-storage': 0, 'opensip-evaluator': 0}
SERIAL = set()
DETECTORS = {
    'host': [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', '--', 'schema_sources'],
    'storage': [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-storage', '--lib', '--', 'schema_sources'],
    'preflight': [PY, '-I', '-B', str(EV / 'check_d2b0_preflight.py'), '/dev/null'],
}
T2 = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
CENSUS_ROW = ('    {\n      "schemaId": "opensip.product.symbol-census.1",\n      "implementationPath": "schemas/sources/symbol-census-v1.schema.json",\n'
              '      "architectureSource": {\n        "path": "docs/implementation/m3/native-successors-fa/fa-2/product/schemas/sources/symbol-census-v1.schema.json",\n'
              '        "bytes": 19045,\n        "sha256": "95d84054ba8d0d37cff59198df3f0c9d33a7701f259298ca2f068f05cf07ad21"\n      }\n    },\n')
SCOPE_REG_ROW = ('    {\n      "schemaId": "opensip.product.rust-subject-scope.1",\n      "sourcePath": "schemas/sources/rust-subject-scope-v1.schema.json",\n'
                 '      "bytes": 8672,\n      "sha256": "17f9b5bc0dbafe510757c1aa9e21e9a65b22820a80f16c4cec2c900cb2f5ba64"\n    },\n')
def include(path): return '    include_bytes!(concat!(\n        env!("CARGO_MANIFEST_DIR"),\n        "/../../' + path + '"\n    )),\n'
MUTATIONS = [
    # (name, file, before, after, detector): each weakens one materialization step; its detector must fail.
    ('host-embedding-omits-census', HS, include('schemas/sources/symbol-census-v1.schema.json'), '', 'host'),
    ('storage-embedding-omits-scope', SS, include('schemas/sources/rust-subject-scope-v1.schema.json'), '', 'storage'),
    ('identity-pin-byte-changed', IR, '            149, 216, 64, 84, 186,', '            150, 216, 64, 84, 186,', 'host'),
    ('identity-annotation-omits-census-law', 'crates/identity/src/schema.rs', '            | "x-opensip-symbol-census-law"\n', '', 'host'),
    ('admission-map-omits-census', AM, CENSUS_ROW, '', 'preflight'),
    ('admission-registry-omits-scope', AR, SCOPE_REG_ROW, '', 'preflight'),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d2b0-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    # Main may have moved while this runner waited (a lock commit or another unit): the worktree follows it, only if
    # nothing that moved touches a candidate path, and the candidate's bytes are unchanged by the move.
    assert git(P, 'status', '--porcelain') == ''
    head, main = git(W, 'rev-parse', 'HEAD'), git(P, 'rev-parse', 'HEAD')
    moved = None
    if head != main:
        mine = sorted(git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
        theirs = set(git(P, 'diff', '--name-only', head, main).splitlines())
        assert not theirs & set(mine), sorted(theirs & set(mine))
        before = {x: (W / x).read_bytes() for x in mine}
        git(W, 'checkout', '-q', '--detach', main)
        assert {x: (W / x).read_bytes() for x in mine} == before
        moved = dict(fromHead=head, toHead=main, mainChangedPaths=sorted(theirs))
        print('worktree moved onto main', main, flush=True)
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD')
    (B / 'worktree-base.json').write_text(json.dumps(dict(productBase=main, moved=moved), indent=2) + '\n')
    for name, ys, before, after, _ in MUTATIONS: assert (W / ys).read_text().count(before) == 1, name
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-identity', '-p', 'opensip-host', '-p', 'opensip-storage', '--all-targets', '--', '-D', 'warnings']),
             ('focused-host-schema-sources', DETECTORS['host'] + ['--nocapture']),
             ('focused-storage-schema-sources', DETECTORS['storage']),
             ('focused-identity-schema-registry', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-identity', '--lib', '--', 'schema_registry']),
             ('design-preflight', [PY, '-I', '-B', str(EV / 'check_d2b0_preflight.py'), str(B / 'design-preflight.json')]),
             ('discovery-census', [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2]),
             ('discovery-fw01', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('census-closure-unchanged', [PY, '-I', '-B', '-c', closure_check])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    for name, ys, before, after, detector in MUTATIONS:
        path = W / ys; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(DETECTORS[detector], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and 'could not compile' not in out and (detector == 'preflight' or 'test result: FAILED' in out)
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=ys, detector=detector, caught=caught, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D2b-0 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
