"""B3-b3a2 candidate checks (the pre-run gate: the blind mode extended to the D15 terms; B3-b plan r2 amendment A5): the
security suite on the base checkout and the candidate (--no-fail-fast, equal failure sets, no new test), the equality
projection of both census records (only the vectors' member-model pin changes), the measured-against-model control and
every census and discovery test, the census vector check, the census tool's and blind receipt's controls, the census
(--check over the integrity-verified lead-readable T2 stores; held-out entries never opened), the blind equivalence (the
blind row over every lead-readable store equals that entry's full-ledger row in the census record), the environment
exceptions, the operability source census, verify_design, and three mutations of the blind mode (each must fail the blind
controls). One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b3b3a2'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
DC = 'tools/security/discovery_census.py'
CENSUS_JSON = 'crates/security/src/custody/discovery_census.json'; CENSUS_VECTORS = 'crates/security/src/custody/discovery_census_vectors.json'
NEW_TESTS = 0
BLIND_CONTROLS = [PY, '-I', '-B', 'tools/tests/test_discovery_census_blind.py']
# The equality projection's allowlist: every other field of both records equals the base's.
ALLOWED = {CENSUS_JSON: [], CENSUS_VECTORS: [r'/memberModel/(bytes|sha256)']}  # attempt 1 matched the bare key only
MUTATIONS = [
    # (name, before, after): each weakens the blind mode; the blind controls must fail.
    ('blind-terms-ignored', "        full = full_ledger(m, terms, c['LIMITS'])\n", "        full = full_ledger(m, {k: (0, 0, 0, 0) for k in terms}, c['LIMITS'])\n"),
    ('receipt-member-model-unbound', " memberModel=pin_row(product, MEMBER_MODEL),", ''),
    ('member-admission-unchecked', "    require(not members and full.observed == m.observed, 'a T2 repository entry admitted a member: ' + label)\n", ''),
]
# The blind equivalence, run in the candidate: the reviewed blind row (the blind mode's own measure and row) over each
# lead-readable store, presented to `blind_row` as held out so the blind join applies, against that entry's full ledger
# in the census record. No held-out store is opened: the entries are the manifest's lead-readable ones.
EQUIVALENCE = r'''
import importlib.util, json, os, sys
from pathlib import Path
W, A, P, CACHE = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location('discovery_census', W / 'tools/security/discovery_census.py')
census = importlib.util.module_from_spec(spec); spec.loader.exec_module(census)
c = census.costs(W)
wv, ref, slm, rule = census.load_reference(W, A, P)
measure = census.blind_measure(c, census.load_member_model(W), rule, lambda tree: census.reference_population(wv, ref, slm, rule, tree))
manifest = json.loads((A / census.MANIFEST).read_bytes())
record = {e['id']: e for e in json.loads((W / census.OUTPUT_CENSUS).read_bytes())['entries']}
rows = []
for entry in manifest['repositories']:
    if entry['heldOut'] is not False:
        continue
    row = census.blind_row(dict(entry, heldOut=True), os.path.join(CACHE, 'store'), c, measure)
    full = record[entry['id']]['d15']['fullLedger']
    expected = dict(id=entry['id'], status='measured', integrity=True, population=True,
                    marginPermille=dict(objects=full['objectMarginPermille'], edges=full['edgeMarginPermille'],
                                        bytes=full['byteMarginPermilleAt'][str(census.ROOT_LENGTHS[-1])]), passes2x=full['passes2x'])
    rows.append(dict(id=entry['id'], equal=row == expected, row=row))
    print(entry['id'], row == expected, flush=True)
print(json.dumps(dict(rows=rows, allEqual=all(r['equal'] for r in rows) and len(rows) > 0)))
sys.exit(0 if rows and all(r['equal'] for r in rows) else 1)
'''
def diff(a, b, p=''):
    if type(a) is not type(b): return [p]
    if isinstance(a, dict): return [x for k in sorted(set(a) | set(b)) for x in ([p + '/' + k] if k not in a or k not in b else diff(a[k], b[k], p + '/' + k))]
    if isinstance(a, list): return [p] if len(a) != len(b) else [x for i, (u, v) in enumerate(zip(a, b)) for x in diff(u, v, f'{p}/{i}')]
    return [] if a == b else [p]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b3b3a2-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    base = failures(P, 'opensip-security', 'base'); cand = failures(W, 'opensip-security', 'candidate')
    comparison = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
    print('security base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='security-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] == NEW_TESTS else 1, niceness=10)]
    projection = {}
    for rel, allowed in ALLOWED.items():
        changed = diff(json.loads(git(P, 'show', 'HEAD:' + rel)), json.loads((W / rel).read_text()))
        unallowed = [p for p in changed if not any(re.fullmatch(a, p) for a in allowed)]
        projection[rel] = dict(changed=sorted(set(re.sub(r'/\d+', '/N', p) for p in changed)), changedCount=len(changed), unallowed=unallowed)
    (B / 'equality-projection.json').write_text(json.dumps(projection, indent=2) + '\n')
    rows.append(dict(name='equality-projection', exitCode=0 if not any(v['unallowed'] for v in projection.values()) else 1, niceness=10))
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines())
    (B / 'edited.json').write_text(json.dumps(dict(paths=edited, rustEdited=[x for x in edited if x.endswith('.rs')]), indent=2) + '\n')
    rows.append(dict(name='no-rust-edited', exitCode=0 if not any(x.endswith('.rs') for x in edited) else 1, niceness=10))
    steps = [('d15-soundness', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'the_census_bounds_the_composed_discovery_at_every_root_length', '--nocapture']),
             ('census-and-discovery-tests', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'discovery_', 'workspace_', 'git_tracking']),
             ('discovery-census-vectors', [PY, '-I', '-B', DC, '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-fw01-pin', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('discovery-walk-storage', [PY, '-I', '-B', 'tools/tests/test_discovery_walk_storage.py', '-v']),
             ('discovery-census-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census.py', '-v']),
             ('discovery-census-blind-controls', BLIND_CONTROLS + ['-v']),
             ('discovery-census', [PY, '-I', '-B', DC, '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]),
             ('blind-equivalence', [PY, '-I', '-B', '-c', EQUIVALENCE, str(W), str(A), str(P), CACHE]),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args if name != 'blind-equivalence' else ['<EQUIVALENCE>', *args[5:]], exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    (B / 'blind-equivalence-program.py').write_text(EQUIVALENCE.lstrip())
    controls = []
    for name, before, after in MUTATIONS:
        path = W / DC; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(BLIND_CONTROLS, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and re.search(r'^FAILED \(failures=\d+\)$', out, re.M) is not None
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=DC, caught=caught, failed=sorted(re.findall(r'^FAIL: (\S+)', out, re.M))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        heldOutStoreOpened=False, installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(),
        productBase=git(P, 'rev-parse', 'HEAD'), standing='UNREVIEWED B3-B3A2 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
