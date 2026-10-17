"""C1a4-blind r2 gate checks (C1a plan r6 RF-3 steps 2 and 3; the owner's decision of 2026-10-16; B2-b4 plan r6 section
2.5; Codex C1A4-R1-NBO-1 and NBO-2): the security suite on the base checkout and the candidate (--no-fail-fast; equal
failure sets after isolated reruns; no new test, one extended); rustfmt on the edited base-clean files; warning-denied
all-targets Clippy on security; the focused census tests; the companion's and discovery's blind controls (synthetic and
hermetic); the equality projection of the companion record (only its new held-out fields, its tool pin and its standing
change); the census, workspace ledger and companion --checks over the lead-readable cache only; the blind equivalence
(the companion's blind row over every lead-readable store, presented as held out, equal to the record's row); the
census closure unchanged; the environment exceptions, the operability source census and verify_design; and mutations,
each of which must fail its focused tests. No held-out store is opened. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1a4'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
TOOL = 'tools/security/snapshot_ledger_census.py'; RECORD = 'crates/security/src/snapshot_ledger_census.json'; TESTS = 'crates/security/src/snapshot_walk_tests.rs'
NEW_TESTS = {'opensip-security': 0}
T2 = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
CARGO = [R + 'cargo', 'test', '--locked', '--offline']
FOCUSED = {
    'margin': CARGO + ['-p', 'opensip-security', '--lib', '--', 'snapshot_walk::tests::the_snapshot_census', 'custody::discovery_census'],
    'controls': [PY, '-I', '-B', 'tools/tests/test_snapshot_ledger_census_blind.py'],
}
EXPECTED_RECORD_CHANGES = {'added': ['capsStatus', 'heldOutEntries', 'heldOutMargin'], 'changed': ['counts', 'pins', 'standing'], 'counts': ['heldOut'], 'pins': [TOOL]}


def truncated(text):
    """The record with its first lead-readable row dropped and its counts kept consistent: only the identity-set
    check against discovery's record catches it (Codex C1A4-R1-NBO-2)."""
    body = json.loads(text); gone = body['entries'].pop(0)
    body['counts']['entries'] -= 1; body['counts']['measured' if gone['status'] == 'measured' else 'overItem5'] -= 1
    return json.dumps(body, indent=1, ensure_ascii=True) + '\n'


def duplicated(text):
    body = json.loads(text); body['entries'][1] = body['entries'][0]
    return json.dumps(body, indent=1, ensure_ascii=True) + '\n'


MUTATIONS = [
    # (name, file, before or transform, after, focused tests): each weakens one rule of this gate.
    ('receipt-sources-unbound', TOOL, "        paths |= set(slm.SESSION_FILES) | {slm.WORK_LEDGER} | set(ANCHORED)\n",
     "        paths |= set(slm.SESSION_FILES) | {slm.WORK_LEDGER}\n", 'controls'),
    ('receipt-freshness-unchecked', TOOL, "    if receipt['bindings'] != current:\n", "    if False:\n", 'controls'),
    ('blind-margins-walk-only', TOOL, "            margins = permille(self.caps[PROFILE], x['full'])\n",
     "            margins = permille(self.caps[PROFILE], x['walk'])\n", 'controls'),
    ('blind-population-unchecked', TOOL, "        if x['disc'].observed != expected:\n", "        if False:\n", 'controls'),
    ('blind-over-item-5-measured', TOOL, "        if x['over']:\n            return dict(id=entry['id'], status='over-item-5'",
     "        if False:\n            return dict(id=entry['id'], status='over-item-5'", 'controls'),
    ('blind-failure-text-printed', TOOL, "        print('Snapshot ledger census blind run failed.', file=sys.stderr)\n",
     "        print('Snapshot ledger census blind run failed.', sys.exc_info()[1], file=sys.stderr)\n", 'controls'),
    ('record-truncated-consistently', RECORD, truncated, None, 'margin'),
    ('record-id-duplicated', RECORD, duplicated, None, 'margin'),
]
EQUIVALENCE = r'''
import json, os, sys
from pathlib import Path
P = Path.cwd(); sys.path.insert(0, str(P / 'tools/security'))
import importlib.util
spec = importlib.util.spec_from_file_location('slc', P / 'tools/security/snapshot_ledger_census.py'); slc = importlib.util.module_from_spec(spec); spec.loader.exec_module(slc)
census = slc.Census(P, Path(sys.argv[1]), Path(sys.argv[2]))
record = json.loads((P / slc.OUTPUT).read_bytes()); rows = {r['id']: r for r in record['entries']}
manifest = json.loads((Path(sys.argv[1]) / census.dc.MANIFEST).read_bytes()); store = os.path.join(sys.argv[3], 'store')
out = []
for entry in manifest['repositories']:
    if entry['heldOut'] is not False:
        continue  # never a held-out store: only the lead-readable ones, each presented to the blind row as held out
    blind = census.blind_row(dict(entry, heldOut=True), store, census.dc._BLIND)
    row = rows[entry['id']]
    if row['status'] == 'over-item-5':
        ok = blind == dict(id=entry['id'], status='over-item-5', integrity=True, population=True)
    else:
        m = row['margins'][slc.PROFILE]
        ok = blind == dict(id=entry['id'], status='measured', integrity=True, population=True,
                           marginPermille={k: m[k]['marginPermille'] for k in slc.KEYS}, passes2x=m['passes2x'])
    out.append(dict(id=entry['id'], status=blind['status'], equal=ok))
    print(entry['id'], blind['status'], ok, flush=True)
json.dump(dict(rows=out, allEqual=all(r['equal'] for r in out), count=len(out)), open(sys.argv[4], 'w'), indent=2)
sys.exit(0 if out and all(r['equal'] for r in out) else 1)
'''
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1a4b-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    rows, comparisons = [], {}
    with (B / 'candidate-build.log').open('wb') as log:
        built = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '--no-run', '-p', 'opensip-security'], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT).returncode
    rows.append(dict(name='candidate-build', exitCode=built, niceness=10)); print('candidate-build exit', built, flush=True)
    if built != 0:
        (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=False, standing='UNREVIEWED C1a4-blind r2 GATE CHECKS: preflight failed'), indent=2) + '\n')
        raise SystemExit(1)

    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
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
    # The equality projection of the companion record: only its new held-out fields, its tool pin and its standing.
    old = json.loads(git(W, 'show', 'HEAD:' + RECORD)); new = json.loads((W / RECORD).read_bytes())
    projection = dict(added=sorted(set(new) - set(old)), removed=sorted(set(old) - set(new)), changed=sorted(k for k in old if k in new and old[k] != new[k]),
                      counts=sorted(k for k in set(old['counts']) | set(new['counts']) if old['counts'].get(k) != new['counts'].get(k)),
                      pins=sorted(o['path'] for o, n in zip(old['pins'], new['pins']) if o != n),
                      entriesEqual=old['entries'] == new['entries'], workspacesEqual=old['workspaces'] == new['workspaces'])
    projection['passed'] = (projection['entriesEqual'] and projection['workspacesEqual'] and projection['removed'] == []
                            and all(projection[k] == v for k, v in EXPECTED_RECORD_CHANGES.items()))
    (B / 'equality-projection.json').write_text(json.dumps(projection, indent=2) + '\n')
    rows.append(dict(name='equality-projection', exitCode=0 if projection['passed'] else 1, niceness=10))
    (B / 'blind-equivalence-program.py').write_text(EQUIVALENCE)
    closure_check = ("import re,sys,subprocess;src=open('tools/security/discovery_census.py').read();closure=set(re.findall(r\"\\('(crates/[^']+)', \\d+, '[0-9a-f]{64}'\\)\",src));"
                     "changed=set(subprocess.check_output(['/usr/bin/git','diff','--name-only','HEAD']).decode().split())|set(subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard']).decode().split());"
                     "hit=sorted(closure&changed);print(len(closure),'closure files;',sorted(changed),'changed; hit',hit);sys.exit(1 if hit or len(closure)<10 or 'tools/security/discovery_census.py' in changed else 0)")
    cache = ['--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2]
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('focused-margin-tests', FOCUSED['margin']),
             ('companion-blind-controls', FOCUSED['controls']),
             ('discovery-blind-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census_blind.py']),
             ('discovery-census-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census.py']),
             ('discovery-census', [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', *cache]),
             ('discovery-workspace-ledger', [PY, '-I', '-B', 'tools/security/discovery_workspace_ledger.py', '--check', *cache]),
             ('snapshot-ledger-census', [PY, '-I', '-B', TOOL, '--check', *cache]),
             ('blind-equivalence', [PY, '-I', '-B', str(B / 'blind-equivalence-program.py'), str(A), str(P), T2, str(B / 'blind-equivalence.json')]),
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
    for name, ys, before, after, focus in MUTATIONS:
        path = W / ys; original = path.read_bytes(); text = original.decode()
        if callable(before):
            mutated = before(text)
        else:
            assert text.count(before) == 1, name
            mutated = text.replace(before, after)
        path.write_text(mutated)
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                r = subprocess.run(FOCUSED[focus], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            failed_marker = 'test result: FAILED' in out if focus == 'margin' else re.search(r'^FAILED \(', out, re.M) is not None
            caught = r.returncode != 0 and 'could not compile' not in out and failed_marker
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=ys, focus=focus, caught=caught,
                             failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)) | set(re.findall(r'^(?:FAIL|ERROR): (\S+)', out, re.M)))))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'), heldOutStoreOpened=False,
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C1a4-blind r2 GATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
