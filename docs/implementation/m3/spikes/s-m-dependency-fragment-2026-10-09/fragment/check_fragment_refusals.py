from pathlib import Path
import types,sys,copy,json,hashlib,io,statistics,os
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B));os.setpriority(os.PRIO_PROCESS,0,10)
def load(name):
 m=types.ModuleType(name);exec(compile((B/(name+'.py')).read_text(),name+'.py','exec'),m.__dict__);return m
A=load('accounting');F=load('frame_codec');S=load('dependency_receiver');pkg='pkg1-'+'a'*64;sid='sha256:'+'b'*64
entries=[dict(packageKey=pkg,path='a.rs',byteLength=1,contentSha256=hashlib.sha256(b'a').hexdigest()),dict(packageKey=pkg,path='z.rs',byteLength=1,contentSha256=hashlib.sha256(b'z').hexdigest())];expected={(r['packageKey'],r['path']):(r['byteLength'],r['contentSha256']) for r in entries}
manifest=dict(dependencySourceSetId=sid,entries=entries,manifestSha256=hashlib.sha256(A.encode(entries)).hexdigest())
chunk=dict(dependencySourceSetId=sid,packageKey=pkg,path='a.rs',chunkIndex=0,byteOffset=0,bytes=b'a')
def fixture():r=S.Receiver(A.encode,sid,expected);r.manifest(copy.deepcopy(manifest));return r
results=[]
def refuse(name,action,r=None):
 try:action()
 except (S.HarnessRefusal,F.WireRefusal) as e:
  if r is not None:assert r.state=='failed'
  results.append(dict(name=name,refused=True,reason=str(e)));return
 raise AssertionError(name+' accepted')
for name,field,value in [('wrong-set','dependencySourceSetId','sha256:'+'c'*64),('wrong-entry-digest','manifestSha256','0'*64),('extra-field','extra',None)]:
 r=S.Receiver(A.encode,sid,expected);v=copy.deepcopy(manifest);v[field]=value;refuse(name,lambda:r.manifest(v),r)
for name,mutation in [('duplicate-entry',lambda v:v['entries'].append(v['entries'][0])),('missing-entry',lambda v:v['entries'].pop()),('boolean-length',lambda v:v['entries'][0].update(byteLength=True)),('wrong-membership-digest',lambda v:v['entries'][0].update(contentSha256='0'*64)),('traversal-path',lambda v:v['entries'][0].update(path='../a.rs'))]:
 r=S.Receiver(A.encode,sid,expected);v=copy.deepcopy(manifest);mutation(v);v['manifestSha256']=hashlib.sha256(A.encode(v['entries'])).hexdigest();refuse(name,lambda:r.manifest(v),r)
for name,field,value in [('wrong-chunk-set','dependencySourceSetId','sha256:'+'c'*64),('wrong-chunk-path','path','z.rs'),('wrong-chunk-index','chunkIndex',1),('wrong-chunk-offset','byteOffset',1),('empty-chunk','bytes',b''),('changed-file-byte','bytes',b'b'),('file-overrun','bytes',b'aa')]:
 r=fixture();v=copy.deepcopy(chunk);v[field]=value;refuse(name,lambda:r.chunk(v),r)
r=fixture();seal=dict(dependencySourceSetId=sid,manifestSha256=manifest['manifestSha256'],entryCount=2,totalBytes=2,totalChunkCount=2);refuse('early-seal',lambda:r.seal(seal),r)
r=fixture();r.chunk(chunk);other=dict(chunk,path='z.rs',bytes=b'z');r.chunk(other);bad=dict(seal,totalChunkCount=3);refuse('wrong-seal-aggregate',lambda:r.seal(bad),r)
r=fixture();r.chunk(chunk);r.chunk(other);echo,vfs=r.seal(seal);assert echo==seal and dict(vfs)=={'.opensip/deps/v2/'+pkg+'/a.rs':b'a','.opensip/deps/v2/'+pkg+'/z.rs':b'z'}
try:vfs['x']=b'x'
except TypeError:pass
else:raise AssertionError('mutable accepted VFS')
refuse('post-accepted-chunk',lambda:r.chunk(chunk),r)
raw=F.frame(dict(protocolMajor=3,direction='host-to-worker',sequence=0,frameType='DependencySourceManifest',payload=manifest),A.encode);bad=bytearray(raw);bad[-1]^=1;refuse('frame-digest-bitflip',lambda:F.Reader(io.BytesIO(bad),A.encode).next())
oversize=(F.MAX_FRAME_PAYLOAD+1).to_bytes(8,'big');refuse('frame-length-before-allocation',lambda:F.Reader(io.BytesIO(oversize),A.encode).next())
observed=json.loads((B/'observations.json').read_text());assert len(observed['runs'])==10 and [r['warmup'] for r in observed['runs']]==[True]*3+[False]*7
metrics=dict(standing='DEPENDENCY-ONLY TRANSFER FRAGMENT TIMING; NO WHOLE SM OR PHASE PEAK MEMORY',measuredFreshChildren=7,warmupChildren=3,medianHostWholeFragmentNanos=statistics.median(r['hostElapsedNanos'] for r in observed['runs'][3:]),maxHostWholeFragmentNanos=max(r['hostElapsedNanos'] for r in observed['runs'][3:]),medianWorkerStreamFragmentNanos=statistics.median(r['wholeWorkerFragmentNanos'] for r in observed['runs'][3:]),workerTimingStartsAfterRetainedDescriptorAndFileManifestJoin=True,workerTimingIncludesFramedManifestChunksSealHashValidationAndReportConstruction=True,sourceAdmission=False,protocolConformance=False,phasePeakMemoryMeasured=False,fullSM=False)
# Timer is sampled after VFS hashes within report-value construction, before JSON serialization.
metrics['workerTimingIncludesFramedManifestChunksSealHashValidationAndReportConstruction']=False;metrics['workerTimingEndsAfterVfsReportHashComprehensionBeforeJsonSerialization']=True;metrics['hostTimingStartsAfterSpawnBeforeFirstFrameWrite']=True;metrics['hostTimingEndsAfterResponseEofProcessJoinAndReportReadBack']=True
(B/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');(B/'refusal-controls.json').write_text(json.dumps(dict(standing='SYNTHETIC TWO-FILE DIRECT RECEIVER/FRAME REFUSAL CONTROLS; NO SOURCESET OR PUBLIC FAILURE ADMISSION',controls=results,positiveSyntheticReceiver=True,acceptedVfsMutationRefused=True,publicFailureCodesSelected=False,protocolConformance=False,sourceAdmission=False,fullSM=False),indent=2)+'\n');print(len(results),'fragment-only refusals; exact synthetic accepted echo/immutable VFS; 7fresh timing boundaries retained')
