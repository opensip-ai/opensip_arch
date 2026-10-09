from pathlib import Path
import os,subprocess,tempfile,time,json,sys
P=Path('/Users/sb/code/opensip-ai/opensip-source-attempt');R=Path('/tmp/opensip-implementation/source-attempt-r1-authoring');LANE=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock')
env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',AR='/usr/bin/ar');env['SDKROOT']=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip();temp=Path(tempfile.mkdtemp(prefix='opensip-source-attempt-check-',dir=str(LANE.parent)));temp.chmod(0o700);env['TMPDIR']=str(temp)
for key in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(key,None)
env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
def lane(name,args,cwd=P):
 owned=False
 try:
  while not owned:
   try:LANE.mkdir();owned=True
   except FileExistsError:time.sleep(0.5)
  with(R/(name+'.log')).open('wb')as log:
   result=subprocess.run(['/usr/bin/nice','-n','10',*args],cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
  print(name,result.returncode,flush=True)
  if result.returncode:print((R/(name+'.log')).read_text()[-12000:],flush=True)
  assert result.returncode==0,name
 finally:
  if owned:LANE.rmdir()
lane('format',['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','src/acquisition_guard.rs'],P/'crates/host')
mode=sys.argv[1] if len(sys.argv)>1 else 'full'
if mode=='focused':
 lane('guard',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib','finalization::tests::no_other_host_module_coordinates_a_commit'])
 lane('copy-focused',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib','raw_stream_copy'])
elif mode=='full':
 lane('test',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib','acquisition_guard'])
if mode=='verify':
 lane('clippy',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','clippy','--locked','--offline','-p','opensip-host','--all-targets','--','-D','warnings'])
 lane('release',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','check','--locked','--offline','-p','opensip-host','--release'])
 lane('test',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib','acquisition_guard'])
print('Requested candidate checks complete; no source/profile/wholeC3a/qualification claim',flush=True)
