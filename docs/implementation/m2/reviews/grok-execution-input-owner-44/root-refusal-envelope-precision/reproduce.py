from pathlib import Path
import json,copy,importlib.util
T=Path('/tmp/opensip-implementation');F=T/'m2-evaluator-parameters-subject-43/reference/archroot/docs/coop/design-corrections/foundation';O=T/'m2-execution-inputs-trial-46/refusal-envelope-check';O.mkdir()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
E=load('execution46_envelope_e',F/'evaluator_input_model.v3.py');X=load('execution46_envelope_x',F/'execution_inputs_model.v1.py');I=E.ENUM.IM;C=I.C;q=json.loads((T/'m2-evaluator-parameters-subject-43/reference-check/requests.ndjson').read_text().splitlines()[0]);objects={r['id']:(r['domain'],r['descriptor'])for r in q['objects']};blobs={r['digest']:bytes.fromhex(r['hex'])for r in q['blobs']};run=objects[q['runId']][1];_,owner=I.open_run_closure(run,objects,blobs);plan=owner['plan'];spec=owner['analysisSpec'];selected,policy,emission=E.required_parameters(plan,spec,blobs,objects,I);enum=selected['foundation/enumeration-plan.schema.v1.json'][1];seal=objects[run['evaluationSealId']][1];eid=seal['executionPlanId'];execution=objects[eid][1];ref=next(r for r in q['inputRefs']if r['domain']=='execution-inputs');manifest=C.parse(blobs[ref['digest']]);results={}
for name,change in [('admitted',False),('plan-mismatch',True)]:
 m=copy.deepcopy(manifest)
 if change:m['analysisSpecDigest']='0'*64
 promised=X.promised_pointers(m,plan,execution,enum,objects=objects,blobs=blobs)
 def records(d):return{r['digest']:C.parse(blobs[r['digest']])for r in m['selectedRefs']if r['domain']==d}
 out=X.admit_execution_inputs(plan_id=q['planId'],plan=plan,execution_plan_id=eid,execution_plan=execution,enumeration_plan=enum,analysis_spec=spec,execution_inputs=m,objects=objects,blobs=blobs,store_pointers=promised['store_pointers'],inventories=records('subject-inventory'),closures={k:v for k,(d,v)in objects.items()if d=='closure'},imports={k.split(':')[1]:objects[k][1]for k in plan['importIds']},candidate_results=records('candidate-producer-result'),target_attributions=records('target-attribution'),incoming_searches=records('incoming-search'),stage_specs={s['stageSpecDigest']:C.parse(blobs[s['stageSpecDigest']])for s in execution['stages']},vcs_observation=C.parse(blobs[owner['snapshot']['vcsDigest']]))
 (O/(name+'.json')).write_text(json.dumps(out,indent=2)+'\n');results[name]={'result':out['result'],'refusals':out['refusals'],'derivedAccounts':len(out['derivedAccounts']),'derivedOutcomes':len(out['derivedOutcomes']),'requiredCellDeficiencies':len(out['requiredCellDeficiencies']),'digest':out['digest']}
assert results['admitted']['result']=='ADMIT'and results['plan-mismatch']['result']=='REFUSE'and results['plan-mismatch']['derivedAccounts']and results['plan-mismatch']['derivedOutcomes']
(O/'result.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results))
