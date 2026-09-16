"""Apply bounded review corrections only in a new mutable application stage."""
from pathlib import Path
import hashlib,json,shutil,copy
B=Path('/tmp/opensip-design-corrections');S=B/'application-stage.v46';F=S/'files';P=B/'application-stage.v45.2';L=Path('/Users/sb/code/opensip-ai/opensip_arch');R=Path(__file__).parent;dc='docs/coop/design-corrections/'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
review=L/dc/'reviews/application-review.v45/review.json';assert sha(review)=='6ff6e1858dd3b606a638b7c780ac2b9c4dce146799786849653831ea8040812f';rv=load(review);assert rv['verdict']=='CHANGES_REQUIRED' and len(rv['newShouldIssues'])==1 and not rv['newMustIssues']
changes=[]
def write(rel,data):
 p=F/rel;q=R/'before'/rel;q.parent.mkdir(parents=True,exist_ok=True);assert not q.exists();shutil.copyfile(p,q)
 p.write_text(json.dumps(data,indent=2)+'\n' if not isinstance(data,str) else data)
 changes.append({'path':rel,'beforeSha256':sha(q),'afterSha256':sha(p)})
rm=load(F/dc/'readiness-row-map.v1.json');old=copy.deepcopy(rm);needed={'DR-103':['DR-G08'],'DR-114':['DR-G12'],'DR-117':['DR-G09','DR-G14','DR-G16','DR-G23'],'DR-119':['DR-G14'],'DR-123':['DR-G01','DR-G02','DR-G05','DR-G12'],'DR-124':['DR-G09']}
issue=rv['newShouldIssues'][0];assert issue['id']=='APP45-S1';assert {v['row']:v['omitted'] for v in issue['selectors']}==needed
for row in rm['rows']:
 if row['id'] in needed:row['releaseGates']=sorted(set(row['releaseGates']+needed[row['id']]))
assert sum(len(a['releaseGates'])-len(b['releaseGates']) for a,b in zip(rm['rows'],old['rows']))==12
for a,b in zip(rm['rows'],old['rows']):
 aa=copy.deepcopy(a);aa['releaseGates']=b['releaseGates'];assert aa==b
write(dc+'readiness-row-map.v1.json',rm)
ir=load(F/dc/'inherited-residuals.applied.v1.json');r10=next(x for x in ir['residuals'] if x['id']=='DR-011-R10');assert r10['dispositionText'].startswith('Fresh independent blind consumer B reconstructed')
r10['dispositionText']='The independent blind consumer B origin completed its source45 continuation with independently authored vectors; its exact result is the evidence below. It remained blind but was not a fresh origin on source45. Blind reviewer session: 9d3dfb70-b2d3-498c-a3c1-f8de9e488514.'
write(dc+'inherited-residuals.applied.v1.json',ir)
for rel,oldtext,newtext in [
 ('docs/v2/architecture/08-decision-and-readiness-register.md','Actual fresh blind consumer B closes R10.','The completed independent blind consumer B continuation closes R10.'),
 ('docs/coop/COORDINATOR-DECISIONS.md','fresh independent blind consumer review `7ee66bb559488109a51d2c64eca8e48c93db7b830a071947e1eaf695c79ac2f1`','independent blind-origin continuation review `7ee66bb559488109a51d2c64eca8e48c93db7b830a071947e1eaf695c79ac2f1`')]:
 text=(F/rel).read_text();assert text.count(oldtext)==1;write(rel,text.replace(oldtext,newtext))
# Preserve the accepted report in its immutable snapshot and record the actual
# regenerated application-provenance report. No ledger pins this report.
rel=dc+'workflows/workflows-report.v1.json';before=load(F/rel);after=load(B/'application-stage.v45.2-validation'/rel)
def differences(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  assert a.keys()==b.keys();return sum((differences(a[k],b[k],path+'/'+k) for k in a),[])
 if isinstance(a,list) and isinstance(b,list):
  assert len(a)==len(b);return sum((differences(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [{'selector':path,'before':a,'after':b}]
delta=differences(before,after);assert len(delta)==1 and delta[0]['selector'].endswith('/source-pins.v1.json'),delta
for p in [F/dc/'foundation/source-pins.v1.json',F/dc/'foundation/evaluator3-source-pins.v1.json',F/dc/'native/source-pins.v2.json',F/dc/'security/source-pins.v1.json',F/dc/'workflows/source-pins.v1.json']:
 assert rel not in p.read_text(),'Workflow report unexpectedly pinned'
write(rel,(B/'application-stage.v45.2-validation'/rel).read_text())
workflow={'standing':'Application-only regenerated report after the reviewed documentation provenance ledger update. Accepted source45 report remains immutable in snapshot/archive; no model/schema/contract/corpus changes.','acceptedSourceReport':{'path':rel,'sha256':sha(P/'files'/rel),'resolveAgainst':{'path':dc+'reviews/candidate-subject.v45.json','sha256':'8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155'}},'appliedReport':{'path':rel,'sha256':sha(F/rel)},'exactLeafDelta':delta,'executionReceipt':{'path':'support/reference-rerun/workflows.json','sha256':sha(S/'support/reference-rerun/workflows.json'),'standing':'Executed in application45.2 validation; exact same semantic inputs and provenance ledgers selected in46. Reused execution, not relabelled fresh46.'}}
(S/'support/workflows-recording-delta.v1.json').write_text(json.dumps(workflow,indent=2)+'\n')
accounts=[
 {'id':'APP45-ADV-01','disposition':'CORRECTED-IN-APPLICATION','assessment':'Select the already regenerated report for the applied ledger, record its single provenance-hash difference in support/workflows-recording-delta.v1.json, and preserve the accepted report in the source45 snapshot/archive. The post-application rerun must leave this selected after-image unchanged.'},
 {'id':'APP45-ADV-02','disposition':'RETAINED-EDITORIAL-LIMITATION','assessment':'The current header and activation-bound decision clearly identify the historical chronology. Keep the original historical headings and historical authorization text byte-for-byte, as requested; they grant no current authority. Outline demotion can be considered in a later documentation-only cleanup.'},
 {'id':'APP45-ADV-03','disposition':'CORRECTED-IN-APPLICATION','assessment':'Current register, D372 evidence sentence and R10 disposition now explicitly say independent blind-origin continuation. Literal prerequisite reviews and schema field names remain unchanged.'},
 {'id':'APP45-ADV-04','disposition':'DOCUMENTED-RECOVERY-LIMIT','assessment':'The reviewed finalizer refuses a torn file before activation. If interrupted, compare all paths with the frozen manifest and retained before/after images; preserve the partial file as evidence, restore only a verified exact image under the existing documentation authorization, and rerun full guarded checks. Do not overwrite unrelated user edits. No claim of atomic copying or automated torn-write repair.'},
 {'id':'APP45-ADV-05','disposition':'PRECISION-DELTA-ACCOUNTED','assessment':'The activation-bound D372 body owns the applying act. Its documented identity-profile and section/origin precision corrections match accepted source45 law; the pinned proposed act is preserved unchanged and grants no different law.'},
 {'id':'APP45-ADV-06','disposition':'HISTORICAL-BASIS-QUALIFIED','assessment':'CB-ADV-4 carriage describes source20/21 history. Current source45 D9 carriage is exactly the DR007/R08 carriedCrossUnitObligation, blind A-c2 account, retained design publication obligation, current README and D372 body. Nothing is discharged by application.'}]
adv=load(F/dc/'accepted-review-advisories.v1.json');adv['priorApplicationReviewAccount']={'review':{'path':str(review.relative_to(L)),'sha256':sha(review),'verdict':'CHANGES_REQUIRED'},'standing':'Root application-successor dispositions; require actual independent application review of46 before activation. No45 acceptance inferred.','requiredFinding':{'id':'APP45-S1','disposition':'CORRECTED-PENDING-INDEPENDENT-REVIEW','rows':needed,'addedGateMemberships':12},'advisories':accounts};write(dc+'accepted-review-advisories.v1.json',adv)
app=load(F/dc/'application.v1.json');assert app['applicationSubject']['path'].endswith('application-subject.v45.json');app['applicationSubject']['path']=dc+'reviews/application-subject.v46.json';app['finalIndependentApplicationReview']['path']=dc+'reviews/application-review.v46/review.json';app['sharedTrustedCodeAssumption']['outcomeAuthority']['path']=dc+'reviews/application-review.v46/review.json';app['boundReceiptSha256']=sha(B/'application46-review-binding.v1/bound-review-receipt.json')
for row in app['appliedRecords']:row['sha256']=sha(F/row['path'])
app['priorApplicationReview']=adv['priorApplicationReviewAccount']['review'];app['workflowRecordingDelta']='support/workflows-recording-delta.v1.json in the frozen application package; accepted source report retained separately';app['interruptedCopyRecovery']=accounts[3]['assessment'];app['acceptedDesignReproduction']['outputPolicy']+=' workflows/run-reference-checks.py also rewrites its default workflows-report.v1.json inside the disposable copy; the applied recording successor is separately bound by workflows-recording-delta.v1.json.'
write(dc+'application.v1.json',app)
report={'standing':'Root application-only correction of actual APP45-S1 plus explicit six-advisory dispositions, all pending independent46 review. No new design or blind acceptance inferred.','priorReviewSha256':sha(review),'requiredGateAdditions':needed,'addedMemberships':12,'fileChanges':changes,'workflowRecordingDelta':workflow,'advisoryDispositions':accounts,'source45SemanticChanges':False,'passed':True}
(R/'corrections.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'filesChanged':len(changes),'requiredRows':len(needed),'gateMembershipsAdded':12,'workflowDelta':delta,'passed':True}))
