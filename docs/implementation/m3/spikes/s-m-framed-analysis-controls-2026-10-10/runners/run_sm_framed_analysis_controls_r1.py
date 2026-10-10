from pathlib import Path
import os,json,struct,hashlib,tempfile,subprocess,time,signal
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-framed-analysis-2026-10-10';O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');SYS=Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot');assert not (V/'controls-r1.json').exists();build=json.loads((V/'build.json').read_bytes());image=Path(build['executable']);root=Path(tempfile.mkdtemp(prefix='opensip-sm-framed-analysis-controls-',dir=O));root.chmod(0o700);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME')
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def map_bytes(rows):return b'OPSMRUST1\0'+struct.pack('>Q',len(rows))+b''.join(struct.pack('>Q',len(p.encode()))+p.encode()+struct.pack('>Q',len(c))+c for p,c in rows)
def framed(raw,corrupt=False):
 header=json.dumps(dict(format='OPSMRUST1',bytes=len(raw),sha256=('0'*64 if corrupt else hashlib.sha256(raw).hexdigest())),sort_keys=True,separators=(',',':')).encode();parts=[header]+[raw[i:i+7] for i in range(0,len(raw),7)];return b''.join(struct.pack('>I',len(p))+p for p in parts)
simple=map_bytes([('/synthetic/main.rs',b'pub fn f()->u8 { 1 }')]);canary=root/'outside-canary.bin';canary.write_bytes(b'firstparty canary outside the prepared source map')
quoted=map_bytes([('/synthetic/main"β.rs',b'pub static B: &[u8;4]=include_bytes!("payload.bin");'),('/synthetic/payload.bin',b'abcd')]);type_error=map_bytes([('/synthetic/main.rs',b'pub fn f()->u8 { "wrong" }')]);outside=map_bytes([('/synthetic/main.rs',('pub static B: &[u8]=include_bytes!('+json.dumps(str(canary))+');').encode())]);duplicate=map_bytes([('/synthetic/main.rs',b'pub fn f(){}'),('/synthetic/other.rs',b''),('/synthetic/main.rs',b'pub fn g(){}')]);row_bound=b'OPSMRUST1\0'+struct.pack('>Q',100001);content_bound=b'OPSMRUST1\0'+struct.pack('>Q',1)+struct.pack('>Q',1)+b'/'+struct.pack('>Q',(8<<30)+1)
bad_header=json.dumps(dict(format='OPSMRUST1',bytes=-1,sha256='0'*64),sort_keys=True,separators=(',',':')).encode();descriptor_bound=map_bytes([('/'+('x'*(4<<20)),b'')]);descriptor_header=json.dumps(dict(format='OPSMRUST1',bytes=len(descriptor_bound),sha256=hashlib.sha256(descriptor_bound).hexdigest()),sort_keys=True,separators=(',',':')).encode();descriptor_wire=struct.pack('>I',len(descriptor_header))+descriptor_header+b''.join(struct.pack('>I',len(p))+p for p in [descriptor_bound[i:i+(1<<20)] for i in range(0,len(descriptor_bound),1<<20)])
cases=[('simple-library',simple,framed(simple),'/synthetic/main.rs',True,True),('quoted-unicode-binary',quoted,framed(quoted),'/synthetic/main"β.rs',True,True),('real-type-error',type_error,framed(type_error),'/synthetic/main.rs',False,True),('disk-canary-outside-map',outside,framed(outside),'/synthetic/main.rs',False,True),('whole-pin-corruption',simple,framed(simple,True),'/synthetic/main.rs',False,False),('nonadjacent-duplicate',duplicate,framed(duplicate),'/synthetic/main.rs',False,False),('oversize-frame',None,struct.pack('>I',(1<<20)+1),'/synthetic/main.rs',False,False),('truncated-frame',None,struct.pack('>I',7)+b'{}','/synthetic/main.rs',False,False),('trailing-input',simple,framed(simple)+b'x','/synthetic/main.rs',False,False),('negative-header-bytes',None,struct.pack('>I',len(bad_header))+bad_header,'/synthetic/main.rs',False,False),('row-bound',row_bound,framed(row_bound),'/synthetic/main.rs',False,False),('content-bound',content_bound,framed(content_bound),'/synthetic/main.rs',False,False),('descriptor-bound',descriptor_bound,descriptor_wire,'/synthetic/main.rs',False,False)]
records=[]
def reap(child):
 while True:
  try:pid,status,usage=os.wait4(child.pid,0);assert pid==child.pid;child.returncode=os.waitstatus_to_exitcode(status);return usage
  except InterruptedError:continue
try:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('Waiting for ordinary framed analysis control lane',flush=True);time.sleep(5)
 for index,(name,raw,wire,input_path,success,compiler_expected) in enumerate(cases):
  assert pin(image)['sha256']==build['sha256'];r=root/name;r.mkdir(mode=0o700);out=r/'libcontrol.rmeta';(r/'input.frames').write_bytes(wire)
  if raw is not None:(r/'source.map').write_bytes(raw)
  argv=[str(image),'--prepared-map-framed-stdin','--crate-type','lib','--crate-name','control','--edition','2024','--sysroot',str(SYS),'--emit','metadata',input_path,'-o',str(out),'-C',f'metadata=framed_control_{index}'];err=(r/'stderr.log').open('xb');started=time.monotonic_ns();child=subprocess.Popen(argv,cwd=root,env={'TMPDIR':str(root)},stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,bufsize=0);reaped=False
  try:
   ready=child.stdout.readline();ready_elapsed=time.monotonic_ns()-started;assert json.loads(ready)==dict(event='transfer_ready');view=memoryview(wire)
   while view:
    n=child.stdin.write(view);assert n is not None and n>0;view=view[n:]
   child.stdin.close();stdout=ready+child.stdout.read();usage=reap(child);reaped=True;elapsed=time.monotonic_ns()-started;(r/'stdout.log').write_bytes(stdout);events=[json.loads(line) for line in stdout.splitlines()];compiled=any(e['event']=='analysis_span_started' for e in events);completed=[e for e in events if e['event']=='after_analysis'];assert compiled==compiler_expected and (child.returncode==0)==success and bool(completed)==success and out.is_file()==success
   if success:assert len(completed)==1 and 0<completed[0]['analysisElapsedNanos']<=elapsed
   verified=[e for e in events if e['event']=='prepared_map_wire_verified']
   if verified:assert raw is not None and verified[0]['mapBytes']==len(raw) and verified[0]['mapSha256']==hashlib.sha256(raw).hexdigest()
   assert type(usage.ru_maxrss) is int and 0<=usage.ru_maxrss<=2**64-1;records.append(dict(name=name,successExpected=success,compilerExpected=compiler_expected,argv=argv,inputFrames=pin(r/'input.frames'),sourceMap=pin(r/'source.map') if raw is not None else None,returncode=child.returncode,rootReapedElapsedNanos=elapsed,workerReadyNanos=ready_elapsed,rssNative=usage.ru_maxrss,rssUnit='Darwin bytes',informationOnly=True,events=events,metadata=pin(out) if out.is_file() else None));print(dict(control=name,returncode=child.returncode,compilerStarted=compiled),flush=True)
  finally:
   if not reaped:os.kill(child.pid,signal.SIGKILL);reap(child)
   child.stdout.close();err.close()
 (V/'controls-r1.json').write_text(json.dumps(dict(standing='NEW FIRSTPARTY FRAMED ANALYSIS CONTROLS; UNREVIEWED; NO CORPUS',root=str(root),controlsPassed=len(records),childProcesses=len(records),compilerInvocations=sum(r['compilerExpected'] for r in records),completedAnalyses=sum(r['successExpected'] for r in records),records=records,driverSource=pin(V/'driver.rs'),compiledImage=pin(image),acceptedTimingParentSource=pin(B/'sm-analysis-timing-2026-10-10/driver.rs'),actualCorpusUse=False,sourceAuthentication=False,nativeAdmission=False,SMComplete=False),indent=2)+'\n')
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
