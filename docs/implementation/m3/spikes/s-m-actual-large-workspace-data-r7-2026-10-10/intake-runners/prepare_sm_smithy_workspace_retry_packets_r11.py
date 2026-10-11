from pathlib import Path
import json,hashlib,os,stat,tempfile,subprocess,shutil
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-large-original-context-census-2026-10-10';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'smithy-workspace-retry-packets-r11.json';assert not dest.exists()
plan_path=V/'original-workspace-entries-r1.json';plan=json.loads(plan_path.read_bytes());copies=json.loads((V/'owned-corpus-copies-r1.json').read_bytes());sui=json.loads((B/'sm-sui-original-inputs-2026-10-10/owned-original-inputs-r1.json').read_bytes());index={r['id']:r['files'] for r in copies['workloads']};index[sui['id']]=sui['files'];template_path=V/'other-large-supplemental-registry-template-r12.json';template=json.loads(template_path.read_bytes());registry=Path(template['templateRoot'])
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def checked(path,row):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
 with os.fdopen(fd,'rb') as f:
  a=os.fstat(f.fileno());assert stat.S_ISREG(a.st_mode);h=hashlib.sha256();size=0
  while raw:=f.read(1048576):h.update(raw);size+=len(raw)
  z=os.fstat(f.fileno());assert (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 assert size==row['bytes'] and h.hexdigest()==row['sha256']
for row in template['files']:checked(registry/row['path'],row)
assert not(registry/'src').exists();print('Existing public registry template verified',len(template['files']),flush=True)
private=Path(tempfile.mkdtemp(prefix='opensip-sm-smithy-workspace-retry-r11-',dir=O));private.chmod(0o700);packets=[];unavailable=[]
prior_path=V/'actual-smithy-original-workspace-attempts-r10.json';prior=json.loads(prior_path.read_bytes());eligible={r['ordinal'] for r in prior['results'] if r['outcome'] and r['outcome']['error'] and ((r['outcome']['error'].startswith('no matching package named `') and 'location searched: crates.io index' in r['outcome']['error']) or r['outcome']['error'].startswith('failed to download `'))};assert eligible=={0,7,10};eligible={0,10}
for entry in plan['entries']:
 if entry['ordinal'] not in eligible:continue
 if len(entry['configurationHierarchyClosestFirst'])!=1:
  unavailable.append(dict(id=entry['id'],ordinal=entry['ordinal'],workspaceManifest=entry['workspaceManifest'],reason='Original multiple Cargo configuration hierarchy requires separately reviewed actual Cargo merge support; no original configuration dropped',collectorLaunched=False,configurationHierarchy=entry['configurationHierarchyClosestFirst']));continue
 root=private/str(entry['ordinal']);root.mkdir(mode=0o700);home=root/'home';home.mkdir(mode=0o700)
 subprocess.run(['/bin/cp','-cR',str(registry),str(home/'registry')],check=True)
 for row in template['files']:checked(home/'registry'/row['path'],row)
 assert not(home/'registry/src').exists()
 checked(Path(entry['workspaceManifest']['path']),entry['workspaceManifest']);config=entry['configurationHierarchyClosestFirst'][0];checked(Path(config['path']),config)
 original=index[entry['id']]
 for row in original:checked(Path(entry['originalMemberRoot'])/row['path'],row)
 packet=dict(schemaVersion=1,workload=entry['id'],manifestEntryOrdinal=entry['ordinal'],observationRoot=str(root),project=entry['project'],memberRoot=entry['originalMemberRoot'],originalFiles=original,configuration={k:config[k] for k in ['path','bytes','sha256']},overlayLinks=[],preserveOriginalConfiguration=True,preserveOriginalLock=entry['originalLock'] is not None,originalLock=entry['originalLock'],registryTemplateMetadata=pin(template_path),registryFiles=template['files'],originalConfigurationPolicy='Preserve one original configuration through reviewed Cargo CV/environment/original-rustflags DATA support; no actual helper use in this preparation',sourceAuthentication=False,nativeAdmission=False,SMComplete=False)
 p=root/'packet.json';p.write_text(json.dumps(packet,indent=2)+'\n');packets.append(dict(**pin(p),id=entry['id'],ordinal=entry['ordinal'],root=str(root),originalRelativeManifest=entry['originalRelativeManifest']))
 print('Prepared original workspace packet',entry['id'],entry['originalRelativeManifest'],flush=True)
receipt=dict(standing='NEW ORIGINAL SMITHY2 REGISTRY-INPUT-BLOCKED WORKSPACE RETRY PACKETS AFTER LOCK-DERIVED PUBLIC INTAKE r12; ORDINAL7 DEFERRED (mixed-case Inflector not admitted by closed intake); FOUR ORIGINAL LOCK UPDATE REFUSALS, LOCAL PACKAGE NAME MISMATCH AND GENERATED INPUT GAPS RETAINED WITHOUT RETRY; UNREVIEWED; NO COLLECTOR OR COMPILER RUN',privateTMPDIR=str(private),mode='0700',entryPlan=pin(plan_path),previousAttempts=pin(prior_path),dependencyInputsChanged=True,missingGeneratedInputsRetainedWithoutRetry=7,registryTemplateMetadata=pin(template_path),packets=packets,unavailableBeforeCollector=unavailable,originalWorkspaceEntries=33,preparedWorkspaceEntries=len(packets),unsupportedConfigurationHierarchies=len(unavailable),privateRegistryCopies=len(packets),logicalRegistryCopyBytes=len(packets)*template['bytes'],physicalCopyDiscountInferred=False,expandedRegistrySourcesCopied=False,collectorRoots=0,compilerChildren=0,originalFilesEdited=False,heldOutSourceOpened=False,fullWorkloadCoverage=False,sourceAuthentication=False,nativeAdmission=False,physicalPeakScratchMeasured=False,SMComplete=False)
dest.write_text(json.dumps(receipt,indent=2)+'\n');preserved=C/'continuation-preserved'/V.name;shutil.copyfile(dest,preserved/dest.name);shutil.copyfile(Path(__file__),C/'continuation-preserved'/Path(__file__).name);print(json.dumps(dict(prepared=len(packets),unsupportedHierarchies=len(unavailable),collectorRoots=0,SMComplete=False)));assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
