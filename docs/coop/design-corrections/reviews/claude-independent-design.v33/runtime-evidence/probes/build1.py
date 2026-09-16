"""review.json part 1 — verification, delta, source-change assessment, package standing."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
REC = os.path.join(BASE, 'receipts')
V32R = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v2/review.json'


def rec(n):
    return json.load(open(os.path.join(REC, n)))


p00, p01 = rec('p00-verify33.json'), rec('p01-delta.json')
p02, p03 = rec('p02-execlaw.json'), rec('p03-suites.json')
p04, p05 = rec('p04-newlawcontrols.json'), rec('p05-fullrun.json')
p06, p07 = rec('p06-fallback-planning.json'), rec('p07-layer-bounded.json')
p08, p09 = rec('p08-envelope.json'), rec('p09-optional33.json')
p10, p11 = rec('p10-pins-planning.json'), rec('p11-package.json')
R = {}

R['review'] = ('Independent design review of exact newly frozen consolidated product source33. '
               'Whole-design obligations retained; not a focused approval of the changed law alone.')
R['sessionIdentity'] = {
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'role': 'independent reviewer; I have authored no source in this lineage',
    'notAForbiddenAcceptor': ('I am none of the six excluded source-author origins (eaa8276c…, '
                              '36a89be8…, 0aa529b3…, 329a5132…, 919c766d…, 823bf66b…). 823bf66b is '
                              'preparing the author package and is not an eligible acceptor.'),
    'priorReviewsHistoricalUnchanged': [
        'claude-independent-design.v32 (ACCEPT on source32)',
        'claude-independent32-reconciliation.v1 and .v2 (record corrections, root-accepted)'],
    'neitherAcceptsTheseBytes': True,
    'blindPolicy': ('No consumer output, runtime, report or root blind replay file was opened. No '
                    'blind result or oracle is an input to this review, and I claim no blind acceptance.')}
R['baselineRecord'] = {
    'path': 'claude-independent32-reconciliation.v2/review.json',
    'sha256': hashlib.sha256(open(V32R, 'rb').read()).hexdigest(),
    'expected': '7336c04d32d147817b696f896154722e63792d206805be54ea2319668a2465af',
    'standing': ('the complete corrected 107-row baseline; preserved unchanged. Its rows are carried '
                 'forward here with current33 status, not regenerated cosmetically.')}
R['baselineRecord']['matches'] = R['baselineRecord']['sha256'] == R['baselineRecord']['expected']

R['subjectManifestSha256'] = p00['manifestSha256']
R['verifiedManifest'] = p00['ALL_VERIFIED']
R['manifestVerification'] = {
    'manifestShaMatchesDeclared': p00['manifestMatchesDeclared'],
    'archiveShaMatchesDeclared': p00['archiveMatchesDeclared'],
    'declaredFiles': p00['declaredFileCount'], 'filesChecked': p00['filesChecked'],
    'declaredTotalBytes': p00['declaredTotalBytes'], 'measuredTotalBytes': p00['measuredTotalBytes'],
    'missing': p00['missingCount'], 'hashMismatches': p00['hashMismatchCount'],
    'sizeMismatches': p00['sizeMismatchCount'], 'extras': p00['extrasCount'],
    'archiveMemberRows': p00['archiveFileRows'],
    'archiveEqualsManifest': p00['archiveEqualsManifest'],
    'parentIsMySource32': p00['parentIsMyV32'],
    'frozenDeviationsAfterAllRuns': p10['frozenDeviationsAfterRuns']}
R['delta32to33'] = {
    'derivedByThisReview': True,
    'added': p01['addedCount'], 'removed': p01['removedCount'], 'changed': p01['changedCount'],
    'touched': p01['touched'], 'netBytes': p01['netBytes'],
    'addedPaths': [a['path'] for a in p01['added']],
    'changedPaths': [c['path'] for c in p01['changed']],
    'rootInventoryAgreement': {'rootDeclared': p01.get('rootDeclaredCount'),
                               'agrees': p01.get('agreesWithRootInventory'),
                               'inMineNotRoot': p01.get('inMineNotRoot'),
                               'inRootNotMine': p01.get('inRootNotMine'),
                               'standing': 'root-delta32-to33.json is inventory only, never approval'}}

R['sourceChangeAssessment'] = {
    'executionInputsLaw': {
        'status': 'SUBSTANTIVELY CORRECT AND CONTROLLED IN BOTH DIRECTIONS',
        'changedOwners': ['docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md',
                          'docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json',
                          'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py',
                          'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py',
                          'docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py',
                          'docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py'],
        'firstMatchPrecedence': {
            'publishedOrder': ['inapplicable-vcs', 'unsupported-typed', 'unavailable-unselected',
                               'unavailable-null-universe', 'supported-available'],
            'myExhaustiveGrid': p02['gridSize'],
            'allFiveTokensReachable': p02['allFiveTokensReachable'],
            'row3BeforeRow4Justified': (
                'The contract argues row 3 must precede row 4 because the enumeration owner refuses a '
                'non-null universe on an unselected enumerator, so testing the universe first would '
                'make unavailable-unselected unreachable. I tested it: unselected+null U yields '
                'unavailable-unselected in all 16 cases and selected+null U yields '
                'unavailable-null-universe in all 16, so the two advertised states stay distinct and '
                'neither collapses.'),
            'twoStatesStayDistinct': p02['twoStatesStayDistinct'],
            'unsupportedOutranksBoth': p02['unsupportedOutranksUnselectedAndNullU'],
            'vcsNoneOutranksAll': p02['vcsNoneOutranksAll'],
            'checkerPrecedenceControl': {'cases': len(p05['precedenceControl'] or []),
                                         'allMatch': p05['precedenceAllMatch']}},
        'externalSourceUniverseJoin': {
            'law': ('nativeCoverageAccounts[i].sourceUniverse equals the binding universe for EVERY '
                    'applicability; a null binding U stays null; carrying no Coverage does not erase '
                    'the coordinate; targetUniverse is deliberately NOT joined.'),
            'publishedAsAnnotations': ('x-opensip-external-joins and '
                                       'x-opensip-applicability-precedence, because JSON Schema '
                                       'cannot compare a different document — an honest statement of '
                                       'what admission compares rather than a pretended per-record check'),
            'negativeControlsThatRefuse': [
                'inapplicable-vcs-account-null-source-universe-refuses',
                'unsupported-typed-account-null-source-universe-refuses',
                'null-binding-universe-account-must-stay-null',
                'foreign-universe-account-source-universe-refuses'],
            'allRefuseWith': 'EXECUTION_INPUTS_COVERAGE_DERIVE',
            'positiveControls': ['unsupported-typed-account-carries-binding-universe',
                                 'inapplicable-vcs-account-carries-binding-universe'],
            'assessment': ('controlled in BOTH directions, which is what makes the published external '
                           'join meaningful rather than declarative')},
        'requestVersusSelectionVersusDisclosure': {
            'assessment': ('The three are kept distinct and I verified each has its own control. A '
                           'capability REQUEST can be UNSUPPORTED-TYPED and still requestable; the '
                           'ENUMERATOR selection is separately unselected or selected-with-null-U; '
                           'and optional retained DISCLOSURE is a third thing — '
                           'optional-unselected-account-retained-typed-disclosure admits, while '
                           'optional-unsupported-cell-owes-no-required-cell-row shows an optional '
                           'unsupported cell is not forced to execute a provider to close.')},
        'selectedUnsupportedCoverageRetention': {
            'law': ('a selected-U UNSUPPORTED-TYPED cell may lawfully have returned Coverage and the '
                    'account names none of it: coverageIds stays empty because only supported-available '
                    'names envelopes, while the Coverage stays in its returned view, the stage capture, '
                    'selectedRefs and native disclosure'),
            'proofPath': ('derivedAccounts carries accountState=unsupported with the MATRIX '
                          '(deficiency, nativeCause) pair, and a REQUIRED such cell additionally emits '
                          'a requiredCellDeficiencies row that bridges to proof and holds the Run at '
                          'indeterminate'),
            'fullRunEvidence': ('full-run-required-unsupported-matrix-pair-bridge is an admitted Run '
                                'with verdict indeterminate carrying the matrix pair '
                                '["language-tier-unsupported","capability-missing"]'),
            'optionalNotForced': 'optional-unsupported-cell-owes-no-required-cell-row admits'},
        'nullNullCarrierForMissingWork': {
            'law': ('where the only incompleteness is missing work — no returned partition, or '
                    'expected subjects no partition covers — no retained source carries a pair, so the '
                    'derived pair is explicitly (null, null) and NOT provider-unavailable'),
            'casesMeasured': p04['summary']['nullNullCarrierCases'],
            'hostMayNotClaimProviderUnavailable': [
                'empty-returned-partitions-host-may-not-claim-provider-unavailable (REFUSE)',
                'census-missing-subjects-host-may-not-claim-provider-unavailable (REFUSE)',
                'partial-inventory-budget-not-replaced-by-provider-unavailable (REFUSE)',
                'unavailable-binding-cause-not-replaced-by-provider-unavailable (REFUSE)'],
            'typedCarrierSurvivesAlongsideCensusFailure': (
                'typed-native-carrier-survives-alongside-census-failure admits with pairs '
                '[["budget-exhausted", null], [null, null]] — the real typed native carrier is kept as '
                'the primary pair while the census failure is reported separately, so real causes are '
                'not suppressed'),
            'wholePairNeverUnzipped': (
                'mixed-accounts-first-typed-pair-not-first-source admits: the pair is taken whole from '
                'the first record that ACTUALLY carries a typed pair, not from the first source record, '
                'and a record carrying no pair never borrows a sibling\'s')},
        'requiredCellBridgeAndUniqueness': {
            'bridge': ('composition §9.6 maps a null deficiency to proof cause required-cell-unsatisfied '
                       'with nativeCause null, the binding universe, and Cset({XI} ∪ row.inputRefs), so '
                       'the originating refs survive and any nonempty executionDeficiencies makes the '
                       'sealed verdict at least indeterminate'),
            'uniquenessSplit': ('internal requiredCellDeficiencies are unique by C of the whole '
                                'internal row including cell/program/relation/resolution/capability, '
                                'while proof items are Cset of the bridged record which has none of '
                                'those coordinates; dedup on (cell, program, cause, relation) is '
                                'explicitly forbidden because it would drop the second inventory or rung'),
            'fullRunEvidence': ['full-run-empty-returned-partitions-bridge-required-cell (indeterminate)',
                                'full-run-census-missing-subjects-bridge-keeps-originating-refs (indeterminate)'],
            'measuredExample': ('typed-inventory-carriers-survive-alongside-census-failure keeps two '
                                'distinct required-cell-unsatisfied rows plus a native-work-incomplete '
                                'row, so sibling carriers are not collapsed')},
        'parentCompositionProviderFallback': {
            'status': 'CONFLICT RESOLVED, AND THE OWNERS ARE CORRECTED TOGETHER',
            'whatTheContractNowRecords': (
                'composition §9.6 states on the record that its own table had EXPLICITLY PRESCRIBED '
                'the provider-unavailable fallback that execution-inputs §4/§5 forbade, that this was '
                'a contradiction between two normative owners rather than merely a reference-side '
                'invention, and that the earlier diagnosis characterising it as a reference-side '
                'invention was too narrow.'),
            'myAssessment': (
                'I agree with that correction of record and consider it the right way to handle it: a '
                'host obeying §4 and a host obeying the old table genuinely could not both admit, so '
                'correcting only the model would have left the contradiction standing. Measured on 33 '
                'the two owners now agree: composition\'s table routes "no Coverage records" to the '
                'account\'s derived primary pair, which is null/null, and execution-inputs forbids '
                'manufacturing a carrier. The four REFUSE controls above enforce it in the model.'),
            'lawfulProviderUnavailableRemains': (
                'provider-unavailable is still lawful where a record genuinely carries it — an '
                'unavailable binding\'s own declared deficiency, or a typed unavailable receipt. The '
                'forbidden thing is manufacturing it for pure missing work. '
                'unavailable-binding-cause-not-replaced-by-provider-unavailable refuses precisely so a '
                'binding\'s own cause cannot be overwritten by the generic token, which is the correct '
                'distinction and one my own keyword scan initially blurred.')},
        'mixedTypedAndUntypedSources': {
            'law': 'deterministic whole-pair selection in a published order, with all evidence retained',
            'order': ('returned partitions in canonical H order, then any named-but-not-returned '
                      'Coverage; the pair is taken whole from the first record that carries one'),
            'evidenceRetention': ('derivedAccounts[].coverageRecords keeps each '
                                  'deficiency+nativeCause+inputRef TOGETHER, and the checker asserts '
                                  'no branch unzips deficiencies and nativeCauses and re-pairs the '
                                  'first of each'),
            'measured': p04['causeRetentionStatement'][:300]},
        'perUniverseAttribution': {
            'assessment': ('The clause is deliberately narrow and says so: it constrains only views '
                           'REACHED THROUGH a selected binding\'s account derivation, forbids exactly '
                           'one thing (one view carrying two universes\' Coverage then attributed to a '
                           'binding fixed at one), and explicitly does not ban multi-universe Runs, '
                           'cross-universe targets or incoming targets. owner-graph-two-universes '
                           'admits, which demonstrates the multi-universe Run stays lawful.')},
        'suiteResults': {'jobs': [{'checker': j['checker'], 'rc': j.get('returncode'),
                                   'justification': j.get('justification')} for j in p03['jobs']],
                         'allExitZero': p03['allExitZero'],
                         'executionInputsControls': {'cases': p04['totalCases'],
                                                     'mismatches': len(p04['mismatches']),
                                                     'admitting': p04['summary']['admittingControls'],
                                                     'refusing': p04['summary']['refusingControls'],
                                                     'fullRunRows': p04['summary']['fullRunRows']}},
        'fullRunColumn': {
            'rows': len(p05['fullRunRows']),
            'allRealRunIds': p05['allHaveRealRunIds'],
            'digestEqualityAsserted': ('the checker asserts '
                                       'attached["graph"]["inputs"]["executionInputsDigest"] == digest0, '
                                       'and each row carries both proofExecutionInputsDigest and '
                                       'sameGraphExecutionInputsDigest'),
            'rowsWithDigestColumn': len(p05['digestEqualityAsserted']),
            'note': ('my allHaveProofRefDigest metric reads False only because the clean PASS row has '
                     'no execution deficiency and therefore no refs — expected, not a gap'),
            'limit': ('these are reference fixture self-consistency controls, not blind reconstruction '
                      'and not provider qualification')}},
    'boundedScopes': {
        'candidateEnvelopeSchemaOnly': {
            'status': 'INDEPENDENTLY REPRODUCED ON FINAL33 AT ITS STATED SCOPE',
            'schemaSha256': p08['schemaSha256'],
            'result': {'originalExecution2Prefix': 'REFUSE', 'correctedExecPlan2Prefix': 'ADMIT'},
            'agreesWithRootControl': p08['agreesWithRootControl'],
            'scopeLimit': p08['assessment']},
        'optionalCandidateCarrierReachability': {
            'status': 'INDEPENDENTLY VERIFIED ON FINAL33',
            'rootScope': ('root\'s own assessment is bound to source32 and an active author draft; my '
                          'verification is on final33 and does not rest on it'),
            'measured': p09['assessment'],
            'fullRunOptionalClosesClean': p09['optionalFullRunClosesWithoutRequiredDeficiency'],
            'candidateRefsOnlyWithEnvelope': p09['candidateRefsOnlyWhenEnvelopeExists']}},
    'planning': {
        'layer4': {'pins': p06['layer4']['pins'], 'binds29': p06['layer4']['binds29'],
                   'allPinsResolveAgainstFrozen33': p06['layer4AllPinsResolve'],
                   'differenceFromLayer3': ('same 29 pins; nothing added or removed; exactly one '
                                            'repin — docs/v2/contracts/product-v1/native-evidence.md, '
                                            'which is in my derived delta'),
                   'repinned': p07['repinnedInLayer4'],
                   'noPyFiles': p06['layer4PyFiles'] == [],
                   'referencePyIsNotANormativeInput': True},
        'historyPreserved': {'layer3': p06['layer3Preserved'], 'layer2': p06['layer2Preserved'],
                             'original25Layer1': p06['layer1Original25Preserved']},
        'populations': p06['populations'],
        'populationsUnchanged': p06['populationsUnchanged'],
        'groupsRun': [{'checker': x['checker'], 'rc': x.get('returncode'),
                       'lastLine': x.get('lastLine')} for x in p10['planningGroups']],
        'pinnedLauncher': p10.get('launcherReport')}}

R['authorPackageReview'] = {
    'status': 'INCOMPLETE — NOT ACCEPTED, NOT VERIFIED',
    'rootInputConsumed': {'file': 'author-package-update.json',
                          'sha256': p11['updateFileSha256'],
                          'status': p11['updateFile']['status'],
                          'namesAPackageManifest': p11['namesAPackageManifest']},
    'whyIncomplete': p11['package10Standing'],
    'package9Assessed': {'standing': 'assessed from preserved receipts; NOT rerun',
                         'genuineFailures': p11['genuineFailures'],
                         'expectedRefusalsNotFailures': p11['expectedRefusalsNotFailures'],
                         'finalVerificationJsonEmitted': p11['verificationJsonEmitted'],
                         'assessment': p11['assessmentOfPackage9']},
    'whatIWillDoWhenComplete': ('independently verify all 13 exact Run/control cases through BOTH '
                                'open_run_closure and close_run, then the 7 query checks, and record '
                                'any failure honestly. I will never remint as the independent reviewer.'),
    'retainedLimits': {
        'A10': ('TS checkpoint is helper-versus-owner only; the other six are owner-derived '
                'self-consistency; exists/none only with other operator limitations; the two-binding '
                'construction is incomplete with a single explicit binding; no compiler, provider or '
                'OS qualification.'),
        'A9': 'the repair controls retain their exact admitted-versus-unit limitations.'}}
json.dump(R, open(os.path.join(BASE, 'part1.json'), 'w'), indent=1, default=str)
print('part1 keys:', list(R))
