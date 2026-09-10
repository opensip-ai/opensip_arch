#!/usr/bin/env python3
"""Independent probes of COMPLETE56 vs COMPLETE30 four MUST / two SHOULD.

Not a 42-row oracle. Discriminating owner-path and published-schema probes.
Python: /tmp/opensip-architecture-review-env/bin/python -I -B
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

PY = sys.executable
HERE = Path(__file__).resolve().parent
OVERLAY = HERE / "overlay"
FOUND = OVERLAY / "docs/coop/design-corrections/foundation"
NATIVE = OVERLAY / "docs/coop/design-corrections/native"
ART = OVERLAY / "docs/coop/artifacts"
PROD = OVERLAY / "docs/v2/contracts/product-v1"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = _load("v4_return_model", FOUND / "provider_attribution_return_model.v2.py")
C = M.C
CHK = _load("v4_return_checker", FOUND / "check-provider-attribution-return.v2.py")
N = _load("v4_native", NATIVE / "native_evidence_model.v2.py")

BATCH = json.loads((NATIVE / "fact-batch.schema.v3.json").read_text(encoding="utf-8"))
COMPANION = json.loads((NATIVE / "occupancy-companion.schema.v1.json").read_text(encoding="utf-8"))
DISPATCH = json.loads((NATIVE / "dispatch-binding.schema.v1.json").read_text(encoding="utf-8"))
RETURN = json.loads((FOUND / "provider-target-attribution-return.schema.v2.json").read_text(encoding="utf-8"))
TARGET = json.loads((FOUND / "target-attribution.schema.v2.json").read_text(encoding="utf-8"))
MODEL_SRC = (FOUND / "provider_attribution_return_model.v2.py").read_text(encoding="utf-8")
NATIVE_MD = (PROD / "native-evidence.md").read_text(encoding="utf-8")
DELIVERY = json.loads((ART / "delivery.v2.json").read_text(encoding="utf-8"))
RPP = json.loads((ART / "rust-provider-protocol.v2.json").read_text(encoding="utf-8"))
CANON_SRC = (FOUND / "canonical.py").read_text(encoding="utf-8")

REG = Registry().with_resources([
    (BATCH["$id"], Resource(contents=BATCH, specification=DRAFT202012)),
    (COMPANION["$id"], Resource(contents=COMPANION, specification=DRAFT202012)),
    (DISPATCH["$id"], Resource(contents=DISPATCH, specification=DRAFT202012)),
    (RETURN["$id"], Resource(contents=RETURN, specification=DRAFT202012)),
    (TARGET["$id"], Resource(contents=TARGET, specification=DRAFT202012)),
])

PROBES = []


def rec(probe_id, title, ok, evidence, classification, notes=None, author_claim_holds=None, helper_only=None):
    PROBES.append({
        "id": probe_id,
        "title": title,
        "ok": ok,
        "author_claim_holds": author_claim_holds,
        "classification": classification,
        "helper_only": helper_only,
        "evidence": evidence,
        "notes": notes,
    })


def catch(fn):
    try:
        out = fn()
        return {
            "raised": False,
            "status": out.get("status") if isinstance(out, dict) else None,
            "phase": out.get("phase") if isinstance(out, dict) else None,
            "nrefs": len(out.get("hostDerivedRefs") or []) if isinstance(out, dict) else None,
            "retained": out.get("retainedStageOrdinal") if isinstance(out, dict) else None,
            "request": out.get("analyzeRequestOrdinal") if isinstance(out, dict) else None,
            "stageId": out.get("stageId") if isinstance(out, dict) else None,
            "producer": out.get("producerClosure") if isinstance(out, dict) else None,
            "key": None,
        }
    except M.ProviderReturnAdmissionError as exc:
        return {"raised": True, "key": exc.key, "detail": exc.detail, "status": None}


def schema_ok(schema, value):
    try:
        C.validate(schema, value, registry=REG)
        return True, None
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {str(exc).splitlines()[0]}"


def probe_no_import_mutation_and_published_allof():
    batch_items = json.loads(json.dumps(M.BATCH_SCHEMA))["properties"]["occupancyCompanions"]["items"]
    rec_items = json.loads(json.dumps(M.RETURN_SCHEMA))["properties"]["records"]["items"]
    mutated = "BATCH_SCHEMA[\"properties\"][\"occupancyCompanions\"][\"items\"] =" in MODEL_SRC
    bad = CHK.companion(0)
    bad["evaluationNativeId"] = None
    cand = CHK.candidate(0)
    batch = CHK.batch([cand], [bad])
    pub_batch_ok, pub_err = schema_ok(BATCH, batch)
    companion_ok, _ = schema_ok(COMPANION, bad)
    rec(
        "P-SCHEMA-NO-MUTATION",
        "Published schemas $ref full companion/V2; no import-time patching; first-party null eval refuses",
        True,
        {
            "batch_items": batch_items,
            "return_items": rec_items,
            "model_assigns_items": mutated,
            "published_batch_admits_first_party_null_eval": pub_batch_ok,
            "published_batch_error": pub_err,
            "companion_schema_admits_null_eval": companion_ok,
            "companion_has_allOf": "allOf" in COMPANION,
            "vocab_published": "candidateOrdinal" in (COMPANION.get("x-opensip-order-vocabulary") or {}),
        },
        "must-operand",
        author_claim_holds=(
            batch_items.get("$ref") == "opensip.product.occupancy-companion.1"
            and rec_items.get("$ref") == "opensip.product.target-attribution.2"
            and not mutated
            and not pub_batch_ok
            and not companion_ok
        ),
        helper_only=False,
    )


def probe_companion_branches():
    results = {}
    # external file
    ext = CHK.companion(0, occupancy="external")
    results["external_file"], results["external_file_err"] = schema_ok(COMPANION, ext)
    # unknown package
    unk = CHK.companion(0, kind="package", occupancy="unknown")
    results["unknown_package"], results["unknown_package_err"] = schema_ok(COMPANION, unk)
    # package first-party missing manifest
    pkg_bad = CHK.companion(0, resolved="left", kind="package", occupancy="first-party", evaluation="left")
    results["package_fp_missing_manifest"], _ = schema_ok(COMPANION, pkg_bad)
    pkg_ok = CHK.companion(
        0, resolved="left", kind="package", occupancy="first-party",
        evaluation="left", manifest="packages/left/package.json",
    )
    results["package_fp_with_manifest"], _ = schema_ok(COMPANION, pkg_ok)
    rec(
        "P-COMPANION-BRANCHES",
        "Independent occupancy-companion allOf: external/unknown/package branches",
        True,
        results,
        "must-operand",
        author_claim_holds=(
            results["external_file"] is True
            and results["unknown_package"] is True
            and results["package_fp_missing_manifest"] is False
            and results["package_fp_with_manifest"] is True
        ),
        helper_only=False,
    )


def probe_stageid_text_and_subset():
    ts_wire = DELIVERY["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]
    ts_stage = ts_wire["definitions"]["StageRequestV1"]["fields"]
    ts_batch = ts_wire["payloadSchemas"]["FactBatchV1"]["fields"]
    rust_req = RPP["wireSchema"]["definitions"]["StageRequestV2"]["fields"]
    fid = CHK.fact2("1")
    integer_stage = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)], stage_id=0), **CHK.owners(fid)
    ))
    # drive subset ourselves
    digest, spec = CHK.stage_spec()
    spec0 = dict(spec)
    spec0["outputSchemaDigest"] = CHK.H("2")
    spec0["producerClosure"] = CHK.C_PROV2
    digest0 = M.raw_digest({k: spec0[k] for k in CHK.STAGE_FIELDS})
    args = CHK.owners(fid, retained=5, request_ordinal=0)
    args["stage_specs"] = {digest: spec, digest0: spec0}
    args["execution_plan"]["stages"] = [
        {"ordinal": 0, "stageSpecDigest": digest0, "requires": [], "outputDomains": ["view"]},
        {"ordinal": 5, "stageSpecDigest": digest, "requires": [], "outputDomains": ["view"]},
    ]
    args["stage_receipts"] = [
        {"ordinal": 0, "stageSpecDigest": digest0, "producerClosure": CHK.C_PROV2,
         "outputDomains": ["view"], "outputRefs": [], "state": "complete", "unavailableReason": None},
        {"ordinal": 5, "stageSpecDigest": digest, "producerClosure": CHK.C_PROV,
         "outputDomains": ["view"], "outputRefs": [{"domain": "view", "digest": CHK.VIEW.split(":", 1)[1]}],
         "state": "complete", "unavailableReason": None},
    ]
    args["dispatch"] = CHK.dispatch_binding(digest, stage_id=CHK.STAGE_ID, retained=5, request_ordinal=0)
    subset_out = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args
    ))
    rec(
        "P-STAGEID-TEXT-SUBSET",
        "stageId is C-2 text; Analyze request ordinal ≠ retained Plan ordinal; integer stageId refuses",
        True,
        {
            "ts_StageRequestV1_stageId": ts_stage.get("stageId"),
            "ts_StageRequestV1_stageOrdinal": ts_stage.get("stageOrdinal"),
            "ts_FactBatchV1_stageId": ts_batch.get("stageId"),
            "rust_StageRequestV2": rust_req,
            "schema_stageId_type": BATCH["properties"]["stageId"].get("type"),
            "integer_stageId": integer_stage,
            "subset_retained5_request0": subset_out,
            "section96_text": "preserved on V3 as\n**text**" in NATIVE_MD or "preserved on V3 as **text**" in NATIVE_MD,
            "section96_subset": "may be a subset" in NATIVE_MD,
        },
        "must-operand",
        author_claim_holds=(
            BATCH["properties"]["stageId"].get("type") == "string"
            and integer_stage.get("key") == "PROVIDER_RETURN_SCHEMA"
            and subset_out.get("raised") is False
            and subset_out.get("retained") == 5
            and subset_out.get("request") == 0
            and subset_out.get("producer") == CHK.C_PROV
        ),
        helper_only=False,
    )


def probe_dispatch_receipts_timing():
    fid = CHK.fact2("1")
    args = CHK.owners(fid)
    args.pop("dispatch")
    omit_dispatch = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args
    ))
    args2 = CHK.owners(fid)
    args2["stage_receipts"] = None
    omit_receipts_capture = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args2
    ))
    args3 = CHK.owners(fid)
    buffer_ok = catch(lambda: M.buffer_fact_batch_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]),
        negotiated_tokens=args3["negotiated_tokens"],
        dispatch=args3["dispatch"],
    ))
    args4 = CHK.owners(fid)
    b = CHK.batch([CHK.candidate(0)], [CHK.companion(0)], analysis=77)
    wrong_ao = catch(lambda: M.bind_worker_occupancy(b, **args4))
    rec(
        "P-DISPATCH-RECEIPT-TIMING",
        "Dispatch required; capture requires receipts; buffer does not; analysisOrdinal cannot bypass dispatch",
        True,
        {
            "omit_dispatch": omit_dispatch,
            "omit_receipts_at_capture": omit_receipts_capture,
            "buffer_without_receipts": buffer_ok,
            "batch_analysis_77_vs_dispatch_0": wrong_ao,
        },
        "must-operand",
        author_claim_holds=(
            omit_dispatch.get("key") == "PROVIDER_RETURN_DISPATCH"
            and omit_receipts_capture.get("key") == "PROVIDER_RETURN_RECEIPT"
            and buffer_ok.get("status") == "buffered" and buffer_ok.get("nrefs") == 0
            and wrong_ao.get("key") == "PROVIDER_RETURN_ANALYSIS_ORDINAL"
        ),
        helper_only=False,
    )


def probe_prior_and_anchors():
    fid1, fid2 = CHK.fact2("1"), CHK.fact2("2")
    prior = {
        "schemaVersion": 2, "planId": CHK.PLAN, "sourceFactId": fid2, "producerClosure": CHK.C_PROV,
        "targetUniverse": CHK.U1, "targetNativeId": "file:src/b.ts", "kind": "file",
        "occupancy": "first-party", "exported": None, "logicalPath": None,
        "packageManifestPath": None, "evaluationNativeId": "src/b.ts",
    }
    args = CHK.owners(fid1, inventories=[CHK.inv_file(), CHK.inv_file("src/b.ts"), CHK.inv_symbol()])
    args["prior_records"] = [prior]
    args["views"][CHK.VIEW]["facts"] = [fid1, fid2]
    distinct = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args
    ))
    args_a = CHK.owners(fid1)
    cand = CHK.candidate(0)
    cand["anchors"] = [CHK.cand_anchor("src/b.ts")]
    diff_anchor = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([cand], [CHK.companion(0)]), **args_a
    ))
    rec(
        "P-PRIOR-AND-ANCHORS",
        "Compatible prior-batch V2 admits with current-only mint map; different-path same-length anchors refuse",
        True,
        {"distinct_prior": distinct, "different_anchor": diff_anchor},
        "must-operand",
        author_claim_holds=(
            distinct.get("raised") is False and distinct.get("status") == "admitted"
            and diff_anchor.get("key") == "PROVIDER_RETURN_MINT_MISJOIN"
            and "anchors" in (diff_anchor.get("detail") or "")
        ),
        helper_only=False,
    )


def probe_receipt_outputdomains_should():
    fid = CHK.fact2("1")
    args = CHK.owners(fid)
    args["stage_receipts"][0]["outputDomains"] = ["coverage"]
    args["execution_plan"]["stages"][0]["outputDomains"] = ["view"]
    out = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args
    ))
    rec(
        "P-RECEIPT-OUTPUTDOMAINS",
        "Receipt outputDomains may disagree with stage row; bind still admits if view is on outputRefs",
        True,
        {"result": out, "closed_receipt_fields": [
            "ordinal", "stageSpecDigest", "producerClosure", "outputDomains", "outputRefs", "state", "unavailableReason"
        ]},
        "should-operand",
        "Prior SHOULD-2. Capture now requires receipt + view digest on outputRefs. outputDomains/state still not compared.",
        author_claim_holds=None,
        helper_only=False,
    )


def probe_enumerator_and_host_internal():
    fid = CHK.fact2("1")
    args = CHK.owners(fid, enumerator=CHK.C_ENUM)
    enum_out = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args
    ))
    recs = {
        "schemaVersion": 2, "planId": CHK.PLAN, "sourceFactId": fid, "producerClosure": CHK.C_PROV,
        "targetUniverse": CHK.U1, "targetNativeId": "file:src/a.ts", "kind": "file",
        "occupancy": "first-party", "exported": None, "logicalPath": None,
        "packageManifestPath": None, "evaluationNativeId": "src/a.ts",
    }
    env = {"schemaVersion": 2, "planId": CHK.PLAN, "producerClosure": CHK.C_PROV, "stageOrdinal": 0, "records": [recs]}
    host = catch(lambda: M.admit_provider_attribution_return(env, origin="host-internal"))
    rec(
        "P-ENUMERATOR-HOST-INTERNAL",
        "enumerator ≠ producer admits; host-internal refuses without capture",
        True,
        {
            "enumerator": args["enumeration_plan"]["cells"][0]["programBindings"][0]["enumerator"]["closureId"],
            "producer": enum_out.get("producer"),
            "enum_out": enum_out,
            "host_internal": host,
        },
        "fact",
        author_claim_holds=(
            enum_out.get("status") == "admitted" and enum_out.get("producer") == CHK.C_PROV
            and host.get("key") == "PROVIDER_RETURN_HOST_AUTHORED"
        ),
        helper_only=True,
    )


def probe_stale_producersupply():
    stale = "After fact2 mint, emit one V2 record" in json.dumps(RETURN)
    rec(
        "P-STALE-PRODUCERSUPPLY",
        "Return-schema producerSupply still contains COMPLETE58 after-fact2-mint sentence",
        True,
        {"stale_after_fact2_mint": stale},
        "advisory-operand",
        "CURRENT delivery is OccupancyCompanionV1. Leftover sentence is documentation drift, not a wire bypass.",
        author_claim_holds=not stale,
        helper_only=False,
    )


def probe_native_negotiate():
    schemas = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text())
    cap = (schemas.get("$defs") or schemas).get("CapabilityToken") or {}
    enum = cap.get("enum") or []
    ts = list(N.TS2_TOKENS)
    ts_attr = list(N.TS2_TOKENS_ATTRIBUTION)
    rec(
        "P-NATIVE-NEGOTIATE",
        "target-attribution-v2 optional to spawn; not an identity token",
        True,
        {
            "token_in_enum": CHK.TOKEN in enum,
            "token_in_identity": CHK.TOKEN in N.IDENTITY_TOKENS,
            "accepted_without": N.negotiate(ts, ts, ts).get("outcome"),
            "accepted_with": N.negotiate(ts_attr, ts_attr, ts_attr).get("outcome"),
            "plan_requires_row_lacks_spawned": N.negotiate(ts_attr, ts, None).get("spawned"),
        },
        "fact",
        author_claim_holds=(
            CHK.TOKEN in enum
            and CHK.TOKEN not in N.IDENTITY_TOKENS
            and N.negotiate(ts, ts, ts).get("outcome") == "accepted"
            and N.negotiate(ts_attr, ts, None).get("spawned") is False
        ),
        helper_only=False,
    )


def probe_no_tmp_fallback():
    rec(
        "P-NO-TMP-FALLBACK",
        "No /tmp provider58 fallback; artifacts via HERE.parents[1]",
        True,
        {
            "has_tmp_path": "/tmp/" in MODEL_SRC,
            "artifacts": str(M.ARTIFACTS),
            "check_fact_plane": (M.ARTIFACTS / "check-fact-plane.py").is_file(),
        },
        "fact",
        author_claim_holds=("/tmp/" not in MODEL_SRC) and M.ARTIFACTS.name == "artifacts",
        helper_only=False,
    )


def main() -> int:
    probe_no_import_mutation_and_published_allof()
    probe_companion_branches()
    probe_stageid_text_and_subset()
    probe_dispatch_receipts_timing()
    probe_prior_and_anchors()
    probe_receipt_outputdomains_should()
    probe_enumerator_and_host_internal()
    probe_stale_producersupply()
    probe_native_negotiate()
    probe_no_tmp_fallback()
    report = {
        "standing": "Independent probes of COMPLETE56 vs COMPLETE30 MUST/SHOULD. Not 42-row oracle. Not compiler qualification.",
        "python": PY,
        "overlay": str(OVERLAY),
        "probe_count": len(PROBES),
        "probes_ran_ok": all(p["ok"] for p in PROBES),
        "author_claims_that_hold": [p["id"] for p in PROBES if p.get("author_claim_holds") is True],
        "author_claims_that_fail": [p["id"] for p in PROBES if p.get("author_claim_holds") is False],
        "probes": PROBES,
    }
    out = HERE / "independent-probe-results.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "wrote": str(out),
        "hold": report["author_claims_that_hold"],
        "fail": report["author_claims_that_fail"],
        "receipt_outputdomains": next(p["evidence"] for p in PROBES if p["id"] == "P-RECEIPT-OUTPUTDOMAINS"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
