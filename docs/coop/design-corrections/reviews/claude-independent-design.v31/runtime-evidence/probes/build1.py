"""review.json part 1 — verification, ancestry, delta, corrections to my own v27 record,
and the substantive assessment of the five source-delta items."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
REC = os.path.join(BASE, 'receipts')


def rec(n):
    return json.load(open(os.path.join(REC, n)))


p00, p01, p02 = rec('p00-verify31.json'), rec('p01-delta.json'), rec('p02-pkgverify.json')
p03, p04 = rec('p03-planning31.json'), rec('p04-plandetail.json')
p18b = rec('p18b-f09enclosure.json')
p19 = rec('p19-suites31.json')
R = {}

R['review'] = ('Independent design review of consolidated product source31 — substantive '
               'exact-source successor review, continuing the same reviewer origin that produced '
               'the source26 CHANGES_REQUIRED and source27 ACCEPT reviews.')
R['origin'] = 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b'
R['sessionAncestry'] = {
    'sameOrigin': True,
    'priorReviews': [
        {'subject': 'source26', 'verdict': 'CHANGES_REQUIRED', 'standing': 'historical, immutable'},
        {'subject': 'source27', 'verdict': 'ACCEPT',
         'reviewSha256': '4cb03aa8438c07757bb67ee0fc8435fe1feae561ebb320b4b13d9451acc32ad2',
         'standing': 'historical and unchanged; not altered by this successor'}],
    'thisReview': 'source31',
    'notAutomaticPromotionOf27': True,
    'notAuthorAssistance': True}

R['subjectManifestSha256'] = p00['manifestSha256']
R['verifiedManifest'] = p00['ALL_VERIFIED']
R['manifestVerification'] = {
    'manifestPath': p00['manifestPath'],
    'manifestSha256': p00['manifestSha256'],
    'manifestShaMatchesDeclared': p00['manifestShaMatchesDeclared'],
    'archiveSha256': p00['archiveSha256'],
    'archiveShaMatchesDeclared': p00['archiveShaMatchesDeclared'],
    'declaredFiles': p00['declaredFileCount'], 'filesChecked': p00['filesChecked'],
    'everyRowHashAndSizeVerified': True,
    'declaredTotalBytes': p00['declaredTotalBytes'], 'measuredTotalBytes': p00['measuredTotalBytes'],
    'missing': p00['missingCount'], 'hashMismatches': p00['hashMismatchCount'],
    'sizeMismatches': p00['sizeMismatchCount'], 'extrasOnDisk': p00['extrasOnDiskCount'],
    'frozenDeviationsAfterAllRuns': p19['frozenDeviationsAfterRuns'],
    'ancestry': ('31 -> 30 -> 29 -> 28 -> 27, each step proven by the child manifest declaring the '
                 'parent manifest digest. The v27 link resolves to sha a1ae88ef..., which is exactly '
                 'the subject my prior review verified and graded.'),
    'ancestryChainVerified': p00['reaches27'] and p00['v27ShaIsTheOneIGraded']}

R['delta27to31'] = {
    'derivedByThisReview': True,
    'method': 'set difference over the five frozen manifests, per step and cumulatively',
    'added': p01['cumulative']['addedCount'], 'removed': p01['cumulative']['removedCount'],
    'changed': p01['cumulative']['changedCount'], 'touched': p01['cumulative']['touchedTotal'],
    'netBytes': p01['cumulative']['netBytes'],
    'addedPaths': [a['path'] for a in p01['cumulative']['added']],
    'changedPaths': [c['path'] for c in p01['cumulative']['changed']],
    'sameByteCountDigestOnlyEdits': [c['path'] for c in p01['cumulative']['changed'] if c['sameByteCount']],
    'perStep': {k: {'added': len(v['added']), 'removed': len(v['removed']), 'changed': len(v['changed'])}
                for k, v in p01.items() if k.startswith('step_')},
    'agreesWithRootListing': p01['agreesWithRoot'],
    'rootListingComparison': ('Root\'s source27-to31-delta.json names 16 paths. My independently '
                              'derived set is the same 16, with no removals: 2 added and 14 changed.'),
    'fileCounts': p01['fileCounts']}

R['authorPackageVerification'] = {
    'artifactManifestSha256': p02['artifactManifestSha256'],
    'matchesDeclared': p02['artifactManifestMatchesDeclared'],
    'declaredMembers': p02['declaredMembers'], 'verified': p02['verified'],
    'mismatched': p02['mismatched'], 'missing': p02['missing'],
    'extrasOnDisk': p02['extrasOnDisk'],
    'sourceManifestBindsExactFrozen31': p02['sourceManifestBindsExact31'],
    'nativeSchemaShaMatchesDeclared': p02['nativeSchemaMatchesDeclared'],
    'standing': ('AUTHOR-assisted evidence. Never a blind result. No row is graded from author '
                 'self-assessment and no expected output is treated as correctness evidence.')}

R['planningDecisions'] = {
    'standing': ('Reviewed in 26/27. I establish unchanged ancestry and current bindings rather than '
                 'proposing another plan. None of these files is in my 27->31 delta.'),
    'repositoryFileInventory': {'paths': p04['inventory']['files'],
                                'packages': p04['inventory']['packages'],
                                'directories': p04['distinctDirectories'],
                                'pendingDecisions': p04['inventory']['pendingDecisions'],
                                'changedIn27to31': False},
    'implementationCoverage': {'groups': p04['coverage']['groups'],
                               'mappings': 320,
                               'mappingsByGroup': {'commands': 45, 'queryOperations': 20,
                                                   'capabilityCells': 66, 'qualificationGates': 32,
                                                   'sharedFlags': 7, 'renderers': 5,
                                                   'workflowGoldens': 43, 'contractSections': 55,
                                                   'fallowConstraints': 15, 'hydraProposals': 8,
                                                   'reportFeatures': 24},
                               'milestoneOrder': p04['coverage']['milestoneOrder'],
                               'moduleFirstMilestoneRows': p04['coverage']['moduleFirstMilestoneCount'],
                               'changedIn27to31': False},
    'commitRecoveryCases': {'cases': p04['recoveryCases'], 'executed': 0, 'changedIn27to31': False},
    'qualificationGates': {'gates': p04['qualificationGates'], 'qualified': p04['gatesQualified'],
                           'demonstrated': p04['gatesDemonstrated'],
                           'harnessAuthored': p04['gatesHarnessAuthored'],
                           'standing': p04['gateStandings']},
    'normativeInputLayer2': {
        'path': p03['layer2Path'], 'sha256': p03['layer2Sha256'], 'pins': p03['layer2PinCount'],
        'everyPinResolvesAgainstFrozen31': p03['layer2AllPinsResolveAgainstFrozen31'],
        'changedIn27to31': p03['layer2ChangedIn27to31'],
        'originalV1LayerPreserved': p03['normativeInputsV1StillInFrozen31'],
        'previousArchitectureInputLayerNamed': p03['previousArchitectureInputLayerPresent'],
        'readingStanding': ('Read COMPLETELY via the Read tool in this session, all 145 lines and all '
                            '28 pinned inputs. In v27 this file was traversed programmatically only; '
                            'root\'s read-coverage measurement of that is correct and I do not '
                            'restate the v27 coverage claim.')}}

R['correctionsToMyOwnV27Record'] = [
    {'id': 'RR27-01', 'scope': 'review evidence wording, not source law',
     'rootFinding': ('F-09 said EXECUTION_INPUTS_COVERAGE_DERIVE is raised only inside load_coverage '
                     'and partitions_in_cell; it also occurs directly in the surrounding '
                     'coverage-account loop.'),
     'myMeasurement': p18b['correctedStatement'],
     'detail': {'raiseSites': p18b['raiseCount'],
                'innermostFunctionCounts': p18b['innermostCounts'],
                'enclosingFunction': p18b['enclosingFunction'],
                'partitionsInCellRaiseSites': 0,
                'method': ('AST enclosure, not the backwards-to-nearest-def heuristic the v27 probe '
                           'used; an intermediate indentation-extent pass of mine also mislabelled '
                           'six sites as module level and is preserved.')},
     'agreeWithRoot': True,
     'consequence': ('My v27 statement was wrong in both directions: it named a function with zero '
                     'raise sites and missed the enclosing loop that holds six of the seven. The '
                     'section 5 attribution is unaffected, because every site is coverage-account '
                     'derivation and execution-inputs-contract.v1.md section 5 is exactly '
                     '"Native Coverage accounts (derived)".'),
     'v27ReportAltered': False},
    {'id': 'RR27-02', 'scope': 'review record temporal consistency',
     'rootFinding': ('Several current scope/basis fields still described resolved source26 issues as '
                     'current although reassessmentFor27 said resolved: AR-09/14/15, FW-06, '
                     'DR-001/006/009/011-R10, DR-202; DR-202 also said carrier owners unchanged '
                     'although carrier files had changed.'),
     'agreeWithRoot': True,
     'howThisReportFixesIt': ('Every row below carries a CURRENT scope that describes source31 only. '
                              'Where a historical issue is worth naming, it is named in an explicit '
                              'historical field and never in the current scope. No row presents M-1, '
                              'S-1, S-2 or S-3 as an open condition of source31.'),
     'v27ReportAltered': False},
    {'id': 'RR27-03', 'scope': 'review owner change accounting',
     'rootFinding': ('ownerBytesChangedIn27=false was false at whole-file level for several '
                     'identity/security owners, because the template matched prose labels rather '
                     'than file paths.'),
     'agreeWithRoot': True,
     'howThisReportFixesIt': ('Every row names actual file paths and carries '
                              'ownerFilesChangedIn27to31 computed by set-membership against my '
                              'derived delta, with the changed files listed. Unchanged SECTION and '
                              'unchanged FILE are stated separately, and no blanket "no changed '
                              'owner paths" claim is made.'),
     'v27ReportAltered': False},
    {'id': 'RR27-04', 'scope': 'review record stale measurement',
     'rootFinding': 'DR-204 basis still said 12892 files and the v26 implementation-normative-inputs.v1 layer.',
     'agreeWithRoot': True,
     'myMeasurement': ('Frozen31 is %d files and %d bytes. The current architecture input layer is '
                       'implementation-normative-inputs.v2.json (28 pins, all resolving against '
                       'frozen31), and the original v1 layer is preserved in the snapshot and named '
                       'by implementation-planning-sources.v1.json as previousArchitectureInputLayer.'
                       % (p03['frozen31FileCount'], p03['frozen31TotalBytes'])),
     'v27ReportAltered': False},
    {'id': 'RR27-05', 'scope': 'review environment claim',
     'rootFinding': 'RES-EP13-11 said rg is not on this host; root executes rg successfully.',
     'agreeWithRoot': True,
     'myMeasurement': ('Measured in THIS session: rg resolves on PATH at %s and reports %s. My v27 '
                       'statement that the binary "is not on this host" was an unmeasured assertion '
                       'and was wrong. What remains true and is all I now claim: I did not execute '
                       'the two historical checkers, and their bytes are not members of the reviewed '
                       'snapshot.' % (p19['rgOnPath'], (p19.get('rgVersion') or [''])[0])),
     'v27ReportAltered': False}]

# ---------- the five source-delta items ----------
p05, p06, p06b = rec('p05-orderlaw.json'), rec('p06-replayorder.json'), rec('p06b-orderrows.json')
p07, p09b, p09c = rec('p07-nativecatalog.json'), rec('p09b-nativechecker.json'), rec('p09c-digestlaw.json')
p22b = rec('p22b-derivedrecompute.json')
p12, p13 = rec('p12-enumcontrols.json'), rec('p13-ax-originals.json')
p08 = rec('p08-recordpointers.json')

R['sourceDeltaAssessment'] = {
    'item1_source28_ruleResultsOrder': {
        'status': 'CORRECT AND COMPLETE',
        'ownerFiles': ['docs/coop/design-corrections/foundation/identity-model.v3.py',
                       'docs/coop/design-corrections/foundation/check-replay.v3.py',
                       'docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py'],
        'threeOwnersNowAgree': ('identity-model.v3.ordered line 156 keys ruleResults by '
                                "v['ruleId'].encode('utf8'); identity-schemas.v3 declares "
                                'x-opensip-order {"by":["ruleId"]}; evaluator-composition-contract.v3 '
                                'line 194 says "ruleResults has one item per policy rule, ordered by '
                                'ruleId UTF-8".'),
        'completenessCheckIRan': ('I enumerated all 57 x-opensip-order annotations. Exactly two carry '
                                  'an explicit {"by":[...]} key order - owner-source-set and '
                                  'ruleResults - and BOTH now have a named branch in ordered(). Zero '
                                  'explicit key orders are left falling through to the generic '
                                  'canonical-member order, so this is a complete fix, not a spot fix.'),
        'executedEvidence': {
            'frozenCheckerExit': p06['frozenRun']['returncode'],
            'correctOrderWholeRunAdmits': p06b['positiveAdmits'],
            'canonicalMemberOrderRefuses': p06b['canonicalOrderRefuses'],
            'duplicateRuleIdRefuses': p06b['duplicateRuleIdRefuses'],
            'refusalBoundary': 'published proof-bundle schema ordering/uniqueness',
            'refusalMessage': "array order {'by': ['ruleId']}: strict unique order required",
            'totalCheckerRows': p06b['totalRows']},
        'fixtureGenuinelyDiscriminates': ('check-replay.v3.py line 115 asserts rr != sorted(rr, '
                                          'key=C.canonical) with the comment "Control must '
                                          'distinguish both ordering recipes", so the fixture PROVES '
                                          'the two orders differ rather than assuming it. The late '
                                          'disabled rule z-disabled sorts after file-observed by '
                                          'ruleId and before it by canonical member order.'),
        'regressionReproducedByMe': {
            'method': ('In a disposable copy whose 1350 files I verified byte-equal to the frozen '
                       'manifest, I deleted the single ruleResults branch so the array falls back to '
                       'generic canonical order, and re-ran the same checker.'),
            'result': ('identity_canonical.AdmissionError: ORDER_OR_DUPLICATE raised from ordered() '
                       'during proof-bundle minting. The pre-28 reference could not even MINT a '
                       'lawfully ordered proof bundle, which is the contradiction source28 removes.'),
            'branchIsLoadBearing': p06['branchIsLoadBearing'],
            'falsePositiveIPreserved': p06['firstRunWasAFalsePositive']},
        'consumerMaterial': 'none supplied and none used'},
    'item2_source29_nativeRetentionCatalog': {
        'status': 'CORRECT AND MEASURED',
        'ownerFiles': ['docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
                       'docs/coop/design-corrections/native/check_native_evidence.v2.py',
                       'docs/coop/design-corrections/native/native-evidence-report.v2.json'],
        'nativeSchemaSha256': '3e37c7b7a6a620dcadc0aaed862eed242065ebd0ce9910da16faa25464f8b0b0',
        'structuredComparisonNotDiff': ('Most of the 37 KB growth is indentation, so I compared '
                                        'structured content: the declared vocabularies, every '
                                        'annotation site and its representation/retention, and the '
                                        'definition the new retention reuses.'),
        'measuredSites': {'syntactic': p07['syntacticSiteCount'],
                          'structural': p07['structuralSiteCount'],
                          'checkerReported': p09c['reportedAnnotationSites'],
                          'staleCountWas': 68,
                          'agreement': ('my syntactic count, my structural walk and the checker\'s own '
                                        'frozen report all say 76')},
        'derivedRetention': {
            'uses': p07['derivedSiteCount'],
            'paths': p07['derivedSitePaths'],
            'allUnderSourceUnitOwnershipV1': p07['derivedAllUnderSourceUnitOwnership'],
            'reusesExistingRecipe': ('UnitIdentityV1 and the native.compilation-unit.v1 domain were '
                                     'already defined in this bundle; derived recomputes '
                                     'H(native.compilation-unit.v1, UnitIdentityV1{schemaVersion, '
                                     'markerPath, targetKind, targetName}) and retains no separate '
                                     'preimage frame, so no unused fragment retention was added.'),
            'retainsNoPreimage': p07['derivedRetainsNoPreimage'],
            'enforcedNotAspirational': ('native_evidence_model.v2.source_unit_ownership_faults '
                                        're-derives every unitId and checks selectedUnitIds and '
                                        'ownership[].unitId membership in the same closed table - '
                                        'exactly the three positions the catalog names.'),
            'myEndToEndRecompute': {
                'identityStable': p22b['identityIsStable'],
                'injectiveOverItsFields': p22b['differentNameDifferentIdentity'],
                'hashInMarkerPathAdmitted': p22b['hashMarkerPathAdmitted'],
                'cleanRecordNoFaults': p22b['cleanFaults'] == [],
                'tamperedUnitIdNamed': p22b['tamperNamedByOwningFault'],
                'selectedMembershipEnforced': p22b['selectedMembershipEnforced'],
                'note': ('The # -in-markerPath case confirms the published rationale: H needs no path '
                         'restriction, unlike the earlier delimiter recipe that had to exclude "#".')}},
        'siteCountLaw': {'text': p07['siteCountLaw'],
                         'noSecondHandMaintainedTotal': p07['anyHandMaintainedTotalField'] == [],
                         'assessment': ('A measured count reported by the checker replaces a prose '
                                        'total. This is the same derive-do-not-transcribe rule the '
                                        'capability matrix already applies, and it is the right fix '
                                        'for a number that went stale.')},
        'vocabularyEnforcement': {
            'checkerPredicate': ('undeclared_retention / undeclared_representation are computed over '
                                 'every annotation site and are conjuncts of the pass condition; the '
                                 'offending paths are printed.'),
            'baselineClean': p09c['inMemoryBaseline']['undeclaredRetention'] == []
            and p09c['inMemoryBaseline']['undeclaredRepresentation'] == [],
            'decidableAndLoadBearing': p09c['lawIsDecidableAndLoadBearing'],
            'howIEstablishedIt': ('The schema and the checker are BOTH source-pinned, so mutating the '
                                  'schema answers PIN-MISMATCH before the digest-law check runs. I '
                                  'did not bypass that gate. I exercised the checker\'s exact '
                                  'predicate in memory over a mutated parsed copy instead: an '
                                  'undeclared retention names its site, an undeclared representation '
                                  'names its site, and removing `derived` from the catalog names '
                                  'exactly the three SourceUnitOwnershipV1 positions.'),
            'myEarlierFalsePositive': ('My first attempt read rc=2 from mutated runs as digest-law '
                                       'enforcement. It was PIN-MISMATCH. Both runs are preserved.')},
        'identitySchemasCurrent': {
            'digestLawNamesV3': True,
            'remainingV2RecordPointer': ('One annotation record pointer still names '
                                         'foundation/identity-schemas.v2.json#/$defs/owner-source-set. '
                                         'I resolved all three record pointers against frozen31: all '
                                         'resolve, and the v2 and v3 definitions of owner-source-set '
                                         '(and of import) are BYTE-IDENTICAL, so the legacy name binds '
                                         'the same record and there is no semantic divergence.'),
            'allRecordPointersResolve': p08['allPointersResolve']}},
    'item3_source30_coverageViewDigestRefresh': {
        'status': 'CONSISTENT ON CURRENT BYTES',
        'ownerFile': 'docs/coop/design-corrections/native/native-cases.v2.json',
        'shape': ('The 29->30 edit has an identical byte count with a different digest, which is the '
                  'signature of a fixed-width 64-hex digest swap and is consistent with one '
                  'coverageView schema digest being refreshed.'),
        'whatIVerified': ('The foundation drift guard that failed at source29 is satisfied on 31: '
                          'check-foundation, check-identity, check-integration and the native suite '
                          'all pass, and the evaluator3 launcher validates 1242 pins with 0 changed '
                          'or missing. No semantic law is changed by a fixture digest refresh.'),
        'limitOfMyEvidence': ('I could not diff the 29->30 bytes directly: the source29 and source30 '
                              'snapshots are not inputs to this review, and the source29 failed '
                              'receipt is not a member of frozen31. I therefore assess the CURRENT '
                              'state as consistent rather than certifying which single field moved. '
                              'That the source29 receipt was preserved and not accepted is an account '
                              'I did not verify against the failed artifact itself.'),
        'preservedFailedReceiptLocated': False},
    'item4_A4_enumerationRootControls': {
        'status': 'RESOLVED - meets the control gap I raised',
        'ownerFile': 'docs/coop/design-corrections/foundation/check-enumeration.v1.py',
        'myV27Advisory': ('A-4: the internal-root guard was enforced and correctly wired but was '
                          'exercised by 0 of 27 reference checkers.'),
        'nowMeasured': {'checkers': p12['checkerCount'],
                        'tokensNowExercised': {k: len(v) for k, v in p12['checkerHits'].items()},
                        'gapClosed': p12['a4GapClosed']},
        'executedControls': p12['unitRootCases'],
        'allFivePassed': p12['allFiveCasesPassed'],
        'positiveEmptyRootAdmitted': p12['positiveEmptyRootAdmitted'],
        'negativesRefuseOnlyTheRootFault': p12['negativesRefuseOnlyTheRootFault'],
        'membershipDigestRebinding': ('The control rebinds membershipDigest after changing the root '
                                      'spelling, so a digest mismatch cannot mask the root-specific '
                                      'refusal and root admission is genuinely reached. Without that, '
                                      'the control would prove nothing.'),
        'loadBearingProvedByMe': {
            'method': ('I disabled the _admit_membership_unit_roots call in a disposable verified copy '
                       'and re-ran the checker.'),
            'result': ('All four negatives fail. The two project-root cases then refuse with '
                       'ENUMERATION_BINDING_PROGRAM_ENTRY - the exact misattribution the original '
                       'F-04 defect was about - and the two member-root cases silently ADMIT. The '
                       'positive still passes, so the mutation is not simply breaking the fixture.'),
            'allFourNegativesFail': p12['allFourNegativesFailWithoutGuard'],
            'positiveUnaffected': p12['positiveStillPassesWithoutGuard']},
        'shapeAssessment': ('These are JOIN controls and the source says so in its own comment. I do '
                            'NOT insist on the structural-ADMIT-then-refuse shape my v27 advisory '
                            'suggested: admit_unit_roots runs at the enumeration join, which precedes '
                            'structural custody of a Run, so a structural-ADMIT claim here would be '
                            'misleading. My v27 suggestion presumed a shape that does not apply at '
                            'this boundary, and declining it is correct.'),
        'rootFirstExpectationPreserved': ('Root\'s initial assertion omitted the diagnostic suffix and '
                                          'is preserved beside the corrected one, which checks the '
                                          'exact prefix plus colon. The frozen file is the corrected '
                                          'version.')},
    'item5_A5_historicalArtifactsNowMembers': {
        'status': 'RESOLVED - evidence restored, nothing repaired',
        'addedPaths': ['docs/coop/artifacts/evaluation-proof.v13.json',
                       'docs/coop/artifacts/ep13.review-independent.json'],
        'myV27Advisory': ('A-5: AX6/AX9/MD5/RX2c preserved neither an inline original nor a title, '
                          'and both cited source artifacts had zero occurrences in the subject.'),
        'nowMeasured': {'bothInFrozen31': True,
                        'proposalSourceFieldsResolve': p13['allProposedSourcesResolve'],
                        'rowsStillWithoutInlineOriginal': ['AX6', 'AX9', 'MD5', 'RX2c']},
        'whatTheOriginalsSay': ('The original artifact declares escapedEveryGuard and '
                                'declaredBlindSpotVariants to be exactly AX6, AX9, MD5 and RX2c, out '
                                'of 29 variants declared and built with 25 caught by at least one '
                                'guard. It also sets escapeSetIsAMeasurementNotACoverageClaim and '
                                'aNarrowingIsNotAClosure to true. Each of the four residual accounts '
                                'is therefore a faithful restatement of its own original.'),
        'whatThisDoesNotDo': ('Reading the originals restores available evidence. It does not repair, '
                              'regrade, rerun or authenticate the original measurements, and no '
                              'historical file was edited. The four rows keep no inline original of '
                              'their own; the cited artifacts now supply it.')}}

json.dump(R, open(os.path.join(BASE, 'part1.json'), 'w'), indent=1)
print('part1 keys:', list(R))
