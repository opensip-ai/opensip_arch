"""R02 — INDEPENDENT closure test for MUST-34-01 on frozen35, discriminated against frozen34.

A predictor written from the source35 contract prose (P1, P2, I1, per-universe accumulation) is compared
with the actual atom answer on EVERY cell of a matrix:
  subject-universe U state  x  other owed programs  x  op  x  endpoint.
Plus: outgoing invariance 34==35, known-match/count dominance with I1 firing (n = 0..3), provider /
cell / attestation / map permutations, and one synthetic contradictory-family boundary.
STANDING: atom-api (global atom-input admission + evaluate_atom, synthetic inputs). Not native producer
admission, not closed enumeration admission, not a retained Run."""
import copy, hashlib, importlib.util, itertools, json, os, sys

S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
S35 = '/tmp/opensip-design-corrections/candidate-subject.v35'
F34, F35 = S34 + '/docs/coop/design-corrections/foundation', S35 + '/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
OUT = os.path.join(BASE, 'receipts')
MAN35 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v35.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


man = json.load(open(MAN35))
drift = lambda: sum(1 for f in man['files'] if sha(os.path.join(S35, f['path'])) != f['sha256'])
K = load('chk35', F35 + '/check-atoms.v1.py')
AM35 = K.AM
AM34 = load('am34', F34 + '/atom_model.v1.py')
U1, U2, UR, F_SYM, F_SUBJ = K.U1, K.U2, K.UR, K.F_SYM, K.F_SUBJ
C1, C2, C3 = K.C_PROV, K.C_PROV2, 'closure2:' + '9d' * 32
G_SYM, H_SYM = 'ts-symbol:pkg-b/src/b.ts#g', 'ts-symbol:pkg-c/src/c.ts#h'
R = {'frozen35DriftBefore': drift(), 'standing': 'atom-api', 'sourceHashes': {
    '35': {n: sha(F35 + '/' + n) for n in ('atom_model.v1.py', 'check-atoms.v1.py', 'atom-evaluation-contract.v1.md')},
    '34atomModel': sha(F34 + '/atom_model.v1.py')}}
FAIL = []


def ev(mod, atom, subj, inputs):
    try:
        r = mod.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj), copy.deepcopy(inputs))
    except mod.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key}
    return {'admission': 'ADMIT', 'value': r['value'],
            'causes': sorted([[c['code'], c.get('universe')] for c in r['causes']], key=json.dumps),
            'universeKeyOnSelectorUnbound': sorted({('universe' in c) for c in r['causes'] if c['code'] == 'selector-unbound'}),
            'knownFactIds': r['knownFactIds'], 'coverageIds': r['coverageIds'], 'scopeIds': r['scopeIds']}


def dig(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()


def rec(cid, claim, ok, observed):
    R.setdefault('checks', []).append({'id': cid, 'claim': claim, 'passed': bool(ok), 'observed': observed})
    if not ok:
        FAIL.append(cid)
    print('%-4s %-66s %s' % ('ok' if ok else 'FAIL', cid[:66], json.dumps(observed, default=str)[:170]), flush=True)


REF = {'relation': 'references', 'minResolution': 'resolved-binding', 'filters': []}


def build(u_state, u2, rust_av, rust_un, cell_order=None, extra_u2b=False, att_u2=False, att_u2b=False):
    keyed = [('subj', K.ref_cell('calls', 'ts-tsconfig', U1, 'pkg-a', C1, ['src/a.ts']))]
    if u_state != 'absent':
        keyed.append(('u1', K.ref_cell('references', 'ts-tsconfig', U1 if u_state.startswith('available') else None,
                                       'pkg-a', C1, ['src/a.ts'])))
    if u2 != 'none':
        keyed.append(('u2', K.ref_cell('references', 'ts-tsconfig', U2, 'pkg-b', C2, ['pkg-b/src/b.ts'])))
    if extra_u2b:
        keyed.append(('u2b', K.ref_cell('references', 'ts-tsconfig', U2, 'pkg-c', C3, ['pkg-c/src/c.ts'])))
    if rust_av:
        keyed.append(('rust', K.ref_cell('references', 'rust-cargo', UR, 'crate', C2, ['crate/src/lib.rs'])))
    if rust_un:
        keyed.append(('rustu', K.ref_cell('references', 'rust-cargo', None, 'crate-u', C2, ['crate-u/src/lib.rs'])))
    keyed.sort(key=lambda kc: (kc[1]['capabilityId'], kc[1]['languageMode'], kc[1]['workspaceRoot']))
    if cell_order is not None:
        keyed = [keyed[k] for k in cell_order]
    ordinal = {k: n for n, (k, _) in enumerate(keyed)}
    plan = K.plan_one(cap='calls')
    plan['cells'] = [c for _, c in keyed]
    inv_f = K.inv_symbol(); inv_f['cellOrdinal'] = ordinal['subj']
    invs = [inv_f]
    if u2 != 'none':
        g = K.inv_symbol(universe=U2, nid=G_SYM, path='pkg-b/src/b.ts', qn='g'); g['cellOrdinal'] = ordinal['u2']
        invs.append(g)
    if extra_u2b:
        h = K.inv_symbol(universe=U2, nid=H_SYM, path='pkg-c/src/c.ts', qn='h'); h['cellOrdinal'] = ordinal['u2b']
        invs.append(h)
    i = K.base_inputs(enumerationPlan=plan, inventories=invs)
    i['closures'][C3] = {'kind': 'provider'}
    if u_state == 'available-evidenced':
        K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
    if u2 == 'evidenced' and not att_u2:
        s, sc = K.scope('references', 'resolved-binding', U2, U1, [G_SYM], sid='2'); sc['enumeratorClosure'] = C2
        K.install_pair(i, s, sc, *K.coverage('references', 'resolved-binding', U2, U1, cid='2'))
    if att_u2:
        s, sc = K.scope('references', 'resolved-binding', U2, U1, [G_SYM], sid='2'); sc['enumeratorClosure'] = C2
        i['scopes'][s] = sc
        i['incomingSearchAttestations'].append(K.incoming_att('references', 'resolved-binding', U2, U1, [s], [g], providerClosure=C2))
    if extra_u2b:
        s, sc = K.scope('references', 'resolved-binding', U2, U1, [H_SYM], sid='3'); sc['enumeratorClosure'] = C3
        if att_u2b:
            i['scopes'][s] = sc
            i['incomingSearchAttestations'].append(K.incoming_att('references', 'resolved-binding', U2, U1, [s], [h], providerClosure=C3))
        else:
            K.install_pair(i, s, sc, *K.coverage('references', 'resolved-binding', U2, U1, cid='3'))
    return i


def predict_in(u_state, u2, rust_av, rust_un):
    if u_state == 'absent' and u2 == 'none' and not rust_av and not rust_un:
        return {('missing-relation-coverage', None)}
    c = set()
    if u_state == 'unavailable':
        c.add(('unavailable-program-binding', None))
    if rust_un:
        c.add(('cross-family-edge-not-owed', None))
    if not u_state.startswith('available'):
        c.add(('selector-unbound', None))
    if rust_av:
        c.add(('cross-family-edge-not-owed', UR))
    if u_state == 'available-unevidenced':
        c |= {('source-target-search-unattested', U1), ('uncovered-expected-source-subject', U1)}
    if u2 == 'unevidenced':
        c |= {('source-target-search-unattested', U2), ('uncovered-expected-source-subject', U2)}
    return c


def predict_out(u_state, u2, rust_av, rust_un):
    if u_state == 'absent' and u2 == 'none' and not rust_av and not rust_un:
        return {('missing-relation-coverage', None)}
    c = {('cross-family-edge-not-owed', None)} if rust_un else set()
    if not u_state.startswith('available'):
        return c | {('selector-unbound', None)}
    if u_state == 'available-unevidenced':
        return c | {('uncovered-expected-source-subject', U1)}
    return c


def value_for(op, complete):
    if op in ('none', 'count-at-most-0', 'all-covered'):
        return 'true' if complete else 'indeterminate'
    return 'false' if complete else 'indeterminate'


OPS = [('none', {}), ('exists', {}), ('count-at-most-0', {'op': 'count-at-most', 'n': 0}), ('all-covered', {})]
rows, bad_in, bad_out, outgoing_changed, diff_cells, negative_without_u = [], [], [], [], [], []
for u_state in ('absent', 'available-evidenced', 'available-unevidenced', 'unavailable'):
    for u2 in ('none', 'evidenced', 'unevidenced'):
        for rust_av in (False, True):
            for rust_un in (False, True):
                inp = build(u_state, u2, rust_av, rust_un)
                pin = predict_in(u_state, u2, rust_av, rust_un)
                pout = predict_out(u_state, u2, rust_av, rust_un)
                cell = {'u': u_state, 'u2': u2, 'rustAvailable': rust_av, 'rustUnavailable': rust_un, 'ops': {}}
                for name, over in OPS:
                    atom = dict(REF, op=over.get('op', name), endpoint='target', **({'n': over['n']} if 'n' in over else {}))
                    o35, o34 = ev(AM35, atom, F_SUBJ, inp), ev(AM34, atom, F_SUBJ, inp)
                    complete_pred = not {c for c in pin if c[0] != 'cross-family-edge-not-owed'}
                    want_val = value_for(name, complete_pred)
                    got = {tuple(c) for c in o35.get('causes', [])}
                    ok = o35.get('value') == want_val and got == pin
                    if not ok:
                        bad_in.append({'cell': [u_state, u2, rust_av, rust_un], 'op': name, 'want': [want_val, sorted(pin, key=str)], 'got': o35})
                    if o35 != o34:
                        diff_cells.append({'cell': [u_state, u2, rust_av, rust_un], 'op': name, '34': [o34.get('value'), o34.get('causes')],
                                           '35': [o35.get('value'), o35.get('causes')]})
                    if o35.get('value') in ('true',) and name in ('none', 'count-at-most-0', 'all-covered') and not u_state.startswith('available'):
                        negative_without_u.append([u_state, u2, rust_av, rust_un, name])
                    if o35.get('value') == 'false' and name == 'exists' and not u_state.startswith('available'):
                        negative_without_u.append([u_state, u2, rust_av, rust_un, name])
                    cell['ops'][name] = {'35': o35.get('value'), '34': o34.get('value')}
                oo35 = ev(AM35, dict(REF, op='none', endpoint='source'), F_SUBJ, inp)
                oo34 = ev(AM34, dict(REF, op='none', endpoint='source'), F_SUBJ, inp)
                if oo35 != oo34:
                    outgoing_changed.append([u_state, u2, rust_av, rust_un])
                want_o = value_for('none', not pout)
                if oo35.get('value') != want_o or {tuple(c) for c in oo35.get('causes', [])} != pout:
                    bad_out.append({'cell': [u_state, u2, rust_av, rust_un], 'want': [want_o, sorted(pout, key=str)], 'got': oo35})
                cell['outgoing'] = oo35.get('value')
                rows.append(cell)
R['matrix'] = rows
i1_cells = [d for d in diff_cells]
rec('M1-incoming-equals-source35-prose-predictor-on-every-cell',
    'value and exact cause set on 48 cells x 4 ops equal a predictor implementing P1, P2, I1 and accumulation from the contract text',
    not bad_in, {'cells': len(rows) * len(OPS), 'mismatches': bad_in[:3]})
rec('M2-no-incoming-negative-without-an-available-binding-at-U',
    'on frozen35 no none/count<=0/all-covered true and no exists false occurs unless U has an available binding',
    not negative_without_u, negative_without_u[:4])
rec('M3-outgoing-and-P2-invariant-34-to-35',
    'outgoing results are byte-equal on frozen34 and frozen35 in every cell and equal the outgoing predictor; the P2 cell is identical on both',
    not outgoing_changed and not bad_out, {'outgoingChanged': outgoing_changed, 'outgoingMismatches': bad_out[:3]})
only_i1 = all(not (d['cell'][0].startswith('available')) for d in diff_cells) and all(
    ['selector-unbound', None] in (d['35'][1] or []) for d in diff_cells)
p2_same = not any(d['cell'] == ['absent', 'none', False, False] for d in diff_cells)
rec('M4-34-to-35-change-is-exactly-I1',
    'every cell that differs between frozen34 and frozen35 has U without an available binding and gains selector-unbound; the P2 cell does not differ',
    only_i1 and p2_same and bool(diff_cells), {'differingCellOps': len(diff_cells),
                                               'valueChanges': sum(1 for d in diff_cells if d['34'][0] != d['35'][0]),
                                               'causeOnly': sum(1 for d in diff_cells if d['34'][0] == d['35'][0])})
sel = ev(AM35, dict(REF, op='none', endpoint='target'), F_SUBJ, build('absent', 'evidenced', False, False))
rec('M5-I1-record-shape', 'I1 emits selector-unbound with the universe KEY omitted (projected null), exactly once',
    sel['universeKeyOnSelectorUnbound'] == [False] and sum(1 for c in sel['causes'] if c[0] == 'selector-unbound') == 1, sel)

# ---------------------------------------------------------------- known matches and count bounds with I1 firing
print('\n=== known matches / count bounds under I1 ===')


def known_inputs(bound):
    keyed = [('subj', K.ref_cell('calls', 'ts-tsconfig', U1, 'pkg-a', C1, ['src/a.ts'])),
             ('u2', K.ref_cell('imports', 'ts-tsconfig', U2, 'pkg-b', C2, ['pkg-b/src/b.ts'], kinds=['symbol', 'file']))]
    if bound:
        keyed.append(('u1', K.ref_cell('imports', 'ts-tsconfig', U1, 'pkg-a', C1, ['src/a.ts'], kinds=['symbol', 'file'])))
    keyed.sort(key=lambda kc: (kc[1]['capabilityId'], kc[1]['languageMode'], kc[1]['workspaceRoot']))
    ordinal = {k: n for n, (k, _) in enumerate(keyed)}
    plan = K.plan_one(cap='calls'); plan['cells'] = [c for _, c in keyed]
    inv_f = K.inv_symbol(); inv_f['cellOrdinal'] = ordinal['subj']
    inv_file = K.inv_file(); inv_file['cellOrdinal'] = ordinal['subj']
    g = K.inv_symbol(universe=U2, nid=G_SYM, path='pkg-b/src/b.ts', qn='g'); g['cellOrdinal'] = ordinal['u2']
    f1, f2 = K.fact2('1'), K.fact2('2')
    facts = {f1: K.incoming_import_fact(f1, F_SYM), f2: K.incoming_import_fact(f2, 'ts-symbol:src/a.ts#f2')}
    attrs = {fid: K.sidecar(fid, 'file:src/a.ts', kind='file', occupancy='first-party', evaluation='src/a.ts') for fid in facts}
    i = K.base_inputs(enumerationPlan=plan, inventories=[inv_f, inv_file, g], facts=facts, targetAttributions=attrs)
    s, sc = K.scope('imports', 'resolved-target', U2, U1, [G_SYM], sid='2'); sc['enumeratorClosure'] = C2
    K.install_pair(i, s, sc, *K.coverage('imports', 'resolved-target', U2, U1, cid='2'))
    if bound:
        K.install_pair(i, *K.paired('imports', 'resolved-target', U1, U1, [F_SYM], tag='1'))
    return i, sorted(facts)


FILE_SUBJ = {'universe': U1, 'kind': 'file', 'nativeSubjectId': 'src/a.ts'}
known = {}
for bound in (False, True):
    inp, fids = known_inputs(bound)
    res = {}
    for label, over in (('exists', {'op': 'exists'}), ('none', {'op': 'none'}), ('count<=0', {'op': 'count-at-most', 'n': 0}),
                        ('count<=1', {'op': 'count-at-most', 'n': 1}), ('count<=2', {'op': 'count-at-most', 'n': 2}),
                        ('count<=3', {'op': 'count-at-most', 'n': 3}), ('all-covered', {'op': 'all-covered'})):
        o = ev(AM35, {'relation': 'imports', 'minResolution': 'resolved-target', 'endpoint': 'target', 'filters': [], **over}, FILE_SUBJ, inp)
        res[label] = {'value': o.get('value', o.get('key')), 'known': o.get('knownFactIds') == fids,
                      'selectorUnbound': ['selector-unbound', None] in (o.get('causes') or [])}
    known['bound' if bound else 'unbound'] = res
want_unbound = {'exists': 'true', 'none': 'false', 'count<=0': 'false', 'count<=1': 'false', 'count<=2': 'indeterminate',
                'count<=3': 'indeterminate', 'all-covered': 'indeterminate'}
want_bound = {'exists': 'true', 'none': 'false', 'count<=0': 'false', 'count<=1': 'false', 'count<=2': 'true',
              'count<=3': 'true', 'all-covered': 'true'}
R['knownMatches'] = known
rec('K1-known-matches-and-exceeded-bounds-survive-I1',
    'two known incoming facts, U unbound: exists true, none false, count<=0/1 false (bound exceeded), count<=2/3 UNKNOWN, all-covered unknown; facts retained; selector-unbound present. U bound: count<=2/3 and all-covered true, no selector-unbound',
    all(known['unbound'][k]['value'] == v and known['unbound'][k]['known'] and known['unbound'][k]['selectorUnbound'] for k, v in want_unbound.items())
    and all(known['bound'][k]['value'] == v and known['bound'][k]['known'] and not known['bound'][k]['selectorUnbound'] for k, v in want_bound.items()),
    {k: {kk: vv['value'] for kk, vv in v.items()} for k, v in known.items()})

# ---------------------------------------------------------------- permutations
print('\n=== provider / cell / attestation / map permutations ===')
perm = {}
for label, u_state, att in (('U-unbound-two-U2-providers-one-attested', 'absent', True),
                            ('U-bound-two-U2-providers-one-attested', 'available-evidenced', True),
                            ('U-unbound-two-U2-providers-coverage', 'absent', False)):
    base = build(u_state, 'evidenced', True, True, extra_u2b=True, att_u2b=att)
    n_cells = len(base['enumerationPlan']['cells'])
    digests, n = {}, 0
    for order in itertools.permutations(range(n_cells)):
        inp = build(u_state, 'evidenced', True, True, cell_order=list(order), extra_u2b=True, att_u2b=att)
        for rev in (False, True):
            j = copy.deepcopy(inp)
            if rev:
                for key in ('scopes', 'coverages', 'coverageScopes'):
                    j[key] = dict(reversed(list(j[key].items())))
                j['incomingSearchAttestations'] = list(reversed(j['incomingSearchAttestations']))
            o = ev(AM35, dict(REF, op='none', endpoint='target'), F_SUBJ, j)
            digests.setdefault(dig(o), o)
            n += 1
    perm[label] = {'orderings': n, 'distinct': len(digests), 'result': next(iter(digests.values()))}
R['permutations'] = perm
rec('P1-one-result-for-every-cell-provider-attestation-and-map-order',
    'all 720 plan-cell orders (with ordinals remapped) x map/attestation reversal give one result in each case',
    all(v['distinct'] == 1 for v in perm.values()), {k: [v['orderings'], v['distinct'], v['result'].get('value'), v['result'].get('causes')] for k, v in perm.items()})
rec('P2-multi-provider-values',
    'U unbound: unknown with selector-unbound beside both cross-family disclosures; U bound: true with only the disclosures',
    perm['U-unbound-two-U2-providers-one-attested']['result'].get('value') == 'indeterminate'
    and ['selector-unbound', None] in perm['U-unbound-two-U2-providers-one-attested']['result']['causes']
    and perm['U-bound-two-U2-providers-one-attested']['result'].get('value') == 'true'
    and all(c[0] == 'cross-family-edge-not-owed' for c in perm['U-bound-two-U2-providers-one-attested']['result']['causes']),
    {k: v['result'].get('causes') for k, v in perm.items()})

# ---------------------------------------------------------------- synthetic contradictory family at U
print('\n=== synthetic boundary: a binding at U whose languageMode family contradicts U\'s domain ===')
keyed = [('subj', K.ref_cell('calls', 'ts-tsconfig', U1, 'pkg-a', C1, ['src/a.ts'])),
         ('weird', K.ref_cell('references', 'rust-cargo', U1, 'weird', C2, ['weird/src/lib.rs'])),
         ('u2', K.ref_cell('references', 'ts-tsconfig', U2, 'pkg-b', C2, ['pkg-b/src/b.ts']))]
keyed.sort(key=lambda kc: (kc[1]['capabilityId'], kc[1]['languageMode'], kc[1]['workspaceRoot']))
ordn = {k: n for n, (k, _) in enumerate(keyed)}
plan = K.plan_one(cap='calls'); plan['cells'] = [c for _, c in keyed]
inv_f = K.inv_symbol(); inv_f['cellOrdinal'] = ordn['subj']
g = K.inv_symbol(universe=U2, nid=G_SYM, path='pkg-b/src/b.ts', qn='g'); g['cellOrdinal'] = ordn['u2']
wi = K.base_inputs(enumerationPlan=plan, inventories=[inv_f, g])
s, sc = K.scope('references', 'resolved-binding', U2, U1, [G_SYM], sid='2'); sc['enumeratorClosure'] = C2
K.install_pair(wi, s, sc, *K.coverage('references', 'resolved-binding', U2, U1, cid='2'))
w35, w34 = ev(AM35, dict(REF, op='none', endpoint='target'), F_SUBJ, wi), ev(AM34, dict(REF, op='none', endpoint='target'), F_SUBJ, wi)
R['contradictoryFamilyAtU'] = {'35': w35, '34': w34}
rec('B1-contradictory-family-binding-at-U-MEASURED',
    'measurement only: a rust-cargo binding carrying the TypeScript-domain universe U satisfies I1 and is then skipped as foreign; reachability is judged against the enumeration contract, not asserted here',
    True, {'35': [w35.get('value'), w35.get('causes')], '34': [w34.get('value'), w34.get('causes')]})
R['failed'] = FAIL
R['frozen35DriftAfter'] = drift()
print('\nfailed:', FAIL, '| frozen35 drift before/after %d/%d' % (R['frozen35DriftBefore'], R['frozen35DriftAfter']))
json.dump(R, open(os.path.join(OUT, 'r02-must-matrix.json'), 'w'), indent=1, default=str)
print('wrote r02-must-matrix.json')
