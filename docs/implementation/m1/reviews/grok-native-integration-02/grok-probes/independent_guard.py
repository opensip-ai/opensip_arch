"""Independent executable counterexamples for closed_idl and TS assembly joins."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import types
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-grok-native-integration-review-02/review")
COPY = REVIEW / "copy"
RESULTS = REVIEW / "results"
NODE = "/Users/sb/.nvm/versions/node/v24.16.0/bin/node"
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"


def load(name):
    p = COPY / name
    m = types.ModuleType(name)
    m.__file__ = str(p)
    exec(compile(p.read_bytes(), str(p), "exec"), m.__dict__)
    return m


class Cases:
    def __init__(self):
        self.rows = []

    def rec(self, name, passed, **detail):
        self.rows.append({"name": name, "passed": bool(passed), **detail})
        print(("PASS" if passed else "FAIL"), name)


def code_of(fn):
    try:
        fn()
        return "accepted"
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__ + ":" + str(exc)[:200]


def main():
    C = Cases()
    IDL = load("closed_idl.py")
    R = load("render.py")
    owner = json.loads((COPY / "inputs/wire-carriers.v1.json").read_bytes())
    meta = json.loads((COPY / "inputs/wire-carriers.meta.schema.json").read_bytes())
    options = json.loads((COPY / "inputs/generator-options.json").read_bytes())

    def admit(o, opts=options):
        checked, receipt = IDL.admit(o, meta, opts)
        renderer = R.Renderer(checked)
        renderer.run()
        return checked, receipt, renderer

    _, receipt, renderer = admit(copy.deepcopy(owner))
    C.rec("baseline-admit-68-native-22-extern-8-selectors", receipt["nativeTypes"] == 68 and len(receipt["externalTypes"]) == 22 and len(renderer.selector_mappings) == 8, receipt=receipt)

    # Unknown type form
    o = copy.deepcopy(owner)
    o["scalars"][next(iter(o["scalars"]))]["type"] = {"t": "int32"}
    C.rec("unknown-type-int32-refuses-idl-type-or-schema", code_of(lambda: admit(o)).split(":")[0] in ("IdlRefusal",) and "IDL_TYPE" in code_of(lambda: admit(o)) or "IDL_SCHEMA" in code_of(lambda: admit(o)), observed=code_of(lambda: admit(o)))

    # Unselected extern join
    o = copy.deepcopy(owner)

    def first_extern(obj):
        pending = [obj["scalars"], obj["records"], obj["protocols"]]
        while pending:
            value = pending.pop()
            if isinstance(value, dict):
                if value.get("t") == "extern":
                    return value
                pending.extend(value.values())
            elif isinstance(value, list):
                pending.extend(value)
        raise AssertionError("missing")

    first_extern(o)["schemaRef"] = "opensip.product.unselected#/$defs/Nope"
    C.rec("unselected-extern-ref-refuses", "IDL_EXTERN" in code_of(lambda: admit(o)), observed=code_of(lambda: admit(o)))

    # Duplicate generated extern registry names
    opts = copy.deepcopy(options)
    opts["entryPoints"].append({"ref": "opensip.product.other#/$defs/X", "typeName": options["entryPoints"][0]["typeName"]})
    C.rec("duplicate-generated-extern-typeName-refuses", "IDL_EXTERN_REGISTRY" in code_of(lambda: admit(owner, opts)), observed=code_of(lambda: admit(owner, opts)))

    # Implicit frame-payload cycle: record field is frame-payload of a protocol whose envelope payload refs that record.
    o = copy.deepcopy(owner)
    recs = [k for k, v in o["records"].items() if v["kind"] == "record" and not k.endswith("FrameV2") and not k.endswith("FrameV3")]
    victim = recs[0]
    proto_name = "typescript-semantic"
    envelope = o["protocols"][proto_name]["envelope"]
    o["records"][victim]["members"][0]["type"] = {"t": "frame-payload", "protocol": proto_name}
    o["protocols"][proto_name]["frames"][0]["payload"] = {"t": "ref", "ref": victim}
    idl_only = code_of(lambda: IDL.admit(o, meta, options))
    combined = code_of(lambda: admit(o))
    C.rec(
        "combined-admit-refuses-frame-payload-cycle-shape",
        combined != "accepted",
        observed=combined,
        victim=victim,
        envelope=envelope,
    )
    C.rec(
        "idl-graph-does-not-add-frame-payload-field-edges",
        "accepted" in idl_only or idl_only == "accepted",
        observed=idl_only,
        note="closed_idl.admit currently accepts a non-envelope record field of frame-payload plus envelope payload ref to that record. Combined Renderer then refuses 'frame-payload outside declared envelope'. Layering gap, not a silent combined accept.",
    )

    # Nullable wrapping of a self-ref
    o = copy.deepcopy(owner)
    a = recs[1]
    o["records"][a]["members"][0]["type"] = {"t": "nullable", "of": {"t": "ref", "ref": a}}
    C.rec("nullable-self-ref-cycle-refuses", "IDL_CYCLE" in code_of(lambda: admit(o)), observed=code_of(lambda: admit(o)))

    # Same-emitted-type alternatives (uint64 vs uint64)
    o = copy.deepcopy(owner)
    payload = next(f["payload"] for p in o["protocols"].values() for f in p["frames"] if isinstance(f["payload"], dict) and "select" in f["payload"])
    keys = list(payload["alternatives"])
    payload["alternatives"][keys[0]] = {"t": "uint64", "max": "1"}
    payload["alternatives"][keys[1]] = {"t": "uint64", "max": "2"}
    C.rec("same-emitted-selector-types-refuse", "identical emitted selection alternative types" in code_of(lambda: admit(o)), observed=code_of(lambda: admit(o)))

    # Type widening: replace a uint64 field with text
    o = copy.deepcopy(owner)
    member = o["records"]["Ts2FrameV2"]["members"][0]
    member["type"] = {"t": "text", "nfc": True}
    # This may fail renderer envelope layout rather than IDL.
    C.rec("header-field-widened-to-text-refuses", code_of(lambda: admit(o)) != "accepted", observed=code_of(lambda: admit(o)))

    # Duplicate scalar/record name
    o = copy.deepcopy(owner)
    shared = next(iter(o["scalars"]))
    o["records"][shared] = copy.deepcopy(next(iter(o["records"].values())))
    C.rec("duplicate-native-declaration-name-refuses", "IDL_NAME" in code_of(lambda: admit(o)), observed=code_of(lambda: admit(o)))

    failed = [r for r in C.rows if not r["passed"]]
    out = {"standing": "Independent closed-IDL/renderer guard probes", "passed": not failed, "caseCount": len(C.rows), "failedCount": len(failed), "failed": [r["name"] for r in failed], "checks": C.rows}
    (RESULTS / "independent-guard.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
