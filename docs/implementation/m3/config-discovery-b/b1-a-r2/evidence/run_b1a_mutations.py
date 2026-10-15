"""B1-a mutation controls: each mutation is applied to configuration.rs in the worktree, the configuration tests run in the lane,
the failing tests are recorded, and the original bytes are restored (checked by SHA-256). A mutation no test catches is reported."""
from pathlib import Path
import hashlib, json, os, re, subprocess, tempfile, time
W = Path('/Users/sb/code/opensip-ai/opensip-b1a'); F = W / 'crates/host/src/configuration.rs'
OUT = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/b1a/evidence/mutations'); OUT.mkdir(parents=True)
MUTATIONS = [
    ('allowlist-off', '                Some(row) if !row.3.contains(&layer) => {', '                Some(row) if row.3.is_empty() => {'),
    ('ci-reads-local', '    let local = if input.mode.interactive {', '    let local = if true {'),
    ('digest-unnormalized', '    let semantic = normalize(&V::Object(semantic), "")?;', '    let semantic = V::Object(semantic);'),
    ('operational-in-digest', '            FieldClass::HostOperabilityNonsemantic => &mut operational,', '            FieldClass::HostOperabilityNonsemantic => &mut semantic,'),
    ('allowed-scopes-sorted', '        V::Array(values) if key == "allowedScopes" => V::Array(values.clone()),', '        V::Array(values) if key == "allowedScopesX" => V::Array(values.clone()),'),
    ('pin-hold-cross-check-off', '                exact.push((id, won.layer, pointer));', '                if field == "pins" {\n                    exact.push((id, won.layer, pointer));\n                }'),
    ('conflict-blamed-on-second', '                    let (layer, pointer) = if host_built(won.layer) && !host_built(*first_layer) {', '                    let (layer, pointer) = if false && !host_built(*first_layer) {'),
    ('completeness-on-winners', '        if !compiled || leaf("analysis", field).is_none() {', '        if (compiled && false) || leaf("analysis", field).is_none() {'),
    ('root-sentinel-for-entry-points', '                let sentinel = path == "." && field != "entryPoints";', '                let sentinel = path == ".";'),
    ('host-layer-as-external', '        Layer::Defaults | Layer::Flags => true,', '        Layer::Defaults | Layer::Flags => false,'),
]
original = F.read_bytes(); digest = hashlib.sha256(original).hexdigest()
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'
os.setpriority(os.PRIO_PROCESS, 0, 10)
while True:
    try: lane.mkdir(); break
    except FileExistsError: time.sleep(5)
rows = []
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b1a-mut-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
             CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    for name, before, after in MUTATIONS:
        text = original.decode(); assert text.count(before) == 1, name
        F.write_text(text.replace(before, after))
        try:
            r = subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo', 'test', '--locked', '--offline', '-p', 'opensip-host', '--lib', 'configuration'], cwd=W, env=E, capture_output=True, text=True)
        finally:
            F.write_bytes(original)
        log = r.stdout + r.stderr; (OUT / (name + '.log')).write_text(log)
        failed = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', log, re.M)))
        compiled = 'test result:' in log
        rows.append(dict(mutation=name, before=before.strip(), after=after.strip(), compiled=compiled, exitCode=r.returncode, failedTests=failed, caught=compiled and bool(failed)))
        print(name, 'caught' if failed else 'NOT CAUGHT', len(failed), flush=True)
    assert hashlib.sha256(F.read_bytes()).hexdigest() == digest
finally:
    lane.rmdir()
(OUT / 'mutations.json').write_text(json.dumps(dict(rows=rows, allCaught=all(r['caught'] for r in rows), restoredSha256=digest, standing='UNREVIEWED B1-a MUTATION CONTROLS'), indent=2) + '\n')
