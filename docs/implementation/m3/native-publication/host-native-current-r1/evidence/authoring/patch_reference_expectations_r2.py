from pathlib import Path
import ast,types,json,hashlib,re
B=Path(__file__).resolve().parent;P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-host-native-current';src=B.parent/'host-current-corpus-r1-authoring/rebuild_replay.py';tree=ast.parse(src.read_text());nodes=[]
for n in tree.body:
 if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='original'for t in n.targets):break
 nodes.append(n)
g=types.ModuleType('recipes');g.__file__=str(src);exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),g.__dict__)
reports=[]
for name in ['execution-input','reconstruction','composition']:
 p=W/('crates/host/tests/fixtures/'+name+'-fixtures.current.json');f=json.loads(p.read_bytes());mapping=json.loads((B/'pooled-candidates-r2'/(name+'-identity-map.json')).read_bytes());changed=[]
 def rewrite_error(v,path=()):
  if isinstance(v,dict):return {k:rewrite_error(x,path+(k,))for k,x in v.items()}
  if isinstance(v,list):return [rewrite_error(x,path+(i,))for i,x in enumerate(v)]
  if isinstance(v,str)and path and path[-1]in ('typedError','error'):
   value=re.sub(r'[a-z][a-z0-9-]*[0-9]:[0-9a-f]{64}',lambda m:mapping.get(m.group(),m.group()),v)
   if value!=v:changed.append('/'.join(map(str,path)))
   return value
  return v
 f=rewrite_error(f)
 if 'expectedPool'in f:
  for key,value in f['expectedPool'].items():
   if 'normalized'in value:
    before=value['normalized'];value['normalized']=g.order_blob(before)
    if value['normalized']!=before:changed.append('expectedPool/'+key+'/normalized canonical-set ordering')
   if 'evidence'in value:value['evidence']=g.order_blob(value['evidence'])
   if 'value'in value and 'objects'in value['value']:
    for identity,row in value['value']['objects'].items():
     assert isinstance(row,list)and len(row)==2;domain,descriptor=row;canonical=g.order_identity(descriptor);assert g.hid(domain,canonical)==identity;row[1]=canonical
    changed.append('expectedPool/'+key+'/value/objects canonical identity ordering')
 p.write_bytes(json.dumps(f,ensure_ascii=False,separators=(',',':')).encode()+b'\n');reports.append(dict(name=name,changes=changed,expectationKindChanged=False))
p=W/'crates/host/tests/fixtures/native-context-fixtures.current.json';new=json.loads(p.read_bytes());old=json.loads((P/'crates/host/tests/fixtures/native-context-fixtures.json').read_bytes());changes=[]
for label,case in old['coverageProducer'].items():
 if case['expected']['result']!='ADMIT':continue
 request=case['request'];descriptor=dict(schemaVersion=2,scopeId=request['scopeId'],payloadSchemaDigest=request['payloadSchemaDigest']or g.OLD,payloadDigest=request['payloadDigest']);assert g.hid('coverage',descriptor)==case['expected']['coverageId'],label
 request=new['coverageProducer'][label]['request'];descriptor=dict(schemaVersion=2,scopeId=request['scopeId'],payloadSchemaDigest=request['payloadSchemaDigest']or g.NEW,payloadDigest=request['payloadDigest']);new['coverageProducer'][label]['expected']['coverageId']=g.hid('coverage',descriptor);changes.append(label)
p.write_bytes(json.dumps(new,ensure_ascii=False,separators=(',',':')).encode()+b'\n');reports.append(dict(name='native-context',coverageProducerExpectedIdsRederived=changes,reference='crates/evaluator/src/coverage.rs:409-427',originalIdsIndependentlyVerified=True,expectationKindChanged=False))
(B/'reference-expectations-r2.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps(reports,indent=2))
