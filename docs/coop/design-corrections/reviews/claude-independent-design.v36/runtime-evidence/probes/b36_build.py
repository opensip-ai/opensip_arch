"""B36 — build the COMPLETE source36 review.json from the complete source35 baseline, the focused totality assessment and my
own source36 receipts. Every baseline field of every row (including all *On33/*On34/*On35 fields) is preserved verbatim as
history; source36 facts are added in *On36 / *35to36 fields; owner arrays come from the two manifests; every claim points at
a receipt and every gating claim is asserted against it before anything is written."""
import hashlib, json, os, time

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
RC = os.path.join(BASE, 'receipts')
V35 = '/tmp/opensip-design-corrections/claude-independent-design.v35'
FOC = '/tmp/opensip-design-corrections/claude-dependency-totality-assessment.v1'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
DSA = '/tmp/opensip-design-corrections/claude-dependency-scope-author.v1'
TOA = '/tmp/opensip-design-corrections/claude-dependency-totality-author.v1'
ROOTP = '/tmp/opensip-design-corrections/root-source36-prose-completion.v1'
ROOTREF = '/tmp/opensip-design-corrections/root-final36-reference.v1'
ROOTPLAN = '/tmp/opensip-design-corrections/root-final36-planning-checks.v1'
CODEX = os.path.join(REV, 'codex-post-reset.v1/final-reference.v36')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


shaif = lambda p: sha(p) if os.path.isfile(p) else None
rc = lambda n: json.load(open(os.path.join(RC, n)))
r00, r01, r04, r05, r08 = (rc(n) for n in ('r00-custody.json', 'r01-diffs.json', 'r04-suites.json', 'r05-package13.json', 'r08-rows.json'))
p01, p02, p03, p04, p05, p06, p07, p08 = (rc(n) for n in ('p01-totality36.json', 'p02-determinism36.json', 'p03-history-runtime36.json', 'p04-package-reach.json',
                                                         'p05-package-lineage.json', 'p06-reference-compare.json', 'p07-package-member-diffs.json',
                                                         'p08-planning-population.json'))
p09 = rc('p09-milestones.json')
BL = json.load(open(os.path.join(V35, 'review.json')))
FJ = json.load(open(os.path.join(FOC, 'review.json')))
m36 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v36.json')))['files']}
m35 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v35.json')))['files']}
DELTA = sorted(c['path'] for c in r00['delta']['changed'])
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
        'scopedReviewOwnerDispositions')
PC = p01['checks']
HC = p03['checks']

# ------------------------------------------------------------------ gating assertions (a failure stops the build)
assert r00['manifestShaMatchesDeclared'] and r00['archiveShaMatchesDeclared'] and r00['archiveEqualsManifest'] and r00['matchesDeclared']
assert r00['missing'] == r00['hashMismatches'] == r00['sizeMismatches'] == r00['extras'] == r00['duplicateManifestPaths'] == 0
assert r00['freezeAgrees'] and r00['parentNamedIsSource35'] and r00['manifest35IsMyAcceptedSource35'] and r00['noParentOmission']
assert r00['delta']['counts'] == {'added': 0, 'removed': 0, 'changed': 10, 'unchanged': 12889} and r00['parentBytesExtractedAndVerified']
assert r01['baselinesMatch'] and r01['checkAtomsExistingCasesBodiesUnchanged'] == []
assert all(v['onlyDigestPairsChanged'] and v['everyNewDigestIsTheFrozen36DigestOfAChangedFile'] for v in r01['pinLedgers'].values())
assert r01['layer4']['unchanged'] and r01['layer4']['pins'] == 29 and r01['layer4']['pinsResolveAgainst36'] == 29 and not r01['layer4']['pinnedPathsInDelta']
assert all(r01['planningOwnersUnchanged35to36'].values())
assert not p01['failedChecks'] and not p01['errors'] and len(PC) == 37
assert not p03['failedChecks'] and len(HC) == 15
assert p02['passed']
assert r04['allJobsExitZero'] and r04['checkAtoms']['passed'] == 101 and not r04['checkAtoms']['failed'] and r04['frozen36DeviationsAfterRuns'] == 0
assert r04['regeneratedWorkflowsReportEqualsFrozen36'] and not r04['disposableFilesRewrittenByCheckers'] and r04['disposableCopied'] == r04['disposableVerified']
assert r04['launcherReport']['sourcePinsValid'] and r04['launcherReport']['passed'] and len(r04['launcherReport']['children']) == 16
assert r05['matchesDeclaredManifest'] and r05['matchesRootVerifiedManifest'] and r05['verified'] == r05['declaredMembers'] == 323 and not r05['mismatched'] and not r05['missing']
assert r05['sourceManifestEqualsFrozen36'] and r05['bindingNamesFrozen36'] and r05['bindingParentIsPackage12'] and r05['constructionProvenance']['mixed33TS30NormalizedRust']
assert r05['allThirteenAsExpected'] and r05['allExportsEqualPackage12'] and r05['queryChecks'] == 7 and r05['verification']['passed']
assert r05['myGroupsObservedAndReportDigestsMatchRoot'] and r05['queryAssessment']['passed'] and r05['frozen36DeviationsAfter'] == 0 and r05['packageDeviationsAfter'] == 0
assert r05['residualAssessment']['bindsFrozen36'] and r05['residualAssessment']['rows'] == 30 and r05['residualAssessment']['grades'] == ['PENDING'] and r05['residualAssessment']['tcbDependents'] == 13
assert p05['package12IsTheOneIVerified'] and p05['allExportsByteEqualPackage12Files'] and p05['provenanceUnchangedFrom12']
assert all(v['equal'] for v in p05['constructionAccountsIdenticalToPackage12'].values()) and not p05['package12To13']['removed']
assert p05['package12To13']['changedCommon'] == ['README.md', 'evaluation-residual-author-assessment.json', 'source-manifest.json', 'verify-package.py']
assert p07['sourceManifests']['package13IsFrozen36'] and p07['residualAssessmentChangedValueKinds'] == ['resolveAgainst', 'standing', 'subjectManifestSha256']
assert p07['textDiffs']['verify-package.py']['plus'] == p07['textDiffs']['verify-package.py']['minus'] == 1
assert not p04['summary']['anyRuntimeOrHistoryAtom'] and not p04['summary']['anyReachabilityAtom'] and not p04['summary']['anyIncomingEndpointAtom']
assert p06['identityCountsAgree'] and p06['evaluatorChildren']['equalNamesAndExits'] and p06['rootGroupSourcesEqualFrozen36'] and p06['myIdentityReportEqualsRootBytes']
assert r08['baselineMatches'] and r08['countsMatchExpected'] and not r08['rowsWithOwnerIn36Delta'] and len(r08['legacyCorrections']) == 9 and r08['rowsAllOwnersEqual35and36'] == 107
assert r08['historical35ClassCheck']['matches91_11_5'] and r08['authorityFlagsFalseOn35']
assert p08['inventory']['topLevelListLengths'] == {'packages': 20, 'files': 198, 'pendingDecisions': 9} and p08['coverage']['topLevelListLengths']['milestoneOrder'] == 7
assert all(v['unchanged35to36'] for v in p08['owners'].values())
assert sha(os.path.join(FOC, 'review.json')) == '4df5fb241d74ec6c3ac15271234b704c7fa2a451149100dcba926e3c2994a421'

# law derived before testing
starts = {}
for d in sorted(os.listdir(RC)):
    cj = os.path.join(RC, d, 'command.json')
    if os.path.isfile(cj):
        starts[d] = json.load(open(cj))['startedUtc']
law = os.path.join(BASE, 'law-derivation36.json')
law_written = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(law)))
first_semantic = min(v for k, v in starts.items() if k.split('.')[0] in ('p01_totality36', 'p02_determinism36', 'p03_history_runtime36'))
assert law_written <= first_semantic
codex_ref = {'codexReferenceChecksEqualsRootBound': shaif(os.path.join(CODEX, 'reference-checks.json')) == shaif(os.path.join(ROOTREF, 'reference-checks.bound.json')),
             'codexRunnerOriginalEqualsRootReferenceChecks': shaif(os.path.join(CODEX, 'runner-original-reference-checks.json')) == shaif(os.path.join(ROOTREF, 'reference-checks.json'))}
chk = lambda name: PC[name]['passed']
E = lambda sec: p01[sec]
J = {}

J['review'] = 'Independent whole design/reference review of exact frozen consolidated product source36'
J['verdict'] = 'ACCEPT'
J['verdictScope'] = ('Design and reference bytes of source36 only. Grants no application outcome, architecture readiness, activation, implementation '
                     'authorization, blind acceptance, package acceptance, product qualification, residual grade, commit or push.')
J['subjectManifestSha256'] = r00['manifestSha256']
J['currentSubject'] = {'manifestPath': os.path.join(REV, 'candidate-subject.v36.json'), 'manifestSha256': r00['manifestSha256'],
                       'archivePath': os.path.join(REV, 'candidate-source.v36.tar.gz'), 'archiveSha256': r00['archiveSha256'],
                       'snapshot': '/tmp/opensip-design-corrections/candidate-subject.v36', 'fileCount': r00['declaredFiles'],
                       'totalBytes': r00['measuredTotalBytes'], 'parentManifestSha256': r00['manifest35Sha256'],
                       'manifestStanding': r00['manifestMeta'].get('standing')}
J['verifiedManifest'] = True
J['sessionIdentity'] = {
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'role': 'independent design/reference reviewer, actual Claude; I authored no byte of source36',
    'notAForbiddenAcceptor': BL['sessionIdentity']['notAForbiddenAcceptor'],
    'notTheSourceAuthors': ('823bf66b-e92a-4789-ab81-63a1a9dc371d authored the dependency-scope and dependency-totality corrections and is not an '
                            'independent acceptor; root authored the later prose/registry/docstring completion and the pin re-sealing. I am neither.'),
    'overlapWithCandidateAuthorship': {
        'myExploratoryRemedyDisclosed': ('In claude-dependency-totality-assessment.v1 (review.json 4df5fb24) I classified the same-kind partial dependency census '
                                         'as a reference defect, wrote in-process prototypes A (drop a non-total same-kind position) and B (the same over an '
                                         "attestation's named scopes), proposed contract wording, and recommended precision for root's history-order and "
                                         'runtime-polarity texts. No byte of any source tree was written by me.'),
        'finalBytesAreNotMine': ('Measured (receipts/p01-totality36.json X1): the final _select_dep_coverages still contains the unpatched text my prototype '
                                 'replaced, my prototype A/B code is absent, my proposed contract wording is absent, and the final atom_model is byte-for-byte '
                                 "the totality author's after file (E14a). The adopted law is the author's two-view sufficiency, which differs from my prototype."),
        'conceptualCoincidence': ('The final law shares the principle of my finding (every owed subject must be covered) and an equivalent attestation owed '
                                  'set (owned-scope subjects, which by admission equal scopeRefs subjects). The totality author reports not reading my '
                                  'in-progress assessment; root read my completed assessment.'),
        'rootTextImplementsMyPrecision': ('Root\'s registry historySubjectOrder.duplicatePaths ("No merge or pick rule is conferred; repair targetSubjectProjection '
                                          'keeps its own ambiguity refusal"), the observabilityFilter disclosure text and the contract Runtime polarity paragraph '
                                          'implement precision items I recommended. For those items my confirmation is owner verification plus measurement, '
                                          'not independent origination, and should be weighted accordingly.'),
        'standingNotClaimed': 'No fresh blind standing, no consumer-reconstruction standing and no application-review standing is claimed.'},
    'blindPolicy': 'No consumer input, output, diagnosis, report, root blind control or expected result was read or used; consumer-custody package members were hashed for custody only.',
    'priorRecordsHistoricalUnchanged': BL['sessionIdentity']['priorRecordsHistoricalUnchanged'] + [
        {'path': 'claude-independent-design.v35/review.json', 'sha256': r01['baselines']['v35ReviewJson'], 'mdSha256': r01['baselines']['v35ReviewMd'],
         'standing': 'ACCEPT on source35; the complete baseline of this review'},
        {'path': 'claude-dependency-totality-assessment.v1/review.json', 'sha256': r01['baselines']['focusedReviewJson'], 'mdSha256': r01['baselines']['focusedReviewMd'],
         'standing': 'bounded focused assessment; not source acceptance; findings re-tested here on final bytes'}],
    'notResurrected': 'Source34 CHANGES_REQUIRED and source33 ACCEPT stay historical; root bounded assessments and author reports are not whole-design assent.'}
J['baselineRecord'] = {
    'complete35': {'path': 'claude-independent-design.v35/review.json', 'sha256': r01['baselines']['v35ReviewJson'],
                   'expected': 'd7dc035c532968df80334809815f1257a49b83fd47f880e3a89630df9669cd52', 'mdSha256': r01['baselines']['v35ReviewMd'],
                   'matches': True, 'baselineVerdict': BL['verdict']},
    'focusedTotality': {'path': 'claude-dependency-totality-assessment.v1/review.json', 'sha256': r01['baselines']['focusedReviewJson'],
                        'expected': '4df5fb241d74ec6c3ac15271234b704c7fa2a451149100dcba926e3c2994a421', 'mdSha256': r01['baselines']['focusedReviewMd'],
                        'matches': True, 'decision': FJ['dependencyTotality']['decision']}}
J['manifestVerification'] = {k: r00[k] for k in ('manifestSha256', 'manifestShaMatchesDeclared', 'archiveSha256', 'archiveShaMatchesDeclared', 'declaredFiles',
                                                 'walkedFiles', 'measuredTotalBytes', 'missing', 'hashMismatches', 'sizeMismatches', 'extras', 'duplicateManifestPaths',
                                                 'archiveMemberRows', 'archiveDistinctRows', 'archiveHashMismatches', 'archiveEqualsManifest', 'matchesDeclared',
                                                 'freezeAgrees', 'parentNamedIsSource35', 'manifest35IsMyAcceptedSource35', 'archive35IsTheSource35IVerified',
                                                 'noParentOmission', 'parentBytesExtractedAndVerified')}
J['manifestVerification']['receipt'] = 'receipts/r00-custody.json'
SUB = ['docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md', 'docs/coop/design-corrections/foundation/atom_model.v1.py',
       'docs/coop/design-corrections/foundation/check-atoms.v1.py', 'docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json']
J['delta35to36'] = {
    'derivedFrom': 'the frozen35 and frozen36 manifests (parent bytes from the archive-verified frozen35 extraction)',
    'added': 0, 'removed': 0, 'changed': 10, 'unchanged': r00['delta']['counts']['unchanged'], 'netBytes': r00['delta']['netBytes'],
    'changedFiles': r00['delta']['changed'],
    'substantive': {p: {k: r01['files'][p][k] for k in ('lines35', 'lines36', 'plus', 'minus', 'diffSha256')} for p in SUB},
    'digestRebindingOnly': sorted(p for p in DELTA if p not in SUB),
    'contractSections': r01['contractSections'], 'contractBoldLabelsAdded': r01['contractBoldLabelsAdded'],
    'modelTopLevel': r01['files'][SUB[1]]['topLevel'], 'checkerTopLevel': r01['files'][SUB[2]]['topLevel'],
    'checkerExistingCaseBodiesChanged': r01['checkAtomsExistingCasesBodiesUnchanged'],
    'modelDiffReading': ('Exactly: removal of the _select_dep_coverages mapping fallback (with its docstring), the new _dependency_totality_gaps, '
                         "run_suff's second sufficiency evaluation on the gap-removed view, and the three gap call sites (outgoing, attestation view, "
                         'per-scope incoming). I1, P1/P2, pairing, selection order, the fold and _result are byte-untouched.'),
    'registryJsonPathDelta': p03['registryJsonPathDelta'],
    'pinLedgers': r01['pinLedgers'], 'workflowsReport': r01['jsonPathChanges']['docs/coop/design-corrections/workflows/workflows-report.v1.json'],
    'rootInventoryAgreement': r00['rootInventory'], 'receipts': ['receipts/r00-custody.json', 'receipts/r01-diffs.json', 'receipts/diffs/']}
bp = p01['byteProvenance']
J['authorshipOfFinalBytes'] = {
    'dependencyScopeAuthor': {'origin': '823bf66b-e92a-4789-ab81-63a1a9dc371d', 'runtime': DSA,
                              'reviewMd': shaif(DSA + '/review.md'), 'reviewJson': shaif(DSA + '/review.json'),
                              'bytes': {'contract': bp['atom-evaluation-contract.v1.md']['authorBefore'], 'model': bp['atom_model.v1.py']['authorBefore'],
                                        'checker': bp['check-atoms.v1.py']['authorBefore']},
                              'finalStanding': 'intermediate: none of the three is a final36 byte; the fallback removal survives unchanged into final36'},
    'dependencyTotalityAuthor': {'origin': '823bf66b-e92a-4789-ab81-63a1a9dc371d', 'runtime': TOA, 'reviewMd': shaif(TOA + '/review.md'),
                                 'reviewJson': shaif(TOA + '/review.json'), 'resultJson': shaif(TOA + '/result.json'),
                                 'bytes': {'contract': bp['atom-evaluation-contract.v1.md']['authorAfter'], 'model': bp['atom_model.v1.py']['authorAfter'],
                                           'checker': bp['check-atoms.v1.py']['authorAfter']},
                                 'finalStanding': 'atom_model is FINAL (E14a); contract and checker were later changed by root'},
    'rootLater': {'record': os.path.join(ROOTP, 'assessment.json'), 'recordSha256': shaif(os.path.join(ROOTP, 'assessment.json')),
                  'changes': ['contract %s -> %s (final): dependency-paragraph "contributes no pairing / occupies no position only when no selected Coverage remains"; '
                              'regrouping consequence qualified; Empty and different-kind boundaries paragraph; Runtime polarity paragraph'
                              % (bp['atom-evaluation-contract.v1.md']['rootBefore'][:8], bp['atom-evaluation-contract.v1.md']['rootAfter'][:8]),
                              'check-atoms %s -> %s (final): one docstring; AST equal ignoring docstrings (E14c)' % (bp['check-atoms.v1.py']['rootBefore'][:8], bp['check-atoms.v1.py']['rootAfter'][:8]),
                              'evaluator-projection-registry %s -> %s (final): historySubjectOrder.order text, uniqueKey removed, duplicatePaths added; '
                              'importQuantifiers.polaritySetR.observabilityFilter text' % (bp['evaluator-projection-registry.v1.json']['rootBefore'][:8], bp['evaluator-projection-registry.v1.json']['rootAfter'][:8])],
                  'rootDesignAssent': False, 'pinsAndGeneratedReport': 'five pin ledgers and workflows-report.v1.json: digest re-pinning only (r01)'},
    'verified': {k: PC[k]['passed'] for k in PC if k.startswith('E14') or k.startswith('T1')},
    'standing': 'I reviewed and executed the FINAL frozen36 bytes; author reports describe intermediate contract/checker bytes and are evidence I assessed, not conclusions I adopted.'}
J['lawDerivedBeforeTesting'] = {'file': 'law-derivation36.json', 'sha256': sha(law), 'writtenUtc': law_written, 'firstSemanticProbeStartedUtc': first_semantic,
                                'writtenBeforeAnySemanticProbe': law_written <= first_semantic,
                                'predictionsMet': 'all fourteen expectation groups E1-E14 held; E2 and E8 held in their qualified forms as written'}

# ------------------------------------------------------------------ resolved issues
res = [dict(x) for x in BL['resolvedIssues']]
for x in res:
    if x['id'] == 'MUST-34-01':
        x['statusOn36'] = ('Remains CLOSED on 36: the 35->36 model diff does not touch the I1 lines; the I1 controls are among check-atoms 101/101 on frozen36 '
                           '(receipts/r04-suites.json, r01-diffs.json).')
e10, e2, e3 = E('E10'), E('E2'), E('E3')
res += [
    {'id': 'A-13', 'status': 'CLOSED ON SOURCE36',
     'law': 'contract section 4: a coverageScopes entry naming a scope outside the exact dependency (relation, rung, S) contributes no pairing, whether or not an exact scope exists; a dependency occupies no position only when no selected Coverage remains',
     'reference': 'atom_model _select_dep_coverages: the mapping fallback branch is deleted (receipts/diffs/...atom_model.v1.py.diff)',
     'evidence': {'frozen35HealedMutationRows': len(p01['E10-healedOnFrozen35']), 'mutationRowsPerEndpoint': 10,
                  'final36EveryMutationEqualsDependencyAbsentOnBothEndpoints': chk('E10a-A13-every-non-exact-mapped-scope-is-absent-on-both-endpoints-final36'),
                  'exactScopeStillPairsBesideMappedNonExactScope': chk('E10c-exact-scope-still-pairs-beside-a-mapped-non-exact-scope'),
                  'final36EqualsDependencyScopeSuccessorOnEveryRow': chk('E10d-final36-equals-depscope-on-every-A13-row (totality changes nothing here)')},
     'standing': 'atom-api (synthetic inputs). It was advisory on 35 because close_run already excluded the shape for retained Runs; that exclusion is unchanged.',
     'receipts': ['receipts/p01-totality36.json']},
    {'id': 'TOT-1', 'title': 'Same-kind partial dependency census, incoming per scope', 'origin': 'dependency-scope author review section 8 observation; my focused assessment',
     'status': 'CLOSED ON SOURCE36',
     'evidence': {k: chk(k) for k in ('E1a-final36-every-missing-shape-unknown-for-all-covered-none-count', 'E1b-final36-missing-shapes-answer-required-relation-missing',
                                      'E1c-final36-f-actual-dependency-stays-cited-when-present', 'E1d-final36-full-covers-true-no-deficiency-unrelated-h-uncited',
                                      'E1e-frozen35-and-depscope-answered-true-on-merged-missing-shapes (defect reproduced)')},
     'receipts': ['receipts/p01-totality36.json']},
    {'id': 'TOT-2', 'title': 'Whole-source attestation view had the same defect', 'origin': 'my focused assessment (p04 there)', 'status': 'CLOSED ON SOURCE36',
     'evidence': {'values': {l: E('E6')[l]['final36']['value'] for l in E('E6')}, 'defectReproducedOnFrozen35AndDepscope': chk('E6b-frozen35-depscope-attestation-f-only-was-true (defect reproduced)')},
     'receipts': ['receipts/p01-totality36.json']},
    {'id': 'TOT-3', 'title': 'Regrouping (merged vs split primary partitions)', 'status': 'CLOSED, WITH ROOT\'S QUALIFICATION CONFIRMED',
     'evidence': {'valueNeverChanges': chk('E2a-final36-regrouping-never-changes-the-value'),
                  'completeEntriesEqualCauses': chk('E2b-final36-complete-entry-shapes-equal-causes-and-deficiencies'),
                  'rootCounterexampleReproduced': PC['E2c-root-counterexample-reproduced-split-adds-a-per-view-carrier-value-unchanged'],
                  'perViewCarrierDivergencePredatesTotality': PC['E2d-per-view-carrier-divergence-predates-totality (frozen35 split vs merged with two partial carriers)']},
     'receipts': ['receipts/p01-totality36.json']},
    {'id': 'TOT-4', 'title': 'Known-match and count dominance under a totality gap', 'status': 'HOLDS ON SOURCE36',
     'evidence': {'final36': {o: E('E5')['f-only']['final36'][o]['value'] for o in E('E5')['f-only']['final36']}, 'fullCover': {o: E('E5')['f-and-g']['final36'][o]['value'] for o in E('E5')['f-and-g']['final36']}},
     'receipts': ['receipts/p01-totality36.json']},
    {'id': 'TOT-5', 'title': 'Empty source program: Coverage and attestation routes differ', 'status': 'SPECIFIED ON SOURCE36 AS A BOUNDED PROFILE DECISION; COHERENT (advisory A-15 on one generic sentence)',
     'evidence': {k: E('E8')[k]['final36']['value'] for k in E('E8')}, 'unchangedFrom35': chk('E8d-empty-behaviour-unchanged-frozen35-to-final36'),
     'receipts': ['receipts/p01-totality36.json']},
    {'id': 'TOT-6', 'title': 'Different-kind whole-source dependency (clones->declares)', 'status': 'SPECIFIED ON SOURCE36 AS A BOUNDED PROFILE DECISION; COHERENT',
     'evidence': {k: E('E9')[k]['final36']['value'] for k in E('E9')}, 'unchangedFrom35': chk('E9-different-kind-whole-source-unchanged-and-unchecked'),
     'receipts': ['receipts/p01-totality36.json']},
    {'id': 'TOT-7', 'title': 'Registry historySubjectOrder contradicted the duplicate-preserving sequence law', 'status': 'CLOSED ON SOURCE36',
     'evidence': {k: HC[k]['passed'] for k in HC if k.startswith('H')}, 'receipts': ['receipts/p03-history-runtime36.json']},
    {'id': 'TOT-8', 'title': 'Runtime polarity quantifier law was registry-only', 'status': 'CLOSED ON SOURCE36',
     'evidence': {k: HC[k]['passed'] for k in HC if k.startswith('R')}, 'receipts': ['receipts/p03-history-runtime36.json']},
    {'id': 'TOT-9', 'title': 'Cause and citation channels, deterministic ordering', 'status': 'HOLDS ON SOURCE36',
     'evidence': {'partialCarrierRetained': chk('E3a-final36-retains-partial-carrier-deficiency-and-citation-beside-required-relation-missing'),
                  'outgoingUnchanged': chk('E4-outgoing-identical-frozen35-depscope-final36-in-value-causes-citations'),
                  'insertionOrders': E('E11'), 'processes': {k: p02['processes'][k] for k in ('distinctOrders', 'distinctDigests', 'errors')}},
     'receipts': ['receipts/p01-totality36.json', 'receipts/p02-determinism36.json']}]
J['resolvedIssues'] = res

# ------------------------------------------------------------------ advisories
adv = {a['id']: dict(a) for a in BL['advisories']}
adv['A-9']['statusOn36'] = 'Carried with limits intact: the repair owners are byte-identical 35->36; the registry history text now states that repair targetSubjectProjection keeps its own ambiguity refusal (H1/H3); admitted-versus-unit limits retained.'
adv['A-10']['statusOn36'] = ('Carried, limits unchanged, measured on package13: all 13 exports and claims files byte-equal to package12 (and so package11/10); '
                             'mixed construction (TS groups on 33, normalized/Rust on 30); construction accounts byte-equal; TS helper-versus-owner only; six '
                             'self-consistency; exists/none only; incomplete two-binding construction with a single explicit binding; no compiler/provider/OS qualification.')
adv['A-11']['statusOn36'] = 'Historical; not reopened.'
adv['A-12']['statusOn36'] = 'Historical, closed on 35; its scope-less/empty-scope boundaries still hold on 36 (E8c references) and its carrier refusals are unchanged (E7b).'
adv['A-13']['statusOn36'] = 'CLOSED ON SOURCE36 (see resolvedIssues A-13): the fallback is deleted; 20/20 frozen35-healed rows are absent on both endpoints.'
adv['A-13']['closureOn36'] = {k: v for k, v in res[-10]['evidence'].items()} if res[-10]['id'] == 'A-13' else None
e7 = E('E7')
a14 = {'id': 'A-14', 'title': 'The attestation-route totality check newly pairs owed-subject dependency scopes, so a failing carrier now refuses',
       'selectors': ['atom_model.v1.py _dependency_totality_gaps (called from the attestation branch of _native_completeness)',
                     'atom-evaluation-contract.v1.md section 4: "covered ... contains it and pairs at least one Coverage"; "a selected scope that fails the subject-scope carrier is refused ATOM_NATIVE_CARRIER when paired"'],
       'measured': {k: {m: e7[k][m]['value'] for m in ('frozen35', 'depscope', 'final36')} for k in e7},
       'why_not_a_should': ('Consistent with the published pairing rule and conservative: it is a global admission refusal, the Coverage route already refused '
                            'the same scope on frozen35 (E7b), scopes holding no owed subject are not paired on either route, and close_run admits every '
                            'retained subject-scope object, so no retained Run can carry such a scope.'),
       'gap': 'No section 9 case and no check-atoms control names the attestation-route refusal; a successor should pin it rather than leave it incidental.',
       'standing': 'atom-api', 'statusOn36': 'NEW on 36; informational', 'receipt': 'receipts/p01-totality36.json E7'}
e8 = E('E8')
a15 = {'id': 'A-15', 'title': 'Admitted-inputs item 1 states the empty-program closure generically; for a relation with a same-kind dependency the Coverage alternative never closes',
       'selectors': ['atom-evaluation-contract.v1.md section 4 Admitted inputs item 1 (lines 242-246): "The admitted way for an empty selected program to close incoming is an explicit scope2 record ... paired with complete S->U Coverage or named by a qualifying attestation"',
                     'section 4 Empty and different-kind dependency boundaries (lines 306-316)',
                     'section 9: "an explicit empty-subject scope with complete Coverage or a qualifying attestation closes it" (its control uses references, which has no dependency); "merged and split partitions answer alike"'],
       'measured': {k: e8[k]['final36']['value'] for k in e8},
       'why_not_a_should': ('No unsound result and no unresolved conflict: the source36 boundary paragraph is the specific, explicitly labelled profile rule and '
                            'states the conservative Coverage-route result and the attestation-route difference; the generic sentence names an admitted '
                            'shape and says it qualifies no provider. A reader of only the generic sentence could close an empty reachability program via '
                            'Coverage where the reference answers unknown: a lenient-versus-conservative conformance difference, never a false result from '
                            'the reference.'),
       'recommendedWording': ('Item 1: after "paired with complete S->U Coverage or named by a qualifying attestation" add "; this closes the search account '
                              'only, and dependency sufficiency still applies, so for a relation with a same-kind dependency the Coverage route stays '
                              'conservative (see Empty and different-kind dependency boundaries)". Section 9: "merged and split partitions answer alike" -> '
                              '"answer alike in value".'),
       'statusOn36': 'NEW on 36; textual precision', 'receipt': 'receipts/p01-totality36.json E8'}
J['advisories'] = [adv['A-9'], adv['A-10'], adv['A-11'], adv['A-12'], adv['A-13'], a14, a15]
J['newMustIssues'] = []
J['newShouldIssues'] = []

# ------------------------------------------------------------------ source change assessment
J['sourceChangeAssessment36'] = {
    'dependencyTotalityLaw': {
        'assessment': ('Correct, conservative and precisely placed. The owed set per view is exactly the primary partition that view evaluates; covered means '
                       'an exact selected scope contains the subject and pairs a Coverage at the evaluated target, reusing the one selection/pairing law; a '
                       'present gap position is evaluated twice (actual view and gap-removed view) and satisfaction needs both, so the removed position '
                       'answers required-relation-missing exactly as native sufficiency_v2 step 1 answers an absent relation (native_evidence_model.v2.py '
                       'sufficiency_v2 recurses DEPENDS_ON to depth 4). It is required by native RC-4 ("over the same examined set"), atom section 4 "No '
                       'fictional complete entries" and identity section 3 ("complete" is a claim about the examined partition).'),
        'evidence': {k: chk(k) for k in PC if k[:2] in ('E1', 'E4', 'E5', 'E6', 'E1')}, 'receipt': 'receipts/p01-totality36.json'},
    'twoViewVersusMyPrototype': {
        'assessment': ('The author\'s two-view law is the better correction and supersedes my focused prototype. Both give unknown on every gap. Two-view '
                       'retains what the evaluation actually read: the partial partition\'s deficiency (input-closure-incomplete), its typed carrier '
                       '(coverage-unknown nativeCause lockfile-missing) and its citation, beside required-relation-missing. My prototype A answers exactly the '
                       'no-dependency result, discarding that deficiency, carrier and citation (E3b), and A without B still answers true on the attestation '
                       'route (E3c). Native section 4.6 says what is retained is "the evidence the evaluation read ... with its own deficiency and nativeCause '
                       'carrier", atom section 4 cites "every folded partition", and required-relation-missing has no entry carrier (native deficiency table), '
                       'so no truthful alternative nativeCause exists for the gap. frozen36 check-atoms fails four totality controls under A and under A+B (E12c).'),
        'causesAndCitations': {'final36': e3['coverage-route/f-unknown+g-uncovered']['final36'], 'protoA': e3['coverage-route/f-unknown+g-uncovered']['protoA'],
                               'protoAB': e3['coverage-route/f-unknown+g-uncovered']['protoAB'],
                               'attestationRouteCompleteF': {m: e3['attestation-route/f-complete+g-uncovered'][m]['value'] for m in ('final36', 'protoA', 'protoAB')}},
        'checkerUnderPrototypes': {m: [f['case'] for f in E('E12')[m]['failed']] for m in ('protoA', 'protoAB')}, 'receipt': 'receipts/p01-totality36.json E3/E12'},
    'regroupingQualification': {
        'assessment': ('Root\'s qualification is correct and necessary. The author\'s original sentence "regrouping ... cannot change the value or the cause set" '
                       'is false for partial carriers: merged {f,g} with f carrying lockfile-missing and g uncovered emits one coverage-unknown (lockfile-missing), '
                       'while split {f},{g} emits two (lockfile-missing and null), with the value unknown in both (E2c). The divergence is the published per-view '
                       'fold law, not the totality rule: frozen35 already splits two partial carriers into two records (E2d). The final text keeps "regrouping '
                       'preserves the truth of this totality check" (E2a: value equal in all six shapes) and disclaims identical proof records, cited primary '
                       'Coverage ids and per-view carriers. No algorithm or assertion changed: check-atoms changed by one docstring (E14c) and the regrouping control '
                       'asserts equal causes only for complete-entry fixtures (E2b).'),
        'evidence': {k: e2[k]['final36'] for k in e2}, 'receipt': 'receipts/p01-totality36.json E2'},
    'emptyAndDifferentKindBoundaries': {
        'assessment': ('Coherent with every upstream owner I can find, and exactly as stated. Empty: the Coverage route selects no same-kind dependency for an '
                       'empty source-subject set, so reachability stays unknown with required-relation-missing even beside an explicit empty calls partition, '
                       'while the whole-source attestation route closes with an explicit empty calls partition and stays unknown without one (E8a/E8b); '
                       'references (no dependency) closes by either route (E8c); all unchanged from 35 (E8d). This is never unsound: native RC-6 invents no '
                       'universal absence from an empty fact set, identity coveragePartitionLaw admits an empty subjects array but promises no closure, and the '
                       'execution-inputs census still discloses uncovered expected subjects. Different kind: clones (file) -> declares (symbol) stays whole-source '
                       'and unchecked (E9); native DEPENDS_ON has only reachability->calls and clones->declares; RC-4 names reachability/calls only; identity '
                       'section 3 owes the omission half only for file@enumerated; no owner publishes a file-to-symbol correspondence, and native-evidence line '
                       '301 is a capability-law statement, not a population rule. Declining to invent one is the honest limit. One generic sentence in Admitted '
                       'inputs item 1 should be scoped (A-15).'),
        'receipt': 'receipts/p01-totality36.json E8/E9'},
    'rootProseAndRegistry': {
        'dependencyParagraph': 'The corrected sentence ("contributes no pairing ... occupies no position only when no selected Coverage remains") is exactly measured: an exact scope still pairs beside a mapped non-exact scope (E10c).',
        'historySubjectOrder': 'Aligned: uniqueKey removed; order is the producer sequence; every duplicate row keeps its ordinal; no merge/pick rule; repair ambiguity refusal retained and still published (H0-H5); stock schema admits duplicates in producer order; atom identical 35/36.',
        'observabilityFilterAndRuntimePolarity': ('Aligned and exact: unfiltered exists true on observed-hit and observable-unhit; eq filters restrict polarity; unobservable/unmapped never enter R and never make exists/none true; a filter naming them is admitted and matches nothing; "relevant" means subject-occupancy-matched rows, which are disclosed uncertain with cause under every filter while a non-matching row is not; atom runtime behaviour identical 35/36 (R0-R8).'),
        'receipts': ['receipts/p01-totality36.json', 'receipts/p03-history-runtime36.json']},
    'reachabilityByStanding': {
        'syntheticAtomApi': 'EXERCISED: p01 (37 checks), p02, p03 (15 checks); frozen36 check-atoms 101/101',
        'nativeProducerOrCarrier': 'native producer not run for this change; the native subject-scope carrier is reached only through atom admission (E7)',
        'closedEnumeration': 'NOT RUN',
        'retainedRun': ('package13: 13 Runs replayed by me through open_run_closure and close_run; they carry only exists/file/source and none/clones/source atoms '
                        'and no reachability, incoming-endpoint, runtime-observation or history-change atom (p04), so no retained Run reaches the changed '
                        'same-kind totality, history or runtime branches; none/clones/source is different-kind and unchanged (E9)'),
        'product': 'NOT ESTABLISHED; no product qualification is implied'},
    'crossOwnerConsequences': {
        'atomModelConsumers': 'evaluator3 launcher 16/16 children (atoms, replay, execution-inputs, composition, projection) pass on frozen36 with pins valid; children equal root\'s',
        'registryConsumers': 'historySubjectOrder and observabilityFilter are consumed only as registry text (H2); no checker or model reads them as machine rules',
        'nativeAndIdentity': 'native 375/375 and identity checks unchanged in count (1,596 passing calls, 1,584 distinct ids) and byte-equal to root\'s identity report',
        'executionInputsCensus': 'unchanged owner; the census still discloses uncovered expected subjects independently of the atom totality check',
        'noNewCauseOrDeficiency': 'required-relation-missing is an existing native deficiency; no cause code, schema keyword or registry enum was added'},
    'planning': {'layer4Retained': True, 'layer4': r01['layer4'], 'checks': r04['planningGroups'],
                 'why': 'implementation-normative-inputs.v4.json byte-identical, all 29 pins resolve against frozen36, none in the delta; no new layer',
                 'populations': {'paths': 198, 'packages': 20, 'coverageMappings': 320, 'plannedRecoveryCases': 54, 'executed': 0,
                                 'milestones': 'M0-M6 (7)' if p09['isM0toM6'] else '%d milestones: %s' % (len(p09['labels']), p09['labels'])},
                 'populationEvidence': {'inventory': p08['inventory']['topLevelListLengths'], 'milestoneOrder': p08['coverage']['topLevelListLengths']['milestoneOrder'],
                                        'milestoneLabels': p09['labels'], 'milestoneReceipt': 'receipts/p09-milestones.json',
                                        'checkerLines': [g['lastLine'] for g in r04['planningGroups']]},
                 'ownersUnchanged35to36': r01['planningOwnersUnchanged35to36'],
                 'rootPlanningRecord': {'path': os.path.join(ROOTPLAN, 'results.json'), 'sha256': shaif(os.path.join(ROOTPLAN, 'results.json')),
                                        'standing': 'root ran both planning checks on the mutable successor tree; mine ran on a hash-verified frozen36 copy'}}}
J['suites'] = {k: r04[k] for k in ('disposableCopied', 'disposableVerified', 'jobs', 'launcherReport', 'planningGroups', 'disposableFilesRewrittenByCheckers',
                                   'regeneratedWorkflowsReportEqualsFrozen36', 'frozen36DeviationsAfterRuns', 'allJobsExitZero', 'checkAtoms')}
J['suites']['receipt'] = 'receipts/r04-suites.json'
J['determinism'] = {'passed': p02['passed'], 'inProcess': p02['inProcess'], 'processes': {k: p02['processes'][k] for k in ('distinctOrders', 'distinctDigests', 'errors')},
                    'totalityInsertionOrders': E('E11'), 'receipts': ['receipts/p02-determinism36.json', 'receipts/p01-totality36.json']}
J['referenceComparison'] = {
    'rootReference': {'path': ROOTREF, 'reportSha256': shaif(os.path.join(ROOTREF, 'report.json')), 'groups': p06['rootReport']['groups'],
                      'evaluatorChildren': p06['rootReport']['evaluatorChildren'], 'ranOnTree': p06['rootReport']['ranOnTree'],
                      'groupSourcesEqualFrozen36': p06['rootGroupSourcesEqualFrozen36']},
    'codexLiveCopy': {'path': CODEX, **p06['rootVsCodexCopy'], **codex_ref},
    'myEvaluatorChildrenEqualRoot': p06['evaluatorChildren']['equalNamesAndExits'],
    'identityCounts': p06['identityCounts'], 'identityCountsAgree': p06['identityCountsAgree'], 'myIdentityReportEqualsRootBytes': p06['myIdentityReportEqualsRootBytes'],
    'generatedReports': {k: {'rootSha256': v['rootSha256'], 'equalsFrozen36CurrentRow': [r for r in v['equalsFrozen36Rows'] if '/reviews/' not in r], 'myRegeneratedEqualsRoot': v['myRegeneratedEqualsRoot']}
                         for k, v in p06['generatedReports'].items()},
    'topLevelReportFields': p06['topLevelReportFields'],
    'standing': 'Root and codex records were compared with my own frozen36 execution and not adopted; the six groups and 16 children counts are as measured by me.',
    'receipt': 'receipts/p06-reference-compare.json'}
J['authorPackageReview'] = {
    'status': 'COMPLETE - INDEPENDENTLY VERIFIED ON SOURCE36 (package13)', 'package': 'claude-author-package-successor.v13',
    'artifactManifestSha256': r05['artifactManifestSha256'], 'matchesDeclared': r05['matchesDeclaredManifest'], 'matchesRootVerified': r05['matchesRootVerifiedManifest'],
    'members': {'declared': r05['declaredMembers'], 'verified': r05['verified'], 'mismatched': r05['mismatched'], 'missing': r05['missing'], 'unlisted': r05['filesOnDiskNotInManifest']},
    'sourceManifestEqualsFrozen36': r05['sourceManifestEqualsFrozen36'], 'binding': r05['sourceBinding'], 'liveBindingCopyEqual': r05['liveBindingCopyEqual'],
    'lineage': {'parentIsPackage12': r05['bindingParentIsPackage12'], 'package12Manifest': p05['package12ManifestSha256'], 'package12To13': p05['package12To13'],
                'constructionAccountsIdenticalToPackage12': p05['constructionAccountsIdenticalToPackage12'], 'claimsFilesEqualPackage12': p05['claimsFilesEqualPackage12'],
                'exportsByteEqualPackage12Files': p05['allExportsByteEqualPackage12Files'], 'provenanceFieldsUnchanged': p05['provenanceUnchangedFrom12'],
                'predecessorArtifactManifestIsNotPackage12': {'sha256': p05['predecessorArtifactManifestSha256'], 'members': p05.get('predecessorMembers'),
                                                              'package12ManifestCarriedAt': p05['whichEqualsPackage12Manifest']},
                'r05LineageRowsSuperseded': p05['r05Superseded']},
    'changedMembersRead': {'verify-package.py': p07['textDiffs']['verify-package.py']['changedLines'], 'README.md': p07['textDiffs']['README.md']['changedLines'],
                           'evaluationResidualAssessmentChangedValueKinds': p07['residualAssessmentChangedValueKinds'], 'bindingDelta': p07['bindingDelta']},
    'constructionProvenance': r05['constructionProvenance'],
    'mixedProvenanceClaimVerified': ('YES: exports and claims byte-equal package12 files, construction accounts byte-equal, binding provenance fields unchanged; '
                                     'package12 exports were byte-equal to package11 and package10 in my source35 review, so the 33-TS / 30-normalized-Rust construction is retained.'),
    'residualAssessment': r05['residualAssessment'],
    'thirteenCases': {'allAsExpected': r05['allThirteenAsExpected'],
                      'rows': [{k: r.get(k) for k in ('group', 'name', 'structural', 'structuralIdMatches', 'semantic', 'semanticIdMatches', 'semanticReason', 'exportEqualsPackage12')} for r in r05['rows']]},
    'ownerSha256': r05['ownerSha256'], 'ownerUnchanged35to36': r05['ownerEqualsFrozen36AndUnchangedFrom35'],
    'verifier': {'command': r05['verifier']['command'], 'returncode': r05['verifier']['returncode'], **r05['verification'], 'queryChecks': r05['queryChecks'],
                 'queryAssessment': r05['queryAssessment'], 'groupsObservedAndReportDigestsEqualRoot': r05['myGroupsObservedAndReportDigestsMatchRoot'],
                 'verificationJsonBytesEqualRoot': r05['myVerificationJsonEqualsRootBytes']},
    'retainedRunReach': p04['summary'],
    'rootVerification': {'path': '/tmp/opensip-design-corrections/author-package-final36-verification.v1/verification.json', 'sha256': r05['rootVerificationSha256'],
                         'matchesDeclared': r05['rootVerificationMatchesDeclared'], 'standing': 'compared, not adopted'},
    'bindingIsNotReplay': 'Replay standing comes from my own open_run_closure and close_run calls on the 13 exports with the frozen36 owner, not from the binding or the verifier.',
    'limitsPreserved': 'A-9 repair/reference-only; A-10 partial helper, exists/none operators, incomplete two-binding construction; 30 PENDING author grades; TCB-SCOPE-01 over 13 rows',
    'noRemintNoRelabel': 'exports byte-identical to package12; no historical execution relabelled', 'grantsNoPackageAcceptance': True,
    'noBlindOrProductConclusion': 'These are synthetic reference examples; no blind or product-qualification conclusion follows.',
    'receipts': ['receipts/r05-package13.json', 'receipts/p05-package-lineage.json', 'receipts/p07-package-member-diffs.json', 'receipts/p04-package-reach.json']}

# ------------------------------------------------------------------ rows
CONS36 = {
    'arDispositions/AR-12': ('STRENGTHENED-ON-36-DEPENDENCY-TOTALITY-CONSEQUENCE',
        'RESTORED ON 35 AND STRENGTHENED ON 36 AT THE ATOM-LAW BOUNDARY. An authoritative incoming negative is only as strong as the atom law consuming '
        'provenance. Source36 adds that it cannot stand on a same-kind dependency census missing any owed subject: every missing shape (g absent, scope '
        'without Coverage, Coverage at another target, wrong-universe scope, unrelated subject only, f absent) is unknown with required-relation-missing for '
        'all-covered, none and count<=1, while full and disjoint covers close; frozen35 answered true (receipts/p01-totality36.json E1). I1 is byte-untouched '
        '(r01). Owners byte-identical 35->36. Standing: atom-api; no package13 retained Run carries a reachability or incoming atom (p04).'),
    'fwDispositions/FW-08': ('STRENGTHENED-ON-36-DEPENDENCY-TOTALITY-CONSEQUENCE',
        'RESTORED ON 35 AND STRENGTHENED ON 36. The omission class this row covers now includes dependency census gaps: an owed subject without a covering '
        'same-kind dependency is disclosed as coverage-unknown with required-relation-missing beside the retained partial evidence, never silently closed, on '
        'the per-scope and attestation routes (E1, E6, E3a); known matches and exceeded count bounds still decide (E5). Owners byte-identical 35->36.'),
    'fwDispositions/FW-06': ('HOLDS-ON-36-REMEASURED',
        'STRENGTHENED ON 34, HOLDING ON 35 AND 36, RE-MEASURED because the sufficiency path changed: E1 24 and E2 480 orderings give one result each, the '
        'totality shapes give one result across their map orderings (p02) and 48 insertion orders per shape on both endpoints (p01 E11), and six fresh '
        'interpreters with six hash-seeded orders give one digest (receipts/p02-determinism36.json).'),
    'inheritedResidualDispositions/DR-009': ('HOLDS-ON-36-REMEASURED',
        'STRENGTHENED ON 34, HOLDING ON 35 AND 36: carrier determinism across processes re-measured on frozen36 including the totality shapes (six processes, '
        'one digest; receipts/p02-determinism36.json). Owners byte-identical 35->36.'),
    'arDispositions/AR-16': ('HOLDS-ON-36-REMEASURED',
        'STRENGTHENED ON 34, HOLDING ON 35 AND 36: the typed coverage-unknown carrier is still the first non-null over positions and first-with-deficiency in '
        'ascending coverage2 order (p02 E1/E2). The totality gap-removed view never supplies the carrier, which is taken from the actual view (E3a keeps '
        'lockfile-missing). Splitting a primary partition can add a per-view carrier record without changing the value; that follows the published per-view '
        'fold law and already happened on frozen35 (p01 E2c/E2d). Owners byte-identical 35->36.'),
}
NOTE36 = {
    'arDispositions/AR-08': ' Specific check on 36: the registry historySubjectOrder text now says repair targetSubjectProjection keeps its own ambiguity refusal; that refusal is still published and no repair owner consumes the registry text (p03 H1-H3).',
    'fwDispositions/FW-10': ' Specific check on 36: repair targetSubjectProjection ambiguity refusal still published and unaffected by the registry history-order text (p03 H2/H3).',
}
F36_TEXT = {
    'F-01': 'the charter custody artifacts are among the 313 members byte-identical to package12 (p05).',
    'F-02': 'the consumer-b.v13 v6/v7 assessment artifacts are among the 313 members byte-identical to package12; hashed for custody only, not read.',
    'F-03': 'verify-package.py ran against frozen36 in this runtime: rc 0, 12,899 source files, 323 package files, 7/7 queries, groups, observed outcomes and report digests equal to root, verification.json byte-equal to root\'s.',
    'F-05': 'ts-invalid-default-entry structurally ADMITS then semantically REFUSES ENUMERATION_BINDING_PROGRAM_ENTRY through the frozen36 identity-model.v3.py owner (unchanged 35->36).',
    'F-06': 'ts-lawful-explicit-selection admits through both boundaries; two-binding construction still incomplete with a single explicit binding.',
    'F-08': 'the property probe stays a separate command (author-properties files byte-equal to package12); README changed only for the source36 binding (p07).',
    'F-10': 'mixed provenance unchanged: exportsChanged false, all 13 exports and claims byte-equal to package12 files (p05) and so to package11/10, construction accounts byte-equal, constructionSourceVersion {typescriptDerivedGroups: 33, normalizedAndRustGroups: 30}, currentVerificationSourceVersion 36.',
    'F-11': 'helper files carrying this row are byte-identical to package12 (only README, residual assessment, source manifest and verifier changed; p05/p07).',
    'F-12': 'weighting holds on the same exports: only checkpoint3/author-ts is helper-versus-owner; six positives are owner-derived self-consistency; three negatives derive from checkpoint3.',
    'F-13': 'package13 evaluation-residual-author-assessment.json binds frozen36, 30 rows independentGrade PENDING, TCB-SCOPE-01 over 13 dependents, evidence resolves against frozen candidate36; its only changes from package12 are resolveAgainst, standing and subjectManifestSha256 (p07).',
    'F-14': 'all 30 rows still proposed-account-supported-with-stated-limits; informational, no grade awarded.',
}
PKG36 = ('Verified on the source36-bound package13 (artifact manifest 47dbe781..., 323/323 members, source-manifest byte-equal to frozen36, all 13 '
         'Run/control cases through open_run_closure AND close_run with my own decoder and the frozen36 owner).')
tcb = set(BL['sharedAssumptionTCBSCOPE01']['dependentRows'])
counts = {}
for mp in MAPS:
    for rid, row in BL[mp].items():
        key = mp + '/' + rid
        info = r08['rows'][key]
        owners = info['owners']
        row['ownerFilesChangedIn35to36'] = sorted(p for p in owners if p in DELTA)
        row['ownerFilesUnchangedIn35to36'] = sorted(p for p in owners if p not in DELTA)
        row['ownerArraysDerivedFromManifests35and36'] = True
        row['ownerPathsResolveInFrozen36'] = all(p in m36 for p in owners) if owners else None
        if row.get('subjectOwnerFilesOn34'):
            row['subjectOwnerBytesEqual35and36'] = all(m35.get(p) == m36.get(p) and p in m36 for p in row['subjectOwnerFilesOn34'])
        if row.get('readingStandingLegacyCorrectionOn34'):
            row['readingStandingLegacyCorrectionStatusOn36'] = 'still accurate on 36; the legacy string, its source34 qualification and its source35 status are unchanged'
        n = len(owners)
        if key in CONS36:
            st, txt = CONS36[key]
            read = ('INHERITED ON EXACT BYTES for this row\'s %d owner file(s) (identical sha256 in the frozen35 and frozen36 manifests), PLUS a fresh source36 '
                    'assessment of the changed atom dependency law\'s consequence for this subject (receipts/p01-totality36.json, p02-determinism36.json).' % n)
            disp = st
        elif mp == 'fDispositions' and rid in F36_TEXT:
            st, txt = 'RE-VERIFIED-ON-PACKAGE13', PKG36 + ' Row-specific on 36: ' + F36_TEXT[rid]
            read = 'PACKAGE-BORNE: re-measured on package13 in this runtime (receipts/r05-package13.json, p05-package-lineage.json); package12/11/10 readings stay in the baseline fields.'
            disp = st
        elif mp == 'fDispositions':
            st = 'INHERITED'
            if rid == 'F-07':
                txt = 'Inherited on 36: package13 carries the same exports byte-identically (p05), so the measured predicate coverage (exists/none only) is unchanged.'
                read = 'INHERITED ON EXACT EXPORT BYTES (receipts/p05-package-lineage.json allExportsByteEqualPackage12Files; r05 exportEqualsPackage12 on all 13).'
            else:
                txt = ('Inherited on 36: every subject owner of this row (%s) is byte-identical 35->36; the source35 account in currentStatusOn35 is inherited, '
                       'not re-derived. The owning suites pass on frozen36 (launcher 16/16).' % ', '.join(p.split('/')[-1] for p in row['subjectOwnerFilesOn34']))
                read = 'INHERITED ON EXACT BYTES (manifests 35/36; receipts/r08-rows.json).'
            disp = st
        else:
            st = 'INHERITED'
            extra = ''
            if mp == 'evaluationResidualDispositions':
                extra = (' The author proposal remains PENDING independent grading; no grade is awarded.' +
                         (' One of the 13 TCB-SCOPE-01 dependents; the joint consequence is not closed.' if rid in tcb else ''))
            txt = ('Inherited on 36: all %d owner path(s) are byte-identical in the frozen35 and frozen36 manifests, none is in the 10-file delta, and the '
                   'source36 changes (dependency-scope fallback removal, same-kind dependency totality, history-order and runtime-polarity text) do not bear on '
                   'this row\'s subject. The source35 account in currentStatusOn35 is inherited with explicit standing, not re-derived.%s%s' % (n, extra, NOTE36.get(key, '')))
            read = ('INHERITED ON EXACT BYTES: %d owner file(s) with identical sha256 in the frozen35 and frozen36 manifests (receipts/r08-rows.json); the '
                    'substantive reading is the one recorded for source34 and carried on source35.' % n)
            disp = 'INHERITED - author proposal PENDING independent grading' if mp == 'evaluationResidualDispositions' else 'INHERITED'
        row['statusChangeOn36'] = st
        row['currentDispositionOn36'] = disp
        row['currentStatusOn36'] = txt
        row['readingStandingOn36'] = read
        row['currentFieldStandingOn36'] = ('currentDispositionOn36 / currentStatusOn36 / readingStandingOn36 are the source36 account; every baseline field, '
                                           'including all *On33, *On34 and *On35 fields, is preserved verbatim.')
        row['appliedByThisReview'] = False
        row['finalApplicationOutcomeGranted'] = False
        counts[st] = counts.get(st, 0) + 1
    J[mp] = BL[mp]
J['rowCarryForwardCounts36'] = {'inherited': counts.get('INHERITED', 0), 'packageReverified': counts.get('RE-VERIFIED-ON-PACKAGE13', 0),
                                'crossOwner': sum(v for k, v in counts.items() if k not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE13')), 'byStatus': counts,
                                'derivation': ('Derived for source36, not copied: no row owner or named subject owner is in the 35->36 delta (r08); the five rows '
                                               'whose subject is the atom completeness law, its carrier or its determinism (AR-12, FW-08, AR-16, FW-06, DR-009) '
                                               'received fresh consequence assessment; the 11 package-borne F rows were re-measured on package13; the rest '
                                               'inherit on exact bytes. The numbers coincide with source35\'s 91/11/5, which remains historical.')}
J['rowCarryForwardCounts'] = BL['rowCarryForwardCounts']
J['readingStandingAudit'] = dict(BL['readingStandingAudit'])
J['readingStandingAudit']['statusOn36'] = 'All nine source34 qualifications retained unchanged and still accurate on 36; no legacy string edited.'
J['sharedAssumptionTCBSCOPE01'] = dict(BL['sharedAssumptionTCBSCOPE01'])
J['sharedAssumptionTCBSCOPE01']['statusOn36'] = 'One joint consequence over the same 13 rows; not closed; dependent owners byte-identical 35->36; package13 carries TCB-SCOPE-01 over 13 dependents.'
J['dispositionCounts'] = {mp: len(BL[mp]) for mp in MAPS}
J['dispositionCounts']['total'] = sum(J['dispositionCounts'].values())
J['dispositionStandingForEveryRow'] = dict(BL['dispositionStandingForEveryRow'])
J['dispositionStandingForEveryRow']['statusOn36'] = 'Unchanged: appliedByThisReview false and finalApplicationOutcomeGranted false on all 107 rows.'
J['crossUnitStanding'] = dict(BL['crossUnitStanding'])
J['crossUnitStanding']['statusOn36'] = ('Carried unchanged: 28 condition-2 obligations retained; 32 product gates, 0 performed, condition 5 NOT MET; 54 recovery '
                                        'cases, 0 executed; TCB-SCOPE-01 one joint consequence over 13 rows; D9 implementation obligation on DR-007 / DR-011-R08 '
                                        'persists; all 30 residual proposals PENDING until the separate final application review.')
J['grantsNothing'] = dict(BL['grantsNothing'])
J['grantsNothing']['statusOn36'] = 'Nothing is granted on 36: no application outcome, architecture readiness, activation, implementation authorization, blind or package acceptance, product qualification, residual grade, commit or push.'
J['correctionsToMyOwnPriorRecords'] = BL['correctionsToMyOwnPriorRecords'] + [{
    'id': 'C36-01', 'records': ['claude-dependency-totality-assessment.v1'],
    'correction': ('My focused assessment called prototype A (drop a non-total same-kind position) the required smallest remedy and A+B recommended, and '
                   'presented "the partial answer equals the no-dependency answer exactly" as a merit. Measured on final36 bytes, the adopted two-view law '
                   'is the better correction: it gives the same values as A+B on every totality shape while retaining the partial partition\'s read '
                   'deficiency, typed carrier and citation that A discards (E3a/E3b), and frozen36 check-atoms fails four totality controls under A and under '
                   'A+B (E12c). My defect classification stands; its remedy recommendation is superseded. The focused record is preserved unchanged.'),
    'evidence': 'receipts/p01-totality36.json E3, E12'}]
J['verdictBasis'] = (
    'SOURCE36 DESIGN: ACCEPT, scoped to design and reference bytes. Custody: manifest a729406b... and archive 7db498f0... match; 12,899 files and '
    '736,854,701 bytes verify with nothing missing, mismatched, extra or omitted from the parent; the archive equals the manifest; the parent is the '
    'source35 I accepted. My manifest-derived delta is 10 changed files, agreeing with root: four carry substance (atom contract section 4/6/9, atom_model, '
    'check-atoms, projection registry text) and six only re-pin. A-13 is CLOSED: the dependency mapping fallback is deleted and all 20 frozen35-healed '
    'rows are absent on both endpoints. Every focused totality finding is closed or explicitly and coherently bounded: same-kind partial census and the '
    'attestation route are unknown with required-relation-missing beside retained partial evidence, full and disjoint covers close, known matches and '
    'exceeded bounds still decide, outgoing is unchanged, results are order- and process-independent, and root\'s regrouping qualification is correct. '
    'The author\'s two-view law is better than my focused prototype. Root\'s history-order and runtime-polarity texts align every owner and are exactly '
    'measured. Suites (check-atoms 101/101, launcher 16/16, foundation, integration 412, native 375/375, security, workflows), planning (layer4 retained) '
    'and package13 (13 cases through both boundaries, 7 queries, mixed provenance retained) pass on frozen36 with zero drift. Two new advisories (A-14 '
    'attestation-route carrier consumption; A-15 one generic empty-program sentence). No new MUST or SHOULD. This grants no application outcome, readiness, '
    'qualification or acceptance of anything beyond these design bytes.')
J['limitations'] = [
    'Design and reference layers only; no product implementation, qualification or readiness.',
    'Totality, A-13, history and runtime evidence is synthetic atom-api (global atom-input admission + evaluate_atom), stock schema and static owner text; the depth-2 case is a synthetic helper graph; no native producer run and no closed enumeration admission; no retained Run reaches the changed branches.',
    'The empty-program Coverage route stays conservative for relations with a same-kind dependency; whether producers emit the attestation form that closes it is not established.',
    'Different-kind dependency population completeness is not guaranteed by this profile and is not claimed.',
    'For the history-order and runtime-polarity texts, my confirmation verifies corrections that implement my own focused recommendations (see sessionIdentity.overlapWithCandidateAuthorship).',
    'A-10 limits retained; A-9 admitted-versus-unit limits retained; all 30 author residual proposals PENDING independent grading.',
    'Unchanged readings are inherited only on exact manifest-byte equality and labelled INHERITED.',
    'Author, root and codex receipts were evidence I assessed; my conclusions rest on my own executions on frozen36 bytes.',
    'No consumer input, output, diagnosis, report, root blind control or expected result was read.']
J['probeErrorsPreserved'] = BL['probeErrorsPreserved'] + [
    'p01 first run (receipts/p01_totality36) stopped at model load after its five byte-provenance checks passed: the disposable tree copied only foundation/native/workflows, but native_evidence_model loads design-corrections/discovery-defaults.py. The builder was widened to the whole design-corrections tree minus reviews/ (still hash-checked against the 35 manifest) and rerun as p01_totality36.2; no semantic check had run before the failure.',
    'r05 assumed package13 predecessor-artifact-manifest.json was package12\'s manifest. It is an older 97-member manifest (c533aa6a...). r05\'s predecessorIsPackage12 and constructionAccountsIdenticalToPackage12 values and its package12To13 member delta are void; p05 re-measured lineage against package12 itself (fb35036f): 6 added, 4 changed, 0 removed, 313 identical; construction accounts, claims and all 13 exports byte-equal.',
    'r05\'s reach heuristic historyOrRuntimeImportMarkers (26) combined its tests with an operator-precedence flaw and is not relied on; p04 lists exact paths: retained Runs carry runtime/history import records and payloads but no runtime-observation, history-change, reachability or incoming atom.',
    'r08\'s keyword scan matched all 107 rows because every row carries *On34/*On35 history text; it selected nothing and was not used. Cross-owner rows were chosen by reading row subjects and the source35 cross-owner classes.']
recs = sorted(f for f in os.listdir(RC) if f.endswith('.json') and not f.startswith('i36'))
J['evidenceReceipts'] = {'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B', 'receipts': {f: sha(os.path.join(RC, f)) for f in recs},
                         'commandReceiptDirs': {d: {'startedUtc': v, 'commandJsonSha256': sha(os.path.join(RC, d, 'command.json')),
                                                    'exit': json.load(open(os.path.join(RC, d, 'command.json')))['exit']} for d, v in starts.items()},
                         'probes': sorted(f for f in os.listdir(os.path.join(BASE, 'probes')) if f.endswith('.py')),
                         'frozen36DriftAfter': {'r04': r04['frozen36DeviationsAfterRuns'], 'r05': r05['frozen36DeviationsAfter'], 'p01OwnersUnchanged': p01['frozen36AtomOwnersUnchanged']}}
out = os.path.join(BASE, 'review.json')
json.dump(J, open(out, 'w'), indent=1, default=str)
print('rows', J['dispositionCounts'], '| carry36', {k: v for k, v in J['rowCarryForwardCounts36'].items() if k != 'derivation'})
print('verdict', J['verdict'], '| MUST', J['newMustIssues'], '| SHOULD', J['newShouldIssues'], '| advisories', [a['id'] for a in J['advisories']])
print('resolved', [x['id'] for x in J['resolvedIssues']])
print('law written %s <= first semantic probe %s' % (law_written, first_semantic), '| codex ref', codex_ref)
print('bytes', os.path.getsize(out), 'sha256', sha(out))
