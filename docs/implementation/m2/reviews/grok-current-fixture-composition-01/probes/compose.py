"""Private current-byte fixture composition probe. No frozen rewrites. No compiler."""
from __future__ import annotations

import hashlib
import json
import sys
import traceback
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m2-grok-current-fixture-composition-01/review")
OVERLAY = REVIEW / "archroot" / "docs" / "coop" / "design-corrections"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
LIVE = Path("/Users/sb/code/opensip-ai/opensip")
HIST_NATIVE = ARCH / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
HIST_POLICY = ARCH / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"
HIST_ID = ARCH / "docs/coop/design-corrections/foundation/identity-schemas.v3.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    if not sys.flags.isolated:
        raise SystemExit("need isolated python")
    pins = {
        "liveIdentity": sha(LIVE / "schemas/sources/identity-v3.schema.json"),
        "histIdentity": sha(HIST_ID),
        "liveNative": sha(LIVE / "schemas/sources/native-v2.schema.json"),
        "histNative": sha(HIST_NATIVE),
        "livePolicyV2": sha(LIVE / "schemas/sources/policy-v2.schema.json"),
        "histPolicyV2": sha(HIST_POLICY),
        "liveRecognition": sha(LIVE / "schemas/sources/framework-recognition-plan-v1.schema.json"),
        "overlayIdentity": sha(OVERLAY / "foundation/identity-schemas.v3.json"),
        "overlayNative": sha(OVERLAY / "native/native-evidence.schemas.v2.json"),
        "overlayPolicy": sha(OVERLAY / "workflows/schemas/policy-document.v2.schema.json"),
        "overlayRecognition": sha(OVERLAY / "foundation/framework-recognition-plan.schema.v1.json"),
        "overlayCanonical": sha(OVERLAY / "foundation/canonical.py"),
        "overlayIdentityModel": sha(OVERLAY / "foundation/identity-model.v3.py"),
        "archRoot": str(REVIEW / "archroot"),
    }
    mismatch = {
        "historicalFixtureWouldHashNative": pins["histNative"],
        "currentProducerRequiresNative": pins["liveNative"],
        "historicalFixtureWouldHashIdentity": pins["histIdentity"],
        "currentProducerRequiresIdentity": pins["liveIdentity"],
        "historicalEqualsCurrentNative": pins["histNative"] == pins["liveNative"],
        "historicalEqualsCurrentIdentity": pins["histIdentity"] == pins["liveIdentity"],
        "historicalEqualsCurrentPolicy": pins["histPolicyV2"] == pins["livePolicyV2"],
        "overlayMatchesLive": pins["overlayNative"] == pins["liveNative"]
        and pins["overlayIdentity"] == pins["liveIdentity"]
        and pins["overlayPolicy"] == pins["livePolicyV2"]
        and pins["overlayRecognition"] == pins["liveRecognition"],
    }
    out: dict = {"pins": pins, "digestAuthorityMismatch": mismatch, "fixture": None, "error": None}
    sys.path.insert(0, str(OVERLAY / "foundation"))
    try:
        from evaluator_graph_fixture.v3 import build_file_inputs, seal_fixture  # type: ignore
        import identity_model_v3  # noqa: F401
    except Exception:
        # composition model loads identity-model.v3.py by path, not package name
        pass
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "current_graph_fixture", OVERLAY / "foundation" / "evaluator_graph_fixture.v3.py"
        )
        G = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(G)
        graph = G.build_file_inputs()
        objects = graph["objects"]
        blobs = graph["blobs"]
        # sample one fact payloadSchemaDigest vs current native/relation
        fact_keys = [k for k, (d, _) in objects.items() if d == "fact"]
        cov_keys = [k for k, (d, _) in objects.items() if d == "coverage"]
        relation = hashlib.sha256(
            (OVERLAY / "foundation" / "relation-payload-schemas.v2.json").read_bytes()
        ).hexdigest()
        native = pins["liveNative"]
        fact_schema = objects[fact_keys[0]][1]["payloadSchemaDigest"] if fact_keys else None
        cov_schema = objects[cov_keys[0]][1]["payloadSchemaDigest"] if cov_keys else None
        run, robjects, rblobs, composed = G.seal_fixture(graph)
        out["fixture"] = {
            "built": True,
            "objectCount": len(objects),
            "blobCount": len(blobs),
            "factCount": len(fact_keys),
            "coverageCount": len(cov_keys),
            "firstFactSchemaDigest": fact_schema,
            "firstCoverageSchemaDigest": cov_schema,
            "relationDocumentSha256": relation,
            "factUsesCurrentRelationDocument": fact_schema == relation,
            "coverageUsesCurrentNativeDocument": cov_schema == native,
            "coverageUsesHistoricalNative": cov_schema == pins["histNative"],
            "runId": None,
            "sealedObjectCount": len(robjects),
            "verdict": composed.get("proof", {}).get("verdict") if isinstance(composed, dict) else None,
        }
        if isinstance(run, dict):
            out["fixture"]["runKeys"] = sorted(run.keys())
            out["fixture"]["runSchemaVersion"] = run.get("schemaVersion")
            out["fixture"]["planId"] = run.get("planId")
            out["fixture"]["snapshotId"] = run.get("snapshotId")
            out["fixture"]["evidenceId"] = run.get("evidenceId")
            out["fixture"]["evaluationSealId"] = run.get("evaluationSealId")
    except Exception as exc:
        out["error"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc()[-4000:],
        }
    (REVIEW / "results" / "composition.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ("digestAuthorityMismatch", "fixture", "error")}, indent=2)[:8000])


if __name__ == "__main__":
    main()
