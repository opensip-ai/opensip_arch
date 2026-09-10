"""Prepared only: update current correction routing BEFORE pins after actual source/review assessment."""
from pathlib import Path
import json,hashlib,copy
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
def write(p,d):assert not p.exists(),str(p);p.write_text(json.dumps(d,indent=2)+'\n')
def ref(p,selector=None):
 r={'path':str(p.relative_to(root)),'sha256':sha(p)}
 if selector is not None:r['selector']=selector
 return r
assessment=ev/'successor-source-assessment.v15.json';a=read(assessment);assert a['finalSourceAssent'] is True and a['independentAcceptance'] is False
for row in a['sourceDelta']:assert sha(root/row['path'])==row['afterSha256'],row['path']
prior=dc/'reviews/post-reset-review.v14/review.json';review=read(prior);assert read(prior.with_name('response.json'))['is_error'] is False
mp=dc/'reviews/candidate-subject.v14.json';assert sha(mp)=='45b1e128ca51d114895f3c406cc92575e6efe95051bf319023dc1f3180c2f92c'
account_path=ev/'v14-review-and-v15-correction-assessment.json';account=read(account_path)
assert account['reviewSha256']==sha(prior) and account['allRequiredAddressedByV15Source'] is True
required=review['newMustIssues']+review['newShouldIssues'];assert {r['id'] for r in account['independentRequiredDispositions']}=={r['id'] for r in required}
assert all(r['status']=='CORRECTED-PENDING-SUCCESSOR-REVIEW' for r in account['independentRequiredDispositions'])
advs=read(ev/'advisory-application-account.v14.proposed.json');assert len(advs['items'])==43
assert {r['id'] for r in account['newAdvisoryApplicationAccounts']}=={r['id'] for r in review['newAdvisories']}
advs['items']+=account['newAdvisoryApplicationAccounts'];assert len({r['id'] for r in advs['items']})==len(advs['items']);advs['standing']=str(len(advs['items']))+' individually accounted historical advisories and stated successor limits; no fresh independent acceptance or product qualification.'
write(ev/'advisory-application-account.v15.proposed.json',advs)
write(dc/'post-reset-dispositions.v15.proposed.json',{'standing':'PROPOSED v15 source corrections; fresh independent acceptance, NEW blind consumer and complete application still required.','predecessorManifestSha256':sha(mp),'actualPredecessorReview':ref(prior),'predecessorVerdict':review.get('overallVerdict',review.get('verdict')),'items':account['independentRequiredDispositions'],'additionalRootCorrections':account['additionalRootCorrections'],'actualCoauthorHandoff':ref(dc/'reviews/bv4-corrections-author.v4/handoff.json'),'finalSourceAssessment':ref(assessment),'actualReviewAssessment':ref(account_path),'advisoryAccount':'reviews/codex-post-reset.v1/advisory-application-account.v15.proposed.json','implementationAuthorized':False,'readinessChanged':False,'productQualification':False})
p=dc/'correction-crosswalk.proposed.json';before=p.read_bytes();bp=ev/'crosswalk-before-v15.json';assert not bp.exists();bp.write_bytes(before);cw=read(p)
for row in cw['items']:
 old=copy.deepcopy(row.get('latestCompletedReview'));history=row.setdefault('historicalReviews',[])
 if old and old not in history:history.append(old)
 assert row['id'] in review['arDispositions']
 row['latestCompletedReview']={**ref(prior,'/arDispositions/'+row['id']),'subjectManifestSha256':sha(mp),'overallVerdict':review.get('overallVerdict',review.get('verdict')),'unresolvedMustIds':[x['id'] for x in review['newMustIssues']],'unresolvedShouldIds':[x['id'] for x in review['newShouldIssues']],'standing':'Actual completed v14 review applies to frozen v14 only. Preserve each literal row disposition and scope; this does not accept v15 source or supply blind/application grades.'}
 row['status']='AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW'
assert len(cw['items'])==16;p.write_text(json.dumps(cw,indent=2)+'\n');write(ev/'crosswalk-update-v15.json',{'beforeSha256':hashlib.sha256(before).hexdigest(),'afterSha256':sha(p),'standing':'Current routing updated BEFORE pins; no acceptance/readiness change.'})
p=dc/'README.md';before=p.read_bytes();bp=ev/'corrections-readme-before-v15.md';assert not bp.exists();bp.write_bytes(before);p.write_text('''# Architecture corrections — v15 awaiting independent review

**Not ready for implementation.** Actual Claude and Codex reconciled the remaining availability-reporting descriptions and the refusal for selections that exceed the analysis limit. Complete default and explicit requests now use a defined pre-Plan boundary, with malformed fields kept under schema validation and earlier invocation outcomes preserved. The [technical assessment](reviews/codex-post-reset.v1/technical-review.v15.md) records exact source, reproduced controls and limitations.

The intended product is one complete design implemented in stages. These corrected bytes still require fresh independent acceptance with zero unresolved MUST/SHOULD, a new blind consumer, and complete independently reviewed application/readiness reconciliation. No earlier review accepts a changed successor by inference. No product implementation, commit or push is authorized. [The resume guide](reviews/NEXT-REVIEW.md) owns current status.

## Earlier progress — historical

'''+before.decode());print(json.dumps({'requiredIndependentDispositions':len(required),'advisories':len(advs['items']),'crosswalkRows':len(cw['items']),'acceptance':False}))
