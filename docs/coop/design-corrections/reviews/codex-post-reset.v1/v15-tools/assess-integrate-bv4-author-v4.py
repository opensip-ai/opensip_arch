"""Prepared only. Requires actual completed handoff, exact root full-read account, and source assent."""
from pathlib import Path
import json,hashlib,shutil,datetime
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1';author=dc/'reviews/bv4-corrections-author.v4';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
h=read(author/'handoff.json');response=read(author/'response.json');assert response['is_error'] is False and response['session_id']=='77758b10-d7ba-4868-9d42-ae0b13e84cb6';assert set(response['modelUsage'])=={'claude-opus-5'}
account=read(ev/'bv4-v4-final-handoff-read.json');assert account['handoffSha256']==sha(author/'handoff.json') and account['handoffMdSha256']==sha(author/'handoff.md') and account['allRequiredResolved'] is True
latest=author/account['latestCheckpointFile'];feedback=author/account['latestFeedbackFile'];fd=read(feedback);assert fd['technicalAssent'] is True and fd['checkpointSha256']==sha(latest)==account['latestCheckpointSha256']
rows=h['delta']['againstFrozenV14']['changedFiles'];assert not h['delta']['againstFrozenV14']['additions'] and not h['delta']['againstFrozenV14']['deletions'];assert rows==read(latest)['delta']['againstFrozenV14']['changedFiles']
mp=dc/'reviews/candidate-subject.v14.json';assert sha(mp)=='45b1e128ca51d114895f3c406cc92575e6efe95051bf319023dc1f3180c2f92c';base={r['path']:r for r in read(mp)['files']}
for row in rows:
 rel=row['path'];assert sha(author/'work'/rel)==row['afterSha256'] and sha(root/rel)==row['beforeSha256']==base[rel]['sha256'] and sha(author/'before-images'/rel)==row['beforeSha256'],rel
assert (author/'custody.json').exists()
def ref(p):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
a={'standing':'Actual Codex final coauthor-source assessment. Assent to integrate exact corrected source for fresh independent review only.','recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finalSourceAssent':True,'independentAcceptance':False,'implementationAuthorized':False,'readinessChanged':False,'productQualification':False,'verdict':'ASSENT-TO-CORRECTED-SOURCE','unresolvedMustIssues':[],'unresolvedShouldIssues':[], 'actualCoauthor':{'sessionId':response['session_id'],'model':'claude-opus-5','role':'COAUTHOR follow-up, not independent reviewer','response':ref(author/'response.json'),'handoff':ref(author/'handoff.json'),'custody':ref(author/'custody.json')},'sourceDelta':rows,'finalHandoffReadAccount':ref(ev/'bv4-v4-final-handoff-read.json'),'finalCheckpoint':ref(latest),'substantiveRootCheckpoint':ref(feedback),'substantiveAssessment':account['substantiveAssessment'],'finalSourceProbes':account['finalSourceProbes'],'limits':account['limits'],'remaining':['six final source-pinned reference commands and sealed successor','fresh independent review at zero unresolved MUST/SHOULD','NEW blind consumer on accepted normative bytes','full application review and readiness reconciliation']}
p=ev/'coauthor-assessment-bv4-v4.json';assert not p.exists();p.write_text(json.dumps(a,indent=2)+'\n')
before=ev/'integration-before-v15';before.mkdir(exist_ok=False)
for row in rows:
 p=root/row['path'];q=before/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
for rel in ['integration-fixtures.py','foundation/source-pins.v1.json','security/source-pins.v1.json','native/source-pins.v2.json','workflows/source-pins.v1.json','validation-summary.v1.json']:
 p=dc/rel;q=before/'root-owned'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
for row in rows:
 p=root/row['path'];assert sha(p)==row['beforeSha256'];shutil.copy2(author/'work'/row['path'],p);assert sha(p)==row['afterSha256']
(ev/'integration-receipt-bv4-v4.json').write_text(json.dumps({'standing':'Integrated exact assessed coauthor source preserving every live before-image; no implementation or readiness change.','files':rows,'assessment':ref(ev/'coauthor-assessment-bv4-v4.json')},indent=2)+'\n');print(json.dumps({'integratedFiles':len(rows),'finalSourceAssent':True,'independentAcceptance':False}))
