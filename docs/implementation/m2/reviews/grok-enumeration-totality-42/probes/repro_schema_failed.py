"""Private totality probe. Does not modify product or frozen evidence."""
from __future__ import annotations
import copy, hashlib, importlib.util, json, traceback
from pathlib import Path

E_PATH = Path("/tmp/opensip-implementation/m2-enumeration-join-trial-41/reference/archroot/docs/coop/design-corrections/foundation/enumeration_model.v1.py")
CASES = Path("/tmp/opensip-implementation/m2-enumeration-join-trial-41/mutation-check/cases.ndjson")
OUT = Path("/tmp/opensip-implementation/m2-grok-enumeration-totality-42/probes")

raw = E_PATH.read_bytes()
assert len(raw) == 50447
assert hashlib.sha256(raw).hexdigest() == "d32883fdfb7a40395169dfb078c1590844a7f6e85e2c15cc2315ab8990626992"
spec = importlib.util.spec_from_file_location("e39", E_PATH)
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

def load_label(label):
    with CASES.open() as f:
        for line in f:
            o = json.loads(line)
            if o["label"] == label:
                return o
    raise KeyError(label)

def kwargs_of(inp):
    kw = copy.deepcopy(inp)
    blobs = {}
    for k, v in (kw.get("source_blobs") or {}).items():
        if isinstance(v, str):
            blobs[k] = bytes.fromhex(v)
        else:
            blobs[k] = v
    kw["source_blobs"] = blobs
    return kw

def call(inp):
    try:
        out = E.admit_enumeration(**kwargs_of(inp))
        return {"ok": True, "result": out.get("result"), "refusals": out.get("refusals")}
    except Exception as exc:
        return {"ok": False, "type": type(exc).__name__, "message": str(exc), "tb": traceback.format_exc(-2)}

def set_path(obj, path, value):
    cur = obj
    for p in path[:-1]:
        cur = cur[p]
    cur[path[-1]] = value

baselines = {lab: load_label(lab) for lab in ("baseline-0", "baseline-14", "baseline-48")}
rows = []
# 18 crash mutations
for bi, lab in enumerate(("baseline-0", "baseline-14", "baseline-48")):
    idx = {0: 0, 1: 14, 2: 48}[bi]
    base = baselines[lab]["input"]
    for field in ("cellOrdinal", "programOrdinal", "kind"):
        for name, val in (("array", []), ("object", {})):
            inp = copy.deepcopy(base)
            set_path(inp, ["inventories", 0, field], val)
            got = call(inp)
            rows.append({"label": f"{idx}:['inventories', 0, '{field}']:{name}", "kind": "unhashable", **got})

# defined bool True vs False vs 0 occupancy
for lab in ("baseline-0",):
    base = baselines[lab]["input"]
    for field, values in (
        ("cellOrdinal", (("True", True), ("False", False), ("0", 0), ("1", 1))),
        ("programOrdinal", (("True", True), ("False", False), ("0", 0))),
        ("kind", (("True", True), ("False", False), ("file", "file"))),
    ):
        for name, val in values:
            inp = copy.deepcopy(base)
            set_path(inp, ["inventories", 0, field], val)
            got = call(inp)
            rows.append({"label": f"control-0-{field}-{name}", "kind": "locator-control", "value": val, "valueType": type(val).__name__, **got})

# schema-invalid but locators intact (schemaVersion array) — defined SCHEMA-only
inp = copy.deepcopy(baselines["baseline-0"]["input"])
set_path(inp, ["inventories", 0, "schemaVersion"], [])
rows.append({"label": "control-0-schemaVersion-array", "kind": "defined-schema-only", **call(inp)})

# python equality demo
eq = {
    "False==0": (False == 0),
    "True==1": (True == 1),
    "hashFalse==hash0": (hash(False) == hash(0)),
    "(False,0,'file')==(0,0,'file')": ((False, 0, "file") == (0, 0, "file")),
    "(True,0,'file')==(0,0,'file')": ((True, 0, "file") == (0, 0, "file")),
    "(True,0,'file')==(1,0,'file')": ((True, 0, "file") == (1, 0, "file")),
}

summary = {
    "eSha256": hashlib.sha256(raw).hexdigest(),
    "pythonEquality": eq,
    "unhashable": [r for r in rows if r["kind"] == "unhashable"],
    "controls": [r for r in rows if r["kind"] != "unhashable"],
}
(OUT / "repro-result.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
n_err = sum(1 for r in rows if r["kind"] == "unhashable" and not r["ok"])
n_ok = sum(1 for r in rows if r["kind"] == "unhashable" and r["ok"])
print(json.dumps({"unhashableErrors": n_err, "unhashableOk": n_ok, "controlRows": sum(1 for r in rows if r["kind"] != "unhashable")}))
