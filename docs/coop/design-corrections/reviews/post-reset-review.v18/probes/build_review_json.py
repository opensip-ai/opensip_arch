import json, hashlib, os

OUT = '/tmp/opensip-design-corrections/post-reset-review.v18'
V17R = 'docs/coop/design-corrections/reviews/post-reset-review.v17-clarification.v1/review.json'
V17SHA = '7acde2944740ff150a5bbcad9a48d1a20ac7a5e1e21755d5674dcf7721628904'
CHK = 'docs/coop/design-corrections/workflows/check_workflows.v1.py'
CHK_NEW = '2ac26ab8194993358b529a764eb3f9f852f4f4385d2f31bff5a203da123e6392'
CHK_OLD = '2fe3143944ff256c84d6ef3f09be685868a22e7937e7f4bb21e4b717b523d17d'

pref = {'path': V17R, 'sha256': V17SHA}


def pr(sel):
    return dict(pref, selector=sel)


GUARDS = [('invocation', 171, 'refusal', 'run_invocation'),
          ('import (with optional errorCode conjunct)', 384, 'refusal', 'build_import'),
          ('source-mapping (reversed comparison order)', 407, 'refusal', 'admit_source_mapping'),
          ('repair.preview', 1112, 'refusal', 'repair_preview'),
          ('repair.recover', 1158, 'recoverRefusal', 'repair_recover'),
          ('repair.apply', 1171, 'refusal', 'repair_apply'),
          ('repair.verify', 1203, 'refusal', 'repair_verify'),
          ('test-execution', 1226, 'refusal', 'admit_test_execution'),
          ('render', 1320, 'refusal', 'render'),
          ('review', 1360, 'refusal', 'review_join')]

ctl = json.load(open(OUT + '/logs/p12-ten-context-controls.json'))
byctx = {r['context']: r for r in ctl['results']}
rnd = json.load(open(OUT + '/logs/p13-render-control.json'))
CTXKEY = {171: 'invocation', 384: 'import', 407: 'source-mapping', 1112: 'repair-preview',
          1158: 'repair-recover', 1171: 'repair-apply', 1203: 'repair-verify',
          1226: 'test-execution', 1320: 'render', 1360: 'review'}

guard_rows = []
for label, line, key, fn in GUARDS:
    c = CTXKEY[line]
    if c == 'render':
        n, samp = len(rnd['found']['falsePassesRemoved']), rnd['found']['falsePassesRemoved'][:2]
        inj = 'render call #%d (earlier calls are outside any try)' % rnd['found']['nth']
    else:
        r = byctx[c]
        n, samp, inj = len(r['falsePassesRemoved']), r['falsePassesRemoved'][:2], r['injection']
    guard_rows.append({
        'context': label, 'checkerLine': line, 'guardedKey': key, 'modelEntryPoint': fn,
        'inspected': True,
        'myControl': {'injection': inj, 'falsePassRowsRemovedByGuard': n,
                      'sampleNewlyCaughtCheckIds': samp, 'oldOnlyFailures': 0},
        'basis': 'I injected a detail-None Refusal at %s and ran the v17 and v18 checkers over the '
                 'identical tree; rows passing under v17 and failing under v18 are actual false '
                 'passes the guard removes.' % fn})

CARRIED = {
    'CB6-MUST-1': 'MUST', 'CB6-MUST-2': 'MUST', 'CB6-SHOULD-1': 'SHOULD', 'CB6-SHOULD-2': 'SHOULD',
    'CB6-ADV-1': 'ADVISORY', 'CB6-ADV-2': 'ADVISORY', 'CB6-ADV-3': 'ADVISORY',
    'CX-BV6-01': 'MUST', 'CX-BV6-02': 'SHOULD', 'CX-BV6-03': 'MUST', 'CX-BV6-04': 'SHOULD',
    'CX-BV6-05': 'SHOULD', 'CX-BV6-06': 'SHOULD', 'CX-BV6-07': 'SHOULD', 'CX-BV6-08': 'SHOULD',
    'CB6-NEW-1': 'observation', 'CB6-NEW-2': 'observation', 'CB6-NEW-3': 'limitation',
    'CB6-NEW-4': 'observation', 'BV6-V3-RECEIPT': 'SHOULD', 'BV6-V3-IMPORT-BINDING': 'MUST',
    'BV6-V3-IMPORT-CAUSE': 'MUST', 'BV6-V3-IMPORT-SEMANTICS': 'MUST', 'BV6-V3-PRECISION': 'SHOULD',
    'BV6-V4-CR-1': 'SHOULD', 'BV6-V5-CR-1': 'SHOULD'}
CB6 = {k for k in CARRIED if k.startswith('CB6-M') or k.startswith('CB6-S') or k.startswith('CB6-A')}

prior = []
for fid, sev in CARRIED.items():
    sel = ('/priorFindingDispositions/' if fid in CB6 else '/additionalSourceFindingDispositions/') + fid
    prior.append({
        'id': fid, 'originalSeverity': sev,
        'dispositionByThisReview': 'PRESERVED-UNCHANGED-SOURCE',
        'priorReference': pr(sel),
        'basis': 'The owning bytes for this finding are byte-identical v17->v18. I verified '
                 'independently that all 42 law-bearing files (product contracts, schemas, models, '
                 'case corpus) are unchanged and that the sole executable delta is ten AND-conjuncts '
                 'in the reference checker, which can only strengthen a check. I therefore preserve '
                 'the v17 resolution at its exact prior reference rather than re-deriving it.',
        'scope': 'Preservation by unchanged source plus monotonic delta. Not a fresh re-verification '
                 'of the original finding evidence, and not an application or readiness grade.'})

prior += [
    {'id': 'CX-V17-REFUSAL-EXPECTATION', 'originalSeverity': 'SHOULD (root)',
     'originalReviewerSeverity': 'advisory (nonblocking), as V17-ADV-3',
     'dispositionByThisReview': 'RESOLVED-VERIFIED-INDEPENDENTLY',
     'priorReference': {'path': 'docs/coop/design-corrections/reviews/codex-post-reset.v1/review-assessment.v17.json',
                        'sha256': '13c35078898fd3d7359a413f6f70357fe33ca4b70a98fb12302c7824f7270b32',
                        'selector': '/unresolvedRootShouldIssues/0'},
     'severityDisagreementPreserved': 'The independent v17 reviewer graded this advisory (nonblocking). '
        'Root graded it SHOULD and withheld promotion; the source coauthor independently agreed SHOULD. '
        'That disagreement stands in the record. The v17 reviewer did NOT regrade its own advisory, and '
        'nothing here should be read as such. My own independent grade agrees with SHOULD, as a new '
        'judgement of my own, because a detail-free refusal made the whole suite exit 0 green.',
     'basis': 'My own AST rollback proof shows rolling back exactly the ten guard conjuncts in the v18 '
              'checker reproduces the v17 AST exactly, and that v17 contained zero guards of that shape. '
              'My own handler census over all 23 except-handlers counts 10 unguarded defaulting '
              'expected-refusal comparisons in v17 and 0 in v18. My own controls demonstrate a real '
              'false pass removed in all ten contexts, with zero regressions.',
     'verifiedAgainst': {'path': CHK, 'beforeSha256': CHK_OLD, 'afterSha256': CHK_NEW}},
    {'id': 'V17-ADV-1', 'originalSeverity': 'advisory (nonblocking)',
     'dispositionByThisReview': 'ACCOUNTED-VERIFIED-AT-ORIGINAL-SEVERITY',
     'priorReference': pr('/newAdvisories/0'),
     'basis': 'I read the consumers directly. Both call sites index '
              "IMPORTED_REQUIREMENT_LAW['perKindApplicability'][req['relation']] by a validated relation "
              'key (workflows_model.v1.py:1012 and :1148), and requirement_plane resolves the plane from '
              'EVIDENCE_RELATIONS registry membership, never from a naming convention, with admit_atom '
              'refusing an unregistered relation first. The embedded `rule` key is therefore unreachable '
              'as a relation and is inert metadata. No silent relocation was performed: the schema still '
              'carries `rule` and the file is byte-identical to v17.',
     'scope': 'Source inspection of the consumer join. Not a host or product qualification.'},
    {'id': 'V17-ADV-2', 'originalSeverity': 'advisory (nonblocking)',
     'dispositionByThisReview': 'RESOLVED-VERIFIED',
     'priorReference': pr('/newAdvisories/1'),
     'basis': 'I swept all 107 declared {path,sha256} joins in the v18 governance records against actual '
              'frozen bytes. 102 resolve exactly, 1 is a subject-manifest digest, and the 4 that do not '
              'match file bytes are each explicitly labelled historical as-of pins that carry a separate '
              'currentSource which DOES resolve. Item 44 (V14-ADV-2) now labels its ef0c244e sourceCorrection '
              'as historical as-of-v16 and binds currentSource 53380a2455490e07 for '
              'foundation/relation-payload-schemas.v2.json, which I confirmed equals the actual v18 bytes. '
              'The frozen v17 advisory account file is not in the changed-path set, so the original is untouched.',
     'scope': 'Digest-join and provenance verification. Distinguishes review-file digests, subject-manifest '
              'digests and historical as-of references.'},
    {'id': 'V17-ADV-3', 'originalSeverity': 'advisory (nonblocking)',
     'dispositionByThisReview': 'CORRECTION-IMPLEMENTED-AND-INDEPENDENTLY-VERIFIED',
     'priorReference': pr('/newAdvisories/2'),
     'basis': 'The original advisory severity is preserved verbatim in the v18 records. The root '
              'CX-V17-REFUSAL-EXPECTATION required correction is implemented at all ten sites and verified '
              'by my own proofs and controls above.',
     'scope': 'Same executable evidence as CX-V17-REFUSAL-EXPECTATION.'},
    {'id': 'V18-OBS-1', 'originalSeverity': 'observation, not required',
     'dispositionByThisReview': 'AGREED-NONBLOCKING',
     'priorReference': {'path': 'docs/coop/design-corrections/reviews/v18-checker-coauthor.v1/handoff.json',
                        'sha256': '4af23cbda4f4b01d3ebf455c609d6933e946cee7f092fb5fcbb9299050ac0fe6',
                        'selector': '/nonBlockingObservation'},
     'basis': 'Reproduced. In my p14 variant A the emitted row is the failing check id with detail null, '
              'exactly as observed. The check id names the failing control and the verdict is correct, so '
              'this is a reference-test diagnostic convenience only. No public contract, schema, model or '
              'case expectation is involved, and no product failure composition changes.',
     'scope': 'Optional future diagnostic richness. Not an unperformed qualification gate.'}]

ar = {'AR-%02d' % i: {
    'id': 'AR-%02d' % i, 'disposition': 'CARRIED-UNCHANGED',
    'basis': 'AR owning document docs/coop/architecture-depth-review/REVIEW.md is byte-identical v17->v18 '
             '(verified against both manifests). correction-crosswalk.proposed.json did change, but I diffed '
             'it leaf-by-leaf: 64 changed leaves are all latestCompletedReview pointers and 96 added leaves '
             'are appended historicalReviews entries, with 0 removals. Every obligation, selector, owner, '
             'unit, contract and status field is unchanged.',
    'scope': 'Preservation only; review-routing moved, obligation did not. This is not a new grade.',
    'authority': "The row's own owner and the separately reviewed application. Not this review's to grant.",
    'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False,
    'priorReference': pr('/arDispositions/AR-%02d' % i)} for i in range(1, 17)}

fw = {'FW-%02d' % i: {
    'id': 'FW-%02d' % i, 'disposition': 'CARRIED-UNCHANGED',
    'basis': 'current-source-map.proposed.md is byte-identical v17->v18 and absent from the 11-path '
             'changed set I computed from the two manifests.',
    'scope': 'Preservation only.', 'authority': "Not this review's to grant.",
    'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False,
    'priorReference': pr('/fwDispositions/FW-%02d' % i)} for i in range(1, 16)}

resid_ids = ['DR-%03d' % i for i in range(1, 12)] + ['DR-011-R%02d' % i for i in range(1, 17)]
resid = {i: {
    'id': i, 'disposition': 'CARRIED-UNCHANGED',
    'basis': 'inherited-residuals.proposed.md and inherited-row-sources.proposed.json are both '
             'byte-identical v17->v18.',
    'scope': 'Preservation only. DR-011-R10 in particular still requires a fresh blind implementer litmus '
             'that this review does not supply; DR-012 is header prose, explicitly excluded, not a row.',
    'authority': "Not this review's to grant.",
    'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False,
    'priorReference': pr('/inheritedResidualDispositions/' + i)} for i in resid_ids}

owners = {'DR-2%02d' % i: {
    'id': 'DR-2%02d' % i, 'disposition': 'ROUTING-ASSESSED-ONLY-NOT-APPLIED',
    'basis': 'Owning register docs/v2/architecture/08-decision-and-readiness-register.md is byte-identical '
             "v17->v18 (verified against both manifests). The row's own historical scoped disposition stands "
             'unchanged as history. Only review routing was assessed.',
    'scope': 'Routing assessment of a scoped review owner. NOT a grade and NOT a final application outcome.',
    'authority': "The row's own owner and the separately reviewed application.",
    'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False,
    'priorReference': pr('/scopedReviewOwnerDispositions/DR-2%02d' % i)} for i in range(1, 6)}

review = {
    'review': 'post-reset-review.v18',
    'subjectManifestSha256': 'cd6e828c22c6bc0ecf07ab8fe1f4bd5d1a5a8726708e0deffac99960bdc25a44',
    'verdict': 'ACCEPT',
    'verdictScope': 'Independent acceptance of the frozen v18 SOURCE bytes only. This is not a blind '
                    'review, not an application, not a readiness reconciliation and not product '
                    'qualification. A fresh blind consumer review and a complete independent application '
                    'remain required after this source ACCEPT.',
    'reviewerStanding': 'Fresh independent Claude review. I authored none of the subject and am not the '
                        'v17 independent reviewer, the blind reviewer, or the v18 source coauthor. '
                        'Read-only on source, reviews and history; all writes confined to '
                        '/tmp/opensip-design-corrections/post-reset-review.v18.',
    'newMustIssues': [],
    'newShouldIssues': [],
    'newAdvisories': [
        {'id': 'V18-ADV-1', 'severity': 'advisory (nonblocking)',
         'title': 'Coauthor rationale "each handler is already paired with a post-try refusal-membership check" is overbroad',
         'finding': 'The handoff justifies the guard as "the checker\'s own law" on the basis that each of the '
                    'ten handlers is already paired with a post-try `if \'refusal\' in exp: check(cid, False, '
                    '"no refusal")`. I checked all ten. That pairing exists at only 4 of 10 sites '
                    '(checker lines 171, 384, 1112, 1226). At the other 6 (407, 1158, 1171, 1203, 1320, 1360) '
                    'there is no such post-try membership check.',
         'whyNonblocking': 'This is an accuracy defect in a justification sentence inside a review record, not '
                           'in the executable delta. The correction is independently correct on its own merits '
                           'and my controls demonstrate its effect at all ten sites, including the six unpaired '
                           'ones, where the guard is if anything more valuable because no other mechanism '
                           'detected an unexpected detail-free refusal there.',
         'owningSelector': {'path': 'docs/coop/design-corrections/reviews/v18-checker-coauthor.v1/handoff.json',
                            'sha256': '4af23cbda4f4b01d3ebf455c609d6933e946cee7f092fb5fcbb9299050ac0fe6',
                            'selector': '/theDefect/whyTheGuardIsTheCheckersOwnLaw'},
         'counterexample': 'checker line 1203 (repair.verify): the statement following the try is '
                           "must_valid(cid + '.verify-result-schema', ...), not a refusal-membership check.'"},
        {'id': 'V18-ADV-2', 'severity': 'advisory (nonblocking)',
         'title': 'One same-class absent/explicit-null conflation remains unguarded, at the import errorCode conjunct',
         'finding': "checker line 384 retains `(case['expect'].get('errorCode') is None or "
                    "case['expect']['errorCode'] == x.error_code)`. A deliberate `errorCode: null` is "
                    'indistinguishable from an absent errorCode, which is the same defaulting conflation the '
                    'ten guards were added to remove.',
         'whyNonblocking': 'I scoped this before raising it. Refusal.__init__ takes error_code as a required '
                           'positional and every one of the 83 raise sites supplies a non-null code, so '
                           '"expect no error code" is not a satisfiable expectation; and no case in the frozen '
                           'corpus declares errorCode: null (6 cases carry errorCode, all named). The '
                           'expression is therefore dead rather than a live false-pass vector, and unlike the '
                           'ten it cannot pass on its own because the guarded refusal-detail conjunct must '
                           'still match.',
         'owningSelector': {'path': CHK, 'sha256': CHK_NEW, 'selector': 'line 384, importCases handler'},
         'suggestionForAFuturePass': "If an explicit-null errorCode is ever meant to be expressible, guard it "
                                     "as `('errorCode' not in case['expect'] or ...)`. Not proposed here; it is "
                                     'outside the bounded v18 scope and would change no current verdict.'},
        {'id': 'V18-ADV-3', 'severity': 'advisory (nonblocking)',
         'title': "Coauthor's first completeness heuristic contains a dead exclusion term",
         'finding': 'In probes/scan_nullable_compares.py, `is_get` requires `len(n.args) == 1`, so the later '
                    '`defaulted = any(len(n.args) > 1 for n, _ in getsides)` can never be True. Two-argument '
                    '`.get(key, default)` calls are not merely un-excluded, they are invisible to that scan '
                    'entirely, so the scan cannot support a completeness claim over them.',
         'whyNonblocking': 'The conclusion happens to be sound here: I counted 39 two-argument `.get` calls in '
                           'the checker and 0 of them participate in an equality comparison inside an except '
                           'handler, so nothing was missed. My own independent census, which does not use that '
                           'heuristic, independently reaches the same set of exactly ten. The method does not '
                           'establish the claim; the claim is nonetheless true.',
         'owningSelector': {'path': 'docs/coop/design-corrections/reviews/v18-checker-coauthor.v1/probes/scan_nullable_compares.py',
                            'selector': 'defaulted = any(len(n.args) > 1 ...)'}}],
    'priorFindingDispositions': prior,
    'priorFindingAccounting': {
        'v17ResolvedFindingsPreserved': 26,
        'method': 'Preserved by exact prior reference plus my own byte-identity and monotonicity proof, not '
                  'by re-deriving each original finding and not by trusting the v17 ACCEPT headline.',
        'newRootAndAdvisoryItemsDisposed': ['CX-V17-REFUSAL-EXPECTATION', 'V17-ADV-1', 'V17-ADV-2',
                                            'V17-ADV-3', 'V18-OBS-1'],
        'everyOriginalSeverityPreserved': True, 'noSeverityDowngraded': True,
        'newAdvisoriesRaisedByThisReview': 3},
    'executableDelta': {
        'declaredScope': 'Ten membership guards in workflows/check_workflows.v1.py',
        'independentlyVerified': True,
        'file': {'path': CHK, 'beforeSha256': CHK_OLD, 'afterSha256': CHK_NEW,
                 'linesBefore': 1423, 'linesAfter': 1423, 'diffHunks': 10},
        'exactAstProof': {
            'method': 'Rolled back every BoolOp of the shape (K in D and RHS) -> RHS, restricted to sites '
                      'where RHS actually reads key K, then compared full AST dumps.',
            'guardSitesInV18': 10, 'guardSitesInV17': 0,
            'rolledBackV18AstEqualsV17Ast': True,
            'note': 'A first, looser transformer over-matched a pre-existing unrelated conjunct '
                    "(`'sarif' in c['formats'] and ...` at line 1340) and reported 11 sites and AST "
                    'inequality. That attempt is preserved; the restricted transformer is the proof.'},
        'handlerCensus': {'totalExceptHandlers': 23,
                          'handlersWithAnExpectedRefusalComparison': 10,
                          'unguardedDefaultingComparisonsInV17': 10,
                          'unguardedDefaultingComparisonsInV18': 0,
                          'noEquivalentMissedWithinChecker': True},
        'guards': guard_rows,
        'monotonicity': 'Each guard is added as the first conjunct of an AND whose second conjunct is the '
                        'unchanged v17 expression, so the new condition implies the old one. A guard can '
                        'only turn a pass into a failure, never a failure into a pass. Confirmed empirically: '
                        'zero old-only failures across all ten context controls.'},
    'myControls': {
        'standing': "Authored by me. Root's 100 synthetic handler-body executions and the coauthor's single "
                    'corpus injection are supporting evidence, not my oracle.',
        'falsePassDemonstratedInContexts': '10 of 10',
        'totalFalsePassRowsRemoved': 69,
        'regressions': 0,
        'nullSemanticsTruthTable': {
            'basis': 'Pure corpus change, no model patching, using the model\'s own detail-None refusal at '
                     "workflows_model.v1.py:1539 (repair_preview, 'target fingerprint not in the evidence Run') "
                     "reached by a case runOverride emptying run['findings'].",
            'A_noRefusalKey': {'v17': 'PASS (false pass, suite exit 0)', 'v18': 'FAIL (exit 1)'},
            'B_explicitNull': {'v17': 'PASS', 'v18': 'PASS', 'meaning': 'deliberate null remains legal'},
            'C_wrongNamedRefusal': {'v17': 'FAIL', 'v18': 'FAIL', 'meaning': 'named negative preserved'},
            'D_untouchedCorpus': {'v17': 'PASS', 'v18': 'PASS', 'meaning': 'no regression'},
            'allFourMatchIntendedSemantics': True},
        'liveReachability': {
            'raiseRefusalSites': 83, 'sitesWhereDetailIsNone': 10,
            'note': 'Detail-None refusals are live in the current model, so the v17 defect was reachable, not '
                    'merely theoretical. The frozen corpus does not currently trigger one, which is why the '
                    'unchanged suite passed under both checkers.'}},
    'custody': {
        'subjectManifest': {'path': 'docs/coop/design-corrections/reviews/candidate-subject.v18.json',
                            'sha256': 'cd6e828c22c6bc0ecf07ab8fe1f4bd5d1a5a8726708e0deffac99960bdc25a44',
                            'bytes': 1907291},
        'verifiedBefore': {'declaredFiles': 7864, 'hashMismatches': 0, 'lengthMismatches': 0,
                           'missing': 0, 'undeclaredExtras': 0,
                           'summedBytes': 544831302, 'declaredTotalBytes': 544831302},
        'verifiedAfter': {'identicalToBefore': True, 'manifestRehashUnchanged': True},
        'transitivePins': {'pinFiles': 4, 'totalPinEntries': 1308, 'verifiedAgainstActualBytes': 1308,
                           'mismatched': 0, 'unresolved': 0,
                           'v17ToV18PinChanges': 'only check_workflows.v1.py (all four pin files) and '
                                                 'correction-crosswalk.proposed.json (security, workflows). '
                                                 'No repinning was performed by me and none was needed.'},
        'disposableCopy': {'root': '/tmp/opensip-design-corrections/post-reset-review.v18/disposable-copy',
                           'basis': 'FULL exact copy of all 7864 files, not a partial extract',
                           'inventoryAfterAllSixRuns': 'added 0, removed 0, changed 0 versus frozen',
                           'note': 'Regenerated reports were byte-identical to the frozen ones, so the copy '
                                   'returned to byte identity with the snapshot.'},
        'writeScope': '/tmp/opensip-design-corrections/post-reset-review.v18 only. No live repository byte '
                      'and no frozen snapshot byte was written at any point.'},
    'referenceChecks': {
        'standing': 'Reference counts are calls and cases, not product qualification.',
        'commandsReproduced': 6, 'exitsMatchedDeclared': 6, 'sourceShasMatchedDeclared': 6,
        'generatedReportsByteIdenticalToFrozen': True, 'stdoutByteIdenticalToFrozenLogs': True,
        'repinningPerformed': False,
        'note': 'I ran the full six through run-reference-checks.py wrappers, so the source-pin gate WAS '
                'exercised in my reproduction. The coauthor invoked the checker directly and explicitly did '
                'not exercise that gate; its 1219-file copies intentionally omit 6452 review files '
                '(v17 carries 1216 non-review plus 6455 review files). I closed that gap with a full copy.'},
    'lawPreservation': {
        'method': 'Byte identity plus delta monotonicity, not an ACCEPT headline and not counts.',
        'changedPathsV17ToV18': 11,
        'lawBearingFilesChanged': 0,
        'lawBearingFilesInV18': 42, 'lawBearingFilesByteIdenticalToV17': 42,
        'categories': {'executable-checker': 1, 'source-pin': 4, 'generated-report': 3,
                       'narrative-record': 1, 'review-record': 1, 'crosswalk-record': 1},
        'preservedLaws': [
            'zero-config discovery and installed capability availability',
            'typed config and TS logical node kinds',
            'language-specific native evidence and provider/body/dialect ownership',
            'clone progression and confidence',
            'import/runtime/history/test evidence authority',
            'per-requirement native-9 / imported-7 causes with lossless producer/consumer vocabulary',
            'coverage partition within the full owning tuple and conditional file totality',
            'stable identity and typed canonical closure',
            'baseline changed-code audit',
            'command/operation/generic-vs-repair replay',
            'immutable Run and current availability',
            'public failure composition',
            'authorization and output failure after a committed Run'],
        'basis': 'Every contract, schema, model and case-corpus file carrying these laws is byte-identical '
                 'v17->v18, so none can have been weakened. The one executable change is confined to a '
                 'reference harness and is monotonically stricter, so no law that was enforced in v17 is '
                 'unenforced in v18. I did not infer this from the v17 verdict.',
        'newRequiredGapsFound': 0},
    'arDispositions': ar, 'fwDispositions': fw,
    'inheritedResidualDispositions': resid, 'scopedReviewOwnerDispositions': owners,
    'ownerRoutingScopeStatement': 'For the five DR-201..205 scoped review owner rows only review routing was '
                                  'assessed. Each literally sets appliedByThisReview=false and '
                                  'finalApplicationOutcomeGranted=false. Carried or routing-only status is '
                                  'not a new grade.',
    'registers': {'arRows': 16, 'fwRows': 15, 'inheritedResiduals': 27,
                  'inheritedResidualNote': 'DR-001..011 plus the DR-011 subledger R01..R16. DR-012 is header '
                                           'prose explicitly excluded, not a table row.',
                  'evaluationSubresiduals': 30, 'scopedReviewOwners': 5,
                  'qualificationGates': 32, 'gateIds': 'DR-G01..DR-G32',
                  'gatesDemonstrated': 0, 'gatesQualified': 0, 'gatesImplementationHarnessAuthored': 0,
                  'allGatesRemainUnperformed': True, 'gatesPerformedByThisReview': 0,
                  'gatesFileByteIdenticalV17ToV18': True,
                  'verification': 'I read qualification-gates.proposed.json directly in the v18 snapshot: 32 '
                                  'rows, and 0 rows carry a non-false value for demonstrated, qualified or '
                                  'implementationHarnessAuthored.',
                  'd372': {'applied': False, 'condition5': 'NOT MET',
                           'basis': 'docs/coop/design-corrections/README.md states D-372 has not been applied '
                                    'and the central readiness register is unchanged; the register document is '
                                    'byte-identical v17->v18.'},
                  'selectedMachineIdsAndLanguagePaths': 'Four selected macOS/Linux machine IDs and the '
                                                        'TS/JS/Rust/bounded-grammar paths are retained '
                                                        'unchanged; their owning files are byte-identical '
                                                        'v17->v18. Carried, not regraded by me.'},
    'evidenceKindDistinctions': {
        'measuredSchemaOrHelper': 'Schema validity and helper-level checks inside the reference suite.',
        'fullClosure': 'Only where a full admitted Run closure was actually computed; partial helper inputs '
                       'are not admitted native or full Runs.',
        'caseInjection': 'My ten-context controls and the four-variant truth table. These are corpus and '
                         'model-entry injections, not product Runs.',
        'sourceInspection': 'The AST proofs, handler census, pin joins and register byte-identity checks.',
        'hostQualification': 'NONE performed. No product host measurement exists and I manufactured none.',
        'firstActualRefusalBoundary': 'The model raises 83 refusals, 10 with a null detail; the first actual '
                                      'boundary I exercised is repair_preview at workflows_model.v1.py:1539.',
        'v17ClosureDenominatorNote': 'The earlier v17 CL3 mixed denominators: 177 of 240 relation/cause '
                                     'cross-product controls plus 14 presence/carryability equals 191, where a '
                                     'full sweep would be 254 with the extra 14. I did not repeat the v17 full '
                                     'probe suite, because no new concern requires it; 7 p06 controls actually '
                                     'exercised full closure and other authorization/config/key claims remain '
                                     'static or helper-level as originally qualified.'},
    'failedAttempts': [
        {'id': 'failed-attempt-01', 'file': 'probes/failed-attempt-01-p11-unconditional-injection.py',
         'whatFailed': 'Parsed the report `failed` field as a list of rows; in these runs it is a count, so '
                       'every context reported 0 failures and 0 deltas.',
         'correction': 'Parsed the `FAIL <id> <detail>` lines from stdout instead (p12).'},
        {'id': 'failed-attempt-02', 'file': 'probes/failed-attempt-02-p22-regex-monotonicity.py',
         'whatFailed': 'A regex restatement of the monotonicity pairing matched 0 of 7 changed check-call '
                       'strings because of nested parentheses.',
         'correction': 'Not repaired; the p04 AST rollback equality already proves the same property exactly.'},
        {'id': 'failed-attempt-03', 'file': 'probes/p04_exact_ast_proof.py (guarded_by predicate)',
         'whatFailed': 'An ancestor-walk predicate reported all ten guarded sites as unguarded.',
         'correction': 'Rebuilt with an explicit parent map in p05, which yields V17=10 and V18=0.'},
        {'id': 'failed-attempt-04', 'file': 'logs/p13-render-control.json',
         'whatFailed': 'Injecting at render call #1..#3 escaped uncaught, because M.render is also called '
                       'outside any try. 3 attempts preserved.',
         'correction': 'Swept the call index; call #4 lands inside the guarded renderCases try.'},
        {'id': 'failed-attempt-05', 'file': 'probes/p08.out',
         'whatFailed': 'Counted a positional Constant None as "has a detail", concluding 0 detail-free raise '
                       'sites and wrongly framing the defect as latent.',
         'correction': 'Re-measured in p10: 10 of 83 raise sites pass detail=None, so the defect is live-reachable.'}],
    'evidenceHonesty': [
        'I verified the delta myself rather than trusting the root or coauthor claims, and I found the '
        'coauthor rationale overbroad and its first heuristic partly dead while still reaching the same set of ten.',
        'Reference check counts are calls and cases. They are not product qualification.',
        '46 handler line hits in the coauthor trace show reachability only, not coverage of all null edge cases. '
        'My controls add the discriminating behaviour the trace does not establish.',
        'No implementation, commit, push, publication or readiness change is part of this review.',
        'I claim no blind agreement, no application agreement and no readiness agreement.'],
    'standing': 'PROPOSED independent source ACCEPT of the frozen v18 candidate. No promotion is conferred.',
    'requiredNextActs': [
        'A fresh blind consumer review of these exact v18 bytes. No blind pass has accepted v17 or v18 yet, '
        'and the prior v16 ACCEPT did not survive blind 6; all blind-6 and earlier corrections remain in view.',
        'A complete, independently reviewed application and readiness reconciliation.',
        'D-372 application and the 32 qualification gates remain entirely unperformed.'],
    'implementationAuthorized': False, 'readinessChanged': False, 'productQualification': False,
    'blindAgreementClaimed': False, 'applicationAgreementClaimed': False,
}

json.dump(review, open(OUT + '/review.json', 'w'), indent=1)
b = open(OUT + '/review.json', 'rb').read()
print('review.json bytes=%d sha256=%s' % (len(b), hashlib.sha256(b).hexdigest()))
print('prior=%d ar=%d fw=%d resid=%d owners=%d adv=%d'
      % (len(prior), len(ar), len(fw), len(resid), len(owners), len(review['newAdvisories'])))
