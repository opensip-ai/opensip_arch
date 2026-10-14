from pathlib import Path
import os,sys,json,hashlib,time,stat,subprocess,tempfile,statistics,struct,shutil
# U-2c SM-7 series r2 (D-2, D-3): per Rust entry, one child per sample receives the sealed repository set (accepted
# run_transfer.py snapshot phase: same sealed copies, canonical manifest, <= 1 MiB u32-framed chunks) and then the entry's
# DependencySourceSetV1 in NE section 3.2/9.2 order (receiver_ne_shape.py): one DependencySourceManifest frame of
# {packageKey, path, byteLength, contentSha256} entries in descriptor package order, raw content chunks <= 1 MiB, and
# DependencySourceSeal, echoed by the receiver. r1 (descriptor frame plus per-package manifests) is retained as history. The overlay's two entries each stream the whole overlay workspace (member mounts). 3 warmups + 7 measured,
# priority 10, lane held, private 0700 TMPDIR. Span: first frame write through the receiver's verified response.
W=Path(__file__).resolve().parent;C=Path('/Users/sb/code/.opensip-implementation-cache');A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document;from store import verify
U=Path('/tmp/opensip-implementation/sm-dependency-source-sets-2026-10-14');V=Path('/tmp/opensip-implementation/sm-overlay-metadata-2026-10-14')
os.setpriority(os.PRIO_PROCESS,0,10);assert os.getpriority(os.PRIO_PROCESS,0)==10
acceptedT=json.loads((A/'docs/implementation/m3/spikes/s-m-transfer-2026-10-09/results.json').read_text());acceptedSnap={w['id']:w for w in acceptedT['workloads']}
raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578';m=manifest_document(raw);entries={r['id']:r for r in m['repositories']}
overlay=next(w for w in m['workspaces'] if w['id']=='mr-rs-medium-serde-json')
inputs=json.loads((W/'u2c-inputs.json').read_text())['entries'];dest=W/'sm7-results-r2.json';assert not dest.exists();E=W/'sm7-r2-evidence';E.mkdir()
def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write_all(pipe,data):
 view=memoryview(data)
 while view:
  n=pipe.write(view)
  if n is None or n<=0:raise OSError('pipe short write without progress')
  view=view[n:]
def send(pipe,payload):assert len(payload)<=1048576;write_all(pipe,struct.pack('>I',len(payload)));write_all(pipe,payload)
def send67(pipe,payload):assert len(payload)<=67108864;write_all(pipe,struct.pack('>I',len(payload)));write_all(pipe,payload)
def members(entry_id):
 if entry_id.startswith('mr-rs-medium-serde-json/'):return [(C/'t2-corpus-c8cc48e1/store'/entries[r['entry']]['treeDigest']['value'],r['mount']+'/',r['entry']) for r in overlay['overlay']['members']]
 return [(C/'t2-corpus-c8cc48e1/store'/entries[entry_id]['treeDigest']['value'],'',entry_id)]
D=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');lane=D/'opensip-lanes.lock';owned=False
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('waiting for lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-u2c-sm7-',dir=D));T.chmod(0o700);env=dict(os.environ,TMPDIR=str(T));results=[]
 for e in inputs:
  sealed=T/e['slug'];sealed.mkdir(mode=0o700);rows=[];excluded=[];verified=[]
  for root,prefix,eid in members(e['entry']):
   verified.append(dict(entry=eid,treeVerified=verify(root,entries[eid])))
   for directory,dirs,files in os.walk(root,followlinks=False):
    for name in list(dirs):
     p=Path(directory)/name
     if p.is_symlink():excluded.append(dict(path=prefix+str(p.relative_to(root)),kind='symlink-directory'));dirs.remove(name)
    for name in files:
     p=Path(directory)/name;info=p.lstat();rel=prefix+str(p.relative_to(root))
     if not stat.S_ISREG(info.st_mode):excluded.append(dict(path=rel,kind='nonregular'));continue
     fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC);dst=sealed/str(len(rows));h=hashlib.sha256();count=0
     with os.fdopen(fd,'rb')as f,dst.open('xb')as out:
      before=os.fstat(f.fileno());assert(info.st_dev,info.st_ino)==(before.st_dev,before.st_ino)
      while part:=f.read(1048576):h.update(part);out.write(part);count+=len(part)
      after=os.fstat(f.fileno());assert(before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)and count==info.st_size
     dst.chmod(0o400);rows.append(dict(path=rel,bytes=count,sha256=h.hexdigest(),sealed=str(dst)))
  rows.sort(key=lambda r:r['path'].encode('utf8'));excluded.sort(key=lambda r:r['path'].encode('utf8'));manifest=can([{k:r[k]for k in ['path','sha256','bytes']}for r in rows]);assert len(manifest)<=1048576
  acc=acceptedSnap.get(e['entry'])
  if acc:assert hashlib.sha256(manifest).hexdigest()==acc['manifestSha256'] and len(rows)==acc['rows'] and excluded==acc['nonregularExcluded']
  snapshotControl=dict(acceptedSnapshotManifestEqual=True,acceptedId=acc['id']) if acc else dict(acceptedSnapshotManifestEqual=None,reason='no accepted repository-only transfer workload for this entry (overlay workspace R8 was not in the accepted 12)')
  (E/f"{e['slug']}-sealed-manifest.json").write_bytes(manifest)
  desc=json.loads(Path(e['descriptor']).read_text());descRaw=can(desc);setdir=(V if e['slug']=='mr-rs-medium-serde-json__rs-medium-serde-json' else U)/'u2b-sets'/e['slug'];assert hashlib.sha256((setdir/'descriptor.json').read_bytes()).hexdigest()==e['descriptorSha256']
  keyof={tuple(r['packageTuple'][:2]):r for r in json.loads((setdir/'file-manifest-observations.json').read_text())['rows']}
  pk={p['name']+'@'+p['version']:p for p in e['packages']};dm=[];paths=[]
  for p in desc['packages']:
   q=pk[p['name']+'@'+p['version']];k=keyof[(p['name'],p['version'])];assert k['fileManifestSha256']==p['fileManifestSha256']==q['fileManifestSha256'];listing=json.loads(Path(q['manifest']).read_text())
   for r in listing:dm.append(dict(packageKey=k['packageKey'],path=r['path'],byteLength=r['byteLength'],contentSha256=r['contentSha256']));paths.append(Path(q['root'])/r['path'])
  dmRaw=can(dict(dependencySourceSetId=e['dependencySourceSetId'],entries=dm));assert len(dmRaw)<=67108864 and len(dm)==e['files']
  depChunks=sum(-(-r['byteLength']//1048576)for r in dm);seal=can(dict(dependencySourceSetId=e['dependencySourceSetId'],manifestSha256=hashlib.sha256(dmRaw).hexdigest(),entryCount=len(dm),totalBytes=e['bytes'],totalChunkCount=depChunks))
  samples=[]
  for n in range(10):
   log=E/f"{e['slug']}-{n}.stderr";err=log.open('wb');child=subprocess.Popen([PY,'-I','-B',str(W/'receiver_ne_shape.py')],cwd=T,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,bufsize=0)
   assert os.getpriority(os.PRIO_PROCESS,child.pid)==10;assert child.stdout.readline()==b'ready\n';start=time.monotonic_ns();frames=1;send(child.stdin,manifest)
   for row in rows:
    with open(row['sealed'],'rb')as f:
     while part:=f.read(1048576):send(child.stdin,part);frames+=1
   send67(child.stdin,dmRaw);frames+=1
   for path in paths:
    with open(path,'rb')as f:
     while part:=f.read(1048576):send(child.stdin,part);frames+=1
   send(child.stdin,seal);frames+=1
   child.stdin.close();response=child.stdout.read();end=time.monotonic_ns();_,status,usage=os.wait4(child.pid,0);code=os.waitstatus_to_exitcode(status);child.stdout.close();err.close();assert code==0,log.read_text()
   obs=json.loads(response);assert obs['rows']==len(rows) and obs['frames']==frames and obs['allDigestsVerified'] and obs['accepted']==json.loads(seal) and obs['dependencyPackages']==len(desc['packages']) and obs['dependencyManifestBytes']==len(dmRaw)
   (E/f"{e['slug']}-{n}.stdout.json").write_bytes(response);samples.append(dict(ordinal=n,warmup=n<3,transferNanos=end-start,receiverNanos=obs['receiverNanos'],frames=frames,rssNative=int(usage.ru_maxrss),rssUnit='bytes'))
  vals=[s['transferNanos']for s in samples if not s['warmup']]
  results.append(dict(entry=e['entry'],slug=e['slug'],members=verified,snapshotControl=snapshotControl,manifestSha256=hashlib.sha256(manifest).hexdigest(),dependencySourceSetId=e['dependencySourceSetId'],descriptorSha256=hashlib.sha256(descRaw).hexdigest(),snapshotRows=len(rows),snapshotBytes=sum(r['bytes']for r in rows),nonregularExcluded=excluded,manifestBytes=len(manifest),dependencyManifestBytes=len(dmRaw),dependencyManifestSha256=hashlib.sha256(dmRaw).hexdigest(),dependencySeal=json.loads(seal),descriptorCanonicalBytes=len(descRaw),dependencyPackages=len(desc['packages']),dependencyFiles=e['files'],dependencyBytes=e['bytes'],runs=samples,medianTransferNanos=statistics.median(vals),maxTransferNanos=max(vals)))
  shutil.rmtree(sealed);print(e['entry'],len(rows),e['files'],round(statistics.median(vals)/1e6,3),flush=True)
  dest.write_text(json.dumps(dict(supersedes='sm7-results-r1.json (descriptor frame plus per-package manifest frames; retained as history)',standing='UNREVIEWED U-2c SM-7 TRANSFER SERIES r2 (D-2, D-3; NE 3.2/9.2 DEPENDENCY ORDER, JSON PAYLOADS, NO CBOR CONFORMANCE); LEAD macOS PRELIMINARY; GENERATED-LOCK SETS ARE SIZING STAND-INS',results=results,TMPDIR=str(T),laneHeldForEntireSet=True,nice=10,maxPayloadChunkBytes=1048576,maxDependencyManifestFrameBytes=67108864,protocolFrameConformanceClaimed=False,frameHeader='u32 big-endian payload length',transferSpan='first frame write through the receiver verified response; child spawn/ready and repository sealing excluded',SM7ValueRecorded=False),indent=1)+'\n')
 def neg(label,data):
  child=subprocess.Popen([PY,'-I','-B',str(W/'receiver_ne_shape.py')],cwd=T,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate(data);assert child.returncode!=0,label;(E/f'control-{label}.stdout').write_bytes(out);(E/f'control-{label}.stderr').write_bytes(err);return dict(label=label,exitCode=child.returncode,synthetic=True)
 fr=lambda b:struct.pack('>I',len(b))+b;empty=fr(can([]));sid0='sha256:'+'0'*64;e1=[dict(packageKey='k',path='a',byteLength=1,contentSha256=hashlib.sha256(b'x').hexdigest())];m1=can(dict(dependencySourceSetId=sid0,entries=e1));s1=dict(dependencySourceSetId=sid0,manifestSha256=hashlib.sha256(m1).hexdigest(),entryCount=1,totalBytes=1,totalChunkCount=1)
 ok=subprocess.run([PY,'-I','-B',str(W/'receiver_ne_shape.py')],cwd=T,env=env,input=empty+fr(m1)+fr(b'x')+fr(can(s1)),capture_output=True);assert ok.returncode==0 and json.loads(ok.stdout.splitlines()[1])['accepted']==s1
 controls=[neg('oversized-frame',struct.pack('>I',1048577)),neg('snapshot-digest-mismatch',fr(can([dict(path='a',bytes=1,sha256='0'*64)]))+fr(b'x')),neg('truncated-frame',struct.pack('>I',4)+b'[]'),
  neg('dependency-digest-mismatch',empty+fr(m1)+fr(b'y')+fr(can(s1))),
  neg('dependency-seal-count-mismatch',empty+fr(m1)+fr(b'x')+fr(can(dict(s1,entryCount=2)))),
  neg('dependency-seal-manifest-digest-mismatch',empty+fr(m1)+fr(b'x')+fr(can(dict(s1,manifestSha256='0'*64)))),
  neg('dependency-oversized-chunk',empty+fr(can(dict(dependencySourceSetId=sid0,entries=[dict(e1[0],byteLength=1048577)])))+struct.pack('>I',1048577)),
  neg('dependency-duplicate-entry',empty+fr(can(dict(dependencySourceSetId=sid0,entries=e1+e1)))),
  neg('trailing-bytes',empty+fr(m1)+fr(b'x')+fr(can(s1))+b'z')]
 positiveControl=dict(label='minimal-valid-dependency-phase',exitCode=0,synthetic=True)
 doc=json.loads(dest.read_text());doc['controls']=controls;doc['positiveControl']=positiveControl;dest.write_text(json.dumps(doc,indent=1)+'\n');print('sm7 complete',flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
