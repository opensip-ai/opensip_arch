import importlib.util,json
from pathlib import Path
s=Path('/tmp/opensip-design-corrections/evaluator-successor.v1/docs/coop/design-corrections')
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
R=load('root_mixed_replay',s/'foundation/check-replay.v3.py');P=load('root_mixed_projection',s/'workflows/workflow_projection_model.v3.py')
scope={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['**'],'exclude':[]}
def graph(pattern):return R.positive(scope_document=scope,atom_override={'op':'exists','relation':'file','minResolution':'enumerated','filters':[{'field':'subject','cmp':'glob','value':pattern}]})
baseline=graph('README.md');current=graph('src/**')
bv=P.project_admitted_run_v3(*baseline);cv=P.project_admitted_run_v3(*current)
art=P.adopt_admitted_baseline_v3(*baseline,{'exportedAtUtc':'2026-09-08T00:00:00Z','exportedByHostRelease':'1.0.0'})
closures={k:{'bytes':'ok','trust':'admitted','trustOrigin':'retained-generation','protocolMajor':v['protocolMajor'],'platform':v['platform']} for k,(d,v) in baseline[1].items() if d=='closure'}
host={'closures':closures,'protocolMajors':sorted({v['protocolMajor'] for v in closures.values()}),'platform':'macos-aarch64','pivotRunId':bv['runId'],'recipeMajors':[2]}
comp=P.compare_admitted_v3(baseline_artifact=art,current_run=current[0],current_objects=current[1],current_blobs=current[2],host=host,profile_name='code-regression',pivot_runs={'E1':baseline})
result={'standing':'Root concrete fully admitted counterexample, not expected-output oracle','baselineRoots':P.admitted_root_predicate_values(bv,bv['policy']['rules'][0]['ruleId']),'currentRoots':P.admitted_root_predicate_values(cv,cv['policy']['rules'][0]['ruleId']),'baselineCanProveAbsentNonhit':P.rule_can_prove_absence(bv,bv['policy']['rules'][0]['ruleId']),'comparison':comp}
Path('/tmp/opensip-design-corrections/mixed-root-absence.v1.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
