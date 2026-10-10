from pathlib import Path
import json,re,hashlib,copy
B=Path(__file__).resolve().parent;W=Path('/Users/sb/code/opensip-ai/opensip-host-native-current');P=W.parent/'opensip';changes=[]
p=W/'crates/host/tests/fixtures/execution-input-fixtures.current.json';f=json.loads(p.read_bytes());mapping=json.loads((B/'pooled-candidates-r2/execution-input-identity-map.json').read_bytes())
for case in f['cases']:
 if 'error'not in case['expected']:continue
 before=case['expected']['error']
 def rewrite(m):
  values=json.loads(m.group(1));assert len(values)==32;old=bytes(values).hex();new=mapping.get(old,old);return 'MissingBlob('+str(list(bytes.fromhex(new)))+')'
 after=re.sub(r'MissingBlob\((\[[0-9, ]+\])\)',rewrite,before);case['expected']['error']=after
 if after!=before:changes.append(dict(case=case['label'],change='MissingBlob debug byte array rebuilt from mapped raw digest',expectationKindChanged=False))
p.write_bytes(json.dumps(f,separators=(',',':')).encode()+b'\n')
p=W/'crates/host/tests/fixtures/reconstruction-fixtures.current.json';f=json.loads(p.read_bytes())
for key,value in f['expectedPool'].items():
 if 'normalized'in value:
  plan=value['normalized']['plan'];before=copy.deepcopy(plan['importIds']);plan['importIds'].sort()
  assert sorted(before)==plan['importIds'];changes.append(dict(expected=key,change='Plan importIds canonical identity-set order',expectationKindChanged=False))
p.write_bytes(json.dumps(f,separators=(',',':')).encode()+b'\n')
# This is a selected current schema positive; historical negative is retained unchanged.
p=W/'crates/host/tests/fixtures/import-payload-fixtures.current.json';f=json.loads(p.read_bytes());oldlabel='dependency-type-acquisitionSourcePath-None';newlabel='dependency-selected-acquisitionSourcePath-null';case=f['cases'].pop(oldlabel)if oldlabel in f['cases']else f['cases'].pop(newlabel);assert case['expected']['result']in ['refused','checked'];case['request']['label']=newlabel;case['expected']={'result':'checked'};f['cases'][newlabel]=case;assert len(f['cases'])==316
schema=json.loads((P/'schemas/sources/native-v2.schema.json').read_bytes());assert [r['type']for r in schema['$defs']['DependencySourcePayloadV1']['properties']['acquisitionSourcePath']['oneOf']]==['string','null']
p.write_bytes(json.dumps(f,separators=(',',':')).encode()+b'\n');changes.append(dict(originalLabel=oldlabel,currentLabel=newlabel,change='Historical negative becomes separately named fresh current positive under selected string-or-null schema; five remaining missing/invalid type refusals retained',authority='schemas/sources/native-v2.schema.json#/$defs/DependencySourcePayloadV1/properties/acquisitionSourcePath',historicalFixtureUnchanged=True))
# Coupled fault precedence follows exact canonical-set order, no successful admission.
p=W/'crates/host/tests/fixtures/full-walk-fixtures.current.json';f=json.loads(p.read_bytes());label='semantic-view-foreign-and-missing-child';case=f['cases'][label];selected={f['objectPool'][k]['id']:f['objectPool'][k]for k in case['request']['objects']};run=selected[case['request']['runId']]['descriptor'];proof=next(r['descriptor']for r in selected.values()if r['domain']=='proof-bundle');refs=proof['evaluationInputRefs'];capture=next(r for r in refs if r['domain']=='execution-inputs');foreign=next(r for r in refs if r['domain']=='view'and selected['view2:'+r['digest']]['descriptor']['planId']!=run['planId']);assert refs.index(capture)<refs.index(foreign)
blobs={f['blobPool'][k]['digest']:bytes.fromhex(f['blobPool'][k]['hex'])for k in case['request']['blobs']};capturevalue=json.loads(blobs[capture['digest']]);missing=[]
def scan(v):
 if isinstance(v,dict):
  if 'viewDigests'in v:
   missing.extend('view2:'+x for x in v['viewDigests']if 'view2:'+x not in selected)
  for x in v.values():scan(x)
 elif isinstance(v,list):
  for x in v:scan(x)
 elif isinstance(v,str)and v.startswith('view2:')and v not in selected:missing.append(v)
scan(capturevalue);assert missing and len(set(missing))==1;case['expected']={'result':'unavailable','cause':'EVIDENCE_UNAVAILABLE:'+missing[0]};assert f['cases']['semantic-view-foreign-plan']['expected']=={'result':'invalid','cause':'REFERENCE_PLAN_JOIN'}
p.write_bytes(json.dumps(f,separators=(',',':')).encode()+b'\n');changes.append(dict(case=label,change='Coupled negative still refuses; current canonical proof refs visit missing capture view before retained foreign-plan view',capturePosition=refs.index(capture),foreignPosition=refs.index(foreign),missingView=missing[0],independentForeignPlanInvalidControlRetained=True,authority='identity-model.v3.py visit/walk + current canonical identity set order',successfulAdmission=False))
(B/'reference-expectations-r3.json').write_text(json.dumps(changes,indent=2)+'\n');print(json.dumps(changes[-2:],indent=2))
