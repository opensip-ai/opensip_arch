"""B-S10 candidate checks (rust3 identity precedent's lane/toolchain recipe): identity dependency policy, fmt, identity/contracts/host
tests, warning-denied all-targets clippy, and the report TypeScript lane (pinned ignored inputs copied as the precedent did)."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, stat
W = Path('/Users/sb/code/opensip-ai/opensip-b-s10'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/b-s10/checks-r9'); B.mkdir()
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
# copy pinned ignored TypeScript lane inputs (as run_rust3_identity_report_check_r1.py)
lanes = json.loads((W / 'tools/typescript-lanes.json').read_bytes()); copied = 0
for row in lanes['files']:
    t = W / row['path']
    if t.exists(): continue
    assert row['path'].startswith('tools/typescript-boundary/node_modules/'), row['path']
    src = P / row['path']; raw = src.read_bytes(); assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    t.parent.mkdir(parents=True, exist_ok=True); t.write_bytes(raw); t.chmod(stat.S_IMODE(src.lstat().st_mode)); copied += 1
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b-s10-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
    # r2: the identity dependency policy is stale at the product base (source census differs; checks-r1 and a base run); it is
    # recorded informationally for base and candidate, which must fail identically, and is not a gate of this unit.
    idcmd = [PY, '-I', '-B', 'tools/check_identity_dependencies.py', '--manifest', 'Cargo.toml', '--target', 'aarch64-apple-darwin', '--cargo', R + 'cargo', '--archives', '/Users/sb/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f', '--policy', 'tools/identity/dependency-policy.json']
    info = {}
    for label, root in [('base', P), ('candidate', W)]:
        r = subprocess.run(idcmd, cwd=root, env=E, capture_output=True, text=True); info[label] = dict(exitCode=r.returncode, tail=(r.stdout + r.stderr).strip().splitlines()[-1:])
    assert info['base']['tail'] == [x.replace(str(W), str(P)) for x in info['candidate']['tail']], info
    (B / 'identity-policy-baseline.json').write_text(json.dumps(dict(info, standing='PRE-EXISTING STALE IDENTITY DEPENDENCY POLICY; IDENTICAL AT BASE AND CANDIDATE; INFORMATIONAL'), indent=2) + '\n')
    steps = [('rustfmt-edited', [R + 'rustfmt', '--edition', '2024', '--check', 'crates/identity/src/schema_registry.rs', 'crates/host/src/schema_sources.rs', 'crates/storage/src/schema_sources.rs']),  # r5: the two hand-edited files; host/identity crates are not fmt-clean at base (checks-r2, r4)
             ('identity-tests', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-identity']),
             ('contracts-tests', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-contracts']),
             
             ('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-identity', '-p', 'opensip-contracts', '-p', 'opensip-host', '-p', 'opensip-storage', '--all-targets', '--', '-D', 'warnings']),
             ('report-lane', [PY, '-I', '-B', 'tools/check_typescript.py', '--root', str(W), '--architecture', str(A), '--node', '/Users/sb/.nvm/versions/node/v24.16.0/bin/node', '--lane', 'report'])]
    # r8: host and storage suites run --no-fail-fast on the base checkout and on the candidate; the failure sets must be equal.
    # Base host admission_tests already fail 8 crash-matrix synthetic cases (PayloadSchemaDocument reconstruction), pre-existing.
    import re
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    comparison = {}
    for pkg in ['opensip-host', 'opensip-storage']:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate'); comparison[pkg] = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesAtLeastBase=cand['suites'] >= base['suites'])
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='host-storage-base-comparison', exitCode=0 if all(c['equalFailureSets'] and c['candidateSuitesAtLeastBase'] for c in comparison.values()) else 1, niceness=10)]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
        if code: print((B / (name + '.log')).read_text()[-4000:], flush=True); break
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=len(rows) == len(steps) and all(r['exitCode'] == 0 for r in rows), typescriptPinnedInputsCopied=copied, privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
                                                   installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), standing='UNREVIEWED B-S10 CANDIDATE CHECKS'), indent=2) + '\n')
finally:
    if owned: lane.rmdir()
