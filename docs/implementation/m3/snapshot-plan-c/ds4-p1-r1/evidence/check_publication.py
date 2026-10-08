"""Design schema/carrier checks only; no source/owner/product admission."""
from pathlib import Path
import sys,json,copy,hashlib
sys.path.insert(0,'/tmp/opensip-implementation/c2a-protocol-major-panel/audit-deps')
from jsonschema import Draft202012Validator
from referencing import Registry,Resource
A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';D=Path(__file__).resolve().parent.parent
extension=json.loads((D/'public-detail-extension.json').read_text());code=extension['newPublicCode'];remedy=extension['remedy']
for c in extension['copies']:
 b=json.loads((A/c['source']['path']).read_text());n=json.loads((D/Path(c['candidate']['path']).relative_to('docs/implementation/m3/snapshot-plan-c/ds4-p1-r1')).read_text());assert n['$defs']['DomainDetailCode']['enum']==b['$defs']['DomainDetailCode']['enum']+[code]
 x=copy.deepcopy(n);x['$defs']['DomainDetailCode']['enum'].pop();x['$defs']['DomainDetailCode']['description']=b['$defs']['DomainDetailCode']['description'];assert x==b
 Draft202012Validator.check_schema(n)
b=json.loads((A/extension['registryParent']['path']).read_text());n=json.loads((D/'completion/public-detail-registry.v1.json').read_text());assert n['records'][:-1]==b['records'];x=copy.deepcopy(n);x['records'].pop();assert x==b
schemas={};pins=[]
for p in sorted((P/'schemas/sources').glob('*.json')):
 raw=p.read_bytes();v=json.loads(raw);pins.append({'path':p.relative_to(P).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
 if '$id' in v:schemas[v['$id']]=v
for p in sorted((D/'completion/product').glob('*.json')):
 v=json.loads(p.read_text());schemas[v['$id']]=v
resolver=Registry().with_resources((k,Resource.from_contents(v)) for k,v in schemas.items())
common=json.loads((D/'completion/product/common-v1.schema.json').read_text());termvalidator=Draft202012Validator({**common,'$ref':'#/$defs/StepTermination'});envelopevalidator=Draft202012Validator(json.loads((P/'schemas/sources/command-envelope-v7.schema.json').read_text()),registry=resolver)
routes=json.loads((D/'path-manifest-limit-routes.json').read_text());key='native.path-manifest-canonical-bound';row=routes['keys'][key];assert row['originDependent'] is False and row['route']['domainDetail'] is None and row['route']['envelopeDetail']==code
existing=json.loads((P/'schemas/sources/native-v2.schema.json').read_text())['x-opensip-public-route-registry'];assert key not in existing['keys'];merged=copy.deepcopy(existing);merged['keys'].update(routes['keys']);assert {k:merged['keys'][k] for k in existing['keys']}==existing['keys']
term={'class':'request-rejected','errorCode':'REQUEST.UNSATISFIABLE'};termvalidator.validate(term)
envelope={'schemaFamily':'opensip.product.envelope','schemaMajor':7,'kind':'failure','requestId':'req1_'+'0'*32,'termination':term,'exitCode':2,'errors':[{'code':code,'subject':key,'remedy':remedy}]};envelopevalidator.validate(envelope)
rejections=[]
for mutation in ['missing-errors','empty-errors','internal-key-code','null-termination-detail','run-envelope','wrong-exit']:
 v=copy.deepcopy(envelope)
 if mutation=='missing-errors':v.pop('errors')
 if mutation=='empty-errors':v['errors']=[]
 if mutation=='internal-key-code':v['errors'][0]['code']=key
 if mutation=='null-termination-detail':v['termination']['domainDetail']=None
 if mutation=='run-envelope':v['kind']='run'
 if mutation=='wrong-exit':v['exitCode']=4
 if mutation=='wrong-exit':
  # General schema does not derive D9 exit; this owning semantic check does.
  assert v['exitCode']!=(2 if v['termination']['class']=='request-rejected' else 4)
 else:assert not envelopevalidator.is_valid(v),mutation
 rejections.append(mutation)
f=json.loads((A/'docs/coop/design-corrections/foundation/identity-schemas.v3.json').read_text());n=json.loads((A/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text());assert json.loads((D/'schema-fragments.json').read_text())=={'SnapshotBlob':f['$defs']['Blob'],'SnapshotInventory':f['$defs']['source-inventory'],'NativeFileManifest':n['$defs']['DependencyFileManifestV1']}
report={'standing':'Exact design schema/real public carrier checks only; no source/owner admission','fourCommonCopiesOneEnumAdditionAndDescriptionOnly':True,'publicRegistryOneRecordAdditionOnly':True,'nativeRouteDisjointAndInheritedValuesPreserved':True,'threeSourceFragmentsEqualByValue':True,'termination':term,'envelope':envelope,'completeFailureEnvelopeSchemaValid':True,'negativeControls':rejections,'originsShareSameWellFormedCapacityRoute':row['possibleOrigins'],'schemaRegistrySourcePins':pins,'pathPopulationSelected':False,'sourceProfilePublished':False,'actualOwnerAdmission':False,'R3Resolved':False,'productImplemented':False,'productQualification':False}
(D/'evidence/check-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['schemaRegistrySourcePins','envelope']},indent=2))
