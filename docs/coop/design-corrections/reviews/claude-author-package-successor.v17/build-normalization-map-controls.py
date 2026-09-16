"""S2 normalization-map discrimination controls: the TypeScript checkpoint Run, fully reminted per variant.

PORTABLE. Declared inputs only (--source/--package/--out, optional --helpers/--kit). NEW in author-package-migration.v1.

Each variant is a COMPLETE fresh construction of the same TypeScript Run as checkpoint3 (two clone bodies, L0 and L1,
interpreted by the TypeScript toolchain closure). Only the toolchain closure's normalization membership differs, set
before the graph is minted through ts_pilot.NORMALIZATION_CONTROL, so every downstream identity is derived.

  ts-map-absent                   no specification-map member                -> BODY_NORMALIZATION_MAP_MISSING
  ts-map-level-unmapped           map names L1 only; the L0 body is unmapped -> BODY_NORMALIZATION_LEVEL_UNMAPPED
  ts-map-level-swapped            map names L1's spec for L0                 -> BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH
  ts-spec-outside-closure         map names L0's spec, spec file not in tree -> BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE

These are AUTHOR constructions. Admission belongs to the frozen owner through check-export.v4.py; the expected
boundary for each is recorded in claims.json and checked by verify-package.py, never asserted here.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import author_portable as AP

_a = AP.arguments(__doc__.splitlines()[0])
PACKAGE = _a.package
OUTROOT = AP.fresh_out(_a.out)
AP.load_helpers(PACKAGE, _a.helpers, kit=_a.kit, out=OUTROOT)

VARIANTS = [
    ("ts-map-absent", {"includeMap": False}, "BODY_NORMALIZATION_MAP_MISSING"),
    ("ts-map-level-unmapped", {"mapLevels": {"L1-lexical": "L1-lexical"}}, "BODY_NORMALIZATION_LEVEL_UNMAPPED"),
    ("ts-map-level-swapped", {"mapLevels": {"L0-verbatim": "L1-lexical", "L1-lexical": "L1-lexical"}},
     "BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH"),
    ("ts-spec-outside-closure", {"treeLevels": ["L1-lexical"]}, "BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE"),
]


def build(tag, control, boundary):
    for m in list(sys.modules):
        if m == "helpers" or m.startswith("helpers."):
            del sys.modules[m]
    AP.load_helpers(PACKAGE, _a.helpers, kit=_a.kit, out=OUTROOT)
    from helpers import ts_pilot
    ts_pilot.NORMALIZATION_CONTROL = control
    g = ts_pilot.build_ts_run()
    export = g["store"].export()
    (OUTROOT / (tag + ".store.json")).write_text(json.dumps(export, indent=2, sort_keys=True) + "\n")
    return {"name": tag, "path": tag + ".store.json", "runId": g["runId"], "control": control,
            "expectedStructuralBoundary": boundary, "objects": len(export["objectTable"])}


rows = [build(*v) for v in VARIANTS]
(OUTROOT / "claims.json").write_text(json.dumps([{"name": r["name"], "path": r["path"], "runId": r["runId"]} for r in rows], indent=2) + "\n")
(OUTROOT / "variants.json").write_text(json.dumps(
    {"standing": "AUTHOR S2 map discrimination controls; freshly minted; expected owner boundary recorded, not asserted.",
     "distinctRunIds": len({r["runId"] for r in rows}) == len(rows), "variants": rows}, indent=2) + "\n")
for r in rows:
    print("%-26s %-72s expects %s" % (r["name"], r["runId"], r["expectedStructuralBoundary"]))
AP.write_provenance(_a)
