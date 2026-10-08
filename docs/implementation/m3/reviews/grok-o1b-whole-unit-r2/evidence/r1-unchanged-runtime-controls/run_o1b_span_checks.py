from pathlib import Path
import os,json,subprocess,tempfile,time
B=Path('/tmp/opensip-implementation/o1b-authoring-r1');P=B/'product';root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=root/'opensip-lanes.lock';owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 private=Path(tempfile.mkdtemp(prefix='opensip-o1b-phase-',dir=root));private.chmod(0o700);env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip(),CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/clang',CARGO_TARGET_X86_64_APPLE_DARWIN_LINKER='/usr/bin/clang')
 r=subprocess.run(['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','src/lib.rs'],cwd=P/'crates/operability',env=env,capture_output=True);assert r.returncode==0,r.stderr
 rows=[]
 for name,args in [('span-default-tests',['test','--lib']),('span-development-tests',['test','--lib','--features','operability-dev-sinks']),('span-harness-tests',['test','--lib','--features','harness-instrumentation']),('span-default-clippy',['clippy','--all-targets','--','-D','warnings']),('span-instrumented-clippy',['clippy','--all-targets','--features','operability-dev-sinks,harness-instrumentation','--','-D','warnings'])]:
  cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo',args[0],'--locked','--offline','-p','opensip-operability',*args[1:]];r=subprocess.run(cmd,cwd=P,env=env,capture_output=True);(B/(name+'.log')).write_bytes(r.stdout+r.stderr);print(name,r.returncode,flush=True);assert r.returncode==0,(r.stdout+r.stderr).decode()[-4500:];rows.append({'name':name,'passed':True})
 (B/'span-preparation-controls.json').write_text(json.dumps({'standing':'UNREVIEWED O1-b clock-anchored span/phase preparation; actual harness and host wiring work remains','passed':True,'checks':rows,'productQualification':False,'inventoryAuthored':False},indent=2)+'\n')
finally:
 if owned:lane.rmdir()
