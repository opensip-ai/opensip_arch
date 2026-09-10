"""Root substantive assessment of the completed actual Claude review, with measured limits."""
from pathlib import Path
import copy,datetime,hashlib,json,shutil,re
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews';own=ev/'codex-post-reset.v1';b=ev/'post-reset-review.v16'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
def ref(p,selector=None):
 d={'path':str(p.relative_to(root)),'sha256':sha(p)}
 if selector:d['selector']=selector
 return d
assert sha(b/'review.json')=='fe00b09c184c577e6c52b8ea33ea768362bf093b551ba0c83220908a034eff19'
assert sha(b/'review.md')=='097309ee97932b84c65375bfdf5c075d9e4dc2ad511ab8526feeca37cfa4590c'
r=load(b/'review.json');response=load(b/'response.json');assert response['is_error'] is False and response['session_id']=='543080e2-18a0-42f2-bfd7-29858aaed6bb'
assert r['overallVerdict']=='ACCEPT' and r['newMustIssues']==r['newShouldIssues']==[]
assert [x['id'] for x in r['newAdvisories']]==['V16-ADV-1','V16-ADV-2']
m=load(ev/'candidate-subject.v16.json');assert sha(ev/'candidate-subject.v16.json')==r['subjectManifestSha256']=='ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9'
base={x['path']:x for x in m['files']};c=load(b/'codex-retention-custody.json')
for x in c['files']:assert sha(b/x['path'])==x['sha256'] and (b/x['path']).stat().st_size==x['bytes']
fix=load(b/'codex-retention-correction.v1.json');assert fix['priorCustodySha256']==sha(b/'codex-retention-custody.json')
assert fix['rootSourceCopyAccounts']['sha256']==c['sourceCopyAccounts']['sha256']==sha(b/'codex-source-copy-accounts.json')
copies=load(b/'codex-source-copy-accounts.json');assert set(copies)=={'copy-A-reference-run','copy-B-probes'}
for name,x in copies.items():assert x['actualFiles']==len(x['unchangedFiles'])==6839 and x['changedFiles']==x['addedFiles']==x['deletedFiles']==[]
for name in copies:
 commands=load(b/('probe-03-run-six-checks.'+name+'.json'));assert commands['commandsExecuted']==6
 for x in commands['results']:
  assert x['exitCode']==0 and x['stderr']==''
  assert x['stdout']==(own/'final-reference.v16'/(x['name']+'.log')).read_text()
p4=load(b/'probe-04-rc-laws-totality.result.json');p5=load(b/'probe-05-scope-mint-pair.result.json')
p6=load(b/'probe-06-full-run-closure.result.json');p7=load(b/'probe-07-cx09-full-run.result.json');p8=load(b/'probe-08-repair-guard-projection.result.json');p9=load(b/'probe-09-lib-fold-and-context.result.json');p10=load(b/'probe-10-advisories-and-ordering.result.json');p14=load(b/'probe-14-preserved-laws.result.json')
assert len(p4['rows'])==257 and all(x['agrees'] for x in p4['rows']) and p4['unregisteredPairsTested']==178
assert len(p5['rows'])==197 and all(x['agrees'] for x in p5['rows']) and p5['negativeControls']==180
assert len(p6['rows'])==10 and all(x['retainedAgrees'] for x in p6['rows']) and not p6['harnessErrors']
assert sum(x['expectedProducer'] is not None for x in p6['rows'])==7
assert len(p7['rows'])==12 and all(x['producerAgrees'] and x['retainedAgrees'] for x in p7['rows']) and not p7['harnessErrors']
assert all(x['retainedDetail'].get('error','').startswith(('AdmissionError:','ValidationError:')) for x in p6['rows']+p7['rows'] if x['observedRetained']=='REFUSE')
q3=next(x for x in p7['rows'] if x['id']=='Q3-not-attempted-nonempty-classes');assert q3['producerDetail']['error'].startswith('ValidationError:exact enum type/value mismatch')
assert p8['previewAgree']==p8['previewCases']==12 and p8['schemaAgree']==p8['schemaCases']==10
assert p9['foldAgree']==7 and p9['joinAgree']==12 and p9['versionBindingGate']['gateEffective'] and p9['versionBindingGate']['referenceEnvironmentErrorIsNotAdmissionError']
assert p10['staticAgree']==29 and p10['orderingAgree']==17 and p14['lawsWithAllAnchorsPresent']==12
aggregate=257+197+17+24+22+19+46+12;assert aggregate==r['independentProbeCasesPassed']==594
assert len(r['priorFindingDispositions'])==22
assert len(r['arDispositions'])==16 and len(r['fwDispositions'])==15 and len(r['inheritedResidualDispositions'])==27 and len(r['scopedReviewOwnerDispositions'])==5
assert all(v['appliedByThisReview'] is False for k in ['arDispositions','fwDispositions','inheritedResidualDispositions','scopedReviewOwnerDispositions'] for v in r[k].values())
# Independently account inherited rows, rather than reusing the probe's 12-parent-token scan.
ids=[]
for line in (dc/'inherited-residuals.proposed.md').read_text().splitlines():
 if line.startswith('| DR-'):ids.append(line.split('|')[1].strip().split()[0])
assert set(r['inheritedResidualDispositions']) <= set(ids)
advice1={'id':'V16-ADV-1','severity':'advisory (nonblocking)','reviewEvidence':ref(b/'review.json','/newAdvisories/0'),'disposition':'Label V14-ADV-1 sourceCorrection explicitly as the as-of-v15 historical correction pin, preserving its original digest and historical source. Separately bind the current v16 native contract. No frozen source, historical review or pin is rewritten.','historicalSourceSubject':ref(ev/'candidate-subject.v15.json'),'currentSource':{'path':'docs/v2/contracts/product-v1/native-evidence.md','sha256':base['docs/v2/contracts/product-v1/native-evidence.md']['sha256']},'applicationObligation':'Carry the explicit historical context and current source reference into the separately reviewed accepted-review-advisories application record.','whyNonblocking':'Agreed: the preserved sourceCorrection denotes actual historical bytes and its substantive projection clarification survives in the accepted current contract. This is provenance clarification, not an admission defect.'}
advice2={'id':'V16-ADV-2','severity':'advisory (nonblocking)','reviewEvidence':ref(b/'review.json','/newAdvisories/1'),'disposition':'The Python reference uses unicodedata.unidata_version as the same-build proxy for the case data used by str.lower. This is a declared reference-environment assumption. An implementation that sources conversion and Unicode data independently must bind and verify the actual conversion tables to the selected UCD 15.0.0; checking an unrelated module version is insufficient.','applicationObligation':'Carry this assumption and equivalent-binding obligation explicitly in accepted-review-advisories; preserve the accepted normative bytes. No real alternate Unicode implementation or public host fault route was qualified by the probes.','whyNonblocking':'Agreed: the selected operation and version already determine the contract, and the reference gate refuses unavailable declared data. The advisory clarifies the mechanism and portability assumption without choosing a new operation or weakening the binding.'}
basis=[
 'I read the complete final 105893-byte JSON including all individually keyed scope records, complete 25228-byte Markdown and successful actual CLI receipt; final hashes match. Actual independent Claude session543080e2-18a0-42f2-bfd7-29858aaed6bb, claude-opus-5,162turns,zero permission denials/subagents. This is fresh v16 acceptance, not extension of earlier v15 acceptance.',
 'I agree with the normative scoped ADM-DOMAIN selection in both owning contracts. All13relations and relation-specific ladders remain explicit, and the v15-to-v16 registry membership is unchanged. The original CB5 finding was missing normative selection, not absence of the existing registry. Pair helper/mint probes corroborate the shared ladder law, not a separately executed full capability-manifest codec gate.',
 'I agree with the TS lib-name mapping, complete inventory and unique basename joins, raw unfolded ordering and configuration fold agreement. Independent Unicode and context probes retain exact expected refusals, valid selection, actual locale attempts and a simulated unavailable binding with a distinct environment error. The two revised expectations (J4 raw ordering and J7 declared duplicate versus tree ambiguity) are justified by the published rules; their failed results remain.',
 'I agree with RC0 membership, NA attempted/classes law, complete/not-attempted empty-class consistency and retained view-scope membership even without Coverage. Full-Run positive controls and actual typed refusal boundaries corroborate the earlier root counterexamples. Separate incomplete/partial controls preserve honest partial observations; stage/examined semantics are independent subject to their owning schema.',
 'I agree with exact repair projection and all-delete/replace guarding. Pure helper evidence is limited: it consumes already-admitted native records and satisfied evidence requirements, reads eligibility/reasons before projection, and applies no global dynamic veto. Invalid projection shapes do not measure security authorization, original evidence re-admission or destructive product execution. Valid present/not-applicable controls support the no-global-veto claim; absent/unknown are outside the native dynamicDispatch enum and provide no native-admission evidence.',
 'Both6839-file copies remain exactly equal to the frozen manifest, and all six logs from both copies match the final root logs byte-for-byte. All1308pins verified without repinning. Foundation1679 includes1331identity passing calls over1319distinctIDs; no product qualification or exhaustive coverage inferred.',
 'The594 figure is a reproducible mixed expectation aggregation, not594 independent product tests:257 helper rows+197mint rows+17producer/retained expectations+24producer/retained expectations+22preview/schema checks+19fold/context checks+46static/ordering checks+12anchor-preservation checks. Exceptions, schema masking, invalid pure-helper inputs, reused fixtures and static checks retain their precise limits below.',
 'Both new advisories are accepted at original nonblocking severity and individually accounted, including historical pin context and same-build Unicode proxy assumption. They require no mutation of the accepted design during blind/application stages. All earlier required/advisory finding severity and original failed evidence remain preserved.',
 'All16AR15FW27inherited30evaluation records remain preservation-only; five owner rows remain routing-only with appliedByThisReviewfalse and explicit no-grade authority. These are not application grades. The separate full application reviewer must substantively assess every proposed outcome and all32unperformed qualification gates.',
 'Fresh blind reconstructability and complete independent application/readiness reconciliation remain required. No implementation, commit/push, product compiler/OS/storage/crypto qualification or readiness change is inferred.'
]
qualifications=[
 'probe04 has178 unregistered cross-product pairs at coverage_bijection, not180. probe05 has180mint negatives (178cross-product plus two unknown-token controls). Its separate probe04 mintCases still contain three correctly disclosed failed positive constructions, excluded from the594 main aggregate and superseded by probe05.',
 'probe06 producerAgree10 counts three null producer expectations; actual producer invocations are7 plus10retained expectations=17, which the review aggregate correctly uses. No-Coverage scope controls have no producer boundary to exercise.',
 'probe07 Q3 uses unregistered dynamic-import-expression and refuses at schema enum, so its two successful refusal expectations do not isolate the new not-attempted empty-class guard. Registered-class helper/coauthor controls and the source guard establish that law; Q1 isolates complete empty-class law through fullRun.',
 'probe08 R7 dynamicDispatch absent/unknown are outside ClosedWorldV2 enum (resolved,present,not-applicable). The pure workflow helper assumes admitted native evidence and does not validate these invented inputs. Exclude those two rows from claims about admitted native contexts; no product host bypass inferred. Evidence requirements are empty in this probe, so target-relative semantic sufficiency is assessed from the owning contract/source, not dynamically demonstrated here.',
 '594 includes static substring/shape checks and duplicated-boundary expectations, with no comprehensive or product-coverage meaning. Final summary saying allnineCX corrected in admission overstates precision: several are explicitly prose/docstring/report clarifications; exactsource account and individual dispositions own scope.',
 'The onlyStructuralJsonChange statement is limited to the five selected normative JSON comparisons. Pins, generated reports and governance JSON also changed structurally. Adding two valid fixture fields is fixture correction, not a changed schema constraint. The refusal-only description is a semantic assessment, not a literal claim that every added line is a refusal.',
 'probe13 inheritedResidualCount12 scans DR001..012 parent tokens; it is not the full27obligation set. The actual report individually preserves11parents+16subresiduals, and root verifies those IDs directly. Its45-to50 advice comparison is against v15 PROPOSED account; the completed v15 assent had46, so successor50 actually adds the four CB5advisories to46, carrying V15ADV1. No advisory was dropped.',
 'Eight failed-attempt artifacts are retained, but six-plus-two shorthand conflates attempts and cases: attempt04 contains two revised expectation cases, while attempt08 is a corpus/hardwrap probe defect. Preserve exact eight item descriptions instead of treating shorthand as eight disjoint classes.',
 'The825reference scan yields71raw mismatches;70are disposable-copy state under their own frozenv15base and one is the historical V14ADV1source pin. Relative-path failures in the first scan were scanner errors. No blanket825current-live-source match claim.',
 'Final pin seal was actually executed by root and independently verified. The live NEXT guide update was a separate root recording command after launch, not a write by launch-review-v16.py itself; reviewer correctly disclaims ownership. Frozen NEXT remains unchanged.',
 'All-write-custody assertions concern reviewer-directed outputs; actual CLI session/shell metadata lives in its normal external runtime directories. No private thinking content retained. Actual Python IO/hashlib and OS locale calls executed; no product qualification inferred.'
]
out=own/'review-assessment.v16.json';assert not out.exists()
out.write_text(json.dumps({'standing':'Root full substantive assessment of actual completed independent v16 review. Technical assent only; blind and application remain required.','recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actualReviewSession':response['session_id'],'reviewSha256':sha(b/'review.json'),'markdownSha256':sha(b/'review.md'),'fullRead':True,'rootDesignAssent':True,'unresolvedRootMustIssues':[],'unresolvedRootShouldIssues':[],'basis':basis,'newAdvisoryApplicationAccount':[advice1,advice2],'evidenceQualifications':qualifications,'reportedProbeExpectations':aggregate,'actualCustody':ref(b/'codex-retention-custody.json'),'sourceCopies':ref(b/'source-copy-accounts.json'),'implementationAuthorized':False,'readinessChanged':False,'blindAccepted':False,'applicationAccepted':False},indent=2)+'\n')
print(json.dumps({'actualReviewSession':response['session_id'],'rootSourceDesignAssent':True,'newAdvisories':2,'reportedMixedExpectations':aggregate,'blindRequired':True,'applicationRequired':True}))
