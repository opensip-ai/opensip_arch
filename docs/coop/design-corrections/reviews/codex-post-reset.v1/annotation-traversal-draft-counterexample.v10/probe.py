from pathlib import Path
import copy,hashlib,importlib.util,json,shutil
from jsonschema import Draft202012Validator
root=Path.cwd();dc=root/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1/annotation-traversal-draft-counterexample.v10';assert not out.exists();model=dc/'foundation/identity-model.py';schema=dc/'foundation/relation-payload-schemas.v2.json';raw=model.read_bytes();schemaraw=schema.read_bytes()
spec=importlib.util.spec_from_file_location('codex_draft_annotation',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
annotation={'representation':'raw-artifact','retention':'not-joined','authority':'hypothetical-schema-probe','join':'Synthetic schema-only annotation control; no runtime field or authority introduced.'}
base=M.RELATION_DOCUMENT;rows=[]
def run(label,doc):
 coverage=M.relation_digest_annotation_coverage(doc)
 try:M.relation_annotation_closure('file',doc);admission={'admitted':True}
 except Exception as e:admission={'admitted':False,'exception':type(e).__name__,'cause':str(e)}
 Draft202012Validator.check_schema(doc)
 row={'id':label,'fileCoverage':coverage['byRelation'].get('file'),'admission':admission,'syntheticFileSchema':doc['$defs']['FilePayloadV1']['properties'].get('stray'),'extraDefs':{k:v for k,v in doc['$defs'].items() if k.startswith('Probe')}};rows.append(row)
run('real-document-control',copy.deepcopy(base))
doc=copy.deepcopy(base);doc['$defs']['ProbeContainer']={'type':'object','properties':{'hidden':{'$ref':'#/$defs/DigestHex'}},'required':['hidden'],'additionalProperties':False};doc['$defs']['FilePayloadV1']['properties']['stray']={'$ref':'#/$defs/ProbeContainer'};run('unannotated-leaf-through-container-ref',doc)
doc=copy.deepcopy(base);uncovered={'$ref':'#/$defs/DigestHex','enum':['a'*64]};covered={'$ref':'#/$defs/CanonicalPath','enum':['src/a.rs'],'x-opensip-digest':annotation};doc['$defs']['FilePayloadV1']['properties']['stray']={'oneOf':[uncovered,covered]};run('unannotated-branch-before-annotated-branch',doc)
doc=copy.deepcopy(doc);doc['$defs']['FilePayloadV1']['properties']['stray']['oneOf'].reverse();run('same-unannotated-branch-after-annotated-branch',doc)
assert model.read_bytes()==raw and schema.read_bytes()==schemaraw,'Source changed during probe; do not claim stable capture'
out.mkdir();(out/'identity-model.draft.py').write_bytes(raw);(out/'relation-schema.json').write_bytes(schemaraw);shutil.copyfile(__file__,out/'probe.py')
result={'standing':'Codex captured in-progress v7 schema/reference traversal counterexample, not a current payload attack, complete Run bypass or independent acceptance. Hypothetical schema documents are metaschema-valid.','baseManifestSha256':'288ac21453b635115b833935386ca5d65dbb6f482f51e078b118ffefb3ac1249','sourceImages':[{'path':str(model.relative_to(root)),'sha256':hashlib.sha256(raw).hexdigest(),'capture':'identity-model.draft.py'},{'path':str(schema.relative_to(root)),'sha256':hashlib.sha256(schemaraw).hexdigest(),'capture':'relation-schema.json'}],'sourceStableDuringExecution':True,'vectors':rows}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps([{k:r[k] for k in ('id','fileCoverage','admission')} for r in rows],indent=2))
