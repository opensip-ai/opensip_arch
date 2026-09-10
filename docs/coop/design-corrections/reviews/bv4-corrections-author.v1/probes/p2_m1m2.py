"""M1 (residual anchor questions) and M2 (cause carrier) diagnosis on ORIGINAL v13."""
import json,sys,pathlib,copy
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from kitload import load_kit
K=load_kit(sys.argv[1]);M=K.M;C=K.C;N=K.N
out={}
def attempt(label,fn):
    try:out[label]={'admitted':True,'info':fn()}
    except Exception as exc:out[label]={'admitted':False,'error':type(exc).__name__+':'+str(exc)[:220]}
    return out[label]

def remint_fact(run,objects,blobs,mutate):
    key=next(k for k,(d,v) in objects.items() if d=='fact')
    fact=copy.deepcopy(objects[key][1]);payload=C.parse(blobs[fact['payloadDigest']]);orig=fact['payloadDigest']
    mutate(fact,payload,blobs)
    if fact['payloadDigest']==orig:fact['payloadDigest']=K.put_blob(blobs,payload)
    K.rekey(objects,key,fact,run)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    w=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    w.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=K.put_blob(blobs,w),scopeIds=view['scopeIds'])
    K.rekey(objects,pk,proof,run)

def remint_coverage(run,objects,blobs,mutate):
    key=next(k for k,(d,v) in objects.items() if d=='coverage')
    coverage=copy.deepcopy(objects[key][1]);payload=C.parse(blobs[coverage['payloadDigest']])
    mutate(payload)
    coverage['payloadDigest']=K.put_blob(blobs,payload)
    K.rekey(objects,key,coverage,run)
    K.resync_witness(objects,blobs,run);K.resync_proof_refs(objects,blobs,run)

# ---------------------------------------------------------------- M1 residuals
def unanchored_under_compiler(rel,lang='typescript'):
    run,objects,blobs=K.build(universe_language=lang,relation=rel,has_match=True)
    remint_fact(run,objects,blobs,lambda f,p,b:f.update(anchors=[]))
    return M.close_run(run,objects,blobs)
attempt('M1.P declares@syntactic ZERO anchors under a TYPESCRIPT universe',
        lambda: unanchored_under_compiler('declares'))
attempt('M1.Q references@resolved-binding ZERO anchors under a TYPESCRIPT universe',
        lambda: unanchored_under_compiler('references'))
attempt('M1.R clones ZERO anchors under a TYPESCRIPT universe (cardinality 1 must bite)',
        lambda: unanchored_under_compiler('clones'))
attempt('M1.S file@enumerated ZERO anchors under a TYPESCRIPT universe',
        lambda: unanchored_under_compiler('file'))

def package_foreign_anchor():
    """A package fact whose anchor names an unrelated file. package has no anchorPathField."""
    run,objects,blobs=K.build(universe_language='typescript',relation='package',has_match=True)
    key=next(k for k,(d,v) in objects.items() if d=='fact')
    return {'anchors':objects[key][1]['anchors'],
            'payload':C.parse(blobs[objects[key][1]['payloadDigest']]),
            'run':M.close_run(run,objects,blobs)}
attempt('M1.T package@manifest-declared anchored at an UNRELATED file (arbitrary anchor)',
        package_foreign_anchor)

def complete_file_scope_with_no_fact():
    """file@enumerated Coverage claiming `complete` over an INVENTORIED subject with no fact."""
    run,objects,blobs=K.build(universe_language='typescript',relation='file',has_match=False)
    scope=next(v for d,v in objects.values() if d=='subject-scope')
    cov=next(v for d,v in objects.values() if d=='coverage')
    entry=C.parse(blobs[cov['payloadDigest']])['entry']
    M.close_run(run,objects,blobs)
    inv={r['path'] for r in next(v for d,v in objects.values() if d=='snapshot')['sourceInventory']}
    return {'subjects':scope['subjects'],'subjectsInventoried':[s for s in scope['subjects'] if s in inv],
            'coverage':entry['coverage'],'deficiency':entry['deficiency'],'facts':
            next(v for d,v in objects.values() if d=='view')['facts']}
attempt('M1.U file@enumerated `complete` over an inventoried subject with ZERO facts',
        complete_file_scope_with_no_fact)

# ---------------------------------------------------------------- M2
attempt('M2.A resolution-incomplete with nativeCause NULL (the honest RC-3 entry)',
        lambda: K.build(resolved=False,universe_language='typescript',relation='references')
                and M.close_run(*K.build(resolved=False,universe_language='typescript',relation='references')))

def cause_swap(cause,deficiency=None):
    run,objects,blobs=K.build(resolved=False,universe_language='typescript',relation='references')
    def mut(p):
        p['entry']['nativeCause']=cause
        if deficiency is not None:p['entry']['deficiency']=deficiency
    remint_coverage(run,objects,blobs,mut)
    return M.close_run(run,objects,blobs)
attempt('M2.B resolution-incomplete with an UNRELATED but schema-valid cause lockfile-missing',
        lambda: cause_swap('lockfile-missing'))
attempt('M2.C resolution-incomplete relabelled as capability-missing cause',
        lambda: cause_swap('capability-missing'))
attempt('M2.D deficiency NULL while resolutionCompleteness is partial (undisclosed)',
        lambda: cause_swap(None,deficiency=None))
attempt('M2.E deficiency swapped to external-consumers-unknown with a null cause',
        lambda: cause_swap(None,deficiency='external-consumers-unknown'))
attempt('M2.F deficiency swapped to derivation-policy-unmet with a null cause',
        lambda: cause_swap(None,deficiency='derivation-policy-unmet'))
attempt('M2.G nativeCause = computed-member-access (an unresolved-edge class)',
        lambda: cause_swap('computed-member-access'))
attempt('M2.H nativeCause = exports-open',lambda: cause_swap('exports-open'))
attempt('M2.I nativeCause = compiler-inferred',lambda: cause_swap('compiler-inferred'))
out['M2.nativeCauseMembers']=N.NATIVE_SCHEMAS['$defs']['NativeCause']['enum'] if hasattr(N,'NATIVE_SCHEMAS') else None
print(json.dumps(out,indent=1,sort_keys=True))
