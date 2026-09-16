"""P01 — dependency totality over the current source subjects, tested AFTER law-derivation-dependency.json.

Three models, same frozen35 check-atoms builders:
  frozen35   /tmp/.../candidate-subject.v35 atom_model.v1.py (sha recorded)
  successor  author's mutable dependency-scope-successor.v1 atom_model.v1.py, loaded READ-ONLY (sha recorded)
  remedy     the successor module with ONLY _select_dep_coverages replaced in-process by the candidate
             smallest remedy (paired exact scopes must jointly contain every current subject). No file of
             any tree is written.
STANDING: atom-api over synthetic inputs (global atom-input admission + evaluate_atom). Helper-unit where
labelled. Nothing here is native producer admission, closed enumeration or a retained Run."""
import copy, hashlib, importlib.util, inspect, itertools, json, os, sys, traceback

F35 = '/tmp/opensip-design-corrections/candidate-subject.v35/docs/coop/design-corrections/foundation'
FSU = '/tmp/opensip-design-corrections/dependency-scope-successor.v1/source/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-dependency-totality-assessment.v1'
OUT = os.path.join(BASE, 'receipts')
os.makedirs(OUT, exist_ok=True)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


R = {'standing': 'atom-api synthetic; remedy is an in-process candidate, not source',
     'hashesBefore': {'frozen35AtomModel': sha(F35 + '/atom_model.v1.py'), 'successorAtomModel': sha(FSU + '/atom_model.v1.py'),
                      'successorCheckAtoms': sha(FSU + '/check-atoms.v1.py'), 'frozen35CheckAtoms': sha(F35 + '/check-atoms.v1.py')},
     'authorReportedSuccessorAtomModel': '2c5fdabb93785349c9c9a77ddf253685309727724d98897f60a0e8abf7177dac'}
R['successorMatchesAuthorReport'] = R['hashesBefore']['successorAtomModel'] == R['authorReportedSuccessorAtomModel']
K = load('chk35', F35 + '/check-atoms.v1.py')
A35 = K.AM
ASU = load('am_successor', FSU + '/atom_model.v1.py')
ARE = load('am_remedy', FSU + '/atom_model.v1.py')

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
src = inspect.getsource(ARE._select_dep_coverages)
assert src.count(OLD) == 1, 'successor function text differs from the text this remedy was written against'
exec(src.replace(OLD, NEW), ARE.__dict__)
R['remedyFunctionSource'] = src.replace(OLD, NEW)
MODELS = {'frozen35': A35, 'successor': ASU, 'remedy': ARE}
U1, U2, F, G = K.U1, K.U2, K.F_SYM, K.G_SYM
FS = K.F_SUBJ
GS = {'universe': U1, 'kind': 'symbol', 'nativeSubjectId': G}
REACH = {'relation': 'reachability', 'minResolution': 'from-resolved-calls', 'filters': []}


def ev(mod, atom, subj, inputs):
    try:
        r = mod.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj), copy.deepcopy(inputs))
    except mod.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key}
    return {'value': r['value'], 'causes': sorted([[c['code'], c.get('universe'), c.get('nativeCause')] for c in r['causes']], key=json.dumps),
            'nativeDeficiencies': r['nativeDeficiencies'], 'coverageIds': r['coverageIds'], 'known': r['knownFactIds']}


def install_scope_cov(i, rel, rung, src_u, tgt_u, subjects, tag, cov='complete', map_it=True, scope_u=None):
    s, sc = K.scope(rel, rung, scope_u or src_u, tgt_u, subjects, sid=tag)
    i['scopes'][s] = sc
    if cov is not None:
        c, cv = K.coverage(rel, rung, src_u, tgt_u, cid=tag, cov=cov)
        i['coverages'][c] = cv
        if map_it:
            i['coverageScopes'][c] = s


def inc2(dep):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'), inventories=[K.inv_symbol(), K.inv_symbol(nid=G, qn='g')])
    install_scope_cov(i, 'reachability', 'from-resolved-calls', U1, U1, [F, G], '1')
    if dep == 'total-one-scope':
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F, G], '2')
    elif dep == 'disjoint-two-scopes':
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F], '2')
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [G], '3')
    elif dep == 'partial-f-only':
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F], '2')
    elif dep == 'partial-g-scope-wrong-universe':
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F], '2')
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [G], '3', scope_u=U2)
    elif dep == 'partial-g-scope-without-coverage':
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F], '2')
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [G], '3', cov=None)
    elif dep == 'g-coverage-unknown':
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F], '2')
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [G], '3', cov='unknown')
    elif dep == 'overlap-UNLAWFUL-at-close_run':
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F], '2')
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F, G], '3')
    elif dep == 'no-dependency':
        pass
    return i


EXPECT = {'total-one-scope': 'true', 'disjoint-two-scopes': 'true', 'partial-f-only': 'indeterminate',
          'partial-g-scope-wrong-universe': 'indeterminate', 'partial-g-scope-without-coverage': 'indeterminate',
          'g-coverage-unknown': 'indeterminate', 'no-dependency': 'indeterminate', 'overlap-UNLAWFUL-at-close_run': None}
ALL_IN = dict(REACH, op='all-covered', endpoint='target')
T1 = {}
for dep in EXPECT:
    T1[dep] = {m: ev(mod, ALL_IN, FS, inc2(dep)) for m, mod in MODELS.items()}
    print('%-36s law=%-13s 35=%-13s succ=%-13s remedy=%-13s' % (dep, EXPECT[dep], T1[dep]['frozen35'].get('value'),
                                                              T1[dep]['successor'].get('value'), T1[dep]['remedy'].get('value')), flush=True)
R['T1-incomingTwoSubjectPrimary'] = T1
lawful = [d for d in EXPECT if EXPECT[d] is not None]
R['defectCases'] = {m: [d for d in lawful if T1[d][m].get('value') != EXPECT[d]] for m in MODELS}
R['remedyMatchesLawOnAllLawfulCases'] = not R['defectCases']['remedy']
R['remedyPartialEqualsNoDependencyAnswer'] = all(
    {k: v for k, v in T1[d]['remedy'].items() if k != 'coverageIds'} == {k: v for k, v in T1['no-dependency']['remedy'].items() if k != 'coverageIds'}
    and T1[d]['remedy']['coverageIds'] == T1['no-dependency']['remedy']['coverageIds']
    for d in ('partial-f-only', 'partial-g-scope-wrong-universe', 'partial-g-scope-without-coverage'))
print('defect cases by model:', R['defectCases'])
print('remedy partial == no-dependency answer (value, causes, nativeDeficiencies, coverageIds):', R['remedyPartialEqualsNoDependencyAnswer'])

perm = {}
for dep in ('disjoint-two-scopes', 'partial-f-only', 'total-one-scope'):
    for m in ('successor', 'remedy'):
        seen = set()
        for order in itertools.permutations(['scopes', 'coverages', 'coverageScopes']):
            for rev in (False, True):
                i = inc2(dep)
                if rev:
                    for key in order:
                        i[key] = dict(reversed(list(i[key].items())))
                seen.add(json.dumps(ev(MODELS[m], ALL_IN, FS, i), sort_keys=True))
        perm['%s/%s' % (dep, m)] = len(seen)
R['permutationsDistinct'] = perm
print('permutations distinct results:', perm)

T2 = {}
for label, subj in (('outgoing-from-f', FS), ('outgoing-from-g', GS)):
    T2[label] = {m: ev(mod, dict(REACH, op='all-covered', endpoint='source'), subj, inc2('partial-f-only')) for m, mod in MODELS.items()}
R['T2-outgoingPerSubject'] = T2
R['outgoingUnchangedByRemedy'] = all(T2[l]['frozen35'] == T2[l]['successor'] == T2[l]['remedy'] for l in T2)
print('outgoing f/g:', {l: {m: v.get('value') for m, v in T2[l].items()} for l in T2}, '| unchanged by remedy:', R['outgoingUnchangedByRemedy'])

fid = K.fact2('7')
fact = {'factId': fid, 'relation': 'reachability', 'resolution': 'from-resolved-calls', 'sourceUniverse': U1, 'targetUniverse': U1,
        'producerClosure': K.C_PROV, 'confidenceMillionths': 1000000, 'payload': {'origin': G, 'reachable': F},
        'anchors': [{'path': 'src/a.ts', 'blobDigest': K.H('0'), 'startByte': 0, 'endByte': 1}]}
T3 = {}
for dep in ('total-one-scope', 'partial-f-only'):
    i = inc2(dep); i['facts'] = {fid: fact}
    T3[dep] = {m: {op + (str(ex.get('n')) if ex else ''): ev(mod, dict(REACH, op=op, endpoint='target', **ex), FS, i)
                   for op, ex in (('exists', {}), ('none', {}), ('count-at-most', {'n': 0}), ('count-at-most', {'n': 1}), ('all-covered', {}))}
               for m, mod in MODELS.items()}
R['T3-knownMatchDominance'] = T3
R['knownFactMatched'] = all(T3[d][m]['exists'].get('known') == [fid] for d in T3 for m in MODELS)
print('dominance (value per op):', {d: {m: {k: v.get('value') for k, v in T3[d][m].items()} for m in MODELS} for d in T3}, '| fact matched:', R['knownFactMatched'])


def empty_program(dep):
    p = K.plan_one(cap='reachability')
    p['cells'].append(K.ref_cell('reachability', 'ts-tsconfig', U2, 'pkg-empty', K.C_PROV2, ['pkg-empty/src/i.ts']))
    inv2 = K.inv_symbol(universe=U2, nid='ts-symbol:pkg-empty/src/i.ts#x', path='pkg-empty/src/i.ts', qn='x')
    inv2.update({'cellOrdinal': 1, 'rows': [], 'examinedPaths': ['pkg-empty/src/i.ts']})
    i = K.base_inputs(enumerationPlan=p, inventories=[K.inv_symbol(), inv2])
    install_scope_cov(i, 'reachability', 'from-resolved-calls', U1, U1, [F], '1')
    install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F], '2')
    s, sc = K.scope('reachability', 'from-resolved-calls', U2, U1, [], sid='7'); sc['enumeratorClosure'] = K.C_PROV2
    c, cv = K.coverage('reachability', 'from-resolved-calls', U2, U1, cid='7')
    i['scopes'][s] = sc; i['coverages'][c] = cv; i['coverageScopes'][c] = s
    if dep == 'explicit-empty-calls-scope':
        s8, sc8 = K.scope('calls', 'resolved-callee', U2, U1, [], sid='8'); sc8['enumeratorClosure'] = K.C_PROV2
        c8, cv8 = K.coverage('calls', 'resolved-callee', U2, U1, cid='8')
        i['scopes'][s8] = sc8; i['coverages'][c8] = cv8; i['coverageScopes'][c8] = s8
    return i


T4 = {dep: {m: ev(mod, ALL_IN, FS, empty_program(dep)) for m, mod in MODELS.items()} for dep in ('no-calls', 'explicit-empty-calls-scope')}
R['T4-emptySourceProgram'] = T4
print('empty source program:', {d: {m: [v.get('value'), [c[0] for c in v.get('causes', [])]] for m, v in T4[d].items()} for d in T4})

FILE = {'universe': U1, 'kind': 'file', 'nativeSubjectId': 'src/a.ts'}


def clones(dep):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap='clones-fact', kinds=['file']),
                      inventories=[K.inv_file(), K.inv_symbol(), K.inv_symbol(nid=G, qn='g')])
    install_scope_cov(i, 'clones', 'normalized-body-hash', U1, U1, ['src/a.ts'], '1')
    if dep in ('declares-f-only', 'declares-f-and-g'):
        install_scope_cov(i, 'declares', 'syntactic', U1, U1, [F], '5')
    if dep == 'declares-f-and-g':
        install_scope_cov(i, 'declares', 'syntactic', U1, U1, [G], '6')
    return i


T5 = {dep: {m: ev(mod, {'op': 'all-covered', 'relation': 'clones', 'minResolution': 'normalized-body-hash', 'filters': []}, FILE, clones(dep))
            for m, mod in MODELS.items()} for dep in ('no-declares', 'declares-f-only', 'declares-f-and-g')}
R['T5-differentKindWholeSource'] = T5
print('clones->declares whole-source:', {d: {m: v.get('value') for m, v in T5[d].items()} for d in T5})


def attested(dep):
    inv_f, inv_g = K.inv_symbol(), K.inv_symbol(nid=G, qn='g')
    i = K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'), inventories=[inv_f, inv_g])
    s, sc = K.scope('reachability', 'from-resolved-calls', U1, U1, [F, G], sid='1')
    i['scopes'][s] = sc
    i['incomingSearchAttestations'] = [K.incoming_att('reachability', 'from-resolved-calls', U1, U1, [s], [inv_f, inv_g])]
    if dep == 'calls-f-only':
        install_scope_cov(i, 'calls', 'resolved-callee', U1, U1, [F], '2')
    return i


T6 = {dep: {m: ev(mod, ALL_IN, FS, attested(dep)) for m, mod in MODELS.items()} for dep in ('no-calls', 'calls-f-only')}
R['T6-attestationWholeSourceView'] = T6
print('attestation view:', {d: {m: v.get('value', v.get('key')) for m, v in T6[d].items()} for d in T6})

KS = load('chk_successor', FSU + '/check-atoms.v1.py')
reg = {}
for label, patch in (('successor-model', False), ('remedy-on-successor-model', True)):
    if patch:
        s2 = inspect.getsource(KS.AM._select_dep_coverages)
        exec(s2.replace(OLD, NEW), KS.AM.__dict__)
    fails = []
    for fn in KS.CASES:
        try:
            fn()
        except Exception as ex:  # noqa: BLE001
            fails.append({'case': fn.__name__, 'error': '%s: %s' % (type(ex).__name__, str(ex)[:200])})
    reg[label] = {'cases': len(KS.CASES), 'failed': fails}
    print('successor check-atoms on %s: %d cases, %d failed %s' % (label, len(KS.CASES), len(fails), [f['case'] for f in fails]))
R['checkAtomsRegression'] = reg
R['hashesAfter'] = {'frozen35AtomModel': sha(F35 + '/atom_model.v1.py'), 'successorAtomModel': sha(FSU + '/atom_model.v1.py'),
                    'successorCheckAtoms': sha(FSU + '/check-atoms.v1.py')}
R['noTreeChanged'] = R['hashesAfter'] == {k: R['hashesBefore'][k] for k in R['hashesAfter']}
json.dump(R, open(os.path.join(OUT, 'p01-dependency-totality.json'), 'w'), indent=1, default=str)
print('no tree changed:', R['noTreeChanged'], '\nwrote p01-dependency-totality.json')
