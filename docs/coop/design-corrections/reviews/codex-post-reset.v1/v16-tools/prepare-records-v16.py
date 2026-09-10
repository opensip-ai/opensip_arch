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
assessment=ev/'successor-source-assessment.v16.json';a=load(assessment)
assert a['finalSourceAssent'] is True and a['independentAcceptance'] is False
coauthor=root/a['actualCoauthorHandoff']['path'];assert sha(coauthor)==a['actualCoauthorHandoff']['sha256']
assert load(coauthor.with_name('response.json'))['is_error'] is False
additional=a['additionalFindingDispositions'];assert {f'CX-BV5-{i:02}' for i in range(1,10)} <= {x['id'] for x in additional}
assert all(x['status'] in ('CORRECTED-PENDING-SUCCESSOR-REVIEW','ACCOUNTED-PENDING-SUCCESSOR-REVIEW') for x in additional)
for row in a['sourceDelta']:assert sha(root/row['path'])==row['afterSha256'],row['path']
mp=dc/'reviews/candidate-subject.v15.json';assert sha(mp)=='5ec7928426c7a91e323240337dc382c4de32bd4e5f2626eba92c8991067b365f'
prior=dc/'reviews/post-reset-review.v15/review.json';review=load(prior)
blind=dc/'reviews/consumer-b.v5/output/blind-review.json';br=load(blind)
assert load(prior.with_name('response.json'))['is_error'] is False and load(blind.with_name('response.json'))['is_error'] is False
assert br['verdict']=='CHANGES_REQUIRED'
required=br['newMustIssues']+br['newShouldIssues']
assert {x['id'] for x in a['findingDispositions']}=={x['id'] for x in required}
assert all(x['status']=='CORRECTED-PENDING-SUCCESSOR-REVIEW' for x in a['findingDispositions'])
old=load(ev/'design-assent.v15.json')['advisoryApplicationAccount'];assert len(old)==46
items=copy.deepcopy(old);byid={x['id']:x for x in items};ad={x['id']:x for x in a['advisoryDispositions']}
expected={x['id'] for x in br['nonblockingAdvisories']}|{'V15-ADV-1'};assert set(ad)==expected
for i,x in enumerate(br['nonblockingAdvisories']):
 assert x['id'] not in byid
 item={'id':x['id'],'originalSeverity':'ADVISORY','reviewEvidence':ref(blind,'/nonblockingAdvisories/'+str(i)),'disposition':ad[x['id']],'standing':'Addressed by exact proposed successor source; independent acceptance/application pending.'}
 items.append(item);byid[x['id']]=item
byid['V15-ADV-1']['successorCorrection']=ad['V15-ADV-1']
assert len(items)==len({x['id'] for x in items})==50
put(ev/'advisory-application-account.v16.proposed.json',{'standing':'50 individually accounted advisories with original severity/history; current corrections require fresh independent acceptance.','items':items,'sourceAssessment':ref(assessment)})
put(dc/'post-reset-dispositions.v16.proposed.json',{'standing':'PROPOSED completed blind-v5 corrections; fresh independent review, NEW blind and full application remain required.','predecessorManifestSha256':sha(mp),'actualPredecessorReview':ref(prior),'predecessorVerdict':review.get('verdict',review.get('overallVerdict')),'actualBlindReview':ref(blind),'blindVerdict':br['verdict'],'items':a['findingDispositions'],'actualCoauthorHandoff':ref(coauthor),'additionalFindingDispositions':additional,'finalSourceAssessment':ref(assessment),'actualBlindRootAssessment':ref(ev/'blind-assessment.v5.json'),'advisoryAccount':'reviews/codex-post-reset.v1/advisory-application-account.v16.proposed.json','implementationAuthorized':False,'readinessChanged':False,'productQualification':False})
p=dc/'correction-crosswalk.proposed.json';before=p.read_bytes();bp=ev/'crosswalk-before-v16.json';assert not bp.exists();bp.write_bytes(before);cw=load(p)
for row in cw['items']:
 old=copy.deepcopy(row.get('latestCompletedReview'));hist=row.setdefault('historicalReviews',[])
 if old and old not in hist:hist.append(old)
 assert row['id'] in review['arDispositions']
 row['latestCompletedReview']={**ref(prior,'/arDispositions/'+row['id']),'subjectManifestSha256':sha(mp),'overallVerdict':review.get('verdict',review.get('overallVerdict')),'unresolvedMustIds':[x['id'] for x in review['newMustIssues']],'unresolvedShouldIds':[x['id'] for x in review['newShouldIssues']],'standing':'Actual v15 review preserves its literal scope. Subsequent blind v5 requires four corrections; this prior review does not accept v16 or provide blind/application grades.'}
 row['status']='AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW'
assert len(cw['items'])==16;p.write_text(json.dumps(cw,indent=2)+'\n')
put(ev/'crosswalk-update-v16.json',{'beforeSha256':hashlib.sha256(before).hexdigest(),'afterSha256':sha(p),'standing':'Updated before pins; no acceptance/readiness change.'})
p=dc/'README.md';before=p.read_bytes();bp=ev/'corrections-readme-before-v16.md';assert not bp.exists();bp.write_bytes(before)
p.write_text('''# Architecture corrections — v16 awaiting independent review

**Not ready for implementation.** Actual Claude and Codex addressed the fresh blind review's capability-registry selection, TypeScript library-name mapping, coverage-state applicability and repair-plan projection findings. The [technical assessment](reviews/codex-post-reset.v1/technical-review.v16.md) records exact source, reference evidence and limitations, including the accompanying advisory clarifications and further producer/retained-Run coverage checks.

The intended product remains one complete design implemented in stages. These corrected bytes require fresh independent acceptance with zero unresolved MUST/SHOULD, a NEW blind consumer and complete independently reviewed application/readiness reconciliation. Historical v15 acceptance does not accept a changed successor. No product implementation, commit or push is authorized. [The resume guide](reviews/NEXT-REVIEW.md) owns current status.

## Earlier progress — historical

'''+before.decode())
print(json.dumps({'requiredDispositions':len(required),'advisories':len(items),'crosswalkRows':len(cw['items']),'acceptance':False}))
