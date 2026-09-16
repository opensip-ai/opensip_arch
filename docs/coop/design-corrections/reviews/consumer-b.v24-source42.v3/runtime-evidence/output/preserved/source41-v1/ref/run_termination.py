"""Whole-Run indeterminate termination of an evaluator3 analysis Run (foundation/run-termination-contract.v1.md s1-s7), source39.

Independent reconstruction from the contract text: condition population (s3), cause bridge and total order (s4), coverageId (s5),
the candidate projection check (s6) and the host composition of the whole analysis StepTermination (s7). The retained inputs are the
graph ref/closure.py admits by complete replay; s7 host observations (attempts, durability, receipt, installation) are explicit
synthetic trusted inputs and are never read from the Run.

Reconstruction readings recorded for phase 10 (not contradictions of the text):
  * s6 step 2 "outside the projection and delegated members": errorCode / faultCause / signal are members the projection governs
    (s1: their presence contradicts it), so they refuse RUN_TERMINATION_NOT_DERIVED at step 3, not UNKNOWN_FIELD.
  * s3 "RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_*" is spelled here with the suffixes _RULE and _RUN.
  * HC-41 (source41 run-termination s6 step 1, line 173): the non-object key is published, RUN_TERMINATION_CANDIDATE_NOT_OBJECT; the
    source39 reconstruction's own cb24.RUN_TERMINATION_NOT_AN_OBJECT is withdrawn. s7.6 step 1 names no key of its own and uses it too.
  * s7.3 commit_inventory: objects = the exported Run store's typed object identities, blobDigests = its retained blob digests.
"""
import canonical as K
import schemas
from native_facts import PRECEDENCE

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
COMMON3 = "workflows/schemas/evaluator3/common.schema.json"
INVOC3 = "workflows/schemas/evaluator3/invocation-record.schema.json"
DEFREG = KIT.doc(ID)["x-opensip-evaluator-deficiency-registry"]
NONBLOCKING = set(DEFREG["nonBlockingDisclosures"])
REGISTERED = {c for causes in DEFREG["sources"].values() for c in causes}
TO_REASON = KIT.doc("coop/artifacts/d9-exit-contract.v1.14.json")["codeMaps"]["deficiencyToReasonCode"]
STAGE_TERMINAL = {"budget-exhausted": "budget-exhausted", "unavailable": "provider-unavailable"}
ROW3 = ("budget-exhausted", "derivation-policy-unmet", "external-consumers-unknown", "input-closure-incomplete", "resolution-incomplete")
GOVERNED = {"class", "runId", "reasonCodes", "coverageId", "errorCode", "faultCause", "signal"}
DELEGATED = {"executionId", "domainDetail", "authority"}
NOT_COMPOSED = {"operational-failed", "request-rejected", "interrupted"}


class TerminationRefusal(Exception):
    def __init__(self, key, detail=""):
        super().__init__(f"{key}:{detail}" if detail else key)
        self.key, self.detail = key, detail


def cset(items):
    uniq = {K.C(x): x for x in items}
    return [uniq[k] for k in sorted(uniq)]


def bridge(cause):
    """s4 cause bridge -> (rank, D9 deficiency)."""
    if cause in PRECEDENCE:
        return PRECEDENCE.index(cause), (cause if cause in TO_REASON else "verdict-indeterminate")
    if cause == "work-budget-exhausted":
        return PRECEDENCE.index("budget-exhausted"), "budget-exhausted"
    if cause in REGISTERED:
        return len(PRECEDENCE), "verdict-indeterminate"
    raise TerminationRefusal("RUN_TERMINATION_CAUSE_UNREGISTERED", cause)


def _blocks(record, required_kinds):
    if record["source"] == "correspondence" or record["cause"] in NONBLOCKING:
        return False
    if record["source"] == "import":
        return record["evidenceKind"] in required_kinds
    return True


def _blocking(store, proofs, rule_id, subject_id, address, required_kinds):
    node = proofs[(rule_id, subject_id, address)]
    if node["value"] != "indeterminate":
        return []
    witness = store.get_record(node["witnessDigest"])
    if witness["kind"] == "boolean":
        out = []
        for child in witness["childPredicateIds"]:
            out += _blocking(store, proofs, rule_id, subject_id, child, required_kinds)
        return out
    return [d for d in witness["deficiencies"] if _blocks(d, required_kinds)]


def population(g, store):
    """s3 over the admitted proof, witnesses and policy."""
    proof = g["proof"]
    rules = {r["ruleId"]: r for r in g["policy"]["rules"]}
    proofs = {(p["ruleId"], p["subjectId"], p["predicateId"]): p for p in proof["predicateProofs"]}
    records = list(proof["executionDeficiencies"])
    for rr in proof["ruleResults"]:
        if rr["outcome"] != "indeterminate":
            continue
        required = {e["kind"] for e in rules[rr["ruleId"]]["evidenceUse"] if e["requirement"] == "required"}
        rule_records = [x for x in rr["deficiencies"]
                        if x["source"] == "enumeration" or (x["source"] == "import" and x["subjectId"] is None and x["predicateId"] is None)
                        or (x["source"] == "execution" and x["cause"] == "work-budget-exhausted")]
        for sid in rr["enumeration"]["selectedSubjectIds"]:
            if proofs.get((rr["ruleId"], sid, "p"), {}).get("value") == "indeterminate":
                rule_records += _blocking(store, proofs, rr["ruleId"], sid, "p", required)
        if not rule_records:
            raise TerminationRefusal("RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RULE", rr["ruleId"])
        records += rule_records
    return cset(records)


def _originating(record):
    covs = [r["digest"] for r in record["inputRefs"] if r["domain"] == "coverage"]
    if record["source"] == "execution":
        return ["coverage2:" + h for h in covs]
    if record["source"] == "native" and len(record["inputRefs"]) == 1 and len(covs) == 1:
        return ["coverage2:" + covs[0]]
    return []


def conditions(g, records):
    """s4 record and stage-terminal conditions with their declared and stage carriers."""
    out = []
    for rec in records:
        rank, d9 = bridge(rec["cause"])
        origin = _originating(rec)
        for cid in origin:
            if cid not in g["coverages"]:
                raise TerminationRefusal("cb24.RUN_TERMINATION_ORIGINATING_COVERAGE_UNADMITTED", cid)
        declared = [c for c in origin if g["coverages"][c][1]["entry"]["deficiency"] == rec["cause"]]
        out.append({"kind": "record", "cause": rec["cause"], "rank": rank, "d9": d9, "declared": declared, "stage": []})
        for cid in origin:
            terminal = g["coverages"][cid][1]["entry"]["resolutionCompleteness"]["stageTerminal"]
            if terminal in STAGE_TERMINAL:
                cause = STAGE_TERMINAL[terminal]
                rank, d9 = bridge(cause)
                out.append({"kind": "stage-terminal", "cause": cause, "rank": rank, "d9": d9, "declared": [], "stage": [cid]})
    return out


def derive(g, store, run_id, records=None):
    """The analysis projection of a committed Run (s1 class, s3-s5)."""
    verdict = g["proof"]["verdict"]
    if verdict == "pass":
        return {"projection": {"class": "success", "runId": run_id}, "deficiency": None, "secondaryDeficiencies": [], "population": [], "conditions": []}
    if verdict == "fail":
        return {"projection": {"class": "policy-failed", "runId": run_id}, "deficiency": None, "secondaryDeficiencies": [], "population": [], "conditions": []}
    records = population(g, store) if records is None else records
    if not records:
        raise TerminationRefusal("RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RUN", run_id)
    conds = conditions(g, records)
    least = {}
    for c in conds:
        least[c["d9"]] = min(least.get(c["d9"], len(PRECEDENCE) + 1), c["rank"])
    order = sorted(least, key=lambda d: least[d])
    primary_rank = least[order[0]]
    at_primary = [c for c in conds if c["rank"] == primary_rank]
    declared = sorted({x for c in at_primary for x in c["declared"]}, key=lambda s: s.encode())
    stage = sorted({x for c in at_primary for x in c["stage"]}, key=lambda s: s.encode())
    projection = {"class": "indeterminate", "runId": run_id, "reasonCodes": [TO_REASON[d] for d in order]}
    if declared or stage:
        projection["coverageId"] = (declared or stage)[0]
    return {"projection": projection, "deficiency": order[0], "secondaryDeficiencies": order[1:], "population": records,
            "conditions": conds, "primaryRank": primary_rank}


def step_termination_shape_ok(candidate):
    return KIT.admit(candidate, COMMON3, "#/$defs/StepTermination")["ok"]


def check_projection(candidate, derived, validate=None):
    """s6 candidate check, refusals in the published order."""
    if not isinstance(candidate, dict):
        return {"admitted": False, "refusal": "RUN_TERMINATION_CANDIDATE_NOT_OBJECT"}
    if set(candidate) - GOVERNED - DELEGATED:
        return {"admitted": False, "refusal": "RUN_TERMINATION_UNKNOWN_FIELD", "members": sorted(set(candidate) - GOVERNED - DELEGATED)}
    if {k: v for k, v in candidate.items() if k in GOVERNED} != derived["projection"]:
        return {"admitted": False, "refusal": "RUN_TERMINATION_NOT_DERIVED"}
    delegated = sorted(set(candidate) & DELEGATED)
    if delegated and validate is None:
        return {"admitted": False, "refusal": "RUN_TERMINATION_DELEGATED_SHAPE_UNCHECKED"}
    if delegated and not validate(candidate):
        return {"admitted": False, "refusal": "RUN_TERMINATION_DELEGATED_SHAPE"}
    return {"admitted": True, "delegated": {k: "owner-validation-required" for k in delegated}}


def commit_inventory(run_id, object_ids, blob_digests):
    record = {"schemaVersion": 2, "runId": run_id, "objects": sorted(set(object_ids), key=K.C), "blobDigests": sorted(set(blob_digests), key=K.C)}
    return record, K.raw_digest(record)


def select_detail(derived, g, closure_not_installed):
    """s7.5 closed allowlist: the first row whose prerequisites hold, else none."""
    proj = derived["projection"]
    if proj["class"] != "indeterminate":
        return None
    if any(r["cause"] == "work-budget-exhausted" for r in derived["population"]) and derived["deficiency"] == "budget-exhausted":
        return "EVALUATION.WORK_BUDGET_EXHAUSTED"
    if proj["reasonCodes"][0] == "COVERAGE.PROVIDER_UNAVAILABLE" and closure_not_installed is True:
        return "COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED"
    cid = proj.get("coverageId")
    if cid is not None and g["coverages"][cid][1]["entry"]["deficiency"] in ROW3:
        return g["coverages"][cid][1]["entry"]["deficiency"]
    return None


def admit_step_termination(candidate, g, store, run_id, published, observation):
    """s7.6 admit_analysis_step_termination. published: (object ids, blob digests) of the Run's commit. observation: {attempts,
    durability, receipt, requiredClosureNotInstalled} from the trusted host finalizer."""
    def refuse(key, detail=""):
        return {"admitted": False, "refusal": key, "detail": detail}
    if not isinstance(candidate, dict):
        return refuse("RUN_TERMINATION_CANDIDATE_NOT_OBJECT")
    if candidate.get("class") in NOT_COMPOSED:
        return {"admitted": None, "owner": "D9 v1.14 causeModel / workflows-and-surfaces s1 and s9 / security S12 / native s10 route registry"}
    attempts, durability = observation.get("attempts"), observation.get("durability")
    receipt, installed_flag = observation.get("receipt"), observation.get("requiredClosureNotInstalled")
    if not isinstance(attempts, list) or not attempts or durability not in ("authoritative", "ephemeral") or \
            not isinstance(installed_flag, bool) or any(not KIT.admit(a, INVOC3, "#/$defs/Attempt")["ok"] for a in attempts) or \
            (receipt is not None and not KIT.admit(receipt, ID, "#/$defs/commit-receipt")["ok"]):
        return refuse("RUN_TERMINATION_OBSERVATION_SHAPE")
    ids = [a["executionId"] for a in attempts]
    if len(set(ids)) != len(ids):
        return refuse("RUN_TERMINATION_ATTEMPT_ID_REUSED")
    last = attempts[-1]
    if last["outcome"] != "completed" or any(a["outcome"] == "completed" for a in attempts[:-1]) or "derivation" not in last:
        return refuse("RUN_TERMINATION_ATTEMPT_NOT_TERMINATING")
    if durability == "ephemeral":
        if "runId" in candidate:
            return refuse("RUN_TERMINATION_EPHEMERAL_NOT_COMMITTED_RUN")
        if candidate.get("authority") != "ephemeral":
            return refuse("RUN_TERMINATION_EPHEMERAL_AUTHORITY_REQUIRED")
        if "executionId" in candidate and candidate["executionId"] != last["executionId"]:
            return refuse("RUN_TERMINATION_EXECUTION_ID_NOT_ATTEMPT")
        if "domainDetail" in candidate:
            return refuse("RUN_TERMINATION_DETAIL_NOT_ADMITTED")
        return {"admitted": True, "branch": "ephemeral", "reasonsAdmittedHere": False}
    try:
        derived = derive(g, store, run_id)
    except TerminationRefusal as exc:
        return refuse(exc.key, exc.detail)
    if receipt is None:
        return refuse("RUN_TERMINATION_OBSERVATION_SHAPE", "committed Run without receipt")
    if receipt["runId"] != run_id:
        return refuse("RUN_TERMINATION_RECEIPT_RUN_MISMATCH")
    if receipt["executionId"] != last["executionId"]:
        return refuse("RUN_TERMINATION_RECEIPT_ATTEMPT_MISMATCH")
    if receipt["inventoryDigest"] != commit_inventory(run_id, *published)[1]:
        return refuse("RUN_TERMINATION_RECEIPT_INVENTORY_MISMATCH")
    binding = last["derivation"]
    if binding["planId"] != g["plan_id"]:
        return refuse("RUN_TERMINATION_ATTEMPT_PLAN_MISMATCH")
    if binding["executionPlanId"] != g["seal"]["executionPlanId"]:
        return refuse("RUN_TERMINATION_ATTEMPT_EXECUTION_PLAN_MISMATCH")
    stages = store.get_object(g["seal"]["executionPlanId"])["stages"]
    if binding["stageCount"] != len(stages):
        return refuse("RUN_TERMINATION_ATTEMPT_STAGE_COUNT_MISMATCH")
    if binding["stagesCompleted"] > binding["stageCount"] or \
            ("firstFailedStage" in binding and binding["firstFailedStage"] not in {s["ordinal"] for s in stages}):
        return refuse("RUN_TERMINATION_ATTEMPT_STAGE_PROGRESS_MISMATCH")
    checked = check_projection(candidate, derived, validate=step_termination_shape_ok)
    if not checked["admitted"]:
        return dict(checked, derived=derived["projection"])
    if "authority" in candidate:
        return refuse("RUN_TERMINATION_AUTHORITY_NOT_COMPOSED")
    if "executionId" in candidate and candidate["executionId"] != last["executionId"]:
        return refuse("RUN_TERMINATION_EXECUTION_ID_NOT_ATTEMPT")
    selected = select_detail(derived, g, installed_flag)
    detail = candidate.get("domainDetail")
    if selected is None and detail is not None:
        return refuse("RUN_TERMINATION_DETAIL_NOT_ADMITTED", detail.get("code", ""))
    if selected is not None:
        if detail is None:
            return refuse("RUN_TERMINATION_DETAIL_REQUIRED", selected)
        if detail.get("code") != selected:
            return refuse("RUN_TERMINATION_DETAIL_NOT_ADMITTED", detail.get("code", ""))
        if set(detail) - {"code", "remedy"}:
            return refuse("RUN_TERMINATION_DETAIL_MEMBER_NOT_ADMITTED", ",".join(sorted(set(detail) - {"code", "remedy"})))
    return {"admitted": True, "branch": "committed", "projection": derived["projection"], "selectedDetail": selected,
            "deficiency": derived["deficiency"], "secondaryDeficiencies": derived["secondaryDeficiencies"]}
