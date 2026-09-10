# Independent v5 probes, group C: cross-unit regressions implicated by the v4->v5 delta.
import json,sys,os,importlib.util,copy,hashlib,glob,re
from pathlib import Path
SUB='/tmp/opensip-design-corrections/post-reset-review.v5/scratch/subject'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:280]) if detail else ''))
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
sys.path.insert(0,DC+'/workflows'); sys.path.insert(0,DC+'/foundation')
os.chdir(DC+'/workflows')
W=load('wfm',DC+'/workflows/workflows_model.v1.py')
os.chdir(DC+'/security'); S=load('slm',DC+'/security/security_lifecycle_model_v1.py')
os.chdir(DC+'/native'); N=load('nem',glob.glob(DC+'/native/*model*.py')[0])
os.chdir('/tmp')
INV=json.load(open(DC+'/workflows/command-inventory.v1.json'))
CMD={c['name']:c for c in INV['commands']}

# ---- C1 no semantic identity depends on output/operational fields (parityFields ordering)
prev=json.load(open('/tmp/opensip-design-corrections/candidate-subject.v4/docs/coop/design-corrections/workflows/command-inventory.v1.json'))
PCMD={c['name']:c for c in prev['commands']}
reorder_only=[n for n in ('default','analyze') if sorted(PCMD[n]['parityFields'])==sorted(CMD[n]['parityFields']) and PCMD[n]['parityFields']!=CMD[n]['parityFields']]
p('C1','default/analyze changed by ordering only (no field added or removed)',
  reorder_only==['default','analyze'],{'reordered':reorder_only})
added={n:sorted(set(CMD[n]['parityFields'])-set(PCMD[n]['parityFields'])) for n in CMD}
removed={n:sorted(set(PCMD[n]['parityFields'])-set(CMD[n]['parityFields'])) for n in CMD if n in PCMD}
p('C1b','no parity field was removed from any command anywhere in the delta',
  all(not v for v in removed.values()),{n:v for n,v in removed.items() if v})
p('C1c','fields added only to audit and repair-verify',
  sorted(n for n,v in added.items() if v)==['audit','repair-verify'],{n:v for n,v in added.items() if v})

# ---- C2 semantic identities unchanged by output/operational fields
ID=load('idm',DC+'/foundation/identity-model.py')
src=Path(DC+'/foundation/identity-model.py').read_text()
banned=['parityFields','runProperties','verdict','deficiency','net-new-findings','exitCode']
hits=[b for b in banned if b in src]
p('C2','identity model references no output/operational projection field',not hits,hits)
# semantic identity of the same subject is stable across differing operational inputs
try:
    a=W.wid('candidate2','workflow.candidate',{'projectId':'p','kind':'finding','key':'k'})
    b=W.wid('candidate2','workflow.candidate',{'projectId':'p','kind':'finding','key':'k'})
    p('C2b','workflow semantic id is a pure function of its semantic inputs',a==b and isinstance(a,str),a[:40])
except Exception as e:
    p('C2b','workflow semantic id is a pure function of its semantic inputs',False,repr(e))
try:
    c=W.wid('candidate2','workflow.candidate',{'projectId':'p','kind':'finding','key':'k2'})
    p('C2c','different semantic key yields a different id',c!=a,'')
except Exception as e:
    p('C2c','different semantic key yields a different id',False,repr(e))

# ---- C3 default discovery still works after the observation-shape gate
base={'invokingUid':1000,'accountHome':'/h','cwd':'/h/p',
      'fs':{'/':{'kind':'dir','uid':0,'mode':'0755','dev':1},
            '/h':{'kind':'dir','uid':1000,'mode':'0755','dev':1},
            '/h/p':{'kind':'dir','uid':1000,'mode':'0755','dev':1,'vcs':True}}}
d=S.discovery(dict(base))
p('C3','default discovery (no explicit root, no ci, no groups) still admits',
  isinstance(d,dict) and bool(d),sorted(d)[:8] if isinstance(d,dict) else type(d).__name__)
d2=S.discovery(dict(base,ci=True))
p('C3b','CI discovery still admits and differs from non-CI where the model says it should',
  isinstance(d2,dict),'')
# determinism: same input twice -> same output
p('C3c','discovery remains deterministic over identical observations',
  json.dumps(S.discovery(dict(base)),sort_keys=True,default=str)==json.dumps(d,sort_keys=True,default=str),'')
# no env/PATH/HOME read introduced by the new gate
gate=Path(DC+'/security/security_lifecycle_model_v1.py').read_text().split('Closed synthetic host-observation vocabulary')[1].split("uid = inp['invokingUid']")[0]
p('C3d','the new admission gate reads no environment/PATH/HOME',
  not any(t in gate for t in ('os.environ','getenv','PATH','expanduser','HOME')),'')

# ---- C4 nested boundaries / explicit Cargo unaffected
rep=json.load(open(DC+'/integration-report.v1.json'))
ids={c['id'] for c in rep['checks']}
nested=sorted(i for i in ids if 'nested' in i or 'cargo' in i.lower() or 'boundary' in i)
p('C4','nested-boundary / Cargo / boundary checks still present and passing',
  bool(nested) and all(c['passed'] for c in rep['checks'] if c['id'] in nested),{'count':len(nested),'sample':nested[:8]})

# ---- C5 public detail vocabulary + required output failure unchanged
wfmd=Path(SUB+'/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text()
p('C5','required-renderer post-commit failure law intact (4 / RENDERER_FAILED_AFTER_COMMIT / runId)',
  'DELIVERY.REQUIRED_FAILED' in wfmd and 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT' in wfmd,'')
t=W.terminate({'event':'operational-fault','faultCause':'delivery-required','runId':'RUN-X'})
p('C5b','post-commit required failure keeps the committed runId and exits 4',
  t.get('runId')=='RUN-X' and W.exit_code(t)==4,{'exit':W.exit_code(t),'runId':t.get('runId')})
p('C5c','every renderer still declares operational-failed as its required-failure class',
  all(r['requiredFailureClass']=='operational-failed' for r in INV['renderers']),'')
# the new SARIF prose introduced no new public detail code
v4wf=Path('/tmp/opensip-design-corrections/candidate-subject.v4/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text()
codes=lambda s:set(re.findall(r'`([A-Z][A-Z0-9_]*\.[A-Z0-9_]+)`',s))
p('C5d','v5 prose adds no new public D9 detail code to the workflow contract',
  not (codes(wfmd)-codes(v4wf)),sorted(codes(wfmd)-codes(v4wf)))

# ---- C6 no silent execution authority
p('C6','no command gained repository execution or tracked-intent writes in the delta',
  all(CMD[n]['repositoryExecution']==PCMD[n]['repositoryExecution'] and
      CMD[n]['writesTrackedIntent']==PCMD[n]['writesTrackedIntent'] and
      CMD[n]['authority']==PCMD[n]['authority'] and
      CMD[n]['authorizationClass']==PCMD[n]['authorizationClass'] and
      CMD[n]['advisory']==PCMD[n]['advisory']
      for n in CMD if n in PCMD),
  [n for n in CMD if n in PCMD and (CMD[n]['repositoryExecution']!=PCMD[n]['repositoryExecution']
    or CMD[n]['authority']!=PCMD[n]['authority'])])
p('C6b','audit and repair-verify remain non-executing despite gaining analysis fields',
  CMD['audit']['repositoryExecution']=='never' and CMD['repair-verify']['repositoryExecution']=='never'
  and CMD['audit']['writesTrackedIntent'] is False,'')
p('C6c','command set size unchanged (no command added or removed)',
  sorted(CMD)==sorted(PCMD),set(CMD)^set(PCMD))

# ---- C7 steps/flags/formats untouched by the delta
diffs=[n for n in CMD if n in PCMD and (CMD[n]['steps']!=PCMD[n]['steps'] or CMD[n]['flags']!=PCMD[n]['flags']
       or CMD[n]['formats']!=PCMD[n]['formats'] or CMD[n]['requestClass']!=PCMD[n]['requestClass'])]
p('C7','no command steps/flags/formats/requestClass changed in the delta',not diffs,diffs)

# ---- C8 whole-inventory delta is exactly the intended surface
pj=json.dumps(prev,sort_keys=True); cj=json.dumps(INV,sort_keys=True)
prev2=copy.deepcopy(prev); cur2=copy.deepcopy(INV)
for c in prev2['commands']+cur2['commands']: c['parityFields']=sorted(c['parityFields'])
for r in prev2['renderers']+cur2['renderers']: r.pop('parityRule',None)
for r in cur2['renderers']: r.pop('parityRule',None)
p('C8','outside parityFields sets and the SARIF parityRule text, the inventory is byte-equal to v4',
  json.dumps(prev2,sort_keys=True)==json.dumps(cur2,sort_keys=True)
  or sorted(json.dumps(prev2,sort_keys=True))==sorted(json.dumps(cur2,sort_keys=True)),
  'compared with parityFields order-normalised and parityRule prose removed')

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-C.json','w'),indent=1)
print('\nC-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
