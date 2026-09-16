"""Full Run closure probe for programEntry x provenance on the TypeScript semantic fixture.

The maintained fixture (evaluator_semantic_fixture.v3.build_ts_semantic_graph) has NO U-1 unit
(`N.assign_membership([], paths)`) and binds its inventory cell as explicit-plan-selection with
programEntry "tsconfig.json". To exercise a U-1 default, a PROBE VARIANT of that fixture is executed from
its own source bytes (no file written, __file__ = the real fixture path so sibling loads are unchanged) with
exactly two textual substitutions, both asserted to match once:
  1. membership = N.assign_membership(<units from N.discover_units over the snapshot markers>, paths)
  2. the inventory cell binding's provenance and programEntry literals.
Everything else (native universe, config graph entry "tsconfig.json", Coverage, views, policy) is the
maintained fixture. Closed Runs use the check-semantic-replay.v3.close_positive sequence.
Tree: env VA_TREE; default frozen41 read-only. Receipt name: argv[1].
"""
import copy
import hashlib
import importlib.util
import json
import os
import sys
import traceback
import types
from pathlib import Path

TREE = Path(os.environ.get("VA_TREE", "/tmp/opensip-design-corrections/candidate-subject.v41"))
FOUND = TREE / "docs/coop/design-corrections/foundation"
RT = Path("/private/tmp/opensip-design-corrections/claude-program-entry-enforcement.v1")

_rs = importlib.util.spec_from_file_location("pe_replay", FOUND / "evaluator_replay_model.v3.py")
R = importlib.util.module_from_spec(_rs)
_rs.loader.exec_module(R)
IDENTITY = R.M

FIXTURE = FOUND / "evaluator_semantic_fixture.v3.py"
SRC = FIXTURE.read_text()
MEMB_OLD = "membership = N.assign_membership([], paths)"
BIND_OLD = ('"ordinal": 0, "provenance": "explicit-plan-selection",\n'
            '            "enumerator": {"status": "selected", "closureId": provider},\n'
            '            "nativeContextDigest": ctx, "universe": u1, "programEntry": "tsconfig.json",\n'
            '            "extents": inv_extents,')
BIND_NEW = ('"ordinal": 0, "provenance": __PE_PROVENANCE__,\n'
            '            "enumerator": {"status": "selected", "closureId": provider},\n'
            '            "nativeContextDigest": ctx, "universe": u1, "programEntry": __PE_ENTRY__,\n'
            '            "extents": inv_extents,')
assert SRC.count(MEMB_OLD) == 1 and SRC.count(BIND_OLD) == 1, "fixture text drifted"


def _units(N, sources, paths):
    markers = {}
    for p in paths:
        base = p.rsplit("/", 1)[-1]
        if base in ("tsconfig.json", "jsconfig.json", "package.json", "Cargo.toml"):
            raw = sources[p] if type(sources[p]) is bytes else sources[p].encode()
            row = {"sha256": hashlib.sha256(raw).hexdigest()}
            if base in ("tsconfig.json", "jsconfig.json"):
                row["allowJs"] = False
            markers[p] = row
    found = N.discover_units(markers)
    _units.last = {"markers": sorted(markers), "units": [{k: u.get(k) for k in ("rootPath", "languageMode", "markerPath", "provenance")}
                                                          for u in found["units"]]}
    return found["units"]


def variant(with_unit, provenance, entry):
    src = SRC.replace(BIND_OLD, BIND_NEW)
    if with_unit:
        src = src.replace(MEMB_OLD, "membership = N.assign_membership(__PE_UNITS__(N, sources, paths), paths)")
    mod = types.ModuleType("pe_semantic_variant")
    mod.__dict__.update(__file__=str(FIXTURE), __name__="pe_semantic_variant",
                        __PE_PROVENANCE__=provenance, __PE_ENTRY__=entry, __PE_UNITS__=_units)
    exec(compile(src, str(FIXTURE), "exec"), mod.__dict__)
    return mod


ATOM = {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}


def closed_run(S, graph):
    g = copy.deepcopy(graph)
    try:
        seed, objects, blobs, _ = S.seed_seal(g)
        _, owner = IDENTITY.open_run_closure(seed, objects, blobs)
        i = g["inputs"]
        out = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"], i["evaluationInputRefs"], objects, blobs, owner)
        run, objects, blobs = S.seal_derived(g, out, objects, blobs)
        actual = R.replay(run, objects, blobs)
        run_id = IDENTITY.close_run(run, objects, blobs)
        if run_id != actual["runId"]:
            raise AssertionError("close_run runId != replay runId")
    except Exception as exc:  # noqa: BLE001 - preserved verbatim
        return {"standing": "closed-run (semantic driver)", "closed": False, "exception": type(exc).__name__ + ":" + str(exc)[:600]}
    return {"standing": "closed-run (semantic driver)", "closed": True, "verdict": actual["verdict"], "runId": run_id,
            "exactManifest": out["proof"]["executionInputsDigest"] == g["inputs"]["executionInputsDigest"]}


results, order = {}, []
for name, with_unit, prov, entry, note in [
    ("R0-maintained-no-unit-explicit-marker-config", False, "explicit-plan-selection", "tsconfig.json", "maintained fixture bytes (substitution is identity)"),
    ("R1-unit-explicit-marker-config-control", True, "explicit-plan-selection", "tsconfig.json", "U-1 unit present; explicit non-null control"),
    ("R2-unit-default-null-control", True, "default-unit", None, "U-1 default control"),
    ("R3-unit-explicit-null-QUESTION", True, "explicit-plan-selection", None, "R2 with ONLY provenance changed"),
    ("R4-unit-default-nonnull-marker", True, "default-unit", "tsconfig.json", "default-unit carrying the marker"),
    ("R5-no-unit-explicit-null", False, "explicit-plan-selection", None, "maintained membership (no unit), entry null"),
]:
    order.append(name)
    entry_rec = {"note": note, "withUnit": with_unit, "provenance": prov, "programEntry": entry}
    try:
        S = variant(with_unit, prov, entry)
        graph = S.build_ts_semantic_graph(atom=ATOM, subject_kind="file")
        b = graph["enumerationPlan"]["cells"][0]["programBindings"][0]
        entry_rec["binding"] = {k: b[k] for k in ("provenance", "programEntry")}
        if with_unit:
            entry_rec["units"] = getattr(_units, "last", None)
        entry_rec["closedRun"] = closed_run(S, graph)
    except Exception as exc:  # noqa: BLE001
        entry_rec["buildError"] = type(exc).__name__ + ":" + str(exc)[:600]
        entry_rec["traceback"] = traceback.format_exc()[-1500:]
    results[name] = entry_rec

label = sys.argv[1] if len(sys.argv) > 1 else "probe-fullrun-base.json"
path = RT / "receipts" / label
if path.exists():
    raise SystemExit("refusing to overwrite " + str(path))
raw = json.dumps({"tree": str(TREE), "order": order, "worlds": results}, indent=2).encode() + b"\n"
path.write_bytes(raw)
for n in order:
    r = results[n]
    cr = r.get("closedRun") or {}
    print(n, "| units", (r.get("units") or {}).get("units"), "|",
          r.get("buildError") or (("CLOSED " + str(cr.get("verdict")) + " exact=" + str(cr.get("exactManifest"))) if cr.get("closed") else "NOT CLOSED " + str(cr.get("exception"))))
print("receipt", label, hashlib.sha256(raw).hexdigest())
