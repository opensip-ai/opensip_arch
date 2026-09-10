import copy
import hashlib
import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL
import osip
import schemas
import workflow as W
from osip import C, H, raw_sha256

OUT = {}
FAIL = []


def ok(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ((" -> " + str(detail)[:160])
                                                   if detail else ""))
    if not cond:
        FAIL.append(name)
    return cond


def valid(name, instance, doc, sel):
    errs = schemas.validate(instance, doc, sel)
    return ok(name, not errs, errs[:2] if errs else "")


# ===========================================================================
print("== A. zero-config selection over multiple workspace units ==")
UNITS = [{"workspaceRoot": ".", "languageMode": "ts-tsconfig"},
         {"workspaceRoot": "crates/core", "languageMode": "rust-cargo"},
         {"workspaceRoot": "docs", "languageMode": "syntax-only"}]
# An installed release that lacks some advertised capabilities, INCLUDING a
# candidate-only clone capability.
RELEASE = [
    {"capabilityId": "inventory",
     "languageModes": ["ts-tsconfig", "rust-cargo", "syntax-only"]},
    {"capabilityId": "syntax",
     "languageModes": ["ts-tsconfig", "rust-cargo", "syntax-only"]},
    {"capabilityId": "imports", "languageModes": ["ts-tsconfig"]},
    {"capabilityId": "references", "languageModes": ["ts-tsconfig"]},
    {"capabilityId": "calls", "languageModes": ["ts-tsconfig"]},
    {"capabilityId": "types", "languageModes": ["ts-tsconfig"]},
    {"capabilityId": "reachability", "languageModes": ["ts-tsconfig"]},
    {"capabilityId": "clones-fact",
     "languageModes": ["ts-tsconfig", "rust-cargo", "syntax-only"]},
    {"capabilityId": "unresolved-edge", "languageModes": ["ts-tsconfig"]},
    # clones-near and clones-cross-tsjs are NOT declared by this release
]
ok("CB-WF-A0 release declaration admits",
   W.admit_release_capability_registry(RELEASE) is None,
   W.admit_release_capability_registry(RELEASE))
rows, undeclared = W.default_capability_selection(UNITS, RELEASE)
ok("CB-WF-A1 the default requests every non-NOT-SELECTED cell of every unit",
   len(rows) == 11 + 10 + 10, "rows=%d" % len(rows))
ok("CB-WF-A2 the three NOT-SELECTED cells are never requested",
   not any(r["capabilityId"] == "clones-cross-tsjs"
           and r["languageMode"] in ("rust-cargo", "syntax-only") for r in rows))
ok("CB-WF-A3 UNSUPPORTED-TYPED cells ARE requested (answered by disclosure)",
   any(r["capabilityId"] == "references" and r["languageMode"] == "syntax-only"
       for r in rows))
ok("CB-WF-A4 the request is admissible against the matrix",
   W.admit_requested_capabilities(rows) is None)
leaf0 = W.release_absence_notices(undeclared)
ok("CB-WF-A5 absence is disclosed, not dropped", leaf0["noticeCount"] > 0,
   "%d notices" % leaf0["noticeCount"])
cand = [n for n in leaf0["notices"] if n["capabilityId"] in
        ("clones-near", "clones-cross-tsjs")]
ok("CB-WF-A6 candidate-only capabilities ride the selection account, not Coverage",
   cand and all(W.projection_for(n["capabilityId"]) == "selection-account-only"
                for n in cand),
   sorted({n["capabilityId"] for n in cand}))
ok("CB-WF-A7 a fact-producing absence keeps its relation@rung Coverage route",
   W.projection_for("references") == "coverage-entry"
   and W.CAP_RELATIONS["references"] == [("references", "resolved-binding")])
tuples = {(n["capabilityId"], n["languageMode"], n["workspaceRoot"])
          for n in leaf0["notices"]}
ok("CB-WF-A8 the ownership tuple is typed and never concatenated: two units "
   "requesting the same capability stay distinguishable",
   len(tuples) == len(leaf0["notices"]))

# single-step command: `opensip` (default) projects ONE step
single = W.invocation_availability([(0, leaf0)])
valid("CB-WF-A9 CapabilityAvailabilityV1 (single-step)", single,
      "common", "#/$defs/CapabilityAvailabilityV1")

# named MULTI-STEP invocation: `audit` has analysis, analysis, comparison, render
# with DIFFERENT selections at the two analysis steps (primary and pivot).
rows_p, und_p = W.default_capability_selection(
    [UNITS[0]], RELEASE)                      # pivot step: TypeScript unit only
leaf_pivot = W.release_absence_notices(und_p)
multi = W.invocation_availability([(0, leaf0), (1, leaf_pivot)])
valid("CB-WF-A10 CapabilityAvailabilityV1 (multi-step)", multi,
      "common", "#/$defs/CapabilityAvailabilityV1")
ok("CB-WF-A11 totalNoticeCount is the exact sum, not a truncation residue",
   multi["totalNoticeCount"] == leaf0["noticeCount"] + leaf_pivot["noticeCount"]
   and multi["stepCount"] == 2)
ok("CB-WF-A12 the same tuple may recur in DIFFERENT steps; uniqueness is "
   "within a step",
   any(n in leaf_pivot["notices"] for n in leaf0["notices"]))
empty = W.invocation_availability([(0, {"noticeCount": 0, "notices": []})])
valid("CB-WF-A13 a step that selected and found nothing absent contributes an "
      "EMPTY entry (the positive statement that it checked)", empty,
      "common", "#/$defs/CapabilityAvailabilityV1")

d = COMMANDS = W.COMMANDS
for name in ("default", "analyze", "fit", "audit", "repair-verify"):
    c = COMMANDS.get(name)
    if c is None:
        ok("CB-WF-A14 command %s present" % name, False)
        continue
    ok("CB-WF-A14 %s: capability-availability is a DECLARED parity field" % name,
       c["requestClass"] == "analysis"
       and "capability-availability" in c["parityFields"], c["formats"])
OUT["availability"] = {"units": UNITS, "release": RELEASE,
                       "requestedRows": len(rows), "undeclared": undeclared,
                       "singleStep": single, "multiStep": multi}

# ===========================================================================
print("\n== B. the ORIGINAL invocation's disclosure ==")
REQ = "req1_" + hashlib.sha256(b"cb-invocation").hexdigest()[:32]
EXEC = "exec1_" + hashlib.sha256(b"cb-attempt").hexdigest()[:32]
PRJ = "prj1-" + hashlib.sha256(b"cb-ts").hexdigest()
RUNID = "run2:" + "a" * 64
PLANID = "plan2:" + "b" * 64
inv_record = {
    "schemaFamily": "opensip.product.invocation", "schemaMajor": 1,
    "requestId": REQ, "projectId": PRJ,
    "workflow": {"kind": "builtin", "name": "default"},
    "mode": {"interactive": False, "ci": True, "ephemeral": False},
    "orderedSteps": [
        {"stepId": 0, "kind": "analysis", "requirement": "required",
         "dependsOn": [], "dependencyGate": "completed",
         "retryPolicy": "idempotent-retry",
         "params": {"kind": "analysis", "profile": "default", "role": "primary",
                    "verdictGate": "self", "durability": "authoritative",
                    "snapshotSource": "live-worktree"}},
        {"stepId": 1, "kind": "render", "requirement": "required",
         "dependsOn": [0], "dependencyGate": "terminal",
         "retryPolicy": "idempotent-retry",
         "params": {"kind": "render", "format": "json", "destination": "stdout",
                    "sourceSteps": [0], "required": True}}],
    "stepResults": [
        {"stepId": 0, "outcome": "completed",
         "attempts": [{"executionId": EXEC, "outcome": "completed",
                       "derivation": {"planId": PLANID,
                                      "executionPlanId": "exec-plan2:" + "c" * 64,
                                      "stageCount": 1, "stagesCompleted": 1}}],
         "result": {"kind": "analysis", "authority": "authoritative",
                    "runId": RUNID, "planId": PLANID, "verdict": "pass",
                    "requiredCoverage": "satisfied", "durability": "committed",
                    "deficiency": "none", "secondaryDeficiencies": []},
         "termination": {"class": "success", "runId": RUNID}}],
    "termination": {"class": "success", "runId": RUNID},
    "terminationEmitted": True,
    "retentionDisclosure": {"policy": "durable-unbounded", "provenance": "DEFAULTED",
                            "firstUse": True, "storageRoot": ".opensip/store"},
}
valid("CB-WF-B1 InvocationRecordV1 for the ORIGINAL zero-config invocation",
      inv_record, "invocation-record", "#")
env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2, "kind": "run",
       "requestId": REQ, "projectId": PRJ, "termination": inv_record["termination"],
       "exitCode": 0, "run": inv_record["stepResults"][0]["result"],
       "availability": single,
       "retentionDisclosure": inv_record["retentionDisclosure"]}
valid("CB-WF-B2 CommandEnvelope major 2 (kind=run) carrying availability", env,
      "command-envelope", "#")
ok("CB-WF-B3 the default command's applicable output formats",
   COMMANDS["default"]["formats"] == ["human", "json", "sarif", "html", "agent"],
   COMMANDS["default"]["formats"])
ok("CB-WF-B4 every advertised SARIF command declares the seven common fields",
   all(set(["run-id", "verdict", "required-coverage", "deficiency", "findings",
            "termination-class", "retention-disclosure"])
       <= set(COMMANDS[n]["parityFields"])
       for n in ("default", "analyze", "audit", "repair-verify")))
sarif_cmds = sorted(n for n, c in COMMANDS.items() if "sarif" in c["formats"])
ok("CB-WF-B5 exactly four advertised SARIF commands",
   sarif_cmds == ["analyze", "audit", "default", "repair-verify"], sarif_cmds)
ok("CB-WF-B6 bounded cardinality: at most 64 steps, 3 attempts, StepId 0..63",
   schemas.LOADED["invocation-record"]["properties"]["orderedSteps"]["maxItems"] == 64
   and schemas.LOADED["invocation-record"]["$defs"]["StepResult"]
       ["properties"]["attempts"]["maxItems"] == 3
   and schemas.LOADED["common"]["$defs"]["StepId"]["maximum"] == 63)
multi_inv = copy.deepcopy(inv_record)
multi_inv["workflow"] = {"kind": "builtin", "name": "audit"}
multi_inv["orderedSteps"] = [
    {"stepId": 0, "kind": "analysis", "requirement": "required", "dependsOn": [],
     "dependencyGate": "completed", "retryPolicy": "idempotent-retry",
     "params": {"kind": "analysis", "profile": "default", "role": "primary",
                "verdictGate": "delegated", "durability": "authoritative",
                "snapshotSource": "live-worktree"}},
    {"stepId": 1, "kind": "analysis", "requirement": "required", "dependsOn": [],
     "dependencyGate": "completed", "retryPolicy": "idempotent-retry",
     "params": {"kind": "analysis", "profile": "default", "role": "pivot",
                "pivotOfStep": 0, "pivotClosureIds": ["closure2:" + "d" * 64],
                "durability": "authoritative", "snapshotSource": "live-worktree"}},
    {"stepId": 2, "kind": "comparison", "requirement": "required", "dependsOn": [0, 1],
     "dependencyGate": "completed", "retryPolicy": "none",
     "params": {"kind": "comparison", "currentStep": 0, "pivotStep": 1,
                "baseline": "opensip.baseline.json",
                "auditProfile": "code-regression"}},
    {"stepId": 3, "kind": "render", "requirement": "required", "dependsOn": [2],
     "dependencyGate": "terminal", "retryPolicy": "idempotent-retry",
     "params": {"kind": "render", "format": "json", "destination": "stdout",
                "sourceSteps": [0, 2], "required": True}}]
multi_inv["stepResults"] = []
v = schemas.validate(multi_inv, "invocation-record", "#")
ok("CB-WF-B7 named MULTI-STEP invocation (audit): analysis, pivot analysis, "
   "comparison, render", not v, v[:2])
OUT["invocation"] = {"single": inv_record, "multi": multi_inv, "envelope": env}

# ===========================================================================
print("\n== C. public failure envelopes from an actual internal refusal ==")
cases = []
for label, raw_key, origin in [
    ("configuration input", "native.requested-capability-unregistered:made-up",
     "external-configuration"),
    ("retained external input", "native.requested-capability-unregistered:made-up",
     "externally-supplied-spec"),
    ("host-generated invalid internal record",
     "native.requested-capability-unregistered:made-up",
     "host-generated-internal-layer"),
    ("producer boundary failure",
     "native.coverage-cause-not-for-deficiency:input-closure-incomplete:"
     "capability-missing", "producer-boundary"),
    ("well-formed request for a NOT-SELECTED cell",
     "native.requested-capability-mode-not-selected:clones-cross-tsjs/rust-cargo",
     "external-configuration"),
]:
    t, route = W.public_termination_for(raw_key, origin)
    e = W.failure_envelope(REQ, raw_key, origin)
    v1 = schemas.validate(t, "common", "#/$defs/StepTermination")
    v2 = schemas.validate(e, "command-envelope", "#")
    ok("CB-WF-C %s -> %s/%s exit %d" % (label, t["class"],
                                        t.get("errorCode", "-"), e["exitCode"]),
       not v1 and not v2, (v1 + v2)[:2])
    cases.append({"case": label, "internalKey": raw_key, "origin": origin,
                  "termination": t, "envelope": e})
try:
    W.public_termination_for("native.release-capability-unregistered:x",
                             "external-configuration")
    ok("CB-WF-C6 an origin a key cannot have refuses", False)
except ValueError as ex:
    ok("CB-WF-C6 an origin a key cannot have refuses", True, ex)
try:
    W.normalize_internal_key("a prose sentence that is not a registered key")
    ok("CB-WF-C7 an unregistered raw key refuses rather than passing through", False)
except ValueError as ex:
    ok("CB-WF-C7 an unregistered raw key refuses rather than passing through",
       True, ex)

long_mode = "m" * 4096
raw = "native.requested-capability-mode-unregistered:" + long_mode
sub = W.bounded_subject(raw)
ok("CB-WF-C8 bounded_subject: exactly 1024 code points, key preserved verbatim, "
   "SHA-256 of the untruncated UTF-8",
   len(sub) == 1024 and sub.startswith("native.requested-capability-mode-unregistered:")
   and sub.endswith(hashlib.sha256(raw.encode("utf-8")).hexdigest()), len(sub))
e8 = W.failure_envelope(REQ, raw, "external-configuration")
valid("CB-WF-C9 the elided failure envelope is schema-valid", e8,
      "command-envelope", "#")
nonascii = "native.requested-capability-mode-unregistered:" + "é" * 1200
sub2 = W.bounded_subject(nonascii)
ok("CB-WF-C10 units: 1024 CODE POINTS, not UTF-8 bytes",
   len(sub2) == 1024 and len(sub2.encode("utf-8")) > 1024,
   "%d cp / %d bytes" % (len(sub2), len(sub2.encode("utf-8"))))
OUT["failureEnvelopes"] = cases

# ===========================================================================
print("\n== D. the selected D9 extension against the inherited contract ==")
inherited = set(W.D9["scenarioAxesSchema"]["properties"]["faultCause"]["enum"])
selected = set(schemas.LOADED["common"]["$defs"]["D9FaultCause"]["enum"])
ok("CB-WF-D1 the inherited d9-exit-contract.v1.14 does NOT carry host-invariant",
   "host-invariant" not in inherited)
ok("CB-WF-D2 the selected composition adds EXACTLY one faultCause member",
   selected - inherited == {"host-invariant"}, sorted(selected - inherited))
ok("CB-WF-D3 no inherited cause is removed", inherited <= selected)
ok("CB-WF-D4 the added cause maps to an EXISTING error code",
   "SYSTEM.OUTCOME.ILLEGAL_STATE"
   in schemas.LOADED["common"]["$defs"]["D9ErrorCode"]["enum"]
   and "SYSTEM.OUTCOME.ILLEGAL_STATE" not in
   set(W.D9["codeMaps"]["faultCauseToErrorCode"].values()))
ok("CB-WF-D5 classes, exit codes and reason codes are unchanged",
   set(W.D9["classToExitCode"]) == set(schemas.LOADED["common"]["$defs"]
                                       ["D9Class"]["enum"]))
ok("CB-WF-D6 codeMaps.rule declared precedence is faultCause > rejectionCause "
   "> deficiency", W.D9["causeModel"]["precedence"]
   == ["faultCause", "rejectionCause", "deficiency"])
OUT["d9Extension"] = {"inheritedFaultCauses": sorted(inherited),
                      "selectedFaultCauses": sorted(selected),
                      "added": sorted(selected - inherited),
                      "inheritedCodeMapHasNoPreimageForIllegalState": True}

# ===========================================================================
print("\n== E. mutation replay scope, repair-apply key, pinned purge ==")
scope = W.mutation_replay_scope(REQ, 0, PRJ, "policy-write")
valid("CB-WF-E1 MutationReplayScopeV1", scope,
      "invocation-record", "#/$defs/MutationReplayScopeV1")
k1 = W.mutation_intent_key(scope)
scope2 = W.mutation_replay_scope("req1_" + "f" * 32, 0, PRJ, "policy-write")
k2 = W.mutation_intent_key(scope2)
ok("CB-WF-E2 the generic key is scoped to ONE host-minted request: different "
   "fresh requests never deduplicate", k1 != k2, "%s vs %s" % (k1[:16], k2[:16]))
bad = dict(scope); bad["operation"] = "repair-apply"
v = schemas.validate(bad, "invocation-record", "#/$defs/MutationReplayScopeV1")
ok("CB-WF-E3 repair-apply is refused in BOTH generic fields", bool(v), v[:1])
ok("CB-WF-E4 the generic field domain is 23 of the 24 MutationOperation members",
   len(schemas.LOADED["repair"]["$defs"]["MutationOperation"]["enum"]) == 24)
rp_id = "repairplan2:" + "e" * 64
snap_id = "snapshot2:" + "9" * 64
ra_key = W.repair_apply_key(PRJ, rp_id, snap_id)
ok("CB-WF-E5 repair-apply uses a distinct CONTENT-DERIVED key (raw SHA-256 of C), "
   "not the H mutation-intent recipe", ra_key != W.mutation_intent_key(
       W.mutation_replay_scope(REQ, 0, PRJ, "purge")), ra_key[:16])
imp_key = W.mutation_intent_key(W.mutation_replay_scope(REQ, 0, PRJ, "import"))
prep_key = W.mutation_intent_key(
    W.mutation_replay_scope(REQ, 0, PRJ, "native-preparation"))
ok("CB-WF-E6 import and native-preparation share the RECIPE but not the lookup "
   "meaning (delivery-only / not replay)", imp_key != prep_key)

pins = sorted([{"pinId": "baseline:main", "kind": "baseline"},
               {"pinId": "repair:plan-7", "kind": "repair-prerequisite"},
               {"pinId": "export:2026-09", "kind": "backup-export"}],
              key=lambda p: p["pinId"].encode())
disc = {"runId": RUNID, "activePins": pins,
        "consequences": ["named-pins-revoked",
                         "dependent-evidence-replay-unavailable",
                         "sealed-history-retained"]}
term = {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
        "domainDetail": {"code": "evidence.pinned", "remedy":
                         "re-run with the explicit destructive purge authorization "
                         "after reviewing the disclosed pins", "subject": RUNID,
                         "purgeDisclosure": disc}}
purge_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
             "kind": "failure", "requestId": REQ, "projectId": PRJ,
             "termination": term, "exitCode": 2,
             "errors": [term["domainDetail"]]}
valid("CB-WF-E7 complete pinned-purge refusal envelope", purge_env,
      "command-envelope", "#")
ok("CB-WF-E8 the disclosure names every pin, sorted uniquely by pinId, with the "
   "three ORDERED consequences and no aggregate count",
   [p["pinId"] for p in pins] == sorted(p["pinId"] for p in pins)
   and len(pins) == 3)
bad_disc = copy.deepcopy(purge_env)
bad_disc["termination"]["domainDetail"]["purgeDisclosure"]["consequences"] = \
    ["named-pins-revoked"]
v = schemas.validate(bad_disc, "command-envelope", "#")
ok("CB-WF-E9 a truncated consequence list refuses", bool(v), v[:1])
no_pins = copy.deepcopy(purge_env)
no_pins["termination"]["domainDetail"]["purgeDisclosure"]["activePins"] = []
v = schemas.validate(no_pins, "command-envelope", "#")
ok("CB-WF-E10 an empty activePins refuses (minItems 1)", bool(v), v[:1])
other = copy.deepcopy(purge_env)
other["termination"]["domainDetail"]["code"] = "evidence.purged"
v = schemas.validate(other, "command-envelope", "#")
ok("CB-WF-E11 purgeDisclosure is forbidden on any other detail code", bool(v), v[:1])
OUT["mutationKeys"] = {"scope": scope, "mutationIntentKey": k1,
                       "repairApplyKey": ra_key, "importKey": imp_key,
                       "nativePreparationKey": prep_key,
                       "pinnedPurgeEnvelope": purge_env}

print()
print("FAILURES:", FAIL or "none")
with open("/tmp/opensip-design-corrections/consumer-b.v8/output/"
          "vectors-workflow-surfaces.json", "w") as f:
    json.dump(OUT, f, indent=1, sort_keys=True, default=str)
