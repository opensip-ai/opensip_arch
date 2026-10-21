from pathlib import Path
import ast,types,json,hashlib,copy
from pathlib import Path
import importlib.util
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('accepted_current_recipe',B/'reference.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
P=g.P;out=B/'pooled-candidates-r1';out.mkdir(exist_ok=True);reports=[]
for name in ['enumeration-join','evaluator-parameter','execution-input','full-walk','import-payload','input-structure','plan-input','reconstruction','composition']:
 p=P/('crates/host/tests/fixtures/'+name+'-fixtures.current.json');raw=p.read_bytes();f=json.loads(raw);records=[];blobrows=[];embedded=[];valid_ids=set();invalid=[]
 def walk(v,path=()):
  if isinstance(v,dict):
   if {'id','domain','descriptor'}.issubset(v):
    valid=g.hid(v['domain'],v['descriptor'])==v['id'];records.append((path,v,valid));(valid_ids if valid else set()).add(v['id'])
    if not valid:invalid.append(path)
   elif {'domain','descriptor'}.issubset(v) and path and path[-1].startswith(tuple(x+':'for x in g.PREFIX.values())):
    row=dict(id=path[-1],domain=v['domain'],descriptor=v['descriptor']);assert g.hid(row['domain'],row['descriptor'])==row['id'];embedded.append((path,row));valid_ids.add(row['id'])
   if {'digest','hex'}.issubset(v):blobrows.append((path,v))
   if {'proofBundleId','proof'}.issubset(v) and isinstance(v['proof'],dict):
    row=dict(id=v['proofBundleId'],domain='proof-bundle',descriptor=v['proof']);assert g.hid(row['domain'],row['descriptor'])==row['id'];embedded.append((path+('proof',),row));valid_ids.add(row['id'])
   for k,x in v.items():
    if k!='hex':walk(x,path+(k,))
  elif isinstance(v,list):
   if len(v)==2 and isinstance(v[0],str)and v[0]in g.PREFIX and isinstance(v[1],dict)and path and isinstance(path[-1],str)and path[-1].startswith(g.PREFIX[v[0]]+':'):
    row=dict(id=path[-1],domain=v[0],descriptor=v[1]);assert g.hid(row['domain'],row['descriptor'])==row['id'],path;embedded.append((path,row));valid_ids.add(row['id'])
   for i,x in enumerate(v):walk(x,path+(i,))
 walk(f)
 # Expected blobs are raw-digest-to-hex maps and must be rebuilt as well.
 blobmaps=[]
 def collect_maps(v,path=()):
  if isinstance(v,dict):
   if v and all(isinstance(k,str)and len(k)==64 and isinstance(x,str)for k,x in v.items()):
    try: rows=[dict(digest=k,hex=x)for k,x in v.items()];assert all(hashlib.sha256(bytes.fromhex(r['hex'])).hexdigest()==r['digest']for r in rows)
    except (ValueError,AssertionError):pass
    else:blobmaps.append((path,rows))
   for k,x in v.items():collect_maps(x,path+(k,))
  elif isinstance(v,list):
   for i,x in enumerate(v):collect_maps(x,path+(i,))
 collect_maps(f);allblobs=[r for _,r in blobrows]+[r for _,rs in blobmaps for r in rs]
 invalid_blobs=[path for path,r in blobrows if hashlib.sha256(bytes.fromhex(r['hex'])).hexdigest()!=r['digest']]
 validblobs=[r for r in allblobs if hashlib.sha256(bytes.fromhex(r['hex'])).hexdigest()==r['digest']]
 g.mapping=dict(g.INITIAL_MAPPING)
 for iteration in range(len(records)+len(embedded)+len(allblobs)+2):
  changes={}
  for _,r,valid in records:
   if not valid:continue
   new=g.hid(r['domain'],g.order_identity(g.sub(r['descriptor'])))
   if new!=r['id']:changes[r['id']]=new;changes[r['id'].rsplit(':',1)[1]]=new.rsplit(':',1)[1]
  for _,r in embedded:
   new=g.hid(r['domain'],g.order_identity(g.sub(r['descriptor'])))
   if new!=r['id']:changes[r['id']]=new;changes[r['id'].rsplit(':',1)[1]]=new.rsplit(':',1)[1]
  for r in validblobs:
   new=hashlib.sha256(g.rebuild_blob(r)).hexdigest()
   if new!=r['digest']:changes[r['digest']]=new
  merged=dict(g.mapping,**changes)
  if merged==g.mapping:break
  g.mapping=merged
 else:raise AssertionError((name,'graph did not settle'))
 new=g.sub(copy.deepcopy(f))
 def put(path,value):
  obj=new
  for k in path[:-1]:obj=obj[g.mapping.get(k,k)if isinstance(k,str)else k]
  key=path[-1];obj[g.mapping.get(key,key)if isinstance(key,str)else key]=value
 for path,r,valid in records:
  row=g.sub(r)
  if valid:row['descriptor']=g.order_identity(row['descriptor'])
  assert (g.hid(row['domain'],row['descriptor'])==row['id'])==valid,(name,path,'fault healed or introduced')
  put(path,row)
 for path,r in embedded:
  descriptor=g.order_identity(g.sub(r['descriptor']))
  assert g.hid(r['domain'],descriptor)==g.mapping.get(r['id'],r['id'])
  if path[-1]=='proof':put(path,descriptor)
  else:
   original=f
   for k in path:original=original[k]
   put(path,[r['domain'],descriptor]if isinstance(original,list)else dict(domain=r['domain'],descriptor=descriptor))
 for path,r in blobrows:
  if path in invalid_blobs:
   row=dict(digest=g.mapping.get(r['digest'],r['digest']),hex=r['hex']);assert hashlib.sha256(bytes.fromhex(row['hex'])).hexdigest()!=row['digest'];put(path,row)
  else:
   b=g.rebuild_blob(r);put(path,dict(digest=hashlib.sha256(b).hexdigest(),hex=b.hex()))
 for path,rs in blobmaps:put(path,{hashlib.sha256(g.rebuild_blob(r)).hexdigest():g.rebuild_blob(r).hex()for r in rs})
 # Pool names are local selection keys; compact only those lookup namespaces.
 for pool,casekey in [('objectPool','objects'),('blobPool','blobs'),('expectedPool','expected')]:
  if pool not in f:continue
  keys={k:pool[0]+str(i)for i,k in enumerate(f[pool])};new[pool]={keys[k]:new[pool][g.mapping.get(k,k)]for k in f[pool]}
  pairs=zip(f['cases'].values(),new['cases'].values())if isinstance(f['cases'],dict)else zip(f['cases'],new['cases'])
  for original,case in pairs:
   if isinstance(f['cases'],dict)and casekey!='expected':original=original['request'];case=case['request']
   if casekey not in original:continue
   v=original[casekey];case[casekey]=[keys[k]for k in v]if isinstance(v,list)else keys[v]
 assert len(f['cases'])==len(new['cases'])
 if isinstance(f['cases'],dict):assert list(f['cases'])==list(new['cases'])
 else:assert [c['label']for c in f['cases']]==[c['label']for c in new['cases']]
 data=json.dumps(new,ensure_ascii=False,separators=(',',':')).encode()+b'\n';assert len(data)<=4*1024*1024,(name,len(data))
 target=out/(name+'-fixtures.native-owner-r1.json');assert not target.exists();target.write_bytes(data);assert p.read_bytes()==raw
 report=dict(name=name,standing='PRIVATE UNREVIEWED CONSTRUCTION; RUNTIME/CORRESPONDENCE NOT YET VERIFIED',originalBytes=len(raw),originalSha256=hashlib.sha256(raw).hexdigest(),candidateBytes=len(data),candidateSha256=hashlib.sha256(data).hexdigest(),cases=len(f['cases']),objectOccurrences=len(records),deliberateInvalidObjects=len(invalid),deliberateInvalidBlobs=len(invalid_blobs),expectedIdentityOccurrences=len(embedded),blobOccurrences=len(allblobs),rounds=iteration,historicalBytesUnchanged=True,objectIdentityFaultStatusPreserved=True,testsPassed=False)
 reports.append(report);(out/(name+'-identity-map.json')).write_text(json.dumps(g.mapping,indent=2)+'\n');(out/'construction-report.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps(report),flush=True)
