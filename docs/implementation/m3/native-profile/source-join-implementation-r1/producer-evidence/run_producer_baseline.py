from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib
B=Path('/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09');W=B/'compatible-producer';os.setpriority(os.PRIO_PROCESS,0,10);parent=os.getpriority(os.PRIO_PROCESS,0);assert parent==10;receipt=json.loads((B/'locked-vendor-receipt.json').read_text());assert len(receipt['packages'])==507;lock_before=(W/'Cargo.lock').read_bytes();assert hashlib.sha256(lock_before).hexdigest()==receipt['lockSha256']
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for ordinary producer build lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-producer-build-',dir=D)).resolve();T.chmod(0o700);env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',CXX='/usr/bin/clang++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null');
 for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(k,None)
 args=['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','build','--locked','--offline','-p','cargo','--bin','cargo','--target-dir',str(B/'baseline-target'),'--config','source.crates-io.replace-with="opensip-pinned-source"','--config','source.opensip-pinned-source.directory='+json.dumps(str(B/'vendor'))]
 start=time.monotonic_ns()
 with(B/'baseline-build.log').open('wb')as out:
  child=subprocess.Popen(args,cwd=W,env=env,stdout=out,stderr=subprocess.STDOUT);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;result=child.wait()
 report=dict(standing='UNREVIEWED OFFLINE UPSTREAM BASELINE BUILD; NOT COMPATIBLE SEALED PRODUCER OR SIGNED TOOL',command=args,observedParentNiceness=parent,observedChildNiceness=priority,exitCode=result,elapsedNanos=time.monotonic_ns()-start,privateTMPDIR=str(T),TMPDIRMode='0700',HOMEUnchanged=True,CARGO_HOME='/Users/sb/.cargo',laneOwned=True,upstreamCommit=receipt['upstreamCommit'],CargoLockUnchanged=(W/'Cargo.lock').read_bytes()==lock_before,lockedDependencySourceReceiptSha256=hashlib.sha256((B/'locked-vendor-receipt.json').read_bytes()).hexdigest(),buildDependencyScriptsExecuted=True,T2RepositoryCodeExecuted=False,compatibleProducerImplemented=False,sourceProfilePublished=False,sourceAdmissionImplemented=False,productQualification=False)
 exe=B/'baseline-target/debug/cargo'
 if result==0:
  raw=exe.read_bytes();report['runtimePin']=dict(path=str(exe),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 (B/'baseline-build.json').write_text(json.dumps(report,indent=2)+'\n');assert report['CargoLockUnchanged'];print(json.dumps(report,indent=2),flush=True)
 if result:print((B/'baseline-build.log').read_text()[-5000:],flush=True)
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
