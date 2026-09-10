import json, pathlib
D = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2')
h = json.loads((D / 'evidence/handoff-skeleton.json').read_text(encoding='utf-8'))

h['rootPointDispositions'] = [
 {'id':'CX-BV6-01','severity':'MUST','disposition':'CORRECTED. My CB6-NEW-3 deferral is WITHDRAWN.',
  'agreement':'Full. Deferring a demonstrated violation of existing published law was not defensible.',
  'whatWasDone':'coveragePartitionLaw published in the relation registry beside coverageTotalityLaw; identity-model READS its partitionKey and enforces per-view subject disjointness at retained Run closure; seven full-Run controls.',
  'proposalBoundariesAssessed':{
   'groupingKey':'ACCEPTED - equals the registry matchOn and the tuple already stated in identity section 3, so the enforced key and the stated key are one object.',
   'perViewIsolation':'ACCEPTED and controlled by a full Run with one scope referenced by two views.',
   'scopesWithoutCoverage':'ACCEPTED and controlled. Wording corrected per the Codex note: they bypass the per-Coverage PRODUCER guard but still reach the retained-scope ladder guard, so saying they reach no other check would be false.',
   'singleProducerLimit':'ACCEPTED - admit_coverage_result_v3 sees one scope and cannot decide a between-scopes property.',
   'placement':'NOT adopted as proposed. The overlap test runs AFTER every scope passes its own well-formedness checks, so a foreign-snapshot or unselected-enumerator scope refuses as ITSELF.',
   'authority':'NOT adopted as proposed. The key is published in the registry and READ by the model rather than hardcoded in it.'},
  'codexPrecisionPointsApplied':[
   '(1) scopes without Coverage bypass the per-Coverage producer guard; the ladder guard still applies to them',
   '(2) the reported subject is min by UTF-8 BYTE order, named exactly and implemented as such; canonical-JSON order is explicitly not equated with it, and only which subject is reported depends on it',
   '(3) whyItIsNeeded now says an invalid partition was ACCEPTED and that claims over such a view can be ambiguous or double-counted, without asserting that every consumer necessarily double-counts'],
  'identityConsequenceDisclosed':'Adding the law to the relation registry changes that registered schema document digest, which is committed in view.schemaDigests, so retained-Run identities over fixtures move. Ordinary consequence of editing a committed schema document, not a defect, and disclosed because the root probe baseline RunId visibly changed.'},
 {'id':'CX-BV6-02','severity':'SHOULD','disposition':'CORRECTED.','agreement':'Full; reproduced exactly.',
  'whatWasDone':'admit_evidence_requirement now requires an actual bool for satisfied, distinguishes key PRESENCE from value so an explicit null refuses in both branches, and routes every violation to CONFIG.INVALID as validate_import_record and admit_atom do. Root’s five-case probe now agrees on all five.',
  'commentCorrected':'The claim that the boundary holds "even when a host skips schema validation" is gone. The controls now assert that two boundaries deciding one law AGREE on an enumerated table, and separately record the two cross-plane rows the schema cannot decide.',
  'scopeAcknowledged':'Root is right that the five-case comparison is not a whole-product exploit claim; the defect was two boundaries claiming one law and disagreeing.'},
 {'id':'CX-BV6-03','severity':'MUST','disposition':'CORRECTED, then REWORKED after the Codex note.',
  'agreement':'Full. My v1 importSemanticsPreserved answer addressed imported-prepared NATIVE Runs, a different plane.',
  'whatWasDone':'A separate owning law in imported-evidence.schema.json with seven outcomes, each bound to the payload field that grounds it; a mirrored ImportedRequirementDeficiency; EvidenceRequirement.deficiency as a plane-tagged union with the plane decided at admission from registry membership; and a reference projection implementing per-kind precedence.',
  'codexCoherencePointsApplied':[
   '(1) SATISFIED no longer means POSITIVE. observable-unhit is bounded NEGATIVE evidence that can satisfy, and the disclosure carries the polarity. Optional absence is satisfiedBy declared-optional-absence, i.e. by ABSENCE, not by evidence.',
   '(2) The wording no longer says imported evidence can NEVER affect applicability. It can never BY ITSELF establish the native closed world or authorize an unsafe delete/replace, but it may be an ADDITIONAL required condition; both directions are controlled by real repair_preview cases.',
   '(3) The optional projection is explicit and bound: required is NEVER defaulted to optional, so an unsupplied or unknown evidenceUse declaration is REQUIRED and an unresolved condition is never silently satisfied.',
   '(4) Every input is bound to an owning field. targets come from RepairPlanDescriptor.targets, not from EvidenceRequirement, and no field is added to that record; all-versus-any is the EXISTING completeness field; required-versus-optional is evidenceUse; the window demand is the admitted recipe’s. The projection is documented as PURE over already-admitted inputs and does not claim to validate an opaque Run or to admit payload, observation scope or polarity.',
   '(5) History is NOT projected through runtime fields. HistoryPayloadV1 carries revisionRange and collectionScope and has no observationWindow/observedPopulation/observability, so history has its own two outcomes, neither kind may report the other’s, and the producer refuses rather than borrowing.'],
  'rootCounterexampleResolved':'root-input/imported-target-draft.v1.json (complete over [seen, missing], only seen observed) returned satisfied=true under the draft any(). Against final bytes it returns import-absent-for-requirement, and partial-acceptable over the same inputs still satisfies. Both directions controlled.',
  'preserved':['both imported relations remain admissible requirement relations','the original evidence Run remains the authority','per-target evaluation','window/population and revision-range bounds travel with the outcome','required-versus-optional stays with evidenceUse','no D9 widening, no new rung, and no universal non-use inferred from cold observations']},
 {'id':'CX-BV6-04','severity':'SHOULD','disposition':'CORRECTED, then MATERIALLY REVISED after the Codex note.',
  'agreement':'Full, including on the point where the note corrected my own initial v2 assessment.',
  'whereMyAssessmentWasWrong':'My initial v2 assessment concluded that no import or native-preparation receipt operation was established and proposed to disclose them as operations with no published emitter. Codex is right that this confuses (a) a reference model not exercising a production emitter with (b) a missing design law for a REQUIRED receipt. I verified the citations myself: ImportResult and NativePreparationResult BOTH require receiptId; ReceiptId is receipt2:; workflows section 10 declares exactly one receipt domain, workflow.mutation-receipt; and MutationReceiptV1 REQUIRES operation. Both steps already owed a receipt carrying an operation and only the binding was missing.',
  'whatWasDone':'Published byStepKindReceiptOperation - a deterministic step-kind to receipt-operation law for mutation, repair-apply, import and native-preparation, each with its owning result/params citations - alongside byCommandGenericMutationStep (20 command rows) and admissibleGenericFieldDomain (the actual 23 tokens). The conflated genericMutationClasses key is removed.',
  'analyzeResolved':'Not an exception. The binding is by STEP KIND and not by request class, so analyze’s import step carries the operation import exactly as the import command’s does. The checker’s v1 subtraction of analyze is removed.',
  'injectivity':'DROPPED as a law and replaced by a worked counter-case: import is emitted by TWO commands (import and analyze), so the map is explicitly not invertible. Injectivity of the 20 generic rows is recorded only as an observation about the current inventory.',
  'noNarrowing':'The generic field domain remains all 24 members except repair-apply = 23 tokens, verified by admitting each at the actual field schema. config-write stays admissible although no step kind binds it.',
  'preserved':['no auto-retry and no native execution introduced','import custody and source-correspondence joins unchanged','a fresh native preparation is a new authorized execution, never a generic delivery replay','no new authorization or permission']},
 {'id':'CX-BV6-05','severity':'SHOULD','disposition':'CORRECTED.','agreement':'Full.',
  'whatWasDone':'The unit prerequisite is scoped to the five rows naming a COMPILATION universe. syntax-only explicitly carries no such prerequisite, has no compilation unit, and is the path for a repository where U-1 yields no TS or Rust unit; such files are syntax-only membership with unitOrdinal null under U-4. The bare-JS clarification stands without the over-general claim.'},
 {'id':'CX-BV6-06','severity':'SHOULD','disposition':'CORRECTED.','agreement':'Full.',
  'whatWasDone':'Section 4.6, the native registry block and the field description now state the PROJECTION law: the full producer result is {satisfied, deficiency?, disclosures, causes}, causes is returned on both branches and disclosures may be non-empty on the failing branch; the record carries the satisfaction/deficiency projection only, and causes and disclosures stay with the producer and the retained Coverage. Per-requirement cause, retained Coverage cause and public D9 detail remain distinct and none is dropped.'},
 {'id':'CX-BV6-07','severity':'SHOULD','disposition':'CORRECTED, all four items.','agreement':'Full.',
  'items':['the unverified external TypeScript claim is removed from the law and the prose, replaced by the internal rationale (total, decidable from the retained path, already what the model derives)',
   'the ordering claim is corrected: the candidate digest IS computed and compared before typescript_config_graph_faults; what never happens is ADMISSION of the universe or acceptance of an identity',
   'the drift claim is scoped by a new driftScope key: model and table cannot drift because the model reads the table; prose agreement is not established by that control and is not claimed',
   'the ADV-2 imported/non-native example is removed - imports mint no ViewEntryV3 and no such path is invented. The global native provider exact-confidence scope is retained, as root accepts it is defensible.']},
 {'id':'CX-BV6-08','severity':'SHOULD','disposition':'CORRECTED.','agreement':'Full.',
  'v1EvidenceCorrections':[
   'v1 said every write was under the v1 output directory. FALSE: /tmp/cb6_*.py, /tmp/bl-*.json, /tmp/w1-w4.json, /tmp/i2-i4.json, /tmp/id2.json, /tmp/id3.json, /tmp/probe-cw.json and /tmp/cb6-delta*.json were written outside it.',
   'v1 said D9Deficiency is byte-unchanged. FALSE: only its ENUM is unchanged; I added a description to that definition.',
   'v1 said config-write occurs in exactly one place across the whole live tree. OVERSTATED: the search covered this subject snapshot excluding reviews/. Now scoped to the command inventory, the four step-kind bindings and that source tree.',
   'v1 called byCommand keyed both ways. It is NOT an inverse map; import is now a worked case of one operation emitted by two commands.',
   'v1 said no filesystem was executed. IMPRECISE: Python read, wrote and hashed files throughout. What was not performed is product execution or host/OS durability qualification.',
   'v1 said DomainDetailCode carries five members. It is a 287-member registry; the statement concerns its intersection with the nine native outcomes, and the control now says so.',
   'The generated native-evidence-report.v2.json in v1 work was overwritten by an unpinned run and restored byte-exactly. Disclosed in v1 and retained here.',
   'run-six.sh lacked pipefail and is not the canonical six. v2 run-suites.sh sets pipefail, is labelled not-canonical, and every verdict is read from the suite report JSON.',
   'The disposable copy excludes most of reviews/ and reuses report filenames, so not every intermediate report version or full stdout is retained.'],
  'methodCorrection':'The two v1 prose-substring/wrapping controls are REMOVED rather than repaired, and replaced by full-Run enforcement of the same reconciled wording. No new prose-substring or wrapping control was added in v2, and no suite was re-run after every edit.'}]

h['originalFindingDispositions'] = [
 {'id':'CB6-MUST-1','origin':'blind v6 MUST-1','severity':'MUST','disposition':'CORRECTED in v1; EXTENDED in v2 - the field is plane-tagged, its presence law is typed, its error routing is consistent, and the v1 only-producer claim is corrected.'},
 {'id':'CB6-MUST-2','origin':'blind v6 MUST-2','severity':'MUST','disposition':'CORRECTED in v1; substance unchanged in v2. Three rationale/precision statements corrected under CX-BV6-07.'},
 {'id':'CB6-SHOULD-1','origin':'blind v6 SHOULD-1','severity':'SHOULD','disposition':'CORRECTED in v1; MATERIALLY REVISED in v2 under CX-BV6-04 - three published lists separated, receipt-operation law added, injectivity dropped.'},
 {'id':'CB6-SHOULD-2','origin':'blind v6 SHOULD-2','severity':'SHOULD','disposition':'CORRECTED in v1 as text; in v2 the disjointness half is ENFORCED at retained Run closure, so the reconciled wording is held by behaviour rather than by assertion.'},
 {'id':'CB6-ADV-1','origin':'blind v6 ADV-1','severity':'nonblocking advisory','disposition':'CLARIFIED in v1; SCOPED in v2 under CX-BV6-05 so it no longer contradicts compiler-free syntax-only.'},
 {'id':'CB6-ADV-2','origin':'blind v6 ADV-2','severity':'nonblocking advisory','disposition':'CLARIFIED in v1 with a recorded disagreement from the reviewer’s inference; retained in v2 (root accepts the global provider law as defensible) with the imported/non-native example removed under CX-BV6-07.'},
 {'id':'CB6-ADV-3','origin':'blind v6 ADV-3','severity':'nonblocking advisory','disposition':'CARRIED FORWARD in v1 as a mandatory cross-unit obligation; unchanged in v2. Inherited d9-exit-contract.v1.14.json bytes still untouched.'},
 {'id':'CB6-NEW-1','origin':'own','severity':'observation','disposition':'RETAINED. Four command/operation name mismatches among the generic rows, not three; still held equal to the derived set.'},
 {'id':'CB6-NEW-2','origin':'own','severity':'observation','disposition':'CORRECTED AND NARROWED. v1 named one orphan; my v2 assessment widened it to three; the Codex note showed import and native-preparation have REQUIRED receipts, so they are bound by the new step-kind law and only config-write remains unbound. My interim widening was wrong and is withdrawn.'},
 {'id':'CB6-NEW-3','origin':'own','severity':'limitation','disposition':'WITHDRAWN. The deferral was not defensible; disjointness is enforced under CX-BV6-01.'},
 {'id':'CB6-NEW-4','origin':'own, this turn','severity':'observation','disposition':'DISCLOSED. Editing a registered schema document (relation-payload-schemas.v2.json) changes its committed digest and therefore moves retained-Run identities over fixtures. Expected, not a defect, and visible in the root probe baselines.'}]

h['referenceControls'] = {'interpreter':'/tmp/opensip-architecture-review-env/bin/python -I -B',
 'counts':{'foundation/check-foundation.py':{'v1':231,'v2':231},'foundation/check-identity.py':{'v1':1338,'v2':1345},
  'security/check-security-lifecycle.v1.py':{'v1':456,'v2':456},'native/check_native_evidence.v2.py':{'v1':355,'v2':355,'unit':'cases'},
  'workflows/check_workflows.v1.py':{'v1':1672,'v2':1761},'check-integration.py':{'v1':378,'v2':388}},
 'whatTheseControlsAre':'SCHEMA-level jsonschema validation; HELPER-level direct calls into the reference models over synthetic already-admitted inputs; FULL RETAINED-RUN closure for the CX-BV6-01 partition controls and for the repair_preview cases. HOST ENFORCEMENT: NONE. No provider, compiler, renderer, ledger or product emitter was executed, and no control demonstrates that a host obeys any of this.',
 'notMirroredImplementation':'Parity controls compare a workflows mirror against the OWNING authority document; the config-kind and partition controls compare model behaviour against the PUBLISHED table the model reads. No control asserts the model equals a second copy of itself.',
 'countHonesty':'These are check rows and case rows, not distinct properties and not exhaustive coverage. The workflows delta is inflated relative to distinct assertions because 23 rows are one per admissible operation and several are one per vocabulary member.'}

h['executedCommands'] = {
 'where':'/tmp/opensip-design-corrections/bv6-corrections-author.v2/disposable/checker-run.v1, a SEPARATE disposable repinned copy. work/ was never repinned; its four source-pins files are byte-unchanged and therefore stale, which is expected and is neither a product failure nor a PASS.',
 'notTheCanonicalSix':'run-suites.sh sets pipefail and is explicitly NOT the canonical final six. Root runs the canonical six after final source, records and pins. Every verdict below is read from the suite’s own report JSON, not from a shell exit status.',
 'disposableCopyDeltas':['excludes docs/coop/design-corrections/reviews/ except the three author-feedback files the pin manifests name, copied in individually',
  'repin.py refreshed 58 pin rows across the four manifests; those pins exist ONLY in the disposable copy',
  'the suites rewrite their own report files there; those regenerated reports exist ONLY in the disposable copy',
  'report filenames are reused across runs, so not every intermediate version is retained'],
 'results':[{'suite':'foundation/check-foundation.py','result':'PASS 231/231'},
  {'suite':'foundation/check-identity.py','result':'1345 passed, 0 failed'},
  {'suite':'security/check-security-lifecycle.v1.py','result':'456/456, 10 sweeps true'},
  {'suite':'native/check_native_evidence.v2.py','result':'PASS 355/355 cases, uncovered feedback []'},
  {'suite':'workflows/run-reference-checks.py','result':'pins valid, 1761/1761'},
  {'suite':'check-integration.py','result':'388 passed, failed []'}],
 'rootProbesReRunAgainstFinalBytes':[
  {'probe':'probe-bv6-scope-overlap-v3.py','before':'overlap ADMITTED','after':'overlap REFUSES SUBJECT_SCOPE_PARTITION_OVERLAP:references@resolved-binding:foo; disjoint and different-relation still ADMIT','evidence':'evidence/final-probe-bv6-scope-overlap-v3.json'},
  {'probe':'probe-bv6-scope-no-coverage-v1.py','before':'overlap with no Coverage ADMITTED on final v1','after':'REFUSES with the same cause; disjoint-no-coverage still ADMITs','evidence':'evidence/final-probe-bv6-scope-no-coverage-v1.json'},
  {'probe':'probe-bv6-requirement-draft.py','before':'helper admitted two shapes the owning schema refused','after':'helper and schema agree on all five; every refusal is CONFIG.INVALID','evidence':'evidence/final-probe-bv6-requirement-draft.json'},
  {'probe':'probe-bv6-imported-requirement-draft.py','after':'the boundary now reports plane `imported` for both relations instead of treating them as native','evidence':'evidence/root-probe-imported-reproduced-after.json'},
  {'probe':'probe-bv6-mutation-map-draft-v2.py','after':'CANNOT RUN UNMODIFIED: it reads m[genericMutationClasses], the key this correction removed because that key WAS the conflation. Its unmodified failure is retained; probes/probe_cx04_map.py asks the same question against the corrected structure and reports fieldDomainMatchesSchemaExactly=true over 23 operations.','evidence':'evidence/root-probe-mutation-map-unmodified-fails-on-removed-key.txt, evidence/probe_cx04_map.result.json'},
  {'probe':'root-input/imported-target-draft.v1.json counterexample','before':'draft returned satisfied=true for complete over [seen, missing]','after':'returns import-absent-for-requirement; partial-acceptable over the same inputs still satisfies','evidence':'evidence/probe_cx03_targets.result.json'}],
 'preservedFailedAttempts':[
  {'what':'probe_cx01_partition first attempt','cause':'HARNESS defect, not a design result: the second scope had identical subjects, so it had the same identity and its Coverage id duplicated inside evidence.coverageIds, refusing on uniqueItems before the partition law ran.','retained':['evidence/probe_cx01_partition.first-attempt.py','evidence/probe_cx01_partition.first-attempt.result.json']},
  {'what':'repair.boundary-and-schema-agree rows 10 and 11','cause':'MY control asserted too much: it required schema and boundary to agree on the two CROSS-PLANE rows, which the schema cannot decide because relation is not an enum. Replaced by two controls that record exactly where the schema stops.','retained':['evidence/workflows-report.boundary-agreement-first-attempt.json']},
  {'what':'my initial v2 assessment of CX-BV6-04','cause':'I concluded import and native-preparation had no published emitter. The Codex note showed both results REQUIRE a receiptId. Corrected in the final source; the wrong reasoning is retained verbatim.','retained':['assessment/assessment.json','assessment/assessment.md']}],
 'disposableCopyRoots':['/tmp/opensip-design-corrections/bv6-corrections-author.v2/disposable/checker-run.v1']}

h['whatWasNotTouched'] = ['bv6-corrections-author.v1 and its handoff','all root-input files','every generated report in work/',
 'all four source-pins manifests in work/','correction crosswalk, historical preservation reports, post-reset dispositions, qualification gates, validation summary',
 'docs/coop/artifacts/d9-exit-contract.v1.14.json and every inherited historical artifact','the blind v6 report and its output directory',
 'the live repository at /Users/sb/code/opensip-ai (read-only throughout)']

h['limitations'] = {
 'evidenceClass':'Design reference evidence over synthetic trusted inputs. No compiler, provider, repository, renderer, ledger or product emitter was executed. Passing controls is not product qualification.',
 'referenceModelVersusDesignLaw':'The reference model emits a MutationReceiptV1 only for repair-apply and does not exercise a production import or native-preparation receipt emitter. That is a stated qualification limit, deliberately distinguished from the design law, which is normative and complete.',
 'importedProjectionIsPure':'imported_requirement_outcome is a pure projection over inputs an authenticated importer and the retained Run closure have already admitted. It does not validate an opaque Run, re-derive source correspondence, or admit payload, observation scope or polarity.',
 'multiViewFixture':'The shared integration fixture builds one view per Run. The per-view isolation control constructs a second view directly and adds its proof evaluationInputRef; it is a synthetic construction, not a producer-generated multi-view Run.',
 'identitiesMoved':'Editing relation-payload-schemas.v2.json changes a committed schema document digest and therefore moves retained-Run identities over fixtures. Disclosed, expected, not a defect.',
 'stalePinsInProposedCopy':'Expected. Root refreshes pins after final source and records, then runs the canonical six.',
 'notReviewed':'I did not re-derive the blind v6 positive reconstruction, its 78 vector groups or its 355 retained objects; the v1 reservations about that reconstruction stand unchanged.',
 'successorStillOwed':'A fresh independent Claude review and a NEW blind consumer on the accepted successor bytes remain required. This is coauthor assent to exact bytes, not agreement, acceptance or readiness.'}

h['independence'] = False; h['blindAcceptance'] = False; h['readinessChanged'] = False
h['productQualification'] = False; h['implementationAuthorized'] = False
h['codexAgreement'] = 'NOT CLAIMED. Codex has not assented; this handoff exists so Codex can check the final bytes.'
(D / 'handoff.json').write_text(json.dumps(h, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print('written', len(json.dumps(h)))
