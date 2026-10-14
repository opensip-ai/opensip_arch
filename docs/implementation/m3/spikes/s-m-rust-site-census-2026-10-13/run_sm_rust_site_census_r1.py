from pathlib import Path
import os,json,hashlib,sys,tempfile,time
# S-M Rust site census r1 (M3-L r6 item 9, the S-M round's SM-13 decomposition input). Runs the site-walk variant of the
# closed framed driver through the UNCHANGED closed graph executor and observer over the nine accepted prepared entries
# of the framed analysis series, twice each (run 0 measures, run 1 checks that site counts are deterministic).
# Sites are compiler observations, not fact candidates. No timing statistic is claimed; no stage, key, emission factor,
# census kind or batching is chosen here.
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-framed-analysis-2026-10-10';CMD=B/'sm-command-data-2026-10-10';H=Path(__file__).resolve().parent;O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T')
A=Path('/Users/sb/code/opensip-ai/opensip_arch');SERIES=A/'docs/implementation/m3/spikes/s-m-actual-framed-analysis-series-2026-10-10'
dest=H/'site-census-r1.json';assert not dest.exists()
def pin(p):raw=Path(p).read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def check(row):assert pin(row['path'])==row,row['path'];return Path(row['path']).read_bytes()
build=json.loads((H/'producer/build.json').read_text());wrapper=dict(path=build['executable'],bytes=build['bytes'],sha256=build['sha256']);check(wrapper)
for k in ['driverSource','siteWalkSource','closedParentSource']:assert pin(build[k]['path'])==build[k]
assert build['closedParentSource']['sha256']=='43315ea6b81bd9b7a41174c1db41d50423b557ab6877be77db724ec96a7b75aa'
executor=pin(V/'framed_profile_graph_execution.py');assert executor['sha256']==pin(SERIES/'closed-graph-executor.py')['sha256']
observer=pin(V/'framed_root_observation.py');assert observer['sha256']==pin(SERIES/'closed-root-observer.py')['sha256']
closed=json.loads((B/'sm-graph-metadata-controls-r1-stage/source.json').read_bytes());index=pin(CMD/'actual-command-source-maps-r1.json');prepared=json.loads(check(index));assert len(prepared['results'])==9
accepted={r['ordinal']:{u['index']:(u['standing'],u.get('reason')) for u in r['result']['unitResults']} for r in json.loads((SERIES/'actual-framed-analysis-pilots-r1.json').read_bytes())['results']}
sys.path.insert(0,str(V));from framed_profile_graph_execution import execute_graph
lane=O/'opensip-lanes.lock';owned=False;home=os.environ.get('HOME');records=[]
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('waiting for lane',flush=True);time.sleep(5)
try:
 root=Path(tempfile.mkdtemp(prefix='opensip-sm-site-census-r1-',dir=O));root.chmod(0o700)
 for entry in prepared['results']:
  graph=json.loads(check(entry['graph']));runs=[]
  for n in range(2):
   check(wrapper);check(executor);check(observer)
   result=execute_graph(graph,entry['sourceMap'],root/f"{entry['ordinal']}-{n}",wrapper,closed['sysroot'],Path(entry['cwd']),entry['unitCommandData'])
   units=[]
   for u in result['unitResults']:
    row=dict(index=u['index'],packageId=graph['units'][u['index']]['pkg_id'],firstParty=graph['units'][u['index']]['pkg_id'].startswith('path+'),standing=u['standing'],reason=u.get('reason'),compilerLaunched=u['compilerLaunched'])
    if u['compilerLaunched']:
     walks=[e for e in u['events'] if e['event']=='site_walk'];spans=[e for e in u['events'] if e['event']=='after_analysis']
     row.update(siteWalkEvents=len(walks),afterAnalysisEvents=len(spans),siteWalk=walks[0] if walks else None,informationalRSSNative=u['observationInformational']['rss_native'])
    units.append(row)
   runs.append(dict(run=n,compilerChildren=result['compilerChildren'],units=units))
  population=[{u['index']:(u['standing'],u['reason']) for u in r['units']} for r in runs]
  strip=lambda r:[{k:v for k,v in (u['siteWalk'] or {}).items() if k!='walkElapsedNanos'} for u in r['units'] if u['compilerLaunched']]
  records.append(dict(id=entry['id'],ordinal=entry['ordinal'],cwd=entry['cwd'],graph=entry['graph'],sourceMap=entry['sourceMap'],runs=runs,acceptedPilotPopulationRepeated=all(p==accepted[entry['ordinal']] for p in population),siteCountsDeterministic=strip(runs[0])==strip(runs[1])))
  report=dict(standing='UNREVIEWED OUTSIDE-PRODUCT RUST SITE CENSUS (SM-13 DECOMPOSITION INPUT); SITES ARE NOT CANDIDATES',root=str(root),results=records,wrapperPin=wrapper,build=build,executorPin=executor,observerPin=observer,preparedMaps=index,
              compilerChildren=sum(r['compilerChildren'] for x in records for r in x['runs']),ownedLaneForEntireSet=True,niceness=os.getpriority(os.PRIO_PROCESS,0),timingStatisticClaimed=False,
              stageListChosen=False,requestedKeysChosen=False,emissionFactorsChosen=False,censusKindsChosen=False,batchingChosen=False,physicalPeakScratchMeasured=False,nativeAdmission=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False)
  dest.write_text(json.dumps(report,indent=1)+'\n');print(entry['ordinal'],entry['id'],records[-1]['acceptedPilotPopulationRepeated'],records[-1]['siteCountsDeterministic'],flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
