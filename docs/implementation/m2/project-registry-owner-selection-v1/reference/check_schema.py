from pathlib import Path
import json
import jsonschema
import registry_model as m
D=Path(__file__).parent
schema=json.loads((D/'project-registry.schema.json').read_text()); jsonschema.Draft202012Validator.check_schema(schema)
v=jsonschema.Draft202012Validator(schema)
r={'projectId':'prj1-'+'0'*64,'namespaceId':'00000000-0000-4000-8000-000000000000','status':'ACTIVE','allocationKind':'random','root':{'platform':'macos','canonicalPathBytesHex':'2f','deviceId':'0','inodeId':str((1<<64)-1),'birthSeconds':-(1<<63),'birthNanoseconds':999999999}}
base={'schemaVersion':1,'entries':[r]}
assert v.is_valid(base);m.validate(base)
checks=[]
for key in r:
 wrong=json.loads(json.dumps(base));del wrong['entries'][0][key];assert not v.is_valid(wrong);checks.append('missing-entry-'+key)
for key in r['root']:
 wrong=json.loads(json.dumps(base));del wrong['entries'][0]['root'][key];assert not v.is_valid(wrong);checks.append('missing-root-'+key)
for member in ('projectId','namespaceId'):
 for suffix in ('\n','\r',' '):
  wrong=json.loads(json.dumps(base));wrong['entries'][0][member]+=suffix;assert not v.is_valid(wrong);checks.append('trailing-'+member+repr(suffix))
for obj in (base,r,r['root']):
 # Independent envelope reassembly for closed-shape checks.
 wrong=json.loads(json.dumps(base));target=wrong if obj is base else wrong['entries'][0] if obj is r else wrong['entries'][0]['root'];target['extra']=None;assert not v.is_valid(wrong);checks.append('additional-member-'+str(len(checks)))
wrong=json.loads(json.dumps(base));wrong['schemaVersion']=True;assert not v.is_valid(wrong);checks.append('schema-boolean-not-integer')
# Semantic constraints deliberately outside JSON Schema must still refuse.
for name,change in [('u64-overflow',lambda x:x['entries'][0]['root'].__setitem__('inodeId',str(1<<64))),('dot-component',lambda x:x['entries'][0]['root'].__setitem__('canonicalPathBytesHex',b'/a/../b'.hex())),('duplicate-N',lambda x:x['entries'].append(json.loads(json.dumps(r))))]:
 wrong=json.loads(json.dumps(base));change(wrong);assert v.is_valid(wrong)
 try:m.validate(wrong)
 except m.Refused:checks.append('extra-rule-'+name)
 else:raise AssertionError(name)
o=D/'schema-results.r1.json';assert not o.exists();o.write_text(json.dumps({'validator':'jsonschema Draft202012Validator','validatorModule':jsonschema.__file__,'checks':checks,'count':len(checks),'failed':0,'standing':'Schema and extra-rule checks only; not native admission'},indent=2)+'\n');print(len(checks),'checks pass')
