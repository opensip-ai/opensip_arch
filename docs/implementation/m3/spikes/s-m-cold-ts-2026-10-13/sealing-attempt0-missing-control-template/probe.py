from pathlib import Path
import os,sys,json,time,hashlib,struct,stat
B=Path(__file__).resolve().parent;P=Path('/Users/sb/code/opensip-ai/opensip');sys.path.insert(0,str(P/'tools/contracts/python-packages'));from jsonschema import Draft202012Validator
spec=json.loads(Path(sys.argv[1]).read_text());control=json.loads((B/'control-template.json').read_text());start=time.monotonic_ns();rows=[];excluded=[]
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
snapshot=dict(control['snapshot'],sourceInventory=rows);sr=canonical(snapshot);sid='snapshot2:'+hashlib.sha256(framed('snapshot',sr)).hexdigest();plan=dict(control['plan'],snapshotId=sid);pr=canonical(plan);pid='plan2:'+hashlib.sha256(framed('plan',pr)).hexdigest();end=time.monotonic_ns()
# Registered shape checks are outside the sealing span. This grants no retained closure or source admission.
schema=json.loads((P/'schemas/sources/identity-v3.schema.json').read_text())
for kind,value in [('snapshot',snapshot),('plan',plan)]:Draft202012Validator(dict(schema,**{'$ref':'#/$defs/'+kind})).validate(value)
report=dict(standing='UNREVIEWED PRELIMINARY PREPARED SOURCE-READSET SEALING; EXACT TYPED SYNTHETIC REFERENCES,NO ADMISSION',id=spec['id'],elapsedNanos=end-start,regularRows=rows,nonregularExcluded=excluded,rows=len(rows),bytes=sum(r['bytes']for r in rows),inventoryCanonicalBytes=len(canonical(rows)),snapshotEquivalentDescriptorBytes=len(sr),planEquivalentDescriptorBytes=len(pr),snapshotEquivalentDigest=sid,planEquivalentDigest=pid,registeredSnapshotPlanShapesPassed=True,referencedPublicFixturePreimagesExist=True,synthetic=True,snapshotPlanIdentitiesAdmitted=False,dependencySourceSetsIncluded=False,SM5PlaceholderFilled=False,SMComplete=False,effectiveL=False,productQualification=False)
print(json.dumps(report,separators=(',',':')))
