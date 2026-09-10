from pathlib import Path
import importlib.util,json,copy,hashlib
base=Path('/tmp/opensip-design-corrections');root=base/'v19-native-coauthor.v1/work';dc=root/'docs/coop/design-corrections';out=base/'codex-post-reset.v1/v19-invocation-subject.v1';out.mkdir(exist_ok=False)
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
N=load('scope_probe_native',dc/'native/native_evidence_model.v2.py');W=load('scope_probe_workflows',dc/'workflows/workflows_model.v1.py')
cases=json.loads((dc/'workflows/workflow-cases.v1.json').read_text());case=copy.deepcopy(cases['invocationCases'][0]);const=cases['constants']
def expand(v):
 if isinstance(v,str) and v.startswith('$'):return const[v[1:]]
 if isinstance(v,list):return [expand(x) for x in v]
 if isinstance(v,dict):return {k:expand(x) for k,x in v.items()}
 return v
case=expand(case);step=case['steps'][0];steps=[dict(stepId=i,kind=step['kind'],requirement=step['requirement'],dependsOn=[] if i==0 else [0],dependencyGate='completed',retryPolicy=step['retry'],params=step['params']) for i in range(2)]
record=dict(schemaFamily='opensip.product.invocation',schemaMajor=1,requestId=const['REQ'],projectId=const['PRJ'],workflow={'kind':'builtin','name':'analyze'},mode=case['mode'],orderedSteps=steps)
rows=[]
for field,count,prefix in [('semanticClosures',129,'closure2:'),('nativeContextDigests',129,''),('importIds',257,'import2:')]:
 try:N.admit_plan_selection_cardinality({field:[prefix+('%064x'%i) for i in range(count)]})
 except N.ScopeRefusal as exc:termination=N.scope_refusal_termination(exc)
 else:raise AssertionError('expected actual refusal')
 detail=termination['domainDetail'];observation={'event':'rejected','errorCode':termination['errorCode'],'detail':detail['code'],'subject':detail['subject'],'remedy':detail['remedy']}
 script={'0':case['script']['0'],'1':[observation]};result=W.run_invocation(record,script)
 r=result['stepResults'];assert r[0]['result']==case['script']['0'][0]['result'];assert r[1]['outcome']=='rejected' and 'result' not in r[1] and 'derivation' not in r[1]['attempts'][0]
 rows.append({'field':field,'nativeTermination':termination,'workflowTermination':r[1]['termination'],'subjectPreserved':r[1]['termination'].get('domainDetail',{}).get('subject')==detail['subject'],'earlierResultPreserved':True,'refusedStepHasNoResultOrDerivation':True,'record':record,'script':script,'result':result})
report={'standing':'Actual reference composition over synthetic trusted invocation observations and IDs; no product host, earlier Run closure, or OS execution. Native cardinality function raises real exception; its actual typed fields supplied to existing workflow rejected observation.','sourceHashes':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [dc/'native/native_evidence_model.v2.py',dc/'workflows/workflows_model.v1.py']},'rows':rows}
(out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps([{k:r[k] for k in ['field','subjectPreserved','earlierResultPreserved','refusedStepHasNoResultOrDerivation']} for r in rows],indent=2))
