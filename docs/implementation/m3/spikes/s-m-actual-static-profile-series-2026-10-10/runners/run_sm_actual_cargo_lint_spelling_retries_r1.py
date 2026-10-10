from pathlib import Path
import os,json,hashlib,sys,tempfile,time
B=Path('/tmp/opensip-implementation');V=B/'sm-command-data-2026-10-10';S=B/'sm-cargo-lint-spelling-controls-r1-stage';Q=B/'reviews/grok-sm-cargo-lint-spelling-controls-r1';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'actual-cargo-lint-spelling-retries-r1.json';assert not dest.exists();os.setpriority(os.PRIO_PROCESS,0,10)
state=json.loads((C/'CURRENT-STATE.json').read_bytes());publication=state['SMCargoLintSpellingControlsPublication'];review=json.loads((Q/'review.json').read_bytes());subject=hashlib.sha256((S/'subject.json').read_bytes()).hexdigest();assert review['verdict']=='ACCEPT' and review['requiredFindings']==[] and review['subjectManifestSha256']==publication['subjectManifest']['sha256']==subject;assert review['controlsPassed']==4 and review['compilerChildren']==3
source=json.loads((S/'source.json').read_bytes())
def check(row):
 raw=Path(row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];return raw
executor=source['executorSource'];wrapper=source['closedWrapperImage'];check(executor);check(wrapper);check(source['parentExecutorSource']);closed=json.loads((B/'sm-graph-metadata-controls-r1-stage/source.json').read_bytes());check(closed['closedWrapperSource'])
p=V/'actual-command-source-maps-r1.json';raw=p.read_bytes();prepared=json.loads(raw);assert len(prepared['results'])==9;check(prepared['dependencyDataReceipt']);root=Path(tempfile.mkdtemp(prefix='opensip-sm-actual-cargo-lint-retries-',dir=O));root.chmod(0o700);lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME');results=[]
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary experimental metadata lane',flush=True);time.sleep(5)
try:
 sys.path.insert(0,str(V));from cargo_lint_spelling_graph_execution import execute_graph
 for entry in prepared['results']:
  if entry['ordinal'] not in [0,2]:continue
  check(executor);check(entry['sourceMap']);graph=json.loads(check(entry['graph']));check(entry['packet']);check(entry['unitCommandData']);r=root/str(entry['ordinal']);r.mkdir(mode=0o700);started=time.monotonic_ns()
  try:
   result=execute_graph(graph,entry['sourceMap'],r/'graph',wrapper,closed['sysroot'],Path(entry['cwd']),entry['unitCommandData']);refusal=None
  except ValueError as e:
   assert not (r/'graph').exists();result=None;refusal=str(e)
  elapsed=time.monotonic_ns()-started
  item=dict(id=entry['id'],ordinal=entry['ordinal'],elapsedNanos=elapsed,preparedMap=entry['sourceMap'],graph=entry['graph'],unitCommandData=entry['unitCommandData'],result=result,executionRefusedBeforeLaunch=refusal,actualCorpusTypecheckAttempted=True,staticProfileCheckCfgArgumentsApplied=result is not None,operationalSourceOutputSearchExternBindingsReplaced=result is not None,constructedPackageEnvironmentCwdCapLintsUsed=result is not None,completeRuntimeCommand=False,fullCargoProfileEnvironment=False,nativeAdmission=False,physicalPeakScratchMeasured=False,completeStatisticalSet=False,SMComplete=False);results.append(item)
  report=dict(standing='NEW TWO ENTRY RETRIES USING ACCEPTED CARGO MANIFEST LINT SPELLING DATA; EARLIER REFUSALS RETAINED; NO FULL NATIVE OR S-M CLAIM',root=str(root),ownedLane=True,niceness=os.getpriority(os.PRIO_PROCESS,0),HOMEUnchanged=os.environ.get('HOME')==home,ownAcceptedExecutorSubject=subject,executorPin=executor,preparedMaps=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),results=results,totalCompilerChildren=sum(x['result']['compilerChildren'] for x in results if x['result'] is not None),completeRuntimeCommand=False,fullCargoProfileEnvironment=False,physicalPeakScratchMeasured=False,sourceAuthentication=False,nativeAdmission=False,completeStatisticalSet=False,SMComplete=False,effectiveL=False,productQualification=False);dest.write_text(json.dumps(report,indent=2)+'\n');print(dict(ordinal=entry['ordinal'],refusedBeforeLaunch=refusal,compilerChildren=None if result is None else result['compilerChildren']),flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
