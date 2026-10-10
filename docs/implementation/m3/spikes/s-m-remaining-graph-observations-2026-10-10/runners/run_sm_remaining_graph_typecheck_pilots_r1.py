from pathlib import Path
import os,json,hashlib,sys,tempfile,time
B=Path('/tmp/opensip-implementation');V=B/'sm-graph-typecheck-2026-10-10';S=B/'sm-graph-metadata-controls-r1-stage';Q=B/'reviews/grok-sm-graph-metadata-controls-r1';O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'remaining-graph-typecheck-pilots-r1.json';assert not dest.exists();os.setpriority(os.PRIO_PROCESS,0,10)
review=json.loads((Q/'review.json').read_bytes());subject=hashlib.sha256((S/'subject.json').read_bytes()).hexdigest();assert subject==review['subjectManifestSha256']=='b8e6c28f66a1c53ee57e82a93bdeb75606a3fbfc542cb8fdf87217a215946588' and review['verdict']=='ACCEPT' and review['requiredFindings']==[]
source=json.loads((S/'source.json').read_bytes())
def check(row):
 raw=Path(row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];return raw
for key in ['executorSource','closedWrapperSource','closedWrapperImage']:check(source[key])
p=V/'remaining-graph-source-maps-r1.json';raw=p.read_bytes();prepared=json.loads(raw);assert len(prepared['results'])==6;check(prepared['dependencyDataReceipt'])
root=Path(tempfile.mkdtemp(prefix='opensip-sm-remaining-graph-pilots-',dir=O));root.chmod(0o700);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME');results=[]
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for experimental metadata lane',flush=True);time.sleep(5)
try:
 sys.path.insert(0,str(V));from graph_execution import execute_graph
 for entry in prepared['results']:
  check(source['executorSource']);check(entry['sourceMap']);graph=json.loads(check(entry['graph']));check(entry['packet']);r=root/str(entry['ordinal']);r.mkdir(mode=0o700);started=time.monotonic_ns();result=execute_graph(graph,entry['sourceMap'],r/'graph',source['closedWrapperImage'],source['sysroot'],Path(entry['cwd']));elapsed=time.monotonic_ns()-started
  item=dict(id=entry['id'],ordinal=entry['ordinal'],elapsedNanos=elapsed,preparedMap=entry['sourceMap'],graph=entry['graph'],cwd=entry['cwd'],result=result,actualCorpusTypecheckAttempted=True,allDeclaredRootsCompleted=all(x['standing']=='analysis-and-metadata-completed' for x in result['rootResults']),fullCargoProfileEnvironment=False,actualPerPackageCargoCwdMaterialized=False,nativeAdmission=False,physicalPeakScratchMeasured=False,completeStatisticalSet=False,SMComplete=False);results.append(item)
  report=dict(standing='ACTUAL EXPERIMENTAL ADDITIONAL GRAPH TYPECHECK PILOTS; UNREVIEWED; NO FULL NATIVE OR S-M CLAIM',root=str(root),ownedLane=True,niceness=os.getpriority(os.PRIO_PROCESS,0),HOMEUnchanged=os.environ.get('HOME')==home,ownAcceptedExecutorSubject=subject,preparedMaps=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),results=results,totalCompilerChildren=sum(x['result']['compilerChildren'] for x in results),fullCargoProfileEnvironment=False,physicalPeakScratchMeasured=False,sourceAuthentication=False,nativeAdmission=False,completeStatisticalSet=False,SMComplete=False,effectiveL=False,productQualification=False);dest.write_text(json.dumps(report,indent=2)+'\n');print(dict(ordinal=entry['ordinal'],compilerChildren=result['compilerChildren'],roots=[(x['index'],x['standing']) for x in result['rootResults']]),flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
