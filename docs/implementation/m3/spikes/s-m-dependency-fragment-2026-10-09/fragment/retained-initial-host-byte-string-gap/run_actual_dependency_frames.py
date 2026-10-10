from pathlib import Path
import json,os,subprocess,tempfile,time,hashlib,types,stat
B=Path(__file__).resolve().parent;P=B.parent;os.setpriority(os.PRIO_PROCESS,0,10)
def load(name):
 m=types.ModuleType(name);exec(compile((B/(name+'.py')).read_text(),name+'.py','exec'),m.__dict__);return m
I=load('independent_host_codec');F=load('frame_codec');D=P/'actual-dependency-source-set';set_observations=json.loads((D/'observations.json').read_text());set_id=set_observations['dependencySourceSetId'];A=json.loads((P/'axum-dependency-source-audit.json').read_text());K=json.loads((P/'actual-feature-projection/package-keys.json').read_text())['packages'];lookup={r['metadataId']:r['packageKey'] for r in K};entries=[];sources={}
for pkg in A['rows']:
 key=lookup[pkg['packageId']]
 for f in pkg['regularFiles']:
  entries.append(dict(packageKey=key,path=f['path'],byteLength=f['bytes'],contentSha256=f['sha256']));sources[(key,f['path'])]=Path(pkg['root'])/f['path']
entries.sort(key=lambda r:(r['packageKey'].encode(),r['path'].encode()));assert len(entries)==7338;manifest_sha=hashlib.sha256(I.encode(entries)).hexdigest();total=sum(r['byteLength'] for r in entries)
manifest=dict(dependencySourceSetId=set_id,manifestSha256=manifest_sha,entries=entries);(B/'actual-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
darwin=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lane=darwin/'opensip-lanes.lock';owned=False
while not owned:
 try:lane.mkdir();owned=True
 except FileExistsError:print('Waiting for ordinary dependency-fragment lane',flush=True);time.sleep(5)
runs=[];worker_started=False
try:
 for ordinal in range(10):
  T=Path(tempfile.mkdtemp(prefix='opensip-sm-dependency-fragment-',dir=darwin));T.chmod(0o700);report=T/'report.json';errpath=B/(str(ordinal)+'.stderr');E=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
  if 'HOME' in os.environ:E['HOME']=os.environ['HOME']
  with errpath.open('wb') as stderr:
   child=subprocess.Popen(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(B/'dependency_wire_worker.py'),str(D/'descriptor.json'),str(P/'actual-dependency-file-manifests'),str(report)],env=E,cwd=T,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=stderr);worker_started=True;priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;sequence=0;chunks=0;sent=0;started=time.monotonic_ns()
   def send(kind,payload):
    global sequence,sent
    raw=F.frame(dict(protocolMajor=3,direction='host-to-worker',sequence=sequence,frameType=kind,payload=payload),I.encode);child.stdin.write(raw);sequence+=1;sent+=len(raw)
   try:
    send('DependencySourceManifest',manifest)
    for row in entries:
     p=sources[(row['packageKey'],row['path'])];st=p.lstat();assert stat.S_ISREG(st.st_mode);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
     with os.fdopen(fd,'rb') as inp:
      before=os.fstat(inp.fileno());raw=inp.read();after=os.fstat(inp.fileno());assert (st.st_dev,st.st_ino)==(before.st_dev,before.st_ino);assert (before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
     assert len(raw)==row['byteLength'] and hashlib.sha256(raw).hexdigest()==row['contentSha256']
     for idx,off in enumerate(range(0,len(raw),1048576)):
      send('DependencySourceChunk',dict(dependencySourceSetId=set_id,packageKey=row['packageKey'],path=row['path'],chunkIndex=idx,byteOffset=off,bytes=raw[off:off+1048576]));chunks+=1
    seal=dict(dependencySourceSetId=set_id,manifestSha256=manifest_sha,entryCount=len(entries),totalBytes=total,totalChunkCount=chunks);send('DependencySourceSeal',seal);child.stdin.close();response=F.Reader(child.stdout,I.encode).next()[0];assert response==dict(protocolMajor=3,direction='worker-to-host',sequence=0,frameType='DependencySourceAccepted',payload=seal);assert child.stdout.read()==b'';code=child.wait();assert code==0,(code,errpath.read_text())
   except BaseException:
    # Only this fragment process is ours; no cargo process is signalled.
    if child.poll() is None:child.kill()
    child.wait();raise
  observed=json.loads(report.read_text());assert observed['accepted']==seal and observed['workerRederivedDependencySourceSetId']==set_id
  expected={'.opensip/deps/v2/'+r['packageKey']+'/'+r['path']:dict(bytes=r['byteLength'],sha256=r['contentSha256']) for r in entries};assert observed['immutableVfsFiles']==expected and errpath.read_bytes()==b'';dest=B/(str(ordinal)+'-report.json');dest.write_bytes(report.read_bytes());runs.append(dict(ordinal=ordinal,warmup=ordinal<3,observedChildNiceness=priority,privateTMPDIR=str(T),TMPDIRMode='0700',report=str(dest),stderr=str(errpath),hostElapsedNanos=time.monotonic_ns()-started,wholeWorkerFragmentNanos=observed['wholeFragmentNanos'],sentBytes=sent,frames=sequence,totalChunks=chunks));print('dependency fragment',ordinal,'PASS',len(entries),'files',flush=True)
 v=dict(standing='ACTUAL DEPENDENCY-ONLY FRAGMENT 3WARM/7FRESH CHILDREN; NOT WHOLE SM/PROTOCOL/SOURCE IMPORT ADMISSION',dependencySourceSetId=set_id,registryPackages=187,regularFiles=7338,totalFileBytes=total,manifestSha256=manifest_sha,runs=runs,independentWorkerSetAndFileManifestJoins=True,exactDependencySourceAccepted=True,immutableVfsByteHashesEqual=True,nofollowStableSourceReadEveryRun=True,actualAcceptedDependencyFragment=True,selectedImportWrapperConstructed=False,actualC2PlanOrKeys=False,protocolConformance=False,sourceAdmission=False,phasePeakMemoryMeasured=False,fullSM=False);(B/'observations.json').write_text(json.dumps(v,indent=2)+'\n');print('10actual dependency fragments complete',flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
