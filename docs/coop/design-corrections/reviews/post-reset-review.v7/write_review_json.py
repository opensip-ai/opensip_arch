import json, hashlib
from pathlib import Path

OUT = Path('/tmp/opensip-design-corrections/post-reset-review.v7')
P = OUT / 'probes'
def load(n):
    p = P / n
    return json.loads(p.read_text()) if p.is_file() else {}

p3, p5, p6 = load('p3.json'), load('p5.json'), load('p6.json')
p7, p8, p10, p11, p12 = load('p7.json'), load('p8.json'), load('p10.json'), load('p11.json'), load('p12.json')

AR_BASIS = ("Row contract/selector/evidence paths and unit all resolve in the frozen subject; row "
            "carries the verified three-way review separation (immutable historical, exact completed "
            "v6 predecessor pinned by rehashed bytes cb345532..., pending unhashed current binding); "
            "status asserts no award; the cited unit executes at its declared count with a "
            "byte-identical deterministic report. Accepted as a review record, not an award of readiness.")

ar = {}
for i in range(1, 17):
    ar['AR-%02d' % i] = {
        'disposition': 'ACCEPT',
        'scopedBasis': AR_BASIS,
        'selectors': ['docs/coop/design-corrections/correction-crosswalk.proposed.json#/items/%d' % (i - 1),
                      'docs/coop/design-corrections/reviews/post-reset-review.v6/review.json#/arDispositions/AR-%02d' % i,
                      'docs/coop/design-corrections/validation-summary.v1.json'],
        'independentEvidence': ['probes/p10_crosswalk.py', 'runs/'],
    }

FW_BASIS = {
    'FW-01': 'Zero-config discovery bound to security project custody, native automatic units, Config2 resolver and workflow recommend, with no implicit effect or config write.',
    'FW-02': 'Clone facts are native exact/normalized/structural with near/cross-TSJS candidates; external semantic-similarity stays advisory with no bundled model and no semantic-equivalence or repair authority.',
    'FW-03': 'Native TS/JS/Rust capability matrix, sufficiency, unknown-edge and versioned wire contracts; 60 matrix cells, 0 qualified, stated as such.',
    'FW-04': 'Shared import2 registry with exact correspondence and observation scope; runtime/test/history explicitly do not become static Coverage or universal non-use.',
    'FW-05': 'Portable baseline, executable detector pivot, multiple comparison axes and separate audit gate participation.',
    'FW-06': 'Exact canonical input/identity/proof/evidence/seal/Run with independent replay; verified directly by closing two complete Runs and reproducing all five record recipes from prose.',
    'FW-07': 'Host invocation, bounded step DAG, fresh attempts, derivation DAG and common failure/storage/output behaviour; execution-plan stage ordinals are contiguous and enforced.',
    'FW-08': 'Coverage3 separates examined from resolution completeness; output required/optional omissions and unavailable-versus-operational-fault stay distinct.',
    'FW-09': 'Closed advisory artifacts with exact Control citations and stale/unknown-reference refusal.',
    'FW-10': 'Recipe-specific closed-world/proof/current-trust requirements, separate apply consent, guarded journals and fresh verification.',
    'FW-11': 'Architecture13 section 6 restrictions remain binding; comparison separates policy/waiver/scope/evidence changes from advisory observations and refuses to read redistribution as improvement.',
    'FW-12': 'Bounded review brief schema with explicit truncation and membership; no claim of complete review or prose verification.',
    'FW-13': 'Command inventory plus authenticated capability/schema/closure declarations, generated or drift-checked projections and typed refusal of unknown records.',
    'FW-14': 'Accepted on disclosure, not completeness: still states plainly that no digest-pinned corpus, matrix or thresholds exist, that synthetic design cases are not that corpus, and that g13 platform aliases are old-corpus labels rather than machine IDs accepted by product grants.',
    'FW-15': 'Closed declarative DSL with effective-policy preview and deterministic suites; exercised here against the actual PolicyDocumentV1/RuleProgramV1 schemas with a real three-level predicate, not only the fixture atom.',
}
fw = {k: {'disposition': 'ACCEPT',
          'scopedBasis': v,
          'selectors': ['docs/coop/design-corrections/current-source-map.proposed.md#%s' % k]}
      for k, v in FW_BASIS.items()}

RES = {
    'DR-011-R01': 'Product subject-scope/view/fact/Coverage schemas supply the declared view and subject-set joins; the old D9-v1.6 checker is explicitly not the current validator.',
    'DR-011-R02': 'Relation payload and normalization recipes preserved by exact version; fact2/finding-key2 supply current authority; no authority inferred from hostile-code corpus parks.',
    'DR-011-R03': 'plan2/exec-plan2 schemas and exact semantic joins are the stated alternative; no v4/v5 checker relabelled accepted.',
    'DR-011-R04': 'Native protocol and security lifecycle/core bridge are explicit successors; historical OBS-1/checker skew retains its original standing.',
    'DR-011-R05': 'Protocol-major-3 negotiation with exact transaction/EOF/error rules and sealed dependency/prepared inputs; rejected base-v2 stays rejected.',
    'DR-011-R06': 'Verified in these bytes: identity-and-evidence is the owning Phase-1A packet with proof/evidence/seal closure, retained regeneration closure, custody, immutable-assurance versus current-availability split and typed D9 joins.',
    'DR-011-R07': 'CD-RT-5 and applied v28 posture preserved explicitly; the old unreviewed checker remains unreviewed rather than accepted by a passing invocation.',
    'DR-011-R08': 'Closed host-owned outcome with precise observation-to-faultCause mapping, branch-specific optional fields, cancellation and post-commit required-output exit4; the three checker-derived gaps are named as needing retained cases rather than closed.',
    'DR-011-R09': 'Semantic IDs verified to exclude RequestId/ExecutionId, lifetime, credentials, cache state, receipt timestamps and storage paths; policy-derivation2 binds Plan/proof/policy/waivers/verdict.',
    'DR-011-R10': 'Correctly states it cannot be closed by the proposed table and requires a fresh implementer litmus after final integration. The litmus is a later independent session and was not performed here.',
    'DR-011-R11': 'Durable commit, acknowledgements, recovery, retention pins, GC, backup/import and availability/D9 are defined; real supported-platform fsync/process-death/storage measurements remain explicit release gates and are not claimed completed.',
    'DR-011-R12': 'Verified item-by-item: 30 items carry 30 dispositions (19 RES-EP13-01..19 historical-limitation-preserved, 7 historical-observation-preserved, 4 historical measured escapes preserved as outside product authority). No escape is reclassified as fixed and no same-process containment claim is made.',
    'DR-011-R13': 'Executable detector pivot, portable baseline and typed multi-axis comparison are the owning successor; old v14/v15/v16 rejection and v17 unreviewed standing remain unchanged.',
    'DR-011-R14': 'CFG-6 threat root preserved in TM v3 and expressly not reopened by the stale v2 note; no claim that a stale citation was itself the remaining defect.',
    'DR-011-R15': 'ProjectId marker/registry/namespace and RequestId/ExecutionId stay operational; hash equality expressly does not grant permission, prove custody or authorize replay of expired grants.',
    'DR-011-R16': 'D-367 delegation and D-370/D-371 scope preserved; first-party bounded component selection opens no third-party catalog or plugin ecosystem; CD-RT-5 durable-unbounded default remains binding.',
}
PARENT = {
    'DR-001': 'Current source/selector/claim map and refreshed reading path with individual residual dispositions, preserving old custody.',
    'DR-002': 'Full identity/evidence/proof/authority/retention chain rather than a vector-only preview; independently exercised end to end here.',
    'DR-003': 'Prospective pre-blueprint split is explicit and scoped; expressly not SATISFIED or DEMONSTRATED, leaving DR-G09/G18/G19/G21/G22 and DR-012 mandatory before release.',
    'DR-004': 'Phase-1A packet with resolution-complete facts/Coverage/proof semantics and retained failure/negative cases.',
    'DR-005': 'Applied evidence/retention/D9 integration plus executable custody reference; native carrier qualification separately required before release.',
    'DR-006': 'Every semantic identifier and producing input is supplied in the descriptor graph. Verified: no domain omits an input its contract row names, and all five previously parked recipes are now constructible.',
    'DR-007': 'Exact D9 branch/cause/result behaviour joined to authoritative commit, retention loss, cancellation and selected output failure.',
    'DR-008': 'Applied retention posture preserved with the evidence/D9/Phase-1A join completed.',
    'DR-009': 'Lifetime neutrality, one-shot operational authority and reproducible semantic identities.',
    'DR-010': 'Delegated product scope preserves bounded first-party composition; no third-party ecosystem or untrusted runtime selected.',
    'DR-011': 'All sixteen residual rows and every nested evaluation residual carry an individual disposition; the blind implementer litmus correctly follows final integration and is not claimed here.',
}
inherited = {}
for k, v in RES.items():
    inherited[k] = {'disposition': 'ACCEPT', 'scopedBasis': v,
                    'selectors': ['docs/coop/design-corrections/inherited-residuals.proposed.md#%s' % k]}
for k, v in PARENT.items():
    inherited[k] = {'disposition': 'ACCEPT', 'scopedBasis': v,
                    'selectors': ['docs/coop/design-corrections/inherited-residuals.proposed.md#%s' % k]}
inherited['DR-011-R12']['selectors'].append(
    'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json')
inherited['DR-011-R10']['note'] = 'Accepted as a disposition. The litmus itself is a later independent session.'
inherited['DR-003']['selectors'].append(
    'docs/coop/design-corrections/D-372-corrections.proposed.md#explicit-dr-003-pre-blueprint-disposition')

scoped = {
    'DR-201': {
        'title': 'Semantic correctness',
        'disposition': 'ACCEPT',
        'priorDisposition': 'CHANGES_REQUIRED (v6)',
        'scopedBasis': (
            'The v6 CHANGES_REQUIRED rested entirely on parked producing recipes; nothing is parked in '
            'these bytes. 57/57 bare-64-hex field sites carry x-opensip-digest under a law that admits no '
            'default, so an unannotated field refuses rather than inheriting a plausible rule. The five '
            'named fields have registered records (program-predicate, finding-parameters, stage-spec, '
            'commit-inventory, owner-source-set) with every field required. I reconstructed C and H from '
            'the contract prose without reading canonical.py: my encoder agreed with theirs on 21 '
            'adversarial values with 0 disagreements, reproduced all five author literal vectors, and my '
            'own five fresh vectors reproduced under their encoder and validated under the registered '
            'selectors. The v6 divergence (proof2:edba615b... vs proof2:67d4359b... for identical inputs) '
            'can no longer arise: representation is declared per site, a payload offered where a frame is '
            'required fails on the framing prefix, and a frame offered where a canonical record is '
            'required fails parsing. Predicate node addressing is total and deterministic over a real '
            'three-level RuleProgramV1 predicate: 8 addresses, distinct digests, and the same node at two '
            'addresses mints different digests. Happy-path versus pre-admission branches, Run versus '
            'command finalization and post-commit output failure remain unblurred.'),
        'selectors': [
            'docs/v2/contracts/product-v1/identity-and-evidence.md#the-closing-digest-law',
            'docs/coop/design-corrections/foundation/identity-schemas.v2.json#/$defs/program-predicate',
            'docs/coop/design-corrections/foundation/identity-schemas.v2.json#/$defs/finding-parameters',
            'docs/coop/design-corrections/foundation/identity-schemas.v2.json#/$defs/stage-spec',
            'docs/coop/design-corrections/foundation/identity-schemas.v2.json#/$defs/commit-inventory',
            'docs/coop/design-corrections/foundation/identity-schemas.v2.json#/$defs/owner-source-set',
            'docs/coop/design-corrections/foundation/identity-schemas.v2.json#/x-opensip-digest-domains'],
        'independentEvidence': ['probes/p1_digest_annotation_sweep.py', 'probes/p2_digest_residue.py',
                                'probes/p3_recipe_reconstruction.py', 'probes/p9_cross_unit.py',
                                'probes/p12_recipe_sweep.py'],
    },
    'DR-202': {
        'title': 'Delivery/operations',
        'disposition': 'ACCEPT',
        'scopedBasis': (
            'Re-measured in these bytes rather than carried over. evidence.regeneration-mismatch is typed '
            'HOST.IO_FAILURE/host-io, is a member of the closed 282-entry public detail registry, and the '
            'suite asserts the sealed Run bytes are byte-unchanged across the mismatch; evidence.missing is '
            'typed as retention/custody loss rather than a false predicate. Generation coexistence, '
            'mandatory storage, recovery, repair, permissions, state classes and loader TCB are stated; '
            'commit ordering and the immutable-assurance versus current-availability split are explicit. '
            'All 32 gates carry qualified:false and demonstrated:false. Cache HIT admission is separated '
            'from pure lookup-key construction and grantsEvidenceAuthority is false.'),
        'selectors': ['docs/v2/contracts/product-v1/identity-and-evidence.md#5',
                      'docs/coop/design-corrections/qualification-gates.proposed.json',
                      'docs/coop/design-corrections/public-detail-registry.v1.json'],
        'independentEvidence': ['probes/p5_deep_attacks.py', 'probes/p11_governance.py'],
    },
    'DR-203': {
        'title': 'Prototype lessons',
        'disposition': 'ACCEPT',
        'acceptanceKind': 'scoped-partial: accepted on the honesty of the disclosure, not on completeness',
        'scopedBasis': (
            'FW-14 and the g13 note still state plainly that no digest-pinned language-quality corpus, '
            'matrix or accepted thresholds exist, that synthetic design cases are not that corpus, that '
            'g13 platform display aliases are labels within the old preview corpus rather than machine IDs '
            'accepted by product grants or profiles, and that historical preview evidence never qualifies a '
            'native product cell. DR-118 and DR-G13 remain blocking by design. The verdict accepts the '
            'accuracy of the split; it awards no measurement.'),
        'selectors': ['docs/v2/architecture/prototype-evidence-reference.md',
                      'docs/v2/architecture/05-v1-to-v2-relationship.md',
                      'docs/coop/design-corrections/current-source-map.proposed.md#FW-14'],
    },
    'DR-204': {
        'title': 'V1/coop invariant coverage',
        'disposition': 'ACCEPT',
        'carries': ['NEW-SHOULD-2'],
        'scopedBasis': (
            'Independently re-measured: manifest hash exact, 1743/1743 files verified by hash and length '
            'before and after review, 0 undeclared files, 0 symlinks, declared byte total consistent; '
            '1288/1288 source-pin rows hash-exact across all four pin manifests; all eleven deterministic '
            'reports regenerate byte-identically; and 31/31 historical files verified unchanged against the '
            'live repository with openingSha256 equal to currentSha256. NEW-SHOULD-2 is resolved: all 16 '
            'crosswalk rows separate immutable historical reviews from the exact completed v6 predecessor '
            '(rehashed 269c1622..., subject manifest cb345532... equal to v7 predecessorManifestSha256 and '
            'to the embedded v6 manifest) from a pending, unhashed current binding; every row selector '
            'resolves inside the v6 review; the v7 manifest hash appears nowhere, so no self-hash cycle is '
            'demanded; and post-reset-review.v1 appears only as historical. No newest-head heuristic or '
            'baseline-only standing; readinessChanged false. One repository working-tree file '
            '(reviews/NEXT-REVIEW.md) diverges from its declared bytes; it is an orchestration ledger '
            'outside the design surface, the frozen snapshot copy is intact, and it is recorded rather '
            'than absorbed.'),
        'selectors': ['docs/coop/design-corrections/historical-preservation-report.v7.json',
                      'docs/coop/design-corrections/correction-crosswalk.proposed.json',
                      'docs/coop/design-corrections/foundation/source-pins.v1.json',
                      'docs/coop/design-corrections/native/source-pins.v2.json',
                      'docs/coop/design-corrections/security/source-pins.v1.json',
                      'docs/coop/design-corrections/workflows/source-pins.v1.json'],
        'independentEvidence': ['verify_subject.py', 'probes/p10_crosswalk.py', 'probes/p11_governance.py'],
    },
    'DR-205': {
        'title': 'Small-core/components',
        'disposition': 'ACCEPT',
        'scopedBasis': (
            'Core/TCB/product boundaries, storage, compatibility, quality, packaging, component SDK/UX and '
            'fault containment are stated; component selection is explicitly first-party bounded and opens '
            'no third-party catalog, plugin ecosystem or untrusted runtime, consistent with the D-371 scope '
            'that admits no untrusted ecosystem and no implicit repository execution; P-1/P-2/G3 '
            'implications are carried explicitly by D-372 as a seven-item full-product successor; MVP and '
            'future scope are separated and DR-128 remains post-MVP.'),
        'selectors': ['docs/v2/architecture/02-distribution-and-components.md',
                      'docs/v2/architecture/10-mvp-and-future-scope.md',
                      'docs/coop/design-corrections/D-372-corrections.proposed.md'],
    },
}

review = {
    'artifact': 'post-reset-review.v7',
    'verdict': 'ACCEPT',
    'overallVerdict': 'ACCEPT',
    'standing': ('FRESH INDEPENDENT DESIGN/REFERENCE REVIEW of frozen bytes; an exact review record for '
                 'later application. No readiness grade, no product qualification, no implementation '
                 'authorization. Condition 5 remains NOT MET.'),
    'verdictBasis': (
        'No unresolved required design gap remains. NEW-MUST-1 is resolved by a closing digest law that '
        'admits no default: 57/57 bare-64-hex sites are annotated, the five previously parked fields have '
        'registered closed records, and I reconstructed all five recipes plus C and H from the contract '
        'prose alone, reproducing the author literals and landing my own fresh vectors on the same digests. '
        'Complete Runs closed for BOTH TypeScript and Rust, each with its own-language semantic universe, '
        'nonempty facts, Coverage and nativeContextDigests, through actual native compiler/stdlib closure '
        'admission and universe binding; 26 independent attacks, including a forged ADMIT and a '
        'schema-valid but admission-refused re-framed context, were all refused with exact typed causes. '
        'NEW-SHOULD-1 is resolved with 329/329 arrays annotated across all 20 schema documents and real '
        'keyword enforcement. NEW-SHOULD-2 is resolved across all 16 rows with no self-hash cycle. The '
        'three advisories are addressed or correctly preserved. All suites match their expected counts '
        'exactly with byte-identical report regeneration.'),
    'reviewer': {
        'identity': 'actual Claude, fresh independent design/reference review session',
        'authoredNoSubjectBytes': True,
        'distinctFrom': [
            'actual Claude coauthor session 5dec928a-6357-4726-9ea8-49a3079fb726',
            'v6 reviewer session 96d049d9-abe2-457b-b05b-1ea5733b0f3e',
            'v5 reviewer session 52cf468a-f434-4b29-882d-3967c7644d51',
            'blind consumer consumer-b.v1', 'Codex'],
        'agentsUsed': False,
        'wroteOnlyUnder': '/tmp/opensip-design-corrections/post-reset-review.v7',
    },
    'subject': {
        'manifestPath': 'docs/coop/design-corrections/reviews/candidate-subject.v7.json',
        'manifestSha256': 'b5cfb5d316eb0101950476a37a2095ed0d9c5d51263408d3462f105d63165f7b',
        'requiredManifestSha256': 'b5cfb5d316eb0101950476a37a2095ed0d9c5d51263408d3462f105d63165f7b',
        'manifestSha256Matches': True,
        'snapshotRoot': '/tmp/opensip-design-corrections/candidate-subject.v7',
        'predecessorManifestSha256': 'cb345532f52980c1cba9d519eacecbe6748885c6693594d0845f0c9b7489a69f',
        'predecessorManifestVerifiedByRehashingEmbeddedCopy': True,
        'fileCount': 1743, 'filesVerified': 1743,
        'hashMismatches': 0, 'lengthMismatches': 0,
        'undeclaredFilesOnDisk': 0, 'symlinks': 0, 'duplicateManifestPaths': 0,
        'totalBytes': 28439483, 'measuredBytes': 28439483,
        'verifiedBeforeReview': True, 'verifiedAfterReview': True,
        'snapshotOrRepositoryModifiedByReviewer': False,
        'deltaFromV6': {'added': 133, 'changed': 47, 'removed': 0, 'unchanged': 1563},
        'priorAcceptanceHandling': ('The v5 ACCEPT and all earlier grades were extended to nothing. Every '
                                    'disposition here rests on measurement of v7 bytes.'),
    },
    'custody': {
        'historicalFilesDeclared': 31,
        'historicalFilesVerifiedUnchangedInRepository': 31,
        'historicalFilesChanged': 0,
        'sourcePinManifestsVerified': {'foundation': 1094, 'native': 68, 'security': 67,
                                       'workflows': 59, 'total': 1288, 'mismatches': 0, 'absent': 0},
        'coauthorHandoffsVerified': [
            {'path': 'docs/coop/design-corrections/reviews/digest-corrections-author.v1/handoff.json',
             'declaredSha256': 'e6eeaa5a683979b705381b950337e8f5b662dae602e3f1180dcd49a55884c3fe',
             'rehashMatches': True, 'sessionId': '5dec928a-6357-4726-9ea8-49a3079fb726',
             'standing': 'COAUTHOR, not independent review',
             'authorSourceImageVsFinalV7': '0 of 4 identical; superseded by the v2 turn, as its custody states'},
            {'path': 'docs/coop/design-corrections/reviews/digest-corrections-author.v2/handoff.json',
             'declaredSha256': 'e3b0ba75ce7eeb927130f85a099f41037e5a2406ebdba6bde833df488868666e',
             'rehashMatches': True, 'sessionId': '5dec928a-6357-4726-9ea8-49a3079fb726',
             'standing': 'COAUTHOR, not independent review',
             'authorSourceImageVsFinalV7': '7 of 7 byte-identical to the frozen v7 bytes'}],
        'codexArtifactsTreatedAs': 'assertions to verify, never acceptance evidence',
        'codexNativeCounterexampleInspected': {
            'path': 'docs/coop/design-corrections/reviews/codex-post-reset.v1/native-run-counterexample.v7',
            'finalRecheckCopiedCurrentSources': 85, 'ofWhichMatchFrozenV7': 85,
            'resultFinalCapturedSources': 77, 'ofWhichMatchFrozenV7': 77,
            'originalPositiveRun': 'run2:88bd8348fef1d7ade6c1e3c9c56b1879d685a4f55c50e46ca25865333a1fe6b9',
            'reframedContradictoryContext': 'refused: NATIVE_CONTEXT_ADMISSION:native.native-context-field-mismatch:moduleResolutionMode',
            'independentlyReproducedByThisReviewer': True,
            'note': 'Its closure was inspected directly and re-derived, not inferred from author assertions.'},
        'repositoryDivergenceFromFrozenSubject': {
            'declaredPathsComparedAgainstRepository': 1743,
            'byteIdentical': 1742,
            'diverged': [{'path': 'docs/coop/design-corrections/reviews/NEXT-REVIEW.md',
                          'declaredSha256': 'bf1a5baaeb3a24006461ef9406809f11fef50ed82a1e471af4c6ed8282565b39',
                          'repositorySha256': '3c44beb425ed6d3c4856f52b8b8d58b93e3b89bc7e20d123e2afbbc4f06eb1fd',
                          'declaredBytes': 50391, 'repositoryBytes': 54122,
                          'writtenByReviewer': False,
                          'assessment': ('Orchestration next-review ledger written after the freeze; not a '
                                         'design or semantic artifact. The frozen snapshot copy is intact '
                                         'and is what was reviewed, so the verdict is unaffected.')}]},
    },
    'suiteRuns': {
        'executedIn': 'disposable copy at post-reset-review.v7/work',
        'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B',
        'expectedSource': 'docs/coop/design-corrections/validation-summary.v1.json',
        'results': {
            'foundation': {'expected': 697, 'measured': 697, 'delta': 0,
                           'components': {'foundation': 231, 'identity': 354, 'product-quality': 24,
                                          'product-configuration': 28, 'array-order': 60},
                           'sourcePinsExpected': 1094, 'sourcePinsMeasured': 1094},
            'security': {'expectedCases': 456, 'measuredCases': 456, 'delta': 0,
                         'expectedSweeps': 10, 'measuredSweeps': 10},
            'native': {'expectedCases': 132, 'measuredCases': 132, 'delta': 0,
                       'matrixCells': 60, 'qualifiedCells': 0},
            'workflows': {'expected': 1253, 'measured': 1253, 'delta': 0},
            'integration': {'expected': 360, 'measured': 360, 'delta': 0}},
        'totalFailures': 0, 'totalCountDeltas': 0,
        'deterministicReportsRegenerated': 11,
        'deterministicReportsByteIdentical': 11,
        'caveat': 'Passing tests are not semantic acceptance and were not treated as such.',
    },
    'priorFindingDispositions': {
        'NEW-MUST-1': {'disposition': 'RESOLVED',
                       'independentlyVerified': True,
                       'howVerified': ('Own residue sweep with $ref resolution (57/57 annotated, 0 residue); '
                                       'own C and H implemented from contract prose, 0 disagreements on 21 '
                                       'adversarial values; all five author literals reproduced; five fresh '
                                       'reviewer vectors agreed and validated under the registered records; '
                                       'own addressing implementation matched the model over a real '
                                       'three-level predicate under the actual workflow schemas.'),
                       'probes': ['probes/p1_digest_annotation_sweep.py', 'probes/p2_digest_residue.py',
                                  'probes/p3_recipe_reconstruction.py', 'probes/p4_native_complete_runs.py',
                                  'probes/p5_deep_attacks.py', 'probes/p9_cross_unit.py',
                                  'probes/p12_recipe_sweep.py']},
        'NEW-SHOULD-1': {'disposition': 'RESOLVED', 'independentlyVerified': True,
                         'coverage': {'arraysFound': 329, 'annotated': 329, 'documents': 20,
                                      'vocabularyViolations': 0,
                                      'previouslyUnenumerated': ['foundation/import-source-context.schema.json',
                                                                 'foundation/product-quality-report.schema.v3.json']},
                         'probes': ['probes/p7_order_coverage.py', 'probes/p8_order_semantics.py']},
        'NEW-SHOULD-2': {'disposition': 'RESOLVED', 'independentlyVerified': True,
                         'rowsVerified': 16, 'probes': ['probes/p10_crosswalk.py']},
        'NEW-ADV-1': {'disposition': 'ADDRESSED',
                      'basis': 'Explicit statusVocabulary separates in-progress, author-corrected-pending-review and application-binding-pending; the crosswalk uses matching status values; earlier frozen vocabulary retained historically.'},
        'NEW-ADV-2': {'disposition': 'CLOSED',
                      'basis': 'The x-opensip-digest annotation at execution-plan.stages[].stageSpecDigest and at cache-key.stageSpecDigest is byte-identical and names #/$defs/stage-spec; regeneration-key is literally {"$ref": "#/$defs/cache-key"}.'},
        'NEW-ADV-3': {'disposition': 'CORRECTLY-PRESERVED-AS-UNDEMONSTRATED',
                      'gateCount': 32, 'gatesQualifiedTrue': 0, 'gatesDemonstratedTrue': 0,
                      'gatesWithAuthoredHarness': 0,
                      'platformFamilies': ['linux-x86_64-gnu', 'linux-aarch64-gnu', 'macos-aarch64', 'macos-x86_64'],
                      'basis': 'All 32 gates carry DESIGN-CONTRACT-PENDING-REVIEW with qualified, demonstrated and implementationHarnessAuthored all false; the four families are exactly the D-371 machine IDs; DR-G17 is present and unqualified after the D-372 SARIF re-entry.'},
        'earlierBlindFindings': {'disposition': 'INTACT',
                                 'basis': 'M1-M5, S1-S6 and A1-A4 fixes remain present and passing within the unchanged 354-check identity suite; the array-encoder, policy-order, resolved-config, subject-scope, TS-context and CVE-1 checks v6 verified are still exercised.'},
    },
    'arDispositions': ar,
    'fwDispositions': fw,
    'inheritedResidualDispositions': inherited,
    'scopedReviewOwnerDispositions': scoped,
    'scopedReviewOwnerAccounting': {
        'accept': 5, 'changesRequired': 0,
        'condition3': ('Discharged on the current scope for these exact frozen bytes. This is one input to '
                       'the central register condition set, not a readiness grade.'),
        'historicalAcceptanceHandling': ('DR-201..205 were ACCEPTED 2026-08-13 at old digests and are '
                                         'reopened for the current scope by the register itself. No blanket '
                                         'extension of an old grade was awarded; each disposition above was '
                                         're-measured on v7 bytes.'),
        'dr201PriorGrade': 'CHANGES_REQUIRED in v6; re-earned here on new evidence, not extended.'},
    'newMustIssues': [],
    'newShouldIssues': [],
    'newAdvisories': [
        {'id': 'V7-ADV-1',
         'title': '"Every 64-hex field" is stated more broadly than the rule it enforces',
         'detail': ('The closing-digest-law paragraph says every 64-hex field in identity-schemas.v2 carries '
                    'an x-opensip-digest annotation and that an unannotated one is inadmissible. Enforcement '
                    'correctly covers BARE 64-hex fields; 52 prefixed identity fields (plan2:, closure2:, '
                    'prj1- and so on) carry no annotation because their domain is carried by the prefix and '
                    'defined by the section 3 domain table. The design is closed either way and no residue '
                    'exists; only the sentence is wider than what it enforces, which a blind implementer '
                    'could read as requiring annotations on prefixed identities.'),
         'suggestedRemedy': 'Say "every bare 64-hex field".',
         'severity': 'ADVISORY', 'blocksAcceptance': False,
         'selectors': ['docs/v2/contracts/product-v1/identity-and-evidence.md#the-closing-digest-law'],
         'probe': 'probes/p2_digest_residue.py'},
        {'id': 'V7-ADV-2',
         'title': 'A Plan may select several admitted native contexts of one language',
         'detail': ('Adding a second, fully well-formed and independently admitted TypeScript context to '
                    'plan.nativeContextDigests closes a Run. Characterised before judging: it is not an '
                    'identity or trust break. The extra context is genuinely re-admitted (removing its '
                    'closures or frame bytes refuses), a snapshot-foreign context is refused with an exact '
                    'typed cause (NATIVE_CONTEXT_SOURCE_MISMATCH), no universe binds it so no evidence is '
                    'attributed to it, and both Plan and Run identities change so nothing is silently equal. '
                    'No contract text requires per-language uniqueness, so this matches the design as '
                    'written. The residue is presentational: a consumer reading plan.nativeContextDigests as '
                    'THE toolchain for a language would be reading a set as a scalar; the authoritative '
                    'per-fact answer is the fact sourceUniverse.'),
         'severity': 'ADVISORY', 'blocksAcceptance': False,
         'probe': 'probes/p6_b7_characterise.py'},
        {'id': 'V7-ADV-3',
         'title': 'Application should bind frozen snapshot bytes, not working-tree bytes',
         'detail': ('One declared path (reviews/NEXT-REVIEW.md) already differs between the frozen snapshot '
                    'and the repository working tree. An application step that copies from the working tree '
                    'would bind bytes this review did not cover.'),
         'severity': 'ADVISORY', 'blocksAcceptance': False},
    ],
    'independentProbes': [
        {'source': 'verify_subject.py', 'purpose': 'manifest, per-file hash+length, undeclared files, symlinks; run before and after',
         'result': '1743/1743 both times; 0 mismatches; 0 undeclared'},
        {'source': 'delta.py', 'purpose': 'exact v6 to v7 delta', 'result': '133 added, 47 changed, 0 removed, 1563 unchanged'},
        {'source': 'probes/p1_digest_annotation_sweep.py', 'purpose': 'first-pass 64-hex annotation sweep',
         'result': 'exposed that a naive walker misses $ref-to-Hash sites and that anchors are (?![\\s\\S]) not $'},
        {'source': 'probes/p2_digest_residue.py', 'purpose': 'residue hunt with $ref resolution',
         'result': '57 bare-hex sites, 57 annotated, 0 residue; 52 prefixed identity sites unannotated by design'},
        {'source': 'probes/p3_recipe_reconstruction.py', 'purpose': 'C and H reimplemented from contract prose; own vectors',
         'result': '0 encoder disagreements on 21 adversarial values; 5/5 author literals reproduced; 5/5 own vectors agreed and validated; H never equals raw payload SHA; length field load-bearing'},
        {'source': 'probes/p4_native_complete_runs.py', 'purpose': 'complete Runs for both languages plus first attack round',
         'result': 'TS run2:d3ae6d56... and Rust run2:6dfd7d9b... both closed with own-language universes, nonempty facts/Coverage/contexts; all attacks refused'},
        {'source': 'probes/p5_deep_attacks.py', 'purpose': 'attacks re-hashed under their own digests so the store check cannot fire; cache and regeneration',
         'result': 'all 12 deep attacks refused by the semantic law with exact typed causes; all cache negatives refused; legitimate cache and regeneration hits admitted with grantsEvidenceAuthority false'},
        {'source': 'probes/p6_b7_characterise.py', 'purpose': 'characterise the one admitted case before judging it',
         'result': 'legitimately admissible extra Plan input, not a trust break; became V7-ADV-2'},
        {'source': 'probes/p7_order_coverage.py', 'purpose': 'independent array-order coverage across every schema document',
         'result': '329 arrays, 329 annotated, 20 documents, 0 vocabulary violations'},
        {'source': 'probes/p8_order_semantics.py', 'purpose': 'adversarial order semantics',
         'result': 'keyword really registered; encoder never normalizes; utf8 vs canonical-set and tuple vs canonical object orders demonstrably disagree; canonical-order admits measured duplicates where canonical-set refuses; every selector holds positively and negatively'},
        {'source': 'probes/p9_cross_unit.py', 'purpose': 'records against the real workflow policy/rule-program schemas; native order refusal typing',
         'result': 'deep policy and compiled program validate under the real schemas; 8 addresses enumerated identically to the model; native order violations typed as order faults, never as language faults'},
        {'source': 'probes/p10_crosswalk.py', 'purpose': 'crosswalk provenance', 'result': '16/16 rows verified; no self-hash cycle; v1 only historical'},
        {'source': 'probes/p11_governance.py', 'purpose': 'gates, evaluation residuals, historical preservation, AR/FW/residual inventories',
         'result': '32 gates all unqualified and undemonstrated; 30/30 residual dispositions; 16 AR, 15 FW, 16 residual rows, 11 parent rows'},
        {'source': 'probes/p12_recipe_sweep.py', 'purpose': 'hidden recipe collisions and excluded semantic inputs',
         'result': 'every annotation resolves; all Ref domain enums registered; no domain omits an input its contract row names; acyclicity structural; no field spelling carries two conflicting recipes'},
    ],
    'scopeLimitations': [
        'Every OS, compiler, cargo, stdlib, LLVM, sysroot, lockfile, dependency-acquisition, crypto, clock, lease and evaluator observation is a synthetic trusted TCB assumption. Nothing was executed or measured and no platform was qualified.',
        'The fixture evaluator interprets a single-atom subset. Mitigated by exercising record shapes, digests and the addressing law against a real three-level predicate under the actual workflow policy and rule-program schemas, but the declarative language itself is not qualified here, nor is a native Coverage or relation payload registry.',
        'The Rust corpus is one vendored registry package over a two-package Cargo.lock. Real crate graphs, workspace member enumeration, feature unification by an actual cargo metadata run and missing-crate Coverage remain the native unit cases and later qualification.',
        'admit_cache_entry is a post-construction conformance check over a lookup key and its consumed input closure, not a cache subsystem; it does not fetch or validate cached output bytes or decide reuse policy.',
        'The subject fixture builders were reused to obtain valid graphs. Every attack, mutation and assertion is this reviewer own, and the digest reconstruction uses an encoder written from the contract prose alone; no self-consistent author vector was accepted as independent reconstruction.',
        'Documentation prose was read for consistency with the schemas and models it governs; it was not exhaustively proofread.',
    ],
    'laterActsNotPerformedHere': [
        'fresh blind consumer-B review reconstructing both the TypeScript and Rust paths from normative inputs alone',
        'complete application review and the application itself',
        'any product implementation, source fix, commit or push',
        'product qualification of any of the 32 gates on any of the four machine IDs',
    ],
    'productQualification': False,
    'implementationAuthorized': False,
    'readinessChanged': False,
    'condition5': 'NOT MET',
    'independentAcceptance': True,
    'acceptanceMeaning': ('On the exact frozen bytes of manifest b5cfb5d3..., no unresolved required design '
                          'gap remains. This is an exact review record for later application, not an award '
                          'of readiness, qualification or implementation authority.'),
    'retainedArtifacts': {
        'root': '/tmp/opensip-design-corrections/post-reset-review.v7',
        'files': ['review.md', 'review.json', 'verify_subject.py', 'delta.py',
                  'subject-verify.before.json', 'subject-verify.after.json', 'delta-v6-v7.json',
                  'git-status.after.txt', 'probes/', 'runs/', 'work/ (disposable copy)'],
    },
}

(OUT / 'review.json').write_text(json.dumps(review, indent=1) + '\n')
print('wrote review.json',
      (OUT / 'review.json').stat().st_size, 'bytes')
for k in ('verdict', 'subject', 'arDispositions', 'fwDispositions',
          'inheritedResidualDispositions', 'scopedReviewOwnerDispositions'):
    print(' top-level', k, 'present:', k in review)
print(' subject.manifestSha256 ==', review['subject']['manifestSha256'])
print(' scoped keys', sorted(review['scopedReviewOwnerDispositions']))
print(' scoped dispositions', {k: v['disposition'] for k, v in review['scopedReviewOwnerDispositions'].items()})
print(' ar count', len(ar), 'fw count', len(fw), 'inherited count', len(inherited))
