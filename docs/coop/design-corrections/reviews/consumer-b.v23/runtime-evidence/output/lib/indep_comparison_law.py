"""INDEPENDENT re-derivation of every comparison and baseline vector from its RETAINED PREMISES
(generation 23, V23-D6).

Written separately from comparison_law.py (the module phase 8 builds the records with) and
deliberately NOT importing it. It reads vectors/comparison-premises.json and, for every scenario:

  1. re-reads the REAL-side premises from the TypeScript Run store with its own extraction (policy,
     scope and waiver documents and their raw C digests, detector and pivot closures, the bound import,
     matched findings with fingerprint subject paths, the waived set, rule results, evaluation state
     and execution deficiencies) and refuses a real side whose premises differ; a side that is not
     real must be listed under syntheticHelperOnly;
  2. rebuilds the baseline artifact from the baseline-side premises and compares it with the retained
     artifact field by field, re-admitting it and recomputing baselineId;
  3. re-derives every semantic field of the ComparisonResult (admission, contexts, contextDelta,
     detector dispositions, pivotsAvailable, per-fingerprint presence / classification / direction /
     subsequentDeltas / liveInCurrent / gates / gateReason, counts, ruleDeficiencies, correspondence
     coverage, unmatched occurrences, verdict) and compares each with the retained record;
  4. re-admits the retained record against its owning schema and recomputes comparisonResultId.

The derivation follows workflows-and-surfaces sections 2-3 and the comparison-result schema, with
the declared interpretations I-C1..I-C5 that comparison_law.py discloses. It measures agreement
between two separately written derivations over the same premises and the owner clauses; it does not
execute a product comparison, a prior detector or a re-evaluation.
"""
import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
CMP_DOC = 'workflows/schemas/evaluator3/comparison-result.schema.json'
BASE_DOC = 'workflows/schemas/evaluator3/baseline-artifact.schema.json'
IMPORTED_DOC = 'workflows/schemas/imported-evidence.schema.json'
SEV = ('note', 'warning', 'error')
CLASSES = ('UNCHANGED', 'CODE-NET-NEW', 'CODE-FIXED', 'DETECTION-DELTA', 'POLICY-DELTA',
           'SCOPE-DELTA', 'WAIVER-DELTA', 'EVIDENCE-DELTA', 'INDETERMINATE')
# the pivot chain of section 3: (axis, left pivot, right pivot, the context flag that must change)
CHAIN = (('code', 'B', 'E0', 'codeChanged'), ('detection', 'E0', 'E1', 'detectorChanged'),
         ('policy', 'E1', 'E2', 'policyChanged'), ('scope', 'E2', 'E3', 'scopeChanged'))
REMEDY = {'baseline-schema-major-unsupported': 'BASELINE.SCHEMA_MAJOR_UNSUPPORTED',
          'baseline-recipe-unsupported': 'BASELINE.RECIPE_UNSUPPORTED',
          'baseline-project-unmapped': 'BASELINE.PROJECT_UNMAPPED',
          'baseline-context-document-missing': 'BASELINE.CONTEXT_DOCUMENT_MISSING'}


class Refused(Exception):
    pass


def kitjson(name):
    return json.load(open(S.KIT + '/' + S.doc_path(name)))


EVREL = kitjson(IMPORTED_DOC)['x-opensip-evidence-relation-registry']['relations']


def sha_c(doc):
    return hashlib.sha256(K.C(doc)).hexdigest()


def gating(policy, rid):
    for r in policy['rules']:
        if r['ruleId'] == rid:
            return bool(r['enabled'] and r['gate']
                        and SEV.index(r['severity']) >= SEV.index(policy['gateSeverityAtLeast']))
    return False


def waived(waivers, fp, rid, path):
    return any(w['target'].get('fingerprint') == fp
               or (w['target'].get('ruleId'), w['target'].get('subjectPath')) == (rid, path)
               for w in waivers['waivers'])


# ------------------------------------------------------------------ 1. the real TypeScript side
def real_ts_side():
    st, doc = ST.Store.load(OUT + '/runs/typescript.store.json')
    run_id = doc['claim']['runId']
    run = st.objects[run_id]
    proof = st.objects[st.objects[run['evaluationSealId']]['proofBundleId']]
    blob = lambda label: json.loads(st.get_blob(st.labels[label]).decode())
    policy, scope, waivers = blob('policy'), blob('scope-document'), blob('waivers')
    emit = blob('emission-plan')
    sev = {r['ruleId']: r['severity'] for r in policy['rules']}
    # a detector is named by its retained component manifest body
    names = {t: json.loads(st.get_blob(r['manifestDigest']).decode())['name']
             for t, r in st.objects.items() if t.startswith('closure2:') and r.get('kind') == 'detector'}
    findings = []
    for fid in proof['findingIds']:
        f = st.objects[fid]
        key = st.objects[f['fingerprint']]
        findings.append({'findingId': fid, 'fingerprint': f['fingerprint'], 'ruleId': f['ruleId'],
                         'detectorId': names[f['ruleClosure']], 'subjectId': f['subjectId'],
                         'subjectPath': key['subjectKey']['logicalPath'],
                         'severity': sev[f['ruleId']], 'waived': fid in proof['waivedFindingIds'],
                         'matched': f['correspondence']['state'] == 'matched'})
    imports = []
    for t, w in sorted(st.objects.items()):
        if t.startswith('import2:'):
            if K.ID('import', w) != t:
                raise Refused('IMPORT_IDENTITY_DOES_NOT_RECOMPUTE:%s' % t)
            imports.append({'kind': w['kind'], 'importId': t, 'payloadDigest': w['payloadDigest'],
                            'sourceCorrespondenceDigest': w['sourceCorrespondenceDigest'],
                            'scopeDigest': w['scopeDigest'],
                            'observationDigest': w['observationDigest']})
    closures = {t: r for t, r in st.objects.items() if t.startswith('closure2:')}
    return {'store': st, 'runId': run_id, 'snapshotId': run['snapshotId'], 'planId': run['planId'],
            'projectId': run['projectId'],
            'documents': {'policy': policy, 'scope': scope, 'waivers': waivers},
            'digestsAreTheRetainedLabels': (sha_c(policy) == st.labels['policy']
                                            and sha_c(scope) == st.labels['scope-document']
                                            and sha_c(waivers) == st.labels['waivers']),
            'findings': findings, 'boundImports': imports,
            'ruleResults': {rr['ruleId']: {'outcome': rr['outcome'],
                                           'enumerationState': rr['enumeration']['state'],
                                           'unresolvedSubjects':
                                               len(rr['enumeration']['unresolvedSubjectIds'])}
                            for rr in proof['ruleResults']},
            'evaluationState': proof['evaluationState'],
            'executionDeficiencies': proof['executionDeficiencies'], 'closures': closures,
            'detectorNames': names,
            'stabilityClassByRule': {r['ruleId']: r['stabilityClass'] for r in emit['rules']},
            'contributionByDetector': {r['detectorClosure']: r['contributionId']
                                       for r in emit['rules']}}


def rebind_real(side, real, where, f):
    for k in ('runId', 'snapshotId', 'planId', 'projectId', 'evaluationState'):
        f(side[k] == real[k], 'REAL_SIDE_%s_IS_THE_TYPESCRIPT_RUN' % k.upper(), where)
    f(K.C(side['documents']) == K.C(real['documents']) and real['digestsAreTheRetainedLabels'],
      'REAL_SIDE_DOCUMENTS_ARE_THE_RETAINED_BLOBS', where)
    f(K.C(sorted(side['findings'], key=lambda x: x['findingId']))
      == K.C(sorted(real['findings'], key=lambda x: x['findingId'])),
      'REAL_SIDE_FINDINGS_ARE_THE_PROOF_FINDINGS', where)
    f(K.C(side['boundImports']) == K.C(real['boundImports']),
      'REAL_SIDE_BOUND_IMPORTS_ARE_THE_RETAINED_WRAPPERS', where)
    f(K.C(side['ruleResults']) == K.C(real['ruleResults'])
      and K.C(side['executionDeficiencies']) == K.C(real['executionDeficiencies']),
      'REAL_SIDE_RULE_RESULTS_AND_EXECUTION_DEFICIENCIES_ARE_THE_PROOF', where)
    for d in side['detectors']:
        rec = real['closures'].get(d['closureId'])
        f(rec is not None and rec.get('kind') == 'detector'
          and rec.get('manifestDigest') == d['manifestDigest']
          and rec.get('semanticVersion') == d['semanticVersion']
          and d['semanticsMajor'] == int(rec['semanticVersion'].split('.')[0])
          and d['detectorId'] == real['detectorNames'].get(d['closureId'])
          and d['contributionId'] == real['contributionByDetector'].get(d['closureId']),
          'REAL_SIDE_DETECTOR_IS_A_RETAINED_DETECTOR_CLOSURE', dict(where, closure=d['closureId']))
    f(side['stabilityClassByRule'] == real['stabilityClassByRule'],
      'REAL_SIDE_STABILITY_CLASSES_ARE_THE_EMISSION_PLAN', where)
    retained_pivots = sorted(t for t, r in real['closures'].items()
                             if r.get('kind') in ('detector', 'evaluator', 'provider', 'toolchain',
                                                  'stdlib', 'schema-set'))
    f(sorted(c['closureId'] for c in side['pivotClosure']) == retained_pivots,
      'REAL_SIDE_PIVOT_CLOSURE_IS_EVERY_RETAINED_PIVOT_KIND_CLOSURE', where)
    for c in side['pivotClosure']:
        rec = real['closures'].get(c['closureId'])
        f(rec is not None and rec.get('kind') == c['kind']
          and rec.get('manifestDigest') == c['manifestDigest'],
          'REAL_SIDE_PIVOT_CLOSURE_IS_RETAINED', dict(where, closure=c['closureId']))


# ------------------------------------------------------------------ 2. the baseline artifact
def context_of(side):
    kinds = sorted({b['kind'] for b in side['boundImports']})
    return {'policyDigest': sha_c(side['documents']['policy']),
            'scopeDigest': sha_c(side['documents']['scope']),
            'waiverSetDigest': sha_c(side['documents']['waivers']),
            'detectorClosureIds': [d['closureId'] for d in side['detectors']],
            'evidenceAvailability': {
                'importKinds': kinds,
                'relations': sorted(r for r, row in EVREL.items() if row['evidenceKind'] in kinds),
                'imports': sorted(side['boundImports'], key=lambda b: b['importId'].encode())}}


def rebuild_baseline(side, override):
    docs = dict(side['documents'], **(override or {}))
    policy = side['documents']['policy']
    rows = sorted({f['fingerprint']: {'fingerprint': f['fingerprint'], 'ruleId': f['ruleId'],
                                      'detectorId': f['detectorId'],
                                      'stabilityClass': side['stabilityClassByRule'][f['ruleId']],
                                      'subjectPath': f['subjectPath'], 'waived': f['waived']}
                   for f in side['findings'] if f['matched']}.items())
    desc = {'schemaFamily': 'opensip.product.baseline', 'schemaMajor': 2,
            'originProjectId': side['projectId'], 'source': {'snapshotId': side['snapshotId']},
            'runId': side['runId'], 'planId': side['planId'],
            'fingerprintRecipe': {'domain': 'finding-fingerprint', 'recipeMajor': 2},
            'detectorClosure': [{k: d[k] for k in ('detectorId', 'closureId', 'semanticsMajor',
                                                   'semanticVersion', 'contributionId',
                                                   'manifestDigest')}
                                for d in side['detectors']],
            'pivotClosure': sorted(side['pivotClosure'], key=lambda c: c['closureId'].encode()),
            'context': context_of(side), 'contextDocuments': docs,
            'ruleCoverage': sorted([{'ruleId': r['ruleId'],
                                     'requiredCoverage': 'unknown' if side['ruleResults'].get(
                                         r['ruleId'], {}).get('outcome') == 'indeterminate'
                                     else 'satisfied',
                                     'enabled': r['enabled'],
                                     'gating': gating(policy, r['ruleId']),
                                     'evidenceUse': r['evidenceUse']} for r in policy['rules']],
                                   key=lambda r: r['ruleId'].encode()),
            'entries': [v for _k, v in sorted(rows, key=lambda kv: kv[0].encode())],
            'unmatchedOccurrences': sorted([
                {'side': 'baseline', 'findingId': f['findingId'], 'ruleId': f['ruleId'],
                 'subjectId': f['subjectId'], 'subjectPath': f['subjectPath'],
                 'severity': f['severity'], 'waived': f['waived']}
                for f in side['findings'] if not f['matched']],
                key=lambda u: u['findingId'].encode())}
    return desc


# ------------------------------------------------------------------ 3. the comparison
def rederive(sc, baseline):
    cur = copy.deepcopy(sc['currentSide'])
    cur_ctx = context_of(cur)
    bd = baseline['descriptor']
    piv = sc.get('pivots') or {}
    prof = sc['auditProfileRecord']
    # detector dispositions
    base_det = {e['detectorId']: e for e in bd['detectorClosure']}
    cur_det = {d['detectorId']: d for d in cur['detectors']}
    compat = {tuple(x) for x in sc.get('declaredCompatible') or []}
    disp = []
    for det in sorted(set(base_det) | set(cur_det), key=str.encode):
        b, c = base_det.get(det), cur_det.get(det)
        row = {'detectorId': det, 'baselineClosureId': b['closureId'] if b else None,
               'currentClosureId': c['closureId'] if c else None,
               'baselineSemanticsMajor': b['semanticsMajor'] if b else None,
               'currentSemanticsMajor': c['semanticsMajor'] if c else None}
        if b and c:
            if b['closureId'] == c['closureId']:
                row['method'] = 'identical-closure'
            elif (det, b['closureId']) in compat:
                row['method'] = 'declared-compatible'
            elif piv.get('E0'):
                row['method'], row['pivotRunId'] = 'three-way-pivot', piv['E0']['pivotRunId']
            else:
                row['method'] = 'indeterminate'
                row['indeterminateReason'] = piv.get('E0Unavailable') or 'pivot-detector-unavailable'
        elif c:
            row['method'] = 'detector-added'
        elif piv.get('E0'):
            row['method'], row['pivotRunId'] = 'detector-removed', piv['E0']['pivotRunId']
        else:
            row['method'] = 'indeterminate'
            row['indeterminateReason'] = piv.get('E0Unavailable') or 'pivot-detector-unavailable'
        disp.append(row)
    delta = {'codeChanged': bd['source']['snapshotId'] != cur['snapshotId'],
             'detectorChanged': any(r['method'] != 'identical-closure' for r in disp),
             'policyChanged': bd['context']['policyDigest'] != cur_ctx['policyDigest'],
             'scopeChanged': bd['context']['scopeDigest'] != cur_ctx['scopeDigest'],
             'waiversChanged': bd['context']['waiverSetDigest'] != cur_ctx['waiverSetDigest'],
             'evidenceAvailabilityChanged': K.C(bd['context']['evidenceAvailability'])
             != K.C(cur_ctx['evidenceAvailability'])}
    ms = {r['method'] for r in disp}
    status = {'E0': ('not-needed' if ms <= {'identical-closure', 'declared-compatible'} else
                     'unavailable' if 'indeterminate' in ms else
                     'available' if piv.get('E0') else 'unavailable')}
    for k, flag in (('E1', 'policyChanged'), ('E2', 'scopeChanged'), ('E3', 'waiversChanged')):
        status[k] = 'not-needed' if not delta[flag] else ('available' if piv.get(k)
                                                          else 'unavailable')
    ctx, docs = bd['context'], bd['contextDocuments']
    reason = ('baseline-schema-major-unsupported' if bd['schemaMajor'] != 2 else
              'baseline-recipe-unsupported' if bd['fingerprintRecipe']['recipeMajor'] < 2 else
              'baseline-project-unmapped' if bd['originProjectId'] != cur['projectId']
              and not cur.get('acceptOrigin') else
              'baseline-context-document-missing'
              if (sha_c(docs['policy']), sha_c(docs['scope']), sha_c(docs['waivers']))
              != (ctx['policyDigest'], ctx['scopeDigest'], ctx['waiverSetDigest']) else None)
    out = {'comparisonPerformed': reason is None, 'wholeIndeterminateReason': reason,
           'remedyCode': REMEDY.get(reason), 'baselineContext': bd['context'],
           'currentContext': cur_ctx, 'contextDelta': delta, 'pivotsAvailable': status,
           'detectors': disp, 'projectCorrespondence':
               'same-project' if bd['originProjectId'] == cur['projectId'] else
               ('declared' if cur.get('acceptOrigin') else 'unmapped'),
           'currentEvaluationState': cur['evaluationState'],
           'currentExecutionDeficiencies': cur['executionDeficiencies']}
    if reason is not None:
        out.update(entries=[], counts={k: 0 for k in CLASSES + ('gating',)},
                   verdict='indeterminate', ruleDeficiencies=[], unmatchedOccurrences=[],
                   correspondenceCoverage=[])
        return out
    # the fingerprint population: B union every bound pivot union E4
    meta = {}
    for e in bd['entries']:
        meta.setdefault(e['fingerprint'], (e['ruleId'], e['detectorId'], e['subjectPath']))
    sets = {'B': {e['fingerprint'] for e in bd['entries']},
            'E4': {f['fingerprint'] for f in cur['findings'] if f['matched']}}
    for k in ('E0', 'E1', 'E2', 'E3'):
        if status[k] == 'available':
            sets[k] = {p['fingerprint'] for p in piv[k]['fingerprints']}
            for p in piv[k]['fingerprints']:
                meta.setdefault(p['fingerprint'], (p['ruleId'], p['detectorId'], p['subjectPath']))
    for f in cur['findings']:
        if f['matched']:
            meta[f['fingerprint']] = (f['ruleId'], f['detectorId'], f['subjectPath'])
    bpol, cpol = docs['policy'], cur['documents']['policy']
    rule_by_id = {r['ruleId']: r for r in bpol['rules']}
    rule_by_id.update({r['ruleId']: r for r in cpol['rules']})
    cur_kinds = set(cur_ctx['evidenceAvailability']['importKinds'])
    entries = []
    gating_unknown = False
    for fp in sorted(meta, key=str.encode):
        rid, det, path = meta[fp]
        method = next(r for r in disp if r['detectorId'] == det)['method']
        col = {'B': fp in sets['B'], 'E4': fp in sets['E4']}
        for k in ('E0', 'E1', 'E2', 'E3'):
            col[k] = (fp in sets[k]) if status[k] == 'available' else None
        if method == 'detector-added':
            col['E0'] = False
        wb, wc = waived(docs['waivers'], fp, rid, path), waived(cur['documents']['waivers'], fp,
                                                                 rid, path)
        gb, gc = gating(bpol, rid), gating(cpol, rid)
        under = (gb or gc) if prof['gateRuleUnder'] == 'baseline-or-current' else gc
        e = {'fingerprint': fp, 'ruleId': rid, 'detectorId': det,
             'presence': dict(col, waivedB=wb, waivedC=wc), 'subsequentDeltas': [],
             'liveInCurrent': bool(col['E4'] and not wc), 'gates': False}
        uses = rule_by_id.get(rid, {}).get('evidenceUse') or []
        why = None
        if status['E0'] == 'unavailable' and method == 'indeterminate':
            why = next(r for r in disp if r['detectorId'] == det)['indeterminateReason']
        elif 'unavailable' in (status['E1'], status['E2'], status['E3']):
            why = 'pivot-reevaluation-unavailable'
        elif any(u['requirement'] == 'required' and u['kind'] not in cur_kinds for u in uses):
            why = 'required-evidence-unavailable'
        elif uses and delta['evidenceAvailabilityChanged'] and (gb or gc):
            why = ('evidence-content-changed'
                   if bd['context']['evidenceAvailability']['importKinds']
                   == cur_ctx['evidenceAvailability']['importKinds']
                   else 'evidence-availability-changed')
        if why is None:
            eff = dict(col)
            for k, right in (('E3', 'E4'), ('E2', 'E3'), ('E1', 'E2'), ('E0', 'E1')):
                if status[k] == 'not-needed':
                    eff[k] = eff[right]
            if eff['E3'] != eff['E4']:
                raise Refused('E3_AND_E4_PRESENCE_DIFFER:%s' % fp)
            moves = []
            for axis, left, right, flag in CHAIN:
                if eff[left] != eff[right]:
                    if delta[flag]:
                        name = axis
                    elif axis == 'code' and uses and delta['evidenceAvailabilityChanged']:
                        name = 'evidence'
                    else:
                        raise Refused('PRESENCE_MOVED_ON_AN_UNCHANGED_AXIS:%s:%s' % (axis, fp))
                    moves.append((name, eff[left], eff[right]))
            if eff['E4'] and wb != wc:
                if not delta['waiversChanged']:
                    raise Refused('WAIVER_STATUS_MOVED_WITHOUT_A_WAIVER_CHANGE:%s' % fp)
                moves.append(('waiver', wb, wc))
            code_and_evidence = (eff['B'] != eff['E0'] and delta['codeChanged'] and uses
                                 and delta['evidenceAvailabilityChanged'])
            if code_and_evidence:
                why = 'evidence-availability-changed'
            elif not moves:
                e['classification'] = 'UNCHANGED'
            else:
                name, before, after = moves[0]
                if name == 'waiver':
                    e['direction'] = 'waiver-added' if after else 'waiver-removed'
                    e['classification'] = 'WAIVER-DELTA'
                else:
                    e['direction'] = 'appeared' if after else 'vanished'
                    e['classification'] = {'code': 'CODE-NET-NEW' if after else 'CODE-FIXED',
                                           'evidence': 'EVIDENCE-DELTA',
                                           'detection': 'DETECTION-DELTA',
                                           'policy': 'POLICY-DELTA',
                                           'scope': 'SCOPE-DELTA'}[name]
                e['subsequentDeltas'] = [m[0] for m in moves[1:]]
                if under:
                    live = e['liveInCurrent']
                    if e['classification'] == 'CODE-NET-NEW' and prof['gateCodeNetNew'] \
                            and not (prof['newWaiverSuppressesCodeNetNew'] and wc):
                        e['gates'] = True
                        e['gateReason'] = 'code-net-new' if live else 'code-net-new-policy-hidden'
                    elif (prof['gateNewlyLiveByPolicyAxes'] and live
                          and e['classification'] in ('POLICY-DELTA', 'SCOPE-DELTA', 'WAIVER-DELTA')
                          and e['direction'] in ('appeared', 'waiver-removed')):
                        e['gates'], e['gateReason'] = True, 'newly-live-policy-axis'
                    elif prof['gateAllCurrentLive'] and live:
                        e['gates'], e['gateReason'] = True, 'current-live'
        if why is not None:
            e = {k: v for k, v in e.items() if k not in ('direction', 'gateReason')}
            e.update(classification='INDETERMINATE', indeterminateReason=why, gates=False,
                     subsequentDeltas=[])
            gating_unknown = gating_unknown or under
        entries.append(e)
    counts = {k: 0 for k in CLASSES}
    for e in entries:
        counts[e['classification']] += 1
    counts['gating'] = sum(1 for e in entries if e['gates'])
    rdefs = []
    for r in sorted(cpol['rules'], key=lambda r: r['ruleId'].encode()):
        if not r['enabled']:
            continue
        rr = cur['ruleResults'].get(r['ruleId'], {})
        found = []
        if any(u['requirement'] == 'required' and u['kind'] not in cur_kinds
               for u in r['evidenceUse']):
            found.append('required-evidence-unavailable')
        if rr.get('outcome') == 'indeterminate':
            found.append('required-coverage-unknown')
        if rr.get('enumerationState') not in (None, 'complete') or rr.get('unresolvedSubjects') \
                or any(not f['matched'] for f in cur['findings'] if f['ruleId'] == r['ruleId']):
            found.append('correspondence-incomplete')
        rdefs += [{'ruleId': r['ruleId'], 'gating': gating(cpol, r['ruleId']), 'cause': c}
                  for c in sorted(found)]
    corr = []
    for r in sorted(cpol['rules'], key=lambda r: r['ruleId'].encode()):
        mine = [f for f in cur['findings'] if f['ruleId'] == r['ruleId']]
        rr = cur['ruleResults'].get(r['ruleId'], {})
        corr.append({'ruleId': r['ruleId'], 'gating': gating(cpol, r['ruleId']),
                     'matchedCount': len([f for f in mine if f['matched']]),
                     'unmatchedCount': len([f for f in mine if not f['matched']]),
                     'populationUnknown': bool(r['enabled'] and (
                         rr.get('enumerationState') not in (None, 'complete')
                         or rr.get('unresolvedSubjects'))),
                     'zeroFindings': len(mine) == 0})
    unmatched = list(bd['unmatchedOccurrences']) + [
        {'side': 'current', 'findingId': f['findingId'], 'ruleId': f['ruleId'],
         'subjectId': f['subjectId'], 'subjectPath': f['subjectPath'], 'severity': f['severity'],
         'waived': f['waived']} for f in cur['findings'] if not f['matched']]
    verdict = ('fail' if counts['gating'] else
               'indeterminate' if (gating_unknown or any(d['gating'] for d in rdefs)
                                   or cur['executionDeficiencies']) else 'pass')
    out.update(entries=entries, counts=counts, verdict=verdict, ruleDeficiencies=rdefs,
               unmatchedOccurrences=sorted(unmatched, key=lambda u: (u['side'], u['findingId'])),
               correspondenceCoverage=corr)
    return out


FIELDS = ('comparisonPerformed', 'baselineContext', 'currentContext', 'contextDelta',
          'pivotsAvailable', 'detectors', 'projectCorrespondence', 'entries', 'counts', 'verdict',
          'ruleDeficiencies', 'unmatchedOccurrences', 'correspondenceCoverage',
          'currentEvaluationState', 'currentExecutionDeficiencies')


def pointer(doc, ptr):
    node = doc
    for part in [p for p in (ptr or '').split('/') if p]:
        node = node[part]
    return node


def check_scenario(sc, real):
    rows = []

    def f(cond, check, detail=None):
        rows.append({'check': check, 'result': 'PASS' if cond else 'REFUSE', 'detail': detail})
        return bool(cond)
    where = {'scenario': sc['scenario']}
    labels = set(sc.get('syntheticHelperOnly') or [])
    for side in ('baselineSide', 'currentSide'):
        if sc['realSides'].get(side):
            rebind_real(sc[side], real, dict(where, side=side), f)
        else:
            f(side in labels, 'NON_REAL_SIDE_IS_LABELLED_SYNTHETIC_HELPER_ONLY', dict(where, side=side))
    base_doc = json.load(open(OUT + '/' + sc['baselineRef']['file']))
    baseline = pointer(base_doc, sc['baselineRef'].get('pointer'))
    rebuilt = rebuild_baseline(sc['baselineSide'], sc.get('overrideDocuments'))
    f(K.C(rebuilt) == K.C(baseline['descriptor']), 'BASELINE_DESCRIPTOR_REBUILT_FROM_PREMISES_EQUALS',
      None if K.C(rebuilt) == K.C(baseline['descriptor']) else
      sorted(k for k in rebuilt if K.C(rebuilt[k]) != K.C(baseline['descriptor'].get(k))))
    f(K.ID('workflow.baseline', baseline['descriptor']) == baseline['baselineId'],
      'BASELINE_ID_RECOMPUTES')
    adm = S.admit(BASE_DOC, '#', baseline, 'indep-cmp:baseline')
    f(adm['admitted'], 'BASELINE_READMITTED_BY_ITS_OWNING_SCHEMA',
      adm['stockSchemaErrors'][:2] + adm['publishedKeywordRefusals'][:2])
    rec_doc = json.load(open(OUT + '/' + sc['recordRef']['file']))
    rec = pointer(rec_doc, sc['recordRef'].get('pointer'))
    adm = S.admit(CMP_DOC, '#', rec, 'indep-cmp:record')
    f(adm['admitted'], 'COMPARISON_READMITTED_BY_ITS_OWNING_SCHEMA',
      adm['stockSchemaErrors'][:2] + adm['publishedKeywordRefusals'][:2])
    f(K.ID('workflow.comparison', rec['descriptor']) == rec['comparisonResultId'],
      'COMPARISON_ID_RECOMPUTES')
    d = rec['descriptor']
    f(d['baselineId'] == baseline['baselineId'] and d['currentRunId'] == sc['currentSide']['runId']
      and d['currentSnapshotId'] == sc['currentSide']['snapshotId']
      and d['auditProfile'] == sc['auditProfileRecord'],
      'RECORD_BINDS_THE_PREMISE_BASELINE_CURRENT_SIDE_AND_PROFILE')
    try:
        derived = rederive(sc, baseline)
    except Refused as e:
        f(False, 'PREMISES_REFUSED_BY_THE_LAW', str(e))
        return rows, None
    for k in FIELDS:
        f(K.C(derived[k]) == K.C(d[k]), 'DERIVED_%s_EQUALS_THE_RECORD' % k,
          None if K.C(derived[k]) == K.C(d[k]) else {'derived': derived[k], 'record': d[k]})
    if not derived['comparisonPerformed']:
        f(d.get('wholeIndeterminateReason') == derived['wholeIndeterminateReason']
          and (d.get('remedy') or {}).get('code') == derived['remedyCode'],
          'DERIVED_WHOLE_INDETERMINATE_REASON_AND_REMEDY_CODE_EQUAL_THE_RECORD')
    return rows, derived


def main():
    premises = json.load(open(OUT + '/vectors/comparison-premises.json'))
    real = real_ts_side()
    out = {'standing': __doc__, 'scenarios': []}
    failed = []
    for sc in premises['scenarios']:
        rows, derived = check_scenario(sc, real)
        refusals = [r for r in rows if r['result'] != 'PASS']
        out['scenarios'].append({'scenario': sc['scenario'], 'requirements': sc['requirements'],
                                 'realSides': sc['realSides'],
                                 'syntheticHelperOnly': sc.get('syntheticHelperOnly'),
                                 'checks': len(rows), 'refusals': refusals,
                                 'result': 'PASS' if not refusals else 'REFUSE',
                                 'derived': derived})
        if refusals:
            failed.append(sc['scenario'])
        print('%-44s checks %-3d refused %d%s' % (sc['scenario'], len(rows), len(refusals),
                                                  '' if not refusals else '  first ' +
                                                  json.dumps(refusals[0], default=str)[:300]))
    out['summary'] = {'scenarios': len(out['scenarios']), 'failed': failed}
    with open(OUT + '/vectors/indep-comparison-law.json', 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    raise SystemExit(1 if failed else 0)


if __name__ == '__main__':
    main()
