from pathlib import Path
import os,sys,json,time,hashlib,struct,stat,importlib.util
# U-2c SM-5 TWO-PART VARIANT (PLAN-r3 D-2, D-3): one timed span per child. Part 1 is the accepted typed sealing probe's
# span unchanged (s-m-sealing-typed-2026-10-09/probe.py: no-follow walk, typed snapshot2/plan2-equivalent identities from its
# control template). Part 2 follows in the same span: the entry's DependencySourceSetV1 members are read and SHA-256-hashed
# (no-follow, manifest order) against their file manifests, then every fileManifestSha256 and the set identity are computed
# with the reference model. A monotonic mark between the parts labels each. Shape checks follow the span.
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';TYPED=A/'docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09';sys.path.insert(0,str(P/'tools/contracts/python-packages'));from jsonschema import Draft202012Validator
model=A/'docs/coop/design-corrections/native/native_evidence_model.v2.py';ms=importlib.util.spec_from_file_location('native_model',model);M=importlib.util.module_from_spec(ms);ms.loader.exec_module(M)
spec=json.loads(Path(sys.argv[1]).read_text());control=json.loads((TYPED/'control-template.json').read_text());dep=spec['dependency'];desc=json.loads(Path(dep['descriptor']).read_text());plan_ds=[(p,json.loads(Path(p['manifest']).read_text()))for p in dep['packages']]
start=time.monotonic_ns();rows=[];excluded=[]
for member in spec['members']:
 root=Path(member['root']);prefix=member['prefix']
 for directory,dirs,files in os.walk(root,followlinks=False):
  for name in list(dirs):
   path=Path(directory)/name
   if path.is_symlink():excluded.append(dict(path=prefix+path.relative_to(root).as_posix(),kind='symlink-directory'));dirs.remove(name)
  for name in files:
   path=Path(directory)/name;metadata=path.lstat();relative=prefix+path.relative_to(root).as_posix()
   if not stat.S_ISREG(metadata.st_mode):excluded.append(dict(path=relative,kind='nonregular'));continue
   assert len(relative)<=4096 and '\\'not in relative and '\0'not in relative and all(0<len(s)<=255 and s not in ['.','..']for s in relative.split('/'));fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC);h=hashlib.sha256()
   with os.fdopen(fd,'rb')as source:
    before=os.fstat(source.fileno());assert(metadata.st_dev,metadata.st_ino)==(before.st_dev,before.st_ino)
    while chunk:=source.read(1048576):h.update(chunk)
    after=os.fstat(source.fileno());assert(before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
   rows.append(dict(path=relative,sha256=h.hexdigest(),bytes=before.st_size))
rows.sort(key=lambda r:r['path'].encode());excluded.sort(key=lambda r:r['path'].encode());assert len({r['path']for r in rows})==len(rows)
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def framed(domain,raw):return b'opensip.product.v1\0'+domain.encode()+b'\0'+struct.pack('>Q',len(raw))+raw
snapshot=dict(control['snapshot'],sourceInventory=rows);sr=canonical(snapshot);sid='snapshot2:'+hashlib.sha256(framed('snapshot',sr)).hexdigest();plan=dict(control['plan'],snapshotId=sid);pr=canonical(plan);pid='plan2:'+hashlib.sha256(framed('plan',pr)).hexdigest();mid=time.monotonic_ns()
files=0;total=0;fms=[]
for p,listing in plan_ds:
 seen={}
 for f in listing:
  path=Path(p['root'])/f['path'];metadata=path.lstat();assert stat.S_ISREG(metadata.st_mode);fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC);h=hashlib.sha256();n=0
  with os.fdopen(fd,'rb')as source:
   before=os.fstat(source.fileno());assert(metadata.st_dev,metadata.st_ino)==(before.st_dev,before.st_ino)
   while chunk:=source.read(1048576):h.update(chunk);n+=len(chunk)
   after=os.fstat(source.fileno());assert(before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
  assert h.hexdigest()==f['contentSha256'] and n==f['byteLength'];seen[f['path']]=dict(sha256=h.hexdigest(),byteLength=n);files+=1;total+=n
 fid=M.file_manifest_identity(seen);assert fid==p['fileManifestSha256'];fms.append(fid)
setid=M.dependency_source_set_identity(desc);end=time.monotonic_ns()
assert setid==dep['dependencySourceSetId'] and [p['fileManifestSha256']for p in desc['packages']]==[p['fileManifestSha256']for p,_ in plan_ds]
schema=json.loads((P/'schemas/sources/identity-v3.schema.json').read_text())
for kind,value in [('snapshot',snapshot),('plan',plan)]:Draft202012Validator(dict(schema,**{'$ref':'#/$defs/'+kind})).validate(value)
ns=json.loads((A/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text());Draft202012Validator(dict(ns,**{'$ref':'#/$defs/DependencySourceSetV1'})).validate(desc)
dr=canonical(desc)
print(json.dumps(dict(standing='UNREVIEWED U-2c SM-5 TWO-PART CHILD (D-2); TYPED SYNTHETIC REPOSITORY REFERENCES; NO ADMISSION',id=spec['id'],entry=spec['entry'],elapsedNanos=end-start,repositoryPartNanos=mid-start,dependencyPartNanos=end-mid,
 repository=dict(rows=len(rows),bytes=sum(r['bytes']for r in rows),inventoryCanonicalBytes=len(canonical(rows)),snapshotEquivalentDescriptorBytes=len(sr),planEquivalentDescriptorBytes=len(pr),snapshotEquivalentDigest=sid,planEquivalentDigest=pid,nonregularExcluded=excluded,inventorySha256=hashlib.sha256(canonical(rows)).hexdigest()),
 dependency=dict(packages=len(plan_ds),entries=files,bytes=total,descriptorCanonicalBytes=len(dr),descriptorFileBytes=Path(dep['descriptor']).stat().st_size,dependencySourceSetId=setid,fileManifestIdentities=len(fms)),
 registeredSnapshotPlanShapesPassed=True,dependencyDescriptorSchemaPassed=True,synthetic=True,snapshotPlanIdentitiesAdmitted=False,sourceAdmission=False,SM5PlaceholderFilled=False,SMComplete=False,effectiveL=False,productQualification=False),separators=(',',':')))
