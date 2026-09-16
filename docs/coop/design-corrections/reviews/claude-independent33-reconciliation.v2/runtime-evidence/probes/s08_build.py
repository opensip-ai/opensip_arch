"""S08 — build the COMPLETE corrected review.json for reconciliation v2.

Four root items plus one defect of my own finding. Writes only into this runtime; frozen33, package10,
the v33 report and the v1 report are read-only inputs.
"""
import hashlib, json, os

V1 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v10'
BASE = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
REC = os.path.join(BASE, 'receipts')

s00 = json.load(open(os.path.join(REC, 's00-verify.json')))
s02 = json.load(open(os.path.join(REC, 's02-inputs.json')))
s04 = json.load(open(os.path.join(REC, 's04-compdiff.json')))
s05 = json.load(open(os.path.join(REC, 's05-nativediff.json')))
s06 = json.load(open(os.path.join(REC, 's06-census.json')))
s07 = json.load(open(os.path.join(REC, 's07-widerscan.json')))
R = json.load(open(os.path.join(V1, 'review.json')))
p01 = json.load(open(os.path.join(V33, 'receipts', 'p01-delta.json')))
p12 = json.load(open(os.path.join(V33, 'receipts', 'p12-package10.json')))
p13 = json.load(open(os.path.join(V33, 'receipts', 'p13-queries.json')))
DELTA = set([c['path'] for c in p01['changed']] + [a['path'] for a in p01['added']])
assert len(DELTA) == 18
LEDGER = []

NATSEC = s05['changedSections'][0]
COMPSEC = s04['changedSections'][0]
assert len(s05['changedSections']) == 1 and len(s04['changedSections']) == 1
NAT_DELETIONS = len([l for k in s05['changedSectionDiffs']
                     for l in s05['changedSectionDiffs'][k]
                     if l.startswith('-') and not l.startswith('---')])
NATIVE_SCOPE = (
    'docs/v2/contracts/product-v1/native-evidence.md IS in my 18-file delta. I measured its change at '
    'section level against frozen32, read-only on both sides: 61 sections on each side, none added and '
    'none removed, and EXACTLY ONE changed — "%s" — with %d deleted lines, i.e. a pure addition. '
    'The added paragraph states where an answered native `unknown` Coverage is accounted for: it stays '
    'in the view its stage returned, in the stage capture and in selectedRefs, while its '
    'nativeCoverageAccount names NO coverageIds; the account-level disclosure is the unsupported-typed '
    'applicability plus the pair on the derived account; a REQUIRED such cell holds the Run at '
    'indeterminate through the required-execution bridge; an execution outcome of `complete` means that '
    'cell\'s execution account was ANSWERED, never that the capability became supported; and it points '
    'at execution-inputs-contract.v1.md §5 and enumeration-contract.v1.md §1.' % (NATSEC, NAT_DELETIONS))
COMP_SCOPE = (
    'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md IS in my 18-file '
    'delta. Measured at section level against frozen32, read-only on both sides: 19 sections on each '
    'side, none added and none removed, and EXACTLY ONE changed — "%s" — which corrects the '
    'required-execution bridge table (each Coverage record\'s OWN pair; null/null kept and bridged; '
    'empty returned partitions no longer carrying provider-unavailable) and records on the contract\'s '
    'own face that the old table had prescribed the fallback execution-inputs §4/§5 forbade.' % COMPSEC)

# ---------------------------------------------------------------- R33-REC2-01
FIX = {
    ('arDispositions', 'AR-13'): (
        'OWNER CHANGED; THIS ROW\'S LAW UNCHANGED. ' + NATIVE_SCOPE + ' This row is about TS/JS/Rust '
        'native cells, monorepos and output handling: those sections are among the 60 byte-identical '
        'ones, and the added paragraph creates no language-cell, monorepo or output-handling '
        'obligation — it constrains how an answered but UNSUPPORTED capability request is disclosed and '
        'accounted for. CURRENT IMPLICATION: the row\'s account holds on 33 unchanged in substance, and '
        'check_native_evidence.v2.py exits 0 on frozen33 in my source33 run. The prior substantive '
        'reasoning is inherited for the byte-identical sections; the changed section was read here and '
        'found not to bear on this subject.'),
    ('fwDispositions', 'FW-01'): (
        'OWNER CHANGED; THIS ROW\'S LAW UNCHANGED. ' + NATIVE_SCOPE + ' This row is about zero-config '
        'operation and recommendation: the added paragraph introduces no default, no recommendation and '
        'no configuration surface, and the sections that carry them are byte-identical. CURRENT '
        'IMPLICATION: zero-config/recommend is unchanged in substance on 33; nothing in the changed '
        'section alters what a caller must configure or what the product recommends.'),
    ('fwDispositions', 'FW-02'): (
        'OWNER CHANGED; THIS ROW\'S LAW UNCHANGED. ' + NATIVE_SCOPE + ' This row is about clones: the '
        'added paragraph adds no clone-detection obligation, no new capability and no new cell, and the '
        'clone sections are byte-identical. CURRENT IMPLICATION: unchanged in substance on 33. If a '
        'clones capability is matrix-unsupported for a language, the added paragraph is what now says '
        'how that is disclosed and accounted for — which is a disclosure rule, not a change to clone '
        'semantics.'),
    ('fwDispositions', 'FW-04'): (
        'OWNER CHANGED; THIS ROW\'S LAW UNCHANGED, AND MILDLY REINFORCED. ' + NATIVE_SCOPE + ' This row '
        'is about richer evidence. The added paragraph is evidence-RETAINING: it states that the '
        'answered `unknown` Coverage remains real retained evidence in its returned view, the stage '
        'capture and selectedRefs even though the account names no coverageIds. CURRENT IMPLICATION: '
        'the richer-evidence account is unchanged and the retention it depends on is now stated '
        'explicitly in the native chapter rather than only in execution-inputs. No new obligation and '
        'no weakening.'),
    ('inheritedResidualDispositions', 'DR-011-R03'): (
        'OWNER CHANGED; THIS ROW\'S LAW UNCHANGED. ' + COMP_SCOPE + ' This row is C-2: plan2/exec-plan2 '
        'with the closed stage-spec record and the operation-token ownership statement. Those sections '
        'are among the 18 byte-identical ones. §9.6 changes only how required-execution deficiencies '
        'project into proof causes; it adds no stage-spec field, no operation token and no new owner. '
        'CURRENT IMPLICATION: unchanged in substance on 33, and the defective historical join remains '
        'preserved history rather than repaired.'),
    ('inheritedResidualDispositions', 'DR-011-R05'): (
        'OWNER CHANGED; THIS ROW\'S LAW UNCHANGED. ' + NATIVE_SCOPE + ' This row is Rust PC-7: protocol '
        'major 3 with identity negotiation and reject-before-disclosure ordering. The published table '
        'owner native/protocol3-transitions.v1.json is NOT in my 18-file delta, and the one changed '
        'native section adds no phase, no negotiation step and no disclosure-ordering rule. CURRENT '
        'IMPLICATION: PC-7 is unchanged on 33; the direct reading of the published transition table I '
        'completed in the source33 pass is inherited here on byte-verified unchanged bytes.'),
    ('inheritedResidualDispositions', 'DR-011-R08'): (
        'OWNER CHANGED; THIS ROW\'S LAW UNCHANGED; THE OBLIGATION STAYS OPEN. ' + NATIVE_SCOPE +
        ' This row is D9: closed host-owned termination with its observation-to-faultCause mapping. The '
        'OWNING contract evaluator-fault-contract.v3.md is NOT in my 18-file delta, and the one changed '
        'native section adds no fault route, no condition and no termination branch. CURRENT '
        'IMPLICATION: D9 branch/cause/result behaviour is unchanged on 33, and the published D9 '
        'successor carrying host-invariant remains an ASSIGNED implementation obligation — carried '
        'forward, not closed by this review and not closed by the native chapter edit.'),
    ('fwDispositions', 'FW-10'): (
        'CORRECTED HERE ON MY OWN FINDING — the previous text named only the unchanged owners. Five of '
        'this row\'s six owners are byte-identical 32->33: repair_closed_world_selection.v1.py, both '
        'repair schemas, workflows-and-surfaces.md and security-and-lifecycle.md. The SIXTH, '
        'native-evidence.md, IS in my 18-file delta and my previous current text did not say so. ' +
        NATIVE_SCOPE + ' The changed section adds no repair obligation, no descriptor and no '
        'snapshot/preimage join. CURRENT IMPLICATION: repair evidence is unchanged on 33 — the published '
        'selection law, the named reference owner and both schema annotations are byte-identical — and '
        'the A-9 admitted-versus-unit limitations are retained exactly. No repair is applied anywhere.'),
}
HIST_CLAUSE = (' [HISTORY: the source32 reasoning for this row is preserved verbatim in %s and is not '
               'offered as current evidence.]')

# ---------------------------------------------------------------- R33-REC2-04
idev = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
IDEV_UNCHANGED = idev not in DELTA
pkgrows = s02['packageResidualRows']


def idev_bytes_equal(rid):
    for e in pkgrows.get(rid, {}).get('evidence', []):
        if e.get('path') == idev:
            return e.get('sha256') == e.get('previousSha256'), e.get('sha256')
    return None, None


RESFIX = {}
for rid, body in (
    ('RES-EP13-01',
     'CURRENT IMPLICATION OF THE COMPOSITION DELTA FOR THIS ROW: none. This row is the replacement of '
     'the defective transitive C-2 join by the explicit product plan/derivation DAG schema with '
     'recomputed source/Plan joins. The composition change is confined to §9.6, and none of this row\'s '
     'subject terms (derivation DAG, plan2/exec-plan2, the transitive C-2 join) occurs anywhere in the '
     'added text. The row\'s other owner, identity-and-evidence.md, is byte-unchanged 32->33. So the '
     'published replacement law and the historical-defect boundary stand exactly as assessed, and the '
     'defective EP6/8 chain remains history that final application must not mark repaired. The row '
     'stays PROPOSED-REPLACEMENT-REVIEWABLE-AS-DESIGN-NOT-GRADED: package10 carries the author '
     'assessment proposed-account-supported-with-stated-limits with independentGrade PENDING, and I '
     'award no grade here.'),
    ('RES-EP13-07',
     'CURRENT IMPLICATION OF THE COMPOSITION DELTA FOR THIS ROW: adjacent and tightening, not '
     'loosening. This row is the product seal binding Plan, execution plan, evidence, evaluator, '
     'policy, proof and verdict, with wrong-Plan and rehashed false-proof cases refusing. The one '
     'changed section, §9.6, is precisely the projection of required-execution deficiencies INTO proof, '
     'and it now requires each Coverage record\'s own pair, keeps null/null rather than manufacturing a '
     'carrier, and forbids the provider-unavailable fallback — so what reaches proof for a required '
     'cell is more tightly specified than on 32, which cannot weaken a seal that binds proof. The '
     'row\'s supporting controls are the three false-result cases in semantic-controls1, which is one '
     'of the THREE groups newly constructed on source33, and I replayed them in my package10 '
     'verification: each structurally ADMITS and then REFUSES complete proof replay, as the row '
     'requires. That evidence is current-on-33 and re-measured, not inherited. Still PENDING and '
     'ungraded here; the claim remains about registered selected semantic inputs, not arbitrary store '
     'content.'),
    ('RES-EP13-15',
     'CURRENT IMPLICATION OF THE COMPOSITION DELTA FOR THIS ROW: none, and the blocking adjudication is '
     'not cleared. This row declines to re-pin onto check-c2-v5.py to escape a blocking adjudication '
     'and declines to elevate the old C-2 v4 self-census. The composition change is confined to §9.6 '
     'and none of this row\'s subject terms (self-census, check-c2-v5, v4, adjudication) occurs in the '
     'added text; §9.6 adds no pin, no census route and no adjudication path. So on 33 the proposed '
     'replacement continues to rest on the current plan/DAG/proof contracts rather than on C-2 v4, and '
     'the adjudication stays open. Not closed here, not graded here; final application must inspect the '
     'current replacement semantics.'),
):
    eq, digest = idev_bytes_equal(rid)
    RESFIX[rid] = body + (
        ' Owner bytes: evaluator-composition-contract.v3.md changed and was re-read this session; '
        'identity-and-evidence.md is byte-unchanged 32->33 (not in my 18-file delta%s) and resolves in '
        'frozen33.' % ('' if eq is None else
                       (', and package10 records the same sha256 %s before and after' % (digest or '')[:12])
                       if eq else ', though package10 records differing before/after digests'))

# ---------------------------------------------------------------- apply row edits
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': ('currentBasisOn33', 'priorBasisOn32')}
INHERIT = (' [INHERITED: this row\'s owner bytes are verified unchanged 32->33 and all owner paths '
           'resolve in frozen33, so the prior substantive reasoning preserved verbatim in %s is '
           'expressly ADOPTED AS CURRENT for this row on that byte verification. It is inherited '
           'evidence, explicitly not a fresh independent re-derivation.]')
audit = {'rowsRewrittenSubstantively': [], 'rowsGivenExplicitInheritance': 0,
         'rowsKeepingHistoryClause': 0, 'rowsUntouched': 0}
for mp in MAPS:
    fld, pf = FIELD.get(mp, ('currentStatusOn33', 'priorStatusOn32'))
    for rid, row in R[mp].items():
        key = mp + '/' + rid
        ch = row.get('ownerFilesChangedIn32to33')
        if ch is None:
            ch = row.get('ownerSelectorsChangedIn32to33')
        cur = str(row.get(fld) or '')
        new = FIX.get((mp, rid)) or RESFIX.get(rid)
        if new:
            row[fld] = new + (HIST_CLAUSE % pf)
            row['currentFieldStandingOn33'] = (
                'States current source33 truth for a row whose owner bytes CHANGED: the change is '
                'scoped by my own section-level measurement and the current implication is stated. The '
                'source32 reasoning stays verbatim in %s as history.' % pf)
            row['ownerChangeScopeMeasuredOn33'] = {
                'changedOwners': ch,
                'method': 'read-only section-level comparison of the changed owner between frozen32 and frozen33',
                'changedSections': ([COMPSEC] if any('composition' in c for c in (ch or [])) else [NATSEC]),
                'sectionsAddedOrRemoved': 0,
                'receipt': ('receipts/s04-compdiff.json' if any('composition' in c for c in (ch or []))
                            else 'receipts/s05-nativediff.json')}
            audit['rowsRewrittenSubstantively'].append(key)
        elif ch == [] and row.get('ownerPathsResolveInFrozen33') is True or \
                (ch == [] and row.get('ownerSelectorsResolveInFrozen33') is True):
            if '[HISTORY:' in cur:
                row[fld] = cur.replace(HIST_CLAUSE % pf, INHERIT % pf)
                row['currentFieldStandingOn33'] = (
                    'Owner bytes verified unchanged 32->33 and resolving in frozen33. The prior '
                    'substantive reasoning in %s is expressly adopted as current for this row on that '
                    'byte verification — inherited evidence, not a fresh re-derivation.' % pf)
                audit['rowsGivenExplicitInheritance'] += 1
            else:
                audit['rowsUntouched'] += 1
        else:
            audit['rowsKeepingHistoryClause'] += 1
R['currentFieldAuditV2'] = audit

LEDGER.append({
    'id': 'R33-REC2-01', 'disposition': 'ACCEPTED AND CORRECTED — AND ONE MORE ROW FOUND',
    'rootIsCorrect': True,
    'evidence': ('I re-derived the contradiction set myself instead of taking the list: scanning all 107 '
                 'rows for a current text that denies a delta touch while the row\'s OWN '
                 'changed-owner array is non-empty returns exactly root\'s seven for the phrase they '
                 'quoted. Widening the phrasing to any denial across all 21 changed-owner rows returns '
                 'NINE: root\'s seven, plus FW-10, plus DR-007. FW-10 is a genuine eighth defect — it '
                 'named only the five unchanged owners and silently omitted native-evidence.md, which '
                 'is in its own changed array. DR-007 is a FALSE POSITIVE: its text already says "the '
                 'owning fault contract is not in my 32->33 delta; the native chapter is", which is '
                 'correct and complete, so I left it alone.'),
    'howFixed': ('each of the eight now states, from my own read-only section-level measurement of the '
                 'changed owner against frozen32: that the owner changed, what exactly changed (one '
                 'section on each side, none added or removed), why this row\'s specific law is '
                 'nonetheless unchanged, and the CURRENT implication. Unique prior reasoning is not '
                 'replaced by a generic prefix and is not claimed as fresh review: where it carries '
                 'forward it is marked inherited on byte verification.'),
    'measuredScope': {'nativeEvidenceMd': {'sections32': s05['sections32'], 'sections33': s05['sections33'],
                                           'added': s05['addedSections'], 'removed': s05['removedSections'],
                                           'changed': s05['changedSections'], 'deletedLines': NAT_DELETIONS},
                      'compositionContractV3': {'sections32': s04['sections32'], 'sections33': s04['sections33'],
                                                'added': s04['addedSections'], 'removed': s04['removedSections'],
                                                'changed': s04['changedSections']}},
    'affectedSelectors': ['$.arDispositions.AR-13.currentStatusOn33',
                          '$.fwDispositions.FW-01.currentStatusOn33',
                          '$.fwDispositions.FW-02.currentStatusOn33',
                          '$.fwDispositions.FW-04.currentStatusOn33',
                          '$.fwDispositions.FW-10.currentStatusOn33',
                          '$.inheritedResidualDispositions.DR-011-R03.currentStatusOn33',
                          '$.inheritedResidualDispositions.DR-011-R05.currentStatusOn33',
                          '$.inheritedResidualDispositions.DR-011-R08.currentStatusOn33',
                          '$.*.*.ownerChangeScopeMeasuredOn33',
                          '$.*.*.currentFieldStandingOn33']})

# ---------------------------------------------------------------- R33-REC2-02
old_ap = R['evidenceReceipts']['authorPackage']
R['evidenceReceipts']['authorPackage'] = {
    'status': 'COMPLETE — INDEPENDENTLY VERIFIED ON SOURCE33 (package10)',
    'currentMeasurement': {
        'receipts': ['claude-independent-design.v33/receipts/p12-package10.json',
                     'claude-independent-design.v33/receipts/p13-queries.json'],
        'artifactManifestSha256': p12['artifactManifestSha256'],
        'matchesRootNamedManifest': p12['matchesRootNamedManifest'],
        'members': '%d/%d verified, %d mismatched, %d missing' % (
            p12['verified'], p12['declaredMembers'], p12['mismatched'], p12['missing']),
        'sourceManifestEqualsFrozen33': p12['sourceManifestEqualsFrozen33'],
        'rootInputSha256': R['authorPackageReview']['rootInputConsumed']['readyVersionSha256'],
        'rootInputStatus': R['authorPackageReview']['rootInputConsumed']['status'],
        'verifierReturncode': p13['returncode'],
        'sourceFilesVerified': p13['verification']['sourceFilesVerified'],
        'packageFilesVerified': p13['verification']['packageFilesVerified'],
        'thirteenCasesAsExpected': R['authorPackageReview']['myVerification']['allThirteenAsExpected'],
        'queryChecks': R['authorPackageReview']['myVerification']['queryChecks']},
    'historicalP11': {
        'standing': 'HISTORICAL — superseded during the source33 review; retained, not deleted',
        'status': old_ap.get('status'),
        'rootInputSha256': old_ap.get('rootInputSha256'),
        'why': ('p11 ran while the root-owned author-package-update.json was still PENDING and named no '
                'package10 manifest. The input then transitioned to READY_FOR_INDEPENDENT_REVIEW and '
                'p12/p13 are the measurement of the package that actually exists on source33.'),
        'receipt': 'claude-independent-design.v33/receipts/p11-package.json'},
    'correctionR33REC2_02': (
        'The CURRENT evidence pointer read INCOMPLETE with the PENDING root-input digest while '
        'authorPackageReview.status correctly read COMPLETE — the two disagreed inside one record. The '
        'current pointer now binds the actual package10 measurement; p11 is kept and labelled '
        'historical.')}
LEDGER.append({
    'id': 'R33-REC2-02', 'disposition': 'ACCEPTED AND CORRECTED', 'rootIsCorrect': True,
    'evidence': ('measured in my own v1 record: evidenceReceipts.authorPackage was {"status": '
                 '"INCOMPLETE", "rootInputSha256": "5ac4a3ec…"} — the PENDING input digest — while '
                 'authorPackageReview.status read "COMPLETE — INDEPENDENTLY VERIFIED ON SOURCE33" and '
                 'p12/p13 recorded 305/305 members, manifest 88c38b16…, source-manifest equal to '
                 'frozen33, rc 0 and 7/7 queries. A single record cannot hold both as current.'),
    'affectedSelectors': ['$.evidenceReceipts.authorPackage',
                          '$.evidenceReceipts.authorPackage.currentMeasurement',
                          '$.evidenceReceipts.authorPackage.historicalP11']})

# ---------------------------------------------------------------- R33-REC2-03
EL = R['sourceChangeAssessment']['executionInputsLaw']
EL['requiredCellBridgeAndUniqueness']['exactCauseRule'] = (
    'Composition §9.6 step 3, implemented by bridge_cause in check-execution-inputs.v1.py:714-721 '
    'against identity-schemas.v3.json#/x-opensip-evaluator-deficiency-registry/sources/execution '
    '(11 registered execution deficiencies): if the requiredCellDeficiencies row\'s own `deficiency` is '
    'REGISTERED, the proof cause IS that deficiency, carried through unchanged; the cause is '
    '`required-cell-unsatisfied` ONLY when that deficiency is null — the (null, null) derived carrier '
    'for pure missing work — or `source-syntax-invalid`; anything else bridges to UNREGISTERED and '
    'fails. So the ROW and the CAUSE are different things: a required cell always owes the row, while '
    'the cause it projects depends on whether the row carries a registered typed deficiency.')
EL['requiredCellBridgeAndUniqueness']['measuredCauseSplit'] = {
    'matrixTypedRequiredCell': {
        'case': 'full-run-required-unsupported-matrix-pair-bridge',
        'verdict': 'indeterminate',
        'causePair': ['language-tier-unsupported', 'capability-missing'],
        'reading': 'a REQUIRED selected-U matrix-unsupported cell emits its requiredCellDeficiencies '
                   'row AND projects the MATRIX deficiency as the proof cause — not required-cell-unsatisfied'},
    'pureMissingWork': [
        {'case': 'full-run-empty-returned-partitions-bridge-required-cell-unsatisfied',
         'causePair': ['required-cell-unsatisfied', None]},
        {'case': 'full-run-census-missing-subjects-bridge-keeps-originating-coverage',
         'causePair': ['required-cell-unsatisfied', None]}],
    'bothInOneRun': {'case': 'full-run-mixed-accounts-first-typed-pair',
                     'causePairs': [['budget-exhausted', None], ['required-cell-unsatisfied', None]],
                     'reading': 'the typed account projects its own registered deficiency while the '
                                'untyped one falls back — the clearest single demonstration that the '
                                'fallback is conditional, not general'},
    'sourceOfThisSplit': 'my own v1 evidenceReceipts.fullRunRows, re-read here; no control was re-run'}
EL['selectedUnsupportedCoverageRetention']['causeIsTheMatrixPairNotTheFallback'] = (
    'A REQUIRED such cell owes a requiredCellDeficiencies ROW and holds the Run at indeterminate, and '
    'the cause that reaches proof is the MATRIX pair (language-tier-unsupported, capability-missing). '
    'required-cell-unsatisfied is the cause only for an otherwise untyped required source. See '
    'requiredCellBridgeAndUniqueness.exactCauseRule.')
LEDGER.append({
    'id': 'R33-REC2-03', 'disposition': 'ACCEPTED — MD CORRECTED, AND THE EXACT RULE ADDED',
    'rootIsCorrect': True,
    'evidence': ('read at source: bridge_cause (check-execution-inputs.v1.py:714-721) returns the '
                 'deficiency itself when it is in the registered execution set and returns '
                 'required-cell-unsatisfied only for null or source-syntax-invalid; the registry in '
                 'identity-schemas.v3.json lists 11 execution deficiencies including '
                 'language-tier-unsupported and budget-exhausted. The retained control at '
                 'check-execution-inputs.v1.py:1412-1414 expects exactly ["language-tier-unsupported"], '
                 'while lines 1406-1411 expect ["required-cell-unsatisfied"]. My own fullRunRows receipt '
                 'records the matching cause pairs.'),
    'scopeOfTheError': ('the defect was in review.md §1 only. My v1 JSON was already correct: '
                        'requiredCellBridgeAndUniqueness.bridge said "maps a NULL deficiency to proof '
                        'cause required-cell-unsatisfied" and selectedUnsupportedCoverageRetention '
                        'recorded the matrix pair. The MD dropped the null-deficiency precondition and '
                        'so conflated the structural ROW with the cause fallback.'),
    'affectedSelectors': ['review.md §1 "Selected-U unsupported Coverage, and the required bridge"',
                          '$.sourceChangeAssessment.executionInputsLaw.requiredCellBridgeAndUniqueness.exactCauseRule',
                          '$.sourceChangeAssessment.executionInputsLaw.requiredCellBridgeAndUniqueness.measuredCauseSplit',
                          '$.sourceChangeAssessment.executionInputsLaw.selectedUnsupportedCoverageRetention.causeIsTheMatrixPairNotTheFallback']})

LEDGER.append({
    'id': 'R33-REC2-04', 'disposition': 'ACCEPTED AND CORRECTED', 'rootIsCorrect': True,
    'evidence': ('the three rows carried only "Cited owner bytes CHANGED …; re-read this session" plus a '
                 'pointer disclaiming the prior reasoning — an owner-provenance note with no current '
                 'substantive status, which cannot support a carried disposition. Scoped by measurement: '
                 'the composition change is confined to ONE section of 19 (§9.6 required-execution '
                 'bridge), none added or removed; none of RES-EP13-01\'s or RES-EP13-15\'s subject terms '
                 'occurs in the added text, while RES-EP13-07\'s subject (proof content for required '
                 'cells) is exactly what §9.6 tightens. Their other owner identity-and-evidence.md is '
                 'byte-unchanged. RES-EP13-07\'s supporting controls sit in semantic-controls1, one of '
                 'the three groups newly constructed on 33, which I replayed in the package10 '
                 'verification.'),
    'noNewSuites': 'no control or suite was re-run; the section comparison is a read of two frozen files',
    'allThreeRemain': 'PROPOSED-REPLACEMENT-REVIEWABLE-AS-DESIGN-NOT-GRADED, reviewStatus PENDING, '
                      'independentGradeAwardedHere null',
    'affectedSelectors': ['$.evaluationResidualDispositions.RES-EP13-01.currentStatusOn33',
                          '$.evaluationResidualDispositions.RES-EP13-07.currentStatusOn33',
                          '$.evaluationResidualDispositions.RES-EP13-15.currentStatusOn33']})

# ---------------------------------------------------------------- lineage, standing, ledger
R['review'] = ('Independent design review of exact frozen consolidated product source33 — COMPLETE '
               'corrected record, second bounded review-record reconciliation. Supersedes the record of '
               'reconciliation v1; v1 and the source33 report are preserved unchanged.')
R['recordLineage'] = {
    'thisRuntime': 'claude-independent33-reconciliation.v2',
    'supersededRecord': {'path': 'claude-independent33-reconciliation.v1/review.json',
                         'sha256': s00['v1JsonSha256'], 'mdSha256': s00['v1MdSha256'],
                         'standing': 'preserved unchanged on disk; this is a successor record, not a patch'},
    'originalSource33Record': R.get('recordLineage', {}).get('supersededRecord'),
    'subjectUnchanged': ('frozen source33 is IMMUTABLE at 12,899 files, manifest 1cf3db70d4b73b0c42f13'
                         '93331e6a874ee26f7ddf67aa05c6ac15a5753069299. No source34 is requested, '
                         'proposed or implied.'),
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'writesConfinedTo': 'claude-independent33-reconciliation.v2',
    'substantiveVerdictPreserved': ('ACCEPT on source33 is unchanged, and so is every disposition. The '
                                    'REC01/02/03/05 corrections, the F-row provenance work and the '
                                    'layer4 mapping root accepted are carried forward untouched.')}
R['correctionLedgerR33REC2'] = {
    'standing': ('root\'s four items were assessed against the source and my own record, not accepted on '
                 'authority. All four are substantiated. My own wider scan then found one further '
                 'defective row root did not name (FW-10) and one row root\'s pattern would have caught '
                 'that is actually correct (DR-007), which I left alone.'),
    'items': LEDGER, 'itemsAccepted': 4, 'itemsRefuted': 0,
    'additionalDefectFoundByMe': {
        'row': 'fwDispositions/FW-10',
        'defect': ('its current text asserted repair evidence unchanged and named only the repair module '
                   'and the workflows chapter as absent from the delta, silently omitting '
                   'native-evidence.md, which is in the row\'s own changed-owner array'),
        'severity': 'record accuracy; no source defect and no disposition change',
        'fixed': True},
    'rootPatternCheckedAndRejected': {
        'row': 'inheritedResidualDispositions/DR-007',
        'finding': ('matched my widened phrasing scan but is CORRECT as written: it states that the '
                    'owning fault contract is not in the delta and that the native chapter is. No change '
                    'made.')}}
R['reconciliationStanding'] = {
    'scope': 'second bounded review-record correction on immutable source33',
    'newSourceDefectDemonstrated': False,
    'newRecordDefectFoundByMe': 'one — FW-10, fixed here',
    'dispositionsChanged': 0, 'verdictChanged': False,
    'suitesRerun': ('none. The only new reads are two read-only section-level comparisons of the two '
                    'changed owners the affected rows cite, plus re-reads of my own receipts.'),
    'whatThisStillDoesNotDo': ('no source authoring and no source34, no package implementation, no '
                               'product qualification, no recovery-case execution, no TCB-SCOPE-01 '
                               'closure, no residual grading, no blind reconstruction, no activation, '
                               'no commit or push, and no consumer/blind/private material was read'),
    'rootAssentPending': 'root withheld assent pending these four items; this record supplies all four.'}
R['limitations'] = R['limitations'] + [
    'The section-level comparisons behind the eight corrected rows are heading-scoped reads of two files '
    'in frozen32 and frozen33. They establish which sections changed, not a semantic proof that an '
    'unchanged section cannot interact with a changed one; each row states its reasoning so that '
    'inference can be checked.',
    'Inherited rows are marked INHERITED: their prior substantive reasoning is adopted on exact-byte '
    'verification of the owners, and is explicitly not a fresh independent re-derivation on 33.']
out = os.path.join(BASE, 'review.json')
json.dump(R, open(out, 'w'), indent=1, default=str)
print('rows rewritten substantively :', len(audit['rowsRewrittenSubstantively']))
print('  ', audit['rowsRewrittenSubstantively'])
print('rows marked INHERITED        :', audit['rowsGivenExplicitInheritance'])
print('rows keeping HISTORY clause  :', audit['rowsKeepingHistoryClause'])
print('rows untouched               :', audit['rowsUntouched'])
print('ledger items                 :', [i['id'] for i in LEDGER])
print('identity-and-evidence unchanged in delta:', IDEV_UNCHANGED)
print('bytes:', os.path.getsize(out))
print('sha256:', hashlib.sha256(open(out, 'rb').read()).hexdigest())
