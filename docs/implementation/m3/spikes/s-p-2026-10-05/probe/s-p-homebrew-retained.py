import datetime,json,os,pathlib,subprocess,tempfile,time
p=pathlib.Path('/tmp/opensip-implementation/s-p-acquisition');v=json.loads((p/'exclusive-probe-results.json').read_text());rust=pathlib.Path(v['rustSysroot']);darwin=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip();lock=pathlib.Path(darwin)/'opensip-lanes.lock';created=False
while not created:
 try:lock.mkdir();created=True
 except FileExistsError:print('Waiting for an available lane.',flush=True);time.sleep(15)
try:
 processes=subprocess.check_output(['/bin/ps','-Ao','pid=,comm='],text=True);active=[s.strip() for s in processes.splitlines() if s.split() and pathlib.Path(s.split()[-1]).name=='cargo'];assert not active
 started=datetime.datetime.now(datetime.UTC).isoformat();out=pathlib.Path(tempfile.mkdtemp(prefix='opensip-sp-homebrew-',dir=darwin));os.chmod(out,0o700)
 env=dict(os.environ);env.update(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(out),DYLD_LIBRARY_PATH=str(rust/'lib')+':'+str(rust/'lib/rustlib/aarch64-apple-darwin/lib'));env.pop('RUSTC_BOOTSTRAP',None)
 binary=out/'callbacks';command=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','--sysroot',str(rust),'-C','prefer-dynamic','-C','rpath','-C','linker=/usr/bin/cc',str(p/'verified-probe-source/callbacks.rs'),'-o',str(binary)]
 built=subprocess.run(command,cwd=out,env=dict(env,SDKROOT=v['sdkRoot'],RUSTC_BOOTSTRAP='1'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(out/'build.log').write_text(built.stdout);result={'standing':'PRELIMINARY MATCHING RETAINED COMPONENT SUBPROBE','directory':str(out),'buildCommand':command,'buildExitCode':built.returncode,'buildOutput':built.stdout,'lane':{'path':str(lock),'ownedByThisProcess':True,'startedAt':started,'otherBuildsBeforeStart':active},'bootstrapForWrapperCompileOnly':True,'runtimeCompilerIsRetainedOfficialDriver':True,'noProductionPinChange':True}
 if built.returncode==0:
  runtime=[str(binary),'--crate-type','lib','--edition','2024','--sysroot',str(rust),'--emit','metadata',v['inputFiles'][0]['path'],'--out-dir',str(out)]
  run=subprocess.run(['/usr/bin/nice','-n','10',*runtime],cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(out/'run.log').write_text(run.stdout);result.update(runCommand=runtime,runExitCode=run.returncode,runOutput=run.stdout,callbackPassed=run.returncode==0 and 'after_analysis' in run.stdout)
 else:result['callbackPassed']=False
 result['lane']['completedAt']=datetime.datetime.now(datetime.UTC).isoformat();(p/'homebrew-retained-probe.json').write_text(json.dumps(result,indent=2)+'\n');assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists();print(json.dumps(result,indent=2))
finally:
 if created:lock.rmdir()
