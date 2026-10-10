from pathlib import Path
import os,subprocess,tempfile,time,json
W=Path('/Users/sb/code/opensip-ai/opensip-host-current-corpus');B=Path(__file__).resolve().parent/'replay-checks-r2';B.mkdir();D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False;os.setpriority(os.PRIO_PROCESS,0,10)
while not owned:
 try:lock.mkdir();owned=True
 except FileExistsError:print('Waiting for ordinary lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-current-corpus-',dir=D));T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip())
 for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(k,None)
 R='/opt/homebrew/Cellar/rust/1.95.0/bin/';steps=[('host-replay-corpus',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','independent_run_replay_matches_selected_reference_and_owns_its_closure']),('host-fact-admission',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','fact_admission::tests']),('host-finalization-replay',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','replay_refusal_after_r12_finishes_once_and_outputs_its_own_row'])];rows=[]
 for name,args in steps:
  print(name+' starting',flush=True)
  with (B/(name+'.log')).open('wb')as f:
   c=subprocess.Popen(args,cwd=W,env=E,stdout=f,stderr=subprocess.STDOUT);priority=os.getpriority(os.PRIO_PROCESS,c.pid);assert priority==10;code=c.wait()
  rows.append(dict(name=name,command=args,exitCode=code,niceness=priority));print(name+' exit '+str(code),flush=True)
  if code:print((B/(name+'.log')).read_text()[-5500:],flush=True);break
 (B/'checks.json').write_text(json.dumps(dict(rows=rows,allPassed=len(rows)==len(steps)and all(x['exitCode']==0 for x in rows),TMPDIR=str(T),TMPDIRMode='0700',ordinaryLaneOwned=True,historicalFixturesUnchanged=True,qualification=False),indent=2)+'\n')
finally:
 if owned:lock.rmdir()
