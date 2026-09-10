from pathlib import Path
import json,hashlib,importlib.util,copy,shutil
from jsonschema import Draft202012Validator
r=Path.cwd();dc=r/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1/annotation-aggregation-final-recheck.v11';assert not out.exists();prior=dc/'reviews/digest-corrections-author.v9';h=json.loads((prior/'handoff.json').read_text());assert (prior/'custody.json').is_file()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for row in h['ownedFilesChanged']:assert sha(r/row['path'])==row['sha256']
src=dc/'foundation/identity-model.py';spec=importlib.util.spec_from_file_location('codex_v11_aggregation',src);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
ann={'representation':'raw-artifact','retention':'not-joined','reason':'Codex adaptation of actual independent p02/p03 schema-only construction; no runtime authority.'}
def leaf(annotated):
 d={'$ref':'#/$defs/DigestHex'}
 if annotated:d['x-opensip-digest']=copy.deepcopy(ann)
 return d
rows=[]
for case in ['container-unannotated-first','container-annotated-first','items-first','additionalProperties-first','both-container-sightings-annotated','both-array-map-sightings-annotated','single-unannotated','single-annotated']:
 d=copy.deepcopy(M.RELATION_DOCUMENT);props=d['$defs']['FilePayloadV1']['properties']
 if case.startswith('container-') or case=='both-container-sightings-annotated':
  first=case!='container-unannotated-first';second=case!='container-annotated-first'
  d['$defs']['ProbeContainer']={'type':'object','properties':{'leaf':leaf(first)}}
  props['probe']={'$ref':'#/$defs/ProbeContainer','properties':{'leaf':leaf(second)}}
 elif case in ['items-first','additionalProperties-first','both-array-map-sightings-annotated']:
  entries=[('items',leaf(case=='both-array-map-sightings-annotated')),('additionalProperties',leaf(True))]
  if case=='additionalProperties-first':entries.reverse()
  props['probe']=dict(entries)
 else:props['probe']=leaf(case=='single-annotated')
 Draft202012Validator.check_schema(d)
 try:M.relation_annotation_closure('file',d);result={'admitted':True}
 except Exception as exc:result={'admitted':False,'cause':str(exc),'exception':type(exc).__name__}
 positive=case.startswith('both-') or case=='single-annotated';passed=result['admitted'] if positive else 'RELATION_DIGEST_UNANNOTATED' in result.get('cause','')
 rows.append({'id':case,'expectedAdmit':positive,'result':result,'passed':passed})
out.mkdir();captures=[]
for row in h['ownedFilesChanged']:
 q=out/'source-delta'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(r/row['path'],q);captures.append(dict(row,capturedPath=str(q.relative_to(out))))
shutil.copyfile(__file__,out/'probe.py');result={'standing':'Codex final-source adaptation of actual independent v10 p02/p03; schema/reference guard evidence only, not a Run attack or independent acceptance.','baseManifestSha256':'82c1be11d3b61908b2a45ebb6e59e71bb5cb31d8450a96a61857ced430e786fd','sourceDelta':captures,'allVectorsMetaschemaValid':True,'vectors':rows,'passed':all(x['passed'] for x in rows)};(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');assert result['passed'],'Exact failed source/result retained; do not overwrite';print('Eight same-path/order and lawful controls pass on released source.')
