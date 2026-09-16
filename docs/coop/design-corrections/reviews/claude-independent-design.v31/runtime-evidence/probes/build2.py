"""review.json part 2 — the 30 evaluationResidualDispositions on frozen31 and TCB-SCOPE-01.

Keyed by the exact ids of source31 evaluation-residual-dispositions.proposed.json. Every row names
current owner selectors and evidence, its current status and its limits. Rows whose substantive
reading is unchanged since v27 say so explicitly, after exact-byte verification, and are labelled
inherited rather than presented as fresh.
"""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
REC = os.path.join(BASE, 'receipts')
p20 = json.load(open(os.path.join(REC, 'p20-residuals31.json')))
p13 = json.load(open(os.path.join(REC, 'p13-ax-originals.json')))
own = {r['id']: [e['path'] for e in r['evidence']] for r in p20['rows']}
src = {r['id']: r['sourceField'] for r in p20['rows']}
TCB13 = p20['tcbDependents']

D = 'PROPOSED-REPLACEMENT-REVIEWABLE-AS-DESIGN-NOT-GRADED'
H = 'HISTORICAL-MEASURED-ESCAPE-PRESERVED-NOT-REPAIRED-NOT-GRADED'
rows = {}


def r(rid, current, limits, inherited=True, disposition=D, extra=None):
    rows[rid] = {
        'disposition': disposition,
        'currentStatusOn31': current,
        'owningSelectors': own[rid] + ([src[rid]] if src.get(rid) else []),
        'evidenceResolvesAgainstFrozen31': True,
        'reviewStatus': 'PENDING',
        'independentGradeAwardedHere': None,
        'limits': limits,
        'sharedAssumption': 'TCB-SCOPE-01' if rid in TCB13 else None,
        'readingStanding': ('inherited from my v27 reading of the same bytes, re-verified byte-equal '
                            'this session' if inherited else 'read afresh this session'),
        'appliedByThisReview': False,
        'finalApplicationOutcomeGranted': False}
    if extra:
        rows[rid].update(extra)


r('RES-EP13-01',
  'Unchanged on 31. The proposed replacement is the product plan/derivation DAG schema with '
  'recomputed source/Plan joins, which exists as published law in identity-and-evidence and the '
  'composition contract; the defective historical EP6/C-2 join is preserved as history, not repaired.',
  'The historical EP6 join is not executable here: its bytes are not members of frozen31.')
r('RES-EP13-02',
  'Unchanged on 31. admission-and-qualification.md (sha 69cd6ba3..., not in my 27->31 delta) states '
  'the authenticated first-party TCB with inert typed inputs, so the account is faithful to its '
  'cited bytes.',
  'A trust-boundary replacement, as the row itself says; the historical attack class is not '
  'eliminated. I claim no same-process hostile-code containment, no qualified provider isolation and '
  'no measured compiler, OS or crypto enforcement.')
r('RES-EP13-03',
  'Unchanged on 31. The seven-vector census stays a finite historical measurement and conformance is '
  'routed to independent source/semantic cases.',
  'No independent conformance corpus exists yet; the replacement is specified, not demonstrated.')
r('RES-EP13-04',
  'Unchanged on 31. No identifier tripwire carries product authority; closed schemas plus '
  'authenticated selected code replace it. I executed closed-selector refusals on 31 at the '
  'internal-root boundary, which is an instance of that mechanism working.',
  'Shares TCB-SCOPE-01. The attempted same-process containment is abandoned, not achieved by other '
  'means.')
r('RES-EP13-05',
  'Unchanged on 31, and this review is again an instance of the correction: my pins came from the '
  'frozen manifest, I verified all 12895 rows before use, and no checker self-scan was treated as '
  'authentication.',
  'Applies to review method, not product runtime. The manifest I trust is supplied to me; I verified '
  'its internal consistency and its declared ancestry, not its provenance.')
r('RES-EP13-06',
  'Unchanged on 31. foundation/canonical.py is cited and is not in my delta; product canonical '
  'admission rejects float/exponent/negative-zero and distinguishes bool from int.',
  'Measured and not repaired remains the row\'s own label. I did not re-execute the historical encoder.')
r('RES-EP13-07',
  'Unchanged on 31. The seal binds Plan, execution plan, evidence, evaluator, policy, proof and '
  'verdict. I executed the current analogue: three false-result controls structurally admit and then '
  'fail complete proof replay with EVALUATOR_COMPLETE_PROOF_REPLAY.',
  'My replay evidence is over author-constructed synthetic Runs, not over the historical EP artifacts.')
r('RES-EP13-08',
  'Unchanged on 31. The fourteen-intent family is retained as bounded history; universality is routed '
  'to schemas, joins and implementation conformance.',
  'No product proof over all PlanIntents exists and none is claimed.')
r('RES-EP13-09',
  'Unchanged on 31. Provenance stays distinct from correctness, with independent oracle comparison '
  'and real native measurement reserved for qualification.',
  'Those obligations are named, not demonstrated.')
r('RES-EP13-10',
  'Unchanged on 31. Candidate self-counters decide nothing; exact schema typing precedes evaluation.',
  'The historical battery is not re-run here.')
r('RES-EP13-11',
  'Unchanged on 31. Historical checker failures stay recorded by cause, and the row retracts a '
  'previous wrong attribution (RET-EP13-06) rather than tidying it away, which is the strongest '
  'evidence in the row.',
  'I did not execute either historical checker and their bytes are not members of frozen31. I make no '
  'claim about tool availability: measured in this session, rg IS present and invocable, so my v27 '
  'statement that it was absent from this host was wrong and is withdrawn.',
  extra={'v27StatementWithdrawn': ('v27 said one checker "needs an rg binary that is not on this host '
                                   'either". Measured now: rg 15.2.0 resolves on PATH and runs. The '
                                   'unmeasured environment claim is withdrawn; the '
                                   'historical-nonexecution limit stands.')})
r('RES-EP13-12',
  'Unchanged on 31. No sole Python answer-provenance guard carries product authority, and the row '
  'explicitly adds that correctness still needs qualification rather than banking the removal as a gain.',
  'Shares TCB-SCOPE-01. The nine named historical variants remain escapes against the historical system.')
r('RES-EP13-13',
  'Unchanged in substance on 31. check-replay.v3.py DID change at 27->28 for the ruleResults work, '
  'and the row\'s sourceBytesChanged=false is scoped to its own predecessor baseline where '
  'previousSha256 equals the current sha; its cited sha matches frozen31 exactly.',
  'Shares TCB-SCOPE-01: "fixture isolation only, no process isolation against hostile Python" is the '
  'TCB move restated. Fixture isolation is not process isolation.',
  extra={'changeClaimScopeNote': ('My 27->31 baseline flags this row as the one change-claim '
                                  'disagreement. On inspection it is a baseline difference, not an '
                                  'error: previousSha256 == sha256 == 8405862f..., stable since v28.')})
r('RES-EP13-14',
  'Unchanged on 31. The differential census is not used as an equivalence proof or a release oracle.',
  'The replacement obligations are specified and unperformed.')
r('RES-EP13-15',
  'Unchanged on 31. The row declines to re-pin onto check-c2-v5.py to escape a blocking adjudication '
  'and records that v5 admits 13 of 66 integer leaves behind a green banner.',
  'The adjudication is not closed here, and the historical v4/v5 bytes are not members of frozen31.')
r('RES-EP13-16',
  'Unchanged on 31. No observed-window guarantee is retained and producer-supplied flags cannot bypass '
  'independent replay. That last clause is testable and my replay supports it: the controls carry '
  'claimed verdicts and are refused because the owner recomputes rather than trusting them.',
  'Shares TCB-SCOPE-01. Replay independence is demonstrated over synthetic author Runs only.')
r('RES-EP13-17',
  'Unchanged on 31. Text-only disclosures stay text-only and meaning is assigned to substantive design '
  'review; this review is that discharge for the design layer.',
  'No padding or anchor counter establishes architectural completeness, and I do not treat my own '
  'reading counts as establishing it.')
r('RES-EP13-18',
  'Unchanged on 31. No hidden-window mechanism is retained, so ledger-entry-count discrimination is '
  'not claimed as a containment boundary.',
  'Shares TCB-SCOPE-01. The row states the attack remains valid against the historical system rather '
  'than repaired, which is the honest form.')
r('RES-EP13-19',
  'Unchanged on 31. The row concedes that load-bearing anchors cannot stop contradictory padding, '
  'because binding is not meaning, and requires independent semantic review. My own receipts are '
  'recorded as receipts, never as the assessment.',
  'This row\'s discharge depends on a reader being honest, which no mechanism in the subject can '
  'guarantee.')
r('IR-EP13-NB-01',
  'Unchanged on 31. The correction generalises to the capability class rather than to variant names, '
  'which is right precisely because enumerating names was the defect RES-EP13-04 records.',
  'Shares TCB-SCOPE-01. The stronger gate/preimage substitution is covered by exclusion, not by a control.')
r('IR-EP13-NB-02',
  'Unchanged on 31. The scan is retired as a scope decider and semantic reading of the complete '
  'contract is required.',
  'NOT a TCB-SCOPE-01 dependent. I re-read the row on current bytes: its disposition - a grep is not '
  'a structural guarantee - holds wherever the trust boundary is drawn.')
r('IR-EP13-NB-03',
  'Unchanged on 31. No unreachability claim is made; product code is authenticated TCB and providers '
  'communicate through sealed protocol data.',
  'Shares TCB-SCOPE-01. The real provider boundary is deferred to implementation and is unqualified; '
  'I make no qualified-provider-isolation claim.')
r('IR-EP13-NB-04',
  'Unchanged on 31. One explicit TCB/scope account is used and historical variant counts are not '
  'treated as a security claim.',
  'Shares TCB-SCOPE-01. The stale nonClaims/guardInventory prose is still present as history and a '
  'reader could still mistake it for current; only the routing is fixed.')
r('IR-EP13-NB-05',
  'Unchanged on 31. Message granularity is classified as an operability acceptance case rather than '
  'proof validity - the same distinction that makes the internal-root diagnostic worth having, since '
  'a misattributed fault code is exactly an operability defect.',
  'Operability cases are acceptance obligations this design review does not perform.')
r('IR-EP13-NB-06',
  'Unchanged on 31. The parity rule is preserved as history and not imported as a product isolation '
  'guarantee.',
  'NOT a TCB-SCOPE-01 dependent on my reading: a parity rule imposing cost without closing a class is '
  'independent of where the trust boundary sits.')
r('IR-EP13-NB-07',
  'Strengthened on 31 rather than changed. The row requires preserved environment and measurements '
  'with new reports naming their own pins. The package keeps source25/26/27/28/30 preparation dirs '
  'intact beside current artifacts, and the two cited historical artifacts are now frozen members, '
  'which removes the custody gap that weakened this row in the predecessor review.',
  'Corroborated in form. "Preserved unchanged" remains an author account for periods before my first '
  'verification.')
for v, note in (
    ('AX6', 'stack-walking witness forgery'),
    ('AX9', 'obfuscated witness forgery, which defeats identifier scans'),
    ('MD5', 'observed-window discrimination by ledger-entry count'),
    ('RX2c', 'unenumerated witness forgery, standing for the open remainder')):
    r(v,
      'Historical measured escape (%s), now readable in the subject: the cited original is a frozen31 '
      'member and declares this variant in escapedEveryGuard and declaredBlindSpotVariants, with '
      'escapeSetIsAMeasurementNotACoverageClaim and aNarrowingIsNotAClosure both true. The residual '
      'account is a faithful restatement of that original.' % note,
      'Shares TCB-SCOPE-01. The row still carries no inline original of its own; the evidence now '
      'comes from the cited artifact. Reading it restores evidence and repairs, regrades, reruns and '
      'authenticates nothing.',
      inherited=False, disposition=H)

assert len(rows) == 30, len(rows)
out = {'evaluationResidualDispositions': rows}
out['evaluationResidualStanding'] = {
    'keyedByExactSourceIds': True,
    'source': 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json',
    'sourceSha256': p20['proposalSha256'],
    'sourceUnchangedSince27': not p20['proposalChangedSince27'],
    'authorAssessmentSha256': p20['authorAssessmentSha256'],
    'authorAssessmentBindsFrozen31': p20['authorBindsFrozen31Manifest'],
    'rowCount': 30, 'noneClosedByThisReview': True, 'gradedFromAuthorSelfAssessment': False,
    'bindingChecksIRan': {
        'idsIdenticalToSource31': p20['idsIdentical'],
        'selectorMismatches': p20['selectorMismatches'],
        'correctionTextMismatches': p20['correctionMismatches'],
        'evidencePathsNotInFrozen31': p20['evidenceNotInFrozen31'],
        'evidenceShaMismatches': p20['evidenceShaMismatches'],
        'rowsNotPending': p20['rowsNotPending'], 'rowsClaimingApplied': p20['rowsApplied'],
        'citedDocuments': p20['citedDocuments'],
        'changeClaimBaselineNote': ('One row (RES-EP13-13) reports sourceBytesChanged=false for a file '
                                    'my 27->31 delta shows changing at 27->28. Its previousSha256 '
                                    'equals its current sha, so the claim is scoped to the package\'s '
                                    'own predecessor baseline and is correct in that frame.')},
    'authorSelfAssessmentUniformity': ('All 30 rows again carry the identical verdict '
                                       'proposed-account-supported-with-stated-limits. That is '
                                       'informational only and is not corroboration; F-14 asked for no '
                                       'forced change and I do not demand one.')}
out['sharedAssumptionTCBSCOPE01'] = {
    'id': 'TCB-SCOPE-01',
    'assessedOnceAsOneAssumption': True,
    'assumption': p20['sharedReviewDependencies'][0]['assumption'],
    'consequence': p20['sharedReviewDependencies'][0]['consequence'],
    'dependentRowCount': 13, 'dependentRows': TCB13,
    'myIndependentVerification': (
        'I re-decided the set on current bytes by reading each row\'s reasoning rather than adopting '
        'the declared list or a keyword match. RES-EP13-13 belongs in it, because "fixture isolation '
        'only, no process isolation against hostile Python" is the TCB move restated. IR-EP13-NB-02 '
        'and IR-EP13-NB-06 do not, because their dispositions hold wherever the boundary is drawn. No '
        'non-declared row rests on the move. The declared 13 is exactly right.'),
    'myDesignAssessment': (
        'As design the assumption is coherent, disclosed and consistently applied, and '
        'admission-and-qualification.md states it explicitly instead of leaving it implicit. I do not '
        'grade it. Rejecting or changing this one assumption reopens all thirteen accounts TOGETHER; '
        'it would never be thirteen independent successes, and it would neither repair the historical '
        'attacks nor establish containment.'),
    'adjudicationOwner': 'the separate final application review, which must adjudicate it once, explicitly'}
json.dump(out, open(os.path.join(BASE, 'part2.json'), 'w'), indent=1)
print('rows:', len(rows), '| TCB dependents:', sum(1 for v in rows.values() if v['sharedAssumption']))
