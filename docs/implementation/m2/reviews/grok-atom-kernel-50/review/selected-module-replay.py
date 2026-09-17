"""Replay pinned atom-kernel corpora against actual selected modules.

Uses the native-case15 reference interpreter (jsonschema installed). Does not stub
jsonschema and does not inline atom_model / native_evidence_model helpers.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

FOUND = Path(
    "/tmp/opensip-implementation/m2-reconstruction-subject-48/reference/archroot/docs/coop/design-corrections/foundation"
)
NATIVE = FOUND.parent / "native" / "native_evidence_model.v2.py"
TRIAL = Path("/tmp/opensip-implementation/m2-composition-trial-50")
OUT = Path("/tmp/opensip-implementation/m2-grok-atom-kernel-50-advisory/review/selected-module-replay.json")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


A = load("atom_model_v1_selected", FOUND / "atom_model.v1.py")
N = A.N
assert Path(NATIVE).resolve() == Path(A.NATIVE_PY).resolve()
assert hasattr(N, "sufficiency_v2")


def key_of(exc: BaseException):
    if isinstance(exc, A.AtomAdmissionError):
        return exc.key
    return None


def expected_value(exp):
    if isinstance(exp, dict) and "refused" in exp:
        return ("refused", exp["refused"])
    if isinstance(exp, dict) and "value" in exp:
        return ("value", exp["value"])
    return ("value", exp)


def run_case(corpus: str, c: dict):
    kind = c.get("kind")
    if corpus == "imported" or (c.get("label") and "atom" in c and "spec" in c):
        return A._eval_imported(c["atom"], c["subject"], c["inputs"], c["spec"])
    q = c.get("input")
    if kind == "scope":
        return A._path_in_scope(q["scope"], q["path"])
    if kind == "string":
        return A._cmp_string(q["cmp"], q["projected"], q["value"])
    if kind == "int":
        return A._cmp_int(q["cmp"], q["projected"], q["value"])
    if kind == "completeness":
        return [
            A._import_complete_runtime(q["wrapper"], q["payload"], {}),
            A._import_complete_history(q["wrapper"], q["payload"]),
            A._import_complete_test(q["wrapper"], q["payload"], {}, q["consumable"], q["staleness"]),
        ]
    if kind == "process":
        return A._test_process_result(q)
    if kind == "filters":
        return A._apply_import_filters(q["atom"], {}, q["projected"])
    if kind == "lookup":
        s = q["subject"]
        plan = None if q["plan"] is None else q["plan"]
        return A._lookup_rows(
            s["nativeSubjectId"],
            s["universe"],
            s["kind"],
            q["inventories"],
            plan,
            s.get("packageManifestPath"),
        )
    if kind == "occupancy":
        s = q["subject"]
        plan = None if q["plan"] is None else q["plan"]
        return A._runtime_occupancy(
            q["row"],
            s,
            {"inventories": q["inventories"], "enumerationPlan": plan},
        )
    if kind == "causes":
        return A._uniq_causes(q)
    if kind == "addresses":
        return A._sort_addrs(q)
    if kind == "result":
        return A._result(
            value=q["value"],
            kind="imported-atom",
            knownObservationAddresses=q["known"],
            uncertainObservationAddresses=q["uncertain"],
            causes=q["causes"],
            evaluationInputRefs=q["consumed"],
        )
    if kind == "entry":
        return A._entry_from_cov("calls", q)
    if kind == "fold":
        entry, ids = A._conservative_entry("calls", [(a[0], a[1]) for a in q])
        return [entry, ids]
    if kind == "sufficiency":
        return N.sufficiency_v2(
            q["req"],
            q["view"],
            bool(q["exported"]),
            bool(q["affected"]),
            int(q["depth"]),
        )
    raise RuntimeError("unhandled " + repr(kind))


def replay(label: str, rel: str) -> dict:
    ok = fail = 0
    fails = []
    path = TRIAL / rel
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        c = json.loads(line)
        exp = c.get("expected")
        kind, want = expected_value(exp)
        try:
            actual = run_case(label, c)
            if kind == "refused":
                fail += 1
                if len(fails) < 8:
                    fails.append({"i": i, "name": c.get("kind") or c.get("label"), "got": actual, "want": want})
            elif actual != want:
                fail += 1
                if len(fails) < 8:
                    fails.append({"i": i, "name": c.get("kind") or c.get("label"), "got": actual, "want": want})
            else:
                ok += 1
        except Exception as exc:
            got = key_of(exc)
            if kind == "refused" and got == want:
                ok += 1
            else:
                fail += 1
                if len(fails) < 8:
                    fails.append(
                        {
                            "i": i,
                            "name": c.get("kind") or c.get("label"),
                            "got": got or (type(exc).__name__ + ":" + str(exc)[:180]),
                            "want": want,
                        }
                    )
    return {"ok": ok, "fail": fail, "fails": fails}


def main() -> int:
    reports = {
        "interpreter": sys.executable,
        "version": sys.version,
        "selectedAtom": str(FOUND / "atom_model.v1.py"),
        "selectedNative": str(A.NATIVE_PY),
        "jsonschemaStubbed": False,
        "helpersInlined": False,
        "errorComparison": "typed key only",
        "corpora": {},
    }
    for label, rel in [
        ("helpers", "atom-helper-check/cases.ndjson"),
        ("inventory", "atom-inventory-check/cases.ndjson"),
        ("results", "atom-result-check/cases.ndjson"),
        ("imported", "imported-atom-check/cases.ndjson"),
        ("native-sufficiency", "native-sufficiency-check/cases.ndjson"),
    ]:
        row = replay(label, rel)
        reports["corpora"][label] = row
        print(label, "ok", row["ok"], "fail", row["fail"])
        for item in row["fails"]:
            print(" ", item)
    OUT.write_text(json.dumps(reports, indent=2, default=str) + "\n", encoding="utf-8")
    if any(v["fail"] for v in reports["corpora"].values()):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
