from pathlib import Path
import json,hashlib,shutil,os,stat
W=Path('/Users/sb/code/opensip-ai/opensip-native-public');P=W.parent/'opensip';D=Path('/tmp/opensip-implementation/native-publication-r1');PRE='docs/implementation/m3/native-publication/native-common-materialization-r1'
def read(p):return json.loads(p.read_text())
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2)+'\n')
closure=read(W/'tools/contracts/generator-closure.json');missing=[]
for row in closure['files']:
 p=W/row['path']
 if p.exists():continue
 src=P/row['path'];assert row['path'].startswith(('tools/contracts/node_modules/','tools/contracts/python-packages/')),row['path'];st=src.lstat();assert stat.S_ISREG(st.st_mode);fd=os.open(src,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
 with os.fdopen(fd,'rb') as f:
  before=os.fstat(f.fileno());raw=f.read();after=os.fstat(f.fileno());assert (st.st_dev,st.st_ino)==(before.st_dev,before.st_ino);assert (before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);missing.append(row)
changed=[]
for row in closure['files']:
 raw=(W/row['path']).read_bytes();after=dict(path=row['path'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 if after!=row:changed.append(dict(before=dict(row),after=after))
 row.update(after)
allowed={'schemas/source-map.json','schemas/admission-source-map.json','tools/contracts/pipeline.py',*[f'schemas/sources/common-v{v}.schema.json' for v in [1,3,4]],'schemas/sources/native-v2.schema.json'}
assert {r['after']['path'] for r in changed}<=allowed;write(W/'tools/contracts/generator-closure.json',closure)
registry=read(W/'schemas/registry.json')
for row in registry['sources']:
 if row['sourcePath'] in allowed:row['sourceSha256']=hashlib.sha256((W/row['sourcePath']).read_bytes()).hexdigest()
registry['recipes'][0]['sourceSha256s']=sorted({row['sourceSha256'] for row in registry['sources']});registry['recipes'][0]['generatorClosureSha256']=hashlib.sha256((W/'tools/contracts/generator-closure.json').read_bytes()).hexdigest();write(W/'schemas/registry.json',registry)
write(D/'preparation.json',dict(standing='UNREVIEWED EXACT SELECTED NATIVE/COMMON MATERIALIZATION CANDIDATE; NOT CONSUMER ADMISSION',candidateWorktree=str(W),architectureStage=str(D/'architecture'),archive=PRE,changedSources=sorted(p for p in allowed if p.startswith('schemas/sources/')),addedNativeRouteRows=9,addedPublicDetailCodes=['native.closure-protocol-invalid','native.input-import-invalid'],NIJ1NullAlternativeMerged=True,DTMD1DigestAnnotationsMerged=True,HOMEOverrideRemoved=True,existingPinnedGeneratorDependenciesCopied=len(missing),generatorClosureChangedRows=changed,coreAuthentication=False,importAdmission=False,fullC2a=False,fullC3a=False,effectiveL=False,qualification=False))
print('Preserved source preparation; copied',len(missing),'missing exact pinned generation input files; re-pinned',len(changed),'selected input rows.')
