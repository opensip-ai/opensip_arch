from pathlib import Path
import json,hashlib,importlib.util,ast,sys,base64
P=Path(__file__).parent
mp=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v19.json')
assert hashlib.sha256(mp.read_bytes()).hexdigest()=='312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b'
base=Path(json.loads(mp.read_text())['snapshotRoot'])/'docs/coop/design-corrections'
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=module('root_identity',base/'foundation/identity-model.py');W=module('root_workflow',base/'workflows/workflows_model.v1.py');N=module('root_native',base/'native/native_evidence_model.v2.py')
ns={'__name__':'root_captured_blind_gaps','__file__':str(P/'work/t_gaps.py')};results=[]
def audit_report(*args,**kw):
 ns['report'](*args,**kw);idc=args[0];row={'id':idc}
 try:
  if idc=='CB-GAP-2':
   spec=ns['spec'];N.admit_analysis_spec(spec);row.update(result='ANALYSIS_SPEC_ADMITTED',spec=spec)
  else:
   fx=ns['fx'];rid=ns['run_id'] if idc=='CB-GAP-1' else ns['new_run'];osip=ns['osip'];objects={}
   for h,b in fx.s.blobs.items():
    assert hashlib.sha256(b).hexdigest()==h
    if b.startswith(osip.FRAME_PREFIX+b'\0'):
     dom,desc=osip.parse_frame(b)
     if dom in M.PREFIX:objects[M.PREFIX[dom]+':'+h]=(dom,desc)
   row.update(runId=rid,result='CLOSURE_ADMITTED',admittedRunId=M.close_run(objects[rid][1],objects,fx.s.blobs))
   (P/(idc+'-root-computed-graph.json')).write_text(json.dumps({'runId':rid,'objects':objects,'blobs':{h:base64.b64encode(b).decode() for h,b in fx.s.blobs.items()}},indent=2)+'\n')
   if idc=='CB-GAP-1':
    spec=json.loads(fx.s.blobs[ns['A'].spec_digest]);row['bothScopeBindings']=[W.verify_scope_parameter_binding(spec,ns[k]) for k in ['SCOPE_A','SCOPE_B']]
 except Exception as e:row.update(result='REFUSED',exception=type(e).__name__,detail=str(e))
 results.append(row)
ns['audit_report']=audit_report
tree=ast.parse((P/'work/t_gaps.py').read_text())
class Wrap(ast.NodeTransformer):
 def visit_Call(self,node):
  self.generic_visit(node)
  if isinstance(node.func,ast.Name) and node.func.id=='report':node.func.id='audit_report'
  return node
exec(compile(ast.fix_missing_locations(Wrap().visit(tree)),str(P/'work/t_gaps.py'),'exec'),ns)
(P/'result.json').write_text(json.dumps({'standing':'Root reproduction using accepted19 reference; closure and direct scope/request helpers only. No semantic proof replay or blind assent.','results':results},indent=2)+'\n');print(json.dumps(results,indent=2))
