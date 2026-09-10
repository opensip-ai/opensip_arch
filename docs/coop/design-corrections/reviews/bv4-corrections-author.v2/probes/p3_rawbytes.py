"""CX-BV4-CONTROLS: a zero-anchor inventory fact over raw bytes that are not source text.

An inventory claim must retain path/hash/length without anyone decoding the bytes as code or UTF8.
The negatives confirm the digest/length/path joins still bite, and the code-span laws are shown
untouched by anchoring a source-text fact into the same non-UTF8 blob."""
import copy,json,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from bounded_loader import load
f,hashes=load(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'rawbytes')
rows=[]
def record(label,fn):
    try:rows.append({'case':label,'outcome':'ADMIT','detail':fn()})
    except Exception as exc:rows.append({'case':label,'outcome':'REFUSE','error':type(exc).__name__+':'+str(exc)[:170]})

EMPTY=b''
BINARY=bytes([0x89,0x50,0x4e,0x47,0x0d,0x0a,0x1a,0x0a,0xff,0xfe,0x00,0x01,0x80,0xc0])
def inventory_run(body,path,mutate=None,relation='file'):
    """A full Run whose file@enumerated fact claims `path`, whose retained bytes are `body`."""
    run,objects,blobs=f.build(relation=relation,has_match=True,resolved=True,source_path=path)
    snap=copy.deepcopy(objects[run['snapshotId']][1])
    digest=f.put_blob(blobs,body)
    snap['sourceInventory']=sorted([r for r in snap['sourceInventory'] if r['path']!=path]+
                                   [{'path':path,'sha256':digest,'bytes':len(body)}],
                                   key=lambda r:r['path'].encode())
    vcs=f.C.parse(blobs[snap['vcsDigest']])
    vcs['sourceInventoryDigest']=f.put_blob(blobs,snap['sourceInventory'])
    snap['vcsDigest']=f.put_blob(blobs,vcs)
    f.rekey(objects,run['snapshotId'],snap,run)
    f.resync_stage_spec(objects,blobs,run)
    key=next(k for k,(d,v) in objects.items() if d=='fact')
    fact=copy.deepcopy(objects[key][1])
    payload={'path':path,'contentSha256':digest,'byteLength':len(body)}
    if mutate:mutate(payload,blobs,body)
    fact['payloadDigest']=f.put_blob(blobs,payload)
    f.rekey(objects,key,fact,run)
    f.resync_coverage(objects,blobs,run);f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
    return {'runId':f.M.close_run(run,objects,blobs),'bytes':len(body),
            'decodesAsUtf8':(lambda b:(b.decode('utf8'),True)[1] if True else None).__call__(body)
                            if _utf8(body) else False}
def _utf8(b):
    try:b.decode('utf8');return True
    except Exception:return False

record('R1 EMPTY inventoried file, zero anchors, exact digest/length',
       lambda:inventory_run(EMPTY,'assets/empty.bin'))
record('R2 NON-UTF8 BINARY inventoried file, zero anchors, exact digest/length',
       lambda:inventory_run(BINARY,'assets/logo.png'))
record('R3 binary file at an EXTENSIONLESS path',lambda:inventory_run(BINARY,'assets/blob'))
# negatives: the joins that must still bite on exactly those bytes
record('R4 binary file claiming the WRONG content digest',
       lambda:inventory_run(BINARY,'assets/logo.png',
           mutate=lambda p,b,body:p.update(contentSha256=f.put_blob(b,body+b'x'))))
record('R5 binary file claiming the WRONG byte length',
       lambda:inventory_run(BINARY,'assets/logo.png',mutate=lambda p,b,body:p.update(byteLength=len(body)+1)))
record('R6 binary file claiming a path the snapshot does not inventory',
       lambda:inventory_run(BINARY,'assets/logo.png',mutate=lambda p,b,body:p.update(path='assets/other.png')))
record('R7 empty file claiming a nonzero byte length',
       lambda:inventory_run(EMPTY,'assets/empty.bin',mutate=lambda p,b,body:p.update(byteLength=1)))
# the code-span laws are untouched: a source-text fact anchored into the same non-UTF8 blob refuses
def code_fact_into_binary():
    run,objects,blobs=f.build(relation='declares',has_match=True,resolved=True,source_path='a.ts')
    snap=copy.deepcopy(objects[run['snapshotId']][1])
    digest=f.put_blob(blobs,BINARY)
    snap['sourceInventory']=sorted(snap['sourceInventory']+[{'path':'assets/logo.png','sha256':digest,
                                                            'bytes':len(BINARY)}],
                                   key=lambda r:r['path'].encode())
    vcs=f.C.parse(blobs[snap['vcsDigest']])
    vcs['sourceInventoryDigest']=f.put_blob(blobs,snap['sourceInventory'])
    snap['vcsDigest']=f.put_blob(blobs,vcs)
    f.rekey(objects,run['snapshotId'],snap,run)
    f.resync_stage_spec(objects,blobs,run)
    key=next(k for k,(d,v) in objects.items() if d=='fact')
    fact=copy.deepcopy(objects[key][1])
    fact['anchors']=[{'path':'assets/logo.png','blobDigest':digest,'startByte':0,'endByte':len(BINARY)}]
    f.rekey(objects,key,fact,run)
    f.resync_coverage(objects,blobs,run);f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
    return {'runId':f.M.close_run(run,objects,blobs)}
record('R8 a SOURCE-TEXT fact anchored into the non-UTF8 blob (code-span law must still bite)',
       code_fact_into_binary)
print(json.dumps({'sourceHashes':hashes,'cases':rows},indent=1))
