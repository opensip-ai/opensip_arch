"""Diagnose EVALUATION_VIEW_ROOTS on the asymmetric fixture shape."""
import importlib.util, json
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/repair-selection-successor.v2/source')
FOUND = SRC / 'docs/coop/design-corrections/foundation'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load('dev_replay', FOUND / 'check-replay.v3.py')
F, M = P.F, P.M
SYMBOL_ROWS = [{'nativeSubjectId': 'ts-symbol:src/index.ts#x', 'qualifiedName': 'x'}]

for label, kw in [('symbols only (control)', dict(multiple_universes=True, symbol_rows=SYMBOL_ROWS)),
                  ('asymmetric', dict(multiple_universes=True, symbol_rows=SYMBOL_ROWS,
                                      symbol_only_second_program=True))]:
    g = F.build_file_inputs(**kw)
    print('===', label)
    print('  graph viewIds       ', len(g['viewIds']))
    refs = [r for r in g['inputs']['evaluationInputRefs'] if r['domain'] == 'view']
    print('  inputRefs view count', len(refs))
    vset = {v.split(':', 1)[1] for v in g['viewIds']}
    rset = {r['digest'] for r in refs}
    print('  viewIds - refs      ', sorted(vset - rset))
    print('  refs - viewIds      ', sorted(rset - vset))
    inv = g['inventoryResults']
    print('  inventories         ', [(i['cellOrdinal'], i['programOrdinal'], i['kind'], i['state'])
                                     for _d, i in inv])
    ep = g['enumerationPlan']
    print('  cells               ', [(c['capabilityId'], c['kinds'],
                                      [(b['ordinal'], (b['universe'] or 'null')[:8]) for b in c['programBindings']])
                                     for c in ep['cells']])
    print('  population kinds    ', sorted({p['kind'] for p in g['inputs']['population'].values()}))
    print('  population universes', sorted({p['universe'][:8] for p in g['inputs']['population'].values()}))
    try:
        seed, objects, blobs, _ = F.seal_fixture(g)
        M.open_run_closure(seed, objects, blobs)
        print('  open_run_closure    : ADMIT')
    except Exception as exc:
        print('  open_run_closure    : REFUSE', type(exc).__name__, str(exc)[:160])
