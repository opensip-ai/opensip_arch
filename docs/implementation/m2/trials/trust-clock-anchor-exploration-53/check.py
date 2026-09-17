from pathlib import Path
import importlib.util,json,copy,itertools,sys,unicodedata,lzma,hashlib
assert sys.version_info[:3]==(3,12,13)and unicodedata.unidata_version=='15.0.0'
S=Path(__file__).resolve().parent;O=S/'checks';assert not O.exists();O.mkdir()
def load(lane):
 p=S/lane/'docs/coop/design-corrections/security/security_lifecycle_model_v1.py';sp=importlib.util.spec_from_file_location('clock53_'+lane,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
P=load('parent');N=load('candidate');rows=[];changed=0
for r in json.loads((S/'parent-inputs.json').read_bytes())['files']:
 raw=(S/'parent'/r['path']).read_bytes();assert(len(raw),hashlib.sha256(raw).hexdigest())==(r['bytes'],r['sha256'])
def call(m,q):
 try:return {'value':m.clock_decision(q['record'],q['observation'],q.get('payload'),q.get('reportOnly',False))}
 except m.Reject as e:return {'rejected':str(e)}
def check(label,q):
 global changed
 saved=copy.deepcopy(q);old=call(P,q);new=call(N,q);assert q==saved
 if old!=new:
  r=q['record'];o=q['observation'];a=r['anchor'];assert r['evalHighWater']is not None and a['bootId']==o['bootId']and(type(a.get('mono'))is not int or o['mono']<a['mono'])and not q.get('reportOnly',False)
  expected=copy.deepcopy(old);assert expected['value']['decision']=='PROCEED';assert expected['value']['anchorWrite']==o;expected['value']['anchorWrite']=None;expected['value']['writes'].remove('anchor');assert expected==new;changed+=1
 if 'value'in new:
  v=new['value']
  if q.get('reportOnly')or v['decision']=='REFUSE':assert v['writes']==[]and all(v[k]is None for k in ['floorWrite','anchorWrite','lastAcceptedWrite'])
  elif v['decision']=='PROCEED':assert v['floorWrite']==v['evaluationTime']
  if v['decision']=='PROCEED'and q['record'].get('evalHighWater'):assert N.ts(v['evaluationTime'])>=N.ts(q['record']['evalHighWater'])
 rows.append({'label':label,'input':q,'parent':old,'candidate':new});return new
f=json.loads((S/'parent/docs/coop/design-corrections/security/trust-clock-cases.v1.json').read_bytes())
for c in f['cases']:
 q=copy.deepcopy(c['input']);r=q['record'];q['record']=copy.deepcopy(f['baseRecord'])if r=='$base'else({**f['baseRecord'],**{k:v for k,v in r.items()if k!='$from'}}if isinstance(r,dict)and'$from'in r else r);out=check('selected-'+c['id'],q)
 if 'expectReject'in c:assert out=={'rejected':c['expectReject']}
 else:
  for path,want in c['expect'].items():
   v=out['value']
   for part in path.split('.'):v=len(v)if part=='length'else v[int(part)]if isinstance(v,list)else v[part]
   assert v==want,(c['id'],path,v,want)
base=f['baseRecord'];epoch=P.ts(base['anchor']['wall'])
for i,(wall_delta,mono,anchor_kind,payload_kind,report)in enumerate(itertools.product([-86401,-86400,-1,0,1,86400,86401,90*86400,90*86400+1],[0,999,1000,1001,83800],['same','other','absent','malformed-string','malformed-bool'],['none','older','current','future'],[False,True])):
 r=copy.deepcopy(base);o={'wall':P.iso(epoch+wall_delta),'mono':mono,'bootId':'boot-A'}
 if anchor_kind=='other':r['anchor']['bootId']='other'
 elif anchor_kind=='absent':r['anchor']=None
 elif anchor_kind.startswith('malformed'):r['anchor']['mono']='bad'if anchor_kind.endswith('string')else True
 q={'record':r,'observation':o,'reportOnly':report}
 if payload_kind!='none':q['payload']={'newestIssuedAt':P.iso(epoch+{'older':-5*86400,'current':wall_delta,'future':wall_delta+86401}[payload_kind])}
 check('sweep-'+str(i),q)
raw=(''.join(json.dumps(r,separators=(',',':'))+'\n'for r in rows)).encode();(O/'cases.ndjson.xz').write_bytes(lzma.compress(raw));result={'selectedHandAuthoredCases':len(f['cases']),'sweepCases':len(rows)-len(f['cases']),'total':len(rows),'changedOnlyMalformedAnchorWrites':changed,'otherwiseExactParentEquality':len(rows)-changed,'inputsUnchanged':True,'reportOnlyAndRefusalNeverWrite':True,'proceedFloorEqualsEvaluation':True,'floorNeverLowers':True,'standing':'Root proposal qualification only; no independent review or selection'};(O/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
