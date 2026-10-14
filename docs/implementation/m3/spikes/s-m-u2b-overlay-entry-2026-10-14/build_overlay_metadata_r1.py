from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re
# Build the U-2b overlay metadata variant (accepted command-data producer clone + one appended ignored test) with the
# accepted controls recipe: cargo test --no-run, --locked --offline, vendored crates.io source, lane held.
V = Path(__file__).resolve().parent; P = V / 'producer'; os.setpriority(os.PRIO_PROCESS, 0, 10)
D = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T'); lane = D / 'opensip-lanes.lock'; owned = False
T = Path(tempfile.mkdtemp(prefix='opensip-u2b-overlay-build-', dir=D)); T.chmod(0o700)
E = {k: v for k, v in os.environ.items() if k not in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE')}
E.update(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), RUSTFLAGS='-C linker=/usr/bin/cc', CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar',
         CARGO_TARGET_DIR=str(V / 'check-target'), SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path'], text=True).strip(), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
argv = ['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo', 'test', '--locked', '--offline', '--config', 'source.crates-io.replace-with="opensip-vendor"', '--config',
        'source.opensip-vendor.directory="/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/cargo-producer-vendor"', '-p', 'cargo', '--lib', '--no-run']
while True:
    try: lane.mkdir(); owned = True; break
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    with (V / 'build.log').open('wb') as log: code = subprocess.run(argv, cwd=P, env=E, stdout=log, stderr=log).returncode
    assert code == 0, (V / 'build.log').read_text()[-3000:]
    exe = Path(re.search(r'Executable unittests src/cargo/lib.rs \(([^)]+)\)', (V / 'build.log').read_text())[1]); raw = exe.read_bytes()
    (V / 'build.json').write_text(json.dumps(dict(executable=str(exe), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), argv=argv, locked=True, offline=True), indent=2) + '\n'); print('built', exe, hashlib.sha256(raw).hexdigest())
finally:
    if owned: lane.rmdir()
