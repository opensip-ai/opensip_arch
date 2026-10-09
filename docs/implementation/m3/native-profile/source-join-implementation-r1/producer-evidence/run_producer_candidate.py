from pathlib import Path
import os,subprocess,time,tempfile,json,hashlib
B=Path('/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09');W=B/'compatible-producer';os.setpriority(os.PRIO_PROCESS,0,10);assert os.getpriority(os.PRIO_PROCESS,0)==10;D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=D/'opensip-lanes.lock';owned=False
commands=[('format',['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','src/cargo/core/sealed_source_comparison.rs']),('build',['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','build','--locked','--offline','-p','cargo','--bin','cargo','--target-dir',str(B/'candidate-target'),'--config','source.crates-io.replace-with="opensip-pinned-source"','--config','source.opensip-pinned-source.directory='+json.dumps(str(B/'vendor'))])];rows=[]
for label,args in commands:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('waiting for ordinary producer candidate lane',flush=True);time.sleep(5)
 try:
  T=Path(tempfile.mkdtemp(prefix='opensip-producer-candidate-',dir=D)).resolve();T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',CXX='/usr/bin/clang++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
  for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:E.pop(k,None)
  start=time.monotonic_ns()
  with(B/('candidate-'+label+'.log')).open('wb')as out:
   child=subprocess.Popen(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT);nice=os.getpriority(os.PRIO_PROCESS,child.pid);assert nice==10;code=child.wait()
  rows.append(dict(check=label,command=args,exitCode=code,observedParentNiceness=10,observedChildNiceness=nice,ownedLane=True,privateTMPDIR=str(T),TMPDIRMode='0700',HOMEUnchanged=True,elapsedNanos=time.monotonic_ns()-start));assert code==0,(label,code)
 finally:
  if owned:lane.rmdir();owned=False
original=Path(json.loads((B/'source-receipt.json').read_text())['originalRoot']);before=json.loads((B/'source-receipt.json').read_text());changed=[]
for f in before['files']:
 p=W/f['path'];raw=p.read_bytes();assert p.is_file()
 if hashlib.sha256(raw).hexdigest()!=f['sha256']:changed.append(f['path'])
assert changed==['src/cargo/core/mod.rs'];new='src/cargo/core/sealed_source_comparison.rs';exe=B/'candidate-target/debug/cargo';raw=exe.read_bytes();report=dict(standing='UNREVIEWED PRODUCER FORK SUPPORTING CSJ1 DATA KERNEL ONLY; SOURCELOADER/PROFILE NOT IMPLEMENTED',upstreamCommit=before['upstreamCommit'],checks=rows,changedUpstreamFiles=changed,newSourceFiles=[new],sourcePins=[dict(path=r,bytes=(W/r).stat().st_size,sha256=hashlib.sha256((W/r).read_bytes()).hexdigest())for r in changed+[new]],runtimePin=dict(path=str(exe),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),CargoLockUnchanged=(W/'Cargo.lock').read_bytes()==(original/'Cargo.lock').read_bytes(),originalBaselineImageUnchanged=hashlib.sha256(Path(json.loads((B/'baseline-build.json').read_text())['runtimePin']['path']).read_bytes()).hexdigest()==json.loads((B/'baseline-build.json').read_text())['runtimePin']['sha256'],sourceComparisonDataKernelImplemented=True,sourceAdmissionImplemented=False,compatibleProducerImplemented=False,sourceProfilePublished=False,productQualification=False);assert report['CargoLockUnchanged']and report['originalBaselineImageUnchanged'];(B/'candidate-build.json').write_text(json.dumps(report,indent=2)+'\n');print('Isolated Cargo fork compiles private CSJ1 kernel; only2authorized sourcepaths differ, baseline and lock unchanged.',flush=True)
