from pathlib import Path
import json,hashlib,importlib.util
root=Path('/tmp/opensip-design-corrections/v20-combined-source.v1/work');dc=root/'docs/coop/design-corrections';out=Path('/tmp/opensip-design-corrections/codex-post-reset.v1/v20-scope-public-routes.v1');out.mkdir(exist_ok=False)
p=dc/'workflows/workflows_model.v1.py';s=importlib.util.spec_from_file_location('root_public_scope',p);W=importlib.util.module_from_spec(s);s.loader.exec_module(W)
a={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['src/**'],'exclude':[]};b={**a,'exclude':['src/generated/**']};doc=hashlib.sha256((dc/'workflows/schemas/policy-document.schema.json').read_bytes()).hexdigest();row={'schemaDigest':doc,'payloadDigest':W.doc_digest(a)}
results=[]
for name,params,scope in [('missing',[],a),('mismatch',[row],b),('valid',[row],a)]:
 r={'case':name}
 try:r['returnedDigest']=W.verify_scope_parameter_binding({'schemaVersion':2,'parameters':params},scope)
 except W.Refusal as exc:
  r['actualRefusal']={'errorCode':exc.error_code,'detail':exc.detail};term=exc.termination();r['actualTermination']=term
  try:W.validate_import_record('workflows/schemas/common.schema.json','#/$defs/StepTermination',term);r['carrier']='ADMITTED'
  except W.Refusal as ve:r['carrier']='REFUSED';r['carrierRefusal']=str(ve)
 results.append(r)
assert results[0]['actualRefusal']['detail']=='BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER' and results[0]['carrier']=='REFUSED'
assert results[1]['actualRefusal']['detail']=='BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH' and results[1]['carrier']=='REFUSED'
assert results[2]['returnedDigest']==row['payloadDigest']
d={'standing':'Root independent reproduction of actual direct binding Refusals projected through Refusal.termination and actual owning StepTermination validator. Not adopt_baseline/invocation/CommandEnvelope/product execution.','sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'results':results,'passed':True}
(out/'result.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
