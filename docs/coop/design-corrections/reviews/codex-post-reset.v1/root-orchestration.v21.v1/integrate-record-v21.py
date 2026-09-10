"""Root substantive final-peer assessment, bounded custody and exact source21 integration."""
from pathlib import Path
import json,hashlib,shutil,datetime,copy,ast,collections
root=Path('/Users/sb/code/opensip-ai/opensip_arch');dc=root/'docs/coop/design-corrections';ev=dc/'reviews';own=ev/'codex-post-reset.v1';tmp=Path('/tmp/opensip-design-corrections');peer=ev/'reference-hardening-final-peer.v1';src=tmp/peer.name
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
def put(p,d):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def ref(p):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
def cp(p,q):
 assert not q.exists(),q;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert sha(p)==sha(q)
m=load(peer/'proposed-changes.json');receipt=load(peer/'response.json');assert receipt['session_id']=='b20560e2-5bfb-45f8-9f75-19e13c979406' and not receipt['is_error']
assert load(peer/'assessment.json')['verdict']['value']=='BOUNDED_FINAL_SOURCE_ASSENT'
parent=ev/'candidate-subject.v20.json';assert sha(parent)=='878e5bebd5a7b144ef7900e774af0e13eb1b3a01d32e7f289b6f483de6832f3c'
for row in m['changes']:
 for p,h,n in [(root/row['path'],row['beforeSha256'],row['beforeBytes']),(peer/row['overlay'],row['afterSha256'],row['afterBytes'])]:
  assert sha(p)==h and p.stat().st_size==n,(p,h)
 for k in ['diffVsFrozenV20','diffVsFirstCoauthorProposal']:
  assert sha(peer/row[k]['path'])==row[k]['sha256']
# Retain small author scripts and actual component reports excluded with disposable work.
additional=peer/'additional-custody';rows=[]
for p in sorted((src/'work').glob('*.py')):
 q=additional/'author-scripts'/p.name;cp(p,q);rows.append(ref(q))
for name in ['foundation-report.json','product-quality-report.json','product-configuration-report.json','array-order-report.json']:
 p=src/'work/source-copy/docs/coop/design-corrections/foundation'/name;q=additional/'component-reports'/name;cp(p,q);rows.append(ref(q))
# Preserve actual out-of-task memory writes as evidence, without altering their originals.
memory=Path('/Users/sb/.claude/projects/-private-tmp-opensip-design-corrections-reference-hardening-final-peer-v1/memory')
for name in ['MEMORY.md','reference-suite-needs-cpython-312.md']:
 p=memory/name;q=additional/'out-of-scope-memory-writes'/name;cp(p,q);rows.append(ref(q))
put(additional/'custody.json',{'standing':'Exact additional small author evidence; memory writes were outside the requested output root and prior bytes were not captured. No live/frozen source mutation inferred from these writes. No private thinking.','files':rows})
probe=tmp/'codex-post-reset.v1/final-wrapper-timeout.v1';probe_dest=own/'final-wrapper-timeout.v1'
for p in sorted(probe.iterdir()):
 if p.is_file():cp(p,probe_dest/p.name)
cp(tmp/'codex-post-reset.v1/probe-final-wrapper-timeout.v1.py',probe_dest/'probe-final-wrapper-timeout.v1.py')
pr=load(probe_dest/'root-result.json');assert pr['exitCode']==1 and pr['timedOutEntryDeclinesChildReport'] and pr['otherFourChildrenCompleted']
assert {x['path']:x['prospectiveSha256'] for x in pr['prospectiveSource']}=={x['path']:x['afterSha256'] for x in m['changes']}
# Actual reported calls, including failures, are checked rather than inferred from prose.
normal=load(peer/'logs/identity-report.FINAL.json');mut=load(peer/'logs/identity-report.MUTATED.json')
ids=collections.Counter(x['id'] for x in normal['checks']);assert normal['passed']==1596 and normal['failed']==0 and len(ids)==1584 and sum(ids.values())-len(ids)==12
fails=[x['id'] for x in mut['checks'] if not x['passed']];assert mut['passed']==1594 and mut['failed']==2 and fails==m['measuredCounts']['reorderingMutation']['failingControls']
def stripped(p):
 t=ast.parse(p.read_text())
 for n in ast.walk(t):
  if isinstance(n,(ast.Module,ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and n.body and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and isinstance(n.body[0].value.value,str):n.body[0].value.value='DOCSTRING'
 return ast.dump(t,include_attributes=False)
assert stripped(peer/'proposed/docs/coop/design-corrections/workflows/workflows_model.v1.py')==stripped(root/'docs/coop/design-corrections/workflows/workflows_model.v1.py')
assert stripped(peer/'proposed/docs/coop/design-corrections/foundation/run-reference-checks.py')==stripped(ev/'reference-hardening-after20.v1/proposed/docs/coop/design-corrections/foundation/run-reference-checks.py')
qualifications=[
 'Full read means complete final assessment JSON/Markdown/receipt, all six diffs, proposal, substantive comparison/mutation/precedence scripts and evidence. Public tool access was inspected as provenance; not every unchanged full report line or private reasoning was read.',
 'Source assent is bounded coauthor agreement, not independent21 acceptance. Frozen20 remains CHANGES_REQUIRED0M1S; prior source20 root review qualifications remain authoritative limits.',
 'Wrapper executable AST matches first coauthor modulo module docstring. Workflow executable AST matches frozen20 modulo one function docstring. Observable documentation/trace line positions differ; do not claim literally identical raw compiled objects or all introspection behavior.',
 'The comparison script normalizes docstrings before compilation and its code tuple omits metadata; full normalized AST equality and inspected diff provide the relevant execution-equivalence basis, not universal bytecode identity.',
 'Static inventory only includes literal IDs at six named call forms in ast.walk traversal order. Its 992sites/991distinct are not measured1596calls/1584distinct and its reported order is not general runtime order. Actual full reports establish measured counts.',
 'Final peer directly measured all five components, not the wrapper or other units. Final root six-command run remains required. Its mutation1594/2 is separately executed with exact mutated bytes retained; timeout reuse is explicitly reuse.',
 'Root separately executed the final proposal with a synthetic5second budget, locally repinned copied inputs: exit1, new failed aggregate, onlyidentitytimedout, stalechildhashdeclined and otherfourcompleted. This is not a completed foundation suite.',
 'The final peer language that outer600preemption already happened one level up is overstated. Observed predecessor failure was inner120TimeoutExpired; outer600risk is prospective. Outer3600 is a root orchestration budget, not proof of universal completion.',
 'Scope precedence applies after doc_digest(scope), ahead of payload matching. Direct helper supplies no complete Run/authorization proof; adopt_baseline has earlier authority/availability guards.',
 'The final source has no new cardinality law: guard behavior unchanged; five new controls distinguish zero/one/multiple parameters and a genuine noncandidate. Removing the source-text-count assertion preserves actual registered-carrier tests.',
 'All31historical files will be in successor21. Predecessor20 contained10;21remaining verified against live bytes there. Do not retroactively enlarge20scope.',
 'ADVISORY-NEW-1 is narrowly an absent launcher environment field, not unpublished interpreter/case semantics: foundation README already specifies Python3.12/jsonschema4.25.1 and native contract publishes UCD15.0.0. Final peer used jsonschema4.26.0; this is a distinct measured environment, not the documented/root environment.',
 'Initial wrongPython3.14/Unicode16 refusal and zsh component-loop failure are preserved as attempts; they are not source defects or canonical passing runs.',
 'First coauthor mislabeled beforeBytes in intermediate custody is already qualified by root; final proposal provides verified actual before/after sizes. Preserve flawed original record, add accurate successor account.',
 'Final peer wrote two Claude project memory files outside its requested output directory. Their postwrite bytes/public calls are retained; priorstate unavailable. Its delivered-only-to-output claim is qualified. No product/live/frozen source change authorized by memory.',
 'Allfour final pin ledgers, measured successor counts, readiness records and independent/blind/application reviews remain root/downstream obligations. No historical count or verdict is rewritten.'
]
assessment={'standing':'Codex substantive final peer assessment on exact three-source proposal. Bounded mutual source assent, no independent or blind acceptance.','recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fullRead':True,'finalSourceAssent':True,'independentAcceptance':False,'subjectManifest':ref(peer/'proposed-changes.json'),'actualClaudeSession':receipt['session_id'],'actualClaudeModel':list(receipt['modelUsage']),'actualHandoff':ref(peer/'assessment.json'),'actualMarkdown':ref(peer/'assessment.md'),'actualReceipt':ref(peer/'response.json'),'priorRootAssessment':ref(own/'coauthor-assessment.reference-hardening.v1.json'),'rootTimeoutEvidence':ref(probe_dest/'root-result.json'),'qualifications':qualifications,'sourceDelta':m['changes'],'readinessChanged':False,'implementationAuthorized':False}
ap=own/'coauthor-assessment.reference-hardening-final.v1.json';put(ap,assessment)
advisories=copy.deepcopy(load(own/'advisory-application-account.v20.proposed.json')['items']);assert len(advisories)==76
review=ev/'post-reset-review.v20/review.json'
for ident,disp in [('ADV-1','Addressed by explicit failed timeout reporting and600second per-child reference budget; root5second failure reproduction retained. Final full commands and independent successor reproduction owed.'),('ADV-2','Add all31unchanged protected files to new21inventory; preserve20scope and historical hashes.'),('ADV-3','Remove redundant source-text-count assertion, retain behavioral carrier/registry controls and five new ordering controls.')]:
 advisories.append({'id':'V20-'+ident,'originalSeverity':'advisory','reviewEvidence':ref(review),'originalReviewId':ident,'disposition':disp,'standing':'Corrected/accounted in successor21; independent review pending.'})
for ident,disp in [('ADVISORY-NEW-1',qualifications[11]),('ADVISORY-NEW-2',qualifications[13])]:
 advisories.append({'id':'V21-FINAL-PEER-'+ident,'originalSeverity':'advisory','reviewEvidence':ref(peer/'assessment.json'),'originalReviewId':ident,'disposition':disp,'standing':'Explicit qualified account; record final root environment separately, preserve earlier evidence.'})
assert len(advisories)==len({x['id'] for x in advisories})==81
put(own/'advisory-application-account.v21.proposed.json',{'standing':'76source20 accounts preserved plus3independent20 advisories plus2final-peer advisories; original severity and evidence retained. No readiness grade.','items':advisories})
prior=load(own/'successor-source-assessment.v20.json')
items=[{'id':'NEW-SHOULD-1','severity':'SHOULD','correction':'Five real third-document controls expose reordered ambiguity guard; model prose distinguishes existence, ordering and earlier canonicalization.','status':'CORRECTED-PENDING-SUCCESSOR-INDEPENDENT-REVIEW'}, {'id':'ROOT-V20-REVIEW-SCOPE','severity':'SHOULD','correction':'Fresh successor reviewer must read complete five contracts and index first, and qualify copied-law probes versus actual admission; no retroactive claim of full20scope.','status':'PENDING-FRESH-SUBSTANTIVE-SUCCESSOR-REVIEW'}]
a={'standing':'Mutually assessed source21 reference corrections. Source20 design-law assessment remains cumulative context, independently rejected20 has not accepted any successor.','recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finalSourceAssent':True,'independentAcceptance':False,'actualCoauthorHandoffs':prior['actualCoauthorHandoffs']+[ref(ev/'reference-hardening-after20.v1/assessment.json'),ref(peer/'assessment.json')],'actualCoauthorSessions':prior['actualCoauthorSessions']+['2bd2b874-fcf2-46b0-ac0a-4893d5721464',receipt['session_id']],'rootCoauthorAssessments':prior['rootCoauthorAssessments']+[ref(own/'coauthor-assessment.reference-hardening.v1.json'),ref(ap)],'predecessorManifest':ref(parent),'priorIndependentReview':ref(review),'priorRootAssessment':ref(own/'review-assessment.v20.json'),'cumulativeSource20Assessment':ref(own/'successor-source-assessment.v20.json'),'sourceDelta':m['changes'],'findingDispositions':items,'inheritedSource20FindingDispositions':prior['findingDispositions'],'normativeInputAdditions':prior['normativeInputAdditions'],'rootIntegrationQualifications':qualifications,'referenceEvidence':'Pending final allsix source-pinned commands; actual peer1596/0 plus mutation1594/2 and root synthetic timeout retained.','requiredNextActs':['Allfour pins and six final commands','Freeze21 including all31history files','Fresh actual independent21 fullfivecontracts and all changed laws with zero unresolved MUST/SHOULD','NEW blind9 complete semantic proof reconstruction','Complete independently reviewed application/readiness reconciliation'],'implementationAuthorized':False,'readinessChanged':False,'productQualification':False}
put(own/'successor-source-assessment.v21.json',a)
for row in m['changes']:
 cp(root/row['path'],own/'source-before-v21'/row['path']);cp(peer/row['overlay'],own/'source-proposal-v21'/row['path']);shutil.copyfile(peer/row['overlay'],root/row['path'])
put(dc/'post-reset-dispositions.v21.proposed.json',{'standing':'PROPOSED source21 corrections; fresh independent21, NEWblind9 and complete application remain required.','predecessorManifestSha256':sha(parent),'actualPredecessorReview':ref(review),'predecessorVerdict':'CHANGES_REQUIRED','predecessorRootAssessment':ref(own/'review-assessment.v20.json'),'items':items,'inheritedSource20Dispositions':ref(dc/'post-reset-dispositions.v20.proposed.json'),'actualCoauthorHandoffs':a['actualCoauthorHandoffs'],'finalSourceAssessment':ref(own/'successor-source-assessment.v21.json'),'advisoryAccount':'reviews/codex-post-reset.v1/advisory-application-account.v21.proposed.json','implementationAuthorized':False,'readinessChanged':False,'productQualification':False})
p=dc/'correction-crosswalk.proposed.json';cw=load(p)
for row in cw['items']:row['successorCorrection21']={'sourceAssessment':ref(own/'successor-source-assessment.v21.json'),'standing':'PENDING-FRESH-INDEPENDENT21-NEWBLIND-FULLAPPLICATION; no readiness grade'}
p.write_text(json.dumps(cw,indent=1)+'\n')
p=dc/'README.md';cp(p,own/'README.before-v21.md');p.write_text('''# Architecture corrections — source21 awaiting independent review

**Not ready for implementation.** Actual Claude and Codex strengthened the scope-selection regression checks, corrected their explanation and made reference-run timeouts produce explicit failure reports. Source20's design corrections remain included. The successor also includes all31unchanged protected historical files for direct review.

These are corrections to one complete intended design. Fresh source-pinned checks, independent acceptance with a full reading of the five contracts, a NEW blind consumer and complete independently reviewed application/readiness reconciliation remain required. [Resume guide](reviews/NEXT-REVIEW.md).

## Earlier progress — historical

'''+p.read_text())
print(json.dumps({'integratedPaths':3,'advisories':81,'rootSourceAssent':True,'independentAcceptance':False,'rootAssessmentSha256':sha(ap)}))
