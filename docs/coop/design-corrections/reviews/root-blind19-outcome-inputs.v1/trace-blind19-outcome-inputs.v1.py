from pathlib import Path
import json,sys,importlib.util,hashlib
B=Path('/tmp/opensip-design-corrections');S=B/'candidate-subject.v32';O=B/'root-blind19-outcome-inputs.v1';O.mkdir()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
R=mod('root_transport',B/'check-blind-successor32-export.v1.py');M=mod('root_identity',S/'docs/coop/design-corrections/foundation/identity-model.v3.py')
raw=(B/'root-blind19-final-source32.v1/captured/syntax-code.store.json').read_bytes();d=R.parse(raw);objects,blobs,_=R.decode(raw,M);rid=d['claim']['runId'];calls=[]
def trace(f,event,arg):
 if event=='return' and f.f_code.co_filename.endswith('execution_inputs_model.v1.py') and f.f_code.co_name in ('_summarize_coverage_records','derive_outcome'):
  keys=['expected','covered','records','enumerator_status','universe','required','inventories','account_summaries','candidate_rec','candidate_cap','binding'];data={k:sorted(f.f_locals[k]) if isinstance(f.f_locals[k],set) else f.f_locals[k] for k in keys if k in f.f_locals};calls.append({'function':f.f_code.co_name,'inputs':data,'result':arg})
 return trace
try:
 sys.settrace(trace);M.close_run(objects[rid][1],objects,blobs);reason=None
except Exception as e:reason=str(e)
finally:sys.settrace(None)
r={'standing':'Exact source32 over unchanged final19 syntax-code export; read-only return-value diagnostic, not acceptance. No consumer imports or supplied blind oracle.','runId':rid,'exportSha256':hashlib.sha256(raw).hexdigest(),'reason':reason,'calls':calls};(O/'report.json').write_text(json.dumps(r,indent=2)+'\n');(O/p.name).write_bytes(p.read_bytes());print('traced',len(calls),'calls; reason',reason)
