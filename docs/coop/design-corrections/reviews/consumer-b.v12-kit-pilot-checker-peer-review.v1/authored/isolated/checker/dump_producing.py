#!/usr/bin/env python3
"""Dump producing-law operands from the two exact pilot stores (read-only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from canonical import admit_json_bytes, parse_h_frame, sha256_hex  # noqa: E402
from store import Store  # noqa: E402

PILOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/output/isolated/run")


def rec_from_blob(store: Store, digest: str, expected_domain: str | None = None):
    raw = store.require_blob(digest, "dump", expected_domain or "blob")
    if raw.startswith(b"opensip.product.v1\x00"):
        domain, rec, _ = parse_h_frame(raw, expected_domain=expected_domain)
        return domain, rec
    return "canonical-record", admit_json_bytes(raw, profile="product", citation="dump")


def summarize_inventory(inv: dict) -> dict:
    rows = inv.get("rows") or []
    return {
        "schemaVersion": inv.get("schemaVersion"),
        "planId": inv.get("planId"),
        "parameterDigest": inv.get("parameterDigest"),
        "cellOrdinal": inv.get("cellOrdinal"),
        "programOrdinal": inv.get("programOrdinal"),
        "kind": inv.get("kind"),
        "state": inv.get("state"),
        "deficiency": inv.get("deficiency"),
        "nativeCause": inv.get("nativeCause"),
        "examinedPaths": inv.get("examinedPaths"),
        "rowCount": len(rows),
        "rowPaths": [r.get("path") for r in rows],
        "rowNativeIds": [r.get("nativeSubjectId") for r in rows],
        "rowQualifiedNames": [r.get("qualifiedName") for r in rows],
        "rowLanguages": [r.get("subjectLanguage") for r in rows],
    }


def dump_one(name: str, rel: str, claimed: str) -> dict:
    store = Store(PILOT / rel, claimed)
    store.rehash_all_blobs()
    run_hex = claimed.split(":", 1)[1]
    _, run = rec_from_blob(store, run_hex, "run")
    _, seal = rec_from_blob(store, run["evaluationSealId"].split(":")[1], "evaluation-seal")
    _, evidence = rec_from_blob(store, run["evidenceId"].split(":")[1], "semantic-evidence")
    _, plan = rec_from_blob(store, run["planId"].split(":")[1], "plan")
    _, snapshot = rec_from_blob(store, run["snapshotId"].split(":")[1], "snapshot")
    _, proof = rec_from_blob(store, evidence["proofBundleId"].split(":")[1], "proof-bundle")
    _, ei = rec_from_blob(store, proof["executionInputsDigest"])
    _, exec_plan = rec_from_blob(store, proof["executionPlanId"].split(":")[1], "execution-plan")
    _, aspec = rec_from_blob(store, plan["analysisSpecDigest"])
    _, policy = rec_from_blob(store, plan["policyDigest"])
    enum_digest = ei["enumerationPlanDigest"]
    _, enum_plan = rec_from_blob(store, enum_digest)
    _, membership = rec_from_blob(store, enum_plan["membershipDigest"])
    _, scope = rec_from_blob(store, plan["scopeDigest"])
    inventories = []
    for ref in ei.get("selectedRefs") or []:
        if ref.get("domain") == "subject-inventory":
            _, inv = rec_from_blob(store, ref["digest"])
            inventories.append({"digest": ref["digest"], **summarize_inventory(inv)})
    views = []
    for vid in evidence.get("viewIds") or []:
        hx = vid.split(":")[1]
        _, view = rec_from_blob(store, hx, "view")
        views.append(
            {
                "id": vid,
                "producerClosure": view.get("producerClosure"),
                "coverageIds": view.get("coverageIds"),
                "scopeIds": view.get("scopeIds"),
                "factCount": len(view.get("facts") or []),
                "facts": view.get("facts"),
            }
        )
    facts = []
    for fid in (views[0]["facts"] if views else []) or []:
        hx = fid.split(":")[1]
        _, fact = rec_from_blob(store, hx, "fact")
        payload = None
        if fact.get("payloadDigest"):
            try:
                _, payload = rec_from_blob(store, fact["payloadDigest"])
            except Exception as e:
                payload = {"error": str(e)}
        facts.append(
            {
                "id": fid,
                "relation": fact.get("relation"),
                "resolution": fact.get("resolution"),
                "sourceUniverse": fact.get("sourceUniverse"),
                "payload": payload,
            }
        )
    coverages = []
    for cid in evidence.get("coverageIds") or []:
        hx = cid.split(":")[1]
        _, cov = rec_from_blob(store, hx, "coverage")
        payload = None
        if cov.get("payloadDigest"):
            try:
                _, payload = rec_from_blob(store, cov["payloadDigest"])
            except Exception as e:
                payload = {"error": str(e)}
        coverages.append(
            {
                "id": cid,
                "scopeId": cov.get("scopeId"),
                "payload": payload,
            }
        )
    scopes = []
    for sid in (views[0].get("scopeIds") if views else []) or []:
        hx = sid.split(":")[1]
        _, sc = rec_from_blob(store, hx, "subject-scope")
        scopes.append(
            {
                "id": sid,
                "relation": sc.get("relation"),
                "resolution": sc.get("resolution"),
                "sourceUniverse": sc.get("sourceUniverse"),
                "subjects": sc.get("subjects"),
            }
        )
    inv_paths = [r["path"] for r in snapshot.get("sourceInventory") or []]
    return {
        "name": name,
        "claimedRunId": claimed,
        "run": run,
        "planKeys": {
            "planId": run["planId"],
            "snapshotId": run["snapshotId"],
            "policyDigest": plan.get("policyDigest"),
            "analysisSpecDigest": plan.get("analysisSpecDigest"),
            "scopeDigest": plan.get("scopeDigest"),
            "importIds": plan.get("importIds"),
            "semanticClosures": plan.get("semanticClosures"),
            "nativeContextDigests": plan.get("nativeContextDigests"),
            "budget": plan.get("budget"),
        },
        "snapshotPaths": inv_paths,
        "scope": scope,
        "analysisSpec": {
            "requestedCapabilities": aspec.get("requestedCapabilities"),
            "parameters": [
                {"schemaDigest": p.get("schemaDigest"), "payloadDigest": p.get("payloadDigest")}
                for p in aspec.get("parameters") or []
            ],
        },
        "policyRules": [
            {
                "ruleId": r.get("ruleId"),
                "enabled": r.get("enabled"),
                "gate": r.get("gate"),
                "severity": r.get("severity"),
                "subjectEnumeration": r.get("subjectEnumeration"),
                "emitWhen": r.get("emitWhen"),
                "messageCode": r.get("messageCode"),
            }
            for r in policy.get("rules") or []
        ],
        "policyGateSeverityAtLeast": policy.get("gateSeverityAtLeast"),
        "enumerationPlan": enum_plan,
        "membership": {
            "schemaVersion": membership.get("schemaVersion"),
            "unitCount": len(membership.get("units") or []),
            "units": membership.get("units"),
            "rows": membership.get("rows"),
            "unsupportedFiles": membership.get("unsupportedFiles"),
            "outsideBoundaryFiles": membership.get("outsideBoundaryFiles"),
            "erasedFiles": membership.get("erasedFiles"),
        },
        "executionInputs": ei,
        "executionPlanStages": [
            {
                "ordinal": s.get("ordinal"),
                "outputDomains": s.get("outputDomains"),
                "producerClosure": s.get("producerClosure"),
                "keys": sorted(s.keys()) if isinstance(s, dict) else type(s).__name__,
            }
            for s in exec_plan.get("stages") or []
        ],
        "inventories": inventories,
        "views": views,
        "facts": facts,
        "coverages": coverages,
        "scopes": scopes,
        "proofSelected": {
            "verdict": proof.get("verdict"),
            "findingIds": proof.get("findingIds"),
            "executionInputsDigest": proof.get("executionInputsDigest"),
            "evaluationInputRefs": proof.get("evaluationInputRefs"),
            "evaluatorClosure": proof.get("evaluatorClosure"),
        },
    }


def main() -> int:
    eman = json.loads((PILOT / "export-manifest.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    dumps = {}
    for rec in eman["files"]:
        name = rec.get("name") or Path(rec["path"]).name
        print(f"dumping {name}", flush=True)
        dumps[name] = dump_one(name, rec["path"], rec["claimedRunId"])
    (OUT / "producing-operands.dump.json").write_text(json.dumps(dumps, indent=2) + "\n")
    # compact overview
    overview = {}
    for name, d in dumps.items():
        ei = d["executionInputs"]
        overview[name] = {
            "snapshotPaths": d["snapshotPaths"],
            "scope": d["scope"],
            "requestedCapabilities": d["analysisSpec"]["requestedCapabilities"],
            "policyRules": d["policyRules"],
            "enumCells": [
                {
                    "capabilityId": c.get("capabilityId"),
                    "languageMode": c.get("languageMode"),
                    "workspaceRoot": c.get("workspaceRoot"),
                    "required": c.get("required"),
                    "kinds": c.get("kinds"),
                    "bindings": [
                        {
                            "ordinal": b.get("ordinal"),
                            "provenance": b.get("provenance"),
                            "universe": b.get("universe"),
                            "enumerator": b.get("enumerator"),
                            "programEntry": b.get("programEntry"),
                            "extents": b.get("extents"),
                            "candidateSourcePaths": b.get("candidateSourcePaths"),
                            "deficiency": b.get("deficiency"),
                        }
                        for b in c.get("programBindings") or []
                    ],
                }
                for c in d["enumerationPlan"].get("cells") or []
            ],
            "membershipRows": d["membership"]["rows"],
            "membershipUnits": d["membership"]["units"],
            "selectedRefs": ei.get("selectedRefs"),
            "cellOutcomes": ei.get("cellOutcomes"),
            "nativeCoverageAccounts": ei.get("nativeCoverageAccounts"),
            "candidateResultRefs": ei.get("candidateResultRefs"),
            "hostCapture": {
                "custody": (ei.get("hostCapture") or {}).get("custody"),
                "observation": (ei.get("hostCapture") or {}).get("observation"),
                "stageReceipts": (ei.get("hostCapture") or {}).get("stageReceipts"),
                "hostDerivedRefs": (ei.get("hostCapture") or {}).get("hostDerivedRefs"),
            },
            "inventories": d["inventories"],
            "views": d["views"],
            "facts": d["facts"],
            "coverages": d["coverages"],
            "scopes": d["scopes"],
            "importIds": d["planKeys"]["importIds"],
            "execStages": d["executionPlanStages"],
        }
    (OUT / "producing-operands.overview.json").write_text(json.dumps(overview, indent=2) + "\n")
    print("wrote producing-operands.dump.json and overview", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
