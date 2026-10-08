from pathlib import Path
import os,json,subprocess,tempfile,time
B=Path('/tmp/opensip-implementation/o1b-authoring-r1');P=B/'product';root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=root/'opensip-lanes.lock';owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 private=Path(tempfile.mkdtemp(prefix='opensip-o1b-release-',dir=root));private.chmod(0o700)
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),CC='/usr/bin/clang',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip(),CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/clang',CARGO_TARGET_X86_64_APPLE_DARWIN_LINKER='/usr/bin/clang')
 checks=[]
 def run(name,args,refuse=False):
  cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo',args[0],'--locked','--offline',*args[1:]]
  r=subprocess.run(cmd,cwd=P,env=env,capture_output=True);(B/(name+'.stdout')).write_bytes(r.stdout);(B/(name+'.stderr')).write_bytes(r.stderr);print(name,r.returncode,flush=True)
  if refuse:assert r.returncode!=0 and b'the harness-instrumentation feature requires debug assertions' in r.stderr,r.stderr.decode()[-3500:]
  else:assert r.returncode==0,r.stderr.decode()[-3500:]
  checks.append({'name':name,'passed':True,'refusal':refuse});return r
 run('harness-release-refusal',['check','--release','-p','opensip-operability','--features','harness-instrumentation'],True)
 run('featureless-release-build',['build','--release','-p','opensip-cli'])
 r=subprocess.run(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B','tools/check_operability.py','release-absence','--binary','target/release/opensip'],cwd=P,env=env,capture_output=True);(B/'release-absence.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stdout;checks.append({'name':'featureless-release-absence','passed':True})
 # An inherited writable stream remains untouched by a featureless binary.
 stream=private/'featureless.stream';out=private/'featureless.stdout';err=private/'featureless.stderr'
 with stream.open('wb') as channel,out.open('wb') as stdout,err.open('wb') as stderr:
  inherited=os.dup(channel.fileno())
  exe=str(P/'target/release/opensip');pid=os.posix_spawn(exe,[exe,'version','--format','json'],env,file_actions=[(os.POSIX_SPAWN_DUP2,stdout.fileno(),1),(os.POSIX_SPAWN_DUP2,stderr.fileno(),2),(os.POSIX_SPAWN_DUP2,inherited,3)]);_,status=os.waitpid(pid,0);os.close(inherited)
 assert os.waitstatus_to_exitcode(status)==0 and stream.stat().st_size==0 and err.stat().st_size==0
 body=json.loads(out.read_bytes());expected=json.loads((B/'version-regular.stdout').read_bytes());body.pop('requestId');expected.pop('requestId');assert body==expected,(body,expected)
 checks.append({'name':'featureless-descriptor-result-invariance','passed':True});(B/'featureless-release.stdout').write_bytes(out.read_bytes())
 r=run('harness-profile-build',['build','--profile','harness','-p','opensip-cli','--features','harness-instrumentation','--message-format','json'])
 profiles=[]
 for line in r.stdout.splitlines():
  try:x=json.loads(line)
  except ValueError:continue
  if x.get('reason')=='compiler-artifact' and x['target']['name']=='opensip':profiles.append(x['profile'])
 assert len(profiles)==1 and profiles[0]['debug_assertions'] is True and profiles[0]['overflow_checks'] is False and profiles[0]['opt_level']=='3',profiles
 checks.append({'name':'actual-optimized-harness-profile','passed':True,'profile':profiles[0]})
 (B/'release-controls.json').write_text(json.dumps({'standing':'Unreviewed build/refusal/absence/profile owning controls; no product/M6 qualification','passed':True,'checks':checks,'productQualification':False,'inventoryAuthored':False},indent=2)+'\n')
finally:
 if owned:lane.rmdir()
