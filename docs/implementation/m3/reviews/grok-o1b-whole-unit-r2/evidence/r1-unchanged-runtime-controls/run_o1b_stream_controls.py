from pathlib import Path
import os,json,subprocess,tempfile,time,hashlib
B=Path('/tmp/opensip-implementation/o1b-authoring-r1');P=B/'product';root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=root/'opensip-lanes.lock';owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:time.sleep(5)
try:
 private=Path(tempfile.mkdtemp(prefix='opensip-o1b-stream-',dir=root));private.chmod(0o700)
 env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(private),CC='/usr/bin/clang',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip(),CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/clang',CARGO_TARGET_X86_64_APPLE_DARWIN_LINKER='/usr/bin/clang')
 args=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','build','--locked','--offline','-p','opensip-cli','--features','harness-instrumentation','--message-format','json']
 r=subprocess.run(args,cwd=P,env=env,capture_output=True);(B/'stream-build.jsonl').write_bytes(r.stdout);(B/'stream-build.stderr').write_bytes(r.stderr);assert r.returncode==0,r.stderr.decode()[-4000:]
 artifacts={}
 for line in r.stdout.splitlines():
  try:x=json.loads(line)
  except ValueError:continue
  if x.get('reason')=='compiler-artifact':artifacts[x['target']['name']]=x
 exe=artifacts['opensip']['executable'];rows=[]
 def invoke(name,kind,argv):
  out=private/(name+'.stdout');err=private/(name+'.stderr');stream=private/(name+'.stream')
  with out.open('wb') as output,err.open('wb') as error:
   actions=[(os.POSIX_SPAWN_DUP2,output.fileno(),1),(os.POSIX_SPAWN_DUP2,error.fileno(),2)]
   source=None
   if kind=='regular':source=os.open(stream,os.O_RDWR|os.O_CREAT|os.O_TRUNC,0o600)
   elif kind=='readonly':stream.write_bytes(b'');source=os.open(stream,os.O_RDONLY)
   elif kind=='directory':source=os.open(private,os.O_RDONLY)
   if source is None:actions.append((os.POSIX_SPAWN_CLOSE,3))
   else:actions.append((os.POSIX_SPAWN_DUP2,source,3))
   pid=os.posix_spawn(exe,[exe,*argv],env,file_actions=actions);_,status=os.waitpid(pid,0)
   if source is not None:os.close(source)
  stdout=out.read_bytes();stderr=err.read_bytes();data=stream.read_bytes() if stream.exists() else b''
  assert os.waitstatus_to_exitcode(status)==0,(name,stdout,stderr)
  response=json.loads(stdout);assert response['kind']=='meta'
  records=[json.loads(line) for line in data.splitlines()]
  if kind=='regular':
   assert records[0]['event']=='log.stream.opened' and records[0]['fields']['sink']=='harness',records
   req=response['requestId'];assert all(x['requestId']==req for x in records)
   assert not stderr,stderr
   starts={x['fields']['phase']:x for x in records if x['event']=='host.phase.started'}
   ends={x['fields']['phase']:x for x in records if x['event']=='host.phase.completed'}
   assert set(starts)==set(ends)=={'request','delivery'},records
   assert starts['request']['fields']['at']==0 and 'parent' not in starts['request']['fields']
   assert starts['delivery']['fields']['parent']=='request'
   for phase in starts:
    a=starts[phase]['fields']['at'];z=ends[phase]['fields']['at'];assert z>=a and ends[phase]['fields']['wall']==z-a
    assert ends[phase]['fields']['cpu']>=0 and ends[phase]['fields']['outcome']=='completed'
   assert ends['request']['fields']['at']>=ends['delivery']['fields']['at']>=starts['delivery']['fields']['at']
   assert records[-1]['event']=='log.loss.counted' and records[-1]['fields']['sink']=='harness',records
  else:assert not data,(name,data)
  normalized=dict(response);normalized.pop('requestId');rows.append({'name':name,'descriptor':kind,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'recordCount':len(records),'passed':True})
  (B/(name+'.stream')).write_bytes(data);(B/(name+'.stdout')).write_bytes(stdout);(B/(name+'.stderr')).write_bytes(stderr)
  return normalized
 for command in ['version','help']:
  expected=invoke(command+'-regular','regular',[command,'--format','json'])
  for kind in ['closed','readonly','directory']:assert invoke(command+'-'+kind,kind,[command,'--format','json'])==expected
 (B/'stream-controls.json').write_text(json.dumps({'standing':'Unreviewed owning first-record/admission/metadata/phase controls; FIFO/error/inheritance/reader/digest envelope/release controls remain','passed':True,'checks':rows,'productQualification':False,'inventoryAuthored':False},indent=2)+'\n');print('stream controls passed',len(rows),flush=True)
finally:
 if owned:lane.rmdir()
