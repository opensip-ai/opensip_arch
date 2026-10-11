from pathlib import Path
import json,hashlib,os,stat,tempfile,subprocess,shutil
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-large-original-context-census-2026-10-10';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=V/'original-hierarchy-workspace-packets-r9.json';assert not dest.exists()
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
private=Path(tempfile.mkdtemp(prefix='opensip-sm-original-hierarchy-packets-r9-',dir=O));private.chmod(0o700);packets=[];unavailable=[]
prior_path=V/'actual-original-hierarchy-workspace-attempts-r8.json';prior=json.loads(prior_path.read_bytes());eligible={r['ordinal'] for r in prior['results'] if r['outcome'] and r['outcome']['error'] and 'location searched: crates.io index' in r['outcome']['error']};assert len(eligible)==7
for entry in plan['entries']:
 if entry['ordinal'] not in eligible:continue
 if len(entry['configurationHierarchyClosestFirst'])<=1:continue
 root=private/str(entry['ordinal']);root.mkdir(mode=0o700);home=root/'home';home.mkdir(mode=0o700)
 subprocess.run(['/bin/cp','-cR',str(registry),str(home/'registry')],check=True)
 for row in template['files']:checked(home/'registry'/row['path'],row)
 assert not(home/'registry/src').exists()
 checked(Path(entry['workspaceManifest']['path']),entry['workspaceManifest']);configurations=entry['configurationHierarchyClosestFirst'];
 for config in configurations:checked(Path(config['path']),config)
 original=index[entry['id']]
 for row in original:checked(Path(entry['originalMemberRoot'])/row['path'],row)
 packet=dict(schemaVersion=1,workload=entry['id'],manifestEntryOrdinal=entry['ordinal'],observationRoot=str(root),project=entry['project'],memberRoot=entry['originalMemberRoot'],originalFiles=original,configuration=None,configurationHierarchy=[{k:config[k] for k in ['path','bytes','sha256']} for config in configurations],overlayLinks=[],preserveOriginalConfiguration=True,preserveOriginalLock=entry['originalLock'] is not None,originalLock=entry['originalLock'],registryTemplateMetadata=pin(template_path),registryFiles=template['files'],originalConfigurationPolicy='Preserve all original closest-first ancestor configurations; exact accepted Cargo ConfigValue merge helper; no actual helper use in preparation',sourceAuthentication=False,nativeAdmission=False,SMComplete=False)
 p=root/'packet.json';p.write_text(json.dumps(packet,indent=2)+'\n');packets.append(dict(**pin(p),id=entry['id'],ordinal=entry['ordinal'],root=str(root),originalRelativeManifest=entry['originalRelativeManifest']))
 print('Prepared original workspace packet',entry['id'],entry['originalRelativeManifest'],flush=True)
receipt=dict(standing='NEW EXACT ORIGINAL SEVEN ANCESTOR CONFIGURATION DEPENDENCY RETRY PACKETS AFTER LOCK-DERIVED PUBLIC INTAKE r12; ORIGINAL RSPACK NIGHTLY FAILURE RETAINED; UNREVIEWED; NO COLLECTOR OR COMPILER RUN',privateTMPDIR=str(private),mode='0700',entryPlan=pin(plan_path),registryTemplateMetadata=pin(template_path),packets=packets,unavailableBeforeCollector=unavailable,originalWorkspaceEntries=33,preparedWorkspaceEntries=len(packets),unsupportedConfigurationHierarchies=len(unavailable),privateRegistryCopies=len(packets),logicalRegistryCopyBytes=len(packets)*template['bytes'],physicalCopyDiscountInferred=False,expandedRegistrySourcesCopied=False,collectorRoots=0,compilerChildren=0,originalFilesEdited=False,heldOutSourceOpened=False,fullWorkloadCoverage=False,sourceAuthentication=False,nativeAdmission=False,physicalPeakScratchMeasured=False,SMComplete=False)
dest.write_text(json.dumps(receipt,indent=2)+'\n');preserved=C/'continuation-preserved'/V.name;shutil.copyfile(dest,preserved/dest.name);shutil.copyfile(Path(__file__),C/'continuation-preserved'/Path(__file__).name);print(json.dumps(dict(prepared=len(packets),unsupportedHierarchies=len(unavailable),collectorRoots=0,SMComplete=False)));assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
