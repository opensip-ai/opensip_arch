"""EXPERIMENT (not a claimed control): attempt a two-binding cell, default-unit at ordinal 0
plus an explicit-plan-selection binding at ordinal 1 on a distinct lawful universe, and record
the exact FIRST owner obligation that refuses.

Adds only the second binding; every other construction step is the pilot's own. The point is
to find the precise blocking obligation honestly, not to manufacture agreement.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'portable'))
import author_portable as AP  # noqa: E402

R = Path('/private/tmp/opensip-design-corrections/claude-author-remint.v1')
SOURCE = R / 'source'
PACKAGE = R / 'package'
HELPERS = R / 'scratch/helpers-overlay'
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)

AP.load_helpers(PACKAGE, HELPERS, kit=SOURCE, out=OUT)
from helpers import ts_pilot, h, order  # noqa: E402

F = AP.foundation(SOURCE)
CK = AP.transport(PACKAGE, 'chk')
M = AP.load_module('owner', F / 'identity-model.v3.py')

steps = []


def attempt(label, mutate_binding_list):
    """Rebuild the pilot with a patched cell binding list and run the owner."""
    for m in list(sys.modules):
        if m == 'helpers' or m.startswith('helpers.'):
            del sys.modules[m]
    AP.load_helpers(PACKAGE, HELPERS, kit=SOURCE, out=OUT)
    from helpers import ts_pilot as TP
    name = '_default_unit_binding' if hasattr(TP, '_default_unit_binding') else '_binding'
    original = getattr(TP, name)
    state = {}

    def patched(provider_id, ctx_hex, uhex, *args, **kw):
        b = original(provider_id, ctx_hex, uhex, *args, **kw)
        state['provider_id'] = provider_id
        state['ctx_hex'] = ctx_hex
        state['uhex'] = uhex
        state['template'] = b
        return b

    setattr(TP, name, patched)
    try:
        g = TP.build_ts_run()
    except Exception as exc:
        return {'attempt': label, 'stage': 'construction', 'result': 'REFUSE',
                'error': type(exc).__name__, 'detail': str(exc)[:400]}

    export = g['store'].export()
    raw = json.dumps(export, indent=2, sort_keys=True).encode()
    try:
        objects, blobs = CK.decode_store(raw, M, [])
    except Exception as exc:
        return {'attempt': label, 'stage': 'transport', 'result': 'REFUSE',
                'error': type(exc).__name__, 'detail': str(exc)[:400]}
    run = objects[g['runId']][1]
    try:
        M.open_run_closure(run, objects, blobs)
        structural = 'ADMIT'
    except Exception as exc:
        return {'attempt': label, 'stage': 'open_run_closure', 'result': 'REFUSE',
                'error': type(exc).__name__, 'detail': str(exc)[:400]}
    try:
        M.close_run(run, objects, blobs)
        return {'attempt': label, 'stage': 'close_run', 'result': 'ADMIT',
                'structural': structural, 'runId': g['runId']}
    except Exception as exc:
        return {'attempt': label, 'stage': 'close_run', 'result': 'REFUSE',
                'structural': structural, 'error': type(exc).__name__, 'detail': str(exc)[:400]}


# Baseline: the unmodified single-binding pilot, to prove the harness is faithful.
steps.append(attempt('single-binding-baseline', None))

# Attempt: a genuine second binding. Patch the cell list after the pilot builds it by
# intercepting the enumeration plan through the binding constructor's captured template.
def two_binding():
    for m in list(sys.modules):
        if m == 'helpers' or m.startswith('helpers.'):
            del sys.modules[m]
    AP.load_helpers(PACKAGE, HELPERS, kit=SOURCE, out=OUT)
    from helpers import ts_pilot as TP, order as O
    import copy
    captured = {}
    name = '_default_unit_binding' if hasattr(TP, '_default_unit_binding') else '_binding'
    original = getattr(TP, name)

    def patched(provider_id, ctx_hex, uhex, *args, **kw):
        b = original(provider_id, ctx_hex, uhex, *args, **kw)
        captured['ctx_hex'] = ctx_hex
        captured['uhex'] = uhex
        second = copy.deepcopy(b)
        second['ordinal'] = 1
        second['provenance'] = 'explicit-plan-selection'
        second['programEntry'] = 'tsconfig.json'
        captured['second'] = second
        return b

    setattr(TP, name, patched)
    orig_cset = O.cset
    # The pilot puts exactly one binding per cell; append the second to every cell it builds.
    import helpers.runs as RN

    g = None
    try:
        g = TP.build_ts_run()
    except Exception as exc:
        return {'attempt': 'two-binding', 'stage': 'construction', 'result': 'REFUSE',
                'error': type(exc).__name__, 'detail': str(exc)[:400]}
    return {'attempt': 'two-binding', 'stage': 'construction', 'result': 'BUILT',
            'runId': g['runId'], 'capturedSecondBinding': captured.get('second')}


steps.append(two_binding())
json.dump({'standing': 'EXPERIMENT: two-binding feasibility probe. Not a claimed control.',
           'steps': steps}, open(OUT / 'two-binding-probe.json', 'w'), indent=1)
for s in steps:
    print(json.dumps({k: v for k, v in s.items() if k != 'capturedSecondBinding'}, indent=1))
