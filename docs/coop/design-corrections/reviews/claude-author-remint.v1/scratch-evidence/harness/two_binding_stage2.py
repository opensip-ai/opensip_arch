"""Stage 2 of the two-binding experiment: give the second binding a DISTINCT lawful universe,
so the remaining owner obligations are isolated and ordered rather than lumped together."""
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

VARIANT = OUT / 'helpers-two-binding-distinct'
if VARIANT.exists():
    shutil.rmtree(VARIANT)
shutil.copytree(BASE_HELPERS, VARIANT)

src = (VARIANT / 'ts_pilot.py').read_text(encoding='utf-8')
name = '_default_unit_binding' if '_default_unit_binding(' in src else '_binding'
OLD = '"programBindings": [%s(provider_id, ctx_hex, uhex, extents, cand)],' % name
assert src.count(OLD) == 1, src.count(OLD)
src = src.replace(
    OLD,
    '"programBindings": _two_bindings(st, %s(provider_id, ctx_hex, uhex, extents, cand), uni, ctx_hex),' % name,
    1)

helper = '''
def _two_bindings(st, default_binding, uni, ctx_hex):
    """EXPERIMENT: default-unit at ordinal 0 plus explicit-plan-selection at 1 on a DISTINCT
    universe. The second universe is a lawful sibling: same mode and context, a different
    program root set, minted and retained like any other universe record."""
    import copy as _copy
    uni2 = _copy.deepcopy(uni)
    uni2["programRootFiles"] = ["src/index.ts", "src/util.ts"]
    uhex2 = h.native_bare_hex("native.semantic-universe.typescript.v2", uni2)
    st.put_canonical_record("native.semantic-universe.typescript.v2", uni2)
    second = _copy.deepcopy(default_binding)
    second["ordinal"] = 1
    second["provenance"] = "explicit-plan-selection"
    second["programEntry"] = "tsconfig.json"
    second["universe"] = uhex2
    second["nativeContextDigest"] = ctx_hex
    return [default_binding, second]


'''
anchor = 'def _inventory('
assert src.count(anchor) == 1
src = src.replace(anchor, helper.lstrip('\n') + anchor, 1)
(VARIANT / 'ts_pilot.py').write_text(src, encoding='utf-8')

AP.load_helpers(PACKAGE, VARIANT, kit=SOURCE, out=OUT)
from helpers import ts_pilot as TP  # noqa: E402

F = AP.foundation(SOURCE)
CK = AP.transport(PACKAGE, 'chk')
M = AP.load_module('owner', F / 'identity-model.v3.py')

row = {'standing': 'EXPERIMENT stage 2: two bindings, distinct universes. Not a claimed control.'}
try:
    g = TP.build_ts_run()
    row['construction'] = 'BUILT'
    row['runId'] = g['runId']
except Exception as exc:
    row.update(construction='REFUSE', stage='construction',
               error=type(exc).__name__, detail=str(exc)[:600])
    print(json.dumps(row, indent=1))
    json.dump(row, open(OUT / 'two-binding-stage2.json', 'w'), indent=1)
    raise SystemExit(0)

raw = json.dumps(g['store'].export(), indent=2, sort_keys=True).encode()
objects, blobs = CK.decode_store(raw, M, [])
run = objects[g['runId']][1]
try:
    M.open_run_closure(run, objects, blobs)
    row['structural'] = 'ADMIT'
except Exception as exc:
    row.update(structural='REFUSE', stage='open_run_closure',
               error=type(exc).__name__, detail=str(exc)[:600])
    print(json.dumps(row, indent=1))
    json.dump(row, open(OUT / 'two-binding-stage2.json', 'w'), indent=1)
    raise SystemExit(0)
try:
    M.close_run(run, objects, blobs)
    row['semantic'] = 'ADMIT'
except Exception as exc:
    row.update(semantic='REFUSE', stage='close_run',
               error=type(exc).__name__, detail=str(exc)[:600])
    row['remainingObligations'] = str(exc).split(':', 1)[-1].split(',')
print(json.dumps(row, indent=1))
json.dump(row, open(OUT / 'two-binding-stage2.json', 'w'), indent=1)
