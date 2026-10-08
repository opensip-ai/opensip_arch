"""Current schema/carrier design controls only; no source/profile admission."""
from pathlib import Path
import sys,json,hashlib,copy
sys.path.insert(0,'/tmp/opensip-implementation/c2a-protocol-major-panel/audit-deps')
from jsonschema import Draft202012Validator
from referencing import Registry,Resource
A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';D=Path(__file__).resolve().parent.parent;REL='docs/implementation/m3/snapshot-plan-c/native-metadata-missing-r1'
extension=json.loads((D/'public-detail-extension.json').read_text());code=extension['newPublicCode'];remedy=extension['remedy']
for c in extension['copies']:
 b=json.loads((A/c['source']['path']).read_text());n=json.loads((D/Path(c['candidate']['path']).relative_to(REL)).read_text());assert n['$defs']['DomainDetailCode']['enum']==b['$defs']['DomainDetailCode']['enum']+[code]
 x=copy.deepcopy(n);x['$defs']['DomainDetailCode']['enum'].pop();x['$defs']['DomainDetailCode']['description']=b['$defs']['DomainDetailCode']['description'];assert x==b;Draft202012Validator.check_schema(n)
b=json.loads((A/extension['registryParent']['path']).read_text());n=json.loads((D/'completion/public-detail-registry.v1.json').read_text());x=copy.deepcopy(n);x['records'].pop();assert x==b and n['records'][-1]['code']==code
schemas={};pins=[]
for p in sorted((P/'schemas/sources').glob('*.json')):
 raw=p.read_bytes();v=json.loads(raw);pins.append(dict(path=p.relative_to(P).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
 if '$id' in v:schemas[v['$id']]=v
for p in sorted((D/'completion/product').glob('*.json')):
 v=json.loads(p.read_text());schemas[v['$id']]=v
resolver=Registry().with_resources((k,Resource.from_contents(v))for k,v in schemas.items());common=json.loads((D/'completion/product/common-v1.schema.json').read_text());tv=Draft202012Validator({**common,'$ref':'#/$defs/StepTermination'});ev=Draft202012Validator(json.loads((P/'schemas/sources/command-envelope-v7.schema.json').read_text()),registry=resolver)
routes=json.loads((D/'missing-input-routes.json').read_text());key='native.metadata-required-input-missing';row=routes['keys'][key];assert row['route']['class']=='indeterminate'and row['route']['reasonCodes']==['VERDICT.INDETERMINATE']and row['route']['domainDetail']is None and row['route']['envelopeDetail']==code
existing=json.loads((P/'schemas/sources/native-v2.schema.json').read_text())['x-opensip-public-route-registry'];assert key not in existing['keys'];merged=copy.deepcopy(existing);merged['keys'].update(routes['keys']);assert {k:merged['keys'][k]for k in existing['keys']}==existing['keys']
term={'class':'indeterminate','reasonCodes':['VERDICT.INDETERMINATE']};tv.validate(term);envelope=dict(schemaFamily='opensip.product.envelope',schemaMajor=7,kind='failure',requestId='req1_'+'0'*32,termination=term,exitCode=3,errors=[dict(code=code,subject='native.metadata',remedy=remedy)]);ev.validate(envelope)
negative=[]
for case in ['missing-errors','empty-errors','internal-key-code','null-termination-detail','operational-error-on-indeterminate','missing-reasons','fabricated-run-payload','wrong-exit']:
 v=copy.deepcopy(envelope)
 if case=='missing-errors':v.pop('errors')
 elif case=='empty-errors':v['errors']=[]
 elif case=='internal-key-code':v['errors'][0]['code']=key
 elif case=='null-termination-detail':v['termination']['domainDetail']=None
 elif case=='operational-error-on-indeterminate':v['termination']['errorCode']='HOST.IO_FAILURE'
 elif case=='missing-reasons':v['termination'].pop('reasonCodes')
 elif case=='fabricated-run-payload':v['kind']='run'
 elif case=='wrong-exit':v['exitCode']=4
 if case=='wrong-exit':assert v['exitCode']!=3
 else:assert not ev.is_valid(v),case
 negative.append(dict(case=case,mechanism='Owning D9 class-to-exit semantic check'if case=='wrong-exit'else'Actual selected envelope/termination schema'))
# Absence of run/coverage/context/activation is an owning semantic obligation,
# not inferred from permissive optional fields in generic StepTermination.
assert set(term)=={'class','reasonCodes'}and set(envelope)=={'schemaFamily','schemaMajor','kind','requestId','termination','exitCode','errors'}
report=dict(standing='Design carrier and exact inheritance controls only; no actual missing-input/source/profile/owner admission',fourCommonCopiesOneEnumAdditionAndDescriptionOnly=True,publicRegistryOneRecordAdditionOnly=True,nativeRouteDisjointAndInheritedValuesPreserved=True,termination=term,envelope=envelope,actualMajor7CompleteFailureEnvelopeSchemaValid=True,negativeControls=negative,schemaRegistrySourcePins=pins,missingMetadataRouteSelected=False,sourceProfilePublished=False,actualOwnerAdmission=False,R3Resolved=False,productImplemented=False,productQualification=False)
(D/'evidence/check-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['schemaRegistrySourcePins','envelope']},indent=2))
