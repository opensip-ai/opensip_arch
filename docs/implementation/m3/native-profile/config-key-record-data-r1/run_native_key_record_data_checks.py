from pathlib import Path
import os,subprocess,json,tempfile,time,hashlib
W=Path('/Users/sb/code/opensip-ai/opensip-native-config-key-record-data');R=Path('/tmp/opensip-implementation/native-key-record-data-checks-2026-10-10-r2');assert not R.exists();R.mkdir();D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());L=D/'opensip-lanes.lock';T=Path(tempfile.mkdtemp(prefix='opensip-key-data-',dir=D));T.chmod(0o700);E=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T),RUSTFLAGS='-C linker=/usr/bin/cc',CC='/usr/bin/clang',CXX='/usr/bin/clang++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path']).decode().strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:E.pop(k,None)
owned=False
while not owned:
 try:L.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 results=[]
 for rel in ['src/native_config_key_record_data.rs','src/native_config_key_record_data_tests.rs']:
  cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','--config','skip_children=true',rel];run=subprocess.run(cmd,cwd=W/'crates/host',env=E,capture_output=True);(R/(Path(rel).stem+'-format.log')).write_bytes(run.stdout+run.stderr);assert run.returncode==0;results.append(dict(command=cmd,exitCode=0))
 fmt=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','--config','skip_children=true','--check','src/lib.rs'];f=subprocess.run(fmt,cwd=W/'crates/host',env=E,capture_output=True);(R/'format-lib.log').write_bytes(f.stdout+f.stderr);assert f.returncode==0;results.append(dict(command=fmt,exitCode=0))
 for name,args in [('host-tests',['test','-p','opensip-host','--lib']),('host-clippy',['clippy','-p','opensip-host','--all-targets','--','-D','warnings'])]:
  cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo',*args];idx=cmd.index('--')if '--'in cmd else len(cmd);cmd[idx:idx]=['--locked','--offline'];run=subprocess.run(cmd,cwd=W,env=E,capture_output=True);(R/(name+'.log')).write_bytes(run.stdout+run.stderr);assert run.returncode==0,name;results.append(dict(command=cmd,exitCode=0))
 source_cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B','tools/check_operability.py','source','--repository',str(W)];audit=subprocess.run(source_cmd,cwd=W,env=E,capture_output=True);(R/'source-census.json').write_bytes(audit.stdout);assert audit.returncode==0 and json.loads(audit.stdout)==dict(findings=[],passed=True,rows=113)
 assert '300 passed; 0 failed' in (R/'host-tests.log').read_text()
 checks=dict(requiredChecksPassed=True,wholeHostSuitePassed=True,hostTestsExpected=300,newKeyRecordDataTests=11,allTargetsClippyWarningsDenied=True,commands=results,privateTmpdir=str(T),ownedLaneReleasedAfterSet=True,dataOnly=True,actualOwnedDiscovery=False,actualKeyClassification=False,publicFailureRoutesSelected=False,productQualification=False,entirePlanComplete=False);(R/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))
finally:
 if owned:L.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
