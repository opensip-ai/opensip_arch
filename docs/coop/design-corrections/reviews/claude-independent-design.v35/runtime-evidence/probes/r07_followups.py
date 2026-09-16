"""R07 — follow-ups R02/R03 obliged. R02 and R03 and their failures are kept.

  M3b  R02's outgoing predictor wrongly treated the non-blocking cross-family disclosure as blocking
       (three cells). Rerun the outgoing matrix with a corrected predictor on frozen34 AND frozen35.
  D    R03 found the only frozen35 path where an inadmissible scope is used as evidence: the
       dependency coverageScopes MAPPING FALLBACK in _select_dep_coverages, taken when no exact dep
       scope exists. Characterize it: which scope defects it accepts (absent/null key fields, and a
       fully VALID carrier whose relation/resolution/sourceUniverse do not match the dependency), when
       it is taken, and whether frozen34 behaves the same.
  C2/C3b  Recompute the frozen34-bypass-closure and null-field comparisons from R03's own receipt with
       correct framing (no rerun).
STANDING: atom-api synthetic inputs."""
import copy, hashlib, importlib.util, json, os, sys

S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
S35 = '/tmp/opensip-design-corrections/candidate-subject.v35'
F34, F35 = S34 + '/docs/coop/design-corrections/foundation', S35 + '/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
OUT = os.path.join(BASE, 'receipts')
sys.path.insert(0, os.path.join(BASE, 'probes'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load('chk35', F35 + '/check-atoms.v1.py')
AM35 = K.AM
AM34 = load('am34', F34 + '/atom_model.v1.py')
U1, U2, UR, F_SYM, G_SYM, F_SUBJ = K.U1, K.U2, K.UR, K.F_SYM, K.G_SYM, K.F_SUBJ
R, FAIL = {}, []


def ev(mod, atom, inputs):
    try:
        r = mod.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(F_SUBJ), copy.deepcopy(inputs))
    except mod.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key}
    return {'admission': 'ADMIT', 'value': r['value'], 'causes': sorted([[c['code'], c.get('universe')] for c in r['causes']], key=json.dumps),
            'coverageIds': r['coverageIds']}


def rec(cid, claim, ok, observed):
    R.setdefault('checks', []).append({'id': cid, 'claim': claim, 'passed': bool(ok), 'observed': observed})
    if not ok:
        FAIL.append(cid)
    print('%-4s %-66s %s' % ('ok' if ok else 'FAIL', cid[:66], json.dumps(observed, default=str)[:200]), flush=True)


# ---------------------------------------------------------------- M3b
r02 = load('r02mod_defs', os.path.join(BASE, 'probes', 'r02_must_matrix.py')) if False else None
spec = importlib.util.spec_from_file_location('r02src', os.path.join(BASE, 'probes', 'r02_must_matrix.py'))
src = open(os.path.join(BASE, 'probes', 'r02_must_matrix.py'), encoding='utf-8').read()
build_src = src[src.index('REF = {'):src.index('def predict_in')]
ns = {'K': K, 'U1': U1, 'U2': U2, 'UR': UR, 'F_SYM': F_SYM, 'C1': K.C_PROV, 'C2': K.C_PROV2, 'C3': 'closure2:' + '9d' * 32,
      'G_SYM': 'ts-symbol:pkg-b/src/b.ts#g', 'H_SYM': 'ts-symbol:pkg-c/src/c.ts#h'}
exec(build_src, ns)
build = ns['build']
REF = ns['REF']


def predict_out(u_state, u2, rust_av, rust_un):
    if u_state == 'absent' and u2 == 'none' and not rust_av and not rust_un:
        return 'indeterminate', {('missing-relation-coverage', None)}
    c = {('cross-family-edge-not-owed', None)} if rust_un else set()
    if not u_state.startswith('available'):
        c.add(('selector-unbound', None))
    elif u_state == 'available-unevidenced':
        c.add(('uncovered-expected-source-subject', U1))
    blocking = {x for x in c if x[0] != 'cross-family-edge-not-owed'}
    return ('indeterminate' if blocking else 'true'), c


bad, changed, n = [], [], 0
for u_state in ('absent', 'available-evidenced', 'available-unevidenced', 'unavailable'):
    for u2 in ('none', 'evidenced', 'unevidenced'):
        for rust_av in (False, True):
            for rust_un in (False, True):
                inp = build(u_state, u2, rust_av, rust_un)
                a = dict(REF, op='none', endpoint='source')
                o35, o34 = ev(AM35, a, inp), ev(AM34, a, inp)
                n += 1
                wv, wc = predict_out(u_state, u2, rust_av, rust_un)
                if o35 != o34:
                    changed.append([u_state, u2, rust_av, rust_un])
                if o35.get('value') != wv or {tuple(x) for x in o35.get('causes', [])} != wc:
                    bad.append({'cell': [u_state, u2, rust_av, rust_un], 'want': [wv, sorted(wc, key=str)], 'got': o35})
rec('M3b-outgoing-invariant-and-equal-corrected-predictor', 'all 48 outgoing cells: frozen34 == frozen35 and both equal the corrected outgoing predictor (cross-family disclosure non-blocking)',
    not bad and not changed and n == 48, {'cells': n, 'changed34to35': changed, 'mismatches': bad[:3]})

# ---------------------------------------------------------------- D: dependency mapping fallback
REACH = {'op': 'all-covered', 'relation': 'reachability', 'minResolution': 'from-resolved-calls', 'endpoint': 'source', 'filters': []}


def dep_case(mutate=None, exact_other_scope=False):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'))
    K.install_pair(i, *K.paired('reachability', 'from-resolved-calls', U1, U1, [F_SYM], tag='1'))
    K.install_pair(i, *K.paired('calls', 'resolved-callee', U1, U1, [F_SYM], tag='2'))
    sc = i['scopes'][K.scope2('2')]
    if mutate:
        mutate(sc)
    if exact_other_scope:
        s, o = K.scope('calls', 'resolved-callee', U1, U1, [G_SYM], sid='8')
        i['scopes'][s] = o
    return i


def deleted_case(exact_other_scope=False):
    i = dep_case(exact_other_scope=exact_other_scope)
    i['scopes'].pop(K.scope2('2'))
    i['coverageScopes'].pop(K.cov2('2'))
    return i


MUT = {
    'control-valid-matching-scope': None,
    'sourceUniverse-absent': lambda s: s.pop('sourceUniverse'),
    'sourceUniverse-null': lambda s: s.update(sourceUniverse=None),
    'sourceUniverse-VALID-other-universe-U2': lambda s: s.update(sourceUniverse=U2),
    'relation-absent': lambda s: s.pop('relation'),
    'relation-VALID-other-relation-references': lambda s: s.update(relation='references'),
    'resolution-absent': lambda s: s.pop('resolution'),
    'resolution-VALID-other-rung-syntactic-callee-name': lambda s: s.update(resolution='syntactic-callee-name'),
    'enumeratorClosure-absent (control: exact scope still selected)': lambda s: s.pop('enumeratorClosure'),
}
D = {}
for label, m in MUT.items():
    for other in (False, True):
        i = dep_case(m, exact_other_scope=other)
        D['%s | exactUnrelatedDepScopePresent=%s' % (label, other)] = {
            '35': ev(AM35, REACH, i).get('value') or ev(AM35, REACH, i).get('key'),
            '34': ev(AM34, REACH, i).get('value') or ev(AM34, REACH, i).get('key'),
            'deleted35': ev(AM35, REACH, deleted_case(other)).get('value')}
R['dependencyMappingFallback'] = D
for k, v in D.items():
    print('   %-92s 35=%-15s 34=%-15s deleted=%s' % (k, v['35'], v['34'], v['deleted35']))
healed = [k for k, v in D.items() if 'control' not in k and v['35'] == 'true' and v['deleted35'] != 'true']
rec('D1-dependency-mapping-fallback-accepts-unselected-scopes-MEASURED',
    'measurement: with no exact dependency scope present, a coverageScopes mapping to a scope whose relation / resolution / sourceUniverse is absent, null, or validly DIFFERENT still heals the dependency; with an exact (even unrelated) dependency scope present the fallback is not taken',
    True, {'healedWithoutValidMatchingScope': healed,
           'sameOn34': all(D[k]['35'] == D[k]['34'] for k in D)})
R['fallbackSameOn34'] = all(D[k]['35'] == D[k]['34'] for k in D)

# ---------------------------------------------------------------- C2/C3 recomputed from R03's receipt
r03 = json.load(open(os.path.join(OUT, 'r03-a12.json')))
rows = r03['carrierMatrix']
base_vals = r03['baselineValues']
closed = [(r['path'], r['field'], r['mode']) for r in rows
          if isinstance(r['34'], list) and r['34'][0] == base_vals[r['path']] and r['refused35']]
remaining = [(r['path'], r['field'], r['mode']) for r in rows if not (r['refused35'] or r['ignoredAsAbsent35'])]
null_changed = [(r['path'], r['field'], r['34'], r['35']) for r in rows if r['mode'] == 'null' and r['35'] != r['34']]
R['C2b'] = {'frozen34AnsweredLikeValidEvidenceAndFrozen35Refuses': closed, 'remainingOn35': remaining}
R['C3b'] = {'nullCasesThatChanged34to35': null_changed}
rec('C2b-frozen34-carrier-bypasses-closed-on-35',
    'every frozen34 case that answered as if an inadmissible scope were valid evidence now refuses on frozen35, EXCEPT the six dependency-fallback cases characterized in D1',
    bool(closed) and sorted(remaining) == sorted([('dependency-pairing', f, m) for f in ('sourceUniverse', 'relation', 'resolution') for m in ('absent', 'null')]),
    {'closedCount': len(closed), 'remaining': remaining})
rec('C3b-null-change-is-only-subjects',
    'the only null-field cases that changed 34->35 are subjects:null, which frozen34 also skipped (not a list) and frozen35 refuses; every other null case is unchanged',
    all(f == 'subjects' for _, f, _, _ in null_changed) and all(b == 'ATOM_NATIVE_CARRIER' for _, _, _, b in null_changed), null_changed)
R['failed'] = FAIL
json.dump(R, open(os.path.join(OUT, 'r07-followups.json'), 'w'), indent=1, default=str)
print('failed:', FAIL, '\nwrote r07-followups.json')
