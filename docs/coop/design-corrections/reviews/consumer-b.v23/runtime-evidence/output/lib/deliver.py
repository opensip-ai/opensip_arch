"""Phase 11 -- write output/blind-review.json and output/blind-review.md (generation 22).

Every number in the deliverable is READ FROM AN ARTIFACT produced by an earlier stage of the same
from-scratch command (the measured read graph, notes/v23-read-graph.json, checks that). The only
hand-authored content is prose explaining what was measured, and the standing statements the
charter requires. The generation-20 version of this module is kept in lib.before-image.v20; its
narrative, custody notes and verdict rule were those of generation 20 and are not reused.
"""
import collections
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = '/tmp/opensip-design-corrections/consumer-b.' + 'v23'
OUT = ROOT + '/output'
LABELS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']
SESSION = '79569ae1-10f4-4181-972b-334f7ed2f07a'
PY = '/tmp/opensip-architecture-review-env/bin/python'
PHASE11 = ('R-DELIVER-MD-JSON', 'R-VERDICT-ENUM', 'R-MUST-SHOULD-ADVISORY',
           'R-NO-ACCEPT-IF-INCOMPLETE', 'R-NO-QUALIFICATION-CLAIM')


def J(rel):
    try:
        return json.load(open(OUT + '/' + rel))
    except Exception:
        return None


def sha_of(rel):
    p = OUT + '/' + rel
    if not os.path.exists(p):
        return None
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    cust = J('notes/v23-input-custody.json') or {}
    hist = J('notes/v23-history-standing.json') or {}
    labels = J('notes/v23-label-history.json') or {}
    census = J('notes/v23-path-census.json') or {}
    rgraph = J('notes/v23-read-graph.json') or {}
    gaps = J('vectors/phase10-design-gaps.json') or {}
    status = J('requirement-status.json') or {}
    helpers = J('helper-corrections.json') or {}
    verify = J('verify-all.json') or {}
    audit = J('vectors/claimed-positive-audit.json') or {}
    atom = J('vectors/indep-atom-law.json') or {}
    qs = J('query/indep-query-surface.json') or {}
    ms = J('vectors/indep-mutation-surface.json') or {}
    xin = J('vectors/indep-execution-inputs.json') or {}
    auth = J('vectors/test-prep-repair-authorization.json') or {}
    reqfile = json.load(open(ROOT + '/requirements.json'))

    runs = []
    for lab in LABELS:
        st = J('runs/%s.store.json' % lab) or {}
        cl = J('runs/%s.closure.json' % lab) or {}
        rp = J('runs/%s.replay.json' % lab) or {}
        ct = J('runs/%s.controls.json' % lab) or {}
        fams = (ct.get('tamperedResultControls') or []) \
            + (ct.get('identityAndRetentionControls') or [])
        al = (atom.get('runs') or {}).get(lab) or {}
        claim = st.get('claim') or {}
        runs.append({
            'label': lab,
            'claimedRunId': claim.get('runId'), 'claimedSealId': claim.get('sealId'),
            'claimedProofId': claim.get('proofId'), 'claimedPlanId': claim.get('planId'),
            'claimedSnapshotId': claim.get('snapshotId'), 'verdict': claim.get('verdict'),
            'exportFile': 'runs/%s.store.json' % lab,
            'exportFileSha256': sha_of('runs/%s.store.json' % lab),
            'objectCount': st.get('objectCount'), 'blobCount': st.get('blobCount'),
            'totalBlobBytes': st.get('totalBlobBytes'),
            'closure': {'admitted': cl.get('admitted'), 'checksPassed': cl.get('checksPassed'),
                        'checksNotApplicable': cl.get('checksNotApplicable'),
                        'checksRefused': cl.get('checksRefused'),
                        'file': 'runs/%s.closure.json' % lab,
                        'fileSha256': sha_of('runs/%s.closure.json' % lab)},
            'freshProcessReplay': {
                'file': 'runs/%s.replay.json' % lab,
                'fileSha256': sha_of('runs/%s.replay.json' % lab),
                'verdict': rp.get('verdict'),
                'matched': rp.get('verdict') == 'REPLAY_MATCH' and bool(rp.get('replayAdmitted')),
                'findingsCompared': len(rp.get('findingComparisons') or []),
                'predicateWitnessesCompared': len(rp.get('witnessComparisons') or []),
                'standing': ('the store was reloaded from its own exported bytes in a SEPARATE '
                             'process, every blob key was re-hashed on import, and the complete '
                             'proof bundle was recomputed and compared')},
            'controls': {'file': 'runs/%s.controls.json' % lab,
                         'fileSha256': sha_of('runs/%s.controls.json' % lab),
                         'count': len(fams),
                         'allRefused': bool(fams) and all(c.get('refused') for c in fams)},
            'independentAtomLaw': {'atoms': len(al.get('atoms') or []), 'checks': al.get('checks'),
                                   'passed': al.get('passed'),
                                   'refusals': len(al.get('refusals') or [])},
            'independentExecutionInputs': {
                'passed': ((xin.get('runs') or {}).get(lab) or {}).get('passed'),
                'refusals': len(((xin.get('runs') or {}).get(lab) or {}).get('refusals') or [])},
            'requirementIds': st.get('requirementIds'),
        })

    digests = {}
    for d in ('vectors', 'envelopes', 'query', 'notes', 'traces', 'checkpoints', 'runs'):
        base = OUT + '/' + d
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if f.endswith('.json'):
                digests['%s/%s' % (d, f)] = sha_of('%s/%s' % (d, f))
    for f in ('requirement-status.json', 'helper-corrections.json'):
        digests[f] = sha_of(f)

    counts = collections.Counter(v['status'] for v in status.values())
    blocking = sorted(k for k, v in status.items()
                      if v.get('acceptBlocking') and k not in PHASE11
                      and v['status'] in ('unexecuted', 'failed'))
    phase11_failed = sorted(k for k in PHASE11 if (status.get(k) or {}).get('status') == 'failed')
    must = gaps.get('newMustIssues') or []
    should = gaps.get('newShouldIssues') or []
    adv = gaps.get('advisories') or []
    open_helpers = helpers.get('openHelperFailuresOnAClaimedPositive') or []
    audit_failed = sorted(k for k, r in (audit.get('requirements') or {}).items()
                          if r.get('result') == 'FAIL')
    all_runs_ok = all(r['closure']['admitted'] and r['freshProcessReplay']['matched']
                      and r['controls']['allRefused'] and r['independentAtomLaw']['refusals'] == 0
                      for r in runs)
    stages = verify.get('stages') or []
    final_stage = verify.get('stagesRecorded') == (verify.get('declaredStageCount') or 0) - 1
    preceding_ok = bool(stages) and not verify.get('failedStages') and all(
        s['exit'] == 0 for s in stages)
    read_graph_ok = (rgraph.get('result') == 'PASS'
                     and rgraph.get('commandStageIoDir') == verify.get('stageIoDir'))
    conditions = {
        'acceptBlockingRequirementsNotExecuted': blocking,
        'phase11RowsFailed': phase11_failed,
        'claimedPositiveAuditFailures': audit_failed,
        'newMustIssueCount': len(must), 'newShouldIssueCount': len(should),
        'openHelperFailuresOnAClaimedPositive': open_helpers,
        'everyCompleteRunClosedReplayedControlledAndAtomLawAdmitted': all_runs_ok,
        'everyPrecedingStageOfThisCommandExitedZero': preceding_ok,
        'measuredReadGraphOfThisCommandPasses': read_graph_ok,
        'thisIsTheFinalReconciliationStage': final_stage,
    }
    accept = (not blocking and not phase11_failed and not audit_failed and not must and not should
              and not open_helpers and all_runs_ok and preceding_ok and read_graph_ok)
    verdict = 'ACCEPT-RECONSTRUCTABLE' if accept else 'CHANGES_REQUIRED'

    delta = cust.get('claim4_normativeDeltaMeasuredHere') or {}
    audit_rows = [{'id': k, 'kind': r.get('kind'), 'evidenceClass': r.get('evidenceClass'),
                   'result': r.get('result'), 'checksPassed': r.get('checksPassed'),
                   'evidenceClassSufficientForKind': r.get('evidenceClassSufficientForKind'),
                   'firstRefusal': r.get('firstRefusal'), 'artifacts': r.get('artifacts'),
                   'method': r.get('method')}
                  for k, r in sorted((audit.get('requirements') or {}).items())]

    doc = {
        'schema': 'consumer-b blind design review, generation 23',
        'consumerId': 'consumer-b.' + 'v23',
        'sessionId': SESSION,
        # split literals (V19-D1): no mechanical rewrite can reach these entries
        'sameOriginAncestry': ['consumer-b' + '.v14', 'consumer-b' + '.v15',
                               'consumer-b' + '.v16', 'consumer-b' + '.v17',
                               'consumer-b' + '.v18', 'consumer-b' + '.v19',
                               'consumer-b' + '.v20', 'consumer-b' + '.v22',
                               'consumer-b' + '.v23'],
        'generation21': cust.get('generation21'),
        'ancestryStanding': (
            'ONE continuous fresh blind consumer origin (14 -> 15 -> 16 -> 17 -> 18 -> 19 -> 20 -> '
            '22 -> 23). Generation 21 was prepared and never launched, so no generation-21 input, '
            'output or result exists and nothing is inherited from it. No earlier generation is '
            'retroactively accepted or re-graded by this one; their reports stand as written, '
            'including the defects later generations found in them (helper-corrections V22-* and '
            'V23-*). No '
            'number here is inherited: every one comes from the command recorded in '
            'verify-all.json. This origin verifies only the disclosed kit and its own work -- no '
            'root admission, agreement or verdict is known to it or claimed.'),
        'whatChangedInTheInputThisGeneration': {
            'kind': 'NORMATIVE SUCCESSOR',
            'fileCount': (cust.get('claim3_everyRowVerified') or {}).get('rowCount'),
            'measuredDelta': delta,
            'deltaMethod': (
                "MEASURED per path against this origin's own retained generation-22 per-file map "
                '(%s); the supplied normative-delta.json hash inventory was then VERIFIED against '
                'both sides rather than adopted (notes/v23-input-custody.json claim 5).'
                % delta.get('priorRecord')),
            'whatTheChangedOwnerDecides': (
                'foundation/atom-evaluation-contract.v1.md now publishes: section 6 runtime polarity '
                '(an unfiltered exists is satisfied by observed-hit or observable-unhit; an '
                'observability filter restricts the polarity set); section 4 dependency totality for '
                'same-kind dependencies (a gap view is evaluated with and without its gap positions '
                'and a removed position answers required-relation-missing), no mapped-scope fallback, '
                'ATOM_NATIVE_CARRIER for an absent or null enumeratorClosure, the admitted-input '
                'refusals INCOMING_SEARCH_SCHEMA / INCOMING_SEARCH_SCOPE_MISJOIN, the explicit '
                'empty-subject scope that closes an empty program, and I1 (a subject universe with no '
                'available owed binding is blocking). The projection registry and the IncomingSearchV1 '
                'schema carry the matching registry and admission text.'),
            'consequence': (
                'the atom evaluator was reconciled (V23-D1..V23-D3): the TypeScript and rust Runs '
                'changed identity (findings 3 -> 5 and 8 -> 7), all five Runs were rebuilt, '
                're-exported, re-closed, re-replayed and re-controlled, and the independent atom-law '
                'instrument admits all five and refuses the generation-22 and generation-20 '
                'predecessors. The whole-charter recheck then found and corrected claimed positives '
                'whose semantic fields were not derived from their premises (V23-D6..V23-D11).'),
        },
        'changedOwnerReadingScope': {
            'readInFull': ['%s (%s bytes)' % (c.get('path'), c.get('nowBytes'))
                           for c in delta.get('changed') or []],
            'crossOwnerReferencesRead': [
                'foundation/evaluator-composition-contract.v3.md sections 9.5 and 9.6',
                'foundation/identity-schemas.v3.json subject-scope, evaluation-deficiency',
                'native/native-evidence.schemas.v2.json CoverageResultV3, DeficiencyV2',
                'docs/v2/contracts/product-v1/native-evidence.md sections 4.6 and 10',
                'workflows/schemas/imported-evidence.schema.json RuntimeSubject.observability',
                'workflows/query-projection-contract.v3.md and evaluator3/graph-query.schema.json',
                'foundation/target-attribution.schema.v2.json join law',
                'docs/v2/contracts/product-v1/identity-and-evidence.md section 5',
                'docs/v2/contracts/product-v1/workflows-and-surfaces.md sections 1-3',
                'workflows/command-inventory.v3.json goldens; docs/coop/artifacts/d9-exit-contract.v1.14.json',
                'workflows/schemas/evaluator3/invocation-record.schema.json AnalysisResult, ComparisonStepResult'],
            'wholeCharterRecheck': (
                'every one of the 131 required ids was re-checked from its final bytes by the '
                'claimed-positive audit (vectors/claimed-positive-audit.json), not only the ids '
                'touched by the changed file'),
            'kitQuotesVerifiedByTheAtomInstrument': atom.get('kitQuotesVerified'),
        },
        'verdict': verdict,
        'verdictBasis': {
            'conditions': conditions,
            'rule': (
                'ACCEPT-RECONSTRUCTABLE requires: every acceptBlocking requirement executed with '
                'evidence sufficient for its kind (claimed-positive audit, not presence or counts), '
                'no claimed-positive audit failure, no unresolved MUST or SHOULD, no open helper '
                'failure on a claimed positive, every complete Run closed, replayed, controlled and '
                'admitted by the independent atom law, every preceding stage of this command exited '
                'zero, and the measured read graph of this command passes. MEASURED: %d '
                'acceptBlocking not executed, %d audit failures, %d MUST, %d SHOULD, %d open helper '
                'failures, Runs ok = %s, preceding stages ok = %s, read graph ok = %s.'
                % (len(blocking), len(audit_failed), len(must), len(should), len(open_helpers),
                   all_runs_ok, preceding_ok, read_graph_ok))},
        'inputKit': {
            'subjectManifestPath': 'subject/consumer-input-manifest.json',
            'subjectManifestSha256': (cust.get('claim1_manifestOwnBytes') or {}).get('measured'),
            'manifestOwnBytesResult': (cust.get('claim1_manifestOwnBytes') or {}).get('result'),
            'parentSubjectSha256DeclaredInThatManifest':
                (cust.get('claim2_declaredParentBinding') or {}).get('declared'),
            'declaredParentBindingResult':
                (cust.get('claim2_declaredParentBinding') or {}).get('result'),
            'fileCount': (cust.get('claim3_everyRowVerified') or {}).get('rowCount'),
            'filesVerifiedPass': (cust.get('claim3_everyRowVerified') or {}).get('filesVerified'),
            'everyRowVerifiedResult': (cust.get('claim3_everyRowVerified') or {}).get('result'),
            'hashVerification': (cust.get('claim3_everyRowVerified') or {}).get('result'),
            'undisclosedExtraFilesUnderSubject': (cust.get('claim3_everyRowVerified') or {}).get(
                'undisclosedExtraFilesUnderSubject'),
            'measuredDeltaAgainstThePriorDisclosedKit': delta,
            'custodyOfEveryOpenedKitDocument': cust.get('custody'),
            'parentVerificationStanding': (
                'NOT a parent whole-candidate verification. Only the parent digest DECLARED in the '
                'held manifest was compared to the value the instruction names; the parent subject '
                'itself was never held, read or verified.'),
            'sameOriginSubjectAncestry': ((J('notes/phase0-input-custody.json') or {}).get(
                'inputKit') or {}).get('sameOriginSubjectAncestry'),
        },
        'claimedCompletePositives': runs,
        'claimedPositiveAudit': {
            'file': 'vectors/claimed-positive-audit.json',
            'fileSha256': sha_of('vectors/claimed-positive-audit.json'),
            'counts': audit.get('counts'),
            'evidenceClassCounts': audit.get('evidenceClassCounts'),
            'sufficientClassesByKind': audit.get('sufficientClassesByKind'),
            'currentRunIds': audit.get('currentRunIds'),
            'rows': audit_rows,
            'standing': (
                'each requirement was re-checked from its FINAL bytes in a fresh process. The '
                'evidence class says what the re-check actually is; a static comparison, a '
                'shape-only check or a helper assumption never makes a requirement executed. The '
                'five phase-11 rows are decided by the requirement-status stage after this '
                'deliverable is written.'),
        },
        'atomContractReconciliation': {
            'instrument': 'lib/indep_atom_law.py (imports no evaluator)',
            'artifact': 'vectors/indep-atom-law.json',
            'perRun': {r['label']: r['independentAtomLaw'] for r in runs},
            'predecessorControls': [
                {'predecessor': p.get('predecessor'), 'refused': p.get('refused'),
                 'firstRefusal': (p.get('firstRefusal') or {}).get('check'),
                 'refusalCount': p.get('refusalCount')}
                for p in atom.get('predecessorControls') or []],
            'tamperControls': [
                {'run': t.get('run'), 'control': t.get('control'), 'clause': t.get('clause'),
                 'refused': t.get('refused'),
                 'firstRefusal': (t.get('firstRefusal') or {}).get('check')}
                for t in atom.get('tamperControls') or []],
            'lawVectors': [{'vector': v.get('vector'), 'result': v.get('result')}
                           for v in atom.get('lawVectors') or []],
            'minResolutionAtomLevelCases': len(atom.get('minResolutionAtomLevelCrossCheck') or []),
            'minResolutionAtomLevelRefused': sum(
                1 for r in atom.get('minResolutionAtomLevelCrossCheck') or []
                if r.get('result') != 'PASS'),
            'summary': atom.get('summary'),
            'claimLimits': atom.get('claimLimits'),
        },
        'wholePublishedQuerySurface': {
            'instrument': 'lib/indep_query_surface.py', 'artifact': 'query/indep-query-surface.json',
            'runUnderQuery': (qs.get('runUnderQuery') or {}).get('runId'),
            'operationsWithActualRecords': qs.get('operationCount'),
            'checks': len(qs.get('checks') or []), 'refusals': len(qs.get('refusals') or []),
            'negativeControls': len(qs.get('negativeControls') or []),
            'graphOutcomesRecomputed': (qs.get('graphRecomputation') or {}).get('cases'),
            'graphOutcomesDisagreeing': (qs.get('graphRecomputation') or {}).get('disagreeing'),
            'reinjectedDefectsDetected': '%d of %d' % (
                sum(1 for t in (qs.get('graphRecomputation') or {}).get('tamperControls') or []
                    if t.get('detected')),
                len((qs.get('graphRecomputation') or {}).get('tamperControls') or [])),
            'graphExecutorArtifact': 'query/graph-query-reconstruction.json'},
        'wholePublishedMutationSurface': {
            'instrument': 'lib/indep_mutation_surface.py',
            'artifact': 'vectors/indep-mutation-surface.json',
            'checks': len(ms.get('checks') or []), 'refusals': len(ms.get('refusals') or []),
            'negativeControls': len(ms.get('negativeControls') or []),
            'measuredKeys': ms.get('measuredKeys')},
        'authorizationRecords': {
            'artifact': 'vectors/test-prep-repair-authorization.json',
            'recordsAdmitted': sum(1 for r in auth.get('records') or []
                                   for s in r.get('submitted') or [] if s.get('admitted')),
            'controlsRefused': sum(1 for c in auth.get('controls') or [] if c.get('refused')),
            'syntheticHelperOnlyFields': {r.get('step'): r.get('syntheticHelperOnly')
                                          for r in auth.get('records') or []},
            'standing': auth.get('standing')},
        'fromScratchCommand': {
            'command': '%s -I -B %s/output/lib/verify_all.py' % (PY, ROOT),
            'declaredStageCount': verify.get('declaredStageCount'),
            'stagesRecordedWhenThisReconciliationRan': verify.get('stagesRecorded'),
            'stageIoDir': verify.get('stageIoDir'),
            'reconciliationStanding': (
                'this deliverable is written by the FINAL stage of that command. verify-all.json is '
                'rewritten after every stage, so the row count above is every preceding stage of '
                'the SAME command; the only row it cannot contain is this stage\'s own exit, which '
                'the command appends after it returns.'),
            'stages': stages,
            'failedStages': verify.get('failedStages'),
            'earlierCommandsOfThisGeneration': J('notes/v23-command-attempts.json'),
            'staticReadOrderGuard': (verify.get('readOrderGuard') or {}).get('violations'),
            'measuredReadGraph': {
                'file': 'notes/v23-read-graph.json', 'result': rgraph.get('result'),
                'stagesLogged': rgraph.get('stagesLogged'), 'edges': len(rgraph.get('edges') or []),
                'orderViolations': rgraph.get('orderViolations'),
                'undeclaredEdges': rgraph.get('undeclaredEdges'),
                'readsOfArtifactsNoStageWrote': rgraph.get('readsOfArtifactsNoStageWrote'),
                'childProcessReadsMeasured': False}},
        'requirementStatus': {
            'file': 'requirement-status.json', 'fileSha256': sha_of('requirement-status.json'),
            'counts': dict(counts), 'declaredTotals': reqfile['counts'],
            'notExecuted': sorted(k for k, v in status.items()
                                  if v['status'] in ('unexecuted', 'failed')),
            'acceptBlockingNotExecuted': blocking},
        'newMustIssues': must,
        'newShouldIssues': should,
        'advisories': adv,
        'blockerStatement': gaps.get('blockerStatement'),
        'withdrawnOrResolvedSinceTheLastGeneration':
            gaps.get('itemsThisOriginWithdrewOrThatTheNewKitResolved'),
        'algorithmFreedomNotGaps': gaps.get('algorithmFreedomNotGaps'),
        'emptyMustJustification': gaps.get('emptyMustJustification'),
        'resolvedByANormativeSuccessor': gaps.get('resolvedByTheNormativeSuccessorThisGeneration'),
        'coverageLimitationsDisclosedNotDesignGaps':
            gaps.get('coverageLimitationsDisclosedNotDesignGaps'),
        'whatTheGeneration23SuccessorDecidedAboutThisOriginsOwnReadings':
            gaps.get('whatTheGeneration23SuccessorDecidedAboutThisOriginsOwnReadings'),
        'whatTheGeneration22SuccessorDecidedAboutThisOriginsOwnReadings':
            gaps.get('whatTheGeneration22SuccessorDecidedAboutThisOriginsOwnReadings'),
        'helperCorrections': helpers.get('helperCorrections'),
        'openHelperFailuresOnAClaimedPositive': open_helpers,
        'retainedArtifactDigests': digests,
        'retainedArtifactDigestStanding': {
            'whatTheTableIs': (
                'the sha256 of every exported artifact AS READ by this reconciliation stage, %d '
                'rows, re-derived by each command from the bytes on disk. Artifacts written AFTER '
                'this stage by the command (none are declared) would not be in it.' % len(digests)),
            'reproducibility': (
                'NOT re-measured in generation 23. The generation-20 report claimed a three-command '
                'leaf comparison through diagnostics outside output/ that were never exported '
                '(helper-corrections V22-D12), so that claim is not repeated here.')},
        'limitations': [
            ('Every compiler, provider, toolchain, OS and runtime observation in these Runs is a '
             'SYNTHETIC TRUSTED INPUT authored by this origin. Nothing here qualifies a compiler, '
             'provider, host or operating system, and no such qualification is claimed.'),
            ('No product code was written, no repository was modified, no commit or push was made, '
             'and no product was executed. Every byte produced lives under this origin\'s own '
             'generation-23 output directory.'),
            ('The parent subject was never held. Only the disclosed kit and the parent digest '
             'declared inside its manifest were verified.'),
            ('%d claimed positives are graded schema-admitted-record (%s): each record is re-admitted '
             'against its owning schema and its identities and Run joins are recomputed, which is the '
             'evidence class accepted for its requirement kind. Their remaining semantic fields were '
             'SURVEYED against their owners in generation 23 rather than re-derived by a separate '
             'instrument; the survey found and corrected positives in other classes (V23-D6..V23-D11).'
             % (len([r for r in audit_rows if r['evidenceClass'] == 'schema-admitted-record']),
                ', '.join(r['id'] for r in audit_rows if r['evidenceClass'] == 'schema-admitted-record'))),
            ('The repair, comparison, baseline, invocation, authorization and query records are '
             'RECORD reconstructions with their identities recomputed and their admission laws '
             'executed. No repair was previewed, applied or authorized; no test or preparation '
             'ran; no baseline was adopted; no query engine was run by a product. Fields that name '
             'records this origin did not construct are labelled helper-only.'),
            ('L1-L3 normalised body identities, symbol-to-path attribution and provider occupancy '
             'are not recomputable by a consumer; the kit says so and substitutes retained custody, '
             'which is what was executed.'),
            ('%s of the %s advertised language modes (%s) have an admitted representable path at '
             'the record level but were NOT exercised end-to-end on a sealed Run '
             '(vectors/advertised-mode-paths.json).'
             % (len((J('vectors/advertised-mode-paths.json') or {}).get(
                 'modesRepresentedButNotExercisedEndToEnd') or []),
                (J('vectors/advertised-mode-paths.json') or {}).get('modeCount'),
                ', '.join((J('vectors/advertised-mode-paths.json') or {}).get(
                    'modesRepresentedButNotExercisedEndToEnd') or []))),
            ('Coverage limitations that are not design gaps are listed with the artifact that '
             'measures each in coverageLimitationsDisclosedNotDesignGaps; none is merged into the '
             'complete-positive claim.'),
            ('No root admission, agreement, expected result, author model, checker or golden was '
             'supplied, read or inferred. The root outcome over these exact bytes is UNOBSERVED by '
             'this origin.'),
        ],
        'standing': {
            'noRootAdmissionClaim': (
                'this origin reports ONLY its own independently executed admission, closure, replay, '
                'audit and controls. It does not claim that any root, author or successor admitted, '
                'agreed with or validated these bytes.'),
            'noProductQualificationClaim': (
                'nothing here authorizes a product implementation or qualifies any product, '
                'component, compiler, provider or host.'),
            # a CURRENT declaration (V20-D6): read from the custody artifact, never restated
            'kitOnly': (
                'every citation names a path and selector inside the frozen kit. The disclosed '
                'PRIOR-OWN inputs are named in notes/v23-input-custody.json disclosedPriorInputs '
                'and are, verbatim from that artifact: %s'
                % '; '.join('%s -- %s' % (p, s) for p, s in sorted(
                    (cust.get('disclosedPriorInputs') or {}).items()) if p != 'notClaimed')),
            'nothingElseClaimedAsAnInput': (cust.get('disclosedPriorInputs') or {}).get('notClaimed'),
            'runtimeFilesNotNamedAsInputs': cust.get('runtimeFilesNotNamedAsInputs'),
            'pathCensus': census.get('verdict'),
            'priorGenerationsUnmodified': hist.get('measuredC_priorGenerations'),
            'writeConfinement': hist.get('measuredA_writeConfinement'),
            'historyStanding': hist.get('state'),
            'generationLabelProvenance': {
                'verdict': labels.get('verdict'), 'method': labels.get('method'),
                'standing': (
                    'audited against the retained before-images before any copied code ran and '
                    'again after every stage; the one drift found at generation 22 (a generation-19 '
                    'sentence rewritten by the generation-20 rebind) was restored from its '
                    'before-image (V22-D1); at generation 23 the only report was a false positive on a '
                    'current-origin check, corrected in the classifier (V23-D4)')},
            'writesMadeUnderAPriorGeneration': {
                'thisSession': (
                    'generations modified during this session, measured in '
                    'notes/v23-history-standing.json measuredC: %s'
                    % (hist.get('measuredC_priorGenerations') or {}).get(
                        'generationsModifiedDuringThisSession')),
                'historicalDamageStillOpen': (
                    'the GENERATION-17 session overwrote TWO files under the generation-16 output '
                    'before its own control caught the defect: helper-corrections.json and '
                    'notes/siblings-untouched.json. The prior bytes were not retained by this '
                    'origin and are NOT claimed to be restorable. The item stays OPEN and is '
                    'carried forward rather than marked clean (helper-corrections V17-D8).'),
                'generation17Census': J('notes/prior-generation-writes.json')},
        },
    }
    with open(OUT + '/blind-review.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    write_md(doc)
    print('blind-review.json + blind-review.md written')
    print('verdict:', verdict, '| final stage:', final_stage)
    print('requirementStatus counts:', dict(counts))
    print('conditions:', json.dumps(conditions)[:600])


def write_md(d):
    L = []
    A = L.append
    A('# OpenSIP blind consumer design review -- consumer-b.' + 'v23')
    A('')
    A('**Verdict: %s**' % d['verdict'])
    A('')
    delta = d['inputKit']['measuredDeltaAgainstThePriorDisclosedKit'] or {}
    A('| | |')
    A('|---|---|')
    A('| sessionId | `%s` |' % d['sessionId'])
    A('| same-origin ancestry | %s (generation 21 prepared, never launched) |'
      % ' -> '.join(d['sameOriginAncestry']))
    A('| subject manifest SHA-256 | `%s` |' % d['inputKit']['subjectManifestSha256'])
    A('| parent digest declared in that manifest | `%s` (%s) |'
      % (d['inputKit']['parentSubjectSha256DeclaredInThatManifest'],
         d['inputKit']['declaredParentBindingResult']))
    A('| kit files verified | %s / %s (%s) |'
      % (d['inputKit']['filesVerifiedPass'], d['inputKit']['fileCount'],
         d['inputKit']['everyRowVerifiedResult']))
    A('| measured normative delta | %s unchanged, %s changed, %s added |'
      % (delta.get('unchangedCount'), delta.get('changedCount'), delta.get('addedCount')))
    A('| changed owner | %s |' % ', '.join('`%s`' % c['path'] for c in delta.get('changed') or []))
    A('| requirement status | %s |'
      % ', '.join('%s %d' % (k, v) for k, v in sorted(d['requirementStatus']['counts'].items())))
    A('| claimed-positive audit | %s |' % d['claimedPositiveAudit']['counts'])
    A('| new MUST / SHOULD / advisories | %d / %d / %d |'
      % (len(d['newMustIssues']), len(d['newShouldIssues']), len(d['advisories'])))
    A('')
    A('> This is NOT a parent whole-candidate verification: only the parent digest declared inside')
    A('> the held manifest was compared. No root admission, agreement, expected result, author')
    A('> model or checker was supplied, read or inferred; the root outcome over these exact bytes')
    A('> is unobserved by this origin. Nothing here qualifies any product, compiler, provider or')
    A('> host; every toolchain and host observation is a synthetic trusted input.')
    A('')
    A('## Why this verdict')
    A('')
    A(d['verdictBasis']['rule'])
    A('')
    for k, v in d['verdictBasis']['conditions'].items():
        A('- %s: **%s**' % (k, v if not isinstance(v, list) else (len(v) if v else 'none')))
        if isinstance(v, list) and v:
            A('  - %s' % ', '.join(v))
    A('')
    A('## What changed in the input')
    A('')
    w = d['whatChangedInTheInputThisGeneration']
    A('- kind: %s; %s' % (w['kind'], w['deltaMethod']))
    A('- what the changed owner decides: %s' % w['whatTheChangedOwnerDecides'])
    A('- consequence: %s' % w['consequence'])
    A('')
    A('## Complete positive Runs')
    A('')
    A('| Run | runId | verdict | objects | blobs | closure | replay | controls | atom law |')
    A('|---|---|---|---|---|---|---|---|---|')
    for r in d['claimedCompletePositives']:
        A('| %s | `%s...` | %s | %s | %s | %s passed / %s n-a / %s refused | %s (%s findings, %s '
          'witnesses) | %d, all refused: %s | %s atoms, %s checks, %s refused |'
          % (r['label'], (r['claimedRunId'] or '')[:22], r['verdict'], r['objectCount'],
             r['blobCount'], r['closure']['checksPassed'], r['closure']['checksNotApplicable'],
             r['closure']['checksRefused'], r['freshProcessReplay']['verdict'],
             r['freshProcessReplay']['findingsCompared'],
             r['freshProcessReplay']['predicateWitnessesCompared'], r['controls']['count'],
             r['controls']['allRefused'], r['independentAtomLaw']['atoms'],
             r['independentAtomLaw']['checks'], r['independentAtomLaw']['refusals']))
    A('')
    for r in d['claimedCompletePositives']:
        A('- `%s` sha256 %s' % (r['exportFile'], r['exportFileSha256']))
    A('')
    A('## Claimed-positive audit (every requirement, from its final bytes)')
    A('')
    cpa = d['claimedPositiveAudit']
    A('Counts: %s. Evidence classes: %s.' % (cpa['counts'], cpa['evidenceClassCounts']))
    A('')
    A(cpa['standing'])
    A('')
    A('| id | kind | evidence class | result | checks passed | first refusal |')
    A('|---|---|---|---|---|---|')
    for r in cpa['rows']:
        fr = r['firstRefusal']
        A('| %s | %s | %s | %s | %s | %s |'
          % (r['id'], r['kind'], r['evidenceClass'], r['result'], r['checksPassed'],
             ('`%s`' % fr['check']) if fr else ''))
    A('')
    A('## Atom contract reconciliation')
    A('')
    ac = d['atomContractReconciliation']
    A('- instrument: %s -> `%s`' % (ac['instrument'], ac['artifact']))
    for lab, v in ac['perRun'].items():
        A('- %s: %s' % (lab, v))
    for p in ac['predecessorControls']:
        A('- predecessor `%s`: refused %s at `%s` (%s refusals)'
          % (p['predecessor'], p['refused'], p['firstRefusal'], p['refusalCount']))
    for t in ac['tamperControls']:
        A('- tamper %s / %s (%s): refused %s at `%s`'
          % (t['run'], t['control'], t['clause'], t['refused'], t['firstRefusal']))
    A('- law vectors: %d, passed %d'
      % (len(ac['lawVectors']), sum(1 for v in ac['lawVectors'] if v['result'] == 'PASS')))
    A('- min-resolution atom-level cases: %s, refused %s'
      % (ac['minResolutionAtomLevelCases'], ac['minResolutionAtomLevelRefused']))
    for c in ac['claimLimits'] or []:
        A('- claim limit: %s' % c)
    A('')
    A('## Query, mutation and authorization surfaces')
    A('')
    for k in ('wholePublishedQuerySurface', 'wholePublishedMutationSurface', 'authorizationRecords'):
        A('- **%s**: %s' % (k, json.dumps(d[k], default=str)))
    A('')
    A('## From-scratch command')
    A('')
    A('```')
    A(d['fromScratchCommand']['command'])
    A('```')
    A('')
    fs = d['fromScratchCommand']
    A('The command declares **%s** stages; **%s** preceding stages of this same command were '
      'recorded when this reconciliation ran; failed stages: **%s**. %s'
      % (fs['declaredStageCount'], fs['stagesRecordedWhenThisReconciliationRan'],
         fs['failedStages'], fs['reconciliationStanding']))
    A('')
    for att in ((fs.get('earlierCommandsOfThisGeneration') or {}).get('attempts') or []):
        A('- earlier command %s (`%s`): failed stages %d%s'
          % (att['attempt'], att['stageIoDir'], att['failedStageCount'],
             ''.join('\n  - %s' % f for f in att['failedStages'])
             or ('\n  - ' + att.get('whyNotFinal', ''))))
    A('')
    mg = fs['measuredReadGraph']
    A('Measured read graph (`%s`): **%s**; %s stages logged, %s edges, order violations %d, '
      'undeclared edges %d, unknown reads %d. Child-process reads are not measured.'
      % (mg['file'], mg['result'], mg['stagesLogged'], mg['edges'],
         len(mg['orderViolations'] or []), len(mg['undeclaredEdges'] or []),
         len(mg['readsOfArtifactsNoStageWrote'] or [])))
    A('')
    A('## New MUST issues')
    A('')
    if not d['newMustIssues']:
        A('None. ' + (d['emptyMustJustification'] or ''))
    for s in d['newMustIssues']:
        A('- **%s** %s' % (s.get('id'), s.get('title')))
    A('')
    A('## New SHOULD issues')
    A('')
    if not d['newShouldIssues']:
        A('None open. Earlier SHOULD items resolved by a normative successor:')
        A('')
        for s in d.get('resolvedByANormativeSuccessor') or []:
            A('- **%s** -- %s (%s)' % (s['id'], s['title'], s.get('disposition')))
    for s in d['newShouldIssues']:
        A('- **%s** %s' % (s.get('id'), s.get('title')))
        for k in ('selectors', 'whatTheKitSays', 'consequence', 'readingApplied', 'smallestFix'):
            if s.get(k):
                A('  - %s: %s' % (k, '; '.join(s[k]) if isinstance(s[k], list) else s[k]))
    A('')
    A('Blocker statement: %s' % d['blockerStatement'])
    A('')
    A('## Advisories')
    A('')
    for s in d['advisories']:
        A('- **%s** (%s) %s' % (s['id'], s['class'], s['title']))
        A('  - observation: %s' % s['observation'])
        A('  - handled here by: %s' % s['howThisOriginHandledIt'])
    A('')
    A('## What the generation-23 successor decided about this origin\'s own readings')
    A('')
    for k, v in (d.get('whatTheGeneration23SuccessorDecidedAboutThisOriginsOwnReadings') or {}).items():
        A('- **%s**: %s' % (k, v))
    A('')
    A('## Withdrawn by this origin, or resolved in kit bytes')
    A('')
    for s in d['withdrawnOrResolvedSinceTheLastGeneration'] or []:
        A('- **%s** -- %s. %s' % (s['id'], s['disposition'], s['why']))
    A('')
    A('## Algorithm freedom that is NOT a gap')
    A('')
    for s in d['algorithmFreedomNotGaps'] or []:
        A('- **%s**: pinned observable -- %s; left open -- %s. %s'
          % (s['topic'], s['pinnedObservable'], s['left open'], s['why']))
    A('')
    A('## Coverage limitations (disclosed, not design gaps)')
    A('')
    for c in d.get('coverageLimitationsDisclosedNotDesignGaps') or []:
        A('- %s' % c['limitation'])
        A('  - why not a gap: %s' % c['whyNotAGap'])
        A('  - measured where: `%s`' % c['measuredWhere'])
    A('')
    A('## Helper corrections (helper bug != design gap)')
    A('')
    A('| id | generation | status | where |')
    A('|---|---|---|---|')
    for h in d['helperCorrections'] or []:
        A('| %s | %s | %s | %s |' % (h['id'], h.get('generation'), h['status'], h['where']))
    A('')
    for h in d['helperCorrections'] or []:
        if str(h['id']).startswith('V23-'):
            A('### %s' % h['id'])
            A('')
            A('- original failure: %s' % h['originalFailure'])
            A('- kit selector: %s' % h['kitSelector'])
            A('- correction: %s' % h['correction'])
            A('')
    A('Open helper failures on a claimed positive: **%d**.'
      % len(d['openHelperFailuresOnAClaimedPositive'] or []))
    A('')
    A('## Limitations and scope')
    A('')
    for x in d['limitations']:
        A('- %s' % x)
    A('')
    A('Artifact digests: %s' % d['retainedArtifactDigestStanding']['whatTheTableIs'])
    A('')
    A('Reproducibility: %s' % d['retainedArtifactDigestStanding']['reproducibility'])
    A('')
    A('## Standing')
    A('')
    for k, v in d['standing'].items():
        if k == 'writesMadeUnderAPriorGeneration':
            A('- **%s**: %s' % (k, v['thisSession']))
            A('  - still open from generation 17: %s' % v['historicalDamageStillOpen'])
        elif k in ('priorGenerationsUnmodified', 'writeConfinement', 'runtimeFilesNotNamedAsInputs'):
            A('- **%s**: %s' % (k, json.dumps(v, default=str)[:1200]))
        else:
            A('- **%s**: %s' % (k, v))
    A('')
    with open(OUT + '/blind-review.md', 'w') as f:
        f.write('\n'.join(L) + '\n')


main()
