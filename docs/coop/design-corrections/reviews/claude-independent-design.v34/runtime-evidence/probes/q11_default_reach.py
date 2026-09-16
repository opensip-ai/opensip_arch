"""Q11 — correct rerun of Q10 part 2. Q10's matrix parser read the wrong shape and returned null for
every cell, so Q10 measured NOTHING about default reachability; that error is kept in its receipt.

Question: under the DEFAULT profile (native-capability-matrix requiredDefault: every unit requests every
capability whose (capability, unit mode) cell is not NOT-SELECTED), can a subject's own unit lack a
binding for an incoming-capable relation while another unit of the SAME engine family has one?
That happens exactly when a family mixes NOT-SELECTED cells with requested cells for that capability."""
import json, os

S34 = '/tmp/opensip-design-corrections/candidate-subject.v34/docs/coop/design-corrections'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v34/receipts'
M = json.load(open(S34 + '/native/native-capability-matrix.v2.json'))
REG = json.load(open(S34 + '/foundation/evaluator-projection-registry.v1.json'))
R = {'matrixTopLevelKeys': list(M)}

cells = None
for k, v in M.items():
    if isinstance(v, list) and v and isinstance(v[0], dict) and {'capability', 'mode', 'state'} <= set(v[0]):
        cells, R['cellArrayKey'] = v, k
        break
assert cells is not None, 'no cell array found'
state = {(c['capability'], c['mode']): c['state'] for c in cells}
R['cellCount'] = len(cells)
fam_modes = {fam: row.get('languageModes') or [] for fam, row in REG['engineFamilies']['families'].items()}
R['familyModes'] = fam_modes
rels = {r: s for r, s in REG['relations'].items() if s.get('plane') == 'native' and s.get('endpointTarget') != 'forbidden'}
R['byRelation'] = {}
print('cell array key: %s (%d cells)' % (R['cellArrayKey'], len(cells)))
for rel, spec in sorted(rels.items()):
    cap = REG['capabilityForRelation'].get(rel)
    per = {fam: {m: state.get((cap, m)) for m in modes} for fam, modes in fam_modes.items()}
    mixed = {fam: st for fam, st in per.items()
             if any(s == 'NOT-SELECTED' for s in st.values()) and any(s not in (None, 'NOT-SELECTED') for s in st.values())}
    R['byRelation'][rel] = {'capability': cap, 'endpointTarget': spec.get('endpointTarget'),
                            'statesByFamily': per, 'familiesMixingNotSelectedWithRequested': mixed}
    print('%-14s cap=%-14s mixed families=%s' % (rel, cap, list(mixed)))
    for fam, st in per.items():
        print('      %-8s %s' % (fam, st))
R['defaultReachable'] = any(v['familiesMixingNotSelectedWithRequested'] for v in R['byRelation'].values())
print('\nreachable under the DEFAULT profile through a same-family NOT-SELECTED mode:', R['defaultReachable'])
json.dump(R, open(os.path.join(OUT, 'q11-default-reach.json'), 'w'), indent=1)
print('wrote q11-default-reach.json')
