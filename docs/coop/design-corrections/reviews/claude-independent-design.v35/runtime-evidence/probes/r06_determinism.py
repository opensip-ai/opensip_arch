"""R06 — justified rerun of the source34 determinism controls on frozen35. The pairing path changed
(_scope_descriptor / _derive_scope_commitment), and FW-06, DR-009 and AR-16 were STRENGTHENED on 34 by
these exact controls, so their current standing needs current bytes. Child mode = one fresh interpreter."""
import copy, hashlib, importlib.util, itertools, json, os, subprocess, sys

F35 = '/tmp/opensip-design-corrections/candidate-subject.v35/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
PY = '/tmp/opensip-architecture-review-env/bin/python'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load('chk35', F35 + '/check-atoms.v1.py')
AM = K.AM
U1, F_SYM, G_SYM, F_SUBJ = K.U1, K.F_SYM, K.G_SYM, K.F_SUBJ
REACH = {'op': 'all-covered', 'relation': 'reachability', 'minResolution': 'from-resolved-calls', 'filters': []}


def ev(atom, inputs):
    r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(F_SUBJ), copy.deepcopy(inputs))
    return {'value': r['value'], 'causes': r['causes'], 'coverageIds': r['coverageIds']}


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


if len(sys.argv) > 1 and sys.argv[1] == '--child':
    inp = e2(hash_order=True)
    outs = {ep: ev(dict(REACH, endpoint=ep), inp) for ep in ('source', 'target')}
    print(json.dumps({'order': list(inp['coverages']), 'digest': hashlib.sha256(json.dumps(outs, sort_keys=True).encode()).hexdigest(),
                      'carriers': [c.get('nativeCause') for o in outs.values() for c in o['causes'] if c['code'] == 'coverage-unknown']}))
    sys.exit(0)

R = {'standing': 'atom-api rerun on frozen35 of the source34 E1/E2/H3 determinism controls'}
res = {}
for low, high in (('lockfile-missing', 'no-program-unit'), ('no-program-unit', 'lockfile-missing')):
    base = K.dep_fold_inputs(low, high)
    for ep in ('source', 'target'):
        seen = set()
        n = 0
        for pc in itertools.permutations(list(base['coverages'])):
            for sk in (list(base['scopes']), list(base['scopes'])[::-1]):
                for mk in (list(base['coverageScopes']), list(base['coverageScopes'])[::-1]):
                    j = copy.deepcopy(base)
                    j['coverages'] = {c: j['coverages'][c] for c in pc}
                    j['scopes'] = {s: j['scopes'][s] for s in sk}
                    j['coverageScopes'] = {c: j['coverageScopes'][c] for c in mk}
                    o = ev(dict(REACH, endpoint=ep), j)
                    seen.add(json.dumps(o, sort_keys=True))
                    n += 1
        carriers = sorted({c.get('nativeCause') for o in map(json.loads, seen) for c in o['causes'] if c['code'] == 'coverage-unknown'})
        res['E1/%s/%s' % (low, ep)] = {'orderings': n, 'distinct': len(seen), 'carriers': carriers, 'expectedCarrier': low}
base = e2()
pair5 = [c for c, _ in AM._pair_scope_coverages(K.scope2('5'), base['scopes'][K.scope2('5')], AM._coverages_exact(base, 'calls', 'resolved-callee', U1, None), base)]
pair6 = [c for c, _ in AM._pair_scope_coverages(K.scope2('6'), base['scopes'][K.scope2('6')], AM._coverages_exact(base, 'calls', 'resolved-callee', U1, None), base)]
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
    res['E2/%s' % ep] = {'orderings': n, 'distinct': len(seen),
                         'coverageUnknown': [c for c in one['causes'] if c['code'] == 'coverage-unknown'],
                         'coverageIds': one['coverageIds']}
R['inProcess'] = res
R['e2Pairing'] = {'scope5': pair5, 'scope6': pair6, 'coverage4PairedByBoth': K.cov2('4') in pair5 and K.cov2('4') in pair6}
procs = []
for _ in range(6):
    r = subprocess.run([PY, '-I', '-B', os.path.abspath(__file__), '--child'], capture_output=True, text=True, timeout=900)
    procs.append(json.loads(r.stdout) if r.returncode == 0 else {'error': r.stderr[-400:]})
R['processes'] = {'runs': procs, 'distinctOrders': len({json.dumps(p.get('order')) for p in procs if 'error' not in p}),
                  'distinctDigests': len({p.get('digest') for p in procs if 'error' not in p}),
                  'errors': [p['error'] for p in procs if 'error' in p]}
ok = (all(v['distinct'] == 1 for v in res.values())
      and all(v['carriers'] == [v['expectedCarrier']] for k, v in res.items() if k.startswith('E1'))
      and all(v['coverageUnknown'] and v['coverageUnknown'][0].get('nativeCause') == 'lockfile-missing' and K.cov2('9') not in v['coverageIds']
              for k, v in res.items() if k.startswith('E2'))
      and R['e2Pairing']['coverage4PairedByBoth'] and not R['processes']['errors']
      and R['processes']['distinctOrders'] > 1 and R['processes']['distinctDigests'] == 1)
R['passed'] = ok
print(json.dumps({k: [v['orderings'], v['distinct']] for k, v in res.items()}))
print('pairing:', R['e2Pairing'])
print('processes: orders=%d digests=%d errors=%d' % (R['processes']['distinctOrders'], R['processes']['distinctDigests'], len(R['processes']['errors'])))
print('determinism holds on frozen35:', ok)
json.dump(R, open(os.path.join(BASE, 'receipts', 'r06-determinism.json'), 'w'), indent=1, default=str)
print('wrote r06-determinism.json')
