from pathlib import Path
import importlib.util,sys,json
B=Path('/tmp/opensip-design-corrections');F=B/'candidate-subject.v31/docs/coop/design-corrections/foundation';O=B/'root-blind16-join-diagnosis.v1';assert not O.exists();O.mkdir()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
D=load('root_strict_transport',B/'check-blind-successor31-export.v1.py');M=load('root_exact_owner',F/'identity-model.v3.py');captures=[]
for name in ['typescript','rust-partial','syntax-data']:
 p=B/'root-blind16-source31-pilots.v1/inputs'/(name+'.input.json');objects,blobs,_=D.decode(p.read_bytes(),M);rid=[k for k,(d,r) in objects.items() if d=='run'];assert len(rid)==1;events=[];seen=set()
 def trace(frame,event,arg):
  if event=='call' and frame.f_code.co_name=='_add' and Path(frame.f_code.co_filename).name in ['enumeration_model.v1.py','execution_inputs_model.v1.py']:
   code=next((v for v in frame.f_locals.values() if isinstance(v,str) and v.startswith(('ENUMERATION_','EXECUTION_INPUTS_'))),None);caller=frame.f_back;key=(code,caller.f_lineno)
   if code and key not in seen:
    seen.add(key);values={k:caller.f_locals[k] for k in ['entry','expected_entry','derived','expected_kinds','ext_kinds','e','derived_ext','acc','want_app','want_u','want_def','want_cause','d_state','row','derived_pair','host_pair','ci','po','rel','rung'] if k in caller.f_locals}
    # These are exact observed reference locals, not repaired or supplied consumer values.
    events.append({'fault':code,'file':str(Path(caller.f_code.co_filename).relative_to(F.parent)),'line':caller.f_lineno,'locals':json.loads(json.dumps(values,default=str))})
  return trace
 sys.settrace(trace)
 try:M.close_run(objects[rid[0]][1],objects,blobs);result='ADMIT'
 except Exception as e:result=str(e)
 finally:sys.settrace(None)
 captures.append({'name':name,'runId':rid[0],'result':result,'observedFaults':events});print(name,result,flush=True)
(O/'diagnosis.json').write_text(json.dumps({'standing':'Root reference trace of exact captured blind16 exports. No consumer imports/input edits. Internal diagnostics are not supplied to blind and are not a design-fault finding by themselves.','source31Sha256':'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5','cases':captures},indent=2)+'\n')
