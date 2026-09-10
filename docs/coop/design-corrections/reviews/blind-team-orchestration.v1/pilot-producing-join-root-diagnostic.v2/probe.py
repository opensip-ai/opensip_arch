from pathlib import Path
import importlib.util,json,hashlib
B=Path('/tmp/opensip-design-corrections');F=B/'candidate-subject.v24/docs/coop/design-corrections/foundation'
OUT=B/'pilot-producing-join-root-diagnostic.v2';OUT.mkdir(exist_ok=False)
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=load('parser',B/'check-blind12-exported-graphs.v1.py');R=load('replay',F/'evaluator_replay_model.v3.py')
path=B/'consumer-b.v12-team-pilot-corrections.v4/output/runs/syntax-code.store.json';raw=path.read_bytes()
objects,blobs=P.decode_store(raw,R.M);rid='run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b'
captured={};orig_load=R.I.load
def capture_load(name,path):
 m=orig_load(name,path)
 if path.name=='execution_inputs_model.v1.py':
  admit=m.admit_execution_inputs;derive=m.derive_outcome
  def captured_derive(**kw):
   result=derive(**kw);captured.setdefault('derivedOperands',[]).append({'operands':kw,'result':result});return result
  def captured_admit(**kw):
   captured['claimedCellOutcomes']=kw['execution_inputs']['cellOutcomes']
   result=admit(**kw);captured['actualAdmission']=result;return result
  m.derive_outcome=captured_derive;m.admit_execution_inputs=captured_admit
 return m
R.I.load=capture_load
try:result=R.replay(objects[rid][1],objects,blobs);status={'result':result}
except Exception as e:status={'exceptionType':type(e).__name__,'refusal':str(e)}
report={'standing':'Root read-only unchanged-reference instrumentation records actual producing operands/results; no expected-value changes, graph remint, or blind-team input.','runId':rid,'exportSha256':hashlib.sha256(raw).hexdigest(),'referenceSha256':hashlib.sha256((F/'execution_inputs_model.v1.py').read_bytes()).hexdigest(),**status,**captured}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({**status,'claimed':captured.get('claimedCellOutcomes'),'derived':[x['result'] for x in captured.get('derivedOperands',[])],'report':str(OUT/'report.json')},indent=2))
