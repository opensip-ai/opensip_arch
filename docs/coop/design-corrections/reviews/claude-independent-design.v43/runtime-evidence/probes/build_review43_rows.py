# Executed by build_review43.py in its own globals (exec). The 107 individually reasoned rows with current owners and
# consequences, the single TCB-SCOPE-01 object, retained obligations, authority and limitations. Flags are always false.

N, I = 'new-43', 'unchanged-42-basis'
BASIS_RULE = ('unchanged-42-basis: the governing owner bytes are byte-identical 42->43, and the conclusion rests on that identity plus this origin\'s named source42 row assessment, quoted in unchanged42Basis. '
              'Re-executed suites and ported probes are corroboration only. new-43: the conclusion rests on a source43 read, diff, probe or measurement newly performed under this charter, including rows whose bytes are unchanged but whose read-only response, availability or parity owner is affected by the query change. '
              'Every row carries its own current text, current owner and consequence. No row is carried forward in bulk, and no grade is assigned.')
V42ROWS = {r['id']: r for k in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions') for r in V42[k]}
TCB_DEPS = ['RES-EP13-02', 'RES-EP13-04', 'RES-EP13-12', 'RES-EP13-13', 'RES-EP13-16', 'RES-EP13-18', 'IR-EP13-NB-01', 'IR-EP13-NB-03', 'IR-EP13-NB-04', 'AX6', 'AX9', 'MD5', 'RX2c']


def base_row(rid, basis, disposition, assessment, owner, consequence, **extra):
    prior = V42ROWS.get(rid)
    if prior is None:
        GAPS.append('no source42 row for ' + rid)
    r = {'id': rid, 'prior42Disposition': prior['disposition'] if prior else None, 'prior42AssessmentBasis': prior['assessmentBasis'] if prior else None,
         'disposition': disposition, 'assessmentBasis': basis, 'unchanged42Basis': (prior['currentAssessment'] if (prior and basis == I) else None),
         'currentAssessment': assessment, 'currentOwner': owner, 'consequence': consequence}
    r.update(extra)
    r.update(appliedByThisReview=False, finalApplicationOutcomeGranted=False)
    return r


RESOWN = 'evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review'
F_ROWS = []
for i in range(1, 15):
    rid = 'F-%02d' % i
    st = V42ROWS[rid]['priorRootStanding']
    F_ROWS.append(base_row(rid, I, 'CARRIED-NOT-REGRADED',
                           '%s: prior root standing %s (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the nine source42->43 delta files is an F record.' % (rid, st),
                           'root custody of the F record (outside the frozen snapshot)', 'No source43 change; remains carried without regrade and is not source43 acceptance.', priorRootStanding=st))

RES_TEXT = {
    'RES-EP13-01': (I, 'Plan and derivation joins stay inside complete replay on byte-identical owners (evaluator_replay_model %s, identity-model %s); the full-replay child equals root and this origin\'s source42 receipt, and the lawful query Run closes to the same RunId on both trees.' % (U['evaluator_replay_model.v3.py'], U['identity-model.v3.py']), 'Grade PENDING; residual retained.'),
    'RES-EP13-02': (N, 'Depends on TCB-SCOPE-01. Capture and current availability are both trusted host observations. The ported capture-join measurement on source43 still admits a non-provider-producer view and refuses it only at closure (ADV42-01), and an availability observation or record only refuses or selects the disclosed state, never admission (CH43-OBSERVATION-GRANTS-NOTHING). No answer-provenance claim against the host is made.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-03': (I, 'Admission contract (%s) and residual ledger (%s) byte-identical 42->43; the finite historical measurement is unchanged.' % (U['admission-and-qualification.md'], U['evaluation-residual-dispositions.proposed.json']), 'Grade PENDING; finite historical measurement unchanged.'),
    'RES-EP13-04': (N, 'Depends on TCB-SCOPE-01. Closed input admission is unchanged, and the query adds no open input. The availability observation is a closed vocabulary: null or unknown values are a reference precondition and, in a product adapter, a host-invariant fault; retained availability records failing identity admission are evidence.corrupt (P43-QUERY-X, P43-QUERY-ADAPTER-X).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-05': (N, 'The frozen subject was verified outside every author instrument: formal43 manifest db43ee76..., archive d1ff8312..., all 12,913 members by hash and length, parent42 f602fc7e... (12,913 members), the declared chain, the exact 9/0/0 delta and every entry of the five pin ledgers.', 'Grade PENDING.'),
    'RES-EP13-06': (N, 'canonical.py stays outside the delta (%s). The ported run-termination probe recomputes the commit-inventory digest over a closed source43 Run with the reviewer\'s own C()/H(), with every row identical to source42.' % U['canonical.py'], 'Grade PENDING.'),
    'RES-EP13-07': (I, 'Seal and replay owners byte-identical 42->43; the analysis-seal child equals root and this origin\'s source42 receipt.', 'Grade PENDING.'),
    'RES-EP13-08': (I, 'A bounded historical measurement. Source43 adds a response-disclosure correction and a representation pin and claims no proof over all PlanIntents.', 'Grade PENDING.'),
    'RES-EP13-09': (N, 'Provenance stays distinct from correctness on source43: package v20 semantic-controls1 keeps owner ADMIT with semantic REFUSE, content-equal to the root final43 verification, and a partial availability disclosure never turns a failing closure into an answer.', 'Grade PENDING.'),
    'RES-EP13-10': (N, 'Author self-counters did not decide this review. The five added checker controls (204 -> 209) are reference self-consistency; the decisive evidence is the reviewer\'s own old-versus-new discrimination with each tree\'s own modules (P43-QUERY-X, P43-QUERY-ADAPTER-X).', 'Grade PENDING.'),
    'RES-EP13-11': (N, 'Failures stay recorded by cause. This review preserves its first query-probe launch (the parent failed after a child could not write into a not-yet-created receipts/probes directory), the pin checker attempt 1 (a ledger key assumption) and the adapter probe attempt 1 (four rows built with an inadmissible missingRefs record). The root planning verification keeps its exit-2 prior attempt.', 'Grade PENDING.'),
    'RES-EP13-12': (N, 'Depends on TCB-SCOPE-01. No sole Python guard enters product authority: close_run remains the positive admission for every graph read, and SELECTED_COVER still detects internal capture inconsistency, never malicious omission.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-13': (N, 'Depends on TCB-SCOPE-01. The discrimination probes ran each tree (base42, source43) in its own process on verified copies, which were re-verified unchanged afterwards (copy-verification-final.json).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-14': (I, 'The differential census is not used as an oracle; the source43 delta touches no census owner.', 'Grade PENDING.'),
    'RES-EP13-15': (I, 'The C-2 v4 self-census is not elevated. Enumeration owners are byte-identical 42->43, and their 54 checker cases equal the source42 receipt after removing path fields only.', 'Grade PENDING.'),
    'RES-EP13-16': (I, 'Depends on TCB-SCOPE-01. Producer flags cannot bypass replay: row-attribution re-derivation and exact VIEW_TOTALITY sit in byte-identical execution-inputs owners (%s), and the 95 cases are unchanged.' % U['execution_inputs_model.v1.py'], 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-17': (N, 'Text-only disclosures remain text-only. Source43\'s two contract sentences are not text-only: each is paired with model behaviour and checker controls and was independently discriminated. Limitation notes stay bounded free text carried by parity (P43-QUERY-PROSE).', 'Grade PENDING.'),
    'RES-EP13-18': (I, 'Depends on TCB-SCOPE-01. Native discovery and custody bytes are unchanged and marker observations stay trusted; ported native (%d rows) and custody (%d rows) observations are identical to source42.' % (PORTED_EQUAL['P43-PORTED-NATIVE']['rows'], PORTED_EQUAL['P43-PORTED-CUSTODY']['rows']), 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RES-EP13-19': (N, 'Substantive review on source43: old-versus-new discrimination on a lawful closed Run, the adapter path and the prose law. The retained advisory\'s standing was assessed rather than carried, and all pinned groups pass.', 'Grade PENDING.'),
    'IR-EP13-NB-01': (N, 'Depends on TCB-SCOPE-01. Every source43 probe ran in-process with owner modules (the query and adapter probes in one process per tree); containment is not claimed.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'IR-EP13-NB-02': (N, 'No name scan decides a query route: close_retained_run routes by the typed identity outcome, the availability observation by a closed vocabulary, and section 7 forbids selection by filename, exception prefix or caller-supplied fault origin. The checker control close-retained-run-routes-without-message-parsing passes.', 'Grade PENDING.'),
    'IR-EP13-NB-03': (N, 'Depends on TCB-SCOPE-01. Loaded owner instances stay reachable in-process. Host availability, latest and snapshot observations are trusted host context, which is why each can only refuse or select, never admit.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'IR-EP13-NB-04': (N, 'Depends on TCB-SCOPE-01; one TCB account, assessed once on source43, covers all thirteen rows.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'IR-EP13-NB-05': (N, 'Contradictory prose still needed substantive review. Source42 identity law said a query reports current availability, while the graph model reported retained for an admitted partial observation; source43 aligns contract section 7 and the model, and the alignment was discriminated on both trees.', 'Grade PENDING.'),
    'IR-EP13-NB-06': (I, 'Historical attacker cost preserved as history; no source43 file addresses it.', 'Grade PENDING.'),
    'IR-EP13-NB-07': (I, 'The original environment is preserved; this review names its interpreter (/tmp/opensip-architecture-review-env/bin/python -I -B) and verifies every pin.', 'Grade PENDING.'),
    'AX6': (N, 'Depends on TCB-SCOPE-01. None of the nine source43 delta files claims same-process route-region protection (all nine diffs read).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'AX9': (N, 'Depends on TCB-SCOPE-01. The source43 additions (disclosed availability state, hop representation) are typed response data under a trusted evaluator, not a protection mechanism.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'MD5': (N, 'Depends on TCB-SCOPE-01. Source43 adds no Python-containment mechanism (delta read).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
    'RX2c': (I, 'Depends on TCB-SCOPE-01. Complete replay and full-Run closure on the same manifest remain reproducibility evidence, not containment, and the replay owners are byte-identical 42->43.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.'),
}
RES_ROWS = []
for rid in ['RES-EP13-%02d' % i for i in range(1, 20)] + ['IR-EP13-NB-%02d' % i for i in range(1, 8)] + ['AX6', 'AX9', 'MD5', 'RX2c']:
    basis, text, cons = RES_TEXT[rid]
    p = V42ROWS[rid]
    dep = 'TCB-SCOPE-01' if rid in TCB_DEPS else None
    if (p.get('sharedDependency') or None) != dep:
        GAPS.append('shared dependency differs from source42 for ' + rid)
    RES_ROWS.append(base_row(rid, basis, 'ASSESSED-CONSISTENT-GRADE-PENDING', text + ' Historical limitation preserved; no historical guard claimed repaired.', RESOWN, cons,
                             proposedDisposition=p['proposedDisposition'], authorGrade='PENDING', sharedDependency=dep, residualRetained=True))

AR_TEXT = {
    'AR-01': (I, 'NO-NEW-ISSUE', 'Admission section 1 byte-identical 42->43; ported query carriers (%d rows) identical.' % PORTED_EQUAL['P43-PORTED-QUERY']['rows'], 'No change required.'),
    'AR-02': (I, 'NO-NEW-ISSUE', 'Admission sections 2-4 and the qualification gate ledger byte-identical 42->43: %d gates, none qualified (qualified=true %d); no delta file is a gate owner.' % (len(GATES), gates_true), 'All gates stay unperformed.'),
    'AR-03': (I, 'NO-NEW-ISSUE', 'Security discovery text byte-identical; ported custody rows identical.', 'No change required.'),
    'AR-04': (I, 'NO-NEW-ISSUE', 'Security trust time byte-identical; security group stdout equals root.', 'No change required.'),
    'AR-05': (I, 'NO-NEW-ISSUE', 'Security root chain and revocation byte-identical; no delta file touches them.', 'No change required.'),
    'AR-06': (I, 'NO-NEW-ISSUE', 'Platform admission and carrier DDL byte-identical; ported read-only carrier rows (%d) identical.' % PORTED_EQUAL['P43-PORTED-CARRIER']['rows'], 'No change required.'),
    'AR-07': (I, 'NO-NEW-ISSUE', 'Native sections 3/5/9 byte-identical; native group stdout equals root and source42.', 'No change required.'),
    'AR-08': (I, 'NO-NEW-ISSUE', 'Invocation and repair text byte-identical; ported repair:2 rows identical.', 'No change required.'),
    'AR-09': (N, 'NO-NEW-ISSUE (ADVISORY ADV42-01 RETAINED)', 'identity-and-evidence is byte-identical, and graph responses now honour its current-availability law (:1718-1725, "A query reports both"): source43 section 7 reports an observed partial state instead of retained (CH43-AVAILABILITY-REPORTING). Section 5 (:1753-1767) still routes refusing states through query section 7. S40-01 remains resolved; ADV42-01 is retained.', 'No change required; the advisory is optional.'),
    'AR-10': (I, 'NO-NEW-ISSUE', 'Baseline and comparison text byte-identical; ported comparison knowledge rows identical.', 'No change required.'),
    'AR-11': (I, 'NO-NEW-ISSUE', 'Comparison and import text byte-identical; the execution-inputs child equals root after removing path fields only.', 'No change required.'),
    'AR-12': (I, 'NO-NEW-ISSUE', 'Native section 4 and atoms byte-identical; atoms child equals root and source42.', 'No change required.'),
    'AR-13': (I, 'NO-NEW-ISSUE', 'Native sections 1/2/6/8 and discovery byte-identical; enumeration cases equal source42 after removing path fields only.', 'No change required.'),
    'AR-14': (I, 'NO-NEW-ISSUE', 'Stage transition and lease bytes unchanged; no delta file is a lifecycle owner.', 'No change required.'),
    'AR-15': (I, 'NO-NEW-ISSUE', 'Contract index README byte-identical; the query contract stays incorporated through workflows-and-surfaces section 8.', 'No change required.'),
    'AR-16': (N, 'NO-NEW-ISSUE', 'workflows-and-surfaces is byte-identical, but the query change reaches its query command outcomes and parity: the availability parity field (:1190, :1228-1229) now carries partial exactly, every graph refusal route and exit is unchanged, and no D9 code is added. The D9 successor stays carried.', 'No change required.'),
}
AR_ROWS = []
for i in range(1, 17):
    rid = 'AR-%02d' % i
    basis, disp, text, cons = AR_TEXT[rid]
    p = V42ROWS[rid]
    c = p['contract']
    unchanged = same(S42, S43, c)
    if basis == I and not unchanged:
        GAPS.append('unchanged basis claimed for a changed contract: ' + rid)
    AR_ROWS.append(base_row(rid, basis, disp, text, c + ' (' + p['selector'] + ')', cons, contract=c, selector=p['selector'], statusRecorded=p['statusRecorded'],
                            contractSha256=sha(S43 + '/' + c), contractUnchanged42to43=unchanged))

SMI = U['current-source-map.proposed.md'] and U['repository-file-inventory.v1.json']
FW_TEXT = {
    'FW-01': (I, 'discovery.rs binding construction obligation unchanged; enumeration owners byte-identical.', 'Not executed.'),
    'FW-02': (I, 'review.rs review-brief carriers unchanged; ported carriers identical.', 'Not executed.'),
    'FW-03': (N, 'analysis.rs composes provider work, admission, evaluation and complete replay (layout 14 :475, search output). Beyond the source42 capture obligation it now carries the ADV42-01 implementation verification obligation: never list a returned view on another producer\'s complete receipt. The root note routes it there, and this review assesses the routing as correctly scoped but not executed.', 'Implementation verification obligation retained; not executed.'),
    'FW-04': (I, 'imports.rs unchanged; typed-null targetUniverse account stands.', 'Not executed.'),
    'FW-05': (I, 'comparison.rs presence knowledge unchanged; ported comparison rows identical.', 'Not executed.'),
    'FW-06': (I, 'finalization.rs delivery laws unchanged; commit-inventory recipe re-derived identically on source43.', 'Not executed.'),
    'FW-07': (I, 'invocation.rs argvDigest unchanged.', 'Not executed.'),
    'FW-08': (N, 'outcomes.rs detail allowlist is unchanged and sufficient for source43: the adapter\'s invalid availability observation uses the existing HOST.INVARIANT_VIOLATED detail, and every availability refusal uses an existing evidence.* detail (P43-QUERY-ADAPTER-X). No detail is added.', 'Not executed.'),
    'FW-09': (I, 'review.rs candidates/inspect carriers unchanged; their non-graph context keeps availability=retained (workflows :687-689).', 'Not executed.'),
    'FW-10': (I, 'repair.rs repair:2 constructor unchanged; ported repair rows identical.', 'Not executed.'),
    'FW-11': (I, 'comparison.rs baseline.show unchanged; pivot-closure availability is a separate non-graph surface.', 'Not executed.'),
    'FW-12': (I, 'review.rs produce-brief host-only unchanged.', 'Not executed.'),
    'FW-13': (I, 'configuration.rs policy-test admission routes unchanged; ported policy rows identical.', 'Not executed.'),
    'FW-14': (I, 'discovery.rs recommend units unchanged; the same binding construction rule applies.', 'Not executed.'),
    'FW-15': (I, 'policy.rs show/test unchanged; the policy-derivation child equals source42.', 'Not executed.'),
}
FW_ROWS = []
for i in range(1, 16):
    rid = 'FW-%02d' % i
    basis, text, cons = FW_TEXT[rid]
    p = V42ROWS[rid]
    FW_ROWS.append(base_row(rid, basis, 'OWNER-ROUTING-ASSESSED-NOT-EXECUTED',
                            text + ' Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 42->43: %s).' % SMI,
                            ', '.join(p['owners']) + ' (' + p['milestone'] + ')', cons, owners=p['owners'], milestone=p['milestone']))

IRU = U['inherited-residuals.proposed.md']
DROWN = 'successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md'
DR_TEXT = {
    'DR-001': (I, 'current-source-map and residual ledgers byte-identical 42->43.', 'Condition-1 obligation retained.'),
    'DR-002': (I, 'ExecutionInputsV1 view attribution and exact selection remain published on byte-identical owners; S40-01 remains resolved.', 'Condition-1 obligation retained.'),
    'DR-003': (I, 'Read-only carrier routes unchanged; the graph query remains a read that mints no Run; 54 recovery cases unexecuted.', 'Condition-1 obligation retained; release demonstration still required.'),
    'DR-004': (I, 'Native binding construction consumed by enumeration unchanged; the explicit TS/JS null refusal stands.', 'Condition-1 obligation retained.'),
    'DR-005': (I, 'Custody reference groups pass unchanged; native carrier qualification still required.', 'Condition-1 obligation retained.'),
    'DR-006': (I, 'Descriptor graph unchanged; the full-replay child equals root and source42.', 'Condition-1 obligation retained.'),
    'DR-007': (I, 'The D9 published successor artifact remains a carried implementation-unit obligation; source43 adds no D9 code.', 'Mandatory future implementation-unit obligation; not a new blocker.'),
    'DR-008': (N, 'The applied retention posture is unchanged. Its current-availability consequence is now disclosed by graph responses exactly (partial is never upgraded), and refusing states still refuse.', 'Condition-1 obligation retained.'),
    'DR-009': (I, 'The host capture stays outside the sealed Run on byte-identical owners; census exclusion unchanged.', 'Condition-1 obligation retained.'),
    'DR-010': (I, 'Bounded first-party composition unchanged.', 'Condition-1 obligation retained.'),
    'DR-011': (I, 'The blind implementer litmus follows final integration and is not closed by this review.', 'Condition-1 obligation retained.'),
    'DR-011-R01': (I, 'Fact-plane successor schemas unchanged.', 'Retained.'),
    'DR-011-R02': (I, 'Imperative plugins stay outside D-371.', 'Retained.'),
    'DR-011-R03': (I, 'plan2 EnumerationPlanV1 binding joins unchanged; explicit TS/JS null entries still refuse.', 'Retained.'),
    'DR-011-R04': (I, 'carrierFormat mapping unchanged.', 'Retained.'),
    'DR-011-R05': (I, 'Rust protocol major 3 unchanged.', 'Retained.'),
    'DR-011-R06': (N, 'Typed close_run outcomes were re-exercised through the graph query on source43: EvidenceUnavailable -> evidence.missing and AdmissionError -> evidence.corrupt under every observation, identical to source42.', 'Retained.'),
    'DR-011-R07': (N, 'Query retained-availability routes are unchanged on source43 (purged, expired, corrupt, unavailable and missing refuse with exit 4), while a successful read now reports the observed partial state; measured on both trees.', 'Retained.'),
    'DR-011-R08': (I, 'D9 successor remains carried (DR-007).', 'Mandatory future implementation-unit obligation.'),
    'DR-011-R09': (N, 'Semantic identity still excludes attempt identity and current availability: the same lawful Run closes to the same RunId on both trees, availability sits outside the cursor binding, and package export stores are byte-equal to package19.', 'Retained.'),
    'DR-011-R10': (I, 'OPEN: this nonblind review cannot close the fresh blind implementer litmus.', 'Retained open.'),
    'DR-011-R11': (I, 'Real platform durability unmeasured; 54 cases not executed.', 'Retained.'),
    'DR-011-R12': (N, 'Depends on TCB-SCOPE-01, assessed once on source43.', 'Retained; reopens with TCB-SCOPE-01 only.'),
    'DR-011-R13': (N, 'Source43 changes a response value (availability disclosure) and pins a representation without a schema major or identity record change; graph-query:3 bytes are unchanged, consistent with the composition profile.', 'Retained.'),
    'DR-011-R14': (I, 'CFG-6/TM unchanged.', 'Retained.'),
    'DR-011-R15': (N, 'Trusted request context stays host-only: requestId, availability, latestRunId and runsForSnapshot are host observations that the reference takes as call arguments and a product adapter supplies; none is request-authored.', 'Retained.'),
    'DR-011-R16': (I, 'No executable report-hook admission; prototype-report-inventory and admission section 5 unchanged.', 'Retained.'),
}
DR_ROWS = []
for rid in ['DR-%03d' % i for i in range(1, 12)] + ['DR-011-R%02d' % i for i in range(1, 17)]:
    basis, text, cons = DR_TEXT[rid]
    DR_ROWS.append(base_row(rid, basis, 'CONDITION-1-OBLIGATION-RETAINED-ASSESSED',
                            text + ' Successor routing in inherited-residuals.proposed.md (byte-identical 42->43: %s) is consistent with source43.' % IRU, DROWN, cons))

REGU = U['08-decision-and-readiness-register.md']
SCOPED_TEXT = {
    'DR-201': (N, 'Semantic-correctness owner row: the source43 availability disclosure correction, the path hop representation and the retained ADV42-01 fall in its area.'),
    'DR-202': (I, 'Delivery/operations owner row: recovery, repair and loader TCB unchanged.'),
    'DR-203': (I, 'Prototype-lessons owner row (PARTIAL-SCOPED): no delta file is the prototype reference.'),
    'DR-204': (N, 'V1/coop invariant owner row: every pin of the five ledgers verified against the formal manifest; the ledgers repin only the three query owner files and the sibling ledgers; layer v11 retained with unchanged inputs.'),
    'DR-205': (N, 'Small-core/components owner row: TCB-SCOPE-01 remains coherent on source43.'),
}
SCOPED_ROWS = [base_row(rid, SCOPED_TEXT[rid][0], 'ROUTING-ASSESSED-ONLY-NOT-APPLIED', SCOPED_TEXT[rid][1] + ' Register 08 byte-identical 42->43 (%s).' % REGU,
                        'register 08 condition-3 review owner row ' + rid, 'Input to the integrated review; routing only, not applied.')
               for rid in ('DR-201', 'DR-202', 'DR-203', 'DR-204', 'DR-205')]

V42TCB = V42['sharedAssumptionTCBSCOPE01']
TCB = {
    'id': 'TCB-SCOPE-01', 'assessedOnceAsOneAssumption': True,
    'assumption': 'Authenticated selected in-process host/evaluator code is trusted; providers and inert inputs are untrusted; adversarial code sharing the process is outside the product threat model.',
    'consequence': 'Rejecting or changing the assumption reopens the thirteen dependent rows jointly, not as thirteen independent proofs. It repairs no historical attack and qualifies no containment. All thirteen author grades stay PENDING.',
    'dependentRows': TCB_DEPS, 'dependentRowCount': len(TCB_DEPS),
    'currentAssessment': 'NOT REJECTED: coherent as a scope selection on source43 and unqualified; the source43 changes add response disclosure, not trust.',
    'substantiveCurrentAssessment': [
        'Coherent as a scope selection on source43: admission section 5 (byte-identical 42->43: %s) and prototype-report-inventory (byte-identical: %s) still admit no untrusted native/WASM, imperative contributions or executable report hooks.' % (U['admission-and-qualification.md'], U['prototype-report-inventory.md']),
        'The source43 changes add typed response disclosure and a representation pin, not trust. Availability observations and retained records can only refuse or select the disclosed state, and close_run remains the positive admission on every graph read.',
        'Host observations stay TCB inputs. A product adapter\'s out-of-vocabulary observation is a host-invariant fault, not evidence. Capture remains a host observation: ADV42-01 is retained as an implementation verification obligation, not a trust-boundary violation.',
        'Providers stay untrusted: view producer closures must be Plan-selected providers at Run closure (CLOSURE_FIELD_KIND re-measured on source43).',
        'Unqualified: it rests on the authenticated closure/TCB inventory and provider process boundaries, and all %d gates are unperformed (qualified=true %d).' % (len(GATES), gates_true),
    ],
    'reviewerPosition': 'NOT REJECTED', 'standing': 'ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE43; final application adjudication not granted',
    'adjudicationOwner': 'separate final application review, by a NEW different actual Claude origin (not this origin %s and not any author, design or blind origin)' % ORIGIN,
    'prior42Standing': V42TCB['standing'],
}
for rid in TCB_DEPS:
    if next(r for r in RES_ROWS if r['id'] == rid)['sharedDependency'] != 'TCB-SCOPE-01':
        GAPS.append('TCB dependent row lacks shared dependency: ' + rid)

RETAINED = {
    'residuals': len(RES_ROWS), 'authorGradesPending': sum(1 for r in RES_ROWS if r['authorGrade'] == 'PENDING'),
    'condition2Obligations': 28 if cond2_ok else None,
    'condition2Source': 'docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 42->43: %s)' % REGU,
    'productQualificationGates': {'count': len(GATES), 'qualifiedTrue': gates_true, 'standing': 'UNPERFORMED'},
    'plannedRecoveryCases': {'count': PC['recoveryCases'], 'notExecuted': PC['recoveryCasesNotExecuted'], 'standing': 'UNPERFORMED'},
    'condition5': 'NOT MET (not a design defect)',
    'd9PublishedSuccessor': 'Mandatory future implementation-unit obligation (DR-007 / DR-011-R08); not a newly invented design blocker.',
    'adv4201ImplementationVerification': 'crates/host/src/analysis.rs verification that no returned view is listed on another producer\'s complete receipt (root note routing; not executed).',
    'gradeAndConditionOwner': 'All 30 evaluation grades and 28 condition-2 obligations belong to final application adjudication.',
    'finalApplication': 'Requires a NEW different actual Claude origin, not this origin (%s) and not any author, design or blind origin.' % ORIGIN,
    'acceptanceStanding': 'Source-level acceptance only; distinct from final application, readiness and product qualification.',
}
AUTHORITY = {'gradeGranted': False, 'activationGranted': False, 'implementationAuthorized': False, 'blindReconstructionClaimed': False,
             'freshOriginIndependenceClaimed': False, 'source42ReviewConclusionInherited': False, 'frozenInputsModified': False,
             'applicationOrReadinessGranted': False, 'productQualificationGranted': False, 'blindConsumerArtifactsOrOutcomesAccessed': False,
             'queryAuthorRuntimeOrReportsRead': False, 'historicalExportsRelabelled': False, 'runIdsReminted': False, 'productCommitPushOrActivation': False,
             'subagentsWebOrPrivateLogsUsed': False}
LIMITATIONS = [
    'Nonblind successor review by the same origin that completed the source40 and source42 reviews; not fresh-origin independence. The source-only note, root reference/planning/package records and codex receipts were read as evidence. The query-author runtime and reports were not read, and no blind consumer artifact, export, helper, review or root blind outcome was read.',
    'Two broad content searches over docs/ surfaced file names and single matching lines from snapshot-internal historical review directories (including consumer-b.* and bv*-corrections-author copies) before the searches were restricted with !**/reviews/**. None of those files was opened or read, and nothing from them is used (readScope.searchOnlySightings).',
    'Reference Python models over synthetic inputs; no product code. No compiler, provider, host adapter, evidence store, OS durability, process isolation or cryptography is qualified. 32 gates and 54 recovery cases remain unperformed (condition 5 NOT MET).',
    'Whole-file claims are limited to fresh43Read and inheritedUnchanged42Read. The query contract was freshly read completely. The model and checker were read in named ranges plus their complete 42->43 diffs, and the other changed files as complete diffs. Range reads and search-only sightings are listed separately and are not whole-file reads.',
    'Closed-run discrimination used one lawful TypeScript semantic fixture Run plus algorithm goldens over projected edges; the adapter path exercised the reference adapter laws, not a product adapter. No multi-provider, multi-stage Plan was minted, so the ADV42-01 multi-provider shape stays argued from source.',
    'The source42 three-tree view-attribution and program-entry probes and the case-population comparisons were not re-run. Their conclusions stand on byte-identical owners and are named as unchanged-42 basis, corroborated by the equal enumeration and execution-inputs child receipts.',
    'Failed attempts preserved and not counted: the first query-probe launch (a child could not write before receipts/probes existed; the parent then failed with KeyError; no receipt), source-pins43 attempt 1 (KeyError on a ledger key assumption; receipt kept), and query-adapter43-x attempt 1 (four rows used a missingRefs entry, a bare fact id, that fails identity availability admission, so those rows stopped at the record stage; its run receipt and stdout are kept, and its probe JSON was superseded by attempt 2, which is the result).',
    'Ported source42 probes keep their original labels ("source40"/"source42") as historical text; only runtime paths changed, and the current side is the verified source43 copy.',
    'The package verifier and native probe are author tools re-executed on this review\'s copy; content equality with root evidence is not independent reconstruction. Four TS normalization-map negatives are executed; the Rust map negative is unexercised; the partial and/or/not helper is unexercised; count/all are unimplemented; two-binding qualification is incomplete.',
    'Cursor assessment covers same-host continuation only; the cursor is an opaque host token, and no cross-host portability or canonical preimage is assessed or required.',
    'Byte-identical owners outside the query change (composition section 7, policy-derivation3, attribution/capture, programEntry, identity digest scope) rely on this origin\'s named source42 assessments and were not re-read this charter.',
    'No grade, activation, application, readiness, implementation authorization or product qualification is granted.',
]
