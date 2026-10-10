from pathlib import Path
import os,subprocess,tempfile,time,json
W=Path('/Users/sb/code/opensip-ai/opensip-host-native-current');B=Path(__file__).resolve().parent/'checks-r1';B.mkdir();D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False;os.setpriority(os.PRIO_PROCESS,0,10)
while not owned:
 try:lock.mkdir();owned=True
 except FileExistsError:print('Waiting for ordinary lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-native-current-',dir=D));T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip())
 for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(k,None)
 R='/opt/homebrew/Cellar/rust/1.95.0/bin/';args=[R+'rustfmt','--edition','2024','--config','skip_children=true','src/native_owner_tests.rs'];p=subprocess.run(args,cwd=W/'crates/host',env=E,capture_output=True);(B/'format.log').write_bytes(p.stdout+p.stderr);assert p.returncode==0
 args=[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','native_owner_tests'];print('Native owner corpus checks starting',flush=True)
 with(B/'native-owner.log').open('wb')as log:
  p=subprocess.Popen(args,cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT);priority=os.getpriority(os.PRIO_PROCESS,p.pid);assert priority==10;code=p.wait()
 report=dict(command=args,exitCode=code,niceness=priority,TMPDIR=str(T),TMPDIRMode='0700',ordinaryLaneOwned=True,qualification=False);(B/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));print((B/'native-owner.log').read_text()[-12000:])
finally:
 if owned:lock.rmdir()
