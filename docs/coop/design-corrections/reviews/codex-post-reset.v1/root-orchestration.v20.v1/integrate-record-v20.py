"""Prepared only; requires completed substantive root assessment of actual Claude combined peer."""
from pathlib import Path
import json,hashlib,shutil,datetime,copy
root=Path('/Users/sb/code/opensip-ai/opensip_arch');dc=root/'docs/coop/design-corrections';ev=dc/'reviews';own=ev/'codex-post-reset.v1';tmp=Path('/tmp/opensip-design-corrections');proposal=tmp/'v20-final-source.v2';src=proposal/'work'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
def ref(p,selector=None):
 r={'path':str(p.relative_to(root)),'sha256':sha(p)}
 if selector is not None:r['selector']=selector
 return r
def put(p,d):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
assessment=load(own/'coauthor-assessment.v20-combined.v1.json');assert assessment['fullRead'] and assessment['finalCombinedSourceAssent'] and not assessment['independentAcceptance']
m=load(proposal/'proposal.json');assert sha(proposal/'proposal.json')==assessment['subjectManifestSha256']
parent=ev/'candidate-subject.v19.json';assert sha(parent)=='312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b'
for row in m['files']:
 assert sha(src/row['path'])==row['afterSha256'];assert sha(root/row['path'])==row['beforeSha256']
for row in m['files']:
 for prefix,source in [('source-before-v20',root),('source-proposal-v20',src)]:
  q=own/prefix/row['path'];assert not q.exists();q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/row['path'],q)
 shutil.copyfile(src/row['path'],root/row['path'])
findings=[
 ('CB-GAP-1','MUST','At most one selected parameter per registered row, at prospective and retained boundaries and direct workflow scope binding; zero and distinct-row coexistence remain legal.'),
 ('CB-GAP-2','SHOULD','Unique capability/mode/root ownership tuple, distinct requiredness conflicts refused, existing origin-dependent public routes and correct remedies.'),
 ('CB-GAP-3','MUST','RC6 complete coverage implies exhaustive examination; preserve unknown cases and distinct resolution completeness, validate producer and retained claims.'),
 ('CB-GAP-4','SHOULD','Registered output domains at both stage selectors; explicit selected-provider operation interface, complete identity inputs and empty-set/no-authority law.'),
 ('CB-GAP-5','SHOULD','Publish existing evaluated/selected closure membership; sixdirect,twoequal,sevenother-input dependencies and deliberate extra selections. Original broad exactly-one-field premise qualified.'),
 ('CX-V20-SCHEMA-REGISTRATION','SHOULD','Enforce existing registered-schema-document law at view declarations and schema Refs; registry-derived annotation dispatch with retention first. Correct bounded native fixture digest.'),
 ('CX-V20-STAGE-REF-COMPATIBILITY','SHOULD','Replace root deep schema ref with flat Domain compatible with existing walkers; durable vocabulary agreement and actual closure controls.'),
 ('V20-ROOT-3','MUST','Register the two existing baseline-scope public details in the closed registry and mirrored enum; actual direct binder and adopt_baseline carrier/envelope controls, no emission rename.'),
 ('V20-ROOT-4','SHOULD','Route default duplicate construction through the existing ownership-tuple internal key and host-invariant route; preserve refusal/no deduplication and distinguish explicit schema-first from default guard-first paths.'),
 ('V20-ROOT-5','advisory','Keep public-code-keyed remedies; publish the shared-code truthfulness maintenance constraint and measure route/code/table composition. Text semantics still require review.'),
 ('CX-V20-SENTINEL-SUCCESS','SHOULD','Apply actual Claude final-peer sentinel correction so the positive distinguishes successful return from a Refusal with detail=None; exact authored patch and seven root helper controls plus1592passingidentitychecks.'),
 ('CX-V20-FINAL-FIXTURE','SHOULD','Refresh the native fragment schema digest after final route annotation changes, add a registered-schema fixture drift guard, and strengthen the selected-baseline positive to fail on any refusal.'),
 ('CX-V20-REVIEW-PRECISION','SHOULD','Correct optional whole-hash-input overclaim, false not-schema-decidable statement, vacuous test clause and noncompeting precedence vector; preserve historical evidence.')]
items=[{'id':i,'severity':s,'correction':c,'status':'CORRECTED-PENDING-SUCCESSOR-INDEPENDENT-REVIEW'} for i,s,c in findings]
prior=load(own/'design-assent.v19.json');advisories=copy.deepcopy(prior['advisoryApplicationAccount']);assert len(advisories)==68
blind=ev/'consumer-b.v8/output/blind-review.json';bd=load(blind)
texts=[
 'Declaration remains selected, not derived; actual unenforced registration law corrected at both declaration and schema Ref. Original root assumption explicitly superseded by advisory assessment, preserved historically.',
 'Publish existing exact evidence/Plan importIds equality; evaluated subset and finding citability stay separate, with retained/admitted unused selections.',
 'Preserve one raw-SHA content store and first-refusal semantics. One shared lost blob may mask a second join; diagnostics and finite tests do not establish only one dependency.',
 'Carry existing D9 successor-artifact obligation: selected faultCause enum12 versus inherited11 adds host-invariant under existing SYSTEM.OUTCOME.ILLEGAL_STATE; inherited bytes preserved, application must reconcile the current successor.']
for i,(row,text) in enumerate(zip(bd['advisories'],texts)):
 advisories.append({'id':row['id'],'originalSeverity':'advisory','reviewEvidence':ref(blind,'/advisories/'+str(i)),'disposition':text,'standing':'Accounted in successor; no independent/application acceptance inferred.'})
peer=ev/'v20-combined-peer.v1/assessment.json'
for i,row in enumerate(load(peer)['nonBlockingObservations']):
 advisories.append({'id':'V20-PEER-'+row['id'],'originalSeverity':'advisory','reviewEvidence':ref(peer,'/nonBlockingObservations/'+str(i)),'disposition':row['detail'],'standing':'Correct current domain subsets remain unchanged; flat duplicated enum intentionally compatibility-preserving with tested equality guard. Independent review receives both observations.'})
lastpeer=ev/'v20-final-delta-peer.v1/assessment.json'
lastobs=load(lastpeer)['observations']
for i,disposition in [(0,'Preserve the historical staging metadata as-of. The root-level temporary v20-root-augmentation.json is not among integrated source paths and is not a current semantic input; any retained historical copy keeps its original meaning.'),(1,'Leave optional line wrapping unchanged. No line-width law is violated and no semantic or implementation choice depends on wrapping.')]:
 advisories.append({'id':'V20-FINAL-PEER-OBS-'+str(i+1),'originalSeverity':lastobs[i]['severity'],'reviewEvidence':ref(lastpeer,'/observations/'+str(i)),'disposition':disposition,'standing':'Explicit nonblocking disposition; no source or readiness authority inferred.'})
assert len(advisories)==len({v['id'] for v in advisories})==76
put(own/'advisory-application-account.v20.proposed.json',{'standing':'Prospective source20 account:68 prior accepted-source advisory records preserved plus4blind8advisories and2 bounded composition-peer observations plus2 final-peer advisory/cosmetic observations. The positive informational observation remains in the peer/root evidence and calls for no action. New registration correction is required source work; no readiness grade.','items':advisories,'sourceAssessment':'successor-source-assessment.v20.json'})
coauthors=assessment['actualCoauthorHandoffs'];sessions=assessment['actualCoauthorSessions'];roots=assessment['rootCoauthorAssessments']
a={'standing':'Substantive actual-Claude/Codex agreement on exact proposed source20; not independent acceptance, blind acceptance or readiness.', 'recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finalSourceAssent':True,'independentAcceptance':False,'actualCoauthorHandoffs':coauthors,'actualCoauthorSessions':sessions,'rootCoauthorAssessments':roots,'priorIndependentReview':ref(ev/'post-reset-review.v19/review.json'),'priorRootAssessment':ref(own/'review-assessment.v19.json'),'predecessorManifest':ref(parent),'latestCompletedBlindReview':ref(blind),'latestRootBlindAssessment':ref(own/'blind-assessment.v8.json'),'sourceDelta':m['files'],'findingDispositions':items,'normativeInputAdditions':[ref(root/'docs/coop/design-corrections/native/protocol3-transitions.v1.json')],'referenceEvidence':'Pending final allsix source-pinned commands; bounded root checks referenced by combined assessment.','rootIntegrationQualifications':assessment['qualifications'],'requiredNextActs':['Final pin seal and allsix reference commands','Freeze20 and fresh independent actual Claude with zero unresolved MUST/SHOULD','NEW blind9 including complete semantic replay','Complete independently reviewed application/readiness reconciliation'],'implementationAuthorized':False,'readinessChanged':False,'productQualification':False}
put(own/'successor-source-assessment.v20.json',a)
put(dc/'post-reset-dispositions.v20.proposed.json',{'standing':'PROPOSED completed20source correction; final checks/freeze/independent/NEWblind/fullapplication remain required','predecessorManifestSha256':sha(parent),'actualPredecessorReview':ref(ev/'post-reset-review.v19/review.json'),'predecessorVerdict':'ACCEPT','predecessorRootAssent':ref(own/'design-assent.v19.json'),'latestCompletedBlindReview':ref(blind),'items':items,'actualCoauthorHandoffs':coauthors,'finalSourceAssessment':ref(own/'successor-source-assessment.v20.json'),'advisoryAccount':'reviews/codex-post-reset.v1/advisory-application-account.v20.proposed.json','implementationAuthorized':False,'readinessChanged':False,'productQualification':False})
# Current proposed crosswalk pointers change before pins. Preserve original row content in snapshot19.
p=dc/'correction-crosswalk.proposed.json';cw=load(p)
for row in cw['items']:
 row['successorCorrection20']={'sourceAssessment':ref(own/'successor-source-assessment.v20.json'),'standing':'PENDING-FRESH-INDEPENDENT20-NEWBLIND-FULLAPPLICATION; no readiness grade'}
 old=row.get('latestCompletedBlindReview')
 if old and old not in row.get('historicalBlindReviews',[]):row.setdefault('historicalBlindReviews',[]).append(old)
 row['latestCompletedBlindReview']={**ref(blind),'overallVerdict':'CHANGES_REQUIRED','rootAssessment':ref(own/'blind-assessment.v8.json'),'scopeLimitation':'Historical blind8 reconstruction has qualified claims; source20 changes require NEWblind, not retroactive acceptance.'}
p.write_text(json.dumps(cw,indent=1)+'\n')
p=dc/'README.md';old=p.read_text();(own/'README.before-v20.md').write_text(old)
p.write_text('''# Architecture corrections — source20 awaiting independent review

**Not ready for implementation.** Actual Claude and Codex corrected parameter-selection ambiguity, conflicting capability ownership and contradictory coverage claims. Stage vocabulary and closure selection are explicit; registered schema references are now enforced, and import-selection equality is documented. Baseline-scope errors now satisfy the public response schema, and default duplicate-selection errors use the registered route. The source assessment binds the exact changes and their reference limits.

These corrections belong to one complete intended design. Final source-pinned checks, fresh independent acceptance, a NEW blind consumer with complete semantic replay and complete independently reviewed application/readiness reconciliation remain required. Historical acceptance applies only to its frozen bytes. No product implementation, commit or push is authorized. [Resume guide](reviews/NEXT-REVIEW.md).

## Earlier progress — historical

'''+old)
print(json.dumps({'integratedSourceFiles':len(m['files']),'advisories':len(advisories),'sourceAssent':True,'independentAcceptance':False}))
