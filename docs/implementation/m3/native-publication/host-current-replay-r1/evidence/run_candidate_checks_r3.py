from pathlib import Path
import os,subprocess,tempfile,time,json
W=Path('/Users/sb/code/opensip-ai/opensip-host-current-corpus');B=Path(__file__).resolve().parent/'candidate-checks-r3';B.mkdir();D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False;os.setpriority(os.PRIO_PROCESS,0,10)
while not owned:
 try:lock.mkdir();owned=True
 except FileExistsError:print('Waiting for ordinary lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-current-corpus-',dir=D));T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip())
 for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(k,None)
 R='/opt/homebrew/Cellar/rust/1.95.0/bin/';rows=[]
 fmt=['crates/host/src/schema_sources.rs','crates/host/src/native_owner_tests.rs','crates/host/src/fact_admission_tests.rs','crates/host/src/finalization_tests.rs','crates/host/tests/admission_tests.rs','crates/evaluator/src/coverage.rs','crates/evaluator/src/import_payloads.rs','crates/evaluator/src/atoms.rs']
 for rel in fmt:
  crate=W/Path(rel).parts[0]/Path(rel).parts[1];local=str(Path(rel).relative_to(Path(rel).parts[0]+'/'+Path(rel).parts[1]));args=[R+'rustfmt','--edition','2024','--config','skip_children=true',local];result=subprocess.run(args,cwd=crate,env=E,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(B/(rel.replace('/','-')+'.fmt.log')).write_bytes(result.stdout);assert result.returncode==0
 steps=[('current-schema-guard',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','current_replay_schema_tests'],True),('evaluator-library',[R+'cargo','test','--locked','--offline','-p','opensip-evaluator','--lib'],True),('host-full-library',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib'],False),('host-clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-host','--all-targets','--','-D','warnings'],True),('evaluator-clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-evaluator','--all-targets','--','-D','warnings'],True)]
 for name,args,required in steps:
  print(name+' starting',flush=True)
  with (B/(name+'.log')).open('wb')as f:
   c=subprocess.Popen(args,cwd=W,env=E,stdout=f,stderr=subprocess.STDOUT);priority=os.getpriority(os.PRIO_PROCESS,c.pid);assert priority==10;code=c.wait()
  rows.append(dict(name=name,command=args,exitCode=code,niceness=priority,requiredPass=required));print(name+' exit '+str(code),flush=True)
  if code:print((B/(name+'.log')).read_text()[-5000:],flush=True)
  if code and required:break
 (B/'checks.json').write_text(json.dumps(dict(rows=rows,requiredChecksPassed=len(rows)==len(steps)and all(x['exitCode']==0 for x in rows if x['requiredPass']),wholeHostSuitePassed=any(x['name']=='host-full-library'and x['exitCode']==0 for x in rows),TMPDIR=str(T),TMPDIRMode='0700',ordinaryLaneOwned=True,qualification=False),indent=2)+'\n')
finally:
 if owned:lock.rmdir()
