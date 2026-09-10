"""Bounded clarification probe for consumer-b.v2 finding G8 / S-4 (plan.budget).

Reads ONLY the frozen original kit at
  /tmp/opensip-design-corrections/consumer-b.v2/subject
and imports (read-only, never runs the mains of) the frozen original tools at
  /tmp/opensip-design-corrections/consumer-b.v2/output/work
Writes ONLY under /tmp/opensip-design-corrections/consumer-b.v2-clarification.

No original kit, output, review or work file is edited.
"""

import copy
import hashlib
import json
import os
import sys

ORIG = "/tmp/opensip-design-corrections/consumer-b.v2"
SUBJECT = os.path.join(ORIG, "subject")
TOOLS = os.path.join(ORIG, "output", "work")
OUT = "/tmp/opensip-design-corrections/consumer-b.v2-clarification"

sys.path.insert(0, TOOLS)
import osref as O                      # noqa: E402  (frozen original tool)
from osref import C, H, REC, Refuse    # noqa: E402
import graph as G                      # noqa: E402
import build as B                      # noqa: E402
import closure as CL                   # noqa: E402

IDENTITY_REL = "docs/coop/design-corrections/foundation/identity-schemas.v2.json"
RESULT = {}


# ------------------------------------------------------------ 1. custody ----

def custody():
    manifest = json.load(open(os.path.join(SUBJECT, "consumer-input-manifest.json")))
    row = [f for f in manifest["files"] if f["path"] == IDENTITY_REL][0]
    raw = open(os.path.join(SUBJECT, IDENTITY_REL), "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    return {
        "selector": IDENTITY_REL + " #/$defs/plan/properties/budget",
        "declaredSha256": row["sha256"],
        "recomputedSha256": got,
        "declaredBytes": row["bytes"],
        "actualBytes": len(raw),
        "exactMatch": got == row["sha256"] and len(raw) == row["bytes"],
        "manifestSelfSha256": hashlib.sha256(
            open(os.path.join(SUBJECT, "consumer-input-manifest.json"), "rb").read()
        ).hexdigest(),
        "sourceIsTheSameFrozenKitAsTheOriginalReview": True,
    }


# --------------------------------------------- 2. the exact frozen bytes ----

def frozen_subschema():
    ident = json.load(open(os.path.join(SUBJECT, IDENTITY_REL)))
    plan_budget = ident["$defs"]["plan"]["properties"]["budget"]
    cfg_budget = (ident["$defs"]["semantic-configuration"]["properties"]["analysis"]
                  ["properties"]["budget"])
    return {
        "planBudgetSchema": plan_budget,
        "semanticConfigurationAnalysisBudgetSchema": cfg_budget,
        "planBudgetIsClosed": plan_budget.get("additionalProperties") is False,
        "planBudgetRequired": plan_budget.get("required"),
        "planBudgetUnitConst": plan_budget["properties"]["unit"].get("const"),
        "planBudgetLimitBounds": {
            "type": plan_budget["properties"]["limit"].get("type"),
            "minimum": plan_budget["properties"]["limit"].get("minimum"),
            "maximum": plan_budget["properties"]["limit"].get("maximum"),
        },
        "twoSubschemasAreByteIdentical":
            json.dumps(plan_budget, sort_keys=True) == json.dumps(cfg_budget, sort_keys=True),
    }


# ------------------------------- 3. discriminating admission matrix ---------

def discriminating_matrix():
    """Exercise plan.budget IN SITU inside the whole #/$defs/plan record, not
    just the subschema, so nothing depends on how the subschema is quoted."""
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    ident = json.load(open(os.path.join(SUBJECT, IDENTITY_REL)))
    registry = Registry().with_resource(ident["$id"], Resource.from_contents(ident))
    schema = dict(ident)
    schema["$ref"] = "#/$defs/plan"
    validator = Draft202012Validator(schema, registry=registry)

    store = G.Store()
    part = B.build_typescript(store)
    g = B.assemble_run(store, part)
    base_plan = copy.deepcopy(g["plan"])

    cases = [
        ("valid-unit-limit", {"unit": "work-units", "limit": 100000}, "ADMIT"),
        ("valid-limit-minimum-1", {"unit": "work-units", "limit": 1}, "ADMIT"),
        ("valid-limit-maximum", {"unit": "work-units", "limit": 9007199254740991}, "ADMIT"),
        ("empty-object", {}, "REFUSE"),
        ("missing-unit", {"limit": 100000}, "REFUSE"),
        ("missing-limit", {"unit": "work-units"}, "REFUSE"),
        ("extra-key", {"unit": "work-units", "limit": 100000, "extra": 1}, "REFUSE"),
        ("wrong-unit-const", {"unit": "seconds", "limit": 100000}, "REFUSE"),
        ("limit-zero", {"unit": "work-units", "limit": 0}, "REFUSE"),
        ("limit-negative", {"unit": "work-units", "limit": -1}, "REFUSE"),
        ("limit-above-maximum", {"unit": "work-units", "limit": 9007199254740992}, "REFUSE"),
        ("limit-boolean-true", {"unit": "work-units", "limit": True}, "REFUSE"),
        ("limit-string", {"unit": "work-units", "limit": "100000"}, "REFUSE"),
        ("unit-boolean", {"unit": True, "limit": 100000}, "REFUSE"),
        ("budget-is-an-array", [{"unit": "work-units", "limit": 1}], "REFUSE"),
        ("budget-is-null", None, "REFUSE"),
    ]
    rows = []
    disagreements = []
    for name, value, expected in cases:
        candidate = copy.deepcopy(base_plan)
        candidate["budget"] = value
        errs = sorted(validator.iter_errors(candidate), key=lambda e: e.json_path)
        outcome = "ADMIT" if not errs else "REFUSE"
        rows.append({"case": name, "budget": value, "expected": expected,
                     "observed": outcome, "agrees": outcome == expected,
                     "firstError": (errs[0].message[:180] if errs else None)})
        if outcome != expected:
            disagreements.append(name)

    # The float-spelled integer is a LEXICAL refusal that precedes schema
    # validation (admission-and-qualification section 1); JSON Schema alone
    # would treat 1.0 as integer-valued, so this case is shown separately.
    lexical = {}
    for name, text in (("limit-float-spelled-1.0", '{"unit":"work-units","limit":1.0}'),
                       ("limit-exponent-1e5", '{"unit":"work-units","limit":1e5}'),
                       ("duplicate-limit-key",
                        '{"unit":"work-units","limit":1,"limit":2}')):
        try:
            O.parse(text)
            lexical[name] = "ADMITTED (unexpected)"
        except Refuse as exc:
            lexical[name] = exc.code + (":" + exc.detail if exc.detail else "")

    return {"validatedAgainst": IDENTITY_REL + " #/$defs/plan (whole record)",
            "cases": rows,
            "casesTotal": len(rows),
            "casesAgreeingWithExpectation": sum(1 for r in rows if r["agrees"]),
            "disagreements": disagreements,
            "lexicalAdmissionPrecedingSchema": lexical}


# ------------- 4. does any REAL budget issue remain?  Actual reproducer -----

def residual_probe():
    """The only budget-family observation I can actually reproduce: the Plan
    carries `budget` inline AND commits `resolvedConfigDigest`, whose
    semantic-configuration carries a byte-identical `analysis.budget` record,
    and no contract sentence states the two must agree."""
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    ident = json.load(open(os.path.join(SUBJECT, IDENTITY_REL)))
    registry = Registry().with_resource(ident["$id"], Resource.from_contents(ident))
    schema = dict(ident)
    schema["$ref"] = "#/$defs/plan"
    validator = Draft202012Validator(schema, registry=registry)

    store = G.Store()
    part = B.build_typescript(store)
    g = B.assemble_run(store, part)

    # The resolved semantic configuration this Plan commits to:
    cfg = json.loads(store.objects[g["plan"]["resolvedConfigDigest"]].decode())
    cfg_budget = cfg["analysis"]["budget"]

    plan_a = copy.deepcopy(g["plan"])                      # budget == config budget
    plan_b = copy.deepcopy(g["plan"])
    plan_b["budget"] = {"unit": "work-units", "limit": 7}  # disagrees with the config

    valid_a = not list(validator.iter_errors(plan_a))
    valid_b = not list(validator.iter_errors(plan_b))
    id_a = "plan2:" + H("plan", plan_a)
    id_b = "plan2:" + H("plan", plan_b)

    return {
        "observation": "plan.budget and semantic-configuration.analysis.budget are "
                       "two byte-identical closed records carrying the same value, "
                       "and the Plan commits BOTH (the field inline and the "
                       "configuration by resolvedConfigDigest). No sentence in the "
                       "five contracts states they must agree.",
        "exactSelectors": [
            IDENTITY_REL + " #/$defs/plan/properties/budget",
            IDENTITY_REL + " #/$defs/plan/properties/resolvedConfigDigest",
            IDENTITY_REL + " #/$defs/semantic-configuration/properties/analysis/properties/budget",
            "identity-and-evidence.md section 3 closure list "
            "('Snapshot config/scope, Plan config/scope and native-context source "
            "correspondence must agree.' -- names config and scope; budget is not named)",
            "admission-and-qualification.md section 1.1 ('analysis always contains "
            "profileId, capabilities and the complete {unit,limit} budget supplied by "
            "the authenticated compiled defaults and then overridden by admitted layers')",
        ],
        "reproducer": {
            "resolvedConfigDigest": g["plan"]["resolvedConfigDigest"],
            "configuredBudget": cfg_budget,
            "planA_budget": plan_a["budget"],
            "planB_budget": plan_b["budget"],
            "planA_schemaValid": valid_a,
            "planB_schemaValid": valid_b,
            "planA_id": id_a,
            "planB_id": id_b,
            "twoDistinctPlanIdsForOneResolvedConfiguration": id_a != id_b,
            "bothCloseUnderTheOriginalClosureChecker": None,  # filled below
        },
        "countervailingReading": "A per-invocation narrowing of the configured "
                                 "budget is a plausible intended meaning, and either "
                                 "way the Plan is deterministic and replayable "
                                 "because both values enter PlanId. This is why the "
                                 "item is advisory and not a MUST or SHOULD.",
        "severity": "advisory",
        "doesNotRestoreG8": True,
    }


def close_both(residual):
    """Confirm both Plans really do close, so the reproducer is not theoretical."""
    outcomes = {}
    for label, limit in (("planA-config-agreeing", None), ("planB-disagreeing", 7)):
        store = G.Store()
        part = B.build_typescript(store)
        if limit is not None:
            saved = B.assemble_run

            def patched(store_, part_, _limit=limit):
                res = saved(store_, part_)
                plan = copy.deepcopy(res["plan"])
                plan["budget"] = {"unit": "work-units", "limit": _limit}
                pid = "plan2:" + store_.put_frame("plan", plan, "budget-variant")
                return res, plan, pid
            res, plan, pid = patched(store, part)
            # rebuild the graph around the variant Plan so nothing is stale
            outcomes[label] = _rebuild_and_close(store, part, res, plan, pid)
        else:
            g = B.assemble_run(store, part)
            try:
                CL.close_run(store, g["runId"], "typescript")
                outcomes[label] = {"closes": True, "planId": g["planId"],
                                   "runId": g["runId"]}
            except Refuse as exc:
                outcomes[label] = {"closes": False, "refusal": exc.code}
    residual["reproducer"]["bothCloseUnderTheOriginalClosureChecker"] = outcomes
    return residual


def _rebuild_and_close(store, part, res, plan, pid):
    """Re-key every descriptor that names the Plan, so only the budget differs."""
    try:
        # subject scope / coverage / fact are Plan-independent; view, exec-plan,
        # stage-spec, proof, evidence, seal and run all name the Plan.
        stage = copy.deepcopy(res["stageSpec"]); stage["planId"] = pid
        stage_digest = store.put_record(stage, "stage-spec")
        ep = copy.deepcopy(res["execPlan"]); ep["planId"] = pid
        ep["stages"][0]["stageSpecDigest"] = stage_digest
        epid = "exec-plan2:" + store.put_frame("execution-plan", ep, "variant")
        view = copy.deepcopy(res["view"]); view["planId"] = pid
        vid = "view2:" + store.put_frame("view", view, "variant")
        proof = copy.deepcopy(res["proof"])
        proof["planId"] = pid
        proof["executionPlanId"] = epid
        proof["evaluationInputRefs"] = sorted(
            [r for r in proof["evaluationInputRefs"] if r["domain"] != "view"]
            + [{"domain": "view", "digest": vid.split(":", 1)[1]}], key=lambda r: C(r))
        proof["predicateProofs"][0]["inputRefs"] = sorted(
            [r for r in proof["predicateProofs"][0]["inputRefs"] if r["domain"] != "view"]
            + [{"domain": "view", "digest": vid.split(":", 1)[1]}], key=lambda r: C(r))
        prid = "proof2:" + store.put_frame("proof-bundle", proof, "variant")
        ev = copy.deepcopy(res["evidence"])
        ev.update(planId=pid, viewIds=[vid], proofBundleId=prid)
        eid = "evidence2:" + store.put_frame("semantic-evidence", ev, "variant")
        seal = copy.deepcopy(res["seal"])
        seal.update(planId=pid, executionPlanId=epid, evidenceId=eid, proofBundleId=prid)
        sid = "seal2:" + store.put_frame("evaluation-seal", seal, "variant")
        run = copy.deepcopy(res["run"])
        run.update(planId=pid, evidenceId=eid, evaluationSealId=sid)
        rid = "run2:" + store.put_frame("run", run, "variant")
        CL.close_run(store, rid, "typescript")
        return {"closes": True, "planId": pid, "runId": rid}
    except Refuse as exc:
        return {"closes": False, "refusal": exc.code + ":" + exc.detail}


# ------------------------------------------------------------ 5. verdict ----

def main():
    RESULT["clarificationOf"] = {
        "originalReview": "/tmp/opensip-design-corrections/consumer-b.v2/output/blind-review.json",
        "retainedImmutableAt": "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/"
                               "design-corrections/reviews/consumer-b.v2/",
        "findingIds": ["G8", "S-4"],
        "alsoCorrects": "blind-review.json invented[] row 'plan.budget = "
                        "{unit: work-units, limit: 100000}'",
    }
    RESULT["inputCustody"] = custody()
    RESULT["frozenSubschema"] = frozen_subschema()
    RESULT["discriminatingCheck"] = discriminating_matrix()
    RESULT["residualBudgetObservation"] = close_both(residual_probe())
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "clarification-probe.json"), "w") as fh:
        json.dump(RESULT, fh, indent=1)
        fh.write("\n")

    d = RESULT["discriminatingCheck"]
    print("custody exact:", RESULT["inputCustody"]["exactMatch"])
    print("plan.budget closed:", RESULT["frozenSubschema"]["planBudgetIsClosed"],
          "required:", RESULT["frozenSubschema"]["planBudgetRequired"])
    print("identical to config budget:",
          RESULT["frozenSubschema"]["twoSubschemasAreByteIdentical"])
    print("matrix: %d/%d agree, disagreements=%s"
          % (d["casesAgreeingWithExpectation"], d["casesTotal"], d["disagreements"]))
    for r in d["cases"]:
        print("   %-28s %-7s %s" % (r["case"], r["observed"],
                                    "" if r["agrees"] else "<< UNEXPECTED"))
    print("lexical:", d["lexicalAdmissionPrecedingSchema"])
    rp = RESULT["residualBudgetObservation"]["reproducer"]
    print("residual reproducer: distinct PlanIds:",
          rp["twoDistinctPlanIdsForOneResolvedConfiguration"],
          "closures:", {k: v["closes"] for k, v in
                        rp["bothCloseUnderTheOriginalClosureChecker"].items()})


if __name__ == "__main__":
    main()
