from pathlib import Path
import os,subprocess,tempfile,time,json
P=Path('/Users/sb/code/opensip-ai/opensip-dtmd1');B=Path('/tmp/opensip-implementation/dtmd1-product-checks-r1');B.mkdir();D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=D/'opensip-lanes.lock';owned=False;os.setpriority(os.PRIO_PROCESS,0,10)
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:print('Waiting for ordinary lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-dtmd1-check-',dir=D));T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:E.pop(k,None)
 steps=[('fmt',['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','src/dependency_transport_digest.rs'],P/'crates/host'),('digest-test',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib','dependency_transport_digest'],P),('scope-regression',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','opensip-host','--lib','rust_scope_data'],P),('clippy',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','clippy','--locked','--offline','-p','opensip-host','--all-targets','--','-D','warnings'],P)];rows=[]
 for name,args,cwd in steps:
  print(name,'starting',flush=True)
  with (B/(name+'.log')).open('wb') as log:
   child=subprocess.Popen(args,cwd=cwd,env=E,stdout=log,stderr=subprocess.STDOUT);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;code=child.wait()
  rows.append(dict(name=name,args=args,cwd=str(cwd),exitCode=code,niceness=priority));print(name,'exit',code,flush=True)
  if code:print((B/(name+'.log')).read_text()[-5000:],flush=True);break
 (B/'checks.json').write_text(json.dumps(dict(rows=rows,allPassed=len(rows)==len(steps) and all(r['exitCode']==0 for r in rows),privateTMPDIR=str(T),TMPDIRMode='0700',laneOwnedByThisProcess=True,installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists()),indent=2)+'\n')
finally:
 if owned:lane.rmdir()
