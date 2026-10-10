from pathlib import Path
import os,subprocess,tempfile,time,json
D=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');lane=D/'opensip-lanes.lock';owned=False
B=Path('/tmp/opensip-implementation/sm-public-cache-intake-2026-10-10');P=B/'producer';os.setpriority(os.PRIO_PROCESS,0,10)
T=Path(tempfile.mkdtemp(prefix='opensip-sm-control-checks-',dir=D));T.chmod(0o700)
E=dict(os.environ);E.update(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_DIR=str(B/'check-target'))
E['SDKROOT']=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip()
initial_home=os.environ.get('HOME')
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary checks lane',flush=True);time.sleep(5)
try:
 for relative,cwd in [('src/process_builder.rs',P/'crates/cargo-util'),('src/cargo/util/rustc.rs',P),('src/cargo/util/context/mod.rs',P),('src/cargo/util/context/experimental_public_cache_intake.rs',P)]:
  code=subprocess.call(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','--config','skip_children=true',relative],cwd=cwd,env=E)
  if code:raise RuntimeError('isolated formatter failed')
 with (B/'public-intake-controls-r2.log').open('wb') as log:
  argv=['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','--config','source.crates-io.replace-with="opensip-vendor"','--config','source.opensip-vendor.directory="/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09/vendor"','-p','cargo','--lib','experimental_public_cache_intake','--','--nocapture']
  child=subprocess.Popen(argv,cwd=P,env=E,stdout=log,stderr=log)
  print('Ordinary isolated public cache intake control started',child.pid,flush=True);code=child.wait()
 (B/'public-intake-checks-r2.json').write_text(json.dumps(dict(exitCode=code,argv=argv,privateTMPDIR=str(T),ownedLane=True,niceness=os.getpriority(os.PRIO_PROCESS,0),HOMEUnchanged=os.environ.get('HOME')==initial_home,fullSM=False,nativeAdmission=False),indent=2)+'\n')
 print('Public cache intake checks exit',code,flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
