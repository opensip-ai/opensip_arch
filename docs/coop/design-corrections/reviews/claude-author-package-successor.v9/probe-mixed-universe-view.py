"""Author counterexample: merge lawful views without changing their scopes or facts."""
from pathlib import Path
import importlib.util,copy,json
import argparse
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--package',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
ROOT=a.package.resolve()
for source_root in (ROOT,a.source.resolve()):
 if a.out.resolve().is_relative_to(source_root):raise ValueError('Output must be outside frozen source/package trees')
if a.out.exists():raise ValueError('Use a fresh output path; prior evidence must be preserved')
F=a.source/'docs/coop/design-corrections/foundation'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=load('author_replay_check',F/'check-replay.v3.py');X=load('author_host_capture',F/'execution_inputs_fixture.v3.py')
M=P.M;rows=[]
for merged in [False,True]:
 g=P.F.build_file_inputs(multiple_universes=True)
 if merged:
  objects=g['objects'];blobs=g['blobs'];views=[objects[v][1] for v in g['viewIds']];v=copy.deepcopy(views[0])
  for key in ['scopeIds','facts','coverageIds']:v[key]=P.E.cset([x for view in views for x in view[key]])
  vid=M.identifier('view',v);objects[vid]=('view',v);g['viewIds']=[vid];g['viewId']=vid
  g['inputs']['evaluationInputRefs']=[r for r in g['inputs']['evaluationInputRefs'] if r['domain']!='view']+[{'domain':'view','digest':vid.split(':',1)[1]}]
 try:
  capture=X.attach_host_capture(g)
  seed,objects,blobs,_=P.F.seal_fixture(g);_,owner=M.open_run_closure(seed,objects,blobs)
  row={'merged':merged,'structural':'ADMIT','captureResult':capture['admission']['result'],'captureRefusals':capture['admission']['refusals']}
  i=g['inputs']
  try:
   result=P.R.derive(i['planId'],i['executionPlanId'],i['evaluatorClosure'],i['evaluationInputRefs'],objects,blobs,owner)
   run,objects,blobs=P.seal(g,result,objects,blobs);rid=M.close_run(run,objects,blobs);row.update(semantic='ADMIT',runId=rid)
  except Exception as e:row.update(semantic='REFUSE',reason=str(e))
 except Exception as e:row={'merged':merged,'error':str(e)}
 rows.append(row)
a.out.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
