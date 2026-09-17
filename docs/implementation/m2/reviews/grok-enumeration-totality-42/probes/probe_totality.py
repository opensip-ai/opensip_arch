"""Private totality probe. Does not modify product or frozen evidence."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

PY = Path(sys.executable)
assert sys.flags.int_max_str_digits == 0 and sys.get_int_max_str_digits() == 0

OUT = Path("/tmp/opensip-implementation/m2-grok-enumeration-totality-42/probes")
E_SEL = Path(
    "/tmp/opensip-implementation/m2-enumeration-join-trial-41/reference/archroot"
    "/docs/coop/design-corrections/foundation/enumeration_model.v1.py"
)
E_CAND = Path(
    "/tmp/opensip-implementation/m2-enumeration-totality-candidate-42/reference/archroot"
    "/docs/coop/design-corrections/foundation/enumeration_model.v1.py"
)
CASES = Path("/tmp/opensip-implementation/m2-enumeration-join-trial-41/mutation-check/cases.ndjson")
EXC = Path("/tmp/opensip-implementation/m2-enumeration-join-trial-41/mutation-check/oracle-exceptions.json")
BOOL_CASES = Path("/tmp/opensip-implementation/m2-enumeration-join-trial-41/boolean-check/cases.ndjson")
CAND_CASES = Path("/tmp/opensip-implementation/m2-enumeration-totality-candidate-42/cases.ndjson")

SEL_SHA = "d32883fdfb7a40395169dfb078c1590844a7f6e85e2c15cc2315ab8990626992"
CAND_SHA = "a02960c631df0f0342f039fcef395dbba402d67453dbc9aba760fad0e6719d5c"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_mod(name: str, path: Path):
    raw = path.read_bytes()
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, len(raw), hashlib.sha256(raw).hexdigest()


def kwargs_of(inp: dict) -> dict:
    kw = copy.deepcopy(inp)
    blobs = {}
    for k, v in (kw.get("source_blobs") or {}).items():
        blobs[k] = bytes.fromhex(v) if isinstance(v, str) else v
    kw["source_blobs"] = blobs
    return kw


def call(mod, inp: dict) -> dict:
    try:
        out = mod.admit_enumeration(**kwargs_of(inp))
        return {"ok": True, "result": out.get("result"), "refusals": list(out.get("refusals") or [])}
    except Exception as exc:
        return {
            "ok": False,
            "type": type(exc).__name__,
            "message": str(exc),
            "tb": traceback.format_exc(-2),
        }


def set_path(obj, path, value):
    cur = obj
    for p in path[:-1]:
        cur = cur[p]
    cur[path[-1]] = value


def load_label(path: Path, label: str) -> dict:
    with path.open() as f:
        for line in f:
            o = json.loads(line)
            if o["label"] == label:
                return o
    raise KeyError(label)


sel, sel_bytes, sel_sha = load_mod("e39_selected", E_SEL)
cand, cand_bytes, cand_sha = load_mod("e39_candidate", E_CAND)
assert sel_bytes == 50447 and sel_sha == SEL_SHA
assert cand_bytes == 50678 and cand_sha == CAND_SHA

C = sel.C
eq = {
    "False==0": False == 0,
    "True==1": True == 1,
    "hashFalse==hash0": hash(False) == hash(0),
    "(False,0,'file')==(0,0,'file')": (False, 0, "file") == (0, 0, "file"),
    "(True,0,'file')==(0,0,'file')": (True, 0, "file") == (0, 0, "file"),
    "(True,0,'file')==(1,0,'file')": (True, 0, "file") == (1, 0, "file"),
    "0.0==0": 0.0 == 0,
    "1.0==1": 1.0 == 1,
    "hash0.0==hash0": hash(0.0) == hash(0),
    "C.equal_typed(False,0)": C.equal_typed(False, 0),
    "C.equal_typed(True,1)": C.equal_typed(True, 1),
    "C.equal_typed(0.0,0)": C.equal_typed(0.0, 0),
    "type(False) is int": type(False) is int,
    "isinstance(False,int)": isinstance(False, int),
}

oracle = json.loads(EXC.read_text())
assert len(oracle) == 18

baselines = {lab: load_label(CASES, lab) for lab in ("baseline-0", "baseline-14", "baseline-48")}

unhashable = []
for bi, lab in enumerate(("baseline-0", "baseline-14", "baseline-48")):
    idx = {0: 0, 1: 14, 2: 48}[bi]
    base = baselines[lab]["input"]
    for field in ("cellOrdinal", "programOrdinal", "kind"):
        for name, val in (("array", []), ("object", {})):
            label = f"{idx}:['inventories', 0, '{field}']:{name}"
            inp = copy.deepcopy(base)
            set_path(inp, ["inventories", 0, field], val)
            selected = call(sel, inp)
            candidate = call(cand, inp)
            unhashable.append({"label": label, "field": field, "mut": name, "selected": selected, "candidate": candidate})

# oracle TypeError messages
oracle_by = {row["label"]: row for row in oracle}
oracle_match = []
for row in unhashable:
    o = oracle_by[row["label"]]
    s = row["selected"]
    oracle_match.append(
        {
            "label": row["label"],
            "oracleType": o["type"],
            "oracleMessage": o["message"],
            "selectedType": s.get("type"),
            "selectedMessage": s.get("message"),
            "typesMatch": (not s["ok"]) and s.get("type") == o["type"] and s.get("message") == o["message"],
        }
    )

controls = []
base0 = baselines["baseline-0"]["input"]
for field, values in (
    ("cellOrdinal", (("True", True), ("False", False), ("0", 0), ("1", 1), ("None", None), ("0.0", 0.0), ("1.0", 1.0))),
    ("programOrdinal", (("True", True), ("False", False), ("0", 0), ("None", None), ("0.0", 0.0))),
    ("kind", (("True", True), ("False", False), ("file", "file"), ("None", None))),
    ("schemaVersion", (("array", []), ("object", {}), ("True", True))),
):
    for name, val in values:
        inp = copy.deepcopy(base0)
        set_path(inp, ["inventories", 0, field], val)
        controls.append(
            {
                "label": f"control-0-{field}-{name}",
                "field": field,
                "valueType": type(val).__name__,
                "selected": call(sel, inp),
                "candidate": call(cand, inp),
            }
        )

# Replay every defined mutation case on selected and candidate (result+refusals).
defined = {"n": 0, "selectedMatch": 0, "candidateMatch": 0, "selectedMismatch": [], "candidateMismatch": []}
with CASES.open() as f:
    for line in f:
        o = json.loads(line)
        defined["n"] += 1
        exp_r = o["expected"]["result"]
        exp_f = list(o["expected"]["refusals"])
        s = call(sel, o["input"])
        c = call(cand, o["input"])
        if s.get("ok") and s["result"] == exp_r and s["refusals"] == exp_f:
            defined["selectedMatch"] += 1
        else:
            if len(defined["selectedMismatch"]) < 8:
                defined["selectedMismatch"].append({"label": o["label"], "got": s, "exp": [exp_r, exp_f]})
        if c.get("ok") and c["result"] == exp_r and c["refusals"] == exp_f:
            defined["candidateMatch"] += 1
        else:
            if len(defined["candidateMismatch"]) < 8:
                defined["candidateMismatch"].append({"label": o["label"], "got": c, "exp": [exp_r, exp_f]})

# Boolean diagnostic cases: selected E39 vs candidate vs expected.
bool_rows = []
bool_summary = {"n": 0, "selectedMatch": 0, "candidateMatch": 0}
with BOOL_CASES.open() as f:
    for line in f:
        o = json.loads(line)
        bool_summary["n"] += 1
        exp_r = o["expected"]["result"]
        exp_f = list(o["expected"]["refusals"])
        s = call(sel, o["input"])
        c = call(cand, o["input"])
        sm = s.get("ok") and s["result"] == exp_r and s["refusals"] == exp_f
        cm = c.get("ok") and c["result"] == exp_r and c["refusals"] == exp_f
        if sm:
            bool_summary["selectedMatch"] += 1
        if cm:
            bool_summary["candidateMatch"] += 1
        if o["label"].endswith(":False") or o["label"].endswith(":True") or o["label"].endswith(":0.0"):
            bool_rows.append({"label": o["label"], "expected": exp_f, "selected": s, "candidate": c, "selectedMatch": sm, "candidateMatch": cm})

# Candidate formerly-unhashable expected rows
former = []
with CAND_CASES.open() as f:
    for line in f:
        o = json.loads(line)
        if o["label"].startswith("formerly-unhashable-"):
            c = call(cand, o["input"])
            former.append(
                {
                    "label": o["label"],
                    "expected": o["expected"]["refusals"],
                    "got": c.get("refusals"),
                    "match": c.get("ok") and c["result"] == o["expected"]["result"] and c["refusals"] == o["expected"]["refusals"],
                }
            )

summary = {
    "python": sys.version.split()[0],
    "intMaxStrDigitsFlags": sys.flags.int_max_str_digits,
    "intMaxStrDigitsGet": sys.get_int_max_str_digits(),
    "selected": {"bytes": sel_bytes, "sha256": sel_sha},
    "candidate": {"bytes": cand_bytes, "sha256": cand_sha},
    "pythonEquality": eq,
    "unhashable": unhashable,
    "oracleMatch": {
        "n": len(oracle_match),
        "allMatch": all(r["typesMatch"] for r in oracle_match),
        "rows": oracle_match,
    },
    "candidateUnhashableAllRefuseSchemaThenMissing": all(
        r["candidate"]["ok"]
        and r["candidate"]["result"] == "REFUSE"
        and r["candidate"]["refusals"] == ["ENUMERATION_INVENTORY_SCHEMA", "ENUMERATION_INVENTORY_MISSING_RECORD"]
        for r in unhashable
    ),
    "controls": controls,
    "definedMutationReplay": defined,
    "booleanReplay": bool_summary,
    "booleanFalseTrueSample": bool_rows,
    "candidateFormerlyUnhashable": {
        "n": len(former),
        "allMatch": all(r["match"] for r in former),
        "rows": former,
    },
}
(OUT / "totality-result.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
print(
    json.dumps(
        {
            "selectedSha": sel_sha,
            "candidateSha": cand_sha,
            "oracleAllMatch": summary["oracleMatch"]["allMatch"],
            "unhashableSelectedErrors": sum(1 for r in unhashable if not r["selected"]["ok"]),
            "unhashableCandidateOk": sum(1 for r in unhashable if r["candidate"]["ok"]),
            "candidateSchemaThenMissing": summary["candidateUnhashableAllRefuseSchemaThenMissing"],
            "definedN": defined["n"],
            "definedSelectedMatch": defined["selectedMatch"],
            "definedCandidateMatch": defined["candidateMatch"],
            "boolN": bool_summary["n"],
            "boolSelectedMatch": bool_summary["selectedMatch"],
            "boolCandidateMatch": bool_summary["candidateMatch"],
            "formerN": len(former),
            "formerAllMatch": all(r["match"] for r in former),
        }
    )
)
