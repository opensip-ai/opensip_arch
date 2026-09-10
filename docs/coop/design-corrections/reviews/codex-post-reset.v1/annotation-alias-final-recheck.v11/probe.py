from pathlib import Path
import copy,hashlib,importlib.util,json,shutil
from jsonschema import Draft202012Validator
root=Path.cwd();dc=root/'docs/coop/design-corrections';model=dc/'foundation/identity-model.py';raw=model.read_bytes();out=dc/'reviews/codex-post-reset.v1/annotation-alias-final-recheck.v11';assert not out.exists()
spec=importlib.util.spec_from_file_location('codex_annotation_alias_draft',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
a={'representation':'raw-artifact','retention':'not-joined','authority':'hypothetical-schema-probe','join':'Synthetic schema annotation-location control; not a runtime field or authority.'};rows=[]
for label,at_use,at_definition in [('unannotated-negative',False,False),('annotation-on-field-positive',True,False),('annotation-on-alias-definition-positive',False,True)]:
 d=copy.deepcopy(M.RELATION_DOCUMENT);d['$defs']['ProbeAlias']={'$ref':'#/$defs/DigestHex'};d['$defs']['FilePayloadV1']['properties']['stray']={'$ref':'#/$defs/ProbeAlias'}
 if at_use:d['$defs']['FilePayloadV1']['properties']['stray']['x-opensip-digest']=a
 if at_definition:d['$defs']['ProbeAlias']['x-opensip-digest']=a
 Draft202012Validator.check_schema(d);c=M.relation_digest_annotation_coverage(d)
 try:M.relation_annotation_closure('file',d);result={'admitted':True}
 except Exception as e:result={'admitted':False,'cause':str(e),'exception':type(e).__name__}
 rows.append({'id':label,'coverage':c['byRelation']['file'],'admission':result,'fieldSchema':d['$defs']['FilePayloadV1']['properties']['stray'],'aliasSchema':d['$defs']['ProbeAlias']})
assert model.read_bytes()==raw;out.mkdir();(out/'identity-model.final.py').write_bytes(raw);(out/'relation-schema.json').write_bytes((dc/'foundation/relation-payload-schemas.v2.json').read_bytes());shutil.copyfile(__file__,out/'probe.py');(out/'result.json').write_text(json.dumps({'standing':'Codex final-source schema/reference annotation-location recheck; not a Run or payload attack or independent acceptance. Tests helper claim that an annotation anywhere on path to governed leaf covers it.','modelSha256':hashlib.sha256(raw).hexdigest(),'sourceStableDuringExecution':True,'vectors':rows},indent=2)+'\n');print(json.dumps([{k:r[k] for k in ('id','coverage','admission')} for r in rows],indent=2))
