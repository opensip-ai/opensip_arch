from pathlib import Path
import os,sys,json,time,subprocess,tempfile,hashlib,statistics,datetime
B=Path(__file__).resolve().parent;C=Path('/Users/sb/code/.opensip-implementation-cache');A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=Path('/Users/sb/code/opensip-ai/opensip');sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document
from store import verify
TOOLS=C/'sm-tools-2026-10-09';NODE=TOOLS/'node/node-v24.21.0-darwin-arm64/bin/node';TS=TOOLS/'typescript/package/lib/typescript.js';DARWIN=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());LOCK=DARWIN/'opensip-lanes.lock';raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578';m=manifest_document(raw);entries={r['id']:r for r in m['repositories']};ids=m['counts']['tsjs']['medium']['devIds'];assert len(ids)==6 and all(not entries[i]['heldOut'] for i in ids);owned=False
while True:
 try:LOCK.mkdir();owned=True;break
 except FileExistsError:print('waiting for lane',flush=True);time.sleep(5)
try:
 ps=subprocess.check_output(['/bin/ps','-Ao','pid=,comm=']).decode().splitlines();assert not [r for r in ps if r.split()[-1].rsplit('/',1)[-1] in ['cargo','rustc','clippy-driver']]
 T=Path(tempfile.mkdtemp(prefix='opensip-sm-semantic-',dir=DARWIN));T.chmod(0o700);env=dict(os.environ,TMPDIR=str(T),CARGO_HOME='/Users/sb/.cargo',PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin');env.pop('RUSTC_BOOTSTRAP',None);result=[]
 for id_ in ids:
  entry=entries[id_];root=C/'t2-corpus-c8cc48e1/store'/entry['treeDigest']['value'];verified=verify(root,entry);print(id_,'offline tree/content verified',flush=True);rows=[];firstShape=None
  for n in range(10):
   out=B/'evidence'/f'{id_}-{n}.stdout.json';err=B/'evidence'/f'{id_}-{n}.stderr';start=time.monotonic_ns()
   with out.open('wb') as o,err.open('wb') as e:
    child=subprocess.Popen(['/usr/bin/nice','-n','10',str(NODE),'--no-addons',str(B/'probe/semantic.cjs'),str(TS),str(root)],cwd=T,env=env,stdout=o,stderr=e)
    _,status,usage=os.wait4(child.pid,0);child.returncode=os.waitstatus_to_exitcode(status)
   elapsed=time.monotonic_ns()-start
   try:observed=json.loads(out.read_text())
   except (ValueError,UnicodeError):observed=dict(standing='incomplete',reason='prototype-process-failed')
   shape={k:observed.get(k) for k in ['standing','reason','configuredFiles','programFiles','diagnosticCounts','diagnosticsCount','projectReferences','readPaths','blockedPaths']}
   if firstShape is None:firstShape=shape
   else:assert shape==firstShape,(id_,n,'semantic-shape-drift')
   row=dict(ordinal=n,warmup=n<3,elapsedNanos=elapsed,exitCode=child.returncode,ruMaxrssNative=int(usage.ru_maxrss),rssUnit='bytes',rssBytes=int(usage.ru_maxrss),stdout=str(out),stderr=str(err),standing=observed['standing'],maxPublicCompilerCall=observed.get('maxPublicCompilerCall'),instrumentedCompilerNanos=observed.get('totalInstrumentedNanos'));rows.append(row);print(id_,n,'elapsed ns',elapsed,'standing',observed['standing'],flush=True)
   if child.returncode!=0:break
  samples=[r for r in rows if not r['warmup']];completed=len(samples)==7
  result.append(dict(id=id_,commit=entry['commit'],treeDigest=entry['treeDigest']['value'],contentDigest=entry['contentDigest']['value'],heldOut=False,treeVerified=verified,runs=rows,semanticShape=firstShape,sevenSamples=completed,medianProcessNanos=statistics.median([r['elapsedNanos'] for r in samples]) if completed else None,maxProcessNanos=max((r['elapsedNanos'] for r in samples),default=None),maxObservedPublicCompilerCallNanos=max((r['maxPublicCompilerCall']['elapsedNanos'] for r in samples if r.get('maxPublicCompilerCall')),default=None),SM2PlaceholderFilled=False,SM8PlaceholderFilled=False,fullWorkspaceSemanticsClaimed=False))
  (B/'semantic-progress.json').write_text(json.dumps(dict(standing='UNREVIEWED PRELIMINARY PARTIAL S-M',workloads=result),indent=2)+'\n')
 report=dict(schemaVersion=1,standing='UNREVIEWED PRELIMINARY CONFIGURED ROOT SEMANTIC PASSES; NOT COMPLETE SM2/SM8',host='lead-workstation',recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),manifestSha256=hashlib.sha256(raw).hexdigest(),selection='exact counts.tsjs.medium.devIds, no held-out',TMPDIR=str(T),TMPDIRMode='0700',ownedLane=str(LOCK),laneHeldForEntireSet=True,nice=10,workloads=result,repositoryOnly=True,dependencyTreePinned=False,productionSelection=False,repositoryCodeExecuted=False,heldOutSourceInspected=False,macOSWholeTreeSettlementVerified=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False)
 (B/'semantic-results.json').write_text(json.dumps(report,indent=2)+'\n');print('semantic batch complete',flush=True)
finally:
 if owned:LOCK.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
