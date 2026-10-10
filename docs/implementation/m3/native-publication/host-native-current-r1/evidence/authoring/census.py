from pathlib import Path
import json,hashlib,ast
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';B=Path(__file__).resolve().parent;tree=ast.parse((A/'docs/coop/design-corrections/foundation/identity-model.v3.py').read_text());prefix=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='PREFIX'for t in n.targets));rows=[]
def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def hid(d,v):
 c=can(v);return prefix[d]+':'+hashlib.sha256(b'opensip.product.v1\0'+d.encode()+b'\0'+len(c).to_bytes(8,'big')+c).hexdigest()
for p in sorted((P/'crates/host/tests/fixtures').glob('*.json')):
 raw=p.read_bytes()
 if b'e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773'not in raw or p.name=='replay-fixtures.json':continue
 v=json.loads(raw);valid=[];nonmatching=[];indices=[]
 def walk(v,path):
  if isinstance(v,dict):
   if {'id','domain','descriptor'}.issubset(v)and isinstance(v['domain'],str):
    if v['domain']in prefix:
     row={'pointer':path,'id':v['id'],'domain':v['domain']};(valid if hid(v['domain'],v['descriptor'])==v['id']else nonmatching).append(row)
    else:nonmatching.append({'pointer':path,'id':v['id'],'domain':v['domain'],'unknownDomain':True})
   for k,c in v.items():
    if k in ('objectIndices','blobIndices'):indices.append({'pointer':path+'/'+k,'count':len(c)})
    if k!='hex':walk(c,path+'/'+k)
  elif isinstance(v,list):
   for i,c in enumerate(v):walk(c,path+'/'+str(i))
 walk(v,'');rows.append({'path':str(p.relative_to(P)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'matchingObjectOccurrences':len(valid),'nonmatchingObjectOccurrences':nonmatching,'indexedSelections':indices,'fixtureModified':False})
(B/'current-native-construction-census.json').write_text(json.dumps({'standing':'READONLY PUBLIC NEXT-CORPUS CONSTRUCTION CENSUS; NO CANDIDATE OR SELECTION CHANGE','fixtures':rows},indent=2)+'\n');print(json.dumps([{'path':r['path'],'objects':r['matchingObjectOccurrences'],'nonmatching':len(r['nonmatchingObjectOccurrences']),'indexedSelections':len(r['indexedSelections'])}for r in rows],indent=2))
