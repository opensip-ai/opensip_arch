from pathlib import Path
import os,json,hashlib,copy,shutil,importlib.util
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'fixture-authoring-r1';S=B/'product';W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip';A=P.parent/'opensip_arch'
spec=importlib.util.spec_from_file_location('reference',B/'reference.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rel='crates/host/tests/fixtures/full-walk-fixtures.native-owner-r1.json';value=json.loads((S/rel).read_text());old=json.loads((P/'crates/host/tests/fixtures/full-walk-fixtures.current.json').read_text());assert (S/rel).read_bytes()==(W/rel).read_bytes();E=B/'all-cases-diagnostic-attempt1';E.mkdir();shutil.copyfile(S/rel,E/'full-walk-fixtures.native-owner-r1.json');shutil.copyfile(B/'staged-companions.json',E/'staged-companions.json')
changes=[]
label='semantic-file-payload-sha256-0';case=value['cases'][label];assert case['expected']['result']=='unavailable'
payloads=[]
for key in case['request']['blobs']:
 try:doc=json.loads(bytes.fromhex(value['blobPool'][key]['hex']))
 except (ValueError,UnicodeError):continue
 if isinstance(doc,dict) and set(doc)=={'byteLength','contentSha256','path','sha256'}:payloads.append((key,doc))
assert len(payloads)==1;key,mutant=payloads[0]
schema=json.loads((W/'schemas/sources/relation-payload-v2.schema.json').read_text())['$defs']['FilePayloadV1'];assert schema['additionalProperties'] is False and set(schema['properties'])=={'byteLength','contentSha256','path'}
assert set(mutant)-set(schema['properties'])=={'sha256'}
assert old['blobPool'][key]['hex']==value['blobPool'][key]['hex'],'mutant bytes must remain exact'
before=copy.deepcopy(case['expected']);case['expected']=dict(result='invalid',cause='PAYLOAD_RECORD:#/$defs/FilePayloadV1',typedRefusal='schema-mismatch')
changes.append(dict(label=label,priorMappedExpected=before,newExpected=case['expected'],mutantPoolKey=key,mutantRawDigest=value['blobPool'][key]['digest'],mutantBytesUnchanged=True,independentShapeLaw=dict(document='foundation/relation-payload-schemas.v2.json',selector='#/$defs/FilePayloadV1',additionalProperties=False,unregisteredProperty='sha256'),reason='Same malformed payload is reached before the incidental missing observed base fact under current canonical identity order; exact registered shape must refuse. No payload is repaired or admitted.'))
label='semantic-view-foreign-and-missing-child';case=value['cases'][label];before=copy.deepcopy(case['expected']);assert before['result']=='unavailable'
def order_witness(f):
 c=f['cases'][label];rows=[f['objectPool'][k] for k in c['request']['objects']];run=next(r for r in rows if r['id']==c['request']['runId']);proof=next(r for r in rows if r['domain']=='proof-bundle');foreign=[r for r in rows if r['domain']=='view' and r['descriptor']['planId']!=run['descriptor']['planId']];assert len(foreign)==1
 refs=proof['descriptor']['evaluationInputRefs'];assert refs==sorted(refs,key=g.can)
 foreign_position=next(i for i,r in enumerate(refs) if r['domain']=='view' and foreign[0]['id'].endswith(r['digest']));capture_position=next(i for i,r in enumerate(refs) if r['domain']=='execution-inputs')
 return dict(foreignView=foreign[0]['id'],foreignPlan=foreign[0]['descriptor']['planId'],selectedRunPlan=run['descriptor']['planId'],foreignPosition=foreign_position,capturePosition=capture_position)
was=order_witness(old);now=order_witness(value);assert was['capturePosition']<was['foreignPosition'] and now['foreignPosition']<now['capturePosition']
missing=before['cause'].removeprefix('EVIDENCE_UNAVAILABLE:');assert missing.startswith('view2:') and missing not in {value['objectPool'][k]['id'] for k in case['request']['objects']}
case['expected']=dict(result='invalid',cause='REFERENCE_PLAN_JOIN',typedRefusal='reference-plan-join')
assert value['cases']['semantic-view-foreign-plan']['expected']==old['cases']['semantic-view-foreign-plan']['expected']
changes.append(dict(label=label,priorMappedExpected=before,newExpected=case['expected'],oldCanonicalReferenceOrder=was,currentCanonicalReferenceOrder=now,missingChildStillAbsent=missing,missingChildNotRepaired=True,independentForeignPlanNegativeUnchanged=True,reason='Published canonical typed-reference order now visits the foreign view before execution capture with the missing child; current Plan join must refuse first.'))
raw=json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()+b'\n';(S/rel).write_bytes(raw);(W/rel).write_bytes(raw)
# Require the exact current typed failures for these two fresh cases.
p=W/'crates/host/src/native_owner_tests.rs';text=p.read_text();needle='''                if let Some(cause) = expected.get("cause") {
                    let cause = string(cause);
                    if [
                        "REFERENCE_SOURCE_JOIN",''';assert text.count(needle)==1
insert='''                if let Some(refusal) = expected.get("typedRefusal") {
                    match string(refusal) {
                        "schema-mismatch" => assert!(matches!(
                            &error,
                            opensip_evaluator::RetainedWalkError::Graph(
                                opensip_identity::GraphError::Schema(
                                    opensip_identity::SchemaAdmissionError::Mismatch
                                )
                            )
                        ), "{name}: {detail}"),
                        "reference-plan-join" => assert!(matches!(
                            &error,
                            opensip_evaluator::RetainedWalkError::Refused("REFERENCE_PLAN_JOIN")
                        ), "{name}: {detail}"),
                        other => panic!("unknown expected typed refusal: {other}"),
                    }
                }
'''
(E/'native_owner_tests.rs').write_text(text);p.write_text(text.replace(needle,insert+needle))
manifest=json.loads((B/'staged-companions.json').read_text());manifest['expectedVerdictsNotRewritten']=False;manifest['explicitCurrentRefusalAdaptations']=changes;manifest['allOtherVerdictsPreserved']=True;manifest['noSuccessfulAdmissionAdded']=True
for row in manifest['newFiles']:
 if row['path']==rel:row['candidate']=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
(B/'staged-companions.json').write_text(json.dumps(manifest,indent=2)+'\n');(B/'current-refusal-precedence.json').write_text(json.dumps(dict(standing='TWO EXPLICIT FRESH CURRENT-IDENTITY REFUSAL PRECEDENCE ADAPTATIONS; NOT PRODUCT ROUTING CHANGES',adaptations=changes,allOther524VerdictsPreserved=True,allOriginalFixturesUnchanged=True,exactTypedErrorsRequired=True,noSuccessfulAdmissionAdded=True),indent=2)+'\n');print(json.dumps(dict(refusalAdaptations=len(changes),bothRemainRefusals=True,oldViewOrder=was,currentViewOrder=now),indent=2))
