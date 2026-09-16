"""P02 — substantive execution of the changed execution-inputs law.

Tests the published FIRST-MATCH precedence and the external sourceUniverse join against the actual
model, including the reachability argument the contract makes for row 3 before row 4.
SCOPE: unit-level execution of the published model functions. Labelled as such; full-Run controls
are assessed separately.
"""
import importlib.util, inspect, itertools, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v33/receipts'
spec = importlib.util.spec_from_file_location('eim33', os.path.join(F, 'execution_inputs_model.v1.py'))
M = importlib.util.module_from_spec(spec)
sys.modules['eim33'] = M
spec.loader.exec_module(M)
R = {'probeScope': 'unit-level execution of published model functions; not a full admitted Run'}

print('--- derived_applicability source ---')
src = inspect.getsource(M.derived_applicability)
R['derivedApplicabilitySource'] = src
print(src[:1400])

# ---- exhaustive precedence grid ----
RELS = ['vcs-change', 'file', 'symbol']
UNIS = [None, 'u' * 64]
STATUS = ['selected', 'unselected']
MATRIX = [None, 'UNSUPPORTED-TYPED', 'SUPPORTED']
VCS = [None, 'none', 'git']
rows = []
for rel, uni, st, mx, vk in itertools.product(RELS, UNIS, STATUS, MATRIX, VCS):
    got = M.derived_applicability(rel, uni, st, mx, vk)
    rows.append({'relation': rel, 'universe': 'null' if uni is None else 'U', 'status': st,
                 'matrix': mx, 'vcsKind': vk, 'applicability': got})
R['gridSize'] = len(rows)
R['grid'] = rows
tokens = sorted({r['applicability'] for r in rows})
R['tokensReached'] = tokens
print('\ngrid cells: %d | distinct tokens reached: %s' % (len(rows), tokens))
R['allFiveTokensReachable'] = set(tokens) == {'inapplicable-vcs', 'unsupported-typed',
                                              'unavailable-unselected', 'unavailable-null-universe',
                                              'supported-available'}
print('all five advertised tokens reachable:', R['allFiveTokensReachable'])

# ---- the contract's own reachability argument for row3 before row4 ----
unsel_null = [r for r in rows if r['status'] == 'unselected' and r['universe'] == 'null'
              and r['matrix'] != 'UNSUPPORTED-TYPED' and not (r['relation'] == 'vcs-change' and r['vcsKind'] == 'none')]
R['unselectedWithNullU'] = {'cases': len(unsel_null),
                            'allUnavailableUnselected': all(r['applicability'] == 'unavailable-unselected'
                                                            for r in unsel_null)}
print('\nunselected + null U -> unavailable-unselected in all %d cases: %s'
      % (len(unsel_null), R['unselectedWithNullU']['allUnavailableUnselected']))
sel_null = [r for r in rows if r['status'] == 'selected' and r['universe'] == 'null'
            and r['matrix'] != 'UNSUPPORTED-TYPED' and not (r['relation'] == 'vcs-change' and r['vcsKind'] == 'none')]
R['selectedWithNullU'] = {'cases': len(sel_null),
                          'allNullUniverse': all(r['applicability'] == 'unavailable-null-universe'
                                                 for r in sel_null)}
print('selected + null U   -> unavailable-null-universe in all %d cases: %s'
      % (len(sel_null), R['selectedWithNullU']['allNullUniverse']))
R['twoStatesStayDistinct'] = (R['unselectedWithNullU']['allUnavailableUnselected']
                              and R['selectedWithNullU']['allNullUniverse'])

# ---- row 2 outranks rows 3 and 4 ----
unsup = [r for r in rows if r['matrix'] == 'UNSUPPORTED-TYPED'
         and not (r['relation'] == 'vcs-change' and r['vcsKind'] == 'none')]
R['unsupportedOutranksUnselectedAndNullU'] = all(r['applicability'] == 'unsupported-typed' for r in unsup)
print('UNSUPPORTED-TYPED outranks unselected and null-U in all %d cases: %s'
      % (len(unsup), R['unsupportedOutranksUnselectedAndNullU']))

# ---- row 1 outranks everything ----
vcsnone = [r for r in rows if r['relation'] == 'vcs-change' and r['vcsKind'] == 'none']
R['vcsNoneOutranksAll'] = all(r['applicability'] == 'inapplicable-vcs' for r in vcsnone)
print('vcs-change + kind=none outranks all in %d cases: %s' % (len(vcsnone), R['vcsNoneOutranksAll']))

# ---- the contract's precedence table matches the model constant ----
tbl = getattr(M, 'APPLICABILITY_PRECEDENCE', None)
R['modelPrecedenceConstant'] = tbl
print('\nmodel precedence constant:', json.dumps(tbl)[:320] if tbl else 'not exported under that name')
contract = open(os.path.join(F, 'execution-inputs-contract.v1.md'), encoding='utf-8').read()
order_doc = ['inapplicable-vcs', 'unsupported-typed', 'unavailable-unselected',
             'unavailable-null-universe', 'supported-available']
pos = [contract.index('`%s`' % t) for t in order_doc]
R['contractTableIsInPublishedOrder'] = pos == sorted(pos)
print('contract table lists the five tokens in precedence order:', R['contractTableIsInPublishedOrder'])

json.dump(R, open(os.path.join(OUT, 'p02-execlaw.json'), 'w'), indent=1, default=str)
print('\nwrote p02-execlaw.json')
