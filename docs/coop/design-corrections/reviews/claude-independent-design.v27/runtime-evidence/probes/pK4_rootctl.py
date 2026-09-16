"""PROBE K4 (v27) — correct the pK3 precedence metric (it compared against the DEFINITION line of
_unit_for_cell, not its call site) and measure whether any reference checker on snapshot27
exercises the new root-representation guard."""
import json, os, re, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
F = os.path.join(SRC, 'docs/coop/design-corrections')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
R = {'corrects': 'pK3.guardPrecedesBindingJoin used min(_unit_for_cell lines)=249, which is the '
                 'def, so the metric was wrong. Re-measured against real call sites.'}

lines = open(os.path.join(F, 'foundation/enumeration_model.v1.py'), encoding='utf-8').read().splitlines()
for n in (249, 581, 738, 747):
    print('%5d  %s' % (n, lines[n - 1].strip()[:150]))
    R.setdefault('lines', {})[n] = lines[n - 1].strip()
defs = [i for i, l in enumerate(lines, 1) if re.match(r'\s*def _unit_for_cell\(', l)]
calls = [i for i, l in enumerate(lines, 1) if '_unit_for_cell(' in l and i not in defs]
R['unitForCellDef'] = defs
R['unitForCellCalls'] = calls
R['guardCall'] = 581
R['guardPrecedesBindingJoinCorrected'] = all(581 < c for c in calls) and all(581 < p for p in (738, 740, 750, 757))
print('\n_unit_for_cell def=%s calls=%s' % (defs, calls))
print('guard(581) precedes every call and every PROGRAM_ENTRY raise:',
      R['guardPrecedesBindingJoinCorrected'])

# does the guard short-circuit, i.e. is the binding join reachable after a root refusal?
R['guardShortCircuits'] = 'return empty' in '\n'.join(lines[580:583])
print('guard short-circuits admit_enumeration:', R['guardShortCircuits'])

# ---- control coverage: does ANY reference checker exercise the new guard? ----
checkers = []
for dp, dn, fn in os.walk(F):
    if '/reviews/' in dp or '__pycache__' in dp:
        continue
    for n in fn:
        if n.startswith('check') and n.endswith('.py'):
            checkers.append(os.path.join(dp, n))
R['checkerCount'] = len(checkers)
hits = {}
for tok in ('NATIVE_UNIT_ROOT_REPRESENTATION', 'ENUMERATION_MEMBERSHIP_UNIT_ROOT',
            'admit_unit_roots', 'InternalUnitRootV1', 'rootPath'):
    h = [os.path.relpath(c, SRC) for c in checkers
         if tok in open(c, encoding='utf-8', errors='replace').read()]
    hits[tok] = h
    print('\n%-34s in %d/%d reference checkers' % (tok, len(h), len(checkers)))
    for x in h[:10]:
        print('     ', x)
R['checkerHits'] = hits
R['newRootGuardHasNoReferenceControl'] = not (hits['NATIVE_UNIT_ROOT_REPRESENTATION']
                                              or hits['ENUMERATION_MEMBERSHIP_UNIT_ROOT']
                                              or hits['admit_unit_roots'])
print('\nnew root guard exercised by NO reference checker:', R['newRootGuardHasNoReferenceControl'])

json.dump(R, open(os.path.join(OUT, 'pK4-rootctl.json'), 'w'), indent=1, default=str)
print('wrote pK4-rootctl.json')
