"""Shared current-law sealing of plan membership, execution-inputs, and expected proof.

Builders supply native observations, facts, coverages and inventories. This
module does not treat a previously saved proof as truth.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from helper.canonical import C
from helper.compose_proof import compose_expected_proof, select_file_subjects, sort_set
from helper.execution_inputs import (
    derive_account,
    derive_outcome,
    expected_matrix_accounts,
    join_host_outcome,
    matching_coverages_for_account,
    selected_refs_totality,
    vcs_applicability,
)
from helper.identity import typed_id
from helper.schema_admit import validate_against
from helper.store import Store

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-other-runs-corrections.v5/subject")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-other-runs-corrections.v5/output")
MATRIX = json.loads((KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json").read_text())
IDENT = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
EXEC = "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"
NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"


def rc_na(*, exhaustive: bool = True):
    return {
        "state": "not-applicable",
        "attempted": False,
        "examinedExhaustive": exhaustive,
        "stageTerminal": "complete",
        "unresolvedEdgeCount": 0,
        "unresolvedEdgeClasses": [],
    }


def closed_world():
    return {
        "exportsClosed": "unknown",
        "entryPointsRecognized": "none",
        "nonliteralLoading": "none",
        "externalConsumers": "unknown",
        "dynamicDispatch": "not-applicable",
        "reasons": [],
        "deadCodeRepairEligible": False,
    }


def mint_coverage(
    store: Store,
    *,
    scope_h: dict,
    relation: str,
    resolution: str,
    uni_hex: str,
    nsubj: int,
    native_schema_d: str,
    coverage: str = "complete",
    deficiency=None,
    native_cause=None,
    exhaustive: bool | None = None,
):
    if exhaustive is None:
        exhaustive = coverage == "complete"
    commit = "sha256:" + scope_h["digest"]
    key = {
        "relation": relation,
        "resolution": resolution,
        "sourceUniverse": uni_hex,
        "targetUniverse": uni_hex,
        "subjectScopeCommitment": commit,
    }
    entry = {
        "relation": relation,
        "resolution": resolution,
        "coverage": coverage,
        "examinedUniverse": {"subjectScopeCommitment": commit, "subjectCount": nsubj},
        "resolutionCompleteness": rc_na(exhaustive=exhaustive),
        "closedWorld": closed_world(),
        "derivationKinds": [],
        "confidenceMillionths": 1000000,
        "deficiency": deficiency,
        "nativeCause": native_cause,
    }
    payload = {"schemaVersion": 3, "key": key, "entry": entry}
    pd = store.put_canonical(payload, label=f"CoverageResultV3-{relation}")
    rec = {
        "schemaVersion": 2,
        "scopeId": scope_h["typedId"],
        "payloadSchemaDigest": native_schema_d,
        "payloadDigest": pd,
    }
    h = store.put_h("coverage", rec, label=f"coverage-{relation}")
    return h, rec, payload


def mint_scope(store: Store, *, snapshot_id, uni_hex, enumerator, relation, resolution, subjects):
    rec = {
        "schemaVersion": 2,
        "snapshotId": snapshot_id,
        "sourceUniverse": uni_hex,
        "targetUniverse": uni_hex,
        "relation": relation,
        "resolution": resolution,
        "enumeratorClosure": enumerator,
        "subjects": sorted(subjects),
    }
    return store.put_h("subject-scope", rec, label=f"scope-{relation}"), rec


def mint_inventory(
    store: Store,
    *,
    plan_id: str,
    enum_d: str,
    cell_ordinal: int,
    kind: str,
    rows: list,
    examined: list,
    state: str = "complete",
    deficiency=None,
    native_cause=None,
):
    rec = {
        "schemaVersion": 1,
        "planId": plan_id,
        "parameterDigest": enum_d,
        "cellOrdinal": cell_ordinal,
        "programOrdinal": 0,
        "kind": kind,
        "state": state,
        "deficiency": deficiency,
        "nativeCause": native_cause,
        "examinedPaths": sorted(examined),
        "rows": rows,
    }
    d = store.put_canonical(rec, label=f"sinv-{cell_ordinal}-{kind}")
    return d, rec


def plan_semantic_closures(*, provider, evaluator, detector, extras=None):
    xs = [provider, evaluator, detector] + list(extras or [])
    return sort_set(xs)


def close_execution_and_proof(
    store: Store,
    *,
    plan_id: str,
    exec_plan_id: str,
    ss_d: str,
    prov_c: str,
    eval_c: str,
    policy: dict,
    policy_d: str,
    rule_program: dict,
    rp_d: str,
    enum_d: str,
    as_d: str,
    uni_hex: str,
    language_mode: str,
    cells: list[dict],
    view: dict,
    view_h: dict,
    facts_for_eval: list,
    payloads: dict,
    coverages_full: list,
    inventories: list[tuple[str, dict]],
    nca: list[dict],
    vcs: dict,
    import_ids: list[str],
    file_scope_id: str,
    atom: dict,
    project_id: str,
    snapshot_id: str,
    cap_id: str,
    export_stem: str,
    extra_meta: dict,
    schema_checks: list,
):
    """Mint execution-inputs from derive_outcome, compose expected proof, export."""
    inv_by_d = {d: rec for d, rec in inventories}
    inv_refs = sort_set([{"domain": "subject-inventory", "digest": d} for d, _ in inventories])
    complete_output_refs = [{"domain": "view", "digest": view_h["digest"]}]
    host_cap = {
        "custody": "host-tcb-evidence-store",
        "observation": "stage-return",
        "stageReceipts": [
            {
                "ordinal": 0,
                "stageSpecDigest": ss_d,
                "producerClosure": prov_c,
                "outputDomains": ["view"],
                "outputRefs": sort_set(complete_output_refs),
                "state": "complete",
                "unavailableReason": None,
            }
        ],
        "hostDerivedRefs": inv_refs,
    }

    cell_outcomes = []
    derived_notes = []
    for i, cell in enumerate(cells):
        loc_invs = [
            (d, rec)
            for d, rec in inventories
            if rec["cellOrdinal"] == i and rec["programOrdinal"] == 0
        ]
        inv_recs = [rec for _, rec in loc_invs]
        accounts = [a for a in nca if a["cellOrdinal"] == i]
        derived_accounts = []
        for acc in accounts:
            matching = matching_coverages_for_account(
                account=acc,
                view_coverages=coverages_full,
                enumerator_closure=prov_c,
                universe=uni_hex,
            )
            derived_accounts.append(derive_account(account=acc, matching_coverage_entries=matching))
        candidate_owed = cell["capabilityId"] in ("clones-near", "clones-cross-tsjs")
        derived = derive_outcome(
            enumerator_status="selected",
            universe=uni_hex,
            inventories=inv_recs,
            derived_accounts=derived_accounts,
            candidate_state=None,
            candidate_owed=candidate_owed,
        )
        row = {
            "ordinal": i,
            "cellOrdinal": i,
            "programOrdinal": 0,
            "capabilityId": cell["capabilityId"],
            "languageMode": language_mode,
            "workspaceRoot": ".",
            "required": cell.get("required", True),
            "kinds": cell["kinds"],
            "universe": uni_hex,
            "enumeratorStatus": "selected",
            "enumeratorClosure": prov_c,
            "state": derived["state"],
            "deficiency": derived["deficiency"],
            "nativeCause": derived["nativeCause"],
            "stageOrdinal": 0 if derived["state"] != "unavailable" else None,
            "stageOrdinalNullReason": None if derived["state"] != "unavailable" else "unavailable-binding",
            "inventoryDigests": sort_set([d for d, _ in loc_invs]),
            "viewDigests": [view_h["digest"]],
            "candidateResultDigest": None,
        }
        join_host_outcome(row, derived)
        cell_outcomes.append(row)
        derived_notes.append({"ordinal": i, "capabilityId": cell["capabilityId"], "derived": derived})
        expected_pairs = set(expected_matrix_accounts(cell["capabilityId"], MATRIX))
        present = {(a["relation"], a["resolution"]) for a in accounts}
        if present != expected_pairs:
            raise RuntimeError(f"native coverage totality {cell['capabilityId']}: {present} != {expected_pairs}")

    selected_refs = selected_refs_totality(
        complete_receipt_output_refs=complete_output_refs,
        views=[view],
        cell_outcomes=cell_outcomes,
        plan_import_ids=import_ids,
        host_derived_refs=inv_refs,
    )
    exec_inputs = {
        "schemaVersion": 1,
        "planId": plan_id,
        "executionPlanId": exec_plan_id,
        "evaluatorClosure": eval_c,
        "enumerationPlanDigest": enum_d,
        "analysisSpecDigest": as_d,
        "hostCapture": host_cap,
        "selectedRefs": selected_refs,
        "cellOutcomes": cell_outcomes,
        "nativeCoverageAccounts": nca,
        "candidateResultRefs": [],
    }
    ei_d = store.put_canonical(exec_inputs, label="ExecutionInputsV1")

    file_invs = [rec for _, rec in inventories if rec["kind"] == "file"]
    subjects = select_file_subjects(inventories=file_invs, universe=uni_hex, store=store)
    proof = compose_expected_proof(
        plan_id=plan_id,
        execution_plan_id=exec_plan_id,
        evaluator_closure=eval_c,
        policy=policy,
        policy_digest=policy_d,
        rule_program=rule_program,
        rule_program_digest=rp_d,
        execution_inputs=exec_inputs,
        execution_inputs_digest=ei_d,
        subjects=subjects,
        facts=facts_for_eval,
        payloads=payloads,
        coverages=coverages_full,
        view_digest=view_h["digest"],
        file_scope_id=file_scope_id,
        file_inventories=[i for i in file_invs if i["state"] == "complete"],
        store=store,
    )
    proof_h = store.put_h("proof-bundle", proof, label="proof")
    evidence = {
        "schemaVersion": 3,
        "planId": plan_id,
        "viewIds": [view_h["typedId"]],
        "coverageIds": sort_set(list(view["coverageIds"])),
        "importIds": list(import_ids),
        "findingIds": [],
        "proofBundleId": proof_h["typedId"],
    }
    ev_h = store.put_h("semantic-evidence", evidence, label="evidence")
    seal = {
        "schemaVersion": 3,
        "planId": plan_id,
        "executionPlanId": exec_plan_id,
        "evidenceId": ev_h["typedId"],
        "evaluatorClosure": eval_c,
        "policyDigest": policy_d,
        "proofBundleId": proof_h["typedId"],
        "verdict": proof["verdict"],
    }
    seal_h = store.put_h("evaluation-seal", seal, label="seal")
    run = {
        "schemaVersion": 3,
        "projectId": project_id,
        "snapshotId": snapshot_id,
        "planId": plan_id,
        "evidenceId": ev_h["typedId"],
        "evaluationSealId": seal_h["typedId"],
        "capabilityManifestId": cap_id,
    }
    run_h = store.put_h("run", run, label="run")

    checks = list(schema_checks)
    for label, inst, rel, sel in [
        ("run", run, IDENT, "#/$defs/run"),
        ("proof", proof, IDENT, "#/$defs/proof-bundle"),
        ("exec_inputs", exec_inputs, EXEC, "#"),
        ("seal", seal, IDENT, "#/$defs/evaluation-seal"),
        ("evidence", evidence, IDENT, "#/$defs/semantic-evidence"),
        ("plan_check", None, IDENT, "#/$defs/plan"),
    ]:
        if inst is None:
            continue
        r = validate_against(inst, rel, selector=sel, label=label)
        checks.append({"label": label, "stockOk": r["stockOk"], "errors": r["errors"][:5]})

    export_path = OUT / "runs" / f"{export_stem}.store.json"
    store.export(export_path)
    replay_cmd = {
        "store": str(export_path),
        "command": "/tmp/opensip-architecture-review-env/bin/python -I -B " + str(OUT / "scripts/replay_from_export.py"),
        "args": [str(export_path)],
        "tamperArgs": ["--tamper", str(export_path)],
        "kind": "complete-expected-proof-from-admitted-inputs",
    }
    (OUT / "runs" / f"{export_stem}.replay-cmd.json").write_text(json.dumps(replay_cmd, indent=2) + "\n")
    meta = {
        "runId": run_h["typedId"],
        "planId": plan_id,
        "proofId": proof_h["typedId"],
        "verdict": proof["verdict"],
        "derivedCellOutcomes": derived_notes,
        "blobCount": len(store.blobs),
        "export": str(export_path),
        "schemaChecks": checks,
        **extra_meta,
    }
    (OUT / "runs" / f"{export_stem}.meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    failed = [c for c in checks if c.get("stockOk") is False]
    return {
        "runId": run_h["typedId"],
        "planId": plan_id,
        "proofId": proof_h["typedId"],
        "verdict": proof["verdict"],
        "ei_d": ei_d,
        "failed": failed,
        "derived": derived_notes,
        "proof": proof,
        "exec_inputs": exec_inputs,
    }
