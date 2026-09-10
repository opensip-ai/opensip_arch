"""Record final v9 reference evidence only after released coauthor source integration and all checks."""
from pathlib import Path
import hashlib,json,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(rel):return json.loads((dc/rel).read_text())
assert (dc/'reviews/digest-corrections-author.v4/custody.json').is_file()
assert (dc/'reviews/digest-corrections-author.v5/custody.json').is_file()
assert (dc/'reviews/digest-corrections-author.v6/custody.json').is_file()
f=read('foundation/validation-report.json');s=read('security/security-lifecycle-report.v1.json');n=read('native/native-evidence-report.v2.json');w=read('workflows/workflows-validation-report.json');wi=read('workflows/workflows-report.v1.json');i=read('integration-report.v1.json')
assert f['passed'] and s['passed'] and n['result']=='PASS' and w['passed'] and not i['failed']
counts={name:read('foundation/'+name+'-report.json')['passed'] for name in ['foundation','identity','product-quality','product-configuration']};orders=read('foundation/array-order-report.json');assert orders['passed'];counts['array-order']=sum(row['passed'] for row in orders['checks'])
summary=read('validation-summary.v1.json');summary['foundation'].update(checksPassed=sum(counts.values()),sourcePinsVerified=f['sourceFileCount'],components=counts);summary['security'].update(casesPassed=s['counts']['pass'],invariantSweepsPassed=len(s['sweeps']));summary['native'].update(casesPassed=n['cases']['passed']);summary['workflows']['checksPassed']=wi['passed'];summary['integration']['checksPassed']=i['passed'];summary['claudePriorReview']='reviews/post-reset-review.v8/review.json';summary['claudeFinalReview']='PENDING-FROZEN-V9';summary['priorReviewLimitation']='v8 headline ACCEPT retained two unresolved SHOULD findings; v9 requires zero unresolved MUST/SHOULD before promotion.';(dc/'validation-summary.v1.json').write_text(json.dumps(summary,indent=2)+'\n')
d=read('post-reset-dispositions.v9.proposed.json');d['standing']='PROPOSED completed coauthor corrections; new frozen v9 independent review, fresh blind and final application required'
for row in d['items']:
 if row['status'] in ('AUTHOR-CORRECTION-IN-PROGRESS','CORRECTION-PREPARED-PENDING-FINAL-PIN-REFRESH'):row['status']='AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW'
d['actualCoauthorHandoffs']=[{'path':'docs/coop/design-corrections/reviews/digest-corrections-author.'+v+'/handoff.json','sha256':sha(dc/('reviews/digest-corrections-author.'+v+'/handoff.json')),'sessionId':'5dec928a-6357-4726-9ea8-49a3079fb726','role':'COAUTHOR follow-up, not independent acceptance'} for v in ('v4','v5','v6')]
d['remaining']=['fresh actual independent review of exact frozen v9 with zero unresolved MUST/SHOULD','fresh blind B reconstructing both languages plus file/clone paths from the same accepted normative inputs','complete independently reviewed application and exact readiness reconciliation','no product implementation, committing, pushing or qualification']
(dc/'post-reset-dispositions.v9.proposed.json').write_text(json.dumps(d,indent=2)+'\n')
h=read('historical-preservation-report.v8.json')
for row in h['files']:row['currentSha256']=sha(root/row['path']);row['unchanged']=row['currentSha256']==row['openingSha256']
h['unchanged']=sum(row['unchanged'] for row in h['files']);h['changed']=[row['path'] for row in h['files'] if not row['unchanged']];assert not h['changed'];(dc/'historical-preservation-report.v9.json').write_text(json.dumps(h,indent=2)+'\n')
print('Final v9 reference evidence recorded; no acceptance',counts,'native',n['cases']['passed'],'integration',i['passed'],'historical',h['unchanged'])
