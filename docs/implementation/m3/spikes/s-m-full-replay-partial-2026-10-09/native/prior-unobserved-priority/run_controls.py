from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib
B=Path(__file__).resolve().parent;D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for native replay control lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-native-replay-',dir=D)).resolve();T.chmod(0o700);pin=json.loads((B/'build.json').read_text());binary=Path(pin['executable']);raw=binary.read_bytes();assert len(raw)==pin['bytes']and hashlib.sha256(raw).hexdigest()==pin['sha256'];env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
 for k in ['HOME','LANG','LC_ALL','TZ']:
  if k in os.environ:env[k]=os.environ[k]
 results=[]
 for name in ['packet-3-selected']:
  out=B/(name+'.stdout');err=B/(name+'.stderr')
  with out.open('wb')as o,err.open('wb')as e:
   child=subprocess.Popen([str(binary),str(B/(name+'.json'))],cwd=T,env=env,stdout=o,stderr=e);_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
  row=dict(case=name,exitCode=child.returncode,stdout=str(out),stderr=str(err),rssNative=int(usage.ru_maxrss),rssUnit='bytes');results.append(row);(B/'controls.json').write_text(json.dumps(dict(standing='UNREVIEWED ACTUAL NATIVE REPLAY CONTROLS; NO QUALIFICATION',controls=results),indent=2)+'\n');print(name,child.returncode,flush=True)
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
