"""Gated new observations only: repository plus dependency source map transfer."""
from pathlib import Path
import os,json,hashlib,sys,subprocess,struct,time,tempfile,statistics,signal,stat
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-dependency-map-transfer-2026-10-10';S=B/'sm-dependency-map-transfer-controls-r1-stage';Q=B/'reviews/grok-sm-dependency-map-transfer-controls-r1';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'actual-samples-r1.json';assert not dest.exists();state=json.loads((C/'CURRENT-STATE.json').read_bytes());pub=state['SMDependencyMapTransferControlsPublication'];review=json.loads((Q/'review.json').read_bytes());subject=hashlib.sha256((S/'subject.json').read_bytes()).hexdigest();assert review['verdict']=='ACCEPT' and review['requiredFindings']==[] and review['subjectManifestSha256']==pub['subjectManifest']['sha256']==subject;assert review['controlsPassed']==10 and review['childProcesses']==10 and review['historicalReadinessImportFailureChildren']==1
source=json.loads((S/'source.json').read_bytes())
def check(pin):
 p=Path(pin['path']);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
 with os.fdopen(fd,'rb') as f:
  a=os.fstat(f.fileno());assert stat.S_ISREG(a.st_mode);h=hashlib.sha256();count=0
  while b:=f.read(1<<20):h.update(b);count+=len(b)
  z=os.fstat(f.fileno());assert (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns);assert count==pin['bytes'] and h.hexdigest()==pin['sha256']
 return p
for key in ['receiverSource','readinessWrapperSource']:check(source[key])
mp=B/'sm-command-data-2026-10-10/actual-command-source-maps-r1.json';raw=mp.read_bytes();maps=json.loads(raw);assert len(maps['results'])==9;root=Path(tempfile.mkdtemp(prefix='opensip-sm-dependency-transfer-samples-',dir=O));root.chmod(0o700);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME');results=[]
def write_all(pipe,data):
 view=memoryview(data)
 while view:
  n=pipe.write(view)
  if n is None or n<=0:raise OSError('pipe made no progress')
  view=view[n:]
def send(pipe,data):assert 0<len(data)<=1<<20;write_all(pipe,struct.pack('>I',len(data)));write_all(pipe,data)
def reap(child):
 while True:
  try:pid,status,usage=os.wait4(child.pid,0);assert pid==child.pid;child.returncode=os.waitstatus_to_exitcode(status);return usage
  except InterruptedError:continue
try:
 while True:
  try:lane.mkdir();owned=True;break
  except FileExistsError:print('Waiting for ordinary transfer measurement lane',flush=True);time.sleep(5)
 for entry in maps['results']:
  assert entry['excluded']==[];p=check(entry['sourceMap']);samples=[];expected=None
  for n in range(10):
   for key in ['receiverSource','readinessWrapperSource']:check(source[key])
   check(entry['sourceMap']);prefix=root/(str(entry['ordinal'])+'-'+str(n));err=prefix.with_suffix('.stderr').open('xb');child=subprocess.Popen(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',source['readinessWrapperSource']['path']],cwd=root,env={'TMPDIR':str(root)},stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,bufsize=0);reaped=False
   try:
    ready=child.stdout.readline();assert ready==b'ready\n';start=time.monotonic_ns();header=json.dumps(dict(format='OPSMRUST1',bytes=entry['sourceMap']['bytes'],sha256=entry['sourceMap']['sha256']),sort_keys=True,separators=(',',':')).encode();send(child.stdin,header);frames=0;h=hashlib.sha256();length=0
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    with os.fdopen(fd,'rb') as f:
     a=os.fstat(f.fileno())
     while chunk:=f.read(1<<20):send(child.stdin,chunk);h.update(chunk);length+=len(chunk);frames+=1
     z=os.fstat(f.fileno());assert (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
    child.stdin.close();response=child.stdout.read();end=time.monotonic_ns();usage=reap(child);reaped=True;assert child.returncode==0 and length==entry['sourceMap']['bytes'] and h.hexdigest()==entry['sourceMap']['sha256'];value=json.loads(response);assert value['rows']==entry['preparedFiles'] and value['contentBytes']==entry['sourceContentBytes'] and value['contentFrames']==frames and value['mapSha256']==entry['sourceMap']['sha256'];assert expected is None or value==expected;expected=value;prefix.with_suffix('.stdout').write_bytes(ready+response);rss=usage.ru_maxrss;assert type(rss) is int and 0<=rss<=2**64-1;samples.append(dict(ordinal=n,warmup=n<3,transferNanos=end-start,rssNative=rss,rssUnit='bytes',rssBytes=rss,informationOnly=True,contentFrames=frames,headerBytes=len(header),returncode=child.returncode,result=value))
   finally:
    if not reaped:
     # Only the unreaped child started by this invocation may be signalled.
     os.kill(child.pid,signal.SIGKILL);reap(child)
    child.stdout.close();err.close()
  measured=[r['transferNanos'] for r in samples if not r['warmup']];results.append(dict(id=entry['id'],ordinal=entry['ordinal'],sourceMap=entry['sourceMap'],preparedFiles=entry['preparedFiles'],sourceContentBytes=entry['sourceContentBytes'],samples=samples,medianTransferNanos=statistics.median(measured),maxTransferNanos=max(measured)));report=dict(standing='NEW PRELIMINARY REPOSITORY PLUS EXPANDED RUST DEPENDENCY MAP TRANSFER; NOT FULL SM7',root=str(root),inputMaps=dict(path=str(mp),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),results=results,receiverControlsSubject=subject,compilerExecuted=False,repositoryCodeExecuted=False,sourceBytesWrittenToDisk=False,sourceAuthentication=False,nativeAdmission=False,physicalPeakScratchMeasured=False,SM7Complete=False,SMComplete=False,effectiveL=False,productQualification=False,span='parent first header frame write through final verified response; child startup and preflight map hashing excluded; sender streamed rehash included',warmups=3,measuredRuns=7,ownedLane=True,niceness=10);dest.write_text(json.dumps(report,indent=2)+'\n');print(dict(ordinal=entry['ordinal'],medianTransferNanos=results[-1]['medianTransferNanos']),flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
