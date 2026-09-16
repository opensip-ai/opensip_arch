from pathlib import Path
import json,hashlib,copy
from jsonschema import Draft202012Validator,validators,ValidationError
r=Path(__file__).parent;arch=Path('/Users/sb/code/opensip-ai/opensip_arch');schema_path=arch/'docs/coop/completion/control-completion.schema.v3.json';cases_path=arch/'docs/coop/completion/control-completion.cases.v5.json';schema=json.loads(schema_path.read_bytes());source=json.loads(cases_path.read_bytes())
def utf8(v,limit,item,s):
 if isinstance(item,str):
  try:raw=item.encode('utf-8')
  except UnicodeError:yield ValidationError('invalid Unicode');return
  if len(raw)>limit:yield ValidationError('UTF8 length')
V=validators.extend(Draft202012Validator,{'x-maxUtf8Bytes':utf8})(schema)
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError('duplicate key')
  d[k]=v
 return d
def badfloat(_):raise ValueError('not exact integer JSON')
rows=[];seen=set();skipped=[];bases={}
def add(name,value):
 raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8');key=hashlib.sha256(raw).hexdigest()
 if key in seen:return
 seen.add(key);valid=V.is_valid(value);rows.append({'id':name,'raw':raw.decode(),'valid':valid})
 if valid:bases.setdefault(value.get('type'),value)
for case in source['cases']:
 if 'frameHex' not in case:continue
 try:
  frame=bytes.fromhex(case['frameHex']);n=int.from_bytes(frame[:4],'big')
  if len(frame)<4 or n!=len(frame)-4 or n==0:raise ValueError('framing')
  value=json.loads(frame[4:].decode('utf-8'),object_pairs_hook=pairs,parse_float=badfloat,parse_constant=badfloat)
  add(case['id'],value)
 except (ValueError,UnicodeError,RecursionError) as e:skipped.append({'id':case['id'],'reason':type(e).__name__})
for width,char in [(1,'a'),(2,'é'),(3,'界'),(4,'🦀')]:
 for count in sorted({1,127//width,128//width,128//width+1,129}):
  v=copy.deepcopy(bases['ping']);v['body']['nonce']=char*count;add('ping-utf8-'+str(width)+'-'+str(count),v)
# Ensure every current frame type has a positive representability witness.
assert set(bases)=={s['properties']['type']['const'] for s in schema['oneOf']}
(r/'cases.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(r/'positive.json').write_text(json.dumps([json.loads(x['raw']) for x in rows if x['valid']],ensure_ascii=False,indent=2)+'\n')
result={'sourcePins':[{'path':str(p.relative_to(arch)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in [schema_path,cases_path]],'uniqueCases':len(rows),'positive':sum(x['valid'] for x in rows),'negative':sum(not x['valid'] for x in rows),'frameTypes':sorted(bases),'excludedFramingLexicalCases':skipped,'scope':'exact JSON schema plus explicitly owned UTF8 keyword only; state/sequence/permission/correlation not qualified'}
(r/'corpus-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['uniqueCases','positive','negative','frameTypes']}))
