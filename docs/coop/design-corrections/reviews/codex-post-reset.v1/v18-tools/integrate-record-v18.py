"""Integrate the mutually assessed reference-checker correction; update routing before pins."""
from pathlib import Path
import json,hashlib,datetime,copy,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews';own=ev/'codex-post-reset.v1';tmp=Path('/tmp/opensip-design-corrections');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
def put(p,d):
 assert not p.exists(),str(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def ref(p,selector=None):
 d={'path':str(p.relative_to(root)),'sha256':sha(p)}
 if selector is not None:d['selector']=selector
 return d
mp=ev/'candidate-subject.v17.json';m=load(mp);assert sha(mp)=='8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c'
for row in m['files']:
 assert sha(Path(m['snapshotRoot'])/row['path'])==row['sha256']
 if row['path']!='docs/coop/design-corrections/reviews/NEXT-REVIEW.md':assert sha(root/row['path'])==row['sha256'],('unexpected live drift',row['path'])
co=ev/'v18-checker-coauthor.v1';h=load(co/'handoff.json');rr=load(co/'response.json');assert rr['is_error'] is False and rr['session_id']=='4b48ccdd-92fb-4f92-9db2-ac8942f796d6';assert h['technicalAssent']['value'] is True and not h['changesRequired'];assert (co/'codex-retention-custody.json').exists()
review=ev/'post-reset-review.v17-clarification.v1/review.json';r=load(review);assert load(review.with_name('response.json'))['is_error'] is False;assert r['subjectManifestSha256']==sha(mp)
proposal=own/'v18-checker-proposal.v1';pr=load(proposal/'proposal.json');p=root/pr['path'];q=proposal/'proposal'/pr['path'];assert sha(p)==pr['beforeSha256']==h['custody']['frozenCheckerSha256'];assert sha(q)==pr['afterSha256']==h['custody']['proposedCheckerSha256']
assert load(proposal/'root-exact-ast-proof.json')['completeRemainingAstEqualsBefore'];assert not load(proposal/'exception-handler-results.json')['mismatches']['proposal']
for name in ['report.frozen-checker.json','report.proposed-checker.json']:
 x=load(co/'evidence'/name);assert x['checkCount']==x['passed']==1787 and not x['failed']
injected=load(co/'evidence/inject_false_pass.json');assert injected['discriminates'] and injected['results']['frozen']['failedCount']==0 and injected['results']['proposed']['failedIds']==['repair.preview-applicable']
before=own/'source-before-v18';before.mkdir(exist_ok=False);bp=before/pr['path'];bp.parent.mkdir(parents=True);shutil.copyfile(p,bp);shutil.copyfile(q,p);assert sha(p)==pr['afterSha256']
qualifications=[
 'Coauthor partialcopies contain1219of7671files, intentionallyomit6452reviewfiles. Directchecker1787passes do not exercise source-pin gate; rootcanonical6afterrecordingdoes.',
 'Coauthor first ast_delta.py has an always-true originalComparisonPreserved expression; it is not a proof. Its later comparator inventory is stronger but does not alone prove all other AST nodes unchanged. Root exact whole-AST rollback/equality proof independently establishes precisely ten added guards.',
 'Coauthor universal claim every handler has an explicit post-try missing-refusal guard is overbroad: several rely on later expected fields or distinct stage logic. Existing expectation-key convention and actual counterexample justify the fix without that universal claim.',
 'Coauthor scanner completeness is scoped to matching expectation-side defaulting comparisons in this checker, not all exception handling. Its prose about every other fifteen comparison is overbroad (golden absence comparison is a named exception). Root independent ten-site inventory and exact handler tests agree on the affected scope.',
 'Reachability46linehits shows every changed handler executes; it does not independently discriminate each null edge. Root ten-handler synthetic controls supply that separate evidence.',
 'Coauthor reference corpus injection exercises actual model refusal using synthetic model inputs; no product Run/host/compiler/security enforcement is measured.',
 'V18-OBS-1 null diagnostic remains nonblocking: caseID identifies the failed control, correct failure is emitted. Optional richer reference-test diagnostics require no public design change; preserve observation as future convenience, not unperformed qualification.'
]
put(own/'coauthor-assessment-v18-checker.v1.json',{'standing':'Root fully read actual coauthor handoffJSON/MD/receipt, all seven probe sources, executed reports/trace and exact ten-line proposal. Actual source assent to this bounded reference correction.','handoff':ref(co/'handoff.json'),'markdown':ref(co/'handoff.md'),'response':ref(co/'response.json'),'actualSession':rr['session_id'],'fullRead':True,'finalSourceAssent':True,'requiredChanges':[],'sourcePath':pr['path'],'finalSha256':sha(p),'reportQualifications':qualifications,'implementationAuthorized':False,'readinessChanged':False})
finding={'id':'CX-V17-REFUSAL-EXPECTATION','severity':'SHOULD','originalReviewerId':'V17-ADV-3','originalReviewerSeverity':'advisory (nonblocking)','status':'CORRECTED-PENDING-SUCCESSOR-REVIEW','finding':'Ten defaulting expected-refusal comparisons can falsely pass an unexpected null-detail exception.','correction':'Each handler now requires its exact expected-refusal key to be present before comparing the detail. Deliberate null, named detail, error-code and remedy checks retain their existing meanings.','evidence':[ref(proposal/'exception-handler-results.json'),ref(proposal/'root-exact-ast-proof.json'),ref(co/'evidence/inject_false_pass.json')],'source':ref(p)}
assessment={'standing':'Root/coauthor source assent to one bounded checker correction. Fresh independent acceptance of successor18 still required.','recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finalSourceAssent':True,'independentAcceptance':False,'actualCoauthorHandoff':ref(co/'handoff.json'),'rootCoauthorAssessment':ref(own/'coauthor-assessment-v18-checker.v1.json'),'priorIndependentReview':ref(review),'priorRootAssessment':ref(own/'review-assessment.v17.json'),'predecessorManifest':ref(mp),'sourceDelta':[{'path':pr['path'],'beforeSha256':pr['beforeSha256'],'afterSha256':sha(p),'coauthorSha256':h['custody']['proposedCheckerSha256']}],'findingDispositions':[finding],'additionalFindingDispositions':[],'nonBlockingObservation':{'original':h['nonBlockingObservation'],'disposition':qualifications[-1]},'implementationAuthorized':False,'readinessChanged':False,'productQualification':False}
put(own/'successor-source-assessment.v18.json',assessment)
items=copy.deepcopy(load(own/'advisory-application-account.v17.proposed.json')['items']);assert len(items)==55
for i,x in enumerate(r['newAdvisories']):
 if x['id'] in ('V17-ADV-1','V17-ADV-2'):disposition=copy.deepcopy(x['rootProposedDisposition'])
 else:disposition={'rootRequiredFinding':'CX-V17-REFUSAL-EXPECTATION','actualCoauthorSuggestedSeverity':'SHOULD','correction':finding,'standing':'Original independent advisorygrade preserved; root/coauthor required and corrected this beforepromotion. Fresh18reviewpending.'}
 items.append({'id':x['id'],'originalSeverity':x['severity'],'reviewEvidence':ref(review,'/newAdvisories/'+str(i)),'disposition':disposition,'standing':'Individually accounted; no independent successor/application acceptance inferred.'})
byid={x['id']:x for x in items};assert len(items)==len(byid)==58
# New prospective provenance account, preserving all frozen17historical bytes.
v14=byid['V14-ADV-2'];assert v14['sourceCorrection']['sha256']=='ef0c244e7817e8bda6039ec66fc3180114f8e9997b3eacee4fe313c7f3d737b8';source=root/v14['sourceCorrection']['path'];assert sha(source)=='53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a'
v14['sourceCorrectionContext']={'standing':'Original sourceCorrection is historical, valid as-of-v16. Explicit current binding is separate; original frozen records preserved.','asOfSubject':ref(ev/'candidate-subject.v16.json'),'currentSource':ref(source),'currentSourceStanding':'Current proposedv18source; byte-identical to frozen17 for this document. Successorreview/applicationpending.'}
put(own/'advisory-application-account.v18.proposed.json',{'standing':'58individualadvisories with originalseverity/history; newprospectiveaccountlabelsV14ADV2historicalandbindscurrent. Successoracceptance/applicationpending.','items':items,'sourceAssessment':ref(own/'successor-source-assessment.v18.json')})
put(dc/'post-reset-dispositions.v18.proposed.json',{'standing':'PROPOSED completed bounded reference-checker correction. Freshindependent18,NEWblind andfullapplicationrequired.','predecessorManifestSha256':sha(mp),'actualPredecessorReview':ref(review),'predecessorVerdict':r['verdict'],'predecessorRootAssent':False,'items':[finding],'actualCoauthorHandoff':ref(co/'handoff.json'),'finalSourceAssessment':ref(own/'successor-source-assessment.v18.json'),'advisoryAccount':'reviews/codex-post-reset.v1/advisory-application-account.v18.proposed.json','nonBlockingObservation':assessment['nonBlockingObservation'],'implementationAuthorized':False,'readinessChanged':False,'productQualification':False})
p=dc/'correction-crosswalk.proposed.json';shutil.copyfile(p,own/'crosswalk-before-v18.json');cw=load(p)
for row in cw['items']:
 old=copy.deepcopy(row.get('latestCompletedReview'));hist=row.setdefault('historicalReviews',[])
 if old and old not in hist:hist.append(old)
 assert row['id'] in r['arDispositions'];row['latestCompletedReview']={**ref(review,'/arDispositions/'+row['id']),'subjectManifestSha256':sha(mp),'overallVerdict':r['verdict'],'unresolvedMustIds':[],'unresolvedShouldIds':[],'standing':'Actual independent17clarifiedreview carries originalobligations and routingonly scope. Root withheld17promotionforreferencecheckerCX-V17-REFUSAL-EXPECTATION; thisreviewdoesnotaccept18orgrantblind/applicationgrades.'}
p.write_text(json.dumps(cw,indent=2)+'\n')
p=dc/'README.md';before=p.read_bytes();(own/'corrections-readme-before-v18.md').write_bytes(before);p.write_text('''# Architecture corrections — v18 awaiting independent review

**Not ready for implementation.** Codex and actual Claude corrected a reference-checker weakness that could pass an unexpected refusal. The ten affected handlers now require an explicit expected-refusal key. Product contracts and models are unchanged. The [technical assessment](reviews/codex-post-reset.v1/technical-review.v18.md) records the exact correction and evidence. Original independent v17 ACCEPT, its substantive clarification and the root decision to fix the weakness remain preserved.

The intended product remains one complete design implemented in stages. Fresh independent acceptance of these revised bytes, a NEW blind consumer and complete independently reviewed application/readiness reconciliation remain required. No implementation, commit or push is authorized. [Resume guide](reviews/NEXT-REVIEW.md).

## Earlier progress — historical

'''+before.decode())
print(json.dumps({'sourceIntegrated':pr['path'],'afterSha256':sha(root/pr['path']),'advisories':len(items),'independentAcceptance':False}))
