"""Part 3 — the four v26 maps re-decided against the measured 26->27 delta, plus probes,
issues, standing flags and verdict.

No row is copied. Each says whether its owning bytes changed in 27, what I re-verified, and what
changed in its disposition. Rows whose owners are unchanged say so explicitly rather than implying
a fresh read.
"""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v27'
REC = os.path.join(BASE, 'receipts')


def rec(n):
    return json.load(open(os.path.join(REC, n)))


v26 = json.load(open('/tmp/opensip-design-corrections/claude-independent-design.v26/review.json'))
p01, p05 = rec('p01-delta.json'), rec('p05-pins.json')
p04, p06 = rec('p04-planning-layer2.json'), rec('p06-package-verify.json')
pE, pF, pF3 = rec('pE-exports.json'), rec('pF-portable.json'), rec('pF3-blobdelta.json')
pH, pK4 = rec('pH-groups27.json'), rec('pK4-rootctl.json')
pL, pP = rec('pL-pkgprobes.json'), rec('pP-handoff.json')
CH = {c['path'] for c in p01['changed']} | {a['path'] for a in p01['added']}
O = {}

RESOLVED = 'DESIGN-SPECIFIED-IN-CURRENT-OWNER-NOT-APPLIED'


def carry(mapname, updates):
    """Re-decide each row of a v26 map. `updates` supplies the per-row 27 reason."""
    out = {}
    for rid, old in v26[mapname].items():
        u = updates.get(rid) or updates['__default__']
        row = {k: old[k] for k in old if k not in ('newIssues',)}
        row['disposition'] = u.get('disposition', RESOLVED if old['disposition'].endswith(
            'WITH-NEW-ISSUE-NOT-APPLIED') else old['disposition'])
        row['ownerBytesChangedIn27'] = u['changed']
        row['reassessmentFor27'] = u['why']
        if u.get('resolvedIssues'):
            row['v26IssuesNowResolved'] = u['resolvedIssues']
        row['appliedByThisReview'] = False
        row['finalApplicationOutcomeGranted'] = False
        out[rid] = row
    return out


UNCH = ('Owning bytes are unchanged in my derived 26->27 delta, so my v26 assessment of this row '
        'stands on the reading I completed then. I re-ran the reference groups that cover it on 27 '
        '(0 frozen-snapshot deviations) and record no fresh prose read here.')

O['arDispositions'] = carry('arDispositions', {
    '__default__': {'changed': False, 'why': UNCH},
    'AR-03': {'changed': True, 'why': (
        'security-and-lifecycle.md changed in 27: S13 replaces the literal case and sweep counts with '
        '"the current case fixtures"/"the current invariant sweeps" and names the measured report as '
        'the authority. I read the changed sentences and re-ran check-security-lifecycle.v1.py on 27; '
        'the obligation text for S3/S3.1/S12 is untouched.')},
    'AR-04': {'changed': True, 'why': (
        'Same security-and-lifecycle.md edit; S4/S4.5 clock and poisoned-floor law is untouched by it. '
        'Re-verified by re-running the security group on 27.')},
    'AR-05': {'changed': True, 'why': (
        'Same security-and-lifecycle.md edit; S5/S6/S9.1 continuity and revocation law is untouched. '
        'Re-verified by re-running the security group on 27.')},
    'AR-06': {'changed': True, 'why': (
        'security-and-lifecycle.md and carrier-format.v3.md both changed. The carrier change adds an '
        'evidence-custody and diagnosis-vocabulary paragraph (scratch citations are runtime-relative '
        'and add no law; witnessMalformed is a read-only diagnosis and deliberately not a durable '
        'quarantine reason). S8 support-population law is unchanged. This closes my v26 advisories '
        'A-1 and A-3.'), 'resolvedIssues': ['A-1', 'A-3']},
    'AR-09': {'changed': True, 'why': (
        'identity-and-evidence.md and identity-schemas.v3.json both changed, and this is where my v26 '
        'S-1 landed. The standing and the three prose sentences are narrowed to bare 64-hex digest '
        'fields and a new x-opensip-digest-domains.scope block publishes the selectors. I measured 64 '
        'bare occurrences with 0 unannotated and 63 typed-prefix occurrences now explicitly outside '
        'scope. S-1 is resolved, so this row loses its new-issue qualifier.'),
        'resolvedIssues': ['S-1']},
    'AR-12': {'changed': True, 'why': (
        'target-attribution.schema.v2.json, occupancy-companion.schema.v1.json and '
        'atom-evaluation-contract.v1.md changed. The negative-provenance surface this row owns now '
        'excludes logicalPath at kind=unknown in both schemas and in the atom sentence. My 24-cell '
        'audit finds 24/24 conforming and the executed host entries refuse every meaningless-position '
        'hint.')},
    'AR-14': {'changed': True, 'why': (
        'carrier-migration.v1.md, carrier-dispatch.v3.json and carrier-format.v3.md all changed, and '
        'this is where my v26 S-2 and advisory A-1 landed. Intent validation is now scoped to the '
        'inherited-carrier path including a resumed migration, and the fresh-install path in '
        'openDispatch step 8 — including its interrupted-install act-C resume — is stated to take no '
        'intent with first_generation 1 and null migration fields. witnessMalformed is now declared a '
        'read-only diagnosis. Both S-2 and A-1 resolved.'),
        'resolvedIssues': ['S-2', 'A-1']},
    'AR-15': {'changed': True, 'why': (
        'report-asset-binding.v1.json changed (same byte count, different digest) and this is where my '
        'v26 S-1 and S-3 landed. security-completion.v1.md is now anchor B14, workflows-and-surfaces.md '
        'keeps B11, there are 14 anchors with 0 duplicate ids, and I re-counted the citations: 0 '
        'B11/B12 remain and 3 B14/B12 are present. Root updated three citations, one more than my v26 '
        'text described. With S-1 also resolved in identity, this row loses its new-issue qualifier.'),
        'resolvedIssues': ['S-1', 'S-3']},
    'AR-16': {'changed': True, 'why': (
        'security-and-lifecycle.md changed; my v26 advisory A-2 named the stale 456-case/ten-sweep '
        'literals and they are gone, replaced by derived language naming the measured report as the '
        'count authority. A-2 resolved. The section 8/9 and native section 10 remedy law is '
        'unchanged.'), 'resolvedIssues': ['A-2']},
})

O['fwDispositions'] = carry('fwDispositions', {
    '__default__': {'changed': False, 'why': UNCH},
    'FW-06': {'changed': True, 'why': (
        'identity-and-evidence.md, identity-schemas.v3.json, both logicalPath schemas and the atom '
        'contract changed. This row carried my v26 MUST M-1 — two admissible spellings of one provider '
        'claim minting different run3 identities at positions the contract calls meaningless. 27 '
        'closes it: the eight meaningless positions now admit exactly one encoding (measured), the '
        'four meaningful ones still admit the lawful hint, and all three host entries plus the '
        'retained-atom admission refuse the excluded spelling when executed. The remaining multi-digest '
        'positions are the ones the contract declares meaningful, which is the fact.anchors precedent, '
        'not a determinism defect. M-1 resolved.'),
        'resolvedIssues': ['M-1']},
})

O['inheritedResidualDispositions'] = carry('inheritedResidualDispositions', {
    '__default__': {'changed': False, 'why': UNCH},
    'DR-001': {'changed': True, 'why': (
        'This row carried my v26 S-1 and S-3. report-asset-binding.v1.json now disambiguates B11/B14 '
        'with all three citations updated, and the digest law is scoped to bare 64-hex fields with '
        'machine-readable selectors. Both resolved, so the one-effective-narrative obligation no '
        'longer carries a precision defect from me.'), 'resolvedIssues': ['S-1', 'S-3']},
    'DR-002': {'changed': True, 'why': (
        'identity-and-evidence.md changed in section 3 only, narrowing three digest-law sentences. '
        'Sections 2-5 otherwise stand as I read them in v26.')},
    'DR-006': {'changed': True, 'why': (
        'This row carried my v26 S-1 and is its natural owner: identity section 3 with the '
        'digest-domain registry. The registry standing is now "Every bare 64-hex digest field" and '
        'carries the scope block naming the pattern, the $ref, the nullable-branch rule and the '
        'typed-prefix exclusion. Measured 0 unannotated bare fields. S-1 resolved.'),
        'resolvedIssues': ['S-1']},
    'DR-007': {'changed': False, 'why': (
        'Owning bytes unchanged in 27. The scope statement stands verbatim and deliberately: the D9 '
        'successor artifact carrying host-invariant remains a disclosed, attributed implementation '
        'obligation of that unit, carried forward by this review and not closed by it.')},
    'DR-011': {'changed': False, 'why': (
        'inherited-residuals.proposed.md is unchanged and evaluation-residual-dispositions.proposed.json '
        'is unchanged in 27 (I verified its sha 8f7d940e... against the frozen manifest). I read all 30 '
        'rows of that file completely this session and disposed each individually below.')},
    'DR-011-R08': {'changed': False, 'why': (
        'Owning bytes unchanged. Scope retained verbatim: the successor D9 artifact carrying '
        'host-invariant stays a disclosed, attributed obligation of the D9 unit. Nothing in the 27 '
        'delta touches it, and this review does not discharge it.')},
    'DR-011-R10': {'changed': False, 'why': (
        'Owning bytes unchanged, and this row is still closable only by an actual fresh implementer '
        'litmus that this review is explicitly not. My v26 scope named S-1 as the obstacle such a '
        'reader would hit first; S-1 is now resolved, which removes that particular obstacle but '
        'closes nothing here. The separate blind original 123/8/3 test remains required and '
        'uninfluenced by me: I did not read or touch the blind consumer work, and the frozen charter '
        'I verified shows all 123 dispositions PENDING with independentAcceptance false.')},
    'DR-011-R12': {'changed': False, 'why': (
        'Owning bytes unchanged. All 30 nested residuals are retained and individually disposed below '
        'against source27 bytes, with TCB-SCOPE-01 assessed once as a shared assumption over 13 of '
        'them. No malicious-same-process containment is claimed here either.')},
})

O['scopedReviewOwnerDispositions'] = carry('scopedReviewOwnerDispositions', {
    '__default__': {'changed': False, 'why': (
        'Owning bytes unchanged in my derived 26->27 delta. The routing assessment I made in v26 '
        'stands on the reading I completed then. Re-verified only that the owners still exist and '
        'still say what I recorded, via the reference groups re-run on 27.')},
    'DR-201': {'changed': True, 'why': (
        'Partly changed: identity-and-evidence.md section 3 and the carrier documents moved. Neither '
        'edit touches the branch separation this row is about — the step DAG versus derivation DAG '
        'split, Run-versus-command finalization, post-commit output failure and parked recipes. '
        'Routing assessment unchanged; still not applied and still not re-accepted.')},
    'DR-204': {'changed': True, 'why': (
        'security-and-lifecycle.md changed its S13 count sentences, which is the invariant-coverage '
        'territory this row routes. The change replaces stale literals with the measured report as '
        'authority, which improves the row\'s subject without changing its routing. Not applied.')},
})
for k in O['scopedReviewOwnerDispositions']:
    O['scopedReviewOwnerDispositions'][k]['disposition'] = 'ROUTING-ASSESSED-ONLY-NOT-APPLIED'

# ---------------- probes ----------------
O['independentProbes'] = [
    {'id': 'P-00', 'what': 'full manifest, per-file sha/byte and archive verification of snapshot27',
     'result': 'all 12893 files verified, 736,295,158 bytes, archive sha matches, no extras'},
    {'id': 'P-01/02/03', 'what': '26->27 delta derived from the two frozen manifests, then line-diffed',
     'result': '1 added, 0 removed, 19 changed, +17,818 bytes; 8 files are pure digest/pin refreshes'},
    {'id': 'P-04/05', 'what': 'planning layer 2 provenance and the five pin ledgers',
     'result': 'previousArchitectureInputLayer resolves; pin ledgers differ from 26 only in digests'},
    {'id': 'PM1-hint-space', 'what': 'exhaustive 4 kinds x 3 occupancies x 2 spellings admissibility audit',
     'result': '24/24 cells conform to the declared meaning; 8 meaningless positions closed to one encoding'},
    {'id': 'PM1-boundaries', 'what': 'first attempt to execute the buffer/bind/capture/atom boundaries',
     'result': 'FAILED with two TypeErrors from my own wrong call signatures; preserved as a probe defect'},
    {'id': 'PM1-routes', 'what': 'corrected boundary execution plus public route derivation',
     'result': 'all three host entries refuse the excluded hint; the two pre-existing sibling keys reach '
               'the identical public termination as the chosen route, so no new key is needed'},
    {'id': 'PM1-weighting', 'what': 'position-indexed distinct-digest counts under three hint values',
     'result': 'the four remaining multi-digest positions are exactly those the contract calls meaningful'},
    {'id': 'PS-reassess', 'what': 'S-1/S-2/S-3 and A-1/A-2/A-3 re-measurement on 27',
     'result': 'all six RESOLVED, each by a measured property rather than by prose'},
    {'id': 'PE-exports', 'what': 'independent store decoder plus snapshot27 owner over all 13 exports',
     'result': '7 positives ADMIT/ADMIT; 3 false-result controls ADMIT then REFUSE '
               'EVALUATOR_COMPLETE_PROOF_REPLAY; binding invalid-default ADMIT then REFUSE '
               'ENUMERATION_BINDING_PROGRAM_ENTRY; lawful-default and single-explicit ADMIT/ADMIT'},
    {'id': 'PF-portable', 'what': 'from-scratch construction in a fresh arbitrary directory',
     'result': 'all five builders succeeded with only --source/--package/--out (no helper overlay); '
               'every claimed runId identical'},
    {'id': 'PF2/PF3-blobdelta', 'what': 'audit of why fresh bytes differ from shipped bytes',
     'result': 'exactly one unreferenced retained blob per store differs — the changed '
               'target-attribution.schema.v2.json document — proven inert by mutual replay'},
    {'id': 'PG-launcher27', 'what': 'the current source-pinned evaluator3 launcher on 27',
     'result': '1242 pins valid, 0 changed or missing, 16/16 children exit 0'},
    {'id': 'PH-groups27', 'what': 'remaining contract and reference groups inside a verified disposable copy',
     'result': '1351 copied bytes all equal to the frozen manifest; 0 frozen-snapshot deviations after all runs'},
    {'id': 'PK2-rootexec', 'what': 'execution of the internal-root admission boundary',
     'result': 'first run FAILED on my own wrong argument shape (preserved); corrected run refuses "." '
               'and "./" with the root-specific fault and still admits "" and "packages/a"'},
    {'id': 'PK3/PK4-rootwiring', 'what': 'is the root guard wired before the binding join, and is it controlled',
     'result': 'wired at :581 and short-circuits before the only _unit_for_cell call and every '
               'PROGRAM_ENTRY raise; exercised by 0 of 27 reference checkers (advisory A-4). '
               'PK3 first computed precedence against a definition line and was wrong; corrected in PK4'},
    {'id': 'PL-pkgprobes', 'what': 'I ran the package\'s four portable probes myself against source27',
     'result': 'all four exit 0; the seven query checks regenerate BYTE-IDENTICAL to the shipped copies; '
               'assess PASS 7; properties PASS; mixed-universe merged view refuses '
               'EXECUTION_INPUTS_COVERAGE_DERIVE. One earlier invocation failed on my own wrong flags'},
    {'id': 'PM-f09tcb', 'what': 'clause check for the corrected citation and my own TCB classification',
     'result': 'the fault is raised only in coverage-account derivation, and §5 is exactly that clause; '
               'my keyword classifier returned 14 and was wrong on three rows, corrected by reading'},
    {'id': 'PN-residualbind', 'what': 'binding all 30 residual rows to frozen27',
     'result': '30/30 ids match, 0 selector mismatches, 0 evidence paths unresolved, 0 sha mismatches, '
               '0 change-claim disagreements with my delta, 30/30 PENDING, 0 applied'},
    {'id': 'PP-handoff', 'what': 'the 123/8/3 charter handoff',
     'result': '123/8/3 with ids identical to the frozen charter, 123 PENDING, independentAcceptance '
               'false, 0 waiver tokens. One earlier run failed on my own key-selection bug'}]

O['evidenceReceipts'] = {
    'authorPackage': {
        'artifactManifestSha256': p06['artifactManifestSha256'],
        'declaredFiles': p06['declaredFileCount'], 'verified': p06['verified'],
        'mismatched': p06['mismatched'], 'missing': p06['missing'],
        'sourceManifestBinding': p06['binding_sourceManifestSha256'],
        'bindsExact27': p06['mentionsExact27Manifest'],
        'standing': ('AUTHOR-assisted evidence. Never a blind reconstruction, never independent '
                     'acceptance. I graded no row from author self-assessment and treated no expected '
                     'output as correctness evidence.')},
    'exportReplay': {'positives': pE['positives'], 'falseResultControls': pE['falseResultControls'],
                     'bindingControls': pE['bindingControls'],
                     'structuralBoundary': pE['structuralBoundary'],
                     'semanticBoundary': pE['semanticBoundary'],
                     'allMeetReferenceExpectation': pE['allMeetReferenceExpectation'],
                     'ownerSha256': pE['ownerSha256'],
                     'note': 'my own store decoder; the package checkers were not imported'},
    'portableConstruction': {'arbitraryRoot': pF['arbitraryOutputRoot'],
                             'allBuildsSucceeded': pF['allBuildsSucceeded'],
                             'runIdsIdenticalEverywhere': pF['claimRunIdsIdenticalEverywhere'],
                             'freshPositivesAllAdmit': pF3['freshPositivesAllAdmit'],
                             'freshControlsAdmitThenReplayRefuse':
                                 pF3['freshControlsAllStructuralAdmitSemanticRefuse'],
                             'exportsRepaired': False},
    'referenceGroups': {'frozenDeviationsAfterAllRuns': pH['frozenDeviationsAfterRuns'],
                        'disposableCopyBytesVerified': pH['disposableCopyVerified'],
                        'pinGateBypassed': False},
    'packageProbesIRanMyself': {'allExitZero': pL['allProbesExitZero'],
                                'queryOutputsRegeneratedByteIdentical': 8},
    'charterHandoff': {'requirements': 123, 'standingRules': 8, 'futureQualification': 3,
                       'allPending': pP['pendingCount'] == 123,
                       'independentAcceptance': False, 'waiverTokens': 0}}

# ---------------- issues ----------------
O['newMustIssues'] = []
O['newShouldIssues'] = []
O['advisories'] = [
    {'id': 'A-4', 'title': ('The internal-root representation guard is enforced and correctly wired '
                            'but is exercised by no reference checker'),
     'selectors': ['docs/coop/design-corrections/native/native_evidence_model.v2.py admit_unit_roots '
                   'and NATIVE_UNIT_ROOT_REPRESENTATION',
                   'docs/coop/design-corrections/foundation/enumeration_model.v1.py:500-520 '
                   '_admit_membership_unit_roots and ENUMERATION_MEMBERSHIP_UNIT_ROOT',
                   'docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/InternalUnitRootV1'],
     'measured': ('0 of 27 reference checkers on 27 mention NATIVE_UNIT_ROOT_REPRESENTATION, '
                  'ENUMERATION_MEMBERSHIP_UNIT_ROOT, admit_unit_roots or InternalUnitRootV1.'),
     'why_not_a_should': (
         'The law itself is complete and correct and I demonstrated it by direct execution: the '
         'sentinel refuses with a root-specific fault naming the offending value and its schema '
         'selector, lawful spellings still admit, and the guard short-circuits before the binding '
         'join so the old misattribution cannot recur. Nothing in the normative text is wrong, which '
         'is the bar my v26 SHOULDs met. This is control coverage, and it is inherited material: '
         'these three files are unchanged in my 26->27 delta, so it is not a regression introduced '
         'here and it would be inconsistent to raise it as blocking against a delta that did not '
         'touch it.'),
     'suggestion': ('Add a negative control asserting structural ADMIT then the '
                    'NATIVE_UNIT_ROOT_REPRESENTATION refusal, in the same shape as the '
                    'ts-invalid-default-entry binding control. An application reviewer may reasonably '
                    'elevate this.'),
     'inheritedNotNewIn27': True},
    {'id': 'A-5', 'title': ('AX6, AX9, MD5 and RX2c preserve neither an inline original nor a title, '
                            'and their cited source artifacts are not members of the subject'),
     'selectors': ['docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json '
                   '$.items[26..29]',
                   'cited source docs/coop/artifacts/evaluation-proof.v13.json',
                   'cited source docs/coop/artifacts/ep13.review-independent.json'],
     'measured': ('19 rows carry a full inline original and 7 carry an originalTitle; these 4 carry '
                  'neither. Both cited artifacts have 0 occurrences anywhere in the 12893 files of '
                  'frozen27. The four variant names are mentioned inside other rows\' prose (AX6 x3, '
                  'AX9 x2, MD5 x6, RX2c x3), so context exists, but their own statements do not.'),
     'why_not_a_should': (
         'The dispositions are assessable on their own terms against admission-and-qualification.md, '
         'which I read and whose bytes I verified, and all four correctly claim nothing. This limits '
         'the evidence available for four rows rather than showing a defect in them, and it is the '
         'same custody shape that F-01 and F-02 fixed for the charter, so the remedy is known and '
         'cheap. The proposed file is unchanged in my 26->27 delta.'),
     'suggestion': ('Preserve a one-line original statement inline for these four, as the other 26 '
                    'rows do, or freeze the two cited artifacts into the subject.'),
     'inheritedNotNewIn27': True},
    {'id': 'A-6', 'title': 'The regenerated query checks are not wired into verify-package.py',
     'selectors': ['claude-author-package-successor.v4/verify-package.py',
                   'claude-author-package-successor.v4/check-author-query.py'],
     'measured': ('verify-package.py contains no reference to the query checks. I regenerated all '
                  'eight outputs byte-identically myself, so regeneration works; it is simply not '
                  'automatic.'),
     'why_not_a_should': ('This is an author-package convenience, not subject design law, and F-03\'s '
                          'actual impact — evidence nobody can regenerate — is eliminated.'),
     'suggestion': 'Call check-author-query.py from verify-package.py, or say plainly that it is a separate step.',
     'inheritedNotNewIn27': False}]

O['resolvedSinceV26'] = {
    'M-1': 'RESOLVED', 'S-1': 'RESOLVED', 'S-2': 'RESOLVED', 'S-3': 'RESOLVED',
    'A-1': 'RESOLVED', 'A-2': 'RESOLVED', 'A-3': 'RESOLVED',
    'note': ('Every MUST and SHOULD I raised against source26 is resolved in source27 by a property I '
             'measured or executed, not by a promise. My v26 verdict was CHANGES_REQUIRED and those '
             'changes were made.')}

# ---------------- standing ----------------
O['crossUnitStanding'] = dict(v26['crossUnitStanding'])
O['crossUnitStanding'].update({
    'evaluationResidualsRetained': 30,
    'evaluationResidualsClosedByThisReview': 0,
    'condition2Obligations': 28,
    'condition2ObligationsRetained': 28,
    'condition2Standing': ('All 28 remain OPEN for full-product integration. Historical preview '
                           'acceptance is not counted as review of the changed scope, and nothing in '
                           'the 26->27 delta discharges any of them.'),
    'qualificationGates': 32,
    'qualificationGatesPerformed': 0,
    'condition5': 'NOT MET',
    'qualificationGateMeasurement': ('Every row of qualification-gates.proposed.json still carries '
                                     'qualified=false, demonstrated=false, '
                                     'implementationHarnessAuthored=false and standing '
                                     'DESIGN-CONTRACT-PENDING-REVIEW. I re-measured this on 27.'),
    'commitRecoveryCases': 54,
    'commitRecoveryCasesExecuted': 0,
    'commitRecoveryStanding': ('All 54 planned recovery cases remain unexecuted product obligations. '
                               'Native carrier qualification is separately required.'),
    'd9SuccessorObligation': ('DR-007 and DR-011-R08: the successor D9 artifact carrying host-invariant '
                              'remains a disclosed, attributed implementation obligation of the D9 unit. '
                              'Carried forward, not closed.')})
O['dispositionStandingForEveryRow'] = {
    'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False, 'gradeAwarded': None,
    'ownerRoutesAllFalse': ('All 5 scopedReviewOwnerDispositions carry appliedByThisReview=false and '
                            'finalApplicationOutcomeGranted=false.')}
O['dispositionVocabulary'] = dict(v26['dispositionVocabulary'])
O['dispositionVocabulary'].update({
    'PROPOSED-REPLACEMENT-REVIEWABLE-AS-DESIGN-NOT-GRADED': (
        'The proposed correction exists in current owner bytes I read or executed, is individually '
        'reasoned, and is assessable as design. Grading belongs to the separate application review.'),
    'HISTORICAL-MEASURED-ESCAPE-PRESERVED-NOT-REPAIRED-NOT-GRADED': (
        'A historical measured escape retained as history. The mechanism is absent from product '
        'authority and nothing claims it repaired.')})
O['dispositionCounts'] = {'arDispositions': 16, 'fwDispositions': 15,
                          'inheritedResidualDispositions': 27, 'scopedReviewOwnerDispositions': 5,
                          'evaluationResidualDispositions': 30, 'fDispositions': 14, 'total': 107}
O['grantsNothing'] = {
    'grade': None, 'activation': False, 'implementationAuthorized': False,
    'blindAcceptance': False, 'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False,
    'note': ('This design review assesses and routes. It grants no application grade, no activation, '
             'no blind acceptance and no implementation authorization. The final separate application '
             'review must still grade the 30 evaluation residuals and the 28 condition-2 obligations. '
             'Root independently assesses this review.')}
O['limitations'] = [
    'Design, architecture, schema and reference layers only. No product implementation exists to test.',
    'The author package is AUTHOR-assisted evidence. It is never a blind reconstruction and I graded '
    'no row from its self-assessment.',
    'The seven positive Runs are not seven independent agreements: one is an author-helper composition '
    'compared with the frozen owner, and six are frozen-owner derivations replayed by that same owner. '
    'I weight them accordingly.',
    'The predicate algebra is exercised for exists and none only. and/or/not remain unexercised and '
    'count-at-most/all-covered remain unimplemented in the partial helper.',
    'The two-binding construction is incomplete. I accept the recorded refusals as an evidence limit, '
    'not as a demonstrated owner defect, so AR-01 Q3 stays unanswerable from this package.',
    'Missing author controls limit evidence; they are not by themselves a demonstrated normative defect.',
    'An authenticated pure host/evaluator consuming inert typed data is what the bytes describe. I '
    'claim no same-process hostile-code containment, no qualified provider isolation, and no measured '
    'compiler, OS, filesystem or crypto enforcement.',
    'All 54 commit-recovery cases and all 32 qualification gates remain unperformed product obligations; '
    'condition 5 is NOT MET.',
    'The separate blind original 123/8/3 test remains required and uninfluenced by me. I did not read '
    'or touch the blind consumer work at any point.',
    'My reading of unchanged material is inherited from the v26 session and is labelled as such, not '
    're-badged as a fresh read.',
    'Reference checkers that write reports were run only inside a disposable copy whose every byte I '
    'verified against the frozen manifest; the frozen snapshot measured unchanged afterwards.']

O['requiredReviewActions'] = {
    'source27ManifestAndEveryFileVerified': True,
    'archiveDigestVerified': True,
    'parent26RelationshipVerified': True,
    'delta26to27DerivedByMe': True,
    'everyChangedNormativeOwnerReadInFullContext': True,
    'everyChangedMappingAndPinFileRead': True,
    'providerTargetAttributionReturnSchemaReadCompletely': True,
    'providerReturnLawsAndRegisteredDefinitionsAndAffectedJoinsIncorporated': True,
    'v26ScopeOverclaimCorrectedWithoutAlteringV26': True,
    'v26EvidenceLabellingCorrected': True,
    'm1s1s2s3AndA1A2A3ReassessedSubstantively': True,
    'routeSufficiencyReEvaluatedWithoutDemandingASuggestedKey': True,
    'evidenceWeightingResolvedCandidly': True,
    'authorPackageEveryFileAndSourceBindingVerified': True,
    'packageReadmeHandoffAndResidualAssessmentRead': True,
    'authoredReviewAndBuildersAndTransportAndHelpersRead': True,
    'noRowGradedFromAuthorSelfAssessment': True,
    'sevenExportsReExecutedStructuralAndSemantic': True,
    'threeFalseResultControlsStructurallyAdmitThenReplayRefuse': True,
    'bindingControlsBehaveAsSpecified': True,
    'fromScratchPortableConstructorExecutedInFreshArbitraryDirectory': True,
    'exportBytesComparedWithoutRepairingInputs': True,
    'allSixteenEvaluator3ChildrenRunOn27': True,
    'contractAndReferenceGroupsRunOn27': True,
    'sourcePinsPreservedAndRawFailuresKept': True,
    'f01ThroughF14Assessed': True,
    'thirtyEvaluationResidualDispositionsProduced': True,
    'tcbScope01AssessedAsOneSharedAssumption': True,
    'allFourInheritedDispositionMapsUpdatedForCurrent27': True,
    'progressFileKept': True,
    'failedProbesPreservedHonestly': True}

O['verdict'] = 'ACCEPT'
O['verdictBasis'] = (
    'Every required action above is completed, and there is no unresolved MUST or SHOULD. The one MUST '
    '(M-1) and all three SHOULDs (S-1, S-2, S-3) I raised against source26 are resolved in source27 by '
    'properties I measured or executed, as are all three of my v26 advisories. I raise no new MUST and '
    'no new SHOULD against source27. Three advisories are recorded, two of them on inherited material '
    'that the 26->27 delta did not touch, and each states why it is not a SHOULD. This verdict is an '
    'independent design assessment only: it grants no application grade, no activation, no blind '
    'acceptance and no implementation authorization, it closes none of the 30 evaluation residuals, '
    'none of the 28 condition-2 obligations, none of the 32 gates and none of the 54 recovery cases.')

json.dump(O, open(os.path.join(BASE, 'review.part3.json'), 'w'), indent=1)
print('part3 keys:', len(O))
print('verdict:', O['verdict'])
for k in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
          'scopedReviewOwnerDispositions'):
    print('%-32s %d' % (k, len(O[k])))
