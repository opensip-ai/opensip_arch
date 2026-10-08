from pathlib import Path
import subprocess,os,time,tempfile,json
B=Path('/tmp/opensip-implementation/o1b-authoring-r1');P=B/'product';root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=root/'opensip-lanes.lock';owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 r=subprocess.run(['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','src/phase_clock.rs'],cwd=P/'crates/operability',capture_output=True);assert r.returncode==0,r.stderr
finally:
 if owned:lane.rmdir()
private=Path(tempfile.mkdtemp(prefix='opensip-o1b-clock-',dir=root));private.chmod(0o700);env=dict(os.environ,TMPDIR=str(private));old=Path('/tmp/opensip-implementation/j3ao-authoring-r1');platform=list((old/'identity-controls-r2/development').glob('libopensip_platform*.rlib'));assert len(platform)==1
cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','--test',str(P/'crates/operability/src/phase_clock.rs'),'-o',str(B/'phase-clock-tests'),'-C','linker=/usr/bin/clang','-L','dependency='+str(old/'product/target/debug/deps'),'--extern','opensip_platform='+str(platform[0])];r=subprocess.run(cmd,env=env,capture_output=True);(B/'phase-clock-rustc.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr.decode()
r=subprocess.run(['/usr/bin/nice','-n','10',str(B/'phase-clock-tests')],env=env,capture_output=True);(B/'phase-clock-tests.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr.decode();(B/'phase-clock-controls.json').write_text(json.dumps({'standing':'DEPENDENT O1-b TIMING PREPARATION ONLY; not span/phase/harness completion','passed':True,'controls':4,'actualNativeObservationUsed':True,'strictTimingQualification':False,'productQualification':False,'inventoryAuthored':False,'realInstallationRead':False,'private413Read':False},indent=2)+'\n');print(r.stdout.decode())
