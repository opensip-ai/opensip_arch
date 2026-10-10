from pathlib import Path
import os,json,hashlib,sys,tempfile,time
B=Path('/tmp/opensip-implementation');V=B/'sm-cargo-unit-context-2026-10-10';BASE=B/'sm-graph-typecheck-2026-10-10';S=B/'sm-unit-context-controls-r1-stage';Q=B/'reviews/grok-sm-unit-context-controls-r1';O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'actual-context-typecheck-pilots-r1.json';assert not dest.exists();os.setpriority(os.PRIO_PROCESS,0,10)
subject=(S/'subject.json').read_bytes();manifest=json.loads(subject);review=json.loads((Q/'review.json').read_bytes());assert review['verdict']=='ACCEPT' and review['requiredFindings']==[] and review['subjectManifestSha256']==hashlib.sha256(subject).hexdigest()=='0c162537802e5507976f8948ca04c9fe3a476cb0ec7472e2da22554b34b06ff3'
def check(row):
 raw=Path(row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];return raw
executor=next(x for x in manifest['files'] if x['path']=='context_graph_execution.py');executor=dict(executor,path=str(V/executor['path']));check(executor)
closed=json.loads((B/'sm-graph-metadata-controls-r1-stage/source.json').read_bytes());wrapper=closed['closedWrapperImage'];check(wrapper);check(closed['closedWrapperSource'])
p=V/'actual-context-source-maps-r1.json';raw=p.read_bytes();prepared=json.loads(raw);assert len(prepared['results'])==2;check(prepared['dependencyDataReceipt'])
root=Path(tempfile.mkdtemp(prefix='opensip-sm-actual-context-pilots-',dir=O));root.chmod(0o700);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME');results=[]
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for experimental metadata lane',flush=True);time.sleep(5)
try:
 sys.path.insert(0,str(V));from context_graph_execution import execute_graph
 for entry in prepared['results']:
  check(executor);check(entry['sourceMap']);graph=json.loads(check(entry['graph']));check(entry['packet']);check(entry['unitContextData']);r=root/str(entry['ordinal']);r.mkdir(mode=0o700);started=time.monotonic_ns();result=execute_graph(graph,entry['sourceMap'],r/'graph',wrapper,closed['sysroot'],Path(entry['cwd']),entry['unitContextData']);elapsed=time.monotonic_ns()-started
  item=dict(id=entry['id'],ordinal=entry['ordinal'],elapsedNanos=elapsed,preparedMap=entry['sourceMap'],graph=entry['graph'],unitContextData=entry['unitContextData'],result=result,actualCorpusTypecheckAttempted=True,allDeclaredRootsCompleted=all(x['standing']=='analysis-and-metadata-completed' for x in result['rootResults']),constructedPackageEnvironmentCwdCapLintsUsed=True,completeCompilerCommand=False,fullCargoProfileEnvironment=False,primaryPackageMaterialized=False,realCargoOutputLayoutMaterialized=False,nativeAdmission=False,physicalPeakScratchMeasured=False,completeStatisticalSet=False,SMComplete=False);results.append(item)
  report=dict(standing='ACTUAL EXPERIMENTAL AXUM AND TOKIO GRAPH ANALYSIS WITH CHECKED CONSTRUCTED PACKAGE CONTEXT; UNREVIEWED; NO FULL NATIVE OR S-M CLAIM',root=str(root),ownedLane=True,niceness=os.getpriority(os.PRIO_PROCESS,0),HOMEUnchanged=os.environ.get('HOME')==home,ownAcceptedExecutorSubject=review['subjectManifestSha256'],executorPin=executor,preparedMaps=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),results=results,totalCompilerChildren=sum(x['result']['compilerChildren'] for x in results),fullCargoProfileEnvironment=False,completeCompilerCommand=False,physicalPeakScratchMeasured=False,sourceAuthentication=False,nativeAdmission=False,completeStatisticalSet=False,SMComplete=False,effectiveL=False,productQualification=False);dest.write_text(json.dumps(report,indent=2)+'\n');print(dict(ordinal=entry['ordinal'],compilerChildren=result['compilerChildren'],roots=[(x['index'],x['standing']) for x in result['rootResults']]),flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
