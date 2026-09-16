#!/usr/bin/env python3
"""Mutation controls for check.py: each control seeds one defect into a temporary copy of the candidate and requires
that at least one named check fails. Proves the reference check can fail; not approval.

Run: /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B selftest.py
"""
import copy, json, shutil, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
from jsonschema import Draft202012Validator  # noqa: E402
import common as CM  # noqa: E402
from check_static import Static  # noqa: E402
from check_reference import Reference  # noqa: E402


def mem(doc, rec, name):
    return next(m for m in doc["records"][rec]["members"] if m["name"] == name)


def m_member_rename(d, cov, succ):
    mem(d, "Rust3PreparedOutputEntryV3", "planRow")["name"] = "setRow"


def m_limit(d, cov, succ):
    mem(d, "Ts2FactBatchV1", "facts")["type"]["maxItems"] = "8192"


def m_int_literal(d, cov, succ):
    mem(d, "Ts2FactBatchV1", "facts")["type"]["maxItems"] = 4096


def m_bare_name(d, cov, succ):
    d["records"]["CoverageKeyV2"] = d["records"].pop("Rust3CoverageKeyV2")


def m_p3_guard(d, cov, succ):
    d["protocols"]["rust-semantic"]["transitions"]["guardAdditions"] = {}


def m_anchor_order(d, cov, succ):
    mem(d, "Rust3FactCandidateV1", "anchors")["type"]["order"] = "cbor-bytes-strict"


def m_frame_terminal(d, cov, succ):
    next(f for f in d["protocols"]["rust-semantic"]["frames"] if f["frameType"] == "Cancel")["workerTerminal"] = True


def m_bytes_as_text(d, cov, succ):
    mem(d, "Rust3SnapshotFileChunkV2", "bytes")["type"] = {"t": "text", "nfc": True}


def m_fact_ref_dropped(d, cov, succ):
    del d["records"]["Ts2AnchorRefV1"]["variants"]["fact-ref"]


def m_commit_domain(d, cov, succ):
    d["commitmentMap"]["rows"][0]["domain"] = "opensip.ts-provider.stage-coverage.v9"


def m_coverage_row(d, cov, succ):
    cov["rows"]["typescript-semantic"].pop()
    cov["totals"]["typescript-semantic"] -= 1


def m_gap_unresolved(d, cov, succ):
    for r in cov["rows"]["rust-semantic"]:
        if r["gaps"]:
            r["gapResolutions"][r["gaps"][0]] = None
            return


def m_selector(d, cov, succ):
    f = next(f for f in d["protocols"]["rust-semantic"]["frames"] if f["frameType"] == "Unavailable")
    f["payload"]["alternatives"] = {"READY_ANALYZE": f["payload"]["alternatives"]["ANALYZING"],
                                    "WAIT_NATIVE_CONTEXT_VERIFIED": f["payload"]["alternatives"]["WAIT_NATIVE_CONTEXT_VERIFIED"]}


def m_nullable_to_optional(d, cov, succ):
    mem(d, "Ts2CancelV1", "executionId")["presence"] = "optional"


def m_scalar_pattern(d, cov, succ):
    d["scalars"]["Rust3Sha256Text"]["type"]["pattern"] = "^[0-9a-f]{64}(?![\\s\\S])"


def m_successor_check(d, cov, succ):
    succ["rows"][0]["referenceChecks"].append("nonexistent-check")


CONTROLS = [m_member_rename, m_limit, m_int_literal, m_bare_name, m_p3_guard, m_anchor_order, m_frame_terminal,
            m_bytes_as_text, m_fact_ref_dropped, m_commit_domain, m_coverage_row, m_gap_unresolved, m_selector,
            m_nullable_to_optional, m_scalar_pattern, m_successor_check]

ANCHOR_ORDER_CHECK = "anchor-order-sources"


def run(tmp):
    st = Static(CM.ARCH_DEFAULT, tmp)
    res = st.run(Draft202012Validator) + Reference(CM.ARCH_DEFAULT, tmp, st).run()
    ids = {r["id"] for r in res}
    for row in st.succ["rows"]:
        for cid in row["referenceChecks"]:
            if cid not in ids:
                res.append({"id": "successor-check-exists:" + cid, "ok": False})
    return [r["id"] for r in res if not r["ok"]]


def main():
    names = ["wire-carriers.v1.json", "field-coverage.json", "successor.json", "wire-carriers.meta.schema.json"]
    with tempfile.TemporaryDirectory() as t:
        base = Path(t) / "base"
        base.mkdir()
        for n in names:
            shutil.copy(HERE / n, base / n)
        baseline = run(base)
        out = {"baselineFailures": baseline, "controls": []}
        for control in CONTROLS:
            work = Path(t) / control.__name__
            work.mkdir()
            d, cov, succ = (json.loads((HERE / n).read_text()) for n in names[:3])
            control(d, cov, succ)
            for n, obj in zip(names[:3], (d, cov, succ)):
                (work / n).write_text(json.dumps(obj))
            shutil.copy(HERE / names[3], work / names[3])
            try:
                failed = run(work)
            except Exception as exc:  # noqa: BLE001
                failed = ["checker-exception:" + type(exc).__name__]
            out["controls"].append({"control": control.__name__, "caught": bool(failed), "failedChecks": failed[:8]})
    out["allCaught"] = all(c["caught"] for c in out["controls"]) and not baseline
    (HERE / "selftest-result.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({"baselineFailures": baseline, "caught": sum(c["caught"] for c in out["controls"]), "controls": len(CONTROLS),
                      "missed": [c["control"] for c in out["controls"] if not c["caught"]]}, indent=1))
    return 0 if out["allCaught"] else 1


if __name__ == "__main__":
    sys.exit(main())
