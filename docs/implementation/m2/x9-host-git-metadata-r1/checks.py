import datetime,json,os,pathlib,subprocess,tempfile,time
root=pathlib.Path('/Users/sb/code/opensip-ai/opensip-x9-metadata');evidence=pathlib.Path('/tmp/opensip-implementation/x9-metadata-authoring')
darwin=pathlib.Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip());lock=darwin/'opensip-lanes.lock';owned=False
while not owned:
 try:lock.mkdir();owned=True
 except FileExistsError:print('Waiting for the build lane.',flush=True);time.sleep(15)
try:
 active=[line for line in subprocess.check_output(['/bin/ps','-Ao','pid=,comm='],text=True).splitlines() if line.split() and pathlib.Path(line.split()[-1]).name=='cargo'];assert not active,active
 scratch=pathlib.Path(tempfile.mkdtemp(prefix='opensip-x9-metadata-',dir=darwin));scratch.chmod(0o700)
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(scratch),RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/cc',AR='/usr/bin/ar',RANLIB='/usr/bin/ranlib',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for key in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE','RUSTC_BOOTSTRAP','OPENSIP_X9_RUN_SET','OPENSIP_X9_CENSUS_ONLY','OPENSIP_X9_ROWS']:env.pop(key,None)
 rows=[]
 def run(label,cmd,cwd):
  result=subprocess.run(['/usr/bin/nice','-n','10',*cmd],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(evidence/(label+'.log')).write_text(result.stdout);rows.append({'label':label,'command':cmd,'cwd':str(cwd),'exitCode':result.returncode});print(json.dumps(rows[-1]),flush=True);assert result.returncode==0,result.stdout
 for package,target in [('storage','commit_tests'),('host','commit_matrix_tests')]:
  run(package+'-format',['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','--config','skip_children=true','tests/'+target+'.rs'],root/'crates'/package)
  run(package+'-metadata-tests',['cargo','test','--locked','--offline','-p','opensip-'+package,'--features','crash-matrix','--test',target,'x9_metadata_','--','--test-threads=1'],root)
  run(package+'-clippy',['cargo','clippy','--locked','--offline','-p','opensip-'+package,'--features','crash-matrix','--test',target,'--','-D','warnings'],root)
 assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 (evidence/'checks.json').write_text(json.dumps({'standing':'X9 HOST-GIT METADATA FOLLOW-UP ONLY; NO CRASH MATRIX OR QUALIFICATION', 'commands':rows,'completedAt':datetime.datetime.now(datetime.UTC).isoformat(),'scratch':str(scratch),'laneOwned':True,'nice':10,'matrixRan':False,'private413Read':False,'installationAbsent':True,'PATH':env['PATH']},indent=2)+'\n')
finally:
 if owned:lock.rmdir()
