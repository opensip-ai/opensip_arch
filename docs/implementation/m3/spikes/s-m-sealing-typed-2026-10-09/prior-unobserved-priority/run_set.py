from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib,statistics,sys
B=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';C=Path('/Users/sb/code/.opensip-implementation-cache');sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document;from store import verify
raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578';m=manifest_document(raw);entries={r['id']:r for r in m['repositories']};ids=sorted(set(m['counts']['tsjs']['medium']['devIds']+m['counts']['rust']['medium']['devIds']));assert len(ids)==12 and all(entries[i]['heldOut']is False for i in ids);overlay=next(w for w in m['workspaces']if w['id']=='mr-rs-medium-serde-json');assert overlay['heldOut']is False and all(entries[i]['heldOut']is False for i in overlay['memberIds'])
workloads=[dict(id=i,members=[dict(root=str(C/'t2-corpus-c8cc48e1/store'/entries[i]['treeDigest']['value']),prefix='',entry=i)])for i in ids];workloads.append(dict(id=overlay['id'],members=[dict(root=str(C/'t2-corpus-c8cc48e1/store'/entries[r['entry']]['treeDigest']['value']),prefix=r['mount']+'/',entry=r['entry'])for r in overlay['overlay']['members']],overlayDefinition=overlay['overlay'],overlayDigest=overlay['overlayDigest'],overlayConfigurationNotCaptured=True))
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for typed sealing measurement lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-seal-typed-',dir=D)).resolve();T.chmod(0o700);env=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T))
 for key in ['HOME','LANG','LC_ALL','TZ']:
  if key in os.environ:env[key]=os.environ[key]
 result=[]
 for w in workloads:
  proofs=[]
  for member in w['members']:proofs.append(dict(entry=member['entry'],treeVerified=verify(Path(member['root']),entries[member['entry']])))
  inp=B/(w['id']+'-input.json');inp.write_text(json.dumps(w,indent=2)+'\n');runs=[];shape=None
  for n in range(10):
   out=B/f'{w["id"]}-{n}.stdout';err=B/f'{w["id"]}-{n}.stderr'
   with out.open('wb')as o,err.open('wb')as e:
    child=subprocess.Popen(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(B/'probe.py'),str(inp)],cwd=T,env=env,stdout=o,stderr=e);_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
   assert child.returncode==0,(w['id'],n,err.read_text());r=json.loads(out.read_text());current={k:v for k,v in r.items()if k!='elapsedNanos'};shape=current if shape is None else shape;assert shape==current and r['registeredSnapshotPlanShapesPassed']is True and err.read_bytes()==b'';rss=int(usage.ru_maxrss);assert 0<=rss<2**64;runs.append(dict(ordinal=n,warmup=n<3,elapsedNanos=r['elapsedNanos'],exitCode=0,rssNative=rss,rssUnit='bytes',rssBytes=rss))
  values=[r['elapsedNanos']for r in runs if not r['warmup']];result.append(dict(id=w['id'],heldOut=False,shape=shape,verifiedMembers=proofs,runs=runs,medianNanos=statistics.median(values),maxNanos=max(values),overlayConfigurationNotCaptured=w.get('overlayConfigurationNotCaptured',False)));report=dict(standing='UNREVIEWED PRELIMINARY13PREPARED READSETS130SEALING CHILDREN; TYPED SYNTHETIC REFERENCES,OVERLAYCONFIG/DEPENDENCY/ADMISSION SCOPE OPEN',workloads=result,host='leadmacOSpreliminary,notD12',ownedTMPDIR=str(T),TMPDIRMode='0700',laneHeldForEntireSet=True,nice=10,HOMEUnchanged=True,dependencySourceSetsIncluded=False,snapshotPlanIdentitiesAdmitted=False,SM5FigureComplete=False,SM5PlaceholderFilled=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False);(B/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(w['id'],'typed equivalent sealing',statistics.median(values),'ns',shape['rows'],'rows',flush=True)
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
