"""CX-BV5-04 / CX-BV5-08 regression control on FULL retained Run closures.

Built on the same shared integration fixture the root probe used
(`docs/coop/design-corrections/integration-fixtures.py`), so each case is a complete re-keyed
reference Run closed through `identity-model.close_run`, not a helper call. It extends the root
probe in three ways the correction needs:

  * it sweeps EVERY registered (relation, rung) pair through the producer boundary, so the new
    RC-0 membership rule is shown to preserve all of them and to refuse only non-pairs;
  * it includes a FACT-FREE coverage entry (empty examined scope), which no fact-admission guard
    can protect;
  * it asserts the two fields RC-1 deliberately leaves free - `stageTerminal` and
    `examinedExhaustive` - still vary on a not-applicable entry.

Usage: /tmp/opensip-architecture-review-env/bin/python -I -B probe_coverage_pair_and_na_law.py <work-root>
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
DC = ROOT / "docs/coop/design-corrections"

spec = importlib.util.spec_from_file_location("bv5_v2_full_graph", DC / "integration-fixtures.py")
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
N, M, C = F.N, F.M, F.C

LADDERS = json.loads((DC / "foundation/relation-payload-schemas.v2.json").read_text(encoding="utf-8"))[
    "x-opensip-relation-registry"]["relations"]
RESOLVED = {"resolved-target", "resolved-binding", "resolved-callee", "checked", "from-resolved-calls"}

out = {"probe": "coverage-pair-membership-and-not-applicable-minting-law",
       "boundariesExercised": ["native.admit_coverage_result_v3 (producer)",
                               "identity-model.close_run -> admit_coverage_result_v3 (retained closure)",
                               "native.subject_scope_descriptor (scope mint)"],
       "fullRunCases": [], "producerSweep": [], "freeFieldControls": [], "checks": [], "failures": []}


def check(name, condition, **detail):
    out["checks"].append({"check": name, "ok": bool(condition), **detail})
    if not condition:
        out["failures"].append(name)


# --------------------------------------------------------------------------------------------
# 1. FULL retained Run closures - the exact four root cases plus a fact-free fifth
# --------------------------------------------------------------------------------------------

def full_run(rung, delta, subjects=None):
    """One complete re-keyed Run, following the root probe's construction exactly."""
    run, objects, blobs = F.build(resolved=True, has_match=True)
    baseline = M.close_run(run, objects, blobs)
    plan = copy.deepcopy(objects[run["planId"]][1])
    analysis = C.parse(blobs[plan["analysisSpecDigest"]])
    request = copy.deepcopy(analysis["requestedCapabilities"][0])
    request["capabilityId"] = "unresolved-edge"
    if request not in analysis["requestedCapabilities"]:
        analysis["requestedCapabilities"].append(request)
    plan["analysisSpecDigest"] = F.put_blob(blobs, F.sort_canonical_sets("analysis-spec", analysis))
    F.rekey_plan(objects, blobs, run, plan)
    scope = copy.deepcopy(next(v for d, v in objects.values() if d == "subject-scope"))
    scope.update(relation="unresolved-edge", resolution=rung)
    if subjects is not None:
        scope["subjects"] = subjects
    sid = M.identifier("subject-scope", scope)
    objects[sid] = ("subject-scope", scope)
    paths = [r["path"] for r in objects[run["snapshotId"]][1]["sourceInventory"]]
    payload = F.coverage_result(scope, scope["sourceUniverse"], True, blobs, paths)
    if subjects is not None:
        payload["key"]["subjectScopeCommitment"] = "sha256:" + sid.split(":", 1)[1]
        payload["entry"]["examinedUniverse"] = {"subjectScopeCommitment": "sha256:" + sid.split(":", 1)[1],
                                                "subjectCount": len(scope["subjects"])}
    payload["entry"]["resolutionCompleteness"].update(delta)
    schema = next(v["payloadSchemaDigest"] for d, v in objects.values() if d == "coverage")
    producer = N.admit_coverage_result_v3(payload, scope, [], schema)
    coverage = {"schemaVersion": 2, "scopeId": sid, "payloadSchemaDigest": schema,
                "payloadDigest": F.put_blob(blobs, payload)}
    cid = M.identifier("coverage", coverage)
    objects[cid] = ("coverage", coverage)
    vid = objects[run["evidenceId"]][1]["viewIds"][0]
    view = copy.deepcopy(objects[vid][1])
    view["scopeIds"].append(sid); view["coverageIds"].append(cid)
    F.rekey(objects, vid, view, run)
    evidence = copy.deepcopy(objects[run["evidenceId"]][1])
    evidence["coverageIds"].append(cid)
    F.rekey(objects, run["evidenceId"], evidence, run)
    F.resync_witness(objects, blobs, run); F.resync_proof_refs(objects, blobs, run)
    # the closure outcome is captured HERE, so a refusal at retained closure does not also discard
    # the producer-boundary result the case is about (first-attempt defect, preserved in evidence/)
    try:
        closure = {"closure": "ADMIT", "runId": M.close_run(run, objects, blobs)}
    except Exception as exc:
        closure = {"closure": "REFUSED", "error": type(exc).__name__ + ":" + str(exc)[:240]}
    return baseline, producer, closure, payload


CASES = [
    ("valid-observed", "observed", {}, None, "ADMIT"),
    ("wrong-cross-relation-rung", "enumerated", {}, None, "REFUSE"),
    ("wrong-attempted", "observed", {"attempted": True}, None, "REFUSE"),
    ("wrong-classes", "observed", {"unresolvedEdgeClasses": ["computed-member-access"]}, None, "REFUSE"),
    # a FACT-FREE entry: empty examined partition, so no unresolved-edge fact could ever guard it
    ("fact-free-cross-relation-rung", "enumerated", {}, [], "REFUSE"),
    ("fact-free-valid-observed", "observed", {}, [], "ADMIT"),
]

for label, rung, delta, subjects, expect in CASES:
    row = {"case": label, "pair": "unresolved-edge@" + rung, "expect": expect,
           "subjectsOverride": subjects}
    try:
        baseline, producer, closure, payload = full_run(rung, delta, subjects)
        row.update(baselineRunId=baseline, producer={"result": producer["result"],
                                                     "faults": [f["fault"] for f in producer["faults"]],
                                                     "refusals": producer["refusals"]},
                   completeness=payload["entry"]["resolutionCompleteness"], **closure)
    except Exception as exc:
        row.update(closure="HARNESS_ERROR", error=type(exc).__name__ + ":" + str(exc)[:240])
    out["fullRunCases"].append(row)
    if expect == "ADMIT":
        check("full retained Run closes for " + label,
              row.get("closure") == "ADMIT" and row.get("producer", {}).get("result") == "ADMIT",
              row=row)
    else:
        check("full retained Run REFUSES for " + label,
              row.get("closure") == "REFUSED" and row.get("producer", {}).get("result") == "REFUSE",
              row=row)

# --------------------------------------------------------------------------------------------
# 2. every registered pair still admits at the producer boundary; only non-pairs refuse
# --------------------------------------------------------------------------------------------
run, objects, blobs = F.build(resolved=True, has_match=True)
base_scope = copy.deepcopy(next(v for d, v in objects.values() if d == "subject-scope"))
schema_digest = next(v["payloadSchemaDigest"] for d, v in objects.values() if d == "coverage")
paths = [r["path"] for r in objects[run["snapshotId"]][1]["sourceInventory"]]


def producer_attempt(relation, rung, delta=None):
    scope = copy.deepcopy(base_scope)
    scope.update(relation=relation, resolution=rung)
    payload = F.coverage_result(scope, scope["sourceUniverse"], True, blobs, paths)
    if delta:
        payload["entry"]["resolutionCompleteness"].update(delta)
    return N.admit_coverage_result_v3(payload, scope, [], schema_digest)


registered = [(r, g) for r in sorted(LADDERS) for g in LADDERS[r]["ladder"]]
for relation, rung in registered:
    res = producer_attempt(relation, rung)
    out["producerSweep"].append({"pair": relation + "@" + rung, "resolved": rung in RESOLVED,
                                 "result": res["result"],
                                 "faults": [f["fault"] for f in res["faults"]],
                                 "refusals": res["refusals"]})
check("every registered (relation, rung) pair still admits at the producer boundary",
      all(r["result"] == "ADMIT" for r in out["producerSweep"]),
      registeredPairs=len(registered),
      refused=[r for r in out["producerSweep"] if r["result"] != "ADMIT"])

non_pairs = [("unresolved-edge", "enumerated"), ("unresolved-edge", "resolved-binding"),
             ("file", "observed"), ("declares", "resolved-callee"), ("clones", "syntactic")]
for relation, rung in non_pairs:
    res = producer_attempt(relation, rung)
    faults = [f["fault"] for f in res["faults"]]
    check("non-pair " + relation + "@" + rung + " refuses on RC-0 membership",
          res["result"] == "REFUSE" and any("RC-0: rung is not a member" in f for f in faults),
          faults=faults)

# the scope descriptor itself refuses a non-pair at mint
try:
    N.subject_scope_descriptor(base_scope["snapshotId"], "unresolved-edge", "enumerated",
                               base_scope["sourceUniverse"], base_scope["targetUniverse"],
                               base_scope["enumeratorClosure"], list(base_scope["subjects"]))
    check("subject_scope_descriptor refuses a non-pair at mint", False, note="it admitted")
except Exception as exc:
    check("subject_scope_descriptor refuses a non-pair at mint",
          "SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER" in str(exc), error=str(exc)[:160])
ok_scope = N.subject_scope_descriptor(base_scope["snapshotId"], "unresolved-edge", "observed",
                                      base_scope["sourceUniverse"], base_scope["targetUniverse"],
                                      base_scope["enumeratorClosure"], list(base_scope["subjects"]))
check("subject_scope_descriptor still mints a registered pair", ok_scope["resolution"] == "observed")

# --------------------------------------------------------------------------------------------
# 3. the fields RC-1 deliberately leaves free, and the rules it must not weaken
# --------------------------------------------------------------------------------------------
for label, delta in [("stageTerminal complete", {"stageTerminal": "complete"}),
                     ("stageTerminal budget-exhausted", {"stageTerminal": "budget-exhausted"}),
                     ("stageTerminal null", {"stageTerminal": None}),
                     ("examinedExhaustive false", {"examinedExhaustive": False})]:
    res = producer_attempt("unresolved-edge", "observed", delta)
    out["freeFieldControls"].append({"variation": label, "result": res["result"],
                                     "faults": [f["fault"] for f in res["faults"]]})
    check("not-applicable keeps a free " + label, res["result"] == "ADMIT",
          faults=[f["fault"] for f in res["faults"]])

res = producer_attempt("references", "resolved-binding", {"state": "not-applicable"})
check("resolved rung still refuses not-applicable (RC-1 not weakened)",
      res["result"] == "REFUSE" and any("resolved rung must not claim" in f["fault"] for f in res["faults"]),
      faults=[f["fault"] for f in res["faults"]])
res = producer_attempt("references", "resolved-binding", {"stageTerminal": "budget-exhausted"})
check("RC-2 not weakened: complete over a non-complete stage still refuses",
      res["result"] == "REFUSE" and any("RC-2" in f["fault"] for f in res["faults"]),
      faults=[f["fault"] for f in res["faults"]])

# --------------------------------------------------------------------------------------------
# 4. CX-BV5-09: the class list is part of the same observation as the count
# --------------------------------------------------------------------------------------------
for label, delta, expect in [
        ("complete with a non-empty class list beside a zero count",
         {"state": "complete", "attempted": True, "examinedExhaustive": True,
          "stageTerminal": "complete", "unresolvedEdgeCount": 0,
          "unresolvedEdgeClasses": ["computed-member-access"]}, "REFUSE"),
        ("not-attempted carrying a class it cannot have observed",
         {"state": "not-attempted", "attempted": False, "examinedExhaustive": True,
          "stageTerminal": None, "unresolvedEdgeCount": 0,
          "unresolvedEdgeClasses": ["computed-member-access"]}, "REFUSE"),
        ("valid complete with an empty class list",
         {"state": "complete", "attempted": True, "examinedExhaustive": True,
          "stageTerminal": "complete", "unresolvedEdgeCount": 0,
          "unresolvedEdgeClasses": []}, "ADMIT"),
        ("valid not-attempted with an empty class list",
         {"state": "not-attempted", "attempted": False, "examinedExhaustive": True,
          "stageTerminal": None, "unresolvedEdgeCount": 0,
          "unresolvedEdgeClasses": []}, "ADMIT"),
        ("honest partial keeps its stage and stays admissible",
         {"state": "partial", "attempted": True, "examinedExhaustive": False,
          "stageTerminal": "budget-exhausted", "unresolvedEdgeCount": 0,
          "unresolvedEdgeClasses": []}, "ADMIT")]:
    res = producer_attempt("references", "resolved-binding", delta)
    faults = [f["fault"] for f in res["faults"]]
    out["freeFieldControls"].append({"variation": label, "result": res["result"], "faults": faults})
    check("RC-2 class law: " + label + " -> " + expect, res["result"] == expect, faults=faults)

# an honest INCOMPLETE observation still carries its classes and is not converted into completeness
run2, objects2, blobs2 = F.build(resolved=True, has_match=True)
scope2 = copy.deepcopy(next(v for d, v in objects2.values() if d == "subject-scope"))
paths2 = [r["path"] for r in objects2[run2["snapshotId"]][1]["sourceInventory"]]
payload2 = F.coverage_result(scope2, scope2["sourceUniverse"], True, blobs2, paths2)
referrer = scope2["subjects"][0]
payload2["entry"]["resolutionCompleteness"] = {
    "state": "incomplete", "attempted": True, "examinedExhaustive": True,
    "stageTerminal": "complete", "unresolvedEdgeCount": 1,
    "unresolvedEdgeClasses": ["computed-member-access"]}
facts = [{"relation": scope2["relation"], "referrer": referrer,
          "edgeKind": "computed-member-access"}]
res = N.admit_coverage_result_v3(payload2, scope2, facts,
                                 next(v["payloadSchemaDigest"] for d, v in objects2.values() if d == "coverage"))
check("an honest incomplete observation still carries its classes and admits",
      res["result"] == "ADMIT", faults=[f["fault"] for f in res["faults"]], refusals=res["refusals"])

# --------------------------------------------------------------------------------------------
# 5. CX-BV5-08 completion: a RETAINED scope with no Coverage wrapper
# --------------------------------------------------------------------------------------------
def scope_only_run(rung):
    run, objects, blobs = F.build(resolved=True, has_match=True)
    baseline = M.close_run(run, objects, blobs)
    scope = copy.deepcopy(next(v for d, v in objects.values() if d == "subject-scope"))
    scope.update(relation="unresolved-edge", resolution=rung)
    sid = M.identifier("subject-scope", scope)
    objects[sid] = ("subject-scope", scope)
    vid = objects[run["evidenceId"]][1]["viewIds"][0]
    view = copy.deepcopy(objects[vid][1]); view["scopeIds"].append(sid)
    F.rekey(objects, vid, view, run)
    F.resync_witness(objects, blobs, run); F.resync_proof_refs(objects, blobs, run)
    try:
        return {"pair": "unresolved-edge@" + rung, "baselineRunId": baseline, "extraScopeId": sid,
                "extraCoverageAdded": False, "closure": "ADMIT",
                "runId": M.close_run(run, objects, blobs)}
    except Exception as exc:
        return {"pair": "unresolved-edge@" + rung, "baselineRunId": baseline, "extraScopeId": sid,
                "extraCoverageAdded": False, "closure": "REFUSED",
                "error": type(exc).__name__ + ":" + str(exc)[:200]}


for rung, expect in [("observed", "ADMIT"), ("enumerated", "REFUSED")]:
    row = scope_only_run(rung)
    out["fullRunCases"].append(dict(row, case="retained-scope-without-coverage-" + rung))
    check("a retained scope with NO coverage wrapper, pair " + rung + " -> " + expect,
          row["closure"] == expect, row=row)

out["ok"] = not out["failures"]
print(json.dumps(out, indent=1))
sys.exit(0 if out["ok"] else 1)
