import pathlib,subprocess,os,tempfile,time,json
b=pathlib.Path('/tmp/opensip-implementation/f9-authoring');c=b/'product'
root=pathlib.Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip());lock=root/'opensip-lanes.lock'
e=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(b/'target'),RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/cc',AR='/usr/bin/ar',RANLIB='/usr/bin/ranlib',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip())
e['TMPDIR']=tempfile.mkdtemp(prefix='opensip-f9-',dir=root);os.chmod(e['TMPDIR'],0o700)
for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:e.pop(k,None)
e.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
while True:
 try:lock.mkdir();break
 except FileExistsError:time.sleep(5)
try:
 ca='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'
 for name,args in [
 ('unit-tests',[ca,'test','--locked','--offline','-p','opensip-security','--lib']),
 ('native-scenario-test',[ca,'test','--locked','--offline','-p','opensip-security','--lib','--features','scenario-fixtures','scenario::tests']),
 ('fixture-gate-tests',[ca,'test','--locked','--offline','-p','opensip-security','--lib','--features','scenario-fixtures,crash-matrix','crash_matrix_sites::']),
 ('feature-clippy',[ca,'clippy','--locked','--offline','-p','opensip-security','--lib','--features','scenario-fixtures,crash-matrix','--','-D','warnings'])]:
  with (b/(name+'.log')).open('w') as f:r=subprocess.run(['/usr/bin/nice','-n','10',*args],cwd=c,env=e,stdout=f,stderr=subprocess.STDOUT)
  print(name,r.returncode,flush=True)
  if r.returncode:break
finally:lock.rmdir()
assert r.returncode == 0
(b/'checks.json').write_text(json.dumps(dict(passed=True,newTests=5,privateTmpdir=e['TMPDIR'],inventoryUnchanged=166,qualification=False),indent=2)+'\n')
