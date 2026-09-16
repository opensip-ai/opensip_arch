"""Record substantive root decisions after completed actual reviews and measured replay.
No product or final application acceptance is granted by this record.
"""
from pathlib import Path
import hashlib,json,copy,shutil
B=Path('/tmp/opensip-design-corrections');ROOT=Path('/Users/sb/code/opensip-ai/opensip_arch');L=ROOT/'docs/coop/design-corrections/reviews';O=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
def ref(p):return {'path':str(Path(p).relative_to(ROOT)),'sha256':sha(p)}
mf=L/'candidate-subject.v45.json';assert sha(mf)=='8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155'
manifest=read(mf);src=Path(manifest['snapshotRoot']);old=B/'candidate-subject.v44'
D=L/'claude-independent-design.v45';C=L/'consumer-b.v24-source45.v1';d=read(D/'review.json');c=read(C/'blind-review.json');md=(D/'review.md').read_text()
assert d['verdict']=='ACCEPT' and c['verdict']=='ACCEPT-RECONSTRUCTABLE'
for j in (d,c):assert not j['newMustIssues'] and not j['newShouldIssues']
for name in ['root-independent45-public-custody.v1','root-blind45-public-custody.v1']:assert read(L/name/'verification.json')['result']=='PASS'
assert read(L/'root-blind45-query-assessment.v1/assessment.json')['result']=='PASS'
replay=read(L/'root-blind45-exact-replay.v1/verification.json');assert len(replay['runs'])==27 and all(r['passed'] for r in replay['runs'])
# Verify machine rows against the complete human report read by root, their actual
# previous row basis, and the named unchanged governing source files.
prev=read(B/'claude-independent-design.v44/review.json');counts={};audited=[]
for key in ['fDispositions','evaluationResidualDispositions','arDispositions','fwDispositions','inheritedResidualDispositions','scopedReviewOwnerDispositions']:
 rows=d[key];assert len({r['id'] for r in rows})==len(rows);p=prev[key];p=p if isinstance(p,dict) else {r['id']:r for r in p}
 for r in rows:
  assert r['currentAssessment'] in md and r['currentOwner'] in md and r['consequence'] in md,r['id']
  assert r['appliedByThisReview'] is False and r['finalApplicationOutcomeGranted'] is False
  assert r['prior44Disposition']==p[r['id']]['disposition']
  if r['assessmentBasis']=='unchanged-44-basis':
   assert r['unchanged44Basis']==p[r['id']]['currentAssessment'],r['id']
   own=r['unchanged44GoverningOwners']
   if own!='outside-snapshot':
    for name in own:
     candidates=[q for q in src.rglob(name) if q.is_file() and '/reviews/' not in str(q)]
     assert candidates,name
     assert any(q.read_bytes()==(old/q.relative_to(src)).read_bytes() for q in candidates),name
  audited.append({'id':r['id'],'basis':r['assessmentBasis'],'sourceCollection':key,'currentHumanAssessmentMatches':True,'priorBasisVerified':True})
 counts[key]=len(rows)
assert sum(counts.values())==107
for r in d['readScope']['inheritedUnchanged44Read']:
 assert sha(src/r['path'])==r['sha256']==sha(old/r['path'])
for r in d['readScope']['complete44ReadPlusComplete45Diff']:
 assert sha(src/r['path'])==r['sha45'] and sha(old/r['path'])==r['sha44']
for path,r in d['mapSources'].items():
 assert sha(src/path)==r['sha256']
 if r.get('sha44'):assert sha(old/path)==r['sha44']
for r in d['receiptInventory']:assert sha(B/'claude-independent-design.v45'/r['path'])==r['sha256']
for r in read(B/'root-independent45-inflight-read.v1/assessment.json')['reads']:assert sha(r['path'])==r['sha256']
assert d['commandReceipts']['referenceGroupsPassed'] and d['commandReceipts']['evaluator3ChildrenAllExit0']
assert not d['buildGaps'] and not d['readScope']['changedPriorReadNotReread'] and not d['readScope']['deltaFilesWithoutReadEntry']
audit={'standing':'Root read the complete final 624-line substantive design report, all107 current row assessments, both advisories, every item disposition/observation/limitation and TCB account. Machine metadata/209 receipt digests, 59 unchanged prior read bindings, three complete-diff bindings and prior row bases additionally verified. This is not a claim to newly read every unchanged source file or every byte of large JSON inventories. Focused scripts and receipts full-read record preserved separately.','rows':audited,'counts':counts,'result':'PASS'}
(O/'design-evidence-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
adv={
'A-c1':'Internal cb24 refusal keys are implementation naming freedom only where no owner publishes a key; public termination/detail routes remain closed and validated.',
'A-c2':'Carry the mandatory D9 successor publication on DR-007 and DR-011-R08. This application does not discharge publication or qualification.',
'A-c3':'Exact-snapshot imported observation identity intentionally changes with source; evidence-content-changed INDETERMINATE preserves confidence rather than silently trusting stale correspondence.',
'A-n1':'Closed reason precedence is deterministic; earlier unknown presence masks detector disposition by design. Preserve the measured explanation; no extra branch is owed.',
'A-n6':'The published language-mode table determines Rust membership. Duplicate restatement and retained-record enforcement beyond the selected reference scope are not required for reconstruction; product must apply the table.',
'A-v2-1':'Composition section7 closes outputs; workflow-owned Plan input documents have their own closure law. Keep the owner distinction, no universal string-prefix traversal.',
'A-v2-2':'Unreachable policy-derivation frames remain non-authoritative; full Run replay and reachable-output equality are the accepted boundary. Do not claim unreachable frames authoritative.',
'A-v2-3':'Closed vocabularies are owned by the selected bundle; native/relation digest laws extend their own domains explicitly. Consumer dispatch follows those owners.',
'A-s41-1':'Non-object private refusal spelling is not a missing public outcome. Reusing the section6 key at section7.6 preserves the registered route.',
'A-s41-2':'Apply the specific section1.2 allowJs derivation from checkJs before the omitted-value default. No competing deterministic recipe remains after owner precedence.',
'A-s42-1':'Enforce the explicit at-most-one default binding rule; the unassigned internal key is naming freedom, not permission to admit duplicates.',
'A-s42-2':'Native U-0 assigns ENUMERATION_BINDING_PROGRAM_ENTRY to the common entry join; apply it to default, derived and explicit mismatch.',
'A-s42-3':'Build the published default-unit syntax recipe. Explicit selection is a distinct Plan input and provenance, so it may produce a different identity; no claim that every historical representation must be refused.',
'A-s43-1':'Missing availability observation is a reference-only case; actual product host must provide its current availability record. Complete stored traversal alone does not prove native absence.',
'A-s44-2':'The absent pin ledger is absent from the blind normative kit, not the full frozen candidate. Published wire digest plus retained contract bytes determines Hello; no author ledger supplied to blind origin.',
'A-s45-1':'Retain as optional editorial cleanup in a future legitimate revision. Duplicated Historical wording changes no per-language payload law and is not an implementation blocker.'}
assert set(adv)=={r['id'] for r in c['advisories']}
blind={'rootBlindAssent':True,'fullRead':True,'actualSessionId':'9d3dfb70-b2d3-498c-a3c1-f8de9e488514','parentSubjectSha256':sha(mf),'review':ref(C/'blind-review.json'),'unresolvedRootMustIssues':[],'unresolvedRootShouldIssues':[],
 'standing':'Root accepts the exact final original blind-origin source45 reconstruction under the complete original charter; final application/readiness and product qualification remain separate.',
 'fullReadScope':'Complete final blind-review.md and substantive JSON fields, original current charter123requirements8standing3future, all134 requirement rows (125 verified unchanged from fully read44 rows plus9 fully read current changes), all16 advisory dispositions and limitations; HC60 source change read. Exact current artifacts verified by hash. No assertion of full line-read of all consumer implementation.',
 'assessment':'M-s44-1 was a real missing normative recipe, now resolved by the exact published seven-field pre-analysis record. Both language conversions carry it and refuse all four predecessor alternatives. Coverage remains unknown and repair false; no loading/dispatch absence is inferred. Root independently admitted and fully semantically replayed all27 exact exported Runs, without reminting, filling missing evidence or importing consumer implementation. The complete result carrier assessment covers66 query vectors;63 strong-owner capture cases agree structurally apart from documented diagnostics/optional fields and two legitimately foreign opaque tokens. Those two consumer-host pages have exact token binding, a fixed retained Run, ordered union equal to the independently validated unpaged result, and unchanged cache behavior. All32 success carriers preserve full human/JSON/agent parity;34 failures schema-admit. Missing/corrupt retained-byte controls refuse with the intended host-io routes. The in-memory tampered-verdict negative is consumer evidence, not claimed root exact-export replay.',
 'measurementVintage':'Fresh45 closure/replay, exports, query, native wire/startup, custody and retained negatives; exact prior phases1/2/4-8 and selected vector/mutation/tamper measurements reused with unchanged helpers and source owner bindings. All104 stores and27RunIds are unchanged44->45; no changed result is called identical. Source44 arithmetic corrected to370/473 identical, source45 is446/546 identical;89 transient process-id differences are explicitly scoped to non-authoritative replay diagnostics.',
 'scopeLimits':'Provider payload/transition reference traces are not complete retained Runs or real workers; descriptor custody, commitments, crypto, OS/process/compiler qualification remain unperformed as disclosed. P3-09/10 are abstract unreachable-from-admitted-frame table rows. Future obligations are not fabricated design gaps. Historical HC54 incoming-path ambiguity was partly an actual source42 law gap, not solely a consumer omission; retain original report and this root qualification.',
 'newAdvisoryApplicationAccount':[{'id':r['id'],'disposition':'CARRIED-NONBLOCKING','applicationAccount':adv[r['id']]} for r in c['advisories']],
 'evidence':[ref(L/x/y) for x,y in [('root-blind45-public-custody.v1','verification.json'),('root-blind45-exact-replay.v1','verification.json'),('root-blind45-query-assessment.v1','assessment.json'),('root-blind45-negative-query.v1','report.json')]],'implementationAuthorized':False}
contracts=read(L/'codex-post-reset.v1/design-assent.v36.json')['contracts']
design={'rootDesignAssent':True,'subjectManifestSha256':sha(mf),'actualSessionId':'85a08aec-9d22-4ac6-8ec2-c10170e727d7','independentReview':ref(D/'review.json'),'unresolvedRootMustIssues':[],'unresolvedRootShouldIssues':[],
 'standing':'Root substantive source45 design acceptance with actual nonauthor Claude independent-origin successor review. No final application/activation/product grade granted.',
 'assessment':'The exact seven-field record resolves the only remaining normative ambiguity at pre-analysis host conversion. Absence of observations yields unknown exports and no repair permission; none/not-applicable are scoped sentinels, not claims about analyzed repository behavior. Both normative owners, the converter and independently pinned case expectations agree. Three discriminating mutations reach their intended checker failures after positive admission. The full parsed case delta is three assertions across two existing cases, not477 new tests. Coverage2 payloads remain byte-identical44->45. The generic closed-world helper and other producers retain their independent scope. Per-language historical payload text now agrees with TypeScriptV1/RustV2/V3 negotiation; no registered schema shape changed. Five contracts and incorporated composition/query/enumeration/capture owners remain coherent on audited unchanged basis, with fresh reference corroboration and exact consumer replay. Layer13 binds changed inputs and preserves predecessors. Layout198files20packages, report24features, mappings322 and54planned recovery cases remain design obligations. No remaining source MUST/SHOULD demonstrated.',
 'reviewReadAndEvidence':ref(O/'design-evidence-audit.json') if False else {'path':'docs/coop/design-corrections/reviews/root-source45-assents.v1/design-evidence-audit.json','sha256':sha(O/'design-evidence-audit.json')},
 'contracts':[{'path':r['path'],'sha256':sha(src/r['path'])} for r in contracts],
 'advisoryApplicationAccount':[
 {'id':'ADV42-01','disposition':'CARRIED-NONBLOCKING','applicationAccount':'Require crates/host/src/analysis.rs implementation verification of receipt/view producer equality and every candidate view Plan join before producer filtering. Current measured foreign producers are refused at full closure; the two-provider case remains unexercised. This is a concrete host verification obligation, not a same-process containment proof.'},
 {'id':'ADV44-01','disposition':'CARRIED-NONBLOCKING','applicationAccount':'Optional future planning-layer direct binding of Rust protocol3 table and FactBatchV3; current formal candidate binds both and planning already binds their law through native-evidence. Preserve layer13 and all historical layers; no source rewrite solely for this advisory.'}],
 'sharedAssumption':copy.deepcopy(d['sharedAssumptionTCBSCOPE01']),
 'rootTrustAssessment':'Accept the selected authenticated in-process host/evaluator as trusted while treating providers and inert input bytes as untrusted. This is coherent with no imperative/executable report hooks and closed provider boundaries. It is one assumption with13joint dependents; it does not repair historical attacks or prove runtime containment. Production host admission, compiler/wire/cancellation/commitment validation and32release gates remain required.',
 'referenceScope':'Focused closed-world19rows are18checks plus1explanatory record. Own serializer independently canonicalizes the payload; coverage-id comparison uses two model admission returns, not a second standalone hash implementation. Startup reference takes trusted fixture host inputs and omits some inherited validation; complete27Run replay is separately measured. Sixgroups17children and other probe evidence remain scoped corroboration.',
 'evidence':[ref(L/'root-independent45-public-custody.v1/verification.json'),ref(L/'root-independent45-inflight-read.v1/assessment.json'),ref(L/'codex-post-reset.v1/final-reference.v45/reference-checks.json')],
 'implementationAuthorized':False,'finalApplicationGranted':False}
for n,j in [('design-assent.v45.json',design),('blind-assessment.v24-source45.v1.json',blind)]:
 (O/n).write_text(json.dumps(j,indent=2)+'\n');q=L/'codex-post-reset.v1'/n;assert not q.exists();shutil.copyfile(O/n,q)
shutil.copytree(O,L/O.name)
print(json.dumps({'designRootAssent':True,'blindRootAssent':True,'allIndividualRows':107,'finalApplication':'PENDING'}))
