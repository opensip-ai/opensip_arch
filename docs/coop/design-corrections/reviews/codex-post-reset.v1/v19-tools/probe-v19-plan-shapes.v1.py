from pathlib import Path
import json,copy,importlib.util,hashlib,argparse
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(exist_ok=False);dc=a.root/'docs/coop/design-corrections'
s=importlib.util.spec_from_file_location('plan_shape_fixtures',dc/'integration-fixtures.py');F=importlib.util.module_from_spec(s);s.loader.exec_module(F);N=F.N;M=F.M
run,objects,blobs=F.build();plan=objects[run['planId']][1];rows=[]
for field in N.PLAN_SELECTION_FIELDS:
 for label,val in [('null',None),('bool',True),('number',1025),('long-string','x'*1025),('object',{}),('bad-element',[7])]:
  probe=copy.deepcopy(plan);probe[field]=val;assert N.admit_plan_selection_cardinality(probe) is probe
  try:M.identifier('plan',probe)
  except N.ScopeRefusal:raise AssertionError('schema route misclassified')
  except Exception as exc:result={'exceptionType':type(exc).__name__,'messageHead':str(exc)[:400]}
  else:raise AssertionError((field,label,'malformed Plan admitted'))
  rows.append({'field':field,'shape':label,'cardinalityPassThrough':True,'schemaRefused':True,**result})
 probe=copy.deepcopy(plan);probe.pop(field);assert N.admit_plan_selection_cardinality(probe) is probe
 try:M.identifier('plan',probe)
 except Exception as exc:rows.append({'field':field,'shape':'missing','cardinalityPassThrough':True,'schemaRefused':True,'exceptionType':type(exc).__name__})
 else:raise AssertionError('missing required field admitted')
 limit=N.plan_selection_bound(field);probe=copy.deepcopy(plan);probe[field]=[7]*(limit+1)
 try:N.admit_plan_selection_cardinality(probe)
 except N.ScopeRefusal as exc:
  assert exc.subject=={'field':field,'count':limit+1,'limit':limit};rows.append({'field':field,'shape':'oversized-bad-elements','cardinalityFirst':True,'subject':exc.subject})
 else:raise AssertionError('oversized malformed array admitted')
# Producer refusal is earlier than assembled-Plan declaration ordering; narrowing makes next boundary reachable.
try:N.plan_native_context_digests([{'refusals':[],'planNativeContextDigest':'%064x'%i} for i in range(129)])
except N.ScopeRefusal as exc:assert exc.subject['field']=='nativeContextDigests';producer=exc.subject
else:raise AssertionError('producer limit absent')
try:N.admit_plan_selection_cardinality({'semanticClosures':['closure2:'+'%064x'%i for i in range(129)],'nativeContextDigests':N.plan_native_context_digests([{'refusals':[],'planNativeContextDigest':'%064x'%i} for i in range(128)])})
except N.ScopeRefusal as exc:assert exc.subject['field']=='semanticClosures';assembled=exc.subject
else:raise AssertionError('assembled limit absent')
report={'standing':'Root exact reference composition over synthetic plan fixture and admission rows, not complete129context records, producthost or stored corruption routing. Actual full plan identity schema validates malformed shapes after cardinality pass-through.','sourceHashes':{str(p.relative_to(a.root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [dc/'integration-fixtures.py',dc/'native/native_evidence_model.v2.py',dc/'foundation/identity-model.py',dc/'foundation/identity-schemas.v2.json']},'checks':rows,'producerBeforeAssembled':{'early':producer,'afterNarrowing':assembled},'passed':len(rows),'failed':0};(a.out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':len(rows),'failed':0,'producerBeforeAssembled':report['producerBeforeAssembled']}))
