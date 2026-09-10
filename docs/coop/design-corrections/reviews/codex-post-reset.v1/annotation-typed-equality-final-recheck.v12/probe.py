from pathlib import Path
import copy,hashlib,importlib.util,json,shutil
from jsonschema import Draft202012Validator
r=Path.cwd();dc=r/'docs/coop/design-corrections';author=dc/'reviews/digest-corrections-author.v10';out=dc/'reviews/codex-post-reset.v1/annotation-typed-equality-final-recheck.v12';assert not out.exists();h=json.loads((author/'handoff.json').read_text());assert (author/'custody.json').is_file();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for row in h['ownedFilesChanged']:assert sha(r/row['path'])==row['sha256']
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=load(dc/'foundation/identity-model.py','codex_v12_typed_final');P=load(Path('/tmp/opensip-design-corrections/candidate-subject.v11/docs/coop/design-corrections/foundation/identity-model.py'),'codex_v11_typed_before')
pairs=[('integer-vs-boolean',1,True,False),('boolean-vs-integer',True,1,False),('nested-integer-vs-boolean',{'v':[1]},{'v':[True]},False),('same-integer',1,1,True),('same-boolean',True,True,True),('same-nested',{'v':[True]},{'v':[True]},True),('ordinary-string-conflict','one','two',False)]
def annotation(value):return {'representation':'raw-artifact','retention':'not-joined','authority':'Codex schema-only probe','ordinal':copy.deepcopy(value)}
def leaf(ann):return {'$ref':'#/$defs/DigestHex','x-opensip-digest':ann}
def document(shape,a,b):
 d=copy.deepcopy(M.RELATION_DOCUMENT);props=d['$defs']['FilePayloadV1']['properties']
 if shape=='property-alias':d['$defs']['ProbeAlias']=leaf(b);props['probe']={'$ref':'#/$defs/ProbeAlias','x-opensip-digest':a}
 elif shape=='parent-nullable-branch':props['probe']={'x-opensip-digest':a,'oneOf':[leaf(b),{'type':'null'}]}
 elif shape=='alias-chain':d['$defs']['ProbeA']={'$ref':'#/$defs/ProbeB','x-opensip-digest':a};d['$defs']['ProbeB']=leaf(b);props['probe']={'$ref':'#/$defs/ProbeA'}
 elif shape=='enclosing-container':props['probe']={'type':'object','x-opensip-digest':a,'properties':{'leaf':leaf(b)}}
 elif shape=='same-path-merge':d['$defs']['ProbeContainer']={'type':'object','properties':{'leaf':leaf(a)}};props['probe']={'$ref':'#/$defs/ProbeContainer','properties':{'leaf':leaf(b)}}
 else:raise AssertionError(shape)
 Draft202012Validator.check_schema(d);return d
def run(model,d):
 try:model.relation_annotation_closure('file',copy.deepcopy(d));return {'admitted':True}
 except Exception as e:return {'admitted':False,'cause':str(e),'exception':type(e).__name__}
rows=[]
for shape in ['property-alias','parent-nullable-branch','alias-chain','enclosing-container','same-path-merge']:
 for label,a,b,equal in pairs:
  d=document(shape,annotation(a),annotation(b));before=run(P,d);final=run(M,d);passed=final['admitted'] if equal else 'RELATION_DIGEST_ANNOTATION_CONFLICT' in final.get('cause','')
  rows.append({'id':shape+'/'+label,'expectedAdmit':equal,'pythonValuesEqual':a==b,'before':before,'final':final,'passed':passed})
out.mkdir();captured=[]
for row in h['ownedFilesChanged']:
 p=out/'source-delta'/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(r/row['path'],p);captured.append(dict(row,capturedPath=str(p.relative_to(out))))
shutil.copyfile(__file__,out/'probe.py');result={'standing':'Codex final-source variants of actual independent v11 p10 typed-equality counterexample. Hypothetical schema/reference evidence only, not a current payload/Run attack, independent acceptance or product qualification.','baseManifestSha256':'a03b7fe987ee886101a6d5b85bf4b0760f59b06a5a9e9c5f627accb9a7263bdf','allVectorsMetaschemaValid':True,'sourceDelta':captured,'vectors':rows,'discriminatingRefusals':sum(x['before']['admitted'] and not x['final']['admitted'] and not x['expectedAdmit'] for x in rows),'passed':all(x['passed'] for x in rows)};(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');assert result['passed'],'Exact failed result/source retained; do not overwrite';assert result['discriminatingRefusals']>0;print('35 typed annotation cases pass across five collection/inheritance/merge locations;',result['discriminatingRefusals'],'refusals discriminate frozen v11 from final source.')
