"""Q05 — INDEPENDENT controls for the changed source34 atom completeness law.

Designed from the contract text and the frozen34 branches, not copied from the author's or root's
cases. Each control records its STANDING:
  atom-api     real global atom-input admission (admit_atom_inputs, including IncomingSearchV1
               schema/joins) + evaluate_atom, over SYNTHETIC inputs. Not native producer admission,
               not a retained Run, not qualification.
  helper-unit  a private reference function called directly (the fold); no admission at all.
Fixtures are built with the frozen34 check-atoms builders (read-only import). Source33's atom_model
is loaded side by side ONLY to show whether a control discriminates the 33->34 change.
"""
import copy, hashlib, importlib.util, itertools, json, os, subprocess, sys

S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
S33 = '/tmp/opensip-design-corrections/candidate-subject.v33'
F34 = S34 + '/docs/coop/design-corrections/foundation'
F33 = S33 + '/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
MAN34 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v34.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def dig(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, default=str).encode()).hexdigest()


K = load('chk34', F34 + '/check-atoms.v1.py')
AM = K.AM


def ev(mod, atom, subj, inputs):
    try:
        r = mod.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj), copy.deepcopy(inputs))
    except mod.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key, 'detail': str(e)[:160]}
    return {'admission': 'ADMIT', 'value': r['value'],
            'causes': sorted([c['code'], c.get('universe'), c.get('nativeCause')] for c in r['causes']),
            'universeKeyPresent': sorted([c['code'], 'universe' in c] for c in r['causes']),
            'coverageIds': r['coverageIds'], 'scopeIds': r['scopeIds'],
            'nativeDeficiencies': r['nativeDeficiencies'], 'knownFactIds': r['knownFactIds']}


def codes(o, u=Ellipsis):
    return {c[0] for c in o.get('causes', []) if u is Ellipsis or c[1] == u}


# ------------------------------------------------------------------ child mode (process boundary)
if len(sys.argv) > 1 and sys.argv[1] == '--child':
    order = list({'coverage2:a', 'coverage2:b', 'coverage2:c', 'scope2:x', 'scope2:y', 'k' * 9})
    from q05_fixtures import e2_inputs  # noqa: E402  (written below by the parent)
    atom = {'op': 'all-covered', 'relation': 'reachability', 'minResolution': 'from-resolved-calls', 'filters': []}
    outs = {}
    for ep in ('source', 'target'):
        a = dict(atom, endpoint=ep)
        outs[ep] = ev(AM, a, K.F_SUBJ, e2_inputs(K, AM, hash_order=True))
    print(json.dumps({'setOrderFingerprint': order, 'digest': dig(outs), 'outs': outs}))
    sys.exit(0)

man = json.load(open(MAN34))


def drift():
    return sum(1 for f in man['files'] if sha(os.path.join(S34, f['path'])) != f['sha256'])


AM33 = load('am33', F33 + '/atom_model.v1.py')
R = {'standingKey': {'atom-api': 'global atom-input admission + evaluate_atom over synthetic inputs',
                     'helper-unit': 'direct private reference function, no admission'},
     'sourceHashes': {n: sha(F34 + '/' + n) for n in ('atom_model.v1.py', 'check-atoms.v1.py',
                                                     'atom-evaluation-contract.v1.md', 'incoming-search.schema.v1.json')},
     'source33AtomModelSha256': sha(F33 + '/atom_model.v1.py'),
     'frozen34DriftBefore': drift(), 'cases': []}
U1, U2, UR = K.U1, K.U2, K.UR
F_SYM, G_SYM, F_SUBJ = K.F_SYM, K.G_SYM, K.F_SUBJ
H_SYM = 'ts-symbol:pkg-b/src/b.ts#h'
REF_IN = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'endpoint': 'target', 'filters': []}
REF_OUT = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'filters': []}
FAIL = []


def rec(cid, standing, claim, ok, observed, **kw):
    row = {'id': cid, 'standing': standing, 'claim': claim, 'passed': bool(ok), 'observed': observed}
    row.update(kw)
    R['cases'].append(row)
    if not ok:
        FAIL.append(cid)
    print('%-4s %-58s %s' % ('ok' if ok else 'FAIL', cid[:58], json.dumps(observed, default=str)[:150]), flush=True)


def plan_with(*cells, base_cap='references'):
    p = K.plan_one(cap=base_cap)
    p['cells'] = list(cells)
    return p


# =================================================================== A. prelude and binding presence
print('\n=== A. no owed binding vs no binding at the subject universe ===')
i = K.base_inputs(enumerationPlan=K.plan_one(cap='inventory'))
a1 = {ep: ev(AM, dict(REF_OUT, endpoint=ep), F_SUBJ, i) for ep in ('source', 'target')}
rec('A1-no-owed-binding-both-endpoints', 'atom-api',
    'P2 is shared: both endpoints emit only missing-relation-coverage, projected null universe (key absent), empty ids, unknown',
    all(o['value'] == 'indeterminate' and codes(o) == {'missing-relation-coverage'} and not o['coverageIds']
        and not o['scopeIds'] and o['universeKeyPresent'] == [['missing-relation-coverage', False]] for o in a1.values()), a1)

i = K.base_inputs(enumerationPlan=K.plan_one(universe=U2, cap='references'))
o_out, o_in = ev(AM, REF_OUT, F_SUBJ, i), ev(AM, REF_IN, F_SUBJ, i)
rec('A2-binding-only-at-other-same-family-universe', 'atom-api',
    'outgoing: selector-unbound (no universe). incoming: NOT selector-unbound; it accounts S=U2 and every endpoint cause carries universe U2',
    'selector-unbound' in codes(o_out) and o_out['value'] == 'indeterminate'
    and 'selector-unbound' not in codes(o_in) and o_in['value'] == 'indeterminate'
    and all(c[1] == U2 for c in o_in['causes']) and o_in['causes'],
    {'outgoing': o_out['causes'], 'incoming': o_in['causes']})

p = K.plan_one(cap='references')
p['cells'][0]['programBindings'][0]['universe'] = None
i = K.base_inputs(enumerationPlan=p)
o_out, o_in = ev(AM, REF_OUT, F_SUBJ, i), ev(AM, REF_IN, F_SUBJ, i)
rec('A3-only-unavailable-same-family-binding', 'atom-api',
    'P2 not taken (an unavailable binding exists). outgoing: selector-unbound, no unavailable-program-binding. incoming: unavailable-program-binding only, unknown',
    codes(o_out) == {'selector-unbound'} and codes(o_in) == {'unavailable-program-binding'}
    and o_out['value'] == o_in['value'] == 'indeterminate', {'outgoing': o_out['causes'], 'incoming': o_in['causes']})

rust_unavail = K.ref_cell('references', 'rust-cargo', None, 'crate', K.C_PROV2, ['crate/src/lib.rs'])
rust_avail = K.ref_cell('references', 'rust-cargo', UR, 'crate', K.C_PROV2, ['crate/src/lib.rs'])
A4 = {}
for label, cell in (('unavailable-foreign', rust_unavail), ('available-foreign', rust_avail)):
    i = K.base_inputs(enumerationPlan=plan_with(cell))
    A4[label] = {op: {ep: ev(AM, dict(REF_OUT, op=op, endpoint=ep), F_SUBJ, i) for ep in ('source', 'target')}
                 for op in ('none', 'exists')}
a1_in = a1['target']
vac = {l: (v['none']['target']['value'], v['exists']['target']['value'], v['none']['target']['coverageIds'],
           v['none']['target']['scopeIds'], v['none']['target']['causes']) for l, v in A4.items()}
R['A4-foreign-only-plans'] = A4
rec('A4-foreign-family-only-plan-MEASURED', 'atom-api',
    'measurement, not an expectation: what incoming answers when the ONLY owed bindings are foreign-family, versus no binding at all (A1)',
    True, {'noBindingAtAll_incoming': a1_in['value'], 'foreignOnly_incoming[none,exists,covIds,scopeIds,causes]': vac,
           'foreignOnly_outgoing_none': {l: v['none']['source']['causes'] for l, v in A4.items()}})
R['monotonicityObservation'] = {
    'noBindingAtAll_incoming_none': a1_in['value'],
    'unavailableForeignOnly_incoming_none': A4['unavailable-foreign']['none']['target']['value'],
    'unavailableForeignOnly_incoming_exists': A4['unavailable-foreign']['exists']['target']['value'],
    'availableForeignOnly_incoming_none': A4['available-foreign']['none']['target']['value'],
    'citedEvidenceWhenForeignOnly': {'coverageIds': A4['unavailable-foreign']['none']['target']['coverageIds'],
                                     'scopeIds': A4['unavailable-foreign']['none']['target']['scopeIds']}}


def evidenced_refs(extra_cells=()):
    p = K.plan_one(cap='references')
    p['cells'].extend(extra_cells)
    i = K.base_inputs(enumerationPlan=p)
    K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
    i['incomingSearchAttestations'] = [K.incoming_att('references', 'resolved-binding', U1, U1, [K.scope2('1')], [K.inv_symbol()])]
    return i


b_out, b_in = ev(AM, REF_OUT, F_SUBJ, evidenced_refs()), ev(AM, REF_IN, F_SUBJ, evidenced_refs())
mystery = K.ref_cell('references', 'mystery-mode-not-in-registry', None, 'x', K.C_PROV2, ['x/a.ts'])
u_out, u_in = ev(AM, REF_OUT, F_SUBJ, evidenced_refs([mystery])), ev(AM, REF_IN, F_SUBJ, evidenced_refs([mystery]))
rec('A5-unknown-family-unavailable-blocks-incoming-only', 'atom-api',
    'baseline evidenced TS incoming/outgoing are TRUE; adding an unavailable binding of UNKNOWN family makes incoming unknown via unavailable-program-binding and leaves outgoing TRUE',
    b_out['value'] == b_in['value'] == 'true' and u_out['value'] == 'true' and u_in['value'] == 'indeterminate'
    and 'unavailable-program-binding' in codes(u_in) and 'unavailable-program-binding' not in codes(u_out),
    {'baseline': [b_out['value'], b_in['value']], 'withUnknownFamily': [u_out['value'], u_in['value'], u_in['causes']]})

# =================================================================== B. completeness returns never stop matches
print('\n=== B. outgoing early returns end completeness only ===')
f1, f2 = K.fact2('1'), K.fact2('2')
facts = {f1: K.outgoing_import_fact(f1), f2: K.outgoing_import_fact(f2)}
IMP = dict(K.IMPORTS_ATOM)
B = {}
okB = True
for label, inputs, code, u in K.early_stops():
    inputs = copy.deepcopy(inputs)
    inputs['facts'] = copy.deepcopy(facts)
    res = {'exists': ev(AM, dict(IMP, op='exists'), F_SUBJ, inputs),
           'none': ev(AM, dict(IMP, op='none'), F_SUBJ, inputs),
           'count<=1': ev(AM, dict(IMP, op='count-at-most', n=1), F_SUBJ, inputs),
           'count<=2': ev(AM, dict(IMP, op='count-at-most', n=2), F_SUBJ, inputs),
           'all-covered': ev(AM, dict(IMP, op='all-covered'), F_SUBJ, inputs)}
    vals = {k: v['value'] for k, v in res.items()}
    good = (vals == {'exists': 'true', 'none': 'false', 'count<=1': 'false', 'count<=2': 'indeterminate',
                     'all-covered': 'indeterminate'}
            and all(code in codes(v) for v in res.values())
            and set(res['exists']['knownFactIds']) == {f1, f2})
    okB = okB and good
    B[label] = {'values': vals, 'completenessCauseKept': all(code in codes(v) for v in res.values())}
i = K.base_inputs(enumerationPlan=K.plan_one(cap='imports'), facts=copy.deepcopy(facts),
                  inventories=[K.inv_symbol(), K.inv_symbol(nid=G_SYM, qn='g')])
K.install_pair(i, *K.paired('imports', 'resolved-target', U1, U1, [F_SYM], tag='1'))
comp = ev(AM, dict(IMP, op='count-at-most', n=2), F_SUBJ, i)
rec('B1-known-matches-dominate-each-early-stop-including-count-bound', 'atom-api',
    'at every early stop with TWO known facts: exists true, none false, count<=1 false (2>1), count<=2 UNKNOWN (not true), all-covered unknown; completeness cause retained',
    okB, B)
rec('B2-count-bound-discriminator-without-early-stop', 'atom-api',
    'the same two facts with complete outgoing evidence make count<=2 TRUE, so B1 unknowns are caused by the completeness return, not by the facts',
    comp['value'] == 'true', comp)

# =================================================================== D. dependency traversal
print('\n=== D. dependency view: no fictional complete entries ===')
REACH = {'op': 'all-covered', 'relation': 'reachability', 'minResolution': 'from-resolved-calls', 'filters': []}


def reach_base():
    i = K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'))
    K.install_pair(i, *K.paired('reachability', 'from-resolved-calls', U1, U1, [F_SYM], tag='1'))
    return i


D = {}
d5 = reach_base(); K.install_pair(d5, *K.paired('calls', 'resolved-callee', U1, U1, [F_SYM], tag='2'))
d1 = reach_base()
d2 = reach_base(); K.install_pair(d2, *K.paired('calls', 'resolved-callee', U1, U1, [G_SYM], tag='2'))
d3 = reach_base(); K.install_pair(d3, *K.paired('calls', 'resolved-callee', U1, U1, [G_SYM], tag='2'))
s3, sc3 = K.scope('calls', 'resolved-callee', U1, U1, [F_SYM], sid='3'); d3['scopes'][s3] = sc3
d4 = reach_base(); K.install_pair(d4, *K.paired('calls', 'resolved-callee', U1, U2, [F_SYM], tag='2'))
for label, inp in (('D5-positive-paired-calls', d5), ('D1-no-calls-at-all', d1), ('D2-calls-only-for-unrelated-subject', d2),
                   ('D3-containing-calls-scope-unpaired', d3), ('D4-calls-only-at-other-target', d4)):
    D[label] = {'34': ev(AM, dict(REACH, endpoint='source'), F_SUBJ, inp), '33': ev(AM33, dict(REACH, endpoint='source'), F_SUBJ, inp)}
rec('D-dependency-traversal-outgoing', 'atom-api',
    'only a calls partition paired to the CURRENT subject at the SAME (S,T) heals the dependency: D5 true; D1-D4 unknown with coverage-unknown and required-relation-missing',
    D['D5-positive-paired-calls']['34']['value'] == 'true'
    and all(D[k]['34']['value'] == 'indeterminate' and 'coverage-unknown' in codes(D[k]['34'])
            and 'required-relation-missing' in D[k]['34']['nativeDeficiencies']
            for k in D if not k.startswith('D5')),
    {k: [v['34']['value'], sorted(codes(v['34'])), v['34']['nativeDeficiencies']] for k, v in D.items()},
    unchangedFrom33={k: v['34'] == v['33'] for k, v in D.items()})
reg = AM.REGISTRY['relations']
R['relationKinds'] = {r: {'sourceSubjectKind': reg.get(r, {}).get('sourceSubjectKind'), 'ladder': reg.get(r, {}).get('ladder')}
                      for r in ('reachability', 'calls', 'clones', 'declares', 'references', 'imports')}
print('relation kinds:', json.dumps(R['relationKinds']))

# =================================================================== E. fold ordering and ties
print('\n=== E. fold ordering: selection order, dedup after pairing, carriers ===')


def reorder(inputs, ck, sk, mk):
    j = copy.deepcopy(inputs)
    j['coverages'] = {c: j['coverages'][c] for c in ck}
    j['scopes'] = {s: j['scopes'][s] for s in sk}
    j['coverageScopes'] = {c: j['coverageScopes'][c] for c in mk}
    return j


def perm_family(mod, inputs, atom, max_combos=None):
    ck, sk, mk = list(inputs['coverages']), list(inputs['scopes']), list(inputs['coverageScopes'])
    seen, n = {}, 0
    for pc in itertools.permutations(ck):
        for ps in (sk, sk[::-1]):
            for pm in (mk, mk[::-1]):
                o = ev(mod, atom, F_SUBJ, reorder(inputs, pc, ps, pm))
                seen.setdefault(dig(o), o)
                n += 1
                if max_combos and n >= max_combos:
                    return seen, n
    return seen, n


E1 = {}
for low, high in (('lockfile-missing', 'no-program-unit'), ('no-program-unit', 'lockfile-missing')):
    base = K.dep_fold_inputs(low, high)
    for ep in ('source', 'target'):
        a = dict(REACH, endpoint=ep)
        s34, n = perm_family(AM, base, a)
        s33, _ = perm_family(AM33, base, a)
        carriers34 = sorted({next((c[2] for c in o['causes'] if c[0] == 'coverage-unknown'), None) for o in s34.values()} - {None})
        carriers33 = sorted({next((c[2] for c in o['causes'] if c[0] == 'coverage-unknown'), None) for o in s33.values()} - {None})
        E1['%s/%s' % (low, ep)] = {'orderings': n, 'distinct34': len(s34), 'carrier34': carriers34,
                                   'distinct33': len(s33), 'carriers33': carriers33}
rec('E1-dep-fold-invariant-under-every-map-insertion-order', 'atom-api',
    'all permutations of coverages x scopes x coverageScopes insertion order give ONE result on 34, carrier = lower coverage id; 33 is order-dependent (discriminates the change)',
    all(v['distinct34'] == 1 and v['carrier34'] == [k.split('/')[0]] for k, v in E1.items())
    and any(v['distinct33'] > 1 for v in E1.values()), E1)


def e2_inputs(Kmod, AMmod, hash_order=False):
    """3 same-kind calls scopes, 4 calls Coverage: one paired by TWO scopes via commitment, one unrelated.
    The lowest id carries NO deficiency, so the carrier must be the first WITH one."""
    i = Kmod.base_inputs(enumerationPlan=Kmod.plan_one(cap='reachability'))
    Kmod.install_pair(i, *Kmod.paired('reachability', 'from-resolved-calls', Kmod.U1, Kmod.U1, [Kmod.F_SYM], tag='1'))
    s5, sc5 = Kmod.scope('calls', 'resolved-callee', Kmod.U1, Kmod.U1, [Kmod.F_SYM], sid='5')
    s6, sc6 = Kmod.scope('calls', 'resolved-callee', Kmod.U1, Kmod.U1, [Kmod.F_SYM], sid='6')
    s7, sc7 = Kmod.scope('calls', 'resolved-callee', Kmod.U1, Kmod.U1, [Kmod.G_SYM], sid='7')
    derived = AMmod._derive_scope_commitment(sc5)
    covs = {}
    for cid, dfc, nc in (('2', None, None), ('3', 'input-closure-incomplete', 'lockfile-missing'),
                         ('4', 'input-closure-incomplete', 'no-program-unit'), ('9', 'input-closure-incomplete', 'no-program-unit')):
        c, cv = Kmod.coverage('calls', 'resolved-callee', Kmod.U1, Kmod.U1, cov='unknown', cid=cid)
        cv['entry']['deficiency'], cv['entry']['nativeCause'] = dfc, nc
        covs[cid] = (c, cv)
    if derived:
        covs['4'][1]['key']['subjectScopeCommitment'] = derived
    i['scopes'].update({s5: sc5, s6: sc6, s7: sc7})
    items = [covs[k] for k in ('9', '4', '3', '2')]
    for c, cv in items:
        i['coverages'][c] = cv
    i['coverageScopes'].update({covs['2'][0]: s6, covs['3'][0]: s5, covs['9'][0]: s7})
    if not derived:
        i['coverageScopes'][covs['4'][0]] = s5
    if hash_order:
        order = list(set(i['coverages']))
        i['coverages'] = {c: i['coverages'][c] for c in order}
        sorder = list(set(i['scopes']))
        i['scopes'] = {s: i['scopes'][s] for s in sorder}
    return i


open(os.path.join(BASE, 'probes', 'q05_fixtures.py'), 'w').write(
    'import copy\n' + __import__('inspect').getsource(e2_inputs))
e2 = e2_inputs(K, AM)
derived = AM._derive_scope_commitment(e2['scopes'][K.scope2('5')])
pair5 = [c for c, _ in AM._pair_scope_coverages(K.scope2('5'), e2['scopes'][K.scope2('5')],
                                                  AM._coverages_exact(e2, 'calls', 'resolved-callee', U1, None), e2)]
pair6 = [c for c, _ in AM._pair_scope_coverages(K.scope2('6'), e2['scopes'][K.scope2('6')],
                                                  AM._coverages_exact(e2, 'calls', 'resolved-callee', U1, None), e2)]
R['E2-pairing'] = {'derivedCommitment': derived, 'scope5Pairs': pair5, 'scope6Pairs': pair6,
                   'coverage4PairedByBothScopes': K.cov2('4') in pair5 and K.cov2('4') in pair6}
print('E2 pairing:', json.dumps(R['E2-pairing'])[:300])
E2 = {}
for ep in ('source', 'target'):
    a = dict(REACH, endpoint=ep)
    s34, n = perm_family(AM, e2, a)
    s33, _ = perm_family(AM33, e2, a)
    one = next(iter(s34.values()))
    E2[ep] = {'orderings': n, 'distinct34': len(s34), 'distinct33': len(s33),
              'coverageUnknown34': [c for c in one['causes'] if c[0] == 'coverage-unknown'],
              'coverageIds34': one['coverageIds'],
              'carriers33': sorted({str([c for c in o['causes'] if c[0] == 'coverage-unknown']) for o in s33.values()})}
rec('E2-multi-scope-same-kind-dedup-and-first-carrier-with-deficiency', 'atom-api',
    'lowest Coverage id has NO deficiency, so the carrier is the next WITH one (lockfile-missing); a Coverage paired by two scopes is cited once; the unrelated scope Coverage is not cited; invariant under all orderings on 34',
    all(v['distinct34'] == 1 and v['coverageUnknown34'] and v['coverageUnknown34'][0][2] == 'lockfile-missing'
        and v['coverageUnknown34'][0][1] == U1 and K.cov2('9') not in v['coverageIds34']
        and {K.cov2('2'), K.cov2('3'), K.cov2('4')} <= set(v['coverageIds34'])
        for v in E2.values()) and R['E2-pairing']['coverage4PairedByBothScopes'],
    E2)

e4a = reach_base(); e4b = reach_base()
for inp, prim_nc in ((e4a, 'no-program-unit'), (e4b, None)):
    pc = inp['coverages'][K.cov2('1')]
    pc['entry'].update({'coverage': 'unknown', 'deficiency': 'input-closure-incomplete', 'nativeCause': prim_nc})
    c, cv = K.coverage('calls', 'resolved-callee', U1, U1, cov='unknown', cid='2')
    cv['entry'].update({'deficiency': 'input-closure-incomplete', 'nativeCause': 'lockfile-missing'})
    s, sc = K.scope('calls', 'resolved-callee', U1, U1, [F_SYM], sid='2')
    K.install_pair(inp, s, sc, c, cv)
oa, ob = ev(AM, dict(REACH, endpoint='source'), F_SUBJ, e4a), ev(AM, dict(REACH, endpoint='source'), F_SUBJ, e4b)
cu = lambda o: [c for c in o['causes'] if c[0] == 'coverage-unknown']
rec('E4-position-order-primary-before-dependency', 'atom-api',
    'coverage-unknown nativeCause is the first non-null over positions: primary no-program-unit wins over dependency lockfile-missing; with a null primary cause the dependency cause is used',
    cu(oa) and cu(oa)[0][2] == 'no-program-unit' and cu(ob) and cu(ob)[0][2] == 'lockfile-missing',
    {'primaryCarries': cu(oa), 'primaryNull': cu(ob)})

# ---- E5 whole-record ties (helper-unit), over natively schema-validated RC / CW records
N = AM.N


def valid(name, rec_):
    try:
        N.validate_native(name, rec_)
        return True
    except Exception as ex:  # noqa: BLE001
        return '%s: %s' % (type(ex).__name__, str(ex)[:100])


rcs = {
    'partial_a': {'state': 'partial', 'attempted': True, 'examinedExhaustive': False, 'stageTerminal': 'budget-exhausted',
                  'unresolvedEdgeCount': 3, 'unresolvedEdgeClasses': ['computed-member-access']},
    'partial_b': {'state': 'partial', 'attempted': True, 'examinedExhaustive': False, 'stageTerminal': 'complete',
                  'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []},
    'incomplete_c': {'state': 'incomplete', 'attempted': True, 'examinedExhaustive': True, 'stageTerminal': 'complete',
                     'unresolvedEdgeCount': 1, 'unresolvedEdgeClasses': ['dynamic-import']},
    'incomplete_d': {'state': 'incomplete', 'attempted': True, 'examinedExhaustive': True, 'stageTerminal': 'complete',
                     'unresolvedEdgeCount': 2, 'unresolvedEdgeClasses': ['computed-member-access', 'dynamic-import']},
    'complete_x': K.rc_for('resolved-callee', state='complete', cov='complete'),
    'na_y': K.rc_for('syntactic', cov='complete'),
}
cws = {
    'open_a': {**K.CW_CLOSED, 'exportsClosed': 'open', 'deadCodeRepairEligible': False},
    'open_b': {**K.CW_CLOSED, 'exportsClosed': 'open', 'entryPointsRecognized': 'none', 'deadCodeRepairEligible': False},
    'unknown_c': {**K.CW_CLOSED, 'exportsClosed': 'unknown', 'externalConsumers': 'unknown', 'deadCodeRepairEligible': False},
}
R['E5-nativeValidation'] = {**{'RC:' + k: valid('ResolutionCompletenessV2', v) for k, v in rcs.items()},
                            **{'CW:' + k: valid('ClosedWorldV2', v) for k, v in cws.items()}}
print('E5 native validation of the records used:', R['E5-nativeValidation'])


def part(cid, rc, cw, conf, kinds, rub, dfc=None, nc=None):
    c, cv = K.coverage('calls', 'resolved-callee', U1, U1, cov='unknown', cid=cid)
    cv['entry'].update({'resolutionCompleteness': copy.deepcopy(rc), 'closedWorld': copy.deepcopy(cw),
                        'confidenceMillionths': conf, 'derivationKinds': kinds, 'rungUnavailableBecause': rub,
                        'deficiency': dfc, 'nativeCause': nc})
    return c, cv


seq = [part('a', rcs['partial_a'], cws['open_a'], 900000, ['declared'], 'first'),
       part('b', rcs['partial_b'], cws['open_b'], 950000, ['compiler-inferred'], 'second'),
       part('c', rcs['incomplete_c'], cws['unknown_c'], 990000, ['declared', 'annotated'], 'third'),
       part('d', rcs['incomplete_d'], cws['open_a'], 800000, [], 'fourth')]
folded, cited = AM._conservative_entry('calls', copy.deepcopy(seq))
tie1, _ = AM._conservative_entry('calls', [part('x', rcs['complete_x'], cws['open_a'], 1000000, [], 'x'),
                                           part('y', rcs['na_y'], cws['open_b'], 1000000, [], 'y')])
tie2, _ = AM._conservative_entry('calls', [part('y', rcs['na_y'], cws['open_b'], 1000000, [], 'y'),
                                           part('x', rcs['complete_x'], cws['open_a'], 1000000, [], 'x')])
car, _ = AM._conservative_entry('calls', [part('p', rcs['partial_a'], cws['open_a'], 1, [], 'p'),
                                          part('q', rcs['partial_a'], cws['open_a'], 1, [], 'q', 'input-closure-incomplete', 'lockfile-missing'),
                                          part('r', rcs['partial_a'], cws['open_a'], 1, [], 'r', 'budget-exhausted', 'no-program-unit')])
e5 = {
    'rcWholeFromFirstStrictlyWorse(c)': folded['resolutionCompleteness'] == rcs['incomplete_c'],
    'rcLaterTieKeptIncumbent(d not taken)': folded['resolutionCompleteness'] != rcs['incomplete_d'],
    'cwWholeFromStrictlyWorse(c)': folded['closedWorld'] == cws['unknown_c'],
    'confidenceIndependentMinimumFromLoser(d)': folded['confidenceMillionths'] == 800000,
    'derivationKindsOrderedUnion': folded['derivationKinds'] == ['declared', 'compiler-inferred', 'annotated'],
    'unfoldedFieldKeepsFirst': folded['rungUnavailableBecause'] == 'first',
    'everyPartitionCited': cited == [K.cov2('a'), K.cov2('b'), K.cov2('c'), K.cov2('d')],
    'completeVsNotApplicableTieKeepsIncumbent(x first)': tie1['resolutionCompleteness'] == rcs['complete_x'],
    'completeVsNotApplicableTieKeepsIncumbent(y first)': tie2['resolutionCompleteness'] == rcs['na_y'],
    'carrierWholeFromFirstWithDeficiency': (car['deficiency'], car['nativeCause']) == ('input-closure-incomplete', 'lockfile-missing'),
}
rec('E5-whole-record-folds-ties-minimum-union-carrier', 'helper-unit', 'fold semantics of contract section 4 step 3, field by field, over four and three partitions',
    all(e5.values()), e5, recordValidity=R['E5-nativeValidation'])

# =================================================================== F. incoming accumulation per provider
print('\n=== F. incoming: per-(U, provider) accumulation, typed source-universe attribution ===')
invB = K.inv_symbol(universe=U1, nid=H_SYM, path='pkg-b/src/b.ts', qn='h'); invB['cellOrdinal'] = 1
cellB = K.ref_cell('references', 'ts-tsconfig', U1, 'pkg-b', K.C_PROV2, ['pkg-b/src/b.ts'])


def two_provider(b_scope=True, b_att=False, untagged=False, a_att=False, b_scope_refs=None):
    p = K.plan_one(cap='references'); p['cells'].append(copy.deepcopy(cellB))
    i = K.base_inputs(enumerationPlan=p, inventories=[K.inv_symbol(), copy.deepcopy(invB)])
    if untagged:
        sx, scx = K.scope('references', 'resolved-binding', U1, U1, [F_SYM, H_SYM], sid='8')
        scx['enumeratorClosure'] = None
        i['scopes'][sx] = scx
        if a_att:
            i['incomingSearchAttestations'].append(K.incoming_att('references', 'resolved-binding', U1, U1, [sx], [K.inv_symbol()]))
        if b_att:
            i['incomingSearchAttestations'].append(K.incoming_att('references', 'resolved-binding', U1, U1, [sx], [invB], providerClosure=K.C_PROV2))
        return i
    K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
    if b_scope:
        sb, scb = K.scope('references', 'resolved-binding', U1, U1, [H_SYM], sid='2'); scb['enumeratorClosure'] = K.C_PROV2
        i['scopes'][sb] = scb
    else:
        i['scopes'][K.scope2('1')]['subjects'] = sorted([F_SYM, H_SYM], key=AM.C.canonical)
    if b_att:
        refs = b_scope_refs if b_scope_refs is not None else ([K.scope2('2')] if b_scope else [])
        i['incomingSearchAttestations'].append(K.incoming_att('references', 'resolved-binding', U1, U1, refs, [invB], providerClosure=K.C_PROV2))
    return i


F = {
    'F1a-providerB-scope-unpaired-no-attestation': ev(AM, REF_IN, F_SUBJ, two_provider(True, False)),
    'F1b-providerB-qualifying-attestation': ev(AM, REF_IN, F_SUBJ, two_provider(True, True)),
    'F2a-providerB-emitted-no-scope-no-attestation': ev(AM, REF_IN, F_SUBJ, two_provider(False, False)),
    'F2b-providerB-emitted-no-scope-attestation-empty-scopeRefs': ev(AM, REF_IN, F_SUBJ, two_provider(False, True)),
    'F4a-untagged-shared-scope-only-A-attests': ev(AM, REF_IN, F_SUBJ, two_provider(untagged=True, a_att=True)),
    'F4b-untagged-shared-scope-both-attest': ev(AM, REF_IN, F_SUBJ, two_provider(untagged=True, a_att=True, b_att=True)),
}
R['F'] = F
rec('F1-provider-B-owes-its-own-scope-account', 'atom-api',
    'provider A complete does not cover provider B: B unpaired + no attestation -> scope-without-coverage@U1 unknown; B qualifying attestation -> true',
    'scope-without-coverage' in codes(F['F1a-providerB-scope-unpaired-no-attestation'], U1)
    and F['F1a-providerB-scope-unpaired-no-attestation']['value'] == 'indeterminate'
    and F['F1b-providerB-qualifying-attestation'].get('value') == 'true',
    {k: F[k].get('value', F[k].get('key')) for k in F if k.startswith('F1')})
rec('F2-selected-provider-with-no-scope-cannot-disappear', 'atom-api',
    'table row 1: provider B selected but emitted no scope -> source-target-search-unattested@U1; a qualifying B attestation with empty scopeRefs is recorded as measured',
    'source-target-search-unattested' in codes(F['F2a-providerB-emitted-no-scope-no-attestation'], U1)
    and F['F2a-providerB-emitted-no-scope-no-attestation']['value'] == 'indeterminate',
    {k: [F[k].get('value'), F[k].get('key'), F[k].get('causes')] for k in F if k.startswith('F2')})
rec('F4-untagged-shared-scope-owed-to-every-contributor', 'atom-api',
    'an untagged scope joins every contributor group: one provider attesting leaves the other owing -> scope-without-coverage; both attesting -> true',
    'scope-without-coverage' in codes(F['F4a-untagged-shared-scope-only-A-attests'], U1)
    and F['F4b-untagged-shared-scope-both-attest'].get('value') == 'true',
    {k: [F[k].get('value'), F[k].get('key'), F[k].get('causes')] for k in F if k.startswith('F4')})

p = K.plan_one(cap='references'); p['cells'].append(K.ref_cell('references', 'ts-tsconfig', U2, 'pkg-b', K.C_PROV2, ['src/b.ts']))
inv_b2 = K.inv_symbol(universe=U2, nid='ts-symbol:src/b.ts#g', path='src/b.ts', qn='g'); inv_b2['cellOrdinal'] = 1
i = K.base_inputs(enumerationPlan=p, inventories=[K.inv_symbol(), inv_b2])
K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1', cov='unknown'))
f3 = ev(AM, REF_IN, F_SUBJ, i)
endpoint_causes = [c for c in f3['causes'] if c[0] not in ('target-export-unknown',)]
rec('F3-typed-source-universe-attribution-across-universes', 'atom-api',
    'coverage-unknown carries U1 (its Coverage sourceUniverse); U2 search/population causes carry U2; no endpoint cause is mis-attributed; nothing is hidden by U1 failing first',
    ['coverage-unknown', U1, None] in f3['causes'] and 'uncovered-expected-source-subject' in codes(f3, U2)
    and 'source-target-search-unattested' in codes(f3, U2)
    and not (codes(f3, U1) & {'source-target-search-unattested', 'uncovered-expected-source-subject', 'scope-without-coverage'})
    and all(c[1] in (U1, U2) for c in endpoint_causes), f3)

# =================================================================== G. the three-case search-accounting table
print('\n=== G. search-accounting table vs actual provider-group/scope/coverage/attestation branches ===')
SEARCH = {'source-target-search-unattested', 'scope-without-coverage'}


def g_inputs(pairing, att_kind):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap='references'), inventories=[K.inv_symbol()])
    if pairing == 'scope-none':
        s, sc = K.scope('references', 'resolved-binding', U1, U1, [F_SYM], sid='1'); i['scopes'][s] = sc
    elif pairing == 'scope-SV':
        K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U2, [F_SYM], tag='1'))
    elif pairing in ('scope-SU', 'scope-SU+SV', 'scope-SU+SVunknown'):
        K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
        if pairing != 'scope-SU':
            c, cv = K.coverage('references', 'resolved-binding', U1, U2, cid='2',
                               cov='unknown' if pairing.endswith('unknown') else 'complete')
            i['coverages'][c] = cv; i['coverageScopes'][c] = K.scope2('1')
    refs = [] if pairing == 'no-scope' else [K.scope2('1')]
    if att_kind == 'nonqual':
        att = K.incoming_att('references', 'resolved-binding', U1, U1, refs, [K.inv_symbol()], completeSearch=False,
                             examinedExhaustive=False, coverage='unknown',
                             resolutionCompleteness=K.rc_for('resolved-binding', state='partial', cov='unknown'))
    elif att_kind == 'qual':
        att = K.incoming_att('references', 'resolved-binding', U1, U1, refs, [K.inv_symbol()])
    elif att_kind == 'qual-failing-sufficiency':
        att = K.incoming_att('references', 'resolved-binding', U1, U1, refs, [K.inv_symbol()],
                             closedWorld={**K.CW_CLOSED, 'exportsClosed': 'open', 'deadCodeRepairEligible': False})
    else:
        att = None
    if att:
        i['incomingSearchAttestations'] = [att]
    return i


def predict(pairing, att_kind, admitted):
    qualifying = admitted and att_kind in ('qual', 'qual-failing-sufficiency')
    if pairing == 'no-scope':
        return set() if qualifying else {'source-target-search-unattested'}
    if pairing.startswith('scope-SU') or qualifying:
        return set()
    return {'source-target-search-unattested'} if pairing == 'scope-SV' else {'scope-without-coverage'}


G, gbad = [], []
for pairing in ('no-scope', 'scope-none', 'scope-SV', 'scope-SU', 'scope-SU+SV', 'scope-SU+SVunknown'):
    for att_kind in ('absent', 'nonqual', 'qual', 'qual-failing-sufficiency'):
        o = ev(AM, REF_IN, F_SUBJ, g_inputs(pairing, att_kind))
        row = {'pairing': pairing, 'attestation': att_kind, 'admission': o['admission'], 'refusal': o.get('key')}
        if o['admission'] == 'ADMIT':
            want = predict(pairing, att_kind, True)
            got = {c[0] for c in o['causes'] if c[0] in SEARCH and c[1] == U1}
            want_cu = att_kind == 'qual-failing-sufficiency' or pairing == 'scope-SU+SVunknown'
            got_cu = any(c[0] == 'coverage-unknown' and c[1] == U1 for c in o['causes'])
            want_true = not want and not want_cu
            row.update(predictedSearchCauses=sorted(want), observedSearchCauses=sorted(got),
                       predictedCoverageUnknown=want_cu, observedCoverageUnknown=got_cu, value=o['value'],
                       allCauses=o['causes'], agrees=(want == got and want_cu == got_cu
                                                      and (o['value'] == 'true') == want_true))
            if not row['agrees']:
                gbad.append(row)
        G.append(row)
        print('   %-20s %-26s %-6s %-18s pred=%-38s obs=%-38s cu=%s/%s val=%s' % (
            pairing, att_kind, o['admission'], o.get('key') or '', row.get('predictedSearchCauses'),
            row.get('observedSearchCauses'), row.get('predictedCoverageUnknown'), row.get('observedCoverageUnknown'),
            row.get('value')), flush=True)
R['G-table'] = G
rec('G1-table-agrees-with-branches-on-every-admitted-cell', 'atom-api',
    'my predictor implements ONLY the published table prose; it must equal the observed search-accounting causes, coverage-unknown and value on every admitted cell of 6 pairings x 4 attestation kinds',
    not gbad and sum(1 for r in G if r['admission'] == 'ADMIT') >= 18, {'admitted': sum(1 for r in G if r['admission'] == 'ADMIT'),
                                                                        'refused': [(r['pairing'], r['attestation'], r['refusal']) for r in G if r['admission'] != 'ADMIT'],
                                                                        'disagreements': gbad})
qf = [r for r in G if r['attestation'] == 'qual-failing-sufficiency' and r['admission'] == 'ADMIT']
rec('G2-sufficiency-fails-independently-of-search-qualification', 'atom-api',
    'a QUALIFYING attestation whose own view is insufficient (exported target, closedWorld open) emits coverage-unknown@S and no search cause, and the value stays unknown',
    bool(qf) and all(r['observedCoverageUnknown'] and not (set(r['observedSearchCauses']) - set(r['predictedSearchCauses']))
                     and r['value'] == 'indeterminate' for r in qf),
    [(r['pairing'], r['observedSearchCauses'], r['observedCoverageUnknown'], r['value']) for r in qf])

print('\n--- qualification predicate matrix (scope-none pairing) ---')
Q, qbad = [], []
for cs in (True, False):
    for cov in ('complete', 'unknown'):
        for ee in (True, False):
            for rcee in (True, False):
                rc = K.rc_for('resolved-binding', state='complete' if cov == 'complete' else 'partial', cov=cov)
                rc['examinedExhaustive'] = rcee
                att = K.incoming_att('references', 'resolved-binding', U1, U1, [K.scope2('1')], [K.inv_symbol()],
                                     completeSearch=cs, coverage=cov, examinedExhaustive=ee, resolutionCompleteness=rc)
                i = g_inputs('scope-none', 'absent'); i['incomingSearchAttestations'] = [att]
                o = ev(AM, REF_IN, F_SUBJ, i)
                four = cs and cov == 'complete' and ee and rcee
                row = {'completeSearch': cs, 'coverage': cov, 'examinedExhaustive': ee, 'rcExaminedExhaustive': rcee,
                       'admission': o['admission'], 'refusal': o.get('key'), 'helperProvesSearch': AM._attestation_proves_search(att)}
                if o['admission'] == 'ADMIT':
                    swc = 'scope-without-coverage' in codes(o, U1)
                    row.update(scopeWithoutCoverage=swc, value=o['value'], consistent=(swc == (not four)) and row['helperProvesSearch'] == four)
                    if not row['consistent']:
                        qbad.append(row)
                Q.append(row)
                print('   cs=%-5s cov=%-8s ee=%-5s rcee=%-5s -> %-6s %-34s proves=%-5s swc=%s' % (
                    cs, cov, ee, rcee, o['admission'], o.get('key') or '', row['helperProvesSearch'], row.get('scopeWithoutCoverage')), flush=True)
R['G-qualificationMatrix'] = Q
rec('G3-admitted-nonqualifying-equals-absent-and-refusals-are-global', 'atom-api',
    'across all 16 combinations: every ADMITTED attestation is qualifying iff all four fields hold, and a non-qualifying admitted one yields exactly the absent-attestation cause; every other combination is a global admission refusal, never an accepted unknown',
    not qbad and all(r['admission'] in ('ADMIT', 'REFUSE') for r in Q)
    and all(r['refusal'] and r['refusal'].startswith('INCOMING_SEARCH') for r in Q if r['admission'] == 'REFUSE'),
    {'admitted': sum(1 for r in Q if r['admission'] == 'ADMIT'),
     'refusedKeys': sorted({r['refusal'] for r in Q if r['admission'] == 'REFUSE'}), 'inconsistent': qbad})

base_ok = g_inputs('scope-SU', 'qual')
glob = {}
for label, mut in (
        ('non-matching-target-scope-misjoin', lambda a: a.update(targetUniverse=U2, scopeRefs=[])),
        ('non-matching-target-schema-invalid', lambda a: a.update(targetUniverse=U2, completeSearch='yes')),
        ('non-matching-target-inventory-misjoin', lambda a: a.update(targetUniverse=U2, expectedInventoryRefs=[K.H('f')])),
        ('non-provider-closure', lambda a: a.update(targetUniverse=U2, providerClosure=K.C_EVAL))):
    i = copy.deepcopy(base_ok)
    extra = copy.deepcopy(i['incomingSearchAttestations'][0]); mut(extra)
    i['incomingSearchAttestations'].append(extra)
    glob[label] = ev(AM, REF_IN, F_SUBJ, i)
rec('G4-attestations-are-admitted-globally-before-matching', 'atom-api',
    'an otherwise-TRUE atom refuses when an attestation that does NOT match its target universe is misjoined or schema-invalid: refusal is global, not a skipped or unknown search',
    ev(AM, REF_IN, F_SUBJ, base_ok)['value'] == 'true' and all(v['admission'] == 'REFUSE' for v in glob.values()),
    {k: v.get('key') for k, v in glob.items()})

# =================================================================== H. order independence at real boundaries
print('\n=== H. order independence at the affected boundaries ===')
f1b = two_provider(True, True)
attA = K.incoming_att('references', 'resolved-binding', U1, U1, [K.scope2('1')], [K.inv_symbol()])
f1b['incomingSearchAttestations'].append(attA)
outs = set()
for perm in itertools.permutations(range(len(f1b['incomingSearchAttestations']))):
    j = copy.deepcopy(f1b)
    j['incomingSearchAttestations'] = [f1b['incomingSearchAttestations'][k] for k in perm]
    for pc in itertools.permutations(list(j['coverages'])):
        for sk in (list(j['scopes']), list(j['scopes'])[::-1]):
            jj = copy.deepcopy(j)
            jj['coverages'] = {c: jj['coverages'][c] for c in pc}
            jj['scopes'] = {s: jj['scopes'][s] for s in sk}
            outs.add(dig(ev(AM, REF_IN, F_SUBJ, jj)))
rec('H1-incoming-two-providers-attestation-list-and-map-orders', 'atom-api',
    'attestation list order (the evaluator input reconstruction appends in input-ref order) and scope/coverage map orders do not change the incoming result',
    len(outs) == 1, {'distinctResults': len(outs)})

pz = K.plan_one(cap='references')
pz['cells'][0]['programBindings'][0]['enumerator'] = {'status': 'selected'}
iz = K.base_inputs(enumerationPlan=pz)
K.install_pair(iz, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
nonq = K.incoming_att('references', 'resolved-binding', U1, U1, [K.scope2('1')], [K.inv_symbol()], completeSearch=False,
                      examinedExhaustive=False, coverage='unknown', resolutionCompleteness=K.rc_for('resolved-binding', state='partial', cov='unknown'))
qual2 = K.incoming_att('references', 'resolved-binding', U1, U1, [], [K.inv_symbol()], providerClosure=K.C_PROV2)
H2 = {'noAttestation': ev(AM, REF_IN, F_SUBJ, iz)}
for label, lst in (('nonqualifyingFirst', [nonq, qual2]), ('qualifyingFirst', [qual2, nonq])):
    j = copy.deepcopy(iz); j['incomingSearchAttestations'] = copy.deepcopy(lst)
    H2[label] = ev(AM, REF_IN, F_SUBJ, j)
schema_path = F34 + '/enumeration-plan.schema.v1.json'
from jsonschema import Draft202012Validator  # noqa: E402
ps = json.load(open(schema_path))
errs_ok = sorted(e.message[:120] for e in Draft202012Validator(ps).iter_errors(K.plan_one(cap='references')))[:5]
errs_z = sorted(e.message[:120] for e in Draft202012Validator(ps).iter_errors(pz))[:5]
R['H2'] = {'results': H2, 'enumerationPlanSchema': {'path': schema_path, 'sha256': sha(schema_path),
                                                      'unmodifiedFixtureErrors': errs_ok, 'closureIdlessBindingErrors': errs_z}}
H2_order_dependent = H2['nonqualifyingFirst'] != H2['qualifyingFirst']
rec('H2-phantom-null-provider-group-MEASURED', 'atom-api',
    'measurement: an AVAILABLE binding with no enumerator closureId creates a provider group keyed None that has no scopes and consumes the FIRST matching attestation of any provider; reachability is then checked against the enumeration-plan schema',
    True, {'orderDependent': H2_order_dependent,
           'values': {k: [v.get('value'), v.get('key'), [c for c in v.get('causes', []) if c[0] in SEARCH]] for k, v in H2.items()},
           'schemaRefusesClosureIdlessSelectedBinding': bool(errs_z) and not errs_ok,
           'schemaErrorsUnmodified': errs_ok, 'schemaErrorsClosureIdless': errs_z})

fx = os.path.join(BASE, 'probes')
proc = []
for _ in range(4):
    r = subprocess.run([sys.executable, '-I', '-B', os.path.abspath(__file__), '--child'], capture_output=True,
                       text=True, cwd=fx, env={'PATH': os.environ.get('PATH', ''), 'PYTHONPATH': fx}, timeout=900)
    proc.append(json.loads(r.stdout) if r.returncode == 0 else {'error': r.stderr[-400:]})
R['H3-processes'] = [{'setOrderFingerprint': p.get('setOrderFingerprint'), 'digest': p.get('digest'), 'error': p.get('error')} for p in proc]
rec('H3-separate-processes-with-hash-seeded-map-order', 'atom-api',
    'four fresh interpreters (-I ignores PYTHONHASHSEED, so string hashing is randomized per process) build the E2 maps in SET iteration order; all produce one result digest',
    all('digest' in p for p in proc) and len({p['digest'] for p in proc}) == 1,
    {'distinctSetOrders': len({json.dumps(p.get('setOrderFingerprint')) for p in proc}),
     'distinctResultDigests': len({p.get('digest') for p in proc}), 'errors': [p.get('error') for p in proc if p.get('error')]})

# =================================================================== I. projection of the nullable universe
print('\n=== I. cause representation: optional atom universe -> required nullable projected universe ===')
acv = AM.REGISTRY['$defs']['AtomCauseV1']
ids = json.load(open(F34 + '/identity-schemas.v3.json'))
hits = []


def walk(o, path):
    if isinstance(o, dict):
        props = o.get('properties')
        if isinstance(props, dict) and 'universe' in props and ('cause' in props or 'origin' in props or 'source' in props):
            hits.append({'path': path, 'required': 'universe' in (o.get('required') or []), 'universe': props['universe']})
        for k, v in o.items():
            walk(v, path + '/' + k)
    elif isinstance(o, list):
        for n_, v in enumerate(o):
            walk(v, path + '/%d' % n_)


walk(ids, '#')
proj = []
for fn in sorted(os.listdir(F34)):
    if fn.endswith('.py') and fn not in ('atom_model.v1.py', 'check-atoms.v1.py'):
        for ln, line in enumerate(open(os.path.join(F34, fn), encoding='utf-8'), 1):
            if "get('universe')" in line or 'get("universe")' in line:
                proj.append('%s:%d: %s' % (fn, ln, line.strip()[:160]))
R['I-projection'] = {'AtomCauseV1': {'universeInProperties': 'universe' in (acv.get('properties') or {}),
                                     'universeSchema': (acv.get('properties') or {}).get('universe'),
                                     'required': acv.get('required')},
                     'deficiencySchemasWithUniverse': hits, 'defaultingGetsInFoundation': proj[:25]}
rec('I1-nullable-universe-projection-claim', 'static',
    'AtomCauseV1 universe optional+nullable; a deficiency schema with universe REQUIRED+nullable exists; the replay/composition code reads it with a defaulting get',
    'universe' not in (acv.get('required') or []) and any(h['required'] for h in hits) and bool(proj),
    R['I-projection'])

R['frozen34DriftAfter'] = drift()
R['failed'] = FAIL
R['passed'] = len([c for c in R['cases'] if c['passed']])
print('\ncontrols: %d passed, failed: %s | frozen34 drift before/after %d/%d'
      % (R['passed'], FAIL, R['frozen34DriftBefore'], R['frozen34DriftAfter']))
json.dump(R, open(os.path.join(OUT, 'q05-atomlaw.json'), 'w'), indent=1, default=str)
print('wrote q05-atomlaw.json')
