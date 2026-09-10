#!/usr/bin/env python3
"""Successor pilot full review: structural admission then independent semantic replay."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from admit import Admit  # noqa: E402
from kit import Kit, sha256_file  # noqa: E402
from laws_catalog import APPLICABLE_LAWS  # noqa: E402
from schema_validate import SchemaBundle  # noqa: E402
from store import Store  # noqa: E402

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-full-review.v1")
PRED_ORIGIN = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-export-admission.v1")
OUT = ROOT / "output"


def verify_inputs() -> dict:
    rows = []
    all_ok = True
    # New export manifest
    p = ROOT / "export-manifest.json"
    actual, size = sha256_file(p)
    exp = "11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f"
    ok = actual == exp
    all_ok = all_ok and ok
    rows.append({"path": "export-manifest.json", "sha256": actual, "expected": exp, "bytes": size, "ok": ok})

    pred_rows = []
    pred_ok = True
    pred_expected = {
        "original-consumer-charter.txt": "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec",
        "requirements.json": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
        "subject/consumer-input-manifest.json": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
    }
    for rel, expected in pred_expected.items():
        pp = PRED_ORIGIN / rel
        actual, size = sha256_file(pp)
        ok = actual == expected
        pred_ok = pred_ok and ok
        pred_rows.append({"path": rel, "origin": str(PRED_ORIGIN), "sha256": actual, "expected": expected, "bytes": size, "ok": ok})

    man = json.loads((PRED_ORIGIN / "subject/consumer-input-manifest.json").read_text())
    kit_ok = True
    kit_rows = []
    for rec in man["files"]:
        pp = PRED_ORIGIN / "subject" / rec["path"]
        actual, size = sha256_file(pp)
        ok = actual == rec["sha256"] and size == rec["bytes"]
        kit_ok = kit_ok and ok
        if not ok:
            kit_rows.append(
                {
                    "path": rec["path"],
                    "ok": False,
                    "actual": actual,
                    "expected": rec["sha256"],
                    "bytes": size,
                    "expectedBytes": rec["bytes"],
                }
            )
    eman = json.loads((ROOT / "export-manifest.json").read_text())
    exp_ok = True
    exp_rows = []
    for rec in eman["files"]:
        pp = ROOT / rec["path"]
        actual, size = sha256_file(pp)
        ok = actual == rec["sha256"] and size == rec["bytes"]
        exp_ok = exp_ok and ok
        name = rec.get("name") or Path(rec["path"]).name.replace(".store.json", "")
        exp_rows.append(
            {
                "name": name,
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
        "standing": "Successor of consumer-b.v12-fresh-export-admission.v1; kit remains the original 80-file subset.",
        "manifestSHA": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
        "parentfrozenSHA": man.get("parentSubjectSha256"),
        "newExportManifestSHA": "11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f",
        "kitFileCount": len(man["files"]),
        "kitAllOk": kit_ok,
        "kitMismatches": kit_rows,
        "topLevel": rows,
        "topLevelOk": all_ok,
        "predecessorKitHashes": pred_rows,
        "predecessorKitOk": pred_ok,
        "exports": exp_rows,
        "exportsOk": exp_ok,
        "exportManifestStanding": eman.get("standing"),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    hashes = verify_inputs()
    (OUT / "verified-input-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    if not (hashes["kitAllOk"] and hashes["topLevelOk"] and hashes["exportsOk"] and hashes["predecessorKitOk"]):
        print("INPUT HASH VERIFICATION FAILED", file=sys.stderr)
        print(json.dumps(hashes, indent=2))
        return 2
    kit = Kit()
    schemas = SchemaBundle(kit)
    eman = json.loads((ROOT / "export-manifest.json").read_text())
    results = []
    for rec in eman["files"]:
        name = rec.get("name") or Path(rec["path"]).name.replace(".store.json", "")
        store = Store(ROOT / rec["path"], rec["claimedRunId"])
        admit = Admit(kit, schemas, store, name)
        result = admit.run_admission()
        executed = result.get("laws") or {}
        coverage = []
        for law in APPLICABLE_LAWS:
            st = executed.get(law["id"], {})
            status = st.get("status") or "notReached"
            coverage.append({**law, "status": status, "detail": st.get("detail")})
        result["applicableLawCoverage"] = coverage
        results.append(result)
        print(f"{name}: overall={result['verdict']} structural={result.get('structuralVerdict')} replay={result.get('replay') if not isinstance(result.get('replay'), dict) else result['replay'].get('status')}", flush=True)
        if result["firstRefusal"]:
            fr = result["firstRefusal"]
            print(f"  firstRefusal {fr.get('code')} {fr.get('citation')}", flush=True)
            print(f"  {fr.get('message')}", flush=True)
    (OUT / "admission-results.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
