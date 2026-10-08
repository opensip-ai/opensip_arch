"""Design evidence only: exact schema preservation and real public carrier checks.

Usage: check.py --deps PATH [--check]. No product/architecture writes. Without
--check only evidence/audit.json next to this script is written. This executes
no security Rust validation, signatures, native projection, lexical parser,
provider, compiler, Cargo, trust fixture, or historical replay.
"""
from pathlib import Path
import sys,json,hashlib,copy,argparse
p=argparse.ArgumentParser();p.add_argument('--deps',type=Path,required=True);p.add_argument('--check',action='store_true');args=p.parse_args()
sys.path.insert(0,str(args.deps))
from jsonschema import Draft202012Validator
from referencing import Registry,Resource
D=Path(__file__).resolve().parents[1]; A=Path('/Users/sb/code/opensip-ai/opensip_arch'); P=A.parent/'opensip'
source=json.loads((D/'source.json').read_text())
def check_pin(root,row):
 b=(root/row['path']).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
for row in source['authorities']:check_pin(A,row)
for row in source['productSourcePins']:check_pin(P,row)
base=json.loads((A/'docs/implementation/m3/snapshot-plan-c/cr-1/completion/manifest-schema.completed.v1.json').read_text()); candidate=json.loads((D/'completion/manifest-schema.completed.v1.json').read_text())
without=copy.deepcopy(candidate);declaration=without['properties'].pop('closureProtocolMajor');assert without==base
assert declaration=={'type':'integer','minimum':1,'maximum':9223372036854775807}
assert candidate['required']==base['required'] and 'closureProtocolMajor' not in candidate['required']
v0=Draft202012Validator(base); v1=Draft202012Validator(candidate); Draft202012Validator.check_schema(candidate)
fixture=P/'crates/security/tests/fixtures/manifest268-shape.ndjson'; n=0; bases=[]
with fixture.open() as f:
 for line in f:
  case=json.loads(line); n+=1; assert v0.is_valid(case['value'])==case['valid'] and v1.is_valid(case['value'])==case['valid'],case['label']
  if case['valid'] and '/' not in case['label']:bases.append((case['label'],case['value']))
assert n==11010 and len(bases)==5
controls=[]; absent=0
for label,body in bases:
 for role in ['analyzer','toolchain','stdlib','rust-dev-llvm','grammar']:
  body=copy.deepcopy(body);body['role']=role
  if role!='analyzer':body.pop('commands',None);body['capabilities']=[];body['permissions']=[]
  assert v0.is_valid(body) and v1.is_valid(body); absent+=1
  for value,want in [(None,False),(False,False),(0,False),(-1,False),(1.5,False),(1,True),(9223372036854775807,True),(9223372036854775808,False)]:
   row={**body,'closureProtocolMajor':value};assert not v0.is_valid(row) and v1.is_valid(row)==want
   controls.append({'base':label,'role':role,'declaration':value,'oldReaderValid':False,'newShapeValid':want})
# A mathematical JSON Schema integer is not the raw metadata lexical domain.
assert v1.is_valid({**bases[0][1],'closureProtocolMajor':1.0})
detail=json.loads((D/'public-detail-extension.json').read_text()); new_code=detail['newPublicCode']; assert new_code=='native.closure-protocol-invalid'
registry_base=json.loads((A/detail['registryParent']['path']).read_text()); registry_new=json.loads((D/'completion/public-detail-registry.v1.json').read_text())
assert len(registry_new['records'])==len(registry_base['records'])+1
assert [r for r in registry_new['records'] if r['code']!=new_code]==registry_base['records']
for c in detail['copies']:
 root=A if c['source']['path'].startswith('docs/') else P; check_pin(root,c['source']); check_pin(D.parents[4],c['candidate'])
 before=json.loads((root/c['source']['path']).read_text());after=json.loads((D.parents[4]/c['candidate']['path']).read_text()); enum=after['$defs']['DomainDetailCode']['enum']; assert new_code in enum and new_code not in before['$defs']['DomainDetailCode']['enum']
 assert [v for v in enum if v!=new_code]==before['$defs']['DomainDetailCode']['enum']
 restored=copy.deepcopy(after);restored['$defs']['DomainDetailCode']['enum']=before['$defs']['DomainDetailCode']['enum'];restored['$defs']['DomainDetailCode']['description']=before['$defs']['DomainDetailCode']['description'];assert restored==before
common=json.loads((D/'completion/product/common-v1.schema.json').read_text()); public=Draft202012Validator({**common,'$ref':'#/$defs/StepTermination'})
schemas={};schema_pins=[]
for file in sorted((P/'schemas/sources').glob('*.json')):
 b=file.read_bytes();doc=json.loads(b);schema_pins.append({'path':file.relative_to(P).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 if '$id' in doc:schemas[doc['$id']]=doc
for n in ['common-v1.schema.json','common-v3.schema.json','common-v4.schema.json']:
 doc=json.loads((D/'completion/product'/n).read_text());schemas[doc['$id']]=doc
resolver=Registry().with_resources((key,Resource.from_contents(doc)) for key,doc in schemas.items())
envelope=json.loads((P/'schemas/sources/command-envelope-v7.schema.json').read_text()); envelope_validator=Draft202012Validator(envelope,registry=resolver)
extension=json.loads((D/'closure-protocol-routes.json').read_text()); field=json.loads((D/'manifest-field-extension.json').read_text()); existing=json.loads((P/'schemas/sources/native-v2.schema.json').read_text())['x-opensip-public-route-registry']
assert set(extension['keys']).isdisjoint(existing['keys']) and set(field['projectionGuardOrder'])==set(extension['keys'])
merged=copy.deepcopy(existing);merged['keys'].update(extension['keys']); assert {k:merged['keys'][k] for k in existing['keys']}==existing['keys']
carriers=[]
for key,row in extension['keys'].items():
 assert sorted(row['possibleOrigins'])==sorted(row['byOriginatingBoundary']) and row['originDependent'] is True
 for origin,value in row['byOriginatingBoundary'].items():
  assert value['domainDetail'] is None and value['envelopeDetail']==('HOST.INVARIANT_VIOLATED' if origin=='host-generated-internal-layer' else new_code)
  term={k:value[k] for k in ['class','errorCode','faultCause'] if k in value}
  assert public.is_valid(term),(key,origin,term,list(public.iter_errors(term)))
  wrong=copy.deepcopy(term);wrong['domainDetail']={'code':key};assert not public.is_valid(wrong)
  wrong=copy.deepcopy(term);wrong['domainDetail']=None;assert not public.is_valid(wrong)
  if origin=='host-generated-internal-layer':
   assert term=={'class':'operational-failed','errorCode':'SYSTEM.OUTCOME.ILLEGAL_STATE','faultCause':'host-invariant'}
   wrong=copy.deepcopy(term);wrong.pop('faultCause');assert not public.is_valid(wrong)
  else:assert term=={'class':'request-rejected','errorCode':'REQUEST.PRECONDITION_FAILED'}
  code=value['envelopeDetail']; error={'code':code,'remedy':extension['publicRemedies'][code],'subject':key};exit_value=4 if term['class']=='operational-failed' else 2
  whole={'schemaFamily':'opensip.product.envelope','schemaMajor':7,'kind':'failure','requestId':'req1_'+'0'*32,'termination':term,'exitCode':exit_value,'errors':[error]}
  assert envelope_validator.is_valid(whole),(key,origin,list(envelope_validator.iter_errors(whole)))
  missing=copy.deepcopy(whole);missing.pop('errors');assert not envelope_validator.is_valid(missing)
  empty=copy.deepcopy(whole);empty['errors']=[];assert not envelope_validator.is_valid(empty)
  invented=copy.deepcopy(whole);invented['errors'][0]['code']=key;assert not envelope_validator.is_valid(invented)
  null_term=copy.deepcopy(whole);null_term['termination']['domainDetail']=None;assert not envelope_validator.is_valid(null_term)
  carriers.append({'key':key,'origin':origin,'termination':term,'exitDerived':exit_value,'envelopeDetail':code,'publicSchemaValid':True,'wholeFailureEnvelopeValid':True,'requiredErrorsOmissionRejected':True,'emptyErrorsRejected':True,'internalKeyAsPublicCodeRejected':True,'inventedPublicDetailRejected':True,'nullPublicDetailRejected':True})
order=field['projectionGuardOrder'];expect=['native.closure-protocol-declaration-missing','native.closure-protocol-analyzer-mismatch','native.closure-protocol-descriptor-mismatch','native.closure-protocol-unsupported'];assert order==expect
# Cross-check explicitly authored combined failure selection against published order.
combined=[{'failures':[expect[2],expect[3]],'first':expect[2]},{'failures':[expect[1],expect[2],expect[3]],'first':expect[1]},{'failures':expect,'first':expect[0]}]
for c in combined:assert next(k for k in order if k in c['failures'])==c['first']
assert field['semanticRule']['privatePredicateDiscriminator']=='ClosureProtocolMismatch' and field['semanticRule']['inheritedCompatibilityReasonsUnchanged'] is True
report={'schemaVersion':1,'standing':'DESIGN SCHEMA/CARRIER EVIDENCE ONLY; no authenticated product projection or qualification','inheritedShapeCases':11010,'inheritedVerdictChanges':0,'absentFieldRoleControls':absent,'roleBoundaryControls':controls,'publicCarrierControls':carriers,'completeFailureEnvelopeControls':len(carriers),'newPublicDetailMembers':1,'publicCodeKeyedRemediesChecked':True,'inheritedPublicRegistryRecordsPreserved':True,'commonCopiesExactlyOneEnumAddition':len(detail['copies']),'schemaRegistrySourcePins':schema_pins,'combinedFailureSpecificationControls':combined,'routeKeysDisjointFromExisting':True,'existingRouteValuesPreserved':True,'exactOnePropertySchemaChange':True,'lexicalParserExecuted':False,'sharedSemanticValidationExecuted':False,'authenticatedProjectionExecuted':False,'historicalReplayExecuted':False,'parserRuns':0,'producerRuns':0,'fullC2aComplete':False,'productQualification':False,'fixturePin':{'path':'crates/security/tests/fixtures/manifest268-shape.ndjson','bytes':fixture.stat().st_size,'sha256':hashlib.sha256(fixture.read_bytes()).hexdigest()},'jsonSchemaIntegralFloatNote':'1.0 mathematical integer passes independent value-level shape; raw FloatForbidden is a separate existing parser duty and not executed here.'}
raw=json.dumps(report,indent=2,ensure_ascii=False)+'\n'; out=D/'evidence/audit.json'
if args.check:assert out.read_text()==raw
else:out.write_text(raw)
print(json.dumps({'inheritedShapeCases':11010,'inheritedVerdictChanges':0,'absentFieldRoleControls':absent,'boundaryControls':len(controls),'publicCarrierControls':len(carriers),'completeFailureEnvelopes':len(carriers),'newPublicDetailMembers':1,'combinedFailureSpecificationControls':len(combined),'productExecuted':False}))
