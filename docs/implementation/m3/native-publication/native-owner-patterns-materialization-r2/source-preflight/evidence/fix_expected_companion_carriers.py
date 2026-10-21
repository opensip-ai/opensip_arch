"""Rebind only expected identity carriers using the published accepted recipes.
Never rewrites a verdict/cause class or historical input; operates on staged proposals.
"""
from pathlib import Path
import json,re,importlib.util,hashlib,copy
B=Path(__file__).parent/'fixture-authoring-r1';S=B/'product';P=Path('/Users/sb/code/opensip-ai/opensip')
spec=importlib.util.spec_from_file_location('reference',B/'reference.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
reports=[]
for name in ['enumeration-join','evaluator-parameter','execution-input','full-walk','import-payload','input-structure','plan-input','reconstruction','composition']:
 p=S/('crates/host/tests/fixtures/'+name+'-fixtures.native-owner-r1.json');f=json.loads(p.read_text());mapping=json.loads((B/'pooled-candidates-r1'/(name+'-identity-map.json')).read_text());changes=[]
 token=re.compile('|'.join(re.escape(k) for k,v in sorted(mapping.items(),key=lambda r:-len(r[0])) if k!=v and len(k)>=64))
 def rewrite(x,path=(),expected=False):
  if isinstance(x,dict):return {k:rewrite(v,path+(k,),expected or k in ['expected','expectedPool']) for k,v in x.items()}
  if isinstance(x,list):return [rewrite(v,path+(str(i),),expected) for i,v in enumerate(x)]
  if isinstance(x,str) and expected and path[-1] in ['typedError','error','cause']:
   value=token.sub(lambda m:mapping[m[0]],x)
   def debug(m):
    values=json.loads(m[1]);assert len(values)==32 and all(type(v) is int and 0<=v<=255 for v in values);old=bytes(values).hex();new=mapping.get(old,old);return 'MissingBlob('+str(list(bytes.fromhex(new)))+')'
   value=re.sub(r'MissingBlob\((\[[0-9, ]+\])\)',debug,value)
   if value!=x:changes.append(dict(path='/'.join(path),change='Mapped full identity/raw-digest carrier only; error class preserved'))
   return value
  return x
 f=rewrite(f)
 for key,value in f.get('expectedPool',{}).items():
  for field in ['normalized','evidence']:
   if field in value:
    before=copy.deepcopy(value[field]);value[field]=g.order_blob(value[field])
    if value[field]!=before:changes.append(dict(path='expectedPool/'+key+'/'+field,change='Published selected canonical-set ordering'))
  if 'normalized' in value and 'plan' in value['normalized'] and 'importIds' in value['normalized']['plan']:
   before=value['normalized']['plan']['importIds'];after=sorted(before)
   if before!=after:value['normalized']['plan']['importIds']=after;changes.append(dict(path='expectedPool/'+key+'/normalized/plan/importIds',change='Published Plan identity import-set order'))
  if 'evidence' in value and 'planSelectedImportIds' in value['evidence']:
   before=value['evidence']['planSelectedImportIds'];after=sorted(before)
   if before!=after:value['evidence']['planSelectedImportIds']=after;changes.append(dict(path='expectedPool/'+key+'/evidence/planSelectedImportIds',change='Published selected import identity order'))
 p.write_text(json.dumps(f,ensure_ascii=False,separators=(',',':'))+'\n');reports.append(dict(name=name,changes=changes,verdictOrCauseClassChanged=False))
p=S/'crates/host/tests/fixtures/native-context-fixtures.native-owner-r1.json';f=json.loads(p.read_text());old=json.loads((P/'crates/host/tests/fixtures/native-context-fixtures.current.json').read_text());coverage=[]
for label,case in old['coverageProducer'].items():
 if case['expected']['result']!='ADMIT':continue
 request=case['request'];descriptor=dict(schemaVersion=2,scopeId=request['scopeId'],payloadSchemaDigest=request['payloadSchemaDigest'] or g.OLD,payloadDigest=request['payloadDigest']);assert g.hid('coverage',descriptor)==case['expected']['coverageId'],label
 current=f['coverageProducer'][label];request=current['request'];descriptor=dict(schemaVersion=2,scopeId=request['scopeId'],payloadSchemaDigest=request['payloadSchemaDigest'] or g.NEW,payloadDigest=request['payloadDigest']);current['expected']['coverageId']=g.hid('coverage',descriptor);assert current['expected']['result']=='ADMIT';coverage.append(label)
p.write_text(json.dumps(f,ensure_ascii=False,separators=(',',':'))+'\n');reports.append(dict(name='native-context',oldCoverageIdsIndependentlyVerified=True,coverageExpectedIdentitiesRecomputed=coverage,verdictOrCauseClassChanged=False))
manifest=json.loads((B/'staged-companions.json').read_text())
for row in manifest['newFiles']:
 raw=(S/row['path']).read_bytes();row['candidate']=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());assert len(raw)<=4*1024*1024
(B/'staged-companions.json').write_text(json.dumps(manifest,indent=2)+'\n');(B/'expected-carrier-rebinding.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps(reports,indent=2))
