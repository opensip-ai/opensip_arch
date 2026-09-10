"""RE-RUN of ROOT's executed traversal counterexample against the CORRECTED source. NOT my construction.

Provenance: docs/coop/design-corrections/reviews/codex-post-reset.v1/annotation-traversal-draft-counterexample.v10/probe.py,
authored by Codex/root against the captured in-progress v7 model (identity-model.py sha256
f60657124060eb0078a9348498dc5f1b73f777ced8f0f99218989076ad5e44b3). Its four vectors and its
judgement are theirs and are not rewritten. Changes here are only those needed to re-ask the same
questions without writing into the repository: the output directory write and the source capture are
removed, and the model is loaded from the working tree. The original file and its result.json are
retained unaltered in the review directory.

Root's finding on the draft: vectors 2 and 3 were ADMITTED with coverage reporting nothing missing,
and vector 4 - the same two oneOf branches in the other order - refused. Expected now: the control
still admits and all three defect vectors refuse, with order making no difference.
"""
from pathlib import Path
import copy,hashlib,importlib.util,json,shutil
from jsonschema import Draft202012Validator
root=Path('/Users/sb/code/opensip-ai/opensip_arch');dc=root/'docs/coop/design-corrections';model=dc/'foundation/identity-model.py';schema=dc/'foundation/relation-payload-schemas.v2.json';raw=model.read_bytes();schemaraw=schema.read_bytes()
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
result={'standing':'actual Claude coauthor RE-RUN of a ROOT-authored counterexample against the CORRECTED source; construction is ROOT-authored; not a current payload attack, complete Run bypass or independent acceptance. Hypothetical schema documents are metaschema-valid.','baseManifestSha256':'288ac21453b635115b833935386ca5d65dbb6f482f51e078b118ffefb3ac1249','sourceImages':[{'path':str(model.relative_to(root)),'sha256':hashlib.sha256(raw).hexdigest(),'capture':'identity-model.draft.py'},{'path':str(schema.relative_to(root)),'sha256':hashlib.sha256(schemaraw).hexdigest(),'capture':'relation-schema.json'}],'sourceStableDuringExecution':True,'vectors':rows}
print(json.dumps([{k:r[k] for k in ('id','fileCoverage','admission')} for r in rows],indent=2))
