#!/usr/bin/env python3
"""PROBE 4 - the four Bv4 findings and the established laws must not regress.

Independently authored expectations. This delta touches native_evidence_model,
native-evidence.schemas, check-identity, two contracts and one registry string;
native_evidence_model IS reached from retained Run closure (identity-model:691),
so complete Run admission is exercised here rather than assumed.

Anything whose owning file is byte-identical to v14 is stated as CARRIED on the
reproduced suite and the v14 independent review, not re-graded.
"""
import copy
import importlib.util
import inspect
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as H  # noqa: E402

N, M, C, W = H.N, H.M, H.C, H.W
DC = H.DC
VE = C.ValidationError

REL = json.loads((DC / "foundation/relation-payload-schemas.v2.json").read_text())
NATIVE_SCHEMAS = json.loads((DC / "native/native-evidence.schemas.v2.json").read_text())
MATRIX = json.loads((DC / "native/native-capability-matrix.v2.json").read_text())

_s = importlib.util.spec_from_file_location("intfix", DC / "integration-fixtures.py")
FIX = importlib.util.module_from_spec(_s)
sys.modules["intfix"] = FIX
_s.loader.exec_module(FIX)

# =============================================== CB4-MUST-1: anchor cardinality
reg = REL["x-opensip-relation-registry"]
law = reg["anchorLaw"]
classes = law["classes"]
members = {cls: set(v["members"]) for cls, v in classes.items()}
all_members = set().union(*members.values())

H.check("CB4-MUST-1-the-anchor-law-is-still-closed-over-all-13-relations",
        len(all_members) == 13 and len(M.RELATIONS) == 13
        and all_members == set(M.RELATIONS),
        {"members": len(all_members), "relations": len(M.RELATIONS)})
H.check("CB4-MUST-1-the-three-classes-are-unchanged",
        set(classes) == {"source-text", "body-identity", "inventory"})
H.check("CB4-MUST-1-source-text-is-minimum-1-with-no-per-relation-maximum",
        classes["source-text"]["cardinality"].startswith("minimum 1")
        and "no additional relation-specific maximum" in classes["source-text"]["cardinality"])
H.check("CB4-MUST-1-body-identity-clones-is-exactly-1",
        classes["body-identity"]["cardinality"] == "exactly 1"
        and members["body-identity"] == {"clones"})
H.check("CB4-MUST-1-inventory-is-exactly-0-over-file-package-vcs-change",
        classes["inventory"]["cardinality"] == "exactly 0"
        and members["inventory"] == {"file", "package", "vcs-change"})
H.check("CB4-MUST-1-the-shared-upper-bound-is-still-present-and-not-overridden",
        M.SCHEMA["$defs"]["fact"]["properties"]["anchors"]["maxItems"] == 100000
        and M.SCHEMA["$defs"]["fact"]["properties"]["anchors"]["uniqueItems"] is True)
H.check("CB4-MUST-1-no-class-is-left-without-a-rule",
        all("rule" in v and v["rule"] for v in classes.values()))
H.check("CB4-MUST-1-the-classes-partition-the-relations-without-overlap",
        sum(len(v) for v in members.values()) == 13)

# the enforcedAt clarification: producer obligation preserved, evidence limited
ea = law["enforcedAt"]
H.check("V14-ADV-2-the-producer-obligation-is-preserved-as-a-MUST",
        "producer must enforce this law on every owning fact" in ea)
H.check("V14-ADV-2-the-verifier-obligation-at-retained-closure-is-preserved",
        "verifier must enforce it again at retained Run closure" in ea)
H.check("V14-ADV-2-the-exhibited-reference-evidence-is-limited-to-run-closure",
        "does not exhibit a separate producer-boundary call site" in ea)
H.check("V14-ADV-2-no-producer-implementation-is-claimed",
        "remains an implementation conformance obligation" in ea)
H.check("V14-ADV-2-no-producer-function-or-call-site-is-invented",
        "admit_" not in ea.split("open_run_closure")[-1])
H.check("V14-ADV-2-the-ordering-clause-before-snapshot-joins-is-preserved",
        "checked before the relation's snapshot joins" in ea)

# independently recheck the call-site claim in the byte-identical model
IM_SRC = (DC / "foundation/identity-model.py").read_text().split("\n")
calls = [i + 1 for i, l in enumerate(IM_SRC)
         if "anchor_law(" in l and not l.strip().startswith("#")
         and not l.strip().startswith("def ")]
H.check("V14-ADV-2-anchor_law-really-has-exactly-one-call-site",
        len(calls) == 1, {"callLines": calls})
H.check("V14-ADV-2-the-only-call-site-is-inside-relation_payload_rules",
        calls and 923 < calls[0] < 1003, {"callLine": calls[0] if calls else None})
rpr_calls = [i + 1 for i, l in enumerate(IM_SRC)
             if "relation_payload_rules(" in l and not l.strip().startswith("def ")]
H.check("V14-ADV-2-relation_payload_rules-is-reached-only-inside-open_run_closure",
        len(rpr_calls) == 1 and 566 < rpr_calls[0] < 923, {"lines": rpr_calls})

# ================================================ CB4-MUST-2: deficiency causes
def find(o, key):
    if isinstance(o, dict):
        if key in o:
            return o[key]
        for v in o.values():
            r = find(v, key)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r is not None:
                return r
    return None


cause_reg = find(NATIVE_SCHEMAS, "x-opensip-deficiency-cause-registry")
defs = NATIVE_SCHEMAS["$defs"]
H.check("CB4-MUST-2-the-deficiency-cause-registry-is-still-present",
        cause_reg is not None)
dv2 = defs["DeficiencyV2"]["enum"]
nc = defs["NativeCause"]["enum"]
uek = defs["UnresolvedEdgeKindV1"]["enum"]
H.check("CB4-MUST-2-DeficiencyV2-is-still-9-members", len(dv2) == 9, {"n": len(dv2)})
H.check("CB4-MUST-2-NativeCause-is-still-14-members", len(nc) == 14, {"n": len(nc)})
H.check("CB4-MUST-2-UnresolvedEdgeKindV1-is-still-16-members", len(uek) == 16,
        {"n": len(uek)})
rows = cause_reg.get("rows", cause_reg) if isinstance(cause_reg, dict) else cause_reg
if isinstance(rows, dict):
    keys = set(rows)
else:
    keys = {r.get("deficiency") for r in rows}
H.check("CB4-MUST-2-the-registry-is-total-over-DeficiencyV2-with-no-gap-or-extra",
        keys == set(dv2), {"missing": sorted(set(dv2) - keys),
                           "extra": sorted(keys - set(dv2))})
H.check("CB4-MUST-2-no-enum-was-widened-by-this-delta",
        len(dv2) == 9 and len(nc) == 14 and len(uek) == 16)

# =========================================== CB4-SHOULD-2: capability authority
caps = MATRIX["capabilities"]
H.check("CB4-SHOULD-2-the-capability-id-authority-is-still-11-members",
        len(caps) == 11)
H.check("CB4-SHOULD-2-no-capability-id-contains-an-at-sign",
        not any("@" in c["id"] for c in caps))
H.check("CB4-SHOULD-2-cells-are-the-complete-11-by-6-product",
        len(MATRIX["cells"]) == 66 and len(MATRIX["languageModes"]) == 6)
H.check("CB4-SHOULD-2-the-capabilityIdLaw-is-still-published",
        "capabilityIdLaw" in MATRIX)
H.check("CB4-SHOULD-2-no-cell-is-promoted-to-qualified-by-this-delta",
        MATRIX.get("platformQualified") in (False, None),
        {"platformQualified": MATRIX.get("platformQualified")})

# a release declaring an unregistered capability / mode / NOT-SELECTED cell refuses
NOT_SELECTED = {(c["capability"], c["mode"]) for c in MATRIX["cells"]
                if c["state"] == "NOT-SELECTED"}
H.check("CB4-SHOULD-2-there-really-are-NOT-SELECTED-cells-to-test",
        len(NOT_SELECTED) == 3, {"n": len(NOT_SELECTED)})
cap0, mode0 = sorted(NOT_SELECTED)[0]
H.raises("CB4-SHOULD-2-a-release-declaring-a-NOT-SELECTED-cell-refuses",
         lambda: N.admit_release_capability_registry(
             [{"capabilityId": cap0, "languageModes": [mode0]}]),
         (N.AdmissionError, VE, ValueError),
         must_contain="not-selected")
H.raises("CB4-SHOULD-2-a-release-declaring-an-unregistered-capability-refuses",
         lambda: N.admit_release_capability_registry(
             [{"capabilityId": "no-such-capability", "languageModes": ["ts-tsconfig"]}]),
         (N.AdmissionError, VE, ValueError))
H.raises("CB4-SHOULD-2-a-release-declaring-an-unregistered-mode-refuses",
         lambda: N.admit_release_capability_registry(
             [{"capabilityId": caps[0]["id"], "languageModes": ["klingon"]}]),
         (N.AdmissionError, VE, ValueError))
H.raises("CB4-SHOULD-2-a-duplicate-capabilityId-in-a-release-refuses",
         lambda: N.admit_release_capability_registry(
             [{"capabilityId": caps[0]["id"], "languageModes": ["ts-tsconfig"]},
              {"capabilityId": caps[0]["id"], "languageModes": ["js-allowjs"]}]),
         (N.AdmissionError, VE, ValueError))
# requesting a NOT-SELECTED cell is unsatisfiable, not merely unregistered
H.raises("CB4-SHOULD-2-requesting-a-NOT-SELECTED-cell-is-refused-as-unsatisfiable",
         lambda: N.admit_requested_capabilities(
             [{"capabilityId": cap0, "languageMode": mode0,
               "workspaceRoot": ".", "required": True}]),
         (N.AdmissionError, VE, ValueError), must_contain="not-selected")

# ======================= complete Run admission, where this delta can reach it
run, objects, blobs = FIX.build()
try:
    rid = M.close_run(copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs))
    H.check("POSITIVE-CONTROL-the-typescript-run-closes-under-this-delta", bool(rid))
    ok = True
except BaseException as e:  # noqa: BLE001
    H.check("POSITIVE-CONTROL-the-typescript-run-closes-under-this-delta", False,
            {"exc": type(e).__name__, "msg": str(e)[:300]})
    ok = False

for lang in ("rust", "syntax"):
    try:
        r2, o2, b2 = FIX.build(universe_language=lang,
                               **({"pure_syntax": True} if lang == "syntax" else {}))
        rid2 = M.close_run(r2, o2, b2)
        H.check("POSITIVE-CONTROL-a-complete-run-closes-under-the-%s-universe" % lang,
                bool(rid2))
    except BaseException as e:  # noqa: BLE001
        H.check("POSITIVE-CONTROL-a-complete-run-closes-under-the-%s-universe" % lang,
                False, {"exc": type(e).__name__, "msg": str(e)[:300]})

# the delta's own reach into Run closure: a retained spec naming an unregistered
# capability must still refuse as a VOCABULARY fault, not as a scope limit.
if ok:
    o3 = copy.deepcopy(objects)
    b3 = copy.deepcopy(blobs)
    r3 = copy.deepcopy(run)
    plan_domain, plan = o3[r3["planId"]]
    spec_v = json.loads(b3[plan["analysisSpecDigest"]])
    row0 = spec_v["requestedCapabilities"][0]
    bad = dict(spec_v, requestedCapabilities=[dict(row0, capabilityId="no-such-cap")])
    nd = FIX.put_blob(b3, bad)
    FIX.rekey_plan(o3, b3, r3, dict(plan, analysisSpecDigest=nd))
    try:
        M.close_run(r3, o3, b3)
        exc3 = None
    except BaseException as e:  # noqa: BLE001
        exc3 = e
    H.check("a-retained-spec-naming-an-unregistered-capability-still-refuses-at-closure",
            exc3 is not None, {"exc": type(exc3).__name__ if exc3 else "CLOSED"})
    H.check("the-retained-vocabulary-fault-keeps-its-own-ANALYSIS_SPEC_CAPABILITY-key",
            exc3 is not None and "ANALYSIS_SPEC_CAPABILITY" in str(exc3),
            {"msg": str(exc3)[:200] if exc3 else ""})
    H.check("the-retained-vocabulary-fault-is-not-reported-as-a-scope-limit",
            exc3 is not None and not isinstance(exc3, N.ScopeRefusal)
            and "PROJECT.SCOPE_LIMIT" not in str(exc3))

# ================================ established laws reachable from this delta
H.check("typed-canonical-equality-still-distinguishes-bool-from-int",
        not C.equal_typed(True, 1) and not C.equal_typed(False, 0)
        and not C.equal_typed("1", 1) and not C.equal_typed(None, False))
H.check("canonical-encoding-distinguishes-bool-from-int",
        C.canonical(True) != C.canonical(1))
H.check("ordered-arrays-are-still-enforced-on-the-requested-capability-set",
        M.SCHEMA["$defs"]["analysis-spec"]["properties"]
        ["requestedCapabilities"].get("x-opensip-order") == "canonical-set")
H.check("the-relation-registry-is-still-the-single-ladder-authority",
        len(M.RELATIONS) == 13
        and all(M.RELATIONS[r].get("ladder") or M.RELATIONS[r].get("rungs")
                for r in M.RELATIONS))
H.check("the-availability-notice-bound-is-tied-to-the-request-bound-not-restated",
        json.loads((DC / "workflows/schemas/common.schema.json").read_text())
        ["$defs"]["CapabilityAvailabilityStepV1"]["properties"]["notices"]["maxItems"]
        == M.SCHEMA["$defs"]["analysis-spec"]["properties"]
        ["requestedCapabilities"]["maxItems"])

# required-output failure after a committed Run: render parity access is strict
render_src = inspect.getsource(W.render) if hasattr(W, "render") else ""
H.check("required-output-failure-after-committed-run-is-still-strict",
        "if k in envelope['parity']" not in render_src
        and "if k in envelope[\"parity\"]" not in render_src,
        {"note": "the weakened guard the v14 delta removed has not returned"})

exit_code = H.report(
    str(pathlib.Path(__file__).resolve().parent.parent /
        "evidence/probe-preserved-laws.json"),
    "Bv4 non-regression and established laws under the v15 delta",
    ["Reference-model only; no compiler, cargo, parser, OS, renderer or "
     "repository code executes. Every native/grammar observation remains a "
     "synthetic trusted assumption.",
     "Families whose owning files are byte-identical to v14 (identity-model, "
     "identity-schemas, native-capability-matrix, common.schema, "
     "command-envelope.schema, workflows_model, permission tables, security "
     "lifecycle schemas, d9-exit-contract) are CARRIED on the reproduced suite "
     "and on the v14 independent review with its original limitations, not "
     "re-graded here.",
     "control-flow and literal remain covered at registry level only; the "
     "candidate's fixture has no payload shape for them.",
     "Passing these probes shows the named refusals fire and a lawful graph is "
     "constructible; it does not show any implementation is correct."])
sys.exit(1 if exit_code else 0)
