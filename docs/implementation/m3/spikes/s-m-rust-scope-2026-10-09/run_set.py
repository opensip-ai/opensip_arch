from pathlib import Path
import os,subprocess,tempfile,time,json,statistics,hashlib
B=Path(__file__).resolve().parent;os.setpriority(os.PRIO_PROCESS,0,10);parent_nice=os.getpriority(os.PRIO_PROCESS,0);assert parent_nice==10
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for scope measurement lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-scope-',dir=D)).resolve();T.chmod(0o700);env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
 for k in ['HOME','LANG','LC_ALL','TZ']:
  if k in os.environ:env[k]=os.environ[k]
 pins={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [B/'probe.py',B/'scope_codec.py']};workloads=json.loads((B/'inputs.json').read_text())['workloads'];results=[]
 for w in workloads:
  inp=B/(w['id']+'-input.json');packet=json.loads(inp.read_text());assert packet['heldOut']is False;actors=[];commitments=None
  for actor in ['host-a','host-b','worker-prototype']:
   runs=[];shape=None
   for n in range(10):
    out=B/f'{w["id"]}-{actor}-{n}.stdout';err=B/f'{w["id"]}-{actor}-{n}.stderr'
    with out.open('wb')as o,err.open('wb')as e:
     child=subprocess.Popen(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(B/'probe.py'),str(inp),actor],cwd=T,env=env,stdout=o,stderr=e);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
    assert child.returncode==0 and err.read_bytes()==b'',(w['id'],actor,n,err.read_text());row=json.loads(out.read_text());assert row['subjectCount']==w['subjectCount'];current={k:v for k,v in row.items()if k not in ['elapsedNanos','rssNative','rssBytes']};shape=current if shape is None else shape;assert current==shape;rss=int(usage.ru_maxrss);assert 0<=row['rssBytes']<=rss<2**64;runs.append(dict(ordinal=n,warmup=n<3,elapsedNanos=row['elapsedNanos'],observedChildNiceness=priority,childRssBytesBeforeSerialization=row['rssBytes'],exitCode=0,rssNative=rss,rssUnit='bytes',rssBytes=rss))
   shared={k:shape[k]for k in ['subjects','subjectScopeCommitment','domainCommitment','subjectsCborBytes','subjectsCborRawSha256']};commitments=shared if commitments is None else commitments;assert shared==commitments;values=[r['elapsedNanos']for r in runs if not r['warmup']];actors.append(dict(actor=actor,shape=shape,runs=runs,medianNanos=statistics.median(values),maxNanos=max(values),measuredPeakProcessRssBytes=max(r['rssBytes']for r in runs[3:])))
  results.append(dict(id=w['id'],heldOut=False,subjectCount=w['subjectCount'],actors=actors,threeActorArraysAndCommitmentsEqual=True));report=dict(standing='UNREVIEWED PRELIMINARY11DEVREADSETS330FRESH SCOPE REBUILD CHILDREN; SYNTHETIC MANIFEST/REQUEST DOMAIN,NO NATIVE WORKER',workloads=results,observedParentNiceness=parent_nice,nice=10,ownedTMPDIR=str(T),TMPDIRMode='0700',laneHeldForEntireSet=True,HOMEUnchanged=True,actualAcceptedTransportManifest=False,actualNativeWorker=False,coverageKeysValidatedC2Values=False,SM12FigureComplete=False,SM12PlaceholderFilled=False,SM14FigureComplete=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False);(B/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(w['id'],w['subjectCount'],'subjects;30 fresh child derivations agree',flush=True)
 assert pins=={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [B/'probe.py',B/'scope_codec.py']}
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
