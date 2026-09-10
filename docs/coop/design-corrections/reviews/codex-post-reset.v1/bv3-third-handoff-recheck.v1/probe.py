from pathlib import Path
import ast,hashlib,json,shutil,importlib.util
base=Path('/tmp/opensip-design-corrections/bv3-corrections-author.v3/work');out=Path('/tmp/opensip-design-corrections/bv3-third-handoff-recheck.v1');assert json.loads((base.parent/'response.json').read_text()).get('is_error') is False;out.mkdir(exist_ok=False);root=out/'work';shutil.copytree(base,root)
dc=root/'docs/coop/design-corrections';source=dc/'foundation/check-identity.py';raw=source.read_text();tree=ast.parse(raw)
adapter=ast.parse(Path('/tmp/opensip-design-corrections/codex-post-reset.v1/adapt-integration-builder-v13.py').read_text());names=next(ast.literal_eval(n.value) for n in adapter.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='names' for t in n.targets));blocks=[];found=set()
for n in tree.body:
 declared={n.name} if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) else ({t.id for t in n.targets if isinstance(t,ast.Name)} if isinstance(n,ast.Assign) else set())
 if names&declared:blocks.append(ast.get_source_segment(raw,n));found|=names&declared
assert found==names
helper=dc/'integration-fixtures.py';helper.write_text('''import copy,hashlib,json,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent/'foundation'
spec=importlib.util.spec_from_file_location('development_identity',H/'identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
W=M.workflow_admission()
spec=importlib.util.spec_from_file_location('development_native',H.parent/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
NATIVE_FIXTURES=json.loads((H.parent/'native/native-cases.v2.json').read_text())['fixtures']
'''+ '\n\n'.join(blocks)+'\n')
spec=importlib.util.spec_from_file_location('development_fixture',helper);f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
rows=[]
for path,relation,has_match in [('README.md','file',True),('src/plain.rs','declares',True),('README.md','declares',True),('README.md','literal',True),('README.md','clones',False),('README.md','declares',False)]:
 row={'path':path,'relation':relation,'hasMatch':has_match}
 try:
  run,objects,blobs=f.build(resolved=False,has_match=has_match,universe_language='syntax',relation=relation,source_path=path)
  row['runId']=f.M.close_run(run,objects,blobs);row['verdict']='ADMIT'
  row['coveragePayloads']=[f.C.parse(blobs[v['payloadDigest']]) for d,v in objects.values() if d=='coverage']
 except Exception as exc:row.update(verdict='REFUSE',cause=type(exc).__name__+':'+str(exc))
 rows.append(row)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'standing':'Codex counterexample recheck on the completed released coauthor v3 source, exact source hashes retained. Synthetic author construction data, root-selected cases. Not released-source assent, parser execution, independent review or a pure compiler-free snapshot. Source inventory uses existing broad fixture; the observation concerns grammar/capability admission only.','sourceRoot':str(root),'sources':[{'path':str(p.relative_to(root)),'sha256':sha(p)} for p in [source,helper,dc/'foundation/identity-model.py',dc/'native/native_evidence_model.v2.py']],'cases':rows}
(out/'result.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py');print(json.dumps(rows,indent=2))
