import datetime,json,os,pathlib,subprocess,tempfile,time
base=pathlib.Path('/tmp/opensip-implementation/jbs-product-authoring');root=base/'product'
darwin=pathlib.Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip());lock=darwin/'opensip-lanes.lock'
env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',RUSTFLAGS='-C linker=/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip(),CC='/usr/bin/cc',AR='/usr/bin/ar',RANLIB='/usr/bin/ranlib')
for key in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE','RUSTC_BOOTSTRAP'):env.pop(key,None)
env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
rows=[]
for label,command in [('contracts-tests',['cargo','test','--locked','--offline','-p','opensip-contracts','--lib']),('contracts-clippy',['cargo','clippy','--locked','--offline','-p','opensip-contracts','--lib','--','-D','warnings']),('workspace-check',['cargo','check','--locked','--offline','--workspace'])]:
 owned=False
 while not owned:
  try:lock.mkdir();owned=True
  except FileExistsError:print('Waiting for the build lane.',flush=True);time.sleep(15)
 try:
  active=[line for line in subprocess.check_output(['/bin/ps','-Ao','pid=,comm='],text=True).splitlines() if line.split() and pathlib.Path(line.split()[-1]).name=='cargo'];assert not active,active
  scratch=pathlib.Path(tempfile.mkdtemp(prefix='opensip-jbs-check-',dir=darwin));scratch.chmod(0o700);env['TMPDIR']=str(scratch)
  with (base/(label+'.log')).open('w') as log:result=subprocess.run(['/usr/bin/nice','-n','10',*command],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
  rows.append({'label':label,'command':command,'exitCode':result.returncode,'laneOwned':True,'nice':10,'privateTmpdir':str(scratch)});print(json.dumps(rows[-1]),flush=True)
  assert result.returncode==0,label
 finally:
  if owned:lock.rmdir()
assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
(base/'build-checks.json').write_text(json.dumps({'passed':True,'commands':rows,'completedAt':datetime.datetime.now(datetime.UTC).isoformat(),'productQualification':False},indent=2)+'\n')
