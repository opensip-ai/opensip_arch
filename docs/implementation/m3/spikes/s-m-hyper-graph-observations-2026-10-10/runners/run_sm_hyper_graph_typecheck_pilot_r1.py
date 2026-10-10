from pathlib import Path
import os,json,hashlib,sys,tempfile,time
B=Path('/tmp/opensip-implementation');V=B/'sm-graph-typecheck-2026-10-10';S=B/'sm-graph-metadata-controls-r1-stage';Q=B/'reviews/grok-sm-graph-metadata-controls-r1';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');os.setpriority(os.PRIO_PROCESS,0,10);assert not(V/'hyper-graph-typecheck-pilot-r1.json').exists();st=json.loads((C/'CURRENT-STATE.json').read_bytes());publication=st['SMGraphMetadataControlsPublication'];review=json.loads((Q/'review.json').read_bytes());subject=hashlib.sha256((S/'subject.json').read_bytes()).hexdigest();assert subject==publication['subjectManifest']['sha256']==review['subjectManifestSha256']=='b8e6c28f66a1c53ee57e82a93bdeb75606a3fbfc542cb8fdf87217a215946588';assert review['verdict']=='ACCEPT' and review['requiredFindings']==[] and review['controlsPassed']==8
source=json.loads((S/'source.json').read_bytes())
def check(row):
 raw=Path(row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];return raw
for key in ['executorSource','closedWrapperSource','closedWrapperImage']:check(source[key])
prepared=json.loads((V/'hyper-source-map-preparation-r1.json').read_bytes());check(prepared['sourceMap']);graph=json.loads(check(prepared['graph']));root=Path(tempfile.mkdtemp(prefix='opensip-sm-hyper-typecheck-pilot-',dir=O));root.chmod(0o700);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME')
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary experimental metadata lane',flush=True);time.sleep(5)
try:
 sys.path.insert(0,str(V));from graph_execution import execute_graph
 started=time.monotonic_ns();result=execute_graph(graph,prepared['sourceMap'],root/'graph',source['closedWrapperImage'],source['sysroot'],root);elapsed=time.monotonic_ns()-started;report=dict(standing='ACTUAL SINGLE EXPERIMENTAL HYPER GRAPH TYPECHECK PILOT; NOT FULL NATIVE PROFILE OR S-M',root=str(root),elapsedNanos=elapsed,ownedLane=True,niceness=os.getpriority(os.PRIO_PROCESS,0),HOMEUnchanged=os.environ.get('HOME')==home,ownAcceptedExecutorSubject=subject,preparedMap=prepared['sourceMap'],graph=prepared['graph'],result=result,rootAnalysisCompleted=all(r['standing']=='analysis-and-metadata-completed' for r in result['rootResults']),actualCorpusTypecheckAttempted=True,completeStatisticalSet=False,fullCargoProfileEnvironment=False,sourceAuthentication=False,nativeAdmission=False,physicalPeakScratchMeasured=False,SMComplete=False,effectiveL=False,productQualification=False);(V/'hyper-graph-typecheck-pilot-r1.json').write_text(json.dumps(report,indent=2)+'\n');print({'compilerChildren':result['compilerChildren'],'rootAnalysisCompleted':report['rootAnalysisCompleted'],'elapsedNanos':elapsed,'fullCargoProfileEnvironment':False,'fullSM':False},flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
