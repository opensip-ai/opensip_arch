"""C1a1 candidate checks, round 3 after Codex codex-c1a1-r2 (M3-C r8 items 1 and 2: the snapshot root, its pre-walk
opener, the extent walk and its charge model; C1a plan r4 as amended by the accepted r5 and r6, C1a1 preparatory): the
security suite on the base checkout and the candidate (--no-fail-fast, equal
failure sets after isolated reruns, the new passing tests), rustfmt on the new files, warning-denied all-targets Clippy on
opensip-security, the snapshot walk tests, the charge model --check, the T2 census --check over the lead-readable cache
(the census records unchanged), the operability source census, the census-closure check (no closure file changed),
verify_design, and mutations: walk mutations must fail the walk tests; model undercounts, regenerated, must fail the
soundness control. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1a1'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
SW = 'crates/security/src/snapshot_walk.rs'; SS = 'crates/security/src/snapshot_source.rs'; MODEL = 'tools/security/snapshot_ledger_model.py'
VECTORS = 'crates/security/src/snapshot_ledger_vectors.json'
NEW_TESTS = 16
YAML_TESTS = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'snapshot_walk']
SOUNDNESS = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'snapshot_walk::tests::the_native_walk_never_charges_more_than_the_model_predicts', 'snapshot_walk::tests::the_pre_walk_opener_charges_exactly_the_models_prediction']
T2 = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'
MUTATIONS = [
    # (name, file, before, after): each weakens one item 2 rule; the walk tests must fail.
    ('pruned-tree-entered', SW, "        if rule::classify_path(&rel, &known, extent.member_roots).is_some() {\n", "        if false {\n"),
    ('ignore-paths-skipped', SW, "        if extent.ignored(&rel) {\n", "        if false {\n"),
    ('boundary-entered', SW, "        if extent.boundaries.is_boundary(&rel) {\n", "        if false {\n"),
    ('directory-custody-ignored', SW, "                    return Err(lift(\n                        refuse::<()>(SnapshotRefusal::Custody { path: rel, reason }).unwrap_err(),\n                    ));\n", "                    let _ = reason;\n"),
    ('regular-open-not-compared', SS, "    if !same_object(observed, &sample) {\n", "    if false {\n"),
    ('directory-open-not-compared', SS, "    if !observation.matches(&sample) {\n", "    if false {\n"),
    ('marker-custody-row-ignored', SW, "                if marker\n                    && extent\n", "                if false\n                    && extent\n"),
    ('symlink-not-reported', SW, "                report.symlinks.push(rel);\n", ""),
    # r2 (Codex C1A1-R1-RF-1 to RF-3).
    ('opensip-anchor-observed', SW, "    if let Some(index) = anchor {\n        drop(paths.remove(index));\n    }\n", "    drop(anchor);\n"),
    ('boundary-for-directories-only', SW, "        if extent.boundaries.is_boundary(&rel) {\n",
     "        if matches!(kind, ChildKind::Directory) && extent.boundaries.is_boundary(&rel) {\n"),
    ('opener-root-not-judged', SS, "        judge_root(self, custody, work)?;\n", ""),
    # r3 (Codex C1A1-R2-RF-1).
    ('opener-validator-uncharged', SS, "        work.charge::<SnapshotRefusal>(owned(path.len()))?;\n        let Ok(validated)", "        let Ok(validated)"),
    ('extent-validation-uncharged', SW, "            work.charge::<IgnorePathInvalid>(owned(path.len()))?;\n", ""),
]
# (name, before, after) on the model: each undercount, regenerated, must fail the soundness control.
MODEL_MUTATIONS = [
    ('model-classify-dropped', "            self.classify(child)\n", ""),
    ('model-name-copies-free', "            self.add((co, ce, two * (blen(rel) + 1 + blen(name)) + tworec * self.c['RECORD']))\n", "            self.add((co, ce, two * (blen(rel) + 1) + tworec * self.c['RECORD']))\n"),
    ('model-directory-capture-dropped', "                self.capture(child)\n                self.owned(0)\n", "                self.owned(0)\n"),
    # r2 (Codex C1A1-R1-RF-1 and RF-4).
    ('model-anchor-classification-free', "        self.classify(rel)\n        hit = self.rule", "        hit = self.rule"),
    ('model-root-frame-free', "        self.owned(0)                   # the root frame\n", ""),
    ('model-member-lists-free', "        lists = [m for m in self.members if m]\n", "        lists = []\n"),
    # r3 (Codex C1A1-R2-RF-1).
    ('model-opener-validator-free', "    m.owned(blen(path))\n", ""),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-c1a1-check-', dir=D)); T.chmod(0o700)
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
    # A test failing on one side only is rerun alone, three times on each side: it is flaky (and not a
    # difference) only if every isolated run passes on both.
    differing = sorted(set(base['failed']) ^ set(cand['failed']))
    flaky = []
    for name in differing:
        runs = []
        for root in (P, W):
            for _ in range(3):
                r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', '--exact', name], cwd=root, env=E, capture_output=True)
                runs.append(r.returncode == 0 and b'1 passed' in r.stdout)
        (B / ('isolated-' + name.replace(':', '_') + '.json')).write_text(json.dumps(dict(test=name, runs=runs), indent=2) + '\n')
        if all(runs):
            flaky.append(name)
    comparison = dict(base=base, candidate=cand, differing=differing, flakyInIsolation=flaky, equalFailureSets=set(base['failed']) - set(flaky) == set(cand['failed']) - set(flaky), candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'] + len([f for f in flaky if f in cand['failed']]) - len([f for f in flaky if f in base['failed']]))
    print('host base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='security-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesEqualBase'] and comparison['newPassingTests'] == NEW_TESTS else 1, niceness=10)]
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('snapshot-walk-tests', YAML_TESTS + ['--nocapture']),
             ('snapshot-ledger-model', [PY, '-I', '-B', MODEL, '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-census', [PY, '-I', '-B', 'tools/security/discovery_census.py', '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', T2]),
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
                r = subprocess.run(YAML_TESTS, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = r.returncode != 0 and 'could not compile' not in out and 'test result: FAILED' in out
        finally:
            path.write_bytes(original)
        assert path.read_bytes() == original
        controls.append(dict(kind='mutation', name=name, file=ys, caught=caught, failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', out, re.M)))))
        print('mutation', name, caught, flush=True)
    for name, before, after in MODEL_MUTATIONS:
        model = W / MODEL; vectors = W / VECTORS; original = model.read_bytes(); saved = vectors.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        model.write_text(text.replace(before, after))
        try:
            with (B / f'mutation-{name}.log').open('wb') as log:
                g = subprocess.run([PY, '-I', '-B', MODEL, '--write', '--architecture', str(A), '--packages-root', str(P)], cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
                r = subprocess.run(SOUNDNESS, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
            out = (B / f'mutation-{name}.log').read_text(errors='replace')
            caught = g.returncode == 0 and r.returncode != 0 and ('over the model' in out or 'test result: FAILED' in out)
        finally:
            model.write_bytes(original); vectors.write_bytes(saved)
        assert model.read_bytes() == original and vectors.read_bytes() == saved
        controls.append(dict(kind='model-mutation', name=name, file=MODEL, caught=caught))
        print('mutation', name, caught, flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='mutation-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED C1a1 r3 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
