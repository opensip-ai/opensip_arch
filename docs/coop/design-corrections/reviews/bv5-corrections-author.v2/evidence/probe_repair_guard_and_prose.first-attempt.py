"""CX-BV5-02 / CX-BV5-03 / CX-BV5-05 / CX-BV5-06 / CX-BV5-07 controls, plus BV5A-NEW-2.

  * repair: the guard is EVERY delete and EVERY replace; the fixture now carries the full
    seven-member native record; dynamicDispatch is not a global veto.
  * analysis-spec ordering: which inputs reach the schema step, and that the two routes are NOT
    the same public termination.
  * path enforcement: three distinct enforcements, accepted sets unchanged.
  * the Windows citation and the same-observation wording.

Usage: /tmp/opensip-architecture-review-env/bin/python -I -B probe_repair_guard_and_prose.py <work-root>
"""
from __future__ import annotations

import copy
import glob
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
DC = ROOT / "docs/coop/design-corrections"
WF = DC / "workflows"
sys.path.insert(0, str(DC / "foundation"))
import canonical  # noqa: E402
from jsonschema import Draft202012Validator, ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

spec = importlib.util.spec_from_file_location("workflows_model", WF / "workflows_model.v1.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
nspec = importlib.util.spec_from_file_location("nm", DC / "native/native_evidence_model.v2.py")
N = importlib.util.module_from_spec(nspec)
nspec.loader.exec_module(N)

SCHEMAS = {}
for p in sorted(glob.glob(str(WF / "schemas" / "*.schema.json"))):
    s = canonical.parse(Path(p).read_bytes())
    Draft202012Validator.check_schema(s)
    SCHEMAS[s["$id"]] = s
FND = canonical.parse((DC / "foundation/identity-schemas.v2.json").read_bytes())
REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
    + [(FND["$id"], Resource(contents=FND, specification=DRAFT202012))])
U = "urn:opensip:product-v1:workflows:"
NATIVE_SCHEMAS = json.loads((DC / "native/native-evidence.schemas.v2.json").read_text(encoding="utf-8"))
CASES = json.loads((WF / "workflow-cases.v1.json").read_text(encoding="utf-8"))
RS, CONST = CASES["repairScenario"], CASES["constants"]
WF_MD = (ROOT / "docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_text(encoding="utf-8")
NATIVE_MD = (ROOT / "docs/v2/contracts/product-v1/native-evidence.md").read_text(encoding="utf-8")
SECURITY_MD = (ROOT / "docs/v2/contracts/product-v1/security-and-lifecycle.md").read_text(encoding="utf-8")
MATRIX = json.loads((DC / "native/native-capability-matrix.v2.json").read_text(encoding="utf-8"))
DOMAINS = json.loads((DC / "native/capability-manifest-domains.v2.json").read_text(encoding="utf-8"))
REPAIR = json.loads((WF / "schemas/repair.schema.json").read_text(encoding="utf-8"))

out = {"probe": "repair-guard-ordering-paths-and-citations", "checks": [], "failures": []}


def check(name, condition, **detail):
    out["checks"].append({"check": name, "ok": bool(condition), **detail})
    if not condition:
        out["failures"].append(name)


def subst(v):
    if isinstance(v, str) and v.startswith("$") and v[1:] in CONST:
        return copy.deepcopy(CONST[v[1:]])
    if isinstance(v, dict):
        return {k: subst(x) for k, x in v.items()}
    if isinstance(v, list):
        return [subst(x) for x in v]
    return v


RECIPE = subst(RS["recipe"])
FULL_DENIED = {"exportsClosed": "open", "entryPointsRecognized": "partial",
               "nonliteralLoading": "present", "externalConsumers": "possible",
               "dynamicDispatch": "present", "reasons": ["nonliteral-loading-present"],
               "deadCodeRepairEligible": False}
FULL_ELIGIBLE = dict(RS["run"]["closedWorld"])


def preview(closed_world, edits, origin="native-analysis"):
    tree = {k: v.encode() for k, v in RS["tree"].items()}
    run = dict(RS["run"], closedWorld=copy.deepcopy(closed_world), evidenceOrigin=origin,
               snapshotId=M.tree_snapshot_id(CONST["PRJ"], tree), runId=CONST["RUN0"],
               planId=CONST["PLAN0"], findings=[CONST["FP1"], CONST["FP2"]])
    return M.repair_preview(CONST["PRJ"], tree, run, RECIPE, [CONST["FP1"]], edits,
                            RS["evidenceRequirements"], list(RS["permittedScope"]),
                            {CONST["PROD"]: "admitted"})


# ---- BV5A-NEW-2: the fixture now carries the full native record ------------------------------
check("the workflow repair fixture's evidence closedWorld is now the full seven-member record",
      sorted(RS["run"]["closedWorld"]) == sorted(NATIVE_SCHEMAS["$defs"]["ClosedWorldV2"]["required"]),
      fixture=sorted(RS["run"]["closedWorld"]))
check("the not-eligible case fixture carries it too",
      sorted(RS["cases"][18]["closedWorld"]) == sorted(NATIVE_SCHEMAS["$defs"]["ClosedWorldV2"]["required"]))
check("the workflow helper docstring states the admitted-input assumption",
      "ALREADY ADMITTED by the owning native contract" in (WF / "workflows_model.v1.py").read_text(encoding="utf-8"))

# ---- CX-BV5-03: the guard covers EVERY delete and EVERY replace -------------------------------
check("UNSAFE_ACTIONS is exactly delete and replace, unqualified",
      M.UNSAFE_ACTIONS == {"delete", "replace"}, actions=sorted(M.UNSAFE_ACTIONS))
delete_only = [{"path": "src/a.ts", "action": "delete"}]
replace_only = [{"path": "src/b.ts", "action": "replace", "postimage": b"export const b = 3;\n"}]
create_only = [{"path": "src/new.ts", "action": "create", "postimage": b"export const n = 1;\n"}]
for label, edits, expect_applicable in [("delete-only", delete_only, False),
                                        ("replace-only", replace_only, False),
                                        ("create-only", create_only, True)]:
    plan = preview(FULL_DENIED, edits)
    codes = [u["code"] for u in plan["descriptor"]["unmetPreconditions"]]
    check("a " + label + " plan under a denying record is " +
          ("applicable" if expect_applicable else "guarded"),
          plan["descriptor"]["applicable"] is expect_applicable
          and (expect_applicable or "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED" in codes), codes=codes)
check("workflows section 6 no longer narrows replace to exported subjects",
      "`replace` of an exported subject" not in WF_MD
      and "every `delete` and every `replace` edit" in WF_MD)
check("workflows section 6 states dynamicDispatch is target-relative, not a global veto",
      "not** a global veto" in WF_MD and "affected_targets" in WF_MD
      and "target-relative" in WF_MD)
check("workflows section 6 states the projection grants no evidence authority",
      "projection grants no evidence authority of its own" in WF_MD)
check("the repair schema description carries the same two corrections",
      "EVERY delete and EVERY replace" in REPAIR["$defs"]["RepairPlanDescriptor"]["properties"]["closedWorld"]["description"]
      and "NOT a global veto" in REPAIR["$defs"]["RepairPlanDescriptor"]["properties"]["closedWorld"]["description"])

# dynamicDispatch=present alone, with an otherwise eligible record, must not veto
dyn = dict(FULL_ELIGIBLE, dynamicDispatch="present")
plan = preview(dyn, delete_only)
check("dynamicDispatch=present alone does not veto an otherwise eligible unsafe repair",
      plan["descriptor"]["applicable"] is True,
      unmet=plan["descriptor"]["unmetPreconditions"], closedWorld=dyn)
ok, why = (lambda ref, value: (lambda sid, frag: (
    (True, "") if not _validate(sid, frag, value) else (False, "")))(*ref.split("#")))if False else (None, None)


def valid(ref, value):
    sid, _, frag = ref.partition("#")
    try:
        canonical.typed(value)
        canonical.ExactValidator({"$ref": sid + "#" + frag}, registry=REG).validate(value)
        return True, ""
    except (ValidationError, canonical.AdmissionError) as exc:
        return False, str(exc).splitlines()[0][:200]


schema_ok, why = valid(U + "repair#/$defs/RepairPlanV1", plan)
check("the plan still validates against the repair schema", schema_ok, why=why)
check("the descriptor projection is still exactly five members",
      sorted(plan["descriptor"]["closedWorld"]) == sorted(
          ["deadCodeRepairEligible", "exportsClosed", "entryPointsRecognized",
           "nonliteralLoading", "externalConsumers"]))

# ---- CX-BV5-02: which inputs reach the schema step, and the two routes ------------------------
cell = next(c for c in MATRIX["cells"] if c["state"] != "NOT-SELECTED")
row = {"capabilityId": cell["capability"], "languageMode": cell["mode"],
       "workspaceRoot": ".", "required": False}


def admit_spec(requested, break_schema=False):
    s = {"schemaVersion": 2, "requestedCapabilities": requested,
         "policyPackIds": [], "parameters": []}
    if break_schema:
        del s["schemaVersion"]
    try:
        N.admit_analysis_spec(s)
        return {"outcome": "ADMIT"}
    except Exception as exc:
        return {"outcome": type(exc).__name__, "detail": str(exc).splitlines()[0][:140]}


in_bound = [dict(row, workspaceRoot="u%04d" % i) for i in range(10)]
over_bound = [dict(row, workspaceRoot="u%04d" % i) for i in range(1034)]
for label, requested, break_schema in [("missing field", None, False), ("null", None, True),
                                       ("a string of 1025 characters", "x" * 1025, False),
                                       ("a boolean", True, False), ("a number", 7, False),
                                       ("an object", {}, False)]:
    s = {"schemaVersion": 2, "requestedCapabilities": requested, "policyPackIds": [], "parameters": []}
    if label == "missing field":
        del s["requestedCapabilities"]
    try:
        N.admit_analysis_spec(s)
        res = {"outcome": "ADMIT"}
    except Exception as exc:
        res = {"outcome": type(exc).__name__, "detail": str(exc).splitlines()[0][:140]}
    check("a wrong-shape requestedCapabilities (" + label + ") reaches the SCHEMA step",
          res["outcome"] == "ValidationError", result=res)
check("an in-bound array that is otherwise malformed reaches the schema step",
      admit_spec(in_bound, break_schema=True)["outcome"] == "ValidationError",
      result=admit_spec(in_bound, break_schema=True))
big = admit_spec(over_bound, break_schema=True)
check("only an ACTUAL array over its bound is preempted by cardinality",
      "Scope" in big["outcome"] or "count>limit" in json.dumps(big), result=big)
check("native prose now scopes the sentence by the CONDITION, not by the bound alone",
      "absent, null, a boolean, a number, a string or an object" in NATIVE_MD
      and "for every input that reaches that step" in NATIVE_MD)
check("native prose no longer flattens the two routes into request-rejected / exit 2",
      "both routes are request-rejected / exit2" not in NATIVE_MD
      and "origin-dependent** routing" in NATIVE_MD
      and "`operational-failed` (4)** / `SYSTEM.OUTCOME.ILLEGAL_STATE` with `faultCause: host-invariant`" in NATIVE_MD)
check("the admit_analysis_spec docstring carries the same two corrections",
      "ORIGIN-DEPENDENT routing" in N.admit_analysis_spec.__doc__
      and "a missing field, a null, a\n    boolean, a number, a string, an object" in N.admit_analysis_spec.__doc__)

# ---- CX-BV5-05: three distinct path enforcements, accepted sets unchanged ---------------------
lp = FND["$defs"]["LogicalPath"]
check("LogicalPath constraints are still byte-identical",
      lp["pattern"] == "^[^/\\\\\\u0000]{1,255}(/[^/\\\\\\u0000]{1,255})*(?![\\s\\S])"
      and lp["not"] == {"pattern": "(^|/)\\.\\.?(/|$)"}
      and lp["minLength"] == 1 and lp["maxLength"] == 4096)
check("the description distinguishes the three enforcements",
      "THREE DIFFERENT ENFORCEMENTS EXIST AND THEY ARE NOT EQUIVALENT" in lp["description"])
check("it no longer claims a snapshot join for the fingerprint field",
      "to NO snapshot join" in lp["description"]
      and "does NOT enforce the per-segment 255 maximum" in lp["description"])
# the imperative check really is what the description says: refuses dot segments, allows long ones
IM = importlib.util.module_from_spec(
    importlib.util.spec_from_file_location("im", DC / "foundation/identity-model.py"))
importlib.util.spec_from_file_location("im", DC / "foundation/identity-model.py").loader.exec_module(IM)
long_segment = "a" * 300
try:
    IM.ordered({"logicalPath": long_segment})
    long_ok = True
except Exception:
    long_ok = False
try:
    IM.ordered({"logicalPath": "a/../b"})
    dot_ok = True
except Exception:
    dot_ok = False
check("measured: ordered() admits a 300-character segment (no per-segment 255 bound there)", long_ok)
check("measured: ordered() refuses a dot-dot segment", not dot_ok)

# ---- CX-BV5-06 / CX-BV5-07: citations and wording -------------------------------------------
plat = DOMAINS["registries"]["PLATFORM-ID-DOMAIN-V1"]["inheritedVocabularyIsBROADERThanTheSelectedPRODUCT"]
check("the Windows citation now names the actual owner (security S8 / native matrix)",
      "admission-and-qualification section 5 item 1" not in plat
      and "security unit's S8 platform table" in plat
      and "native-capability-matrix.v2.json platformFamilies" in plat)
check("the blind review's original citation is recorded as historical, not silently dropped",
      "blind consumer-B v5 review cited" in plat)
check("the four ids still equal the native matrix platformFamilies",
      sorted(MATRIX["platformFamilies"]) == ["linux-aarch64-gnu", "linux-x86_64-gnu",
                                             "macos-aarch64", "macos-x86_64"])
check("S8 is where Windows is actually excluded",
      "Windows) the core" in SECURITY_MD and "refuses rather than degrades" in SECURITY_MD)
check("RC-1 no longer claims two digests for one observation",
      "for one observation of one universe" not in NATIVE_MD
      and "not** a digest collision" in NATIVE_MD
      and "necessarily differ in `attempted` as well as in `state`" in NATIVE_MD)

out["ok"] = not out["failures"]
print(json.dumps(out, indent=1))
sys.exit(0 if out["ok"] else 1)
