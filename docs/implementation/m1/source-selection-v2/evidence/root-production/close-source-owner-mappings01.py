from pathlib import Path
import json,hashlib,types,shutil
A=Path('/Users/sb/code/opensip-ai/opensip_arch');D=A/'docs/implementation/m1/source-selection-v2';G=Path('/tmp/opensip-implementation/m1-joint-generation-candidate-03');W=Path('/tmp/opensip-implementation/m1-source-owner-closure-check-01');W.mkdir(exist_ok=False)
read=lambda p:json.loads(p.read_bytes())
rows=read(D/'source-map.json')['sources'];old=read(G/'inputs/options.json');options=dict(old);pending=options.pop('pendingSemanticSourceMappings');assert len(pending)==14
fields=['schemaId','declaredMajor','profile','semanticValidatorOwner'];options['sourceMappings']=sorted(({k:r[k] for k in fields} for r in rows),key=lambda r:r['schemaId']);options['standing']='Proposed exact source/semantic-owner allocation;14previously pending mappings resolved. Final independent source selection and product integration remain pending.'
options['openObligations']=['Exact final source-unit independent review and root acceptance','Product generation recipe/tooling/bootstrap/inventory binding','Fresh consumer and combined integration qualification','Product semantic owners and full release qualification']
(D/'generation-options.json').write_text(json.dumps(options,indent=2)+'\n');owners={r['schemaId']:r for r in options['owners']};mapped=[];sources={};documents={}
for r in rows:
 mapped.append(r|{'namespace':owners[r['schemaId']]['namespace'],'module':owners[r['schemaId']]['module'],'standing':'Proposed current or retained schema source; no semantic implementation claim'})
 raw=(A/r['architectureSource']['path']).read_bytes();doc=json.loads(raw);sr={k:r[k] for k in fields}|{'sourcePath':r['implementationPath'],'sourceSha256':hashlib.sha256(raw).hexdigest()};sources[r['schemaId']]=(sr,raw,doc);documents[r['schemaId']]=doc
mapping={'schemaVersion':1,'sources':mapped};(D/'generation-source-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
for src,dst in [('adapter.py','generator_adapter.py'),('prepare.py','prepare.py'),('runtime/schema.ts','runtime/schema.ts')]:
 p=D/'reference-tools'/dst;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(G/'tools/contracts'/src,p)
def load(p):m=types.ModuleType(p.stem);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
adapter=load(D/'reference-tools/generator_adapter.py');adapter.validate_options(options,sources);adapter.validate_source_map(mapping,sources,options)
try:adapter.validate_options(old,sources)
except ValueError as e:assert str(e)=='unsupported generator options';old_refusal=str(e)
else:raise AssertionError('unresolved14source mappings unexpectedly accepted')
prep=load(D/'reference-tools/prepare.py');prep.prepare(documents,options,W)
compared=[]
for name in ['rust-projection.json','ts-projection.json','owners.json','targets.json']:
 assert (W/name).read_bytes()==(G/'reproduction-g/prepared'/name).read_bytes(),name;compared.append(name)
receipt={'passed':True,'resolvedPendingMappings':len(pending),'closedSourceMappings':len(options['sourceMappings']),'selectedEntryPoints':len(options['entryPoints']),'originalPendingOptionsRefused':old_refusal,'unchangedPreparedFiles':compared,'meaning':'Semantic source ownership is now closed and coherent with40source map; prepared Rust/TS carrier inputs unchanged. Downstream Rust/generated algorithms not rerun or newly qualified.','sourceAccepted':False,'productModified':False}
(W/'result.json').write_text(json.dumps(receipt,indent=2)+'\n');(D/'owner-mapping-closure.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
