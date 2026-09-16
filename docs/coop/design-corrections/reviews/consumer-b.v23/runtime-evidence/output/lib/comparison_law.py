"""COMPARISON LAW as a derivation from explicit PREMISES (generation 23, V23-D6).

Owners: docs/v2/contracts/product-v1/workflows-and-surfaces.md sections 2 (portable baseline) and 3
(multi-axis comparison), workflows/schemas/evaluator3/comparison-result.schema.json and
baseline-artifact.schema.json.

Generation 22 published every comparison vector with hand-written semantic fields (classification,
direction, contextDelta, pivotsAvailable, verdict, correspondence coverage) that its own premises did
not support -- an entry whose presence never changed classified EVIDENCE-DELTA, an "empty" result over
a Run that has findings, a scope delta whose E4 presence stayed true, a code-axis change classified on
the detection axis, and verdict `pass` beside a current required execution deficiency. Every field
below is DERIVED from a side's retained documents, findings, rule results and bound pivot results.

A premise that contradicts the law (a presence change across an axis whose context did not change)
raises PremiseInconsistency instead of being classified.

DECLARED INTERPRETATIONS (the owners leave these to a consumer; each is disclosed, none is hidden)
 I-C1 pivotsAvailable.E1/E2/E3 re-evaluate current facts under the baseline POLICY / SCOPE / WAIVERS
      respectively (the pivot table), so each is `not-needed` exactly when that document is unchanged,
      `available` when a bound re-evaluation result is supplied, else `unavailable`. E0 is `not-needed`
      when every detector disposition is identical-closure or declared-compatible.
 I-C2 The B->E0 transition spans the code axis AND the current evidence (E0 runs over current source
      and current inputs). For a rule with evidenceUse whose evidence availability changed: a presence
      change with code unchanged is EVIDENCE-DELTA (non-gating rules only); with code also changed it is
      INDETERMINATE evidence-availability-changed.
 I-C3 waivedB / waivedC are the waived status of the fingerprint under the baseline's embedded
      WaiverSetV1 and the current WaiverSetV1, matched by fingerprint target or (ruleId, subjectPath)
      target -- the same membership recipe the composition applies to findings.
 I-C4 A comparison that is not performed still reports contextDelta, detectors and pivotsAvailable as
      derived from the two contexts; entries, unmatched occurrences and correspondence are empty.
 I-C5 RuleCoverage.requiredCoverage is `unknown` for a rule whose side result is indeterminate and
      `satisfied` otherwise (a disabled rule owes no coverage).
"""
import copy

import opensip_core as K

SEVERITY = {'note': 0, 'warning': 1, 'error': 2}
AUDIT_PROFILES = {
    'code-regression': {'name': 'code-regression', 'gateCodeNetNew': True,
                        'gateNewlyLiveByPolicyAxes': False, 'gateAllCurrentLive': False,
                        'newWaiverSuppressesCodeNetNew': False,
                        'gateRuleUnder': 'baseline-or-current'},
    'policy-change': {'name': 'policy-change', 'gateCodeNetNew': True,
                      'gateNewlyLiveByPolicyAxes': True, 'gateAllCurrentLive': False,
                      'newWaiverSuppressesCodeNetNew': False,
                      'gateRuleUnder': 'baseline-or-current'},
    'full-current': {'name': 'full-current', 'gateCodeNetNew': True,
                     'gateNewlyLiveByPolicyAxes': True, 'gateAllCurrentLive': True,
                     'newWaiverSuppressesCodeNetNew': True, 'gateRuleUnder': 'current-only'},
    'report-only': {'name': 'report-only', 'gateCodeNetNew': False,
                    'gateNewlyLiveByPolicyAxes': False, 'gateAllCurrentLive': False,
                    'newWaiverSuppressesCodeNetNew': True, 'gateRuleUnder': 'current-only'},
}
CLASSIFICATIONS = ('UNCHANGED', 'CODE-NET-NEW', 'CODE-FIXED', 'DETECTION-DELTA', 'POLICY-DELTA',
                   'SCOPE-DELTA', 'WAIVER-DELTA', 'EVIDENCE-DELTA', 'INDETERMINATE')
AXES = ('code', 'detection', 'policy', 'scope', 'waiver')
AXIS_CONTEXT = {'code': 'codeChanged', 'detection': 'detectorChanged', 'policy': 'policyChanged',
                'scope': 'scopeChanged', 'waiver': 'waiversChanged'}
PIVOT_DOCUMENT_AXIS = {'E1': 'policyChanged', 'E2': 'scopeChanged', 'E3': 'waiversChanged'}
REMEDY_CODE = {'baseline-schema-major-unsupported': 'BASELINE.SCHEMA_MAJOR_UNSUPPORTED',
               'baseline-recipe-unsupported': 'BASELINE.RECIPE_UNSUPPORTED',
               'baseline-project-unmapped': 'BASELINE.PROJECT_UNMAPPED',
               'baseline-context-document-missing': 'BASELINE.CONTEXT_DOCUMENT_MISSING'}


class PremiseInconsistency(Exception):
    pass


def doc_digest(doc):
    return K.raw_sha256(K.C(doc))


def rule_of(policy, rule_id):
    return next((r for r in policy['rules'] if r['ruleId'] == rule_id), None)


def rule_gating(policy, rule_id):
    """CorrespondenceCoverage.gating: "Derived from admitted PolicyDocumentV2 enabled AND gate AND
    severity floor. Never inferred from ruleResults.outcome." """
    r = rule_of(policy, rule_id)
    return bool(r and r['enabled'] and r['gate']
                and SEVERITY[r['severity']] >= SEVERITY[policy['gateSeverityAtLeast']])


def waived_under(waivers, fingerprint, rule_id, subject_path):
    for w in waivers['waivers']:
        t = w['target']
        if t.get('fingerprint') == fingerprint:
            return True
        if t.get('ruleId') == rule_id and t.get('subjectPath') == subject_path:
            return True
    return False


def evidence_availability(bound_imports, evidence_relations):
    kinds = sorted({b['kind'] for b in bound_imports})
    rels = sorted(rel for rel, row in evidence_relations.items() if row['evidenceKind'] in kinds)
    return {'importKinds': kinds, 'relations': rels,
            'imports': sorted((dict(b) for b in bound_imports),
                              key=lambda b: b['importId'].encode())}


def evaluation_context(side, evidence_relations):
    docs = side['documents']
    return {'policyDigest': doc_digest(docs['policy']), 'scopeDigest': doc_digest(docs['scope']),
            'waiverSetDigest': doc_digest(docs['waivers']),
            'detectorClosureIds': [d['closureId'] for d in side['detectors']],
            'evidenceAvailability': evidence_availability(side['boundImports'],
                                                          evidence_relations)}


def baseline_artifact(side, evidence_relations, override_documents=None):
    """The portable baseline of section 2, derived from the ADOPTED side."""
    policy = side['documents']['policy']
    ctx = evaluation_context(side, evidence_relations)
    docs = copy.deepcopy(side['documents'])
    for k, v in (override_documents or {}).items():
        docs[k] = copy.deepcopy(v)
    entries = {}
    for f in side['findings']:
        if not f['matched']:
            continue
        entries[f['fingerprint']] = {
            'fingerprint': f['fingerprint'], 'ruleId': f['ruleId'], 'detectorId': f['detectorId'],
            'stabilityClass': side['stabilityClassByRule'][f['ruleId']],
            'subjectPath': f['subjectPath'], 'waived': f['waived']}
    unmatched = [{'side': 'baseline', 'findingId': f['findingId'], 'ruleId': f['ruleId'],
                  'subjectId': f['subjectId'], 'subjectPath': f['subjectPath'],
                  'severity': f['severity'], 'waived': f['waived']}
                 for f in side['findings'] if not f['matched']]
    desc = {
        'schemaFamily': 'opensip.product.baseline', 'schemaMajor': 2,
        'originProjectId': side['projectId'], 'source': {'snapshotId': side['snapshotId']},
        'runId': side['runId'], 'planId': side['planId'],
        'fingerprintRecipe': {'domain': 'finding-fingerprint', 'recipeMajor': 2},
        'detectorClosure': [{k: d[k] for k in ('detectorId', 'closureId', 'semanticsMajor',
                                               'semanticVersion', 'contributionId',
                                               'manifestDigest')} for d in side['detectors']],
        'pivotClosure': sorted((dict(c) for c in side['pivotClosure']),
                               key=lambda c: c['closureId'].encode()),
        'context': ctx, 'contextDocuments': docs,
        'ruleCoverage': sorted([
            {'ruleId': r['ruleId'],
             'requiredCoverage': ('unknown' if (side['ruleResults'].get(r['ruleId']) or {}).get(
                 'outcome') == 'indeterminate' else 'satisfied'),
             'enabled': r['enabled'], 'gating': rule_gating(policy, r['ruleId']),
             'evidenceUse': r['evidenceUse']}
            for r in policy['rules']], key=lambda r: r['ruleId'].encode()),
        'entries': [entries[k] for k in sorted(entries, key=lambda k: k.encode())],
        'unmatchedOccurrences': sorted(unmatched, key=lambda u: u['findingId'].encode()),
    }
    return {'baselineId': K.ID('workflow.baseline', desc), 'descriptor': desc,
            'custody': {'exportedByHostRelease': '3.0.0', 'exportedAtUtc': '2026-09-12T00:00:00Z',
                        'runRetainedAtExport': True,
                        'retentionPins': sorted({side['runId']}
                                                | {c['closureId'] for c in side['pivotClosure']})}}


def admission_reason(baseline, current):
    """Fresh-CI admission of section 2, in the order the section lists the checks."""
    d = baseline['descriptor']
    if d['schemaMajor'] != 2:
        return 'baseline-schema-major-unsupported'
    if d['fingerprintRecipe']['recipeMajor'] < 2:
        return 'baseline-recipe-unsupported'
    if d['originProjectId'] != current['projectId'] and not current.get('acceptOrigin'):
        return 'baseline-project-unmapped'
    ctx, docs = d['context'], d['contextDocuments']
    if (doc_digest(docs['policy']) != ctx['policyDigest']
            or doc_digest(docs['scope']) != ctx['scopeDigest']
            or doc_digest(docs['waivers']) != ctx['waiverSetDigest']):
        return 'baseline-context-document-missing'
    return None


def dispositions(baseline, current, pivots, declared_compatible=()):
    base = {e['detectorId']: e for e in baseline['descriptor']['detectorClosure']}
    cur = {d['detectorId']: d for d in current['detectors']}
    out = []
    for det in sorted(set(base) | set(cur), key=lambda s: s.encode()):
        b, c = base.get(det), cur.get(det)
        e0 = pivots.get('E0')
        row = {'detectorId': det, 'baselineClosureId': b and b['closureId'],
               'currentClosureId': c and c['closureId'],
               'baselineSemanticsMajor': b and b['semanticsMajor'],
               'currentSemanticsMajor': c and c['semanticsMajor']}
        if b and c and b['closureId'] == c['closureId']:
            row['method'] = 'identical-closure'
        elif b and c and (det, b['closureId']) in declared_compatible:
            row['method'] = 'declared-compatible'
        elif b and c and e0:
            row.update(method='three-way-pivot', pivotRunId=e0['pivotRunId'])
        elif c and not b:
            row['method'] = 'detector-added'
        elif b and not c and e0:
            row.update(method='detector-removed', pivotRunId=e0['pivotRunId'])
        else:
            row.update(method='indeterminate',
                       indeterminateReason=(pivots.get('E0Unavailable')
                                            or 'pivot-detector-unavailable'))
        out.append(row)
    return out


def context_delta(baseline, current_ctx, current_snapshot, disp):
    b = baseline['descriptor']
    return {'codeChanged': b['source']['snapshotId'] != current_snapshot,
            'detectorChanged': any(r['method'] != 'identical-closure' for r in disp),
            'policyChanged': b['context']['policyDigest'] != current_ctx['policyDigest'],
            'scopeChanged': b['context']['scopeDigest'] != current_ctx['scopeDigest'],
            'waiversChanged': b['context']['waiverSetDigest'] != current_ctx['waiverSetDigest'],
            'evidenceAvailabilityChanged': K.C(b['context']['evidenceAvailability'])
            != K.C(current_ctx['evidenceAvailability'])}


def pivots_available(delta, disp, pivots):
    methods = {r['method'] for r in disp}
    if methods <= {'identical-closure', 'declared-compatible'}:
        e0 = 'not-needed'
    elif 'indeterminate' in methods:
        e0 = 'unavailable'
    else:
        e0 = 'available' if pivots.get('E0') else 'unavailable'
    out = {'E0': e0}
    for k, axis in PIVOT_DOCUMENT_AXIS.items():
        out[k] = ('not-needed' if not delta[axis] else
                  'available' if pivots.get(k) else 'unavailable')
    return out


def classify(fp, meta, baseline, current, delta, pav, pivots, profile, disp):
    b_desc = baseline['descriptor']
    b_entries = {e['fingerprint']: e for e in b_desc['entries']}
    cur_f = {f['fingerprint']: f for f in current['findings'] if f['matched']}
    b_policy, c_policy = b_desc['contextDocuments']['policy'], current['documents']['policy']
    rule_id, det, path = meta['ruleId'], meta['detectorId'], meta['subjectPath']
    raw = {'B': fp in b_entries, 'E4': fp in cur_f}
    for k in ('E0', 'E1', 'E2', 'E3'):
        raw[k] = ({p['fingerprint'] for p in pivots[k]['fingerprints']}.__contains__(fp)
                  if pav[k] == 'available' else None)
    method = next((r['method'] for r in disp if r['detectorId'] == det), 'identical-closure')
    if method == 'detector-added':
        raw['E0'] = False
    waived_b = waived_under(b_desc['contextDocuments']['waivers'], fp, rule_id, path)
    waived_c = waived_under(current['documents']['waivers'], fp, rule_id, path)
    presence = {'B': raw['B'], 'E0': raw['E0'], 'E1': raw['E1'], 'E2': raw['E2'],
                'E3': raw['E3'], 'E4': raw['E4'], 'waivedB': waived_b, 'waivedC': waived_c}
    live = raw['E4'] and not waived_c
    gb, gc = rule_gating(b_policy, rule_id), rule_gating(c_policy, rule_id)
    rule_gates = (gb or gc) if profile['gateRuleUnder'] == 'baseline-or-current' else gc
    entry = {'fingerprint': fp, 'ruleId': rule_id, 'detectorId': det, 'presence': presence,
             'subsequentDeltas': [], 'liveInCurrent': live, 'gates': False}

    def indeterminate(reason):
        entry.update(classification='INDETERMINATE', indeterminateReason=reason)
        return entry, rule_gates

    # needed pivots that were not bound
    if pav['E0'] == 'unavailable' and method == 'indeterminate':
        return indeterminate(next(r['indeterminateReason'] for r in disp
                                  if r['detectorId'] == det))
    if any(pav[k] == 'unavailable' for k in ('E1', 'E2', 'E3')):
        return indeterminate('pivot-reevaluation-unavailable')
    # evidence axis for a rule with declared evidenceUse
    rule = rule_of(c_policy, rule_id) or rule_of(b_policy, rule_id) or {'evidenceUse': []}
    uses_evidence = bool(rule['evidenceUse'])
    cur_kinds = set(current['context']['evidenceAvailability']['importKinds'])
    if uses_evidence and any(eu['requirement'] == 'required' and eu['kind'] not in cur_kinds
                             for eu in rule['evidenceUse']):
        return indeterminate('required-evidence-unavailable')
    if uses_evidence and delta['evidenceAvailabilityChanged'] and (gb or gc):
        same_kinds = (b_desc['context']['evidenceAvailability']['importKinds']
                      == current['context']['evidenceAvailability']['importKinds'])
        return indeterminate('evidence-content-changed' if same_kinds
                             else 'evidence-availability-changed')
    # fill not-needed pivots from the pivot nearer the current side
    filled = dict(raw)
    for k, nxt in (('E3', 'E4'), ('E2', 'E3'), ('E1', 'E2'), ('E0', 'E1')):
        if pav[k] == 'not-needed':
            filled[k] = filled[nxt]
    if filled['E3'] != filled['E4']:
        raise PremiseInconsistency('E3 and E4 differ only by waivers, never by presence: %s' % fp)
    changes = {'code': filled['B'] != filled['E0'], 'detection': filled['E0'] != filled['E1'],
               'policy': filled['E1'] != filled['E2'], 'scope': filled['E2'] != filled['E3'],
               'waiver': bool(filled['E4']) and waived_b != waived_c}
    axis_of = {}
    for axis in AXES:
        if not changes[axis]:
            continue
        if delta[AXIS_CONTEXT[axis]]:
            axis_of[axis] = axis
        elif axis == 'code' and uses_evidence and delta['evidenceAvailabilityChanged']:
            axis_of[axis] = 'evidence'
        else:
            raise PremiseInconsistency('presence changed on the %s axis whose context did not '
                                       'change: %s' % (axis, fp))
    if changes['code'] and delta['codeChanged'] and uses_evidence \
            and delta['evidenceAvailabilityChanged']:
        return indeterminate('evidence-availability-changed')
    changed = [a for a in AXES if changes[a]]
    if not changed:
        entry['classification'] = 'UNCHANGED'
        return entry, rule_gates
    first = changed[0]
    kind = axis_of[first]
    if first == 'waiver':
        entry['classification'] = 'WAIVER-DELTA'
        entry['direction'] = 'waiver-added' if waived_c else 'waiver-removed'
    else:
        before, after = ((filled['B'], filled['E0']) if first == 'code' else
                         (filled['E0'], filled['E1']) if first == 'detection' else
                         (filled['E1'], filled['E2']) if first == 'policy' else
                         (filled['E2'], filled['E3']))
        entry['direction'] = 'appeared' if (not before and after) else 'vanished'
        entry['classification'] = {
            'code': 'CODE-NET-NEW' if entry['direction'] == 'appeared' else 'CODE-FIXED',
            'evidence': 'EVIDENCE-DELTA', 'detection': 'DETECTION-DELTA',
            'policy': 'POLICY-DELTA', 'scope': 'SCOPE-DELTA'}[kind]
    entry['subsequentDeltas'] = [axis_of[a] for a in changed[1:]]
    # gates by the named audit profile
    if rule_gates:
        c = entry['classification']
        if c == 'CODE-NET-NEW' and profile['gateCodeNetNew'] and not (
                profile['newWaiverSuppressesCodeNetNew'] and waived_c):
            entry.update(gates=True, gateReason='code-net-new' if live
                         else 'code-net-new-policy-hidden')
        elif (profile['gateNewlyLiveByPolicyAxes'] and live
              and c in ('POLICY-DELTA', 'SCOPE-DELTA', 'WAIVER-DELTA')
              and entry.get('direction') in ('appeared', 'waiver-removed')):
            entry.update(gates=True, gateReason='newly-live-policy-axis')
        elif profile['gateAllCurrentLive'] and live:
            entry.update(gates=True, gateReason='current-live')
    return entry, rule_gates


def population(baseline, current, pivots, pav):
    meta = {}
    for e in baseline['descriptor']['entries']:
        meta.setdefault(e['fingerprint'], {'ruleId': e['ruleId'], 'detectorId': e['detectorId'],
                                           'subjectPath': e['subjectPath']})
    for k in ('E0', 'E1', 'E2', 'E3'):
        if pav[k] == 'available':
            for p in pivots[k]['fingerprints']:
                meta.setdefault(p['fingerprint'], {x: p[x] for x in ('ruleId', 'detectorId',
                                                                     'subjectPath')})
    for f in current['findings']:
        if f['matched']:
            meta[f['fingerprint']] = {'ruleId': f['ruleId'], 'detectorId': f['detectorId'],
                                      'subjectPath': f['subjectPath']}
    return meta


def rule_deficiencies(current):
    policy = current['documents']['policy']
    kinds = set(current['context']['evidenceAvailability']['importKinds'])
    out = []
    for r in policy['rules']:
        if not r['enabled']:
            continue
        rr = current['ruleResults'].get(r['ruleId']) or {}
        causes = []
        if any(eu['requirement'] == 'required' and eu['kind'] not in kinds
               for eu in r['evidenceUse']):
            causes.append('required-evidence-unavailable')
        if rr.get('outcome') == 'indeterminate':
            causes.append('required-coverage-unknown')
        if rr.get('enumerationState') not in (None, 'complete') or rr.get('unresolvedSubjects') \
                or any(not f['matched'] for f in current['findings'] if f['ruleId'] == r['ruleId']):
            causes.append('correspondence-incomplete')
        for c in causes:
            out.append({'ruleId': r['ruleId'], 'gating': rule_gating(policy, r['ruleId']),
                        'cause': c})
    return sorted(out, key=lambda d: (d['ruleId'].encode(), d['cause'].encode()))


def correspondence_coverage(current):
    policy = current['documents']['policy']
    out = []
    for r in policy['rules']:
        mine = [f for f in current['findings'] if f['ruleId'] == r['ruleId']]
        rr = current['ruleResults'].get(r['ruleId']) or {}
        out.append({'ruleId': r['ruleId'], 'gating': rule_gating(policy, r['ruleId']),
                    'matchedCount': sum(1 for f in mine if f['matched']),
                    'unmatchedCount': sum(1 for f in mine if not f['matched']),
                    'populationUnknown': bool(r['enabled'] and (
                        rr.get('enumerationState') not in (None, 'complete')
                        or rr.get('unresolvedSubjects'))),
                    'zeroFindings': not mine})
    return sorted(out, key=lambda c: c['ruleId'].encode())


def derive(premises, baseline, evidence_relations):
    """The ComparisonResult of section 3 derived from a scenario's premises and baseline artifact."""
    current = copy.deepcopy(premises['currentSide'])
    current['context'] = evaluation_context(current, evidence_relations)
    pivots = premises.get('pivots') or {}
    profile = AUDIT_PROFILES[premises['profile']]
    disp = dispositions(baseline, current, pivots,
                        {tuple(x) for x in premises.get('declaredCompatible') or []})
    delta = context_delta(baseline, current['context'], current['snapshotId'], disp)
    pav = pivots_available(delta, disp, pivots)
    reason = admission_reason(baseline, current)
    desc = {
        'schemaFamily': 'opensip.product.comparison', 'schemaMajor': 2,
        'baselineId': baseline['baselineId'], 'currentRunId': current['runId'],
        'currentSnapshotId': current['snapshotId'], 'auditProfile': profile,
        'projectCorrespondence': ('same-project'
                                  if baseline['descriptor']['originProjectId']
                                  == current['projectId'] else
                                  'declared' if current.get('acceptOrigin') else 'unmapped'),
        'comparisonPerformed': reason is None,
        'baselineContext': baseline['descriptor']['context'],
        'currentContext': current['context'], 'contextDelta': delta, 'pivotsAvailable': pav,
        'detectors': disp, 'ruleDeficiencies': [], 'entries': [],
        'counts': {k: 0 for k in CLASSIFICATIONS + ('gating',)}, 'verdict': 'indeterminate',
        'unmatchedOccurrences': [], 'correspondenceCoverage': [],
        'currentEvaluationState': current['evaluationState'],
        'currentExecutionDeficiencies': current['executionDeficiencies'],
    }
    if reason is not None:
        desc['wholeIndeterminateReason'] = reason
        desc['remedy'] = {'code': REMEDY_CODE[reason],
                          'remedy': premises.get('remedyText') or
                          'the baseline cannot be admitted for comparison; re-export or re-adopt it'}
        return {'comparisonResultId': K.ID('workflow.comparison', desc), 'descriptor': desc}
    meta = population(baseline, current, pivots, pav)
    entries, gating_indeterminate = [], False
    for fp in sorted(meta, key=lambda k: k.encode()):
        e, rule_gates = classify(fp, meta[fp], baseline, current, delta, pav, pivots, profile,
                                 disp)
        entries.append(e)
        if e['classification'] == 'INDETERMINATE' and rule_gates:
            gating_indeterminate = True
    counts = {k: sum(1 for e in entries if e['classification'] == k) for k in CLASSIFICATIONS}
    counts['gating'] = sum(1 for e in entries if e['gates'])
    rdefs = rule_deficiencies(current)
    unmatched = [u for u in baseline['descriptor']['unmatchedOccurrences']] + [
        {'side': 'current', 'findingId': f['findingId'], 'ruleId': f['ruleId'],
         'subjectId': f['subjectId'], 'subjectPath': f['subjectPath'], 'severity': f['severity'],
         'waived': f['waived']} for f in current['findings'] if not f['matched']]
    if counts['gating']:
        verdict = 'fail'
    elif (gating_indeterminate or any(d['gating'] for d in rdefs)
          or current['executionDeficiencies']):
        verdict = 'indeterminate'
    else:
        verdict = 'pass'
    desc.update(entries=entries, counts=counts, ruleDeficiencies=rdefs, verdict=verdict,
                unmatchedOccurrences=sorted(unmatched, key=lambda u: (u['side'].encode(),
                                                                      u['findingId'].encode())),
                correspondenceCoverage=correspondence_coverage(current))
    return {'comparisonResultId': K.ID('workflow.comparison', desc), 'descriptor': desc}
