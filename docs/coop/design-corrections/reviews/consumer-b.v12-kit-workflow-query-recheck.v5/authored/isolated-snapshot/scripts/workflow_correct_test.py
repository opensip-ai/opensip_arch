#!/usr/bin/env python3
"""Independent assertions over executed workflow reconstructions.

Fails with nonzero exit on any required failed assertion or schema/setup error.
Does not treat saved helper results as an oracle: expected values are recomputed
from kit laws in helper.workflow_laws / helper.evaluator / helper.identity.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-query-recheck.v5/output/isolated-snapshot")
OUT = ROOT
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.errors import AdmissionError  # noqa: E402
from helper.evaluator import eval_atom  # noqa: E402
from helper.identity import H  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.workflow_laws import (  # noqa: E402
    admit_clones_fact,
    admit_config_path,
    admit_edition_map_crate,
    admit_syntax_suffix,
    classify_presence,
    committed_id,
    counts_from_entries,
    cursor_token,
    derive_rust_edition,
    mutation_intent_key,
    neighbors,
    project_edges,
    reach,
    repair_apply_key,
    repair_target_join,
    rust_body_l0,
    rust_body_l0_retained,
    shortest_path,
    unit_id,
)

FAILED = []


def fail(msg: str) -> None:
    FAILED.append(msg)
    print("FAIL", msg)


def load(rel: str):
    return json.loads((OUT / rel).read_text())


def must(cond, msg):
    if not cond:
        fail(msg)


# frozen stores
frozen = load("frozen-run-hashes.json")["runs"]
for name, exp in frozen.items():
    b = (OUT / "runs" / name).read_bytes()
    got = hashlib.sha256(b).hexdigest()
    must(got == exp["sha256"] and len(b) == exp["bytes"], f"frozen {name}")

# 48 reconstructed IDs present
res = load("workflow-correct-results.json")["results"]
got_ids = [r["id"] for r in res]
must(len(got_ids) == 48 and len(set(got_ids)) == 48, f"result count {len(got_ids)}")

# repair-apply key recipe
rak = load("vectors/repair-apply-key.json")
recomputed = repair_apply_key(
    project_id=rak["applyKeyPreimage"]["projectId"],
    repair_plan_id=rak["applyKeyPreimage"]["repairPlanId"],
    base_snapshot_id=rak["applyKeyPreimage"]["baseSnapshotId"],
)
must(set(rak["applyKeyPreimage"]) == {"operation", "projectId", "repairPlanId", "baseSnapshotId"}, "apply preimage fields")
must(rak["applyKeyPreimage"]["operation"] == "repair-apply", "apply operation")
must(rak["repairApplyKey"] == recomputed["key"], "apply key digest")
must(rak["unequal"] is True, "apply key != mutation intent")
must("requestId" not in rak["applyKeyPreimage"] and "kind" not in rak["applyKeyPreimage"], "apply key not request-scoped")

# repair plan H
rp = load("vectors/repair-descriptor.json")
must(rp["repairPlanId"] == committed_id("repairplan2:", "workflow.repair-plan", rp["descriptor"]), "repairPlanId H")
r = validate_against(rp, "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json", selector="#/$defs/RepairPlanV1")
must(r["stockOk"], f"repair schema {r['errors'][:2]}")

# mutation scope
mrs = load("vectors/mutation-replay-scope.json")
scope = {k: mrs[k] for k in ("schemaVersion", "requestId", "stepId", "projectId", "operation")}
must(scope["operation"] == "purge", "mrs purge")
must(mrs["mutationIntentKey"] == mutation_intent_key(scope), "mutation intent H")
try:
    mutation_intent_key({**scope, "operation": "repair-apply"})
    fail("repair-apply must be refused in MutationReplayScope")
except AdmissionError:
    pass

# min-resolution: retained facts/Coverage, not helper labels
mr = load("vectors/min-resolution.json")
by = {c["level"]: c for c in mr["cases"]}
must(set(by) == {"syntactic", "resolved", "type"}, "three levels")
must(by["syntactic"]["qualifying"]["value"] == "true" and by["syntactic"]["insufficient"]["value"] == "indeterminate", "syn")
must(by["resolved"]["qualifying"]["value"] == "true" and by["resolved"]["insufficient"]["value"] == "false", "res")
must(by["type"]["qualifying"]["value"] == "true" and by["type"]["insufficient"]["value"] == "false", "type")
must(all(c["qualifyingAgrees"] and c["insufficientAgrees"] for c in mr["cases"]), "agrees kit")
must(by["syntactic"]["qualifying"]["facts"] and by["syntactic"]["qualifying"]["coverages"], "syn facts/coverage retained")
must(by["resolved"]["qualifying"]["facts"] and by["type"]["qualifying"]["facts"], "resolved/type facts retained")
subj = {"kind": "file", "nativeSubjectId": "a.ts"}
for level, case in by.items():
    atom = case["atom"]
    q = eval_atom(atom, subject=subj, facts=case["qualifying"]["facts"], coverages=case["qualifying"]["coverages"], payloads=case["qualifying"]["payloads"])
    i = eval_atom(atom, subject=subj, facts=case["insufficient"]["facts"], coverages=case["insufficient"]["coverages"], payloads=case["insufficient"]["payloads"])
    must(q["value"] == case["qualifying"]["value"] == case["qualifyingExpected"], f"recompute {level} qualifying")
    must(i["value"] == case["insufficient"]["value"] == case["insufficientExpected"], f"recompute {level} insufficient")

mre = load("vectors/min-resolution-repair-evidence.json")
must("repairPlan" in mre and mre["repairPlan"]["repairPlanId"].startswith("repairplan2:"), "repair evidence plan")
must(len(mre["requirements"]) == 3, "three evidence reqs")

# negatives executed
ug = load("vectors/unsupported-grammar.json")
must(ug["positive"]["result"]["ok"] is True, "rs suffix ok")
must(ug["negative"]["result"]["ok"] is False and ug["negative"]["result"]["firstRefusal"]["code"] == "unsupported-file", "unknown suffix")
try:
    admit_syntax_suffix("notes.unknownlang")
    fail("suffix should refuse")
except AdmissionError as e:
    must(e.code == "unsupported-file", e.code)

hm = load("vectors/hidden-mismatch.json")
must(hm["typescript"]["negative"]["ok"] is False, "ts hidden")
must(hm["rust"]["negative"]["ok"] is False, "rust hidden")
try:
    admit_config_path("missing.tsconfig.json", {"tsconfig.json"})
    fail("config should refuse")
except AdmissionError:
    pass

cn = load("vectors/clones-negatives.json")
codes = [v["firstRefusal"]["code"] for v in cn["vectors"] if not v["ok"]]
must("FACT_ANCHOR_CARDINALITY" in codes and "CLONE_LEVEL_SPEC_MISSING" in codes and "BODY_LANGUAGE_MISMATCH" in codes, codes)
ok_js = [v for v in cn["vectors"] if v["name"] == "javascript-body-through-ts-ok"][0]
must(ok_js["ok"] is True, "js through ts ok")

ra = load("vectors/repair-authority-per-target.json")
must(ra["positive"]["result"]["ok"] is True, "repair pos")
must(ra["negative"]["result"]["ok"] is False and ra["negative"]["result"]["firstRefusal"]["code"] == "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE", "repair neg")
try:
    repair_target_join(target="finding-key2:" + "d" * 64, matched_fingerprints={"finding-key2:" + "b" * 64})
    fail("join should refuse")
except AdmissionError:
    pass

# ownership + remint L0 from retained span/BLV/frame
own = load("vectors/rust-body-identity-pair.json")
must(own["stableWhenOnlyOwnershipChangesWithoutDialect"] is True, "stable")
must(own["distinctWhenDialectChanges"] is True, "dialect moves")
s0, s1 = own["sameDialectOwnershipSelections"]
e0 = derive_rust_edition(ownership=s0["ownership"], body_path="src/lib.rs", edition_map={"demo": 2018})
e1 = derive_rust_edition(ownership=s1["ownership"], body_path="src/lib.rs", edition_map={"demo": 2018})
must(e0 == e1 == 2018, "derived editions")
must(s0["l0"] == s1["l0"], "same L0")
must(s0["ownership"] != s1["ownership"], "two maps")
must("selectedUnitIds" in s0["ownership"] and "units" in s0["ownership"], "retained maps")
must(own.get("retainedSpanUtf8") and own.get("retainedCompilerBuild") and own.get("retainedLevelSpecUtf8"), "retained preimages")
must(s0["retained"]["bodyLanguageVersion"]["dialect"]["edition"] == 2018, "edition integer")
must(type(s0["retained"]["bodyLanguageVersion"]["dialect"]["edition"]) is int, "edition type int")
span = own["retainedSpanUtf8"].encode("utf-8")
remint = rust_body_l0_retained(
    edition=e0,
    span=span,
    compiler_build=own["retainedCompilerBuild"],
    level_spec_bytes=own["retainedLevelSpecUtf8"].encode("utf-8"),
)
must(remint["bodyIdentity"] == s0["l0"] == s1["l0"], "remint L0 from retained preimages")
must(remint["frameSha256"] == s0["retained"]["frameSha256"], "retained frame suffix")
r = validate_against(s0["ownership"], "docs/coop/design-corrections/native/native-evidence.schemas.v2.json", selector="#/$defs/SourceUnitOwnershipV1")
must(r["stockOk"], f"own schema {r['errors'][:2]}")
r = validate_against(s0["retained"]["bodyLanguageVersion"], "docs/coop/design-corrections/foundation/identity-schemas.v3.json", selector="#/$defs/body-language-version")
must(r["stockOk"], f"blv schema {r['errors'][:2]}")

# comparisons identities + counts
for rel, rid in [
    ("vectors/comparison-empty-result.json", "empty"),
    ("vectors/comparison-missing.json", "missing"),
    ("vectors/comparison-evidence-changed.json", "changed"),
    ("vectors/pivot-only-fingerprints.json", "pivot"),
]:
    obj = load(rel)
    must(obj["comparisonResultId"] == committed_id("comparison2:", "workflow.comparison", obj["descriptor"]), f"{rid} H")
    must(obj["descriptor"]["counts"] == counts_from_entries(obj["descriptor"]["entries"]), f"{rid} counts")
    r = validate_against(obj, "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json")
    must(r["stockOk"], f"{rid} schema {r['errors'][:2]}")

scope = load("vectors/comparison-scope-policy-only.json")
cmp = scope["comparison"]
must(cmp["comparisonResultId"] == committed_id("comparison2:", "workflow.comparison", cmp["descriptor"]), "scope H")
must(cmp["descriptor"]["baselineContext"]["scopeDigest"] != cmp["descriptor"]["currentContext"]["scopeDigest"], "scope digest differs")
must(cmp["descriptor"]["baselineContext"]["policyDigest"] == cmp["descriptor"]["currentContext"]["policyDigest"], "policy same")
must(cmp["descriptor"]["contextDelta"]["scopeChanged"] is True, "scopeChanged")
must(scope["retainedScopeDocuments"]["digestsUnequal"] is True, "retained docs")

pivot = load("vectors/pivot-only-fingerprints.json")
pent = pivot["descriptor"]["entries"][0]
must(pent["presence"]["B"] is False and pent["presence"]["E0"] is True and pent["presence"]["E4"] is False, "pivot only")
must(pivot["descriptor"]["counts"][pent["classification"]] == 1, "pivot count")
cls, live = classify_presence(pent["presence"])
must(pent["classification"] == cls and pent["liveInCurrent"] == live == False, "pivot classify")

e0e3 = load("vectors/baseline-e0-e3.json")
must(e0e3["E0"]["descriptor"]["pivotsAvailable"]["E0"] == "available", "e0 pivot")
must(e0e3["E1E3"]["descriptor"]["pivotsAvailable"]["E1"] == "available", "e13 pivot")
must(e0e3["E0"]["descriptor"]["counts"]["UNCHANGED"] == 1, "e0 counts")
must(e0e3["E1E3"]["descriptor"]["counts"]["UNCHANGED"] == 1, "e13 counts")
must(e0e3["E0"]["comparisonResultId"] == committed_id("comparison2:", "workflow.comparison", e0e3["E0"]["descriptor"]), "e0 H")

base = load("vectors/baseline-audit.json")
must(base["baselineId"] == committed_id("baseline2:", "workflow.baseline", base["descriptor"]), "baseline H")

# multi-unit / candidate-only
mu = load("vectors/multi-unit-missing-caps.json")
must(len(mu["units"]) == 2, "two units")
must(mu["units"][0]["configGraph"]["entryConfigPath"] is None, "synthesized")
must("clones-cross-tsjs" in mu["units"][0]["missingAdvertised"], "missing cap")
co = load("vectors/candidate-only-clones.json")
must(all(c["kinds"] == [] and "candidateSourcePaths" in c for c in co["cells"]), "kinds empty")
must(co["notSelectedCompleteClones"] is True, "not complete clones")

hc = load("vectors/host-captured-vs-candidate.json")
must("stageReceipts" in hc["hostCaptured"] and hc["selectedRefs"] and hc["candidateResultRefs"], "observations")
must(hc["syntheticHostObservation"] is True, "labeled synthetic")

chain = load("vectors/chain-zero-config-to-receipt.json")
must(chain["notAChecklistSentence"] is True, "chain not checklist")
must(all(a.get("measured") for a in chain["arrows"]), "measured arrows")
roles = {a["role"] for a in chain["arrows"]}
must("workflow-trace" in roles and "complete-run-bytes" in roles and "workflow-envelope" in roles, "chain roles")
must(chain["frozenRunAdmission"]["accepted"] is False, "close_run not accepted")
must("close_run" in chain["frozenRunAdmission"]["concreteDependency"], "concrete pending")
must(chain["frozenRunAdmission"]["status"] == "pending-final-integration", "pending status")

# custom multi-base: repeated later-wins edge in one sequence
cmb = load("vectors/config-custom-multi-base.json")
entry = next(n for n in cmb["graph"]["nodes"] if n["path"] == cmb["graph"]["entryConfigPath"])
must(entry["extendsResolved"].count("tsconfig.base.json") >= 2, "repeated base edge")
must(entry["extendsResolved"][-1] == "tsconfig.base.json", "later wins")
must(cmb.get("orderIsSequenceNotSet") is True, "sequence not set")
r = validate_against(cmb["graph"], "docs/coop/design-corrections/native/native-evidence.schemas.v2.json", selector="#/$defs/TypeScriptConfigGraphV1")
must(r["stockOk"], f"custom graph schema {r['errors'][:2]}")

# empty/partial/unavailable/missing exhibited as records
epum = load("vectors/empty-partial-unavailable-missing.json")
must(epum["completeEmpty"]["kind"] == "package" and epum["completeEmpty"]["state"] == "complete" and epum["completeEmpty"]["rows"] == [], "complete-empty")
must(epum["partial"]["state"] == "partial" and epum["partial"]["rows"], "partial known rows")
must(epum["unavailable"]["state"] == "unavailable" and epum["unavailable"]["rows"] == [], "unavailable")
must(epum["missingCommittedBytes"]["code"] == "EXECUTION_INPUTS_REF_LOST_BYTES" and epum["missingCommittedBytes"]["blobPresent"] is False, "lost bytes")
must(len(set(epum["distinctStates"])) == 4, "four distinct states")
r = validate_against(epum["completeEmpty"], "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json")
must(r["stockOk"], f"empty inv {r['errors'][:2]}")
r = validate_against(epum["partial"], "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json")
must(r["stockOk"], f"partial inv {r['errors'][:2]}")
r = validate_against(epum["unavailable"], "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json")
must(r["stockOk"], f"unavail inv {r['errors'][:2]}")

# graph query
gq = load("query/graph-query-bundle.json")
res_by = {r["id"]: r for r in res}
must(res_by["R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR"].get("executed") is False, "R-GRAPH not claimed executed")
must(res_by["R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR"].get("status") == "incomplete-pending-admitted-run", "R-GRAPH incomplete")
must(gq["underlyingRunAdmissionUnverified"] is True, "unverified")
must(gq["projectableRelation"] == ["calls", "resolved-callee"], "projectable")
must(gq["failureEnvelope"]["termination"]["domainDetail"]["code"] == "QUERY.RELATION_UNSUPPORTED", "unsupported fail")
must(gq["cursor"]["nextCursor"] and gq["cursor"]["nextCursor"].startswith("q3."), f"cursor {gq['cursor']}")
parts = gq["cursor"]["nextCursor"].split(".")
must(len(parts) == 4 and parts[0] == "q3" and len(parts[1]) == 64 and len(parts[2]) == 64, "cursor form")
must(gq["responses"]["neighbors"]["context"]["evidence"]["coverageIds"] == [gq["coverageId"]], "coverage from views")
must(gq["responses"]["path"]["items"][0]["hopCount"] >= 1, "nontrivial path")
must(len(gq["responses"]["reach"]["items"]) >= 2, "reach")
must(set(gq["rendererParity"]["rendered"]) >= {"human", "json", "agent"}, "parity formats")
six = {"resolved-view", "availability", "truncated", "total-items", "termination-class", "query-response"}
for fmt in ("human", "json", "agent"):
    rendered = gq["rendererParity"]["rendered"][fmt]
    must(isinstance(rendered, dict) and set(rendered) >= six, f"{fmt} six fields")
    qr = rendered["query-response"]
    must(qr.get("schemaFamily") == "opensip.product.query" and "context" in qr and "items" in qr, f"{fmt} complete GraphQueryResponseV1")
paged = gq["responses"]["neighborsPaged"]
must(paged["context"]["traversalCoverage"] == "truncated-page" and paged["context"]["truncated"] is False, "page fullness truncated=false")
must(gq["cursor"]["nextCursor"] and gq["responses"]["neighborsPage2"]["items"], "page-2 continuation retained")
must(gq["cursor"]["remainingNeighborFactId"] == gq["responses"]["neighborsPage2"]["items"][0]["factId"], "remaining neighbor")
must(gq["responses"]["neighborsPage2"]["context"].get("nextCursor") in (None, "") or "nextCursor" not in gq["responses"]["neighborsPage2"]["context"], "last page no further cursor")
try:
    project_edges([], relation="file", min_resolution="enumerated")
    fail("file@enumerated should refuse")
except AdmissionError as e:
    must(e.code == "QUERY.RELATION_UNSUPPORTED", e.code)

r = validate_against(gq["requests"]["neighbors"], "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json", selector="#/$defs/GraphQueryRequestV1")
must(r["stockOk"], f"gq req {r['errors'][:2]}")
r = validate_against(gq["responses"]["neighbors"], "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json", selector="#/$defs/GraphQueryResponseV1")
must(r["stockOk"], f"gq resp {r['errors'][:2]}")
r = validate_against(gq["failureEnvelope"], "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json")
must(r["stockOk"], f"gq fail schema {r['errors'][:2]}")

# D9
d9 = json.loads((KIT / "docs/coop/artifacts/d9-exit-contract.v1.14.json").read_text())["classToExitCode"]
must(load("vectors/d9-extension-precedence.json")["equal"] is True and load("vectors/d9-extension-precedence.json")["inherited"] == d9, "d9")

# original failed examples preserved
pres = OUT / "preserved-failures/workflow-review-v2-refused-original"
must((pres / "vectors/repair-apply-key.json").exists(), "preserved apply key")
must((pres / "query/graph-query-bundle.json").exists(), "preserved gq")
old_apply = json.loads((pres / "vectors/repair-apply-key.json").read_text())
must("kind" in old_apply.get("applyKey", {}), "original wrong preimage kept")

print("assertions", "FAIL" if FAILED else "PASS", "nfail", len(FAILED))
if FAILED:
    for m in FAILED:
        print(" -", m)
    raise SystemExit(1)
print("OK")
