from pathlib import Path
import os,sys,json,hashlib,time,stat,subprocess,tempfile,statistics,struct,datetime,shutil
B=Path(__file__).resolve().parent;C=Path('/Users/sb/code/.opensip-implementation-cache');A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document
from store import verify
raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578';m=manifest_document(raw);entries={r['id']:r for r in m['repositories']};ids=sorted(set(m['counts']['tsjs']['medium']['devIds']+m['counts']['rust']['medium']['devIds']));assert len(ids)==12 and all(not entries[i]['heldOut']for i in ids)
previous=json.loads(Path('/tmp/opensip-implementation/sm-foundation-2026-10-09/sealing-results.json').read_text());prior={w['id']:w['shape']for w in previous['workloads']};DARWIN=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());LOCK=DARWIN/'opensip-lanes.lock';owned=False
while True:
 try:LOCK.mkdir();owned=True;break
 except FileExistsError:print('waiting for owned measurement lane',flush=True);time.sleep(5)
try:
 ps=subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines();assert not [r for r in ps if r.split()[-1].rsplit('/',1)[-1]in ['cargo','rustc','clippy-driver']]
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-transfer-',dir=DARWIN));T.chmod(0o700);env=dict(os.environ,TMPDIR=str(T));results=[]
 def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
 def write_all(pipe,data):
  view=memoryview(data)
  while view:
   n=pipe.write(view)
   if n is None or n<=0:raise OSError('pipe short write without progress')
   view=view[n:]
 def send(pipe,payload):assert len(payload)<=1048576;write_all(pipe,struct.pack('>I',len(payload)));write_all(pipe,payload)
 for id_ in ids:
  entry=entries[id_];root=C/'t2-corpus-c8cc48e1/store'/entry['treeDigest']['value'];verified=verify(root,entry);sealed=T/id_;sealed.mkdir(mode=0o700);rows=[];excluded=[]
  for directory,dirs,files in os.walk(root,followlinks=False):
   for name in list(dirs):
    p=Path(directory)/name
    if p.is_symlink():excluded.append(dict(path=str(p.relative_to(root)),kind='symlink-directory'));dirs.remove(name)
   for name in files:
    p=Path(directory)/name;info=p.lstat();rel=str(p.relative_to(root))
    if not stat.S_ISREG(info.st_mode):excluded.append(dict(path=rel,kind='nonregular'));continue
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC);dest=sealed/str(len(rows));h=hashlib.sha256();count=0
    with os.fdopen(fd,'rb')as f,dest.open('xb')as out:
     before=os.fstat(f.fileno());assert(info.st_dev,info.st_ino)==(before.st_dev,before.st_ino)
     while part:=f.read(1048576):h.update(part);out.write(part);count+=len(part)
     after=os.fstat(f.fileno());assert(before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)and count==info.st_size
    dest.chmod(0o400);rows.append(dict(path=rel,bytes=count,sha256=h.hexdigest(),sealed=str(dest)))
  rows.sort(key=lambda r:r['path'].encode('utf8'));excluded.sort(key=lambda r:r['path'].encode('utf8'));manifest=[{k:r[k]for k in ['path','sha256','bytes']}for r in rows];manifestRaw=can(manifest);assert len(manifestRaw)<=1048576;assert hashlib.sha256(manifestRaw).hexdigest()==prior[id_]['inventoryDigest']and excluded==prior[id_]['nonregularExcluded'];assert sum(r['bytes']for r in rows)==prior[id_]['totalRegularBytes'];(B/'evidence'/f'{id_}-sealed-manifest.json').write_bytes(manifestRaw);samples=[]
  for n in range(10):
   log=B/'evidence'/f'{id_}-{n}.stderr';err=log.open('wb');child=subprocess.Popen(['/usr/bin/nice','-n','10',PY,'-I','-B',str(B/'receiver.py')],cwd=T,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,bufsize=0);assert child.stdout.readline()==b'ready\n';start=time.monotonic_ns();sentFrames=1;send(child.stdin,manifestRaw)
   for row in rows:
    with open(row['sealed'],'rb')as f:
     while part:=f.read(1048576):send(child.stdin,part);sentFrames+=1
   child.stdin.close();response=child.stdout.read();end=time.monotonic_ns();_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status);child.stdout.close();err.close();assert child.returncode==0,log.read_text();observed=json.loads(response);assert observed['rows']==len(rows)and observed['contentBytes']==sum(r['bytes']for r in rows)and observed['frames']==sentFrames and observed['allDigestsVerified'];out=B/'evidence'/f'{id_}-{n}.stdout.json';out.write_bytes(response);rss=int(usage.ru_maxrss);assert 0<=rss<2**64;samples.append(dict(ordinal=n,warmup=n<3,transferNanos=end-start,receiverNanos=observed['receiverNanos'],rssNative=rss,rssUnit='bytes',rssBytes=rss,frames=sentFrames,stdout=str(out),stderr=str(log),exitCode=0))
  measured=[r['transferNanos']for r in samples if not r['warmup']];results.append(dict(id=id_,heldOut=False,commit=entry['commit'],treeDigest=entry['treeDigest']['value'],treeVerified=verified,rows=len(rows),contentBytes=sum(r['bytes']for r in rows),manifestBytes=len(manifestRaw),manifestSha256=hashlib.sha256(manifestRaw).hexdigest(),nonregularExcluded=excluded,runs=samples,medianTransferNanos=statistics.median(measured),maxTransferNanos=max(measured)));shutil.rmtree(sealed);print(id_,len(rows),'rows',statistics.median(measured),'median ns',flush=True)
 controls=[]
 for label,data in [('oversized-frame',struct.pack('>I',1048577)),('digest-mismatch',struct.pack('>I',len(can([dict(path='a',bytes=1,sha256='0'*64)])))+can([dict(path='a',bytes=1,sha256='0'*64)])+struct.pack('>I',1)+b'x'),('truncated-frame',struct.pack('>I',4)+b'[]')]:
  child=subprocess.Popen(['/usr/bin/nice','-n','10',PY,'-I','-B',str(B/'receiver.py')],cwd=T,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate(data);assert child.returncode!=0; (B/'evidence'/f'control-{label}.stdout').write_bytes(out);(B/'evidence'/f'control-{label}.stderr').write_bytes(err);controls.append(dict(label=label,exitCode=child.returncode,synthetic=True))
 report=dict(schemaVersion=1,standing='UNREVIEWED PRELIMINARY REPOSITORY-ONLY REGULAR-SET PIPE TRANSFER; PARTIAL S-M',recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),platformVersion=subprocess.check_output(['/usr/bin/sw_vers']).decode(),manifestSha256=hashlib.sha256(raw).hexdigest(),workloads=results,controls=controls,TMPDIR=str(T),TMPDIRMode='0700',ownedLane=str(LOCK),laneHeldForEntireSet=True,nice=10,maxPayloadChunkBytes=1048576,frameHeader='u32 big-endian payload length',transferSpan='parent first frame write through receiver final verified response; child spawn/ready and file sealing excluded',dependencySourceSetsIncluded=False,nonregularSnapshotPolicySelected=False,protocolFrameConformanceClaimed=False,SM7PlaceholderFilled=False,SMComplete=False,LG1Met=False,repositoryCodeExecuted=False,heldOutSourceInspected=False,Q6Qualification=False,effectiveL=False,productQualification=False)
 (B/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('transfer batch complete',flush=True)
finally:
 if owned:LOCK.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
