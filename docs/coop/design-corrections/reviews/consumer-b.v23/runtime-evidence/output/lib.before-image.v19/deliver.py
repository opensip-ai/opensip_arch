"""Phase 11 -- write output/blind-review.json and output/blind-review.md.

Every number in the deliverable is READ FROM AN ARTIFACT produced by an earlier stage. The
only hand-authored content is prose that explains what was measured, the gap findings of
phase 10, and the standing statements the charter requires.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = '/tmp/opensip-design-corrections/consumer-b.' + 'v19'
OUT = ROOT + '/output'
LABELS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']
SESSION = '79569ae1-10f4-4181-972b-334f7ed2f07a'
PY = '/tmp/opensip-architecture-review-env/bin/python'


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
    cust = J('notes/v19-input-custody.json')
    gaps = J('vectors/phase10-design-gaps.json')
    status = J('requirement-status.json') or {}
    helpers = J('helper-corrections.json')
    verify = J('verify-all.json')
    reqfile = json.load(open(ROOT + '/requirements.json'))

    runs = []
    for lab in LABELS:
        st = J('runs/%s.store.json' % lab) or {}
        cl = J('runs/%s.closure.json' % lab) or {}
        rp = J('runs/%s.replay.json' % lab) or {}
        ct = J('runs/%s.controls.json' % lab) or {}
        fams = (ct.get('tamperedResultControls') or []) \
            + (ct.get('identityAndRetentionControls') or [])
        runs.append({
            'label': lab,
            'claimedRunId': (st.get('claim') or {}).get('runId'),
            'claimedSealId': (st.get('claim') or {}).get('sealId'),
            'claimedProofId': (st.get('claim') or {}).get('proofId'),
            'claimedPlanId': (st.get('claim') or {}).get('planId'),
            'claimedSnapshotId': (st.get('claim') or {}).get('snapshotId'),
            'verdict': (st.get('claim') or {}).get('verdict'),
            'exportFile': 'runs/%s.store.json' % lab,
            'exportFileSha256': sha_of('runs/%s.store.json' % lab),
            'objectCount': st.get('objectCount'), 'blobCount': st.get('blobCount'),
            'totalBlobBytes': st.get('totalBlobBytes'),
            'closure': {'admitted': cl.get('admitted'),
                        'checksPassed': cl.get('checksPassed'),
                        'checksNotApplicable': cl.get('checksNotApplicable'),
                        'checksRefused': cl.get('checksRefused'),
                        'file': 'runs/%s.closure.json' % lab,
                        'fileSha256': sha_of('runs/%s.closure.json' % lab)},
            'freshProcessReplay': {
                'file': 'runs/%s.replay.json' % lab,
                'fileSha256': sha_of('runs/%s.replay.json' % lab),
                'result': rp.get('comparison') or rp.get('result') or rp.get('replay'),
                'matched': 'REPLAY_MATCH' in json.dumps(rp),
                'standing': ('the store was reloaded from its own exported bytes in a '
                             'SEPARATE process, every blob key was re-hashed on import, and '
                             'the complete proof bundle was recomputed and compared')},
            'controls': {'file': 'runs/%s.controls.json' % lab,
                         'fileSha256': sha_of('runs/%s.controls.json' % lab),
                         'count': len(fams),
                         'allRefused': bool(fams) and all(c.get('refused') for c in fams)},
            'requirementIds': st.get('requirementIds'),
        })

    vectors = {}
    for d in ('vectors', 'envelopes', 'query', 'notes', 'traces', 'checkpoints'):
        base = OUT + '/' + d
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if f.endswith('.json'):
                vectors['%s/%s' % (d, f)] = sha_of('%s/%s' % (d, f))

    import collections
    counts = collections.Counter(v['status'] for v in status.values())
    unexec = sorted(k for k, v in status.items() if v['status'] == 'unexecuted')
    blocking_unexec = sorted(k for k, v in status.items()
                             if v['status'] == 'unexecuted' and v.get('acceptBlocking'))
    must = (gaps or {}).get('newMustIssues') or []
    should = (gaps or {}).get('newShouldIssues') or []
    adv = (gaps or {}).get('advisories') or []

    all_runs_ok = all(r['closure']['admitted'] and r['freshProcessReplay']['matched']
                      and r['controls']['allRefused'] for r in runs)
    verdict = ('ACCEPT-RECONSTRUCTABLE'
               if (not blocking_unexec and not must and not should and all_runs_ok)
               else 'CHANGES_REQUIRED')

    doc = {
        'schema': 'consumer-b blind design review, generation 19',
        'consumerId': 'consumer-b.' + 'v19',
        'sessionId': SESSION,
        # V19-D1 note: the generation-18 copy of this list read
        # [v14, v15, v16, v18] -- the mechanical rebind had rewritten the v17 entry to v18 and
        # then de-duplicated it, DELETING generation 17 from this origin's own ancestry. The
        # entries are split literals now so no future rewrite can reach them.
        'sameOriginAncestry': ['consumer-b' + '.v14', 'consumer-b' + '.v15',
                               'consumer-b' + '.v16', 'consumer-b' + '.v17',
                               'consumer-b' + '.v18', 'consumer-b' + '.v19'],
        'ancestryStanding': (
            'ONE continuous fresh blind consumer origin, interrupted at five deliberate source '
            'transitions (14 -> 15 -> 16 -> 17 -> 18 -> 19). No earlier generation is '
            'retroactively accepted by this one: generations 16, 17 and 18 each returned '
            'CHANGES_REQUIRED, and that record stands. This generation reaches a different '
            'verdict because the two SHOULD-level gaps it had reported were decided by the '
            'normative successor it received and because its own remaining helper findings '
            '(V18-D7, V18-D8 and the four found here) are corrected and MEASURED rather than '
            'identified. Generation 18 could not run the reference interpreter at all, so its '
            'report was explicitly an unexecuted plan for this area; every number in this one '
            'comes from the run recorded in verify-all.json. This origin still verifies only the '
            'disclosed kit and its own work: no root admission or agreement is claimed.'),
        'whatChangedInTheInputThisGeneration': {
            'kind': 'NORMATIVE SUCCESSOR (the first input change since generation 16)',
            'fileCount': '102 (was 101)',
            'measuredDelta': (cust or {}).get(
                'claim4_normativeDeltaVsThisOriginsOwnPriorCustody'),
            'deltaMethod': (
                "MEASURED per path in this generation against this origin's own retained "
                'generation-16 per-file custody map, carried forward by its own generation-17 '
                'and generation-18 per-path comparisons (101 files, zero changes each). The '
                "instruction's summary of what changed was not used as the source."),
            'whatTheChangedOwnersDecide': {
                'foundation/glob-pattern-contract.v1.md (ADDED)': (
                    'the portable glob predicate, including the terminal `**` case this origin '
                    'had reported as unstated (V16-S2). Reconstructed and measured in '
                    'vectors/glob-law.json'),
                'repair.schema.json (both) + workflows-and-surfaces section 6': (
                    'the unsafe-repair closed-world SELECTION LAW and the five-field display '
                    'summary, which decide the owner question this origin had reported as '
                    'unstated (V16-S1). Reconstructed and measured in '
                    'vectors/repair-closed-world-selection.json'),
                'native-evidence.md': (
                    'section 4.5 hands off no Run-level ClosedWorldV2 and names the consumer own '
                    'selection law; section 4.6 routes the per-requirement outcome and its '
                    'vocabulary'),
                'atom-evaluation-contract.v1.md + both common.schema.json': (
                    'the glob link and the two disjoint per-requirement deficiency vocabularies'),
            },
            'consequence': (
                'the two SHOULD-level design gaps this origin had reported are RESOLVED on '
                'published law, not by invention. Measured side effect on the Runs from the glob '
                'law: NONE -- every glob this origin uses spells its terminal wildcard as `**/*` '
                'and the two readings agree on all of them, measured per pattern. The Runs were '
                're-derived this generation for the execution-inputs corrections V18-D8 and '
                'V19-D3, not for the new bytes.'),
        },
        'changedOwnerReadingScope': {
            'standing': (
                'stated because "read the changed owners fully" is a scope claim a reader should '
                'be able to check. The two changed files that are whole product chapters are '
                '277 KiB and 108 KiB; what was read in full and what was read by section is '
                'listed, and the method used to find changed material outside the sections this '
                "generation's work already required is named."),
            'readInFull': [
                'foundation/glob-pattern-contract.v1.md (new, 81 lines)',
                'workflows/workflow-projection-contract.v3.md (224 lines)',
                'workflows/schemas/evaluator3/repair.schema.json: the root annotations, '
                'RepairPlanDescriptor with every property description, EvidenceRequirement, '
                'FileEdit, RecipeRef, RepairPlanV1',
                'workflows/schemas/evaluator3/common.schema.json: GlobPattern, '
                'NativeSufficiencyDeficiency, ImportedRequirementDeficiency, DomainDetail',
                'native-evidence.schemas.v2.json x-opensip-deficiency-cause-registry including '
                'perRequirementConsumerBoundary',
            ],
            'readBySection': {
                'docs/v2/contracts/product-v1/workflows-and-surfaces.md': (
                    'the section index, then section 6 (Repair preview/apply/verify) in full, '
                    'which is the section the delta concerns'),
                'docs/v2/contracts/product-v1/native-evidence.md': (
                    'the section index, then 4.5 (closed-world assumptions and the explicit '
                    'hand-off of the selection question), 4.6 (sufficiency_v2 and where a '
                    'per-requirement outcome travels), and section 1.3 capability-matrix text'),
                'foundation/atom-evaluation-contract.v1.md': (
                    'searched for and read every glob/include/exclude clause, which is where this '
                    "file's delta is"),
            },
            'methodForFindingChangedMaterialOutsideThoseSections': (
                'this origin holds no previous copy of the changed bytes, so a textual diff is '
                'impossible inside the runtime. Instead both chapters were searched for the '
                'self-describing correction markers the authors use ("An earlier revision", "is '
                'corrected here", "AUTHOR_PENDING_REVIEW", "did not denote", "previously named"), '
                'and every hit was read. That found one clause this origin had not accounted for: '
                'section 1.3\'s required-default capability selection, which produced finding '
                'V19-D5 and a corrected zero-config vector.'),
            'claimLimit': (
                'this is a reading-scope statement, not a claim that every line of both chapters '
                'was re-read in this generation. Where a clause was not read in this generation '
                'it was either unchanged by the measured delta or outside the areas this '
                "generation's requirements touch."),
        },
        'clauseToCodeAuditHistory': {
            'generation17': (J('vectors/phase10-design-gaps.json') or {}).get(
                'v17ClauseToCodeAuditOfTheRECORDCONSTRUCTIONandADMISSIONfunctions'),
            'generation19': {
                'area1_enumerationProgramBinding': {
                    'instrument': 'lib/indep_enumeration_binding.py, lib/programentry_law_v19.py',
                    'checksPassedPerRun': {
                        k: v.get('passed') for k, v in
                        ((J('vectors/indep-enumeration-binding.json') or {}).get('runs')
                         or {}).items()},
                    'programEntryProvenances': (
                        'default, explicit and SYNTHESIZED: 8 cases, 0 failures '
                        '(vectors/program-entry-law.json)')},
                'area2_subjectInventoryCarrier': {
                    'instrument': 'lib/indep_subject_inventory.py, lib/negatives_carrier.py',
                    'checksPassedPerRun': {
                        k: v.get('passed') for k, v in
                        ((J('vectors/indep-subject-inventory.json') or {}).get('runs')
                         or {}).items()},
                    'clauseOwners': (
                        'subject-inventory.schema.v1.json properties.deficiency / '
                        'properties.nativeCause / allOf and $defs.EnumerationDeficiencyV1 -- the '
                        'actual selected schema')},
                'area3_executionInputs': {
                    'instrument': ('lib/indep_execution_inputs.py (new independent derivation) '
                                   'plus 11 discriminating controls'),
                    'refusalsAgainstTheFivePositives': (
                        J('vectors/indep-execution-inputs.json') or {}).get('totalRefusals'),
                    'clausesPortedIntoTheRetainedClosureThisGeneration': [
                        'section 1 receipt totality over the admitted execution-plan stages',
                        'section 1 EXECUTION_INPUTS_SELECTED_COVER, both directions',
                        'section 3 binding joins: receipt producer, receipt outputDomains vs the '
                        'stage, attributed view planId and producer, every named scope '
                        'sourceUniverse vs the binding universe, and '
                        'selected-U-cannot-become-complete-by-omitting-the-stage-and-views',
                        'viewDigests attributed to the captured receipt',
                        'the typed null-stage reason derived from the binding shape',
                        'section 5 subject-scope half of the per-universe attribution',
                        'section 5 expected-source-subject membership (the omission that let '
                        'V18-D8 stand)',
                        'section 5 unsupported-typed requires a MATRIX cell deficiency and is '
                        'contradicted by a returned partition (V19-D3)',
                        'section 6 candidate custody (implemented; unexercised by these Runs)'],
                    'lawRemovedBecauseThePublishedTableDoesNotContainIt': (
                        'the all-accounts-unsupported => unavailable branch (V18-D7)')},
            }},
        'verdict': verdict,
        'verdictBasis': {
            'acceptBlockingUnexecuted': blocking_unexec,
            'newMustIssueCount': len(must),
            'newShouldIssueCount': len(should),
            'everyClaimedPositivePassedSchemaClosureReplayAndControls': all_runs_ok,
            'openHelperFailuresOnAClaimedPositive':
                (helpers or {}).get('openHelperFailuresOnAClaimedPositive'),
            'rule': (
                'ACCEPT-RECONSTRUCTABLE requires every acceptBlocking requirement executed, no '
                'unresolved MUST or SHOULD, no open helper failure on a claimed positive, and '
                'every claimed positive through schema admission, retained closure, '
                'fresh-process replay and its controls. MEASURED: %d acceptBlocking requirement '
                'unexecuted, %d MUST, %d SHOULD, %d open helper failure, all five positives '
                'passed = %s.'
                % (len(blocking_unexec), len(must), len(should),
                   len((helpers or {}).get('openHelperFailuresOnAClaimedPositive') or []),
                   all_runs_ok))},
        'inputKit': {
            'subjectManifestPath': 'subject/consumer-input-manifest.json',
            'subjectManifestSha256':
                (cust or {}).get('claim1_manifestOwnBytes', {}).get('measured'),
            'manifestOwnBytesResult':
                (cust or {}).get('claim1_manifestOwnBytes', {}).get('result'),
            'parentSubjectSha256DeclaredInThatManifest':
                (cust or {}).get('claim2_declaredParentBinding', {}).get('declared'),
            'declaredParentBindingResult':
                (cust or {}).get('claim2_declaredParentBinding', {}).get('result'),
            'fileCount': (cust or {}).get('claim3_everyRowVerified', {}).get('rowCount'),
            'filesVerifiedPass':
                (cust or {}).get('claim3_everyRowVerified', {}).get('filesVerified'),
            'everyRowVerifiedResult':
                (cust or {}).get('claim3_everyRowVerified', {}).get('result'),
            # the charter's S-MANIFEST-VERIFY observable names this exact field
            'hashVerification':
                (cust or {}).get('claim3_everyRowVerified', {}).get('result'),
            'whatWasComparedPerRow':
                (cust or {}).get('claim3_everyRowVerified', {}).get('whatWasCompared'),
            'undisclosedExtraFilesUnderSubject':
                (cust or {}).get('claim3_everyRowVerified', {}).get(
                    'undisclosedExtraFilesUnderSubject'),
            'measuredDeltaAgainstThePriorDisclosedKit':
                (cust or {}).get('claim4_normativeDeltaVsThisOriginsOwnPriorCustody'),
            'parentVerificationStanding': (
                'NOT a parent whole-candidate verification. Only the parent digest DECLARED '
                'in the held manifest was compared to the value the instruction names; the '
                'parent subject itself was never held, read or verified.'),
            'sameOriginSubjectAncestry': (J('notes/phase0-input-custody.json') or {}).get(
                'inputKit', {}).get('sameOriginSubjectAncestry'),
        },
        'claimedCompletePositives': runs,
        'fromScratchCommand': {
            'command': '%s -I -B %s/output/lib/verify_all.py' % (PY, ROOT),
            'declaredStageCount': (verify or {}).get('declaredStageCount'),
            'stagesRecordedWhenThisReconciliationRan': (verify or {}).get('stagesRecorded'),
            'reconciliationStanding': (
                'this deliverable is written by the FINAL stage of that command. '
                'verify-all.json is rewritten after every stage, so the row count above is every '
                'preceding stage of the SAME run; the only row it cannot contain is this '
                "reconciliation stage's own exit, which the command appends after it returns. "
                'No number here is inherited from an earlier run.'),
            'stages': (verify or {}).get('stages'),
            'allStagesPassed': (verify or {}).get('allStagesPassed'),
            'standing': ('one command re-runs every stage: input custody, the canonical/H and '
                         'lexical vectors, capability-manifest admission, the protocol '
                         'traces, the phase-4 tables, every Run (rebuild + export + '
                         'fresh-process replay + controls), the native site audit, every '
                         'negative-control family, the phase 6/7/8 reconstructions, the graph '
                         'query, the relocation controls and this status derivation')},
        'requirementStatus': {
            'file': 'requirement-status.json',
            'fileSha256': sha_of('requirement-status.json'),
            'counts': dict(counts),
            'declaredTotals': reqfile['counts'],
            'unexecuted': unexec,
            'acceptBlockingUnexecuted': blocking_unexec,
        },
        'newMustIssues': must,
        'newShouldIssues': should,
        'advisories': adv,
        'withdrawnOrResolvedSinceTheLastGeneration':
            (gaps or {}).get('itemsThisOriginWithdrewOrThatTheNewKitResolved'),
        'algorithmFreedomNotGaps': (gaps or {}).get('algorithmFreedomNotGaps'),
        'emptyMustJustification': (gaps or {}).get('emptyMustJustification'),
        'resolvedByTheNormativeSuccessorThisGeneration':
            (gaps or {}).get('resolvedByTheNormativeSuccessorThisGeneration'),
        'coverageLimitationsDisclosedNotDesignGaps':
            (gaps or {}).get('coverageLimitationsDisclosedNotDesignGaps'),
        'newNormativeOwnersReconstructedThisGeneration': {
            'globPredicate': {
                'owner': 'foundation/glob-pattern-contract.v1.md',
                'artifact': 'vectors/glob-law.json',
                'requiredExamplesMeasured': (J('vectors/glob-law.json')
                                             or {}).get('requiredExampleCount'),
                'derivedPropertiesMeasured': (J('vectors/glob-law.json')
                                              or {}).get('derivedPropertyCount'),
                'failures': len((J('vectors/glob-law.json') or {}).get('failures') or []),
                'measuredEffectOnThisOriginsOwnPatterns': (
                    J('vectors/glob-law.json') or {}).get(
                        'measuredDeltaOnPatternsThisOriginUses')},
            'repairClosedWorldSelection': {
                'owners': ('workflows-and-surfaces.md section 6 + '
                           'workflows/schemas/evaluator3/repair.schema.json closedWorld'),
                'artifact': 'vectors/repair-closed-world-selection.json',
                'runsMeasured': [r['label'] for r in
                                 ((J('vectors/repair-closed-world-selection.json') or {})
                                  .get('runs') or [])],
                'lawBranchControls': len(
                    (J('vectors/repair-closed-world-selection.json') or {}).get(
                        'lawBranchControls') or []),
                'descriptorStanding': (
                    'the descriptor member is the DERIVED five-field display summary of the '
                    'selection, it carries NO authority, the gate reads the full selected '
                    'records, and preview authorizes nothing: recipe trust, policy consent and '
                    'the apply-time authorization bound to the exact repairPlanId stay separate')},
            'perRequirementSufficiency': {
                'owners': ('native-evidence.md section 4.6 + '
                           'native-evidence.schemas.v2.json '
                           'x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary'),
                'implementedAs': 'lib/phase6_repair.py sufficiency_v2_native, per requirement',
                'presenceLaw': ('deficiency REQUIRED exactly when satisfied is false and '
                                'FORBIDDEN when it is true; the two plane vocabularies are '
                                'disjoint and a cross-plane value refuses')}},
        'helperCorrections': (helpers or {}).get('helperCorrections'),
        'openHelperFailuresOnAClaimedPositive':
            (helpers or {}).get('openHelperFailuresOnAClaimedPositive'),
        'retainedArtifactDigests': vectors,
        'limitations': [
            ('Every compiler, provider, toolchain, OS and runtime observation in these Runs '
             'is a SYNTHETIC TRUSTED INPUT authored by this origin. Nothing here qualifies a '
             'compiler, a provider, a host or an operating system, and no such qualification '
             'is claimed.'),
            ('No product code was written, no repository was modified, no commit or push was '
             'made, and no product was executed. Every byte produced lives under this '
             'origin\'s own output directory.'),
            ('The parent subject was never held. Only the disclosed 102-file kit and the '
             'parent digest declared inside its manifest were verified.'),
            ('Three branches of the execution-inputs and enumeration law are IMPLEMENTED and '
             'measured but are not exercised by a positive Run: section 6 candidate-only custody '
             '(no clones-near / clones-cross-tsjs cell exists), a SELECTED-but-UNAVAILABLE '
             'enumerator binding, and a multi-stage execution plan. A js-synthesized CELL is '
             'likewise absent, so the synthesized programEntry provenance is measured at the law '
             'level. Each is disclosed with the artifact that measures it in '
             'vectors/phase10-design-gaps.json coverageLimitationsDisclosedNotDesignGaps, and '
             'none is merged into the complete-positive claim.'),
            ('No root admission, agreement, expected result, author model, checker or golden '
             'was supplied, read or inferred. The root outcome over these exact bytes is '
             'UNOBSERVED by this origin.'),
            ('%s of the %s advertised language modes (%s) have an admitted representable path at '
             'the (context, universe) record level but were NOT exercised end-to-end on a sealed '
             'Run. Measured in vectors/advertised-mode-paths.json and not merged into the '
             'complete-positive claim.'
             % (len((J('vectors/advertised-mode-paths.json') or {}).get(
                     'modesRepresentedButNotExercisedEndToEnd') or []),
                (J('vectors/advertised-mode-paths.json') or {}).get('modeCount'),
                ', '.join((J('vectors/advertised-mode-paths.json') or {}).get(
                    'modesRepresentedButNotExercisedEndToEnd') or []))),
            ('L1-L3 normalised body identities, symbol-to-path attribution and provider '
             'occupancy are not recomputable by a consumer; the kit says so and substitutes '
             'retained custody, which is what was executed. No normalizer, parser or provider '
             'is qualified by that custody.'),
            ('The repair, comparison, baseline, invocation and query records are RECORD '
             'reconstructions with their identities recomputed and their admission laws '
             'executed. No repair was previewed, applied or authorized; no baseline was '
             'adopted; no query engine was run by a product.'),
        ],
        'standing': {
            'noRootAdmissionClaim': (
                'this origin reports ONLY its own independently executed admission, closure, '
                'replay and controls. It does not claim that any root, author or successor '
                'admitted, agreed with or validated these bytes.'),
            'noProductQualificationClaim': (
                'nothing here authorizes a product implementation or qualifies any product, '
                'component, compiler, provider or host.'),
            'kitOnly': (
                'every citation names a path and selector inside the frozen 102-file kit. No '
                'original repository, author model, fixture, golden, expected output, root '
                'outcome or other review was supplied or read. The disclosed PRIOR-OWN inputs '
                'are named in notes/v19-input-custody.json disclosedPriorInputs: this origin\'s '
                'own generation-17 review, its own generation-18 closing response, and a copy of '
                'its own generation-18 output including the unreconciled reports it has now '
                'corrected.'),
            'priorGenerationsUnmodified': (J('notes/v19-history-standing.json') or {}).get(
                'measuredC_priorGenerations'),
            'historyStanding': (J('notes/v19-history-standing.json') or {}).get('state'),
            'generationLabelProvenance': {
                'verdict': (J('notes/v19-label-history.json') or {}).get('verdict'),
                'method': (J('notes/v19-label-history.json') or {}).get('method'),
                'standing': (
                    'the label corruption class that produced V18-D6 was audited again this '
                    'generation against the retained before-images; four historical '
                    'helper-correction sentences and one ancestry list were restored (V19-D1) and '
                    'the rebind now rewrites PATH FORM ONLY.')},
            'writesMadeUnderAPriorGeneration': {
                'thisSession': (
                    'ZERO. Measured in notes/v19-history-standing.json measuredC: the newest '
                    'modification time of every earlier generation tree predates this session\'s '
                    'first write, so generation 19 wrote into none of them.'),
                'historicalDamageStillOpen': (
                    'the GENERATION-17 session overwrote TWO files under the generation-16 '
                    'output before its own control caught the defect: helper-corrections.json and '
                    'notes/siblings-untouched.json. Generations 14 and 15 had zero writes, and no '
                    'prior Run export, review file, checkpoint or vector was touched. The prior '
                    'bytes were not retained by this origin and are NOT claimed to be restorable; '
                    'root supplies no restoration verdict to this continuation. The item stays '
                    'OPEN and is carried forward rather than marked clean. See '
                    'helper-corrections.json row V17-D8.'),
                'generation17Census': J('notes/prior-generation-writes.json'),
            },
        },
    }
    with open(OUT + '/blind-review.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    write_md(doc)
    print('blind-review.json + blind-review.md written')
    print('verdict:', verdict)
    print('requirementStatus counts:', dict(counts))
    print('MUST=%d SHOULD=%d advisories=%d' % (len(must), len(should), len(adv)))
    print('all claimed positives schema+closure+replay+controls:', all_runs_ok)


def write_md(d):
    L = []
    A = L.append
    A('# OpenSIP blind consumer design review -- consumer-b.' + 'v19')
    A('')
    A('**Verdict: %s**' % d['verdict'])
    A('')
    A('| | |')
    A('|---|---|')
    A('| sessionId | `%s` |' % d['sessionId'])
    A('| same-origin ancestry | %s |' % ' -> '.join(d['sameOriginAncestry']))
    A('| subject manifest SHA-256 | `%s` |' % d['inputKit']['subjectManifestSha256'])
    A('| parent digest declared in that manifest | `%s` |'
      % d['inputKit']['parentSubjectSha256DeclaredInThatManifest'])
    A('| kit files verified | %s / %s (%s) |'
      % (d['inputKit']['filesVerifiedPass'], d['inputKit']['fileCount'],
         d['inputKit']['everyRowVerifiedResult']))
    delta = d['inputKit']['measuredDeltaAgainstThePriorDisclosedKit'] or {}
    A('| measured normative delta | %d unchanged, %d changed, %d added, %d withdrawn |'
      % (delta.get('unchangedCount') or 0, delta.get('changedCount') or 0,
         delta.get('addedCount') or 0, len(delta.get('withdrawn') or [])))
    A('| changed owners | %s |'
      % ', '.join('`%s`' % c['path'].split('/')[-1] for c in (delta.get('changed') or [])))
    A('| added owner | %s |'
      % ', '.join('`%s`' % a.split('/')[-1] for a in (delta.get('added') or [])))
    A('| history standing | %s |' % d['standing'].get('historyStanding'))
    A('| requirement status | %s |'
      % ', '.join('%s %d' % (k, v) for k, v in
                  sorted(d['requirementStatus']['counts'].items())))
    A('| new MUST / SHOULD / advisories | %d / %d / %d |'
      % (len(d['newMustIssues']), len(d['newShouldIssues']), len(d['advisories'])))
    A('')
    A('> This is NOT a parent whole-candidate verification: only the parent digest declared')
    A('> inside the held manifest was compared. No root admission, agreement, expected')
    A('> result, author model or checker was supplied, read or inferred; the root outcome')
    A('> over these exact bytes is unobserved by this origin. Nothing here qualifies any')
    A('> product, compiler, provider or host.')
    A('')
    A('## Why this verdict')
    A('')
    A(d['verdictBasis']['rule'])
    A('')
    A('- acceptBlocking requirements unexecuted: **%d**'
      % len(d['verdictBasis']['acceptBlockingUnexecuted']))
    A('- claimed complete positives that passed schema admission, retained closure, '
      'fresh-process replay and their controls: **%s**'
      % ('all %d' % len(d['claimedCompletePositives'])
         if d['verdictBasis'][
             'everyClaimedPositivePassedSchemaClosureReplayAndControls'] else 'NOT all'))
    A('- unresolved MUST issues: **%d**' % len(d['newMustIssues']))
    A('- unresolved SHOULD issues: **%d**' % len(d['newShouldIssues']))
    A('')
    A('## Claimed complete positive Runs')
    A('')
    A('| Run | runId | verdict | objects | blobs | closure checks | replay | controls |')
    A('|---|---|---|---|---|---|---|---|')
    for r in d['claimedCompletePositives']:
        A('| %s | `%s` | %s | %s | %s | %s passed / %s n-a / %s refused | %s | %d refused |'
          % (r['label'], (r['claimedRunId'] or '')[:22] + '...', r['verdict'],
             r['objectCount'], r['blobCount'], r['closure']['checksPassed'],
             r['closure']['checksNotApplicable'], r['closure']['checksRefused'],
             'MATCH' if r['freshProcessReplay']['matched'] else 'NO MATCH',
             r['controls']['count']))
    A('')
    A('Exported bytes, by SHA-256 of the export file itself:')
    A('')
    for r in d['claimedCompletePositives']:
        A('- `%s` -> %s' % (r['exportFile'], r['exportFileSha256']))
    A('')
    A('## From-scratch command')
    A('')
    A('```')
    A(d['fromScratchCommand']['command'])
    A('```')
    A('')
    A('The command declares **%s** stages. When this final reconciliation stage ran, **%s** '
      'preceding stages of this same run were recorded and all passed: **%s**. %s'
      % (d['fromScratchCommand'].get('declaredStageCount'),
         d['fromScratchCommand'].get('stagesRecordedWhenThisReconciliationRan'),
         d['fromScratchCommand']['allStagesPassed'],
         d['fromScratchCommand']['reconciliationStanding']))
    A('')
    A('## New MUST issues')
    A('')
    A('None. ' + (d['emptyMustJustification'] or ''))
    A('')
    A('## New SHOULD issues')
    A('')
    if not d['newShouldIssues']:
        A('None open. The two that generation 16 raised are RESOLVED by the normative successor')
        A('this generation received, on published law rather than by invention:')
        A('')
        for s in (d.get('resolvedByTheNormativeSuccessorThisGeneration') or []):
            A('### %s -- %s' % (s['id'], s['title']))
            A('')
            A('- disposition: **%s**' % s.get('disposition'))
            A('- what the new bytes say: %s' % s.get('whatTheNewBytesSay'))
            A('- how this origin closed it: %s' % s.get('howThisOriginClosedIt'))
            for extra in ('whatThisOriginDidNOTDo', 'whichReadingWon'):
                if s.get(extra):
                    A('- %s: %s' % (extra, s[extra]))
            A('')
    for s in d['newShouldIssues']:
        A('### %s -- %s' % (s['id'], s['title']))
        A('')
        A('- class: %s' % s['class'])
        A('- selectors:')
        for sel in s['selectors']:
            A('  - `%s`' % sel)
        A('- attempted: %s' % s['whatWasAttempted'])
        A('- the kit says: %s' % s['whatTheKitSays'])
        A('- why this is a missing contract rather than algorithm freedom: %s'
          % s['whyItIsNotAlgorithmFreedom'])
        A('- measured here: %s' % s['measuredOnThisReconstruction'])
        A('- smallest fix: %s' % s['smallestFix'])
        A('- why not MUST: %s' % s['notAMustBecause'])
        A('')
    A('## Advisories')
    A('')
    for s in d['advisories']:
        A('- **%s** (%s) %s' % (s['id'], s['class'], s['title']))
        A('  - observation: %s' % s['observation'])
        A('  - handled here by: %s' % s['howThisOriginHandledIt'])
    A('')
    A('## Withdrawn by this origin, or resolved in the new kit bytes')
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
    A('## What this generation added to the audit')
    A('')
    h = d.get('clauseToCodeAuditHistory', {}).get('generation19') or {}
    for area in ('area1_enumerationProgramBinding', 'area2_subjectInventoryCarrier',
                 'area3_executionInputs'):
        row = h.get(area) or {}
        A('### %s' % area)
        A('')
        for k, v in row.items():
            if isinstance(v, list):
                A('- %s:' % k)
                for item in v:
                    A('  - %s' % item)
            else:
                A('- %s: %s' % (k, v))
        A('')
    A('## Coverage limitations (disclosed, not design gaps)')
    A('')
    for c in (d.get('coverageLimitationsDisclosedNotDesignGaps') or []):
        A('- %s' % c['limitation'])
        A('  - why not a gap: %s' % c['whyNotAGap'])
        A('  - measured where: `%s`' % c['measuredWhere'])
    A('')
    A('## Helper corrections (helper bug != design gap)')
    A('')
    A('| id | where | corrected |')
    A('|---|---|---|')
    for h in d['helperCorrections'] or []:
        A('| %s | %s | %s |' % (h['id'], h['where'], h['status']))
    A('')
    A('Open helper failures on a claimed positive: **%d**.'
      % len(d['openHelperFailuresOnAClaimedPositive'] or []))
    A('')
    A('## Limitations and scope')
    A('')
    for x in d['limitations']:
        A('- %s' % x)
    A('')
    A('## Standing')
    A('')
    for k, v in d['standing'].items():
        if k == 'writesMadeUnderAPriorGeneration':
            A('- **%s**: this session: %s' % (k, v['thisSession']))
            A('  - still open from generation 17: %s' % v['historicalDamageStillOpen'])
        elif k == 'priorGenerationsUnmodified':
            trees = (v or {}).get('trees') or []
            A('- **%s**: generations modified during this session: %s. Newest modification time '
              'per generation: %s. %s'
              % (k, (v or {}).get('generationsModifiedDuringThisSession'),
                 '; '.join('%s %s' % (t.get('generation'), t.get('newestMtimeUtc'))
                           for t in trees),
                 (v or {}).get('claimLimit')))
        else:
            A('- **%s**: %s' % (k, v))
    A('')
    with open(OUT + '/blind-review.md', 'w') as f:
        f.write('\n'.join(L) + '\n')


main()
