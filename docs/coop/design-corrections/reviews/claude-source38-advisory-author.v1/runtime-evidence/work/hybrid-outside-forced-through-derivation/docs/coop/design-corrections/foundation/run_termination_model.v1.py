"""Reference derivation of an evaluator3 analysis Run's whole-Run termination (run-termination-contract.v1.md).

The host finalizer is the only constructor of a Run's termination (d9-exit-contract invariant-one-mapper). For
the branch this owner governs - no fault, no rejection, no interruption before settle, durability committed -
the class follows the SEALED verdict, and for `indeterminate` the ordered reasonCodes, the D9
(deficiency, secondaryDeficiencies) pair and `coverageId` are a pure function of retained admitted Run content:

  1. admit: identity-model.v3 close_run (complete replay) must admit the Run; nothing below reads a claim
     that replay did not recompute.
  2. population: every proof.executionDeficiencies record, plus, for each ruleResult whose sealed outcome is
     `indeterminate`, its rule-level records (enumeration, required import, work budget) and the verdict-
     blocking witness deficiencies of each selected subject whose root value is `indeterminate`
     (composition section 5, recomputed over the retained witness tree).
  3. conditions: each record contributes its own cause; a record's ORIGINATING Coverage (composition 9.5 item
     3 / 9.6 step 7) contributes a declared carrier when its entry.deficiency equals that cause, and a
     stage-implied condition when its entry.resolutionCompleteness.stageTerminal is a clean typed terminal
     (budget-exhausted -> budget-exhausted, unavailable -> provider-unavailable; native section 10).
  4. order: rank = native section 10 precedence index of a DeficiencyV2 cause (work-budget-exhausted ranks as
     budget-exhausted); every other registered cause ranks after all nine. reasonCodes are the distinct D9
     deficiencies by least rank, mapped through d9-exit-contract codeMaps.deficiencyToReasonCode.
  5. coverageId: the canonically least declared carrier of the primary cause, else the least stage-implied
     carrier, else omitted.

Discovery order, proof array order, host scheduling and trusted host observations of the invocation are not
inputs, so any permutation of the population yields the same termination. What is derived is the ANALYSIS
PROJECTION of the step termination (class, runId, reasonCodes, coverageId, and the absence of errorCode, faultCause
and signal). A host StepTermination may also carry executionId, domainDetail or authority; those members are
delegated to their own owners, and `check_projection` reports them as owner-validation-required, never as lawful.
`admit_analysis_step_termination` is their admission law at the host composition boundary (contract section 7).
Reference evidence only.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DC = HERE.parent
D9_CONTRACT_PATH = HERE.parents[1] / "artifacts" / "d9-exit-contract.v1.14.json"


def _load(name, path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


R = _load("run_termination_replay3", HERE / "evaluator_replay_model.v3.py")
M = R.M
C = M.C
N = _load("run_termination_native2", DC / "native" / "native_evidence_model.v2.py")
D9 = json.loads(D9_CONTRACT_PATH.read_text(encoding="utf-8"))
REGISTRY = M.SCHEMA["x-opensip-evaluator-deficiency-registry"]

PRECEDENCE = list(N.PRECEDENCE_V2)
EVALUATOR_ONLY_RANK = len(PRECEDENCE)
STAGE_TERMINAL_DEFICIENCY = dict(N.STAGE_TERMINAL_DEFICIENCY)
WORK_BUDGET = "work-budget-exhausted"
CODE_MAP = D9["codeMaps"]["deficiencyToReasonCode"]


class RunTerminationError(C.AdmissionError):
    """A candidate termination that is not the derived one, or a Run this owner cannot explain."""


def cause_route(cause: str) -> dict:
    """(rank, D9 deficiency) of ONE registered evaluator cause. Total over the registry; refuses anything else."""
    registered = {c for members in REGISTRY["sources"].values() for c in members}
    if cause not in registered:
        raise RunTerminationError("RUN_TERMINATION_CAUSE_UNREGISTERED:" + cause)
    if cause in PRECEDENCE:
        return {"rank": PRECEDENCE.index(cause), "d9Deficiency": N.native_deficiency_d9(cause)["d9Deficiency"]}
    if cause == WORK_BUDGET:
        return {"rank": PRECEDENCE.index("budget-exhausted"), "d9Deficiency": "budget-exhausted"}
    return {"rank": EVALUATOR_ONLY_RANK, "d9Deficiency": "verdict-indeterminate"}


def route_drift() -> list[str]:
    """Faults between this owner's tables and their owners (native route, D9 codeMaps, evaluator registry)."""
    faults = list(N.d9_route_drift())
    if PRECEDENCE != N.SCHEMAS["$defs"]["DeficiencyV2"]["enum"]:
        faults.append("section 10 precedence is not DeficiencyV2 in declared order")
    for source, members in REGISTRY["sources"].items():
        for cause in members:
            d9 = cause_route(cause)["d9Deficiency"]
            if d9 not in CODE_MAP:
                faults.append(f"{source}/{cause} routes to {d9}, which the D9 owner does not map")
    for d9 in {cause_route(c)["d9Deficiency"] for m in REGISTRY["sources"].values() for c in m}:
        if not CODE_MAP[d9].startswith(("COVERAGE.", "VERDICT.")):
            faults.append(f"{d9} maps to {CODE_MAP[d9]}, outside the evaluator whole-Run vocabulary")
    return faults


def _xi(proof):
    refs = [r for r in proof["evaluationInputRefs"] if r["domain"] == "execution-inputs"]
    if len(refs) != 1:
        raise RunTerminationError("RUN_TERMINATION_EXECUTION_INPUTS_REF")
    return refs[0]


def _originating_coverage(record, xi):
    """Composition 9.6 step 7 (execution: inputRefs minus XI) and 9.5 item 3 (native: exactly one Coverage ref).
    Whole-selection refs (atom items 1-2, inputRefs = EI) name no originating record."""
    if record["source"] == "execution":
        refs = [r for r in record["inputRefs"] if r != xi]
    elif record["source"] == "native" and len(record["inputRefs"]) == 1:
        refs = list(record["inputRefs"])
    else:
        refs = []
    return sorted("coverage2:" + r["digest"] for r in refs if r["domain"] == "coverage")


def retained_population(run, objects, blobs):
    """Admit the Run (complete replay) and return (runId, verdict, the verdict-relevant deficiency records)."""
    run_id = M.close_run(run, objects, blobs)
    seal = objects[run["evaluationSealId"]][1]
    proof = objects[seal["proofBundleId"]][1]
    plan = objects[run["planId"]][1]
    policy = C.parse(blobs[plan["policyDigest"]])
    rules = {r["ruleId"]: r for r in policy["rules"]}
    by_address = {(p["ruleId"], p["subjectId"], p["predicateId"]): p for p in proof["predicateProofs"]}
    witness = {}

    def blocks(rule, record):
        if record["cause"] in REGISTRY["nonBlockingDisclosures"]:
            return False
        if record["source"] != "import":
            return record["source"] in ("native", "enumeration", "execution")
        return record["evidenceKind"] in {v["kind"] for v in rule["evidenceUse"] if v["requirement"] == "required"}

    def blocking(rule_id, subject_id, predicate_id):
        node = by_address[(rule_id, subject_id, predicate_id)]
        if node["value"] != "indeterminate":
            return []
        w = witness.setdefault(node["witnessDigest"], C.parse(blobs[node["witnessDigest"]]))
        if w["kind"] != "boolean":
            return list(w["deficiencies"])
        return [d for child in w["childPredicateIds"] for d in blocking(rule_id, subject_id, child)]

    population = list(proof["executionDeficiencies"])
    for result in proof["ruleResults"]:
        if result["outcome"] != "indeterminate":
            continue
        rule = rules[result["ruleId"]]
        rule_level = [d for d in result["deficiencies"]
                      if d["source"] == "enumeration"
                      or (d["source"] == "import" and d["subjectId"] is None and d["predicateId"] is None)
                      or (d["source"] == "execution" and d["cause"] == WORK_BUDGET)]
        root_level = [d for sid in result["enumeration"]["selectedSubjectIds"] if (result["ruleId"], sid, "p") in by_address
                      for d in blocking(result["ruleId"], sid, "p") if blocks(rule, d)]
        explained = rule_level + root_level
        if not explained:
            raise RunTerminationError("RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RULE:" + result["ruleId"])
        population.extend(explained)
    if proof["verdict"] == "indeterminate" and not population:
        raise RunTerminationError("RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RUN")
    return run_id, proof["verdict"], population, {"proof": proof, "xi": _xi(proof)}


def conditions(population, objects, blobs, xi):
    """Every condition the population exhibits: its own cause, and stage terminals its originating Coverage retains."""
    out = []
    for record in population:
        route = cause_route(record["cause"])
        declared, implied = [], []
        for cid in _originating_coverage(record, xi):
            entry = C.parse(blobs[objects[cid][1]["payloadDigest"]])["entry"]
            if entry["deficiency"] == record["cause"]:
                declared.append(cid)
            terminal = entry["resolutionCompleteness"]["stageTerminal"]
            if terminal in STAGE_TERMINAL_DEFICIENCY:
                stage_cause = STAGE_TERMINAL_DEFICIENCY[terminal]
                out.append({"cause": stage_cause, "origin": "stage-terminal", "source": record["source"],
                            **cause_route(stage_cause), "declaredCarriers": [], "stageCarriers": [cid],
                            "entryDeficiency": entry["deficiency"]})
        out.append({"cause": record["cause"], "origin": "record", "source": record["source"], **route,
                    "declaredCarriers": declared, "stageCarriers": []})
    return out


def reduce(conds):
    """Total pre-reduction order, then the D9 codeDerivation. Independent of the order of `conds`."""
    if not conds:
        raise RunTerminationError("RUN_TERMINATION_EMPTY_DEFICIENCY_SET")
    least = {}
    for c in conds:
        least[c["d9Deficiency"]] = min(least.get(c["d9Deficiency"], c["rank"]), c["rank"])
    ordered = sorted(least, key=lambda d9: least[d9])
    if len(set(least.values())) != len(least):
        raise RunTerminationError("RUN_TERMINATION_RANK_COLLISION")
    primary_rank = least[ordered[0]]
    at_primary = [c for c in conds if c["rank"] == primary_rank]
    declared = sorted({cid for c in at_primary for cid in c["declaredCarriers"]}, key=str.encode)
    staged = sorted({cid for c in at_primary for cid in c["stageCarriers"]}, key=str.encode)
    carrier = (declared or staged or [None])[0]
    return {"deficiency": ordered[0], "secondaryDeficiencies": ordered[1:],
            "reasonCodes": [CODE_MAP[d9] for d9 in ordered],
            "primaryCause": PRECEDENCE[primary_rank] if primary_rank < EVALUATOR_ONLY_RANK else None,
            "coverageId": carrier, "carrierKind": "declared" if declared else ("stage-terminal" if staged else None)}


def derive(run, objects, blobs):
    """The analysis projection and its reduction, plus the retained population the host composition reads (section 7)."""
    run_id, verdict, population, ctx = retained_population(run, objects, blobs)
    if verdict == "pass":
        return {"termination": {"class": "success", "runId": run_id}, "reduction": None, "population": population}
    if verdict == "fail":
        return {"termination": {"class": "policy-failed", "runId": run_id}, "reduction": None, "population": population}
    reduction = reduce(conditions(population, objects, blobs, ctx["xi"]))
    term = {"class": "indeterminate", "reasonCodes": reduction["reasonCodes"], "runId": run_id}
    if reduction["coverageId"] is not None:
        term["coverageId"] = reduction["coverageId"]
    return {"termination": term, "reduction": reduction, "population": population}


def finalize(run, objects, blobs):
    """Settled analysis Run with no fault, rejection or pre-settle interruption: its analysis projection."""
    derived = derive(run, objects, blobs)
    return {"termination": derived["termination"], "reduction": derived["reduction"]}


# The ANALYSIS PROJECTION: the StepTermination members this owner derives from the admitted Run. errorCode,
# faultCause and signal belong to it because the derived classes (success, policy-failed, indeterminate) never
# carry them, so their presence contradicts the derived class.
PROJECTION_FIELDS = ("class", "runId", "reasonCodes", "coverageId", "errorCode", "faultCause", "signal")
# Optional StepTermination members the analysis projection neither derives nor licenses. check_projection checks
# only their shape; admit_analysis_step_termination (section 7) is their admission law.
DELEGATED_FIELDS = {
    "executionId": "attempt identity: workflows-and-surfaces section 1 (a fresh ExecutionId per admitted attempt) "
                   "and identity-and-evidence section 2 (host-CSPRNG draw); admitted by section 7.3",
    "domainDetail": "explanatory DomainDetail beside the existing code: workflows-and-surfaces sections 8 and 9, the "
                    "public detail registry, composition section 8 and native section 10; admitted by section 7.5",
    "authority": "workflows-and-surfaces sections 1 and 9 and the StepTermination branch contract "
                 "(authority=ephemeral only without a runId); admitted by section 7.4",
}


def check_projection(candidate, derived, validate_shape=None):
    """Admit a candidate StepTermination's analysis projection; never report its delegated members as lawful.

    Refusal order is fixed: a non-object; a member outside PROJECTION_FIELDS and DELEGATED_FIELDS
    (RUN_TERMINATION_UNKNOWN_FIELD); a projection that is not exactly the derived one - class, runId, reasonCodes
    and their order, coverageId presence and value, or any errorCode/faultCause/signal (RUN_TERMINATION_NOT_DERIVED);
    a delegated member with no shape validator (RUN_TERMINATION_DELEGATED_SHAPE_UNCHECKED) or whose candidate the
    validator refuses (RUN_TERMINATION_DELEGATED_SHAPE). Otherwise it returns the projection, the delegated members
    and their owners with standing `owner-validation-required`: a shape-valid delegated value is not thereby lawful.
    This is the pure projection check; that standing is scoped to it and is never a host admission (section 7).
    """
    if type(candidate) is not dict:
        raise RunTerminationError("RUN_TERMINATION_CANDIDATE_NOT_OBJECT")
    unknown = sorted(set(candidate) - set(PROJECTION_FIELDS) - set(DELEGATED_FIELDS))
    if unknown:
        raise RunTerminationError("RUN_TERMINATION_UNKNOWN_FIELD:" + ",".join(unknown))
    projection = {k: candidate[k] for k in PROJECTION_FIELDS if k in candidate}
    if projection != derived:
        raise RunTerminationError("RUN_TERMINATION_NOT_DERIVED:" + json.dumps({"derived": derived}, sort_keys=True))
    delegated = {k: candidate[k] for k in DELEGATED_FIELDS if k in candidate}
    if delegated:
        if validate_shape is None:
            raise RunTerminationError("RUN_TERMINATION_DELEGATED_SHAPE_UNCHECKED:" + ",".join(sorted(delegated)))
        try:
            validate_shape(candidate)
        except Exception as exc:
            raise RunTerminationError("RUN_TERMINATION_DELEGATED_SHAPE:" + str(exc).split("\n")[0][:200]) from exc
    return {"projection": projection, "delegated": delegated,
            "delegatedOwners": {k: DELEGATED_FIELDS[k] for k in sorted(delegated)},
            "delegatedStanding": "owner-validation-required" if delegated else None}


def admit_projection(candidate, run, objects, blobs, validate_shape=None):
    """Derive the analysis projection from the admitted Run, then check_projection."""
    return check_projection(candidate, finalize(run, objects, blobs)["termination"], validate_shape)


# ---------------------------------------------------------------------------------------------------------------
# Host composition of the whole analysis StepTermination (run-termination-contract.v1.md section 7). The analysis
# projection above stays pure. The composition admits the delegated members by closed laws over two separate inputs:
# the admitted Run (retained semantic content, re-derived here) and the host's trusted operational observation of
# the admitted attempt (its StepResult attempts, durability, commit receipt and installation observation). Neither is
# caller input, and no candidate member blesses itself.

ANALYSIS_CLASSES = ("success", "policy-failed", "indeterminate")
# Classes the sealed verdict never decides. Their owners compose them; the composition returns the owner WITHOUT
# reading the Run, so an operational carrier is never passed through verdict derivation (section 7.1).
OUTSIDE_ANALYSIS_PROJECTION = {
    "operational-failed": "fault precedence: d9-exit-contract.v1.14 causeModel; workflows-and-surfaces sections 1 and 9; "
                          "security S12; native section 10 route registry",
    "request-rejected": "rejection precedence: d9-exit-contract.v1.14 causeModel and the refusing admission owner",
    "interrupted": "interruption before settle: d9-exit-contract.v1.14 and workflows-and-surfaces section 1",
}
WORK_BUDGET_DETAIL = "EVALUATION.WORK_BUDGET_EXHAUSTED"
CLOSURE_DETAIL = "COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED"
# Registered native DomainDetailCode members that are DeficiencyV2 entry deficiencies (public-detail-registry owner
# native; native-evidence.md section 10, "Retained and public routes are different, and both are named").
NATIVE_ENTRY_DETAILS = ("budget-exhausted", "derivation-policy-unmet", "external-consumers-unknown",
                        "input-closure-incomplete", "resolution-incomplete")
# The closed analysis domainDetail allowlist, in selection order (section 7.5).
ANALYSIS_DETAIL_ALLOWLIST = (WORK_BUDGET_DETAIL, CLOSURE_DETAIL) + NATIVE_ENTRY_DETAILS
OBSERVATION_FIELDS = frozenset({"stepId", "durability", "attempts", "commitReceipt", "requiredClosureNotInstalled"})


def _refuse(key, detail=None):
    raise RunTerminationError(key if detail is None else key + ":" + detail)


def analysis_detail_code(derived, objects, blobs, required_closure_not_installed):
    """The one domainDetail code a composed committed analysis termination carries, or None (section 7.5).

    1. EVALUATION.WORK_BUDGET_EXHAUSTED: the retained population holds a work-budget-exhausted record and the primary
       D9 deficiency is budget-exhausted, so the work budget sits at the primary rank;
    2. else COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED: reasonCodes[0] is COVERAGE.PROVIDER_UNAVAILABLE and the host
       observed that a required provider closure of the attempt is not installed;
    3. else the coverageId record's own entry.deficiency, when it is a native entry detail;
    4. else None. success and policy-failed carry none.
    """
    reduction = derived["reduction"]
    if reduction is None:
        return None
    if reduction["deficiency"] == "budget-exhausted" and any(r["cause"] == WORK_BUDGET for r in derived["population"]):
        return WORK_BUDGET_DETAIL
    if reduction["reasonCodes"][0] == CODE_MAP["provider-unavailable"] and required_closure_not_installed is True:
        return CLOSURE_DETAIL
    if reduction["coverageId"] is not None:
        entry = C.parse(blobs[objects[reduction["coverageId"]][1]["payloadDigest"]])["entry"]
        if entry["deficiency"] in NATIVE_ENTRY_DETAILS:
            return entry["deficiency"]
    return None


def admit_attempt_observation(observation, validate_attempt, validate_receipt):
    """Admit the host's operational observation of the step and return its terminating attempt (sections 7.2, 7.3).

    Shapes are the existing records (invocation-record Attempt, identity commit-receipt). Joins are checked; the host
    that supplies them is trusted, not authenticated (section 7.7).
    """
    if type(observation) is not dict or set(observation) != OBSERVATION_FIELDS:
        _refuse("RUN_TERMINATION_OBSERVATION_SHAPE", "fields")
    step_id, durability, attempts = observation["stepId"], observation["durability"], observation["attempts"]
    if (type(step_id) is not int or not 0 <= step_id <= 63 or durability not in ("authoritative", "ephemeral")
            or type(observation["requiredClosureNotInstalled"]) is not bool
            or type(attempts) is not list or not 1 <= len(attempts) <= 3):
        _refuse("RUN_TERMINATION_OBSERVATION_SHAPE", "members")
    for attempt in attempts:
        try:
            validate_attempt(attempt)
        except Exception as exc:
            _refuse("RUN_TERMINATION_OBSERVATION_SHAPE", "attempt " + str(exc).split("\n")[0][:120])
    ids = [a["executionId"] for a in attempts]
    if len(set(ids)) != len(ids):
        _refuse("RUN_TERMINATION_ATTEMPT_ID_REUSED")
    terminating = attempts[-1]
    if (terminating["outcome"] != "completed" or "derivation" not in terminating
            or any(a["outcome"] == "completed" for a in attempts[:-1])):
        _refuse("RUN_TERMINATION_ATTEMPT_NOT_TERMINATING")
    receipt = observation["commitReceipt"]
    if durability == "ephemeral":
        if receipt is not None:
            _refuse("RUN_TERMINATION_OBSERVATION_SHAPE", "an ephemeral attempt has no commit receipt")
    else:
        try:
            validate_receipt(receipt)
        except Exception as exc:
            _refuse("RUN_TERMINATION_OBSERVATION_SHAPE", "receipt " + str(exc).split("\n")[0][:120])
    return terminating


def admit_analysis_step_termination(candidate, run, objects, blobs, observation, validate_shape, validate_attempt,
                                    validate_receipt):
    """Admit a whole StepTermination at the host composition boundary (section 7.6). Fixed order:

    0. a non-object refuses; a class the verdict never decides returns its owner without reading the Run;
    1. the attempt observation (OBSERVATION_SHAPE, ATTEMPT_ID_REUSED, ATTEMPT_NOT_TERMINATING);
    2. an ephemeral attempt: no runId, authority=ephemeral, executionId of the attempt, no domainDetail; its
       projection is not derived here;
    3. a committed Run: close_run and the derivation, then the attempt/Run joins (RECEIPT_RUN_MISMATCH,
       RECEIPT_ATTEMPT_MISMATCH, ATTEMPT_PLAN_MISMATCH), check_projection, authority omitted
       (AUTHORITY_NOT_COMPOSED), executionId of the terminating attempt (EXECUTION_ID_NOT_ATTEMPT), and exactly the
       selected detail (DETAIL_NOT_ADMITTED, DETAIL_REQUIRED, DETAIL_MEMBER_NOT_ADMITTED). The remedy text is
       presentation and is not compared.
    """
    if type(candidate) is not dict:
        _refuse("RUN_TERMINATION_CANDIDATE_NOT_OBJECT")
    if validate_shape is None or validate_attempt is None or validate_receipt is None:
        _refuse("RUN_TERMINATION_COMPOSITION_UNCHECKED")
    terminating = admit_attempt_observation(observation, validate_attempt, validate_receipt)
    execution_id = candidate.get("executionId")
    detail = candidate.get("domainDetail")
    if observation["durability"] == "ephemeral":
        unknown = sorted(set(candidate) - set(PROJECTION_FIELDS) - set(DELEGATED_FIELDS))
        if unknown:
            _refuse("RUN_TERMINATION_UNKNOWN_FIELD", ",".join(unknown))
        try:
            validate_shape(candidate)
        except Exception as exc:
            _refuse("RUN_TERMINATION_DELEGATED_SHAPE", str(exc).split("\n")[0][:200])
        if candidate.get("class") not in ANALYSIS_CLASSES or "runId" in candidate:
            _refuse("RUN_TERMINATION_EPHEMERAL_NOT_COMMITTED_RUN")
        if candidate.get("authority") != "ephemeral":
            _refuse("RUN_TERMINATION_EPHEMERAL_AUTHORITY_REQUIRED")
        if execution_id is not None and execution_id != terminating["executionId"]:
            _refuse("RUN_TERMINATION_EXECUTION_ID_NOT_ATTEMPT")
        if detail is not None:
            _refuse("RUN_TERMINATION_DETAIL_NOT_ADMITTED", "ephemeral")
        return {"standing": "ephemeral-attribution-admitted", "executionId": terminating["executionId"],
                "projectionStanding": "not derived: section 1 derives the analysis projection only for a committed Run"}
    derived = derive(run, objects, blobs)
    receipt = observation["commitReceipt"]
    if receipt["runId"] != derived["termination"]["runId"]:
        _refuse("RUN_TERMINATION_RECEIPT_RUN_MISMATCH")
    if receipt["executionId"] != terminating["executionId"]:
        _refuse("RUN_TERMINATION_RECEIPT_ATTEMPT_MISMATCH")
    if terminating["derivation"]["planId"] != run["planId"]:
        _refuse("RUN_TERMINATION_ATTEMPT_PLAN_MISMATCH")
    checked = check_projection(candidate, derived["termination"], validate_shape)
    if "authority" in candidate:
        _refuse("RUN_TERMINATION_AUTHORITY_NOT_COMPOSED", str(candidate["authority"]))
    if execution_id is not None and execution_id != terminating["executionId"]:
        _refuse("RUN_TERMINATION_EXECUTION_ID_NOT_ATTEMPT")
    want = analysis_detail_code(derived, objects, blobs, observation["requiredClosureNotInstalled"])
    if detail is None:
        if want is not None:
            _refuse("RUN_TERMINATION_DETAIL_REQUIRED", want)
    else:
        if detail["code"] != want:
            _refuse("RUN_TERMINATION_DETAIL_NOT_ADMITTED", detail["code"])
        if set(detail) != {"code", "remedy"}:
            _refuse("RUN_TERMINATION_DETAIL_MEMBER_NOT_ADMITTED", ",".join(sorted(set(detail) - {"code", "remedy"})))
    return {"standing": "composed-analysis-termination-admitted", "projection": checked["projection"],
            "executionId": terminating["executionId"], "domainDetailCode": want,
            "trustedHostInputs": ["attempts", "durability", "commitReceipt", "requiredClosureNotInstalled"]}


def d9_concurrent_reducer(deficiencies):
    """d9-exit-contract concurrentConditionReducer deficiency branch, verbatim: primary = deficiencies[0]."""
    primary, rest = deficiencies[0], []
    for d in deficiencies[1:]:
        if d != primary and d not in rest:
            rest.append(d)
    return [CODE_MAP[primary]] + [CODE_MAP[d] for d in rest]


def discovery_orders(items):
    """Every order when there are at most six items; otherwise every rotation of the list and of its reverse.
    Each rotation puts a different record first, which is what decides a first-discovered primary."""
    items = list(items)
    if len(items) <= 6:
        return [list(p) for p in itertools.permutations(items)]
    orders = []
    for base in (items, items[::-1]):
        orders.extend(base[k:] + base[:k] for k in range(len(base)))
    return orders


def permutation_invariance(conds):
    """Derived reductions versus the raw D9 reducer fed in host discovery order, over discovery_orders."""
    derived, raw = set(), set()
    orders = discovery_orders(conds)
    for perm in orders:
        r = reduce(perm)
        derived.add(json.dumps({k: r[k] for k in ("reasonCodes", "coverageId")}, sort_keys=True))
        raw.add(tuple(d9_concurrent_reducer([c["d9Deficiency"] for c in perm])))
    return {"orders": len(orders), "distinctDerived": len(derived),
            "distinctRawReducerSequences": len(raw), "rawPrimaryCodes": sorted({s[0] for s in raw})}
