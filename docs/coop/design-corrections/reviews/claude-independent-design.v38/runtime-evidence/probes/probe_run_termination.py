"""Independent whole-Run termination probe over newly frozen source38 bytes (verified probe copy).

IND   an independent derivation written from run-termination-contract.v1.md sections 3-5 (not the author model) is
      compared with run_termination_model.finalize over actually closed Runs, including variants the goldens omit.
PERM  host discovery order and object-map order do not change the derived projection.
NAT   native run_termination helper on a stage/entry-disagreement Run (contract section 5 claim).
FALSE a structurally admitted, semantically false Run has no termination (close_run refuses).
PROJ  check_projection boundary: schema-valid alternatives refuse; a shape-valid but unrelated delegated detail is
      only owner-validation-required.
BRIDGE total cause bridge over the evaluator registry; unregistered cause refused; mixed synthetic conditions
      outside retained goldens (requirement-relative, input-closure) ordered by section 4.
Reference evidence only.
"""
import copy, hashlib, importlib.util, itertools, json, random, sys, traceback

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v38'
SRC = RT + '/work/source38-pkg'
DC = SRC + '/docs/coop/design-corrections'
OUT = RT + '/receipts/probe-run-termination.json'


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


SR = load('rt38_semantic', DC + '/foundation/check-semantic-replay.v3.py')
T = load('rt38_termination', DC + '/foundation/run_termination_model.v1.py')
Q = load('rt38_query', DC + '/workflows/query_projection_model.v3.py')
N = T.N
C = SR.C
D9 = json.load(open(SRC + '/docs/coop/artifacts/d9-exit-contract.v1.14.json'))
IDS = json.load(open(DC + '/foundation/identity-schemas.v3.json'))
REG = IDS['x-opensip-evaluator-deficiency-registry']
CODE = D9['codeMaps']['deficiencyToReasonCode']
# native-evidence.md section 10 precedence and bridge, transcribed from the contract text (lines 2857-2860, 2920-2924)
PREC = ['language-tier-unsupported', 'provider-unavailable', 'input-closure-incomplete', 'budget-exhausted',
        'confidence-floor-unmet', 'derivation-policy-unmet', 'resolution-incomplete', 'external-consumers-unknown',
        'required-relation-missing']
BRIDGED = {'input-closure-incomplete', 'resolution-incomplete', 'external-consumers-unknown', 'derivation-policy-unmet'}
STAGE = {'budget-exhausted': 'budget-exhausted', 'unavailable': 'provider-unavailable'}
res = {'standing': 'independent reviewer probe; reference evidence only'}


def ind_route(cause):
    if cause in PREC:
        return PREC.index(cause), ('verdict-indeterminate' if cause in BRIDGED else cause)
    if cause == 'work-budget-exhausted':
        return 3, 'budget-exhausted'
    if cause not in {c for m in REG['sources'].values() for c in m}:
        raise ValueError('unregistered ' + cause)
    return 9, 'verdict-indeterminate'


def ind_derive(run, objects, blobs):
    """Independent section 3-5 derivation over already closed retained content (caller closed the Run)."""
    seal = objects[run['evaluationSealId']][1]
    proof = objects[seal['proofBundleId']][1]
    plan = objects[run['planId']][1]
    policy = C.parse(blobs[plan['policyDigest']])
    rules = {r['ruleId']: r for r in policy['rules']}
    if proof['verdict'] == 'pass':
        return {'class': 'success', 'runId': None}
    if proof['verdict'] == 'fail':
        return {'class': 'policy-failed', 'runId': None}
    preds = {(p['ruleId'], p['subjectId'], p['predicateId']): p for p in proof['predicateProofs']}
    xi = [r for r in proof['evaluationInputRefs'] if r['domain'] == 'execution-inputs']
    assert len(xi) == 1
    xi = xi[0]

    def blocking(rid, sid, pid):
        node = preds[(rid, sid, pid)]
        if node['value'] != 'indeterminate':
            return []
        w = C.parse(blobs[node['witnessDigest']])
        if w['kind'] != 'boolean':
            return list(w['deficiencies'])
        out = []
        for child in w['childPredicateIds']:
            out.extend(blocking(rid, sid, child))
        return out

    def blocks(rule, d):
        if d['cause'] in REG['nonBlockingDisclosures']:
            return False
        if d['source'] == 'correspondence':
            return False
        if d['source'] == 'import':
            return d['evidenceKind'] in {u['kind'] for u in rule['evidenceUse'] if u['requirement'] == 'required'}
        return True

    pop = list(proof['executionDeficiencies'])
    for rr in proof['ruleResults']:
        if rr['outcome'] != 'indeterminate':
            continue
        rule = rules[rr['ruleId']]
        for d in rr['deficiencies']:
            if d['source'] == 'enumeration' or (d['source'] == 'import' and d['subjectId'] is None and d['predicateId'] is None) \
                    or (d['source'] == 'execution' and d['cause'] == 'work-budget-exhausted'):
                pop.append(d)
        for sid in rr['enumeration']['selectedSubjectIds']:
            if (rr['ruleId'], sid, 'p') in preds:
                pop.extend(d for d in blocking(rr['ruleId'], sid, 'p') if blocks(rule, d))
    conds = []
    for d in pop:
        rank, d9 = ind_route(d['cause'])
        if d['source'] == 'execution':
            orig = [r for r in d['inputRefs'] if r != xi and r['domain'] == 'coverage']
        elif d['source'] == 'native' and len(d['inputRefs']) == 1 and d['inputRefs'][0]['domain'] == 'coverage':
            orig = list(d['inputRefs'])
        else:
            orig = []
        declared = []
        for r in orig:
            cid = 'coverage2:' + r['digest']
            entry = C.parse(blobs[objects[cid][1]['payloadDigest']])['entry']
            if entry['deficiency'] == d['cause']:
                declared.append(cid)
            st = entry['resolutionCompleteness']['stageTerminal']
            if st in STAGE:
                srank, sd9 = ind_route(STAGE[st])
                conds.append((srank, sd9, [], [cid]))
        conds.append((rank, d9, declared, []))
    least = {}
    for rank, d9, _, _ in conds:
        least[d9] = min(least.get(d9, 99), rank)
    order = sorted(least, key=lambda k: least[k])
    pr = least[order[0]]
    dec = sorted({c for r, _, ds, _ in conds if r == pr for c in ds}, key=str.encode)
    stg = sorted({c for r, _, _, ss in conds if r == pr for c in ss}, key=str.encode)
    term = {'class': 'indeterminate', 'reasonCodes': [CODE[d] for d in order]}
    carrier = (dec or stg or [None])[0]
    if carrier:
        term['coverageId'] = carrier
    return term, len(pop), len(conds)


def validate_shape(t):
    Q.validate_schema(Q.COMMON_ID + '#/$defs/StepTermination', t)


REFS_NONE_TGT = SR.REFS_NONE_TGT
BASE = dict(atom=REFS_NONE_TGT, has_declares=False, has_references_fact=True, second_partition=True, references_resolved=False,
            incoming_search=True, incoming_complete=False, target_sidecar=True)
VARIANTS = [
    ('base-incoming-incomplete', dict(BASE)),
    ('foo-budget-bar-unavailable', dict(BASE, references_stage_terminals={'foo': 'budget-exhausted', 'bar': 'unavailable'})),
    ('bar-budget-only', dict(BASE, references_stage_terminals={'bar': 'budget-exhausted'})),
    ('foo-provider-fault', dict(BASE, references_stage_terminals={'foo': 'provider-fault'})),
    ('foo-cancelled', dict(BASE, references_stage_terminals={'foo': 'cancelled'})),
    ('foo-complete-terminal', dict(BASE, references_stage_terminals={'foo': 'complete'})),
    ('work-budget-both-stages', dict(BASE, budget_limit=1, references_stage_terminals={'foo': 'budget-exhausted', 'bar': 'unavailable'})),
    ('work-budget-bar-unavailable', dict(BASE, budget_limit=1, references_stage_terminals={'bar': 'unavailable'})),
    ('declares-pass-or-fail', dict(atom=SR.DECLARES, has_declares=True)),
    ('complete-empty-reference', dict(atom=SR.REFS_EXISTS_SRC, has_declares=False, has_references_fact=False, second_partition=True)),
    ('missing-inventory', dict(atom=SR.REFS_EXISTS_SRC, has_declares=False, has_references_fact=False, second_partition=True,
                               complete_required_inventory=False)),
]
ind_rows = []
built = {}
for label, params in VARIANTS:
    row = {'variant': label}
    try:
        g = SR.S.build_ts_semantic_graph(**params)
        run, objects, blobs, actual = SR.close_positive(g)
        built[label] = (run, objects, blobs)
        fin = T.finalize(run, objects, blobs)
        author = fin['termination']
        ind = ind_derive(run, objects, blobs)
        if isinstance(ind, tuple):
            ind_term, npop, ncond = ind
            ind_term = dict(ind_term, runId=actual['runId'])
        else:
            ind_term, npop, ncond = dict(ind, runId=actual['runId']), 0, 0
        row.update({'runId': actual['runId'], 'verdict': actual['verdict'], 'author': author, 'independent': ind_term,
                    'equal': author == ind_term, 'population': npop, 'conditions': ncond,
                    'schemaValid': Q.validate_schema(Q.COMMON_ID + '#/$defs/StepTermination', author) is not None})
        if author.get('coverageId'):
            e = C.parse(blobs[objects[author['coverageId']][1]['payloadDigest']])['entry']
            row['carrierEntry'] = {'deficiency': e['deficiency'], 'stageTerminal': e['resolutionCompleteness']['stageTerminal'],
                                   'state': e['resolutionCompleteness']['state']}
        if fin['reduction']:
            _, _, popl, ctx = T.retained_population(run, objects, blobs)
            conds = T.conditions(popl, objects, blobs, ctx['xi'])
            row['permutation'] = T.permutation_invariance(conds)
            # object-map order and population shuffles
            rnd = random.Random(38)
            keys = list(objects)
            rnd.shuffle(keys)
            shuffled = {k: objects[k] for k in keys}
            p2 = list(popl)
            rnd.shuffle(p2)
            row['shuffledObjectsSame'] = T.finalize(run, shuffled, blobs)['termination'] == author
            row['shuffledPopulationSame'] = {k: T.reduce(T.conditions(p2, objects, blobs, ctx['xi']))[k] for k in ('reasonCodes', 'coverageId')} == \
                {k: fin['reduction'][k] for k in ('reasonCodes', 'coverageId')}
    except Exception as exc:
        row['error'] = type(exc).__name__ + ': ' + str(exc)[:300]
        row['tb'] = traceback.format_exc()[-1200:]
    ind_rows.append(row)
res['IND'] = ind_rows

# NAT: native helper on the stage/entry disagreement Run
try:
    run, objects, blobs = built['foo-budget-bar-unavailable']
    fin = T.finalize(run, objects, blobs)
    entries, nat = [], []
    for cid in sorted(objects):
        if objects[cid][0] != 'coverage':
            continue
        e = C.parse(blobs[objects[cid][1]['payloadDigest']])['entry']
        st = e['resolutionCompleteness']['stageTerminal']
        term_kind = {'budget-exhausted': 'budget-exhausted', 'unavailable': 'unavailable'}.get(st)
        if term_kind:
            out = N.run_termination({'authority': 'authoritative', 'terminalKind': term_kind, 'd9': {'class': 'success', 'exitCode': 0, 'code': None}},
                                    [{'deficiency': e['deficiency'], 'nativeCause': e.get('nativeCause')}])
            nat.append({'coverageId': cid, 'stageTerminal': st, 'entryDeficiency': e['deficiency'], 'helperCode': out['d9']['code'],
                        'helperTypedDetail': (out.get('typedDetail') or {}).get('deficiency')})
    res['NAT'] = {'runTermination': fin['termination'], 'stageRecords': nat}
except Exception as exc:
    res['NAT'] = {'error': repr(exc), 'tb': traceback.format_exc()[-1200:]}

# FALSE: reminted semantically false Run has no termination
try:
    gi, (run, objects, blobs), acti = SR.case_incoming_incomplete_unknown()
    M = T.M
    r2, o2, b2 = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
    seal = copy.deepcopy(o2[r2['evaluationSealId']][1])
    proof = copy.deepcopy(o2[seal['proofBundleId']][1])
    ev = copy.deepcopy(o2[r2['evidenceId']][1])
    for p in proof['predicateProofs']:
        if p['value'] == 'indeterminate':
            w = C.parse(b2[p['witnessDigest']])
            w.update(matchingFactIds=[], uncertainFactIds=[], deficiencies=[])
            raw = C.canonical(w)
            d = hashlib.sha256(raw).hexdigest()
            b2[d] = raw
            p.update(witnessDigest=d, value='false')
    for rr in proof['ruleResults']:
        rr.update(deficiencies=[], outcome='pass' if rr['outcome'] == 'indeterminate' else rr['outcome'])
    proof.update(executionDeficiencies=[], verdict='pass')
    pid = M.identifier('proof-bundle', proof)
    o2[pid] = ('proof-bundle', proof)
    ev['proofBundleId'] = pid
    eid = M.identifier('semantic-evidence', ev)
    o2[eid] = ('semantic-evidence', ev)
    seal.update(proofBundleId=pid, evidenceId=eid, verdict='pass')
    sid = M.identifier('evaluation-seal', seal)
    o2[sid] = ('evaluation-seal', seal)
    r2.update(evidenceId=eid, evaluationSealId=sid)
    structural = M.open_run_closure(r2, o2, b2)[0]
    try:
        T.finalize(r2, o2, b2)
        res['FALSE'] = {'structural': structural, 'finalize': 'ADMITTED-FALSE-RESULT'}
    except Exception as exc:
        res['FALSE'] = {'structural': structural, 'finalize': 'REFUSED', 'type': type(exc).__name__, 'isIdentityCompleteReplayMismatch': type(exc) is M.CompleteReplayMismatch,
                        'diagnostic': str(exc)[:120]}
except Exception as exc:
    res['FALSE'] = {'error': repr(exc), 'tb': traceback.format_exc()[-1200:]}

# PROJ: boundary controls on the two-stage Run
try:
    run, objects, blobs = built['foo-budget-bar-unavailable']
    derived = T.finalize(run, objects, blobs)['termination']
    stage_cids = [n['coverageId'] for n in res['NAT']['stageRecords']]
    other = [c for c in stage_cids if c != derived.get('coverageId')]
    rows = []
    for label, cand, shape in (
            ('other-stage-carrier', dict(derived, coverageId=other[0]) if other else None, True),
            ('reasons-swapped', dict(derived, reasonCodes=[derived['reasonCodes'][1], derived['reasonCodes'][0]] + derived['reasonCodes'][2:]), True),
            ('unrelated-registered-detail', dict(derived, domainDetail={'code': 'HOST.INVARIANT_VIOLATED', 'remedy': 'unrelated'}), True),
            ('query-detail-on-analysis', dict(derived, domainDetail={'code': 'QUERY.PARAMS_MALFORMED', 'remedy': 'unrelated'}), True),
            ('signal-member', dict(derived, signal='SIGINT'), True)):
        if cand is None:
            continue
        sv = True
        try:
            validate_shape(cand)
        except Exception as e:
            sv = 'INVALID'
        try:
            got = T.check_projection(cand, derived, validate_shape if shape else None)
            rows.append({'label': label, 'schemaValid': sv, 'result': 'ADMIT', 'standing': got['delegatedStanding']})
        except T.RunTerminationError as e:
            rows.append({'label': label, 'schemaValid': sv, 'result': str(e).split(':', 1)[0]})
    res['PROJ'] = rows
except Exception as exc:
    res['PROJ'] = {'error': repr(exc), 'tb': traceback.format_exc()[-1200:]}

# BRIDGE
try:
    reg = sorted({c for m in REG['sources'].values() for c in m})
    mism = []
    for cause in reg:
        a = T.cause_route(cause)
        b = ind_route(cause)
        if (a['rank'], a['d9Deficiency']) != b:
            mism.append((cause, a, b))
    try:
        T.cause_route('not-a-cause')
        unreg = 'ADMITTED'
    except T.RunTerminationError as e:
        unreg = str(e)
    def cond(cause, source='native', declared=(), staged=()):
        r = T.cause_route(cause)
        return {'cause': cause, 'origin': 'record', 'source': source, **r, 'declaredCarriers': list(declared), 'stageCarriers': list(staged)}
    mixes = {}
    for label, cs in (
            ('requirement-relative-plus-input-closure', [cond('required-relation-missing'), cond('input-closure-incomplete', declared=['coverage2:' + 'b' * 64])]),
            ('confidence-floor-plus-coverage-unknown', [cond('confidence-floor-unmet'), cond('coverage-unknown')]),
            ('language-tier-plus-work-budget', [cond('work-budget-exhausted', 'execution'), cond('language-tier-unsupported', declared=['coverage2:' + 'a' * 64])]),
            ('import-plus-enumeration-only', [cond('evidence-kind-unavailable', 'import'), cond('incomplete-inventory', 'enumeration')])):
        orders = {json.dumps({k: T.reduce(list(p))[k] for k in ('reasonCodes', 'coverageId')}) for p in itertools.permutations(cs)}
        mixes[label] = {'derivations': sorted(orders)}
    res['BRIDGE'] = {'registered': len(reg), 'routeMismatchVsIndependent': mism, 'unregistered': unreg, 'routeDrift': T.route_drift(), 'mixes': mixes}
except Exception as exc:
    res['BRIDGE'] = {'error': repr(exc), 'tb': traceback.format_exc()[-1200:]}

json.dump(res, open(OUT, 'w'), indent=1, default=str)
print(json.dumps({'IND': [(r['variant'], r.get('equal'), r.get('author'), r.get('error')) for r in res['IND']],
                  'NAT': res.get('NAT'), 'FALSE': res.get('FALSE'), 'PROJ': res.get('PROJ'),
                  'BRIDGE': {k: v for k, v in res.get('BRIDGE', {}).items() if k != 'tb'}}, indent=1, default=str)[:9000])
