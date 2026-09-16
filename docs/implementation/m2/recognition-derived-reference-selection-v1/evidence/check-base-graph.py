from pathlib import Path
import importlib.util,json
B=Path('/tmp/opensip-implementation/m2-recognition-derived-fix-candidate-01')
F=B/'archroot/docs/coop/design-corrections/foundation'
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
G=load('derived_fix_graph',F/'evaluator_graph_fixture.v3.py')
I=load('derived_fix_identity',F/'identity-model.v3.py')
graph=G.build_file_inputs();run,objects,blobs,composed=G.seal_fixture(graph)
result=I.open_run_closure(run,objects,blobs)
runid=I.identifier('run',run)
assert runid=='run3:697e7fb028de4a95e807c7de6af264a8db158ef8b4e4f7fc7254cc7752cf244d'
r={'standing':'Proposed reference only; syntax fixture unchanged candidate Run','runId':runid,'objects':len(objects),'blobs':len(blobs),'fullStructuralReferencePassed':True,'completeReplayExecuted':False,'runtimeAccepted':False}
(B/'base-graph-result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
