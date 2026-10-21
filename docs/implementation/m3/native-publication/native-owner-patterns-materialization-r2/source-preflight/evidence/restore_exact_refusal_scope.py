from pathlib import Path
import os,json,hashlib,shutil
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'fixture-authoring-r1';S=B/'product';W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip'
E=B/'refusal-precedence-attempt2';assert not E.exists();E.mkdir()
rel='crates/host/tests/fixtures/full-walk-fixtures.native-owner-r1.json'
for src,name in [(S/rel,'full-walk-fixtures.native-owner-r1.json'),(B/'staged-companions.json','staged-companions.json'),(B/'ordering-and-refusal-adaptations.json','ordering-and-refusal-adaptations.json'),(W/'crates/host/src/native_owner_tests.rs','native_owner_tests.rs')]:shutil.copyfile(src,E/name)
base=json.loads((B/'focused-attempt1'/rel).read_text());assert (S/rel).read_bytes()==(W/rel).read_bytes()
label='semantic-fact-payloadSchemaDigest-0';case=base['cases'][label];identity='fact2:040de0b5febbea5fbcd58829892891297b831c638ab3af28405e38448437d2f0';key=next(k for k,r in base['objectPool'].items() if r['id']==identity);assert key not in case['request']['objects']
assert case['expected']['result']=='invalid' and case['expected']['cause']=='PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT:foundation/relation-payload-schemas.v2.json'
witnesses=[]
for bk in case['request']['blobs']:
 try:obj=json.loads(bytes.fromhex(base['blobPool'][bk]['hex']))
 except (ValueError,UnicodeError):continue
 if isinstance(obj,dict) and identity in obj.get('matchingFactIds',[]):witnesses.append(dict(blobPoolKey=bk,digest=base['blobPool'][bk]['digest'],field='matchingFactIds',identity=identity))
assert witnesses
case['request']['objects'].append(key)
raw=json.dumps(base,ensure_ascii=False,separators=(',',':')).encode()+b'\n';(S/rel).write_bytes(raw);(W/rel).write_bytes(raw)
shutil.copyfile(B/'focused-attempt1/native_owner_tests.rs',W/'crates/host/src/native_owner_tests.rs')
old=json.loads((P/'crates/host/tests/fixtures/full-walk-fixtures.current.json').read_text())
assert all(c['expected']['result']==old['cases'][n]['expected']['result'] for n,c in base['cases'].items())
manifest=json.loads((B/'staged-companions.json').read_text());manifest.pop('explicitCoupledNegativePrecedenceAdaptation',None);manifest['expectedVerdictsNotRewritten']=True
retention=dict(label=label,addedExistingPoolKey=key,addedValidIdentity=identity,referencedByExistingObservation=witnesses,originalMutantStillSelected=True,oldAndNewExpected=case['expected'],authority='Published H observation matchingFactIds closure; original schema-fault mutant remains proof/view reachable. Retain the existing valid observed base fact so canonical hash order cannot turn the intended registered-document refusal into incidental missing evidence.',otherCaseSelectionsUnchanged=True)
manifest['explicitSingleFaultRetention']=retention
for row in manifest['newFiles']:
 raw=(S/row['path']).read_bytes();row['candidate']=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
(B/'staged-companions.json').write_text(json.dumps(manifest,indent=2)+'\n');(B/'final-retention-scope.json').write_text(json.dumps(dict(standing='EXPLICIT FRESH SYNTHETIC SINGLE-FAULT ISOLATION; NO VERDICT CHANGES',retention=retention,earlierUnneededEightCaseAndCoupledVerdictProposalRejectedAndPreserved=True,allOriginalFixturesPreserved=True),indent=2)+'\n');print(json.dumps(retention,indent=2))
