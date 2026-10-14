# Rows-transport variant build: the accepted run_release_build.py recipe unchanged except its standing label; it builds
# this directory (Cargo.toml path deps into the git-archive export of product 37581132, the accepted Cargo.lock).
from pathlib import Path
import subprocess,os,tempfile,time,json,hashlib
B=Path(__file__).resolve().parent;D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for optimized replay build lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-native-build-',dir=D)).resolve();T.chmod(0o700);env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),CARGO_TARGET_DIR=str(B/'target'),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(k,None)
 env.update(RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',CXX='/usr/bin/clang++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip())
 command=['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','build','--release','--locked','--offline','--manifest-path',str(B/'Cargo.toml')]
 with (B/'build-release.log').open('wb')as out:r=subprocess.run(command,cwd=B,env=env,stdout=out,stderr=subprocess.STDOUT)
 assert r.returncode==0,(B/'build-release.log').read_text();p=B/'target/release/opensip-sm-replay-bench';raw=p.read_bytes();(B/'build-release.json').write_text(json.dumps(dict(standing='UNREVIEWED THROWAWAY FIRSTPARTY NATIVE REPLAY MEASUREMENT DRIVER; ROWS-TRANSPORT VARIANT OF THE CLOSED e82a4e2f DRIVER; PRODUCT EXPORT git archive 37581132',productExport='product-37581132',productCommit='37581132d8099b8fb4ad9ef8fb2f90ff8b89d02d',executable=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),locked=True,offline=True,privateTMPDIR=str(T),HOMEUnchanged=True,productSourceUnedited=True),indent=2)+'\n');print('rows variant release driver built',flush=True)
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
