"""Independent S1/bypass probes for native-integration03 closed_idl slot guard."""
from __future__ import annotations

import copy
import json
import types
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-root-native-integration03-reproduction")
COPY = REVIEW / "copy"
RESULTS = REVIEW / "results"


def load(name):
    p = COPY / name
    m = types.ModuleType(name)
    m.__file__ = str(p)
    exec(compile(p.read_bytes(), str(p), "exec"), m.__dict__)
    return m


def code_of(fn):
    try:
        fn()
        return "accepted"
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__ + ":" + str(exc)[:240]


def main():
    IDL = load("closed_idl.py")
    PARENT = load("closed_idl-native02.py")
    R = load("render.py")
    owner = json.loads((COPY / "inputs/wire-carriers.v1.json").read_bytes())
    meta = json.loads((COPY / "inputs/wire-carriers.meta.schema.json").read_bytes())
    options = json.loads((COPY / "inputs/generator-options.json").read_bytes())
    rows = []

    def rec(name, passed, **detail):
        rows.append({"name": name, "passed": bool(passed), **detail})
        print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))

    def idl(o):
        return code_of(lambda: IDL.admit(copy.deepcopy(o), meta, options))

    def parent_idl(o):
        return code_of(lambda: PARENT.admit(copy.deepcopy(o), meta, options))

    def combined(o):
        def run():
            checked, receipt = IDL.admit(copy.deepcopy(o), meta, options)
            R.Renderer(checked).run()
        return code_of(run)

    checked, receipt = IDL.admit(copy.deepcopy(owner), meta, options)
    rec(
        "valid-owner-still-admits",
        receipt["nativeTypes"] == 68 and len(receipt["externalTypes"]) == 22,
        nativeTypes=receipt["nativeTypes"],
        externs=len(receipt["externalTypes"]),
    )
    renderer = R.Renderer(checked)
    rust, ts = renderer.run()
    rec("valid-owner-renderer-runs", bool(rust) and bool(ts) and len(renderer.selector_mappings) == 8, selectors=len(renderer.selector_mappings))

    records = [k for k, v in owner["records"].items() if v["kind"] == "record" and not k.endswith("FrameV2") and not k.endswith("FrameV3")]
    victim = records[0]
    proto = "typescript-semantic"
    envelope = owner["protocols"][proto]["envelope"]
    o = copy.deepcopy(owner)
    o["records"][victim]["members"][0]["type"] = {"t": "frame-payload", "protocol": proto}
    o["protocols"][proto]["frames"][0]["payload"] = {"t": "ref", "ref": victim}
    now = idl(o)
    was = parent_idl(o)
    rec(
        "original-s1-non-envelope-now-idl-protocol",
        "IDL_PROTOCOL" in now and now != "accepted",
        observed=now,
        parentObserved=was,
        victim=victim,
        envelope=envelope,
        parentAccepted=was == "accepted",
    )
    rec(
        "original-s1-parent-idl-still-accepted",
        was == "accepted",
        observed=was,
        note="native02 closed_idl admits the layering counterexample; 03 must not",
    )

    a, b = records[0], records[1]
    o = copy.deepcopy(owner)
    o["records"][a]["members"][0]["type"] = {"t": "ref", "ref": a}
    rec("true-self-ref-still-idl-cycle", "IDL_CYCLE" in idl(o), observed=idl(o))
    o = copy.deepcopy(owner)
    o["records"][a]["members"][0]["type"] = {"t": "ref", "ref": b}
    o["records"][b]["members"][0]["type"] = {"t": "ref", "ref": a}
    rec("true-pair-ref-still-idl-cycle", "IDL_CYCLE" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    o["records"][a]["members"][0]["type"] = {"t": "frame-payload", "protocol": proto}
    rec("non-envelope-field-without-cycle-edge-refuses", "IDL_PROTOCOL" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    o["records"]["Ts2FrameV2"]["members"][-1]["type"] = {"t": "nullable", "of": {"t": "frame-payload", "protocol": proto}}
    rec("hidden-nullable-on-envelope-payload-refuses", "IDL_PROTOCOL" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    o["protocols"][proto]["frames"][0]["payload"] = {"t": "frame-payload", "protocol": proto}
    rec("marker-as-protocol-frame-payload-refuses", "IDL_PROTOCOL" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    o["records"]["Ts2FrameV2"]["members"][0]["type"] = {"t": "frame-payload", "protocol": proto}
    rec("marker-on-envelope-non-payload-field-refuses", "IDL_PROTOCOL" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    o["records"]["Ts2FrameV2"]["members"][-1]["type"] = {"t": "frame-payload", "protocol": "rust-semantic"}
    rec("correct-envelope-wrong-protocol-refuses", "IDL_PROTOCOL" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    o["records"]["Rust3ProviderFrameV3"]["members"][-1]["type"] = {"t": "frame-payload", "protocol": "typescript-semantic"}
    rec("rust-envelope-ts-protocol-refuses", "IDL_PROTOCOL" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    scalar = next(iter(o["scalars"]))
    o["scalars"][scalar]["type"] = {"t": "frame-payload", "protocol": proto}
    obs = idl(o)
    rec("marker-as-scalar-target-refuses", obs != "accepted" and ("IDL_SCHEMA" in obs or "IDL_PROTOCOL" in obs), observed=obs, note="meta schema closes this placement before IDL_PROTOCOL")

    o = copy.deepcopy(owner)
    alias = next(k for k, v in o["records"].items() if v["kind"] == "alias")
    o["records"][alias]["target"] = {"t": "frame-payload", "protocol": proto}
    obs = idl(o)
    rec("marker-as-alias-target-refuses", obs != "accepted" and ("IDL_SCHEMA" in obs or "IDL_PROTOCOL" in obs), observed=obs, note="meta schema closes this placement before IDL_PROTOCOL")

    o = copy.deepcopy(owner)
    variant = next(k for k, v in o["records"].items() if v["kind"] == "variant-record")
    first_var = next(iter(o["records"][variant]["variants"].values()))
    first_member = next(iter(first_var))
    first_var[first_member] = {"t": "frame-payload", "protocol": proto}
    rec("marker-as-variant-member-refuses", "IDL_PROTOCOL" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    o["records"]["Ts2FrameV2"]["members"][-1]["type"] = {"t": "array", "items": {"t": "frame-payload", "protocol": proto}, "minItems": "0", "order": "sequence"}
    rec("array-wrapped-marker-on-payload-slot-refuses", "IDL_PROTOCOL" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    payload = next(f["payload"] for p in o["protocols"].values() for f in p["frames"] if isinstance(f.get("payload"), dict) and "select" in f["payload"])
    key = next(iter(payload["alternatives"]))
    payload["alternatives"][key] = {"t": "frame-payload", "protocol": proto}
    rec("marker-as-select-alternative-refuses", "IDL_PROTOCOL" in idl(o), observed=idl(o))

    o = copy.deepcopy(owner)
    o["records"][victim]["members"][0]["type"] = {"t": "frame-payload", "protocol": "no-such-protocol"}
    obs = idl(o)
    rec("unknown-protocol-refuses", obs != "accepted" and ("IDL_SCHEMA" in obs or "IDL_PROTOCOL" in obs), observed=obs, note="meta schema enumerates protocol names; unknown protocol is IDL_SCHEMA")

    # Behavioral justification: unconditional origin->envelope edge would self-cycle valid owner.
    envelope_name = owner["protocols"][proto]["envelope"]
    rec(
        "unconditional-origin-envelope-edge-would-self-cycle-valid-owner",
        envelope_name == "Ts2FrameV2" and owner["records"][envelope_name]["members"][-1]["type"]["t"] == "frame-payload",
        envelope=envelope_name,
        note="Valid payload marker origin is the envelope itself; origin->envelope is a self-edge. Slot check is the selected alternative.",
    )

    failed = [r for r in rows if not r["passed"]]
    out = {
        "standing": "independent Grok native03 S1/bypass probes; not product selection",
        "passed": not failed,
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "checks": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-s1.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
