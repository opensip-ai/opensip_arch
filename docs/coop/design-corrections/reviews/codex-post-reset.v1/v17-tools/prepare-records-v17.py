"""Prepare current routing AFTER exact coauthor/root source assent, BEFORE pins."""
from pathlib import Path
import copy, hashlib, json
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
def put(p,d):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(d,indent=2)+'\n')
def ref(p,selector=None):
 r={'path':str(p.relative_to(root)),'sha256':sha(p)}
 if selector is not None:r['selector']=selector
 return r
assessment=ev/'successor-source-assessment.v17.json';a=load(assessment)
assert a['finalSourceAssent'] is True and a['independentAcceptance'] is False
coauthor=root/a['actualCoauthorHandoff']['path'];assert sha(coauthor)==a['actualCoauthorHandoff']['sha256']
assert load(coauthor.with_name('response.json'))['is_error'] is False
additional=a['additionalFindingDispositions'];assert {'CX-BV6-01'} <= {x['id'] for x in additional}
assert all(x['status'] in ('CORRECTED-PENDING-SUCCESSOR-REVIEW','ACCOUNTED-PENDING-SUCCESSOR-REVIEW') for x in additional)
for row in a['sourceDelta']:assert sha(root/row['path'])==row['afterSha256'],row['path']
mp=dc/'reviews/candidate-subject.v16.json';assert sha(mp)=='ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9'
prior=dc/'reviews/post-reset-review.v16/review.json';review=load(prior)
blind=dc/'reviews/consumer-b.v6/output/blind-review.json';br=load(blind)
assert load(prior.with_name('response.json'))['is_error'] is False and load(blind.with_name('response.json'))['is_error'] is False
assert br['verdict']=='CHANGES_REQUIRED'
required=br['newMustIssues']+br['newShouldIssues']
assert {x['id'] for x in a['findingDispositions']}=={x['id'] for x in required}
assert all(x['status']=='CORRECTED-PENDING-SUCCESSOR-REVIEW' for x in a['findingDispositions'])
old=load(ev/'design-assent.v16.json')['advisoryApplicationAccount'];assert len(old)==52
items=copy.deepcopy(old);byid={x['id']:x for x in items};ad={x['id']:x for x in a['advisoryDispositions']}
expected={'CB6-'+x['id'] for x in br['advisories']};assert set(ad)==expected
for i,x in enumerate(br['advisories']):
 aid='CB6-'+x['id'];assert aid not in byid
 item={'id':aid,'originalId':x['id'],'originalSeverity':'ADVISORY','reviewEvidence':ref(blind,'/advisories/'+str(i)),'disposition':ad[aid],'standing':'Addressed/accounted by exact proposed successor source; independent acceptance/application pending.'}
 items.append(item);byid[aid]=item
# This is a NEW prospective account, never a rewrite of the frozen v16 account.
# Preserve as-of-v15 sourceCorrection; evolve only explicitly-current pointers and retain their history.
for aid in ['V14-ADV-1','V16-ADV-1']:
 item=byid[aid];holder=item['sourceCorrectionContext'] if aid=='V14-ADV-1' else item
 previous=copy.deepcopy(holder['currentSource'])
 holder.setdefault('historicalCurrentSourceReferences',[]).append({'asOfSubject':ref(mp),'reference':previous})
 holder['currentSource']=ref(root/previous['path'])
 holder['currentSourceStanding']='Current proposed v17 source. Prior as-of-v16 pointer preserved explicitly above; as-of-v15 original correction is historical and unchanged. Fresh successor review and application pending.'
assert len(items)==len({x['id'] for x in items})==55
put(ev/'advisory-application-account.v17.proposed.json',{'standing':'55 individually accounted advisories with original severity/history; current corrections require fresh independent acceptance.','items':items,'sourceAssessment':ref(assessment)})
put(dc/'post-reset-dispositions.v17.proposed.json',{'standing':'PROPOSED completed blind-v6 corrections; fresh independent review, NEW blind and full application remain required.','predecessorManifestSha256':sha(mp),'actualPredecessorReview':ref(prior),'predecessorVerdict':review.get('verdict',review.get('overallVerdict')),'actualBlindReview':ref(blind),'blindVerdict':br['verdict'],'items':a['findingDispositions'],'actualCoauthorHandoff':ref(coauthor),'additionalFindingDispositions':additional,'finalSourceAssessment':ref(assessment),'actualBlindRootAssessment':ref(ev/'blind-assessment.v6.json'),'advisoryAccount':'reviews/codex-post-reset.v1/advisory-application-account.v17.proposed.json','implementationAuthorized':False,'readinessChanged':False,'productQualification':False})
p=dc/'correction-crosswalk.proposed.json';before=p.read_bytes();bp=ev/'crosswalk-before-v17.json';assert not bp.exists();bp.write_bytes(before);cw=load(p)
for row in cw['items']:
 old=copy.deepcopy(row.get('latestCompletedReview'));hist=row.setdefault('historicalReviews',[])
 if old and old not in hist:hist.append(old)
 assert row['id'] in review['arDispositions']
 row['latestCompletedReview']={**ref(prior,'/arDispositions/'+row['id']),'subjectManifestSha256':sha(mp),'overallVerdict':review.get('verdict',review.get('overallVerdict')),'unresolvedMustIds':[x['id'] for x in review['newMustIssues']],'unresolvedShouldIds':[x['id'] for x in review['newShouldIssues']],'standing':'Actual v16 review preserves its literal scope. Subsequent blind v6 requires four corrections; this prior review does not accept v17 or provide blind/application grades.'}
 row['status']='AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW'
assert len(cw['items'])==16;p.write_text(json.dumps(cw,indent=2)+'\n')
put(ev/'crosswalk-update-v17.json',{'beforeSha256':hashlib.sha256(before).hexdigest(),'afterSha256':sha(p),'standing':'Updated before pins; no acceptance/readiness change.'})
p=dc/'README.md';before=p.read_bytes();bp=ev/'corrections-readme-before-v17.md';assert not bp.exists();bp.write_bytes(before)
p.write_text('''# Architecture corrections — v17 awaiting independent review

**Not ready for implementation.** Actual Claude and Codex addressed the fresh blind review's per-requirement evidence causes, TypeScript configuration-node naming, command-to-mutation mapping and coverage-partition findings. The [technical assessment](reviews/codex-post-reset.v1/technical-review.v17.md) records exact source, reference evidence and limitations, including accompanying advisories and the independently demonstrated overlapping-scope admission gap.

The intended product remains one complete design implemented in stages. These corrected bytes require fresh independent acceptance with zero unresolved MUST/SHOULD, a NEW blind consumer and complete independently reviewed application/readiness reconciliation. Historical v16 acceptance does not accept a changed successor. No product implementation, commit or push is authorized. [The resume guide](reviews/NEXT-REVIEW.md) owns current status.

## Earlier progress — historical

'''+before.decode())
print(json.dumps({'requiredDispositions':len(required),'advisories':len(items),'crosswalkRows':len(cw['items']),'acceptance':False}))
