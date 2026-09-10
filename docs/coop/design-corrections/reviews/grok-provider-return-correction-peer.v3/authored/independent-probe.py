#!/usr/bin/env python3
"""Independent coauthor-peer probes of provider-return e2e correction (source v3).

Design-reference / owner-schema probes. Not close_run. Not compiler qualification.
Not an expected-output oracle of the 27 helper cases.
Python: /tmp/opensip-architecture-review-env/bin/python -I -B
"""
from __future__ import annotations

import copy
import importlib.util
import inspect
import json
import sys
from pathlib import Path

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


M = _load("v3_provider_return", FOUND / "provider_attribution_return_model.v2.py")
C = M.C
N = _load("v3_native", NATIVE / "native_evidence_model.v2.py")
CHK = _load("v3_return_checker", FOUND / "check-provider-attribution-return.v2.py")

BATCH_PUBLISHED = json.loads((NATIVE / "fact-batch.schema.v3.json").read_text(encoding="utf-8"))
COMPANION_PUBLISHED = json.loads((NATIVE / "occupancy-companion.schema.v1.json").read_text(encoding="utf-8"))
RETURN_PUBLISHED = json.loads((FOUND / "provider-target-attribution-return.schema.v2.json").read_text(encoding="utf-8"))
TARGET_PUBLISHED = json.loads((FOUND / "target-attribution.schema.v2.json").read_text(encoding="utf-8"))
NATIVE_MD = (PROD / "native-evidence.md").read_text(encoding="utf-8")
DELIVERY = json.loads((ART / "delivery.v2.json").read_text(encoding="utf-8"))
RPP = json.loads((ART / "rust-provider-protocol.v2.json").read_text(encoding="utf-8"))
EXEC_SCHEMA = json.loads((FOUND / "execution-inputs.schema.v1.json").read_text(encoding="utf-8"))
CANON_SRC = (FOUND / "canonical.py").read_text(encoding="utf-8")
MODEL_SRC = (FOUND / "provider_attribution_return_model.v2.py").read_text(encoding="utf-8")

U1 = CHK.U1
PLAN = CHK.PLAN
C_PROV = CHK.C_PROV
TOKEN = CHK.TOKEN

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
        return {"raised": False, "status": out.get("status") if isinstance(out, dict) else None,
                "producerClosure": out.get("producerClosure") if isinstance(out, dict) else None,
                "stageId": out.get("stageId") if isinstance(out, dict) else None,
                "nrefs": len(out.get("hostDerivedRefs") or []) if isinstance(out, dict) else None,
                "key": None}
    except M.ProviderReturnAdmissionError as exc:
        return {"raised": True, "key": exc.key, "detail": exc.detail, "status": None}


def probe_published_batch_schema_incomplete():
    """NEW blind using only fact-batch.schema.v3.json $defs OccupancyCompanionV1 (no allOf)."""
    payload = CHK.imports_payload()
    cbor_hex = M.deterministic_cbor(payload).hex()
    cand = CHK.candidate(0)
    # first-party with null evaluationNativeId: COMPANION_PUBLISHED allOf refuses; published $defs may not.
    bad_comp = CHK.companion(0)
    bad_comp["evaluationNativeId"] = None
    batch = {
        "schemaVersion": 3, "analysisOrdinal": 0, "stageId": 0, "batchIndex": 0,
        "candidates": [cand],
        "occupancyCompanions": [bad_comp],
    }
    pub_ok = True
    pub_err = None
    try:
        C.validate(BATCH_PUBLISHED, batch)
    except Exception as exc:  # noqa: BLE001
        pub_ok = False
        pub_err = f"{type(exc).__name__}: {str(exc).splitlines()[0]}"
    full_ok = True
    try:
        C.validate(COMPANION_PUBLISHED, bad_comp)
    except Exception:  # noqa: BLE001
        full_ok = False
    mutated_items_are_full = M.BATCH_SCHEMA["properties"]["occupancyCompanions"]["items"].get("$id") == COMPANION_PUBLISHED.get("$id")
    rec(
        "P-SCHEMA-PUBLISHED-INCOMPLETE",
        "Published FactBatchV3 $defs OccupancyCompanionV1 lacks allOf; Python mutates items at import",
        True,
        {
            "published_batch_admits_first_party_null_eval": pub_ok,
            "published_batch_error": pub_err,
            "full_companion_schema_admits_null_eval": full_ok,
            "model_mutates_batch_items": "BATCH_SCHEMA[\"properties\"][\"occupancyCompanions\"][\"items\"] = COMPANION_SCHEMA" in MODEL_SRC,
            "model_mutates_return_items": "RETURN_SCHEMA[\"properties\"][\"records\"][\"items\"] = TARGET_SCHEMA" in MODEL_SRC,
            "published_defs_has_allOf": "allOf" in BATCH_PUBLISHED.get("$defs", {}).get("OccupancyCompanionV1", {}),
            "companion_schema_has_allOf": "allOf" in COMPANION_PUBLISHED,
            "mutated_items_id": (M.BATCH_SCHEMA["properties"]["occupancyCompanions"]["items"] or {}).get("$id"),
        },
        "must-operand",
        "A new blind implementer of fact-batch.schema.v3.json alone does not get occupancy allOf.",
        author_claim_holds=not pub_ok,
        helper_only=False,
    )


def probe_return_schema_not_ref_v2():
    items = RETURN_PUBLISHED["properties"]["records"]["items"]
    has_ref = "$ref" in items
    has_allof = "allOf" in items
    leftover_after_mint = "After fact2 mint, emit one V2 record" in json.dumps(RETURN_PUBLISHED)
    leftover_joins_envelope = any("envelope.stageOrdinal" in j for j in RETURN_PUBLISHED["x-opensip-return-law"]["joins"])
    rec(
        "P-RETURN-SCHEMA-NOT-REF",
        "Return records.items is a field list, not $ref selected V2; leftover COMPLETE58 join/producerSupply prose",
        True,
        {
            "items_$ref": items.get("$ref"),
            "items_allOf": has_allof,
            "items_additionalProperties": items.get("additionalProperties"),
            "logicalPath_schema": items.get("properties", {}).get("logicalPath"),
            "leftover_after_fact2_mint": leftover_after_mint,
            "leftover_envelope_stageOrdinal_joins": leftover_joins_envelope,
            "python_replaces_items": "RETURN_SCHEMA[\"properties\"][\"records\"][\"items\"] = TARGET_SCHEMA" in MODEL_SRC,
        },
        "must-operand",
        author_claim_holds=has_ref or has_allof,
        helper_only=False,
    )


def probe_optional_receipt_and_analysis_ordinal():
    fid = CHK.fact2("1")
    args = CHK.owners(fid)
    args.pop("stage_receipts", None)
    omit_receipts = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args
    ))
    args2 = CHK.owners(fid)
    args2.pop("analyze_analysis_ordinal", None)
    b = CHK.batch([CHK.candidate(0)], [CHK.companion(0)])
    b["analysisOrdinal"] = 9
    omit_ao = catch(lambda: M.bind_worker_occupancy(b, **args2))
    args3 = CHK.owners(fid)
    args3["analyze_analysis_ordinal"] = 0
    b3 = CHK.batch([CHK.candidate(0)], [CHK.companion(0)])
    b3["analysisOrdinal"] = 9
    with_ao = catch(lambda: M.bind_worker_occupancy(b3, **args3))
    sig = inspect.signature(M.bind_worker_occupancy)
    rec(
        "P-OPTIONAL-RECEIPT-ANALYSIS",
        "Omitting stage_receipts or analyze_analysis_ordinal bypasses those joins",
        True,
        {
            "omit_receipts": omit_receipts,
            "omit_analysis_ordinal_wrong_batch_9": omit_ao,
            "supplied_analysis_ordinal_wrong_batch_9": with_ao,
            "param_defaults": {
                "stage_receipts": sig.parameters["stage_receipts"].default,
                "analyze_analysis_ordinal": sig.parameters["analyze_analysis_ordinal"].default,
            },
            "published_invocation_inputs": list(RETURN_PUBLISHED["x-opensip-return-law"]["invocation"]["inputs"]),
            "section96_trusted_mentions_receipts": "hostCapture.stageReceipts" in NATIVE_MD.split("### 9.6")[1][:2500] if "### 9.6" in NATIVE_MD else None,
        },
        "must-operand",
        "Published invocation.inputs omits receipts/analysisOrdinal; function docstring lists them as trusted observations; skip-if-None is not complete-entry enforcement.",
        author_claim_holds=not (
            omit_receipts.get("raised") is False and omit_receipts.get("status") == "admitted"
            and omit_ao.get("raised") is False and omit_ao.get("status") == "admitted"
            and with_ao.get("raised") is True
        ),
        helper_only=False,
    )


def probe_analyze_subset_stage_correlation():
    """Plan ordinals 0=other, 2=this producer. Analyze contiguous stageOrdinal=0 for the producer stage.
    Bind looks up execution_plan.stages by ordinal==batch.stageId."""
    fid = CHK.fact2("1")
    args = CHK.owners(fid)
    digest, spec = CHK.stage_spec()
    other = {
        "schemaVersion": 2, "planId": PLAN, "producerClosure": CHK.C_PROV2,
        "operation": "analyze", "parameters": [], "outputDomains": ["view"],
        "outputSchemaDigest": CHK.H("9"),
    }
    other_digest = M.raw_digest({k: other[k] for k in CHK.STAGE_FIELDS})
    args["stage_specs"] = {digest: spec, other_digest: other}
    args["execution_plan"] = {
        "schemaVersion": 2, "planId": PLAN,
        "stages": [
            {"ordinal": 0, "stageSpecDigest": other_digest, "requires": [], "outputDomains": ["view"]},
            {"ordinal": 2, "stageSpecDigest": digest, "requires": [], "outputDomains": ["view"]},
        ],
    }
    args["stage_receipts"] = [
        {"ordinal": 0, "stageSpecDigest": other_digest, "producerClosure": CHK.C_PROV2,
         "outputDomains": ["view"], "outputRefs": [], "state": "complete", "unavailableReason": None},
        {"ordinal": 2, "stageSpecDigest": digest, "producerClosure": C_PROV,
         "outputDomains": ["view"], "outputRefs": [], "state": "complete", "unavailableReason": None},
    ]
    # Worker echoes Analyze contiguous stageOrdinal 0 (StageRequestV2 / AnalyzeV1 law).
    contiguous = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)], stage_id=0), **args
    ))
    # If host instead stuffed plan ordinal 2 into FactBatch.stageId:
    plan_ord = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)], stage_id=2), **args
    ))
    rec(
        "P-ANALYZE-SUBSET-STAGEID",
        "Analyze-contiguous stageId=0 binds the wrong Plan stage when Analyze is a provider subset",
        True,
        {
            "contiguous_analyze_ordinal_0": contiguous,
            "plan_ordinal_2": plan_ord,
            "wrong_producer_if_contiguous": contiguous.get("producerClosure"),
        },
        "must-operand",
        "StageRequestV2.stageOrdinal is contiguous Analyze order; TS AnalyzeV1.stageId is C-2 text; execution-plan.stages[].ordinal is Plan-wide. §9.6 stages[k] index equality is not a law.",
        author_claim_holds=(
            contiguous.get("raised") is False and contiguous.get("producerClosure") == C_PROV
        ),
        helper_only=False,
    )


def probe_stageid_type_vs_owners():
    ts_wire = DELIVERY["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]
    ts_stage = ts_wire["definitions"]["StageRequestV1"]["fields"]
    ts_batch = ts_wire["payloadSchemas"]["FactBatchV1"]["fields"]
    rust_req = RPP["wireSchema"]["definitions"]["StageRequestV2"]["fields"]
    rust_batch_req = RPP["wireSchema"]["payloadSchemas"]["FactBatchV2"]["required"]
    v3_stageid = BATCH_PUBLISHED["properties"]["stageId"]
    sec96 = NATIVE_MD.split("### 9.6")[1].split("### 9.")[0] if "### 9.6" in NATIVE_MD else ""
    rec(
        "P-STAGEID-TYPE-OWNERS",
        "FactBatchV3.stageId integer vs owning TS text stageId and Rust contiguous Analyze stageOrdinal",
        True,
        {
            "ts_StageRequestV1_stageId": ts_stage.get("stageId"),
            "ts_StageRequestV1_stageOrdinal": ts_stage.get("stageOrdinal"),
            "ts_FactBatchV1_stageId": ts_batch.get("stageId"),
            "rust_StageRequestV2_stageOrdinal": rust_req.get("stageOrdinal"),
            "rust_FactBatchV2_required": rust_batch_req,
            "factBatchV3_stageId": v3_stageid,
            "section96_claims_unchanged_analyze": "Stage correlation (unchanged Analyze)" in sec96,
            "section96_index_k": "AnalyzeV2.stages[k].stageOrdinal" in sec96 and "execution-plan.stages[k].ordinal" in sec96,
            "section96_batch_stageOrdinal_typo": "batch.stageOrdinal" in sec96,
            "section94_mentions_analyze_payload": "stageRequests" in NATIVE_MD.split("### 9.4")[1].split("### 9.5")[0],
        },
        "must-operand",
        author_claim_holds=False,
        helper_only=False,
    )


def probe_prior_records_distinct_admittable():
    fid1, fid2 = CHK.fact2("1"), CHK.fact2("2")
    prior = {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": fid2, "producerClosure": C_PROV,
        "targetUniverse": U1, "targetNativeId": "file:src/b.ts", "kind": "file",
        "occupancy": "first-party", "exported": None, "logicalPath": None,
        "packageManifestPath": None, "evaluationNativeId": "src/b.ts",
    }
    args = CHK.owners(fid1, inventories=[CHK.inv_file(), CHK.inv_file("src/b.ts"), CHK.inv_symbol()])
    args["prior_records"] = [prior]
    args["views"][CHK.VIEW]["facts"] = [fid1, fid2]
    # current batch only mints fid1 — prior batch fact is independently known
    distinct = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args
    ))
    rec(
        "P-PRIOR-DISTINCT-ADMITTABLE",
        "Distinct prior-batch V2 is not admittable unless smuggled into current minted_by_ordinal",
        True,
        {"result": distinct, "current_mint_keys": list(args["minted_by_ordinal"])},
        "must-operand",
        "Author prior test only covers contradictory occupancy while both facts sit in the current mint map.",
        author_claim_holds=not (distinct.get("raised") is True),
        helper_only=False,
    )


def probe_mint_anchors_count_only():
    fid = CHK.fact2("1")
    args = CHK.owners(fid)
    fact = args["minted_by_ordinal"][0]
    fact = dict(fact)
    fact["anchors"] = [{"kind": "source-span", "path": "other.ts"}]  # same count, different content
    args["minted_by_ordinal"] = {0: fact}
    out = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args
    ))
    rec(
        "P-MINT-ANCHORS-COUNT-ONLY",
        "Mint correspondence compares payload fully but anchors only by count",
        True,
        {"result": out},
        "should-operand",
        author_claim_holds=out.get("raised") is True,
        helper_only=False,
    )


def probe_receipt_fields_partial():
    fields = EXEC_SCHEMA["$defs"]["StageReceiptV1"]["required"]
    src = MODEL_SRC
    rec(
        "P-RECEIPT-FIELDS-PARTIAL",
        "Closed StageReceiptV1 has 7 required fields; bind checks ordinal/stageSpecDigest/producerClosure only",
        True,
        {
            "closed_required": fields,
            "bind_checks_outputDomains": "outputDomains" in src and "_require_receipt" in src,
            "require_receipt_source": [ln.strip() for ln in src.split("def _require_receipt", 1)[1].split("def ", 1)[0].splitlines() if ln.strip()][:20],
        },
        "should-operand",
        helper_only=False,
    )


def probe_enumerator_distinct_from_producer():
    fid = CHK.fact2("1")
    args = CHK.owners(fid, enumerator=CHK.C_ENUM)
    out = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0)], [CHK.companion(0)]), **args
    ))
    rec(
        "P-ENUMERATOR-DISTINCT",
        "XI enumerator.closureId may differ from Analyze stage-spec producerClosure; bind uses producer",
        True,
        {
            "result": out,
            "enumerator": args["enumeration_plan"]["cells"][0]["programBindings"][0]["enumerator"]["closureId"],
            "producer": out.get("producerClosure"),
        },
        "fact",
        "Required join is execution-plan stage-spec producerClosure + receipt producerClosure + fact.producerClosure + view.producerClosure. Not enumerator.closureId.",
        author_claim_holds=out.get("raised") is False and out.get("producerClosure") == C_PROV,
        helper_only=True,
    )


def probe_host_internal_and_c15():
    recs = {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": CHK.fact2("1"), "producerClosure": C_PROV,
        "targetUniverse": U1, "targetNativeId": "file:src/a.ts", "kind": "file",
        "occupancy": "first-party", "exported": None, "logicalPath": None,
        "packageManifestPath": None, "evaluationNativeId": "src/a.ts",
    }
    env = {"schemaVersion": 2, "planId": PLAN, "producerClosure": C_PROV, "stageOrdinal": 0, "records": [recs]}
    host = catch(lambda: M.admit_provider_attribution_return(env, origin="host-internal"))
    fid = CHK.fact2("1")
    args = CHK.owners(fid, resolved="file:src/a.ts",
                      inventories=[CHK.inv_file("file:src/a.ts"), CHK.inv_file("src/b.ts"), CHK.inv_symbol()])
    args["minted_by_ordinal"] = {0: CHK.imports_fact(fid, "file:src/a.ts")}
    c15 = catch(lambda: M.bind_worker_occupancy(
        CHK.batch([CHK.candidate(0, "file:src/a.ts")], [CHK.companion(0, "file:src/a.ts", evaluation="src/b.ts")]),
        **args,
    ))
    rec(
        "P-HOST-INTERNAL-AND-C15",
        "host-internal refuses without capture; C15 still refuses contradictory first-party",
        True,
        {"host_internal": host, "c15": c15},
        "fact",
        author_claim_holds=(
            host.get("key") == "PROVIDER_RETURN_HOST_AUTHORED"
            and c15.get("key") == "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT"
        ),
        helper_only=True,
    )


def probe_candidateordinal_vocab():
    rec(
        "P-CANDIDATEORDINAL-VOCAB",
        "candidateOrdinal is registered in canonical.py exact_order and documented as unique nondecreasing integers",
        True,
        {
            "in_canonical": "elif order == 'candidateOrdinal':" in CANON_SRC,
            "contiguous_not_required_by_order_token": "contiguous" not in CANON_SRC.split("candidateOrdinal")[1][:400],
            "schema_says_contiguous_additional": "Contiguous-within-stage is additional admission" in json.dumps(BATCH_PUBLISHED),
            "bind_checks_contiguous": "contiguous" in MODEL_SRC.lower(),
        },
        "advisory-operand",
        "Token is implementable from canonical.py. Contiguous-within-stage across batches is not this token and is not enforced in bind.",
        author_claim_holds="elif order == 'candidateOrdinal':" in CANON_SRC,
        helper_only=False,
    )


def probe_native_negotiate():
    schemas = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text())
    cap = (schemas.get("$defs") or schemas).get("CapabilityToken") or {}
    enum = cap.get("enum") or []
    ts = list(N.TS2_TOKENS)
    ts_attr = list(N.TS2_TOKENS_ATTRIBUTION)
    missing = N.negotiate(["plan-identity-plan2"], ["sealed-vfs-v1"], None)
    no_token_spawn = N.negotiate(ts, ts, ts)
    with_token = N.negotiate(ts_attr, ts_attr, ts_attr)
    plan_requires_attr_row_lacks = N.negotiate(ts_attr, ts, None)
    rec(
        "P-NATIVE-NEGOTIATE",
        "target-attribution-v2 is optional to spawn; Plan-required missing token does not spawn",
        True,
        {
            "token_in_capability_enum": TOKEN in enum,
            "identity_missing": missing,
            "accepted_without_attr": no_token_spawn,
            "accepted_with_attr": with_token,
            "plan_requires_attr_row_lacks": plan_requires_attr_row_lacks,
        },
        "fact",
        "Owner native negotiate, not a synthetic occupancy map. Still not a live FactBatch through protocol3_run.",
        author_claim_holds=(
            missing.get("spawned") is False
            and no_token_spawn.get("outcome") == "accepted"
            and with_token.get("outcome") == "accepted"
            and plan_requires_attr_row_lacks.get("spawned") is False
        ),
        helper_only=False,
    )


def probe_no_tmp_fallback():
    rec(
        "P-NO-TMP-FALLBACK",
        "Model loads only HERE siblings and HERE.parents[1]/artifacts/check-fact-plane.py",
        True,
        {
            "artifacts_path_expr": "HERE.parents[1] / \"artifacts\"",
            "has_provider58_fallback": "target-provider-return-successor" in MODEL_SRC or "/tmp/" in MODEL_SRC,
            "file_not_found_on_missing": "raise FileNotFoundError" in MODEL_SRC,
            "resolved_artifacts": str(M.ARTIFACTS),
            "check_fact_plane_exists": (M.ARTIFACTS / "check-fact-plane.py").is_file(),
        },
        "fact",
        author_claim_holds=("/tmp/" not in MODEL_SRC) and (M.ARTIFACTS.name == "artifacts"),
        helper_only=False,
    )


def main() -> int:
    probe_published_batch_schema_incomplete()
    probe_return_schema_not_ref_v2()
    probe_optional_receipt_and_analysis_ordinal()
    probe_analyze_subset_stage_correlation()
    probe_stageid_type_vs_owners()
    probe_prior_records_distinct_admittable()
    probe_mint_anchors_count_only()
    probe_receipt_fields_partial()
    probe_enumerator_distinct_from_producer()
    probe_host_internal_and_c15()
    probe_candidateordinal_vocab()
    probe_native_negotiate()
    probe_no_tmp_fallback()
    report = {
        "standing": "Independent Grok coauthor-peer probes of v3 corrected bytes vs source58 findings. Not 27-pass oracle. Not close_run. Not pin seal. Pins stale; overlay disposable.",
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
        "probe_count": len(PROBES),
        "fail_claims": report["author_claims_that_fail"],
        "hold_claims": report["author_claims_that_hold"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
