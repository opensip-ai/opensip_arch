"""B35 — build the COMPLETE source35 review.json from the complete source34 baseline and my own receipts.
Baseline row fields (including every *On34 field) are preserved verbatim as history; source35 facts are
added in *On35 / *34to35 fields; owner arrays come from the two manifests; every claim points at a receipt."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
RC = os.path.join(BASE, 'receipts')
B34 = '/tmp/opensip-design-corrections/claude-independent-design.v34'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


rc = lambda n: json.load(open(os.path.join(RC, n)))
r00, r01, r02, r03, r04, r05, r06, r07, r08 = (rc(n) for n in (
    'r00-custody.json', 'r01-diffs.json', 'r02-must-matrix.json', 'r03-a12.json', 'r04-suites.json', 'r05-package12.json',
    'r06-determinism.json', 'r07-followups.json', 'r08-rows.json'))
BL = json.load(open(os.path.join(B34, 'review.json')))
m35 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v35.json')))['files']}
m34 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v34.json')))['files']}
DELTA = sorted(c['path'] for c in r00['delta']['changed'])
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
        'scopedReviewOwnerDispositions')
chk = lambda R, cid: next(c for c in R['checks'] if c['id'] == cid)
assert r04['allJobsExitZero'] and r05['allThirteenAsExpected'] and r06['passed'], 'a gating measurement failed; reassess before building'
assert not r08['rowsWithOwnerIn35Delta'], 'a row owner is in the delta; classify it before building'
assert all(chk(r02, c)['passed'] for c in ('M1-incoming-equals-source35-prose-predictor-on-every-cell', 'M2-no-incoming-negative-without-an-available-binding-at-U',
                                            'M4-34-to-35-change-is-exactly-I1', 'M5-I1-record-shape', 'K1-known-matches-and-exceeded-bounds-survive-I1',
                                            'P1-one-result-for-every-cell-provider-attestation-and-map-order', 'P2-multi-provider-values'))
assert not r07['failed']
J = {}

J['review'] = 'Independent design review of exact frozen consolidated product source35'
J['verdict'] = 'ACCEPT'
J['verdictScope'] = ('Design and reference bytes of source35 only. Grants no application outcome, readiness, activation, '
                     'implementation authorization, blind acceptance, package acceptance, product qualification, commit or push.')
J['subjectManifestSha256'] = r00['manifestSha256']
J['verifiedManifest'] = bool(r00['manifestShaMatchesDeclared'] and r00['archiveShaMatchesDeclared'] and r00['archiveEqualsManifest']
                             and r00['missing'] == r00['hashMismatches'] == r00['sizeMismatches'] == r00['extras'] == 0 and r00['matchesDeclared'])
J['sessionIdentity'] = {
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b', 'role': 'independent reviewer, actual Claude; I have authored no source',
    'notAForbiddenAcceptor': BL['sessionIdentity']['notAForbiddenAcceptor'],
    'notTheSourceAuthorOfThisCorrection': '823bf66b-e92a-4789-ab81-63a1a9dc371d authored the source35 correction and is excluded; I am not it',
    'blindPolicy': 'No consumer output, diagnosis, report, root blind control or expected result was read or used.',
    'priorRecordsHistoricalUnchanged': BL['sessionIdentity']['priorReviewsHistoricalUnchanged'] + [
        {'path': 'claude-independent-design.v34/review.json', 'sha256': r01['baseline']['reviewJson'], 'mdSha256': r01['baseline']['reviewMd'],
         'standing': 'CHANGES_REQUIRED on source34; the complete baseline of this review'}],
    'notResurrected': 'source33 acceptance is not resurrected; root bounded assessments are not whole-design assent'}
J['baselineRecord'] = {'path': 'claude-independent-design.v34/review.json', 'sha256': r01['baseline']['reviewJson'],
                       'expected': 'c31f1c4779b8fa60385520009c73139d46572b29a7f22f251c5a0182a2a42bb3', 'mdSha256': r01['baseline']['reviewMd'],
                       'matches': r01['baselineMatches'], 'baselineVerdict': BL['verdict']}
J['manifestVerification'] = {k: r00[k] for k in ('manifestSha256', 'manifestShaMatchesDeclared', 'archiveSha256', 'archiveShaMatchesDeclared',
                                                 'declaredFiles', 'measuredTotalBytes', 'missing', 'hashMismatches', 'sizeMismatches', 'extras',
                                                 'archiveMemberRows', 'archiveHashMismatches', 'archiveEqualsManifest', 'matchesDeclared',
                                                 'parentNamedIsSource34', 'manifest34IsMyReviewedSource34', 'freezeAgrees')}
J['manifestVerification']['receipt'] = 'receipts/r00-custody.json'
SUB = ['docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md', 'docs/coop/design-corrections/foundation/atom_model.v1.py',
       'docs/coop/design-corrections/foundation/check-atoms.v1.py', 'docs/coop/design-corrections/foundation/incoming-search.schema.v1.json']
J['delta34to35'] = {
    'derivedFrom': 'the frozen34 and frozen35 manifests', 'added': 0, 'removed': 0, 'changed': len(DELTA), 'netBytes': r00['delta']['netBytes'],
    'changedFiles': r00['delta']['changed'],
    'substantive': {p: {k: r01['files'][p][k] for k in ('lines34', 'lines35', 'plus', 'minus')} for p in SUB},
    'digestRebindingOnly': sorted(p for p in DELTA if p not in SUB),
    'contractSections': r01['contractSections'],
    'modelTopLevelChanged': r01['files'][SUB[1]]['topLevel'], 'checkerTopLevelChanged': r01['files'][SUB[2]]['topLevel'],
    'schemaOwnerJsonPathChanges': r01['schemaJsonPathChanges'], 'schemaValidationKeywordChanged': r01['schemaValidationKeywordChanged'],
    'rootInventoryAgreement': r00.get('rootInventories'), 'receipts': ['receipts/r00-custody.json', 'receipts/r01-diffs.json', 'receipts/diffs/']}
J['authorshipOfFinalBytes'] = {
    'author': {'origin': '823bf66b-e92a-4789-ab81-63a1a9dc371d', 'bytes': {'contract': '7ee61c18...', 'model': 'c1243ca9... (final)', 'checker': '258099be...'}},
    'rootLater': {'record': 'reviews/root-incoming-binding-prose-completion.v1/root-changes.json',
                  'changes': ['contract 7ee61c18 -> f6c3b375 (final): empty scopeRefs SCHEMA vs borrowed nonempty SCOPE_MISJOIN; generic defensive-fallback sentence',
                              'incoming-search.schema.v1.json fd5c51ea -> fcea86fa (final): joins/5 metadata text only',
                              'check-atoms.v1.py 258099be -> 11aa038a (final): one SCOPE_MISJOIN assertion'],
                  'finalEqualsFrozen35': all(m35[p] == h for p, h in (
                      (SUB[0], 'f6c3b375a359d0fcac657ecf2f55213ad80e3c7bb368dd6656d181b9df979ce3'),
                      (SUB[3], 'fcea86fa7ffe43a7ea9533231f1abaad65fb4aea72c0ebdb5da43727d31afa68'),
                      (SUB[2], '11aa038a56e84b0142b496d0d3d77beac90d7f323d3c64047294ca50455dd2c8'),
                      (SUB[1], 'c1243ca9bd1e2b73aac4456d09df18813b7dc7e72e141a577d908519e2dc9660')))},
    'standing': 'I reviewed and tested the FINAL frozen35 bytes, including every root-authored later change; author reports describe earlier bytes'}

m1, m4, k1, p1 = (chk(r02, c) for c in ('M1-incoming-equals-source35-prose-predictor-on-every-cell', 'M4-34-to-35-change-is-exactly-I1',
                                         'K1-known-matches-and-exceeded-bounds-survive-I1', 'P1-one-result-for-every-cell-provider-attestation-and-map-order'))
J['resolvedIssues'] = [{
    'id': 'MUST-34-01', 'status': 'CLOSED ON SOURCE35',
    'law': ('contract section 4 incoming step I1: when no available owed binding has universe = U, emit selector-unbound (universe key '
            'omitted), mark completeness unknown, and do NOT return; P1 and P2 precede it; outgoing unchanged'),
    'reference': 'atom_model.v1.py _native_completeness incoming branch, five lines before per-universe accumulation',
    'evidence': {
        'predictorMatrix': {'cellOps': m1['observed']['cells'], 'mismatches': len(m1['observed']['mismatches'])},
        'noNegativeWithoutAvailableBindingAtU': chk(r02, 'M2-no-incoming-negative-without-an-available-binding-at-U')['passed'],
        'outgoingInvariant34to35': chk(r07, 'M3b-outgoing-invariant-and-equal-corrected-predictor')['observed'],
        'changeIsExactlyI1': m4['observed'], 'recordShape': chk(r02, 'M5-I1-record-shape')['passed'],
        'knownMatchesAndCountBounds': k1['observed'],
        'permutations': {k: {'orderings': v[0], 'distinct': v[1], 'value': v[2]} for k, v in p1['observed'].items()},
        'syntheticContradictoryFamilyObservation': r02['contradictoryFamilyAtU']},
    'standing': ('atom-api (global atom-input admission + evaluate_atom, synthetic inputs). Not closed enumeration admission and not a '
                 'retained Run: package12 retained Runs contain no incoming-endpoint atom and no IncomingSearchV1 record. Whether '
                 'product configuration can express per-unit narrowing remains unestablished; the law no longer depends on it, '
                 'because an unbound subject universe is unknown however the request was produced.'),
    'receipts': ['receipts/r02-must-matrix.json', 'receipts/r07-followups.json']}]
c2b, c3b, d1 = chk(r07, 'C2b-frozen34-carrier-bypasses-closed-on-35'), chk(r07, 'C3b-null-change-is-only-subjects'), chk(r07, 'D1-dependency-mapping-fallback-accepts-unselected-scopes-MEASURED')
e1 = chk(r03, 'E1-scopeless-and-empty-subject-scope-boundaries')
adv = {a['id']: a for a in BL['advisories']}
a9 = dict(adv['A-9']); a9['statusOn35'] = 'Carried with limits intact: repair owners byte-identical 34->35; admitted-versus-unit limitations retained exactly.'
a10 = dict(adv['A-10']); a10['statusOn35'] = ('Carried, limits unchanged, measured on package12: all 13 exports byte-identical to package11 and so to '
                                              'package10; mixed construction (TS groups on 33, normalized/Rust on 30); TS helper-versus-owner only; six '
                                              'self-consistency; exists/none only with the other operator limits; incomplete two-binding construction with '
                                              'a single explicit binding; no compiler/provider/OS qualification.')
a11 = dict(adv['A-11']); a11['statusOn35'] = 'Historical; not reopened.'
a12 = dict(adv['A-12'])
a12['statusOn35'] = 'CLOSED ON SOURCE35 for both published alternatives, with one residual reference path recorded separately as A-13.'
a12['closureOn35'] = {
    'scopelessGroup': ('contract row 1 and the Admitted-inputs note now state that no admitted attestation exists; measured: no attestation -> '
                       'source-target-search-unattested; empty scopeRefs -> global INCOMING_SEARCH_SCHEMA; borrowed or nonexistent nonempty '
                       'scopeRefs -> global INCOMING_SEARCH_SCOPE_MISJOIN; an explicit empty-subject scope closes only with complete S->U '
                       'Coverage or a qualifying attestation and cannot hide real inventoried subjects; identical on frozen34 (no code needed)'),
    'untaggedScopeAndMissingKeyCarrierBypass': ('_scope_descriptor now passes present fields through, so absent keys reach the native carrier '
                                                'like null ones. Across 8 carrier fields x absent/null x 4 consumption paths, every frozen35 answer '
                                                'is a refusal or equals the scope-deleted answer, except the dependency mapping fallback (A-13). '
                                                '%d frozen34 cases that answered as if an inadmissible scope were valid evidence now refuse; the only '
                                                'null-field change is subjects:null, which frozen34 also skipped.' % c2b['observed']['closedCount']),
    'schemaOwner': ('incoming-search.schema.v1.json changed only x-opensip-law/joins/5 metadata text; every probe instance gets the same '
                    'stock-schema verdict under both schemas; the text now names the native carrier and states there is no untagged fallback'),
    'evidence': {'E1': e1['observed']['values'], 'C2b': c2b['observed'], 'C3b': c3b['observed'],
                 'S1': chk(r03, 'S1-schema-change-is-metadata-only')['passed'], 'S2': chk(r03, 'S2-schema-metadata-now-states-carrier-and-no-untagged-fallback')['passed']},
    'receipts': ['receipts/r03-a12.json', 'receipts/r07-followups.json']}
a13 = {
    'id': 'A-13', 'title': 'The dependency coverageScopes mapping fallback consumes a scope without carrier validation or key join',
    'selectors': ['atom_model.v1.py _select_dep_coverages mapping branch (taken when no exact dependency scope exists)',
                  'atom-evaluation-contract.v1.md section 4 Admitted inputs item 2: "pairing validates the carrier ... when an evaluation on either endpoint consumes the scope"'],
    'measured': ('With no exact (relation, rung, S) dependency scope present, a coverageScopes mapping to a scope whose relation, resolution or '
                 'sourceUniverse is absent, null, or a VALID but different value still heals the reachability dependency to all-covered '
                 'true; deleting that scope gives unknown. With any exact dependency scope present the fallback is not taken. frozen34 '
                 'behaves identically, so this is pre-existing and not introduced by source35.'),
    'why_not_a_should': ('Unreachable for retained Runs: identity-model close_run admits every retained subject-scope object and, for every '
                         'Coverage, requires coverage.scopeId in the view (COVERAGE_SCOPE_JOIN) and re-runs native admit_coverage_result_v3 '
                         'over that retained scope, so a retained Coverage cannot map to a malformed or mismatched scope. The gap is a '
                         'reference branch at the synthetic atom API, which the new section 4 sentence describes more strictly than the '
                         'reference implements.'),
    'healedCases': d1['observed']['healedWithoutValidMatchingScope'], 'receipt': 'receipts/r07-followups.json',
    'fallbackRowsSameOn34': all(v['35'] == v['34'] for k, v in r07['dependencyMappingFallback'].items() if 'control' not in k),
    'noteOnReceiptFlag': ('r07 fallbackSameOn34 is false only because it also counts the enumeratorClosure-absent CONTROL rows, which '
                          'frozen35 now refuses (a closed bypass); all 14 fallback rows are identical on 34 and 35'),
    'statusOn35': 'NEW on source35 as a finding; the behaviour is pre-existing.'}
J['advisories'] = [a9, a10, a11, a12, a13]
J['newMustIssues'] = []
J['newShouldIssues'] = []

J['sourceChangeAssessment'] = {
    'incomingSubjectUniverseLaw': {'assessment': ('I1 is correct, conservative and precisely placed: after P1/P2, before accumulation, never a '
                                                  'return, emitted once, order independent; it retracts no known evidence; P2 and outgoing are '
                                                  'byte-for-byte unchanged; foreign-family and unavailable bindings never satisfy it; the '
                                                  'subject universe is now always an owed source in the owed-programs paragraph.'),
                                   'receipt': 'receipts/r02-must-matrix.json'},
    'carrierPassThrough': {'assessment': ('_scope_descriptor passes fields through and _derive_scope_commitment has no None escape; the '
                                          'native subject-scope carrier now decides every paired scope and every attestation-named scope.'),
                           'receipt': 'receipts/r03-a12.json'},
    'crossOwnerConsequences': {
        'retainedRunPath': 'package12 13/13 cases through both boundaries and 7/7 queries unchanged; retained Runs do not reach incoming atoms',
        'consumersOfAtomModel': 'launcher 16/16 children including atoms and replay children; workflows/query models import atom_model; all pass',
        'determinismOnChangedPairingPath': ('re-measured because _derive_scope_commitment is on the pairing path: E1 %s, E2 %s, six processes '
                                            'one digest' % ({k: v['distinct'] for k, v in r06['inProcess'].items() if k.startswith('E1')},
                                                            {k: v['distinct'] for k, v in r06['inProcess'].items() if k.startswith('E2')})),
        'schemaOwner': 'metadata-only, no validation keyword changed'},
    'planning': {'layer4Retained': True, 'layer4': r01['layer4'], 'checks': r04['planningGroups'],
                 'why': 'implementation-normative-inputs.v4.json byte-identical, all 29 pins resolve against frozen35, none in the delta',
                 'populations': {'paths': 198, 'packages': 20, 'coverageMappings': 320, 'plannedRecoveryCases': 54, 'executed': 0, 'milestones': 'M0-M6'},
                 'layoutAndCoverageOwnersUnchanged34to35': all(m34.get(p) == m35.get(p) for p in (
                     'docs/v2/architecture/14-repository-and-module-layout.md', 'docs/v2/architecture/repository-file-inventory.v1.json',
                     'docs/v2/architecture/implementation-coverage.v1.json', 'docs/v2/architecture/implementation-planning-sources.v1.json'))},
    'evidenceStanding': {'atom-api': 'R02, R03 atom rows, R06, R07', 'stock schema': 'R03 S1', 'native carrier': 'R03 carrier refusals (via atom admission)',
                         'closed enumeration admission': 'not run', 'retained Run': 'package12 replay only; does not reach the changed incoming branches',
                         'author/root evidence': 'read; not adopted; check-atoms 89/89 run by me as an owning suite, not as acceptance'}}
J['suites'] = {k: r04[k] for k in ('disposableCopied', 'disposableVerified', 'jobs', 'launcherReport', 'planningGroups', 'disposableFilesRewrittenByCheckers',
                                   'regeneratedWorkflowsReportEqualsFrozen35', 'frozen35DeviationsAfterRuns', 'allJobsExitZero', 'checkAtoms')}
J['suites']['receipt'] = 'receipts/r04-suites.json'
J['determinism'] = {'passed': r06['passed'], 'inProcess': r06['inProcess'], 'processes': {k: r06['processes'][k] for k in ('distinctOrders', 'distinctDigests', 'errors')},
                    'receipt': 'receipts/r06-determinism.json'}
J['authorPackageReview'] = {
    'status': 'COMPLETE - INDEPENDENTLY VERIFIED ON SOURCE35 (package12)', 'package': 'claude-author-package-successor.v12',
    'artifactManifestSha256': r05['artifactManifestSha256'], 'matchesDeclared': r05['matchesDeclaredManifest'], 'matchesRootVerified': r05['matchesRootVerifiedManifest'],
    'members': {'declared': r05['declaredMembers'], 'verified': r05['verified'], 'mismatched': r05['mismatched'], 'missing': r05['missing'], 'unlisted': r05['filesOnDiskNotInManifest']},
    'sourceManifestEqualsFrozen35': r05['sourceManifestEqualsFrozen35'], 'binding': r05['sourceBinding'], 'parentIsPackage11': r05['parentIsPackage11IVerified'],
    'constructionAccountsIdenticalToPackage11': r05['constructionAccountsIdenticalToPackage11'], 'allExportsEqualPackage11': r05['allExportsEqualPackage11'],
    'package11To12': r05['package11To12'], 'residualAssessment': r05['residualAssessment'],
    'thirteenCases': {'allAsExpected': r05['allThirteenAsExpected'],
                      'rows': [{k: r.get(k) for k in ('group', 'name', 'structural', 'semantic', 'semanticIdMatches', 'semanticReason', 'exportEqualsPackage11')} for r in r05['rows']]},
    'verifier': {'command': r05['verifier']['command'], 'returncode': r05['verifier']['returncode'], **r05['verification'], 'queryChecks': r05['queryChecks'],
                 'queryAssessment': r05.get('queryAssessment'), 'groupsAndReportDigestsEqualRoot': r05['myGroupsIncludingReportDigestsMatchRoot']},
    'retainedRunsReachIncoming': r05['retainedRunsReachIncoming'],
    'rootVerification': {'path': '/tmp/opensip-design-corrections/author-package-final35-verification.v1/verification.json',
                         'sha256': r05['rootVerificationSha256'], 'matchesDeclared': r05['rootVerificationMatchesDeclared'], 'standing': 'compared, not adopted'},
    'noRemintNoRelabel': 'exports byte-identical to package11; no historical execution relabelled', 'grantsNoPackageAcceptance': True,
    'receipt': 'receipts/r05-package12.json'}

# ---------------------------------------------------------------- rows
CONS35 = {
    'arDispositions/AR-12': ('RESTORED-ON-35-MUST-34-01-CLOSED',
        'RESTORED ON 35. The atom-level gap that partially reopened this row on 34 is closed: under source35 section 4 I1 no incoming '
        'negative can stand unless the subject universe has an available owed binding, verified on every cell of an independent matrix '
        'with no negative produced without it (receipts/r02-must-matrix.json M1/M2) and discriminated against frozen34 (M4). This row\'s '
        'own owners are byte-identical 34->35. Standing: atom-api; no retained Run reaches the incoming branch.'),
    'fwDispositions/FW-08': ('RESTORED-ON-35-MUST-34-01-CLOSED',
        'RESTORED ON 35. The undisclosed omission recorded on 34 is now disclosed and blocking: an incoming atom whose subject program '
        'has no available binding carries selector-unbound and stays unknown, while known matches and exceeded count bounds still decide '
        '(receipts/r02-must-matrix.json M1, K1). Owners byte-identical 34->35.'),
    'fwDispositions/FW-06': ('STRENGTHENED-HOLDS-ON-35-REMEASURED',
        'STRENGTHENED ON 34 AND STILL HOLDING ON 35, RE-MEASURED because the scope-commitment pairing path changed: every insertion order '
        'gives one result (E1 24 orderings, E2 480 orderings, with a Coverage paired by two scopes through the derived commitment), and six '
        'fresh interpreters with six hash-seeded orders give one digest (receipts/r06-determinism.json). I1 is order independent across 240, 1,440 '
        'and 240 plan-cell/map/attestation orderings in its three permutation cases (r02 P1).'),
    'inheritedResidualDispositions/DR-009': ('STRENGTHENED-HOLDS-ON-35-REMEASURED',
        'STRENGTHENED ON 34 AND STILL HOLDING ON 35: carrier determinism across processes re-measured on frozen35 (six processes, one '
        'digest; receipts/r06-determinism.json). Owners byte-identical 34->35.'),
    'arDispositions/AR-16': ('STRENGTHENED-HOLDS-ON-35-REMEASURED',
        'STRENGTHENED ON 34 AND STILL HOLDING ON 35: the typed coverage-unknown carrier is still first-with-deficiency in ascending '
        'coverage2 order on frozen35 (E2 carrier lockfile-missing on both endpoints; receipts/r06-determinism.json), and I1 adds a typed, '
        'shape-identical selector-unbound record rather than a new remedy path. Owners byte-identical 34->35.'),
}
F35_TEXT = {
    'F-01': 'the charter custody artifacts are among the members carried byte-identically from package11 (307 identical common members).',
    'F-02': 'the consumer-b.v13 v6/v7 assessment artifacts are among the 307 members byte-identical to package11.',
    'F-03': 'verify-package.py ran against frozen35 in this runtime: rc 0, 12,899 source files, 317 package files, 7/7 queries, group and report digests equal to root\'s receipt.',
    'F-05': 'ts-invalid-default-entry structurally ADMITS then semantically REFUSES ENUMERATION_BINDING_PROGRAM_ENTRY through the frozen35 identity-model.v3.py owner.',
    'F-06': 'ts-lawful-explicit-selection admits through both boundaries; two-binding construction still incomplete with a single explicit binding.',
    'F-08': 'the property probe stays a separate command (author-properties files unchanged from package11); README changed only for the source35 binding.',
    'F-10': 'mixed provenance unchanged: exportsChanged false, all 13 exports byte-identical to package11 and package10, constructionSourceVersion {typescriptDerivedGroups: 33, normalizedAndRustGroups: 30}, currentVerificationSourceVersion 35.',
    'F-11': 'helper files carrying this row are byte-identical to package11.',
    'F-12': 'weighting holds on the same exports: only checkpoint3/author-ts is helper-versus-owner; six positives are owner-derived self-consistency; three negatives derive from checkpoint3.',
    'F-13': 'package12 evaluation-residual-author-assessment.json binds frozen35, 30 rows independentGrade PENDING, TCB-SCOPE-01 over 13 dependents, evidence resolves against frozen candidate35.',
    'F-14': 'all 30 rows still proposed-account-supported-with-stated-limits; informational, no grade awarded.',
}
PKG = ('Verified on the source35-bound package12 (artifact manifest fb35036f..., 317/317 members, source-manifest byte-equal to '
       'frozen35, all 13 Run/control cases through open_run_closure AND close_run with my own decoder).')
tcb = set(BL['sharedAssumptionTCBSCOPE01']['dependentRows'])
counts = {}
for mp in MAPS:
    for rid, row in BL[mp].items():
        key = mp + '/' + rid
        info = r08['rows'][key]
        owners = info['owners']
        row['ownerFilesChangedIn34to35'] = sorted(p for p in owners if p in DELTA)
        row['ownerFilesUnchangedIn34to35'] = sorted(p for p in owners if p not in DELTA)
        row['ownerPathsResolveInFrozen35'] = all(p in m35 for p in owners) if owners else None
        if row.get('subjectOwnerFilesOn34'):
            row['subjectOwnerBytesEqual34and35'] = all(m34.get(p) == m35.get(p) and p in m35 for p in row['subjectOwnerFilesOn34'])
        if row.get('readingStandingLegacyCorrectionOn34'):
            row['readingStandingLegacyCorrectionStatusOn35'] = 'still accurate; the legacy string and its source34 qualification are both unchanged'
        n = len(owners)
        if key in CONS35:
            st, txt = CONS35[key]
            read = ('INHERITED ON EXACT BYTES for this row\'s %d owner file(s) (identical sha256 in the frozen34 and frozen35 manifests), '
                    'PLUS a fresh source35 assessment of the changed atom law\'s consequence for this subject.' % n)
        elif mp == 'fDispositions' and rid in F35_TEXT:
            st, txt = 'RE-VERIFIED-ON-PACKAGE12', PKG + ' Row-specific on 35: ' + F35_TEXT[rid]
            read = 'PACKAGE-BORNE: re-measured on package12 in this runtime (receipts/r05-package12.json); package11/10 readings stay in the baseline fields.'
        elif mp == 'fDispositions':
            st = 'INHERITED'
            if rid == 'F-07':
                txt = 'Inherited on 35: package12 carries the same exports byte-identically, so the measured predicate coverage (exists/none only) is unchanged.'
                read = 'INHERITED ON EXACT EXPORT BYTES (receipts/r05-package12.json exportEqualsPackage11 on all 13).'
            else:
                txt = ('Inherited on 35: every subject owner of this row (%s) is byte-identical 34->35; the source34 account in currentStatusOn34 '
                       'is inherited, not re-derived. The owning suites pass on frozen35 (launcher 16/16).' % ', '.join(p.split('/')[-1] for p in row['subjectOwnerFilesOn34']))
                read = 'INHERITED ON EXACT BYTES (manifests 34/35; receipts/r08-rows.json).'
        else:
            st = 'INHERITED'
            extra = ''
            if mp == 'evaluationResidualDispositions':
                extra = (' The author proposal remains PENDING independent grading; no grade is awarded.' +
                         (' One of the 13 TCB-SCOPE-01 dependents; the joint consequence is not closed.' if rid in tcb else ''))
            txt = ('Inherited on 35: all %d owner path(s) are byte-identical in the frozen34 and frozen35 manifests, none is in the 10-file delta, '
                   'and the changed incoming/carrier law does not bear on this row\'s subject. The source34 account in currentStatusOn34 is '
                   'inherited with explicit standing, not re-derived.%s' % (n, extra))
            read = ('INHERITED ON EXACT BYTES: %d owner file(s) with identical sha256 in the frozen34 and frozen35 manifests '
                    '(receipts/r08-rows.json); the substantive reading is the one recorded for source34.' % n)
        row['statusChangeOn35'] = st
        row['currentStatusOn35'] = txt
        row['readingStandingOn35'] = read
        row['currentFieldStandingOn35'] = 'currentStatusOn35 / readingStandingOn35 are the source35 account; every baseline field, including all *On34 fields, is preserved verbatim.'
        row['appliedByThisReview'] = False
        row['finalApplicationOutcomeGranted'] = False
        counts[st] = counts.get(st, 0) + 1
    J[mp] = BL[mp]
J['rowCarryForwardCounts'] = {'inherited': counts.get('INHERITED', 0), 'packageReverified': counts.get('RE-VERIFIED-ON-PACKAGE12', 0),
                              'crossOwner': sum(v for k, v in counts.items() if k not in ('INHERITED', 'RE-VERIFIED-ON-PACKAGE12')), 'byStatus': counts}
J['readingStandingAudit'] = dict(BL['readingStandingAudit'])
J['readingStandingAudit']['statusOn35'] = 'All nine source34 qualifications retained unchanged and still accurate; no legacy string edited.'
J['sharedAssumptionTCBSCOPE01'] = dict(BL['sharedAssumptionTCBSCOPE01'])
J['sharedAssumptionTCBSCOPE01']['statusOn35'] = 'One joint consequence over the same 13 rows; not closed; dependent owners byte-identical 34->35.'
J['dispositionCounts'] = {mp: len(BL[mp]) for mp in MAPS}
J['dispositionCounts']['total'] = sum(J['dispositionCounts'].values())
J['dispositionStandingForEveryRow'] = dict(BL['dispositionStandingForEveryRow'])
J['crossUnitStanding'] = dict(BL['crossUnitStanding'])
J['crossUnitStanding']['statusOn35'] = ('Carried unchanged: 28 condition-2 obligations retained; 32 product gates, 0 performed, condition 5 NOT MET; '
                                        '54 recovery cases unexecuted; TCB-SCOPE-01 one joint consequence over 13 rows; D9 implementation obligation '
                                        'on DR-007 / DR-011-R08 persists.')
J['grantsNothing'] = dict(BL['grantsNothing'])
J['correctionsToMyOwnPriorRecords'] = BL['correctionsToMyOwnPriorRecords'] + [{
    'id': 'C35-01', 'records': ['claude-independent-design.v34'],
    'correction': ('My source34 A-12(2) said a scope without enumeratorClosure is refused by the native carrier as soon as it is paired. That '
                   'held for an explicit null only; my fixture never removed the key. On frozen34 an ABSENT key skipped the carrier on every '
                   'consumption path I now test, and so did absent schemaVersion, snapshotId and targetUniverse and subjects:null on the '
                   'attestation path (receipts/r07-followups.json C2b). The source34 record is preserved unchanged; this qualifies it.'),
    'evidence': 'receipts/r03-a12.json, receipts/r07-followups.json'}]
J['verdictBasis'] = (
    'SOURCE35 DESIGN: ACCEPT, scoped to design and reference bytes. Custody: manifest eb45c22b... and archive f5292e68... match; 12,899 '
    'files and 736,823,249 bytes verify with nothing missing, mismatched or extra; the archive equals the manifest; the parent is the '
    'source34 I reviewed. My manifest-derived delta is 10 changed files, agreeing with root; four carry substance (contract section 4, '
    'atom_model, check-atoms, incoming-search schema metadata) and six only re-pin. MUST-34-01 is CLOSED: the incoming I1 guard equals '
    'a predictor written from the prose on every cell of my matrix, no incoming negative occurs without an available binding at the '
    'subject universe, outgoing and P2 are unchanged from frozen34, known matches and exceeded count bounds still decide, and results '
    'are order independent. A-12 is CLOSED for both published alternatives, including the missing-key carrier bypass the source35 '
    'correction found; one residual, pre-existing, retained-Run-unreachable dependency mapping fallback is advisory A-13. Suites, '
    'planning and package12 (13 cases through both boundaries, 7 queries) pass on frozen35 with zero drift; layer4 is retained. No new '
    'MUST or SHOULD. This grants no application outcome, readiness, qualification or acceptance of anything beyond these design bytes.')
J['limitations'] = [
    'Design and reference layers only; no product implementation, qualification or readiness.',
    'Closure evidence is atom-api (synthetic inputs through global atom-input admission and evaluate_atom), stock schema and native carrier as labelled; closed enumeration admission was not run and no retained Run reaches the changed incoming branches.',
    'Whether product configuration can express a per-unit capability narrowing remains unestablished; the source35 law no longer depends on it.',
    'The synthetic contradictory-family binding at U (a rust-cargo binding carrying a TypeScript-domain universe) still answers a negative at the atom API on both 34 and 35; enumeration-contract.v1.md section 1 requires an available binding\'s universe to be the native admission of that mode\'s own context, so this is not an admitted plan and is recorded as an observation, not an issue.',
    'A-10 limits retained; A-9 admitted-versus-unit limits retained; all 30 author residual proposals PENDING independent grading.',
    'Unchanged readings are inherited only on exact manifest-byte equality and labelled INHERITED.',
    'Author and root receipts, including check-atoms 89/89 and root\'s probes, were evidence I assessed; my conclusions rest on my own executions.',
    'No consumer output, diagnosis, report, root blind control or expected result was read.']
J['probeErrorsPreserved'] = [
    'r02 M3: my outgoing predictor treated the non-blocking cross-family disclosure as blocking on three cells; frozen34 == frozen35 held throughout; corrected and passing in r07 M3b.',
    'r02 P1 claim text said "all 720 plan-cell orders": exact for the U-bound case (six cells, 720 orders, 1,440 with reversal) but overstated for the two U-unbound cases (five cells, 120 orders, 240 with reversal); the receipt records 240 / 1,440 / 240. My first draft of this note wrongly called all three 240 and was corrected after the invariant check caught it.',
    'r03 C1 correctly failed on six dependency-fallback cases (now A-13); C2 and C3 were framed too strictly and are recomputed from the same receipt in r07 C2b and C3b.']
recs = sorted(f for f in os.listdir(RC) if f.endswith('.json') and f != 'i35-invariants.json')
J['evidenceReceipts'] = {'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B', 'receipts': {f: sha(os.path.join(RC, f)) for f in recs},
                         'probes': sorted(f for f in os.listdir(os.path.join(BASE, 'probes')) if f.endswith('.py')),
                         'frozen35DriftAfter': {'r02': r02['frozen35DriftAfter'], 'r03': r03['frozen35DriftAfter'], 'r04': r04['frozen35DeviationsAfterRuns'],
                                                'r05': r05['frozen35DeviationsAfter']}}
out = os.path.join(BASE, 'review.json')
json.dump(J, open(out, 'w'), indent=1, default=str)
print('rows', J['dispositionCounts'], '| carry', J['rowCarryForwardCounts'])
print('verdict', J['verdict'], '| MUST', J['newMustIssues'], '| SHOULD', J['newShouldIssues'], '| advisories', [a['id'] for a in J['advisories']])
print('bytes', os.path.getsize(out), 'sha256', sha(out))
