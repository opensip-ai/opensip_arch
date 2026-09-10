from pathlib import Path
import hashlib,json
root=Path.cwd();dc=root/'docs/coop/design-corrections';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(rel):return json.loads((dc/rel).read_text())
pinned_paths=set()
for unit,name,key in [('foundation','source-pins.v1.json','files'),('security','source-pins.v1.json','pins'),('native','source-pins.v2.json','pins'),('workflows','source-pins.v1.json','files')]:
 for row in json.loads((dc/unit/name).read_text())[key]:
  assert sha(root/row['path'])==row['sha256'],('Stale source before recording',row['path'])
  pinned_paths.add(row['path'])
pinned_before={rel:sha(root/rel) for rel in pinned_paths}

assert (dc/'reviews/digest-corrections-author.v10/custody.json').exists()
assert read('reviews/codex-post-reset.v1/annotation-coverage-final-recheck.v12/result.json')['passed']
assert read('reviews/codex-post-reset.v1/annotation-traversal-final-recheck.v12/recheck-assessment.json')['passed']
assert read('reviews/codex-post-reset.v1/annotation-alias-final-recheck.v12/recheck-assessment.json')['passed']
assert read('reviews/codex-post-reset.v1/annotation-inherited-limbs-final-recheck.v12/recheck-assessment.json')['passed']
assert read('reviews/codex-post-reset.v1/annotation-aggregation-final-recheck.v12/result.json')['passed']
assert read('reviews/codex-post-reset.v1/annotation-typed-equality-final-recheck.v12/result.json')['passed']
identity=read('foundation/identity-report.json');by_id={}
for case in identity['checks']:by_id.setdefault(case['id'],[]).append(case['passed'])
assert all(all(values) for values in by_id.values())
count_account={'standing':'Measured passing calls and distinct IDs; neither is a coverage or independent-acceptance claim. Historical duplicate IDs preserved.','sourceReport':'docs/coop/design-corrections/foundation/identity-report.json','sourceReportSha256':sha(dc/'foundation/identity-report.json'),'passingCalls':identity['passed'],'distinctIds':len(by_id),'duplicateExtraInstances':sum(len(v)-1 for v in by_id.values()),'duplicates':{k:{'instances':len(v),'allPass':all(v)} for k,v in sorted(by_id.items()) if len(v)>1}}
cp=dc/'reviews/codex-post-reset.v1/identity-check-counts.v12.json';assert not cp.exists();cp.write_text(json.dumps(count_account,indent=2)+'\n')
f=read('foundation/validation-report.json');s=read('security/security-lifecycle-report.v1.json');n=read('native/native-evidence-report.v2.json');w=read('workflows/workflows-validation-report.json');wi=read('workflows/workflows-report.v1.json');i=read('integration-report.v1.json');assert f['passed'] and s['passed'] and n['result']=='PASS' and w['passed'] and not i['failed']
assert json.loads(Path('/tmp/opensip-design-corrections/final-reference-v12/reference-checks.json').read_text())['passed']
counts={name:read('foundation/'+name+'-report.json')['passed'] for name in ['foundation','identity','product-quality','product-configuration']};orders=read('foundation/array-order-report.json');assert orders['passed'];counts['array-order']=sum(row['passed'] for row in orders['checks'])
summary=read('validation-summary.v1.json');summary['foundation'].update(checksPassed=sum(counts.values()),sourcePinsVerified=f['sourceFileCount'],components=counts);summary['security'].update(casesPassed=s['counts']['pass'],invariantSweepsPassed=len(s['sweeps']));summary['native'].update(casesPassed=n['cases']['passed']);summary['workflows']['checksPassed']=wi['passed'];summary['integration']['checksPassed']=i['passed'];summary['claudePriorReview']='reviews/post-reset-review.v11/review.json';summary['claudeFinalReview']='PENDING-FROZEN-V12';summary['priorReviewLimitation']='v11 CHANGES_REQUIRED: final required findings are retained verbatim in its actual review and individually addressed in the v12 disposition account. A newly frozen successor must receive independent acceptance with no unresolved required findings.';(dc/'validation-summary.v1.json').write_text(json.dumps(summary,indent=2)+'\n')
d=read('post-reset-dispositions.v12.proposed.json');d['standing']='PROPOSED completed v12 coauthor correction; fresh independent review, new blind and complete application required'
for row in d['items']:row['status']='CORRECTED-PENDING-INDEPENDENT-REVIEW'
for row in d['advisoryCorrections']:row['status']='CORRECTED-OR-EXPLICITLY-ACCOUNTED-PENDING-INDEPENDENT-REVIEW'
ap=dc/'reviews/codex-post-reset.v1/advisory-application-account.v12.proposed.json';advs=json.loads(ap.read_text())
for row in advs['items']:
 if row['id']=='v11-A2':row['finalMeasuredAccount']={'path':'reviews/codex-post-reset.v1/identity-check-counts.v12.json','passingCalls':count_account['passingCalls'],'distinctIds':count_account['distinctIds'],'duplicateExtraInstances':count_account['duplicateExtraInstances']}
ap.write_text(json.dumps(advs,indent=2)+'\n')

d['actualCoauthorHandoff']={'path':'docs/coop/design-corrections/reviews/digest-corrections-author.v10/handoff.json','sha256':sha(dc/'reviews/digest-corrections-author.v10/handoff.json'),'sessionId':'5dec928a-6357-4726-9ea8-49a3079fb726','role':'COAUTHOR follow-up, not independent acceptance'};d['finalRechecks']=['reviews/codex-post-reset.v1/annotation-aggregation-final-recheck.v12/result.json','reviews/codex-post-reset.v1/annotation-typed-equality-final-recheck.v12/result.json'];d['finalPinSeal']='Separate final after-recording pin check and freeze guard are mandatory';d['remaining']=['fresh independent review of exact frozen successor at zero unresolved MUST/SHOULD','new fresh blind on same accepted normative inputs','complete independently reviewed application and readiness reconciliation'];(dc/'post-reset-dispositions.v12.proposed.json').write_text(json.dumps(d,indent=2)+'\n')
h=read('historical-preservation-report.v11.json')
for row in h['files']:row['currentSha256']=sha(root/row['path']);row['unchanged']=row['currentSha256']==row['openingSha256']
h['unchanged']=sum(row['unchanged'] for row in h['files']);h['changed']=[row['path'] for row in h['files'] if not row['unchanged']];assert not h['changed'];assert not (dc/'historical-preservation-report.v12.json').exists();(dc/'historical-preservation-report.v12.json').write_text(json.dumps(h,indent=2)+'\n')
print('Final v12 reference evidence recorded; no acceptance',counts,'native',n['cases']['passed'],'integration',i['passed'],'historical',h['unchanged'])

assert all(sha(root/rel)==digest for rel,digest in pinned_before.items()), 'Recording unexpectedly changed a pinned source; do not freeze'
