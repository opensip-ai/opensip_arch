from pathlib import Path
import json,hashlib
T=Path('/tmp/opensip-design-corrections/claude-return-successor.v1')
O=Path('/tmp/opensip-design-corrections/native-discovery-integration.v1')
D=T/'docs/coop/design-corrections'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump_like(raw,obj):
 for n in (1,2,3,4):
  for ascii in (True,False):
   for suffix in ('\n',''):
    if (json.dumps(json.loads(raw),indent=n,ensure_ascii=ascii)+suffix).encode()==raw:
     return (json.dumps(obj,indent=n,ensure_ascii=ascii)+suffix).encode()
 raise AssertionError('Unrecognized JSON formatting')
rows=[]
def write(p,obj):
 raw=p.read_bytes();new=dump_like(raw,obj)
 if raw!=new:
  rel=p.relative_to(T); b=O/'before-pin-rebind'/rel;b.parent.mkdir(parents=True,exist_ok=True);assert not b.exists();b.write_bytes(raw);p.write_bytes(new)
  rows.append({'path':str(rel),'beforeSha256':hashlib.sha256(raw).hexdigest(),'afterSha256':sha(p)})
p=D/'native/native-cases.v2.json';v=json.loads(p.read_bytes());v['fixtures']['coverageView']['schemaDigests']=[sha(D/'native/native-evidence.schemas.v2.json')];write(p,v)
pins=['foundation/source-pins.v1.json','native/source-pins.v2.json','security/source-pins.v1.json','workflows/source-pins.v1.json','foundation/evaluator3-source-pins.v1.json']
for name in pins:
 p=D/name;v=json.loads(p.read_bytes());key='files' if 'files' in v else 'pins'
 for row in v[key]:
  target=T/row['path'];assert target.is_file(),target;row['sha256']=sha(target)
 write(p,v)
for name in pins:
 v=json.loads((D/name).read_bytes());key='files' if 'files' in v else 'pins'
 assert all(sha(T/r['path'])==r['sha256'] for r in v[key]),name
(O/'pin-rebinding.json').write_text(json.dumps({'standing':'Current merged reference source pins, mutable successor only','files':rows},indent=2)+'\n')
print('Rebound and verified',len(rows),'files')
