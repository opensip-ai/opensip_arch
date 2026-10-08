from pathlib import Path
import os,json,subprocess,tempfile,time,hashlib,select
B=Path('/tmp/opensip-implementation/o1b-authoring-r1');P=B/'product';root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());private=Path(tempfile.mkdtemp(prefix='opensip-o1b-descriptor-',dir=root));private.chmod(0o700)
artifacts={}
for line in (B/'stream-build.jsonl').read_bytes().splitlines():
 try:x=json.loads(line)
 except ValueError:continue
 if x.get('reason')=='compiler-artifact':artifacts[x['target']['name']]=x
exe=B/'stream-probe';args=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024','-C','linker=/usr/bin/clang',str(B/'stream_probe.rs'),'-L','dependency='+str(P/'target/debug/deps'),'-o',str(exe)]
for name in ['opensip_host','opensip_operability','opensip_platform']:
 rlib=[x for x in artifacts[name]['filenames'] if x.endswith('.rlib')];assert len(rlib)==1
 args+=['--extern',name+'='+rlib[0]]
env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',TMPDIR=str(private),SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip());r=subprocess.run(args,cwd=P,env=env,capture_output=True);(B/'descriptor-probe-compile.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr.decode()
rows=[]
def invoke(mode,kind):
 out=private/(mode+'.stdout');err=private/(mode+'.stderr');stream=private/(mode+'.stream');reader=None;source=None
 with out.open('wb') as output,err.open('wb') as error:
  actions=[(os.POSIX_SPAWN_DUP2,output.fileno(),1),(os.POSIX_SPAWN_DUP2,error.fileno(),2)]
  if kind=='regular':source=os.open(stream,os.O_RDWR|os.O_CREAT|os.O_TRUNC,0o600)
  else:
   reader,source=os.pipe()
   if mode=='closed-reader':os.close(reader);reader=None
  preload=0
  if mode in ['stall','cancel-stall']:
   os.set_blocking(source,False)
   while True:
    try:preload+=os.write(source,b'x'*4096)
    except BlockingIOError:break
   os.set_blocking(source,True)
  actions.append((os.POSIX_SPAWN_DUP2,source,3));before=time.monotonic_ns();pid=os.posix_spawn(str(exe),[str(exe),mode],env,file_actions=actions);os.close(source)
  deadline=time.monotonic()+10
  while True:
   done,status=os.waitpid(pid,os.WNOHANG)
   if done:break
   assert time.monotonic()<deadline,('probe did not return',mode,pid)
   time.sleep(.01)
  duration=time.monotonic_ns()-before
 if reader is not None:
  data=b''
  while True:
   chunk=os.read(reader,65536)
   if not chunk:break
   data+=chunk
  os.close(reader)
 else:data=stream.read_bytes() if stream.exists() else b''
 stdout=out.read_bytes();stderr=err.read_bytes();assert os.waitstatus_to_exitcode(status)==0,(mode,status,stdout,stderr)
 result=json.loads(stdout);assert result['admitted']
 if mode=='cancel-stall':assert result['cancelled'] is True
 else:assert result['response']['kind']=='meta'
 if mode=='inheritance':assert not result['hasError'] and sum(result['abandoned'])==0
 elif mode=='closed-reader':assert result['hasError'] and sum(result['failed'])>=1
 elif mode in ['stall','cancel-stall']:assert sum(result['abandoned'])>=1 and not result['hasError']
 # Strict finalization deadline qualification belongs to M6. Preserve actual elapsed
 # logging+metadata preparation and whole-process durations without adding tolerance.
 (B/(mode+'-probe.stream')).write_bytes(data);(B/(mode+'-probe.stdout')).write_bytes(stdout);(B/(mode+'-probe.stderr')).write_bytes(stderr)
 row={'name':mode,'passed':True,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'wholeProcessNanoseconds':duration,'driverPreloadBytes':preload,'result':result};rows.append(row)
 return data
normal=invoke('inheritance','regular');invoke('closed-reader','pipe');invoke('stall','pipe');invoke('cancel-stall','pipe')
for ceiling in ['P0','P1']:
 raw=B/'inheritance-probe.stream';r=subprocess.run([str(exe),'reader',str(raw),ceiling],env=env,capture_output=True);assert r.returncode==0,r.stderr
 lines=[json.loads(x) for x in r.stdout.splitlines()];assert len(lines)==6,lines
 opened=lines[0];assert opened['event']=='log.stream.opened';assert ('pid' in opened['fields'])==(ceiling=='P1')
 (B/('reader-'+ceiling+'.jsonl')).write_bytes(r.stdout);(B/('reader-'+ceiling+'.stderr')).write_bytes(r.stderr);rows.append({'name':'actual-reader-'+ceiling,'passed':True,'lines':len(lines)})
# The driver retains exact raw bytes; torn last-line bytes remain in the digest
# even when the reader drops them. This is a C13 digest primitive, not a Q0
# envelope acceptance claim; the envelope's owner decision is still pending.
torn=B/'driver-torn.stream';torn.write_bytes(normal+b'{"torn":');r=subprocess.run([str(exe),'reader',str(torn),'P1'],env=env,capture_output=True);assert r.returncode==0 and len(r.stdout.splitlines())==6
assert hashlib.sha256(torn.read_bytes()).hexdigest()!=hashlib.sha256(normal).hexdigest();rows.append({'name':'exact-byte-torn-digest','passed':True,'bytes':torn.stat().st_size,'sha256':hashlib.sha256(torn.read_bytes()).hexdigest(),'readerDrops':r.stderr.decode().strip(),'Q0EnvelopeAccepted':False})
(B/'descriptor-controls.json').write_text(json.dumps({'standing':'Unreviewed actual descriptor failure/stall/child noninheritance/reader/digest primitive controls; no strict M6 qualification or Q0 envelope acceptance','passed':True,'checks':rows,'productQualification':False,'inventoryAuthored':False},indent=2)+'\n');print('descriptor controls passed',len(rows),flush=True)
