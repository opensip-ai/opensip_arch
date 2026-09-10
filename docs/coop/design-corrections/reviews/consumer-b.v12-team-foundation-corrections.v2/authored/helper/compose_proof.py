"""Independent complete-proof construction from admitted selected inputs.

evaluator-composition-contract.v3.md §§2–5, §7. Does not read claimed
findings, witnesses, or verdicts to choose subjects, truth, or output IDs.
"""
from __future__ import annotations

import hashlib
from typing import Any

from helper.canonical import C
from helper.evaluator import flatten, walk_predicate
from helper.identity import typed_id
from helper.store import Store


SEV_RANK = {"note": 0, "warning": 1, "error": 2}


def sort_set(xs: list) -> list:
    return sorted(xs, key=lambda x: C(x))


def digest_of(obj: Any) -> str:
    return hashlib.sha256(C(obj)).hexdigest()


def put_canonical(store: Store | None, obj: Any, *, label: str = "") -> str:
    d = digest_of(obj)
    if store is not None:
        got = store.put_canonical(obj, label=label)
        if got != d:
            raise RuntimeError(f"canonical digest drift {label}: {got} != {d}")
    return d


def select_file_subjects(*, inventories: list[dict], universe: str, store: Store | None) -> list[dict]:
    """Union file rows across complete file inventories for one universe."""
    seen: dict[tuple, dict] = {}
    for inv in inventories:
        if inv["kind"] != "file" or inv["state"] != "complete":
            continue
        for row in inv["rows"]:
            key = (universe, "file", row["nativeSubjectId"])
            subj = {
                "schemaVersion": 3,
                "universe": universe,
                "kind": "file",
                "nativeSubjectId": row["nativeSubjectId"],
            }
            sid = typed_id("evaluation-subject", subj)
            if store is not None:
                rec = store.put_h("evaluation-subject", subj, label=f"subject-{row['nativeSubjectId']}")
                if rec["typedId"] != sid:
                    raise RuntimeError("subject identity drift")
            seen[key] = {"id": sid, "record": subj, "row": row, "inventory": inv}
    return [seen[k] for k in sorted(seen, key=lambda t: C(list(t)))]


def rule_gates(rule: dict, policy: dict) -> bool:
    if not rule.get("enabled", True):
        return False
    if not rule.get("gate", False):
        return False
    return SEV_RANK[rule["severity"]] >= SEV_RANK[policy["gateSeverityAtLeast"]]


def compose_sealed_verdict(rule_results: list[dict], execution_deficiencies: list) -> str:
    """Composition §5: any gating fail wins; else indeterminate; else pass."""
    if any(r["outcome"] == "fail" for r in rule_results):
        return "fail"
    if any(r["outcome"] == "indeterminate" for r in rule_results) or execution_deficiencies:
        return "indeterminate"
    return "pass"


CAUSE_ENUM = {
    "input-closure-incomplete",
    "language-tier-unsupported",
    "required-cell-unsatisfied",
    "required-relation-missing",
    "resolution-incomplete",
    "coverage-unknown",
    "incomplete-inventory",
    "provider-unavailable",
}


def deficiencies_from_cell_outcomes(execution_inputs: dict) -> list[dict]:
    """Required unsatisfied cells become executionDeficiencies (composition §5)."""
    out = []
    for o in execution_inputs.get("cellOutcomes") or []:
        if not o.get("required"):
            continue
        if o.get("state") == "complete":
            continue
        cause = o.get("deficiency")
        if cause not in CAUSE_ENUM:
            cause = "required-cell-unsatisfied"
        refs = sort_set([{"domain": "subject-inventory", "digest": d} for d in o.get("inventoryDigests") or []])
        out.append(
            {
                "source": "native",
                "cause": cause,
                "subjectId": None,
                "predicateId": None,
                "inputRefs": refs,
                "evidenceKind": None,
                "nativeCause": o.get("nativeCause"),
                "universe": o.get("universe"),
            }
        )
    return sort_set(out)


def compose_expected_proof(
    *,
    plan_id: str,
    execution_plan_id: str,
    evaluator_closure: str,
    policy: dict,
    policy_digest: str,
    rule_program: dict,
    rule_program_digest: str,
    execution_inputs: dict,
    execution_inputs_digest: str,
    subjects: list[dict],
    facts: list[dict],
    payloads: dict,
    coverages: list[dict],
    view_digest: str,
    file_scope_id: str,
    file_inventories: list[dict],
    store: Store | None,
) -> dict:
    """Construct the complete expected proof-bundle record from admitted inputs."""
    pred_proofs: list[dict] = []
    all_finding_ids: list[str] = []
    rule_results: list[dict] = []

    policy_rules = {r["ruleId"]: r for r in policy["rules"]}
    for rp_rule in rule_program["rules"]:
        rule_id = rp_rule["ruleId"]
        pol_rule = policy_rules[rule_id]
        atom = rp_rule["emitWhen"]
        inventory_refs = sort_set(
            [{"domain": "subject-inventory", "digest": digest_of(inv)} for inv in file_inventories]
        )
        selected_ids = sort_set([s["id"] for s in subjects])
        enum_state = "complete"
        if not pol_rule.get("enabled", True):
            rule_results.append(
                {
                    "ruleId": rule_id,
                    "enumeration": {
                        "state": "disabled",
                        "inventoryRefs": [],
                        "selectedSubjectIds": [],
                        "unresolvedSubjectIds": [],
                        "incompleteInventoryRefs": [],
                    },
                    "outcome": "disabled",
                    "findingIds": [],
                    "deficiencies": [],
                }
            )
            continue
        rule_finding_ids: list[str] = []
        root_values: list[str] = []
        for subj in subjects:
            tree = walk_predicate(
                atom,
                prefix="p",
                subject=subj["record"],
                facts=facts,
                coverages=coverages,
                payloads=payloads,
            )
            root_values.append(tree["value"])
            nodes = flatten(tree)
            for n in nodes:
                prog_pred = {
                    "schemaVersion": 2,
                    "ruleProgramDigest": rule_program_digest,
                    "ruleId": rule_id,
                    "predicateId": n["predicateId"],
                    "operation": n["operation"],
                    "nodeDigest": hashlib.sha256(C(n["node"])).hexdigest(),
                }
                pp_d = put_canonical(store, prog_pred, label=f"program-predicate-{n['predicateId']}")
                w = {
                    "schemaVersion": 3,
                    "programPredicateDigest": pp_d,
                    "matchingFactIds": sort_set(list(n.get("matchingFactIds") or [])),
                    "coverageIds": sort_set(list(n.get("coverageIds") or [])),
                    "countLimit": None,
                    "childPredicateIds": sort_set([c["predicateId"] for c in n.get("children") or []]),
                    "matchingImportRows": [],
                    "uncertainFactIds": [],
                    "uncertainImportRows": [],
                    "deficiencies": list(n.get("deficiencies") or []),
                    "kind": n["kind"],
                }
                wd = put_canonical(store, w, label=f"witness-{n['predicateId']}")
                used_cov = []
                for cid in n.get("coverageIds") or []:
                    hex_d = cid.split(":", 1)[1] if ":" in cid else cid
                    used_cov.append({"domain": "coverage", "digest": hex_d})
                pred_proofs.append(
                    {
                        "ruleId": rule_id,
                        "subjectId": subj["id"],
                        "predicateId": n["predicateId"],
                        "operation": n["operation"],
                        "inputRefs": sort_set(
                            [
                                {"domain": "view", "digest": view_digest},
                                {"domain": "rule-program", "digest": rule_program_digest},
                            ]
                            + used_cov
                        ),
                        "scopeIds": sort_set([file_scope_id]),
                        "value": n["value"],
                        "witnessDigest": wd,
                    }
                )
            # Finding emission: emitWhen true → one finding3. This pilot's none-of-file is false.
            if tree["value"] == "true":
                raise RuntimeError("finding emission not exercised on this syntax-code pilot (emitWhen was true)")
        pred_proofs = sorted(
            pred_proofs,
            key=lambda x: (x["ruleId"].encode(), x["subjectId"].encode(), x["predicateId"].encode()),
        )
        live_findings = list(rule_finding_ids)
        gating = rule_gates(pol_rule, policy)
        if live_findings and gating:
            outcome = "fail"
        elif enum_state != "complete" or any(v == "indeterminate" for v in root_values):
            outcome = "indeterminate" if gating else "pass"
        else:
            outcome = "pass"
        rule_results.append(
            {
                "ruleId": rule_id,
                "enumeration": {
                    "state": enum_state,
                    "inventoryRefs": inventory_refs,
                    "selectedSubjectIds": selected_ids,
                    "unresolvedSubjectIds": [],
                    "incompleteInventoryRefs": [],
                },
                "outcome": outcome,
                "findingIds": sort_set(live_findings),
                "deficiencies": [],
            }
        )
        all_finding_ids.extend(live_findings)

    rule_results = sorted(rule_results, key=lambda r: r["ruleId"].encode())
    execution_deficiencies = list(execution_inputs.get("_executionDeficiencies") or [])
    if not execution_deficiencies:
        execution_deficiencies = deficiencies_from_cell_outcomes(execution_inputs)
    verdict = compose_sealed_verdict(rule_results, execution_deficiencies)
    # enumeration-contract.v1.md §7: evaluationInputRefs = selectedRefs + this manifest's execution-inputs reference.
    eval_input_refs = sort_set(
        list(execution_inputs["selectedRefs"])
        + [{"domain": "execution-inputs", "digest": execution_inputs_digest}]
    )
    proof = {
        "schemaVersion": 3,
        "planId": plan_id,
        "executionPlanId": execution_plan_id,
        "evaluatorClosure": evaluator_closure,
        "ruleProgramDigest": rule_program_digest,
        "evaluationInputRefs": eval_input_refs,
        "predicateProofs": pred_proofs,
        "findingIds": sort_set(all_finding_ids),
        "verdict": verdict,
        "evaluationState": "evaluated",
        "ruleResults": rule_results,
        "waivedFindingIds": [],
        "executionDeficiencies": execution_deficiencies,
        "executionInputsDigest": execution_inputs_digest,
    }
    return proof
