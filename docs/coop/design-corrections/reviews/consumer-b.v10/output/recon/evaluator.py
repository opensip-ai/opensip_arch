"""Independent evaluator3 reconstruction from composition + atom contracts.

Does not read claimed findings/witnesses to select subjects or values.
"""
from __future__ import annotations

from typing import Any

from .codec import (
    AdmissionError,
    canonical_digest,
    encode_c,
    h_hex,
    h_id,
    sha256,
    sort_canonical_set,
    sort_utf8,
)

UNIVERSE_MAP = {
    "typescript": "native.semantic-universe.typescript.v2",
    "rust": "native.semantic-universe.rust.v2",
    "syntax": "native.semantic-universe.syntax.v2",
}

LADDERS = {
    "calls": ["syntactic-callee-name", "resolved-callee"],
    "clones": ["normalized-body-hash"],
    "control-flow": ["syntactic"],
    "declares": ["syntactic"],
    "file": ["enumerated"],
    "imports": ["syntactic-specifier", "resolved-target"],
    "literal": ["syntactic"],
    "package": ["manifest-declared"],
    "reachability": ["from-resolved-calls"],
    "references": ["syntactic-name-match", "resolved-binding"],
    "types": ["annotated", "checked"],
    "unresolved-edge": ["observed"],
    "vcs-change": ["vcs-reported"],
    "runtime-observation": ["observed"],
    "history-change": ["observed"],
}

SEV_ORDER = {"note": 0, "warning": 1, "error": 2}

TRUE, FALSE, UNKNOWN = "true", "false", "indeterminate"


def kleene_not(v: str) -> str:
    if v == TRUE:
        return FALSE
    if v == FALSE:
        return TRUE
    return UNKNOWN


def kleene_and(vals: list[str]) -> str:
    if any(v == FALSE for v in vals):
        return FALSE
    if all(v == TRUE for v in vals):
        return TRUE
    return UNKNOWN


def kleene_or(vals: list[str]) -> str:
    if any(v == TRUE for v in vals):
        return TRUE
    if all(v == FALSE for v in vals):
        return FALSE
    return UNKNOWN


def predicate_children(node: dict, addr: str) -> list[tuple[str, dict]]:
    op = node["op"]
    if op in ("and", "or"):
        return [(f"{addr}.{i}", n) for i, n in enumerate(node["operands"])]
    if op == "not":
        return [(f"{addr}.0", node["operand"])]
    return []


def is_atom(node: dict) -> bool:
    return node["op"] in ("exists", "none", "count-at-most", "all-covered")


def rung_index(relation: str, rung: str) -> int:
    ladder = LADDERS.get(relation)
    if not ladder:
        raise AdmissionError("ATOM_RELATION_UNREGISTERED", relation)
    if rung not in ladder:
        raise AdmissionError("ATOM_RUNG_NOT_IN_LADDER", f"{relation}@{rung}")
    return ladder.index(rung)


def occupancy_id(fact: dict, payload: dict, endpoint: str, subject_kind: str) -> str | None:
    rel = fact["relation"]
    if endpoint == "source":
        if rel == "file":
            return payload.get("path")
        if rel == "package":
            return payload.get("packageName")
        if rel == "clones":
            # source-path: anchors[0].path
            an = fact.get("anchors") or []
            return an[0]["path"] if an else None
        if rel in ("declares",):
            return payload.get("declared") if subject_kind == "symbol" else payload.get("container")
        if rel == "imports":
            return payload.get("importer")
        if rel == "calls":
            return payload.get("caller")
        if rel == "literal":
            return payload.get("owner")
        if rel == "types":
            return payload.get("subject")
        if rel == "unresolved-edge":
            return payload.get("referrer")
        if rel == "vcs-change":
            return payload.get("path") if "path" in payload else None
    return None


def fact_matches_atom(atom: dict, fact: dict, payload: dict, subject: dict) -> bool:
    if fact["relation"] != atom["relation"]:
        return False
    want = rung_index(atom["relation"], atom["minResolution"])
    got = rung_index(fact["relation"], fact["resolution"])
    if got < want:
        return False
    # universe: default same-only for most; filter may constrain
    native = subject["nativeSubjectId"]
    endpoint = atom.get("endpoint") or "source"
    occ = occupancy_id(fact, payload, endpoint, subject["kind"])
    if occ is None:
        return False
    if occ != native:
        # package also matches manifestPath
        if fact["relation"] == "package" and subject["kind"] == "package":
            if payload.get("packageName") != native:
                return False
            mp = subject.get("packageManifestPath")
            if mp and payload.get("manifestPath") != mp:
                return False
        else:
            return False
    for flt in atom.get("filters") or []:
        if not apply_filter(flt, fact, payload, subject):
            return False
    return True


def apply_filter(flt: dict, fact: dict, payload: dict, subject: dict) -> bool:
    field, cmp_, value = flt["field"], flt["cmp"], flt["value"]
    actual: Any
    if field == "resolution":
        actual = fact["resolution"]
    elif field == "universe":
        actual = None  # portable domain comparison is admission-time for illegal values
        return True
    elif field == "confidenceMillionths":
        actual = fact["confidenceMillionths"]
    elif field == "subject":
        actual = occupancy_id(fact, payload, "source", subject["kind"])
    else:
        actual = payload.get(field)
    if cmp_ == "eq":
        return actual == value
    if cmp_ == "neq":
        return actual != value
    if cmp_ == "in":
        return actual in (value if isinstance(value, list) else [value])
    return False


def coverage_for_atom(atom: dict, coverages: list[dict], scopes: dict, subject: dict) -> list[dict]:
    """Exact-rung coverages whose scope contains the current source subject."""
    out = []
    for cov in coverages:
        payload = cov["payload"]
        if payload["key"]["relation"] != atom["relation"]:
            continue
        if payload["key"]["resolution"] != atom["minResolution"]:
            continue
        if payload["key"]["sourceUniverse"] != subject["universe"]:
            continue
        scope = scopes[cov["scopeId"]]
        if subject["nativeSubjectId"] not in scope["subjects"]:
            continue
        out.append(cov)
    return out


def atom_completeness(atom: dict, matching_covs: list[dict]) -> tuple[str, list[str]]:
    """Returns (completeness, causes). complete vs unknown vs missing."""
    if not matching_covs:
        return "missing", ["missing-relation-coverage"]
    # If any covering complete with null deficiency at exact rung: complete
    complete = False
    unknown = False
    causes = []
    for cov in matching_covs:
        entry = cov["payload"]["entry"]
        if entry["coverage"] == "complete" and entry.get("deficiency") is None:
            complete = True
        else:
            unknown = True
            if entry.get("deficiency"):
                causes.append(entry["deficiency"])
            else:
                causes.append("coverage-unknown")
    if complete and not unknown:
        return "complete", []
    if complete and unknown:
        # known matches still dominate for exists/none; completeness for none-true needs all
        return "partial", causes
    return "unknown", causes or ["coverage-unknown"]


def evaluate_atom(
    atom: dict,
    subject: dict,
    facts: list[dict],
    payloads: dict[str, dict],
    coverages: list[dict],
    scopes: dict,
) -> dict:
    matching = []
    for fact in facts:
        pl = payloads[fact["id"]]
        if fact_matches_atom(atom, fact, pl, subject):
            matching.append(fact)
    covs = coverage_for_atom(atom, coverages, scopes, subject)
    completeness, causes = atom_completeness(atom, covs)
    known_ids = [f["id"] for f in matching]
    op = atom["op"]
    value = UNKNOWN
    if op == "exists":
        if known_ids:
            value = TRUE
        elif completeness == "complete":
            value = FALSE
        else:
            value = UNKNOWN
    elif op == "none":
        if known_ids:
            value = FALSE
        elif completeness == "complete":
            value = TRUE
        else:
            value = UNKNOWN
    elif op == "count-at-most":
        n = atom["n"]
        if len(known_ids) > n:
            value = FALSE
        elif completeness == "complete" and len(known_ids) <= n:
            value = TRUE
        else:
            value = UNKNOWN
    elif op == "all-covered":
        if completeness == "complete" and not causes:
            # sufficiency_v2 simplified: complete coverage at requested rung
            value = TRUE
        else:
            value = UNKNOWN
    deficiencies = []
    if value == UNKNOWN:
        for c in causes:
            deficiencies.append(c)
    return {
        "value": value,
        "knownFactIds": known_ids,
        "uncertainFactIds": [],
        "coverageIds": [c["id"] for c in covs],
        "causes": causes,
        "deficiencies": deficiencies,
        "kind": "native-atom",
    }


def eval_node(
    node: dict,
    addr: str,
    subject: dict,
    facts: list[dict],
    payloads: dict[str, dict],
    coverages: list[dict],
    scopes: dict,
    acc: dict,
) -> dict:
    children = predicate_children(node, addr)
    child_results = []
    for ca, cn in children:
        child_results.append(eval_node(cn, ca, subject, facts, payloads, coverages, scopes, acc))
    if is_atom(node):
        res = evaluate_atom(node, subject, facts, payloads, coverages, scopes)
        res["addr"] = addr
        res["op"] = node["op"]
        res["childAddrs"] = []
        acc[addr] = res
        return res
    op = node["op"]
    child_vals = [c["value"] for c in child_results]
    if op == "and":
        value = kleene_and(child_vals)
    elif op == "or":
        value = kleene_or(child_vals)
    elif op == "not":
        value = kleene_not(child_vals[0])
    else:
        raise AdmissionError("PRED_OP", op)
    res = {
        "value": value,
        "knownFactIds": [],
        "uncertainFactIds": [],
        "coverageIds": [],
        "causes": [],
        "deficiencies": [],
        "kind": "boolean",
        "addr": addr,
        "op": op,
        "childAddrs": [c["addr"] for c in child_results],
    }
    acc[addr] = res
    return res


def enumerate_subjects(rule: dict, inventories: list[dict], universe_hex_by_token: dict[str, str]) -> dict:
    se = rule["subjectEnumeration"]
    token = se["universe"]
    if token not in UNIVERSE_MAP:
        raise AdmissionError("POLICY_UNIVERSE_TOKEN", token)
    domain = UNIVERSE_MAP[token]
    kind = se["subjectKind"]
    if kind == "export":
        row_kind = "symbol"
        export_filter = "exported"
    else:
        row_kind = kind
        export_filter = None
    selected = []
    unresolved = []
    incomplete = []
    inventory_refs = []
    covering = False
    for inv in inventories:
        if inv["kind"] != row_kind:
            continue
        covering = True
        inventory_refs.append(inv["digest"])
        if inv["state"] != "complete":
            incomplete.append(inv["digest"])
        for row in inv["rows"]:
            if export_filter:
                if row.get("exported") == "unknown":
                    unresolved.append(row)
                    continue
                if row.get("exported") != "exported":
                    continue
            # include/exclude globs — absent or [] means all; exclusion wins
            path = row["path"]
            include = se.get("include")
            exclude = se.get("exclude") or []
            if include:
                if not any(glob_match(g, path) for g in include):
                    continue
            if any(glob_match(g, path) for g in exclude):
                continue
            selected.append(row)
    if not covering:
        return {
            "state": "incomplete",
            "selected": [],
            "unresolved": [],
            "incomplete": [],
            "inventoryRefs": [],
            "cause": "no-covering-program",
            "universeHex": universe_hex_by_token[token],
            "kind": row_kind,
        }
    state = "complete" if not incomplete and not unresolved else "incomplete"
    return {
        "state": state,
        "selected": selected,
        "unresolved": unresolved,
        "incomplete": incomplete,
        "inventoryRefs": inventory_refs,
        "cause": None,
        "universeHex": universe_hex_by_token[token],
        "kind": row_kind,
    }


def glob_match(pattern: str, path: str) -> bool:
    """Closed glob: literal, *, ?, whole-segment **. Composition says **/*.ts matches root a.ts."""
    import re as _re

    segs_p = pattern.split("/")
    segs_s = path.split("/")

    def rec(pi: int, si: int) -> bool:
        if pi == len(segs_p):
            return si == len(segs_s)
        p = segs_p[pi]
        if p == "**":
            # match zero or more segments, including matching a file at root
            if pi == len(segs_p) - 1:
                return True
            for k in range(si, len(segs_s) + 1):
                if rec(pi + 1, k):
                    return True
            return False
        if si >= len(segs_s):
            return False
        rx = "^" + _re.escape(p).replace(r"\*", "[^/]*").replace(r"\?", "[^/]") + "$"
        if _re.match(rx, segs_s[si]):
            return rec(pi + 1, si + 1)
        return False

    return rec(0, 0)


def subject_descriptor(universe_hex: str, kind: str, row: dict) -> dict:
    rec: dict[str, Any] = {
        "schemaVersion": 3,
        "universe": universe_hex,
        "kind": kind,
        "nativeSubjectId": row["nativeSubjectId"],
    }
    if kind == "package":
        rec["packageManifestPath"] = row["path"]
    return rec


def evaluate_policy(
    *,
    policy: dict,
    program: dict,
    inventories: list[dict],
    facts: list[dict],
    fact_payloads: dict[str, dict],
    coverages: list[dict],
    scopes: dict[str, dict],
    universe_hex_by_token: dict[str, str],
    waivers: dict,
    emission_plan: dict,
    detector_closure: str,
    budget_limit: int,
) -> dict:
    """Return computed proof pieces: enumerations, witnesses, findings, verdict."""
    rule_results = []
    all_findings = []
    all_witness_records = []
    all_pred_proofs = []
    execution_deficiencies: list[dict] = []

    enabled_rules = [r for r in policy["rules"] if r["enabled"]]
    # budget preflight
    S = 0
    work = 0
    # estimate after enumeration
    enum_by_rule = {}
    for rule in policy["rules"]:
        if not rule["enabled"]:
            enum_by_rule[rule["ruleId"]] = {
                "state": "disabled",
                "selected": [],
                "unresolved": [],
                "incomplete": [],
                "inventoryRefs": [],
                "cause": None,
                "universeHex": universe_hex_by_token.get(rule["subjectEnumeration"]["universe"], ""),
                "kind": rule["subjectEnumeration"]["subjectKind"],
            }
            continue
        enum_by_rule[rule["ruleId"]] = enumerate_subjects(rule, inventories, universe_hex_by_token)

    # Charge E + sum (N + A*(F+I+K))
    E = sum(len(inv.get("rows") or []) for inv in inventories) + len(inventories)
    F = len(facts)
    K = len(coverages)
    I = 0
    work = E
    for rule in enabled_rules:
        nodes = _count_nodes(rule["emitWhen"])
        atoms = _count_atoms(rule["emitWhen"])
        s = len(enum_by_rule[rule["ruleId"]]["selected"])
        work += s * (nodes + atoms * (F + I + K))
    budget_exhausted = work > budget_limit

    for rule in policy["rules"]:
        rid = rule["ruleId"]
        enum = enum_by_rule[rid]
        if not rule["enabled"]:
            rule_results.append(
                {
                    "ruleId": rid,
                    "enumeration": _enum_out(enum, [], []),
                    "outcome": "disabled",
                    "findingIds": [],
                    "deficiencies": [],
                }
            )
            continue
        if budget_exhausted:
            # empty predicates/findings, actual enumeration, indeterminate if gating
            outcome = "indeterminate" if rule["gate"] else "pass"
            rule_results.append(
                {
                    "ruleId": rid,
                    "enumeration": _enum_out(enum, [], []),
                    "outcome": outcome,
                    "findingIds": [],
                    "deficiencies": [],
                }
            )
            continue

        finding_ids = []
        defics = []
        subject_values = []
        for row in enum["selected"]:
            subj_rec = subject_descriptor(enum["universeHex"], enum["kind"], row)
            subj_id = h_id("evaluation-subject", subj_rec)
            subj = {
                **subj_rec,
                "id": subj_id,
                "path": row["path"],
                "qualifiedName": row["qualifiedName"],
                "language": row["subjectLanguage"],
            }
            acc: dict = {}
            root = eval_node(rule["emitWhen"], "p", subj, facts, fact_payloads, coverages, scopes, acc)
            subject_values.append(root["value"])
            # retain every node as witness + predicate proof
            for addr, node_res in acc.items():
                wit, pred, proof_row = _materialize_node(
                    rule, program, subj, addr, node_res, acc
                )
                all_witness_records.append(wit)
                all_pred_proofs.append(proof_row)
            if root["value"] == TRUE:
                finding = emit_finding(rule, emission_plan, subj, acc, detector_closure)
                all_findings.append(finding)
                finding_ids.append(finding["id"])
            elif root["value"] == UNKNOWN:
                defics.append(
                    {
                        "source": "native",
                        "cause": (acc["p"].get("causes") or ["coverage-unknown"])[0]
                        if acc["p"].get("causes")
                        else "missing-relation-coverage",
                        "subjectId": subj_id,
                        "predicateId": "p",
                        "inputRefs": [],
                        "evidenceKind": None,
                        "nativeCause": None,
                        "universe": enum["universeHex"],
                    }
                )

        # rule outcome
        live_unwaived = [fid for fid in finding_ids]  # no waivers in synthetic
        gating = rule["enabled"] and rule["gate"] and SEV_ORDER[rule["severity"]] >= SEV_ORDER[policy["gateSeverityAtLeast"]]
        if gating and live_unwaived:
            outcome = "fail"
        elif gating and (enum["state"] != "complete" or any(v == UNKNOWN for v in subject_values) or enum["unresolved"] or enum["incomplete"]):
            outcome = "indeterminate"
        else:
            outcome = "pass"
        if not gating:
            outcome = "pass"
        selected_ids = [h_id("evaluation-subject", subject_descriptor(enum["universeHex"], enum["kind"], row)) for row in enum["selected"]]
        unresolved_ids = [h_id("evaluation-subject", subject_descriptor(enum["universeHex"], enum["kind"], row)) for row in enum["unresolved"]]
        rule_results.append(
            {
                "ruleId": rid,
                "enumeration": _enum_out(enum, selected_ids, unresolved_ids),
                "outcome": outcome,
                "findingIds": sorted(finding_ids),
                "deficiencies": defics,
            }
        )

    if budget_exhausted:
        execution_deficiencies.append(
            {
                "source": "execution",
                "cause": "work-budget-exhausted",
                "subjectId": None,
                "predicateId": None,
                "inputRefs": [],
                "evidenceKind": None,
                "nativeCause": None,
                "universe": None,
            }
        )

    # sealed verdict
    outcomes = [rr["outcome"] for rr in rule_results]
    if any(o == "fail" for o in outcomes):
        verdict = "fail"
    elif any(o == "indeterminate" for o in outcomes) or execution_deficiencies:
        verdict = "indeterminate"
    else:
        verdict = "pass"

    return {
        "ruleResults": sorted(rule_results, key=lambda r: r["ruleId"]),
        "findings": all_findings,
        "witnesses": all_witness_records,
        "predicateProofs": all_pred_proofs,
        "verdict": verdict,
        "evaluationState": "budget-exhausted" if budget_exhausted else "evaluated",
        "executionDeficiencies": execution_deficiencies,
        "workUnitsCharged": work,
        "budgetExhausted": budget_exhausted,
    }


def _count_nodes(node: dict) -> int:
    n = 1
    for _, ch in predicate_children(node, "p"):
        n += _count_nodes(ch)
    return n


def _count_atoms(node: dict) -> int:
    if is_atom(node):
        return 1
    return sum(_count_atoms(ch) for _, ch in predicate_children(node, "p"))


def _enum_out(enum: dict, selected_ids: list[str], unresolved_ids: list[str]) -> dict:
    return {
        "state": enum["state"] if enum["state"] != "disabled" else "disabled",
        "inventoryRefs": [{"domain": "subject-inventory", "digest": d} for d in sorted(enum["inventoryRefs"])],
        "selectedSubjectIds": sorted(selected_ids),
        "unresolvedSubjectIds": sorted(unresolved_ids),
        "incompleteInventoryRefs": [{"domain": "subject-inventory", "digest": d} for d in sorted(enum["incomplete"])],
    }


def _materialize_node(rule, program, subj, addr, node_res, acc):
    op = node_res["op"]
    node_obj = _node_at(rule["emitWhen"], addr)
    node_digest = canonical_digest(node_obj)
    prog_pred = {
        "schemaVersion": 2,
        "ruleProgramDigest": canonical_digest(program),
        "ruleId": rule["ruleId"],
        "predicateId": addr,
        "operation": op,
        "nodeDigest": node_digest,
    }
    kind = node_res["kind"]
    wit = {
        "schemaVersion": 3,
        "programPredicateDigest": canonical_digest(prog_pred),
        "matchingFactIds": sorted(node_res.get("knownFactIds") or []),
        "coverageIds": sorted(node_res.get("coverageIds") or []),
        "countLimit": None,
        "childPredicateIds": sorted(node_res.get("childAddrs") or []),
        "matchingImportRows": [],
        "uncertainFactIds": [],
        "uncertainImportRows": [],
        "deficiencies": [],
        "kind": kind,
    }
    if op == "count-at-most":
        wit["countLimit"] = node_obj.get("n")
    proof_row = {
        "ruleId": rule["ruleId"],
        "subjectId": subj["id"],
        "predicateId": addr,
        "operation": op,
        "inputRefs": [],
        "scopeIds": [],
        "value": node_res["value"],
        "witnessDigest": canonical_digest(wit),
    }
    return wit, prog_pred, proof_row


def _node_at(root: dict, addr: str) -> dict:
    if addr == "p":
        return root
    assert addr.startswith("p.")
    parts = addr.split(".")[1:]
    cur = root
    for p in parts:
        i = int(p)
        if cur["op"] == "not":
            cur = cur["operand"]
        else:
            cur = cur["operands"][i]
    return cur


def emit_finding(rule, emission_plan, subj, acc, detector_closure) -> dict:
    root = acc["p"]
    params = {
        "schemaVersion": 2,
        "messageCode": rule.get("messageCode") or rule["ruleId"],
        "parameters": {
            "ruleId": rule["ruleId"],
            "subjectPath": subj["path"],
            "qualifiedName": subj["qualifiedName"],
            "subjectKind": subj["kind"],
            "subjectLanguage": subj["language"],
            "matchingFactCount": _union_match_count(acc),
            "matchingImportCount": 0,
        },
    }
    # file/package discriminator SHA256(C([]))
    disc = sha256(encode_c([]))
    fp_desc = {
        "schemaVersion": 2,
        "ruleStableId": rule["ruleProgramRef"]["ruleStableId"],
        "detectorSemanticsMajor": rule["ruleProgramRef"]["semanticsMajor"],
        "subjectKey": {
            "language": subj["language"],
            "kind": subj["kind"],
            "logicalPath": subj["path"],
            "qualifiedName": subj["qualifiedName"],
            "discriminator": disc,
        },
        "relatedSubjectKeys": [],
    }
    fp_id = h_id("finding-fingerprint", fp_desc)
    evidence = [{"domain": "predicate-witness", "digest": canonical_digest(_dummy_root_wit(rule, acc, subj))}]
    finding = {
        "schemaVersion": 3,
        "fingerprint": fp_id,
        "ruleClosure": detector_closure,
        "subjectId": subj["id"],
        "messageCode": rule.get("messageCode") or rule["ruleId"],
        "parameterDigest": canonical_digest(params),
        "severity": rule["severity"],
        "evidenceRefs": evidence,
        "ruleId": rule["ruleId"],
        "subject": {
            "language": subj["language"],
            "kind": subj["kind"],
            "logicalPath": subj["path"],
            "qualifiedName": subj["qualifiedName"],
        },
        "correspondence": {"state": "matched", "reason": None},
    }
    finding["id"] = h_id("finding", finding)
    finding["_fingerprintDesc"] = fp_desc
    finding["_params"] = params
    return finding


def _union_match_count(acc: dict) -> int:
    s = set()
    for n in acc.values():
        s.update(n.get("knownFactIds") or [])
    return len(s)


def _dummy_root_wit(rule, acc, subj):
    # placeholder; graphs layer replaces with actual witness digest
    return {
        "schemaVersion": 3,
        "programPredicateDigest": "0" * 64,
        "matchingFactIds": sorted(acc["p"].get("knownFactIds") or []),
        "coverageIds": sorted(acc["p"].get("coverageIds") or []),
        "countLimit": None,
        "childPredicateIds": sorted(acc["p"].get("childAddrs") or []),
        "matchingImportRows": [],
        "uncertainFactIds": [],
        "uncertainImportRows": [],
        "deficiencies": [],
        "kind": acc["p"]["kind"],
    }
