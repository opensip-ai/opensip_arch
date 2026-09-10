"""M1 diagnosis on ORIGINAL v13: is an inventory fact over an unsupported .py path
representable under a syntax universe, and in how many lawful spellings?

Run from the foundation directory so check-identity's own loader works."""
import json,sys,pathlib,hashlib
HERE=pathlib.Path(sys.argv[1]).resolve()          # .../design-corrections/foundation
sys.path.insert(0,str(HERE))
import importlib.util
def mod(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
    sys.modules[name]=m;spec.loader.exec_module(m);return m
K=mod('checkidentity',HERE/'check-identity.py')
M=K.M;C=K.C
out={}
def attempt(label,fn):
    try:
        fn();out[label]={'admitted':True}
    except Exception as exc:
        out[label]={'admitted':False,'error':type(exc).__name__+':'+str(exc)}
    return out[label]

# ---- A: whole-file anchor (what relation_fixture builds today) on an UNSUPPORTED .py path
def readingA():
    run,objects,blobs=K.build(pure_syntax=True,universe_language='syntax',relation='file',
                              source_path='tool/main.py',has_match=True)
    out.setdefault('readingA_factIds',[k for k,v in objects.items() if v[0]=='fact'])
    M.close_run(run,objects,blobs)
attempt('A_wholeFileAnchor_py',readingA)

# ---- B: same fact with ZERO anchors
def readingB():
    run,objects,blobs=K.build(pure_syntax=True,universe_language='syntax',relation='file',
                              source_path='tool/main.py',has_match=True)
    # rebuild the single fact with anchors=[]
    fid=[k for k,v in objects.items() if v[0]=='fact'][0]
    fact=dict(objects[fid][1]);fact['anchors']=[]
    new=M.identifier('fact',fact);objects.pop(fid);objects[new]=('fact',fact)
    K.rekey(objects,fid,new,run)
    out['readingB_factId']=new
    M.close_run(run,objects,blobs)
attempt('B_unanchored_py',readingB)

# ---- C: control - whole-file anchor on a SUPPORTED .rs path (must still admit)
def controlRs():
    run,objects,blobs=K.build(pure_syntax=True,universe_language='syntax',relation='file',
                              source_path='src/lib.rs',has_match=True)
    M.close_run(run,objects,blobs)
attempt('C_wholeFileAnchor_rs_control',controlRs)

# ---- D: control - whole-file anchor on a bundled DATA path (.md)
def controlMd():
    run,objects,blobs=K.build(pure_syntax=True,universe_language='syntax',relation='file',
                              source_path='docs/extra.md',has_match=True)
    M.close_run(run,objects,blobs)
attempt('D_wholeFileAnchor_md_control',controlMd)

# ---- E: does the PUBLISHED law (registry boundary 2, prose 1.2) match the model?
import importlib.util as iu
N=K.N
out['model_inventory_exempt_at_fact_boundary']=(
    N.syntax_capability_support([], 'file','enumerated',['tool/main.py'],True) is None)
out['model_code_fact_unanchored_refused']=(
    N.syntax_capability_support([{'languageId':'rust','suffixes':['.rs']}],'declares','syntactic',[],True) is not None)
print(json.dumps(out,indent=1,sort_keys=True))
