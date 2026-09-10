"""CX-BV4-DERIVATION: derivation-policy-unmet is scoped to relation=types by native 4.7 /
sufficiency_v2. Construction follows root's codex-derivation-recheck probe."""
import copy,json,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from bounded_loader import load
f,hashes=load(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'derivation')
rows=[]
def cov(relation,mutate,resolved=False):
    run,objects,blobs=f.build(resolved=resolved,has_match=True,relation=relation)
    cid=next(k for k,(d,v) in objects.items() if d=='coverage')
    coverage=copy.deepcopy(objects[cid][1]);payload=f.C.parse(blobs[coverage['payloadDigest']])
    mutate(payload['entry'])
    coverage['payloadDigest']=f.put_blob(blobs,payload);f.rekey(objects,cid,coverage,run)
    f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
    return f.M.close_run(run,objects,blobs)
def record(label,fn):
    try:rows.append({'case':label,'outcome':'ADMIT','runId':fn()})
    except Exception as exc:rows.append({'case':label,'outcome':'REFUSE','error':type(exc).__name__+':'+str(exc)[:170]})
declare=lambda e:e.update(deficiency='derivation-policy-unmet',nativeCause=None,
                          derivationKinds=['compiler-inferred'])
# root's exact pair
record('D1 derivation-policy-unmet + compiler-inferred on REFERENCES (root: invalid)',
       lambda:cov('references',declare))
record('D2 derivation-policy-unmet + compiler-inferred on TYPES (root: valid control)',
       lambda:cov('types',declare))
# the discriminating negatives that must survive the relation condition
record('D3 derivation-policy-unmet on TYPES with an EMPTY derivationKinds',
       lambda:cov('types',lambda e:e.update(deficiency='derivation-policy-unmet',nativeCause=None)))
record('D4 derivation-policy-unmet on DECLARES carrying compiler-inferred',
       lambda:cov('declares',declare))
# preservation controls the relation condition must NOT break
record('D5 compiler-inferred carried with NO deficiency (policy=any stays valid)',
       lambda:cov('types',lambda e:e.update(derivationKinds=['compiler-inferred']),resolved=True))
record('D6 types entry with compiler-inferred and a complete resolution, no deficiency',
       lambda:cov('types',lambda e:e.update(derivationKinds=['compiler-inferred'],
                                            deficiency=None,nativeCause=None),resolved=True))
print(json.dumps({'sourceHashes':hashes,'cases':rows},indent=1))
