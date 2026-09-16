"""Part 2 — the 30 evaluationResidualDispositions, keyed by the EXACT ids of source27
docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json.

Every row carries its own disposition, basis, owning selectors, scope and limits. No row is graded
from the author's authorAssessment; each basis names bytes I read or executed. TCB-SCOPE-01 is
assessed ONCE as a single shared assumption and its 13 dependents point at that one adjudication.
"""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v27'
REC = os.path.join(BASE, 'receipts')
pN = json.load(open(os.path.join(REC, 'pN-residualbind.json')))
own = {r['id']: [e['path'] for e in r['evidence']] for r in pN['rows']}
TCB13 = ['RES-EP13-02', 'RES-EP13-04', 'RES-EP13-12', 'RES-EP13-13', 'RES-EP13-16', 'RES-EP13-18',
         'IR-EP13-NB-01', 'IR-EP13-NB-03', 'IR-EP13-NB-04', 'AX6', 'AX9', 'MD5', 'RX2c']

D = 'PROPOSED-REPLACEMENT-REVIEWABLE-AS-DESIGN-NOT-GRADED'
H = 'HISTORICAL-MEASURED-ESCAPE-PRESERVED-NOT-REPAIRED-NOT-GRADED'

rows = {}


def r(rid, basis, scope, limits, disposition=D):
    rows[rid] = {
        'disposition': disposition,
        'basis': basis,
        'owningSelectors': own[rid],
        'scope': scope,
        'limits': limits,
        'sharedAssumption': 'TCB-SCOPE-01' if rid in TCB13 else None,
        'independentGradeAwardedHere': None,
        'appliedByThisReview': False,
        'finalApplicationOutcomeGranted': False}


r('RES-EP13-01',
  'The original is preserved inline and states that EP6 is pinned and executed transitively over '
  'defective check-c2.py bytes that this candidate does not repair. The proposed replacement is a '
  'product plan/derivation DAG schema with recomputed source/Plan joins. I read identity-and-evidence '
  'section 3-5 and the composition contract: the derivation DAG and its joins exist as published law '
  'and are recomputable, so the replacement is real design rather than a promise.',
  'Design law only. Replacing a defective historical join is not repairing it, and the old EP6/EP8 '
  'checker bytes remain defective history.',
  'I did not execute the historical EP6 join and could not: those bytes are not members of frozen27.')
r('RES-EP13-02',
  'The original discloses that answer provenance is not established against any adversarial route '
  'region, and names AX6/AX9/MD5/RX2c as measured instances of an unbounded class. The correction '
  'declares an authenticated first-party TCB with inert typed inputs. admission-and-qualification.md '
  '(sha 69cd6ba3..., unchanged 26->27) does state that boundary explicitly, so the account is '
  'faithful to the bytes it cites.',
  'A trust-boundary replacement, exactly as the row itself labels it. It does not eliminate the '
  'historical attack class.',
  'I claim no same-process hostile-code containment. The pure host/evaluator is authenticated and '
  'consumes inert data; provider process isolation is unqualified and the compiler, OS and crypto '
  'enforcement are unmeasured.')
r('RES-EP13-03',
  'The original bounds seven pinned vectors over one PlanIntent and says every value-equality result '
  'inherits that limit. The correction refuses to treat the measurement as an equivalence proof and '
  'routes conformance to independent source/semantic cases. That is the same distinction I apply to '
  'the seven author Runs in this review, so I find it consistent rather than convenient.',
  'A finite historical measurement stays finite. Reference counts confer no universal property.',
  'No independent conformance corpus exists yet to replace it; the replacement is specified, not '
  'demonstrated.')
r('RES-EP13-04',
  'The original records an identifier tripwire that is an enumeration of spellings, unscored, and '
  'measured escaping on every run. The correction declines to carry any identifier tripwire into '
  'product authority and substitutes closed input schemas plus authenticated selected code. I '
  'verified closed-schema admission is real law on 27 by execution elsewhere in this review (the '
  'root-representation and logicalPath boundaries both refuse on closed selectors).',
  'Declining a guard is stronger than lengthening its enumeration, and the row says so.',
  'Shares TCB-SCOPE-01. No claim that the attempted same-process containment is achieved by other '
  'means; it is abandoned, not replaced.')
r('RES-EP13-05',
  'The original is the honest statement that a checker cannot pin itself. The correction moves '
  'reviewer pins outside the author instrument and makes the frozen reviewed snapshot the subject. '
  'This review is an instance of that correction working: my pins came from the frozen manifest at '
  '/Users/sb/.../candidate-subject.v27.json, I verified all 12893 files before use, and I never '
  'treated a checker\'s self-scan as authentication.',
  'Applies to review method, not to product runtime.',
  'The manifest I trust is itself supplied to me; I verified its internal consistency and its '
  'declared parent, not its provenance.')
r('RES-EP13-06',
  'The original measures a canonical unsigned-decimal encoder defect and deliberately leaves it. The '
  'correction points at product canonical admission rejecting float/exponent/negative-zero and '
  'distinguishing bool from int. foundation/canonical.py is cited and is unchanged in 27; my v26 '
  'reading of AR-01 covered exactly this law and found it specified.',
  'Product canonical admission, not the historical encoder.',
  'Measured and not repaired is the row\'s own label and I keep it. I did not re-execute the '
  'historical encoder.')
r('RES-EP13-07',
  'The original measures 3 of 5 identity-moving positions that move durable identity beneath a '
  'byte-identical seal ref. The correction binds Plan, execution plan, evidence, evaluator, policy, '
  'proof and verdict into the seal and requires wrong-Plan and rehashed-false-proof cases to refuse. '
  'I executed the closest current analogue this session: the three false-result controls structurally '
  'admit and then fail complete proof replay with EVALUATOR_COMPLETE_PROOF_REPLAY.',
  'Current seal/replay law; the historical seal stays a poor witness.',
  'My replay evidence is over author-constructed synthetic Runs, not over the historical EP artifacts.')
r('RES-EP13-08',
  'The original publishes 14 distinct intents as a measurement, not a proof over the PlanIntent space. '
  'The correction retains it as bounded history and routes universality to schemas, joins and '
  'implementation conformance. The row does not inflate the number, which is the defect the corpus '
  'kept rejecting.',
  'Bounded historical measurement.',
  'No product proof over all PlanIntents exists; none is claimed.')
r('RES-EP13-09',
  'The original separates provenance from correctness. The correction keeps that separation and adds '
  'independent oracle comparison plus real native measurement for qualification. This is the same '
  'separation I enforce when I decline to treat the package\'s expected outputs as correctness '
  'evidence.',
  'Provenance law only.',
  'Independent oracles and real native measurements are named obligations, not demonstrated ones.')
r('RES-EP13-10',
  'The original records that the own-constant-leaf battery cannot re-run itself and that four of its '
  'counters are admitted under a float spelling. The correction denies candidate self-counters any '
  'role in product admission and puts exact schema typing first. canonical.py is the cited owner and '
  'its float/bool discrimination is the mechanism that would refuse those four positions today.',
  'Admission typing, not report content.',
  'The historical battery is not re-run here.')
r('RES-EP13-11',
  'The original records two pre-existing checkers failing for causes not attributable to the '
  'candidate, and retracts a previous wrong attribution (RET-EP13-06). The correction keeps the '
  'failures recorded by cause and refuses to re-label either checker as passing or to close the blind '
  'litmus by prose. The retraction is the strongest evidence in this row: the account corrects itself '
  'rather than tidying.',
  'Historical checker custody.',
  'I did not run those two historical checkers; one of them needs an rg binary that is not on this '
  'host either.')
r('RES-EP13-12',
  'The original publishes per-variant sole-guard rows so that single points of failure are disclosed. '
  'The correction declares that no sole Python answer-provenance guard is carried into product '
  'authority and explicitly adds that correctness still needs qualification. The row does not '
  'convert the removal of a guard into a security gain.',
  'Product authority only.',
  'Shares TCB-SCOPE-01. The nine named historical variants remain escapes against the historical '
  'system.')
r('RES-EP13-13',
  'The original measures 280 injections through 3 guards mutating nothing, published as a hazard that '
  'has not occurred rather than a repair. The correction deep-copies hostile inputs in the new '
  'mutation/reference cases and says plainly this is fixture isolation only, with no claim that a '
  'Python program is sandboxed. check-replay.v3.py is the cited owner and is unchanged in 27.',
  'Fixture isolation in the reference cases.',
  'Shares TCB-SCOPE-01 — my own reading put this row in the dependent set even though a keyword pass '
  'missed it, because "no process isolation against hostile Python" is the TCB move restated. '
  'Fixture isolation is not process isolation.')
r('RES-EP13-14',
  'The original states the differential oracle is asymmetric and explicitly NOT SUFFICIENT ALONE. The '
  'correction stops using the census as an equivalence proof or release oracle and names independent '
  'oracle, corpus and replay obligations separately.',
  'Oracle weighting.',
  'The replacement obligations are specified and unperformed.')
r('RES-EP13-15',
  'The original refuses to re-pin onto check-c2-v5.py to escape a blocking adjudication, and records '
  'that v5 admits 13 of 66 integer leaves behind a green banner. The correction declines to elevate '
  'the v4 self-census and routes to product plan/derivation identity schemas and retained mutation '
  'tests under D-372, with independent review of their bytes still required.',
  'Pin custody and successor routing.',
  'The adjudication is not closed by this review, and I did not examine the historical v4/v5 bytes: '
  'they are not members of frozen27.')
r('RES-EP13-16',
  'The original states A-2/A-9 hold only inside a window the guard opens, so substitution outside it '
  'is detected and not prevented. The correction retains no observed-window guarantee and declares '
  'the whole callable evaluator trusted selected code whose producer-supplied flags cannot bypass '
  'independent replay. That last clause is the one I can test, and my replay evidence supports it: '
  'the false-result controls carry claimed verdicts and are refused because the owner recomputes '
  'rather than trusting them.',
  'Replay independence, not containment.',
  'Shares TCB-SCOPE-01. Replay independence is demonstrated over synthetic author Runs only.')
r('RES-EP13-17',
  'The original declares two residuals text-only rather than inventing a test that would pass on '
  'hollow text, and puts the text-only ids in the checker so the artifact cannot demote them. The '
  'correction keeps them text-only and assigns meaning to substantive design review. I accept that '
  'assignment and this review is its discharge for the design layer.',
  'Disclosure mechanics.',
  'A padding or anchor counter cannot establish architectural completeness, and I do not treat my own '
  'reading counts as establishing it either.')
r('RES-EP13-18',
  'The original publishes the side channel beside the rule that has it: an unobserved commitment call '
  're-enters the ledger and an anchor-served one does not, and MD5 escapes every scored guard using '
  'that delta. The correction retains no hidden-window mechanism, so ledger-entry-count discrimination '
  'is not claimed as a containment boundary.',
  'Mechanism retirement.',
  'Shares TCB-SCOPE-01. The row states the attack remains valid against the historical system rather '
  'than repaired, which is the honest form.')
r('RES-EP13-19',
  'The original concedes that load-bearing anchors still cannot stop an author padding them with '
  'contradictory prose, because binding is not meaning. The correction requires independent semantic '
  'review and denies that source pins and passing counts replace it. My own review is built that way: '
  'the pinned launcher passing 16/16 is recorded as a receipt, never as the assessment.',
  'Review method.',
  'This is the one row whose discharge depends on a human-or-agent reading being honest, which no '
  'mechanism in the subject can guarantee.')
r('IR-EP13-NB-01',
  'The observation is that the class was disclosed at its weakest reachable severity: the published '
  'instance routes the commitment while a region of the same class routes the gate. The correction '
  'generalises to the capability class rather than to variant names and claims no historical guard '
  'repaired. Generalising to the capability is the right move precisely because enumerating names was '
  'the defect RES-EP13-04 records.',
  'Class-level scope statement.',
  'Shares TCB-SCOPE-01. The stronger gate/preimage substitution is covered by exclusion, not by a '
  'control.')
r('IR-EP13-NB-02',
  'The observation is that a punctuation/name scan is defeated by punctuation and cannot detect '
  'narrowing at all, so "refuses it structurally rather than by intention" was an overclaim. The '
  'correction retires the scan as a scope decider and requires semantic reading of the complete '
  'contract. I read admission-and-qualification.md completely in v26 and its bytes are unchanged in 27.',
  'Scope-determination method.',
  'NOT a TCB-SCOPE-01 dependent. My keyword classifier flagged it, but on reading, its disposition — '
  'a grep is not a structural guarantee — holds wherever the trust boundary is drawn.')
r('IR-EP13-NB-03',
  'The observation measures 75 private instances left in sys.modules, falsifying '
  'independentPathIsUnreachable. The correction makes no unreachability claim at all and states that '
  'product code is authenticated TCB with providers communicating through sealed protocol data.',
  'Reachability claims.',
  'Shares TCB-SCOPE-01. The real provider boundary is deferred to implementation and is unqualified '
  'here; I make no qualified-provider-isolation claim.')
r('IR-EP13-NB-04',
  'The observation is that assurance.nonClaims and guardInventory prose are unenforced and carry stale '
  'counts. The correction uses one explicit TCB/scope account, avoids historical variant counts as a '
  'security claim, and leaves the stale prose as history. Assigning narrative reconciliation to the '
  'final application review is the correct routing, not an evasion.',
  'Narrative consistency.',
  'Shares TCB-SCOPE-01. The stale prose is still present as history and a reader could still mistake '
  'it for current; only the routing is fixed here.')
r('IR-EP13-NB-05',
  'The observation is that contradictory prose around intact anchors still passes and the rejection '
  'message names the block. The correction requires substantive review and classifies message '
  'granularity as an operability acceptance case rather than proof validity. That distinction is '
  'correct and it is also the distinction that makes F-04 a real defect: a misattributed fault code '
  'is an operability and diagnostic defect, which is exactly why 27 now raises a root-specific fault.',
  'Diagnostic granularity.',
  'Operability cases are acceptance obligations that this design review does not perform.')
r('IR-EP13-NB-06',
  'The observation records an attacker cost the design imposes, worth recording as the one place A-9 '
  'bites harder than the scope admits. The correction preserves it as history and refuses to import '
  'it as a product isolation guarantee. Declining to bank a cost as a guarantee is the right call.',
  'Historical cost accounting.',
  'NOT a TCB-SCOPE-01 dependent on my reading: the claim that a parity rule imposes cost without '
  'closing a class is independent of where the trust boundary sits.')
r('IR-EP13-NB-07',
  'The observation is about environment and reproduction. The correction preserves the original '
  'environment and measurements and requires new reports to name their own environment and source '
  'pins without overwriting or reclassifying old results. I verified the form of this myself: the '
  'package keeps historical-source25-preparation, historical-source26-preparation and '
  'historical-intermediate-preparation intact beside the current artifacts, and root-replay-'
  'verification reports are separate files.',
  'Report custody.',
  'Corroborated in form. The F-01/F-02/F-03 custody gaps that weakened this row in the predecessor '
  'review are now closed, which strengthens it, but "preserved unchanged" is still an author account '
  'for the periods before my first verification.')
r('AX6',
  'A historical measured escape: stack-walking witness forgery. The correction claims no protection '
  'against same-process adversarial route regions and names exact typed-data admission plus a trusted '
  'authenticated pure evaluator as the boundary, adding that replayed result comparison is '
  'reproducibility and not Python containment. That last sentence is the one that keeps the row '
  'honest.',
  'Historical escape preserved; mechanism absent from product authority.',
  'Shares TCB-SCOPE-01. This row carries neither an inline original nor an originalTitle, and its '
  'cited source artifact is not a member of frozen27 — see advisory A-5. I assess the disposition on '
  'its own terms against admission-and-qualification.md, not against its cited original.',
  H)
r('AX9',
  'A historical measured escape: obfuscated witness forgery, which defeats identifier scans. Its '
  'correction is textually the same as AX6/MD5/RX2c, but the row is individually reasoned in the '
  'author assessment, and the shared correction is appropriate here because the whole point of '
  'RES-EP13-04 is that the boundary must not depend on enumerating spellings.',
  'Historical escape preserved; mechanism absent from product authority.',
  'Shares TCB-SCOPE-01. Same original-custody limit as AX6 (advisory A-5). The attack class is '
  'unbounded by construction, so no census closes it.',
  H)
r('MD5',
  'A historical measured escape: observed-window discrimination by ledger-entry count. It is the '
  'concrete instance RES-EP13-18 was built to make real rather than leave as a caveat, and it is the '
  'variant measured escaping every scored guard. Preserving it rather than quietly dropping it is the '
  'behaviour I want from this corpus.',
  'Historical escape preserved; mechanism absent from product authority.',
  'Shares TCB-SCOPE-01. Same original-custody limit as AX6 (advisory A-5). Side-channel resistance is '
  'explicitly disclaimed, and I claim none.',
  H)
r('RX2c',
  'A historical measured escape standing for the unenumerated remainder: mechanisms that cannot be '
  'ruled out by an attack-name census. Keeping an explicitly open-ended row is what stops the other '
  'three from being read as an exhaustive list.',
  'Historical escape preserved; mechanism absent from product authority.',
  'Shares TCB-SCOPE-01. Same original-custody limit as AX6 (advisory A-5). Semantic correctness and '
  'host qualification remain open.',
  H)

assert len(rows) == 30, len(rows)
out = {'evaluationResidualDispositions': rows}
out['evaluationResidualStanding'] = {
    'keyedByExactSourceIds': True,
    'source': 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json',
    'sourceSha256': json.load(open(os.path.join(REC, 'pN-residualbind.json')))['proposedSha256'],
    'idsMatchSourceExactly': True,
    'rowCount': 30,
    'noneClosedByThisReview': True,
    'gradedFromAuthorSelfAssessment': False,
    'bindingChecksIRan': {
        'idsIdenticalToSource27': pN['idsIdentical'],
        'selectorMismatches': pN['selectorMismatches'],
        'correctionTextMismatches': pN['correctionMismatches'],
        'evidencePathsNotInFrozen27': pN['evidencePathsNotInFrozen27'],
        'evidenceShaMismatchesVsFrozen27': pN['evidenceShaMismatches'],
        'sourceBytesChangedClaimsDisagreeingWithMyDelta': pN['changeClaimDisagreements'],
        'rowsNotPending': pN['rowsNotPending'],
        'rowsClaimingApplied': pN['rowsClaimingApplied'],
        'rowsReclassifyingHistory': pN['rowsReclassifyingHistory'],
        'distinctCitedDocuments': len(pN['citedDocuments']),
        'onlyCitedDocumentChangedIn27': 'docs/v2/contracts/product-v1/identity-and-evidence.md'}}
out['sharedAssumptionTCBSCOPE01'] = {
    'id': 'TCB-SCOPE-01',
    'assumption': ('Selected authenticated in-process host/evaluator code is trusted; adversarial code '
                   'sharing that process is outside this product threat model. Untrusted inputs are '
                   'inert typed data and provider process boundaries still require real qualification.'),
    'dependentRowCount': 13,
    'dependentRows': TCB13,
    'assessedAsOneAssumption': True,
    'myIndependentVerificationOfTheList': (
        'I classified all 30 rows myself rather than accepting the declared list. A keyword pass '
        'returned 14 and disagreed on three rows; I then read those three in full. RES-EP13-13 belongs '
        'in the set (its disposition is "fixture isolation only, no process isolation against hostile '
        'Python"); IR-EP13-NB-02 and IR-EP13-NB-06 do not, because their dispositions hold wherever '
        'the boundary is drawn and my classifier had matched a shared evidence-scope label rather than '
        'their reasoning. Read row by row, the declared 13 is exactly right.'),
    'consequenceIfRejected': ('Rejecting or changing this one assumption reopens all thirteen accounts '
                              'together. It would never be thirteen independent successes, and it would '
                              'not repair the historical attacks or establish containment.'),
    'myDesignAssessment': (
        'As a design move the assumption is coherent, disclosed and consistently applied, and '
        'admission-and-qualification.md states it explicitly rather than leaving it implicit. I do not '
        'grade it. An authenticated pure host/evaluator consuming inert data is what the bytes '
        'describe; I claim no same-process hostile-code containment, no qualified provider isolation, '
        'and no measured compiler, OS or crypto enforcement.'),
    'adjudicationOwner': 'the separate final application review, which must adjudicate it once, explicitly'}
json.dump(out, open(os.path.join(BASE, 'review.part2.json'), 'w'), indent=1)
print('rows:', len(rows), '| TCB dependents:', sum(1 for v in rows.values() if v['sharedAssumption']))
print('dispositions:', sorted(set(v['disposition'] for v in rows.values())))
