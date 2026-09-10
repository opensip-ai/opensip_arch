"""Record root's substantive released-source assessment and integrate exact agreed files."""
from pathlib import Path
import copy, hashlib, importlib.util, json, shutil
root=Path.cwd(); dc=root/'docs/coop/design-corrections'; ev=dc/'reviews/codex-post-reset.v1'
author=dc/'reviews/bv5-corrections-author.v2'; work=Path('/tmp/opensip-design-corrections/bv5-corrections-author.v2/work')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest(); load=lambda p:json.loads(p.read_text())
def ref(p):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
def put(p,d):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(d,indent=2)+'\n')
h=load(author/'handoff.json'); assert h['technicalAssent']['value'] is True
assert load(author/'response.json')['is_error'] is False
custody=load(author/'custody.json')
for row in custody['files']:
 p=author/row['path']; assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],str(p)
frozen=[]
for v,digest in [('v1','e7403b702d419f381be1cdbee7b886303fb43106b86985bc2f8ec63f5687a0ac'),('v15','5ec7928426c7a91e323240337dc382c4de32bd4e5f2626eba92c8991067b365f')]:
 mp=dc/('reviews/candidate-subject.'+v+'.json');assert sha(mp)==digest;m=load(mp)
 for row in m['files']:
  p=Path(m['snapshotRoot'])/row['path']; assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],str(p)
 frozen.append({'version':v,'manifestSha256':digest,'filesVerified':len(m['files'])})
rows=h['aggregateDeltaVsFrozenV15']['files'];assert len(rows)==11
for row in rows:
 assert sha(root/row['path'])==row['beforeSha256'],row['path']
 assert sha(work/row['path'])==row['afterSha256'],row['path']
 assert sha(author/'work'/row['path'])==row['afterSha256'],row['path']
probes=Path('/tmp/opensip-design-corrections/bv5-final-root-probes.v16');ex=load(probes/'execution.json');assert ex['executionSucceeded']
rc=load(probes/'probe-bv5-rc1-full-run.result.json')['cases']
assert rc[0]['result']=='ADMIT'
assert rc[1]['error']=='AdmissionError:SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER:unresolved-edge@enumerated'
assert all(r['error'].startswith('AdmissionError:COVERAGE_PRODUCER_ADMISSION:') and 'RC-1:' in r['error'] for r in rc[2:])
resolved=load(probes/'probe-bv5-resolved-classes.result.json')['cases'];assert resolved[0]['result']=='ADMIT'
assert resolved[1]['error'].startswith('AdmissionError:COVERAGE_PRODUCER_ADMISSION:') and 'RC-2: complete claims zero unresolved edges' in resolved[1]['error']
scope=load(probes/'probe-bv5-scope-membership.result.json')['cases'];assert scope[0]['result']=='ADMIT' and scope[0]['extraCoverageAdded'] is False
assert scope[1]['error']=='AdmissionError:SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER:unresolved-edge@enumerated'
producer=load(probes/'probe-bv5-draft-rc1.result.json')['rows'];assert producer[0]['result']['result']=='ADMIT'
assert all(r['result']['result']=='REFUSE' and r['result']['faults'][0]['fault'].startswith('RC-1:') for r in producer[1:])
# An independent root check of the effective environment gate, not a claim to run other Unicode data.
sp=importlib.util.spec_from_file_location('root_v16_fixture',work/'docs/coop/design-corrections/integration-fixtures.py');f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f);n=f.N
values=[('ES2022','es2022'),('\u0130','i\u0307'),('\u039f\u03a3','\u03bf\u03c2'),('\u00df','\u00df')]
for value,expected in values:assert n.lib_name_fold(value)==expected
original=n.UNICODE_CASE_DATA_VERSION;n.UNICODE_CASE_DATA_VERSION='root-simulated-unavailable-version'
try:
 try:n.lib_name_fold('DOM')
 except n.ReferenceEnvironmentError as error:
  assert not isinstance(error,n.AdmissionError);gate={'type':type(error).__name__,'message':str(error)}
 else:raise AssertionError('environment gate did not reject')
finally:n.UNICODE_CASE_DATA_VERSION=original
assert n.lib_name_fold('DOM')=='dom'
put(probes/'root-unicode-gate.json',{'sourceSha256':sha(work/'docs/coop/design-corrections/native/native_evidence_model.v2.py'),'measuredRuntime':n.unicodedata.unidata_version,'discriminators':[{'input':v,'expected':e,'actual':n.lib_name_fold(v)} for v,e in values],'gate':gate,'limit':'Changed the declared-version constant to simulate an unavailable binding. Did not execute an alternate Unicode implementation. ReferenceEnvironmentError is distinct from input AdmissionError; no public host exit was executed.'})
dest=ev/'bv5-final-root-probes.v16';assert not dest.exists();shutil.copytree(probes,dest)
coauthor_checks=[]
for name in ['probe_coverage_pair_and_na_law','probe_lib_fold_operation','probe_repair_guard_and_prose']:
 result=load(author/'probes'/(name+'.result.json'));assert result['ok'] and not result['failures'] and all(x['ok'] for x in result['checks'])
 coauthor_checks.append({'result':ref(author/'probes'/(name+'.result.json')),'checkRows':len(result['checks']),'scope':'Substantively read coauthor results, including prose checks and reused controls; not independent case coverage.'})
original=load(dc/'reviews/consumer-b.v5/output/blind-review.json')
dispositions={x['id']:x for x in h['originalBlindDispositions']}
def disposition(item):return {'id':item['id'],'originalSeverity':dispositions[item['id']]['originalSeverity'],'status':'CORRECTED-PENDING-SUCCESSOR-REVIEW','basis':dispositions[item['id']]['disposition'],'sourceEvidence':ref(author/'handoff.json'),'rootAssessment':'Agreed after reading the released source delta and substantive evidence; subject to fresh independent review.'}
additional=[]
for item in h['rootPointDispositions']:
 additional.append({'id':item['id'],'originalSeverity':item['severity'],'status':'ACCOUNTED-PENDING-SUCCESSOR-REVIEW' if item['id']=='CX-BV5-07' else 'CORRECTED-PENDING-SUCCESSOR-REVIEW','coauthorDisposition':item,'rootAssessment':'Agreed on final released bytes. Producer/retained scope and Coverage controls substantively assessed; prose and evidence scope read in full.'})
for item in h['coauthorNewFindingDispositions']:
 additional.append({'id':item['id'],'originalSeverity':item['originalSeverity'],'status':'ACCOUNTED-PENDING-SUCCESSOR-REVIEW' if item['id']=='BV5A-NEW-3' else 'CORRECTED-PENDING-SUCCESSOR-REVIEW','coauthorDisposition':item,'rootAssessment':'Original severity retained. NEW-1 required under CX08, including retained scopes without Coverage. NEW-2 corrected fixture plus explicit already-admitted native input assumption. NEW-3 corroborates ASCII fixture mapping only.'})
a={'standing':'Codex substantive integration/source assent to exact 11-file coauthor proposal. Fresh independent, NEW blind and application acceptance remain required.','finalSourceAssent':True,'independentAcceptance':False,'actualCoauthorHandoff':ref(author/'handoff.json'),'actualCoauthorCustody':ref(author/'custody.json'),'sourceDelta':rows,'frozenVerification':frozen,'findingDispositions':[disposition(x) for x in original['newMustIssues']+original['newShouldIssues']],'advisoryDispositions':[disposition(x) for x in original['nonblockingAdvisories']]+[disposition({'id':'V15-ADV-1'})],'additionalFindingDispositions':additional,'rootProbeExecution':ref(dest/'execution.json'),'rootProbeSemanticAssessment':{'fullRunValidControlsAdmitted':3,'fullRunInvalidCasesRefusedAtExpectedAdmissionBoundary':5,'producerControlAdmitted':1,'producerContradictionsRefused':3,'harmlessExceptionOrHarnessFailureCount':0,'meaning':'Three full-Run probes carry 8 selected case rows; repeated baseline closures are not counted as distinct tests. The root probe discards producer result on later closure exception; separately retained producer controls and coauthor rows establish that boundary. No new product host exercised.'},'rootUnicodeGate':ref(dest/'root-unicode-gate.json'),'coauthorChecks':coauthor_checks,'reportQualifications':['Full final handoff JSON/MD, assessment JSON/MD, response and released-source diff read. Coauthor assessment was written after edits; preserved honestly.','v2 report says all writes under output but discloses three transient /tmp files; scope statement is qualified by final writeCustody, not literal exclusive filesystem write custody.','Disposable final-checks directory was recreated during the turn; retention binds its final state, earlier public outputs retained.','Run identity attribution demonstrates the two measured fixture baselines: reverting only native-schema document bytes restores v1 IDs while behavioral changes remain. This does not prove every possible identity movement universally, nor identical changed semantic inputs.','Unicode discriminator cases and simulated unavailable binding checked. Native prose names the binding and disclosure; exact effective gate and distinct exception are in the referenced model. No claim that alternate case data or public fault routing was executed.','Coauthor handoff referenceControls probe file strings end in .json for three probes; actual executable sources are probes/*.py and corresponding results are *.result.json. Original handoff preserved.','v1 report precision corrections and original v5 cleared issue/history remain preserved.'],'implementationAuthorized':False,'readinessChanged':False,'productQualification':False}
put(ev/'successor-source-assessment.v16.json',a)
before=ev/'source-before-v16';assert not before.exists();before.mkdir()
for row in rows:
 p=root/row['path'];b=before/row['path'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,b)
for row in rows:
 p=root/row['path'];assert sha(p)==row['beforeSha256'];shutil.copyfile(author/'work'/row['path'],p);assert sha(p)==row['afterSha256']
put(ev/'source-integration.v16.json',{'files':rows,'sourceAssessment':ref(ev/'successor-source-assessment.v16.json'),'beforeImages':str(before.relative_to(root)),'implementationAuthorized':False})
print(json.dumps({'integrated':len(rows),'frozenVerified':frozen,'sourceAssent':True,'independentAcceptance':False}))
