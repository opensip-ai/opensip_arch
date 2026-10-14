from pathlib import Path
import os,subprocess,tempfile,json,hashlib,time
# Build the site-walk v2 variant (U-3: adds literal and control-flow sites) of the closed framed driver with the closed build recipe (build_driver_r2.py): bare rustc, pinned 1.95 rustc-dev sysroot.
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path(__file__).resolve().parent;SYS=Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot');W=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes/s-m-framed-analysis-controls-2026-10-10/new-wrapper')
O=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=O/'opensip-lanes.lock';held=False
def pin(p):raw=Path(p).read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
assert pin(B/'closed-driver-source.rs')['sha256']=='43315ea6b81bd9b7a41174c1db41d50423b557ab6877be77db724ec96a7b75aa'
while True:
 try:lock.mkdir();held=True;break
 except FileExistsError:print('waiting for lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-site-driver-v2-build-',dir=O));T.chmod(0o700)
 env=dict(os.environ,TMPDIR=str(T),RUSTC_BOOTSTRAP='1',CARGO_HOME='/Users/sb/.cargo',PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip())
 sha=T/'libsha2_const_stable.rlib';first=[str(SYS/'bin/rustc'),'--edition','2018','--sysroot',str(SYS),'--crate-type','rlib','--crate-name','sha2_const_stable','-C','opt-level=3',str(W/'sha-library-source/src/lib.rs'),'-o',str(sha)]
 r=subprocess.run(first,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(B/'sha-build.log').write_bytes(r.stdout);assert r.returncode==0,r.stdout.decode()
 serde=SYS/'lib/rustlib/aarch64-apple-darwin/lib/libserde_json-9af384fe91ae3f17.rmeta'
 exe=T/'site-driver';cmd=[str(SYS/'bin/rustc'),'--edition','2024','--sysroot',str(SYS),'-C','prefer-dynamic','-C','rpath','-C','linker=/usr/bin/cc','--extern','sha2_const_stable='+str(sha),'--extern','serde_json='+str(serde),str(B/'driver.rs'),'-o',str(exe)]
 r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(B/'build.log').write_bytes(r.stdout);print(r.stdout.decode()[-6000:]);assert r.returncode==0
 (B/'build.json').write_text(json.dumps(dict(standing='UNREVIEWED OUTSIDE-PRODUCT SITE-WALK v2 VARIANT OF THE CLOSED FRAMED DRIVER',siteWalkV1Source=pin(B/'site_walk-v1.rs'),executable=str(exe),**{k:v for k,v in pin(exe).items() if k!='path'},driverSource=pin(B/'driver.rs'),siteWalkSource=pin(B/'site_walk.rs'),closedParentSource=pin(B/'closed-driver-source.rs'),linked=[pin(sha),pin(serde)],SHACompilation=first,command=cmd,bareRustc=True,CargoRun=False,RUSTC_BOOTSTRAPWrapperBuildOnly=True,corpusCodeCompiledOrExecuted=False,TMPDIR=str(T),TMPDIRMode='0700',sysroot=str(SYS)),indent=2)+'\n')
finally:
 if held:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
