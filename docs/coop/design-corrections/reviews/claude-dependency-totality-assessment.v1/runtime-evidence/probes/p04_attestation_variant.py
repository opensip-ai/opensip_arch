"""P04 — does the same totality principle need to reach the ATTESTATION whole-source dependency view?

P01 showed: a qualifying reachability attestation over named scopes {f, g} plus a calls partition for f only
answers all-covered TRUE on frozen35, the successor AND the same-kind remedy (the attestation view passes
current_subjects=None, so every calls partition of (S, T) is taken, however few subjects it covers).

Variant B (in-process candidate, not source): the attestation view's examined set X is the union of the
subjects of the scopes the attestation names; when X is non-empty the same-kind dependency must jointly
cover X exactly as remedy A requires; when X is empty the whole-source behaviour is kept unchanged.
STANDING: atom-api synthetic; helper-graph where labelled."""
import copy, hashlib, importlib.util, inspect, json, os, sys

F35 = '/tmp/opensip-design-corrections/candidate-subject.v35/docs/coop/design-corrections/foundation'
FSU = '/tmp/opensip-design-corrections/dependency-scope-successor.v1/source/docs/coop/design-corrections/foundation'
OUT = '/tmp/opensip-design-corrections/claude-dependency-totality-assessment.v1/receipts'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


OLD = '''    paired = []
    for sid, sc in _scopes_exact(inputs, drel, drung, source_u):
        if not any(_scope_contains(sc, nid) for nid in current_subjects):
            continue
        paired.extend(_pair_scope_coverages(sid, sc, covs, inputs))
    return _unique_pairs(paired)
'''
NEW = '''    paired, covered = [], set()
    for sid, sc in _scopes_exact(inputs, drel, drung, source_u):
        if not any(_scope_contains(sc, nid) for nid in current_subjects):
            continue
        found = _pair_scope_coverages(sid, sc, covs, inputs)
        if found:
            covered.update(sc.get("subjects") or [])
        paired.extend(found)
    if not set(current_subjects) <= covered:
        return []
    return _unique_pairs(paired)
'''
ATT_OLD = '''        covs = _select_dep_coverages(drel, drung, source_u, target_u, inputs, None, None)
'''
ATT_NEW = '''        named = set()
        for sid in att.get("scopeRefs") or []:
            named.update(((inputs.get("scopes") or {}).get(sid) or {}).get("subjects") or [])
        covs = _select_dep_coverages(drel, drung, source_u, target_u, inputs, named or None,
                                     _source_kind_for_relation(rel) if named else None)
'''


def patched(name, with_b):
    m = load(name, FSU + '/atom_model.v1.py')
    s = inspect.getsource(m._select_dep_coverages)
    assert s.count(OLD) == 1
    exec(s.replace(OLD, NEW), m.__dict__)
    if with_b:
        a = inspect.getsource(m._build_attestation_view)
        assert a.count(ATT_OLD) == 1
        exec(a.replace(ATT_OLD, ATT_NEW), m.__dict__)
    return m


K = load('chk35', F35 + '/check-atoms.v1.py')
MODELS = {'frozen35': K.AM, 'successor': load('am_succ', FSU + '/atom_model.v1.py'), 'remedyA': patched('am_a', False), 'remedyA+B': patched('am_ab', True)}
R = {'successorAtomModelSha256': sha(FSU + '/atom_model.v1.py'), 'variantBSource': ATT_NEW}
U1, U2, F, G = K.U1, K.U2, K.F_SYM, K.G_SYM
ATOM = {'op': 'all-covered', 'relation': 'reachability', 'minResolution': 'from-resolved-calls', 'endpoint': 'target', 'filters': []}


def ev(mod, inputs, atom=ATOM):
    try:
        r = mod.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(K.F_SUBJ), copy.deepcopy(inputs))
    except mod.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key}
    return {'value': r['value'], 'causes': sorted(c['code'] for c in r['causes']), 'nativeDeficiencies': r['nativeDeficiencies'], 'coverageIds': r['coverageIds']}


def calls(i, subjects, tag, cov='complete', src=U1, tgt=U1):
    s, sc = K.scope('calls', 'resolved-callee', src, tgt, subjects, sid=tag)
    if src != U1:
        sc['enumeratorClosure'] = K.C_PROV2
    c, cv = K.coverage('calls', 'resolved-callee', src, tgt, cid=tag, cov=cov)
    i['scopes'][s] = sc; i['coverages'][c] = cv; i['coverageScopes'][c] = s


def attested(dep):
    inv_f, inv_g = K.inv_symbol(), K.inv_symbol(nid=G, qn='g')
    i = K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'), inventories=[inv_f, inv_g])
    s, sc = K.scope('reachability', 'from-resolved-calls', U1, U1, [F, G], sid='1')
    i['scopes'][s] = sc
    i['incomingSearchAttestations'] = [K.incoming_att('reachability', 'from-resolved-calls', U1, U1, [s], [inv_f, inv_g])]
    if dep == 'calls-f-only':
        calls(i, [F], '2')
    elif dep == 'calls-total':
        calls(i, [F, G], '2')
    elif dep == 'calls-disjoint':
        calls(i, [F], '2'); calls(i, [G], '3')
    elif dep == 'calls-f-only-plus-unrelated-h':
        calls(i, [F], '2'); calls(i, ['ts-symbol:src/a.ts#h'], '3')
    return i


def attested_empty_program(dep):
    """U1 fully evidenced by Coverage; U2 is an empty selected program closed by an empty-subject reachability
    scope NAMED by a qualifying attestation (A-12 closure shape)."""
    p = K.plan_one(cap='reachability')
    p['cells'].append(K.ref_cell('reachability', 'ts-tsconfig', U2, 'pkg-empty', K.C_PROV2, ['pkg-empty/src/i.ts']))
    inv2 = K.inv_symbol(universe=U2, nid='ts-symbol:pkg-empty/src/i.ts#x', path='pkg-empty/src/i.ts', qn='x')
    inv2.update({'cellOrdinal': 1, 'rows': [], 'examinedPaths': ['pkg-empty/src/i.ts']})
    i = K.base_inputs(enumerationPlan=p, inventories=[K.inv_symbol(), inv2])
    K.install_pair(i, *K.paired('reachability', 'from-resolved-calls', U1, U1, [F], tag='1'))
    calls(i, [F], '2')
    s7, sc7 = K.scope('reachability', 'from-resolved-calls', U2, U1, [], sid='7'); sc7['enumeratorClosure'] = K.C_PROV2
    i['scopes'][s7] = sc7
    i['incomingSearchAttestations'] = [K.incoming_att('reachability', 'from-resolved-calls', U2, U1, [s7], [inv2], providerClosure=K.C_PROV2)]
    if dep == 'explicit-empty-calls-partition':
        calls(i, [], '8', src=U2)
    return i


T = {}
for label, builder, deps in (('attestation-two-subjects', attested, ('no-calls', 'calls-f-only', 'calls-f-only-plus-unrelated-h', 'calls-total', 'calls-disjoint')),
                             ('attestation-empty-program', attested_empty_program, ('no-calls', 'explicit-empty-calls-partition'))):
    for dep in deps:
        T['%s/%s' % (label, dep)] = {m: ev(mod, builder(dep)) for m, mod in MODELS.items()}
        print('%-62s %s' % (label + '/' + dep, {m: v.get('value', v.get('key')) for m, v in T['%s/%s' % (label, dep)].items()}), flush=True)
R['cases'] = T
EXPECT = {'attestation-two-subjects/no-calls': 'indeterminate', 'attestation-two-subjects/calls-f-only': 'indeterminate',
          'attestation-two-subjects/calls-f-only-plus-unrelated-h': 'indeterminate', 'attestation-two-subjects/calls-total': 'true',
          'attestation-two-subjects/calls-disjoint': 'true'}
R['expectedUnderTotalityPrinciple'] = EXPECT
R['mismatchesByModel'] = {m: [k for k, v in EXPECT.items() if T[k][m].get('value') != v] for m in MODELS}
R['emptyProgramUnchangedByB'] = all(T['attestation-empty-program/' + d]['remedyA+B'] == T['attestation-empty-program/' + d]['successor']
                                    for d in ('no-calls', 'explicit-empty-calls-partition'))
print('mismatches vs totality principle:', R['mismatchesByModel'])
print('empty-program attestation behaviour unchanged by variant B:', R['emptyProgramUnchangedByB'])

KS = load('chk_succ_b', FSU + '/check-atoms.v1.py')
s = inspect.getsource(KS.AM._select_dep_coverages); exec(s.replace(OLD, NEW), KS.AM.__dict__)
a = inspect.getsource(KS.AM._build_attestation_view); exec(a.replace(ATT_OLD, ATT_NEW), KS.AM.__dict__)
fails = []
for fn in KS.CASES:
    try:
        fn()
    except Exception as ex:  # noqa: BLE001
        fails.append({'case': fn.__name__, 'error': '%s: %s' % (type(ex).__name__, str(ex)[:200])})
R['checkAtomsWithRemedyAplusB'] = {'cases': len(KS.CASES), 'failed': fails}
print('successor check-atoms with remedy A+B: %d cases, %d failed %s' % (len(KS.CASES), len(fails), [f['case'] for f in fails]))
R['successorUnchanged'] = sha(FSU + '/atom_model.v1.py') == R['successorAtomModelSha256']
json.dump(R, open(os.path.join(OUT, 'p04-attestation-variant.json'), 'w'), indent=1, default=str)
print('successor unchanged:', R['successorUnchanged'], '\nwrote p04-attestation-variant.json')
