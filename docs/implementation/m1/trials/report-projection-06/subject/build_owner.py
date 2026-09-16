"""Deterministic builder for the author-04 successor owners.

Derives envelope5, command-inventory schema5, command-inventory5, a complete coverage overlay, the design-obligation register,
conditional passage overrides and report-projection:1 from pinned originals. Originals are read only. check.py regenerates every
output byte-identically and restores each successor to its exact original.

Mandatory root bounds are derived here from owner schemas and the accepted exact codec (section derivations()).
"""
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
MV2 = ARCH / "docs/implementation/m1/metadata-v2"
EV3 = ARCH / "docs/coop/design-corrections/workflows/schemas/evaluator3"
OWNER = HERE / "owner"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = _load("report_model", HERE / "report_model.py")

C = "urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/"
G = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/"
N = "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/"
I = "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/"
P = "urn:opensip:product-v1:policy-document:2#/$defs/"
R2 = "urn:opensip:product-v1:workflows:evaluator3:review:2#/$defs/"
CMP = "urn:opensip:product-v1:workflows:evaluator3:comparison:2"
ENV5 = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:5"
REPORT_ID = "urn:opensip:product-v1:workflows:evaluator3:report-projection:1"
CODEC_MAX_BYTES = 4194304

FIT_NEW_FIELDS = ["candidates-truncated", "candidates-total-items", "candidates-next-cursor", "candidates-availability"]
FIT_PARITY_PATHS = {
    "run-id": "/advisoryReport/parity/runId",
    "candidates": "/advisoryReport/parity/candidates",
    "evidence-levels": "/advisoryReport/parity/evidenceLevels",
    "termination-class": "/termination/class",
    "capability-availability": "/availability",
    "candidates-truncated": "/advisoryReport/parity/candidatesTruncated",
    "candidates-total-items": "/advisoryReport/parity/candidatesTotalItems",
    "candidates-next-cursor": "/advisoryReport/parity/candidatesNextCursor",
    "candidates-availability": "/advisoryReport/parity/candidatesAvailability",
}
FIT_REQUEST_LAW = {"operation": "candidate.list", "view": "sealed-run", "params": {"includeSuppressed": False}, "completeness": "best-effort",
                   "page": {"size": 100}, "cursor": "none", "order": "candidateId"}
FIT_DISPATCH = {"surface": "fit-candidates", "stepKind": "query", "operations": ["candidate.list"], "request": FIT_REQUEST_LAW, "parityPaths": FIT_PARITY_PATHS}
FIT_GOLDEN = {
    "id": "fit-ephemeral-non-authoritative",
    "command": "fit",
    "situation": "--ephemeral: non-authoritative analysis; run-id is null and candidate parity is unavailable-ephemeral-analysis; no candidate list is invented",
    "class": "success",
    "exitCode": 0,
    "remedy": "none; candidate parity requires a sealed Run",
}
ENVELOPE5_SUFFIX = (" Successor major5 adds only advisoryReport, the fit advisory carrier on kind=run: either the first canonical candidate.list page of"
                    " the sealed authoritative Run (exact request, CandidateListRecordV1, total parity) or the non-authoritative ephemeral form with"
                    " run-id and candidate parity explicitly null. Presence is command-specific host admission through command-inventory:5"
                    " advisoryDispatch. Every major4 constraint, identity and semantic owner remains. A major4 reader rejects 5 and a major5 reader rejects 4.")
JSON_RULE_5 = " fit carries its advisory report in advisoryReport and every fit parity field is read at advisoryDispatch.parityPaths, including explicit null forms."
HTML_RULE_5 = ("static single-file rendering of the embedded report-projection:1 document whose envelope is the sole parity source;"
               " identical counts and identities; resolution-completeness and disclosures; a script-independent static parity section"
               " (declared parity lines, disclosure counts and the canonical envelope) and typed failure notice; no script-fetched data")
INVENTORY5_STANDING = ("Command inventory major5: author-04 successor candidate of the accepted metadata-v2 inventory4. It adds only the fit"
                       " advisoryDispatch with four explicit page-disclosure parity fields, json renderer version 5, the html parity rule naming"
                       " report-projection:1 and golden fit-ephemeral-non-authoritative. inventory4 bytes, approval and identities remain historical.")


def dump(value):
    return json.dumps(value, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"


def read(path):
    return json.loads(path.read_bytes())


def ref(target, **extra):
    return dict({"$ref": target}, **extra)


def closed(required, properties, **extra):
    return dict({"type": "object", "additionalProperties": False, "required": required, "properties": properties}, **extra)


def nullable(schema):
    return {"oneOf": [schema, {"type": "null"}]}


# ---------------------------------------------------------------------------
# envelope5 / inventory5 (unchanged design from author-03)

def envelope5():
    env = read(MV2 / "command-envelope.schema.json")
    env["$id"] = ENV5
    env["title"] = "CommandEnvelope schemaMajor 5 - evaluator3 surfaces, pure metadata and the fit advisory carrier"
    env["description"] = env["description"] + ENVELOPE5_SUFFIX
    env["properties"]["schemaMajor"]["const"] = 5
    env["properties"]["advisoryReport"] = ref("#/$defs/FitAdvisoryReportV1", description="Required exactly on the fit command's kind=run envelope (inventory5 advisoryDispatch). Never alters run, findings, verdict or termination.")
    meta = next(e for e in env["allOf"] if e.get("if", {}).get("properties", {}).get("kind", {}).get("const") == "meta")
    meta["then"]["not"]["anyOf"].append({"required": ["advisoryReport"]})
    env["allOf"] += [
        {"if": {"required": ["advisoryReport"]}, "then": {"required": ["run"], "properties": {"kind": {"const": "run"}}}},
        {"if": {"required": ["advisoryReport"], "properties": {"advisoryReport": {"properties": {"state": {"const": "sealed-run-first-page"}}}}},
         "then": {"properties": {"run": {"required": ["runId"], "properties": {"authority": {"const": "authoritative"}}}}}},
        {"if": {"required": ["advisoryReport"], "properties": {"advisoryReport": {"properties": {"state": {"const": "unavailable-ephemeral-analysis"}}}}},
         "then": {"properties": {"run": {"properties": {"authority": {"const": "ephemeral"}}}}}},
    ]
    candidates = {"type": "array", "maxItems": 100, "items": ref(R2 + "Candidate"), "x-opensip-order": {"by": ["candidateId"]}}
    env["$defs"]["FitSealedParityV1"] = closed(["runId", "candidates", "evidenceLevels", "candidatesTruncated", "candidatesTotalItems", "candidatesNextCursor", "candidatesAvailability"], {
        "runId": ref(C + "RunId"), "candidates": candidates, "evidenceLevels": ref("#/$defs/EvidenceLevelCountsV1"),
        "candidatesTruncated": {"type": "boolean"}, "candidatesTotalItems": ref(C + "Uint53"),
        "candidatesNextCursor": nullable({"type": "string", "minLength": 1, "maxLength": 256}), "candidatesAvailability": {"const": "sealed-run-first-page"}},
        description="Total fit parity of the first canonical page. Not the complete candidate set: candidatesTruncated, candidatesTotalItems and candidatesNextCursor disclose the remainder.")
    env["$defs"]["FitEphemeralParityV1"] = closed(["runId", "candidates", "evidenceLevels", "candidatesTruncated", "candidatesTotalItems", "candidatesNextCursor", "candidatesAvailability"], {
        k: {"type": "null"} for k in ["runId", "candidates", "evidenceLevels", "candidatesTruncated", "candidatesTotalItems", "candidatesNextCursor"]} | {"candidatesAvailability": {"const": "unavailable-ephemeral-analysis"}},
        description="Non-authoritative law (workflows section 8): run-id is explicitly null and no authoritative candidate parity exists; nothing is fabricated.")
    env["$defs"]["FitAdvisoryReportV1"] = {"oneOf": [
        closed(["state", "parity", "request", "candidateList"], {
            "state": {"const": "sealed-run-first-page"},
            "parity": ref("#/$defs/FitSealedParityV1"),
            "request": {"allOf": [ref(G + "GraphQueryRequestV1"), {"not": {"required": ["fieldSelection"]}, "properties": {
                "view": ref(G + "ResolvedView"), "operation": {"const": "candidate.list"}, "params": {"const": {"includeSuppressed": False}},
                "completeness": {"const": "best-effort"}, "page": {"const": {"size": 100}}}}]},
            "candidateList": {"allOf": [ref("#/$defs/CandidateListRecordV1"), {"properties": {"includeSuppressed": {"const": False}, "candidates": {"maxItems": 100}}}]}}),
        closed(["state", "parity"], {"state": {"const": "unavailable-ephemeral-analysis"}, "parity": ref("#/$defs/FitEphemeralParityV1")}),
    ], "description": "fit query step result. sealed-run-first-page: the exact first candidate.list page of the Run this invocation sealed. unavailable-ephemeral-analysis: --ephemeral, no sealed Run."}
    return env


STEPS_DESCRIPTION = ("Maximal step-kind summary of the builtin workflow in canonical order; not the exact planned expansion. For the eight html report commands the exact"
                     " expansions (plan role, requirement, dependsOn, dependencyGate and their conditions) are bound by owner/builtin-step-planning.v1.json;"
                     " a kind listed here that no admitted grammar can plan (analyze import) is recorded there as unresolved, never silently planned.")
PLAN_ROLES = ["primary-analysis", "pivot-analysis", "comparison", "query", "repair-preview", "import", "render"]


def planned(role, kind, requirement, deps, gate, binding=None):
    return {"planRole": role, "kind": kind, "requirement": requirement, "dependsOn": deps, "dependencyGate": gate, "paramsBinding": binding or {}}


PRIMARY_SELF = {"role": "primary", "verdictGate": "self"}
QUERY_RENDER = [planned("query", "query", "required", [], "completed"), planned("render", "render", "required", [0], "terminal", {"sourceSteps": [0], "required": True})]
PLANNING_COMMANDS = {
    "default": [{"variant": "primary", "status": "plannable", "condition": "every default invocation (durable authoritative analysis)",
                 "steps": [planned("primary-analysis", "analysis", "required", [], "completed", PRIMARY_SELF),
                           planned("render", "render", "required", [0], "terminal", {"sourceSteps": [0], "required": True})]}],
    "analyze": [{"variant": "primary", "status": "plannable", "condition": "every analyze invocation, authoritative or --ephemeral (durability binds from the flag)",
                 "steps": [planned("primary-analysis", "analysis", "required", [], "completed", PRIMARY_SELF),
                           planned("render", "render", "required", [0], "terminal", {"sourceSteps": [0], "required": True})]},
                {"variant": "with-import", "status": "unresolved-not-plannable",
                 "condition": "an import step requires ImportParams (evidenceKind, path, correspondence); the declared analyze grammar (inventory flags) supplies none and no owner states when analyze plans it",
                 "steps": None, "obligation": "RP-OBL-P01"}],
    "fit": [{"variant": "primary", "status": "plannable", "condition": "every fit invocation; --ephemeral binds analysis durability and the non-authoritative advisory form",
             "steps": [planned("primary-analysis", "analysis", "required", [], "completed", PRIMARY_SELF),
                       planned("query", "query", "required", [0], "completed", {"operation": "candidate.list"}),
                       planned("render", "render", "required", [0, 1], "terminal", {"sourceSteps": [0, 1], "required": True})]}],
    "audit": [{"variant": "no-pivot", "status": "plannable", "condition": "the comparison does not need the detector pivot",
               "steps": [planned("primary-analysis", "analysis", "required", [], "completed", {"role": "primary", "verdictGate": "delegated"}),
                         planned("comparison", "comparison", "required", [0], "completed", {"currentStep": 0}),
                         planned("render", "render", "required", [0, 1], "terminal", {"sourceSteps": [0, 1], "required": True})]},
              {"variant": "with-pivot", "status": "plannable",
               "condition": "the comparison needs the detector pivot and the baseline pivot closure is admitted; the pivot analysis is auto-planned before the primary analysis (AnalysisParams.role)",
               "steps": [planned("pivot-analysis", "analysis", "required", [], "completed", {"role": "pivot", "verdictGate": "delegated", "pivotOfStep": 1}),
                         planned("primary-analysis", "analysis", "required", [], "completed", {"role": "primary", "verdictGate": "delegated"}),
                         planned("comparison", "comparison", "required", [0, 1], "completed", {"currentStep": 1, "pivotStep": 0}),
                         planned("render", "render", "required", [0, 1, 2], "terminal", {"sourceSteps": [0, 1, 2], "required": True})]}],
    "candidates": [{"variant": "primary", "status": "plannable", "condition": "every candidates invocation", "steps": QUERY_RENDER}],
    "inspect": [{"variant": "primary", "status": "plannable", "condition": "every inspect invocation", "steps": QUERY_RENDER}],
    "review-brief": [{"variant": "primary", "status": "plannable", "condition": "every review-brief invocation", "steps": QUERY_RENDER}],
    "repair-preview": [{"variant": "primary", "status": "plannable", "condition": "every repair-preview invocation (evidence source is an explicit Run, no analysis step)",
                        "steps": [planned("repair-preview", "repair-preview", "required", [], "completed", {"evidenceSource": "runId"}),
                                  planned("render", "render", "required", [0], "terminal", {"sourceSteps": [0], "required": True})]}],
}
PLANNING_SOURCES = [
    {"path": "docs/v2/contracts/product-v1/workflows-and-surfaces.md", "lines": [95, 102], "binds": "generic DAG law: lower dependsOn, required never on optional, gate completed|terminal, terminal only for render/export-delivery, skipped on unmet gate"},
    {"path": "docs/v2/contracts/product-v1/workflows-and-surfaces.md", "lines": [216, 222], "binds": "audit gate ownership: delegated primary analysis consumed by one comparison step"},
    {"path": "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json", "selector": "/$defs/AnalysisParams/properties/role/description", "binds": "pivot analysis auto-planned before the primary analysis only when a comparison needs the detector pivot and its closure is admitted"},
    {"path": "docs/coop/design-corrections/workflows/workflow-cases.v1.json", "selector": "/invocationCases (default-analyze-render-success, audit-*)", "binds": "owner-exercised builtin shapes: analysis then terminal render on [0]; delegated analysis, comparison on [0] with currentStep 0, terminal render on [0,1]"},
    {"path": "docs/coop/design-corrections/workflows/workflows_model.v1.py", "selector": "validate_dag", "binds": "executed on every plannable expansion by check.py"},
]


PLAN_VARIANTS = sorted({v["variant"] for vs in PLANNING_COMMANDS.values() for v in vs if v["status"] == "plannable"})


def planning_spec():
    return {"schemaVersion": 1,
            "standing": "author-06 scoped owner successor proposal for the builtin step planning of the eight html report commands; not accepted; other commands and report feature owners unchanged",
            "inventoryStepsCorrection": {"file": "owner/command-inventory.v5.schema.json", "selector": "/$defs/Command/properties/steps/description",
                                         "before": None, "after": STEPS_DESCRIPTION,
                                         "reason": "inventory steps lists the maximal kind summary; audit plans three or four steps and analyze's import is not plannable by the declared grammar"},
            "planRoles": PLAN_ROLES, "sources": PLANNING_SOURCES,
            "fixturePromotionNotes": ["subject-05 audit-full comparison dependsOn [1] and the skipped-audit fixture's [0,1] were constructions, not owner shapes; both are replaced by the bound variants",
                                      "subject-05 analyze ledgers planned an import step that no grammar can plan; analyze now projects the primary variant"],
            "retryPolicy": "not bound here and not projected into the report ledger",
            "commands": PLANNING_COMMANDS}


QUERY_CONTRACT = "docs/coop/design-corrections/workflows/query-projection-contract.v3.md"
QUERY_SURFACE = "docs/coop/design-corrections/workflows/query_surface_projection.v3.py"
QC_136 = "**Produced-item law.** `maxItemsPerOperation` counts result units of the logical operation, not per page, and does not reset on continuation. Take the canonical prefix. Remaining units after the prefix are owed work (`countBasis=lower-bound`)."
QC_140 = "**Page fullness** is `truncated-page`, `truncated=false`. It is not operation truncation. Empty `nextCursor` is not native closed-world. Completeness is `traversalCoverage=complete` and `countBasis=exact`. Exactly-at-cap with an empty owed frontier is complete, not incomplete. A cursor cannot continue past the caps."
LB_BEFORE = ['    ctx_lb = graph_ctx(', '        totalItems=2,', '        producedItems=2,', '        countBasis="lower-bound",', '        traversalCoverage="truncated-page",', '        truncated=False,', '    )']


def query_fixture_correction():
    return {"schemaVersion": 1,
            "standing": "author-06 conditional correction proposal to the query owner; parents are not edited; applies with acceptance of this report successor",
            "ownerReading": "query_projection_model.v3.py finish_operation (called by execute_graph_query and by traverse_projected_graph) computes every logical unit, applies the produced cap, then slices pages: producedItems is the produced prefix length computed before paging, totalItems equals it, a cursor names position+items inside it, and lower-bound arises only from a reached visited or produced cap (eager canonical law, selected). No lazy algorithm is added.",
            "corrections": [
                {"path": QUERY_SURFACE, "lines": [621, 627], "before": LB_BEFORE,
                 "after": ['    ctx_lb = graph_ctx(', '        totalItems=100000,', '        producedItems=100000,', '        countBasis="lower-bound",', '        traversalCoverage="truncated-page",', '        truncated=False,', '    )'],
                 "reason": "the isolated renderer fixture 'graph-lower-bound-prefix-intermediate-page' (2/2 lower-bound, visitedNodes 4, no cap) is unreachable by the owner paging law; the owner-reachable intermediate lower-bound page is a full page of a capped 100000-unit prefix with a cursor"},
                {"path": QUERY_SURFACE, "lines": [513, 513], "before": ['            "producedItems": 5,'], "after": ['            "producedItems": 2,'],
                 "reason": "graph_ctx default (totalItems 2, producedItems 5, exact) contradicts totalItems == producedItems under the owner law; defaults are used only by the missing-evidence negative"},
                {"path": QUERY_CONTRACT, "lines": [136, 136], "before": [QC_136],
                 "after": [QC_136 + " `producedItems` is the length of that produced prefix, computed over the whole logical operation before any page is sliced; `totalItems` equals `producedItems` under both count bases, and a page is the slice `[position, position+items)` of that prefix."]},
                {"path": QUERY_CONTRACT, "lines": [140, 140], "before": [QC_140],
                 "after": [QC_140 + " A `nextCursor` is issued only while produced-prefix rows remain after the page and names exactly `position+items`; `countBasis=lower-bound` arises only when a visited or produced cap was reached, so an intermediate lower-bound page is a full page of a capped prefix."]}]}


def inventory_schema5():
    schema = read(MV2 / "command-inventory.schema.json")
    schema["$defs"]["Command"]["properties"]["steps"]["description"] = STEPS_DESCRIPTION
    schema["$id"] = "urn:opensip:product-v1:workflows:evaluator3:command-inventory:5"
    schema["properties"]["schemaMajor"]["const"] = 5
    schema["$defs"]["Command"]["properties"]["advisoryDispatch"] = ref("#/$defs/AdvisoryDispatch")
    schema["$defs"]["Command"]["allOf"].append({"if": {"properties": {"name": {"const": "fit"}}, "required": ["name"]},
                                                 "then": {"required": ["advisoryDispatch"]}, "else": {"not": {"required": ["advisoryDispatch"]}}})
    schema["$defs"]["AdvisoryDispatch"] = {"const": FIT_DISPATCH, "description": "Closed dispatch of the analysis-class fit command: its query step request law and the exact CommandEnvelope major5 pointer of every parity field."}
    return schema


def inventory5():
    inv = read(MV2 / "command-inventory.v4.json")
    inv["schemaMajor"] = 5
    inv["standing"] = INVENTORY5_STANDING
    fit = next(c for c in inv["commands"] if c["name"] == "fit")
    fit["parityFields"] = fit["parityFields"] + FIT_NEW_FIELDS
    fit["advisoryDispatch"] = copy.deepcopy(FIT_DISPATCH)
    json_row = inv["renderers"][1]
    assert json_row["format"] == "json" and json_row["version"] == 4 and "major 4" in json_row["parityRule"]
    json_row["version"] = 5
    json_row["parityRule"] = json_row["parityRule"].replace("major 4", "major 5") + JSON_RULE_5
    html_row = inv["renderers"][3]
    assert html_row["format"] == "html"
    html_row["parityRule"] = HTML_RULE_5
    inv["goldens"].append(copy.deepcopy(FIT_GOLDEN))
    return inv


# ---------------------------------------------------------------------------
# conditional passage overrides (text only; parents never edited)

def passage_overrides():
    layout = ARCH / "docs/v2/architecture/14-repository-and-module-layout.md"
    workflows = ARCH / "docs/v2/contracts/product-v1/workflows-and-surfaces.md"
    ll = layout.read_text().splitlines()
    wl = workflows.read_text().splitlines()
    rows = [
        ("docs/v2/architecture/14-repository-and-module-layout.md", 339, ll[338],
         "| `crates/contracts/src/generated/output.rs` | model; generated | Generated command envelope carriers (`workflows:evaluator3:command-envelope:5`) and report projection carriers from `workflows:evaluator3:report-projection:1` and its closure. |"),
        ("docs/v2/architecture/14-repository-and-module-layout.md", 459, ll[458],
         "| `crates/reporting/src/html_renderer.rs` | renderer | Assemble the self-contained HTML report from the admitted `report-projection:1` document and supplied built assets, including the static parity section (declared parity lines, disclosure counts and canonical envelope) and typed failure notice outside script control. |"),
        ("docs/v2/architecture/14-repository-and-module-layout.md", 463, ll[462],
         "| `crates/reporting/src/projection.rs` | adapter | Construct the `report-projection:1` document: envelope5 host admission, the invocation ledger and cancellation carrier, the deterministic history and graph-slot policies, owner re-issued pages and the byte law against the remaining document budget; preserve required parity fields and route missing required data to host delivery failure. |"),
        ("docs/v2/architecture/14-repository-and-module-layout.md", 556, ll[555],
         "| `apps/report/src/generated/report.ts` | model; generated | Generate projection carriers and runtime shape-validation support from `workflows:evaluator3:report-projection:1`, the same selected output schema as Rust; exact generator remains pending, and shape validity grants no semantic authority. |"),
        ("docs/v2/architecture/14-repository-and-module-layout.md", 562, ll[561],
         "| `apps/report/src/overview-view.ts` | view | Display the admitted invocation ledger carrier (invocation/step/attempt summaries, outcomes, cancellation and missing-child disclosure) and the step-duration design-blocker state without deriving verdicts or concealing missing child evidence. |"),
        ("docs/v2/architecture/14-repository-and-module-layout.md", 564, ll[563],
         "| `apps/report/src/report-data.ts` | validator | Apply the report codec (byte ceiling, iterative depth, per-owner native depth) and generated runtime validation to the embedded projection with explicit version/profile compatibility checks; refused or incompatible data keeps the static parity section and shows the typed failure notice, with no hand-maintained duplicate schema or recomputed verdict. |"),
        ("docs/v2/contracts/product-v1/workflows-and-surfaces.md", 1106, wl[1105],
         "its underlying sealed Run retains its own verdict. That report is the first canonical `candidate.list` page of the sealed Run (includeSuppressed false, page size 100, no cursor, candidateId order) with explicit truncated, total-items and next-cursor parity; under `--ephemeral` run-id is null and candidate parity is `unavailable-ephemeral-analysis` (command-envelope:5, command-inventory:5)."),
    ]
    condition = "Applies only after acceptance of the author-06 report-projection:1/envelope5 successor with its recorded design and integration blockers; parents are never edited."
    return [{"path": path, "line": line, "before": before, "after": after, "condition": condition} for path, line, before, after in rows]


def overridden_text(path):
    text = (ARCH / path).read_text()
    lines = text.splitlines(keepends=True)
    for row in passage_overrides():
        if row["path"] == path:
            assert lines[row["line"] - 1].rstrip("\n") == row["before"]
            lines[row["line"] - 1] = row["after"] + "\n"
    return "".join(lines)


# ---------------------------------------------------------------------------
# report features, design obligations

COMMANDS = ["default", "analyze", "fit", "audit", "candidates", "inspect", "review-brief", "repair-preview"]
ANALYSIS = ["default", "analyze", "fit", "audit"]
VIEW_IDS = ["overview", "findings", "candidate-list", "candidate-inspection", "review-brief", "repair-preview", "evidence", "comparison", "history", "catalog", "graph", "symbol-detail"]
VIEWS = {
    "default": ["overview", "findings", "evidence", "history", "catalog", "graph", "symbol-detail"],
    "analyze": ["overview", "findings", "evidence", "comparison", "history", "catalog", "graph", "symbol-detail"],
    "audit": ["overview", "findings", "evidence", "comparison", "history", "catalog", "graph", "symbol-detail"],
    "fit": ["overview", "findings", "candidate-list", "evidence", "history", "catalog", "graph", "symbol-detail"],
    "candidates": ["overview", "candidate-list", "graph", "symbol-detail"],
    "inspect": ["overview", "candidate-inspection", "graph", "symbol-detail"],
    "review-brief": ["overview", "review-brief", "graph", "symbol-detail"],
    "repair-preview": ["overview", "repair-preview", "catalog"],
}
PANELS = {
    "default": ["evidence", "graph", "history", "catalog"],
    "analyze": ["evidence", "graph", "comparison", "history", "catalog"],
    "audit": ["evidence", "graph", "comparison", "history", "catalog"],
    "fit": ["evidence", "graph", "history", "catalog"],
    "candidates": ["graph"], "inspect": ["graph"], "review-brief": ["graph"], "repair-preview": [],
}
GRAPH_COMMANDS = ["default", "analyze", "audit", "fit", "candidates", "inspect", "review-brief"]
FEATURE_REASONS = ["no-admitted-owner", "no-query-carrier", "no-redaction-owner", "no-selection-interface", "owner-carrier-field-absent", "owner-data-not-retained"]
# featureId -> (row, obligation, reason, {command: view})
FEATURES = {
    "capability-descriptions": ("R05", "RP-DO-01", "no-admitted-owner", {c: "catalog" for c in ANALYSIS}),
    "catalog-run-statistics": ("R05", "RP-DO-02", "no-admitted-owner", {c: "catalog" for c in ANALYSIS}),
    "coupling-importer-package-membership": ("R08", "RP-DO-03", "no-query-carrier", {c: "graph" for c in GRAPH_COMMANDS}),
    "declared-configuration": ("R23", "RP-DO-04", "no-redaction-owner", {c: "overview" for c in ANALYSIS}),
    "entry-point-recognition": ("R12", "RP-DO-05", "owner-data-not-retained", {c: "graph" for c in GRAPH_COMMANDS}),
    "recipe-descriptions": ("R06", "RP-DO-06", "no-admitted-owner", {"repair-preview": "repair-preview"}),
    "recipe-parameters": ("R06", "RP-DO-07", "no-admitted-owner", {"repair-preview": "repair-preview"}),
    "rule-descriptions": ("R05", "RP-DO-08", "no-admitted-owner", {c: "catalog" for c in ANALYSIS}),
    "symbol-metrics": ("R07", "RP-DO-09", "no-admitted-owner", {c: "symbol-detail" for c in GRAPH_COMMANDS}),
    "test-reachability": ("R07", "RP-DO-10", "no-admitted-owner", {c: "symbol-detail" for c in GRAPH_COMMANDS}),
    "step-duration": ("R03", "RP-DO-11", "owner-carrier-field-absent", {c: "overview" for c in COMMANDS}),
    "explicit-older-run-selection": ("R14", "RP-DO-12", "no-selection-interface", {c: "history" for c in ANALYSIS}),
}
M4_GATE = "M4 exit criteria (docs/v2/architecture/implementation-boundaries-and-build-plan.md milestone table row M4: report dispositions and exact historical availability scenarios)"
DESIGN_OBLIGATIONS = [
    {"id": "RP-DO-01", "featureId": "capability-descriptions", "requirement": "prototype-report-inventory.md R05 (Preserve): selected policy/capability descriptions",
     "owningDesignUnit": {"document": "docs/v2/contracts/product-v1/native-evidence.md", "section": "1.3 Capability x mode table", "schema": "native-evidence.schemas.v2.json#/$defs/ReleaseCapabilityDeclarationV1"},
     "status": "design-blocker", "gapKind": "owner-record-has-no-description-field", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Native capability owner publishes an admitted description text member (or a registry-bound description record) with provenance; report catalog carries it verbatim.",
     "carrierSuccessor": "report-projection successor adds CapabilityCatalogV1 description members; featureStates drop capability-descriptions for all analysis commands.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-02", "featureId": "catalog-run-statistics", "requirement": "R05: 'Any historical run statistics state their included history' (conditional)",
     "owningDesignUnit": {"document": "docs/coop/design-corrections/workflows/query-projection-contract.v3.md", "section": "1 Selection (run.list non-graph operation)", "schema": "graph-query.schema.json#/$defs/Operation"},
     "status": "conditional-requirement-not-selected", "gapKind": "no-owned-statistic-definition", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Either no statistics are shown (current state satisfies the conditional requirement) or an owned statistic over explicitly included history is defined and carried with its history scope.",
     "carrierSuccessor": "Only if a statistic owner is selected: catalog statistic member with included-history scope; otherwise the feature state stays as the truthful conditional disclosure.", "blocksReportDesignReadiness": False},
    {"id": "RP-DO-03", "featureId": "coupling-importer-package-membership", "requirement": "R08 (Change): package coupling matrix with directional counts",
     "owningDesignUnit": {"document": "docs/v2/contracts/product-v1/native-evidence.md", "section": "1.4 Mixed repositories and workspace units (UnitMembershipV1, WorkspaceUnitV2)",
                          "secondary": "docs/coop/design-corrections/workflows/query-projection-contract.v3.md sections 3-4 (graph carriers)"},
     "status": "design-blocker", "gapKind": "existing-owner-design-gap: unit membership is owned natively but no graph query carrier exposes importer package membership", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Query owner publishes a reviewed coupling projection (importer symbol -> owning workspace/package unit from retained UnitMembershipV1) with counts and completeness disclosure.",
     "carrierSuccessor": "report-projection successor adds a package-coupling slot purpose whose rows carry the owner membership join; featureStates drop coupling-importer-package-membership.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-04", "featureId": "declared-configuration", "requirement": "R23 (Change): declared inputs/configuration disclosure with redaction",
     "owningDesignUnit": {"document": "docs/v2/contracts/product-v1/security-and-lifecycle.md", "section": "redaction and disclosure policy (no report redaction selector selected)"},
     "status": "design-blocker", "gapKind": "no-selected-redaction-owner-for-report-disclosure", "milestone": "M4", "gate": M4_GATE + "; DR-G20 (redaction/bounds evidence)",
     "closureCriterion": "Security owner selects a redaction projection for declared configuration inputs; the report carries only that redacted projection.",
     "carrierSuccessor": "report-projection successor adds a redacted declared-configuration carrier; featureStates drop declared-configuration.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-05", "featureId": "entry-point-recognition", "requirement": "R12 (Change): trace with explicit recognition/resolution evidence",
     "owningDesignUnit": {"document": "docs/v2/contracts/product-v1/native-evidence.md", "section": "8 Zero-config framework recognition (FrameworkRecognitionV1.entryPoints)",
                          "secondary": "docs/v2/contracts/product-v1/identity-and-evidence.md retained Run outputs; query-projection-contract.v3.md section 4 path start law"},
     "status": "design-blocker", "gapKind": "existing-owner-design-gap: entry points are produced natively but not retained in the Run nor carried by a query", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Native and identity owners retain FrameworkRecognitionV1 entry points with the Run; the query owner admits them as path starts with recognition evidence.",
     "carrierSuccessor": "report-projection successor adds entry-point-anchored path slots with recognition evidence; featureStates drop entry-point-recognition.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-06", "featureId": "recipe-descriptions", "requirement": "R06 (Preserve): admitted recipe names and descriptions",
     "owningDesignUnit": {"document": "docs/v2/contracts/product-v1/workflows-and-surfaces.md", "section": "6 Repair preview, apply, verify (RecipeRef)", "schema": "evaluator3/repair.schema.json#/$defs/RecipeRef"},
     "status": "design-blocker", "gapKind": "owner-record-carries-references-only", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Repair/contribution owner publishes an admitted recipe descriptor record (component manifest successor; current manifest schemas are CANDIDATE-NOT-APPLIED).",
     "carrierSuccessor": "report-projection successor carries the admitted recipe descriptor; featureStates drop recipe-descriptions.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-07", "featureId": "recipe-parameters", "requirement": "R06 (Preserve): selectors and applicable parameters",
     "owningDesignUnit": {"document": "docs/v2/contracts/product-v1/workflows-and-surfaces.md", "section": "6 Repair preview, apply, verify", "schema": "evaluator3/repair.schema.json#/$defs/RepairPlanDescriptor"},
     "status": "design-blocker", "gapKind": "no-recipe-selector-parameter-catalogue", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Repair owner publishes the recipe selector/parameter catalogue record bound to the admitted recipe closure.",
     "carrierSuccessor": "report-projection successor carries that catalogue record; featureStates drop recipe-parameters.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-08", "featureId": "rule-descriptions", "requirement": "R05 (Preserve): selected policy descriptions",
     "owningDesignUnit": {"document": "docs/v2/contracts/product-v1/workflows-and-surfaces.md", "section": "5 Declarative policy DSL", "schema": "policy-document.v2.schema.json#/$defs/Rule"},
     "status": "design-blocker", "gapKind": "owner-record-has-no-description-field", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Policy/contribution owner publishes admitted rule description text with provenance (Rule successor or contribution manifest successor).",
     "carrierSuccessor": "report-projection successor adds rule description members to RuleCatalogV1; featureStates drop rule-descriptions.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-09", "featureId": "symbol-metrics", "requirement": "R07 (Change): metrics bound to exact universe/identity with unknown values shown",
     "owningDesignUnit": {"document": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json", "section": "relation registry (no metric relation registered)", "secondary": "native-evidence.md section 4 view entries"},
     "status": "design-blocker", "gapKind": "no-registered-metric-relation", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Native/foundation owners register metric relations with exact subject identity and completeness semantics.",
     "carrierSuccessor": "report-projection successor adds a metric column carrier keyed by subjectIndex; featureStates drop symbol-metrics.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-10", "featureId": "test-reachability", "requirement": "R07 (Change): test reachability bound to exact identity, not runtime hotness",
     "owningDesignUnit": {"document": "docs/v2/contracts/product-v1/workflows-and-surfaces.md", "section": "4 Imported evidence (test payload kind)", "secondary": "native reachability relation (query table)"},
     "status": "design-blocker", "gapKind": "no-owned-test-reachability-fact", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Workflow/native owners define a test-reachability fact or projection with identity, completeness and import provenance.",
     "carrierSuccessor": "report-projection successor adds that carrier to symbol-detail; featureStates drop test-reachability.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-11", "featureId": "step-duration", "requirement": "R03 (Preserve): typed outcomes and duration separately from verdict",
     "owningDesignUnit": {"document": "docs/v2/contracts/product-v1/workflows-and-surfaces.md", "section": "1 Invocation, step, attempt, Run", "schema": "evaluator3/invocation-record.schema.json#/$defs/Attempt"},
     "status": "design-blocker", "gapKind": "existing-owner-carrier-field-absent: invocation:3 Attempt has no observed duration; no owned timing observation carrier was found", "milestone": "M4", "gate": M4_GATE + "; DR-G20 (resource/cancellation behavior evidence)",
     "closureCriterion": "Workflow owner adds an operational observed-duration member to Attempt (host monotonic observation, excluded from Run identity) in an invocation successor.",
     "carrierSuccessor": "report ledger successor carries LedgerAttempt observed duration; featureStates drop step-duration.", "blocksReportDesignReadiness": True},
    {"id": "RP-DO-12", "featureId": "explicit-older-run-selection", "requirement": "R14 (Change): explicit historical selection beyond recent history, no latest fallback",
     "owningDesignUnit": {"document": "docs/coop/design-corrections/workflows/query-projection-contract.v3.md", "section": "1 Selection (run.show / run.list non-graph operations; items owned by artifact-specific owners)",
                          "secondary": "workflows-and-surfaces.md section 8 command inventory (no html command selector for explicit Run ids)"},
     "status": "design-blocker", "gapKind": "existing read interface without typed item carrier or html command selector", "milestone": "M4", "gate": M4_GATE,
     "closureCriterion": "Query owner types the run.show item record and the command owner adds an explicit Run-id selector for html commands; the report history policy gains an explicit-run-ids source.",
     "carrierSuccessor": "report-projection successor adds history selection source explicit-run-ids with exact older Run rows; featureStates drop explicit-older-run-selection.", "blocksReportDesignReadiness": True},
]
ENVELOPE5_SHA256 = "45de2b0a12fc2f1f41f3a4f50b22b5e177fad58b19e5cc5072ff808c737e789d"
C01_COMMANDS = COMMANDS
C01_RENDERERS = ["human", "json", "agent", "html"]
C01_GOLDENS = ["interrupted-before-settle"]
INTEGRATION_OBLIGATIONS = [
    {"id": "RP-OBL-C01", "title": "Pre-Run interruption has no admissible envelope form",
     "owner": "command-envelope owner (workflows-and-surfaces section 8 envelope kinds, D9 termination prose at lines 1340-1367) with the workflow owner (section 1 cancellation)",
     "status": "pending-integration",
     "gap": "An invocation interrupted before any committed Run or query record, with no earlier recorded failure detail, has no admissible command-envelope:4/5 form: kind=failure requires non-empty errors (errors=[] only for REQUEST.UNKNOWN_OPTION) and no DomainDetailCode names an interruption. Host rule J-ENV-INTERRUPTION-DETAIL admits an interruption failure only with errors equal to the exact in-step-order list of recorded earlier request-rejected/operational-failed domainDetails of this invocation's ledger (real details are delivered under envelope5 now); an invented, changed or reordered detail is refused. The empty form stays pending.",
     "affected": {"commands": C01_COMMANDS, "renderers": C01_RENDERERS, "workflowGoldens": C01_GOLDENS},
     "parentDependency": {"candidateSchemaId": "urn:opensip:product-v1:workflows:evaluator3:command-envelope:6",
                          "subject": "/tmp/opensip-implementation/m1-interruption-envelope-subject-01",
                          "subjectManifestSha256": "76897423bc4dd3bfaecbf6a6a0cddfe082c8545f1d4d178b62ff01753f8d71bf",
                          "envelope6ParentEnvelope5Sha256": ENVELOPE5_SHA256,
                          "standing": "root-authored, unselected, conditional on this unaccepted envelope5; review m1-interruption-envelope-review-01 is accept-conditional pending F1 owner prose amendment, F2 named host ledger join refusing Run erasure, F3 verification of the post-commit carrier for query-class commands",
                          "adoptedByThisCandidate": False},
     "closureCriterion": ["an accepted envelope successor (envelope6 or another) with the F1 prose amendment",
                          "a named host admission join tying the empty-errors interruption form to a ledger with no committed Run and phase before-settle (F2), with refusal goldens",
                          "a verified post-commit interruption carrier for candidates/inspect/review-brief after a committed Run (F3)",
                          "this report candidate rebound to that successor: envelope parent sha256, report schema $ref, inventory/coverage rows and the pending goldens turned into delivered goldens"],
     "blocksM1FinalIntegration": True,
     "carrierEffectHere": "envelope5 bytes unchanged so the envelope6 parent binding stays valid; no report carrier, envelope form or error detail is invented; pending expected-refusal goldens document the gap and are counted as not delivered"},
    {"id": "RP-OBL-C02", "title": "Cancellation Run selection successor",
     "owner": "workflow owner (section 1 cancellation; workflows_model.v1.py run_invocation)", "status": "pending-integration",
     "gap": "The current owner model names the last committed Run among required steps. Root interruption successor03 (m1-interruption-envelope-subject-03, manifest dcec8ab9ad2f638a9a7ae6332d27485011fad002faeef05fc6e7c8f7c11d4e14, unreviewed, not selected) selects the last completed analysis/verify Run in step order including optional steps; 6 of its 72 owner-model cases change, exits and step outcomes do not.",
     "closureCriterion": ["the successor is accepted by review and root", "report_model.invocation_aggregate and the cancellation goldens are rebased to it together with the prose and model line", "the settled required-only D9 aggregate stays unchanged"],
     "blocksM1FinalIntegration": True, "carrierEffectHere": "this candidate keeps the current owner model (required-only); no html builtin variant plans an optional analysis step, so no bound report ledger differs today"},
    {"id": "RP-OBL-P01", "title": "analyze import planning selector",
     "owner": "command/workflow owner (command-inventory analyze row and ImportParams)", "status": "pending-owner-decision",
     "gap": "The analyze inventory kind summary lists an import step, but the declared analyze grammar supplies no ImportParams and no owner text states when analyze plans it; owner case required-depends-on-optional-refused shows only that an optional import cannot feed a required analysis.",
     "closureCriterion": ["the owner either states the analyze import planning condition with its requirement/dependency/gate and grammar, or removes import from the analyze kind summary", "the planning record adds that variant as plannable with admission cases"],
     "blocksM1FinalIntegration": False, "carrierEffectHere": "analyze reports project the plannable primary variant only; a planned import step is refused J-LEDGER-PLAN, never admitted with an invented shape"},
    {"id": "RP-OBL-L01", "title": "Invocation record codec bound",
     "owner": "workflow/identity owner (invocation:3 record admission)", "status": "pending-owner-statement",
     "gap": "The report ledger bound is structural (StepTermination up to 6,476,835 B). If invocation:3 records are admitted through the exact canonical codec (4,194,304 B), no single recorded termination above that size is reachable and the ledger bound is loose.",
     "closureCriterion": ["the owner states whether and how invocation:3 records are codec-bounded", "the report ledger bound is re-derived from that statement", "RP-OBL-M01 measures the maximal document either way"],
     "blocksM1FinalIntegration": False, "carrierEffectHere": "structural bound retained; no codec bound is assumed"},
    {"id": "RP-OBL-K01", "title": "Coverage module-milestone key for crates/reporting/src/assets.rs",
     "owner": "implementation-planning coverage owner (successor of docs/implementation/m1/metadata-v2/implementation-coverage.v2.json)", "status": "pending-owner-successor",
     "gap": "The historical coverage lacks moduleFirstMilestone for assets.rs, a delivery owner of the commands/version row (M1); the owned validator stops there.",
     "closureCriterion": ["the coverage owner adds the key in a reviewed coverage successor (value from its delivery rows; M1 here)", "the in-memory scoped workaround in this candidate is then removed"],
     "blocksM1FinalIntegration": True, "carrierEffectHere": "historical bytes unchanged; the workaround is applied in memory identically to base and overlay"},
]
REVIEW_ISSUES = [{"id": row["id"], "kind": "report-design-blocker" if row["blocksReportDesignReadiness"] else "report-conditional-requirement",
                  "standing": "open" if row["blocksReportDesignReadiness"] else "conditional-not-selected (current state satisfies the conditional requirement; does not hold any row open)",
                  "finding": row["gapKind"] + "; closure: " + row["closureCriterion"],
                  "affects": ["reportFeatures:" + FEATURES[row["featureId"]][0]] if row["blocksReportDesignReadiness"] else []} for row in DESIGN_OBLIGATIONS] + [
    {"id": "RP-OBL-C01", "kind": "envelope-owner-integration-gap", "standing": "open; pending an accepted envelope successor before M1 final integration (envelope6 candidate unselected)",
     "finding": INTEGRATION_OBLIGATIONS[0]["gap"], "affects": ["commands:" + c for c in C01_COMMANDS] + ["renderers:" + r for r in C01_RENDERERS] + ["workflowGoldens:" + g for g in C01_GOLDENS]},
    {"id": "RP-OBL-P01", "kind": "command-planning-owner-gap", "standing": "open; pending owner decision (non-blocking for the report carrier)",
     "finding": INTEGRATION_OBLIGATIONS[2]["gap"], "affects": ["commands:analyze"]}]


def feature_states(command):
    return [{"featureId": f, "view": views[command], "state": "unavailable", "reason": reason, "obligationId": obligation}
            for f, (_, obligation, reason, views) in sorted(FEATURES.items()) if command in views]


def design_register():
    blockers = [r["id"] for r in DESIGN_OBLIGATIONS if r["blocksReportDesignReadiness"]]
    obligations = []
    for row in DESIGN_OBLIGATIONS:
        row = dict(row, standing="proposal to the owning design unit; not accepted by that owner; closes only with that owner's reviewed successor and a delivered report carrier")
        if row["id"] == "RP-DO-11":
            row["integrationNote"] = "implies an invocation:3 successor (observed attempt duration) and a report ledger successor after M1 integration"
        if row["id"] == "RP-DO-12":
            row["integrationNote"] = "history stays recent-only (baseline source, then prior commit sequence); explicit older Run selection is not delivered"
        obligations.append(row)
    return {"schemaVersion": 1, "standing": "author-06 design and integration obligation register; proposals to other owners, not approval or completed features",
            "readiness": {"carrierUnit": "candidate for review: shape/admission of delivered carriers (envelope5 fit, report-projection:1 ledger/panels/codec/budget)",
                          "reportDesign": "blocked", "auditG10": "open", "blockers": blockers,
                          "m1FinalIntegrationBlockers": [r["id"] for r in INTEGRATION_OBLIGATIONS if r["blocksM1FinalIntegration"]]},
            "obligations": obligations, "integrationObligations": INTEGRATION_OBLIGATIONS}


# ---------------------------------------------------------------------------
# coverage overlay (commands, reportFeatures, contractSections, review issues)

REPORT_FEATURE_OWNERS = {
    "R03": ["apps/report/src/overview-view.ts", "crates/reporting/src/projection.rs"],
    "R14": ["apps/report/src/history-view.ts", "crates/reporting/src/projection.rs"],
    "R07": ["apps/report/src/symbol-detail-view.ts", "crates/reporting/src/projection.rs"],
    "R08": ["apps/report/src/graph-view.ts", "crates/reporting/src/projection.rs"],
    "R10": ["apps/report/src/graph-view.ts", "crates/reporting/src/projection.rs"],
    "R11": ["apps/report/src/symbol-detail-view.ts", "crates/reporting/src/projection.rs"],
    "R12": ["apps/report/src/graph-view.ts", "crates/reporting/src/projection.rs"],
    "R15": ["crates/reporting/src/projection.rs", "apps/report/src/report-data.ts"],
    "R16": ["apps/report/src/report-view.ts", "apps/report/src/report-data.ts"],
    "R17": ["crates/reporting/src/html_embedding.rs", "apps/report/src/report-data.ts"],
}
SCOPED_VALIDATOR_WORKAROUND = {"moduleFirstMilestone": {"add": {"crates/reporting/src/assets.rs": "M1"}},
                               "appliesIdentically": ["base implementation-coverage.v2.json", "applied overlay"],
                               "reason": "pre-existing key-set condition in the historical coverage: delivery owner crates/reporting/src/assets.rs (commands/version, M1) is absent from moduleFirstMilestone; the owned validator stops there before per-row checks",
                               "valueDerivation": "M1 is the milestone of the only delivery row that owns crates/reporting/src/assets.rs (commands/version). The owned validator also passes with M0 and refuses M6, so the check proves this key alone, not the value.",
                               "owner": "implementation-planning coverage owner; closes with RP-OBL-K01, not in this candidate",
                               "historicalBytesChanged": False}


def coverage_overlay(inv5):
    planning = _load("check_implementation_planning", ARCH / "docs/operations/check_implementation_planning.py")
    base_raw = (MV2 / "implementation-coverage.v2.json").read_bytes()
    base = json.loads(base_raw)
    sources_now, sources_next = {}, {}
    for key, pin in base["sources"].items():
        raw = (ARCH / pin["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == pin["sha256"], pin["path"]
        value = json.loads(raw) if pin["path"].endswith(".json") else raw.decode()
        sources_now[key] = value
        sources_next[key] = value
    sources_next["commands"] = inv5
    sources_next["workflows-and-surfaces"] = overridden_text(base["sources"]["workflows-and-surfaces"]["path"])
    expected_now = planning.expected_groups(sources_now)
    expected_next = planning.expected_groups(sources_next)
    feature_issue = {}
    for row in DESIGN_OBLIGATIONS:
        if row["blocksReportDesignReadiness"]:
            feature_issue.setdefault(FEATURES[row["featureId"]][0], []).append(row["id"])
    c01_rows = {("commands", c) for c in C01_COMMANDS} | {("renderers", r) for r in C01_RENDERERS} | {("workflowGoldens", g) for g in C01_GOLDENS}
    c01_method = (" Open RP-OBL-C01: an interruption before any committed Run has no admissible envelope form; this row cannot be verified for that"
                  " situation until an accepted envelope successor and host ledger join exist. An unrelated error detail is not an acceptable substitute.")
    changes, additions = [], []
    for group, rows in base["groups"].items():
        for index, row in enumerate(rows):
            key, selector, value = expected_now[group][row["id"]]
            assert row["source"] == {"key": key, "selector": selector, "valueSha256": planning.digest(value)}, (group, row["id"])
            nkey, nselector, nvalue = expected_next[group][row["id"]]
            change = {"group": group, "index": index, "id": row["id"], "source": {"key": nkey, "selector": nselector, "valueSha256": planning.digest(nvalue)}}
            fields = {}
            if group == "commands":
                for field in ("requestClass", "authorizationClass", "formats", "parityFields"):
                    if row[field] != nvalue[field]:
                        fields[field] = nvalue[field]
            if group == "commands" and row["id"] == "fit":
                change["verificationMethod"] = ("Admit advisoryReport: sealed first candidate.list page with the exact request, candidate-list joins, parity equality, page/count/cursor joins; "
                                                "--ephemeral non-authoritative null parity; read all nine parity fields at advisoryDispatch.parityPaths identically in human, JSON, HTML and agent output; "
                                                "after-commit query-step outcomes and required renderer failure follow the owned D9 aggregate (per-renderer goldens).")
            if group == "reportFeatures":
                change["owners"] = REPORT_FEATURE_OWNERS.get(row["id"], row["owners"])
                blocked = sorted(feature_issue.get(row["id"], []))
                method = ("Deliver the feature behavior in the built offline report from the admitted report-projection:1 carrier (contract section 12 map); "
                          "reference admission is not browser qualification.")
                if blocked:
                    method += (" Delivered behavior is required: an unavailable feature-state disclosure does not satisfy this row; it stays open on "
                               + ", ".join(blocked) + " until the owning design successor is reviewed and carried.")
                    change["reviewIssues"] = blocked
                change["verificationMethod"] = method
            if (group, row["id"]) == ("commands", "analyze"):
                change["reviewIssues"] = sorted(set(row["reviewIssues"]) | set(change.get("reviewIssues", [])) | {"RP-OBL-P01"})
                change["verificationMethod"] = change.get("verificationMethod", row["verification"]["method"]) + (
                    " Open RP-OBL-P01: verify the planned expansion against owner/builtin-step-planning.v1.json; the import kind is not plannable by the declared grammar until the owner decides.")
            if (group, row["id"]) in c01_rows:
                change["reviewIssues"] = sorted(set(row["reviewIssues"]) | set(change.get("reviewIssues", [])) | {"RP-OBL-C01"})
                change["verificationMethod"] = change.get("verificationMethod", row["verification"]["method"]) + c01_method
            if fields:
                change["fields"] = fields
            if change["source"] != row["source"] or fields or "verificationMethod" in change or "owners" in change:
                changes.append(change)
    for group, expected_rows in expected_next.items():
        known = {r["id"] for r in base["groups"][group]}
        for row_id, (key, selector, value) in expected_rows.items():
            if row_id not in known:
                assert group == "workflowGoldens" and row_id == FIT_GOLDEN["id"], (group, row_id)
                additions.append({"group": group, "row": {
                    "id": row_id, "source": {"key": key, "selector": selector, "valueSha256": planning.digest(value)},
                    "milestone": "M4", "owners": ["crates/host/src/review.rs"],
                    "verification": {"owner": "crates/host/tests/workflow_tests.rs", "kind": "planned-behavioral-test",
                                     "method": "Exercise fit --ephemeral and compare the complete success termination, null run-id and unavailable candidate parity in every renderer.", "standing": "not-executed"},
                    "reviewIssues": [], "command": "fit", "sourceClass": "success", "sourceExitCode": 0}})
    return {"schemaVersion": 1,
            "standing": "AUTHOR-04 candidate overlay; implementation-coverage.v2.json bytes remain historical and unchanged",
            "base": {"path": "docs/implementation/m1/metadata-v2/implementation-coverage.v2.json", "sha256": hashlib.sha256(base_raw).hexdigest(), "bytes": len(base_raw)},
            "sourceSuccession": {"commands": "owner/command-inventory.v5.json", "workflows-and-surfaces": "conditional passage override at line 1106"},
            "rowChanges": changes, "rowAdditions": additions, "reviewIssueAdditions": REVIEW_ISSUES,
            "scopedValidatorWorkaround": SCOPED_VALIDATOR_WORKAROUND}


def apply_overlay(base, overlay, with_workaround):
    applied = copy.deepcopy(base)
    for change in overlay["rowChanges"]:
        row = applied["groups"][change["group"]][change["index"]]
        assert row["id"] == change["id"]
        row["source"] = change["source"]
        for field, value in change.get("fields", {}).items():
            row[field] = value
        if "owners" in change:
            row["owners"] = change["owners"]
        if "reviewIssues" in change:
            row["reviewIssues"] = change["reviewIssues"]
        if "verificationMethod" in change:
            row["verification"]["method"] = change["verificationMethod"]
    for addition in overlay["rowAdditions"]:
        applied["groups"][addition["group"]].append(addition["row"])
    applied["reviewIssues"] = applied["reviewIssues"] + overlay["reviewIssueAdditions"]
    if with_workaround:
        applied["moduleFirstMilestone"] = dict(applied["moduleFirstMilestone"], **overlay["scopedValidatorWorkaround"]["moduleFirstMilestone"]["add"])
    return applied


# ---------------------------------------------------------------------------
# derived bounds

def owner_documents():
    """The 28 schemas pinned by the accepted metadata-v2 sources.json (the same registry check_metadata.load admits)."""
    docs = {}
    for pin in read(MV2 / "sources.json")["schemas"]:
        raw = (ARCH / pin["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == pin["sha256"], pin["path"]
        doc = json.loads(raw)
        docs[doc["$id"]] = doc
    return docs


def _resolve(docs, base_id, reference):
    target_id, _, fragment = reference.partition("#")
    doc_id = target_id or base_id
    node = docs[doc_id]
    for token in [t for t in fragment.split("/") if t]:
        node = node[token]
    return doc_id, node


def _pattern_length(pattern):
    """Maximum length of simple anchored patterns used by identifiers (literal / [class]{n} / (?![\\s\\S])); None when not simple."""
    body = pattern
    if body.startswith("^"):
        body = body[1:]
    body = body.replace("(?![\\s\\S])", "")
    total, i = 0, 0
    while i < len(body):
        ch = body[i]
        if ch == "[":
            end = body.index("]", i)
            i = end + 1
            count = 1
            match = re.match(r"\{(\d+)(?:,(\d+))?\}", body[i:])
            if match:
                count = int(match.group(2) or match.group(1))
                i += match.end()
            elif i < len(body) and body[i] in "*+?":
                return None
            total += count
        elif ch in "()|*+?.\\{":
            return None
        else:
            total += 1
            i += 1
    return total


def structural_max_bytes(docs, base_id, node, stack=()):
    """Upper bound of canonical bytes of any value valid under node (strings count 6 bytes per character for escapes). inf when unbounded."""
    inf = float("inf")
    if node is True:
        return inf
    if not isinstance(node, dict):
        return inf
    if "$ref" in node:
        key = (base_id, node["$ref"])
        if key in stack:
            return inf
        doc_id, target = _resolve(docs, base_id, node["$ref"])
        own = structural_max_bytes(docs, doc_id, target, stack + (key,))
        rest = {k: v for k, v in node.items() if k not in ("$ref", "description")}
        return min(own, structural_max_bytes(docs, base_id, rest, stack)) if rest else own
    if "const" in node:
        return len(M.canonical(node["const"]))
    if "enum" in node:
        return max(len(M.canonical(v)) for v in node["enum"])
    candidates = []
    for keyword in ("oneOf", "anyOf"):
        if keyword in node:
            candidates.append(max(structural_max_bytes(docs, base_id, child, stack) for child in node[keyword]))
    if "allOf" in node:
        candidates.append(min(structural_max_bytes(docs, base_id, child, stack) for child in node["allOf"]))
    types = node.get("type")
    types = types if isinstance(types, list) else ([types] if types else [])
    own = None
    if types:
        values = []
        for t in types:
            if t == "null":
                values.append(4)
            elif t == "boolean":
                values.append(5)
            elif t == "integer":
                low, high = node.get("minimum", -(2 ** 63)), node.get("maximum", 2 ** 64 - 1)
                values.append(max(len(str(low)), len(str(high))))
            elif t == "string":
                if "pattern" in node and _pattern_length(node["pattern"]) is not None:
                    values.append(2 + _pattern_length(node["pattern"]))
                elif "maxLength" in node:
                    values.append(2 + 6 * node["maxLength"])
                else:
                    values.append(inf)
            elif t == "array":
                if "maxItems" not in node or not isinstance(node.get("items"), dict):
                    values.append(inf)
                else:
                    item = structural_max_bytes(docs, base_id, node["items"], stack)
                    n = node["maxItems"]
                    values.append(2 + n * item + max(n - 1, 0))
            elif t == "object":
                if node.get("additionalProperties") is not False or "patternProperties" in node:
                    values.append(inf)
                else:
                    props = node.get("properties", {})
                    values.append(2 + sum(len(M.canonical(k)) + 1 + structural_max_bytes(docs, base_id, v, stack) for k, v in props.items()) + max(len(props) - 1, 0))
        own = max(values)
    if own is not None:
        candidates.append(own)
    return min(candidates) if candidates else inf


DERIVATION_ID = "urn:opensip:report-projection:author-04:derivation"


def derivation_schemas(recorded, total):
    """Structural upper-bound schemas for one command's ledger: exactly the owner references used by InvocationLedgerV1/LedgerStepV1."""
    d = DERIVATION_ID + "#/$defs/"
    attempt = closed(["executionId", "outcome"], {"executionId": ref(I + "Attempt/properties/executionId"), "outcome": ref(I + "Attempt/properties/outcome"),
                                                  "faultCause": ref(I + "Attempt/properties/faultCause"), "retried": ref(I + "Attempt/properties/retried")})
    head = {"stepId": ref(C + "StepId"), "kind": ref(I + "StepKind"), "requirement": ref(I + "StepSpec/properties/requirement"),
            "dependsOn": ref(I + "StepSpec/properties/dependsOn"), "dependencyGate": ref(I + "StepSpec/properties/dependencyGate"),
            "planRole": {"type": "string", "enum": PLAN_ROLES}, "recorded": {"type": "boolean"}}
    recorded_step = closed(list(head), dict(head, outcome=ref(I + "StepOutcome"), skipReason=ref(I + "StepResult/properties/skipReason"),
                                            attempts={"type": "array", "maxItems": 3, "items": attempt}, termination=ref(C + "StepTermination"), analysisRunId=ref(C + "RunId")))
    ledger = closed([], {"requestId": ref(C + "RequestId"), "workflow": ref(I + "WorkflowRef"), "mode": ref(I + "Mode"), "cancellation": ref(I + "Cancellation"),
                         "planVariant": {"type": "string", "enum": PLAN_VARIANTS},
                         "steps": {"type": "array", "maxItems": recorded, "items": ref(d + "RecordedStep")},
                         "missingChildren": {"type": "array", "maxItems": total, "items": closed(["stepId", "missing"], {"stepId": ref(C + "StepId"),
                                             "missing": {"type": "string", "enum": ["render-in-progress", "step-result-not-recorded", "attempts-not-recorded"]}})},
                         "provenance": {"const": PROVENANCE["ledger"]}})
    return {"$id": DERIVATION_ID, "$defs": {"RecordedStep": recorded_step, "UnrecordedStep": closed(list(head), head), "Ledger": ledger}}


def derivations():
    """Mandatory root bounds from owner schemas (structural maxima: 6 bytes per bounded character, fixed-length identifier patterns,
    integer extremes, closed objects), the finite per-command step count and the render-step law (render is never recorded in a projection)."""
    docs = owner_documents()
    common_id = "urn:opensip:product-v1:workflows:evaluator3:common:3"
    termination = structural_max_bytes(docs, common_id, docs[common_id]["$defs"]["StepTermination"])
    pinned = structural_max_bytes(docs, common_id, docs[common_id]["$defs"]["PinnedPurgeDisclosure"])
    inventory = inventory5()
    per_command = {}
    for command in COMMANDS:
        kinds = next(c for c in inventory["commands"] if c["name"] == command)["steps"]
        renders = kinds.count("render")
        recorded = len(kinds) - renders
        schemas = derivation_schemas(recorded, len(kinds))
        local = dict(docs, **{DERIVATION_ID: schemas})
        recorded_step = structural_max_bytes(local, DERIVATION_ID, schemas["$defs"]["RecordedStep"])
        unrecorded_step = structural_max_bytes(local, DERIVATION_ID, schemas["$defs"]["UnrecordedStep"])
        ledger = structural_max_bytes(local, DERIVATION_ID, schemas["$defs"]["Ledger"]) + renders * (1 + unrecorded_step)
        per_command[command] = {"steps": len(kinds), "renderSteps": renders, "maxRecordedSteps": recorded,
                                "recordedStepMaxBytes": recorded_step, "unrecordedStepMaxBytes": unrecorded_step, "ledgerMaxBytes": ledger}
    ledger_max = max(v["ledgerMaxBytes"] for v in per_command.values())
    assert all(isinstance(v["ledgerMaxBytes"], int) for v in per_command.values()), "unbounded ledger member"
    root_members = root_member_maxima()
    overhead = 2 + sum(len(M.canonical(k)) + 1 for k in ROOT_KEYS) + (len(ROOT_KEYS) - 1)
    document = overhead + CODEC_MAX_BYTES + ledger_max + M.EXPLORATION_CAP + sum(root_members.values())
    return {"standing": "structural upper bounds derived from pinned owner schemas; no measured or performance value",
            "stepTerminationStructuralMaxBytes": termination, "pinnedPurgeDisclosureStructuralMaxBytes": pinned,
            "envelopeCodecMaxBytes": CODEC_MAX_BYTES,
            "ledgerNote": "no owner bounds the retained invocation:3 record by the envelope codec, so recorded step terminations are bounded structurally, never truncated",
            "perCommand": per_command, "ledgerMaxBytes": ledger_max, "rootKeyOverheadBytes": overhead, "rootMemberMaxBytes": root_members,
            "explorationMaxCanonicalBytes": M.EXPLORATION_CAP,
            "documentMaxBytes": document,
            "documentMaxFormula": "rootKeyOverhead + envelopeCodecMax + max(per-command ledgerMax) + explorationMax + sum(rootMemberMax)",
            "effectiveExplorationBudget": "min(explorationMax, documentMax - rootKeyOverhead - C(envelope) - C(ledger) - sum(rootMemberMax)); equal to explorationMax for every admissible envelope and ledger by construction"}


ROOT_KEYS = ["budgetProfile", "command", "disclosures", "documentProvenance", "envelope", "featureStates", "invocationLedger", "panels", "pathDisclosure",
             "renderer", "reportObservedAt", "schemaFamily", "schemaMajor", "staticParity", "supportedReportViews"]


def root_member_maxima():
    b = budget_base()
    out = {"schemaFamily": len(M.canonical("opensip.product.report-projection")), "schemaMajor": 1,
           "command": max(len(M.canonical(c)) for c in COMMANDS), "renderer": len(M.canonical({"format": "html", "version": 1})),
           "supportedReportViews": max(len(M.canonical(v)) for v in VIEWS.values()),
           "featureStates": max(len(M.canonical(feature_states(c))) for c in COMMANDS),
           "documentProvenance": len(M.canonical(PROVENANCE["document"])),
           "reportObservedAt": len(M.canonical("2026-09-14T12:00:00Z")),
           "pathDisclosure": len(M.canonical({"mode": "local-editor-links", "editorScheme": "vscode-insiders"})),
           "staticParity": len(M.canonical({"format": M.STATIC_FORMAT, "textSha256": "a" * 64, "textBytes": 9007199254740991})),
           "disclosures": len(M.canonical({"graphPlannedSubjects": 9007199254740991, "graphDescriptorNotRetainedSubjectsHostAsserted": 9007199254740991, "historyPriorRunsInSnapshotHostAsserted": 9007199254740991}))}
    # budgetProfile embeds documentMaxBytes itself: bound with the maximum Uint53 digit width.
    out["budgetProfile"] = len(M.canonical(dict(b, documentMaxBytes=9007199254740991, ledgerMaxBytes=9007199254740991, rootMemberMaxBytes=9007199254740991, graphPublicBounds=GRAPH_BOUNDS)))
    return out


def budget_base():
    return {
        "profileId": "opensip.report-projection.development-caps.4",
        "standing": "development caps derived from owner schemas and the accepted exact codec; not measured performance; not release qualification",
        "envelopeMaxCanonicalBytes": CODEC_MAX_BYTES,
        "embeddedPanelOwnerMaxCanonicalBytes": CODEC_MAX_BYTES,
        "explorationMaxCanonicalBytes": M.EXPLORATION_CAP,
        "ownerCodecDepth": 32,
        "maxJsonDepth": 38,
        "maxGraphSlots": M.MAX_SLOTS,
        "graphPageSizeLadder": M.LADDER,
        "maxGraphItemsPerSlot": M.LADDER[0],
        "maxPlannedSubjects": M.MAX_PLANNED_SUBJECTS,
        "maxSubjectIndexRows": subject_index_bound(),
        "maxEvidenceEntries": 3956,
        "maxHistoryRuns": 4,
        "maxHistoryFindingsPerRun": 5526,
        "maxCatalogRules": 512,
        "maxCapabilityDeclarations": 128,
        "projectionPriority": M.PROJECTION_PRIORITY,
        "browserLimits": {"maxLaidOutGraphNodes": 2000, "maxLaidOutGraphEdges": 4000, "maxRenderedTableRows": 500},
    }


GRAPH_BOUNDS = {"maxItemsPerOperation": 100000, "maxVisitedNodes": 1000000}


def budget():
    d = derivations()
    bounds = read(EV3 / "graph-query.schema.json")["$defs"]["Bounds"]["properties"]
    assert GRAPH_BOUNDS == {k: bounds[k]["const"] for k in GRAPH_BOUNDS}
    return dict(budget_base(), ledgerMaxBytes=d["ledgerMaxBytes"], rootMemberMaxBytes=sum(d["rootMemberMaxBytes"].values()), documentMaxBytes=d["documentMaxBytes"],
                graphPublicBounds=GRAPH_BOUNDS)


def subject_index_bound():
    neighbor_slots = 4
    return neighbor_slots * (2 * M.LADDER[0] + 1) + (M.LADDER[0] + 1) + 65 + M.MAX_PLANNED_SUBJECTS


PROVENANCE = {
    "document": {"verifiedInDocument": ["disclosure-counts-recomputed-from-panels", "feature-states-exact-per-command", "renderer-gating-against-inventory5",
                                        "report-command-equals-ledger-builtin-workflow"],
                 "hostAsserted": ["budget-profile-is-development-caps", "report-observed-at-is-host-clock"]},
    "ledger": {"verifiedInDocument": ["aggregate-termination-recomputed-with-cancellation-law", "attempt-execution-ids-unique", "generic-step-dag-law",
                                      "missing-children-recomputed", "request-id-equals-envelope", "run-id-produced-by-primary-analysis-step", "skipped-records-supported-by-dependencies",
                                      "steps-equal-a-plannable-builtin-planning-variant", "workflow-equals-report-command"],
               "hostAsserted": ["ledger-is-this-invocation-record-at-projection-time", "planning-variant-condition-held"]},
    "evidence": {"verifiedInDocument": ["coverage-id-equals-envelope-run-coverage-id", "coverage-keys-unique", "item-counts-consistent", "rejected-delta-arithmetic-against-effective-budget"],
                 "hostAsserted": ["byte-budget-rejected-delta-measurement", "entries-are-retained-stream-prefix-of-coverage-id"]},
    "graph": {"verifiedInDocument": ["cursor-reference-form", "owner-page-law-total-equals-produced-prefix-coverage-continuation", "path-rows-simple-path-law",
                                     "project-equals-envelope-project", "reach-rows-order-and-depth", "rejected-delta-arithmetic-against-effective-budget",
                                     "request-and-response-run-equal-subject-run", "rows-match-relation-rung-direction-endpoint-and-kinds",
                                     "slot-plan-recomputed-from-policy-subjects-and-stated-resolution", "subject-index-recomputed-at-governed-pointers"],
              "hostAsserted": ["byte-budget-rejected-delta-measurement", "descriptor-not-retained-states", "page-size-reduction-reissued-owner-query", "response-is-owner-admitted-query-result"]},
    "comparison": {"verifiedInDocument": ["comparison-id-equals-envelope-run", "current-run-equals-envelope-run"], "hostAsserted": ["comparison-is-retained-admitted-result"]},
    "history": {"verifiedInDocument": ["baseline-id-equals-comparison-baseline", "baseline-source-excluded-from-prior-runs", "item-counts-consistent", "not-current-run",
                                       "prior-run-count-arithmetic-given-host-snapshot-count", "prior-runs-strictly-descending-below-current-sequence",
                                       "rejected-delta-arithmetic-against-effective-budget", "rows-equal-requested-runs"],
                "hostAsserted": ["baseline-source-run-is-baseline-descriptor-run", "byte-budget-rejected-delta-measurement", "findings-belong-to-history-run",
                                 "prior-runs-are-snapshot-receipts", "prior-runs-in-snapshot-count"]},
    "rules": {"verifiedInDocument": ["finding-rules-listed", "plan-id-equals-envelope-run-plan"], "hostAsserted": ["policy-digest-is-plan-policy-digest", "rules-are-plan-bound-effective-policy"]},
    "capabilities": {"verifiedInDocument": ["registry-sha256-integrity-only"], "hostAsserted": ["registry-is-host-release-declaration"]},
}


def state_wrapper(data_ref):
    return {"oneOf": [closed(["state", "data"], {"state": {"const": "present"}, "data": ref(data_ref)}), ref("#/$defs/PanelNotPresentV1")]}


def report_schema():
    b = budget()
    budget_props = {key: {"const": value} for key, value in b.items()}
    defs = {
        "ReportCommand": {"type": "string", "enum": COMMANDS, "description": "Exactly the command-inventory:5 commands whose formats contain html."},
        "ReportViewId": {"type": "string", "enum": VIEW_IDS},
        "FeatureId": {"type": "string", "enum": sorted(FEATURES)},
        "FeatureStateV1": closed(["featureId", "view", "state", "reason", "obligationId"], {
            "featureId": ref("#/$defs/FeatureId"), "view": ref("#/$defs/ReportViewId"), "state": {"const": "unavailable"},
            "reason": {"type": "string", "enum": FEATURE_REASONS}, "obligationId": {"type": "string", "pattern": "^RP-DO-[0-9]{2}(?![\\s\\S])"}},
            description="Required inventory feature not delivered by this carrier, with its precise cause and design obligation (owner/design-obligations.v1.json). Disclosure only: it never satisfies delivery of the feature."),
        "BudgetProfileV1": closed(sorted(b), budget_props, description="Development caps derived from owner schemas, the exact codec and per-command ledger step counts (contract section 9). Not measured performance or release qualification."),
        "PathDisclosureV1": {"oneOf": [closed(["mode"], {"mode": {"const": "relative-only"}}),
                                       closed(["mode", "editorScheme"], {"mode": {"const": "local-editor-links"}, "editorScheme": {"type": "string", "enum": ["vscode", "vscode-insiders", "idea"]}})]},
        "StaticParityV1": closed(["format", "textSha256", "textBytes"], {
            "format": {"const": M.STATIC_FORMAT}, "textSha256": ref(C + "Sha256Hex"), "textBytes": ref(C + "Uint53")},
            description="Digest of the script-independent static parity section: declared parity pointer lines, disclosure count lines, then the canonical envelope. Admission recomputes it."),
        "DisclosuresV1": closed(["graphPlannedSubjects", "graphDescriptorNotRetainedSubjectsHostAsserted", "historyPriorRunsInSnapshotHostAsserted"], {
            "graphPlannedSubjects": nullable(ref(C + "Uint53")), "graphDescriptorNotRetainedSubjectsHostAsserted": nullable(ref(C + "Uint53")), "historyPriorRunsInSnapshotHostAsserted": nullable(ref(C + "Uint53"))},
            description="Counts shown in the static section. The descriptor-not-retained count and the snapshot count are host assertions, named as such; admission recomputes the counts from the document but cannot prove host retention. Browser admission is shape, codec and internal joins only and must not present verifiedInDocument labels as semantic proof."),
        "InvocationLedgerV1": closed(["requestId", "workflow", "mode", "cancellation", "planVariant", "steps", "missingChildren", "provenance"], {
            "requestId": ref(C + "RequestId"), "workflow": ref(I + "WorkflowRef"), "mode": ref(I + "Mode"), "cancellation": ref(I + "Cancellation"),
            "planVariant": {"type": "string", "enum": PLAN_VARIANTS, "description": "The owner/builtin-step-planning.v1.json variant this invocation planned; its planning condition is a host assertion."},
            "steps": {"type": "array", "minItems": 1, "maxItems": 64, "items": ref("#/$defs/LedgerStepV1"), "x-opensip-order": "sequence"},
            "missingChildren": {"type": "array", "maxItems": 64, "items": closed(["stepId", "missing"], {"stepId": ref(C + "StepId"),
                                "missing": {"type": "string", "enum": ["render-in-progress", "step-result-not-recorded", "attempts-not-recorded"]}}), "x-opensip-order": "sequence"},
            "provenance": {"const": PROVENANCE["ledger"]}},
            description="Bounded projection of this invocation's invocation:3 record at projection time (R03), including its cancellation carrier. Owner fields keep their owner schemas; content is bounded by the record's exact codec."),
        "LedgerStepV1": closed(["stepId", "kind", "requirement", "dependsOn", "dependencyGate", "planRole", "recorded"], {
            "stepId": ref(C + "StepId"), "kind": ref(I + "StepKind"), "requirement": ref(I + "StepSpec/properties/requirement"),
            "dependsOn": ref(I + "StepSpec/properties/dependsOn"), "dependencyGate": ref(I + "StepSpec/properties/dependencyGate"),
            "planRole": {"type": "string", "enum": PLAN_ROLES}, "recorded": {"type": "boolean"},
            "outcome": ref(I + "StepOutcome"), "skipReason": ref(I + "StepResult/properties/skipReason"),
            "attempts": {"type": "array", "maxItems": 3, "items": closed(["executionId", "outcome"], {
                "executionId": ref(I + "Attempt/properties/executionId"), "outcome": ref(I + "Attempt/properties/outcome"),
                "faultCause": ref(I + "Attempt/properties/faultCause"), "retried": ref(I + "Attempt/properties/retried")}), "x-opensip-order": "sequence"},
            "termination": ref(C + "StepTermination"), "analysisRunId": ref(C + "RunId")},
            allOf=[{"if": {"properties": {"recorded": {"const": True}}}, "then": {"required": ["outcome", "attempts", "termination"]},
                    "else": {"not": {"anyOf": [{"required": [k]} for k in ["outcome", "skipReason", "attempts", "termination", "analysisRunId"]]}}},
                   {"if": {"required": ["outcome"], "properties": {"outcome": {"const": "skipped"}}}, "then": {"required": ["skipReason"]}, "else": {"not": {"required": ["skipReason"]}}}]),
        "PanelsV1": closed([], {name: ref("#/$defs/%sPanelStateV1" % name.capitalize()) for name in ["evidence", "graph", "comparison", "history", "catalog"]}),
        "PanelNotPresentV1": {"oneOf": [
            closed(["state", "reason"], {"state": {"const": "omitted"}, "reason": {"type": "string", "enum": ["not-selected", "exploration-budget-exceeded"]}}),
            closed(["state", "reason"], {"state": {"const": "unavailable"}, "reason": {"type": "string", "enum": ["no-admitted-result", "no-run-identity", "evidence-expired", "evidence-purged", "evidence-missing", "source-refused", "prerequisite-panel-not-present"]},
                                         "detail": ref(C + "DomainDetail")}, allOf=[{"if": {"properties": {"reason": {"const": "source-refused"}}}, "then": {"required": ["detail"]}}]),
            closed(["state", "reason"], {"state": {"const": "corrupt"}, "reason": {"const": "retained-bytes-corrupt"}, "detail": ref(C + "DomainDetail")}),
            closed(["state", "reason"], {"state": {"const": "incompatible"}, "reason": {"const": "retained-schema-major-unsupported"}, "detail": ref(C + "DomainDetail")})]},
        "EvidencePanelStateV1": state_wrapper("#/$defs/EvidencePanelV1"),
        "GraphPanelStateV1": state_wrapper("#/$defs/GraphPanelV1"),
        "ComparisonPanelStateV1": state_wrapper("#/$defs/ComparisonPanelV1"),
        "HistoryPanelStateV1": state_wrapper("#/$defs/HistoryPanelV1"),
        "CatalogPanelStateV1": state_wrapper("#/$defs/CatalogPanelV1"),
        "ItemProjectionV1": closed(["total", "omitted", "omissionCause"], {"total": ref(C + "Uint53"), "omitted": ref(C + "Uint53"),
                                                                           "omissionCause": {"type": "string", "enum": ["none", "item-cap", "byte-budget"]},
                                                                           "rejectedByteDelta": ref(C + "Uint53")},
                                   allOf=[{"if": {"properties": {"omissionCause": {"const": "byte-budget"}}}, "then": {"required": ["rejectedByteDelta"]}, "else": {"not": {"required": ["rejectedByteDelta"]}}}]),
        "EvidencePanelV1": closed(["coverageId", "entries", "entriesProjection", "provenance"], {
            "coverageId": ref(C + "CoverageId"), "entries": {"type": "array", "maxItems": b["maxEvidenceEntries"], "items": ref(N + "CoverageResultV3"), "x-opensip-order": "sequence"},
            "entriesProjection": ref("#/$defs/ItemProjectionV1"), "provenance": {"const": PROVENANCE["evidence"]}}),
        "SubjectResolutionV1": {"oneOf": [
            closed(["subjectId", "state", "endpoint"], {"subjectId": ref(C + "SubjectId"), "state": {"const": "resolved"}, "endpoint": ref(G + "GraphEndpoint")}),
            closed(["subjectId", "state"], {"subjectId": ref(C + "SubjectId"), "state": {"const": "descriptor-not-retained"}})]},
        "GraphPanelV1": closed(["policy", "subjectResolution", "slots", "slotsProjection", "subjectIndex", "provenance"], {
            "policy": {"const": "finding-subject-slot-plan.1"},
            "subjectResolution": {"type": "array", "minItems": 1, "maxItems": b["maxPlannedSubjects"], "items": ref("#/$defs/SubjectResolutionV1"), "x-opensip-order": "sequence"},
            "slots": {"type": "array", "maxItems": b["maxGraphSlots"], "items": ref("#/$defs/GraphSlotV1"), "x-opensip-order": "ordinal"},
            "slotsProjection": ref("#/$defs/ItemProjectionV1"),
            "subjectIndex": {"type": "array", "minItems": 1, "maxItems": b["maxSubjectIndexRows"], "items": closed(["subjectId", "endpoint"], {"subjectId": ref(C + "SubjectId"), "endpoint": ref(G + "GraphEndpoint")}),
                             "x-opensip-order": {"by": ["subjectId"]}},
            "provenance": {"const": PROVENANCE["graph"]}}),
        "GraphSlotV1": closed(["ordinal", "purpose", "anchorSubjectIds", "request", "response", "hostProjection"], {
            "ordinal": {"type": "integer", "minimum": 0, "maximum": b["maxGraphSlots"] - 1},
            "purpose": {"type": "string", "enum": ["neighborhood", "package-coupling", "reach", "path"]},
            "anchorSubjectIds": {"type": "array", "minItems": 1, "maxItems": 2, "items": ref(C + "SubjectId"), "x-opensip-order": "sequence"},
            "request": {"allOf": [ref(G + "GraphQueryRequestV1"), {"not": {"required": ["fieldSelection"]}, "properties": {
                "view": ref(G + "ResolvedView"), "operation": ref(G + "GraphOperation"), "completeness": {"const": "best-effort"},
                "page": closed(["size"], {"size": {"enum": b["graphPageSizeLadder"]}})}}]},
            "response": {"allOf": [ref(G + "GraphQueryResponseV1"), {"required": ["items"], "not": {"required": ["termination"]}, "properties": {"operation": ref(G + "GraphOperation")}}]},
            "hostProjection": closed(["continuation", "pageSizeCause"], {"continuation": {"type": "string", "enum": ["complete-page-set", "not-embedded", "operation-truncated-no-continuation"]},
                                                                         "pageSizeCause": {"type": "string", "enum": ["ladder-first", "byte-budget-reduced"]},
                                                                         "rejectedByteDelta": ref(C + "Uint53")},
                                     allOf=[{"if": {"properties": {"pageSizeCause": {"const": "byte-budget-reduced"}}}, "then": {"required": ["rejectedByteDelta"]}, "else": {"not": {"required": ["rejectedByteDelta"]}}}])}),
        "ComparisonPanelV1": closed(["comparison", "provenance"], {"comparison": ref(CMP), "provenance": {"const": PROVENANCE["comparison"]}}),
        "HistoryPanelV1": closed(["selection", "runs", "provenance"], {
            "selection": closed(["policy", "currentCommitSequence", "baselineId", "baselineSourceRunId", "priorRuns", "priorRunsInSnapshot", "requestedRunIds"], {
                "policy": {"const": "baseline-source-then-prior-commit-sequence.1"},
                "currentCommitSequence": {"type": "integer", "minimum": 0, "maximum": 18446744073709551615},
                "baselineId": nullable(ref(C + "BaselineId")), "baselineSourceRunId": nullable(ref(C + "RunId")),
                "priorRuns": {"type": "array", "maxItems": b["maxHistoryRuns"], "items": closed(["runId", "commitSequence"], {"runId": ref(C + "RunId"), "commitSequence": {"type": "integer", "minimum": 0, "maximum": 18446744073709551615}}), "x-opensip-order": "sequence"},
                "priorRunsInSnapshot": ref(C + "Uint53"),
                "requestedRunIds": {"type": "array", "minItems": 1, "maxItems": b["maxHistoryRuns"], "uniqueItems": True, "items": ref(C + "RunId"), "x-opensip-order": "sequence"}}),
            "runs": {"type": "array", "minItems": 1, "maxItems": b["maxHistoryRuns"], "items": ref("#/$defs/HistoryRunV1"), "x-opensip-order": "sequence"},
            "provenance": {"const": PROVENANCE["history"]}}),
        "HistoryRunV1": {"oneOf": [
            closed(["state", "runId", "commitSequence", "run", "findings", "findingsProjection"], {
                "state": {"const": "present"}, "runId": ref(C + "RunId"), "commitSequence": nullable({"type": "integer", "minimum": 0, "maximum": 18446744073709551615}),
                "run": {"allOf": [ref(I + "AnalysisResult"), {"required": ["runId"], "properties": {"authority": {"const": "authoritative"}}}]},
                "findings": {"type": "array", "maxItems": b["maxHistoryFindingsPerRun"], "uniqueItems": True, "items": ref(C + "FindingSurface"), "x-opensip-order": {"by": ["findingId"]}},
                "findingsProjection": ref("#/$defs/ItemProjectionV1")}),
            closed(["state", "runId", "availability"], {"state": {"const": "unavailable"}, "runId": ref(C + "RunId"),
                                                        "availability": {"type": "string", "enum": ["expired", "purged", "corrupt", "unavailable"]}, "detail": ref(C + "DomainDetail")})]},
        "CatalogPanelV1": closed(["rules", "capabilities"], {
            "rules": {"oneOf": [closed(["state", "data"], {"state": {"const": "present"}, "data": ref("#/$defs/RuleCatalogV1")}), ref("#/$defs/PanelNotPresentV1")]},
            "capabilities": {"oneOf": [closed(["state", "data"], {"state": {"const": "present"}, "data": ref("#/$defs/CapabilityCatalogV1")}), ref("#/$defs/PanelNotPresentV1")]}}),
        "RuleCatalogV1": closed(["source", "gateSeverityAtLeast", "rules", "provenance"], {
            "source": closed(["kind", "planId", "policyDigest"], {"kind": {"const": "run-plan-effective-policy"}, "planId": ref(C + "PlanId"), "policyDigest": ref(C + "Sha256Hex")}),
            "gateSeverityAtLeast": ref(P + "Severity"),
            "rules": {"type": "array", "minItems": 1, "maxItems": b["maxCatalogRules"], "items": ref(P + "Rule"), "x-opensip-order": "ruleId"},
            "provenance": {"const": PROVENANCE["rules"]}}),
        "CapabilityCatalogV1": closed(["source", "declarations", "provenance"], {
            "source": closed(["kind", "registrySha256"], {"kind": {"const": "release-capability-registry"}, "registrySha256": ref(C + "Sha256Hex")}),
            "declarations": ref(N + "ReleaseCapabilityRegistryV1"), "provenance": {"const": PROVENANCE["capabilities"]}}),
    }
    per_command = []
    for command in COMMANDS:
        surface = {"candidates": "candidate-list", "inspect": "candidate-inspection", "review-brief": "review-brief", "repair-preview": "repair-preview"}.get(command)
        env = {"properties": {"kind": {"enum": ["query", "failure"] if surface else ["run", "failure"]}}}
        if surface:
            env["properties"]["querySurface"] = {"const": surface}
        panels = {"required": PANELS[command]}
        forbidden = [p for p in ["evidence", "graph", "comparison", "history", "catalog"] if p not in PANELS[command]]
        if forbidden:
            panels["not"] = {"anyOf": [{"required": [p]} for p in forbidden]}
        if command == "audit":
            panels["properties"] = {"comparison": {"not": {"required": ["reason"], "properties": {"reason": {"const": "not-selected"}}}}}
        per_command.append({"if": {"properties": {"command": {"const": command}}}, "then": {"properties": {
            "supportedReportViews": {"const": VIEWS[command]}, "featureStates": {"const": feature_states(command)}, "envelope": env, "panels": panels}}})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": REPORT_ID,
        "title": "ReportProjection schemaMajor 1 - embedded HTML report document (AUTHOR-04 CANDIDATE)",
        "description": "Data document embedded in html v1 output of the eight command-inventory:5 html commands. envelope (command-envelope:5) is the only parity source. invocationLedger projects this invocation's invocation:3 record including cancellation. Panels carry typed optional exploration data with explicit states, separated limit layers and provenance distinguishing checked joins from host assertions. featureStates disclose undelivered required features with precise causes and design obligations; they never satisfy delivery. Report codec, envelope5 host admission, ledger and cancellation joins, slot and history policies, owner page law, subject-index recomputation, derived root bounds and the byte law against the remaining document budget are admission rules of contract.md enforced by check.py.",
        "type": "object", "additionalProperties": False,
        "required": ROOT_KEYS,
        "properties": {
            "schemaFamily": {"const": "opensip.product.report-projection"}, "schemaMajor": {"const": 1},
            "command": ref("#/$defs/ReportCommand"),
            "renderer": closed(["format", "version"], {"format": {"const": "html"}, "version": {"const": 1}}),
            "envelope": ref(ENV5), "invocationLedger": ref("#/$defs/InvocationLedgerV1"), "staticParity": ref("#/$defs/StaticParityV1"), "disclosures": ref("#/$defs/DisclosuresV1"),
            "supportedReportViews": {"type": "array", "minItems": 1, "maxItems": 12, "uniqueItems": True, "items": ref("#/$defs/ReportViewId"), "x-opensip-order": "sequence"},
            "featureStates": {"type": "array", "maxItems": 64, "uniqueItems": True, "items": ref("#/$defs/FeatureStateV1"), "x-opensip-order": {"by": ["featureId"]}},
            "budgetProfile": ref("#/$defs/BudgetProfileV1"), "documentProvenance": {"const": PROVENANCE["document"]},
            "reportObservedAt": ref(C + "UtcTimestamp"), "pathDisclosure": ref("#/$defs/PathDisclosureV1"), "panels": ref("#/$defs/PanelsV1"),
        },
        "allOf": [
            {"properties": {"envelope": {"properties": {"kind": {"enum": ["run", "query", "failure"]}}, "not": {"required": ["agentHints"]}}}},
            {"if": {"properties": {"pathDisclosure": {"properties": {"mode": {"const": "relative-only"}}}}}, "then": {"properties": {"envelope": {"not": {"required": ["projectRoot"]}}}}},
            {"if": {"properties": {"envelope": {"properties": {"kind": {"const": "failure"}}}}},
             "then": {"properties": {"panels": {"properties": {p: ref("#/$defs/PanelNotPresentV1") for p in ["evidence", "graph", "comparison", "history", "catalog"]}}}}},
        ] + per_command,
        "$defs": defs,
    }


def build():
    inv5 = inventory5()
    return {
        "owner/command-envelope.v5.schema.json": envelope5(),
        "owner/command-inventory.v5.schema.json": inventory_schema5(),
        "owner/command-inventory.v5.json": inv5,
        "owner/implementation-coverage-successor.v1.json": coverage_overlay(inv5),
        "owner/passage-overrides.v1.json": {"schemaVersion": 1, "overrides": passage_overrides()},
        "owner/design-obligations.v1.json": design_register(),
        "owner/budget-derivations.v1.json": derivations(),
        "owner/builtin-step-planning.v1.json": planning_spec(),
        "owner/query-fixture-correction.v1.json": query_fixture_correction(),
        "report-projection.schema.json": report_schema(),
    }


if __name__ == "__main__":
    OWNER.mkdir(exist_ok=True)
    for name, value in build().items():
        (HERE / name).write_bytes(dump(value))
