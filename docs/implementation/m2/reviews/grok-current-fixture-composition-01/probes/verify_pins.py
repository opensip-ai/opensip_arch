"""Independent pin, overlay, and A04 owner-closure checks. Private review only."""
from __future__ import annotations

import hashlib
import json
import sys
import traceback
from pathlib import Path

if not sys.flags.isolated:
    raise SystemExit("need isolated python")

REVIEW = Path("/tmp/opensip-implementation/m2-grok-current-fixture-composition-01/review")
OVERLAY = REVIEW / "archroot" / "docs" / "coop" / "design-corrections"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
LIVE = Path("/Users/sb/code/opensip-ai/opensip")
SSV2 = ARCH / "docs/implementation/m1/source-selection-v2"
EXACT = ARCH / "docs/implementation/m2/exact-schema-profile-selection-v1/reference/canonical.py"
PROPOSED = SSV2 / "reference/models/identity_model.proposed.v3.py"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pin(p: Path) -> dict:
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "exists": True}


def main() -> None:
    live_lock = json.loads((LIVE / "design-lock.json").read_text())
    live_map = json.loads((LIVE / "schemas/source-map.json").read_text())
    live_admission = json.loads((LIVE / "schemas/admission-source-map.json").read_text())
    dispatch = json.loads((SSV2 / "current-dispatch.json").read_text())

    files = {
        "liveLock": pin(LIVE / "design-lock.json"),
        "liveSourceMap": pin(LIVE / "schemas/source-map.json"),
        "liveAdmissionSourceMap": pin(LIVE / "schemas/admission-source-map.json"),
        "liveIdentity": pin(LIVE / "schemas/sources/identity-v3.schema.json"),
        "liveNative": pin(LIVE / "schemas/sources/native-v2.schema.json"),
        "livePolicyV2": pin(LIVE / "schemas/sources/policy-v2.schema.json"),
        "liveRecognition": pin(LIVE / "schemas/sources/framework-recognition-plan-v1.schema.json"),
        "liveRelation": pin(LIVE / "schemas/sources/relation-payload-v2.schema.json"),
        "ssv2Identity": pin(SSV2 / "schemas/sources/identity.v3.schema.json"),
        "ssv2Native": pin(SSV2 / "schemas/sources/native.v2.schema.json"),
        "ssv2Policy": pin(SSV2 / "schemas/sources/policy.v2.schema.json"),
        "ssv2Recognition": pin(SSV2 / "schemas/sources/framework-recognition-plan.v1.schema.json"),
        "ssv2SourceMap": pin(SSV2 / "source-map.json"),
        "ssv2CurrentDispatch": pin(SSV2 / "current-dispatch.json"),
        "ssv3Successor": pin(ARCH / "docs/implementation/m1/source-selection-v3/successor.json"),
        "exactProfileCanonical": pin(EXACT),
        "proposedIdentityModel": pin(PROPOSED),
        "histIdentitySchema": pin(ARCH / "docs/coop/design-corrections/foundation/identity-schemas.v3.json"),
        "histNative": pin(ARCH / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"),
        "histPolicyV2": pin(ARCH / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"),
        "histCanonical": pin(ARCH / "docs/coop/design-corrections/foundation/canonical.py"),
        "histIdentityModelV3": pin(ARCH / "docs/coop/design-corrections/foundation/identity-model.v3.py"),
        "histGraphFixture": pin(ARCH / "docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py"),
        "histRelation": pin(ARCH / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"),
        "overlayIdentity": pin(OVERLAY / "foundation/identity-schemas.v3.json"),
        "overlayNative": pin(OVERLAY / "native/native-evidence.schemas.v2.json"),
        "overlayPolicy": pin(OVERLAY / "workflows/schemas/policy-document.v2.schema.json"),
        "overlayRecognition": pin(OVERLAY / "foundation/framework-recognition-plan.schema.v1.json"),
        "overlayCanonical": pin(OVERLAY / "foundation/canonical.py"),
        "overlayIdentityModel": pin(OVERLAY / "foundation/identity-model.v3.py"),
        "overlayGraphFixture": pin(OVERLAY / "foundation/evaluator_graph_fixture.v3.py"),
        "overlayRelation": pin(OVERLAY / "foundation/relation-payload-schemas.v2.json"),
        "admissionRuntimeSuccessor": pin(ARCH / "docs/implementation/m2/admission-runtime-selection-v1/successor.json"),
        "inventoryV11": pin(ARCH / "docs/implementation/m2/repository-file-inventory.v11.json"),
        "exactProfileSuccessor": pin(ARCH / "docs/implementation/m2/exact-schema-profile-selection-v1/successor.json"),
    }

    compares = {
        "overlayIdentityEqualsLive": files["overlayIdentity"]["sha256"] == files["liveIdentity"]["sha256"],
        "overlayNativeEqualsLive": files["overlayNative"]["sha256"] == files["liveNative"]["sha256"],
        "overlayPolicyEqualsLive": files["overlayPolicy"]["sha256"] == files["livePolicyV2"]["sha256"],
        "overlayRecognitionEqualsLive": files["overlayRecognition"]["sha256"] == files["liveRecognition"]["sha256"],
        "liveIdentityEqualsSourceSelection": files["liveIdentity"]["sha256"] == files["ssv2Identity"]["sha256"],
        "liveNativeEqualsSourceSelection": files["liveNative"]["sha256"] == files["ssv2Native"]["sha256"],
        "livePolicyEqualsSourceSelection": files["livePolicyV2"]["sha256"] == files["ssv2Policy"]["sha256"],
        "liveRecognitionEqualsSourceSelection": files["liveRecognition"]["sha256"] == files["ssv2Recognition"]["sha256"],
        "overlayCanonicalEqualsAcceptedExactProfile": files["overlayCanonical"]["sha256"]
        == files["exactProfileCanonical"]["sha256"],
        "overlayIdentityModelEqualsProposed": files["overlayIdentityModel"]["sha256"]
        == files["proposedIdentityModel"]["sha256"],
        "overlayFixtureEqualsHistoricalProducer": files["overlayGraphFixture"]["sha256"]
        == files["histGraphFixture"]["sha256"],
        "relationHistoricalEqualsCurrent": files["histRelation"]["sha256"] == files["liveRelation"]["sha256"],
        "historicalIdentityEqualsCurrent": files["histIdentitySchema"]["sha256"] == files["liveIdentity"]["sha256"],
        "historicalNativeEqualsCurrent": files["histNative"]["sha256"] == files["liveNative"]["sha256"],
        "historicalPolicyEqualsCurrent": files["histPolicyV2"]["sha256"] == files["livePolicyV2"]["sha256"],
        "historicalCanonicalEqualsExactProfile": files["histCanonical"]["sha256"]
        == files["exactProfileCanonical"]["sha256"],
        "historicalIdentityModelEqualsProposed": files["histIdentityModelV3"]["sha256"]
        == files["proposedIdentityModel"]["sha256"],
    }

    dispatch_ids = [row["schemaId"] for row in dispatch["currentSources"]]
    map_by_id = {row["schemaId"]: row for row in live_map["sources"]}
    dispatch_sha = {
        row["schemaId"]: row["architectureSource"]["sha256"] for row in dispatch["currentSources"]
    }

    out: dict = {
        "lock": {
            "inventorySuccessors": len(live_lock.get("inventorySuccessors", [])),
            "contractSuccessors": len(live_lock.get("contractSuccessors", [])),
            "lastContractRecord": live_lock["contractSuccessors"][-1]["record"],
            "lastContractAssent": live_lock["contractSuccessors"][-1]["assent"],
            "lastContractReview": live_lock["contractSuccessors"][-1]["review"],
            "lastContractSubject": live_lock["contractSuccessors"][-1]["subjectManifest"],
            "liveLockSha256": files["liveLock"]["sha256"],
            "liveLockBytes": files["liveLock"]["bytes"],
            "generationSourceMapRows": len(live_map["sources"]),
            "admissionSourceMapRows": len(live_admission["sources"]),
            "currentDispatchCount": len(dispatch["currentSources"]),
            "currentDispatchSchemaIds": dispatch_ids,
        },
        "files": files,
        "compares": compares,
        "dispatchPinsMatchLiveFiles": {
            sid: dispatch_sha[sid] == map_by_id[sid]["architectureSource"]["sha256"]
            for sid in (
                "urn:opensip:product-v1:identity:v3",
                "urn:opensip:product-v1:native:evidence-schemas:v2",
                "urn:opensip:product-v1:policy-document:2",
                "opensip.product.framework-recognition-plan.1",
            )
        },
        "ownerAdmission": None,
        "historicalDigestCounterexample": None,
        "error": None,
    }

    sys.path.insert(0, str(OVERLAY / "foundation"))
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "current_graph_fixture", OVERLAY / "foundation" / "evaluator_graph_fixture.v3.py"
        )
        G = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(G)
        graph = G.build_file_inputs()
        objects, blobs = graph["objects"], graph["blobs"]
        fact_keys = [k for k, (d, _) in objects.items() if d == "fact"]
        cov_keys = [k for k, (d, _) in objects.items() if d == "coverage"]
        relation = files["overlayRelation"]["sha256"]
        native = files["liveNative"]["sha256"]
        fact_schema = objects[fact_keys[0]][1]["payloadSchemaDigest"]
        cov_schema = objects[cov_keys[0]][1]["payloadSchemaDigest"]
        run, robjects, rblobs, composed = G.seal_fixture(graph)

        ident_spec = importlib.util.spec_from_file_location(
            "current_identity_v3", OVERLAY / "foundation" / "identity-model.v3.py"
        )
        IM = importlib.util.module_from_spec(ident_spec)
        ident_spec.loader.exec_module(IM)
        run_id, owner = IM.open_run_closure(run, robjects, rblobs)
        registered = sorted(IM.registered_schema_documents())
        out["ownerAdmission"] = {
            "buildFileInputs": True,
            "objectCount": len(objects),
            "blobCount": len(blobs),
            "factCount": len(fact_keys),
            "coverageCount": len(cov_keys),
            "firstFactSchemaDigest": fact_schema,
            "firstCoverageSchemaDigest": cov_schema,
            "factUsesCurrentRelation": fact_schema == relation,
            "coverageUsesCurrentNative": cov_schema == native,
            "coverageUsesHistoricalNative": cov_schema == files["histNative"]["sha256"],
            "sealedObjectCount": len(robjects),
            "runSchemaVersion": run.get("schemaVersion"),
            "planId": run.get("planId"),
            "snapshotId": run.get("snapshotId"),
            "evidenceId": run.get("evidenceId"),
            "evaluationSealId": run.get("evaluationSealId"),
            "composeVerdict": composed.get("proof", {}).get("verdict") if isinstance(composed, dict) else None,
            "openRunClosure": True,
            "runId": run_id,
            "ownerKeys": sorted(owner.keys()) if isinstance(owner, dict) else None,
            "registeredSchemaDocumentCount": len(registered),
            "registeredIncludesCurrentNative": native in registered,
            "registeredIncludesHistoricalNative": files["histNative"]["sha256"] in registered,
            "registeredIncludesCurrentPolicy": files["livePolicyV2"]["sha256"] in registered,
            "registeredIncludesHistoricalPolicy": files["histPolicyV2"]["sha256"] in registered,
            "registeredIncludesCurrentRelation": relation in registered,
            "primitive": "identity-model.v3.open_run_closure",
            "notCompleteReplay": True,
            "notReplayedRun": True,
        }

        native_spec = importlib.util.spec_from_file_location(
            "current_native_v2", OVERLAY / "native" / "native_evidence_model.v2.py"
        )
        N = importlib.util.module_from_spec(native_spec)
        native_spec.loader.exec_module(N)
        # Reconstruct one admitted coverage payload from the sealed graph and re-admit
        # with the historical native digest as a caller-chosen payloadSchemaDigest.
        cov_payload = IM.C.parse(rblobs[robjects[cov_keys[0]][1]["payloadDigest"]])
        scope = robjects[robjects[cov_keys[0]][1]["scopeId"]][1]
        current_admit = N.admit_coverage_result_v3(cov_payload, scope, [], native)
        historical_admit = N.admit_coverage_result_v3(
            cov_payload, scope, [], files["histNative"]["sha256"]
        )
        out["historicalDigestCounterexample"] = {
            "currentNativeDigest": native,
            "historicalNativeDigest": files["histNative"]["sha256"],
            "sameId": True,
            "currentAdmitResult": current_admit.get("result"),
            "historicalAdmitResult": historical_admit.get("result"),
            "historicalRefusals": historical_admit.get("refusals"),
            "refusesHistoricalDigestAsCurrent": historical_admit.get("result") != "ADMIT"
            and "native.coverage-payload-schema-not-registered" in historical_admit.get("refusals", []),
            "identityRegisteredDocumentsExcludeHistoricalNative": files["histNative"]["sha256"]
            not in registered,
        }
    except Exception as exc:
        out["error"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc()[-6000:],
        }

    dest = REVIEW / "results" / "verify_pins.json"
    dest.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    summary = {
        "lock": out["lock"],
        "compares": out["compares"],
        "ownerAdmission": out.get("ownerAdmission"),
        "historicalDigestCounterexample": out.get("historicalDigestCounterexample"),
        "error": out.get("error"),
    }
    print(json.dumps(summary, indent=2)[:12000])


if __name__ == "__main__":
    main()
