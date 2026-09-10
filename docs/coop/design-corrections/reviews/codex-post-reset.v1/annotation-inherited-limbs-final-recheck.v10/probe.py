from pathlib import Path
import copy,hashlib,importlib.util,json,shutil
from jsonschema import Draft202012Validator
root=Path.cwd();dc=root/'docs/coop/design-corrections';model=dc/'foundation/identity-model.py';raw=model.read_bytes();out=dc/'reviews/codex-post-reset.v1/annotation-inherited-limbs-final-recheck.v10';assert not out.exists();spec=importlib.util.spec_from_file_location('codex_inherited_limbs',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M);rows=[]
for location in ('field','alias','branch'):
 for retention in ('preimage','invented-retention','not-joined'):
  d=copy.deepcopy(M.RELATION_DOCUMENT);d['$defs']['ProbeAlias']={'$ref':'#/$defs/DigestHex'};field={'$ref':'#/$defs/ProbeAlias'};annotation={'representation':'raw-artifact','retention':retention,'authority':'hypothetical-schema-probe','join':'Synthetic schema-only annotation-location control; no product field or authority.'}
  if location=='field':field['x-opensip-digest']=annotation
  elif location=='alias':d['$defs']['ProbeAlias']['x-opensip-digest']=annotation
  else:field={'oneOf':[{'type':'null'},{'$ref':'#/$defs/DigestHex','x-opensip-digest':annotation}]}
  d['$defs']['FilePayloadV1']['properties']['stray']=field;Draft202012Validator.check_schema(d)
  try:M.relation_annotation_closure('file',d);result={'admitted':True}
  except Exception as e:result={'admitted':False,'cause':str(e),'exception':type(e).__name__}
  rows.append({'id':location+'-'+retention,'location':location,'retention':retention,'coverage':M.relation_digest_annotation_coverage(d)['byRelation']['file'],'admission':result,'fieldSchema':field,'aliasSchema':d['$defs']['ProbeAlias']})
assert model.read_bytes()==raw;out.mkdir();(out/'identity-model.final.py').write_bytes(raw);(out/'relation-schema.json').write_bytes((dc/'foundation/relation-payload-schemas.v2.json').read_bytes());shutil.copyfile(__file__,out/'probe.py');(out/'result.json').write_text(json.dumps({'standing':'Codex final-source schema/reference inherited-annotation consistency recheck; not a current payload/Run attack or independent acceptance.','modelSha256':hashlib.sha256(raw).hexdigest(),'sourceStableDuringExecution':True,'probePreparationNote':'An initial exploratory command used system python3 and failed importing jsonschema before any model execution. This retained probe uses the required review environment and executes all cases.','vectors':rows},indent=2)+'\n');print(json.dumps([{k:r[k] for k in ('id','admission')} for r in rows],indent=2))
