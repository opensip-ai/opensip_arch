from pathlib import Path
import os,sys,json,time,subprocess,tempfile,hashlib,statistics,datetime
B=Path(__file__).resolve().parent;C=Path('/Users/sb/code/.opensip-implementation-cache');A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=Path('/Users/sb/code/opensip-ai/opensip');PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document
from store import verify
DARWIN=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());LOCK=DARWIN/'opensip-lanes.lock';raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578';m=manifest_document(raw);entries={r['id']:r for r in m['repositories']};ids=sorted(set(m['counts']['tsjs']['medium']['devIds']+m['counts']['rust']['medium']['devIds']));assert all(not entries[i]['heldOut'] for i in ids);owned=False
while True:
 try:LOCK.mkdir();owned=True;break
 except FileExistsError:print('waiting for lane',flush=True);time.sleep(5)
try:
 ps=subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines();assert not [r for r in ps if r.split()[-1].rsplit('/',1)[-1] in ['cargo','rustc','clippy-driver']]
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-sealing-',dir=DARWIN));T.chmod(0o700);env=dict(os.environ,TMPDIR=str(T),CARGO_HOME='/Users/sb/.cargo',PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin');result=[]
 for id_ in ids:
  entry=entries[id_];root=C/'t2-corpus-c8cc48e1/store'/entry['treeDigest']['value'];verified=verify(root,entry);rows=[];shape=None
  for n in range(10):
   out=B/'evidence'/f'sealing-{id_}-{n}.stdout.json';err=B/'evidence'/f'sealing-{id_}-{n}.stderr'
   with out.open('wb') as o,err.open('wb') as e:
    child=subprocess.Popen(['/usr/bin/nice','-n','10',PY,'-I','-B',str(B/'probe/sealing.py'),str(root),id_],cwd=T,env=env,stdout=o,stderr=e);_,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
   assert child.returncode==0,(id_,n,err.read_text());observed=json.loads(out.read_text());current={k:v for k,v in observed.items() if k!='elapsedNanos'}
   if shape is None:shape=current
   else:assert current==shape,(id_,n,'sealing-drift')
   rows.append(dict(ordinal=n,warmup=n<3,elapsedNanos=observed['elapsedNanos'],ruMaxrssNative=int(usage.ru_maxrss),rssUnit='bytes',rssBytes=int(usage.ru_maxrss),exitCode=child.returncode,stdout=str(out),stderr=str(err)))
  measured=[r['elapsedNanos'] for r in rows if not r['warmup']];result.append(dict(id=id_,commit=entry['commit'],treeDigest=entry['treeDigest']['value'],contentDigest=entry['contentDigest']['value'],treeVerified=verified,heldOut=False,runs=rows,shape=shape,medianNanos=statistics.median(measured),maxNanos=max(measured)));print(id_,'rows',shape['regularInventoryRows'],'descriptor bytes',shape['snapshotEquivalentDescriptorBytes'],'median ns',statistics.median(measured),flush=True)
 report=dict(schemaVersion=1,standing='UNREVIEWED PRELIMINARY REPOSITORY-ONLY SEALING AND EQUIVALENT IDENTITY FRAMING; PARTIAL S-M',recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),host='lead-workstation',manifestSha256=hashlib.sha256(raw).hexdigest(),selection='union exact rust/tsjs medium dev lists; separate multi-repository overlay pending',workloads=result,TMPDIR=str(T),TMPDIRMode='0700',ownedLane=str(LOCK),laneHeldForEntireSet=True,nice=10,referenceRecordsSynthetic=True,dependencySourceSetsIncluded=False,nonregularSnapshotPolicySelected=False,snapshotPlanIdentitiesAdmitted=False,SM5PlaceholderFilled=False,SM6PlaceholderFilled=False,SMComplete=False,LG1Met=False,repositoryCodeExecuted=False,heldOutSourceInspected=False,Q6Qualification=False,effectiveL=False,productQualification=False)
 (B/'sealing-results.json').write_text(json.dumps(report,indent=2)+'\n');print('sealing batch complete',flush=True)
finally:
 if owned:LOCK.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
