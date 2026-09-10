"""ExecutionInputsV1 selected-ref totality, native-account derivation, derive_outcome.

Owners: execution-inputs-contract.v1.md §§1,4,5,7 and execution-inputs.schema.v1.json.
Host cannot mint a complete semantic by asserting the row: state is derived,
then joined to the host CellProgramOutcomeV1.
"""
from __future__ import annotations

from typing import Any

from helper.canonical import C
from helper.errors import AdmissionError

FORBIDDEN_SELECTED_DOMAINS = {
    "proof-bundle",
    "finding",
    "evaluation-seal",
    "run",
    "semantic-evidence",
    "execution-inputs",
}
BLOB_INPUT_DOMAINS = {
    "subject-inventory",
    "candidate-producer-result",
    "target-attribution",
    "incoming-search",
}
STAGE_PRODUCED_DOMAINS_REFERENCE = {"view"}
INAPPLICABLE_ACCOUNT_STATES = {
    "inapplicable-vcs",
    "unsupported-typed",
    "unavailable-unselected",
    "unavailable-null-universe",
}


def sort_set(xs: list) -> list:
    return sorted(xs, key=lambda x: C(x))


def selected_refs_totality(
    *,
    complete_receipt_output_refs: list[dict],
    views: list[dict],
    cell_outcomes: list[dict],
    plan_import_ids: list[str],
    host_derived_refs: list[dict],
) -> list[dict]:
    """Exact totality, not a subset (contract §1)."""
    refs: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(domain: str, digest: str) -> None:
        key = (domain, digest)
        if key in seen:
            return
        seen.add(key)
        refs.append({"domain": domain, "digest": digest})

    for r in complete_receipt_output_refs:
        if r["domain"] in FORBIDDEN_SELECTED_DOMAINS:
            raise AdmissionError("EXECUTION_INPUTS_SELECTED_COVER", r["domain"])
        add(r["domain"], r["digest"])
    for view in views:
        for cid in view.get("coverageIds") or []:
            hex_d = cid.split(":", 1)[1] if ":" in cid else cid
            add("coverage", hex_d)
    for outcome in cell_outcomes:
        for d in outcome.get("inventoryDigests") or []:
            add("subject-inventory", d)
        cand = outcome.get("candidateResultDigest")
        if cand:
            add("candidate-producer-result", cand)
    for iid in plan_import_ids:
        hex_d = iid.split(":", 1)[1] if ":" in iid else iid
        add("import", hex_d)
    for r in host_derived_refs:
        if r["domain"] in BLOB_INPUT_DOMAINS:
            add(r["domain"], r["digest"])
    return sort_set(refs)


def blob_selected_equals_host_derived(selected_refs: list[dict], host_derived_refs: list[dict]) -> bool:
    a = sort_set([r for r in selected_refs if r["domain"] in BLOB_INPUT_DOMAINS])
    b = sort_set([r for r in host_derived_refs if r["domain"] in BLOB_INPUT_DOMAINS])
    return a == b


def derive_account(
    *,
    account: dict,
    matching_coverage_entries: list[dict],
) -> dict:
    """Contract §5: derive completeness from ALL matching CoverageResultV3 entries."""
    applicability = account["applicability"]
    named = list(account.get("coverageIds") or [])
    matching_ids = []
    for e in matching_coverage_entries:
        d = e["digest"]
        matching_ids.append(d)
    matching_ids = sort_set(matching_ids)
    named_sorted = sort_set(named)
    derived = {
        "applicability": applicability,
        "namedCoverageIds": named_sorted,
        "matchingCoverageIds": matching_ids,
        "derivedCoverage": None,
        "accountComplete": False,
        "nativeWorkIncomplete": False,
        "deficiency": None,
        "nativeCause": None,
    }
    if applicability in INAPPLICABLE_ACCOUNT_STATES:
        if named:
            raise AdmissionError(
                "EXECUTION_INPUTS_COVERAGE_DERIVE",
                f"{applicability} must have empty coverageIds",
            )
        derived["accountComplete"] = True
        derived["derivedCoverage"] = None
        return derived
    if applicability != "supported-available":
        raise AdmissionError("EXECUTION_INPUTS_COVERAGE_DERIVE", applicability)
    if named_sorted != matching_ids:
        raise AdmissionError(
            "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY",
            f"coverageIds {named_sorted} != matching partitions {matching_ids}",
        )
    if not named_sorted:
        derived["nativeWorkIncomplete"] = True
        derived["accountComplete"] = False
        derived["derivedCoverage"] = None
        return derived
    states = [e["entry"]["coverage"] for e in matching_coverage_entries]
    if any(s != "complete" for s in states):
        derived["accountComplete"] = False
        derived["derivedCoverage"] = "unknown" if "unknown" in states else "partial"
        return derived
    derived["accountComplete"] = True
    derived["derivedCoverage"] = "complete"
    return derived


def derive_outcome(
    *,
    enumerator_status: str,
    universe: str | None,
    inventories: list[dict],
    derived_accounts: list[dict],
    candidate_state: str | None,
    candidate_owed: bool,
) -> dict:
    """Contract §4. Returns {state, deficiency, nativeCause}."""
    if enumerator_status == "unselected" or universe is None:
        return {
            "state": "unavailable",
            "deficiency": "provider-unavailable",
            "nativeCause": None,
            "reason": "enumerator-unselected-or-null-universe",
        }
    inv_states = [i["state"] for i in inventories]
    if any(s == "unavailable" for s in inv_states) and not any(
        s in ("complete", "partial") for s in inv_states
    ):
        return {
            "state": "unavailable",
            "deficiency": inventories[0].get("deficiency") if inventories else "provider-unavailable",
            "nativeCause": inventories[0].get("nativeCause") if inventories else None,
            "reason": "selected-provider-unavailable-no-work",
        }
    if any(s == "partial" for s in inv_states):
        src = next(i for i in inventories if i["state"] == "partial")
        return {
            "state": "partial",
            "deficiency": src.get("deficiency"),
            "nativeCause": src.get("nativeCause"),
            "reason": "inventory-partial",
        }
    for acc in derived_accounts:
        if acc["applicability"] == "supported-available" and not acc["accountComplete"]:
            return {
                "state": "partial",
                "deficiency": "required-relation-missing" if acc.get("nativeWorkIncomplete") else "resolution-incomplete",
                "nativeCause": None,
                "reason": "supported-available-account-not-complete",
            }
    if candidate_owed and candidate_state != "complete":
        return {
            "state": "partial" if candidate_state == "partial" else "unavailable",
            "deficiency": "provider-unavailable" if candidate_state != "partial" else None,
            "nativeCause": None,
            "reason": "candidate-owed-not-complete",
        }
    if any(s != "complete" for s in inv_states):
        raise AdmissionError("EXECUTION_INPUTS_OUTCOME_DERIVE", f"inventory states {inv_states}")
    return {"state": "complete", "deficiency": None, "nativeCause": None, "reason": "all-complete"}


def join_host_outcome(host_row: dict, derived: dict) -> None:
    if host_row["state"] != derived["state"]:
        raise AdmissionError(
            "EXECUTION_INPUTS_OUTCOME_DERIVE",
            f"host state {host_row['state']} != derived {derived['state']}",
        )
    if host_row["deficiency"] != derived["deficiency"] or host_row["nativeCause"] != derived["nativeCause"]:
        raise AdmissionError(
            "EXECUTION_INPUTS_CAUSE_CARRIER",
            f"host pair {(host_row['deficiency'], host_row['nativeCause'])} != derived "
            f"{(derived['deficiency'], derived['nativeCause'])}",
        )
    if derived["state"] == "complete" and any(
        False for _ in []
    ):
        pass


def matching_coverages_for_account(
    *,
    account: dict,
    view_coverages: list[dict],
    enumerator_closure: str,
    universe: str,
) -> list[dict]:
    """Owner CoverageResultV3 entries of this cell/program/returned-view/enumerator/U/pair."""
    out = []
    for c in view_coverages:
        rec = c["record"]
        payload = c["payload"]
        key = payload["key"]
        if rec.get("relation") and rec["relation"] != account["relation"]:
            continue
        if key["relation"] != account["relation"] or key["resolution"] != account["resolution"]:
            continue
        if key["sourceUniverse"] != universe or key["targetUniverse"] != universe:
            continue
        if account["sourceUniverse"] != universe or account["targetUniverse"] != universe:
            continue
        out.append(
            {
                "digest": c["digest"],
                "id": c.get("id"),
                "entry": payload["entry"],
                "key": key,
            }
        )
    return out


def expected_matrix_accounts(capability_id: str, matrix: dict) -> list[tuple[str, str]]:
    for cap in matrix.get("capabilities") or []:
        if cap["id"] == capability_id:
            return [(r[0], r[1]) for r in cap.get("relations") or []]
    raise AdmissionError("EXECUTION_INPUTS_KIND_MAP", capability_id)


def vcs_applicability(vcs: dict) -> str:
    if vcs.get("kind") == "none":
        return "inapplicable-vcs"
    return "supported-available"
