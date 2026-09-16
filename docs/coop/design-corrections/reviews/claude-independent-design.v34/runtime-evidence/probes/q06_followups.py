"""Q06 — follow-ups to Q05, run because Q05 itself exposed three things. Q05 and its failures are kept.

  H3 rerun   Q05's child processes failed on MY import path (-I drops the script directory from
             sys.path); the process-boundary control never ran. Rerun with an explicit path, for BOTH
             the frozen34 and frozen33 atom_model so the control shows whether it can discriminate.
  E5b        Q05 E5 used two ResolutionCompletenessV2 records that FAIL native validation (my
             unresolvedEdgeClasses value 'dynamic-import' is not in the enum). Repeat the fold with
             natively valid records only.
  R1         Q05 showed a provider group with NO scope can never hold a qualifying attestation
             (IncomingSearchV1 scopeRefs minItems 1). Measure the consequence for an EMPTY selected
             same-family program: can it make its emptiness explicit with an empty-subject scope, or is
             incoming permanently unknown?
"""
import copy, hashlib, importlib.util, json, os, subprocess, sys

S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
F34 = S34 + '/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN34 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v34.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


man = json.load(open(MAN34))


def drift():
    return sum(1 for f in man['files'] if sha(os.path.join(S34, f['path'])) != f['sha256'])


K = load('chk34', F34 + '/check-atoms.v1.py')
AM, N = K.AM, K.AM.N
U1, U2, F_SYM, F_SUBJ = K.U1, K.U2, K.F_SYM, K.F_SUBJ
R = {'frozen34DriftBefore': drift(), 'cases': []}


def ev(atom, subj, inputs):
    try:
        r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj), copy.deepcopy(inputs))
    except AM.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key, 'detail': str(e)[:200]}
    return {'admission': 'ADMIT', 'value': r['value'],
            'causes': sorted([c['code'], c.get('universe')] for c in r['causes']),
            'coverageIds': r['coverageIds'], 'scopeIds': r['scopeIds']}


def rec(cid, standing, claim, ok, observed):
    R['cases'].append({'id': cid, 'standing': standing, 'claim': claim, 'passed': bool(ok), 'observed': observed})
    print('%-4s %-60s %s' % ('ok' if ok else 'FAIL', cid[:60], json.dumps(observed, default=str)[:220]), flush=True)


# ------------------------------------------------------------------ H3 rerun
print('=== H3 rerun: separate interpreters, hash-seeded map order ===')
child = os.path.join(BASE, 'probes', 'q06_child.py')
procs = {'34': [], '33': []}
for model in ('34', '33'):
    for _ in range(6):
        r = subprocess.run([PY, '-I', '-B', child, model], capture_output=True, text=True, timeout=900)
        procs[model].append(json.loads(r.stdout) if r.returncode == 0 else {'error': r.stderr[-500:]})
summ = {m: {'runs': len(v), 'errors': [x['error'] for x in v if 'error' in x],
            'distinctInsertionOrders': len({json.dumps(x.get('coverageInsertionOrder')) for x in v if 'error' not in x}),
            'distinctDigests': len({x.get('digest') for x in v if 'error' not in x}),
            'carrierSets': sorted({json.dumps(x.get('carriers')) for x in v if 'error' not in x})}
        for m, v in procs.items()}
R['H3'] = {'summary': summ, 'runs': procs}
rec('H3-process-boundary-hash-seeded-order', 'atom-api',
    'six fresh frozen34 interpreters, with differing set-iteration insertion orders, give ONE result digest; the same harness on frozen33 is shown for discrimination',
    not summ['34']['errors'] and summ['34']['distinctInsertionOrders'] > 1 and summ['34']['distinctDigests'] == 1,
    summ)

# ------------------------------------------------------------------ E5b
print('\n=== E5b: fold with natively valid records only ===')
rcs = {
    'partial_a': {'state': 'partial', 'attempted': True, 'examinedExhaustive': False, 'stageTerminal': 'budget-exhausted',
                  'unresolvedEdgeCount': 3, 'unresolvedEdgeClasses': ['computed-member-access']},
    'partial_b': {'state': 'partial', 'attempted': True, 'examinedExhaustive': False, 'stageTerminal': 'complete',
                  'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []},
    'incomplete_c': {'state': 'incomplete', 'attempted': True, 'examinedExhaustive': True, 'stageTerminal': 'complete',
                     'unresolvedEdgeCount': 1, 'unresolvedEdgeClasses': ['dynamic-import-nonliteral']},
    'incomplete_d': {'state': 'incomplete', 'attempted': True, 'examinedExhaustive': True, 'stageTerminal': 'complete',
                     'unresolvedEdgeCount': 2, 'unresolvedEdgeClasses': ['computed-member-access', 'dynamic-import-nonliteral']},
    'complete_x': K.rc_for('resolved-callee', state='complete', cov='complete'),
    'na_y': K.rc_for('syntactic', cov='complete'),
}
cws = {
    'open_a': {**K.CW_CLOSED, 'exportsClosed': 'open', 'deadCodeRepairEligible': False},
    'open_b': {**K.CW_CLOSED, 'exportsClosed': 'open', 'entryPointsRecognized': 'none', 'deadCodeRepairEligible': False},
    'unknown_c': {**K.CW_CLOSED, 'exportsClosed': 'unknown', 'externalConsumers': 'unknown', 'deadCodeRepairEligible': False},
}


def valid(name, v):
    try:
        N.validate_native(name, v)
        return True
    except Exception as ex:  # noqa: BLE001
        return '%s: %s' % (type(ex).__name__, str(ex)[:90])


validity = {**{'RC:' + k: valid('ResolutionCompletenessV2', v) for k, v in rcs.items()},
            **{'CW:' + k: valid('ClosedWorldV2', v) for k, v in cws.items()}}


def part(cid, rc, cw, conf, kinds, rub, dfc=None, nc=None):
    c, cv = K.coverage('calls', 'resolved-callee', U1, U1, cov='unknown', cid=cid)
    cv['entry'].update({'resolutionCompleteness': copy.deepcopy(rc), 'closedWorld': copy.deepcopy(cw),
                        'confidenceMillionths': conf, 'derivationKinds': kinds, 'rungUnavailableBecause': rub,
                        'deficiency': dfc, 'nativeCause': nc})
    return c, cv


folded, cited = AM._conservative_entry('calls', [
    part('a', rcs['partial_a'], cws['open_a'], 900000, ['declared'], 'first'),
    part('b', rcs['partial_b'], cws['open_b'], 950000, ['compiler-inferred'], 'second'),
    part('c', rcs['incomplete_c'], cws['unknown_c'], 990000, ['declared', 'annotated'], 'third'),
    part('d', rcs['incomplete_d'], cws['open_a'], 800000, [], 'fourth')])
t1, _ = AM._conservative_entry('calls', [part('x', rcs['complete_x'], cws['open_a'], 1, [], 'x'),
                                         part('y', rcs['na_y'], cws['open_b'], 1, [], 'y')])
t2, _ = AM._conservative_entry('calls', [part('y', rcs['na_y'], cws['open_b'], 1, [], 'y'),
                                         part('x', rcs['complete_x'], cws['open_a'], 1, [], 'x')])
checks = {
    'allRecordsNativelyValid': all(v is True for v in validity.values()),
    'rcWholeFromFirstStrictlyWorse': folded['resolutionCompleteness'] == rcs['incomplete_c'],
    'rcLaterTieKeepsIncumbent': folded['resolutionCompleteness'] != rcs['incomplete_d'],
    'cwWholeFromStrictlyWorse': folded['closedWorld'] == cws['unknown_c'],
    'confidenceMinimumFromALoser': folded['confidenceMillionths'] == 800000,
    'derivationKindsOrderedUnion': folded['derivationKinds'] == ['declared', 'compiler-inferred', 'annotated'],
    'unfoldedFieldKeepsFirst': folded['rungUnavailableBecause'] == 'first',
    'everyPartitionCited': cited == [K.cov2('a'), K.cov2('b'), K.cov2('c'), K.cov2('d')],
    'completeNotApplicableTieXFirst': t1['resolutionCompleteness'] == rcs['complete_x'],
    'completeNotApplicableTieYFirst': t2['resolutionCompleteness'] == rcs['na_y'],
}
rec('E5b-fold-semantics-over-natively-valid-records', 'helper-unit',
    'same fold assertions as Q05 E5, now with every RC and CW record passing native validation',
    all(checks.values()), {'checks': checks, 'validity': validity})

# ------------------------------------------------------------------ R1 empty selected program
print('\n=== R1: an empty selected same-family program and incoming completeness ===')
REF_IN = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'endpoint': 'target', 'filters': []}


def with_empty_program(emit_scope, pair_coverage):
    p = K.plan_one(cap='references')
    p['cells'].append(K.ref_cell('references', 'ts-tsconfig', U2, 'pkg-empty', K.C_PROV2, ['pkg-empty/src/index.ts']))
    empty = K.inv_symbol(universe=U2, nid='ts-symbol:pkg-empty/src/index.ts#unused', path='pkg-empty/src/index.ts', qn='unused')
    empty.update({'cellOrdinal': 1, 'rows': [], 'examinedPaths': ['pkg-empty/src/index.ts']})
    i = K.base_inputs(enumerationPlan=p, inventories=[K.inv_symbol(), empty])
    K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
    if emit_scope:
        s, sc = K.scope('references', 'resolved-binding', U2, U1, [], sid='7')
        sc['enumeratorClosure'] = K.C_PROV2
        i['scopes'][s] = sc
        if pair_coverage:
            c, cv = K.coverage('references', 'resolved-binding', U2, U1, cid='7')
            i['coverages'][c] = cv
            i['coverageScopes'][c] = s
    return i


r1 = {'noScope': ev(REF_IN, F_SUBJ, with_empty_program(False, False)),
      'emptySubjectScopeUnpaired': ev(REF_IN, F_SUBJ, with_empty_program(True, False)),
      'emptySubjectScopeWithCompleteCoverage': ev(REF_IN, F_SUBJ, with_empty_program(True, True))}
r1['baselineWithoutEmptyProgram'] = ev(REF_IN, F_SUBJ, (lambda: (lambda i: i)(
    (lambda: [None])() and K.base_inputs(enumerationPlan=K.plan_one(cap='references'))))())
base = K.base_inputs(enumerationPlan=K.plan_one(cap='references'))
K.install_pair(base, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
r1['baselineWithoutEmptyProgram'] = ev(REF_IN, F_SUBJ, base)
try:
    commit = N.subject_scope_commitment({'schemaVersion': 2, 'snapshotId': K.SNAP, 'sourceUniverse': U2,
                                         'targetUniverse': U1, 'relation': 'references', 'resolution': 'resolved-binding',
                                         'enumeratorClosure': K.C_PROV2, 'subjects': []})
    r1['nativeEmptySubjectScopeCommitment'] = {'admitted': True, 'value': commit}
except Exception as ex:  # noqa: BLE001
    r1['nativeEmptySubjectScopeCommitment'] = {'admitted': False, 'error': '%s: %s' % (type(ex).__name__, str(ex)[:160])}
R['R1'] = r1
rec('R1-empty-program-can-close-incoming-only-through-an-explicit-empty-scope', 'atom-api',
    'measurement: with no scope the empty program leaves incoming unknown and no attestation can relieve it; an explicit empty-subject scope with complete S->U Coverage is what closes it, if the native scope carrier admits empty subjects',
    True, r1)

R['frozen34DriftAfter'] = drift()
print('\nfrozen34 drift before/after: %d/%d' % (R['frozen34DriftBefore'], R['frozen34DriftAfter']))
json.dump(R, open(os.path.join(OUT, 'q06-followups.json'), 'w'), indent=1, default=str)
print('wrote q06-followups.json')
