from pathlib import Path
import json,hashlib,copy,collections
A=Path('/Users/sb/code/opensip-ai/opensip_arch');W=A.parent/'opensip-rust3-successor-takeover';p=A/'docs/coop/design-corrections/native/native-cases.v2.json';raw=p.read_bytes();d=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=='a08b8cc380a2d332a752405fde11df1d5d63b050c7297ec21820516702367ddc'
def expand(v):
 if isinstance(v,str)and v.startswith('$fixtures.'):
  result=d
  for key in v[1:].split('.'):result=result[key]
  return expand(result)
 if isinstance(v,list):return [expand(x)for x in v]
 if isinstance(v,dict):
  if '$merge'in v:
   result=copy.deepcopy(expand(v['$merge']))
   for pointer,value in v.get('$with',{}).items():
    at=result;parts=pointer.split('.')
    for key in parts[:-1]:at=at[int(key)]if isinstance(at,list)else at[key]
    if isinstance(at,list):at[int(parts[-1])]=expand(value)
    else:at[parts[-1]]=expand(value)
   return result
  return {k:expand(x)for k,x in v.items()}
 return v
views=[];shared=[]
for case in d['cases']:
 for idx,step in enumerate(case['steps']):
  fn=step['fn'];args=step.get('args',{})
  if fn=='validate'and args.get('def')in ['CoverageResultV3','ResolutionCompletenessV2']:
   shared.append(dict(caseId=case['id'],stepIndex=idx,definition=args['def'],value=expand(args['value']),expectError=step.get('expectError')))
  if args.get('language')!='rust-semantic'and fn!='protocol3_open_universe_event':continue
  if fn in ['admit_provider_hello','admit_provider_hello_ack','admit_provider_fact_batch']:
   key,name={'admit_provider_hello':('hello','Hello'),'admit_provider_hello_ack':('ack','HelloAck'),'admit_provider_fact_batch':('batch','FactBatch')}[fn];value=expand(args[key]);attribution='target-attribution-v2'in expand(args.get('negotiated_tokens',[]))
  elif fn=='provider_startup_exchange':
   frames=expand(args['frames']);first=next(x for x in frames if 'payload'in x);name=first['frame'];value=first['payload'];attribution=False
  elif fn=='protocol3_open_universe_event':name='OpenUniverse';value=expand(args['open_universe']);attribution=False
  else:continue
  def legacy(x):
   if isinstance(x,dict):return ('rustCommitHash'in x and isinstance(x['rustCommitHash'],str) and len(x['rustCommitHash'])==64)or any(legacy(v)for v in x.values())
   return isinstance(x,list)and any(legacy(v)for v in x)
  views.append(dict(caseId=case['id'],stepIndex=idx,executor=fn,frameType=name,payload=value,targetAttribution=attribution,historicalCaseKind=case['kind'],historicalExpectError=step.get('expectError'),hasLegacy64CharacterRustCommit=legacy(value),scope='Exact original literal payload/current selected shape refusal ONLY. Not a reproduction of the historical whole executor outcome, later intended diagnostic, native admission, table trace or host conversion.'))
assert len(views)==34 and len(shared)==2,(len(views),len(shared))
out=dict(standing='Historical profile incompatibility evidence, NOT34reference conformance passes. Original literal inputs preserved without padding/truncation/relabeling; current RCA-1 requires40-character compiler source commits. Private fact-vector JSON projections are not current wire carriers.',source=dict(path='docs/coop/design-corrections/native/native-cases.v2.json',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),currentAuthority=dict(path='schemas/sources/handshake-v1.schema.json',sha256=hashlib.sha256((W/'schemas/sources/handshake-v1.schema.json').read_bytes()).hexdigest(),rule='ExpectedRustIdentityV3/HelloAckV3 rustCommitHash literal40; RCA-1 forbids padding, hashing, truncation or relabeling.'),legacyLiteralViews=views,sharedSchemaRefusals=shared)
p=W/'crates/components/tests/data/native-rust3-profile-cases.v1.json';p.write_text(json.dumps(out,indent=2)+'\n');print('34 literal current-profile refusals +2shared schema negatives prepared',p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest());print(collections.Counter(x['frameType']for x in views))
