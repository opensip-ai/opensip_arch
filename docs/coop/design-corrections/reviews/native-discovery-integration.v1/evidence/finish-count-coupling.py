from pathlib import Path
import json, hashlib, subprocess, importlib.util, copy
from jsonschema.exceptions import ValidationError
B=Path('/tmp/opensip-design-corrections'); O=B/'native-discovery-integration.v1'; T=B/'claude-return-successor.v1'
spec=importlib.util.spec_from_file_location('root_canonical',T/'docs/coop/design-corrections/foundation/canonical.py'); C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
cases=[(None,'not-enumerated',True),(0,'observed-inventory',True),(2**63-1,'observed-inventory',True),(0,'not-enumerated',False),(None,'observed-inventory',False),(True,'observed-inventory',False),(2**63,'observed-inventory',False),(-1,'observed-inventory',False)]
records=[]
for rel,name in [('native/native-evidence.schemas.v2.json','PrunedTreeV2'),('security/security-lifecycle.schemas.v1.json','PrunedTreeRowV2')]:
 p=T/'docs/coop/design-corrections'/rel; old=p.read_bytes(); d=json.loads(old); before=copy.deepcopy(d)
 def run(schema):
  schema=copy.deepcopy(schema);schema['$ref']='#/$defs/'+name;rows=[]
  for count,basis,expected in cases:
   value={'path':'node_modules','reason':'dependency-tree','markerCount':count,'markerCountBasis':basis}
   try:C.validate(schema,value);accepted=True
   except (C.AdmissionError,ValidationError):accepted=False
   rows.append({'value':value,'expected':expected,'accepted':accepted})
  return rows
 previous=run(d);assert previous[3]['accepted'] and previous[4]['accepted']
 d['$defs'][name]['oneOf']=[{'properties':{'markerCountBasis':{'const':'not-enumerated'},'markerCount':{'type':'null'}}},{'properties':{'markerCountBasis':{'const':'observed-inventory'},'markerCount':{'$ref':'#/$defs/I64NonNegative'}}}]
 after=run(d);assert all(r['accepted']==r['expected'] for r in after)
 indent=1 if b'\n "$' in old or b'\n "' in old[:100] else 2
 target=O/'before-count-coupling'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(old)
 p.write_text(json.dumps(d,indent=indent,ensure_ascii=False)+'\n')
 records.append({'path':rel,'beforeSha256':hashlib.sha256(old).hexdigest(),'afterSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'before':previous,'after':after})
(O/'count-basis-controls.json').write_text(json.dumps({'standing':'Root authored schema correction; exact canonical admission controls, pending independent review','files':records},indent=2)+'\n')
print('Merged root spelling v2 with discovery v2; count/basis controls pass in both schema mirrors')
