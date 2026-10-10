from pathlib import Path
import os,json,hashlib,time,sys,stat,dataclasses
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';S=B/'sm-rust-dependency-preparation-r1-stage';Q=B/'reviews/grok-sm-rust-dependency-preparation-r1';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');lane=O/'opensip-lanes.lock'
os.setpriority(os.PRIO_PROCESS,0,10)
# Own new helper acceptance before actual corpus execution; no native permission inferred.
st=json.loads((C/'CURRENT-STATE.json').read_bytes());S=B/'sm-unit-context-controls-r1-stage';Q=B/'reviews/grok-sm-unit-context-controls-r1';publication=st['SMUnitContextControlsPublication'];review=json.loads((Q/'review.json').read_bytes());subject=hashlib.sha256((S/'subject.json').read_bytes()).hexdigest();assert review['verdict']=='ACCEPT' and review['requiredFindings']==[] and review['subjectManifestSha256']==subject==publication['subjectManifest']['sha256'];assert review['cargoControlsPassed']==4 and review['executorControlsPassed']==7 and review['nativeAdmission'] is False and review['firstUsePermissionGranted'] is False
source=json.loads((S/'source.json').read_bytes());image=Path(source['compiledCargoImage']['path'])
def checked(path,row):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  a=os.fstat(fd);assert stat.S_ISREG(a.st_mode)
  with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read()
  z=os.fstat(fd);assert(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 finally:os.close(fd)
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];return raw
checked(image,source['compiledCargoImage'])
for f in source['finalSourcePins']:checked(Path(source['isolatedProducer'])/f['path'],f)
packets=json.loads((D/'remaining-unit-context-packets-r1.json').read_bytes());private=Path(packets['privateTMPDIR']);assert stat.S_IMODE(private.stat().st_mode)==0o700
quality=Path('/Users/sb/code/opensip-ai/opensip/tools/quality');sys.path.insert(0,str(quality));from root_observation import observe_root
results=[];assert not (D/'remaining-unit-context-attempts-r1.json').exists();owned=False;initial_home=os.environ.get('HOME')
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary experiment lane',flush=True);time.sleep(5)
try:
 for entry in packets['packets']:
  packet=json.loads(checked(Path(entry['path']),entry));root=Path(entry['root']);assert not (root/'stdout.log').exists() and not (root/'stderr.log').exists()
  for f in packet['registryFiles']:checked(root/'home/registry'/f['path'],f)
  assert not(root/'home/registry/src').exists()
  env=dict(os.environ);env.update(TMPDIR=str(private),OPENSIP_EXPERIMENT_GRAPH_PACKET=entry['path']);assert env.get('HOME')==initial_home
  argv=[str(image),'util::context::experimental_unit_context::collect_explicit_experimental_corpus_graph','--exact','--ignored','--nocapture']
  stdout=os.open(root/'stdout.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);stderr=os.open(root/'stderr.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  try:observation=observe_root(argv,cwd=source['isolatedProducer'],environment=env,stdout_fd=stdout,stderr_fd=stderr,timeout_nanos=300_000_000_000)
  finally:os.close(stdout);os.close(stderr)
  outcome=json.loads((root/'experiment-outcome.json').read_bytes()) if (root/'experiment-outcome.json').exists() else None
  record=dict(id=entry['id'],ordinal=entry['ordinal'],packet=entry,argv=argv,rootObservationInformational=dataclasses.asdict(observation),outcome=outcome,compilerQueries=len(list((root/'queries').glob('query-*.arguments'))),completeStatisticalSet=False,typecheckExecuted=False,sourceAuthentication=False,nativeAdmission=False,SMComplete=False)
  graph=root/'unit-graph.json'
  if graph.exists():
   raw=graph.read_bytes();g=json.loads(raw);units=g['units'];assert g['version']==1
   blocked={i for i,u in enumerate(units) if 'custom-build' in u['target']['kind'] or 'proc-macro' in u['target']['kind']}
   while True:
    more={i for i,u in enumerate(units) if any(dep['index'] in blocked for dep in u['dependencies'])};new=blocked|more
    if new==blocked:break
    blocked=new
   record.update(graph=dict(path=str(graph),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),unitCount=len(units),rootIndices=g['roots'],expansionUnavailableUnitIndices=sorted(blocked),expansionUnavailableRootIndices=sorted(set(g['roots'])&blocked),otherUnitCount=len(units)-len(blocked),successfulTypecheckInferred=False)
  data=root/'unit-context-data.json'
  if data.exists():
   raw=data.read_bytes();record['unitContextData']=dict(path=str(data),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());record['constructedPackageEnvironmentCwdCapLintsCollected']=True;record['completeCompilerCommand']=False
  lock=Path(packet['project'])/'Cargo.lock'
  if lock.exists():
   data=lock.read_bytes();copy=root/'experimental-lock-observation.txt';copy.write_bytes(data);record['lockObservation']=dict(path=str(copy),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),originalLockPreserved=packet['preserveOriginalLock'],generatedExperimentalLock=not packet['preserveOriginalLock'])
  results.append(record);(D/'remaining-unit-context-attempts-r1-progress.json').write_text(json.dumps(results,indent=2)+'\n');print('Actual experimental graph attempt',entry['id'],entry['ordinal'],'rootExit',observation.returncode,'graphSuccess',None if outcome is None else outcome['success'],'queries',record['compilerQueries'],flush=True)
 finally_record=dict(standing='ACTUAL NEW UNIT-CONTEXT OFFLINE GRAPH PREPARATION FOR REMAINING SEVEN ORIGINAL ENTRIES; AXUM TOKIO RETAINED SEPARATELY; NOT TYPECHECK/FULLPROFILE/SM',results=results,originalManifestEntries=9,requiredWorkloads=8,actualManifestEntries=len(results),actualWorkloads=len({r['id'] for r in results}),otherOriginalEntriesRetained=True,constructedPackageEnvironmentCwdCapLintsCollected=True,actualDefaultCliTargetFilterUsed=True,completeCompilerCommand=False,fullCargoProfileEnvironment=False,successfulGraphs=sum(bool(r.get('outcome',{}).get('success')) for r in results if r.get('outcome')),compilerQueries=sum(r['compilerQueries'] for r in results),privateTMPDIR=str(private),niceness=os.getpriority(os.PRIO_PROCESS,0),HOMEUnchanged=os.environ.get('HOME')==initial_home,ownedLane=True,physicalRegistryPreparationBytes=packets['physicalRegistryCopyBytes'],nativeRSSInformationalDarwinBytes=True,physicalPeakScratchMeasured=False,completeStatisticalSet=False,sourceAuthentication=False,nativeAdmission=False,SMComplete=False,effectiveL=False,productQualification=False)
 (D/'remaining-unit-context-attempts-r1.json').write_text(json.dumps(finally_record,indent=2)+'\n');print('Actual supplemental offline graph attempts finished; complete S-M false',flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
