"""Explicit successor planning descriptions for proposed invocation5/query4."""
from pathlib import Path
import copy,hashlib,json,types
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v')
raw=V.read_unit('report-projection','owner/builtin-step-planning.v1.json');planning=json.loads(raw)
assert planning['schemaVersion']==1
planning['schemaVersion']=2
planning['standing']='Proposed joint report09 planning descriptions; unaccepted successor of report08. New source-bound fit and query4 representative construction only; no host implementation.'
fit=planning['commands']['fit'];assert len(fit)==1
step=fit[0]['steps'][1]
assert step['kind']=='query' and step['dependsOn']==[0] and step['dependencyGate']=='completed'
old_fit=copy.deepcopy(step)
step['representativeParams']={'kind':'query','operation':'candidate.list','sourceStep':0}
step['paramsBinding']={'type':'object','additionalProperties':False,'required':['kind','operation','sourceStep'],
                      'properties':{k:{'const':v} for k,v in step['representativeParams'].items()}}
changed=[]
for command,variants in planning['commands'].items():
 for variant in variants:
  if variant['status']!='plannable':continue
  for index,row in enumerate(variant['steps']):
   params=row['representativeParams']
   if params['kind']=='query' and 'request' in params:
    request=params['request']
    if request.get('schemaFamily')!='opensip.product.query':
     assert command=='review-brief' and request['operation']=='review.produce-brief'
     continue
    assert request['schemaMajor']==3
    request['schemaMajor']=4;changed.append({'command':command,'variant':variant['variant'],'stepId':index})
planning['fitQueryBinding']={
 'planning':'Exactly one fit candidate.list query names earlier analysis step0 through sourceStep, an explicit completed dependency; no pre-analysis concrete Run query request',
 'resolution':'After that analysis completes authoritatively, construct query4 for its exact RunId and this invocation ProjectId, best-effort/page100/includeSuppressed=false. No latest fallback',
 'ephemeral':'No authoritative public query is constructed; complete the query step with the unavailable-ephemeral-analysis report and its exact summary',
 'completion':'Retain admitted page + exact request + request/step/ExecutionId and compact summary together through required output settlement',
 'interruption':'Completed page remains available; actual noncompleted query produces unavailable-query-result null candidate parity when a Run is carried. No-Run failure has no advisoryReport',
 'requiredSourceOwners':['fit-interruption01','workflow-timing02','report09 complete schema/carrier succession'],
}
folder=HERE/'composed-owners';folder.mkdir(exist_ok=True);path=folder/'builtin-step-planning.proposed.json';path.write_text(json.dumps(planning,indent=2)+'\n')
result={'standing':'Proposed owner description only; source/inventory acceptance and product planning pending','parentSha256':hashlib.sha256(raw).hexdigest(),
 'fitStepBefore':old_fit,'fitStepAfter':step,'otherFreshQueryRequests':changed,'output':{'path':str(path.relative_to(HERE)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}}
(HERE/'planning-composition-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'freshQueryRequests':len(changed),'fitSourceStep':0}))
