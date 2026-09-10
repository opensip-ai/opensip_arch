from pathlib import Path
import json,copy,importlib.util,hashlib
b=Path('/tmp/opensip-design-corrections');before=b/'candidate-subject.v18';after=b/'v19-combined-proposal.v1/work';out=b/'codex-post-reset.v1/v19-subject-final.v1';out.mkdir(exist_ok=False)
def load(name,root):
 p=root/'docs/coop/design-corrections/workflows/workflows_model.v1.py';s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
B=load('subject_before',before);A=load('subject_after',after);cases=json.loads((before/'docs/coop/design-corrections/workflows/workflow-cases.v1.json').read_text());const=cases['constants']
def exp(v):
 if isinstance(v,str) and v.startswith('$'):return const[v[1:]]
 if isinstance(v,list):return [exp(x) for x in v]
 if isinstance(v,dict):return {k:exp(x) for k,x in v.items()}
 return v
rows=[]
for original in cases['invocationCases']:
 c=exp(copy.deepcopy(original));rec={'schemaFamily':'opensip.product.invocation','schemaMajor':1,'requestId':const['REQ'],'projectId':const['PRJ'],'workflow':{'kind':'builtin','name':'analyze'},'mode':c['mode'],'orderedSteps':[{'stepId':i,'kind':s['kind'],'requirement':s['requirement'],'dependsOn':s['dependsOn'],'dependencyGate':s['gate'],'retryPolicy':s['retry'],'params':s['params']} for i,s in enumerate(c['steps'])]}
 def run(m):
  try:return {'returned':m.run_invocation(copy.deepcopy(rec),copy.deepcopy(c['script']))}
  except Exception as e:return {'exceptionType':type(e).__name__,'error':str(e)}
 old,new=run(B),run(A);assert old==new,c['id'];rows.append({'id':c['id'],'equal':True,'kind':'returned' if 'returned' in old else 'exception','outcome':new})
shape=[]
for label,value in [('empty',''),('null',None),('false',False),('zero',0),('list',[]),('object',{}),('overlong','x'*2000)]:
 obs={'event':'rejected','errorCode':'REQUEST.UNSATISFIABLE','detail':'PROJECT.SCOPE_LIMIT','remedy':'narrow','subject':value};term=A.terminate(obs);assert 'subject' in term['domainDetail'] and term['domainDetail']['subject'] is value
 try:A.validate_import_record('workflows/schemas/common.schema.json','#/$defs/DomainDetail',term['domainDetail']);valid=True
 except Exception:valid=False
 assert valid==(label=='empty');shape.append({'shape':label,'preserved':True,'schemaAdmitted':valid})
base={'event':'rejected','errorCode':'REQUEST.UNSATISFIABLE','detail':'PROJECT.SCOPE_LIMIT','remedy':'narrow'};assert A.terminate(base)==B.terminate(base)
report={'standing':'Root exact workflow reference comparison using ORIGINAL case gate/dependency/retry fields, including expected exceptional cases; structured equality, not a product host or earlier Run-closure test. Root fixes coauthor backward-case adapter which erroneously defaulted dependencyGate instead of reading case.gate.','sourceHashes':{k:hashlib.sha256((p/'docs/coop/design-corrections/workflows/workflows_model.v1.py').read_bytes()).hexdigest() for k,p in [('before',before),('after',after)]},'originalCaseComparisons':rows,'originalCaseCount':len(rows),'originalCaseReturned':sum(x['kind']=='returned' for x in rows),'originalCaseExceptional':sum(x['kind']=='exception' for x in rows),'explicitSubjectShapes':shape,'absentSubjectUnchanged':True,'failed':0};(out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['originalCaseCount','originalCaseReturned','originalCaseExceptional','explicitSubjectShapes','failed']}))
