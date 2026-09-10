"""Independent retained closure and cross-record joins."""
from __future__ import annotations

import json
from typing import Any

from helpers.canonical import C, H_digest, parse_h_frame, sha256_hex
from helpers.store import Store


def close_run(store: Store, run_id: str) -> dict[str, Any]:
    faults: list[dict[str, Any]] = []
    run = store.objects[run_id]["descriptor"]
    for field, domain in [
        ("snapshotId", "snapshot"),
        ("planId", "plan"),
        ("evidenceId", "semantic-evidence"),
        ("evaluationSealId", "evaluation-seal"),
    ]:
        iid = run[field]
        if iid not in store.objects:
            faults.append({"code": "MISSING_OBJECT", "id": iid})
            continue
        obj = store.objects[iid]
        digest = iid.split(":")[-1]
        frame = store.blobs.get(digest)
        if frame is None:
            faults.append({"code": "MISSING_FRAME", "id": iid})
            continue
        try:
            d, payload = parse_h_frame(frame)
            recomputed = sha256_hex(frame)
            if recomputed != digest:
                faults.append({"code": "H_MISMATCH", "id": iid})
            c_bytes = C(obj["descriptor"])
            if c_bytes != payload:
                faults.append({"code": "C_MISMATCH", "id": iid, "domain": d})
        except Exception as e:
            faults.append({"code": "FRAME_PARSE", "id": iid, "message": str(e)})

    plan = store.objects[run["planId"]]["descriptor"]
    snap = store.objects[run["snapshotId"]]["descriptor"]
    if plan["snapshotId"] != run["snapshotId"]:
        faults.append({"code": "PLAN_SNAPSHOT_JOIN"})
    if plan["capabilityManifestId"] != run["capabilityManifestId"]:
        faults.append({"code": "CAP_ID_JOIN"})
    # derived capabilityManifestId
    cap_bytes = store.blobs.get(plan["capabilityManifestBytesDigest"])
    if cap_bytes is None:
        faults.append({"code": "CAP_BYTES_MISSING"})
    else:
        derived = sha256_hex(b"opensip.capability-manifest.v1\x00" + cap_bytes)
        if derived != plan["capabilityManifestId"]:
            faults.append({"code": "CAP_DERIVED_MISMATCH", "derived": derived, "claimed": plan["capabilityManifestId"]})

    inv_paths = {row["path"]: row for row in snap["sourceInventory"]}
    # facts join snapshot
    views = [
        o for oid, o in store.objects.items()
        if o["domain"] == "view" and o["descriptor"]["planId"] == run["planId"]
    ]
    for v in views:
        vd = v["descriptor"]
        for fid in vd["facts"]:
            f = store.objects[fid]["descriptor"]
            if f["snapshotId"] != run["snapshotId"]:
                faults.append({"code": "FACT_SNAPSHOT", "id": fid})
            payload = json.loads(store.blobs[f["payloadDigest"]])
            if f["relation"] == "file":
                row = inv_paths.get(payload["path"])
                if row is None:
                    faults.append({"code": "FILE_PATH_NOT_INVENTORIED", "path": payload["path"]})
                else:
                    if row["sha256"] != payload["contentSha256"] or row["bytes"] != payload["byteLength"]:
                        faults.append({"code": "FILE_DIGEST_LENGTH", "path": payload["path"]})
                    blob = store.blobs.get(payload["contentSha256"])
                    if blob is None or len(blob) != payload["byteLength"]:
                        faults.append({"code": "FILE_BLOB_MISSING", "path": payload["path"]})
                if f.get("anchors"):
                    faults.append({"code": "FACT_ANCHOR_CARDINALITY", "id": fid, "relation": "file"})
            if f["relation"] == "clones":
                if len(f.get("anchors") or []) != 1:
                    faults.append({"code": "FACT_ANCHOR_CARDINALITY", "id": fid, "relation": "clones"})
            if f["relation"] in ("calls", "declares", "imports", "references", "literal", "control-flow", "types", "reachability", "unresolved-edge"):
                if not f.get("anchors"):
                    faults.append({"code": "FACT_ANCHOR_CARDINALITY", "id": fid, "relation": f["relation"]})
        # coverage totality for file@enumerated complete
        for cid in vd["coverageIds"]:
            c = store.objects[cid]["descriptor"]
            payload = json.loads(store.blobs[c["payloadDigest"]])
            entry = payload["entry"]
            key = payload["key"]
            if key["relation"] == "file" and key["resolution"] == "enumerated" and entry["coverage"] == "complete" and entry.get("deficiency") is None:
                scope = store.objects[c["scopeId"]]["descriptor"]
                subjects = set(scope["subjects"])
                fact_paths = set()
                for fid in vd["facts"]:
                    f = store.objects[fid]["descriptor"]
                    if f["relation"] == "file" and f["resolution"] == "enumerated" and f["sourceUniverse"] == scope["sourceUniverse"] and f["targetUniverse"] == scope["targetUniverse"]:
                        p = json.loads(store.blobs[f["payloadDigest"]])
                        if p["path"] in subjects:
                            fact_paths.add(p["path"])
                inventoried = set(inv_paths) & subjects
                missing = inventoried - fact_paths
                if missing:
                    faults.append({"code": "COVERAGE_TOTALITY", "missing": sorted(missing)})
        # partition: scopes of same view with same partition key must have disjoint subjects
        scopes = [store.objects[s]["descriptor"] | {"id": s} for s in vd["scopeIds"]]
        from collections import defaultdict
        groups = defaultdict(list)
        for sc in scopes:
            k = (sc["snapshotId"], sc["relation"], sc["resolution"], sc["sourceUniverse"], sc["targetUniverse"])
            groups[k].append(sc)
        for k, g in groups.items():
            seen = set()
            for sc in g:
                inter = seen & set(sc["subjects"])
                if inter:
                    faults.append({"code": "COVERAGE_PARTITION", "subjects": sorted(inter)})
                seen |= set(sc["subjects"])

    # native contexts retained
    for d in plan["nativeContextDigests"]:
        found = False
        for oid, obj in store.objects.items():
            if obj["domain"].startswith("native.context.") and oid.endswith(d):
                found = True
                frame = store.blobs.get(d)
                if frame is None:
                    faults.append({"code": "NATIVE_CONTEXT_FRAME", "digest": d})
        if not found:
            faults.append({"code": "NATIVE_CONTEXT_UNRETAINED", "digest": d})

    seal = store.objects[run["evaluationSealId"]]["descriptor"]
    ev = store.objects[run["evidenceId"]]["descriptor"]
    if seal["proofBundleId"] != ev["proofBundleId"]:
        faults.append({"code": "SEAL_PROOF_JOIN"})
    if seal["evidenceId"] != run["evidenceId"]:
        faults.append({"code": "SEAL_EVIDENCE_JOIN"})
    proof = store.objects[ev["proofBundleId"]]["descriptor"]
    if proof["planId"] != run["planId"]:
        faults.append({"code": "PROOF_PLAN_JOIN"})

    return {
        "runId": run_id,
        "ok": not faults,
        "faults": faults,
        "classification": "valid" if not faults else "invalid",
        "boundaries": {
            "schema": "stock+keywords separately",
            "helper": "C/H/CVE1",
            "closure": "this result",
            "hostEnforcement": "not claimed",
        },
    }
