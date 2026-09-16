from pathlib import Path
import importlib.util,json,hashlib
B=Path('/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v1/source/docs/coop/design-corrections/foundation')
s=importlib.util.spec_from_file_location('root_host_scope_semantic',B/'check-semantic-replay.v3.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
T=S.load('root_host_scope_model','run_termination_model.v1.py')
Q=S.load('root_host_scope_query','../workflows/query_projection_model.v3.py')
rows=[]
for terminal in ['budget-exhausted','unavailable']:
 graph=S.S.build_ts_semantic_graph(atom=S.REFS_NONE_TGT,has_declares=False,has_references_fact=True,second_partition=True,references_resolved=False,incoming_search=True,incoming_complete=False,target_sidecar=True,budget_limit=1,references_stage_terminals={'foo':terminal})
 run,objects,blobs,_=S.close_positive(graph)
 fin=T.finalize(run,objects,blobs);term=fin['termination'];variants=[]
 for name,fields in [('execution-attribution',{'executionId':'exec1_'+'a'*32}),('work-budget-explanation',{'domainDetail':{'code':'EVALUATION.WORK_BUDGET_EXHAUSTED','remedy':'Increase the deterministic evaluator work budget.'}})]:
  alt={**term,**fields}
  Q.validate_schema(Q.COMMON_ID+'#/$defs/StepTermination',alt)
  try:T.check_candidate(alt,term);outcome='ADMIT'
  except T.RunTerminationError as e:outcome='REFUSE:'+str(e)
  variants.append({'name':name,'schema':'ADMIT','derivation':outcome})
 _,_,population,ctx=T.retained_population(run,objects,blobs)
 rows.append({'terminal':terminal,'closeRun':'ADMIT','finalize':fin,'populationCauses':sorted(set(d['cause'] for d in population)),'variants':variants})
d={'standing':'Root actual closed-Run reference scope probes; no product test or acceptance','inputs':{f:hashlib.sha256((B/f).read_bytes()).hexdigest() for f in ['check-semantic-replay.v3.py','run_termination_model.v1.py','run-termination-contract.v1.md','evaluator_semantic_fixture.v3.py']},'rows':rows}
Path(__file__).with_name('report.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
