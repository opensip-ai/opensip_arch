"""D2b-1 candidate checks (M3-D r5 item 10, the shared provider wire mechanics; D2b plan r3, sub-unit D2b-1; unit
round 1): the components and identity suites on the base checkout and the candidate, with equal failure sets after
isolated reruns and the new passing tests; rustfmt on the new and base-clean edited files; warning-denied all-targets
Clippy on opensip-components and opensip-identity; the provider protocol tests; the differential corpus regenerated
byte for byte from trial 07's reference decoder; the package edges under the O1-a package policy; the environment
exceptions; the operability source census; the census-closure check (no closure file changed); verify_design; and ten
mutations, each of which must fail the provider protocol tests. One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d2b'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
PP = 'crates/components/src/provider_protocol.rs'; CB = 'crates/components/src/provider_protocol/cbor.rs'
# The new passing tests per suite: components 17 (cbor 8, frames 9), identity none (is_nfc is exercised by components).
NEW_TESTS = {'opensip-components': 19, 'opensip-identity': 0}
# Both suites keep their binaries: the tests are the lib's own.
NEW_SUITES = 0
YAML_TESTS = [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-components', '--lib', 'provider_protocol']
MUTATIONS = [
    # (name, file, before, after): each weakens one item 10 rule; the provider protocol tests must fail.
    ('non-shortest-accepted', CB, "    if !shortest {\n", "    if false {\n"),
    ('unsorted-map-accepted', CB, "                            if raw <= prior {\n", "                            if raw == prior {\n"),
    ('tag-accepted', CB, "            6 => return Err(CborRefusal::Tag),\n", "            6 => Value::Null,\n"),
    ('non-nfc-accepted', CB, "                            if !opensip_identity::is_nfc(text) {\n", "                            if false {\n"),
    ('depth-unchecked', CB, "                        if stack.len() + 1 > max_depth {\n", "                        if false {\n"),
    ('length-checked-after-allocation', PP,
     "    if length > MAX_FRAME_PAYLOAD_BYTES || remaining.is_some_and(|r| length > r) {\n        return Err(FrameRefusal::Oversize(length));\n    }\n    let mut digest = [0u8; 32];\n    if !read_exact_or_eof(reader, &mut digest)? {\n        return Err(FrameRefusal::Truncated);\n    }\n    let mut payload = vec![0u8; length as usize];\n",
     "    let mut digest = [0u8; 32];\n    if !read_exact_or_eof(reader, &mut digest)? {\n        return Err(FrameRefusal::Truncated);\n    }\n    let mut payload = vec![0u8; length.min(MAX_FRAME_PAYLOAD_BYTES + 1) as usize];\n    if length > MAX_FRAME_PAYLOAD_BYTES || remaining.is_some_and(|r| length > r) {\n        return Err(FrameRefusal::Oversize(length));\n    }\n"),
    ('digest-unchecked', PP, "        return Err(FrameRefusal::Truncated);\n    }\n    if raw_sha256(&payload) != digest {\n",
     "        return Err(FrameRefusal::Truncated);\n    }\n    if false {\n"),
    ('accumulator-digest-unchecked', PP, "        self.have = 0;\n        if raw_sha256(&payload) != digest {\n",
     "        self.have = 0;\n        if false {\n"),
    # r2 (Codex D2B1-R1-RF-2): the length phase copying on into the digest.
    ('accumulator-length-after-digest', PP, "            self.take_prefix(bytes, 8);\n",
     "            self.take_prefix(bytes, FRAME_PREFIX_BYTES);\n"),
    # r2 (Codex D2B1-R1-RF-1): the frames completed before a refusal dropped.
    ('accumulator-frames-dropped-on-refusal', PP, "                    pushed.refusal = Some(refusal);\n",
     "                    pushed.refusal = Some(refusal);\n                    pushed.frames.clear();\n"),
    ('received-node-copied', PP, "        Some(ReceivedBytes(&self.payload[span.start..span.end]))\n",
     "        Some(ReceivedBytes(Box::leak(self.payload[span.start..span.end].to_vec().into_boxed_slice())))\n"),
]
# The package edges (tools/check_package_edges.py) under the O1-a package policy: components may take only its permitted
# internal edges, here opensip-contracts and opensip-identity, both normal since D2b-1.
PACKAGE_EDGES = ("import json,subprocess,sys;R,PY,A,W=sys.argv[1:5];m=subprocess.run([R+'cargo','metadata','--format-version','1','--offline','--locked'],"
                 "capture_output=True,check=True,cwd=W).stdout;open(sys.argv[5],'wb').write(m);"
                 "r=subprocess.run([PY,'-I','-B','tools/check_package_edges.py','--repository',W,'--metadata',sys.argv[5],'--inventory',"
                 "A+'/'+json.load(open(W+'/design-lock.json'))['inventorySuccessors'][-1]['candidate']['path'],'--lane','host','--package-policy',"
                 "A+'/docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json','--architecture',A,'--lock','design-lock.json'],cwd=W,capture_output=True);"
                 "sys.stdout.write(r.stdout.decode()+r.stderr.decode());j=json.loads(r.stdout);"
                 "e=sorted((x['to'],x['kinds'][0]['kind'] or 'normal') for x in j['resolvedInternalEdges'] if x['from']=='opensip-components');"
                 "print(e);sys.exit(0 if j['passed'] and e==[('opensip-contracts','normal'),('opensip-identity','normal')] else 1)")
# The differential corpus, regenerated from trial 07's reference decoder (read in place), must equal the vendored bytes.
DIFFERENTIAL = [PY, '-I', '-B', str(Path(__file__).parent / 'build_cbor_differential.py'), str(A), 'crates/components/tests/data/cbor-differential.v1.json', '--check']
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-d2b1-check-', dir=D)); T.chmod(0o700)
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
    rows = []
    for pkg in ('opensip-components', 'opensip-identity'):
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        # A test failing on one side only is rerun alone, three times on each side: it is flaky (and not a
        # difference) only if every isolated run passes on both.
        differing = sorted(set(base['failed']) ^ set(cand['failed']))
        flaky = []
        for name in differing:
            runs = []
            for root in (P, W):
                for _ in range(3):
                    r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', pkg, '--', '--exact', name], cwd=root, env=E, capture_output=True)
                    runs.append(r.returncode == 0 and b'1 passed' in r.stdout)
            (B / ('isolated-' + name.replace(':', '_') + '.json')).write_text(json.dumps(dict(test=name, runs=runs), indent=2) + '\n')
            if all(runs):
                flaky.append(name)
        comparison = dict(base=base, candidate=cand, differing=differing, flakyInIsolation=flaky, equalFailureSets=set(base['failed']) - set(flaky) == set(cand['failed']) - set(flaky), candidateSuitesAddNew=cand['suites'] == base['suites'] + NEW_SUITES, newPassingTests=cand['passed'] - base['passed'] + len([f for f in flaky if f in cand['failed']]) - len([f for f in flaky if f in base['failed']]))
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
        (B / f'test-comparison-{pkg}.json').write_text(json.dumps(comparison, indent=2) + '\n')
        rows.append(dict(name=f'{pkg}-base-comparison', exitCode=0 if comparison['equalFailureSets'] and comparison['candidateSuitesAddNew'] and comparison['newPassingTests'] == NEW_TESTS[pkg] else 1, niceness=10))
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
    steps = [('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-components', '-p', 'opensip-identity', '--all-targets', '--', '-D', 'warnings']),
             ('provider-protocol-tests', YAML_TESTS),
             ('cbor-differential-current', DIFFERENTIAL),
             ('package-edges', [PY, '-I', '-B', '-c', PACKAGE_EDGES, R, PY, str(A), str(W), str(T / 'cargo-metadata.json')]),
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
                r = subprocess.run(YAML_TESTS, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT)
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
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), productBase=git(P, 'rev-parse', 'HEAD'),
        rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False], standing='UNREVIEWED D2b-1 r2 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
