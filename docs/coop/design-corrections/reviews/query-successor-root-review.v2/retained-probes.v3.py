"""Root discriminating probes using existing admitted reference inputs; not a blind reconstruction."""
from pathlib import Path
import copy,hashlib,importlib.util,json
ROOT=Path('/tmp/opensip-design-corrections/query-successor.v1/docs/coop/design-corrections')
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
qpath=ROOT/'workflows/query_projection_model.v3.py';before=qpath.read_bytes();Q=load('root_query_probe',qpath)
S=load('root_query_fixture',ROOT/'foundation/evaluator_semantic_fixture.v3.py');R=load('root_query_replay',ROOT/'foundation/evaluator_replay_model.v3.py');M=R.M
atom={'op':'none','relation':'references','minResolution':'resolved-binding','endpoint':'target','filters':[]}
g=S.build_ts_semantic_graph(atom=atom,has_declares=False,has_references_fact=True,second_partition=True,references_resolved=False,incoming_search=True,incoming_complete=False,target_sidecar=True)
seed,objects,blobs,_=S.seed_seal(g);_,owner=M.open_run_closure(seed,objects,blobs);i=g['inputs'];derived=R.derive(i['planId'],i['executionPlanId'],i['evaluatorClosure'],i['evaluationInputRefs'],objects,blobs,owner);run,objects,blobs=S.seal_derived(g,derived,objects,blobs);rid=M.close_run(run,objects,blobs)
endpoint={'universe':g['u1'],'kind':'symbol','nativeSubjectId':g['foo']}
request={'schemaFamily':'opensip.product.query','schemaMajor':3,'projectId':run['projectId'],'view':{'runId':rid},'operation':'graph.neighbors','params':{'relation':'references','minResolution':'resolved-binding','direction':'incoming','endpoint':endpoint},'completeness':'required','page':{'size':100}}
results={}
def query(name,req,host=None):
 try:
  result=Q.execute_graph_query(req,run,objects,blobs,host=host);results[name]={'returned':result};return result
 except Exception as exc:
  results[name]={'error':type(exc).__name__,'message':str(exc),'termination':exc.termination() if hasattr(exc,'termination') else None};return None
actual=query('actual-incomplete-incoming',request)
# An invalidated derived cache must never suppress retained factual edges.
req=copy.deepcopy(request);req['params']['direction']='outgoing';baseline=query('actual-outgoing-positive',req,host={'cache':{}})
if baseline:
 cache={'poison':{'edges':[]}};Q.execute_graph_query(req,run,objects,blobs,host={'cache':cache})
 for value in cache.values():value['edges']=[]
 query('same-run-poisoned-derived-cache',req,host={'cache':cache})
# Same Run, fabricated unknown vertex in unknown universe.
req=copy.deepcopy(request);req['operation']='graph.path';unknown={'universe':'e'*64,'kind':'symbol','nativeSubjectId':'missing'};req['params']={'relation':'references','minResolution':'resolved-binding','direction':'outgoing','start':unknown,'target':unknown,'maxDepth':1};query('unknown-endpoint-zero-hop',req)
# Closure-independent authority is forbidden on the advertised strong wrapper.
syn={'standing':'synthetic-only' ,'admittedFactGraph':{'runId':rid,'projectId':run['projectId'],'viewIds':[],'edges':[]}}
try:results['strong-wrapper-with-no-retained-run']={'returned':Q.execute_graph_query(request,host=syn)}
except Exception as exc:results['strong-wrapper-with-no-retained-run']={'error':type(exc).__name__,'message':str(exc)}
# Discriminating globally capped endpoint walk and a stale snapshot-index mapping.
req=copy.deepcopy(request);req['operation']='graph.path';req['params']={'relation':'references','minResolution':'resolved-binding','direction':'outgoing','start':endpoint,'target':{'universe':g['u1'],'kind':'symbol','nativeSubjectId':g['bar']},'maxDepth':1};query('actual-path-visited-cap-one',req,host={'testBounds':{'maxVisitedNodes':1}})
req=copy.deepcopy(request);fake='snapshot2:'+('e'*64);assert fake!=run['snapshotId'];req['view']={'snapshotId':fake};query('wrong-snapshot-index-result',req,host={'runsForSnapshot':{fake:[rid]}})
# Newly discovered v2 selection and error-carrier counterexamples.
req=copy.deepcopy(request);req['view']={'snapshotId':run['snapshotId']}
query('snapshot-with-no-uniqueness-observation',req)
query('snapshot-with-empty-uniqueness-observation',req,host={'runsForSnapshot':{run['snapshotId']:[]}})
query('snapshot-with-explicit-unique-observation',req,host={'runsForSnapshot':{run['snapshotId']:[rid]}})
req=copy.deepcopy(request);req['params']['relation']='calls';req['params']['minResolution']='resolved-callee';query('known-symbol-with-no-selected-native-evidence',req)
for name,req,retained,host in [
 ('malformed-request-no-retained-run',{'schemaMajor':3,'bad':1.25},False,{}),
 ('malformed-project-failure-carrier',dict(request,projectId='not-a-project'),True,{'requestId':'req1_'+'a'*32}),
 ('malformed-float-failure-carrier',dict(request,page={'size':1.25}),True,{}),
 ('deterministic-request-id-fallback',dict(request,page={'size':0}),True,{})]:
 try:
  Q.execute_graph_query(req,run if retained else None,objects if retained else None,blobs if retained else None,host=host)
  results[name]={'unexpected':'ADMIT'}
 except Exception as exc:
  row={'error':type(exc).__name__,'message':str(exc),'termination':exc.termination() if hasattr(exc,'termination') else None}
  if hasattr(exc,'envelope'):
   try:row['failureEnvelope']=exc.envelope()
   except Exception as inner:row['carrierError']={'type':type(inner).__name__,'message':str(inner).splitlines()[0]}
  results[name]=row
report={'standing':'Root probes of exact in-progress query model using author reference input builders plus actual M3 complete Run admission; not blind, independent acceptance or product qualification','queryModelSha256':hashlib.sha256(before).hexdigest(),'modelUnchangedDuringProbe':qpath.read_bytes()==before,'runId':rid,'ownerAdmission':'ADMIT','retainedVerdict':derived['proof']['verdict'],'coveragePayloads':{c:M.C.parse(blobs[objects[c][1]['payloadDigest']]) for c in g['coverageIds']},'results':results}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'modelUnchanged':report['modelUnchangedDuringProbe'],'results':{n:({'items':len(v['returned']['items']),'visited':v['returned']['context']['visitedNodes'],'traversal':v['returned']['context']['traversalCoverage']} if 'returned' in v else v) for n,v in results.items()}},indent=2))
