"""Checkpoint-3: ACTUAL guard execution driven to a schema-admitted envelope.

Root is right that p2_envelope.py labelled a hardcoded array `REAL guard outputs` while never invoking a
guard; those were representative-string composition tests. Here every refusal string is produced BY CALLING
the guard, then normalized, routed and composed. Schema admission only; no host runtime."""
import importlib.util,json,pathlib,sys
DC=pathlib.Path(sys.argv[1])
s=importlib.util.spec_from_file_location('f',DC/'integration-fixtures.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
N,W=f.N,f.W
CM='workflows/schemas/common.schema.json';ENV='workflows/schemas/command-envelope.schema.json'
def adm(doc,sel,v):
    try:W.validate_import_record(doc,sel,v);return 'ADMIT'
    except Exception as e:
        c=e.__cause__;return 'REFUSE:'+(str(c).split('\n')[0] if c else str(e))[:80]
def invoke(fn):
    """Call the real guard and return its raw refusal string."""
    try:fn();return None
    except Exception as exc:return str(exc)
REQ=lambda cap,mode='ts-tsconfig':(lambda:N.admit_requested_capabilities(
    [{'capabilityId':cap,'languageMode':mode,'workspaceRoot':'.','required':True}]))
REL=lambda rows:(lambda:N.admit_release_capability_registry(rows))
CASES=[
 ('requested: unregistered id',REQ('made-up-capability'),'external-configuration'),
 ('requested: unregistered id (supplied spec)',REQ('made-up-capability'),'externally-supplied-spec'),
 ('requested: unregistered id (host bug)',REQ('made-up-capability'),'host-generated-internal-layer'),
 ('requested: unregistered mode',REQ('syntax','cobol-classic'),'external-configuration'),
 ('requested: NOT-SELECTED cell',REQ('clones-cross-tsjs','rust-cargo'),None),
 ('release: unregistered id',REL([{'capabilityId':'made-up','languageModes':['ts-tsconfig']}]),None),
 ('release: preview constant',REL([{'capabilityId':'preview-typescript','languageModes':['ts-tsconfig']}]),None),
 ('release: unregistered mode',REL([{'capabilityId':'syntax','languageModes':['cobol-classic']}]),None),
 ('release: NOT-SELECTED cell',REL([{'capabilityId':'clones-cross-tsjs','languageModes':['rust-cargo']}]),None),
 ('release: duplicate row',REL([{'capabilityId':'syntax','languageModes':['rust-cargo']},
                                {'capabilityId':'syntax','languageModes':['ts-tsconfig']}]),None),
 ('requested: OVERBOUND mode (4096 chars)',REQ('syntax','m'*4096),'external-configuration'),
 ('requested: OVERBOUND mode (supplied spec)',REQ('syntax','m'*4096),'externally-supplied-spec'),
 ('requested: OVERBOUND mode (host bug)',REQ('syntax','m'*4096),'host-generated-internal-layer'),
 ('requested: exact-bound mode (1024 chars)',REQ('syntax','m'*1024),'external-configuration'),
]
rows=[]
for label,guard,origin in CASES:
    raw=invoke(guard)
    if raw is None:rows.append({'case':label,'guardRefused':False});continue
    key,subject=N.normalize_internal_key(raw)
    t=N.public_termination_for(raw,origin)
    errors=N.failure_envelope_errors(raw,origin)
    env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure',
         'requestId':'req1_'+'a'*32,'termination':t,'exitCode':W.EXIT[t['class']],'errors':errors}
    rows.append({'case':label,'guardRefused':True,'rawLength':len(raw),'key':key,
                 'subjectLength':len(errors[0]['subject']),'elided':'#sha256:' in errors[0]['subject'],
                 'class':t['class'],'errorCode':t['errorCode'],'detailCode':errors[0]['code'],
                 'terminationAdmission':adm(CM,'#/$defs/StepTermination',t),
                 'envelopeAdmission':adm(ENV,'',env)})
# per-step availability over two admitted selections that jointly exceed 1024
units=lambda n,tag:[{'rootPath':'u%s/%d'%(tag,i),'languageMode':'ts-tsconfig','languageFamily':'tsjs'} for i in range(n)]
a=N.default_capability_selection(units(93,'a'),[])['undeclaredCapabilities']
b=N.default_capability_selection(units(93,'b'),[])['undeclaredCapabilities']
avail=N.invocation_availability([(0,a),(3,b)])
flat=N.release_absence_notices(a+b)
out={'actualGuardCases':rows,'perStepAvailability':{
  'stepNoticeCounts':[st['noticeCount'] for st in avail['steps']],
  'totalNoticeCount':avail['totalNoticeCount'],'stepCount':avail['stepCount'],
  'flatWouldBe':flat['noticeCount'],
  'collectionAdmission':adm(CM,'#/$defs/CapabilityAvailabilityV1',avail),
  'flatSingleStepAdmission':adm(CM,'#/$defs/CapabilityAvailabilityStepV1',
      dict(flat,stepId=0)),
  'stepIdsPreserved':[st['stepId'] for st in avail['steps']],
  'emptyStepIsRetained':N.invocation_availability([(0,[])])['steps']==[{'stepId':0,'noticeCount':0,'notices':[]}],
  'noSelectionStepAbsent':N.invocation_availability([])['steps']==[],
  'repeatedTupleAcrossSteps':(lambda x:x['steps'][0]['notices'][0]==x['steps'][1]['notices'][0]
      and adm(CM,'#/$defs/CapabilityAvailabilityV1',x)=='ADMIT')(N.invocation_availability([(0,a[:2]),(1,a[:2])]))}}
out['noticeCodeIsConst']=adm(CM,'#/$defs/CapabilityAvailabilityNoticeV1',
  dict(N.release_absence_notices(a[:1])['notices'][0],code='CONFIG.INVALID'))
print(json.dumps(out,indent=1))
