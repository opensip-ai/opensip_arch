# Executed by build_review42.py in its own globals (exec). The 107 individually reasoned rows with current owners and
# consequences, the single TCB-SCOPE-01 object, retained obligations, authority and limitations. Flags are always false.

N, I = 'new-42', 'unchanged-40-basis'
BASIS_RULE = ('unchanged-40-basis: the governing owner bytes are byte-identical 40->42, and the conclusion rests on that identity plus this origin\'s named source40 row assessment, quoted in unchanged40Basis. '
              'Re-executed suites are corroboration only. new-42: the conclusion rests on a source42 read, diff, probe or measurement newly performed under this charter. '
              'Every row carries its own current text, current owner and consequence; no row is carried forward in bulk, and no grade is assigned.')
V40ROWS = {r['id']: r for k in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions') for r in V40[k]}
TCB_DEPS = ['RES-EP13-02', 'RES-EP13-04', 'RES-EP13-12', 'RES-EP13-13', 'RES-EP13-16', 'RES-EP13-18', 'IR-EP13-NB-01', 'IR-EP13-NB-03', 'IR-EP13-NB-04', 'AX6', 'AX9', 'MD5', 'RX2c']


def base_row(rid, basis, disposition, assessment, owner, consequence, **extra):
    prior = V40ROWS.get(rid)
    if prior is None:
        GAPS.append('no source40 row for ' + rid)
    r = {'id': rid, 'prior40Disposition': prior['disposition'] if prior else None, 'disposition': disposition, 'assessmentBasis': basis,
         'unchanged40Basis': (prior['assessment'] if (prior and basis == I) else None), 'currentAssessment': assessment,
         'currentOwner': owner, 'consequence': consequence}
    r.update(extra)
    r.update(appliedByThisReview=False, finalApplicationOutcomeGranted=False)
    return r


RESOWN = 'evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review'
F_ROWS = []
for i in range(1, 15):
    rid = 'F-%02d' % i
    st = V40ROWS[rid]['priorRootStanding']
    F_ROWS.append(base_row(rid, I, 'CARRIED-NOT-REGRADED',
                           '%s: prior root standing %s (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record.' % (rid, st),
                           'root custody of the F record (outside the frozen snapshot)', 'No source42 change; remains carried without regrade and is not source42 acceptance.',
                           priorRootStanding=st))

RES_TEXT = {
    'RES-EP13-01': (N, 'Plan and derivation joins stay inside complete replay: the three-tree probe closes lawful worlds and refuses foreign named scopes and reminted receipts at Run closure on the same manifests (P42-VIEW-ATTRIBUTION-X), and the full-replay child passes.', 'Grade PENDING; residual retained.'),
    'RES-EP13-02': (N, 'Depends on TCB-SCOPE-01. Capture remains a host observation of stage returns; a non-provider-producer view on a receipt is refused only at closure (ADV42-01), so no answer-provenance claim against the host is made.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-03': (I, 'Admission contract and residual ledger are byte-identical 40->42.', 'Grade PENDING; finite historical measurement unchanged.'),
    'RES-EP13-04': (N, 'Depends on TCB-SCOPE-01. Closed input admission now also refuses foreign named scopes on attributed views, internally inconsistent receipts, and explicit TS/JS bindings with null entries (P42-VIEW-ATTRIBUTION-X, P42-PROGRAM-ENTRY-X).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-05': (N, 'The frozen subject was verified outside every author instrument: formal42 manifest, archive, all 12,913 members, parent41 (12,912) and last-reviewed40 (12,911), declared chain and both deltas.', 'Grade PENDING.'),
    'RES-EP13-06': (N, 'canonical.py is outside the delta; the ported run-termination probe recomputes the commit-inventory digest over a closed source42 Run with the reviewer\'s own C()/H().', 'Grade PENDING.'),
    'RES-EP13-07': (I, 'Seal and replay owners are byte-identical 40->42; the analysis-seal child passes.', 'Grade PENDING.'),
    'RES-EP13-08': (I, 'A bounded historical measurement; source42 claims no proof over all PlanIntents.', 'Grade PENDING.'),
    'RES-EP13-09': (N, 'Provenance stays distinct from correctness: semantic-controls1 keeps owner ADMIT and semantic REFUSE, content-equal to the root final42 verification, and a foreign coverage-less scope that source40 admitted and closed now refuses.', 'Grade PENDING.'),
    'RES-EP13-10': (N, 'Author self-counters did not decide this review: the 19 added checker cases are reference self-consistency, and the independent three-tree discrimination runs each tree\'s own modules.', 'Grade PENDING.'),
    'RES-EP13-11': (N, 'Failures stay recorded by cause: this review keeps its programEntry probe attempt 1 harness failure, and root reference v1 (pre-correction) and v2 (launch failure) are not used.', 'Grade PENDING.'),
    'RES-EP13-12': (N, 'Depends on TCB-SCOPE-01. No sole Python guard enters product authority; SELECTED_COVER detects internal capture inconsistency, never malicious omission.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-13': (N, 'Depends on TCB-SCOPE-01. Discrimination probes run each tree in its own process on verified copies, all re-verified unchanged afterwards (copy-verification-final.json).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-14': (I, 'The differential census is not used as an oracle; unchanged.', 'Grade PENDING.'),
    'RES-EP13-15': (N, 'The C-2 v4 self-census is not elevated: the enumeration programEntry change is exercised by the 54-case checker and the independent 24-case owner probe, not by a census.', 'Grade PENDING.'),
    'RES-EP13-16': (N, 'Depends on TCB-SCOPE-01. Producer flags cannot bypass replay: row attribution is re-derived at admission and compared exactly (VIEW_TOTALITY on every tree).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-17': (I, 'Text-only disclosures remain text-only.', 'Grade PENDING.'),
    'RES-EP13-18': (I, 'Depends on TCB-SCOPE-01. Native discovery and custody bytes are unchanged; marker observations stay trusted (ported native probe re-observes).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-19': (N, 'Substantive review with discriminating probes on three byte sets and full-Run closure; all pinned groups pass and an advisory was still found.', 'Grade PENDING.'),
    'IR-EP13-NB-01': (N, 'Depends on TCB-SCOPE-01. Every probe ran in-process with owner modules; containment is not claimed.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'IR-EP13-NB-02': (N, 'No name scan decides scope: attribution compares the first element of matrix pairs and universe values on one scope record, never spellings.', 'Grade PENDING.'),
    'IR-EP13-NB-03': (N, 'Depends on TCB-SCOPE-01. Loaded owner instances stay reachable in-process; the capture record is a trusted host observation, which is why the boundary is trust.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'IR-EP13-NB-04': (N, 'Depends on TCB-SCOPE-01; one TCB account covers all thirteen rows.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'IR-EP13-NB-05': (N, 'Contradictory prose still needed substantive review: the bounded author review found the section 5 "already decides today" sentence false for unsupported rows, and it was corrected with law-conforming controls.', 'Grade PENDING.'),
    'IR-EP13-NB-06': (I, 'Historical attacker cost preserved as history.', 'Grade PENDING.'),
    'IR-EP13-NB-07': (I, 'The original environment is preserved; this review names its interpreter (-I -B) and pins.', 'Grade PENDING.'),
    'AX6': (I, 'Depends on TCB-SCOPE-01. No delta file claims same-process route-region protection.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'AX9': (N, 'Depends on TCB-SCOPE-01. The source42 additions (attribution predicate, capture exactness, programEntry enforcement) are typed data admission under a trusted evaluator.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'MD5': (I, 'Depends on TCB-SCOPE-01. Source42 adds no Python-containment mechanism.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RX2c': (N, 'Depends on TCB-SCOPE-01. Complete replay and full-Run closure on the same manifest remain reproducibility evidence, not containment.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
}
RES_ROWS = []
for rid in ['RES-EP13-%02d' % i for i in range(1, 20)] + ['IR-EP13-NB-%02d' % i for i in range(1, 8)] + ['AX6', 'AX9', 'MD5', 'RX2c']:
    basis, text, cons = RES_TEXT[rid]
    p = V40ROWS[rid]
    dep = 'TCB-SCOPE-01' if rid in TCB_DEPS else None
    if (p.get('sharedDependency') or None) != dep:
        GAPS.append('shared dependency differs from source40 for ' + rid)
    RES_ROWS.append(base_row(rid, basis, 'ASSESSED-CONSISTENT-GRADE-PENDING', text + ' Historical limitation preserved; no historical guard claimed repaired.', RESOWN, cons,
                             proposedDisposition=p['proposedDisposition'], authorGrade='PENDING', sharedDependency=dep, residualRetained=True))

AR_TEXT = {
    'AR-01': (I, 'NO-NEW-ISSUE', 'Admission section 1 byte-identical; ported query carriers pass on source42.', 'No change required.'),
    'AR-02': (I, 'NO-NEW-ISSUE', 'Admission sections 2-4 and gates byte-identical (%d gates, qualified=true %d).' % (len(GATES), gates_true), 'All gates stay unperformed.'),
    'AR-03': (I, 'NO-NEW-ISSUE', 'Security contract byte-identical; ported custody probe passes.', 'No change required.'),
    'AR-04': (I, 'NO-NEW-ISSUE', 'Security trust time byte-identical.', 'No change required.'),
    'AR-05': (I, 'NO-NEW-ISSUE', 'Security root chain and revocation byte-identical.', 'No change required.'),
    'AR-06': (I, 'NO-NEW-ISSUE', 'Platform admission and carrier DDL byte-identical; security group passes.', 'No change required.'),
    'AR-07': (I, 'NO-NEW-ISSUE', 'Native contract byte-identical 40->42; ported native probe passes (39 rows); native group 388/388.', 'No change required.'),
    'AR-08': (I, 'NO-NEW-ISSUE', 'Invocation and repair text byte-identical; ported repair:2 probe passes.', 'No change required.'),
    'AR-09': (N, 'NO-NEW-ISSUE (ADVISORY ADV42-01)', 'identity-and-evidence incorporates the execution-inputs and enumeration contracts, which changed. S40-01 is resolved: the attribution predicate and capture exactness are published and enforced, with independent three-tree discrimination and full-Run closure. ADV42-01 records the remaining admission-scope note; the closing digest law scope is sufficiently explicit.', 'Source-level change requirement from source40 discharged; the advisory is optional.'),
    'AR-10': (I, 'NO-NEW-ISSUE', 'Comparison text and model byte-identical; ported comparison knowledge passes.', 'No change required.'),
    'AR-11': (I, 'NO-NEW-ISSUE', 'Comparison and import byte-identical; execution-inputs child passes with 95 cases.', 'No change required.'),
    'AR-12': (I, 'NO-NEW-ISSUE', 'Native section 4 and atoms byte-identical; atoms child passes.', 'No change required.'),
    'AR-13': (N, 'NO-NEW-ISSUE', 'The enumeration binding construction that native sections 1/2 bind into was clarified and enforced: explicit TS/JS null entries refuse, defaults and marker selections admit, and Rust/syntax/unavailable freedom is preserved (P42-PROGRAM-ENTRY-X). The binder shorthand is OBS42-02.', 'No change required.'),
    'AR-14': (I, 'NO-NEW-ISSUE', 'Stage transition, lease and read-only carrier bytes unchanged; ported carrier probe passes.', 'No change required.'),
    'AR-15': (I, 'NO-NEW-ISSUE', 'Contract index README byte-identical.', 'No change required.'),
    'AR-16': (I, 'NO-NEW-ISSUE', 'D9 and command-outcome text byte-identical; S39-01/S39-02 remain closed by the ported policy probe; D9 successor stays carried.', 'No change required.'),
}
AR_ROWS = []
for i in range(1, 17):
    rid = 'AR-%02d' % i
    basis, disp, text, cons = AR_TEXT[rid]
    p = V40ROWS[rid]
    c = p['contract']
    unchanged = same(S40, S42, c)
    if basis == I and not unchanged:
        GAPS.append('unchanged basis claimed for a changed contract: ' + rid)
    AR_ROWS.append(base_row(rid, basis, disp, text, c + ' (' + p['selector'] + ')', cons, contract=c, selector=p['selector'], statusRecorded=p['statusRecorded'],
                            contractSha256=sha(S42 + '/' + c), contractUnchanged40to42=unchanged))

SMI = U['current-source-map.proposed.md'] and U['repository-file-inventory.v1.json']
FW_TEXT = {
    'FW-01': (N, 'discovery.rs must emit default-unit bindings with a null programEntry (never the U-1 marker), explicit TS/JS programs with the selected config path equal to the retained entryConfigPath, and must not produce explicit js-synthesized available bindings (OBS42-05).', 'Implementation obligation clarified; not executed.'),
    'FW-02': (I, 'review.rs review-brief carriers unchanged; ported query probe passes.', 'Not executed.'),
    'FW-03': (N, 'analysis.rs must capture explicit stage returns on the receipt of the producer that returned them, select exactly the union of complete receipts, and derive row viewDigests by the published section 3 predicate; ADV42-01 suggests checking receipt/view producer equality.', 'Implementation obligation clarified; not executed.'),
    'FW-04': (I, 'imports.rs unchanged; typed-null targetUniverse account stands.', 'Not executed.'),
    'FW-05': (I, 'comparison.rs presence knowledge unchanged; ported probe passes.', 'Not executed.'),
    'FW-06': (I, 'finalization.rs delivery laws unchanged; commit-inventory recipe re-derived by the ported probe.', 'Not executed.'),
    'FW-07': (I, 'invocation.rs argvDigest unchanged.', 'Not executed.'),
    'FW-08': (I, 'outcomes.rs detail allowlist unchanged; ported section 7 probe passes.', 'Not executed.'),
    'FW-09': (I, 'review.rs candidates/inspect carriers unchanged.', 'Not executed.'),
    'FW-10': (I, 'repair.rs repair:2 constructor unchanged; ported probe passes.', 'Not executed.'),
    'FW-11': (I, 'comparison.rs baseline.show unchanged.', 'Not executed.'),
    'FW-12': (I, 'review.rs produce-brief host-only unchanged.', 'Not executed.'),
    'FW-13': (I, 'configuration.rs policy-test admission routes unchanged.', 'Not executed.'),
    'FW-14': (N, 'discovery.rs recommend units: the same binding construction rule applies to recommended default and explicit programs (P42-PROGRAM-ENTRY-X).', 'Implementation obligation clarified; not executed.'),
    'FW-15': (I, 'policy.rs show/test unchanged; ported policy probe passes.', 'Not executed.'),
}
FW_ROWS = []
for i in range(1, 16):
    rid = 'FW-%02d' % i
    basis, text, cons = FW_TEXT[rid]
    p = V40ROWS[rid]
    FW_ROWS.append(base_row(rid, basis, 'OWNER-ROUTING-ASSESSED-NOT-EXECUTED',
                            text + ' Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: %s).' % SMI,
                            ', '.join(p['owners']) + ' (' + p['milestone'] + ')', cons, owners=p['owners'], milestone=p['milestone'], verificationStanding=p['verificationStanding']))

IRU = U['inherited-residuals.proposed.md']
DROWN = 'successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md'
DR_TEXT = {
    'DR-001': (I, 'current-source-map and residual ledgers byte-identical.', 'Condition-1 obligation retained.'),
    'DR-002': (N, 'The identity/evidence chain now publishes ExecutionInputsV1 view attribution and exact stage-produced selection (S40-01 resolved).', 'Condition-1 obligation retained; source40 change requirement discharged at source level.'),
    'DR-003': (I, 'Read-only carrier routes unchanged; 54 recovery cases unexecuted.', 'Condition-1 obligation retained; release demonstration still required.'),
    'DR-004': (N, 'The native binding construction consumed by enumeration is clarified (programEntry discriminator versus retained entry) and enforced for explicit TS/JS nulls; native bytes unchanged.', 'Condition-1 obligation retained.'),
    'DR-005': (I, 'Custody reference groups pass; native carrier qualification still required.', 'Condition-1 obligation retained.'),
    'DR-006': (I, 'Descriptor graph unchanged; full-replay child passes.', 'Condition-1 obligation retained.'),
    'DR-007': (I, 'D9 published successor artifact remains a carried implementation-unit obligation; registry unchanged.', 'Mandatory future implementation-unit obligation; not a new blocker.'),
    'DR-008': (I, 'Applied retention posture unchanged.', 'Condition-1 obligation retained.'),
    'DR-009': (N, 'The host capture stays outside the sealed Run: selection equals the union of complete receipts exactly, and the operational census stays excluded (census-only digest equal to control).', 'Condition-1 obligation retained.'),
    'DR-010': (I, 'Bounded first-party composition unchanged.', 'Condition-1 obligation retained.'),
    'DR-011': (I, 'The blind implementer litmus follows final integration and is not closed here.', 'Condition-1 obligation retained.'),
    'DR-011-R01': (I, 'Fact-plane successor schemas unchanged.', 'Retained.'),
    'DR-011-R02': (I, 'Imperative plugins stay outside D-371.', 'Retained.'),
    'DR-011-R03': (N, 'plan2 EnumerationPlanV1 binding joins now refuse explicit TS/JS null entries; the 46 shared enumeration cases are identical.', 'Retained.'),
    'DR-011-R04': (I, 'carrierFormat mapping unchanged.', 'Retained.'),
    'DR-011-R05': (I, 'Rust protocol major 3 unchanged.', 'Retained.'),
    'DR-011-R06': (N, 'Typed close_run outcomes re-exercised: three-tree full Runs close or refuse with typed keys (EVALUATOR_EXECUTION_INPUTS_JOIN, EVALUATION_VIEW_ROOTS, CLOSURE_FIELD_KIND, REFERENCE_PLAN_JOIN).', 'Retained.'),
    'DR-011-R07': (I, 'Query retained availability routes unchanged; query-projection child passes.', 'Retained.'),
    'DR-011-R08': (I, 'D9 successor remains carried (DR-007).', 'Mandatory future implementation-unit obligation.'),
    'DR-011-R09': (N, 'Semantic identity still excludes attempt identity; the capture correction changes ExecutionInputsV1 only for graphs declaring unowned returned views, and shared cases and maintained RunIds are identical across trees.', 'Retained.'),
    'DR-011-R10': (I, 'OPEN: this nonblind review cannot close the fresh blind implementer litmus.', 'Retained open.'),
    'DR-011-R11': (I, 'Real platform durability unmeasured; 54 cases not executed.', 'Retained.'),
    'DR-011-R12': (N, 'Depends on TCB-SCOPE-01, assessed once on source42.', 'Retained; reopens with TCB-SCOPE-01 only.'),
    'DR-011-R13': (N, 'Prerelease identity changes (same-scope re-encoding, refs-only capture, explicit TS null refusal) change records without relabelling majors, consistent with the composition profile.', 'Retained.'),
    'DR-011-R14': (I, 'CFG-6/TM unchanged.', 'Retained.'),
    'DR-011-R15': (I, 'Trusted request context stays host-only.', 'Retained.'),
    'DR-011-R16': (I, 'No executable report-hook admission; prototype-report-inventory and admission section 5 unchanged.', 'Retained.'),
}
DR_ROWS = []
for rid in ['DR-%03d' % i for i in range(1, 12)] + ['DR-011-R%02d' % i for i in range(1, 17)]:
    basis, text, cons = DR_TEXT[rid]
    DR_ROWS.append(base_row(rid, basis, 'CONDITION-1-OBLIGATION-RETAINED-ASSESSED',
                            text + ' Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: %s) is consistent with source42.' % IRU, DROWN, cons))

REGU = U['08-decision-and-readiness-register.md']
SCOPED_TEXT = {
    'DR-201': (N, 'Semantic-correctness owner row: the attribution and capture corrections and ADV42-01 fall in its area.'),
    'DR-202': (I, 'Delivery/operations owner row: recovery, repair and loader TCB unchanged.'),
    'DR-203': (I, 'Prototype-lessons owner row (PARTIAL-SCOPED): no delta file is the prototype reference.'),
    'DR-204': (N, 'V1/coop invariant owner row: selectors and digests independently validated; ADV40-01 resolved without mutating historical layer bytes; all pin ledgers repin only the eight changed files.'),
    'DR-205': (N, 'Small-core/components owner row: TCB-SCOPE-01 remains coherent on source42.'),
}
SCOPED_ROWS = [base_row(rid, SCOPED_TEXT[rid][0], 'ROUTING-ASSESSED-ONLY-NOT-APPLIED',
                        SCOPED_TEXT[rid][1] + ' Register 08 byte-identical 40->42 (%s).' % REGU,
                        'register 08 condition-3 review owner row ' + rid, 'Input to the integrated review; not applied.')
               for rid in ('DR-201', 'DR-202', 'DR-203', 'DR-204', 'DR-205')]

V40TCB = V40['sharedAssumptionTCBSCOPE01']
TCB = {
    'id': 'TCB-SCOPE-01', 'assessedOnceAsOneAssumption': True,
    'assumption': 'Selected authenticated in-process host/evaluator code is trusted; providers and inert inputs are untrusted; adversarial code sharing the process is outside this product threat model.',
    'consequence': 'Rejecting or changing the assumption reopens all thirteen dependent rows jointly. It is a scope selection, not a containment proof; it repairs no historical attack and is not thirteen independent proofs. All thirteen author grades stay PENDING.',
    'dependentRows': TCB_DEPS, 'dependentRowCount': len(TCB_DEPS),
    'substantiveCurrentAssessment': [
        'Coherent as a scope selection on source42: admission section 5 (byte-identical 40->42: %s) and prototype-report-inventory (byte-identical: %s) still admit no untrusted native/WASM, imperative contributions or executable report hooks.' % (U['admission-and-qualification.md'], U['prototype-report-inventory.md']),
        'The source42 changes add typed data admission, not trust: foreign named scopes, internally inconsistent receipts and explicit TS/JS null entries refuse at owner admission and in the Run.',
        'Capture remains a host TCB observation of stage returns (execution-inputs section 1 :24). SELECTED_COVER detects internal inconsistency, not malicious omission; ADV42-01 records a residual detectable inconsistency that admission does not check, which is not a trust-boundary violation.',
        'Providers stay untrusted: view producer closures must be Plan-selected providers at Run closure (CLOSURE_FIELD_KIND / UNSELECTED_PRODUCER measured).',
        'Unqualified: it rests on the authenticated closure/TCB inventory and provider process boundaries, and all %d gates are unperformed (qualified=true %d).' % (len(GATES), gates_true),
    ],
    'reviewerPosition': 'NOT REJECTED', 'standing': 'ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE42; final application adjudication not granted',
    'adjudicationOwner': 'separate final application review, by a NEW different actual Claude origin (not this origin %s and not any author, design or blind origin)' % ORIGIN,
    'prior40Standing': V40TCB['standing'],
}
for rid in TCB_DEPS:
    if next(r for r in RES_ROWS if r['id'] == rid)['sharedDependency'] != 'TCB-SCOPE-01':
        GAPS.append('TCB dependent row lacks shared dependency: ' + rid)

RETAINED = {
    'residuals': len(RES_ROWS), 'authorGradesPending': sum(1 for r in RES_ROWS if r['authorGrade'] == 'PENDING'),
    'condition2Obligations': 28 if cond2_ok else None,
    'condition2Source': 'docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 40->42: %s)' % REGU,
    'qualificationGatesUnperformed': len(GATES), 'qualificationGatesQualifiedTrue': gates_true,
    'plannedRecoveryCasesUnperformed': PC['recoveryCasesNotExecuted'], 'condition5': 'NOT MET (not a design defect)',
    'd9PublishedSuccessor': 'Mandatory future implementation-unit obligation (DR-007 / DR-011-R08); not a newly invented design blocker.',
    'gradeAndConditionOwner': 'All 30 evaluation grades and 28 condition-2 obligations belong to final application adjudication.',
    'finalApplication': 'Requires a NEW different actual Claude origin, not this origin (%s) and not any author, design or blind origin.' % ORIGIN,
}
AUTHORITY = {'gradeGranted': False, 'activationGranted': False, 'implementationAuthorized': False, 'blindReconstructionClaimed': False,
             'freshOriginIndependenceClaimed': False, 'source40ReviewConclusionInherited': False, 'frozenInputsModified': False,
             'applicationOrReadinessGranted': False, 'productQualificationGranted': False, 'consumerArtifactsAccessedOrRepaired': False,
             'historicalExportsRelabelled': False, 'productCommitPushOrActivation': False, 'subagentsWebOrPrivateLogsUsed': False}
LIMITATIONS = [
    'Nonblind successor review by the same origin that completed the source40 review; not fresh-origin independence. Author proposals, root integration records, package evidence and codex/root reference receipts were read as evidence. No blind consumer artifact, result or implementation was read, and no blind link was followed.',
    'Reference Python models over synthetic inputs; no product code. No compiler, provider, host, OS durability, process isolation or cryptography is qualified. 32 gates and 54 recovery cases remain unperformed (condition 5 NOT MET).',
    'Whole-file claims are limited to fresh42Read and inheritedUnchanged40Read. Changed files not fresh-read were read as complete diffs (40->42 or 41->42). The v10 layer is byte-identical to the fully read v11. Range reads and search-only sightings are listed separately and are not whole-file reads.',
    'Closed-run discrimination used the maintained file fixture and the TypeScript semantic fixture; no multi-provider, multi-stage Plan was minted, so the ADV42-01 multi-provider shape is argued from source, not exercised. The relation-column pin and candidate-only attribution rest on reading plus unchanged shared checker cases, not an independent probe.',
    'programEntry discrimination is at the enumeration owner admission, which complete Run closure consumes; explicit-null full Runs were not re-closed independently.',
    'Failed attempt preserved and not counted: program-entry-x attempt 1 exited 1 because receipts/probes/ did not exist yet (harness defect); its children could not write side files. Kept at receipts/runs/program-entry-x.run.json with stdout/stderr; attempt 2 is the result.',
    'Ported source40 probes keep their original labels ("source40") as historical text; only runtime paths changed, and the current side is the verified source42 copy.',
    'The package verifier and native probe are author tools re-executed on this review\'s copy; content equality with root evidence is not independent reconstruction. Four TS normalization-map negatives are executed; the Rust map negative is unexercised; the partial and/or/not helper is unexercised; count/all are unimplemented; two-binding qualification is incomplete.',
    'Composition section 7, policy-derivation3 and other byte-identical owners rely on this origin\'s named source40 reads and assessments; they were not re-read this charter.',
    'No grade, activation, application, readiness, implementation authorization or product qualification is granted.',
]
