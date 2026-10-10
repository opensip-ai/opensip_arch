from pathlib import Path
import os,json,hashlib,stat,tomllib
os.setpriority(os.PRIO_PROCESS,0,10)
D=Path('/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10');dest=D/'corpus-attempt-inputs-r1.json';assert not dest.exists()
o=json.loads((D/'owned-corpus-copies-r1.json').read_bytes());a=json.loads((D/'original-config-source-audit.json').read_bytes());roots={w['id']:w for w in o['workloads']}
def checked(path,row):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  before=os.fstat(fd);assert stat.S_ISREG(before.st_mode)
  with os.fdopen(fd,'rb',closefd=False) as f:b=f.read()
  after=os.fstat(fd);assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
 finally:os.close(fd)
 assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'];return b
plans=[]
for n,x in enumerate(a['inputs']):
 w=roots[x['id']];root=Path(w['ownedExperimentRoot']);relative=Path(x['manifest']).relative_to(Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-metadata-census-vvr1rulg')/x['id']);manifest=root/relative;inventory={r['path']:r for r in w['files']};mr=inventory[relative.as_posix()];parsed=tomllib.loads(checked(manifest,mr).decode('utf-8'));assert parsed.get('workspace')==x.get('rootManifestWorkspace')
 configs=[]
 for r in x['configs']:
  p=manifest.parent/r['path'];rel=p.relative_to(root).as_posix();raw=checked(p,inventory[rel]);configs.append(dict(path=str(p),bytes=inventory[rel]["bytes"],sha256=inventory[rel]["sha256"],originalAst=tomllib.loads(raw.decode('utf-8')),projection='Full TOML/CV parse, suppress exactly two observed target runner values; empty semantic projection',definitionRoot=str(p.parent.parent)))
 lock=manifest.parent/'Cargo.lock';lr=inventory.get(lock.relative_to(root).as_posix());assert bool(lr)==x['originalLockPresent']
 if lr:checked(lock,lr)
 links=[]
 if x['id']=='mr-rs-medium-serde-json':
  for name in ['serde','serde_core','serde_derive']:
   p=root/'rs-medium-serde'/name;rr=inventory[(p/'Cargo.toml').relative_to(root).as_posix()];t=tomllib.loads(checked(p/'Cargo.toml',rr).decode('utf-8'));assert t['package']['name']==name;links.append(dict(name=name,path=str(p),manifestPin=rr))
 plans.append(dict(ordinal=n,id=x['id'],originalMemberRoot=str(root),manifest=dict(path=str(manifest),bytes=mr['bytes'],sha256=mr['sha256']),manifestWorkspace=parsed.get('workspace'),configuration=configs,originalLock=None if not lr else dict(path=str(lock),bytes=lr['bytes'],sha256=lr['sha256']),lockMode='preserve-original-locked-offline' if lr else 'generate-separate-experimental-offline',overlayLinks=links,overlayAssociation='Two original workspaces; no synthetic root manifest; selected three path patches are experimental inputs, not original config' if links else None,packageSelection='Cargo Packages::Default for each original entry point; multi-repository has two retained entries',requestedTarget='aarch64-apple-darwin',features='original default features, no all-features shortcut',resolverExecuted=False))
result=dict(standing='UNREVIEWED NEXT EXPERIMENT INPUT ASSOCIATIONS; NO CORPUS RESOLVER RUN',requiredWorkloads=8,originalManifestEntries=9,originalLocks=1,missingOriginalLocks=8,plans=plans,registryIntake='Whole checked index/archive copies only. Omit expanded registry/src; fresh Cargo unpack from verified raw bytes. Supplied cache/index consistency is not native source authentication.',corpusResolutionRun=False,sourceAuthentication=False,nativeAdmission=False,SMComplete=False)
dest.write_text(json.dumps(result,indent=2)+'\n');print({'plans':len(plans),'originalLocks':1,'missingLocks':8,'corpusResolutionRun':False})
