"""Export the object table and ALL retained blob/frame bytes for every complete
positive Run, then re-verify each graph from the export alone."""
from __future__ import annotations

import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import closure as CL
import osip
import run_import
import run_rust
import run_syntax
import run_ts
import run_ts_config
from closure import Store

OUTDIR = "/tmp/opensip-design-corrections/consumer-b.v8/output"

RUNS = [
    ("CB-RUN-TS  ordinary TypeScript project (node_modules, bare specifiers, "
     "retained config graph, JS clone body through the TS analyzer universe)",
     lambda: run_ts.build_run()),
    ("CB-RUN-RS-lib  mixed-edition Rust workspace, selection = lib target",
     lambda: run_rust.build_run("lib")),
    ("CB-RUN-RS-test2024  the SAME physical file under the selected test target "
     "whose edition overrides its package default",
     lambda: run_rust.build_run("test2024")),
    ("CB-RUN-RS-libbin  selection widened without changing the effective dialect",
     lambda: run_rust.build_run("lib+bin")),
    ("CB-RUN-RS-ambiguous  ambiguous selected owners: no body, disclosed pair",
     lambda: run_rust.build_run("ambiguous")),
    ("CB-RUN-RS-partial  partial enumeration: empty clone view, disclosed pair",
     lambda: run_rust.build_run("partial")),
    ("CB-RUN-RS-none  no committed ownership: no clone admissible",
     lambda: run_rust.build_run("none")),
    ("CB-RUN-SX-mixed  compiler-free grammar-only repository (no TS/Rust unit)",
     lambda: run_syntax.build_run("mixed")),
    ("CB-RUN-SX-data  data/document-only repository: inventory complete, code "
     "capabilities correctly unavailable",
     lambda: run_syntax.build_run("data-only")),
    ("CB-RUN-CFG-synth  synthesized TypeScript configuration",
     lambda: run_ts_config.build_run("synthesized")),
    ("CB-RUN-CFG-multibase  custom-named config, ordered bases incl. a repeat",
     lambda: run_ts_config.build_run("custom-multibase")),
    ("CB-RUN-CFG-jsconfig  jsconfig inheriting a shared base of another filename",
     lambda: run_ts_config.build_run("jsconfig-shared")),
    ("CB-RUN-RS-prepared  rust-cargo-prepared: inert PreparedOutputSetV3 and the "
     "host-prepared prepare-code projection",
     lambda: run_rust.build_run("lib", prepared=True)),
    ("CB-RUN-RS-imported-inert  imported-inert projects only read-import",
     lambda: run_rust.build_run("lib", {"imported_inert": True}, prepared=True)),
    ("CB-RUN-IMP  a Run with an admitted registered runtime import2",
     lambda: run_import.build_run()),
]


def export():
    out = {"standing": "Blind consumer-B independent reconstruction. Disposable "
                       "design-reference evidence only; not product qualification.",
           "runs": []}
    blobs = {}
    for label, mk in RUNS:
        fx, A, run_id = mk()
        rep = CL.Closure(fx.s).close_run(run_id)
        assert rep["ok"], (label, rep["faults"][:3])
        for h, b in fx.s.blobs.items():
            if h in blobs:
                assert blobs[h] == b
            blobs[h] = b
        table = []
        for h, b in sorted(fx.s.blobs.items()):
            row = {"digest": h, "bytes": len(b),
                   "label": fx.s.labels.get(h, "")}
            if b.startswith(osip.FRAME_PREFIX + b"\x00"):
                try:
                    dom, val = osip.parse_frame(b)
                except osip.AdmissionError:
                    row["kind"] = "raw-artifact"
                    table.append(row)
                    continue
                row["kind"] = "h-identity"
                row["domain"] = dom
                row["typedIdentity"] = (osip.PREFIXES.get(dom) + ":" + h
                                        if dom in osip.PREFIXES
                                        else "sha256:" + h)
                row["descriptor"] = val
            else:
                try:
                    val, _ = osip.admit_raw(b)
                    if osip.C(val) == b:
                        row["kind"] = "canonical-record"
                        row["descriptor"] = val
                    else:
                        row["kind"] = "raw-artifact"
                except Exception:
                    row["kind"] = "raw-artifact"
            table.append(row)
        out["runs"].append({
            "label": label, "runId": run_id, "projectId": fx.project_id,
            "planId": A.plan_id, "snapshotId": A.snapshot_id,
            "closureChecks": rep["checks"], "closureOk": rep["ok"],
            "objectCount": len(table),
            "hIdentityCount": sum(1 for r in table if r["kind"] == "h-identity"),
            "canonicalRecordCount": sum(1 for r in table
                                        if r["kind"] == "canonical-record"),
            "rawArtifactCount": sum(1 for r in table if r["kind"] == "raw-artifact"),
            "objects": table})
    with open(OUTDIR + "/object-table.json", "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    with open(OUTDIR + "/blobs.b64.json", "w") as f:
        json.dump({"codec": "base64 of the exact retained bytes, keyed by their "
                            "raw SHA-256 (the ONE content-addressed store of "
                            "identity-and-evidence section 3)",
                   "count": len(blobs),
                   "blobs": {h: base64.b64encode(b).decode()
                             for h, b in sorted(blobs.items())}},
                  f, indent=1, sort_keys=True)
    return out, blobs


def verify_from_export():
    """Rebuild every store from the base64 export ALONE and re-close each Run."""
    tables = json.load(open(OUTDIR + "/object-table.json"))
    raw = json.load(open(OUTDIR + "/blobs.b64.json"))["blobs"]
    results = []
    for r in tables["runs"]:
        s = Store()
        for row in r["objects"]:
            b = base64.b64decode(raw[row["digest"]])
            assert osip.raw_sha256(b) == row["digest"], "CAS key mismatch"
            s.blobs[row["digest"]] = b
        rep = CL.Closure(s).close_run(r["runId"])
        results.append({"runId": r["runId"], "label": r["label"],
                        "checks": rep["checks"], "ok": rep["ok"],
                        "faults": rep["faults"][:3]})
    return results


if __name__ == "__main__":
    out, blobs = export()
    print("exported %d runs, %d distinct retained objects"
          % (len(out["runs"]), len(blobs)))
    print()
    print("re-verifying every graph FROM THE EXPORT ALONE:")
    bad = 0
    for r in verify_from_export():
        print(("  OK  " if r["ok"] else "  BAD ")
              + "%-6s checks=%-5d %s" % (r["runId"][5:13], r["checks"],
                                         r["label"][:66]))
        if not r["ok"]:
            bad += 1
            print("       ", r["faults"])
    print()
    print("runs re-verified:", len(out["runs"]), "failed:", bad)
    sys.exit(1 if bad else 0)
