from pathlib import Path
import os, subprocess, tempfile, json, hashlib
# U-2b: rebuild the accepted hash_bridge.rs (s-m-context-identity-2026-10-09, unchanged source) against the current product
# opensip-identity crate, offline; lock generated offline then a --locked --offline release build.
H = Path(__file__).resolve().parent; os.setpriority(os.PRIO_PROCESS, 0, 10)
src = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes/s-m-context-identity-2026-10-09/hash_bridge.rs'); assert (H / 'src/main.rs').read_bytes() == src.read_bytes()
T = Path(tempfile.mkdtemp(prefix='opensip-u2b-bridge-build-', dir='/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T')); T.chmod(0o700)
env = {k: v for k, v in os.environ.items() if k not in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE')}
env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null', PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), CARGO_TARGET_DIR=str(H / 'target'),
           RUSTFLAGS='-C linker=/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
cargo = '/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'
with (H / 'build.log').open('wb') as log:
    if not (H / 'Cargo.lock').exists(): subprocess.run([cargo, 'generate-lockfile', '--offline'], cwd=H, env=env, stdout=log, stderr=log, check=True)
    subprocess.run([cargo, 'build', '--release', '--locked', '--offline'], cwd=H, env=env, stdout=log, stderr=log, check=True)
exe = H / 'target/release/opensip-u2b-hash-bridge'; raw = exe.read_bytes()
(H / 'build.json').write_text(json.dumps(dict(executable=str(exe), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), source=dict(path=str(src), sha256=hashlib.sha256(src.read_bytes()).hexdigest()), cargoLock=hashlib.sha256((H / 'Cargo.lock').read_bytes()).hexdigest(), locked=True, offline=True), indent=2) + '\n')
print('built', hashlib.sha256(raw).hexdigest())
