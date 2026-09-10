"""Independent (Claude v12) probe: representative Run/body identities stable across v11->v12.

Harvests the identities the AUTHORED suite actually computes, by instrumenting identifier() in a
DISPOSABLE copy of each frozen tree, then compares the two multisets.
"""
import importlib.util,os,sys,json,hashlib,subprocess,shutil
BASE='/tmp/opensip-design-corrections/post-reset-review.v12/copies/identity'
os.makedirs(BASE,exist_ok=True)
HARNESS=r'''
import importlib.util,os,sys,json,hashlib
d=os.path.join(ROOT,'docs/coop/design-corrections/foundation')
sys.argv=[sys.argv[0]]
os.chdir(d)
spec=importlib.util.spec_from_file_location('M',os.path.join(d,'identity-model.py'))
M=importlib.util.module_from_spec(spec);sys.modules['M']=M;spec.loader.exec_module(M)
_orig=M.identifier
_seen=[]
def _tap(domain,value):
    r=_orig(domain,value)
    try:_seen.append(domain+'|'+ (r if isinstance(r,str) else json.dumps(r,sort_keys=True,default=str)))
    except Exception:pass
    return r
M.identifier=_tap
import runpy
sys.modules['identity_model']=M
try:
    runpy.run_path(os.path.join(d,'check-identity.py'),run_name='__main__')
except SystemExit:pass
except Exception as e:
    print(json.dumps({'error':type(e).__name__+':'+str(e)[:200],'count':len(_seen)}));raise SystemExit(0)
h=hashlib.sha256()
for s in _seen:h.update(s.encode()+b'\n')
print(json.dumps({'count':len(_seen),'distinct':len(set(_seen)),
                  'orderedDigest':h.hexdigest(),
                  'multisetDigest':hashlib.sha256('\n'.join(sorted(_seen)).encode()).hexdigest()}))
'''
res={}
for tag,root in [('v11','/tmp/opensip-design-corrections/candidate-subject.v11'),
                 ('v12','/tmp/opensip-design-corrections/candidate-subject.v12')]:
    work=os.path.join(BASE,tag)
    if os.path.exists(work):shutil.rmtree(work)
    shutil.copytree(root,work)
    script=os.path.join(BASE,'run_%s.py'%tag)
    open(script,'w').write('ROOT=%r\n'%work+HARNESS)
    p=subprocess.run(['/tmp/opensip-architecture-review-env/bin/python','-I','-B',script],
                     capture_output=True,text=True,timeout=900)
    line=[l for l in p.stdout.strip().split('\n') if l.startswith('{')]
    res[tag]=json.loads(line[-1]) if line else {'stdout':p.stdout[-500:],'stderr':p.stderr[-800:]}
print(json.dumps(res,indent=1))
if 'multisetDigest' in res.get('v11',{}) and 'multisetDigest' in res.get('v12',{}):
    print('IDENTITY MULTISET IDENTICAL:',res['v11']['multisetDigest']==res['v12']['multisetDigest'])
    print('v11 identities',res['v11']['count'],'v12 identities',res['v12']['count'])
json.dump(res,open('/tmp/opensip-design-corrections/post-reset-review.v12/probes/body-identity-result.json','w'),indent=1)
