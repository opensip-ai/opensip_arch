#!/usr/bin/env python3
"""Bounded independent probes of root integration delta after COMPLETE17 ACCEPT_SCOPED.

Helper probes using TCB-assumed owners/facts. Not compiler/OS/D9. Not whole launcher.
Python: /tmp/opensip-architecture-review-env/bin/python -I -B
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

PY = sys.executable
HERE = Path(__file__).resolve().parent
OVERLAY = HERE / "overlay"
FOUND = OVERLAY / "docs/coop/design-corrections/foundation"
NATIVE = OVERLAY / "docs/coop/design-corrections/native"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = _load("v5_return_model", FOUND / "provider_attribution_return_model.v2.py")
CHK = _load("v5_return_checker", FOUND / "check-provider-attribution-return.v2.py")
RETURN = json.loads((FOUND / "provider-target-attribution-return.schema.v2.json").read_text(encoding="utf-8"))
COMPANION = json.loads((NATIVE / "occupancy-companion.schema.v1.json").read_text(encoding="utf-8"))
ARRAY_SRC = (FOUND / "check-array-orders.py").read_text(encoding="utf-8")
MODEL_SRC = (FOUND / "provider_attribution_return_model.v2.py").read_text(encoding="utf-8")
QUERY_MD = (OVERLAY / "docs/coop/design-corrections/workflows/query-projection-contract.v3.md").read_text(encoding="utf-8")

PROBES = []


def rec(probe_id, title, ok, evidence, classification, notes=None, author_claim_holds=None):
    PROBES.append({
        "id": probe_id,
        "title": title,
        "ok": ok,
        "author_claim_holds": author_claim_holds,
        "classification": classification,
        "helper_only": True,
        "evidence": evidence,
        "notes": notes,
    })


def catch(fn):
    try:
        out = fn()
        return {"raised": False, "status": out.get("status") if isinstance(out, dict) else None,
                "key": None, "detail": None}
    except M.ProviderReturnAdmissionError as exc:
        return {"raised": True, "status": None, "key": exc.key, "detail": exc.detail}


def buffer(ordinals, companions, first=0, batch_index=0):
    args = CHK.owners(CHK.fact2("1"))
    args["dispatch"]["expectedFirstCandidateOrdinal"] = first
    args["dispatch"]["expectedBatchIndex"] = batch_index
    return M.buffer_fact_batch_occupancy(
        CHK.batch([CHK.candidate(o) for o in ordinals], companions, batch_index=batch_index),
        negotiated_tokens=args["negotiated_tokens"],
        dispatch=args["dispatch"],
    )


def probe_contiguous_stream():
    sparse_comp = catch(lambda: buffer([0, 1, 2], [CHK.companion(0), CHK.companion(2)]))
    in_batch_gap = catch(lambda: buffer([0, 2], []))
    later = catch(lambda: buffer([3, 4], [], first=3, batch_index=1))
    wrong_first = catch(lambda: buffer([3, 4], [], first=0, batch_index=0))
    first_batch_ok = catch(lambda: buffer([0, 1], []))
    rec(
        "P-CANDIDATE-STREAM",
        "Contiguous candidate stream: sparse companions OK; in-batch candidate gap refuses; later [3,4] OK; wrong first [3,4] refuses",
        True,
        {
            "sparse_companions_on_012": sparse_comp,
            "in_batch_gap_02": in_batch_gap,
            "later_batch_34_first_3": later,
            "wrong_first_34_expected_0": wrong_first,
            "first_batch_01": first_batch_ok,
            "stream_enforced_in_model": "list(range(first, first + len(ords)))" in MODEL_SRC,
        },
        "must-operand",
        "Helper TCB buffer path. Stream law is host join, not the candidateOrdinal array annotation.",
        author_claim_holds=(
            sparse_comp.get("status") == "buffered"
            and in_batch_gap.get("key") == "PROVIDER_RETURN_CANDIDATE_STREAM"
            and later.get("status") == "buffered"
            and wrong_first.get("key") == "PROVIDER_RETURN_CANDIDATE_STREAM"
            and first_batch_ok.get("status") == "buffered"
        ),
    )


def probe_stale_producersupply_gone():
    blob = json.dumps(RETURN)
    rec(
        "P-STALE-PRODUCERSUPPLY-GONE",
        "Advisory COMPLETE58 after-fact2-mint sentence removed; current wrapper is in-worker companion",
        True,
        {
            "after_fact2_mint": "After fact2 mint" in blob,
            "in_worker_companion": "In-worker wrapper emits OccupancyCompanionV1" in blob,
            "envelope_not_delivery": "not the worker channel" in blob.lower() or "not the worker channel" in json.dumps(RETURN.get("x-opensip-return-law", {})).lower(),
            "wrapper_text": RETURN["x-opensip-return-law"]["producerSupply"]["modes"]["ts-tsconfig / js-allowjs / js-synthesized"]["wrapper"],
        },
        "advisory-operand",
        author_claim_holds=("After fact2 mint" not in blob and "In-worker wrapper emits OccupancyCompanionV1" in blob),
    )


def probe_array_order_no_silent_skip():
    rec(
        "P-ARRAY-ORDER-NO-SKIP",
        "check-array-orders no longer silently skips missing explicit required schema paths",
        True,
        {
            "has_is_file_filter": "if p.is_file()" in ARRAY_SRC,
            "explicit_security_schema": "security-lifecycle.schemas.v1.json" in ARRAY_SRC,
            "native_glob": "(DC/'native').glob('*.json')" in ARRAY_SRC or 'DC/\'native\'' in ARRAY_SRC,
        },
        "fact",
        "Glob still only yields existing native schema files; explicit security path now raises if missing.",
        author_claim_holds="if p.is_file()" not in ARRAY_SRC,
    )


def probe_query_occupancy_law():
    rec(
        "P-QUERY-OCCUPANCY-INTEGRATION",
        "Query contract uses captured V2 projections of OccupancyCompanionV1; no payload-parse occupancy",
        True,
        {
            "companion_projection": "OccupancyCompanionV1 on negotiated FactBatchV3" in QUERY_MD,
            "no_parse": "MUST NOT parse" in QUERY_MD or "neither path parses payload spelling" in QUERY_MD,
        },
        "fact",
        "Not a re-audit of query/proof/closure. Occupancy-law consistency only.",
        author_claim_holds=(
            "OccupancyCompanionV1 on negotiated FactBatchV3" in QUERY_MD
            and "parses payload spelling" in QUERY_MD
        ),
    )


def probe_vocab_split():
    vocab = COMPANION["x-opensip-order-vocabulary"]["candidateOrdinal"]
    rec(
        "P-VOCAB-VS-STREAM",
        "candidateOrdinal annotation still allows gaps; contiguous stream is a separate host join",
        True,
        {"law": vocab.get("law"), "not": vocab.get("not"), "semanticJoin": vocab.get("semanticJoin")},
        "fact",
        author_claim_holds=("Gaps are lawful at this annotation" in vocab.get("law", "") and "separate host join" in vocab.get("not", "")),
    )


def main() -> int:
    probe_contiguous_stream()
    probe_stale_producersupply_gone()
    probe_array_order_no_silent_skip()
    probe_query_occupancy_law()
    probe_vocab_split()
    report = {
        "standing": "Bounded helper probes of root integration delta. TCB-assumed owners. Not 6-suite launcher. Not compiler/OS/D9.",
        "python": PY,
        "overlay": str(OVERLAY),
        "probe_count": len(PROBES),
        "probes_ran_ok": all(p["ok"] for p in PROBES),
        "author_claims_that_hold": [p["id"] for p in PROBES if p.get("author_claim_holds") is True],
        "author_claims_that_fail": [p["id"] for p in PROBES if p.get("author_claim_holds") is False],
        "helper_only_all": all(p.get("helper_only") for p in PROBES),
        "probes": PROBES,
    }
    out = HERE / "independent-probe-results.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "wrote": str(out),
        "hold": report["author_claims_that_hold"],
        "fail": report["author_claims_that_fail"],
        "helper_only_all": report["helper_only_all"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
