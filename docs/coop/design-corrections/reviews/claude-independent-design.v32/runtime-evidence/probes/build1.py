"""review.json part 1 — verification, delta, source-change assessment, record corrections."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v32'
REC = os.path.join(BASE, 'receipts')


def rec(n):
    return json.load(open(os.path.join(REC, n)))


p00, p01, p02 = rec('p00-verify32.json'), rec('p01-delta.json'), rec('p02-inputs.json')
p03, p04b, p04c = rec('p03-v31record.json'), rec('p04b-ordering.json'), rec('p04c-ordering.json')
p05, p06 = rec('p05-repairlaw.json'), rec('p06-changedchecks.json')
p07, p08 = rec('p07-fixture-glob-planning.json'), rec('p08-planningdetail.json')
p09, p10 = rec('p09-package8.json'), rec('p10-verify-a8.json')
p11, p12c = rec('p11-crossowner.json'), rec('p12c-cellorder.json')
p13 = rec('p13-pins-planning.json')
R = {}

R['review'] = ('Independent design review of exact frozen consolidated product source32, continuing '
               'the same reviewer origin. Integrated successor bytes assessed on their own evidence.')
R['sessionIdentity'] = {
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'role': 'independent reviewer; I have authored no source in this lineage and am not a coauthor',
    'notAForbiddenAcceptor': ('I am none of the five forbidden source-author origins '
                              '(eaa8276c…, 36a89be8…, 0aa529b3…, 329a5132…, 919c766d…). Author SID '
                              '919c766d is a coauthor of these bytes and is not an independent acceptor.'),
    'priorReviews': [{'subject': 'source31', 'verdict': 'ACCEPT', 'standing': 'historical, unchanged'},
                     {'subject': 'bounded glob/repair review', 'standing': 'historical, unchanged'}],
    'neitherPriorReviewAcceptsTheseBytes': True,
    'blindConsumerPolicy': ('No consumer runtime, output or report was listed or opened. consumer-b* '
                            'directories were excluded by name from every inventory I ran. I make no '
                            'blind acceptance claim.')}

R['subjectManifestSha256'] = p00['manifestSha256']
R['verifiedManifest'] = p00['ALL_VERIFIED']
R['manifestVerification'] = {
    'manifestSha256MatchesDeclared': p00['manifestMatchesDeclared'],
    'archiveSha256MatchesDeclared': p00['archiveMatchesDeclared'],
    'declaredFiles': p00['declaredFileCount'], 'filesChecked': p00['filesChecked'],
    'declaredTotalBytes': p00['declaredTotalBytes'], 'measuredTotalBytes': p00['measuredTotalBytes'],
    'missing': p00['missingCount'], 'hashMismatches': p00['hashMismatchCount'],
    'sizeMismatches': p00['sizeMismatchCount'], 'extras': p00['extrasCount'],
    'archiveEqualsManifest': p00['archiveEqualsManifest'],
    'archiveMemberRows': p00['archiveFileRows'],
    'ancestry': ('source32 declares parentManifestSha256 ca713db5…, which is exactly the frozen31 '
                 'manifest my prior review verified and graded.'),
    'parentIsMyV31': p00['parentIsMyV31'],
    'frozenDeviationsAfterAllRuns': p13['frozenDeviationsAfterRuns']}

R['delta31to32'] = {
    'derivedByThisReview': True,
    'added': p01['addedCount'], 'removed': p01['removedCount'], 'changed': p01['changedCount'],
    'touched': p01['touched'], 'netBytes': p01['netBytes'],
    'addedPaths': [a['path'] for a in p01['added']],
    'changedPaths': [c['path'] for c in p01['changed']],
    'rootInventoryComparison': ('root-delta31-to32.json was not present at the path named in my '
                                'instruction nor at the reviews top level, so I could not compare '
                                'against it. My delta is derived independently from the two frozen '
                                'manifests and does not depend on it; root\'s listing is an inventory '
                                'and would not have been approval in any case.'),
    'rootInventoryLocated': False}

R['verificationScopeOfInputs'] = {
    'liveReviewInputsHashed': {k: len(v) for k, v in p02.items() if isinstance(v, list)},
    'excludedByPolicy': p02['excludedByPolicy']}

# ---------------- source change assessment ----------------
R['sourceChangeAssessment'] = {
    'change1_repairClosedWorldSelectionOwner': {
        'status': 'SUBSTANTIVELY CORRECT, CONSERVATIVE AND COMPLETE FOR ITS STATED SCOPE',
        'newOwner': 'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
        'publishedLaw': 'docs/v2/contracts/product-v1/workflows-and-surfaces.md section 6',
        'whatIVerifiedByExecution': p05,
        'findings': [
            'The ownership census now reads the retained EnumerationPlan, not source-path scopes. '
            'In my asymmetric unit case the symbol-extent owner uB is returned, which the source31 '
            'draft omitted. That closes the gap my bounded review confirmed as RRS-A1.',
            'candidateSourcePaths counts as ownership and is reported with its own extent kind.',
            'A selected but UNAVAILABLE binding (universe=null) yields typed unresolved ownership '
            'carrying its deficiency, and an available closed owner of the same path does NOT '
            'discharge it — I verified both halves.',
            'An unselected binding contributes to neither bucket: unselected programs are not inferred.',
            'file / package / symbol extents stay distinct per binding, and an unrelated path is not '
            'in any census, so all snapshot files are not treated as every compiler programRootFiles.',
            'source-path scopes are demoted to an ADDITIONAL witness and are unioned, never treated '
            'as an owner-completeness certificate.',
            'Coverage selection is on sourceUniverse alone and is independent of the plan '
            'evidenceRequirements, so a recipe cannot narrow the evidence set.',
            'The conjunction is non-vacuous: an uncovered relevant universe, an unowned path and an '
            'unresolved unavailable owner each produce REPAIR.CLOSED_WORLD_NOT_ESTABLISHED, and the '
            'display reduction folds absence so it cannot read closed while eligibility is refused.',
            'Remedies now name all six ordering members unabbreviated including the retained '
            'coverage2 identity, so two lawfully distinct records are distinguishable — the exact '
            'defect I reproduced in my bounded review.'],
        'crossOwnerConsistency': p11['chapterModuleConsistency'],
        'allChapterClaimsPublished': p11['allChapterClaimsPresent'],
        'schemaAnnotations': {k: p11[k] for k in ('repairV1', 'repairEvaluator3') if k in p11},
        'nativeChapterLink': p11['nativeChapterLink'],
        'modelSeam': {'v1': p11['seam_v1']['importsSelectionOwner'],
                      'v3': p11['seam_v3']['importsSelectionOwner'],
                      'note': 'workflows_model.v3 exposes closed_world_selection()/evaluator3_closed_world '
                              'and records that the historical major-1 profile keeps its own behaviour'},
        'fixtureExtension': {'optionDefaultIsFalse': p07['optionDefaultIsFalse'],
                             'filesNamingTheOption': [f['path'] for f in p07['filesNamingTheOption']],
                             'guarded': p07.get('optionIsGuarded'),
                             'evidenceThatExistingCallersAreUnaffected':
                                 'check-replay.v3.py and check-workflow-projection.v3.py both exit 0 '
                                 'with the option unset on every existing caller'},
        'cellOrdinalQuestionIRaisedAndResolved': {
            'concern': 'the module derives cellOrdinal with enumerate(), but the enumeration contract '
                       'says cellOrdinal is the index AFTER the published sort and is not stored',
            'resolution': p12c['CONCLUSION'],
            'outcome': 'NO FINDING'}},
    'change2_completedAuthorV2AndRootScopeCorrection': {
        'status': 'READ AND ASSESSED',
        'inputsHashed': True,
        'authorIsCoauthorNotIndependent': True,
        'rootReadScopeDisclosed': ('root states it read the entire selector and prose/handoff but did '
                                   'NOT claim all 174 KB of checker lines or the whole structured '
                                   'author JSON. I treat root\'s six suite results and summaries as '
                                   'evidence to assess, not authority, and my conclusions rest on my '
                                   'own execution.'),
        'myPosition': ('My bounded review confirmed RRS-A1 and all five RRS-A2 points against the '
                       'older captured draft. Measured against these integrated bytes, every one of '
                       'those concerns is resolved in the published law and in the module behaviour '
                       'I executed.')},
    'change3_RRSA3EvidenceScope': {
        'status': 'HONESTLY SCOPED — no narrow reference correction needed',
        'whatIChecked': [
            'The asymmetric control is built from a FULL ADMITTED Run: fixture -> '
            'admit_coverage_result_v3 -> identity-model close_run complete semantic replay, and the '
            'checker asserts the runId starts with run3:.',
            'The empty-target derivation is labelled in the source comment as isolating path '
            'ownership only and explicitly "not a lawful repair request (targets requires '
            'minItems=1)".',
            'The comment states that the sole matched finding belongs to the symbol universe so a '
            'legal target already reaches it under the earlier target-occurrence join, and concludes '
            '"This control does not prove a lawful old-preview bypass."',
            'The projection control now uses actual NONEMPTY targets (CW_ASYM_FPS) with a check '
            'asserting they are nonempty.',
            '_cw_preview carries its own docstring limit: the tree/project/snapshot/trust/requirements '
            'adapter is historical fixture data not derived from the Run, the inherited constructor '
            'emits a major-1 descriptor, and it "demonstrates gate integration only, not current '
            'descriptor admission or snapshot joins".',
            'UNIT controls are labelled as such in their ids, and the unavailable/candidate-only '
            'controls state that the frozen fixture builds no such binding.'],
        'myAssessment': (
            'The bounded design/reference evidence is sufficient for what it claims and is honestly '
            'scoped. The claims that were overstated in the earlier author prose are precisely the '
            'ones the current source retracts in its own comments. I do not report invalid adapter '
            'input as a product bypass, because it is not one: an empty-target derivation and a '
            'major-1 synthetic descriptor are invalid or historical inputs, not a demonstrated '
            'lawful path through current law. I also do not demand a product repair implementation '
            'as a design acceptance prerequisite.'),
        'narrowReferenceCorrectionNeeded': False,
        'whyNot': ('The boundary is not materially misleading: the limit is stated in three separate '
                   'places (the section scope header, the asymmetric control comment, and the '
                   '_cw_preview docstring), and the one control that could have been read as a '
                   'bypass now runs with real nonempty targets.')},
    'change4_portableGlobContract': {
        'status': 'ONE COHERENT NORMATIVE READING ACROSS ALL SIX OWNERS',
        'newOwner': 'docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md',
        'ownersLinking': {k: v['namesGlobContract'] for k, v in p07['globOwnerLinks'].items()},
        'mainChapterLinkIsNew': p07['mainChapterNowLinks'],
        'mainChapterText': p07['globOwnerLinks']['mainChapter']['sample'],
        'matcherUnchanged': ('workflows_model.v1.py changed for the repair seam, but the matcher '
                            'itself is not what changed: my bounded review differential-tested the '
                            'published law against the implementation over 5,927,922 pairs with zero '
                            'mismatches, and that evidence is inherited here under exact-byte '
                            'verification of glob-pattern-contract.v1.md, whose sha is unchanged '
                            'from the bounded review input.'),
        'inheritedEvidenceStanding': ('My bounded review was NOT a blind prose-only origin: I had '
                                      'author and reference code in front of me. The differential '
                                      'result stands as reference-level equivalence evidence, not as '
                                      'a blind reconstruction.')},
    'change5_planning': {
        'status': 'CONSISTENT; NO NEW PACKAGE OR PLANNED FILENAME',
        'existingModulesCarryTheWork': [
            'crates/evaluator/src/policy.rs — owns the pure portable glob predicate used by evaluator '
            'filters and host policy/repair scope checks',
            'crates/host/src/repair.rs — derives relevant program ownership and native closed-world '
            'eligibility from retained evidence'],
        'counts': {'paths': p08['paths'], 'packages': p08['packages'],
                   'coverageMappings': p07['coverageMappings'],
                   'milestoneOrder': p07['milestoneOrder'],
                   'plannedRecoveryCases': 54, 'recoveryCasesExecuted': 0},
        'countsUnchanged': p08['countsUnchanged'],
        'layer3': {'pins': p07['layer3']['pins'], 'binds29': p07['layer3Binds29'],
                   'allPinsResolveAgainstFrozen32': p07['layer3AllPinsResolve'],
                   'layer2Preserved': p07['layer2Preserved'],
                   'originalLayer1Preserved': p07['layer1Preserved']},
        'referencePyIsNotANormativeInput': {
            'layer3ContainsTheGlobContract': p08['layer3HasGlobContract'],
            'layer3ContainsTheRepairPyModule': p08['layer3HasRepairReferenceModule'],
            'anyPyFilesInLayer3': p08['pyFilesInLayer3'],
            'assessment': ('layer3 carries the glob CONTRACT and contains zero .py files at all, so '
                           'the repair reference module is pin-only and is correctly not treated as a '
                           'normative input.')},
        'pinLedgers': {k: {'entries': v['entries'], 'glob': v['hasGlobContract'],
                           'repairModule': v['hasRepairModule']}
                       for k, v in p07['pinLedgers'].items()},
        'allFiveLedgersCarryBothNewOwners': p07['allFiveLedgersCarryBothNewOwners'],
        'chapter14': {'sha256': p08['chapter14Sha256'],
                      'linesTouchingNewWork': p08['chapter14LinesTouchingNewWork'][:4]},
        'coverageVerificationMethods': ('commands/19 now names the section-6 retained-program path '
                                        'census, all matching target occurrences, unavailable owners '
                                        'and the non-vacuous conjunction, and rejects recipe-selected '
                                        'evidence narrowing. I did not have the v31 bytes of '
                                        'implementation-coverage.v1.json in this runtime, so I state '
                                        'what the current methods say rather than certifying that '
                                        'exactly two changed.')}}

# ---------------- record corrections ----------------
R['correctionsToMyOwnV31Record'] = [
    {'id': 'RR31-01', 'rootFinding': 'all 16 DR-011-R01..R16 rows had currentOwnerFiles=[] while '
                                     'RR27-03 claimed every row names actual file paths',
     'verifiedByMe': p03['RR31_01'],
     'agree': True,
     'howFixedHere': ('Every one of the 16 DR-011-R rows below now carries real current owner paths '
                      'and selectors, with changed/unchanged accounting derived from my 31->32 delta. '
                      'Layers and cited historical attachments are accounted separately from '
                      'normative owners.'),
     'v31ReportAltered': False},
    {'id': 'RR31-02', 'rootFinding': 'RES-EP13-13 noted check-replay.v3.py changed since 27 but its '
                                     'readingStanding still said same bytes, re-verified byte-equal',
     'verifiedByMe': p03['RR31_02'], 'agree': True,
     'howFixedHere': ('That row now separates the UNCHANGED normative law from the CHANGED file, and '
                      'its standing states which is inherited and which was read fresh. No generic '
                      'inherited label is applied to newly attached historical artifacts, which were '
                      'not present in the v27 or v31 sessions at all.'),
     'v31ReportAltered': False},
    {'id': 'RR31-03', 'rootFinding': "A-7's reason said the native schema file is not in the 27->31 "
                                     'delta, but it is; the POINTER is unchanged and the v2 '
                                     'definitions are byte-identical to v3',
     'verifiedByMe': p03['RR31_03'], 'agree': True,
     'howFixedHere': ('The scope sentence is corrected: the native schema FILE did change in that '
                      'window; what is unchanged is the record POINTER, and the definitions it binds '
                      'are byte-identical between v2 and v3. No source defect was demonstrated then '
                      'or now, and I select no cosmetic repoint or schema-digest churn.'),
     'v31ReportAltered': False},
    {'id': 'RR31-04', 'rootFinding': 'the source29/30 failure and delta evidence is now supplied; the '
                                     'earlier suggestion to supply the 29/30 manifests was imprecise '
                                     'because those manifests were already used',
     'agree': True,
     'myOwnInspection': p10['a8'],
     'howFixedHere': ('I inspected the supplied bundle directly. native-cases.v2.json for source29 and '
                      'source30 have the SAME byte count and differ in EXACTLY ONE leaf — '
                      '$/fixtures/coverageView/schemaDigests/0 — from 673a9bf8… to 3e37c7b7…, both '
                      '64-hex, and both files are bound by the bundled 29/30 manifests. The failed '
                      'source29 receipt is preserved AS A FAILURE: passed=false with '
                      'sourcePinsValid=true and checksExecuted=true, so the drift guard genuinely '
                      'fired. This is NEW CUSTODY supplied to me now; it is not retro-authentication '
                      'of the original transition, and I do not claim to have witnessed that '
                      'transition. A-8 was an honest reviewer-input limit and is now discharged.'),
     'v31ReportAltered': False},
    {'id': 'RR31-05', 'rootFinding': 'the report said the enumeration join precedes structural custody, '
                                     'but open_run_closure runs before derive reaches admit_enumeration',
     'agree': True,
     'myOwnMeasurement': {'staticCallSites': {'openRunClosureCall': p04b['openRunClosureCallLine'],
                                              'deriveCall': p04b['deriveCallLine'],
                                              'structuralFirst': p04b['structuralPrecedesDeriveCorrected']},
                          'tracedCallOrder': p04c['observedOrder'],
                          'replayResult': p04c['replayOut']},
     'howFixedHere': ('Corrected and proven by execution: tracing an actual fixture replay gives the '
                      'order open_run_closure -> derive -> admit_enumeration -> '
                      'compare_complete_replay. Structural custody runs FIRST. The consequence root '
                      'draws is also right: a structural-ADMIT-then-semantic-REFUSE construction is '
                      'therefore not inherently impossible, so I do not claim it is, and the existing '
                      'join-only controls remain adequate for their claimed scope. I demand no '
                      'whole-Run replacement controls.'),
     'v31ReportAltered': False},
    {'id': 'RR31-06 (wording limit)',
     'rootFinding': 'finite hash controls show distinct hashes for finitely changed inputs, not '
                    'mathematical injectivity of SHA-256 over all inputs',
     'agree': True,
     'howFixedHere': ('Accepted and applied throughout: where I report identity-distinctness evidence '
                      'it is stated as a measured finite control, never as global injectivity.'),
     'v31ReportAltered': False},
    {'id': 'RR31-07 (my own bounded-review correction)',
     'selfIdentified': True,
     'what': ('My bounded glob/repair review demonstrated the remedy-ambiguity point with a '
              'hand-built pair that used pseudo IDs and an unequal source/target universe on a '
              'same-only file relation. Those two rows would not both be lawfully admitted records, '
              'so that particular construction did not demonstrate two lawfully admitted records.'),
     'whatSurvives': ('The structural finding does survive and is what root accepted: the old remedy '
                      'text was built from relation, resolution, sourceUniverse and reasons only, so '
                      'it could not name the actual retained record. source32 fixes exactly that by '
                      'naming all six ordering members including the coverage2 identity, which I '
                      'verified by execution.'),
     'v31ReportAltered': False}]

json.dump(R, open(os.path.join(BASE, 'part1.json'), 'w'), indent=1, default=str)
print('part1 keys:', list(R))
