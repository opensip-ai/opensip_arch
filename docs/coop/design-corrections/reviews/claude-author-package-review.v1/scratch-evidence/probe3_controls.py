
import importlib.util,json
from pathlib import Path
SRC=Path('/tmp/opensip-design-corrections/candidate-subject.v25')
PKG=Path('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2')
FND=SRC/'docs/coop/design-corrections/foundation'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
CK=load('chk',PKG/'check-export.v4.py')
M=load('owner',FND/'identity-model.v3.py')
R=load('rep',FND/'evaluator_replay_model.v3.py')

def diff(a,b,path='proof'):
    out=[]
    if type(a)!=type(b):
        out.append((path,'TYPE',type(a).__name__,type(b).__name__));return out
    if isinstance(a,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a: out.append((path+'.'+k,'ONLY-IN-RECOMPUTED',None,b[k]))
            elif k not in b: out.append((path+'.'+k,'ONLY-IN-CLAIMED',a[k],None))
            else: out.extend(diff(a[k],b[k],path+'.'+k))
    elif isinstance(a,list):
        if len(a)!=len(b): out.append((path,'LEN',len(a),len(b)))
        for i,(x,y) in enumerate(zip(a,b)): out.extend(diff(x,y,path+'['+str(i)+']'))
    elif a!=b:
        out.append((path,'VALUE',a,b))
    return out

for c in json.loads((PKG/'semantic-controls1/claims.json').read_text()):
    raw=(PKG/'semantic-controls1'/c['path']).read_bytes()
    objects,blobs=CK.decode_store(raw,M,[])
    run=objects[c['runId']][1]
    print('=====',c['name'])
    rid,owner=M.open_run_closure(run,objects,blobs)
    print('  structural open_run_closure: ADMIT',rid==c['runId'])
    seal=objects[run['evaluationSealId']][1];claimed=objects[seal['proofBundleId']][1]
    res=R.derive(run['planId'],seal['executionPlanId'],seal['evaluatorClosure'],claimed['evaluationInputRefs'],objects,blobs,owner)
    d=diff(claimed,res['proof'])
    print('  differing selectors (claimed vs recomputed):',len(d))
    for sel,kind,x,y in d[:14]:
        sx=json.dumps(x)[:150];sy=json.dumps(y)[:150]
        print('   ',sel,kind)
        print('        claimed   :',sx)
        print('        recomputed:',sy)
    try:
        R.replay(run,objects,blobs);print('  replay ADMIT (UNEXPECTED)')
    except Exception as e:
        print('  replay refusal:',type(e).__name__,str(e))
