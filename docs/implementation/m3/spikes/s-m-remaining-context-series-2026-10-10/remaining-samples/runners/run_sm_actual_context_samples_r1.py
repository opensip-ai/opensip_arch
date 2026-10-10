from pathlib import Path
import json,statistics
B=Path('/tmp/opensip-implementation')
setup=(B/'run_sm_actual_context_typecheck_pilots_r1.py').read_text().split('while True:\n')[0]
setup=setup.replace('actual-context-typecheck-pilots-r1.json','actual-context-samples-r1.json').replace('opensip-sm-actual-context-pilots-','opensip-sm-actual-context-samples-')
exec(compile(setup,str(__file__),'exec'))
pilot=json.loads((V/'actual-context-typecheck-pilots-r1.json').read_bytes());series=[]
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for experimental sample lane',flush=True);time.sleep(5)
try:
 sys.path.insert(0,str(V));from context_graph_execution import execute_graph
 for entry,previous in zip(prepared['results'],pilot['results']):
  graph=json.loads(check(entry['graph']));samples=[];expected={u['index']:u['standing'] for u in previous['result']['unitResults']};r=root/str(entry['ordinal']);r.mkdir(mode=0o700)
  for ordinal in range(10):
   check(executor);check(wrapper);check(entry['sourceMap']);check(entry['unitContextData']);started=time.monotonic_ns();result=execute_graph(graph,entry['sourceMap'],r/str(ordinal),wrapper,closed['sysroot'],Path(entry['cwd']),entry['unitContextData']);elapsed=time.monotonic_ns()-started
   actual={u['index']:u['standing'] for u in result['unitResults']};success=actual==expected and result['compilerChildren']==previous['result']['compilerChildren']
   samples.append(dict(ordinal=ordinal,warmup=ordinal<3,wholeGraphNanos=elapsed,result=result,exactPilotUnitStandingPopulationRepeated=success));(V/'actual-context-samples-r1-progress.json').write_text(json.dumps(dict(completedSeries=series,currentEntry=entry['ordinal'],currentSamples=samples),indent=2)+'\n');print(dict(entry=entry['ordinal'],sample=ordinal,warmup=ordinal<3,compilerChildren=result['compilerChildren'],populationRepeated=success,wholeGraphNanos=elapsed),flush=True)
   if not success:raise RuntimeError('Incomplete population retained; no complete series inferred')
  measured=[s['wholeGraphNanos'] for s in samples if not s['warmup']];hashes={str(i):sorted({u['metadata']['sha256'] for sample in samples for u in sample['result']['unitResults'] if u['index']==i and u.get('metadata')}) for i,standing in expected.items() if standing=='analysis-and-metadata-completed'}
  series.append(dict(id=entry['id'],ordinal=entry['ordinal'],graph=entry['graph'],sourceMap=entry['sourceMap'],unitContextData=entry['unitContextData'],runs=samples,warmups=3,measuredSamples=7,compilerChildren=sum(s['result']['compilerChildren'] for s in samples),medianWholeGraphNanos=statistics.median(measured),maxWholeGraphNanos=max(measured),metadataHashSets=hashes,metadataByteHashesRepeatForEveryAnalyzedUnit=all(len(v)==1 for v in hashes.values()),allDeclaredRootsCompleted=False,eligibleUnitSeriesComplete=True,completeStatisticalSet=False))
 report=dict(standing='NEW ACTUAL THREE-WARM SEVEN-MEASURED AXUM TOKIO PARTIAL GRAPH ANALYSIS; UNREVIEWED AND NOT FULL S-M',root=str(root),series=series,totalGraphs=20,totalCompilerChildren=sum(s['compilerChildren'] for s in series),executorPin=executor,preparedMaps=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),ownAcceptedExecutorSubject=review['subjectManifestSha256'],ownedLaneForEntireSet=True,niceness=os.getpriority(os.PRIO_PROCESS,0),HOMEUnchanged=os.environ.get('HOME')==home,constructedPackageEnvironmentCwdCapLintsUsed=True,completeCompilerCommand=False,fullCargoProfileEnvironment=False,physicalPeakScratchMeasured=False,sourceAuthentication=False,nativeAdmission=False,completeStatisticalSet=False,SMComplete=False,effectiveL=False,productQualification=False);assert report['totalCompilerChildren']==480;dest.write_text(json.dumps(report,indent=2)+'\n');print('Two experimental sample series completed; full S-M remains false',flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
