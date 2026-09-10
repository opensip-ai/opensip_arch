#!/usr/bin/env python3
"""From-scratch structural admission of the six exported graphs."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

# Isolated interpreter: keep this directory first.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from admit import Admit  # noqa: E402
from kit import Kit, sha256_file  # noqa: E402
from laws_catalog import APPLICABLE_LAWS  # noqa: E402
from schema_validate import SchemaBundle  # noqa: E402
from store import Store  # noqa: E402

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-export-admission.v1")
OUT = ROOT / "output"


def verify_inputs() -> dict:
    expected = {
        "original-consumer-charter.txt": "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec",
        "requirements.json": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
        "export-manifest.json": "4101367795f1a30280601a3a01a8ea36a489f4891f9d0256e92481a8e6369129",
        "subject/consumer-input-manifest.json": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
    }
    rows = []
    all_ok = True
    for rel, exp in expected.items():
        p = ROOT / rel
        actual, size = sha256_file(p)
        ok = actual == exp
        all_ok = all_ok and ok
        rows.append({"path": rel, "sha256": actual, "expected": exp, "bytes": size, "ok": ok})
    man = json.loads((ROOT / "subject/consumer-input-manifest.json").read_text())
    kit_ok = True
    kit_rows = []
    for rec in man["files"]:
        p = ROOT / "subject" / rec["path"]
        actual, size = sha256_file(p)
        ok = actual == rec["sha256"] and size == rec["bytes"]
        kit_ok = kit_ok and ok
        if not ok:
            kit_rows.append({"path": rec["path"], "ok": False, "actual": actual, "expected": rec["sha256"], "bytes": size, "expectedBytes": rec["bytes"]})
    eman = json.loads((ROOT / "export-manifest.json").read_text())
    exp_ok = True
    exp_rows = []
    for rec in eman["files"]:
        p = ROOT / rec["path"]
        actual, size = sha256_file(p)
        ok = actual == rec["sha256"] and size == rec["bytes"]
        exp_ok = exp_ok and ok
        exp_rows.append(
            {
                "name": rec["name"],
                "path": rec["path"],
                "sha256": actual,
                "expected": rec["sha256"],
                "bytes": size,
                "expectedBytes": rec["bytes"],
                "claimedRunId": rec.get("claimedRunId"),
                "ok": ok,
            }
        )
    return {
        "manifestSHA": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
        "parentfrozenSHA": man.get("parentSubjectSha256"),
        "kitFileCount": len(man["files"]),
        "kitAllOk": kit_ok,
        "kitMismatches": kit_rows,
        "topLevel": rows,
        "topLevelOk": all_ok,
        "exports": exp_rows,
        "exportsOk": exp_ok,
        "exportManifestStanding": eman.get("standing"),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    hashes = verify_inputs()
    (OUT / "verified-input-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    if not (hashes["kitAllOk"] and hashes["topLevelOk"] and hashes["exportsOk"]):
        print("INPUT HASH VERIFICATION FAILED", file=sys.stderr)
        print(json.dumps(hashes, indent=2))
        return 2
    kit = Kit()
    schemas = SchemaBundle(kit)
    eman = json.loads((ROOT / "export-manifest.json").read_text())
    results = []
    for rec in eman["files"]:
        store = Store(ROOT / rec["path"], rec["claimedRunId"])
        admit = Admit(kit, schemas, store, rec["name"])
        result = admit.run_admission()
        executed = result.get("laws") or {}
        coverage = []
        for law in APPLICABLE_LAWS:
            st = executed.get(law["id"], {})
            status = st.get("status") or "notReached"
            if result["verdict"] == "REFUSE" and status == "notReached":
                status = "notReached"
            coverage.append({**law, "status": status, "detail": st.get("detail")})
        result["applicableLawCoverage"] = coverage
        results.append(result)
        print(f"{rec['name']}: {result['verdict']}", flush=True)
        if result["firstRefusal"]:
            fr = result["firstRefusal"]
            print(f"  firstRefusal {fr.get('code')} {fr.get('citation')}", flush=True)
            print(f"  {fr.get('message')}", flush=True)
    (OUT / "admission-results.json").write_text(json.dumps(results, indent=2) + "\n")
    # summary verdict
    refused = [r for r in results if r["verdict"] == "REFUSE"]
    admitted = [r for r in results if r["verdict"] == "ADMIT"]
    incomplete = [r for r in results if r["verdict"] not in ("ADMIT", "REFUSE")]
    if incomplete:
        overall = "EXPORTED_STRUCTURAL_ADMISSION_INCOMPLETE"
    elif refused:
        overall = "EXPORTED_STRUCTURAL_ADMISSION_REFUSED"
    else:
        overall = "EXPORTED_STRUCTURAL_ADMISSION_PASSES"
    summary = {
        "overall": overall,
        "admitted": [r["graph"] for r in admitted],
        "refused": [{"graph": r["graph"], "firstRefusal": r["firstRefusal"]} for r in refused],
        "replay": "UNEXECUTED",
    }
    (OUT / "admission-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("OVERALL", overall)
    return 0 if overall != "EXPORTED_STRUCTURAL_ADMISSION_INCOMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
