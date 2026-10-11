from pathlib import Path
import os,json,hashlib,time,sys,stat,dataclasses,shutil
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-large-original-context-census-2026-10-10';S=B/'sm-original-rustflags-controls-r1-stage';Q=B/'reviews/grok-sm-original-rustflags-controls-r1';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');lane=O/'opensip-lanes.lock';dest=V/'actual-other-large-workspace-attempts-r10.json';assert not dest.exists()
st=json.loads((C/'CURRENT-STATE.json').read_bytes());publication=st['SMOriginalRustflagsControlsPublication'];review=json.loads((Q/'review.json').read_bytes());subject=hashlib.sha256((S/'subject.json').read_bytes()).hexdigest();assert review['verdict']=='ACCEPT' and review['requiredFindings']==[] and review['subjectManifestSha256']==publication['subjectManifest']['sha256']==subject and review['controlsPassed']==7 and review['nativeAdmission'] is False
source=json.loads((S/'source.json').read_bytes())
def checked(path,row):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
 with os.fdopen(fd,'rb') as f:
  a=os.fstat(f.fileno());assert stat.S_ISREG(a.st_mode);raw=f.read();z=os.fstat(f.fileno());assert (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];return raw
image=source['compiledCargoImage'];checked(Path(image['path']),image)
for row in source['finalSourcePins']:checked(Path(source['isolatedProducer'])/row['path'],row)
packet_path=V/'other-large-workspace-retry-packets-r10.json';packet_raw=packet_path.read_bytes();packets=json.loads(packet_raw);private=Path(packets['privateTMPDIR']);assert stat.S_IMODE(private.stat().st_mode)==0o700 and len(packets['packets'])==3 and len(packets['unavailableBeforeCollector'])==0
quality=Path('/Users/sb/code/opensip-ai/opensip/tools/quality');sys.path.insert(0,str(quality));from root_observation import observe_root
results=[];owned=False;initial_home=os.environ.get('HOME')
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary experiment lane',flush=True);time.sleep(5)
try:
 for entry in packets['packets']:
  if entry['id']=='rs-large-smithy-rs':continue
  packet=json.loads(checked(Path(entry['path']),entry));root=Path(entry['root']);assert not(root/'stdout.log').exists() and not(root/'stderr.log').exists();checked(Path(image['path']),image)
  for row in packet['registryFiles']:checked(root/'home/registry'/row['path'],row)
  assert not(root/'home/registry/src').exists()
  for row in packet['originalFiles']:checked(Path(packet['memberRoot'])/row['path'],row)
  env=dict(os.environ);env.update(TMPDIR=str(private),OPENSIP_EXPERIMENT_GRAPH_PACKET=entry['path']);assert env.get('HOME')==initial_home
  for key in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(key,None)
  env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
  argv=[image['path'],'util::context::experimental_command_data::collect_explicit_experimental_corpus_graph','--exact','--ignored','--nocapture'];stdout=os.open(root/'stdout.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);stderr=os.open(root/'stderr.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  try:observation=observe_root(argv,cwd=source['isolatedProducer'],environment=env,stdout_fd=stdout,stderr_fd=stderr,timeout_nanos=300_000_000_000)
  finally:os.close(stdout);os.close(stderr)
  for row in packet['originalFiles']:checked(Path(packet['memberRoot'])/row['path'],row)
  outcome=json.loads((root/'experiment-outcome.json').read_bytes()) if (root/'experiment-outcome.json').exists() else None
  record=dict(id=entry['id'],ordinal=entry['ordinal'],originalRelativeManifest=entry['originalRelativeManifest'],packet=entry,argv=argv,rootObservationInformational=dataclasses.asdict(observation),outcome=outcome,compilerInformationQueries=len(list((root/'queries').glob('query-*.arguments'))),originalBytePinsIndependentlyReobserved=True,fullWorkloadCoverage=False,typecheckExecuted=False,applicationExecuted=False,aliasExecuted=False,buildScriptOrProcMacroExecuted=False,sourceAuthentication=False,nativeAdmission=False,SMComplete=False)
  for name,key in [('unit-graph.json','graph'),('unit-command-data.json','unitCommandData')]:
   path=root/name
   if path.exists():
    raw=path.read_bytes();record[key]=dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    if key=='graph':
     graph=json.loads(raw);record['unitCount']=len(graph['units']);record['rootIndices']=graph['roots']
  lock=Path(packet['project'])/'Cargo.lock'
  if lock.exists():
   raw=lock.read_bytes();path=root/'experimental-lock-observation.txt';path.write_bytes(raw);record['lockObservation']=dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),originalLockPreserved=packet['preserveOriginalLock'],generatedExperimentalLock=not packet['preserveOriginalLock'])
  results.append(record);(V/'actual-other-large-workspace-attempts-r10-progress.json').write_text(json.dumps(results,indent=2)+'\n');print(dict(id=entry['id'],manifest=entry['originalRelativeManifest'],exitCode=observation.returncode,graphSuccess=None if outcome is None else outcome['success'],informationQueries=record['compilerInformationQueries']),flush=True)
 receipt=dict(standing='ACTUAL THREE NEW ORIGINAL DENO/SUI OFFLINE DEPENDENCY RETRY GRAPHS AFTER CHANGED PUBLIC REGISTRY INPUTS; EARLIER COMPLETED GRAPH AND UNRELATED COMPILER/GIT FAILURES RETAINED; UNREVIEWED; FULL WORKLOAD COVERAGE NOT INFERRED',ownAcceptedCollectorSubject=subject,compiledCollectorImage=image,inputPackets=dict(path=str(packet_path),bytes=len(packet_raw),sha256=hashlib.sha256(packet_raw).hexdigest()),results=results,unavailableBeforeCollector=[r for r in packets['unavailableBeforeCollector'] if r['id']!='rs-large-smithy-rs'],declaredWorkspaceEntries=8,unrelatedCompilerAndGitFailuresRetainedWithoutRetry=3,dependencyInputsChanged=True,previousAttempts=packets['previousAttempts'],actualCollectorRoots=len(results),unsupportedConfigurationHierarchies=0,successfulGraphs=sum(bool(r['outcome'] and r['outcome']['success']) for r in results),compilerInformationQueries=sum(r['compilerInformationQueries'] for r in results),privateTMPDIR=str(private),niceness=os.getpriority(os.PRIO_PROCESS,0),HOMEUnchanged=os.environ.get('HOME')==initial_home,ownedLane=True,originalBytePinsIndependentlyReobserved=True,fullWorkloadCoverage=False,typecheckExecuted=False,applicationExecuted=False,aliasExecuted=False,buildScriptOrProcMacroExecuted=False,fullCargoProfileEnvironment=False,sourceAuthentication=False,nativeAdmission=False,physicalPeakScratchMeasured=False,completeStatisticalSet=False,SMComplete=False,effectiveL=False,productQualification=False)
 dest.write_text(json.dumps(receipt,indent=2)+'\n');shutil.copyfile(dest,C/'continuation-preserved'/V.name/dest.name);shutil.copyfile(Path(__file__),C/'continuation-preserved'/Path(__file__).name);print('Original large workspace attempts complete; unavailable outcomes retained, no full S-M inference.',flush=True)
finally:
 if owned:lane.rmdir()
 assert os.environ.get('HOME')==initial_home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
