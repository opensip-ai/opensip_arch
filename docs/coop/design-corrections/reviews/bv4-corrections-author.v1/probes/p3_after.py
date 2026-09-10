"""Before/after evidence on the CORRECTED source, constructing each spelling explicitly rather
than relying on what the fixture happens to emit (the fixture itself moved, so a probe that reads
its anchors would silently compare one spelling with itself)."""
import json,sys,pathlib,copy
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from kitload import load_kit
K=load_kit(sys.argv[1]);M=K.M;C=K.C;N=K.N
out={}
def attempt(label,fn):
    try:out[label]={'admitted':True,'info':fn()}
    except Exception as exc:out[label]={'admitted':False,'error':type(exc).__name__+':'+str(exc)[:200]}
    return out[label]

def run_with_anchors(relation,path,anchors,pure=True,language='syntax'):
    kw=dict(relation=relation,has_match=True,source_path=path)
    if pure:kw.update(pure_syntax=True,universe_language='syntax')
    else:kw.update(universe_language=language)
    run,objects,blobs=K.build(**kw)
    key=next(k for k,(d,v) in objects.items() if d=='fact')
    fact=copy.deepcopy(objects[key][1])
    inventory={r['path']:r for r in objects[run['snapshotId']][1]['sourceInventory']}
    fact['anchors']=[{'path':p,'blobDigest':inventory[p]['sha256'],'startByte':0,
                      'endByte':inventory[p]['bytes']} for p in anchors]
    new=K.rekey(objects,key,fact,run)
    K.resync_witness(objects,blobs,run);K.resync_proof_refs(objects,blobs,run)
    return {'factId':new,'runId':M.close_run(run,objects,blobs)}

# The blind's exact two-descriptor counterexample, both spellings constructed explicitly.
attempt('A file@enumerated tool/main.py ANCHORED (spelling A)',
        lambda: run_with_anchors('file','tool/main.py',['tool/main.py']))
attempt('B file@enumerated tool/main.py UNANCHORED (spelling B)',
        lambda: run_with_anchors('file','tool/main.py',[]))
attempt('C file@enumerated src/lib.rs ANCHORED (supported path)',
        lambda: run_with_anchors('file','src/lib.rs',['src/lib.rs']))
attempt('D file@enumerated src/lib.rs UNANCHORED',
        lambda: run_with_anchors('file','src/lib.rs',[]))
attempt('E file@enumerated LICENSE UNANCHORED (extensionless)',
        lambda: run_with_anchors('file','LICENSE',[]))
attempt('F file@enumerated docs/extra.md UNANCHORED (data-document)',
        lambda: run_with_anchors('file','docs/extra.md',[]))
attempt('G vcs-change@vcs-reported tool/main.py ANCHORED',
        lambda: run_with_anchors('vcs-change','tool/main.py',['tool/main.py']))
attempt('H vcs-change@vcs-reported tool/main.py UNANCHORED',
        lambda: run_with_anchors('vcs-change','tool/main.py',[]))
attempt('I file@enumerated anchored into ANOTHER inventoried file (borrowed anchor)',
        lambda: run_with_anchors('file','src/lib.rs',['docs/guide.md']))
attempt('J package@manifest-declared anchored into an unrelated file (borrowed anchor)',
        lambda: run_with_anchors('package','a.ts',['a.ts'],pure=False,language='typescript'))
attempt('K package@manifest-declared UNANCHORED (control: must ADMIT)',
        lambda: run_with_anchors('package','a.ts',[],pure=False,language='typescript'))
attempt('L declares@syntactic UNANCHORED under a TYPESCRIPT universe',
        lambda: run_with_anchors('declares','a.ts',[],pure=False,language='typescript'))
attempt('M declares@syntactic UNANCHORED under a RUST universe',
        lambda: run_with_anchors('declares','src/lib.rs',[],pure=False,language='rust'))
attempt('N declares@syntactic anchored at src/lib.rs under syntax (control: must ADMIT)',
        lambda: run_with_anchors('declares','src/lib.rs',['src/lib.rs']))
attempt('O declares@syntactic anchored at tool/main.py (unsupported suffix, must REFUSE)',
        lambda: run_with_anchors('declares','tool/main.py',['tool/main.py']))
attempt('P declares@syntactic anchored at BOTH a supported and an unsupported path',
        lambda: run_with_anchors('declares','src/lib.rs',['src/lib.rs','docs/guide.md']))
attempt('Q file@enumerated `complete` with NO fact for its inventoried subject',
        lambda: M.close_run(*K.build(resolved=True,has_match=False,relation='file')))
out['identityOfTheTwoSpellings']={
 'A':out['A file@enumerated tool/main.py ANCHORED (spelling A)'].get('info',{}).get('factId'),
 'B':out['B file@enumerated tool/main.py UNANCHORED (spelling B)'].get('info',{}).get('factId')}
print(json.dumps(out,indent=1,sort_keys=True))
