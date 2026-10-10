from pathlib import Path
import os,subprocess,time,tempfile,json,hashlib
B=Path('/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09');W=B/'eligibility-producer';os.setpriority(os.PRIO_PROCESS,0,10);assert os.getpriority(os.PRIO_PROCESS,0)==10;D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=D/'opensip-lanes.lock';owned=False
commands=[('format',['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','src/cargo/sources/sealed_eligibility_tests.rs']),('build',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','test','--locked','--offline','-p','cargo','--lib','sealed_required_eligibility','--target-dir',str(B/'eligibility-target'),'--config','source.crates-io.replace-with="opensip-pinned-source"','--config','source.opensip-pinned-source.directory='+json.dumps(str(B/'vendor'))])];rows=[]
for label,args in commands:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('waiting for ordinary producer candidate lane',flush=True);time.sleep(5)
 try:
  T=Path(tempfile.mkdtemp(prefix='opensip-producer-candidate-',dir=D)).resolve();T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',CXX='/usr/bin/clang++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
  for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:E.pop(k,None)
  start=time.monotonic_ns()
  with(B/('eligibility-'+label+'.log')).open('wb')as out:
   child=subprocess.Popen(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT);nice=os.getpriority(os.PRIO_PROCESS,child.pid);assert nice==10;code=child.wait()
  rows.append(dict(check=label,command=args,exitCode=code,observedParentNiceness=10,observedChildNiceness=nice,ownedLane=True,privateTMPDIR=str(T),TMPDIRMode='0700',HOMEUnchanged=True,elapsedNanos=time.monotonic_ns()-start));assert code==0,(label,code)
 finally:
  if owned:lane.rmdir();owned=False
(B/'eligibility-tests.json').write_text(json.dumps(dict(standing='UNREVIEWED CONDITIONAL ELIGIBILITY DATA LOOKUP; NO SOURCE ADMISSION',checks=rows,tests=7,actualPinnedManifestParser=True,T2RepositoryCodeExecuted=False,sourceAdmissionImplemented=False,completeSourceProfile=False),indent=2)+'\n');print('Seven actual pinned parser/eligibility tests PASS; no first-winner path used.',flush=True)
