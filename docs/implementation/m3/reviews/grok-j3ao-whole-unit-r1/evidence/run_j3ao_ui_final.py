from pathlib import Path
import os,subprocess,json,tempfile,time,importlib.util
B=Path('/tmp/opensip-implementation/j3ao-authoring-r1');P=B/'product';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=root/'opensip-lanes.lock';owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 private=Path(tempfile.mkdtemp(prefix='opensip-j3ao-controls-',dir=root));private.chmod(0o700)
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),CC='/usr/bin/clang',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip(),CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/clang',CARGO_TARGET_X86_64_APPLE_DARWIN_LINKER='/usr/bin/clang')
 for crate,files in [('operability',['src/scope.rs','src/lib.rs','tests/refusal_tests.rs']),('host',['src/request.rs','src/outcomes.rs'])]:
  for file in files:
   r=subprocess.run(['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024',file],cwd=P/'crates'/crate,env=env,capture_output=True);assert r.returncode==0,r.stderr
 spec=importlib.util.spec_from_file_location('checker',P/'tools/check_operability.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);(P/'tools/operability/exceptions.json').write_text(json.dumps(mod.proposed_rows(P),indent=2)+'\n')
 checks=[]
 for name,args in [('checker-tests',['tools/tests/test_check_operability.py']),('source',['tools/check_operability.py','source','--repository',str(P)]),('lock',['tools/check_operability.py','lock','--repository',str(P)])]:
  r=subprocess.run(['/usr/bin/nice','-n','10',PY,'-I','-B',*args],cwd=P,env=env,capture_output=True);(B/('r3-'+name+'.log')).write_bytes(r.stdout+r.stderr);print(name,r.returncode,flush=True);assert r.returncode==0,(r.stdout+r.stderr).decode();checks.append({'name':name,'passed':True})
 commands=[('plain-refusals',['test','-p','opensip-operability','--test','refusal_tests']),('default-clippy',['clippy','-p','opensip-operability','--all-targets','--','-D','warnings'])]
 for name,args in commands:
  cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo',args[0],'--locked','--offline',*args[1:]];r=subprocess.run(cmd,cwd=P,env=env,capture_output=True);(B/('r3-'+name+'.log')).write_bytes(r.stdout+r.stderr);print(name,r.returncode,flush=True);assert r.returncode==0,(r.stdout+r.stderr).decode()[-6000:];checks.append({'name':name,'passed':True,'command':cmd})
 (B/'controls-ui-final.json').write_text(json.dumps({'checks':checks,'passed':True,'productQualification':False,'integrated':False},indent=2)+'\n')
finally:
 if owned:lane.rmdir()
