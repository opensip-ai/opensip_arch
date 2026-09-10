#!/usr/bin/env python3
"""Independent coauthor-peer probes for provider-return correction.

Design-reference boundary only. Not a full Run. Not suite integration.
Does not mutate successor source. Python: -I -B.
"""
from __future__ import annotations

import importlib.util
import inspect
import json
import sys
from pathlib import Path

PY = sys.executable
SUCC = Path("/tmp/opensip-design-corrections/target-provider-return-successor.v1")
FOUND = SUCC / "docs/coop/design-corrections/foundation"
WORKFLOWS = SUCC / "docs/coop/design-corrections/workflows"
PRED = Path("/tmp/opensip-design-corrections/target-identity-successor.v1")
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v24")
HERE = Path(__file__).resolve().parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = _load("peer_provider_return_model", FOUND / "provider_attribution_return_model.v2.py")
AM = M.AM
C = M.C
FM = M.FM
SCHEMA = M.SCHEMA
V2_SCHEMA = json.loads((FOUND / "target-attribution.schema.v2.json").read_text(encoding="utf-8"))
FAULT_SCHEMA = json.loads((FOUND / "evaluator-fault-observation.schema.v3.json").read_text(encoding="utf-8"))
COMMON = json.loads((WORKFLOWS / "schemas/evaluator3/common.schema.json").read_text(encoding="utf-8"))
DELIVERY = json.loads((SUCC / "docs/coop/artifacts/delivery.v2.json").read_text(encoding="utf-8"))
RPP = json.loads((SUCC / "docs/coop/artifacts/rust-provider-protocol.v2.json").read_text(encoding="utf-8"))
NATIVE = (SUCC / "docs/v2/contracts/product-v1/native-evidence.md").read_text(encoding="utf-8")
EXEC_MD = (FOUND / "execution-inputs-contract.v1.md").read_text(encoding="utf-8")
MODEL_SRC = (FOUND / "provider_attribution_return_model.v2.py").read_text(encoding="utf-8")
ATOM_SRC = (FOUND / "atom_model.v1.py").read_text(encoding="utf-8")
PRED_ATOM_SRC = (PRED / "docs/coop/design-corrections/foundation/atom_model.v1.py").read_text(encoding="utf-8")

U1 = "11" * 32
C_PROV = "closure2:" + "aa" * 32
C_EVAL = "closure2:" + "bb" * 32
PLAN = "plan2:" + "cc" * 32
SNAP = "snapshot2:" + "aa" * 32


def H(ch: str) -> str:
    return ch * 64


def fact2(ch: str) -> str:
    return "fact2:" + H(ch)


def inv_file(path="src/a.ts"):
    return {
        "schemaVersion": 1, "planId": PLAN, "parameterDigest": H("0"),
        "cellOrdinal": 0, "programOrdinal": 0, "kind": "file", "state": "complete",
        "deficiency": None, "nativeCause": None, "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": path, "kind": "file", "path": path, "qualifiedName": path,
            "subjectLanguage": "typescript", "signatureTokens": [], "projections": [],
        }],
        "universe": U1,
    }


def inv_symbol(nid="ts-symbol:src/a.ts#f", path="src/a.ts"):
    return {
        "schemaVersion": 1, "planId": PLAN, "parameterDigest": H("0"),
        "cellOrdinal": 0, "programOrdinal": 0, "kind": "symbol", "state": "complete",
        "deficiency": None, "nativeCause": None, "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": nid, "kind": "symbol", "path": path, "qualifiedName": "f",
            "subjectLanguage": "typescript", "exported": "exported",
            "signatureTokens": ["f"], "projections": [],
        }],
        "universe": U1,
    }


def plan_one(kinds=None, closure=C_PROV):
    kinds = kinds or ["symbol", "file"]
    return {
        "schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": H("0"), "membershipDigest": H("0"),
        "cells": [{
            "capabilityId": "imports", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
            "required": True, "kinds": kinds,
            "programBindings": [{
                "ordinal": 0, "provenance": "default-unit",
                "enumerator": {"status": "selected", "closureId": closure},
                "nativeContextDigest": H("0"), "universe": U1, "programEntry": None,
                "extents": [{"kind": k, "paths": ["src/a.ts"]} for k in kinds],
            }],
        }],
    }


def imports_fact(fid, resolved="file:src/a.ts", resolution="resolved-target", producer=C_PROV):
    payload = {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a"}
    if resolution == "resolved-target":
        payload["resolvedTarget"] = resolved
    return {
        "factId": fid, "relation": "imports", "resolution": resolution,
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": producer,
        "confidenceMillionths": 1000000,
        "payload": payload,
        "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
    }


def sidecar(fid, native, kind="file", occupancy="first-party", exported=None, logical=None,
            manifest=None, evaluation=None, producer=C_PROV):
    if occupancy == "first-party" and evaluation is None:
        evaluation = native if kind == "symbol" else None
    if occupancy != "first-party":
        evaluation = None
    return {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": fid, "producerClosure": producer,
        "targetUniverse": U1, "targetNativeId": native, "kind": kind, "occupancy": occupancy,
        "exported": exported, "logicalPath": logical, "packageManifestPath": manifest,
        "evaluationNativeId": evaluation,
    }


def envelope(records, stage=0, producer=C_PROV, plan=PLAN):
    ordered = sorted(records, key=lambda r: r["sourceFactId"].encode("utf-8"))
    return {
        "schemaVersion": 2, "planId": plan, "producerClosure": producer,
        "stageOrdinal": stage, "records": ordered,
    }


def kw(**over):
    base = dict(
        plan_id=PLAN, producer_closure=C_PROV, stage_ordinal=0,
        inventories=[inv_file(), inv_file("src/b.ts"), inv_symbol()],
        enumeration_plan=plan_one(),
        closures={C_PROV: {"kind": "provider"}, C_EVAL: {"kind": "evaluator"}},
    )
    base.update(over)
    return base


def catch_key(fn):
    try:
        out = fn()
        return {"raised": False, "status": out.get("status") if isinstance(out, dict) else None,
                "hostDerivedRefs": (out.get("hostDerivedRefs") if isinstance(out, dict) else None),
                "origin": (out.get("origin") if isinstance(out, dict) else None)}
    except M.ProviderReturnAdmissionError as exc:
        return {"raised": True, "key": exc.key, "detail": exc.detail}
    except AM.AtomAdmissionError as exc:
        return {"raised": True, "key": exc.key, "detail": getattr(exc, "detail", ""), "via": "atom"}


PROBES = []


def rec(probe_id, title, ok, evidence, classification, notes=None, author_claim_holds=None):
    """ok = probe ran without crash and evidence was captured.
    author_claim_holds = whether the author's stated contract holds on this operand.
    None means the probe is observational, not a claim test.
    """
    PROBES.append({
        "id": probe_id,
        "title": title,
        "ok": ok,
        "author_claim_holds": author_claim_holds,
        "classification": classification,
        "evidence": evidence,
        "notes": notes,
    })


def probe_author_controls_are_labeled_boundary():
    src = (FOUND / "check-provider-attribution-return.v2.py").read_text(encoding="utf-8")
    rec(
        "P-LABEL-BOUNDARY",
        "Author checker labels schema/atom/capture boundary and fullRun false",
        ("Not full Run replay" in src) and ("fullRun" in src) and ("LIVE D9 not discharged" in src),
        {"checker_docstring_prefix": src.splitlines()[0], "mentions_fullRun": "fullRun" in src},
        "fact",
        "18 helper controls cannot be whole-design approval.",
        author_claim_holds=("Not full Run replay" in src) and ("fullRun" in src) and ("LIVE D9 not discharged" in src),
    )


def probe_no_build_or_table_type():
    names = [n for n in dir(M) if not n.startswith("_")]
    has_build = any("build" in n.lower() or "encode" in n.lower() or "table" in n.lower() for n in names)
    params = inspect.signature(M.admit_provider_attribution_return).parameters
    missing = [p for p in (
        "execution_plan", "stage_receipts", "views", "selected_views",
        "resolution_table", "compiler_table", "candidate_ordinals",
    ) if p not in params]
    rec(
        "P-NO-WRAPPER-BUILD",
        "No typed wrapper BUILD/table/lifecycle; only host admit of a caller envelope",
        True,
        {
            "public_names": names,
            "has_build_encode_table_symbol": has_build,
            "admit_params": list(params),
            "missing_params": missing,
        },
        "must-operand",
        "Wrapper supply is prose. Admit consumes an already-built envelope.",
        author_claim_holds=False,
    )


def probe_schema_does_not_nest_v2():
    items = SCHEMA["properties"]["records"]["items"]
    ref = items.get("$ref") or items.get("$defs") or items.get("allOf")
    extra = items.get("additionalProperties")
    required = items.get("required")
    incomplete = {
        "schemaVersion": 2,
        "planId": PLAN,
        "producerClosure": C_PROV,
        "stageOrdinal": 0,
        "records": [{
            "schemaVersion": 2,
            "planId": PLAN,
            "sourceFactId": fact2("1"),
            "producerClosure": C_PROV,
            "unknownField": "not-a-v2-body",
        }],
    }
    schema_ok = True
    schema_err = None
    try:
        C.validate(SCHEMA, incomplete)
    except Exception as exc:  # noqa: BLE001
        schema_ok = False
        schema_err = f"{type(exc).__name__}: {exc}"
    v2_ok = True
    v2_err = None
    try:
        C.validate(V2_SCHEMA, incomplete["records"][0])
    except Exception as exc:  # noqa: BLE001
        v2_ok = False
        v2_err = f"{type(exc).__name__}: {str(exc).splitlines()[0]}"
    rec(
        "P-SCHEMA-NEST-V2",
        "Envelope JSON Schema does not $ref selected TargetAttributionV2; additionalProperties true",
        True,
        {
            "items_$ref": ref,
            "items_additionalProperties": extra,
            "items_required": required,
            "incomplete_record_passes_envelope_schema": schema_ok,
            "envelope_schema_error": schema_err,
            "incomplete_record_passes_v2_schema": v2_ok,
            "v2_schema_error": v2_err,
        },
        "must-operand",
        "Prose says each item MUST admit as selected V2; envelope schema does not nest that owner schema.",
        author_claim_holds=not (schema_ok and not v2_ok and extra is True and not ref),
    )


def probe_stage_is_caller_echo():
    fid = fact2("1")
    recs = [sidecar(fid, "file:src/a.ts", evaluation="src/a.ts")]
    # Matching-but-wrong: envelope and caller both say stage 99; enumeration plan has no stages.
    out = catch_key(lambda: M.admit_provider_attribution_return(
        envelope(recs, stage=99),
        facts={fid: imports_fact(fid)},
        **kw(stage_ordinal=99),
    ))
    mismatch = catch_key(lambda: M.admit_provider_attribution_return(
        envelope(recs, stage=0),
        facts={fid: imports_fact(fid)},
        **kw(stage_ordinal=1),
    ))
    rec(
        "P-STAGE-CALLER-ECHO",
        "stageOrdinal checked only against caller argument, not execution-plan/stageReceipts",
        True,
        {
            "matching_wrong_stage_99": out,
            "mismatch_envelope0_caller1": mismatch,
            "admit_has_execution_plan": "execution_plan" in inspect.signature(M.admit_provider_attribution_return).parameters,
            "schema_claims_join": SCHEMA["x-opensip-return-law"]["joins"],
        },
        "must-operand",
        "Author test_stage_mismatch only flips the caller argument to disagree with the envelope.",
        author_claim_holds=not (
            out.get("raised") is False and out.get("status") == "admitted"
            and mismatch.get("raised") is True and mismatch.get("key") == "PROVIDER_RETURN_STAGE_ORDINAL"
        ),
    )


def probe_producer_not_plan_selected():
    fid = fact2("1")
    other = "closure2:" + "dd" * 32
    recs = [sidecar(fid, "file:src/a.ts", evaluation="src/a.ts", producer=other)]
    # kind=provider but not the enumeration-plan selected enumerator
    out = catch_key(lambda: M.admit_provider_attribution_return(
        envelope(recs, producer=other),
        facts={fid: imports_fact(fid, producer=other)},
        **kw(
            producer_closure=other,
            closures={other: {"kind": "provider"}, C_PROV: {"kind": "provider"}},
            enumeration_plan=plan_one(closure=C_PROV),
        ),
    ))
    rec(
        "P-PRODUCER-NOT-PLAN-SELECTED",
        "producerClosure kind=provider admits even when enumeration-plan selected enumerator differs",
        True,
        {"result": out, "enumeration_selected": C_PROV, "admitted_producer": other},
        "must-operand",
        "Schema producerClosure description requires Plan-selected kind=provider. Admit checks kind only.",
        author_claim_holds=not (out.get("raised") is False and out.get("status") == "admitted"),
    )


def probe_host_internal_captures():
    fid = fact2("1")
    recs = [sidecar(fid, "file:src/a.ts", evaluation="src/a.ts")]
    out = catch_key(lambda: M.admit_provider_attribution_return(
        envelope(recs),
        facts={fid: imports_fact(fid)},
        origin="host-internal",
        **kw(),
    ))
    rec(
        "P-HOST-INTERNAL-CAPTURES",
        "origin=host-internal still admits and captures hostDerivedRefs",
        True,
        {"result": out},
        "must-operand",
        "Host-invented mapping is specified as HOST.INVARIANT_VIOLATED, but admit captures.",
        author_claim_holds=not (
            out.get("raised") is False and out.get("status") == "admitted"
            and out.get("origin") == "host-internal" and out.get("hostDerivedRefs")
        ),
    )


def probe_c15_and_unique_join():
    fid = fact2("1")
    conflict = catch_key(lambda: M.admit_provider_attribution_return(
        envelope([sidecar(fid, "file:src/a.ts", evaluation="src/b.ts")]),
        facts={fid: imports_fact(fid, "file:src/a.ts")},
        **kw(inventories=[inv_file("file:src/a.ts"), inv_file("src/b.ts"), inv_symbol()]),
    ))
    agree = catch_key(lambda: M.admit_provider_attribution_return(
        envelope([sidecar(fid, "file:src/a.ts", evaluation="file:src/a.ts")]),
        facts={fid: imports_fact(fid, "file:src/a.ts")},
        **kw(inventories=[inv_file("file:src/a.ts"), inv_file("src/b.ts"), inv_symbol()]),
    ))
    # ordinary file first-party unique join (non-exact-id): payload file:src/a.ts, inventory src/a.ts
    ordinary = catch_key(lambda: M.admit_provider_attribution_return(
        envelope([sidecar(fid, "file:src/a.ts", evaluation="src/a.ts")]),
        facts={fid: imports_fact(fid, "file:src/a.ts")},
        **kw(inventories=[inv_file("src/a.ts"), inv_symbol()]),
    ))
    missing_join = catch_key(lambda: M.admit_provider_attribution_return(
        envelope([sidecar(fid, "file:src/a.ts", evaluation="src/missing.ts")]),
        facts={fid: imports_fact(fid, "file:src/a.ts")},
        **kw(inventories=[inv_file("src/a.ts"), inv_symbol()]),
    ))
    holds = (
        conflict.get("raised") is True and conflict.get("key") == "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT"
        and agree.get("raised") is False and agree.get("status") == "admitted"
        and ordinary.get("raised") is False and ordinary.get("status") == "admitted"
        and missing_join.get("raised") is True and missing_join.get("key") == "TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY"
    )
    rec(
        "P-C15-UNIQUE-JOIN",
        "C15 refuses contradictory first-party identity; unique inventory join and unknown-sidecar ephemeral remain",
        True,
        {
            "conflict": conflict,
            "agreement": agree,
            "ordinary_file_first_party": ordinary,
            "missing_inventory_join": missing_join,
        },
        "fact",
        "C15 does not skip first-party unique inventory join. Ordinary non-exact-id file first-party still admits.",
        author_claim_holds=holds,
    )


def probe_atom_c15_unknown_true():
    fid = fact2("1")
    try:
        r = AM.evaluate_atom(
            {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
             "endpoint": "target", "filters": []},
            {"universe": U1, "kind": "file", "nativeSubjectId": "file:src/a.ts"},
            {
                "planId": PLAN,
                "facts": {fid: imports_fact(fid, "file:src/a.ts")},
                "inventories": [inv_file("file:src/a.ts"), inv_symbol()],
                "enumerationPlan": plan_one(),
                "closures": {C_PROV: {"kind": "provider"}},
                "targetAttributions": {fid: sidecar(fid, "file:src/a.ts", kind="unknown", occupancy="unknown")},
                "scopes": {}, "coverages": {}, "imports": {}, "importPayloads": {},
                "importObservations": {}, "planSelectedImportIds": [], "evaluationInputRefs": [],
                "incomingSearchAttestations": [], "universeDomains": {U1: "native.semantic-universe.typescript.v2"},
                "importScopeAdapter": "normalized-import-scope-descriptor",
            },
        )
        rec("P-C15-UNKNOWN-EPH", "Unknown sidecar keeps independently known ephemeral first-party match",
            True, {"atom": r}, "fact", author_claim_holds=r.get("value") == "true")
    except Exception as exc:  # noqa: BLE001
        rec("P-C15-UNKNOWN-EPH", "Unknown sidecar keeps independently known ephemeral first-party match",
            False, {"error": f"{type(exc).__name__}: {exc}"}, "fact", author_claim_holds=False)


def probe_syntactic_rung_and_unknown_fact_and_atomic():
    fid = fact2("1")
    extra = fact2("9")
    syn = catch_key(lambda: M.admit_provider_attribution_return(
        envelope([sidecar(fid, "file:src/a.ts", evaluation="src/a.ts")]),
        facts={fid: imports_fact(fid, resolution="syntactic-specifier")},
        **kw(),
    ))
    unknown = catch_key(lambda: M.admit_provider_attribution_return(
        envelope([sidecar(extra, "file:src/a.ts", evaluation="src/a.ts")]),
        facts={fid: imports_fact(fid)},
        **kw(),
    ))
    mixed = catch_key(lambda: M.admit_provider_attribution_return(
        envelope([
            sidecar(fid, "file:src/a.ts", evaluation="src/a.ts"),
            sidecar(extra, "file:src/b.ts", evaluation="src/b.ts"),
        ]),
        facts={fid: imports_fact(fid)},
        **kw(),
    ))
    holds = (
        syn.get("raised") is True and syn.get("key") == "TARGET_ATTRIBUTION_FIELD_NOT_ON_RUNG"
        and unknown.get("raised") is True and unknown.get("key") == "PROVIDER_RETURN_UNKNOWN_FACT"
        and mixed.get("raised") is True and mixed.get("key") == "PROVIDER_RETURN_UNKNOWN_FACT"
    )
    rec(
        "P-RUNG-UNKNOWN-ATOMIC",
        "Syntactic rung, unknown fact, and mixed valid+unknown refuse without capture",
        True,
        {"syntactic": syn, "unknown_fact": unknown, "mixed_atomic": mixed},
        "fact",
        "All-or-nothing: mixed valid+unknown raises before hostDerivedRefs is returned.",
        author_claim_holds=holds,
    )


def probe_public_routes_owner_registry():
    routes = FAULT_SCHEMA["x-opensip-routes"]
    codes = set(COMMON["$defs"]["DomainDetailCode"]["enum"])
    internal = list(M.SCHEMA_KEYS) + list(M.JOIN_KEYS)
    leaked = [k for k in internal if k in codes]
    d9ish = [k for k in internal if k.startswith("D9") or k.startswith("EVALUATION.TARGET")]
    schema_route = routes.get("input-schema-invalid:provider-return")
    join_route = routes.get("input-join-invalid:provider-return")
    host_join = routes.get("input-join-invalid:host-internal")
    host_schema = routes.get("input-schema-invalid:host-internal")
    native_map = FAULT_SCHEMA.get("x-opensip-native-origin-map") or {}
    holds = (
        isinstance(schema_route, dict)
        and schema_route.get("detail") == "EVALUATION.INPUT_REFUSED"
        and schema_route.get("termination", {}).get("errorCode") == "PROVIDER.PROTOCOL_VIOLATION"
        and join_route.get("detail") == "EVALUATION.INPUT_REFUSED"
        and host_join.get("detail") == "HOST.INVARIANT_VIOLATED"
        and host_schema.get("detail") == "HOST.INVARIANT_VIOLATED"
        and "EVALUATION.INPUT_REFUSED" in codes
        and "HOST.INVARIANT_VIOLATED" in codes
        and not leaked
        and not d9ish
        and M.ROUTE_LAW.get("liveD9") == "not discharged"
        and native_map.get("provider-return") == "producer-boundary"
    )
    rec(
        "P-PUBLIC-ROUTE-OWNER",
        "Public EVALUATION.INPUT_REFUSED / HOST.INVARIANT_VIOLATED routes exist in owner registry; no new D9/detail aliases",
        True,
        {
            "input-schema-invalid:provider-return": schema_route,
            "input-join-invalid:provider-return": join_route,
            "input-join-invalid:host-internal": host_join,
            "input-schema-invalid:host-internal": host_schema,
            "native_origin_map_provider-return": native_map.get("provider-return"),
            "EVALUATION.INPUT_REFUSED_in_DomainDetailCode": "EVALUATION.INPUT_REFUSED" in codes,
            "HOST.INVARIANT_VIOLATED_in_DomainDetailCode": "HOST.INVARIANT_VIOLATED" in codes,
            "internal_keys_leaked": leaked,
            "invented_d9_or_eval_target": d9ish,
            "route_law": M.ROUTE_LAW,
        },
        "fact",
        author_claim_holds=holds,
    )


def probe_isolation_contracts():
    ts = DELIVERY["typescriptSemanticSubstrate"]
    rust = DELIVERY["rustSemanticSubstrate"]
    def walk(obj, acc):
        if isinstance(obj, dict):
            if "closedWorkerToHostFrames" in obj:
                acc["closedWorkerToHostFrames"] = obj["closedWorkerToHostFrames"]
            if "oneAnalyzePerWorker" in obj:
                acc["oneAnalyzePerWorker"] = obj["oneAnalyzePerWorker"]
            if "retainAfterTerminal" in obj:
                acc["retainAfterTerminal"] = obj["retainAfterTerminal"]
            if "residentWorker" in obj:
                acc["residentWorker"] = obj["residentWorker"]
            for v in obj.values():
                walk(v, acc)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, acc)
    found = {}
    walk(DELIVERY, found)
    rpp_ident = RPP.get("protocolIdentity", {})
    rec(
        "P-ISOLATION-CONTRACTS",
        "Original native worker is a one-shot child; closed worker-to-host frames are FactBatch/Coverage/terminals only",
        True,
        {
            "ts_executionBoundary": ts.get("executionBoundary"),
            "ts_process": ts.get("processModel"),
            "rust_processModel": rust.get("processModel"),
            "delivery_walk": found,
            "rpp_transport": rpp_ident.get("transport"),
            "rpp_oneAnalyzePerChild": rpp_ident.get("oneAnalyzePerChild"),
            "rpp_residentSession": rpp_ident.get("residentSession"),
            "native_96_claims_not_a_wire_frame": "### 9.6 Host-adapter attribution return (not a wire frame)" in NATIVE,
            "native_occupancy_not_worker_product": "Occupancy mapping is\nnot a compiler-worker product" in NATIVE or "not a compiler-worker product" in NATIVE,
            "model_is_design_reference": M.__doc__.splitlines()[0] if M.__doc__ else None,
            "sourceFactId_is_fact2": SCHEMA["properties"]["records"]["items"]["properties"]["sourceFactId"]["pattern"].startswith("^fact2:"),
        },
        "must-operand",
        "Wrapper table lives at SubjectIdV1 encoding time inside the worker. fact2 exists only after host mint. Closed wire returns FactBatch.",
        author_claim_holds=False,
    )


def probe_reconcile_signature():
    sig = str(inspect.signature(AM._reconcile_attribution))
    join_sig = str(inspect.signature(AM._join_sidecar))
    occ_sig = str(inspect.signature(AM._admit_provider_occupancy_conflicts))
    rec(
        "P-RECONCILE-SIGNATURE",
        "Shared atom reconciliation/_join_sidecar/_occupancy-conflict signatures remain (query fix can consume them)",
        True,
        {
            "_reconcile_attribution": sig,
            "_join_sidecar": join_sig,
            "_admit_provider_occupancy_conflicts": occ_sig,
            "c15_in_join": "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT" in ATOM_SRC,
            "c15_absent_from_predecessor_join": "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT" not in PRED_ATOM_SRC,
        },
        "fact",
        author_claim_holds=(
            sig.startswith("(fact") and "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT" in ATOM_SRC
            and "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT" not in PRED_ATOM_SRC
        ),
    )


def probe_query_does_not_call_reconcile():
    q = (WORKFLOWS / "query_projection_model.v3.py").read_text(encoding="utf-8")
    rec(
        "P-QUERY-RAW-SIDECAR",
        "Query projection model still reads raw sidecar occupancy; does not call _reconcile_attribution",
        True,
        {
            "calls_reconcile": "_reconcile_attribution" in q,
            "calls_join_sidecar": "_join_sidecar" in q,
            "schemaVersion_1_omit": 'schemaVersion") == 1' in q,
            "prose_updated_to_v2_return": "ProviderTargetAttributionReturnV2" in (WORKFLOWS / "query-projection-contract.v3.md").read_text(encoding="utf-8"),
        },
        "advisory-operand",
        "Separately pending query fix; signature compatibility only. Do not treat prose update as query integration.",
        author_claim_holds=("_reconcile_attribution" not in q),
    )


def probe_envelope_not_digest_domain():
    ident = SCHEMA.get("x-opensip-identity", {})
    ids = json.loads((FOUND / "identity-schemas.v3.json").read_text(encoding="utf-8"))
    by = (((ids.get("x-opensip-digest-domains") or {}).get("byDomain")) or {})
    holds = (
        ident.get("digest") is None
        and "provider-target-attribution-return" not in json.dumps(by)
        and by.get("target-attribution") is not None
        and (by.get("target-attribution") or {}).get("record", {}).get("document")
        == "foundation/target-attribution.schema.v2.json"
    )
    rec(
        "P-NOT-DIGEST-DOMAIN",
        "Return envelope is not registered as an identity digest domain; captured domain remains target-attribution",
        True,
        {
            "x-opensip-identity": ident,
            "byDomain_has_target-attribution": "target-attribution" in by,
            "target-attribution_record": by.get("target-attribution"),
            "return_schema_in_byDomain": any(
                "provider-target-attribution-return" in json.dumps(v) for v in by.values()
            ) if by else False,
        },
        "fact",
        author_claim_holds=holds,
    )


def probe_frozen24_untouched_attribution_v1():
    v1 = FROZEN / "docs/coop/design-corrections/foundation/target-attribution.schema.v1.json"
    exists = v1.is_file()
    doc = json.loads(v1.read_text(encoding="utf-8")) if exists else {}
    rec(
        "P-FROZEN24-V1-RETAINED",
        "Frozen24 still owns TargetAttributionV1; this successor does not rewrite frozen24",
        exists and doc.get("$id") == "opensip.product.target-attribution.1",
        {"exists": exists, "$id": doc.get("$id"), "bytes": v1.stat().st_size if exists else None},
        "fact",
        author_claim_holds=exists and doc.get("$id") == "opensip.product.target-attribution.1",
    )


def probe_failed_capture_nothing():
    fid = fact2("1")
    try:
        M.admit_provider_attribution_return(
            envelope([sidecar(fid, "file:src/a.ts", evaluation="src/b.ts")]),
            facts={fid: imports_fact(fid)},
            **kw(inventories=[inv_file("file:src/a.ts"), inv_file("src/b.ts"), inv_symbol()]),
        )
        rec("P-FAILED-CAPTURE", "Refused envelope captures nothing", True, {"admitted": True}, "fact",
            author_claim_holds=False)
    except M.ProviderReturnAdmissionError as exc:
        rec("P-FAILED-CAPTURE", "Refused envelope captures nothing", True,
            {"key": exc.key, "no_return_value": True}, "fact", author_claim_holds=True)


def probe_missing_vs_empty():
    fid = fact2("1")
    omitted = M.admit_provider_attribution_return(None, facts={fid: imports_fact(fid)}, **kw())
    empty = M.admit_provider_attribution_return(envelope([]), facts={fid: imports_fact(fid)}, **kw())
    rec(
        "P-MISSING-VS-EMPTY",
        "Missing envelope is omitted; present empty records is admitted incomplete",
        omitted["status"] == "omitted" and empty["status"] == "admitted" and not omitted["hostDerivedRefs"] and not empty["hostDerivedRefs"],
        {"omitted": {k: omitted[k] for k in ("status", "hostDerivedRefs", "records")},
         "empty": {k: empty[k] for k in ("status", "hostDerivedRefs", "records")}},
        "fact",
        author_claim_holds=(
            omitted["status"] == "omitted" and empty["status"] == "admitted"
            and not omitted["hostDerivedRefs"] and not empty["hostDerivedRefs"]
        ),
    )


def probe_selected_views_absent():
    params = inspect.signature(M.admit_provider_attribution_return).parameters
    rec(
        "P-SELECTED-VIEWS-ABSENT",
        "Return admit has no selected-views operand; V2 join law requires fact in a selected view of producerClosure",
        True,
        {
            "admit_params": list(params),
            "v2_joins": V2_SCHEMA["x-opensip-join-law"]["joins"],
            "execution_inputs_later_join": "the fact MUST appear in a selected view" in EXEC_MD,
        },
        "must-operand",
        "Later execution-inputs admit joins selected views if captured refs are in selectedRefs. Return admit does not.",
        author_claim_holds=False,
    )


def main() -> int:
    probe_author_controls_are_labeled_boundary()
    probe_no_build_or_table_type()
    probe_schema_does_not_nest_v2()
    probe_stage_is_caller_echo()
    probe_producer_not_plan_selected()
    probe_host_internal_captures()
    probe_c15_and_unique_join()
    probe_atom_c15_unknown_true()
    probe_syntactic_rung_and_unknown_fact_and_atomic()
    probe_public_routes_owner_registry()
    probe_isolation_contracts()
    probe_reconcile_signature()
    probe_query_does_not_call_reconcile()
    probe_envelope_not_digest_domain()
    probe_frozen24_untouched_attribution_v1()
    probe_failed_capture_nothing()
    probe_missing_vs_empty()
    probe_selected_views_absent()
    report = {
        "standing": "Independent Grok coauthor-peer probes of source58 bytes. Not suite integration. Not source-pin seal. Not full Run. Not whole-design approval of 18 helper controls. Helper preconditions are schema/atom/capture controls with fullRun false.",
        "python": PY,
        "successor": str(SUCC),
        "output_dir": str(HERE),
        "probe_count": len(PROBES),
        "probes_ran_ok": all(p["ok"] for p in PROBES),
        "author_claims_that_hold": [p["id"] for p in PROBES if p.get("author_claim_holds") is True],
        "author_claims_that_fail": [p["id"] for p in PROBES if p.get("author_claim_holds") is False],
        "probes": PROBES,
    }
    out = HERE / "independent-probe-results.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(out), "probe_count": len(PROBES)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
