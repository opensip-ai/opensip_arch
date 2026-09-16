"""R03 — build the COMPLETE successor review.json in this runtime.

Starts from my own completed v32 review.json (preserved untouched at its original location), applies
the four substantiated RR32 corrections and the two bounded-probe qualifications, recomputes every
owner-path resolution boolean from actual frozen32 membership, and preserves all 107 dispositions,
the verdict, original receipt locations, limits, TCB and pending obligations.
"""
import hashlib, json, os

V32 = '/tmp/opensip-design-corrections/claude-independent-design.v32'
BASE = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1'
REC = os.path.join(BASE, 'receipts')
SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = json.load(open(os.path.join(V32, 'review.json')))
r00 = json.load(open(os.path.join(REC, 'r00-verify.json')))
r01 = json.load(open(os.path.join(REC, 'r01-owners.json')))
r02 = json.load(open(os.path.join(REC, 'r02-readinghistory.json')))

FAULT_V3 = 'docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md'
PROTO3 = 'docs/coop/design-corrections/native/protocol3-transitions.v1.json'
FACTID = 'docs/coop/artifacts/fact-identity-policy.v2.json'
CR = 'docs/coop/design-corrections/foundation/check-replay.v3.py'
for p in (FAULT_V3, PROTO3, FACTID, CR):
    assert p in man, p

R['review'] = ('Independent design review of exact frozen consolidated product source32 — COMPLETE '
               'successor record after a bounded review-record reconciliation. Supersedes the record '
               'of my source32 review; that report is preserved unchanged at its original location.')
R['recordLineage'] = {
    'thisRuntime': 'claude-independent32-reconciliation.v1',
    'supersededRecord': {'path': 'claude-independent-design.v32/review.json',
                         'sha256': r00['myV32ReviewSha256'],
                         'standing': 'preserved unchanged; this is a successor record, not a patch'},
    'subjectUnchanged': ('frozen source32 is UNCHANGED. This is a review-record reconciliation, not a '
                         'new source version and not a fresh origin.'),
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'noSourceEdits': True}
R['subjectManifestSha256'] = r00['manifestSha256']
R['manifestVerification']['manifestSha256MatchesRequiredForThisPass'] = r00['manifestMatchesRequired']
R['manifestVerification']['reconciliationScope'] = (
    'Source32 is unchanged, so the full archive scan, the passing suites and the constructors were '
    'NOT repeated. I re-verified the manifest digest and hash-verified every source file I read in '
    'this pass. All executed evidence below is cited at its ORIGINAL receipt location in the v31/v32 '
    'runtimes and is never relabelled as work done here.')

# ---------------- RR32-01 ----------------
dr7 = R['inheritedResidualDispositions']['DR-007']
old7 = list(dr7['currentOwnerFiles'])
dr7['currentOwnerFiles'] = [p for p in old7 if 'evaluator-fault-contract.v1.md' not in p] + [FAULT_V3]
dr7['ownerFilesChangedIn31to32'] = []
dr7['ownerFilesUnchangedIn31to32'] = list(dr7['currentOwnerFiles'])
dr7['ownerPathsResolveInFrozen32'] = all(p in man for p in dr7['currentOwnerFiles'])
dr7['currentStatusOn32'] = (
    'Exact D9 branch/cause/result behaviour is unchanged on 32. The owning fault contract is '
    'evaluator-fault-contract.v3.md, which I read freshly in this pass: it publishes the closed '
    'condition/public-meaning table, states that an internal refusal is not itself a public D9 code '
    'and that origin is never inferred from a filename or error text, and names the 24 allowed '
    'condition/origin pairs as explicit in the schema registry. Critically it states in its own words '
    'that "the mandatory LIVE D9 successor-artifact obligation is not discharged by this design '
    'reference or by a passing route-control suite". The published D9 successor carrying '
    'host-invariant therefore remains an ASSIGNED implementation obligation, carried forward and not '
    'closed by this review.')
dr7['evidence'] = ('freshly read evaluator-fault-contract.v3.md in this reconciliation pass '
                   '(8,678 bytes, sha 5731b41d…, manifest-verified); inherited suite evidence at '
                   'claude-independent-design.v32/receipts/p06-changedchecks.json')
dr7['readingStanding'] = ('the owning fault contract was READ FRESH in this reconciliation pass; the '
                          'other two owners are inherited from my v32 reading after exact-byte '
                          'verification that they are unchanged in the 31->32 delta')
dr7['recordCorrection'] = ('RR32-01: my v32 row cited '
                           'foundation/evaluator-fault-contract.v1.md, which does not exist in '
                           'frozen32. The actual owner is evaluator-fault-contract.v3.md. The '
                           'DISPOSITION was unaffected — the v3 contract states the D9 successor '
                           'obligation is undischarged, which is exactly what the row said — but the '
                           'citation was wrong and is corrected here.')

# ---------------- RR32-04 + all 16 booleans from actual membership ----------------
FIX = {'DR-011-R02': FACTID, 'DR-011-R04': PROTO3, 'DR-011-R05': PROTO3, 'DR-011-R08': FAULT_V3}
for rid, addpath in FIX.items():
    row = R['inheritedResidualDispositions'][rid]
    if addpath not in row['currentOwnerFiles']:
        row['currentOwnerFiles'] = row['currentOwnerFiles'] + [addpath]
    row['ownerFilesUnchangedIn31to32'] = [p for p in row['currentOwnerFiles']
                                          if p not in set(row['ownerFilesChangedIn31to32'])]
R['inheritedResidualDispositions']['DR-011-R02']['currentStatusOn32'] = (
    'FACT-IDENTITY. The policy is still reused by exact selector rather than restated; the framed '
    'bodyIdentity preimage is unchanged on 32. The retained policy owner is '
    'docs/coop/artifacts/fact-identity-policy.v2.json (40,948 bytes, manifest-verified), which my v32 '
    'row cited under a foundation path that does not exist.')
R['inheritedResidualDispositions']['DR-011-R04']['currentStatusOn32'] = (
    'DELIVERY. Native protocol 3 / TS 2 and the security lifecycle core bridge remain the explicit '
    'successors on 32. The protocol owner is native/protocol3-transitions.v1.json, whose standing is '
    '"NORMATIVE and CLOSED", not the native-protocol.v3.md path my v32 row named, which does not exist.')
R['inheritedResidualDispositions']['DR-011-R05']['currentStatusOn32'] = (
    'Rust PC-7. Protocol major 3 with identity negotiation and reject-before-disclosure ordering is '
    'unchanged on 32. I verified the published table directly this pass: '
    'native/protocol3-transitions.v1.json declares phases=22 and ruleCount=34 with 34 rules, which is '
    'exactly the 22-phase state machine and 34-row transition table this row describes. No real '
    'provider process is exercised.')
R['inheritedResidualDispositions']['DR-011-R08']['currentStatusOn32'] = (
    'D9. Closed host-owned termination with its observation-to-faultCause mapping is unchanged on 32. '
    'The owning contract is evaluator-fault-contract.v3.md, read freshly in this pass; it names the 24 '
    'allowed condition/origin pairs and states that the mandatory LIVE D9 successor-artifact '
    'obligation is NOT discharged by this design reference or by a passing route-control suite. That '
    'successor therefore remains an ASSIGNED implementation obligation, carried forward and not '
    'closed here.')
for rid in FIX:
    R['inheritedResidualDispositions'][rid]['recordCorrection'] = (
        'RR32-04: my v32 build silently dropped a nonexistent owner path from this row while still '
        'computing ownerPathsResolveInFrozen32 against the unfiltered list, so the row lost an '
        'intended owner AND reported false. The real owner is restored above and the boolean is now '
        'derived from actual frozen32 membership.')

# recompute EVERY owner-resolution boolean across all 107 rows, from actual membership
MAPS = ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
        'scopedReviewOwnerDispositions')
audit = {'rowsChecked': 0, 'rowsWithUnresolvedOwner': [], 'booleansRecomputed': {}}
for mp in MAPS:
    for rid, row in R[mp].items():
        audit['rowsChecked'] += 1
        owners = row.get('currentOwnerFiles', [])
        miss = [p for p in owners if p not in man]
        resolved = not miss
        row['ownerPathsResolveInFrozen32'] = resolved
        row['ownerPathsVerifiedAgainstFrozen32Membership'] = True
        if miss:
            audit['rowsWithUnresolvedOwner'].append({'row': mp + '/' + rid, 'missing': miss})
        if rid.startswith('DR-011-R'):
            audit['booleansRecomputed'][rid] = resolved
for rid, row in R['evaluationResidualDispositions'].items():
    audit['rowsChecked'] += 1
    sel = row.get('currentOwnerSelectors', [])
    miss = [p for p in sel if p not in man]
    row['ownerSelectorsResolveInFrozen32'] = not miss
    row['ownerPathsVerifiedAgainstFrozen32Membership'] = True
    if miss:
        audit['rowsWithUnresolvedOwner'].append({'row': 'evaluationResidualDispositions/' + rid,
                                                 'missing': miss})
for rid, row in R['fDispositions'].items():
    audit['rowsChecked'] += 1
R['ownerPathAudit'] = audit

# ---------------- RR32-02 ----------------
f04 = R['fDispositions']['F-04']
f04['limits'] = ('Join controls. The internal-root guard runs at the enumeration join, which comes '
                 'AFTER structural custody: the traced order is open_run_closure -> derive -> '
                 'admit_enumeration -> compare_complete_replay. Join-only controls are adequate for '
                 'their claimed scope and I demand no whole-Run replacements; I do not claim a '
                 'structural-ADMIT-then-semantic-REFUSE construction is impossible.')
f04['recordCorrection'] = ('RR32-02: my v32 F-04 limits still said the boundary "precedes structural '
                           'custody", the inverse wording my own RR31-05 correction had already '
                           'retired elsewhere in the same report. Corrected here and checked across '
                           'the whole document.')

# ---------------- RR32-03 ----------------
res13 = R['evaluationResidualDispositions']['RES-EP13-13']
res13['readingStanding'] = (
    'Current bytes READ FRESH in this reconciliation pass (17,179 bytes, sha 8405862f…, '
    'manifest-verified): the deep-copy fixture isolation this row is about is present throughout. '
    'Reading history, stated truthfully: the FILE last changed in the 27->28 window; my review '
    'lineage is source26, source27, source31, source32 and this reconciliation, with NO source28 '
    'review session. I first reviewed and executed the post-28 bytes in my SOURCE31 review, which '
    'assessed the whole 27->31 delta including the source28 ordering work '
    '(claude-independent-design.v31/receipts/p06-replayorder.json, frozen run rc=0), and executed '
    'them again as a changed-input run in the source32 review '
    '(claude-independent-design.v32/receipts/p06-changedchecks.json, rc=0). I did not re-execute it '
    'in this pass and claim no new execution here.')
res13['recordCorrection'] = (
    'RR32-03: my v32 row said the changed file "was read fresh in that session" about the 27->28 '
    'window. No source28 review session exists in my lineage, so that asserted a session that never '
    'happened. The truthful history is above, and the NORMATIVE LAW the row disposes remains '
    'unchanged and is confirmed in the current bytes.')

# ---------------- bounded probe qualifications ----------------
rl = R['evidenceReceipts'].get('repairLawExecution', {})
R['evidenceReceipts']['repairLawExecution'] = {
    'receiptLocation': 'claude-independent-design.v32/receipts/p05-repairlaw.json',
    'results': rl,
    'scopeQualification': (
        'ACCEPTED root note. p05 is unit-level execution of the published module over hand-built '
        'retained views. In particular the remedy-distinctness case is a pair of hand-built rows with '
        'pseudo coverage identities: it establishes that record_coordinates() emits DISTINCT STRING '
        'COORDINATES for inputs differing in targetUniverse, subjectScopeCommitment and identity. It '
        'does NOT establish two lawfully admitted native records. The ownership, unavailability, '
        'unselected-exclusion, extent-distinctness, absence-folding and gate results are likewise '
        'unit-level over constructed views, not full admitted Runs.'),
    'whatDoesCarryFullRunWeight': (
        'the source\'s own asymmetric control, which is built from a fully admitted Run and which I '
        'did not construct: check-workflow-projection.v3.py rc=0 at '
        'claude-independent-design.v32/receipts/p06-changedchecks.json')}
R['sourceChangeAssessment']['change1_repairClosedWorldSelectionOwner']['cellOrdinalQuestionIRaisedAndResolved'].update({
    'evidenceQualification': (
        'ACCEPTED root note. p12c did NOT admit an actual EnumerationPlan: its lookup into the real '
        'plan schema failed with KeyError \'properties\' and it recorded cellsOrderAnnotation=None. '
        'What p12c established is that the ExactValidator enforces x-opensip-order {by:[...]} on an '
        'ISOLATED minimal schema (declared order admits; shuffled and duplicate refuse). The '
        'conclusion that the retained cells array is held to its published sort is therefore a '
        'BOUNDED INFERENCE from three parts: that generic validator behaviour, the static annotation '
        '$/properties/cells/x-opensip-order {"by":["capabilityId","languageMode","workspaceRoot"]} '
        'which I did read directly in p12, and enumeration-contract section 8 naming the ExactValidator '
        '("4 MiB / typed / order") as the plan validator. It is not an executed admission of a real '
        'enumeration plan.'),
    'outcome': 'NO FINDING, on bounded inference rather than executed plan admission',
    'receiptLocations': ['claude-independent-design.v32/receipts/p12-cellordinal.json',
                         'claude-independent-design.v32/receipts/p12c-cellorder.json']})

# ---------------- corrections block ----------------
R['correctionsToMyOwnV32Record'] = [
    {'id': 'RR32-01', 'rootFinding': 'DR-007 cites a nonexistent evaluator-fault-contract.v1.md',
     'independentlyVerified': True,
     'evidence': ('measured: the cited path is absent from frozen32 membership and the only '
                  'evaluator-fault-contract file present is v3. Across all 107 rows this was the '
                  'ONLY owner path absent from the snapshot. See '
                  'claude-independent32-reconciliation.v1/receipts/r00-verify.json.'),
     'agree': True,
     'fix': ('DR-007 and DR-011-R08 now cite '
             'foundation/evaluator-fault-contract.v3.md, read freshly in this pass and '
             'manifest-verified.'),
     'dispositionChanged': False,
     'note': ('The disposition was already correct: the v3 contract itself states the LIVE D9 '
              'successor-artifact obligation is not discharged by this design reference. This was a '
              'citation defect, not a wrong judgement.')},
    {'id': 'RR32-02', 'rootFinding': 'F-04.limits still says the boundary precedes structural custody',
     'independentlyVerified': True,
     'evidence': ('measured: F-04.limits read "a boundary that precedes structural custody". Scanning '
                  'the whole v32 document for precedence sentences found exactly two, the other being '
                  'the RR31-05 correction entry that states the corrected order. So one stale clause '
                  'survived my own correction.'),
     'agree': True,
     'fix': 'F-04.limits now states the traced order explicitly and no inverse wording remains.'},
    {'id': 'RR32-03', 'rootFinding': 'RES-EP13-13 asserts a source28 reading session that does not exist',
     'independentlyVerified': True,
     'evidence': ('measured: the row said the file "was read fresh in that session" about the 27->28 '
                  'window. My lineage is source26, source27, source31, source32 plus a bounded '
                  'prospective-bytes review; there is no source28 review. Original receipts show '
                  'where the post-28 bytes were actually executed: v31 p06-replayorder.json rc=0 and '
                  'v32 p06-changedchecks.json rc=0.'),
     'agree': True,
     'fix': ('The row now carries the truthful history and labels a CURRENT fresh read of the file in '
             'this pass, with no retrospective execution claimed.')},
    {'id': 'RR32-04', 'rootFinding': 'four DR-011-R rows report ownerPathsResolveInFrozen32=false '
                                     'though their listed paths exist',
     'independentlyVerified': True,
     'evidence': ('measured all 16 booleans against actual frozen32 membership: R02, R04, R05 and R08 '
                  'reported false while every path they STORED resolves. Root cause found in my own '
                  'v32 build code: it stored the filtered list but computed the boolean against the '
                  'unfiltered one, so a nonexistent path was silently dropped from the row AND made '
                  'the boolean false. The four dropped owners were fact-identity-policy.v2.json, '
                  'native-protocol.v3.md (twice) and evaluator-fault-contract.v1.md.'),
     'agree': True,
     'fix': ('Real owners restored — docs/coop/artifacts/fact-identity-policy.v2.json, '
             'native/protocol3-transitions.v1.json (verified: phases=22, ruleCount=34) and '
             'evaluator-fault-contract.v3.md — and EVERY owner-resolution boolean across all 107 rows '
             'is now derived from actual frozen32 membership.'),
     'severityNote': ('This is the most substantive of the four: it was not only a false boolean but '
                      'a silently missing owner in four rows, and it came from my own build logic '
                      'rather than from a typo.')},
    {'id': 'RR32-05 (bounded probe scope, accepted)',
     'rootFinding': 'p05 tests string coordinate distinctness only; p12c gives bounded inference, not '
                    'an actual enumeration-plan admission',
     'independentlyVerified': True,
     'evidence': ('confirmed in my own receipts: p05 used pseudo coverage identities coverage2:aaa / '
                  'coverage2:bbb over hand-built rows; p12c recorded enumLookupError KeyError '
                  "'properties' and cellsOrderAnnotation None."),
     'agree': True,
     'fix': 'Both are now qualified in place, with the full-Run weight attributed to the source\'s own '
            'asymmetric control rather than to my unit probes.'},
    {'id': 'RR32-06 (root audit provenance, noted not adopted)',
     'rootStatement': ('root\'s v1 mechanical audit misread currentOwnerSelectors and emitted 30 '
                       'false missing-owner findings; v2 corrected the field access, and only the '
                       'original draft audit hash was retained.'),
     'myPosition': ('I did not rely on either root audit. I recomputed every owner path myself from '
                    'frozen32 membership, which is why I can state independently that exactly one '
                    'path was absent and exactly four booleans were wrong. I note root\'s disclosure '
                    'for the record and neither adopt nor dispute the withdrawn v1 findings, having '
                    'never seen them.')}]

R['verdictBasis'] = R['verdictBasis'] + (
    ' RECORD RECONCILIATION: four review-record defects in my source32 report were independently '
    'confirmed and corrected in this successor record — a nonexistent fault-contract citation, one '
    'surviving inverse-ordering clause, an asserted source28 reading session that never existed, and '
    'four rows whose owner-resolution booleans were false because my build silently dropped a '
    'nonexistent owner path. None of them changes a disposition, the verdict, or any obligation: '
    'root demonstrated no new normative source defect and neither did I. The ACCEPT verdict on '
    'unchanged frozen source32 stands.')
R['reconciliationStanding'] = {
    'sourceUnchanged': True,
    'newNormativeSourceDefectDemonstrated': False,
    'dispositionsChanged': 0,
    'verdictChanged': False,
    'rowsCorrected': ['DR-007', 'DR-011-R02', 'DR-011-R04', 'DR-011-R05', 'DR-011-R08',
                      'F-04', 'RES-EP13-13'],
    'booleansRecomputedAcrossAllRows': audit['rowsChecked'],
    'rootAssentStillWithheldPending': ('an accurate review record, which this successor supplies, plus '
                                       'the separate blind and application prerequisites, which remain '
                                       'open and are not affected by this pass')}
json.dump(R, open(os.path.join(BASE, 'review.json'), 'w'), indent=1, default=str)
print('rows checked:', audit['rowsChecked'])
print('rows with an unresolved owner path:', audit['rowsWithUnresolvedOwner'])
print('DR-011-R booleans now:', json.dumps(audit['booleansRecomputed']))
print('wrote review.json bytes=%d' % os.path.getsize(os.path.join(BASE, 'review.json')))
