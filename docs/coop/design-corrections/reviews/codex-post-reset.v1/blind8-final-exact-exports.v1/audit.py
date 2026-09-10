from pathlib import Path
import json,hashlib,base64,importlib.util
P=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
mp=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v19.json')
assert sha(mp.read_bytes())=='312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b'
manifest=json.loads(mp.read_text());model=Path(manifest['snapshotRoot'])/'docs/coop/design-corrections/foundation/identity-model.py'
s=importlib.util.spec_from_file_location('audit_v19',model);M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
t=json.loads((P/'object-table.json').read_text());raw=json.loads((P/'blobs.b64.json').read_text())['blobs'];blobs={h:base64.b64decode(v,validate=True) for h,v in raw.items()}
assert all(sha(b)==h for h,b in blobs.items())
results=[]
for run in t['runs']:
 selected={r['digest']:blobs[r['digest']] for r in run['objects']};objects={}
 for row in run['objects']:
  h=row['digest'];b=selected[h];assert len(b)==row['bytes']
  if row['kind']=='h-identity':
   dom=row['domain'];desc=row['descriptor'];frame=b'opensip.product.v1\0'+dom.encode()+b'\0'+len(M.C.canonical(desc)).to_bytes(8,'big')+M.C.canonical(desc)
   assert frame==b,(run['label'],h,'descriptor/frame mismatch')
   if dom in M.PREFIX:objects[M.PREFIX[dom]+':'+h]=(dom,desc)
  elif row['kind']=='canonical-record':assert M.C.canonical(row['descriptor'])==b
 r={'label':run['label'],'runId':run['runId'],'blobCount':len(selected),'typedObjectCount':len(objects),'identitiesValid':True}
 try:r['admittedRunId']=M.close_run(objects[run['runId']][1],objects,selected);r['result']='CLOSURE_ADMITTED'
 except Exception as e:r.update(result='REFUSED',exception=type(e).__name__,detail=str(e))
 results.append(r)
out={'standing':'Exact independent export identity/schema/closure audit, NOT semantic proof replay, product qualification or blind assent.','parentSha256':sha(mp.read_bytes()),'inputs':{n:sha((P/n).read_bytes()) for n in ['object-table.json','blobs.b64.json']},'allRawBlobHashesValid':True,'distinctBlobs':len(blobs),'runs':results}
(P/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
