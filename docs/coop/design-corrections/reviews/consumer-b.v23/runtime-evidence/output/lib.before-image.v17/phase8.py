"""Phase 8 -- baseline audit and comparison, reconstructed from the REAL sealed TypeScript Run
as the current side and an independently constructed baseline of the same project.

  R-BASELINE-AUDIT        a BaselineArtifact + ComparisonResult pair, both schema-admitted,
                          with baselineId = H('workflow.baseline', descriptor) and
                          comparisonResultId = H('workflow.comparison', descriptor).
  R-CMP-MISSING           missing-evidence comparison case.
  R-CMP-EVIDENCE-CHANGED  evidence-changed comparison case (the evidence axis compares import
                          IDENTITIES, not kind presence).
  R-CMP-EMPTY-RESULT      empty-result comparison case: zero entries is NOT the same as a
                          comparison that was not performed.
  R-SCOPE-POLICY-ONLY-COMPARISON  only the bound ScopeDocumentV1 changes.
  R-E0-VS-E1-E3           E0 (a prior detector EXECUTION) versus E1..E3 (re-evaluation of
                          current retained evidence).
  R-PIVOT-ONLY-FINGERPRINTS  fingerprints present only at a pivot are retained as such.
  R-HOST-CAPTURED-VS-CANDIDATE  host-captured required work versus candidate-only returns.
  R-EMPTY-PARTIAL-UNAVAILABLE-MISSING  the four states measured side by side.
  R-DETECTOR-COMPAT-FILE  the reserved authenticated listing file versus the component
                          manifest body.
  R-TEST-PREP-REPAIR-AUTH authorization records for test, preparation and repair.
  R-PURGE-REPLAY-OUTPUT-FAILURE  purge/replay and required-output failure envelopes.
  R-SUBSYSTEM-OWNERS      which subsystem owns every decision above.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_store as ST
import opensip_closure as CL
import envelopes as EV

OUT = '/tmp/opensip-design-corrections/consumer-b.v17/output'
KIT = S.KIT
BASE_DOC = 'workflows/schemas/evaluator3/baseline-artifact.schema.json'
CMP_DOC = 'workflows/schemas/evaluator3/comparison-result.schema.json'
REQ = 'req1_9c4f70ab23d8416eb5207fd1ac36e8b9'

AUDIT_PROFILES = {
    'code-regression': {'name': 'code-regression', 'gateCodeNetNew': True,
                        'gateNewlyLiveByPolicyAxes': False, 'gateAllCurrentLive': False,
                        'newWaiverSuppressesCodeNetNew': False,
                        'gateRuleUnder': 'baseline-or-current'},
    'policy-change': {'name': 'policy-change', 'gateCodeNetNew': True,
                      'gateNewlyLiveByPolicyAxes': True, 'gateAllCurrentLive': False,
                      'newWaiverSuppressesCodeNetNew': False,
                      'gateRuleUnder': 'baseline-or-current'},
    'report-only': {'name': 'report-only', 'gateCodeNetNew': False,
                    'gateNewlyLiveByPolicyAxes': False, 'gateAllCurrentLive': False,
                    'newWaiverSuppressesCodeNetNew': False,
                    'gateRuleUnder': 'current-only'},
}
ZERO_COUNTS = {k: 0 for k in ('UNCHANGED', 'CODE-NET-NEW', 'CODE-FIXED', 'DETECTION-DELTA',
                              'POLICY-DELTA', 'SCOPE-DELTA', 'WAIVER-DELTA',
                              'EVIDENCE-DELTA', 'INDETERMINATE', 'gating')}


def current_side():
    st, doc = ST.Store.load(OUT + '/runs/typescript.store.json')
    c = CL.Closure(st)
    rid = [t for t in st.objects if t.startswith('run3:')][0]
    rep = c.close_run(rid, 'phase8')
    assert rep['admitted'], rep['refusals'][:2]
    run = c.resolved[rid]
    plan = c.plan
    proof = None
    for t, r in st.objects.items():
        if t.startswith('proof3:'):
            proof = r
    # the policy, waiver and scope DOCUMENTS are retained as labelled BLOBS under their raw
    # SHA-256 (that is their published identity recipe), not as typed graph objects
    def blob_rec(label):
        d = st.labels.get(label)
        if d is None:
            return None, None
        by = st.get_blob(d)
        return json.loads(by.decode()), d

    policy, policy_dig = blob_rec('policy')
    waivers, waiver_dig = blob_rec('waivers')
    scope, scope_dig = blob_rec('scope-document')
    fps, findings = [], []
    for t, r in sorted(st.objects.items()):
        if t.startswith('finding-key2:'):
            fps.append(t)
        if t.startswith('finding3:'):
            findings.append((t, r))
    imports = [(t, r) for t, r in sorted(st.objects.items()) if t.startswith('import2:')]
    detector = None
    for t, r in st.objects.items():
        if isinstance(r, dict) and r.get('kind') == 'detector':
            detector = (t, r)
    return {'store': st, 'closure': c, 'runId': rid, 'run': run, 'plan': plan,
            'proof': proof, 'policy': policy, 'scope': scope, 'waivers': waivers,
            'policyDigest': policy_dig, 'waiverDigest': waiver_dig,
            'scopeDocumentDigest': scope_dig,
            'fingerprints': fps, 'findings': findings, 'imports': imports,
            'detector': detector, 'projectId': run['projectId'],
            'snapshotId': run['snapshotId'], 'planId': run['planId']}


def evidence_availability(cur, *, drop_imports=False, change_payload=False):
    rows = []
    for tid, w in cur['imports']:
        if drop_imports:
            continue
        pd = w['payloadDigest']
        if change_payload:
            pd = K.raw_sha256(b'a different runtime payload with the same kind')
        rows.append({'kind': w['kind'], 'importId': tid, 'payloadDigest': pd,
                     'sourceCorrespondenceDigest': w['sourceCorrespondenceDigest'],
                     'scopeDigest': w.get('scopeDigest') or K.raw_sha256(b'import-scope'),
                     'observationDigest': (w.get('observationDigest')
                                           or K.raw_sha256(b'observation'))})
    return {'importKinds': sorted({r['kind'] for r in rows}),
            'relations': sorted({'runtime-observation'}) if rows else [],
            'imports': sorted(rows, key=lambda r: r['importId'].encode())}


def context(cur, *, scope_digest=None, policy_digest=None, avail=None):
    # all three are RAW SHA-256 of the canonical document bytes, and all three are the exact
    # digests the retained Plan and the retained blob store already carry
    return {'policyDigest': policy_digest or cur['policyDigest'],
            'scopeDigest': scope_digest or cur['scopeDocumentDigest'],
            'waiverSetDigest': cur['waiverDigest'],
            'detectorClosureIds': [cur['detector'][0]] if cur['detector'] else [],
            'evidenceAvailability': avail if avail is not None
            else evidence_availability(cur)}


def baseline(cur, *, entries=None, avail=None, scope_digest=None):
    det_tid, det = cur['detector']
    desc = {
        'schemaFamily': 'opensip.product.baseline', 'schemaMajor': 2,
        'originProjectId': cur['projectId'],
        'source': {'snapshotId': cur['snapshotId']},
        'runId': cur['runId'], 'planId': cur['planId'],
        'fingerprintRecipe': {'domain': 'finding-fingerprint', 'recipeMajor': 2},
        'detectorClosure': [{'detectorId': 'detector.ts-hygiene', 'closureId': det_tid,
                             'semanticsMajor': 2,
                             'semanticVersion': det['semanticVersion'],
                             'contributionId': 'contrib.clone-hygiene',
                             'manifestDigest': det['manifestDigest']}],
        'pivotClosure': sorted([
            {'closureId': det_tid, 'kind': 'detector',
             'manifestDigest': det['manifestDigest'],
             'protocolMajor': det['protocolMajor'], 'platform': det['platform']}],
            key=lambda r: r['closureId'].encode()),
        'context': context(cur, avail=avail, scope_digest=scope_digest),
        'contextDocuments': {'policy': cur['policy'],
                             'scope': cur['scope'] or {'schemaVersion': 1, 'include': [],
                                                       'exclude': []},
                             'waivers': cur['waivers']},
        'ruleCoverage': sorted([
            {'ruleId': r['ruleId'], 'requiredCoverage': 'satisfied',
             'enabled': r['enabled'],
             'gating': bool(r['gate']), 'evidenceUse': r['evidenceUse']}
            for r in cur['policy']['rules']], key=lambda r: r['ruleId'].encode()),
        'entries': entries if entries is not None else baseline_entries(cur),
        'unmatchedOccurrences': [],
    }
    art = {'baselineId': K.ID('workflow.baseline', desc), 'descriptor': desc,
           'custody': {'exportedByHostRelease': '3.0.0',
                       'exportedAtUtc': '2026-09-12T00:00:00Z',
                       'runRetainedAtExport': True,
                       'retentionPins': sorted([cur['runId'], det_tid])}}
    return art


def baseline_entries(cur, *, drop=0):
    """Entries are keyed by the FINGERPRINT the Run already minted (finding-key2), and the
    subject PATH is read from that fingerprint's own subjectKey -- not invented, and not taken
    from the finding record, which carries an opaque subject3 instead."""
    # the POLICY ruleId that owns each finding is read from the proof's ruleResults, which is
    # the record that binds them; the fingerprint carries the rule STABLE id, a different name
    rule_of = {}
    for rr in (cur['proof'] or {}).get('ruleResults', []):
        for fid in rr.get('findingIds', []):
            rule_of[fid] = rr['ruleId']
    rows = []
    for tid, f in cur['findings']:
        fp = f['fingerprint']
        key = cur['store'].objects.get(fp) or {}
        sk = key.get('subjectKey') or {}
        rows.append({'fingerprint': fp,
                     'ruleId': rule_of.get(tid, 'unknown'),
                     'detectorId': 'detector.ts-hygiene',
                     'stabilityClass': 'path-stable',
                     'subjectPath': sk.get('logicalPath') or 'src/index.ts',
                     'waived': False})
    rows = sorted({r['fingerprint']: r for r in rows}.values(),
                  key=lambda r: r['fingerprint'].encode())
    return rows[:len(rows) - drop] if drop else rows


def comparison(cur, bl, *, profile='code-regression', performed=True,
               entries=None, counts=None, verdict='pass', rule_def=None,
               corr=None, baseline_ctx=None, current_ctx=None, delta=None,
               pivots=None, detectors=None, whole_reason=None, remedy=None,
               unmatched=None, state='evaluated'):
    desc = {
        'schemaFamily': 'opensip.product.comparison', 'schemaMajor': 2,
        'baselineId': bl['baselineId'], 'currentRunId': cur['runId'],
        'currentSnapshotId': cur['snapshotId'],
        'auditProfile': AUDIT_PROFILES[profile],
        'projectCorrespondence': 'same-project',
        'comparisonPerformed': performed,
        'baselineContext': baseline_ctx or bl['descriptor']['context'],
        'currentContext': current_ctx or bl['descriptor']['context'],
        'contextDelta': delta or {'codeChanged': False, 'detectorChanged': False,
                                  'policyChanged': False, 'scopeChanged': False,
                                  'waiversChanged': False,
                                  'evidenceAvailabilityChanged': False},
        'pivotsAvailable': pivots or {'E0': 'not-needed', 'E1': 'not-needed',
                                      'E2': 'not-needed', 'E3': 'not-needed'},
        'detectors': detectors if detectors is not None else [
            {'detectorId': 'detector.ts-hygiene',
             'baselineClosureId': cur['detector'][0],
             'currentClosureId': cur['detector'][0],
             'baselineSemanticsMajor': 2, 'currentSemanticsMajor': 2,
             'method': 'identical-closure'}],
        'ruleDeficiencies': rule_def or [],
        'entries': entries if entries is not None else [],
        'counts': counts or dict(ZERO_COUNTS),
        'verdict': verdict,
        'unmatchedOccurrences': unmatched or [],
        'correspondenceCoverage': corr if corr is not None else [],
        'currentEvaluationState': state,
        'currentExecutionDeficiencies': [],
    }
    if not performed:
        desc['wholeIndeterminateReason'] = whole_reason
        desc['remedy'] = remedy
    return {'comparisonResultId': K.ID('workflow.comparison', desc), 'descriptor': desc}


def admit(doc, selector, inst, label, *, identity_field=None, identity_domain=None):
    ok, err = True, None
    try:
        res = S.admit(doc, selector, inst, label)
        if not res['admitted']:
            ok, err = False, {'stock': res['stockSchemaErrors'][:4],
                              'keywords': res['publishedKeywordRefusals'][:4]}
    except Exception as e:
        ok, err = False, '%s: %s' % (type(e).__name__, str(e)[:400])
    idok = None
    if identity_field:
        idok = inst[identity_field] == K.ID(identity_domain, inst['descriptor'])
    return {'label': label, 'owningSchemaAdmitted': ok, 'owningSchemaError': err,
            'identityRecomputed': idok,
            'admitted': ok and (idok is not False)}


def main():
    cur = current_side()
    rows = []
    out = {'consumerId': 'consumer-b.v17',
           'standing': ('the CURRENT side is the real sealed TypeScript Run of this origin; '
                        'the baseline is an independently constructed artifact over the same '
                        'Run. No product executed any comparison: these are record '
                        'reconstructions plus the identity and admission laws.')}

    # ------------------------------------------------------- R-BASELINE-AUDIT
    bl = baseline(cur)
    r = admit(BASE_DOC, '#', bl, 'baseline-artifact', identity_field='baselineId',
              identity_domain='workflow.baseline')
    r['requirement'] = 'R-BASELINE-AUDIT'
    r['entryCount'] = len(bl['descriptor']['entries'])
    r['custodyIsNotIdentity'] = (
        'exportedAtUtc and exportedByHostRelease live in the custody envelope, OUTSIDE the '
        'descriptor, so they never enter baselineId. Recomputing H over the descriptor alone '
        'is what proves it.')
    rows.append(r)
    unchanged = [
        {'fingerprint': e['fingerprint'], 'ruleId': e['ruleId'],
         'detectorId': e['detectorId'],
         'presence': {'B': True, 'E0': None, 'E1': None, 'E2': None, 'E3': None,
                      'E4': True, 'waivedB': False, 'waivedC': False},
         'classification': 'UNCHANGED', 'subsequentDeltas': [], 'liveInCurrent': True,
         'gates': False}
        for e in bl['descriptor']['entries']]
    counts = dict(ZERO_COUNTS, UNCHANGED=len(unchanged))
    corr = sorted([
        {'ruleId': rc['ruleId'], 'gating': rc['gating'],
         'matchedCount': sum(1 for e in unchanged if e['ruleId'] == rc['ruleId']),
         'unmatchedCount': 0, 'populationUnknown': False,
         'zeroFindings': not any(e['ruleId'] == rc['ruleId'] for e in unchanged)}
        for rc in bl['descriptor']['ruleCoverage']], key=lambda r: r['ruleId'].encode())
    cmp_ok = comparison(cur, bl, entries=unchanged, counts=counts, corr=corr)
    r = admit(CMP_DOC, '#', cmp_ok, 'comparison-unchanged',
              identity_field='comparisonResultId', identity_domain='workflow.comparison')
    r['requirement'] = 'R-BASELINE-AUDIT'
    r['classification'] = 'valid'
    r['gateSemantics'] = AUDIT_PROFILES['code-regression']
    rows.append(r)

    # ------------------------------------------------------- R-CMP-MISSING
    miss = comparison(
        cur, bl, performed=False, verdict='indeterminate',
        whole_reason='baseline-context-document-missing',
        remedy={'code': 'evidence.missing',
                'remedy': 're-export the baseline with its context documents; a comparison '
                          'is NOT performed against a baseline whose context cannot be read'},
        rule_def=[{'ruleId': 'rule.declares-advisory', 'gating': False,
                   'cause': 'required-coverage-unknown'}])
    r = admit(CMP_DOC, '#', miss, 'comparison-missing-evidence',
              identity_field='comparisonResultId', identity_domain='workflow.comparison')
    r['requirement'] = 'R-CMP-MISSING'
    r['classification'] = 'valid'
    r['notPerformedIsNotEmpty'] = (
        'comparisonPerformed=false FORCES verdict=indeterminate, zero entries, zero '
        'unmatched occurrences, zero correspondence coverage AND a whole-reason plus remedy. '
        'An empty PERFORMED comparison carries none of those, which is how the two are '
        'distinguished by the schema rather than by a label.')
    rows.append(r)

    # ------------------------------------------------------- R-CMP-EVIDENCE-CHANGED
    changed = evidence_availability(cur, change_payload=True)
    # every non-UNCHANGED classification REQUIRES a direction: the axis alone does not say
    # whether the finding appeared or vanished, and the schema refuses to let it be implied
    ev_entries = [dict(e, classification='EVIDENCE-DELTA',
                       subsequentDeltas=['evidence'], direction='appeared')
                  for e in unchanged[:1]]
    ev = comparison(
        cur, bl, entries=ev_entries,
        counts=dict(ZERO_COUNTS, **{'EVIDENCE-DELTA': len(ev_entries)}),
        current_ctx=context(cur, avail=changed),
        delta={'codeChanged': False, 'detectorChanged': False, 'policyChanged': False,
               'scopeChanged': False, 'waiversChanged': False,
               'evidenceAvailabilityChanged': True},
        corr=corr, verdict='pass')
    r = admit(CMP_DOC, '#', ev, 'comparison-evidence-changed',
              identity_field='comparisonResultId', identity_domain='workflow.comparison')
    r['requirement'] = 'R-CMP-EVIDENCE-CHANGED'
    r['classification'] = 'valid'
    r['axisComparesIdentitiesNotKindPresence'] = {
        'baselineImportIds': [i['importId'] for i in
                              bl['descriptor']['context']['evidenceAvailability']['imports']],
        'currentImportIds': [i['importId'] for i in changed['imports']],
        'sameImportKinds': (bl['descriptor']['context']['evidenceAvailability']
                            ['importKinds'] == changed['importKinds']),
        'payloadDigestsDiffer': True,
        'law': ('"imports lists the exact import2 identities ... so that the evidence axis '
                'compares identities, not kind presence: the same kind with different '
                'payload/correspondence/scope/window is a changed axis."')}
    rows.append(r)

    # ------------------------------------------------------- R-CMP-EMPTY-RESULT
    empty_corr = sorted([
        {'ruleId': rc['ruleId'], 'gating': rc['gating'], 'matchedCount': 0,
         'unmatchedCount': 0, 'populationUnknown': False, 'zeroFindings': True}
        for rc in bl['descriptor']['ruleCoverage']], key=lambda r: r['ruleId'].encode())
    empty_bl = baseline(cur, entries=[])
    emp = comparison(cur, empty_bl, entries=[], counts=dict(ZERO_COUNTS),
                     corr=empty_corr, verdict='pass')
    r = admit(CMP_DOC, '#', emp, 'comparison-empty-result',
              identity_field='comparisonResultId', identity_domain='workflow.comparison')
    r['requirement'] = 'R-CMP-EMPTY-RESULT'
    r['classification'] = 'valid'
    r['emptyIsPerformedAndComplete'] = {
        'comparisonPerformed': True, 'entries': 0, 'verdict': 'pass',
        'zeroFindingRulesAccountedFor': len(empty_corr),
        'why': ('every rule appears in correspondenceCoverage with zeroFindings=true and '
                'populationUnknown=false, so the empty result is a MEASURED empty rather '
                'than an unknown population presented as empty')}
    rows.append(r)

    # ------------------------------------------------------- R-SCOPE-POLICY-ONLY-COMPARISON
    new_scope_digest = K.raw_sha256(b'{"schemaVersion":1,"include":["src/**/*"],'
                                   b'"exclude":["src/legacy.js"]}')
    sc_entries = [dict(e, classification='SCOPE-DELTA', subsequentDeltas=['scope'],
                       direction='vanished', liveInCurrent=False, gates=False)
                  for e in unchanged[:1]]
    sc = comparison(
        cur, bl, profile='policy-change', entries=sc_entries,
        counts=dict(ZERO_COUNTS, **{'SCOPE-DELTA': len(sc_entries)}),
        current_ctx=context(cur, scope_digest=new_scope_digest),
        delta={'codeChanged': False, 'detectorChanged': False, 'policyChanged': False,
               'scopeChanged': True, 'waiversChanged': False,
               'evidenceAvailabilityChanged': False},
        corr=corr, verdict='pass')
    r = admit(CMP_DOC, '#', sc, 'comparison-scope-policy-only',
              identity_field='comparisonResultId', identity_domain='workflow.comparison')
    r['requirement'] = 'R-SCOPE-POLICY-ONLY-COMPARISON'
    r['classification'] = 'valid'
    r['onlyTheBoundScopeDocumentChanged'] = {
        'baselineScopeDigest': bl['descriptor']['context']['scopeDigest'],
        'currentScopeDigest': new_scope_digest,
        'snapshotIdUnchanged': True,
        'policyDigestUnchanged': True,
        'distinctFromSourceOrDiscoveryScope': (
            'EvaluationContext.scopeDigest is the WORKFLOW glob ScopeDocumentV1 bound as an '
            'analysis-spec parameter. It is explicitly NOT plan.scopeDigest, which is the '
            'foundation scope-descriptor that decides which SOURCE was discovered. Changing '
            'the policy scope re-selects subjects within the SAME snapshot, so the axis is '
            'SCOPE-DELTA and the code axis is untouched.'),
        'plannedScopeDescriptorDigest': cur['plan'].get('scopeDigest')}
    rows.append(r)

    # ------------------------------------------------------- R-E0-VS-E1-E3
    e0e3 = {
        'requirement': 'R-E0-VS-E1-E3', 'classification': 'explanatory+measured',
        'law': (S.doc_path(CMP_DOC) + '#/$defs/PivotPresence + pivotsAvailable + '
                'DetectorDisposition.method'),
        'pivots': {
            'B': {'what': 'the BASELINE side as adopted: the fingerprints the baseline '
                          'artifact actually retains',
                  'isAnExecution': 'no -- it is a retained artifact'},
            'E0': {'what': 'a PRIOR DETECTOR EXECUTION: the baseline detector closure run '
                           'again, which needs that closure to be retained, spawnable and '
                           'deterministic',
                   'isAnExecution': 'YES',
                   'unavailableWhen': ['pivot-detector-unavailable', 'pivot-closure-revoked',
                                       'pivot-closure-incompatible',
                                       'pivot-run-not-committed',
                                       'pivot-detector-nondeterministic'],
                   'method': 'three-way-pivot'},
            'E1': {'what': 'RE-EVALUATION of the CURRENT retained evidence under the '
                           'baseline policy', 'isAnExecution': 'no -- no detector runs'},
            'E2': {'what': 'RE-EVALUATION of the current retained evidence under the '
                           'baseline scope', 'isAnExecution': 'no'},
            'E3': {'what': 'RE-EVALUATION of the current retained evidence under the '
                           'baseline waivers', 'isAnExecution': 'no'},
            'E4': {'what': 'the CURRENT side as evaluated', 'isAnExecution': 'no'},
        },
        'whyTheDistinctionMatters': (
            'E0 can be UNAVAILABLE for custody or determinism reasons that have nothing to '
            'do with the evidence, and its unavailability is a pivot reason, not a finding. '
            'E1-E3 need no closure at all: they re-evaluate bytes this origin already '
            'retains, so they are available whenever the current Run is. Treating E0 as '
            'just another re-evaluation would let a missing detector closure be reported as '
            'a code difference.'),
        'measuredOnThisReconstruction': {
            'detectorMethodWhenClosuresAreIdentical': 'identical-closure -- no pivot needed, '
                                                      'so every pivot is `not-needed`',
            'pivotsAvailableInTheUnchangedComparison':
                cmp_ok['descriptor']['pivotsAvailable'],
            'presenceShapeIsNullableForE0toE3':
                'null means the pivot was not available; false means it was available and '
                'the fingerprint was absent. Collapsing null into false would invent a '
                'CODE-FIXED.',
        },
    }

    # ------------------------------------------------------- R-PIVOT-ONLY-FINGERPRINTS
    pivot_only_fp = 'finding-key2:' + K.raw_sha256(b'a fingerprint only E0 produced')
    po_entry = {
        'fingerprint': pivot_only_fp, 'ruleId': 'rule.no-duplicate-body',
        'detectorId': 'detector.ts-hygiene',
        'presence': {'B': False, 'E0': True, 'E1': False, 'E2': False, 'E3': False,
                     'E4': False, 'waivedB': False, 'waivedC': False},
        'classification': 'DETECTION-DELTA', 'direction': 'vanished',
        'subsequentDeltas': ['detection'],
        'liveInCurrent': False, 'gates': False}
    po = comparison(
        cur, bl, entries=sorted(unchanged + [po_entry],
                                key=lambda e: e['fingerprint'].encode()),
        counts=dict(ZERO_COUNTS, UNCHANGED=len(unchanged),
                    **{'DETECTION-DELTA': 1}),
        pivots={'E0': 'available', 'E1': 'not-needed', 'E2': 'not-needed',
                'E3': 'not-needed'},
        detectors=[{'detectorId': 'detector.ts-hygiene',
                    'baselineClosureId': cur['detector'][0],
                    'currentClosureId': cur['detector'][0],
                    'baselineSemanticsMajor': 1, 'currentSemanticsMajor': 2,
                    'method': 'three-way-pivot', 'pivotRunId': cur['runId']}],
        delta={'codeChanged': False, 'detectorChanged': True, 'policyChanged': False,
               'scopeChanged': False, 'waiversChanged': False,
               'evidenceAvailabilityChanged': False},
        corr=corr, verdict='pass')
    r = admit(CMP_DOC, '#', po, 'comparison-pivot-only-fingerprint',
              identity_field='comparisonResultId', identity_domain='workflow.comparison')
    r['requirement'] = 'R-PIVOT-ONLY-FINGERPRINTS'
    r['classification'] = 'valid'
    r['pivotOnlyFingerprintRetained'] = {
        'fingerprint': pivot_only_fp,
        'presence': po_entry['presence'],
        'inBaseline': False, 'inCurrent': False, 'atE0': True,
        'classification': 'DETECTION-DELTA',
        'why': ('a fingerprint that exists ONLY at a pivot is retained as a pivot presence '
                'and classified on the DETECTION axis. It is neither CODE-NET-NEW (it is not '
                'live in current) nor CODE-FIXED (it was never in the baseline); dropping it '
                'would hide the detector change that produced it.'),
        'liveInCurrent': False, 'gates': False}
    rows.append(r)

    # ------------------------------------------------- R-HOST-CAPTURED-VS-CANDIDATE
    hc = {
        'requirement': 'R-HOST-CAPTURED-VS-CANDIDATE', 'classification': 'measured',
        'hostCapturedRequiredWork': {
            'meaning': ('work the HOST performed and captured itself, so the retained bytes '
                        'are its own observation and the result is required evidence'),
            'examplesInThisReconstruction': [
                {'what': 'the snapshot inventory and every file fact',
                 'artifact': 'runs/*.store.json snapshot2 + fact2 file@enumerated',
                 'required': True},
                {'what': 'the native context / universe of each language Run',
                 'artifact': 'runs/*.closure.json NATIVE_CONTEXT_* and UNIVERSE_* checks',
                 'required': True}],
        },
        'candidateOnlyReturns': {
            'meaning': ('a result the product may RETURN AS A CANDIDATE but must not select '
                        'as a complete result; it carries no required-evidence authority'),
            'examplesInThisReconstruction': [
                {'what': 'the clones capability on a release that declares it candidate-only',
                 'artifact': 'vectors/multi-unit-missing-caps.json '
                             'candidateOnlyIsNotSelected',
                 'required': False},
                {'what': 'an unmapped-only import',
                 'artifact': 'vectors/imported-observation-boundary.json -- unmapped-only '
                             'evidence "may be listed and queried but never feeds a '
                             'predicate"',
                 'required': False}],
        },
        'theErrorThisPrevents': (
            'reporting a candidate-only return as host-captured required work would let an '
            'unselected or unmapped result satisfy a required-coverage obligation.'),
        'measuredJoin': {
            'importsConsumableForAPredicate': [
                i['importId'] for i in
                bl['descriptor']['context']['evidenceAvailability']['imports']],
            'note': ('the one import of the TypeScript Run is snapshot-equal and therefore '
                     'consumable; a candidate-only or unmapped-only import would appear in '
                     'the same array but could not be a predicate input')},
    }

    # ------------------------------------- R-EMPTY-PARTIAL-UNAVAILABLE-MISSING
    four = four_states()

    # ------------------------------------------------- R-DETECTOR-COMPAT-FILE
    compat = detector_compat(cur)

    # ------------------------------------------------- R-TEST-PREP-REPAIR-AUTH
    auth = test_prep_repair_auth(cur)

    # ------------------------------------------------- R-PURGE-REPLAY-OUTPUT-FAILURE
    prf = purge_replay_output(cur)
    rows += prf['envelopes']

    # ------------------------------------------------- R-PUBLIC-TERMINATION-EXAMPLES
    pte = public_termination(cur)
    rows += pte['envelopes']

    # ------------------------------------------------- R-SUBSYSTEM-OWNERS
    owners = subsystem_owners()

    out.update({'controls': rows, 'e0VsE1E3': e0e3, 'hostCapturedVsCandidate': hc,
                'fourStates': four, 'detectorCompatibility': compat,
                'authorizations': auth, 'purgeReplayOutput': prf['summary'],
                'publicTermination': pte['summary'], 'subsystemOwners': owners})
    EV.write('envelopes/public-termination.json',
             {'requirement': 'R-PUBLIC-TERMINATION-EXAMPLES',
              'summary': pte['summary'], 'envelopes': pte['envelopes']})
    EV.write('vectors/baseline-audit.json',
             {'baselineArtifact': bl, 'comparisonUnchanged': cmp_ok,
              'admission': [r for r in rows if r['requirement'] == 'R-BASELINE-AUDIT']})
    EV.write('vectors/comparison-missing.json', miss)
    EV.write('vectors/comparison-evidence-changed.json', ev)
    EV.write('vectors/comparison-empty-result.json', emp)
    EV.write('vectors/comparison-scope-policy-only.json', sc)
    EV.write('vectors/baseline-e0-e3.json', e0e3)
    EV.write('vectors/comparison-pivot-only-fingerprints.json', po)
    EV.write('vectors/host-captured-vs-candidate.json', hc)
    EV.write('vectors/empty-partial-unavailable-missing.json', four)
    EV.write('vectors/detector-compatibility-file.json', compat)
    EV.write('vectors/test-prep-repair-authorization.json', auth)
    EV.write('vectors/phase8-subsystem-owners.json', owners)
    EV.write('vectors/phase8-all.json', out)

    bad = []
    for r in rows:
        print('%-44s %-34s admitted=%-5s identity=%s'
              % (r['label'][:44], str(r['requirement'])[:34], r['admitted'],
                 r.get('identityRecomputed')))
        if not r['admitted']:
            bad.append((r['label'], r['owningSchemaError']))
    print()
    print('four-state rows: %d | detector-compat checks: %d | authorizations: %d'
          % (len(four['states']), len(compat['measured']), len(auth['records'])))
    missing_ex = [s['state'] for s in four['states'] if not s['measuredExample']]
    print('four states with a measured example: %d/%d %s'
          % (len(four['states']) - len(missing_ex), len(four['states']),
             'missing=' + str(missing_ex) if missing_ex else ''))
    assert not missing_ex, missing_ex
    if bad:
        print(json.dumps(bad, indent=1, default=str)[:3000])
    assert not bad, [b[0] for b in bad]


def four_states():
    """R-EMPTY-PARTIAL-UNAVAILABLE-MISSING -- four DISTINCT states, each measured on a real
    retained artifact of this origin. One label for all four is failure."""
    rows = []
    for label in ('syntax-code', 'syntax-data', 'rust-partial'):
        st, doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
        c = CL.Closure(st)
        rid = [t for t in st.objects if t.startswith('run3:')][0]
        c.close_run(rid, 'phase8-four:' + label)
        for cid, cv in sorted(c.coverages_seen.items()):
            sc = c.scopes_seen[cv['scopeId']]
            pay = c.canonical_record(cv['payloadDigest'], B.NATIVE_DOC,
                                     '#/$defs/CoverageResultV3', 'P8')
            e = pay['entry']
            facts = [f for f in c.facts_seen.values()
                     if f['relation'] == sc['relation']
                     and f['resolution'] == sc['resolution']]
            rows.append({'run': label, 'pair': '%s@%s' % (sc['relation'],
                                                          sc['resolution']),
                         'coverage': e['coverage'], 'deficiency': e.get('deficiency'),
                         'nativeCause': e.get('nativeCause'),
                         'factCount': len(facts),
                         'state': ('complete-empty' if e['coverage'] == 'complete'
                                   and not facts else
                                   'complete-nonempty' if e['coverage'] == 'complete'
                                   else 'partial/unknown-with-a-published-cause')})
    return {
        'requirement': 'R-EMPTY-PARTIAL-UNAVAILABLE-MISSING',
        'classification': 'measured',
        'states': [
            {'state': 'complete-empty',
             'means': 'the question was examined exhaustively and the answer is zero',
             'carriedBy': 'CoverageResultV3 coverage=complete with no matching fact and '
                          'deficiency=null',
             'measuredExample': next((r for r in rows
                                      if r['state'] == 'complete-empty'), None)},
            {'state': 'partial',
             'means': ('the question was examined over an incomplete input: the examined '
                       'part is answered and the unexamined part is disclosed with its own '
                       'cause. The defining feature is that the cause is about the INPUT, '
                       'not about the capability'),
             'carriedBy': 'coverage=unknown WITH a published (deficiency, nativeCause) pair '
                          'whose deficiency is an input deficiency',
             'measuredExample': next(
                 (r for r in rows if r['coverage'] != 'complete'
                  and r['deficiency'] != 'language-tier-unsupported'), None),
             'whyItIsNotTheUnavailableRow': (
                 'input-closure-incomplete / body-language-owner-unenumerated says the '
                 'CAPABILITY EXISTS and the input did not support a complete answer. '
                 'language-tier-unsupported / capability-missing says the capability cannot '
                 'be served at all. The two carry different causes on purpose, and '
                 'R-CLONE-DEFICIENCY-PAIRING is the Run that exhibits the first.')},
            {'state': 'unavailable',
             'means': 'the capability cannot be served for this subject at all',
             'carriedBy': 'coverage=unknown with deficiency=language-tier-unsupported and '
                          'nativeCause=capability-missing',
             'measuredExample': next((r for r in rows
                                      if r.get('deficiency') ==
                                      'language-tier-unsupported'), None)},
            {'state': 'missing committed bytes',
             'means': 'a digest is named but its preimage is not retained',
             'carriedBy': 'NOT a Coverage state at all: it is a CUSTODY refusal at closure',
             'measuredExample': {
                 'artifact': 'vectors/native-join-negative-controls.json',
                 'control': 'grammar-bundle-manifest-bytes-dropped-but-still-a-tree-member',
                 'firstRefusal': '*:PREIMAGE_NOT_RETAINED',
                 'why': ('this is why the four must stay distinct: a missing byte is a '
                         'custody failure of the graph, not an analysis outcome, and it '
                         'cannot be reported as an empty or unavailable result')}},
        ],
        'allMeasuredRows': rows,
        'oneLabelForAllFourWouldBe': (
            'reporting unavailable or partial as complete-empty, which would read as a '
            'finding of zero -- the exact concealment the syntax-data Run refuses'),
    }


def detector_compat(cur):
    """R-DETECTOR-COMPAT-FILE: a detector compatibility LISTING is the reserved authenticated
    FILE, not the component manifest BODY."""
    nat = json.load(open(KIT + '/' + S.doc_path(
        'workflows/schemas/evaluator3/detector-manifest.schema.json')))
    det_tid, det = cur['detector']
    tree = det.get('tree') or []
    reserved = [r for r in tree if 'compat' in r.get('path', '').lower()]
    return {
        'requirement': 'R-DETECTOR-COMPAT-FILE', 'classification': 'measured',
        'law': {'detectorManifest': S.doc_path(
            'workflows/schemas/evaluator3/detector-manifest.schema.json'),
            'title': nat.get('title'),
            'reservedFileKeys': [k for k in json.dumps(nat).split('"')
                                 if 'compat' in k.lower()][:6]},
        'measured': [
            {'check': 'THE_LISTING_IS_A_FILE_IN_THE_SIGNED_TREE_NOT_A_MANIFEST_FIELD',
             'componentManifestBodyKeys': sorted(det),
             'listingAmongThoseKeys': any('compat' in k.lower() for k in det),
             'reservedTreeRows': reserved,
             'result': ('the component manifest body of this origin\'s detector closure '
                        'carries NO compatibility listing field, which is the shape the law '
                        'requires: the listing is a separate authenticated file whose digest '
                        'is a row of the signed tree, so it is covered by the same '
                        'closure identity without becoming part of the manifest body')},
            {'check': 'CANONICAL_METADATA_AND_SIGNED_TREE_OWNERS_APPLY',
             'owners': ['identity-and-evidence section 3 component-manifest-id over C of the '
                        'manifest record', 'the signed closure tree rows (path, sha256)'],
             'result': ('a listing file therefore has exactly the custody of any other tree '
                        'member: its bytes must be retained and re-hash, and changing it '
                        'mints a different closure2 identity')},
            {'check': 'WHY_NOT_THE_MANIFEST_BODY',
             'result': ('putting the listing in the manifest body would make every '
                        'compatibility edit a new component-manifest-id and therefore a new '
                        'closure identity for an unchanged executable, and it would make the '
                        'listing unavailable to a consumer who holds the file set but not '
                        'the manifest record')},
        ],
        'notReconstructedBeyondThis': (
            'this origin did not author a compatibility listing: the requirement is '
            'conditional ("if reconstructed") and what it demands is the DISTINCTION, which '
            'is measured above against the real retained detector closure.'),
    }


def test_prep_repair_auth(cur):
    """R-TEST-PREP-REPAIR-AUTH: authorization RECORDS, not host execution."""
    return {
        'requirement': 'R-TEST-PREP-REPAIR-AUTH', 'classification': 'explanatory+measured',
        'standing': ('these are authorization records and their admission rules. NOTHING was '
                     'executed: no test ran, no preparation ran, no repair was applied.'),
        'records': [
            {'step': 'test-execution',
             'paramsDef': 'invocation-record #/$defs/TestExecutionParams',
             'authorizationClass': 'explicit consent, and in CI a policy record',
             'refusals': ['TEST.INTERACTIVE_CONSENT_IN_CI',
                          'TEST.CONFINEMENT_CLAIM_REFUSED'],
             'd9': 'request-rejected 2 / REQUEST.PRECONDITION_FAILED',
             'sealsARun': False,
             'receipt': 'a test import is admitted; the step mints no run3'},
            {'step': 'native-preparation',
             'paramsDef': 'invocation-record #/$defs/NativePreparationParams',
             'authorizationClass': 'per-owner native preparation authorization '
                                   '(workflows section 12 delegating to native section 14 '
                                   'and security S15)',
             'refusals': ['native.execution-not-authorized',
                          'native.prepare-bound-exceeded',
                          'native.prepared-output-not-inert'],
             'd9': 'request-rejected 2 for authorization, operational-failed 4 for a fault',
             'sealsARun': False,
             'receipt': 'an execution receipt plus ONE admitted prepared import, never a Run',
             'retryPolicy': 'none by schema -- there is no automatic retry'},
            {'step': 'repair-apply',
             'paramsDef': 'invocation-record #/$defs/RepairApplyParams',
             'authorizationClass': 'a security authorization bound to the EXACT repairPlanId '
                                   'and baseSnapshotId',
             'refusals': ['AUTHZ.BASE_SNAPSHOT_MISMATCH',
                          'AUTHZ.POLICY_DOES_NOT_ADMIT_REPAIR',
                          'REPAIR.TARGET_PREIMAGE_MISMATCH', 'REPAIR.SOURCE_MOVED'],
             'd9': 'request-rejected 2 / REQUEST.PRECONDITION_FAILED',
             'sealsARun': False,
             'receipt': 'a MutationReceiptV1 keyed by the content-derived repair-apply key; '
                        'VERIFY afterwards admits a FRESH snapshot and seals a NEW Run',
             'measuredKey': 'vectors/mutation-keys.json repairApply.key'},
        ],
        'threeSeparatelyAuthorizedSteps': (
            'preview, apply and verify are three separately authorized steps: a preview '
            'authorization is not an apply authorization, and an apply authorization does '
            'not authorize the verify analysis that follows it.'),
        'whatThisOriginDidNotDo': ['run a test', 'prepare native inputs',
                                   'apply a repair', 'write any product file'],
    }


def purge_replay_output(cur):
    """R-PURGE-REPLAY-OUTPUT-FAILURE: purge, replay and required-output failures."""
    rows = []

    def mk(label, cls, code, detail_code, remedy, subject, exit_code, **extra):
        detail = {'code': detail_code, 'remedy': remedy, 'subject': subject}
        term = dict(cls, domainDetail=detail)
        e = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3,
             'kind': 'failure', 'requestId': REQ, 'projectId': cur['projectId'],
             'termination': term, 'exitCode': exit_code, 'errors': [detail]}
        e.update(extra)
        r = EV.admit(e, label)
        r['requirement'] = 'R-PURGE-REPLAY-OUTPUT-FAILURE'
        r['classification'] = 'valid'
        rows.append(r)
        return r

    mk('purge-after-replay-dependency', {'class': 'request-rejected',
                                         'errorCode': 'REQUEST.PRECONDITION_FAILED'},
       None, 'evidence.purged',
       'the evidence this replay depends on was purged; adopt a new baseline or re-analyse. '
       'Sealed history is retained, so the Run identity still resolves even though its '
       'replay inputs do not',
       cur['runId'], 2)
    mk('replay-required-evidence-missing', {'class': 'indeterminate',
                                            'reasonCodes': ['COVERAGE.REQUIRED_RELATION_MISSING']},
       None, 'evidence.missing',
       'a required retained input is absent, so the replay is INDETERMINATE rather than '
       'failing the policy: an absent input is not a negative finding',
       cur['planId'], 3)
    mk('required-output-delivery-failed', {'class': 'operational-failed',
                                           'errorCode': 'DELIVERY.REQUIRED_FAILED',
                                           'faultCause': 'delivery-required',
                                           'runId': cur['runId']},
       None, 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT',
       'the Run was committed and the REQUIRED output could not be delivered; the commit is '
       'not rolled back and the failure is operational, not a policy verdict',
       'json renderer', 4)
    mk('output-format-not-applicable', {'class': 'request-rejected',
                                        'errorCode': 'REQUEST.PRECONDITION_FAILED'},
       None, 'OUTPUT.FORMAT_NOT_APPLICABLE',
       'the requested format is not applicable to this command\'s request class; choose an '
       'applicable renderer rather than receiving a reshaped one',
       'sarif for a mutation command', 2)
    return {'envelopes': rows,
            'summary': {
                'requirement': 'R-PURGE-REPLAY-OUTPUT-FAILURE',
                'cases': [r['label'] for r in rows],
                'distinctions': {
                    'purgedVsMissing': ('evidence.purged is a DELIBERATE removal under an '
                                        'authorized purge; evidence.missing is an absence '
                                        'the host did not authorize. Both refuse, with '
                                        'different codes and different remedies.'),
                    'requiredOutputAfterCommit': ('a delivery failure AFTER the commit is '
                                                  'operational-failed with '
                                                  'faultCause=delivery-required and keeps '
                                                  'the runId: the Run exists and the '
                                                  'verdict is not reclassified'),
                    'replayIndeterminateNotFailed': ('a missing replay input yields '
                                                     'indeterminate with a reasonCode, '
                                                     'never policy-failed'),
                }}}


def public_termination(cur):
    """R-PUBLIC-TERMINATION-EXAMPLES -- one PUBLIC example per D9 termination class, each
    validated from the schemas rather than described, and each derived from the exit table
    rather than carrying a second opinion about its own exit code."""
    rows = []

    def mk(label, term, exit_code, kind='failure', **extra):
        e = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': kind,
             'requestId': REQ, 'projectId': cur['projectId'],
             'termination': term, 'exitCode': exit_code}
        e.update(extra)
        r = EV.admit(e, label)
        r['requirement'] = 'R-PUBLIC-TERMINATION-EXAMPLES'
        r['classification'] = 'valid'
        r['d9Class'] = term['class']
        rows.append(r)
        return r

    ok_detail = {'code': 'evidence.missing', 'remedy': 'see the per-step terminations',
                 'subject': 'audit'}
    mk('termination-success', {'class': 'success', 'authority': 'authoritative',
                               'runId': cur['runId']}, 0, kind='run',
       run={'kind': 'analysis', 'authority': 'authoritative', 'runId': cur['runId'],
            'planId': cur['planId'], 'verdict': 'pass', 'requiredCoverage': 'satisfied',
            'durability': 'committed', 'deficiency': 'none',
            'secondaryDeficiencies': []})
    mk('termination-policy-failed',
       {'class': 'policy-failed', 'authority': 'authoritative', 'runId': cur['runId']},
       1, kind='run',
       run={'kind': 'analysis', 'authority': 'authoritative', 'runId': cur['runId'],
            'planId': cur['planId'], 'verdict': 'fail', 'requiredCoverage': 'satisfied',
            'durability': 'committed', 'deficiency': 'none',
            'secondaryDeficiencies': []})
    mk('termination-request-rejected',
       {'class': 'request-rejected', 'errorCode': 'REQUEST.UNKNOWN_OPTION',
        'domainDetail': {'code': 'CONFIG.INVALID',
                         'remedy': 'remove the unknown option', 'subject': '--not-an-option'}},
       2, errors=[{'code': 'CONFIG.INVALID', 'remedy': 'remove the unknown option',
                   'subject': '--not-an-option'}])
    mk('termination-indeterminate',
       {'class': 'indeterminate',
        'reasonCodes': ['COVERAGE.REQUIRED_RELATION_MISSING'],
        'domainDetail': ok_detail},
       3, errors=[ok_detail])
    mk('termination-operational-failed',
       {'class': 'operational-failed', 'errorCode': 'LEDGER.BUSY_TIMEOUT',
        'faultCause': 'ledger-busy',
        'domainDetail': {'code': 'storage.backup-choice-required',
                         'remedy': 'retry once the ledger lease is free',
                         'subject': 'evidence ledger'}},
       4, errors=[{'code': 'storage.backup-choice-required',
                   'remedy': 'retry once the ledger lease is free',
                   'subject': 'evidence ledger'}])
    mk('termination-interrupted-before-any-run-was-committed',
       {'class': 'interrupted', 'signal': 'SIGINT'}, 130, kind='failure',
       errors=[{'code': 'evidence.missing',
                'remedy': 'no Run was committed before the interrupt, so none is cited',
                'subject': 'analysis'}])
    return {'envelopes': rows,
            'summary': {'requirement': 'R-PUBLIC-TERMINATION-EXAMPLES',
                        'classesCovered': sorted({r['d9Class'] for r in rows}),
                        'exitTable': EV.EXIT_BY_CLASS,
                        'afterSettleIsNeverReclassified': (
                            'the interrupted example carries NO runId, because a runId is '
                            'lawful there only when a Run was committed before the '
                            'interrupt; an interrupt after settle keeps the settled class '
                            'instead of becoming interrupted')}}


def subsystem_owners():
    return {
        'requirement': 'R-SUBSYSTEM-OWNERS', 'classification': 'explanatory',
        'owners': [
            {'decision': 'what bytes are in the snapshot and what their digests are',
             'subsystem': 'identity (foundation)',
             'selector': 'identity-and-evidence section 3 + identity-schemas.v3 snapshot2'},
            {'decision': 'which relation@rung a fact may carry and what its payload is',
             'subsystem': 'relation registry (foundation)',
             'selector': 'relation-payload-schemas.v2 x-opensip-relation-registry'},
            {'decision': 'what a native context/universe must agree with',
             'subsystem': 'native evidence',
             'selector': 'native-evidence sections 1-3, 11 + '
                         'x-opensip-digest-domains domainSets'},
            {'decision': 'whether a capability can be served at all for a language',
             'subsystem': 'native evidence (grammar capability registry)',
             'selector': 'native-evidence x-opensip-grammar-capability-registry'},
            {'decision': 'which rules are admitted and which predicates they evaluate',
             'subsystem': 'evaluator (composition v3)',
             'selector': 'workflows-and-surfaces section 5 + composition sections 1/2/9'},
            {'decision': 'the verdict of a Run',
             'subsystem': 'evaluator seal',
             'selector': 'composition v3 section 9.7 seal3'},
            {'decision': 'the verdict of an AUDIT',
             'subsystem': 'comparison',
             'selector': 'comparison-result AuditProfile + the comparison STEP, which is '
                         'the only step whose verdict gates an audit'},
            {'decision': 'whether a pivot may be executed and whether it is deterministic',
             'subsystem': 'comparison + closure custody',
             'selector': 'comparison-result IndeterminateReason pivot-* members'},
            {'decision': 'the D9 class, exit code and error code of a request',
             'subsystem': 'workflow host',
             'selector': 'workflows section 9 + common StepTermination'},
            {'decision': 'whether a mutation may happen at all',
             'subsystem': 'security authorization',
             'selector': 'AUTHZ.* detail codes + security unit; workflows explicitly does '
                         'NOT decide authorization'},
            {'decision': 'whether an output format is applicable',
             'subsystem': 'renderer inventory',
             'selector': 'command-inventory renderers[].applicability + '
                         'OUTPUT.FORMAT_NOT_APPLICABLE'},
            {'decision': 'what a retained import may prove',
             'subsystem': 'imported evidence',
             'selector': 'imported-evidence StalenessRule + '
                         'x-opensip-imported-requirement-law'},
        ],
        'whatIsNotOwnedHere': (
            'no subsystem in this kit authorizes a product implementation, and this origin '
            'claims none.'),
    }


main()
