from pathlib import Path
import os,subprocess,json,tempfile,time,hashlib
B=Path('/tmp/opensip-implementation/j3ao-authoring-r1');P=B/'product';root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=root/'opensip-lanes.lock';owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 private=Path(tempfile.mkdtemp(prefix='opensip-j3ao-release-',dir=root));private.chmod(0o700)
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),CC='/usr/bin/clang',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip(),CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/clang',CARGO_TARGET_X86_64_APPLE_DARWIN_LINKER='/usr/bin/clang')
 cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','build','--locked','--offline','--release','-p','opensip-cli','--bin','opensip'];r=subprocess.run(cmd,cwd=P,env=env,capture_output=True);(B/'release-build.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr.decode()[-4000:]
finally:
 if owned:lane.rmdir()
binary=P/'target/release/opensip';raw=binary.read_bytes();assert b'opensip.operability.dev-sink' not in raw and b'opensip.operability.harness-sink' not in raw
r=subprocess.run(['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B','tools/check_operability.py','release-absence','--binary',str(binary)],cwd=P,capture_output=True);(B/'release-absence.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
old=Path('/tmp/opensip-implementation/o1a-whole-unit-candidate-r1/product/target/release/opensip');assert old.is_file()
def normalized(value):
 if isinstance(value,dict):return {k:('<request>'if k=='requestId' else normalized(v))for k,v in value.items()}
 if isinstance(value,list):return [normalized(v)for v in value]
 return value
rows=[]
for name,args in [('help',['help','--format','json']),('version',['version','--format','json']),('reject',['j3ao-unknown-command','--format','json'])]:
 results=[]
 for which,exe in [('accepted-o1a',old),('j3ao',binary)]:
  result=subprocess.run(['/usr/bin/nice','-n','10',str(exe),*args],env=env,capture_output=True,timeout=10);(B/(name+'-'+which+'.stdout')).write_bytes(result.stdout);(B/(name+'-'+which+'.stderr')).write_bytes(result.stderr);results.append((result.returncode,normalized(json.loads(result.stdout)),result.stderr))
 assert results[0]==results[1],(name,results);assert results[1][2]==b'';rows.append({'case':name,'passed':True,'normalization':'fresh requestId only','realInstallationRead':False})
(B/'release-controls.json').write_text(json.dumps({'passed':True,'featurelessSinkMarkersAbsent':True,'binary':{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'metadataInvariance':rows,'private413Read':False,'realInstallationRead':False,'productQualification':False},indent=2)+'\n');print('release absence and3 metadata comparisons passed')
