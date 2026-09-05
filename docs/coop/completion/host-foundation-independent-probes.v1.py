"""Independent review probes; does not modify the reviewed evidence unit."""
import copy,hashlib,importlib.util,json
from pathlib import Path
B=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('review_foundation',B/'host-foundation-model.v1.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
C=json.loads((B/'host-foundation-cases.v1.json').read_text())['cases'];rows=[]
def base(kind):return copy.deepcopy(next(c['input'] for c in C if c['kind']==kind))
def run(id,kind,x,predicate):
 try:actual=M.evaluate(kind,x);ok=predicate(actual)
 except Exception as e:actual={'uncaught':type(e).__name__,'message':str(e)};ok=False
 rows.append({'id':id,'kind':kind,'input':x,'actual':actual,'passed':bool(ok)})
def cfg(id,file,predicate=lambda r:r['status']=='CONFIG-INVALID'):
 x=base('configuration');x['files']={'project/opensip.json':file};run(id,'configuration',x,predicate)
for id,raw in [('escaped-duplicate','{"schemaVersion":1,"schema\\u0056ersion":1}'),('fraction-budget','{"schemaVersion":1,"analysis":{"budget":{"unit":"work-units","limit":1.5}}}'),('overflow-budget','{"schemaVersion":1,"analysis":{"budget":{"unit":"work-units","limit":9007199254740992}}}'),('surrogate','{"schemaVersion":1,"x":"\\udfff"}'),('huge-number','{"schemaVersion":'+('9'*5000)+'}'),('float-overflow','{"schemaVersion":1,"x":1e309}'),('trailing','{"schemaVersion":1} null')]:cfg(id,{'raw':raw})
cfg('escaped-depth-brackets',{'raw':'{"schemaVersion":1,"x":"\\\"[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[["}'})
x=base('configuration');x['defaults']['profile']='forged';run('defaults-host-invariant','configuration',x,lambda r:r['status']=='HOST-INVARIANT-FAILURE')
x=base('configuration');x['hostEnvironment']={'analysis':{'budget':{'unit':'work-units','limit':1}}};run('environment-host-invariant','configuration',x,lambda r:r['status']=='HOST-INVARIANT-FAILURE')
x=base('configuration');x['tty']=True;x['ci']=True;x['files']['project/.opensip/local.json']={'directory':True};run('ci-no-local-access','configuration',x,lambda r:r['status']=='ACCEPT' and all('.opensip/local' not in t for t in r['trace']))
x=base('configuration');x['tty']=True;x['ci']=False;x['files']['project/.opensip/local.json']={'directory':True};run('interactive-bad-local-refuses','configuration',x,lambda r:r['status']=='CONFIG-INVALID')
x=base('configuration');x['files']={'host/settings.json':{'json':{'schemaVersion':1,'analysis':{'budget':{'unit':'work-units','limit':2}},'ui':{'color':'always'}}},'project/opensip.json':{'json':{'schemaVersion':1,'analysis':{'budget':{'unit':'work-units','limit':3}}}}};x['budgetFlag']='4';run('flag-provenance-and-presentation','configuration',x,lambda r:r['semantic']['analysis.budget']['limit']==4 and r['provenance']['analysis.budget']['decidingLayer']=='flags' and r['presentation']=={'ui.color':'always'} and 'ui.color' not in r['semantic'])
x=base('configuration');x['files']={'host/settings.json':{'json':{'schemaVersion':1,'components':{'pins':[]}}}};run('global-cannot-set-components','configuration',x,lambda r:r['status']=='CONFIG-INVALID')
x=base('configuration');sid=x['defaults']['components']['request'][0]['stableId'];item={'stableId':sid,'version':'1.0.0'};x['files']={'project/opensip.json':{'json':{'schemaVersion':1,'components':{'pins':[item],'holds':[item]}}}};run('identical-pin-hold-resolver-refusal','configuration',x,lambda r:r['status']=='CONFIG-INVALID' and r['solverExecuted'])
x=base('project');x.update(ioFailure=True,filesystem='nfs',birth=None);run('io-failure-not-fabricated-unsupported','project',x,lambda r:r['status']=='HOST-IO-FAILURE')
x=base('project');x.update(mode='doctor-project',filesystem='overlay');run('doctor-unsupported-no-fallback','project',x,lambda r:r['status']=='UNDETERMINED' and r['fallbackToCore'] is False and r['effects']==[])
x=base('root');x['ancestors'][0]['kind']='symlink';run('root-symlink-ancestor','root',x,lambda r:r['status']=='REFUSE' and not r['effects'])
x=base('root');x['exists']=False;x['stateUsing']=False;run('root-readonly-no-create','root',x,lambda r:r['status']=='ABSENT' and not r['created'] and not r['effects'])
p={'policySchema':1,'policyScope':'global','grants':[],'denies':[],'consents':[]}
x={'files':{'host/policies/permission-policy.json':{'json':p,'mode':0o644}}};run('policy-world-readable-refuses','policy',x,lambda r:r['status']=='REFUSE' and r['snapshots']==[])
x={'files':{'host/policies/permission-policy.json':{'symlink':'../../repo-policy.json'},'host/repo-policy.json':{'json':p}}};run('policy-leaf-link-refuses','policy',x,lambda r:r['status']=='REFUSE' and r['snapshots']==[])
x={'files':{'project/permission-policy.json':{'raw':'malformed'}},'hostFenceHeld':False};run('policy-fence-before-read','policy',x,lambda r:r['status']=='REFUSE' and r['trace']==[])
x={'files':{'project/permission-policy.json':{'raw':'malformed'}}};run('repository-policy-never-read','policy',x,lambda r:r['status']=='ACCEPT' and all(not t.endswith('project/permission-policy.json') for t in r['trace']) and r['grantsCreated']==[])
report={'scope':'Independent bounded design probes','passed':sum(r['passed'] for r in rows),'total':len(rows),'probes':rows}
(B/'host-foundation-independent-probes.v1.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(report['passed'],report['total']);print([r['id'] for r in rows if not r['passed']])
