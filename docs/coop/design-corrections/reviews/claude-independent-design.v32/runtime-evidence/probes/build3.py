"""review.json part 3 — 14 F rows, 30 evaluation residual dispositions, TCB, issues, verdict."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v32'
REC = os.path.join(BASE, 'receipts')


def rec(n):
    return json.load(open(os.path.join(REC, n)))


p09, p10, p14 = rec('p09-package8.json'), rec('p10-verify-a8.json'), rec('p14-residuals32.json')
p06, p13 = rec('p06-changedchecks.json'), rec('p13-pins-planning.json')
p05 = rec('p05-repairlaw.json')
V31 = json.load(open('/tmp/opensip-design-corrections/claude-independent-design.v31/review.json'))
O = {}
TCB13 = p14['tcbDependents']

# ---------------- 14 F ----------------
F31 = V31['fDispositions']
FN = {}


def f(fid, status, basis, limits=None):
    FN[fid] = {'severity': F31[fid]['severity'], 'area': F31[fid]['area'],
               'v31Disposition': F31[fid]['dispositionOn31'],
               'dispositionOn32': status, 'currentBasisOn32': basis,
               'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False}
    if limits:
        FN[fid]['limits'] = limits


PKGV = ('package8: 277/277 members hash-verified, source-manifest byte-equal to the frozen32 '
        'manifest, verify-package.py rc=0 over 12,898 source files with 13 Run/control outcomes '
        'plus 7 query checks, and my own decoder replayed all 13 through both boundaries.')
f('F-01', 'RESOLVED-AND-STILL-HOLDS',
  'The charter custody artifacts remain package members and all 277 members verify. ' + PKGV,
  'Charter custody only; the blind 123/8/3 charter is a separate uninfluenced requirement.')
f('F-02', 'RESOLVED-AND-STILL-HOLDS',
  'The consumer-b.v13 v6/v7 assessment artifacts remain frozen in-package with their attachment '
  'manifest; all package members verified.',
  'Preserved historical files still carry live working-path strings as provenance, not authority.')
f('F-03', 'RESOLVED-AND-STILL-HOLDS',
  'verify-package.py again runs the query reproduction after the 13 outcomes and asserts all seven; '
  'I executed it against frozen32 with rc=0 and query count 7.')
f('F-04', 'RESOLVED-AND-CONTROLLED',
  'The internal-root law and its five enumeration controls are unchanged on 32; '
  'check-enumeration.v1.py exits 0 in my run.',
  'Join controls, which is the correct shape for a boundary that precedes structural custody.')
f('F-05', 'RESOLVED-AND-STILL-HOLDS',
  'ts-invalid-default-entry again replays as structural ADMIT then semantic REFUSE '
  'EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY through the snapshot32 owner.')
f('F-06', 'PARTIALLY-RESOLVED-REMAINDER-STILL-AN-EVIDENCE-LIMIT',
  'Unchanged on 32: the dead parameter is gone and ts-lawful-explicit-selection admits with a '
  'distinct runId.',
  'The two-binding construction remains incomplete and the shipped control is single-explicit only. '
  'That stays an evidence limit, not a demonstrated owner defect.')
f('F-07', 'RESOLVED-BY-DISCLOSURE-STILL-ACCURATE',
  'Unchanged on 32: exists/none only across the seven positives.',
  'and/or/not remain unexercised and count-at-most/all-covered remain unimplemented in the partial '
  'helper, which bounds what the seven Runs evidence.')
f('F-08', 'RESOLVED-AND-STILL-HOLDS',
  'The property probe remains separate from verify-package by design and the README says so; the '
  'effective-edition assertions are unchanged on 32.',
  'Property and mixed-universe probes are separate commands with their own receipts.')
f('F-09', 'RESOLVED-WITH-MY-V31-EVIDENCE-CLAIM-ALREADY-CORRECTED',
  'The §5 citation stands. My v31 report corrected the over-specific function-exclusivity sentence '
  'by AST enclosure; nothing in the 31->32 delta touches execution_inputs_model.v1.py.',
  'No further correction needed here.')
f('F-10', 'RESOLVED-AND-STILL-HOLDS',
  'The portable constructors are unchanged and the exports were originally built on source30 and '
  'preserved byte-identical through 31 and 32. I did NOT re-run the from-scratch construction in '
  'this pass and I do not relabel the historical source30/31 commands as source32 work.',
  'Inherited standing: my source31 construction evidence applies only under exact-input equality, '
  'which I assert for the package exports (all 13 replay identically) and not for the build commands.')
f('F-11', 'RESOLVED-AND-STILL-HOLDS',
  'No vacuous self-comparison remains in the shipped helper; unchanged on 32.')
f('F-12', 'RESOLVED-AND-STILL-ACCURATE',
  'Weighting holds on my own replay: only TS checkpoint3 is helper-versus-owner agreement; the other '
  'six are owner-derived and owner-replayed self-consistency, and the three negatives derive from '
  'checkpoint3.',
  'I weight the six owner-derived Runs as determinism and self-consistency, never as '
  'two-implementation agreement.')
f('F-13', 'RESOLVED-AND-REVERIFIED',
  'sharedReviewDependencies again declares TCB-SCOPE-01 with exactly 13 dependent ids, and the '
  'author assessment binds the frozen32 manifest.')
f('F-14', 'ACKNOWLEDGED-INFORMATIONAL-NO-CHANGE-DEMANDED',
  'All 30 rows again carry the identical self-assessment verdict with distinct rationales and limits. '
  'F-14 asked for no correction and I demand no forced uniform-verdict fix.',
  'I grade no row from that self-assessment; all 30 proposals remain author PENDING, not grades.')
O['fDispositions'] = FN

# ---------------- 30 residuals ----------------
D = 'PROPOSED-REPLACEMENT-REVIEWABLE-AS-DESIGN-NOT-GRADED'
H = 'HISTORICAL-MEASURED-ESCAPE-PRESERVED-NOT-REPAIRED-NOT-GRADED'
ADM = 'docs/v2/contracts/product-v1/admission-and-qualification.md'
PROP = 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'
IDE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
CAN = 'docs/coop/design-corrections/foundation/canonical.py'
COMP = 'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md'
CR = 'docs/coop/design-corrections/foundation/check-replay.v3.py'
rows = {}


def r(rid, owners, status, limits, disposition=D, extra=None):
    rows[rid] = {'disposition': disposition, 'currentOwnerSelectors': owners,
                 'currentStatusOn32': status,
                 'evidenceResolvesAgainstFrozen32': True,
                 'evidenceFileChangedIn31to32': False,
                 'reviewStatus': 'PENDING', 'independentGradeAwardedHere': None,
                 'limits': limits,
                 'sharedAssumption': 'TCB-SCOPE-01' if rid in TCB13 else None,
                 'readingStanding': 'inherited from my v31 reading; cited bytes re-verified '
                                    'byte-equal against frozen32 this session',
                 'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False}
    if extra:
        rows[rid].update(extra)


r('RES-EP13-01', [IDE, COMP], 'Unchanged on 32. The product plan/derivation DAG replacement exists as '
  'published law; the defective historical join stays preserved history.',
  'The historical EP6 join is not executable here; its bytes are not frozen32 members.')
r('RES-EP13-02', [ADM], 'Unchanged on 32; admission-and-qualification.md states the authenticated '
  'first-party TCB with inert typed inputs.',
  'A trust-boundary replacement, not elimination. No same-process hostile-code containment, no '
  'qualified provider isolation, no measured compiler/OS/crypto enforcement.')
r('RES-EP13-03', [ADM], 'Unchanged on 32; the seven-vector census stays a finite historical measurement.',
  'No independent conformance corpus exists; the replacement is specified, not demonstrated.')
r('RES-EP13-04', [ADM], 'Unchanged on 32; closed schemas plus authenticated selected code replace the '
  'identifier tripwire.', 'Shares TCB-SCOPE-01. The attempted containment is abandoned, not achieved.')
r('RES-EP13-05', [PROP, ADM], 'Unchanged on 32, and this review is again an instance: my pins came '
  'from the frozen manifest and I verified all 12,898 rows plus archive equality before use.',
  'Applies to review method, not product runtime.')
r('RES-EP13-06', [ADM, CAN], 'Unchanged on 32; product canonical admission rejects '
  'float/exponent/negative-zero and distinguishes bool from int.',
  'Measured and not repaired remains the label; I did not re-execute the historical encoder.')
r('RES-EP13-07', [IDE, COMP], 'Unchanged on 32. I executed the current analogue: three false-result '
  'controls structurally admit then fail complete proof replay.',
  'Evidence is over author-constructed synthetic Runs, not the historical EP artifacts.')
r('RES-EP13-08', [ADM], 'Unchanged on 32; the fourteen-intent family is retained as bounded history.',
  'No product proof over all PlanIntents is claimed.')
r('RES-EP13-09', [ADM], 'Unchanged on 32; provenance stays distinct from correctness.',
  'Independent oracles and real native measurement are named, not demonstrated.')
r('RES-EP13-10', [ADM, CAN], 'Unchanged on 32; candidate self-counters decide nothing.',
  'The historical battery is not re-run here.')
r('RES-EP13-11', [PROP, ADM], 'Unchanged on 32; historical checker failures stay recorded by cause, '
  'and the row retracts a previous wrong attribution rather than tidying it away.',
  'I executed neither historical checker and their bytes are not frozen32 members. I make no claim '
  'about tool availability in any environment other than the one I measured.')
r('RES-EP13-12', [ADM], 'Unchanged on 32; no sole Python answer-provenance guard carries product '
  'authority, and correctness still needs qualification.',
  'Shares TCB-SCOPE-01. The nine named historical variants remain escapes against the historical system.')
r('RES-EP13-13', [CR], 'Unchanged on 32: check-replay.v3.py is NOT in my 31->32 delta. The NORMATIVE '
  'LAW this row is about — fixture isolation by deep copy, with no sandboxing claim — is unchanged; '
  'the FILE itself last changed at 27->28 for the ruleResults ordering work, which is a different '
  'concern and which I reviewed then.',
  'Shares TCB-SCOPE-01: "fixture isolation only, no process isolation against hostile Python" is the '
  'TCB move restated. Fixture isolation is not process isolation.',
  extra={'readingStanding': ('RR31-02 remediation: the unchanged NORMATIVE LAW is inherited; the FILE '
                             'changed at 27->28 and was read fresh in that session, not in v31. No '
                             'generic byte-equal standing is applied to it here.'),
         'fileLastChangedWindow': '27->28', 'lawUnchangedSince': '27'})
r('RES-EP13-14', [ADM], 'Unchanged on 32; the differential census is not an equivalence proof or a '
  'release oracle.', 'The replacement obligations are specified and unperformed.')
r('RES-EP13-15', [IDE, COMP], 'Unchanged on 32; the row declines to re-pin onto check-c2-v5.py to '
  'escape a blocking adjudication.',
  'The adjudication is not closed here and the historical v4/v5 bytes are not frozen32 members.')
r('RES-EP13-16', [ADM], 'Unchanged on 32; producer-supplied flags cannot bypass independent replay, '
  'which my replay supports: the controls carry claimed verdicts and are refused because the owner '
  'recomputes.', 'Shares TCB-SCOPE-01. Replay independence is shown over synthetic author Runs only.')
r('RES-EP13-17', [ADM], 'Unchanged on 32; text-only disclosures stay text-only and meaning is '
  'assigned to substantive design review, which this is for the design layer.',
  'No padding or anchor counter establishes architectural completeness.')
r('RES-EP13-18', [ADM], 'Unchanged on 32; no hidden-window mechanism is retained.',
  'Shares TCB-SCOPE-01. The attack remains valid against the historical system rather than repaired.')
r('RES-EP13-19', [ADM], 'Unchanged on 32; the row concedes anchors cannot stop contradictory padding '
  'and requires independent semantic review.',
  'Its discharge depends on a reader being honest, which no mechanism in the subject guarantees.')
r('IR-EP13-NB-01', [ADM], 'Unchanged on 32; the correction generalises to the capability class '
  'rather than to variant names.',
  'Shares TCB-SCOPE-01. Covered by exclusion, not by a control.')
r('IR-EP13-NB-02', [ADM], 'Unchanged on 32; the scan is retired as a scope decider.',
  'NOT a TCB-SCOPE-01 dependent: the disposition holds wherever the boundary is drawn.')
r('IR-EP13-NB-03', [ADM], 'Unchanged on 32; no unreachability claim is made.',
  'Shares TCB-SCOPE-01. The real provider boundary is deferred and unqualified.')
r('IR-EP13-NB-04', [ADM], 'Unchanged on 32; one explicit TCB/scope account is used.',
  'Shares TCB-SCOPE-01. Stale nonClaims prose is still present as history.')
r('IR-EP13-NB-05', [ADM], 'Unchanged on 32; message granularity is an operability acceptance case '
  'rather than proof validity — the same distinction that makes the new repair remedy coordinates '
  'worth having.', 'Operability cases are acceptance obligations this design review does not perform.')
r('IR-EP13-NB-06', [ADM], 'Unchanged on 32; the parity rule is preserved as history.',
  'NOT a TCB-SCOPE-01 dependent on my reading.')
r('IR-EP13-NB-07', [PROP, ADM], 'Unchanged on 32 and further strengthened as an input matter: the '
  'source29 failed receipt and the 29/30 native-cases bytes are now supplied and I inspected them.',
  'Corroborated in form. The bundle is new custody supplied to me now, not retro-authentication of '
  'the original transition.')
for v, note in (('AX6', 'stack-walking witness forgery'),
                ('AX9', 'obfuscated witness forgery'),
                ('MD5', 'observed-window discrimination by ledger-entry count'),
                ('RX2c', 'unenumerated witness forgery')):
    r(v, [ADM, 'docs/coop/artifacts/evaluation-proof.v13.json'],
      'Historical measured escape (%s), unchanged on 32; the cited original remains a frozen member '
      'and declares this variant in the escaped-every-guard set.' % note,
      'Shares TCB-SCOPE-01. The row carries no inline original of its own; evidence comes from the '
      'cited artifact. Nothing is repaired, regraded, rerun or authenticated.',
      disposition=H)
assert len(rows) == 30, len(rows)
O['evaluationResidualDispositions'] = rows
O['evaluationResidualStanding'] = {
    'source': PROP, 'sourceSha256': p14['proposalSha256'],
    'unchangedIn31to32': not p14['proposalChangedIn31to32'],
    'idsMatchAuthorAssessment': p14['idsMatchAuthorAssessment'],
    'authorAssessmentBindsFrozen32': p14['authorBindsFrozen32'],
    'bindingChecks': {'evidenceUnresolved': p14['evidenceUnresolved'],
                      'evidenceShaMismatches': p14['evidenceShaMismatches'],
                      'evidenceFilesChangedIn31to32': p14['evidenceFilesChangedIn31to32'],
                      'rowsNotPending': p14['rowsNotPending'],
                      'citedDocuments': p14['citedDocuments']},
    'allThirtyRemainAuthorProposalsPending': True,
    'gradedFromAuthorSelfAssessment': False,
    'uniformSelfAssessment': p14['authorVerdictCounts']}
O['sharedAssumptionTCBSCOPE01'] = {
    'id': 'TCB-SCOPE-01', 'assessedOnceAsOneAssumption': True,
    'assumption': p14['tcb']['assumption'], 'consequence': p14['tcb']['consequence'],
    'dependentRowCount': 13, 'dependentRows': TCB13,
    'myAssessment': ('Coherent, disclosed and consistently applied as design, and stated explicitly in '
                     'admission-and-qualification.md rather than left implicit. I do not grade it. '
                     'Rejecting or changing this ONE assumption reopens all thirteen dependent '
                     'accounts TOGETHER — never thirteen independent successes — and would neither '
                     'repair the historical attacks nor establish containment.'),
    'adjudicationOwner': 'the separate final application review, once and explicitly'}

# ---------------- issues, standing, verdict ----------------
O['newMustIssues'] = []
O['newShouldIssues'] = []
O['advisories'] = [
    {'id': 'A-9', 'title': 'The repair selection law is reference-level only; no product surface emits it',
     'selectors': ['docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
                   'docs/v2/contracts/product-v1/workflows-and-surfaces.md section 6',
                   'crates/host/src/repair.rs (planned, unwritten)'],
     'measured': ('The law is published, the reference module implements it and I executed it, but '
                  'the only projection of it is a synthetic host adapter that the source itself '
                  'labels as gate integration only. No admitted current RepairPlanDescriptor and no '
                  'real snapshot/preimage join exists anywhere in the subject.'),
     'why_not_a_should': ('This is the expected state of a design-and-reference layer and the source '
                          'says so in three places rather than overstating it. Demanding a product '
                          'repair implementation would be demanding implementation as a design '
                          'acceptance prerequisite, which I decline to do.'),
     'forWhom': 'the separate application review, which must not read the synthetic projection as descriptor evidence'},
    {'id': 'A-10', 'title': 'Two-binding and combinator coverage remain unexercised in the author package',
     'selectors': ['claude-author-package-successor.v8 binding-controls/',
                   'author-helpers/evaluator.py'],
     'measured': ('exists/none only; and/or/not unexercised; count-at-most and all-covered '
                  'unimplemented in the partial helper; the two-binding construction incomplete with '
                  'a single-explicit control.'),
     'why_not_a_should': ('Carried unchanged from source31 where I already assessed it as an evidence '
                          'limit rather than a demonstrated owner defect. Nothing in the 31->32 delta '
                          'changes it and nothing depends on it being closed for this design layer.')}]
O['resolvedSinceV31'] = {
    'repairClosedWorldSelectionGap': {
        'status': 'RESOLVED IN THESE BYTES',
        'whatWasMissing': ('at source31 the selection law read ownership only from source-path '
                           'relation subject scopes, so a selected program owning an unsafe path '
                           'through its retained symbol extent or candidate census could be called '
                           'unrelated — the RRS-A1 gap my bounded review confirmed'),
        'howIVerifiedTheFix': ('executed the new module: the symbol-extent owner is returned; '
                               'candidateSourcePaths counts; unavailable selected bindings give typed '
                               'unresolved ownership that an available closed owner does not '
                               'discharge; unselected programs are never inferred; extents stay '
                               'distinct; witnesses are unioned but never certify completeness'),
        'note': ('My source31 ACCEPT was its historical substantive verdict on those bytes and was '
                 'not authority to ignore this gap. It is closed here on evidence, not on assurance.')},
    'RRS_A2_all_five_points': {
        'status': 'RESOLVED IN THESE BYTES',
        'sentinelWording': 'the five-field least-closed sentinel is described consistently and is '
                           'explicitly "NOT an all-unknown record"; exactly two members are unknown',
        'authoritativeBoolean': 'the module now states NO MEMBER IS AUTHORITATIVE, the boolean included',
        'summaryVersusEligibility': 'absence is folded into the reduction, so the summary cannot read '
                                    'closed while eligibility is refused',
        'orderingPublication': 'UTF-8 encoded bytes and the six-member key including the coverage2 '
                               'identity are published in both the module and chapter 6',
        'remedyNamesTheRecord': 'verified by execution that two records differing only in '
                                'targetUniverse, subjectScopeCommitment and identity now produce '
                                'distinct remedy coordinates'},
    'A_8_inputLimit': {'status': 'DISCHARGED', 'how': 'the bundle was supplied and I inspected it; '
                       'exactly one 64-hex leaf differs between the 29 and 30 native-cases bytes and '
                       'the failed source29 receipt is preserved with passed=false'},
    'A_7_scopeSentence': {'status': 'CORRECTED IN THIS REPORT', 'how': 'the native schema FILE did '
                          'change in the 27->31 window; the POINTER is what is unchanged, and its v2 '
                          'definitions are byte-identical to v3. No cosmetic repoint is selected.'}}
O['evidenceReceipts'] = {
    'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B via stdlib subprocess',
    'changedInputCheckers': {'jobs': [{'checker': j['checker'], 'rc': j.get('returncode'),
                                       'justification': j.get('justification')}
                                      for j in p06['jobs']],
                             'allExitZero': p06['allExitZero'],
                             'disposableCopyVerified': p06['disposableVerified']},
    'pinnedLauncher': p13.get('launcherReport'),
    'planningGroups': [{'checker': x['checker'], 'rc': x.get('returncode'),
                        'lastLine': x.get('lastLine')} for x in p13['planningGroups']],
    'authorPackage': {'members': p09['declaredMembers'], 'verified': p09['verified'],
                      'sourceManifestEqualsFrozen32': p09['sourceManifestEqualsFrozen32Manifest'],
                      'positivesAdmitBoth': p09['positivesAdmitBoth'],
                      'negativesAdmitThenRefuse': p09['negativesAdmitThenRefuse'],
                      'bindingInvalidRefused': p09['bindingInvalidRefused'],
                      'verifierReturncode': p10['verifier']['returncode'],
                      'queryChecks': p10.get('queryChecks'),
                      'thirteenOutcomes': p10.get('thirteenOutcomes')},
    'repairLawExecution': {k: p05[k] for k in
                           ('rrsA1_symbolOwnerFound', 'unavailableBinding', 'unselectedNotInferred',
                            'remedyDistinguishes', 'displaySummary', 'gate')},
    'frozenDeviationsAfterAllRuns': p13['frozenDeviationsAfterRuns'],
    'failedProbesPreserved': [
        'p03 first run had a Python syntax error in my own comprehension',
        'p04 compared open_run_closure against the `def derive` DEFINITION line and monkey-patched '
        'RM.M, which broke the replay; both wrong, preserved',
        'p04b built the graph with build_file_inputs+seal_fixture alone, which is not '
        'replay-consistent and refused EVALUATOR_COMPLETE_PROOF_REPLAY',
        'p05 passed `universe` twice to my own fixture helper',
        'p07 called the fixture option without its required multiple_universes/symbol_rows and hit '
        'the guard FIXTURE3_SYMBOL_ONLY_REQUIRES_TWO_PROGRAMS',
        'p12b used out-of-enum capabilityId/languageMode so both instances refused for an unrelated '
        'reason and the result was inconclusive, not evidence of non-enforcement']}
O['crossUnitStanding'] = {
    'evaluationResidualsRetained': 30, 'closedByThisReview': 0,
    'condition2Obligations': 28, 'condition2ObligationsRetained': 28,
    'qualificationGates': 32, 'qualificationGatesPerformed': 0, 'condition5': 'NOT MET',
    'commitRecoveryCases': 54, 'commitRecoveryCasesExecuted': 0,
    'd9SuccessorObligation': ('DR-007 and DR-011-R08: the published D9 successor carrying '
                              'host-invariant remains an ASSIGNED implementation obligation, carried '
                              'forward and not closed.'),
    'blindCharter': ('The original 123/8/3 blind reconstruction is a separate requirement. I read no '
                     'consumer runtime, output or report and claim no blind acceptance.')}
O['dispositionStandingForEveryRow'] = {
    'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False,
    'independentApplicationGradeAwarded': None,
    'appliesTo': 'every F, evaluation residual, AR, FW, inherited and scoped-owner row without exception'}
O['dispositionCounts'] = {'fDispositions': 14, 'evaluationResidualDispositions': 30,
                          'arDispositions': 16, 'fwDispositions': 15,
                          'inheritedResidualDispositions': 27, 'scopedReviewOwnerDispositions': 5,
                          'total': 107}
O['limitations'] = [
    'Design and reference layers only. No product implementation exists to test, and none is demanded.',
    'The repair selection law is verified at reference level: I executed the published module and the '
    'reference controls. No product repair preview/apply/recovery exists.',
    'The synthetic host projection demonstrates gate integration only. It is not an admitted current '
    'descriptor, not a real snapshot/preimage join and not a lawful old-preview bypass.',
    'The author package is author-assisted evidence. No row is graded from its self-assessment and '
    'all 30 residual proposals remain author PENDING.',
    'Package exports were originally constructed on source30 and preserved through 31 and 32. I '
    'replayed them against frozen32 but did NOT re-run the from-scratch construction in this pass, '
    'and I do not relabel those historical commands as source32 work.',
    'exists/none only; and/or/not unexercised; count-at-most/all-covered unimplemented in the partial '
    'helper; two-binding incomplete with a single-explicit control.',
    'Nothing here grants provider, compiler, OS or process-isolation qualification.',
    'Finite hash controls show distinct identities for finitely changed inputs; they do not prove '
    'global SHA-256 injectivity.',
    'root-delta31-to32.json was not locatable at the named path, so my delta stands on its own '
    'derivation rather than on a comparison with it.',
    'I could not certify that exactly two implementation-coverage verification methods changed, '
    'because the source31 bytes of that file are not in this runtime; I report what the current '
    'methods say.',
    'All 54 commit-recovery cases and all 32 qualification gates remain unperformed; condition 5 is '
    'NOT MET.',
    'Unchanged readings are inherited only after exact-byte verification and are labelled as such.']
O['grantsNothing'] = {
    'grade': None, 'architectureReady': False, 'activation': False, 'implementationAuthorized': False,
    'blindAcceptance': False, 'finalApplicationOutcomeGranted': False, 'commitOrPush': False,
    'stillRequired': ['final application review', 'activation decision',
                      'successful original blind 123/8/3 reconstruction',
                      'product qualification of the 32 gates and 54 recovery cases']}
O['verdict'] = 'ACCEPT'
O['verdictBasis'] = (
    'Every declared input verified before use, including full archive-to-manifest equality over all '
    '12,898 members and ancestry to the exact frozen31 I graded. My independently derived delta is 3 '
    'added, 0 removed, 23 changed. The new repair closed-world selection owner is substantively '
    'correct, conservative and complete for its stated scope: I executed it and confirmed that '
    'ownership now comes from the retained EnumerationPlan census, that unavailable selected bindings '
    'give typed unresolved ownership an available closed owner cannot discharge, that unselected '
    'programs are never inferred, that extents stay distinct, that source-path scopes are witnesses '
    'rather than a completeness certificate, that coverage selection is independent of the recipe, '
    'that the conjunction is non-vacuous with absence folded into the display, and that remedies now '
    'name the actual retained record. Chapter 6 publishes exactly that law, both repair schemas and '
    'the native chapter link agree, and the model seam is in place. The RRS-A3 evidence boundary is '
    'honestly scoped in three separate places and needs no narrow reference correction. The glob '
    'contract now has one coherent normative reading across all six owners including the new main '
    'chapter link. Planning is consistent with no new package or filename, layer3 binds 29 inputs '
    'that all resolve, and all five pin ledgers carry both new owners with the reference .py '
    'correctly pin-only rather than a normative input. All changed-input checkers, the pinned '
    'launcher (1244 pins, 16/16 children) and both planning groups exit 0, with zero frozen '
    'deviations. Package8 verifies 277/277 and all 13 outcomes replay through both boundaries with 7 '
    'query checks. All five root review-record corrections plus one I identified myself are applied '
    'here without altering the source31 report. No unresolved required issue: zero new MUST, zero new '
    'SHOULD, two advisories each stating why it is not a SHOULD. This is a DESIGN review only and '
    'grants no application grade, activation, blind acceptance or implementation authorization.')
json.dump(O, open(os.path.join(BASE, 'part3.json'), 'w'), indent=1, default=str)
print('part3 keys:', len(O), '| verdict:', O['verdict'])
print('residuals:', len(rows), '| TCB dependents:', sum(1 for v in rows.values() if v['sharedAssumption']))
