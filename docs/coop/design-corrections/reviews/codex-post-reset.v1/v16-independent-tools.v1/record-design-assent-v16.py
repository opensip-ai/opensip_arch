"""Record root's actual completed review assessment; never derive assent from a headline alone."""
from pathlib import Path
import json,hashlib,datetime,copy
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews';own=ev/'codex-post-reset.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
mp=ev/'candidate-subject.v16.json';digest=sha(mp)
m=read(mp);snapshot=Path(m['snapshotRoot']);rp=ev/'post-reset-review.v16/review.json';r=read(rp);resp=read(rp.with_name('response.json'))
assessment_session=read(own/'review-assessment.v16.json')['actualReviewSession']
assert resp['is_error'] is False and resp['session_id']==assessment_session
assert r.get('verdict',r.get('overallVerdict'))=='ACCEPT' and all(type(r.get(k)) is list and not r[k] for k in ('newMustIssues','newShouldIssues'))
assert r['subjectManifestSha256']==digest
assessment_path=own/'review-assessment.v16.json';assessment=read(assessment_path)
assert assessment['reviewSha256']==sha(rp) and assessment['fullRead'] is True and assessment['rootDesignAssent'] is True
assert assessment['unresolvedRootMustIssues']==assessment['unresolvedRootShouldIssues']==[]
assert isinstance(assessment['basis'],list) and assessment['basis']
assert {v['id'] for v in assessment['newAdvisoryApplicationAccount']}=={v['id'] for v in r['newAdvisories']}
assert {str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file()}=={row['path'] for row in m['files']}
for row in m['files']:
 p=snapshot/row['path'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],row['path']
 if row['path']!='docs/coop/design-corrections/reviews/NEXT-REVIEW.md':assert sha(root/row['path'])==row['sha256'],('Live accepted-source drift',row['path'])
def ref(p):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
advice=copy.deepcopy(read(own/'advisory-application-account.v16.proposed.json')['items']);assert len(advice)==50
for row in advice:row['currentAssentStanding']='Carried with its exact original severity and limitations. Original pending/history wording is preserved; this current assent does not turn carried or routing-only dispositions into new application grades.'
advice+=assessment['newAdvisoryApplicationAccount'];assert len({r['id'] for r in advice})==len(advice)
historical=next(x for x in advice if x['id']=='V14-ADV-1')
assert historical['sourceCorrection']['sha256']=='706b7e0fc94bb1467e33c9f75d5406046e32ab9859f57f08a1f6642dfbdc7d46'
historical['sourceCorrectionContext']={'standing':'Historical as-of-v15 correction pin; preserved without retrospective repinning. V16-ADV-1 supplies the current reference.','historicalSubject':ref(ev/'candidate-subject.v15.json'),'currentSource':next(x for x in advice if x['id']=='V16-ADV-1')['currentSource']}
contracts=[{'path':r['path'],'sha256':r['sha256']} for r in m['files'] if r['path'].startswith('docs/v2/contracts/product-v1/') and r['path'].endswith('.md')];assert len(contracts)==6
out=own/'design-assent.v16.json';assert not out.exists()
out.write_text(json.dumps({'standing':'Actual Codex technical assent to independently accepted frozen v16. Root coauthor/integration assessment, not a second independent review. NEW blind and complete independent application review remain required.','recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'designManifest':ref(mp),'actualIndependentClaudeReview':{**ref(rp),'sessionId':resp['session_id'],'verdict':'ACCEPT','subjectPinSelector':'/subjectManifestSha256'},'contracts':contracts,'assent':'ACCEPT-DESIGN, subject to separate NEW blind consumer and complete final application acceptance','basis':assessment['basis'],'rootReviewAssessment':ref(assessment_path),'advisoryApplicationAccount':advice,'implementationAuthorized':False,'productQualification':False,'readinessChanged':False,'separateBlindAndApplicationReviewsRequired':True},indent=2)+'\n')
print(json.dumps({'actualReviewSession':resp['session_id'],'manifestSha256':digest,'advisoryAccounts':len(advice),'blindStillRequired':True,'applicationStillRequired':True},indent=2))
