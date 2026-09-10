"""Assemble the fresh independent v10 review.json from the reviewer's measured probe results."""
import hashlib
import json
from pathlib import Path

W = Path('/tmp/opensip-design-corrections/post-reset-review.v10')
WORK = W / 'work'
SUBJECT = Path('/tmp/opensip-design-corrections/candidate-subject.v10')
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v10.json')

MSHA = '82c1be11d3b61908b2a45ebb6e59e71bb5cb31d8450a96a61857ced430e786fd'


def load(n):
    return json.loads((WORK / n).read_text())


p01, p02, p03 = load('p01.json'), load('p02.json'), load('p03.json')
p04, p05, p06 = load('p04.json'), load('p05.json'), load('p06.json')
p07, p08 = load('p07.json'), load('p08.json')
before = json.loads((W / 'subject-verify.before.json').read_text())
after = json.loads((W / 'subject-verify.after.json').read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


SUB_BASIS = ('No normative architecture, catalog, contract, schema or registry byte changed across '
             'the v9->v10 delta (independently recomputed manifest diff: 15 changed files, 0 '
             'removed, 0 normative schema/registry/contract, 0 docs/v2 or docs/catalog). The v9 '
             'individual disposition is re-affirmed against unchanged bytes and is neither '
             'extended nor re-litigated here.')

ar = {}
for i in range(1, 17):
    k = 'AR-%02d' % i
    if k == 'AR-01':
        ar[k] = {'disposition': 'ACCEPT', 'scopedBasis':
                 'Exact integer/lexical admission independently reproduced: foundation 1009 = '
                 '231+661+24+28+65 with 1099 verified pins; all six reference commands re-executed '
                 'by this reviewer in a disposable copy; all six logs byte-identical to the frozen '
                 'images and all regenerated in-tree reports byte-identical to frozen (0 files '
                 'differing, 0 new files).',
                 'selector': 'docs/coop/design-corrections/correction-crosswalk.proposed.json#/items[id=AR-01]'}
    elif k == 'AR-15':
        ar[k] = {'disposition': 'CHANGES_REQUIRED', 'scopedBasis':
                 'Routing itself is correct and honest and no crosswalk defect was found: AR-15 '
                 'status remains PROPOSED-SOURCE-MAP-PENDING-REVIEW-AND-APPLICATION, '
                 'currentReviewBinding remains PENDING-INDEPENDENT-REVIEW with no embedded future '
                 'digest, the crosswalk does not contain its own digest (verified: no self-hash '
                 'cycle), and latestCompletedReview correctly cites the v9 review at sha256 '
                 '13b4a4719799485139d01596eaceff93854d45d4af6d8fd689c42ff28ac9844e with its '
                 'unresolved v9-S1 recorded. It is graded CHANGES_REQUIRED here for the same '
                 'structural reason as v9: this review carries an unresolved SHOULD (v10-S1) that '
                 'the one effective integration narrative must absorb.',
                 'selector': 'docs/coop/design-corrections/correction-crosswalk.proposed.json#/items[id=AR-15]'}
    else:
        ar[k] = {'disposition': 'ACCEPT', 'scopedBasis': SUB_BASIS,
                 'selector': 'docs/coop/design-corrections/correction-crosswalk.proposed.json#/items[id=%s]' % k}

fw = {'FW-%02d' % i: {'disposition': 'ACCEPT', 'scopedBasis': SUB_BASIS,
                      'selector': 'docs/coop/design-corrections/correction-crosswalk.proposed.json#/items (FW-%02d forward-work row)' % i}
      for i in range(1, 16)}

inherited = {}
for i in range(1, 12):
    k = 'DR-%03d' % i
    inherited[k] = {'disposition': 'ACCEPT', 'scopedBasis':
                    'Parent row: successor obligation stated in inherited-residuals.proposed.md and '
                    'routed to an owning contract with retained reproducing evidence. No SATISFIED '
                    'grade granted; inherited history unedited; ' + SUB_BASIS,
                    'selector': 'docs/coop/design-corrections/inherited-residuals.proposed.md#%s' % k}
for i in range(1, 17):
    k = 'DR-011-R%02d' % i
    basis = ('Sub-row of DR-011 routed in inherited-residuals.proposed.md; retained evidence '
             'unedited and no SATISFIED grade granted. ' + SUB_BASIS)
    if i == 10:
        basis = ('DR-011-R10 (blind reconstructability) remains OPEN: no Bv3 exists and this '
                 'review does not grant reconstructability. ' + SUB_BASIS)
    if i == 12:
        basis = ('Evaluation proof row: all 30 evaluation subresiduals (19 RES, 7 NB, 4 measured '
                 'escapes) carry individual dispositions in '
                 'evaluation-residual-dispositions.proposed.json, whose own standing does not '
                 'close the parent row before independent review and application. ' + SUB_BASIS)
    inherited[k] = {'disposition': 'ACCEPT', 'scopedBasis': basis,
                    'selector': 'docs/coop/design-corrections/inherited-residuals.proposed.md#%s' % k}

SCOPED_BASIS = (
    'SCOPED strictly to what this design-correction review can decide: whether the current '
    'crosswalk and source map ROUTE this scoped re-review owner without claiming or re-opening its '
    'historical acceptance. Verified independently: %s is an ownerRow of AR-15 in '
    'correction-crosswalk.proposed.json#/items[id=AR-15]/ownerRows; AR-15 status is '
    'PROPOSED-SOURCE-MAP-PENDING-REVIEW-AND-APPLICATION; currentReviewBinding standing is '
    'PENDING-INDEPENDENT-REVIEW with no embedded future digest and no self-hash cycle; and '
    'docs/v2/architecture/08-decision-and-readiness-register.md is byte-unchanged across the '
    'v9->v10 delta (exact manifest diff: 0 docs/v2 files changed), so the historical grade is '
    'preserved as history and is neither extended nor re-litigated here.')

scoped = {}
for i in range(201, 206):
    k = 'DR-%d' % i
    scoped[k] = {
        'disposition': 'ACCEPT_SCOPED',
        'basis': SCOPED_BASIS % k,
        'selectors': [
            'docs/coop/design-corrections/correction-crosswalk.proposed.json#/items[id=AR-15]/ownerRows',
            'docs/coop/design-corrections/correction-crosswalk.proposed.json#/items[id=AR-15]/status',
            'docs/coop/design-corrections/correction-crosswalk.proposed.json#/items[id=AR-15]/currentReviewBinding',
            'docs/v2/architecture/08-decision-and-readiness-register.md#%s' % k,
        ],
        'notClaimed': ('historical acceptance is not extended to current bytes; product '
                       'qualification, readiness and application are not granted'),
    }

V9_ADVISORY_TITLES = {
    'v9-A1': 'The 723-byte edition-map figure is reproducible only when the wrapping is stated',
    'v9-A2': 'LEVEL_SPECIFICATION remains a fixture stand-in',
    'v9-A3': 'L1-L3 are custody and framing only; no normalizer is qualified',
    'v9-A4': 'The TypeScript suffix table is deliberately conservative and will under-detect',
    'v9-A5': 'Every Rust universe carrying clones facts must commit a SourceUnitOwnershipV1',
    'v9-A6': 'The integration builder is coauthored fixture composition, not an independent oracle',
    'v9-A7': 'Whole-manifest integration checker custody remains intentional',
    'v9-A8': 'A Plan may select several admitted native contexts of one language',
    'v9-A9': 'Application should bind frozen snapshot bytes, not working-tree bytes',
    'v9-A10': 'Pin-inventory truncation remains undetectable by the projection validator alone',
    'v9-A11': 'Probe files in retained coauthor evidence mix diagnostic output with JSON',
}
V9_ADVISORY_BASIS = {
    'v9-A1': ('Independently re-derived: canonical wrapping adds exactly 12 bytes '
              '(this reviewer measured bare 105 vs wrapped 117 on a synthetic four-edition map), '
              "which is exactly 723-711. C({'edition': map}) = 723 and the bare map = 711 are "
              'therefore arithmetically consistent; the original conclusion is unchanged and the '
              'advisory (state the wrapping) stands.'),
    'v9-A6': ('Provenance re-verified exactly: integration-fixtures.py declares source '
              'check-identity.py SHA256 a7f7d393d3b1c9284ce1109b0458b9cb63708794c371365be22e8c5afc4f053c, '
              'which equals the actual released checker digest, and that provenance line is the '
              'ONLY change to the file across the delta. The fixture is nonetheless COPIED from '
              'the checker, so it remains synthetic composition and is not an independent oracle. '
              'Advisory preserved, not discharged.'),
    'v9-A10': ('Independently reproduced: deleting one row from the 1099-row foundation pin '
               'inventory leaves every remaining row verifying, so a pure projection over the pin '
               'list cannot detect truncation. Detection requires an independent expected count or '
               'inventory. Advisory preserved.'),
}
prior_adv = {}
for k, t in V9_ADVISORY_TITLES.items():
    prior_adv[k] = {
        'title': t,
        'disposition': 'CARRIED',
        'basis': V9_ADVISORY_BASIS.get(k, (
            'Re-affirmed on unchanged bytes: the advisory concerns material untouched by the '
            'v9->v10 delta (no normative schema/registry/contract byte changed; the native, '
            'security and integration reports are byte-identical across the delta). Carried, not '
            'discharged.')),
    }

review = {
    'artifact': 'fresh independent design/architecture/reference review of frozen candidate v10',
    'version': 'v10',
    'reviewer': ('actual Claude, fresh independent session; authored none of the subject bytes; '
                 'neither coauthor 5dec928a-6357-4726-9ea8-49a3079fb726 nor prior independent '
                 'reviewer 93403103-b133-4d69-8700-627712411137'),
    'date': '2026-09-06',

    'verdict': 'CHANGES_REQUIRED',
    'verdictBasis': (
        'One new SHOULD (v10-S1) is unresolved. The gate is strict: any unresolved MUST or SHOULD '
        'is CHANGES_REQUIRED, and no headline ACCEPT with a nonblocking-Should explanation is '
        'available. The prior finding v9-S1 IS substantively resolved and independently confirmed, '
        'and every other assertion tested in this review held; but the traversal that resolves it '
        'carries a residual order dependence of the SAME class root previously found in the draft, '
        'which this reviewer reached behaviorally.'),

    'subject': {
        'manifestSha256': MSHA,
        'manifestPath': 'docs/coop/design-corrections/reviews/candidate-subject.v10.json',
        'snapshotRoot': str(SUBJECT),
        'fileCount': before['declaredFileCount'],
        'totalBytes': before['declaredTotalBytes'],
        'predecessorManifestSha256': before['predecessorManifestSha256'],
        'predecessorManifestIndependentlyVerified': True,
    },

    'custody': {
        'manifestDigestMatchesInstruction': before['manifestSha256Matches'],
        'verifiedBeforeReview': {
            'filesVerified': before['declaredFileCount'], 'missing': len(before['missing']),
            'digestMismatches': len(before['digestMismatches']),
            'lengthMismatches': len(before['lengthMismatches']),
            'undeclaredFiles': before['undeclaredCount'],
            'nonRegularEntries': len(before['nonRegularEntries']),
            'totalBytesMatches': before['totalBytesMatches'], 'clean': before['VERDICT_CLEAN']},
        'verifiedAfterReview': {
            'filesVerified': after['declaredFileCount'], 'missing': len(after['missing']),
            'digestMismatches': len(after['digestMismatches']),
            'lengthMismatches': len(after['lengthMismatches']),
            'undeclaredFiles': after['undeclaredCount'],
            'nonRegularEntries': len(after['nonRegularEntries']),
            'totalBytesMatches': after['totalBytesMatches'], 'clean': after['VERDICT_CLEAN']},
        'beforeEqualsAfter': before == after,
        'frozenSubjectUnmodifiedByThisReview': True,
        'allReviewerWritesConfinedTo': str(W),
        'reviewerRanNoSubagents': True,
        'reviewerMadeNoSourceEdits': True,
        'reviewerMadeNoCommitPushResetCheckoutClean': True,
        'originalUserV1Manifest': {
            'sha256': 'e7403b702d419f381be1cdbee7b886303fb43106b86985bc2f8ec63f5687a0ac',
            'fileCount': 1192, 'independentlyVerified': True},
        'priorIndependentReviewV9': {
            'path': 'docs/coop/design-corrections/reviews/post-reset-review.v9/review.json',
            'sha256Recomputed': '13b4a4719799485139d01596eaceff93854d45d4af6d8fd689c42ff28ac9844e',
            'matchesInstruction': True, 'retainedUnchanged': True,
            'verdict': 'CHANGES_REQUIRED', 'newMustIssues': 0, 'newShouldIssues': ['v9-S1']},
        'protectedHistoricalFiles': {
            'declared': 31, 'independentlyReverifiedUnchanged': 31,
            'oracle': ('verified against the live repository, since the frozen subject is a SCOPED '
                       '2502-file snapshot that contains only 10 of the 31; the reviewer corrected '
                       'this harness assumption rather than reporting a false gap'),
        },
    },

    'exactDelta': {
        'basis': 'independently recomputed from the v9 and v10 manifests',
        'added': 214, 'removed': 0, 'changed': 15,
        'changedFiles': p06['changedAcrossDelta'],
        'implementationSourcesChanged': [
            'docs/coop/design-corrections/foundation/identity-model.py',
            'docs/coop/design-corrections/foundation/check-identity.py'],
        'normativeSchemaRegistryContractChanged': p06['normativeSchemaRegistryChanged'],
        'architectureAndCatalogChanged': p06['architectureAndCatalogChanged'],
        'authorsClaimVerified': (
            'the claim "current normative product contracts, schemas and registry bytes are '
            'unchanged from frozen v9" is TRUE: 0 of 244 normative-classified files and 0 of the '
            'docs/v2 + docs/catalog set changed, and no file was removed'),
        'pinChurnAccountedFor': (
            'every source-pin diff is exactly the repin of the changed inputs - check-identity.py '
            'd07cfe7f->a7f7d393, identity-model.py 1a563aa1->f200232b, identity-report '
            '5336f549->10ca48ec, crosswalk d6126348->9560a51e - with no historical repin'),
    },

    'suiteReproduction': {
        'commandsReproduced': 6,
        'method': ('run-final-v10.py executed by this reviewer against an independently verified '
                   'disposable copy of the frozen subject; never regenerated inside the frozen source'),
        'allExitZero': True,
        'logsByteIdenticalToFrozen': ['foundation', 'security', 'native', 'workflows',
                                      'workflow-surface', 'integration'],
        'regeneratedReportsDifferingFromFrozen': 0,
        'newFilesCreatedByRerun': 0,
        'measuredCounts': {
            'foundation': {'total': 1009, 'components': {'foundation': 231, 'identity': 661,
                                                         'product-quality': 24,
                                                         'product-configuration': 28,
                                                         'array-order': 65},
                           'sumMatches': True, 'sourcePinsVerified': 1099},
            'security': {'casesPassed': 456, 'invariantSweeps': 10},
            'native': {'casesPassed': 151, 'matrixCells': 60, 'qualifiedCells': 0},
            'workflows': {'checksPassed': 1290},
            'integration': {'checksPassed': 363},
        },
        'validationSummaryAgreesWithExecutedReports': True,
        'pinsAuthenticateTransitiveInputs': {
            'tested': True,
            'method': ('appended one comment line to identity-model.py - a transitive import, not '
                       'the entry script - in a throwaway copy'),
            'result': ('sourcePinsValid false, changedOrMissing names identity-model.py, '
                       'checksExecuted false, process exit code 1'),
        },
    },

    'priorFindingDispositions': {
        'v9-S1': {
            'title': ('The relation digest law declares three inadmissible conditions and only two '
                      'are consumed; the unannotated-field limb is enforced nowhere'),
            'severity': 'SHOULD',
            'disposition': 'RESOLVED',
            'independentlyConfirmed': True,
            'evidence': {
                'v9ExperimentReRun': (
                    'the v9 reviewer injected an unannotated DigestHex/Sha256Text/CanonicalPath '
                    'field into each of the 13 relation selectors (39 injections) and every one '
                    'ADMITTED. This reviewer re-ran the identical 39 injections against BOTH real '
                    'frozen source images with the identical relation document (verified '
                    'byte-identical across v9 and v10): v9 admitted 39/39, v10 refuses 39/39 at '
                    'RELATION_DIGEST_UNANNOTATED.'),
                'notAStub': (
                    'the discriminating evidence is a source-image comparison, not a neutralisation '
                    'stub; the author\'s own failed stub is retained in the subject and is not '
                    'treated as a passing enforcement-removal test'),
                'coverageAcrossForms': {
                    'directRefInjections': p01['SUMMARY']['directRefRefusals'],
                    'inlinePatternInjections': p01['SUMMARY']['inlineRefusals'],
                    'transitiveAliasInjections': p01['SUMMARY']['aliasRefusals'],
                    'nestedArrayNullableShapes': '%d of %d' % (p01['SUMMARY']['shapeRefusals'],
                                                               p01['SUMMARY']['shapeTotal']),
                    'existingAnnotationRemovals': p01['SUMMARY']['removalRefusals'],
                },
                'positiveControls': {
                    'shippedDocumentAdmitsAll13': p01['SUMMARY']['shippedAdmits'],
                    'lawfulAnnotatedNotJoinedAdmits': '%d of 39' % p01['SUMMARY']['lawfulAdmits'],
                    'nonGovernedUnannotatedFieldsStillAdmit': '%d of 13' % p01['SUMMARY']['nonGovernedAdmits'],
                    'note': ('the refusals are discriminating rather than "any new field refuses"'),
                },
                'authoredCheckNowTruthful': (
                    'the check named every-relation-payload-digest-and-path-field-is-annotated-and-'
                    'joined evaluated True in v9 against a document carrying an unannotated '
                    'CanonicalPath field; against v10 the same document now refuses'),
                'threeLimbConsistency': (
                    'a 12-cell matrix of three effective annotation locations (field-local, '
                    'intermediate alias $def, branch parent) x four cases (lawful not-joined, '
                    'invalid retention, annotated-missing-join, unannotated) behaves identically '
                    'across all three locations with the exact intended causes, closing root\'s v8 '
                    'inherited-limbs counterexample class'),
                'preservationOfEarlierLimbs': (
                    'RELATION_DIGEST_RETENTION, RELATION_DIGEST_LAW_RESIDUE and '
                    'RELATION_JOIN_FIELD_UNKNOWN retain their intended causes; vcs-change '
                    'previousPath keeps its declared not-joined exemption and the shipped document '
                    'admits for all 13 relations'),
            },
            'residual': ('the traversal that resolves v9-S1 carries a residual order dependence '
                         'recorded separately as v10-S1; v9-S1 itself is resolved'),
        },
    },

    'newMustIssues': [],

    'newShouldIssues': [
        {
            'id': 'v10-S1',
            'title': ('The new annotation sweep\'s same-path aggregation is order-dependent: an '
                      'annotated sighting CAN erase an unannotated one, contrary to the rule '
                      'record() states, so an unannotated governed field can be admitted'),
            'severity': 'SHOULD',
            'selectors': [
                'foundation/identity-model.py:333-343 relation_digest_annotation_coverage.record',
                'foundation/identity-model.py:342 (the merge test)',
                'foundation/relation-payload-schemas.v2.json#/x-opensip-digest-law/residueRule',
                'foundation/relation-payload-schemas.v2.json#/x-opensip-digest-law/standing',
                'foundation/check-identity.py check branch-order-does-not-decide-admissibility',
                'reviews/codex-post-reset.v1/annotation-traversal-final-recheck.v10/result.json',
            ],
            'observed': (
                'record() documents the intended invariant explicitly: "Never let an annotated '
                'sighting erase an unannotated one at the same path - ... so admissibility cannot '
                'depend on branch order." The implementation is:\n'
                '    annotations=previous[\'annotations\']+[a for a in annotations if a not in previous[\'annotations\']]\n'
                '    if not previous[\'annotations\'] or not annotations:annotations=[]\n'
                'The local name `annotations` is REBOUND to the merged list on the first line '
                'before it is tested on the second, so `not annotations` can only be true when '
                'previous and incoming were BOTH empty (a no-op). The effective rule therefore '
                'reduces to "poison iff the FIRST-RECORDED sighting was unannotated", which is a '
                'branch-order dependence rather than order independence. Unannotated-then-annotated '
                'refuses; annotated-then-unannotated ADMITS.'),
            'behaviouralProof': {
                'caseA': {
                    'shape': ('a draft-2020-12 node carrying BOTH a $ref to a container $def and a '
                              'sibling `properties` refinement of the same member; walk() follows '
                              'the $ref first and then the node\'s own properties, so both land on '
                              'the same path'),
                    'containerUnannotated_localAnnotated': p03['caseA']['unannotated_seen_first']['verdict'],
                    'containerAnnotated_localUnannotated': p03['caseA']['annotated_seen_first']['verdict'],
                    'refusalCause': p03['caseA']['unannotated_seen_first']['cause'],
                    'orderDecidesAdmission': p03['ASSESSMENT']['caseA_orderDecidesAdmission'],
                },
                'caseB': {
                    'shape': ('`items` and `additionalProperties` on one node both map to '
                              "path + '[]'; the two documents contain the IDENTICAL pair of "
                              'subschemas and differ only in which JSON key is written first'),
                    'itemsWrittenFirst': p03['caseB']['items_written_first']['verdict'],
                    'additionalPropertiesWrittenFirst': p03['caseB']['addprops_written_first']['verdict'],
                    'refusalCause': p03['caseB']['items_written_first']['cause'],
                    'pureKeyOrderSwap': p03['ASSESSMENT']['caseB_pureKeyOrderSwap'],
                    'orderDecidesAdmission': p03['ASSESSMENT']['caseB_orderDecidesAdmission'],
                },
                'positiveControls': {
                    'unmodifiedShippedDocument': p03['controls']['shipped_document']['verdict'],
                    'singleUnannotatedLeafBehindContainerRef':
                        p03['controls']['container_leaf_unannotated_only']['verdict'],
                    'singleLawfulAnnotatedLeafBehindContainerRef':
                        p03['controls']['container_leaf_annotated_only']['verdict'],
                    'controlsDiscriminate': p03['ASSESSMENT']['controlsDiscriminate'],
                },
                'allHypotheticalDocumentsMetaschemaValid':
                    p03['ASSESSMENT']['allHypotheticalDocumentsMetaschemaValid'],
                'mergeBranchReachability': {
                    'method': ('instrumented record() in a throwaway copy to log every same-path '
                               'collision, then ran the FULL authored identity suite'),
                    'collisionsDuringAuthoredSuite': 0,
                    'authoredSuiteChecks': 661,
                    'collisionsDuringReviewerCounterexample': 2,
                    'loggedTuples': [['file.probe[]', False, True], ['file.probe[]', True, False]],
                    'interpretation': (
                        'the merge that carries the order-independence claim is reached ZERO times '
                        'by the shipped document, by all 59 new annotation checks, and by all four '
                        'retained root rechecks. Root\'s counterexample was fixed structurally by '
                        'giving each oneOf branch its own path, which removed the collision '
                        'instead of exercising the merge, so the merge itself has never been tested'),
                },
            },
            'whyItMatters': (
                'This is the identical rationale that made v9-S1 and v8-S1 SHOULDs and was accepted '
                'and fixed in both cases. The declared law states "There is no default and no '
                'residue: a new such field added without an annotation is inadmissible", and the '
                'residueRule states an unannotated digest/path field is inadmissible. In case A and '
                'case B an unannotated governed field IS present and IS admitted, so the reference '
                'contradicts the normative law text it exists to consume - not merely an internal '
                'docstring. An implementer building from the law, or from record()\'s stated rule, '
                'would implement order independence; the reference does not, so two conforming '
                'implementations would disagree on whether a document is admissible. It is also the '
                'same defect CLASS root raised against the draft, re-entering through the general '
                'merge after the specific oneOf case was closed.'),
            'scope': (
                'Hypothetical registered SCHEMA EDIT only, exactly like v9-S1, and NOT a current '
                'payload or Run attack. Independently bounded: the shipped document has 7 governed '
                'sightings, all annotated, all at distinct paths, so no shipped relation is '
                'affected; relation-payload-schemas.v2.json is pinned in all four pin sets with '
                'matching digests and pin drift is a hard exit-1 failure; and both '
                'relation_digest_annotation_coverage and relation_annotation_closure are pure '
                'schema-only functions with no file I/O and no snapshot, Run or cache reference, '
                'so owning-Run admission and the payload decode memo are untouched.'),
            'intendedCause': ('RELATION_DIGEST_UNANNOTATED should be raised in BOTH orders; it is '
                              'raised in only one'),
            'suggestedDirection': (
                'test the INCOMING annotations before rebinding, so that a sighting is uncovered if '
                'EITHER the previous or the incoming sighting was unannotated, and add an authored '
                'check that actually reaches the merge - the present authored suite never does. '
                'This reviewer deliberately proposes no patch text and made no source edit.'),
            'notClaimed': ('no current admission, identity, Run, report count or shipped byte is '
                           'affected; every one of the six reference commands still passes and '
                           'reproduces byte-identically'),
        },
    ],

    'newAdvisories': [
        {
            'id': 'v10-A1',
            'title': ('The implemented inadmissible-cause set has outgrown the three conditions the '
                      'law text declares'),
            'observed': ('residueRule declares three inadmissible conditions. The reference now '
                         'raises RELATION_DIGEST_UNANNOTATED, RELATION_DIGEST_RETENTION, '
                         'RELATION_DIGEST_LAW_RESIDUE, RELATION_JOIN_FIELD_UNKNOWN, '
                         'RELATION_DIGEST_ANNOTATION_CONFLICT and '
                         'RELATION_DIGEST_UNJOINABLE_LOCATION. UNJOINABLE_LOCATION is fairly read '
                         'as a sharper cause for limb 1, but ANNOTATION_CONFLICT is a genuinely new '
                         'inadmissible condition the law text does not name.'),
            'whyNonBlocking': ('both additions only ever REFUSE more, never admit more, so they '
                               'cannot weaken the law; refusing rather than inventing a precedence '
                               'between disagreeing annotations is the conservative correct choice, '
                               'and the technical review states this boundary openly'),
            'suggestion': 'name the conflict condition in the law text when the law is next edited',
        },
        {
            'id': 'v10-A2',
            'title': ('The effective-annotation inheritance rule exists only in reference '
                      'implementation docstrings, not in the normative law document'),
            'observed': ('the x-opensip-digest-law object contains no occurrence of alias, inherit, '
                         'branch, nested, array, container, oneOf, precedence or "anywhere on the '
                         'path". The rule that an x-opensip-digest anywhere on the path to a '
                         'governed leaf covers it - including an intermediate alias $def but '
                         'deliberately NOT the terminal governed $def - appears only in '
                         'identity-model.py and check-identity.py and in retained review records.'),
            'whyItMatters': ('a NEW fresh blind consumer reconstructing from the normative subset '
                             'would have to re-derive this rule from the reference implementation '
                             'rather than the law; relevant to DR-011-R10, which remains open'),
            'whyNonBlocking': ('the reference implementation is itself part of the delivered design '
                               'reference, and the technical review explicitly frames this as the '
                               'present reference boundary'),
        },
        {
            'id': 'v10-A3',
            'title': 'Check-count growth is not coverage growth, and this delta demonstrates it',
            'observed': ('the identity suite grew 602 -> 661 with 59 new annotation checks and zero '
                         'removed and zero changed results, yet reachability instrumentation shows '
                         'the record() merge branch is executed 0 times across the entire 661-check '
                         'suite. The technical review already cautions that "increased test counts '
                         'are not a completeness claim"; this is a measured instance.'),
            'suggestion': ('pair new enforcement code with a reachability measurement, not only '
                           'with new passing cases'),
        },
    ],

    'priorAdvisoryDispositions': prior_adv,
    'carriedAdvisoryAccount': {
        'path': 'reviews/codex-post-reset.v1/advisory-application-account.v10.proposed.json',
        'itemsCarried': 25,
        'independentlyRead': True,
        'disposition': ('the 25 carried v5-v9 advisory accounts are present with actual review '
                        'citations and remain PROPOSED; this review does not grant Codex assent and '
                        'does not discharge any of them'),
    },

    'arDispositions': ar,
    'fwDispositions': fw,
    'inheritedResidualDispositions': inherited,
    'scopedReviewOwnerDispositions': scoped,

    'productQualificationGates': {
        'count': 32, 'demonstrated': 0,
        'basis': ('all 32 items in qualification-gates.proposed.json carry demonstrated false over '
                  'the four canonical platform families linux-x86_64-gnu, linux-aarch64-gnu, '
                  'macos-aarch64 and macos-x86_64. This review demonstrates none of them and grants '
                  'none. No compiler, OS, storage or crypto behaviour was measured; all such '
                  'observations remain synthetic TCB assumptions and qualify nothing.'),
    },
    'evaluationSubresiduals': {
        'count': 30,
        'basis': ('evaluation-residual-dispositions.proposed.json carries an individual disposition '
                  'for each of the 19 RES, 7 NB and 4 measured-escape rows under DR-011-R12; its '
                  'own standing states it does not close the parent row before independent review '
                  'and application. Unchanged across this delta.'),
    },
    'completeIntendedProductScope': {
        'D-371': 'not applied, not granted by this review',
        'D-372': 'not applied; the central readiness/application act remains intentionally unapplied',
        'design': ('one design implemented in stages, TS/JS/Rust over exactly four macOS/Linux '
                   'machine IDs; no implicit execution, no untrusted ecosystem, no bundled semantic '
                   'model and no full Map application are in scope'),
    },

    'independentProbes': [
        {'id': 'p01', 'name': 'third-limb enforcement across 13 relations x 3 forms x 4 shapes',
         'file': 'probes/p01_third_limb.py', 'result': 'work/p01.json',
         'summary': p01['SUMMARY']},
        {'id': 'p02', 'name': 'order-independence of same-path aggregation',
         'file': 'probes/p02_order_independence.py', 'result': 'work/p02.json',
         'summary': p02['ASSESSMENT']},
        {'id': 'p03', 'name': 'hardened order-dependence counterexample with metaschema validation',
         'file': 'probes/p03_order_hardened.py', 'result': 'work/p03.json',
         'summary': p03['ASSESSMENT']},
        {'id': 'p04', 'name': 'three limbs x three effective annotation locations matrix',
         'file': 'probes/p04_limbs_and_locations.py', 'result': 'work/p04.json',
         'summary': p04['ASSESSMENT']},
        {'id': 'p05', 'name': 'enforcement-absent comparison against the real frozen v9 image',
         'file': 'probes/p05_enforcement_absent.py', 'result': 'work/p05.json',
         'summary': p05['ASSESSMENT']},
        {'id': 'p06', 'name': 'preservation: manifest invariance plus recomputed identities',
         'file': 'probes/p06_preservation.py', 'result': 'work/p06.json',
         'summary': p06['ASSESSMENT']},
        {'id': 'p07', 'name': 'scope bounding of hypothetical registry-document mutation',
         'file': 'probes/p07_scope.py', 'result': 'work/p07.json', 'summary': p07['ASSESSMENT']},
        {'id': 'p08', 'name': 're-test of cheaply decidable carried advisories',
         'file': 'probes/p08_advisories.py', 'result': 'work/p08.json', 'summary': p08['ASSESSMENT']},
    ],

    'preservationOfV9ConfirmedBehaviour': {
        'method': ('exact manifest diff plus targeted probes, rather than re-deriving every v9 '
                   'confirmation'),
        'identityCheckIds': {'v9': 602, 'v10': 661, 'added': 59, 'removed': 0,
                             'sharedWithChangedResult': 0,
                             'allV10Pass': True},
        'reportsByteIdenticalAcrossDelta': [
            'integration-report.v1.json (363 checks)',
            'native/native-evidence-report.v2.json (151 cases, 60 cells, 0 qualified)',
            'security/security-lifecycle-report.v1.json (456 cases, 10 sweeps)'],
        'recomputedStable': {
            'framePrefix': p06['ASSESSMENT']['framePrefixStable'],
            'domainPrefixTable': p06['ASSESSMENT']['prefixTableStable'],
            'framedBodyIdentities': p06['ASSESSMENT']['allFramedBodyIdentitiesStable'],
            'identifiersAcrossAllRegisteredDomains': p06['ASSESSMENT']['allIdentifiersStable'],
            'shippedRelationsAdmitOnBothImages': p06['ASSESSMENT']['shippedRelationsAdmitOnBothImages'],
        },
        'itemsCoveredByInvarianceRatherThanRerun': (
            'own-snapshot file hash/length/path joins; owner-specific admission outside the payload '
            'decode memo; valid complete file@enumerated Coverage with non-applicable resolution; '
            'the 13 registered full-schema-document/selector relations; retained normalized body '
            'grammar and level-specification custody; L0 recomputation versus L1-L3 custody and '
            'framing only; raw32 compiler/dialect body version; actual JavaScript body language '
            'through the TypeScript engine; target-specific Rust edition and explicit shared-path '
            'selection; valid #paths/maxsizes/derivedUnitIdentity; stable body ids under unrelated '
            'ownership changes; empty-view Coverage prerequisites preserving honest partial and '
            'healthy empty results; all 4 CVE1 gates; native Coverage producer admission; Plan '
            'enumerator membership; TS custom config, ordered repeated extends and jsconfig '
            'provenance; typed array order separate from canonical encoding; cache lookup versus hit '
            'validation; workflow required-output failure and Run preservation; complete current '
            'leased pin inventory versus pure projection; and generic mutation versus repair apply '
            'replay - each of these is asserted by a check whose id and result are byte-identical '
            'across the delta, or lives in a report that is byte-identical across the delta'),
        'noClonefactsCaveatPreserved': (
            'no-clone-facts alone still does not authorize complete clone Coverage with absent '
            'dialect prerequisites; the owning Coverage law is unchanged bytes'),
    },

    'harnessErrorsCorrectedNotCountedAsDefects': [
        {'error': ('the reviewer first checked the 31 protected historical files against the frozen '
                   'subject and saw 21 as missing'),
         'correction': ('the frozen subject is a SCOPED 2502-file snapshot containing only 10 of '
                        'the 31; the correct oracle is the live repository, against which all 31 '
                        'verify unchanged (openingSha256 == currentSha256 == recomputed). Reported '
                        'as a corrected harness assumption, not as a subject defect.')},
        {'error': 'the first pin-scope probe assumed every pin file uses a "files" key',
         'correction': ('native/source-pins.v2.json and security/source-pins.v1.json use "pins"; '
                        'the probe was corrected and all four pin sets then verified')},
        {'error': 'probes could not import the shared harness under python -I',
         'correction': 'sys.path is set explicitly inside each probe; -I -B retained as required'},
    ],

    'limitations': [
        'Not product qualification. No OS, compiler, cargo, rustc, linker, crypto, SQLite, filesystem, clock, lease or end-to-end measurement was performed and none is claimed. Every native, platform and toolchain observation remains an explicit synthetic trusted input and qualifies nothing.',
        'Synthetic TCB inputs confer no qualification. The reference store, evaluator and replay callback are trusted-host assumptions, not adversarial isolation.',
        'The integration fixture is copied from the released checker with exact provenance; fixture composition is not an independent oracle and this review does not treat it as one.',
        'Not the blind consumer review. Reconstructability from the normative bytes alone is a different act; no Bv3 exists and DR-011-R10 remains open. This review does not grant reconstructability.',
        'Not application and not readiness. The central readiness/application act remains intentionally unapplied, condition 5 remains NOT MET, and application acceptance is scoped separately and is not granted here.',
        'No implementation authority. No implementation, source edit, product change, commit, push, checkout, reset or clean was performed and none is authorized.',
        'Historical grades are not extended. Prior verdicts remain limited to their own bytes; no old grade is treated as blanket acceptance of these bytes.',
        'This review does not create a self-hash acceptance cycle: its own digest is not embedded in the subject it reviews.',
        'The v10-S1 counterexamples are hypothetical schema documents, metaschema-valid under draft 2020-12, exercising forms the implementation explicitly claims to support. They are not current payload attacks and no future schema feature beyond the declared language is demanded.',
        'This reviewer ran no subagents and wrote only under ' + str(W) + '.',
    ],

    'claimsExplicitlyNotMade': [
        'no acceptance of the v10 bytes',
        'no Codex assent',
        'no blind consumer acceptance',
        'no application or readiness acceptance',
        'no product qualification and no gate demonstration',
        'no authorization to implement, commit or push',
        'no claim that the authored suite passing constitutes acceptance',
    ],

    'requiredNextActs': [
        'correct v10-S1 in the same-path aggregation and add an authored check that actually reaches the merge',
        'freeze the corrected successor and obtain a fresh independent review at zero unresolved MUST and SHOULD',
        'actual Codex assent covering all 25 carried advisories and the 3 new v10 advisories',
        'a NEW fresh blind consumer B on the accepted normative bytes',
        'a complete, independently reviewed application and readiness reconciliation, with activation last',
    ],

    'readinessChanged': False,
    'implementationAuthorized': False,
    'productQualification': False,
    'condition5': 'NOT MET',
    'applicationAccepted': False,
    'blindAccepted': False,
}

path = W / 'review.json'
path.write_text(json.dumps(review, indent=2, sort_keys=False) + '\n')
print('wrote', path, path.stat().st_size, 'bytes')
print('verdict', review['verdict'], '| MUST', len(review['newMustIssues']),
      '| SHOULD', len(review['newShouldIssues']), '| advisories', len(review['newAdvisories']))
