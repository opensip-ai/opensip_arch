from pathlib import Path
import os,subprocess,time,tempfile,json
B=Path('/tmp/opensip-implementation/native-config-pipeline-data-2026-10-10');W=B/'producer';V=Path('/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09/vendor');os.setpriority(os.PRIO_PROCESS,0,10);D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=D/'opensip-lanes.lock';owned=False
commands=[('format-module',['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','--config','skip_children=true','src/cargo/util/context/mod.rs']),('format-data',['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','--config','skip_children=true','src/cargo/util/context/config_pipeline_data.rs']),('pipeline-tests',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','cargo','--lib','config_pipeline_data','--target-dir',str(B/'target'),'--config','source.crates-io.replace-with="opensip-pinned-source"','--config','source.opensip-pinned-source.directory='+json.dumps(str(V))]),('whole-producer',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','build','--locked','--offline','-p','cargo','--bin','cargo','--target-dir',str(B/'target'),'--config','source.crates-io.replace-with="opensip-pinned-source"','--config','source.opensip-pinned-source.directory='+json.dumps(str(V))])];rows=[]
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:print('Waiting for ordinary producer lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-config-pipeline-',dir=D)).resolve();T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',CXX='/usr/bin/clang++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:E.pop(k,None)
 for label,args in commands:
  print(label+' starting',flush=True);start=time.monotonic_ns()
  with(B/(label+'.log')).open('wb')as out:
   child=subprocess.Popen(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT);nice=os.getpriority(os.PRIO_PROCESS,child.pid);assert nice==10;code=child.wait()
  rows.append(dict(check=label,command=args,exitCode=code,observedParentNiceness=10,observedDirectChildNiceness=nice,ownedLane=True,privateTMPDIR=str(T),TMPDIRMode='0700',HOMEUnchanged=True,elapsedNanos=time.monotonic_ns()-start));print(label+' exit '+str(code),flush=True)
  if code:print((B/(label+'.log')).read_text()[-6000:],flush=True);break
 (B/'checks.json').write_text(json.dumps(dict(checks=rows,expectedControls=6,requiredChecksPassed=len(rows)==4 and all(r['exitCode']==0 for r in rows),sourceAdmissionImplemented=False,configurationInputAdmitted=False,originalDefinitionsAdmitted=False,completeProjectionImplemented=False,includeCompatibilitySelected=False,sourceProfilePublished=False,productQualification=False,T2RepositoryCodeExecuted=False),indent=2)+'\n')
finally:
 if owned:lane.rmdir()
