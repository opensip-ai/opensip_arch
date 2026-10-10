from pathlib import Path
import json,types,hashlib,subprocess,tempfile,os,stat,time,statistics,io
B=Path(__file__).resolve().parent;C=Path('/Users/sb/code/.opensip-implementation-cache');old=Path('/tmp/opensip-implementation/sm-rust-typecheck-2026-10-09');cohort=json.loads((old/'results.json').read_text());template=json.loads(Path('/tmp/opensip-implementation/sm-sealing-typed-2026-10-09/control-template.json').read_text())['snapshot']

def load(name):
 m=types.ModuleType(name);exec(compile((B/(name+'.py')).read_text(),name+'.py','exec'),m.__dict__);return m
A=load('accounting');F=load('frame_codec');I=load('independent_host_codec');
source_pins={str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(B.glob('*.py'))};helper=json.loads((B/'build.json').read_text());helper_exe=Path(helper['executable']['path']);assert hashlib.sha256(helper_exe.read_bytes()).hexdigest()==helper['executable']['sha256'];os.setpriority(os.PRIO_PROCESS,0,10)
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-sm-public-wire-',dir=D));T.chmod(0o700);lane=D/'opensip-lanes.lock';owned=False
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('waiting for measurement lane',flush=True);time.sleep(5)
try:
 E=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
 if 'HOME' in os.environ:E['HOME']=os.environ['HOME']
 results=[]
 for workload in cohort['workloads']:
  inv=workload['inventory'];id_=inv['id'];root=Path(inv['virtualRoot']);entries=[];blobs={}
  for original in inv['files']:
   p=root/original['path'];st=p.lstat();assert stat.S_ISREG(st.st_mode);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
   with os.fdopen(fd,'rb') as f:
    before=os.fstat(f.fileno());assert (st.st_dev,st.st_ino)==(before.st_dev,before.st_ino);raw=f.read();after=os.fstat(f.fileno());assert (before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
   assert len(raw)==original['bytes'] and hashlib.sha256(raw).hexdigest()==original['sha256'];blobs[original['path']]=raw;entries.append(dict(path=original['path'],kind='file',byteLength=len(raw),contentSha256=original['sha256'],executable=bool(before.st_mode&0o111),targetBytes=None))
  descriptor=dict(template,sourceInventory=[dict(path=row['path'],sha256=row['contentSha256'],bytes=row['byteLength']) for row in entries]);canonical=json.dumps(descriptor,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();assert len(canonical)<=2**22 and len(entries)<=100_000
  sid='snapshot2:'+hashlib.sha256(b'opensip.product.v1\0snapshot\0'+len(canonical).to_bytes(8,'big')+canonical).hexdigest();sha=hashlib.sha256(A.encode(entries)).hexdigest();mp=dict(snapshotId=sid,manifestSha256=sha,entries=entries)
  hp=T/(id_+'-scope-input.json');hp.write_text(json.dumps(dict(snapshotId=sid,manifestEntries=entries))+'\n')
  host_start=time.monotonic_ns();independent_subjects=I.derive(sid,entries);independent_cbor=I.encode(independent_subjects);independent_scope=I.commitment('opensip.rust-provider.subject-scope.v2',independent_subjects);host_python_nanos=time.monotonic_ns()-host_start
  scope_child=subprocess.Popen([str(helper_exe),str(hp)],cwd=T,env=E,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert os.getpriority(os.PRIO_PROCESS,scope_child.pid)==10;host_raw,host_err=scope_child.communicate();assert scope_child.returncode==0,host_err.decode();rust_scope=json.loads(host_raw);assert rust_scope['subjects']==independent_subjects and rust_scope['subjectScopeCommitment']==independent_scope and rust_scope['subjectsCborBytes']==len(independent_cbor) and rust_scope['subjectsCborRawSha256']==hashlib.sha256(independent_cbor).hexdigest()
  (B/(id_+'-host-scope.json')).write_text(json.dumps(dict(rust=rust_scope,independentPythonNanos=host_python_nanos,observedRustHelperNiceness=10),indent=2)+'\n')
  wire=T/(id_+'.frames');sequence=0;count=0;total=0
  with wire.open('wb') as sink:
   def write(kind,payload):
    global sequence
    sink.write(F.frame(dict(protocolMajor=3,direction='host-to-worker',sequence=sequence,frameType=kind,payload=payload),A.encode));sequence+=1
   write('SnapshotManifest',mp)
   for row in entries:
    raw=blobs[row['path']]
    for index,offset in enumerate(range(0,len(raw),2**20)):
     chunk=raw[offset:offset+2**20];write('SnapshotFileChunk',dict(snapshotId=sid,path=row['path'],chunkIndex=index,byteOffset=offset,bytes=chunk));count+=1;total+=len(chunk)
   seal=dict(snapshotId=sid,manifestSha256=sha,entryCount=len(entries),totalFileBytes=total,totalChunkCount=count);write('SnapshotSeal',seal)
  wire.chmod(0o400);blobs.clear();(B/(id_+'-manifest.json')).write_text(json.dumps(mp,indent=2)+'\n');(B/(id_+'-snapshot-fixture.json')).write_text(json.dumps(dict(standing='ACTUAL PUBLIC REGULAR READSET WITH SYNTHETIC HARNESS PROJECT/CONFIG/SCOPE/VCS PRECONDITIONS; NO PRODUCTION ADMISSION',snapshotId=sid,descriptor=descriptor,canonicalDescriptorBytes=len(canonical),originalNonregularExcluded=inv['nonregularExcluded'],dependencySourcesIncluded=False,fullOwningSnapshotAdmitted=False),indent=2)+'\n');samples=[]
  for n in range(10):
   out=B/(id_+'-wire-'+str(n)+'.stdout');err=B/(id_+'-wire-'+str(n)+'.stderr');report=B/(id_+'-wire-'+str(n)+'.json');start=time.monotonic_ns()
   with wire.open('rb') as source,out.open('wb') as o,err.open('wb') as e:
    child=subprocess.Popen(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(B/'snapshot_wire_worker.py'),'0','0',str(report)],stdin=subprocess.PIPE,stdout=o,stderr=e,env=E);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10
    while chunk:=source.read(2**20):child.stdin.write(chunk)
    child.stdin.close();_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
   elapsed=time.monotonic_ns()-start;assert child.returncode==0,(id_,n,err.read_text());decoder=F.Reader(io.BytesIO(out.read_bytes()),A.encode);echo,_=decoder.next();assert echo['frameType']=='SnapshotAccepted' and echo['payload']==seal;observed=json.loads(report.read_text());assert observed['subjects']==independent_subjects and observed['subjectScopeCommitment']==independent_scope and observed['subjectsCborBytes']==len(independent_cbor) and observed['subjectsCborRawSha256']==hashlib.sha256(independent_cbor).hexdigest();assert observed['accepted']==seal and observed['files']=={r['path']:dict(bytes=r['byteLength'],sha256=r['contentSha256']) for r in entries};samples.append(dict(ordinal=n,warmup=n<3,wholeFragmentProcessNanos=elapsed,rssNative=int(usage.ru_maxrss),rssUnit='bytes',observedChildNiceness=priority,scopeRebuildNanos=observed['scopeRebuildNanos'],report=str(report),stdout=str(out),stderr=str(err)))
  results.append(dict(id=id_,manifestSha256=sha,snapshotFixtureId=sid,subjectCount=len(independent_subjects),subjectScopeCommitment=independent_scope,regularEntries=len(entries),fileBytes=total,chunkCount=count,requestFrames=sequence,wireBytes=wire.stat().st_size,wireSha256=hashlib.sha256(wire.read_bytes()).hexdigest(),canonicalDescriptorBytes=len(canonical),runs=samples,medianWorkerScopeRebuildNanos=statistics.median(x['scopeRebuildNanos'] for x in samples[3:]),maxWorkerScopeRebuildNanos=max(x['scopeRebuildNanos'] for x in samples[3:]),medianWholeFragmentProcessNanos=statistics.median(x['wholeFragmentProcessNanos'] for x in samples[3:]),maxWholeFragmentProcessNanos=max(x['wholeFragmentProcessNanos'] for x in samples[3:]),dependencySourcesIncluded=False,wholeWorkspaceOverlayIncluded=False));print(id_,len(entries),'regular rows',total,'bytes;10actualframedchildren PASS',flush=True)
 v=dict(standing='PRELIMINARY REAL PUBLIC T2 REGULAR READSET SNAPSHOT-ONLY TRANSPORT FRAGMENTS; INCOMPLETE DEPENDENCY/OVERLAY/PLAN/DOMAIN WORKLOADS',workloads=results,freshChildren=80,ownedLane=True,observedParentNiceness=os.getpriority(os.PRIO_PROCESS,0),privateTMPDIR=str(T),TMPDIRMode='0700',HOMEUnchanged=True,repositoryCodeExecuted=False,actualFramedSnapshotAcceptance=True,syntheticDescriptorPreconditions=True,completeRequiredWorkload=False,actualC2PlanOrKeys=False,SM7PlaceholderFilled=False,SM12PlaceholderFilled=False,fullSM=False,sourceAdmission=False,protocolConformance=False)
 assert source_pins=={str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(B.glob('*.py'))};v.update(sourcePins=source_pins,scopeHelper=helper,actualAcceptedManifestScopeArrayEquality=True,actualC2PlanOrKeys=False,domainCommitmentMeasured=False,SM12FigureComplete=False,scopePeakMemoryMeasured=False)
 (B/'t2-snapshot-fragments.json').write_text(json.dumps(v,indent=2)+'\n');print('80fresh actual snapshot fragment children complete',flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
