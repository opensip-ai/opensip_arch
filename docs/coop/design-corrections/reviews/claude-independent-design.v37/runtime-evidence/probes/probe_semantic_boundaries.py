"""Independent semantic probes over actual source37 reference owners (verified exact copy).

P-CROSS  cross-unit claim: evaluator proof witnesses and the public graph query project the same retained
         references facts, per subject, across two native universes (no cross-universe union either side).
P-TARGET target/proof boundary: target-side (incoming) predicate values versus the graph query's incoming
         result and disclosures; a query result is never read as proof.
P-REMINT fully reminted false-result graphs: every identity (witness blobs, proof, evidence, seal, Run) is
         re-minted so structural owner closure (open_run_closure) admits, but complete replay
         (close_run), the public graph query and the public SEAL adapter must refuse.
P-CAUSE  whole-Run cause order: retained deficiency population of an actual closed indeterminate Run, its
         D9 routability, and the number of distinct schema-valid terminations that equally lawful
         pre-reduction orders produce for the same sealed Run.

Reference evidence only. Synthetic native-admitted inputs; not compiler/provider/product qualification.
"""
import copy, hashlib, importlib.util, json, sys, traceback

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v37'
SRC = BASE + '/work/source37'
DC = SRC + '/docs/coop/design-corrections'
OUT = BASE + '/receipts/probe-semantic-boundaries.json'


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


SR = load('p37_semantic_replay', DC + '/foundation/check-semantic-replay.v3.py')
S, R, E, M, C = SR.S, SR.R, SR.E, SR.M, SR.C
Q = load('p37_query', DC + '/workflows/query_projection_model.v3.py')
D9 = json.load(open(SRC + '/docs/coop/artifacts/d9-exit-contract.v1.14.json'))
REQ_ID = 'req1_' + '7' * 32
res = {'standing': 'independent reviewer probe; reference evidence only; not qualification'}


def host(**kw):
    h = {'requestId': REQ_ID}
    h.update(kw)
    return h


def ep(universe, kind, nid, manifest=None):
    e = {'universe': universe, 'kind': kind, 'nativeSubjectId': nid}
    if manifest is not None:
        e['packageManifestPath'] = manifest
    return e


def req(op, project, view, params, completeness='required', size=1000):
    return {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'projectId': project, 'view': view,
            'operation': op, 'params': params, 'completeness': completeness, 'page': {'size': size}}


def attempt(fn):
    try:
        return {'result': 'ADMIT', 'value': fn()}
    except Q.QueryRefusal as e:
        env = e.envelope()
        return {'result': 'REFUSE', 'errorCode': e.error_code, 'detail': e.detail, 'class': e.klass,
                'exitCode': env['exitCode'], 'subject': str(e.subject)[:200] if e.subject else None}
    except Exception as e:  # noqa: BLE001 - recorded, never swallowed silently
        return {'result': 'REFUSE-OR-ERROR', 'type': type(e).__name__, 'error': str(e).split('\n')[0][:300]}


def proof_of(run, objects):
    return objects[objects[run['evaluationSealId']][1]['proofBundleId']][1]


def witness(blobs, digest):
    return C.parse(blobs[digest])


def root_predicates(run, objects):
    return {p['subjectId']: p for p in proof_of(run, objects)['predicateProofs'] if p['predicateId'] == 'p'}


# ------------------------------------------------------------------ P-CROSS / P-TARGET
def parity(label, graph_kw, direction):
    g = S.build_ts_semantic_graph(**graph_kw)
    run, objects, blobs, actual = SR.close_positive(g)
    rid = actual['runId']
    roots = root_predicates(run, objects)
    rows = []
    mismatches = []
    for item in [i for i in g['inputs']['population'].values() if i['kind'] == 'symbol']:
        sid = item['subjectId']
        if sid not in roots:
            continue
        pr = roots[sid]
        w = witness(blobs, pr['witnessDigest'])
        nid = item['row']['nativeSubjectId']
        r = req('graph.neighbors', run['projectId'], {'runId': rid}, {
            'relation': 'references', 'minResolution': 'resolved-binding', 'direction': direction,
            'endpoint': ep(item['universe'], 'symbol', nid)})
        out = attempt(lambda: Q.execute_graph_query(r, run, objects, blobs, host=host()))
        row = {'universe': item['universe'][:12], 'nativeSubjectId': nid, 'predicateValue': pr['value'],
               'witnessMatchingFactIds': sorted(w['matchingFactIds']),
               'witnessUncertainFactIds': sorted(w['uncertainFactIds']),
               'witnessDeficiencyCauses': sorted({d['cause'] for d in w['deficiencies']})}
        if out['result'] == 'ADMIT':
            v = out['value']
            q_ids = sorted(x['factId'] for x in v['items'])
            universes = sorted({(x['source']['universe'][:12], x['target']['universe'][:12]) for x in v['items']})
            lim = sorted({x['kind'] for x in v['context']['evidence']['resolutionLimitations']})
            row.update({'queryFactIds': q_ids, 'queryEdgeUniverses': universes,
                        'queryTraversal': v['context']['traversalCoverage'], 'queryCountBasis': v['context']['countBasis'],
                        'queryTermination': v['termination']['class'], 'queryLimitationKinds': lim})
            known_match = set(q_ids) == set(w['matchingFactIds'])
            # parity law under test: the query's known projected facts equal the witness's known matching facts;
            # uncertain witness facts must never appear as known query rows.
            if not known_match or set(q_ids) & set(w['uncertainFactIds']):
                mismatches.append(nid)
            if pr['value'] == 'indeterminate' and not lim:
                mismatches.append(nid + ':indeterminate-proof-without-query-disclosure')
            row['cross_universe_edge'] = any(a != b for a, b in universes)
        else:
            row['query'] = out
        rows.append(row)
    return {'label': label, 'runId': rid, 'verdict': actual['verdict'], 'findingCount': actual['findingCount'],
            'rows': rows, 'mismatches': mismatches, 'passed': not mismatches}


try:
    res['P-CROSS'] = parity('source-side references, two universes', dict(
        atom=SR.REFS_EXISTS_SRC, has_declares=False, has_references_fact=True, second_partition=True,
        second_universe=True, references_resolved=True, incoming_search=True, incoming_complete=True,
        target_sidecar=True, cross_u_binding='foo'), 'outgoing')
except Exception as e:
    res['P-CROSS'] = {'error': type(e).__name__ + ': ' + str(e)[:400], 'tb': traceback.format_exc()[-1500:]}
try:
    res['P-TARGET-complete'] = parity('target-side incoming, complete search, two universes', dict(
        atom=SR.REFS_EXISTS_TGT, has_declares=False, has_references_fact=True, second_partition=True,
        second_universe=True, references_resolved=True, incoming_search=True, incoming_complete=True,
        target_sidecar=True, cross_u_binding='foo'), 'incoming')
    res['P-TARGET-incomplete'] = parity('target-side incoming, incomplete search', dict(
        atom=SR.REFS_NONE_TGT, has_declares=False, has_references_fact=True, second_partition=True,
        references_resolved=False, incoming_search=True, incoming_complete=False, target_sidecar=True), 'incoming')
except Exception as e:
    res['P-TARGET-error'] = {'error': type(e).__name__ + ': ' + str(e)[:400], 'tb': traceback.format_exc()[-1500:]}


# ------------------------------------------------------------------ P-REMINT
def remint(run, objects, blobs, flip):
    """flip(pred) -> new value or None. Re-mint witness blobs, proof, evidence, seal and Run consistently."""
    run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
    seal = copy.deepcopy(objects[run['evaluationSealId']][1])
    proof = copy.deepcopy(objects[seal['proofBundleId']][1])
    evidence = copy.deepcopy(objects[run['evidenceId']][1])
    changed = 0
    for p in proof['predicateProofs']:
        new = flip(p)
        if new is None or new == p['value']:
            continue
        w = witness(blobs, p['witnessDigest'])
        w['matchingFactIds'] = []
        w['uncertainFactIds'] = []
        w['deficiencies'] = []
        raw = C.canonical(w)
        d = hashlib.sha256(raw).hexdigest()
        blobs[d] = raw
        p['witnessDigest'] = d
        p['value'] = new
        changed += 1
    proof['findingIds'] = []
    proof['waivedFindingIds'] = []
    for rr in proof['ruleResults']:
        rr['findingIds'] = []
        rr['deficiencies'] = []
        if rr['outcome'] in ('fail', 'indeterminate'):
            rr['outcome'] = 'pass'
    proof['executionDeficiencies'] = []
    proof['verdict'] = 'pass'
    pid = M.identifier('proof-bundle', proof)
    objects[pid] = ('proof-bundle', proof)
    evidence['findingIds'] = []
    evidence['proofBundleId'] = pid
    eid = M.identifier('semantic-evidence', evidence)
    objects[eid] = ('semantic-evidence', evidence)
    seal['proofBundleId'] = pid
    seal['evidenceId'] = eid
    seal['verdict'] = 'pass'
    sid = M.identifier('evaluation-seal', seal)
    objects[sid] = ('evaluation-seal', seal)
    run['evidenceId'] = eid
    run['evaluationSealId'] = sid
    return run, objects, blobs, changed


def remint_case(label, case_fn, flip, query_endpoint_fn):
    g, (run, objects, blobs), actual = case_fn()
    mrun, mobj, mblob, changed = remint(run, objects, blobs, flip)
    row = {'label': label, 'original': {'runId': actual['runId'], 'verdict': actual['verdict'],
                                         'findingCount': actual['findingCount']},
           'predicatesFlipped': changed}
    try:
        rid, _owner = M.open_run_closure(mrun, mobj, mblob)
        row['structuralOwnerClosure'] = {'result': 'ADMIT', 'remintedRunId': rid, 'differsFromOriginal': rid != actual['runId']}
    except Exception as e:
        row['structuralOwnerClosure'] = {'result': 'REFUSE', 'error': str(e)[:300]}
    for name, fn in (('completeReplay', lambda: R.replay(mrun, mobj, mblob)),
                     ('close_run', lambda: M.close_run(mrun, mobj, mblob))):
        try:
            fn()
            row[name] = {'result': 'ADMIT'}
        except Exception as e:
            row[name] = {'result': 'REFUSE', 'type': type(e).__name__, 'error': str(e).split('\n')[0][:200]}
    universe, nid = query_endpoint_fn(g)
    r = req('graph.neighbors', mrun['projectId'], {'runId': row['structuralOwnerClosure'].get('remintedRunId', 'run3:' + '0' * 64)},
            {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing',
             'endpoint': ep(universe, 'symbol', nid)})
    q = attempt(lambda: Q.execute_graph_query(r, mrun, mobj, mblob, host=host()))
    if q['result'] == 'ADMIT':
        q = {'result': 'ADMIT', 'items': len(q['value']['items'])}
    row['publicGraphQuery'] = q
    # The public SEAL adapter (security_lifecycle_model_v1.admit_analysis_seal) is NOT executed here; by source
    # reading it delegates to identity-model.v3.close_run, whose refusal is recorded above.
    row['discriminates'] = (row['structuralOwnerClosure']['result'] == 'ADMIT' and row['completeReplay']['result'] == 'REFUSE'
                            and row['close_run']['result'] == 'REFUSE' and q['result'] == 'REFUSE')
    return row


def first_symbol(g):
    s = [i for i in g['inputs']['population'].values() if i['kind'] == 'symbol']
    return s[0]['universe'], s[0]['row']['nativeSubjectId']


res['P-REMINT'] = []
for label, fn, flip in (
        ('fail-to-pass: known findings erased (declares-exists)', SR.case_declares_exists,
         lambda p: 'false' if p['value'] == 'true' else None),
        ('indeterminate-to-pass: unknown laundered to known-false (incoming incomplete)', SR.case_incoming_incomplete_unknown,
         lambda p: 'false' if p['value'] == 'indeterminate' else None),
        ('execution-deficiency erased: missing required inventory to pass', SR.case_missing_inventory_execution,
         lambda p: None)):
    try:
        res['P-REMINT'].append(remint_case(label, fn, flip, first_symbol))
    except Exception as e:
        res['P-REMINT'].append({'label': label, 'error': type(e).__name__ + ': ' + str(e)[:400],
                                'tb': traceback.format_exc()[-1500:]})


# ------------------------------------------------------------------ P-CAUSE
def cause_probe():
    g, (run, objects, blobs), actual = SR.case_incoming_incomplete_unknown()
    _, owner = M.open_run_closure(run, objects, blobs)
    seal = objects[run['evaluationSealId']][1]
    proof = objects[seal['proofBundleId']][1]
    normalized, atom_inputs = R.I.reconstruct(run['planId'], seal['executionPlanId'], seal['evaluatorClosure'],
                                              proof['evaluationInputRefs'], objects, blobs, owner, M)
    cov = atom_inputs['coverages']
    entries = [{'coverageId': cid, 'deficiency': v['entry'].get('deficiency'), 'nativeCause': v['entry'].get('nativeCause')}
               for cid, v in sorted(cov.items())]
    retained = []
    for rr in proof['ruleResults']:
        for d in rr['deficiencies']:
            retained.append({'plane': 'ruleResult', 'ruleId': rr['ruleId'], 'source': d['source'], 'cause': d['cause'],
                             'nativeCause': d.get('nativeCause'),
                             'coverageRefs': ['coverage2:' + x['digest'] for x in d['inputRefs'] if x['domain'] == 'coverage']})
    for d in proof['executionDeficiencies']:
        retained.append({'plane': 'execution', 'source': d['source'], 'cause': d['cause'], 'coverageRefs': []})
    dmap = D9['codeMaps']['deficiencyToReasonCode']
    bridge4 = {'input-closure-incomplete', 'resolution-incomplete', 'external-consumers-unknown', 'derivation-policy-unmet'}

    def route(cause):
        if cause in dmap:
            return dmap[cause], 'd9-member'
        if cause in bridge4:
            return 'VERDICT.INDETERMINATE', 'native-bridge'
        return None, 'no-owner-route'
    for r in retained:
        r['reasonCode'], r['routeOwner'] = route(r['cause'])
    unique_causes = []
    for r in retained:
        if r['cause'] not in [u['cause'] for u in unique_causes]:
            unique_causes.append(r)
    # Candidate lawful pre-reduction orders. None is selected by any owner (native section 10 disclaims it).
    PREC = ['language-tier-unsupported', 'provider-unavailable', 'input-closure-incomplete', 'budget-exhausted',
            'confidence-floor-unmet', 'derivation-policy-unmet', 'resolution-incomplete', 'external-consumers-unknown',
            'required-relation-missing']
    orders = {
        'retained-canonical-proof-order': list(retained),
        'native-precedence-first': sorted(retained, key=lambda r: PREC.index(r['cause']) if r['cause'] in PREC else len(PREC)),
        'execution-obligations-first': sorted(retained, key=lambda r: 0 if r['plane'] == 'execution' else 1),
        'reverse-observation': list(reversed(retained)),
    }
    terms = {}
    for name, seq in orders.items():
        codes = []
        primary = None
        for r in seq:
            if r['reasonCode'] is None:
                continue
            if primary is None:
                primary = r
            if r['reasonCode'] not in codes:
                codes.append(r['reasonCode'])
        codes = codes[:9] or ['VERDICT.INDETERMINATE']
        t = {'class': 'indeterminate', 'reasonCodes': codes, 'runId': actual['runId']}
        if primary and primary['coverageRefs']:
            t['coverageId'] = primary['coverageRefs'][0]
        try:
            Q.validate_schema(Q.COMMON_ID + '#/$defs/StepTermination', t)
            t_valid = True
        except Exception as e:
            t_valid = 'INVALID:' + str(e).split('\n')[0][:160]
        terms[name] = {'termination': t, 'schemaValid': t_valid, 'primaryCause': primary and primary['cause']}
    distinct = sorted({json.dumps(v['termination'], sort_keys=True) for v in terms.values()})
    # the verdict-only projection of workflows_model.analysis_termination for the same Run
    W = None
    try:
        W = load('p37_workflows_model', DC + '/workflows/workflows_model.v1.py')
        wterm = W.analysis_termination({'verdict': actual['verdict'], 'requiredCoverage': 'unsatisfied', 'runId': actual['runId']}, 'self')
    except Exception as e:
        wterm = 'NOT-ASSESSED:' + type(e).__name__ + ':' + str(e)[:200]
    # native stage contribution over the same retained Coverage entries
    try:
        N = load('p37_native_model', DC + '/native/native_evidence_model.v2.py')
        stage = N.run_termination({'authority': 'authoritative', 'd9': {'class': 'success', 'exitCode': 0, 'code': None}},
                                  [{'deficiency': e['deficiency'], 'nativeCause': e['nativeCause']} for e in entries])
    except Exception as e:
        stage = 'NOT-ASSESSED:' + type(e).__name__ + ':' + str(e)[:200]
    return {'run': {'runId': actual['runId'], 'verdict': actual['verdict'], 'findingCount': actual['findingCount']},
            'retainedCoverageEntries': entries,
            'deficientCoverageRecords': sum(1 for e in entries if e['deficiency']),
            'retainedDeficiencies': retained,
            'causesWithoutAnyOwnerRoute': sorted({r['cause'] for r in retained if r['reasonCode'] is None}),
            'candidateTerminations': terms,
            'distinctSchemaValidTerminationsForOneSealedRun': len(distinct),
            'workflowsModelAnalysisTermination': wterm,
            'nativeStageRunTermination': stage,
            'retainedOrderIsCanonicalSet': all(rr['deficiencies'] == E.cset(rr['deficiencies']) for rr in proof['ruleResults'])}


try:
    res['P-CAUSE'] = cause_probe()
except Exception as e:
    res['P-CAUSE'] = {'error': type(e).__name__ + ': ' + str(e)[:400], 'tb': traceback.format_exc()[-2500:]}

json.dump(res, open(OUT, 'w'), indent=1, default=str)
summary = {
    'P-CROSS': res.get('P-CROSS', {}).get('passed', res.get('P-CROSS')),
    'P-TARGET-complete': res.get('P-TARGET-complete', {}).get('passed'),
    'P-TARGET-incomplete': res.get('P-TARGET-incomplete', {}).get('passed'),
    'P-REMINT': [(r.get('label'), r.get('discriminates'), r.get('error')) for r in res['P-REMINT']],
    'P-CAUSE-distinct': res.get('P-CAUSE', {}).get('distinctSchemaValidTerminationsForOneSealedRun', res.get('P-CAUSE')),
}
print(json.dumps(summary, indent=1, default=str))
