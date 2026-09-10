from pathlib import Path
import json,hashlib,shutil,ast,copy
b=Path('/tmp/opensip-design-corrections');repo=Path('/Users/sb/code/opensip-ai/opensip_arch');out=b/'v19-combined-proposal.v1';out.mkdir(exist_ok=False);src=out/'work';frozen=b/'candidate-subject.v18';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
# Explicitly partial disposable source tree; excludes historical reviews, never claims complete frozen subject.
shutil.copytree(frozen,src,ignore=shutil.ignore_patterns('reviews','__pycache__'))
main=b/'v19-native-coauthor.v1';h=load(main/'handoff.json')
for row in h['changedFiles']:
 p=main/'work'/row['path'];assert sha(p)==row['v19Sha256'];q=src/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
co=b/'v19-consistency-coauthor.v1';h=load(co/'handoff.json');receipt=load(co/'response.json');assert not receipt['is_error'] and receipt['session_id']=='f8404b42-38fc-491c-973b-3c176e38278d'
for rel,dig in h['hashes']['before'].items():assert sha(src/rel)==dig
for rel,dig in h['hashes']['proposed'].items():assert sha(co/'proposed'/rel)==dig;shutil.copyfile(co/'proposed'/rel,src/rel)
repair=repo/'docs/coop/design-corrections/reviews/v19-repair-coauthor-clarification.v1/workflow.proposed.md';assert sha(repair)=='8d4d9c892c34ec991c8dd2ffc86946d267adc90adbc506422fbe3f01ccf66b1d';shutil.copyfile(repair,src/'docs/v2/contracts/product-v1/workflows-and-surfaces.md')
# Root-owned documentation corrections following coauthor Q2, plus exact error-code naming. No logic changes.
rel='docs/coop/design-corrections/native/native_evidence_model.v2.py';p=src/rel;before=p.read_text();s=before
edits=[('    no field, no count, no limit and no public route. A pure helper exception is not a public termination.','    no typed public scope projection. Its structured fields can identify the failing path and bound;\n    a generic schema exception is not the required public termination.'),('    spec - naming no field, no count and no limit. An oversized ORDINARY SELECTION is not a malformed record and','    spec - without the required typed public scope projection. Its structured fields identify the path and\n    bound. An oversized ORDINARY SELECTION is not a malformed record and'),('no `REQUEST.UNSATISFIABLE` class or exit,','no `REQUEST.UNSATISFIABLE` error code or request-rejected class/exit,'),('    fields across two record families now share the one law - workspaceRoots, pathPrefixes and\n    excludedPathPrefixes on the scope descriptor, and requestedCapabilities on the analysis spec. The published','    fields across these two record families share the law - workspaceRoots, pathPrefixes and\n    excludedPathPrefixes on the scope descriptor, and requestedCapabilities on the analysis spec. The three\n    Plan fields are additionally accounted by admit_plan_selection_cardinality. The published')]
for old,new in edits:assert s.count(old)==1,old;s=s.replace(old,new)
def no_docs(t):
 t=copy.deepcopy(t)
 for node in ast.walk(t):
  if isinstance(node,(ast.Module,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):node.body.pop(0)
 return ast.dump(t,include_attributes=False)
assert no_docs(ast.parse(s))==no_docs(ast.parse(before));p.write_text(s)
(out/'root-comment-corrections.json').write_text(json.dumps({'standing':'Root documentation-only cleanup of coauthor Q2 residue and public error-code label; after removing docstrings, entire native-model AST equals agreed consistency proposal. Fresh independent review will assess final exact bytes.','path':rel,'beforeSha256':hashlib.sha256(before.encode()).hexdigest(),'afterSha256':sha(p),'edits':[{'before':a,'after':z} for a,z in edits],'executableAstUnchanged':True},indent=2)+'\n')
(out/'standing.json').write_text(json.dumps({'standing':'Partial disposable composed source tree for root probes. NOT frozen candidate; historical reviews intentionally omitted. Workflow-subject coauthor completion and final six-command live pin seal still pending.','root':str(src)},indent=2)+'\n');print(src)
