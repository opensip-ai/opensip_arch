"""Prepare a pure selected-source design successor. Never alter product code."""
from pathlib import Path
import json,hashlib,copy,subprocess,shutil,collections
F=Path(__file__).parent;B=F/'source-design-r1';S=B/'architecture'
P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-native-owner-patterns-takeover';A=P.parent/'opensip_arch'
PRE='docs/implementation/m3/native-publication/native-owner-patterns-source-r1'
assert not B.exists()
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def write(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')
def git(root,*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=root,text=True).strip()
assert git(P,'status','--porcelain')=='' and not git(A,'diff','--name-only','HEAD')
L=json.loads((P/'design-lock.json').read_text());accepted={r['path']:r for r in L['inputs']}
for binding in L['contractSuccessors']:
 for row in json.loads((A/binding['record']['path']).read_text())['candidates']:accepted[row['path']]=row
def current_parent(product_path):
 row=pin(P,product_path);matches=[r for r in accepted.values() if r['sha256']==row['sha256'] and r.get('bytes')==row['bytes']]
 assert matches,product_path
 return matches[-1]
old_map=json.loads((P/'schemas/source-map.json').read_text());source_map=copy.deepcopy(old_map)
old_admission_map=json.loads((P/'schemas/admission-source-map.json').read_text());admission_map=copy.deepcopy(old_admission_map)
old_admission=json.loads((P/'schemas/admission-registry.json').read_text());admission=copy.deepcopy(old_admission)
old_registry=json.loads((P/'schemas/registry.json').read_text());registry=copy.deepcopy(old_registry)
old_closure=json.loads((P/'tools/contracts/generator-closure.json').read_text());closure=copy.deepcopy(old_closure)
changes={};parents=[current_parent('schemas/source-map.json'),current_parent('tools/contracts/generator-closure.json'),old_admission_map['registryArchitectureSource']]
for id,rel in [('urn:opensip:product-v1:native:evidence-schemas:v2','schemas/sources/native-v2.schema.json'),('opensip.product.relation-payload.2','schemas/sources/relation-payload-v2.schema.json')]:
 src=next(r for r in old_admission_map['sources'] if r['schemaId']==id);parents.append(src['architectureSource']);assert pin(A,src['architectureSource']['path'])==src['architectureSource']
 dst_rel=PRE+'/sources/'+Path(rel).name;dst=S/dst_rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/rel,dst)
 before=pin(P,rel);after=pin(S,dst_rel);assert before['sha256']!=after['sha256']
 changes[id]=dict(productPath=rel,parent=src['architectureSource'],before=before,source=after)
 for row in source_map['sources']:
  if row['schemaId']==id:row['architectureSource']=after
 for row in admission_map['sources']:
  if row['schemaId']==id:row['architectureSource']=after
 for row in admission['sources']:
  if row['schemaId']==id:row.update(bytes=after['bytes'],sha256=after['sha256'])
 for row in admission['aliases']:
  if row['schemaId']==id:row.update(bytes=after['bytes'],sha256=after['sha256'])
 for row in registry['sources']:
  if row['schemaId']==id:row['sourceSha256']=after['sha256']
write(S/(PRE+'/admission-registry.json'),admission)
admission_map['registryArchitectureSource']=pin(S,PRE+'/admission-registry.json')
write(S/(PRE+'/product/schemas/source-map.json'),source_map)
write(S/(PRE+'/product/schemas/admission-source-map.json'),admission_map)
for row in closure['files']:
 if row['path']=='schemas/source-map.json':
  current=pin(S,PRE+'/product/schemas/source-map.json');row.update(bytes=current['bytes'],sha256=current['sha256'])
 for c in changes.values():
  if row['path']==c['productPath']:row.update(bytes=c['source']['bytes'],sha256=c['source']['sha256'])
write(S/(PRE+'/product/tools/contracts/generator-closure.json'),closure)
closure_pin=pin(S,PRE+'/product/tools/contracts/generator-closure.json')
assert len(registry['recipes'])==1
recipe=registry['recipes'][0];recipe['generatorClosureSha256']=closure_pin['sha256']
replacements={c['before']['sha256']:c['source']['sha256'] for c in changes.values()}
recipe['sourceSha256s']=sorted(replacements.get(s,s) for s in recipe['sourceSha256s'])
write(S/(PRE+'/product/schemas/registry.json'),registry)
owner_path='docs/implementation/m1/source-selection-v2/owners/native/owner-pattern-successor.v1.json';parents.append(accepted[owner_path]);owner=json.loads((A/owner_path).read_text())
def differences(a,b,path=()):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  assert set(a)==set(b);return [q for k in a for q in differences(a[k],b[k],path+(k,))]
 if isinstance(a,list):
  assert len(a)==len(b);return [q for i in range(len(a)) for q in differences(a[i],b[i],path+(str(i),))]
 return [path] if a!=b else []
json_deltas=[]
for id,c in changes.items():
 old=json.loads((P/c['productPath']).read_text());new=json.loads((S/c['source']['path']).read_text());delta=differences(old,new)
 expected=[tuple(r['pointer'].removeprefix('#/').split('/')) for r in owner['schemaPatternRows'] if r['document']==id];assert sorted(delta)==sorted(expected)
 for row in owner['schemaPatternRows']:
  if row['document']!=id:continue
  at_old=old;at_new=new
  for part in row['pointer'].removeprefix('#/').split('/'):
   part=part.replace('~1','/').replace('~0','~');at_old=at_old[int(part)] if isinstance(at_old,list) else at_old[part];at_new=at_new[int(part)] if isinstance(at_new,list) else at_new[part]
  assert at_old==row['from'] and at_new==row['to']
 json_deltas.append(dict(schemaId=id,changedPatternValues=len(delta),allOtherJsonValuesEqual=True))
assert sum(r['changedPatternValues'] for r in json_deltas)==35
assert len(source_map['sources'])==len(old_map['sources'])==43 and len(admission['sources'])==len(old_admission['sources'])==52
assert len(admission['aliases'])==len(old_admission['aliases'])==15
assert all(a==b for a,b in zip(old_map['sources'],source_map['sources']) if a['schemaId'] not in changes)
assert all(a==b for a,b in zip(old_admission['sources'],admission['sources']) if a['schemaId'] not in changes)
assert all(a==b for a,b in zip(old_admission['aliases'],admission['aliases']) if a['schemaId'] not in changes)
assert old_closure.keys()==closure.keys() and all(old_closure[k]==closure[k] for k in closure if k!='files')
closure_changes=[a['path'] for a,b in zip(old_closure['files'],closure['files']) if a!=b];assert sorted(closure_changes)==sorted(['schemas/source-map.json']+[c['productPath'] for c in changes.values() if any(r['path']==c['productPath'] for r in old_closure['files'])])
assert all(a==b for a,b in zip(old_closure['files'],closure['files']) if a['path'].startswith('tools/contracts/python-packages/'))
metadata_product_map=[dict(productPath='schemas/source-map.json',candidate=pin(S,PRE+'/product/schemas/source-map.json')),dict(productPath='schemas/admission-source-map.json',candidate=pin(S,PRE+'/product/schemas/admission-source-map.json')),dict(productPath='schemas/admission-registry.json',candidate=pin(S,PRE+'/admission-registry.json')),dict(productPath='schemas/registry.json',candidate=pin(S,PRE+'/product/schemas/registry.json')),dict(productPath='tools/contracts/generator-closure.json',candidate=closure_pin)]
audit=dict(standing='PROPOSED PURE SELECTED-SOURCE DESIGN; NO PRODUCT/GENERATOR/BLIND EXECUTION',productBase=git(P,'rev-parse','HEAD'),architectureBase=git(A,'rev-parse','HEAD'),parentProductLock=pin(P,'design-lock.json'),sourceChanges=list(changes.values()),exactSelectedPatternRows=owner['schemaPatternRows'],recursiveComparisons=json_deltas,sourceSetCountUnchanged=43,admissionSourceCountUnchanged=52,aliasCountUnchanged=15,closureChangedRows=closure_changes,pythonPackageClosureRowsUnchanged=True,metadataProductMap=metadata_product_map,compiledPinUpdatesStillRequired=[dict(schemaId=id,productPath=c['productPath'],bytes=c['source']['bytes'],sha256=c['source']['sha256']) for id,c in changes.items()],scopedImplementationReviewSeparate=True,generatedOutputsNotClaimed=True,mandatoryBlindRefresh=True,productQualification=False)
write(S/(PRE+'/audit.json'),audit)
readme=S/(PRE+'/README.md');readme.write_text('''# Native-owner current-source selection r1

Proposed pure design selection; independent ACCEPT-DESIGN-UNIT and root assent required. It selects no product implementation and publishes no fresh blind margin.

This successor selects the bound source-selection-v3 native owner correction on the actual current merged native/common sources, preserving their later accepted fields. Exactly34 native and1 relation pattern value changes; all other JSON values, the43generator sources,52admission sources,15aliases, package/owner/namespace/profile/root sets and the exact existing toolchain remain unchanged. Source parents are immutable. Occupancy's raw document remains unchanged; its selected ECMA owner evaluation is a separately reviewed implementation obligation.

The frozen source/admission maps, registries, recipe and generator closure are the exact prospective metadata values for materialization. The generator closure changes only the native source row and the source-map row. The relation-payload source is admission-only, absent from the generator recipe/closure; no carrier namespace or generator source is added. AllPython-package rows and reference-loading code remain byte-equal. The source-design binding must precede selected offline generator execution. Product schema/evaluator changes, complete compiled pins and actual generated output drift need their own complete implementation review; no preliminary source preflight or this design acceptance substitutes for it.

After complete materialization acceptance/integration, immediately perform the mandatory B2-b4c3 sequence: exact-main pre-run review, one authorized unchanged-method/population/disclosure blind run in a clean detached worktree, ordinary write/check, independent post-run review and root assent before receipt commit. No D2b-3c or census-dependent lane consumes the changed reference closure before that sequence completes. On errors or changed rows, commit nothing from the refresh, disclose no content, tune or retry nothing, and report data through the standing owner protocol. Neither the old receipt nor source selection establishes a current held-out margin after materialization.

The separate scoped Program/evaluator proposal is unaccepted and not selected by this artifact. No new selector, source guard weakening, schema repair, source authority from a self-hash, production caller, owner choice, installation/private data access or product/platform/project qualification follows.
''')
candidate_paths=[str(p.relative_to(S)) for p in sorted((S/PRE).rglob('*')) if p.is_file()]
candidates=[pin(S,p) for p in candidate_paths]
parents=sorted({r['path']:r for r in parents}.values(),key=lambda r:r['path'])
for r in parents:assert accepted[r['path']]==r and pin(A,r['path'])==r
record_path=PRE+'/successor.json'
write(S/record_path,dict(schemaVersion=1,standing='PROPOSED selected-source design only; no code/receipt/qualification acceptance',parents=parents,candidates=candidates,passageOverrides=[]))
record=pin(S,record_path);manifest_path=PRE+'-subject.json';write(S/manifest_path,dict(schemaVersion=1,unit='NATIVE-OWNER-PATTERNS-SOURCE-r1',files=sorted(candidates+[record],key=lambda r:r['path'])))
prepared=dict(unit='NATIVE-OWNER-PATTERNS-SOURCE-r1',stage=str(S),subjectManifest=pin(S,manifest_path),record=record,parents=parents,prospectiveContractSuccessor=len(L['contractSuccessors'])+1,productBase=audit['productBase'],architectureBase=audit['architectureBase'],materializationCodeAccepted=False,generatorRun=False,blindRefreshComplete=False,productQualification=False)
write(B/'prepared.json',prepared);print(json.dumps(prepared,indent=2))
