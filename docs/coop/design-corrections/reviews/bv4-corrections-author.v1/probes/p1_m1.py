"""M1 diagnosis: inventory-fact anchor law and syntax-universe representability."""
import json,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from kitload import load_kit
K=load_kit(sys.argv[1]);M=K.M;C=K.C;N=K.N
out={}
def attempt(label,fn):
    try:
        info=fn();out[label]={'admitted':True,'info':info}
    except Exception as exc:
        out[label]={'admitted':False,'error':type(exc).__name__+':'+str(exc)}
    return out[label]

import copy
def make(relation,path,anchors=None,**kw):
    """Build a pure-syntax Run and, when `anchors` is given, re-mint the fact and every record
    that names it, exactly as the kit's own fact_mutation harness does."""
    run,objects,blobs=K.build(pure_syntax=True,universe_language='syntax',relation=relation,
                              source_path=path,has_match=True,**kw)
    if anchors is not None:
        key=next(k for k,(d,v) in objects.items() if d=='fact')
        fact=copy.deepcopy(objects[key][1]);fact['anchors']=anchors(fact['anchors'])
        K.rekey(objects,key,fact,run)
        pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
        view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
        witness=K.C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
        witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
        proof['predicateProofs'][0].update(witnessDigest=K.put_blob(blobs,witness),scopeIds=view['scopeIds'])
        K.rekey(objects,pk,proof,run)
    fid=next(k for k,(d,v) in objects.items() if d=='fact')
    return run,objects,blobs,fid

def close(relation,path,anchors=None,**kw):
    run,objects,blobs,fid=make(relation,path,anchors,**kw)
    M.close_run(run,objects,blobs)
    return {'factId':fid,'runAnchors':objects[fid][1]['anchors']}

# --- the blind's exact two-descriptor counterexample, on ORIGINAL v13
attempt('M1.A file@enumerated tool/main.py WHOLE-FILE anchor',
        lambda: close('file','tool/main.py'))
attempt('M1.B file@enumerated tool/main.py ZERO anchors',
        lambda: close('file','tool/main.py',anchors=lambda a:[]))
# --- both spellings on a SUPPORTED path: are two identities admissible there too?
attempt('M1.C file@enumerated src/lib.rs WHOLE-FILE anchor',
        lambda: close('file','src/lib.rs'))
attempt('M1.D file@enumerated src/lib.rs ZERO anchors',
        lambda: close('file','src/lib.rs',anchors=lambda a:[]))
# --- the other two inventory relations on an unsupported path
attempt('M1.E vcs-change@vcs-reported tool/main.py WHOLE-FILE anchor',
        lambda: close('vcs-change','tool/main.py'))
attempt('M1.F vcs-change@vcs-reported tool/main.py ZERO anchors',
        lambda: close('vcs-change','tool/main.py',anchors=lambda a:[]))
attempt('M1.G package@manifest-declared anchored at tool/main.py',
        lambda: close('package','tool/main.py'))
attempt('M1.H package@manifest-declared ZERO anchors',
        lambda: close('package','tool/main.py',anchors=lambda a:[]))
# --- extensionless inventoried path
attempt('M1.I file@enumerated LICENSE (extensionless) WHOLE-FILE anchor',
        lambda: close('file','LICENSE'))
attempt('M1.J file@enumerated LICENSE (extensionless) ZERO anchors',
        lambda: close('file','LICENSE',anchors=lambda a:[]))
# --- CODE fact controls that MUST keep refusing
attempt('M1.K declares@syntactic ZERO anchors (must refuse: unanchored code fact)',
        lambda: close('declares','src/lib.rs',anchors=lambda a:[]))
attempt('M1.L declares@syntactic anchored at tool/main.py (must refuse: unsupported suffix)',
        lambda: close('declares','tool/main.py'))
attempt('M1.M declares@syntactic anchored at src/lib.rs (control: must ADMIT)',
        lambda: close('declares','src/lib.rs'))
attempt('M1.N clones@normalized-body-hash ZERO anchors (must refuse: cardinality 1)',
        lambda: close('clones','src/lib.rs',anchors=lambda a:[]))
# --- mismatched own path / foreign anchor on a file fact
attempt('M1.O file@enumerated whose anchor names ANOTHER inventoried path (must refuse)',
        lambda: close('file','src/lib.rs',
            anchors=lambda a:[dict(a[0],path='docs/guide.md',
                blobDigest='0'*64)]))
# --- do the two lawful spellings really differ in identity?
try:
    _,_,_,idA=make('file','tool/main.py')
    _,_,_,idB=make('file','tool/main.py',anchors=lambda a:[])
    out['M1.identitiesDiffer']={'A':idA,'B':idB,'differ':idA!=idB}
except Exception as exc:
    out['M1.identitiesDiffer']={'error':str(exc)}
# --- published-law vs model divergence at fact boundary (2)
out['M1.model_boundary2_inventory_exempt']=(
    N.syntax_capability_support([],'file','enumerated',['tool/main.py'],True) is None)
out['M1.published_boundary2_text']=N.GRAMMAR_CAPABILITY_REGISTRY['enforcementBoundaries']
print(json.dumps(out,indent=1,sort_keys=True))
