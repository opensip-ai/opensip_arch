ROOT='/tmp/opensip-design-corrections/post-reset-review.v12/copies/identity/v11'

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
