"""Assemble review.json for the bounded glob + repair-ownership technical review."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1'
REC = os.path.join(BASE, 'receipts')


def rec(n):
    return json.load(open(os.path.join(REC, n)))


v00, v01, v02 = rec('v00-verify.json'), rec('v01-schemadiff.json'), rec('v02-reconstruct.json')
v03, v04, v05 = rec('v03-callers.json'), rec('v04-fieldfilter-atoms.json'), rec('v05-atomdiff.json')
v06, v07 = rec('v06-pinstate.json'), rec('v07-rrsa1.json')
v08, v09 = rec('v08-rrsa2.json'), rec('v09-remedykey.json')
R = {}

R['review'] = ('Bounded read-only independent technical review of prospective successor bytes: '
               'portable glob semantics, and the repair-selection ownership question.')
R['sessionIdentity'] = {
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'role': 'independent reviewer; not a source author and not a coauthor',
    'continuity': ('Same actual Claude origin that produced the source26 CHANGES_REQUIRED, source27 '
                   'ACCEPT and source31 ACCEPT whole-design reviews. The source31 ACCEPT is preserved '
                   'and unchanged by this pass.'),
    'thisPassIs': ('a BOUNDED review of prospective successor bytes; NOT final-source acceptance, NOT '
                   'application acceptance, NOT a readiness statement'),
    'blindConsumerStatus': ('NOT a blind consumer: the repair input contains author code, which I read '
                            'deliberately. No blind consumer material was available or read.')}

R['verificationScope'] = {
    'statement': v00['verificationScope'],
    'source31ManifestSha256': v00['source31ManifestSha256'],
    'source31ManifestMatchesDeclared': v00['source31ManifestMatchesDeclared'],
    'whatIDidNotRepeat': ('the full 12895-row frozen31 sweep, the 107-row disposition assessment and '
                          'the complete reference suites; those belong to the source31 whole-design '
                          'review and this pass is bounded'),
    'globInputs': {'declaredChangedFiles': len(v00['globChanges']),
                   'allAfterHashesMatchDeclared': v00['allAfterHashesMatch'],
                   'everyBeforeImageEqualsFrozen31': v00['allBeforeImagesAreFrozen31'],
                   'beforeImagesResolveToFrozen31': v00.get('allBeforeImagesResolveToFrozen31'),
                   'sourceTreeVsFrozen31': v00['globSourceTree'],
                   'records': v00.get('globRecords')},
    'repairInputs': {'files': v00['repairReviewFiles'],
                     'standing': 'explicitly captured in-progress author bytes, per custody.json'}}

# ---------------- TASK 1 ----------------
R['globDisposition'] = {
    'verdict': 'NO SEMANTIC MISMATCH FOUND — the published law matches the unchanged reference',
    'scope': ('the five declared changes only; the deferred workflow chapter/projection links are '
              'acknowledged by the author and are NOT reported here as an undiscovered gap'),
    'changedFiles': [r['path'] for r in v00['globChanges']],
    'behaviourPreserved': {
        'matcherAlgorithmChangedClaim': False,
        'independentlyConfirmed': ('workflows_model.v1.py is not in the change set, and my '
                                   'differential test found the declared law and the unchanged '
                                   'reference to agree on every case tried'),
        'schemaEditsAreAnnotationOnly': {
            'workflowsCommon': {'addedLeaves': v01['workflows-common']['addedLeaves'],
                                'removedLeaves': v01['workflows-common']['removedLeaves'],
                                'changedLeaves': v01['workflows-common']['changedLeaves'],
                                'onlyChangedLeaf': '$/$defs/GlobPattern/description'},
            'evaluator3Common': {'addedLeaves': v01['evaluator3-common']['addedLeaves'],
                                 'removedLeaves': v01['evaluator3-common']['removedLeaves'],
                                 'changedLeaves': v01['evaluator3-common']['changedLeaves'],
                                 'onlyChangedLeaf': '$/$defs/GlobPattern/description'},
            'consequence': ('Admission is untouched: type, minLength, maxLength and the '
                            '^[^\\\\\\u0000]+(?![\\s\\S]) pattern are unchanged in both schemas, so '
                            'no pattern that was admissible becomes inadmissible or vice versa.')}},
    'reconstructabilityTest': {
        'method': ('I implemented the matching predicate FROM THE CONTRACT PROSE ALONE - split at '
                   'every literal /, ordinary segment matches one candidate segment in full, * is '
                   'zero-or-more scalars, ? is exactly one scalar, a segment that is exactly ** is '
                   'zero-or-more whole segments - and differential-tested it against the unchanged '
                   'workflows_model.v1.glob_match.'),
        'pairsTested': v02['differentialCasesTested'],
        'mismatches': v02['differentialMismatchCount'],
        'documentedExamples': len(v02['requiredExamples']),
        'documentedExamplesHoldInReference': v02['allRequiredExamplesHoldInReference'],
        'documentedExamplesHoldInMyReconstruction': v02['allRequiredExamplesHoldInMyReconstruction'],
        'namedEdgeCases': len(v02['edgeCases']),
        'referenceProseDivergences': len(v02['edgeDivergences']),
        'conclusion': v02['CONCLUSION']},
    'pointsAskedAboutExplicitly': {
        'leadingMiddleTrailingDoubleStar': 'verified in all three positions',
        'terminalFilenameConsumedByDoubleStar': "verified: '**' matches 'a.ts'; '**/*.ts' matches 'a.ts'",
        'zeroSegments': "verified: 'a/**/b' matches 'a/b'; '**/a' matches 'a'; 'a/**' matches 'a'",
        'anchoring': "verified: 'a' does not match 'ab'; 'b' does not match 'ab'; no implicit prefix or suffix",
        'scalarVersusGrapheme': ("verified BOTH directions: '?.ts' matches the single-scalar "
                                 "e-acute and does NOT match 'e' plus combining acute; '?' matches "
                                 "one astral scalar and '??' does not"),
        'literalBracesAndBrackets': ("verified: '[ab].ts' does not match 'a.ts' but matches "
                                     "'[ab].ts'; '{a,b}.ts' likewise; '[a-z]' does not match 'q'"),
        'emptySegments': ("verified: 'a//b' matches 'a//b' and not 'a/b'; trailing slash is an empty "
                          "final segment, so 'src/' does not match 'src' but does match 'src/'"),
        'scopeDocumentVersusStringFieldFilter': ('assessed separately below; both are covered and the '
                                                 'contract scopes its composition rule correctly')},
    'scopeDocumentComposition': {
        'contractClause': ('selected if at least one include matches and no exclude matches; '
                           'exclusion wins a matching inclusion'),
        'matchesInScope': v03['scopeCompositionMatchesContract'],
        'casesTried': v03['scopeDocumentCases']},
    'absentOrEmptyListDivergenceBetweenCallers': {
        'measured': ('in_scope (ScopeDocument) requires a matching include, so an EMPTY include '
                     'selects nothing; the enumeration filter at workflows_model.v1.py:1486 treats an '
                     'absent or empty include as no restriction. The two genuinely differ.'),
        'divergenceExists': v03['divergenceExists'],
        'assessment': ('NOT a defect in the contract. The contract states its composition rule for '
                       'ScopeDocument only and explicitly defers "their own defaults, absent/empty-list '
                       'behavior, and non-glob prefix predicates" to other owners. That deferral is '
                       'necessary and honest, and it is what keeps this from being a second dialect.')},
    'stringFieldFilterCoercion': {
        'observation': ("the caller dispatches cmp:glob as glob_match(x, str(v)), so the CALLER "
                        "applies str() even though the contract says the predicate does not coerce"),
        'checkIRan': ('validated {field, cmp:glob, value} against FieldFilter in both '
                      'policy-document.schema.json and policy-document.v2.schema.json for every '
                      'field in the enum'),
        'globAdmissibleOnIntegerValuedField': v04['strCoercionIsReachable'],
        'finding': ('cmp:glob is INADMISSIBLE on both integer-valued fields (confidenceMillionths in '
                    'both versions, exitStatus in v2), so under any admitted document the value '
                    'reaching str(v) is already a string and str() is a no-op. The contract\'s '
                    '"this predicate neither coerces values" is therefore accurate, and no reader '
                    'reconstructing FieldFilter glob semantics is misled. Not a mismatch.')},
    'atomContractAndChecker': {
        'contractEdit': ('one line: the atom contract no longer says glob "reuses '
                         'workflows_model.v1.glob_match" but points at the normative portable glob '
                         'contract, naming terminal ** and Unicode scalar matching. The dependency '
                         'direction is now correct: the law is normative and the reference implements it.'),
        'checkerFunctions': '%d -> %d' % (v05['functionCountBefore'], v05['functionCountAfter']),
        'newFunctions': v05['newFunctions'],
        'prescribedVectors': v05['prescribedVectorCount'],
        'vectorsDisagreeingWithUnchangedReference': len(v05['vectorsDisagreeingWithReference']),
        'contractTableRowsAlsoPresentAsVectors': '%d of %d parsed table rows'
                                                 % (v05['contractRowsAlsoInVectors'], v05['contractTableRows']),
        'atomUnitCasesInMyRuntime': {'returncode': v04['atomChecker']['returncode'],
                                     'authorReported': v04.get('authorReport'),
                                     'note': 'run in a disposable copy of the successor source in my runtime'}},
    'declaredRemainingWorkConfirmed': {
        'pinRefresh': ('confirmed and scoped: 4 of the 5 changed files appear in frozen31 pin ledgers '
                       '(%d entries), all of which would refuse until the ledgers are refreshed. This '
                       'is the author-declared "pin/planning refresh" item, not a new finding, and it '
                       'is why my atom run used a disposable copy.' % v06['pinsWouldRefuseCount']),
        'deferredWorkflowLinks': v00['deferredLinks'],
        'deferredLinksTreatment': ('acknowledged by the author and deferred until the separate repair '
                                   'coauthor releases ownership; NOT reported here as an undiscovered gap'),
        'authorDeclaredRemaining': v06['declaredRemaining']},
    'findings': [],
    'observations': [
        {'id': 'G-OBS-1',
         'text': ('The contract table annotates its two Unicode rows in prose outside the backticks '
                  '("(one scalar before the dot)"), so a naive table parser extracts 20 of the 22 data '
                  'rows. I verified all 22 by hand and by execution; this is a parsing nicety, not a '
                  'defect, and I raise no action on it.')},
        {'id': 'G-OBS-2',
         'text': ('The law is stated as a result definition and says so ("This defines results, not an '
                  'implementation algorithm or a requirement to use recursion"), which is the right '
                  'framing for a portable published law and is what made a clean-room reconstruction '
                  'possible.')}]}

# ---------------- TASK 2 ----------------
R['repairOwnershipDisposition'] = {
    'inputStanding': ('explicitly captured in-progress author bytes (4 files, custody.json). This is '
                      'NOT a final handoff, and the concurrently changing repair source was not read. '
                      'I do not claim final handoff reviewed and this is not acceptance.'),
    'RRS_A1': {
        'question': ('does a path-owning selected available symbol program or candidate-only binding '
                     'exist independently of source-path Coverage scopes, such that the proposed '
                     'selector can omit a relevant universe?'),
        'answer': 'YES — root\'s finding is CONFIRMED',
        'ownerCitations': v07['ownerCitations'],
        'decisiveSentence': v07['decisiveSentence'],
        'reasoning': v07['FINDING']['why'],
        'structuralProof': {
            'measured': ('the captured selector module contains ZERO occurrences of extents, '
                         'candidateSourcePaths, EnumerationPlan or programBindings; it reads only '
                         'subject_scopes(), filtered to the three source-path relations'),
            'sourcePathRelations': v07['sourcePathRelations'],
            'consequence': ('the retained EnumerationPlan - the normative carrier of program-to-path '
                            'ownership, and a required evaluator3 replay parameter - is not consulted '
                            'at all, so ownership can only ever be seen through a source-path relation '
                            'scope that happens to exist in this Run')},
        'scopedProbe': {
            'scope': v07['probeScope'],
            'asymmetricCase': v07['asymmetricCase'],
            'controlWithSourcePathScope': v07['controlWithSourcePathScope'],
            'controlUnownedPathStaysTyped': v07['unownedIsTyped'],
            'explicitlyNot': ('not a full admitted Run, not a reminted graph, not an executed '
                              'end-to-end bypass. Root states no full-Run counterexample exists for '
                              'this asymmetric case and I constructed none; I do not claim one.')},
        'evidenceClass': v07['FINDING']['evidenceClass'],
        'unavailableAndNullUniverseAccounting': {
            'whatTheOwnerSays': ('enumeration-contract.v1.md L28: an UNAVAILABLE binding has '
                                 'universe=null, deficiency and nativeCause, and "extents still '
                                 'populated from host membership so expected file/package paths are '
                                 'not lost". L125: the unavailable-program symbol extent is the '
                                 'membership-fallback code extent, "never arbitrary caller paths", and '
                                 'file/package candidate extents are compared to binding.extents '
                                 'BEFORE the U-available branch.'),
            'howItShouldBeAccounted': ('An unavailable selected binding whose retained extent contains '
                                       'an unsafe edited path has a real, retained expected ownership '
                                       'claim but no universe to make eligible and no Coverage to '
                                       'establish a closed world. It must therefore produce a TYPED '
                                       'UNRESOLVED OWNERSHIP outcome - the same non-vacuous treatment '
                                       'the module already gives an unowned path - and must not '
                                       'disappear because some other universe is a favourable known '
                                       'owner. Silently satisfying the gate from the available owner '
                                       'alone is exactly the asymmetry RRS-A1 names.'),
            'boundariesToPreserve': [
                'union the available owning universes from the applicable extents and candidate census; '
                'do not collapse legitimate multiple ownership',
                'do not infer unselected programs: enumeration-contract L34 says the host does not '
                'invent extra programs from filenames, and L125 says the symbol extent is '
                'owner-admitted selected paths',
                'do not treat all snapshot files as every compiler programRootFiles: file extent is '
                'first-party scoped membership, symbol extent is the selected code scope only - they '
                'are different extents and must stay distinct',
                'source-path scopes may add a retained ownership witness but cannot by themselves '
                'certify owner completeness',
                'every available relevant universe must still retain gate evidence; imported '
                'observations and optional unsigned maps remain non-authoritative',
                'no symbol parsing and no reconstruction of a path from an opaque native symbol ID']},
        'whereIAgreeWithRootsFraming': ('Root is right that the draft\'s subjectKindLaw argument proves '
                                        'those scopes NAME paths but not that they ENUMERATE every '
                                        'selected program owning a path, and right that the '
                                        'opaque-symbol-ID point answers a different question from the '
                                        'retained program extent.'),
        'disposition': ('SUBSTANTIVE NORMATIVE GAP CONFIRMED in the captured draft. The remedy '
                        'direction root gives - union over the retained selected-program census with '
                        'typed unresolved ownership for unsafe paths under unavailable bindings - is '
                        'consistent with the frozen31 owner as I read it.')},
    'RRS_A2': {
        'point1_sentinelWording': {
            'request': 'describe the five-field least-closed sentinel consistently in the create-only paragraph',
            'measured': ('workflows-and-surfaces.md (captured) line 812 calls it "the fixed all-unknown '
                         'value", but the sentinel defined at lines 789-795 of the same document, and '
                         'EMPTY_DISPLAY_SUMMARY at module lines 95-101, is entryPointsRecognized="none" '
                         'and nonliteralLoading="present" with only exportsClosed and '
                         'externalConsumers "unknown".'),
            'assessment': 'CONFIRMED — a real internal inconsistency, wrong on 2 of the 5 fields',
            'status': 'unmet in the captured bytes'},
        'point2_authoritativeBoolean': {
            'request': "the display's boolean must not be called authoritative anywhere",
            'measured': ('module line 87 comment: "`deadCodeRepairEligible=false` is the authoritative '
                         'part". That is the occurrence root names.'),
            'assessment': 'CONFIRMED present; conflicts with full native selection being the authority',
            'status': 'unmet in the captured bytes'},
        'point3_summaryVersusEligibility': {
            'request': ('explain, or coherently define, how the descriptor summary may differ from '
                        'eligibility when a relevant universe has no Coverage, without making the '
                        'summary a native record'),
            'measured': ('the gate paragraph (lines 663-669) does state non-vacuity and mints '
                         'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED, and the module emits a per-universe '
                         'uncovered remedy; what is not stated is how the five-field DISPLAY reduction '
                         'incorporates that absence.'),
            'assessment': 'root\'s request stands; the gate is handled, the summary/absence relation is not stated',
            'status': 'partially addressed in the captured bytes'},
        'point4_orderingPublication': {
            'request': ('publish UTF-8 byte ordering and the key member sequence: relation, resolution, '
                        'sourceUniverse, targetUniverse, subjectScopeCommitment, coverage identity'),
            'measured': {'moduleOrdersByBytesInCode': v09['usesEncodeForOrdering'],
                         'utf8NamedInModuleProse': v09['utf8NamedInModuleProse'],
                         'utf8NamedInContractProse': v09['utf8NamedInContractProse'],
                         'coverageKeyPublishedAs': ('CoverageKeyV2 (relation, resolution, '
                                                    'sourceUniverse, targetUniverse, '
                                                    'subjectScopeCommitment) - five members, in both '
                                                    'the module header and the contract prose')},
            'assessment': ('the CODE already orders by encoded bytes, so this is a publication gap, not '
                           'a behaviour change: UTF-8 byte ordering is named nowhere in prose, and the '
                           'published key is the five-member CoverageKeyV2 without the coverage '
                           'identity root asks to be sixth'),
            'status': 'unmet in the captured bytes'},
        'point5_remedyNamesTheActualRecord': {
            'request': 'include the exact coverage identity or full key so the remedy names the actual retained record',
            'measured': ('the dissent remedy at module lines 375-379 is built from relation, '
                         'resolution, sourceUniverse and reasons only. I constructed two records '
                         'differing in targetUniverse, subjectScopeCommitment AND coverage identity '
                         'and ran that exact construction: the remedy text is BYTE-IDENTICAL.'),
            'demonstration': v09['twoDistinctRecords'],
            'assessment': 'CONFIRMED — two lawfully distinct retained records are indistinguishable in the remedy',
            'status': 'unmet in the captured bytes'},
        'disposition': ('All five wording requests are well founded against the captured bytes. Four '
                        'are unmet and one is partially addressed. Points 1, 2 and 5 are concrete '
                        'internal inconsistencies or ambiguities I reproduced directly; point 4 is a '
                        'publication gap over already-correct behaviour.')}}

R['limitations'] = [
    'Bounded read-only pass. Not final-source acceptance, not application acceptance, not a readiness '
    'or freeze statement.',
    'I did not author source and am not a coauthor. No live edit, no product implementation, no commit '
    'or push.',
    'The repair input is explicitly captured in-progress author bytes. The concurrently changing repair '
    'source was not read, and I do not claim any final handoff was reviewed.',
    'The repair input contains author code, which I read deliberately, so I am NOT a blind consumer for '
    'this material. No blind consumer material was available or read.',
    'RRS-A1 rests on static normative completeness plus a unit-scoped selector probe. No full admitted '
    'Run counterexample was constructed and none is claimed; root states the same.',
    'My glob differential test is a very large but finite sample over a generated alphabet plus the '
    'documented and named edge cases. It is strong evidence of equivalence, not a proof over all '
    'strings.',
    'The glob deferred workflow chapter and projection links were not assessed; they are '
    'author-acknowledged and awaiting the separate repair coauthor.',
    'Pin ledgers and planning records are not refreshed for the glob change set, which the author '
    'declares as remaining work; pinned checkers therefore refuse on those files until integrated freeze.',
    'This bounded pass did not repeat the frozen31 full-manifest sweep, the 107-row disposition '
    'assessment or the complete reference suites.']

R['grantsNothing'] = {
    'architectureReady': False, 'finalSourceAcceptance': False, 'applicationAcceptance': False,
    'blindAcceptance': False, 'implementationAuthorized': False, 'coauthorship': False,
    'stillRequired': ['integrated freeze', 'final independent source review',
                      'successful original blind reconstruction', 'application review']}

json.dump(R, open(os.path.join(BASE, 'review.json'), 'w'), indent=1, default=str)
print('wrote review.json bytes=%d keys=%d' % (os.path.getsize(os.path.join(BASE, 'review.json')), len(R)))
print('glob verdict :', R['globDisposition']['verdict'])
print('RRS-A1       :', R['repairOwnershipDisposition']['RRS_A1']['answer'])
