from pathlib import Path
import hashlib,json
root=Path.cwd();dc=root/'docs/coop/design-corrections';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(rel):return json.loads((dc/rel).read_text())
assert (dc/'reviews/digest-corrections-author.v8/custody.json').exists()
assert read('reviews/codex-post-reset.v1/annotation-coverage-final-recheck.v10/result.json')['passed']
assert read('reviews/codex-post-reset.v1/annotation-traversal-final-recheck.v10/recheck-assessment.json')['passed']
assert read('reviews/codex-post-reset.v1/annotation-alias-final-recheck.v10/recheck-assessment.json')['passed']
assert read('reviews/codex-post-reset.v1/annotation-inherited-limbs-final-recheck.v10/recheck-assessment.json')['passed']
f=read('foundation/validation-report.json');s=read('security/security-lifecycle-report.v1.json');n=read('native/native-evidence-report.v2.json');w=read('workflows/workflows-validation-report.json');wi=read('workflows/workflows-report.v1.json');i=read('integration-report.v1.json');assert f['passed'] and s['passed'] and n['result']=='PASS' and w['passed'] and not i['failed']
assert json.loads(Path('/tmp/opensip-design-corrections/final-reference-v10/reference-checks.json').read_text())['passed']
counts={name:read('foundation/'+name+'-report.json')['passed'] for name in ['foundation','identity','product-quality','product-configuration']};orders=read('foundation/array-order-report.json');assert orders['passed'];counts['array-order']=sum(row['passed'] for row in orders['checks'])
summary=read('validation-summary.v1.json');summary['foundation'].update(checksPassed=sum(counts.values()),sourcePinsVerified=f['sourceFileCount'],components=counts);summary['security'].update(casesPassed=s['counts']['pass'],invariantSweepsPassed=len(s['sweeps']));summary['native'].update(casesPassed=n['cases']['passed']);summary['workflows']['checksPassed']=wi['passed'];summary['integration']['checksPassed']=i['passed'];summary['claudePriorReview']='reviews/post-reset-review.v9/review.json';summary['claudeFinalReview']='PENDING-FROZEN-V10';summary['priorReviewLimitation']='v9 CHANGES_REQUIRED: zero MUST, one SHOULD v9-S1. A newly frozen successor must receive independent acceptance with no unresolved required findings.';(dc/'validation-summary.v1.json').write_text(json.dumps(summary,indent=2)+'\n')
d=read('post-reset-dispositions.v10.proposed.json');d['standing']='PROPOSED completed v10 coauthor correction; fresh independent review, new blind and complete application required'
for row in d['items']:row['status']='AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW'
d['actualCoauthorHandoff']={'path':'docs/coop/design-corrections/reviews/digest-corrections-author.v8/handoff.json','sha256':sha(dc/'reviews/digest-corrections-author.v8/handoff.json'),'sessionId':'5dec928a-6357-4726-9ea8-49a3079fb726','role':'COAUTHOR follow-up, not independent acceptance'};d['finalRecheck']='reviews/codex-post-reset.v1/annotation-coverage-final-recheck.v10/result.json';d['remaining']=['fresh independent review of exact frozen successor at zero unresolved MUST/SHOULD','new fresh blind on same accepted normative inputs','complete independently reviewed application and readiness reconciliation'];(dc/'post-reset-dispositions.v10.proposed.json').write_text(json.dumps(d,indent=2)+'\n')
h=read('historical-preservation-report.v9.json')
for row in h['files']:row['currentSha256']=sha(root/row['path']);row['unchanged']=row['currentSha256']==row['openingSha256']
h['unchanged']=sum(row['unchanged'] for row in h['files']);h['changed']=[row['path'] for row in h['files'] if not row['unchanged']];assert not h['changed'];assert not (dc/'historical-preservation-report.v10.json').exists();(dc/'historical-preservation-report.v10.json').write_text(json.dumps(h,indent=2)+'\n')
print('Final v10 reference evidence recorded; no acceptance',counts,'native',n['cases']['passed'],'integration',i['passed'],'historical',h['unchanged'])
