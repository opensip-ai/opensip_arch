"""P02 — justified determinism rerun on FINAL frozen36: the sufficiency path changed (two-view evaluation, gap scan), and the
cross-owner rows FW-06, DR-009 and AR-16 were strengthened on 34 and re-measured on 35 by exactly these controls.
In-process: my source34/35 E1 (typed carrier fold order) and E2 (commitment-paired Coverage) controls on frozen36, plus the
totality shapes whose cause records depend on per-view carriers. Cross-process: six fresh interpreters (hash randomisation on;
-I ignores PYTHONHASHSEED so each process draws its own seed) building set-ordered maps. Child mode = one fresh interpreter."""
import copy, hashlib, importlib.util, itertools, json, os, subprocess, sys

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
PY = '/tmp/opensip-architecture-review-env/bin/python'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load('chk36d', S36 + '/check-atoms.v1.py')
AM = K.AM
U1, F_SYM, G_SYM, F_SUBJ = K.U1, K.F_SYM, K.G_SYM, K.F_SUBJ
REACH = {'op': 'all-covered', 'relation': 'reachability', 'minResolution': 'from-resolved-calls', 'filters': []}


def ev(atom, inputs):
    try:
        r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(F_SUBJ), copy.deepcopy(inputs))
    except AM.AtomAdmissionError as e:
        return {'refuse': e.key}
    return {'value': r['value'], 'causes': r['causes'], 'coverageIds': r['coverageIds'], 'nativeDeficiencies': r['nativeDeficiencies']}


def e2(hash_order=False):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'))
    K.install_pair(i, *K.paired('reachability', 'from-resolved-calls', U1, U1, [F_SYM], tag='1'))
    s5, sc5 = K.scope('calls', 'resolved-callee', U1, U1, [F_SYM], sid='5')
    s6, sc6 = K.scope('calls', 'resolved-callee', U1, U1, [F_SYM], sid='6')
    s7, sc7 = K.scope('calls', 'resolved-callee', U1, U1, [G_SYM], sid='7')
    derived = AM._derive_scope_commitment(sc5)
    covs = {}
    for cid, dfc, nc in (('2', None, None), ('3', 'input-closure-incomplete', 'lockfile-missing'),
                         ('4', 'input-closure-incomplete', 'no-program-unit'), ('9', 'input-closure-incomplete', 'no-program-unit')):
        c, cv = K.coverage('calls', 'resolved-callee', U1, U1, cov='unknown', cid=cid)
        cv['entry']['deficiency'], cv['entry']['nativeCause'] = dfc, nc
        covs[cid] = (c, cv)
    covs['4'][1]['key']['subjectScopeCommitment'] = derived
    i['scopes'].update({s5: sc5, s6: sc6, s7: sc7})
    for k in ('9', '4', '3', '2'):
        i['coverages'][covs[k][0]] = covs[k][1]
    i['coverageScopes'].update({covs['2'][0]: s6, covs['3'][0]: s5, covs['9'][0]: s7})
    if hash_order:
        i['coverages'] = {c: i['coverages'][c] for c in list(set(i['coverages']))}
        i['scopes'] = {s: i['scopes'][s] for s in list(set(i['scopes']))}
    return i


def totality_shapes(hash_order=False):
    out = {'merged-f-unknown+g-uncovered': K.totality_inputs([[F_SYM, G_SYM]], [([F_SYM], '2', 'unknown-carrier')]),
           'split-two-carriers': K.totality_inputs([[F_SYM], [G_SYM]], [([F_SYM], '2', 'unknown-carrier'), ([G_SYM], '4', 'unknown-carrier')]),
           'attested-f-only': K.totality_inputs([[F_SYM, G_SYM]], [K.F_DEP], attest=True)}
    out['split-two-carriers']['coverages'][K.cov2('4')]['entry']['nativeCause'] = 'no-program-unit'
    if hash_order:
        for v in out.values():
            for key in ('coverages', 'scopes', 'coverageScopes'):
                v[key] = {k: v[key][k] for k in list(set(v[key]))}
    return out


if len(sys.argv) > 1 and sys.argv[1] == '--child':
    inp = e2(hash_order=True)
    outs = {'E2/' + ep: ev(dict(REACH, endpoint=ep), inp) for ep in ('source', 'target')}
    for label, i in totality_shapes(hash_order=True).items():
        outs['T/' + label] = ev(dict(REACH, endpoint='target'), i)
    print(json.dumps({'order': list(inp['coverages']), 'digest': hashlib.sha256(json.dumps(outs, sort_keys=True).encode()).hexdigest(),
                      'carriers': {k: [c.get('nativeCause') for c in o.get('causes', []) if c['code'] == 'coverage-unknown'] for k, o in outs.items()}}))
    sys.exit(0)

R = {'standing': 'atom-api determinism rerun on frozen36; the sufficiency path changed',
     'checkAtomsSha256': hashlib.sha256(open(S36 + '/check-atoms.v1.py', 'rb').read()).hexdigest(),
     'atomModelSha256': hashlib.sha256(open(S36 + '/atom_model.v1.py', 'rb').read()).hexdigest()}
res = {}
for low, high in (('lockfile-missing', 'no-program-unit'), ('no-program-unit', 'lockfile-missing')):
    base = K.dep_fold_inputs(low, high)
    for ep in ('source', 'target'):
        seen, n = set(), 0
        for pc in itertools.permutations(list(base['coverages'])):
            for sk in (list(base['scopes']), list(base['scopes'])[::-1]):
                for mk in (list(base['coverageScopes']), list(base['coverageScopes'])[::-1]):
                    j = copy.deepcopy(base)
                    j['coverages'] = {c: j['coverages'][c] for c in pc}
                    j['scopes'] = {s: j['scopes'][s] for s in sk}
                    j['coverageScopes'] = {c: j['coverageScopes'][c] for c in mk}
                    seen.add(json.dumps(ev(dict(REACH, endpoint=ep), j), sort_keys=True))
                    n += 1
        carriers = sorted({c.get('nativeCause') for o in map(json.loads, seen) for c in o['causes'] if c['code'] == 'coverage-unknown'})
        res['E1/%s/%s' % (low, ep)] = {'orderings': n, 'distinct': len(seen), 'carriers': carriers, 'expectedCarrier': low}
base = e2()
for ep in ('source', 'target'):
    seen, n = set(), 0
    for pc in itertools.permutations(list(base['coverages'])):
        for sk in (list(base['scopes']), list(base['scopes'])[::-1]):
            for mk in (list(base['coverageScopes']), list(base['coverageScopes'])[::-1]):
                j = copy.deepcopy(base)
                j['coverages'] = {c: j['coverages'][c] for c in pc}
                j['scopes'] = {s: j['scopes'][s] for s in sk}
                j['coverageScopes'] = {c: j['coverageScopes'][c] for c in mk}
                seen.add(json.dumps(ev(dict(REACH, endpoint=ep), j), sort_keys=True))
                n += 1
    one = json.loads(next(iter(seen)))
    res['E2/%s' % ep] = {'orderings': n, 'distinct': len(seen), 'coverageUnknown': [c for c in one['causes'] if c['code'] == 'coverage-unknown'],
                         'coverageIds': one['coverageIds']}
for label, shape in totality_shapes().items():
    seen, n = set(), 0
    keys = list(shape['coverages'])
    for pc in itertools.permutations(keys):
        for sk in (list(shape['scopes']), list(shape['scopes'])[::-1]):
            for mk in (list(shape['coverageScopes']), list(shape['coverageScopes'])[::-1]):
                j = copy.deepcopy(shape)
                j['coverages'] = {c: j['coverages'][c] for c in pc}
                j['scopes'] = {s: j['scopes'][s] for s in sk}
                j['coverageScopes'] = {c: j['coverageScopes'][c] for c in mk}
                seen.add(json.dumps(ev(dict(REACH, endpoint='target'), j), sort_keys=True))
                n += 1
    one = json.loads(next(iter(seen)))
    res['T/%s' % label] = {'orderings': n, 'distinct': len(seen), 'value': one.get('value'),
                           'carriers': sorted([c.get('nativeCause') for c in one.get('causes', []) if c['code'] == 'coverage-unknown'], key=str),
                           'nativeDeficiencies': one.get('nativeDeficiencies')}
R['inProcess'] = res
procs = []
for _ in range(6):
    r = subprocess.run([PY, '-I', '-B', os.path.abspath(__file__), '--child'], capture_output=True, text=True, timeout=900)
    procs.append(json.loads(r.stdout) if r.returncode == 0 else {'error': r.stderr[-400:]})
R['processes'] = {'runs': procs, 'distinctOrders': len({json.dumps(p.get('order')) for p in procs if 'error' not in p}),
                  'distinctDigests': len({p.get('digest') for p in procs if 'error' not in p}), 'errors': [p['error'] for p in procs if 'error' in p]}
ok = (all(v['distinct'] == 1 for v in res.values())
      and all(v['carriers'] == [v['expectedCarrier']] for k, v in res.items() if k.startswith('E1'))
      and all(v['coverageUnknown'] and v['coverageUnknown'][0].get('nativeCause') == 'lockfile-missing' and K.cov2('9') not in v['coverageIds'] for k, v in res.items() if k.startswith('E2'))
      and not R['processes']['errors'] and R['processes']['distinctOrders'] > 1 and R['processes']['distinctDigests'] == 1)
R['passed'] = ok
print(json.dumps({k: [v['orderings'], v['distinct'], v.get('carriers')] for k, v in res.items()}))
print('processes: orders=%d digests=%d errors=%d' % (R['processes']['distinctOrders'], R['processes']['distinctDigests'], len(R['processes']['errors'])))
print('determinism holds on frozen36:', ok)
json.dump(R, open(os.path.join(BASE, 'receipts', 'p02-determinism36.json'), 'w'), indent=1, default=str)
print('wrote p02-determinism36.json')
