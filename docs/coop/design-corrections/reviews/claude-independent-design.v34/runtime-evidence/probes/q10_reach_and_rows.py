"""Q10 — three things the Q09 result obliges me to settle before writing a verdict:

  1. Is the incoming 'subject program unbound' negative NEW in source34, or already present in the
     source33 atom_model I accepted? Same inputs, both frozen models.
  2. Can the DEFAULT analysis reach it, without user narrowing? Read the capability matrix: for each
     incoming-capable relation, does any engine family mix modes where the capability is requested
     with modes where it is NOT-SELECTED (which mints no cell)?
  3. A compact per-row subject dump of the 93 owner-bearing baseline rows, so cross-owner
     consequences are selected by reading each row's own subject.
"""
import copy, hashlib, importlib.util, json, os, sys

S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
S33 = '/tmp/opensip-design-corrections/candidate-subject.v33'
F34 = S34 + '/docs/coop/design-corrections/foundation'
F33 = S33 + '/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
B2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/review.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load('chk34', F34 + '/check-atoms.v1.py')
AM34 = K.AM
AM33 = load('am33', F33 + '/atom_model.v1.py')
U1, U2, UR, F_SYM = K.U1, K.U2, K.UR, K.F_SYM
G_SYM = 'ts-symbol:pkg-b/src/b.ts#g'
R = {}


def ev(mod, atom, inputs):
    try:
        r = mod.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(K.F_SUBJ), copy.deepcopy(inputs))
    except mod.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key}
    return {'value': r['value'], 'causes': sorted([c['code'], c.get('universe')] for c in r['causes'])}


def narrowed(other):
    cells = [{'capabilityId': 'calls', 'languageMode': 'ts-tsconfig', 'workspaceRoot': 'pkg-a', 'required': True,
              'kinds': ['symbol'], 'programBindings': [{'ordinal': 0, 'provenance': 'default-unit',
                                                        'enumerator': {'status': 'selected', 'closureId': K.C_PROV},
                                                        'nativeContextDigest': K.H('0'), 'universe': U1, 'programEntry': None,
                                                        'extents': [{'kind': 'symbol', 'paths': ['src/a.ts']}]}]}]
    if other == 'U2':
        cells.append(K.ref_cell('references', 'ts-tsconfig', U2, 'pkg-b', K.C_PROV2, ['pkg-b/src/b.ts']))
    else:
        cells.append(K.ref_cell('references', 'rust-cargo', UR, 'crate', K.C_PROV2, ['crate/src/lib.rs']))
    p = K.plan_one(cap='calls'); p['cells'] = cells
    inv_f = K.inv_symbol(); inv_f['cellOrdinal'] = 0
    i = K.base_inputs(enumerationPlan=p, inventories=[inv_f])
    if other == 'U2':
        inv_g = K.inv_symbol(universe=U2, nid=G_SYM, path='pkg-b/src/b.ts', qn='g'); inv_g['cellOrdinal'] = 1
        i['inventories'].append(inv_g)
        s, sc = K.scope('references', 'resolved-binding', U2, U1, [G_SYM], sid='2'); sc['enumeratorClosure'] = K.C_PROV2
        c, cv = K.coverage('references', 'resolved-binding', U2, U1, cid='2')
        K.install_pair(i, s, sc, c, cv)
    return i


R['preExisting'] = {}
for other in ('U2', 'rust'):
    inp = narrowed(other)
    for op in ('none', 'exists'):
        a = {'op': op, 'relation': 'references', 'minResolution': 'resolved-binding', 'endpoint': 'target', 'filters': []}
        R['preExisting']['%s/%s' % (other, op)] = {'34': ev(AM34, a, inp), '33': ev(AM33, a, inp)}
print('1. same inputs on frozen34 and frozen33:')
for k, v in R['preExisting'].items():
    print('   %-12s 34=%-40s 33=%s' % (k, json.dumps(v['34'])[:40], json.dumps(v['33'])[:60]))
R['identicalOn33'] = all(v['34'] == v['33'] for v in R['preExisting'].values())
print('   behaviour identical on source33:', R['identicalOn33'])

# 2. default-analysis reachability through the capability matrix
reg = AM34.REGISTRY
fam_modes = {fam: row.get('languageModes') for fam, row in reg['engineFamilies']['families'].items()}
cap_for = reg['capabilityForRelation']
incoming_rel = sorted(r for r, s in reg['relations'].items()
                      if s.get('plane') == 'native' and s.get('endpointTarget') != 'forbidden')
mpath = None
for d, _, fs in os.walk(S34 + '/docs/coop/design-corrections'):
    if '/reviews' in d:
        continue
    for fn in fs:
        if fn.startswith('native-capability-matrix') and fn.endswith('.json'):
            mpath = os.path.join(d, fn)
R['matrixPath'] = mpath
matrix = json.load(open(mpath)) if mpath else {}
R['matrixTopKeys'] = list(matrix)[:12]


def cell_status(cap, mode):
    caps = matrix.get('capabilities')
    rows = caps if isinstance(caps, list) else ([dict(v, id=k) for k, v in caps.items()] if isinstance(caps, dict) else [])
    for row in rows:
        if row.get('id') != cap and row.get('capabilityId') != cap:
            continue
        cells = row.get('cells') or row.get('modes') or {}
        if isinstance(cells, dict):
            v = cells.get(mode)
            return v if isinstance(v, str) else (v or {}).get('status') or (v or {}).get('state') or json.dumps(v)[:60]
        for c in cells:
            if c.get('languageMode') == mode or c.get('mode') == mode:
                return c.get('status') or c.get('state') or json.dumps(c)[:60]
    return None


R['defaultReachability'] = {}
for rel in incoming_rel:
    cap = cap_for.get(rel)
    per_fam = {}
    for fam, modes in fam_modes.items():
        per_fam[fam] = {m: cell_status(cap, m) for m in (modes or [])}
    mixed = {fam: st for fam, st in per_fam.items()
             if len({str(s).upper().startswith('NOT-SELECTED') for s in st.values()}) > 1}
    R['defaultReachability'][rel] = {'capability': cap, 'statusByFamily': per_fam, 'familiesMixingNotSelected': mixed}
    print('2. %-14s cap=%-22s families mixing NOT-SELECTED with requested modes: %s' % (rel, cap, list(mixed)))
print('   matrix:', mpath, 'top keys:', R['matrixTopKeys'])
print('   sample statuses:', json.dumps(R['defaultReachability'].get('references', {}).get('statusByFamily'))[:400])

# 3. per-row subjects
V = json.load(open(B2))
rows = {}
for mp in ('evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
           'scopedReviewOwnerDispositions'):
    for rid, row in V[mp].items():
        rows[mp + '/' + rid] = {'prior': str(row.get('priorStatusOn32'))[:170], 'evidence': str(row.get('evidence'))[:110],
                                'limits': str(row.get('limits'))[:90],
                                'owners': [o.split('/')[-1] for o in (row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or [])]}
R['rowSubjects'] = rows
print('\n3. row subjects:')
for k, v in rows.items():
    print('%-44s %s || owners=%s' % (k.split('/')[-1], v['prior'][:120].replace('\n', ' '), ','.join(v['owners'])[:80]))
json.dump(R, open(os.path.join(OUT, 'q10-reach-and-rows.json'), 'w'), indent=1, default=str)
print('wrote q10-reach-and-rows.json')
