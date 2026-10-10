from pathlib import Path
import os,json,hashlib,sys,tempfile,time
B=Path('/tmp/opensip-implementation');V=B/'sm-framed-analysis-2026-10-10';CMD=B/'sm-command-data-2026-10-10';S=B/'sm-framed-analysis-controls-r1-stage';Q=B/'reviews/grok-sm-framed-analysis-controls-r1';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'actual-framed-analysis-pilots-r1.json'
assert not dest.exists();os.setpriority(os.PRIO_PROCESS,0,10)
def check(row):
 raw=Path(row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];return raw
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
state=json.loads((C/'CURRENT-STATE.json').read_bytes());publication=state['SMFramedAnalysisControlsPublication'];review=json.loads((Q/'review.json').read_bytes());subject=pin(S/'subject.json')['sha256'];assert review['verdict']=='ACCEPT' and review['requiredFindings']==[] and review['subjectManifestSha256']==publication['subjectManifest']['sha256']==subject
assert review['controlsPassed']==24 and review['childProcesses']==20 and review['historicalReportingFailureCompilerChildren']==1
source=json.loads((S/'source.json').read_bytes());wrapper=source['compiledImage'];check(wrapper);check(source['driverSource']);check(source['acceptedTimingParentSource']);check(source['rootObserverSource'])
executor=source['graphExecutorSource'];check(executor);closed=json.loads((B/'sm-graph-metadata-controls-r1-stage/source.json').read_bytes())
data_pub=state['SMActualStaticProfileSeriesPublication'];assert data_pub['subjectManifest']['sha256']==pin(B/'sm-actual-static-profile-series-r1-stage/subject.json')['sha256'] and data_pub['totalNewCompilerChildren']==1947
index=pin(CMD/'actual-command-source-maps-r1.json');prepared=json.loads(check(index));assert len(prepared['results'])==9;check(prepared['dependencyDataReceipt'])
initial=pin(CMD/'actual-lint-command-profile-pilots-r1.json');retry=pin(CMD/'actual-cargo-lint-spelling-retries-r1.json');previous={r['ordinal']:r for r in json.loads(check(initial))['results']};previous.update({r['ordinal']:r for r in json.loads(check(retry))['results']})
root=Path(tempfile.mkdtemp(prefix='opensip-sm-actual-framed-analysis-r1-',dir=O));root.chmod(0o700);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME');records=[]
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary analysis timing lane',flush=True);time.sleep(5)
try:
 check(dict(path=str(B/'audit_sm_analysis_prepared_reads_r1.py'),bytes=2415,sha256='687ca8eadde2abd5c5146c43000cd4584ea592e58551545fcc32406f806e8fb7'))
 sys.path.insert(0,str(B));from audit_sm_analysis_prepared_reads_r1 import audit
 sys.path.insert(0,str(V));from framed_profile_graph_execution import execute_graph
 for entry in prepared['results']:
  before=previous[entry['ordinal']];assert entry['graph']==before['graph'] and entry['unitCommandData']==before['unitCommandData'] and entry['sourceMap']==before['preparedMap'];graph=json.loads(check(entry['graph']));check(executor);check(wrapper)
  started=time.monotonic_ns();result=execute_graph(graph,entry['sourceMap'],root/str(entry['ordinal']),wrapper,closed['sysroot'],Path(entry['cwd']),entry['unitCommandData']);whole=time.monotonic_ns()-started
  expected={u['index']:(u['standing'],u.get('reason')) for u in before['result']['unitResults']};actual={u['index']:(u['standing'],u.get('reason')) for u in result['unitResults']};repeated=expected==actual and result['compilerChildren']==before['result']['compilerChildren'];observations=[]
  for u in result['unitResults']:
   if not u['compilerLaunched']:continue
   spans=[e for e in u['events'] if e['event']=='after_analysis'];assert len(spans)==1;ns=spans[0]['analysisElapsedNanos'];assert type(ns) is int and 0<ns<=u['observationInformational']['root_reaped_elapsed_nanos']
   wire=[e for e in u['events'] if e['event']=='prepared_map_wire_verified'];assert len(wire)==1 and wire[0]['mapSha256']==entry['sourceMap']['sha256'] and wire[0]['mapBytes']==entry['sourceMap']['bytes']
   obs=u['observationInformational'];assert 0<obs['worker_ready_elapsed_nanos']<obs['map_wire_verified_elapsed_nanos']<=obs['map_decode_complete_elapsed_nanos']<=obs['root_reaped_elapsed_nanos']
   reads=[e for e in u['events'] if e['event']=='prepared_source_read'];assert len(reads)==spans[0]['readCalls'] and all((e['preparedMapEntryPresent'] and type(e['contentBytes']) is int) or (not e['preparedMapEntryPresent'] and e['contentBytes'] is None) for e in reads)
   observations.append(dict(unitIndex=u['index'],analysisElapsedNanos=ns,preparedSourceReads=reads,informationalRSSNative=u['observationInformational']['rss_native'],sameChildTransportObservation=u['observationInformational']))
  records.append(dict(id=entry['id'],ordinal=entry['ordinal'],graph=entry['graph'],sourceMap=entry['sourceMap'],unitCommandData=entry['unitCommandData'],wholeGraphNanos=whole,result=result,analysisObservations=observations,preparedReadSetAudit=audit(entry['sourceMap'],result['unitResults']),exactAcceptedPilotPopulationRepeated=repeated))
  report=dict(standing='NEW ACTUAL SAME CHILD FRAMED MAP AND INSTRUMENTED ANALYSIS PILOTS; NOT FULL S-M',root=str(root),results=records,compilerChildren=sum(r['result']['compilerChildren'] for r in records),newCompilerChildrenLaunched=sum(r['result']['compilerChildren'] for r in records),deniedMappedSourceReadsRetained=True,wrapperPin=wrapper,executorPin=executor,preparedMaps=index,initialPilotReceipt=initial,twoEntryRetryReceipt=retry,acceptedFramedControlsSubject=subject,ownedLaneForEntireSet=True,niceness=os.getpriority(os.PRIO_PROCESS,0),mapDecodingExcludedFromAnalysisInterval=True,observerInstrumentationIncluded=True,metadataSysrootRuntimeReadsSealed=False,physicalPeakScratchMeasured=False,sourceAuthentication=False,nativeAdmission=False,completeStatisticalSet=False,SM4Complete=False,SMComplete=False,effectiveL=False,productQualification=False)
  dest.write_text(json.dumps(report,indent=2)+'\n');print(dict(entry=entry['ordinal'],compilerChildren=result['compilerChildren'],populationRepeated=repeated,analysisNanos=sum(x['analysisElapsedNanos'] for x in observations)),flush=True)
  if not repeated:raise RuntimeError('Changed population retained; complete pilot set not inferred')
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
