"""Inject a genuine second program binding at CONSTRUCTION time and report the exact first
owner obligation that refuses.

A scratch variant of ts_pilot.py is produced by a single-line change to the cell's
`programBindings` list, so the second binding is present before any digest is taken and every
downstream identity derives from it. No serialized id is edited.
"""
import copy
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'portable'))
import author_portable as AP  # noqa: E402

R = Path('/private/tmp/opensip-design-corrections/claude-author-remint.v1')
SOURCE = R / 'source'
PACKAGE = R / 'package'
BASE_HELPERS = R / 'scratch/helpers-overlay'
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)

VARIANT = OUT / 'helpers-two-binding'
if VARIANT.exists():
    shutil.rmtree(VARIANT)
shutil.copytree(BASE_HELPERS, VARIANT)

src = (VARIANT / 'ts_pilot.py').read_text(encoding='utf-8')
name = '_default_unit_binding' if '_default_unit_binding(' in src else '_binding'
OLD = '"programBindings": [%s(provider_id, ctx_hex, uhex, extents, cand)],' % name
if OLD not in src:
    OLD = '"programBindings": [%s(provider_id, ctx_hex, uhex, "tsconfig.json", extents, cand)],' % name
assert src.count(OLD) == 1, src.count(OLD)
NEW = ('"programBindings": _two_bindings(%s(provider_id, ctx_hex, uhex, extents, cand)),' % name
       if 'extents, cand)' in OLD else
       '"programBindings": _two_bindings(%s(provider_id, ctx_hex, uhex, "tsconfig.json", extents, cand)),' % name)
helper = '''

def _two_bindings(default_binding):
    """EXPERIMENT: default-unit at ordinal 0 plus an explicit-plan-selection binding at 1."""
    import copy as _copy
    second = _copy.deepcopy(default_binding)
    second["ordinal"] = 1
    second["provenance"] = "explicit-plan-selection"
    second["programEntry"] = "tsconfig.json"
    return [default_binding, second]

'''
src = src.replace(OLD, NEW, 1)
anchor = 'def _inventory('
assert src.count(anchor) == 1
src = src.replace(anchor, helper.lstrip('\n') + '\n' + anchor, 1)
(VARIANT / 'ts_pilot.py').write_text(src, encoding='utf-8')

AP.load_helpers(PACKAGE, VARIANT, kit=SOURCE, out=OUT)
from helpers import ts_pilot as TP  # noqa: E402

F = AP.foundation(SOURCE)
CK = AP.transport(PACKAGE, 'chk')
M = AP.load_module('owner', F / 'identity-model.v3.py')

row = {'standing': 'EXPERIMENT: genuine two-binding cell. Not a claimed control.',
       'secondBinding': {'ordinal': 1, 'provenance': 'explicit-plan-selection',
                         'programEntry': 'tsconfig.json'}}
try:
    g = TP.build_ts_run()
    row['construction'] = 'BUILT'
    row['runId'] = g['runId']
except Exception as exc:
    row['construction'] = 'REFUSE'
    row['stage'] = 'construction'
    row['error'] = type(exc).__name__
    row['detail'] = str(exc)[:600]
    print(json.dumps(row, indent=1))
    json.dump(row, open(OUT / 'two-binding-injected.json', 'w'), indent=1)
    raise SystemExit(0)

export = g['store'].export()
(OUT / 'two-binding.store.json').write_text(json.dumps(export, indent=2, sort_keys=True) + '\n')
raw = json.dumps(export, indent=2, sort_keys=True).encode()
objects, blobs = CK.decode_store(raw, M, [])
run = objects[g['runId']][1]
try:
    M.open_run_closure(run, objects, blobs)
    row['structural'] = 'ADMIT'
except Exception as exc:
    row['structural'] = 'REFUSE'
    row['stage'] = 'open_run_closure'
    row['error'] = type(exc).__name__
    row['detail'] = str(exc)[:600]
    print(json.dumps(row, indent=1))
    json.dump(row, open(OUT / 'two-binding-injected.json', 'w'), indent=1)
    raise SystemExit(0)
try:
    M.close_run(run, objects, blobs)
    row['semantic'] = 'ADMIT'
except Exception as exc:
    row['semantic'] = 'REFUSE'
    row['stage'] = 'close_run'
    row['error'] = type(exc).__name__
    row['detail'] = str(exc)[:600]
print(json.dumps(row, indent=1))
json.dump(row, open(OUT / 'two-binding-injected.json', 'w'), indent=1)
