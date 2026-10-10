from pathlib import Path
import json,hashlib,copy
W=Path('/Users/sb/code/opensip-ai/opensip-native-public');A=W.parent/'opensip_arch';D=Path('/tmp/opensip-implementation/native-publication-r1');D.mkdir();PRE='docs/implementation/m3/native-publication/native-common-materialization-r1'
def read(p):return json.loads(p.read_text())
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2)+'\n')
def pin(p,path):
 b=p.read_bytes();return dict(path=path,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
p=W/'schemas/sources/native-v2.schema.json';base=read(p);new=copy.deepcopy(base)
nij=A/'docs/implementation/m3/snapshot-plan-c/nij-1-r1';c2pm=A/'docs/implementation/m3/snapshot-plan-c/c2pm-1-r2'
field='acquisitionSourcePath';old=new['$defs']['DependencySourcePayloadV1']['properties'][field];assert old==read(nij/'materialization-map.json')['schemaChange']['old'];new['$defs']['DependencySourcePayloadV1']['properties'][field]=read(nij/'materialization-map.json')['schemaChange']['new']
registry=new['x-opensip-public-route-registry']['keys'];oldkeys=copy.deepcopy(registry)
for unit,filename in [(c2pm,'closure-protocol-routes.json'),(nij,'native-import-routes.json')]:
 rows=read(unit/filename)['keys']
 for k,v in rows.items():
  assert k not in registry;registry[k]=v
assert len(registry)==len(oldkeys)+9 and all(registry[k]==v for k,v in oldkeys.items())
# Exact DT-MD1 selected annotations. Retain all other schema values.
record=read(A/'docs/implementation/m3/snapshot-plan-c/dependency-transport-digest-r1/successor.json')
overrides=record['passageOverrides']
for name in ['DependencySourceManifestV3','DependencySourceSealV3']:
 target=new['$defs'][name]['properties']['manifestSha256']['x-opensip-digest'];r=next(r for r in overrides if r['selector'].get('jsonPointer','').endswith('/'+name+'/properties/manifestSha256/x-opensip-digest/artifact'))
 assert target['artifact']==r['before'];target['artifact']=r['after']
write(p,new)
for version in [1,3,4]:
 p=W/f'schemas/sources/common-v{version}.schema.json';j=read(p);old=copy.deepcopy(j);en=j['$defs']['DomainDetailCode']['enum'];before=list(en)
 for code in ['native.closure-protocol-invalid','native.input-import-invalid']:
  assert code not in en;en.append(code)
 assert en[:-2]==before;write(p,j)
# The explicit user constraint forbids HOME overrides. Keep existing child
# deny-default profiles, roots, LANG/PATH/TZ and exact tools; omit HOME entirely.
p=W/'tools/contracts/pipeline.py';t=p.read_text();assert t.count("'HOME':str(home),")==1;t=t.replace("'HOME':str(home),",'');p.write_text(t)
sources=read(W/'schemas/source-map.json');admission=read(W/'schemas/admission-source-map.json')
changed=[f'schemas/sources/common-v{v}.schema.json' for v in [1,3,4]]+['schemas/sources/native-v2.schema.json']
for name in changed:
 artifact=PRE+'/sources/'+Path(name).name
 q=D/'architecture'/artifact;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((W/name).read_bytes());selection=pin(q,artifact)
 for mapping in [sources,admission]:
  rows=[r for r in mapping['sources'] if r['implementationPath']==name];assert len(rows)==1;rows[0]['architectureSource']=selection
write(W/'schemas/source-map.json',sources);write(W/'schemas/admission-source-map.json',admission)
# Re-pin only the changed source rows and exact source set in existing recipe.
r=read(W/'schemas/registry.json')
for row in r['sources']:
 if row['sourcePath'] in changed:row['sourceSha256']=hashlib.sha256((W/row['sourcePath']).read_bytes()).hexdigest()
r['recipes'][0]['sourceSha256s']=sorted({row['sourceSha256'] for row in r['sources']})
# Update existing complete generator input closure by value, leaving the toolchain.
closure=read(W/'tools/contracts/generator-closure.json');before_rows=copy.deepcopy(closure['files'])
for row in closure['files']:
 path=W/row['path'];raw=path.read_bytes();row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
assert [r['path'] for r in closure['files']]==[r['path'] for r in before_rows];write(W/'tools/contracts/generator-closure.json',closure)
r['recipes'][0]['generatorClosureSha256']=hashlib.sha256((W/'tools/contracts/generator-closure.json').read_bytes()).hexdigest();write(W/'schemas/registry.json',r)
write(D/'preparation.json',dict(standing='UNREVIEWED EXACT SELECTED NATIVE/COMMON MATERIALIZATION CANDIDATE; NOT CONSUMER ADMISSION',candidateWorktree=str(W),architectureStage=str(D/'architecture'),archive=PRE,changedSources=changed,addedNativeRouteRows=9,addedPublicDetailCodes=['native.closure-protocol-invalid','native.input-import-invalid'],NIJ1NullAlternativeMerged=True,DTMD1DigestAnnotationsMerged=True,HOMEOverrideRemoved=True,coreAuthentication=False,importAdmission=False,fullC2a=False,fullC3a=False,effectiveL=False,qualification=False))
print('Merged selected native/common source deltas; candidate only. Generation selection not bound.')
