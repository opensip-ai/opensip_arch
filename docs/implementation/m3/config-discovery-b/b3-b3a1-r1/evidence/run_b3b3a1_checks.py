"""B3-b3a1 candidate checks (the D15 terms of the T2 census; B3-b plan r2 section 4.2, amendment A5): the security suite on
the base checkout and the candidate (--no-fail-fast, equal failure sets, one new passing test), the equality projection of
both census records (only the closure, the two new sizes and the D15 fields change), rustfmt on new and base-clean edited
files, warning-denied all-targets Clippy on security (with and without scenario-fixtures), the measured-against-model
control and every census and discovery test, every vector check, the census tool's and blind receipt's controls, the
census (--check over the integrity-verified lead-readable T2 stores; held-out entries never opened), the environment
exceptions, the operability source census, verify_design, and one under-count mutation per term (each patches the model,
regenerates the vectors only, and the measured-against-model control must fail; the vectors are restored). One lane
hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-b3b3a1'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
DM = 'tools/security/discovery_member_model.py'; DC = 'tools/security/discovery_census.py'
CENSUS_JSON = 'crates/security/src/custody/discovery_census.json'; CENSUS_VECTORS = 'crates/security/src/custody/discovery_census_vectors.json'
NEW_TESTS = 1
SOUNDNESS = ['test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'the_census_bounds_the_composed_discovery_at_every_root_length']
VEC = lambda tool: [PY, '-I', '-B', 'tools/security/' + tool, '--check', '--architecture', str(A), '--packages-root', str(P)]
# The equality projection's allowlist (plan r2 section 4.2): every other field of both records equals the base's.
ALLOWED = {
    CENSUS_JSON: [r'/closure', r'/sizes/DescriptorMetadata', r'/sizes/\(Vec<u8>, DescriptorMetadata\)', r'/entries/\d+/d15'],
    CENSUS_VECTORS: [r'/closure', r'/sizes/DescriptorMetadata', r'/sizes/\(Vec<u8>, DescriptorMetadata\)', r'/compositionVectors',
                     r'/memberModel', r'/compositionCases'],
}
MUTATIONS = [
    # (name, file, before, after): one under-count per term; the measured-against-model control must fail.
    ('reader-carrier-read-dropped', DM, "        self.add(read_envelope(self.c, min(size, self.c['CARRIER_CAP'] + 1), self.c['CARRIER_CAP']))\n", ''),
    ('member-index-read-dropped', DM, "        n.add(read_envelope(self.c, self.c['INDEX_CAP'] + 1, self.c['INDEX_CAP']))\n", ''),
    ('member-session-device-dropped', DM, "        n.add(self.c['GIT_STATUS'])  # W's status, for the session's device\n", ''),
    ('descent-dropped', DM, "            term.add((o, e, blen(rel) + c['DESCRIPTOR_METADATA'] + c['RECORD'], 0))\n", '            pass\n'),
    ('walker-members-ignored', DC, '    m = model(c, rule, tree, source, roots, members)\n', '    m = model(c, rule, tree, source, roots)\n'),
]
def diff(a, b, p=''):
    if type(a) is not type(b): return [p]
    if isinstance(a, dict): return [x for k in sorted(set(a) | set(b)) for x in ([p + '/' + k] if k not in a or k not in b else diff(a[k], b[k], p + '/' + k))]
    if isinstance(a, list): return [p] if len(a) != len(b) else [x for i, (u, v) in enumerate(zip(a, b)) for x in diff(u, v, f'{p}/{i}')]
    return [] if a == b else [p]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b3b3a1-check-', dir=D)); T.chmod(0o700)
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
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines() if x.endswith('.rs'))
    def fmt_clean(raw):
        r = subprocess.run([R + 'rustfmt', '--edition', '2024', '--emit', 'stdout'], input=raw, env=E, capture_output=True)
        return r.returncode == 0 and r.stdout == raw
    fmt_rows = []
    for x in edited:
        base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + x], cwd=W, env=E, capture_output=True)
        fmt_rows.append(dict(path=x, baseClean=None if base_raw.returncode else fmt_clean(base_raw.stdout), candidateClean=fmt_clean((W / x).read_bytes())))
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    rows.append(dict(name='rustfmt-edited', exitCode=0 if all(r['candidateClean'] for r in fmt_rows if r['baseClean'] is not False) else 1, niceness=10))
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('clippy-scenario', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--features', 'scenario-fixtures', '--all-targets', '--', '-D', 'warnings']),
             ('d15-soundness', [R + 'cargo', *SOUNDNESS, '--nocapture']),
             ('census-and-discovery-tests', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'discovery_', 'workspace_', 'git_tracking']),
             ('workspace-discovery-vectors', VEC('workspace_discovery_vectors.py')),
             ('workspace-member-vectors', VEC('workspace_member_vectors.py')),
             ('discovery-member-vectors', VEC('discovery_member_vectors.py')),
             ('discovery-walk-vectors', VEC('discovery_walk_vectors.py')),
             ('discovery-scan-vectors', VEC('discovery_scan_vectors.py')),
             ('discovery-upward-vectors', VEC('discovery_upward_vectors.py')),
             ('discovery-rule-vectors', [PY, '-I', '-B', 'tools/security/discovery_rule_vectors.py', '--check', '--architecture', str(A)]),
             ('discovery-fw01-pin', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('discovery-walk-storage', [PY, '-I', '-B', 'tools/tests/test_discovery_walk_storage.py', '-v']),
             ('discovery-census-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census.py', '-v']),
             ('discovery-census-blind-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census_blind.py', '-v']),
             ('discovery-census', [PY, '-I', '-B', DC, '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    vectors_original = (W / CENSUS_VECTORS).read_bytes()
    for name, rel, before, after in MUTATIONS:
        path = W / rel; original = path.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        path.write_text(text.replace(before, after))
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                regen = subprocess.run([PY, '-I', '-B', DC, '--write', '--architecture', str(A), '--packages-root', str(P)], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
                r = subprocess.run([R + 'cargo', *SOUNDNESS], cwd=W, env=E, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                log.write(r.stdout)
            out = r.stdout.decode(errors='replace')
            caught = regen.returncode == 0 and 'could not compile' not in out and r.returncode != 0 and 'the census predicts' in out
        finally:
            path.write_bytes(original); (W / CENSUS_VECTORS).write_bytes(vectors_original)
        assert path.read_bytes() == original and (W / CENSUS_VECTORS).read_bytes() == vectors_original
        controls.append(dict(kind='mutation', name=name, file=rel, caught=caught))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        heldOutStoreOpened=False, installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(),
        productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B3-B3A1 r1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
