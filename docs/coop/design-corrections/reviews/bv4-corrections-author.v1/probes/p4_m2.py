"""M2 before/after: is a declared (deficiency, nativeCause) pair supported by the entry's own
committed evidence? Every case is a full retained Run driven through close_run."""
import json,sys,pathlib,copy
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from kitload import load_kit
K=load_kit(sys.argv[1]);M=K.M;C=K.C;N=K.N
out={}
def attempt(label,fn):
    try:out[label]={'admitted':True,'info':str(fn())[:80]}
    except Exception as exc:out[label]={'admitted':False,'error':type(exc).__name__+':'+str(exc)[:200]}

def cov(mutate,resolved=False,relation='references'):
    run,objects,blobs=K.build(resolved=resolved,has_match=True,relation=relation)
    key=next(k for k,(d,v) in objects.items() if d=='coverage')
    coverage=copy.deepcopy(objects[key][1]);payload=C.parse(blobs[coverage['payloadDigest']])
    mutate(payload['entry'])
    coverage['payloadDigest']=K.put_blob(blobs,payload)
    K.rekey(objects,key,coverage,run)
    K.resync_witness(objects,blobs,run);K.resync_proof_refs(objects,blobs,run)
    return M.close_run(run,objects,blobs)

attempt('A resolution-incomplete + null cause (honest RC entry, must ADMIT)',
        lambda: cov(lambda e:None))
attempt('B resolution-incomplete + unrelated schema-valid cause lockfile-missing',
        lambda: cov(lambda e:e.update(nativeCause='lockfile-missing')))
attempt('C resolution-incomplete relabelled generic capability-missing',
        lambda: cov(lambda e:e.update(nativeCause='capability-missing')))
attempt('D resolution-incomplete over a COMPLETE resolution',
        lambda: cov(lambda e:e.update(deficiency='resolution-incomplete'),resolved=True))
attempt('E external-consumers-unknown over exportsClosed=closed',
        lambda: cov(lambda e:e.update(deficiency='external-consumers-unknown',nativeCause=None)))
attempt('F external-consumers-unknown over exportsClosed=open (must ADMIT)',
        lambda: cov(lambda e:(e.update(deficiency='external-consumers-unknown',nativeCause=None),
                              e['closedWorld'].update(exportsClosed='open'))))
attempt('G derivation-policy-unmet with an EMPTY derivationKinds',
        lambda: cov(lambda e:e.update(deficiency='derivation-policy-unmet',nativeCause=None)))
attempt('H derivation-policy-unmet carrying compiler-inferred (must ADMIT)',
        lambda: cov(lambda e:e.update(deficiency='derivation-policy-unmet',nativeCause=None,
                                      derivationKinds=['compiler-inferred'])))
attempt('I input-closure-incomplete with a NULL cause',
        lambda: cov(lambda e:e.update(deficiency='input-closure-incomplete',nativeCause=None)))
attempt('J input-closure-incomplete borrowing capability-missing',
        lambda: cov(lambda e:e.update(deficiency='input-closure-incomplete',
                                      nativeCause='capability-missing')))
attempt('K budget-exhausted without a budget stage terminal',
        lambda: cov(lambda e:e.update(deficiency='budget-exhausted',nativeCause=None)))
attempt('L budget-exhausted with its stage terminal (must ADMIT)',
        lambda: cov(lambda e:(e.update(deficiency='budget-exhausted',nativeCause=None),
                              e['resolutionCompleteness'].update(stageTerminal='budget-exhausted'))))
attempt('M a cause with NO deficiency',
        lambda: cov(lambda e:e.update(deficiency=None,nativeCause='lockfile-missing'),resolved=True))
attempt('N language-tier-unsupported carrying a foreign cause',
        lambda: cov(lambda e:e.update(deficiency='language-tier-unsupported',
                                      nativeCause='no-program-unit')))
for _t in ('computed-member-access','exports-open','compiler-inferred'):
    attempt('X section-10 cause '+_t+' as nativeCause',
            lambda t=_t: cov(lambda e:e.update(nativeCause=t)))
print(json.dumps(out,indent=1,sort_keys=True))
