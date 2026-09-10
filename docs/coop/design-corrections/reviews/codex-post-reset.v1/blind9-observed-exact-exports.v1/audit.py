from pathlib import Path
import json,hashlib,base64,importlib.util,shutil
P=Path(__file__).parent;R=Path('/Users/sb/code/opensip-ai/opensip_arch');S=Path('/tmp/opensip-design-corrections/candidate-subject.v21');src=Path('/tmp/opensip-design-corrections/consumer-b.v9/output/vectors')
sha=lambda b:hashlib.sha256(b).hexdigest()
mp=R/'docs/coop/design-corrections/reviews/candidate-subject.v21.json';assert sha(mp.read_bytes())=='360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1'
manifest=json.loads(mp.read_text());model=S/'docs/coop/design-corrections/foundation/identity-model.py';assert sha(model.read_bytes())==next(r['sha256'] for r in manifest['files'] if r['path']=='docs/coop/design-corrections/foundation/identity-model.py')
spec=importlib.util.spec_from_file_location('audit_v21',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
results=[]
for original in sorted(src.glob('RUN-*.json')):
 p=P/original.name;assert not p.exists();b=original.read_bytes();p.write_bytes(b);d=json.loads(b)
 blobs={h:base64.b64decode(v,validate=True) for h,v in d['blobs'].items()};assert all(sha(b)==h for h,b in blobs.items());objects={}
 for row in d['objects']:
  dom=row['domain'];desc=row['descriptor'];canon=M.C.canonical(desc);frame=b'opensip.product.v1\0'+dom.encode()+b'\0'+len(canon).to_bytes(8,'big')+canon;h=sha(frame);assert row['id'].split(':')[-1]==h;assert blobs[h]==frame
  if dom in M.PREFIX:objects[M.PREFIX[dom]+':'+h]=(dom,desc)
 rid=d['run']['id'];assert objects[rid][1]==d['run']['descriptor'];r={'label':p.stem,'exportSha256':sha(b),'runId':rid,'blobCount':len(blobs),'typedObjectCount':len(objects),'identitiesValid':True,'consumerComparison':d['comparison']}
 try:r['admittedRunId']=M.close_run(objects[rid][1],objects,blobs);r['result']='CLOSURE_ADMITTED'
 except Exception as e:r.update(result='REFUSED',exception=type(e).__name__,detail=str(e))
 results.append(r)
out={'standing':'Root audit of exact observed in-progress blind9 exports, not final review. Raw hashes/H framing and accepted source21 schema/retained-closure admission only. NOT semantic proof replay, product qualification, or rootBlindAssent. Author model used ONLY by root after independent blind construction; not supplied to blind.','parentSha256':sha(mp.read_bytes()),'modelSha256':sha(model.read_bytes()),'allRawBlobHashesValid':True,'runs':results};(P/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
