"""SHOULD-2 reference control: the ClosedWorldV2 -> RepairPlanDescriptor projection and its authority.

Driven through the HOST functions `repair_preview` / `repair_apply` and the workflow schema
closure, not through a helper. The corrected repair.schema.json description and workflows §6
prose claim:

  * `RepairPlanDescriptor.closedWorld` is the FIVE-field projection of the evidence Run's native
    ClosedWorldV2, dropping `dynamicDispatch` and `reasons`; a literal copy is REFUSED;
  * the destructive-repair gate is decided against the evidence Run's FULL record BEFORE the
    projection is built, and reports the native `reasons`;
  * deleting or editing a field of the descriptor cannot bypass the gate, because the whole
    descriptor is the preimage of `repairPlanId` and apply binds that exact id;
  * `evidenceRunId` is preserved.

Usage: /tmp/opensip-architecture-review-env/bin/python -I -B probe_repair_closed_world_projection.py <work-root>
"""
from __future__ import annotations

import copy
import glob
import importlib.util
import json
import sys
from pathlib import Path

WORK = Path(sys.argv[1]).resolve()
WF = WORK / "docs/coop/design-corrections/workflows"
FOUNDATION_DIR = WORK / "docs/coop/design-corrections/foundation"
NATIVE = WORK / "docs/coop/design-corrections/native"

sys.path.insert(0, str(FOUNDATION_DIR))
import canonical  # noqa: E402
from jsonschema import Draft202012Validator, ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

spec = importlib.util.spec_from_file_location("workflows_model", WF / "workflows_model.v1.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

SCHEMAS = {}
for p in sorted(glob.glob(str(WF / "schemas" / "*.schema.json"))):
    s = canonical.parse(Path(p).read_bytes())
    Draft202012Validator.check_schema(s)
    SCHEMAS[s["$id"]] = s
FND = canonical.parse((FOUNDATION_DIR / "identity-schemas.v2.json").read_bytes())
REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
    + [(FND["$id"], Resource(contents=FND, specification=DRAFT202012))])
U = "urn:opensip:product-v1:workflows:"
NATIVE_SCHEMAS = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))
CASES = json.loads((WF / "workflow-cases.v1.json").read_text(encoding="utf-8"))
RS = CASES["repairScenario"]
CONST = CASES["constants"]

def subst(value):
    """The case file writes constants as $NAME; the reference checker resolves them the same way."""
    if isinstance(value, str) and value.startswith("$") and value[1:] in CONST:
        return copy.deepcopy(CONST[value[1:]])
    if isinstance(value, dict):
        return {k: subst(v) for k, v in value.items()}
    if isinstance(value, list):
        return [subst(v) for v in value]
    return value


RECIPE = subst(RS["recipe"])

out = {"probe": "repair-closed-world-projection-and-authority",
       "host_entry_point": "workflows_model.v1.repair_preview / repair_apply",
       "checks": [], "failures": []}


def check(name, condition, **detail):
    out["checks"].append({"check": name, "ok": bool(condition), **detail})
    if not condition:
        out["failures"].append(name)


def valid(ref, value):
    sid, _, frag = ref.partition("#")
    try:
        canonical.typed(value)
        canonical.ExactValidator({"$ref": sid + "#" + frag}, registry=REG).validate(value)
        return True, ""
    except (ValidationError, canonical.AdmissionError) as exc:
        return False, str(exc).splitlines()[0][:220]


# --- the FULL seven-member native ClosedWorldV2 the native contract closes -------------------
FULL_ELIGIBLE = {"exportsClosed": "closed", "entryPointsRecognized": "all",
                 "nonliteralLoading": "none", "externalConsumers": "none-declared",
                 "dynamicDispatch": "not-applicable", "reasons": [], "deadCodeRepairEligible": True}
FULL_DENIED = {"exportsClosed": "open", "entryPointsRecognized": "partial",
               "nonliteralLoading": "present", "externalConsumers": "possible",
               "dynamicDispatch": "present", "reasons": ["nonliteral-loading-present",
                                                         "entry-points-partial"],
               "deadCodeRepairEligible": False}
PROJECTED = ("deadCodeRepairEligible", "exportsClosed", "entryPointsRecognized",
             "nonliteralLoading", "externalConsumers")

ok, why = valid("urn:opensip:product-v1:native:evidence#/$defs/ClosedWorldV2", FULL_ELIGIBLE) \
    if "urn:opensip:product-v1:native:evidence" in SCHEMAS else (None, "native bundle not in the workflow closure")
check("the seven-member record used here is the native ClosedWorldV2 shape",
      sorted(FULL_ELIGIBLE) == sorted(NATIVE_SCHEMAS["$defs"]["ClosedWorldV2"]["required"]),
      nativeRequired=NATIVE_SCHEMAS["$defs"]["ClosedWorldV2"]["required"])


def preview(closed_world, origin="native-analysis", edits=None, targets=None):
    tree = {k: v.encode() for k, v in RS["tree"].items()}
    run = dict(RS["run"])
    run["closedWorld"] = copy.deepcopy(closed_world)
    run["evidenceOrigin"] = origin
    run["snapshotId"] = M.tree_snapshot_id(CONST["PRJ"], tree)
    run["runId"], run["planId"] = CONST["RUN0"], CONST["PLAN0"]
    run["findings"] = [CONST["FP1"], CONST["FP2"]]
    edits = edits if edits is not None else [
        dict(e, postimage=e["postimage"].encode()) if e.get("postimage") is not None else dict(e)
        for e in RS["edits"]]
    return M.repair_preview(CONST["PRJ"], tree, run, RECIPE,
                            targets if targets is not None else [CONST["FP1"]],
                            edits, RS["evidenceRequirements"], list(RS["permittedScope"]),
                            {CONST["PROD"]: "admitted"}), run


# --- 1. POSITIVE: a valid projection off a full seven-member record --------------------------
plan, run = preview(FULL_ELIGIBLE)
d = plan["descriptor"]
schema_ok, schema_why = valid(U + "repair#/$defs/RepairPlanV1", plan)
check("the plan validates against the workflow repair schema", schema_ok, why=schema_why)
check("descriptor.closedWorld is EXACTLY the five projected members",
      sorted(d["closedWorld"]) == sorted(PROJECTED), got=sorted(d["closedWorld"]))
check("every projected member equals the evidence Run's own value",
      all(d["closedWorld"][k] == FULL_ELIGIBLE[k] for k in PROJECTED), projected=d["closedWorld"])
check("dynamicDispatch and reasons are dropped by the projection",
      "dynamicDispatch" not in d["closedWorld"] and "reasons" not in d["closedWorld"])
check("evidenceRunId is preserved from the evidence Run",
      d["evidenceRunId"] == run["runId"], evidenceRunId=d["evidenceRunId"])
check("the plan with a full eligible closed world is applicable", d["applicable"] is True,
      unmet=d["unmetPreconditions"])

# --- 2. a LITERAL copy of the seven-member record is refused by the repair schema ------------
literal = copy.deepcopy(d)
literal["closedWorld"] = copy.deepcopy(FULL_ELIGIBLE)
lit_ok, lit_why = valid(U + "repair#/$defs/RepairPlanDescriptor", literal)
check("a literal seven-member copy is REFUSED by RepairPlanDescriptor", not lit_ok, refusal=lit_why)
check("the refusal names the two dropped members",
      "dynamicDispatch" in lit_why or "reasons" in lit_why, refusal=lit_why)

# --- 3. AUTHORITY: the gate reads the FULL record before any projection ----------------------
denied_plan, _ = preview(FULL_DENIED)
dd = denied_plan["descriptor"]
codes = [u["code"] for u in dd["unmetPreconditions"]]
check("unsafe edits with a denying full record are NOT applicable", dd["applicable"] is False,
      unmet=dd["unmetPreconditions"])
check("the unmet precondition is REPAIR.CLOSED_WORLD_NOT_ESTABLISHED",
      "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED" in codes, codes=codes)
remedy = next((u["remedy"] for u in dd["unmetPreconditions"]
               if u["code"] == "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED"), "")
check("the remedy carries the native `reasons`, a field the projection does not keep",
      all(r in remedy for r in FULL_DENIED["reasons"]), remedy=remedy)
check("the descriptor still carries only the five projected members after a denial",
      sorted(dd["closedWorld"]) == sorted(PROJECTED))

# --- 4. a DECLARED imported prepared expansion is not authority for an unsafe repair ---------
imported_plan, _ = preview(FULL_ELIGIBLE, origin="imported-prepared-declared")
icodes = [u["code"] for u in imported_plan["descriptor"]["unmetPreconditions"]]
check("imported-prepared-declared origin denies an unsafe repair even when the flag is true",
      imported_plan["descriptor"]["applicable"] is False
      and "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED" in icodes, codes=icodes)

# --- 5. the gate is scoped to unsafe actions: a create-only plan is unaffected ---------------
safe_plan, _ = preview(FULL_DENIED, edits=[{"path": "src/new.ts", "action": "create",
                                            "postimage": b"export const n = 1;\n"}])
check("a create-only plan is applicable under the same denying record (the gate is scoped to "
      "delete/replace)", safe_plan["descriptor"]["applicable"] is True,
      unmet=safe_plan["descriptor"]["unmetPreconditions"])

# --- 6. deleting/editing descriptor fields cannot bypass the gate ----------------------------
forged = copy.deepcopy(denied_plan)
forged["descriptor"]["closedWorld"]["deadCodeRepairEligible"] = True
forged_id = M.wid("repairplan2", "workflow.repair-plan", forged["descriptor"])
check("forging the projected flag moves repairPlanId (the whole descriptor is the preimage)",
      forged_id != denied_plan["repairPlanId"],
      original=denied_plan["repairPlanId"], forged=forged_id)

tree = {k: v.encode() for k, v in RS["tree"].items()}
auth = {"repairPlanId": denied_plan["repairPlanId"], "snapshotId": dd["snapshotId"],
        "projectId": CONST["PRJ"], "live": True, "consentSource": "policy", "ci": False,
        "securityAuthorizationRef": "security.repair-apply-authorization.v1:" + "a" * 64}
try:
    M.repair_apply(forged, {}, dict(tree), CONST["PRJ"], CONST["REQ"], 2, auth, False, "policy",
                   {}, {CONST["PROD"]: "admitted"}, {})
    check("apply of a forged-flag plan refuses", False, note="apply did NOT refuse")
except M.Refusal as r:
    check("apply of a forged-flag plan refuses on the unmet precondition, not on the flag",
          r.detail == "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED", detail=r.detail)

forged2 = copy.deepcopy(forged)
forged2["descriptor"]["applicable"] = True
forged2["descriptor"]["unmetPreconditions"] = []
forged2["repairPlanId"] = M.wid("repairplan2", "workflow.repair-plan", forged2["descriptor"])
try:
    M.repair_apply(forged2, {}, dict(tree), CONST["PRJ"], CONST["REQ"], 2, auth, False, "policy",
                   {}, {CONST["PROD"]: "admitted"}, {})
    check("apply of a fully forged plan under the original authorization refuses", False,
          note="apply did NOT refuse")
except M.Refusal as r:
    check("apply of a fully forged plan refuses: the authorization binds the original repairPlanId",
          r.detail == "REPAIR.CONSENT_NOT_BOUND", detail=r.detail)

# --- 7. honest observation about the reference fixture -------------------------------------
out["observations"] = [{
    "observation": "workflow-cases.v1.json repairScenario.run.closedWorld carries SIX members "
                   "(no dynamicDispatch) and repair_preview does not validate the evidence Run's "
                   "closedWorld against native ClosedWorldV2, so the reference workflow fixture "
                   "does not itself exhibit the seven-member evidence record.",
    "fixtureMembers": sorted(RS["run"]["closedWorld"]),
    "nativeClosedWorldV2Required": sorted(NATIVE_SCHEMAS["$defs"]["ClosedWorldV2"]["required"]),
    "consequenceForThisCorrection": "the corrected prose states the CONTRACT obligation (native "
                                    "§4.5 closes the record at seven and the gate reads it before "
                                    "projection); it does not claim the workflow reference model "
                                    "validates the evidence record. Reported as a new finding.",
}]

out["ok"] = not out["failures"]
print(json.dumps(out, indent=1))
sys.exit(0 if out["ok"] else 1)
