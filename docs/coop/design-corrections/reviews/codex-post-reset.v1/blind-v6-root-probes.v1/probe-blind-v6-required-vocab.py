from pathlib import Path
import json,importlib.util,hashlib
root=Path('/Users/sb/code/opensip-ai/opensip_arch');snap=Path('/tmp/opensip-design-corrections/candidate-subject.v16');dc=snap/'docs/coop/design-corrections';out=root/'docs/coop/design-corrections/reviews/codex-post-reset.v1/blind-v6-root-probes.v1'
spec=importlib.util.spec_from_file_location('root_wf',dc/'workflows/workflows_model.v1.py');W=importlib.util.module_from_spec(spec);spec.loader.exec_module(W)
n=json.loads((dc/'native/native-evidence.schemas.v2.json').read_text());causes=n['$defs']['DeficiencyV2']['enum'];checks=[]
for cause in causes:
 req={'relation':'clones','minResolution':'normalized','completeness':'complete','satisfied':False,'deficiency':cause}
 try:W.validate_import_record('workflows/schemas/repair.schema.json','#/$defs/EvidenceRequirement',req);result='ADMITTED';detail=None
 except Exception as e:result='REFUSED';detail=str(e)
 checks.append({'cause':cause,'schemaResult':result,'detail':detail})
# The field under test is validated independently of relation-specific rung membership.
# Correct rung is selected from the registry for positive context; no native sufficiency execution claimed.
reg=json.loads((dc/'foundation/relation-payload-schemas.v2.json').read_text())['x-opensip-relation-registry']['relations'];rung=reg['clones']['ladder'][0]
for row in checks:
 req={'relation':'clones','minResolution':rung,'completeness':'complete','satisfied':False,'deficiency':row['cause']}
 try:W.validate_import_record('workflows/schemas/repair.schema.json','#/$defs/EvidenceRequirement',req);row['correctRungSchemaResult']='ADMITTED'
 except Exception as e:row['correctRungSchemaResult']='REFUSED';row['correctRungDetail']=str(e)
assert [r['cause'] for r in checks if r['correctRungSchemaResult']=='REFUSED']==[x for x in causes if x in {'derivation-policy-unmet','external-consumers-unknown','input-closure-incomplete','resolution-incomplete'}]
record={'standing':'Root independently validates all nine declared native causes at repair field boundary; schema-only evidence of vocabulary mismatch, no sufficiency/authorization/host execution claim. Initial generic normalized rung attempt preserved separately from registry-selected valid rung.','nativeCauseSourceSha256':hashlib.sha256((dc/'native/native-evidence.schemas.v2.json').read_bytes()).hexdigest(),'rungUsed':rung,'checks':checks}
p=out/'required-vocab.json';assert not p.exists();p.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
