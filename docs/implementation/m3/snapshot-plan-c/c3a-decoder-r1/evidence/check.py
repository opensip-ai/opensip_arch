from pathlib import Path
import os,subprocess,tempfile,time,json,sys
P=Path('/Users/sb/code/opensip-ai/opensip-c3a-decoder');R=Path('/tmp/opensip-implementation/c3a-decoder-r1-authoring');LANE=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock')
env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',AR='/usr/bin/ar');env['SDKROOT']=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip();temp=Path(tempfile.mkdtemp(prefix='opensip-c3a-check-',dir=str(LANE.parent)));temp.chmod(0o700);env['TMPDIR']=str(temp)
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
lane('format',['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','src/archive_decoder.rs'],P/'crates/host')
mode=sys.argv[1] if len(sys.argv)>1 else 'full'
if mode=='focused':
 lane('guard',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib','finalization::tests::no_other_host_module_coordinates_a_commit'])
 lane('decoder',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib','archive_decoder'])
elif mode=='full':
 lane('test',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib'])
if mode=='verify':
 lane('metadata',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','metadata','--locked','--offline','--format-version','1','--filter-platform','aarch64-apple-darwin'])
 r=subprocess.run(['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B','tools/archive/check_dependencies.py','--repository',str(P),'--metadata',str(R/'metadata.log'),'--policy',str(P/'tools/archive/dependency-policy.json'),'--cargo-home','/Users/sb/.cargo'],cwd=P,env=env,capture_output=True)
 (R/'dependency-closure.log').write_bytes(r.stdout+r.stderr);print('dependency-closure',r.returncode,flush=True)
 if r.returncode:print((r.stdout+r.stderr).decode(),flush=True)
 assert r.returncode==0
 lane('clippy',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','clippy','--locked','--offline','-p','opensip-host','--all-targets','--','-D','warnings'])
 lane('release',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','check','--locked','--offline','-p','opensip-host','--release'])
 lane('test',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib'])
print('Requested candidate checks complete; no source/profile/wholeC3a/qualification claim',flush=True)
