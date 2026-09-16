"""Independent RPR3 probes over a byte copy of the frozen subject (work/probe-copy); reviewer-authored, not author evidence.

Rebuilds the checker's admission context exactly as check.py main() steps 0-5 do (without the audit hook, regeneration or the child checker),
then applies reviewer mutations and records the exact admission outcome. Run:
  /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B probe_rpr3.py
"""
import copy
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
COPY = Path(__file__).resolve().parent.parent / "probe-copy"
OUT = Path(__file__).resolve().parent / "probe_rpr3.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


chk = load("chk", COPY / "check.py")  # sets sys.pycache_prefix to a nonexistent directory: no architecture bytecode is read
sys.setrecursionlimit(20000)
from jsonschema import Draft202012Validator
from referencing import Resource
from referencing.jsonschema import DRAFT202012

ctx = chk.Ctx()
cm = chk.load("check_metadata", ARCH / "docs/implementation/m1/metadata-v2/check_metadata.py")
ctx.reference, registry, documents = cm.load(ARCH)
ctx.qsp = chk.load("query_surface_projection", ARCH / "docs/coop/design-corrections/workflows/query_surface_projection.v3.py")
planning = chk.load("check_implementation_planning", ARCH / "docs/operations/check_implementation_planning.py")
ctx.M = M = chk.load("report_model", COPY / "report_model.py")
owner_builder = chk.load("build_owner", COPY / "build_owner.py")
builder = chk.load("build_fixtures", COPY / "build_fixtures.py")
new = {}
for name in ("owner/command-envelope.v5.schema.json", "owner/command-inventory.v5.schema.json", "report-projection.schema.json"):
    doc = ctx.reference.parse((COPY / name).read_bytes())
    Draft202012Validator.check_schema(doc)
    new[doc["$id"]] = doc
    registry = registry.with_resource(doc["$id"], Resource(contents={k: v for k, v in doc.items() if k != "$schema"}, specification=DRAFT202012))
documents = dict(documents, **new)
ctx.registry, ctx.documents, ctx.schema = registry, documents, documents[chk.RID]
ctx.budget = {k: v["const"] for k, v in ctx.schema["$defs"]["BudgetProfileV1"]["properties"].items()}
ctx.inventory5 = json.loads((COPY / "owner/command-inventory.v5.json").read_bytes())
fixture = json.loads((COPY / "fixtures.json").read_bytes())
ctx.material = builder.material()
ctx.owner = M.MockGraphOwner(ctx.material["facts"], ctx.material["template"])
ctx.worst = chk.worst_values(ctx)
C, I = chk.C, chk.I

results = {}


def admit(doc):
    raw = M.canonical(doc)
    try:
        chk.admit_document(ctx, raw)
        return {"outcome": "accept", "bytes": len(raw)}
    except chk.Refused as exc:
        return {"outcome": exc.code, "detail": str(exc)[:160], "bytes": len(raw)}
    except Exception as exc:  # not a typed refusal
        return {"outcome": "UNCAUGHT-" + type(exc).__name__, "detail": str(exc)[:160], "bytes": len(raw)}


def record(pid, claim, expected_if_sound, observed, **extra):
    results[pid] = dict({"claim": claim, "expectedIfSound": expected_if_sound, "observed": observed}, **extra)


def base(name):
    return copy.deepcopy(fixture["bases"][name])


# --- sanity: every positive base admits in this rebuilt context
record("P0-bases", "rebuilt context admits the author positive bases", "accept for each",
       {n: admit(base(n))["outcome"] for n in fixture["bases"]})

# --- G: graph count/cursor joins against the owner completeness law (query-projection-contract.v3.md:140 complete = traversalCoverage complete AND countBasis exact)
doc = base("audit-full")
slots = doc["panels"]["graph"]["data"]["slots"]
slot_summary = [(s["purpose"], len(s["response"]["items"]), s["response"]["context"]["traversalCoverage"], s["response"]["context"]["countBasis"],
                 s["response"]["context"]["totalItems"], "nextCursor" in s["response"]["context"], s["hostProjection"]) for s in slots]
index = max(range(len(slots)), key=lambda i: len(slots[i]["response"]["items"]))
before_items = len(slots[index]["response"]["items"])
record("G0-audit-slot-summary", "audit-full embedded slots (purpose, items, coverage, countBasis, totalItems, cursor, hostProjection)", "informational", slot_summary)


def relabel_complete(slot):
    context = slot["response"]["context"]
    context.update(traversalCoverage="complete", truncated=False)
    context.pop("nextCursor", None)
    slot["hostProjection"] = {"continuation": "complete-page-set", "pageSizeCause": "ladder-first"}


g1 = copy.deepcopy(doc)
s = g1["panels"]["graph"]["data"]["slots"][index]
relabel_complete(s)
s["response"]["context"]["countBasis"] = "lower-bound"
s["response"]["items"] = s["response"]["items"][:1]
g1["panels"]["graph"]["data"]["subjectIndex"] = M.subject_index(g1["panels"]["graph"]["data"]["slots"], g1["panels"]["graph"]["data"]["subjectResolution"])
record("G1-complete-lower-bound-sliced-page", "host slices a complete owner page to 1 row, keeps traversalCoverage complete / continuation complete-page-set, flips countBasis to lower-bound",
       "refused (owner: complete implies exact; items silently cut)", admit(g1), slot=index, ownerItems=before_items, embeddedItems=1,
       totalItemsLeft=s["response"]["context"]["totalItems"])

g2 = copy.deepcopy(doc)
s = g2["panels"]["graph"]["data"]["slots"][index]
s["response"]["context"].update(traversalCoverage="truncated-bound", truncated=True)
s["response"]["context"].pop("nextCursor", None)
s["response"]["items"] = s["response"]["items"][:1]
g2["panels"]["graph"]["data"]["subjectIndex"] = M.subject_index(g2["panels"]["graph"]["data"]["slots"], g2["panels"]["graph"]["data"]["subjectResolution"])
record("G2-truncated-bound-sliced-page", "host slices a complete owner page and relabels it truncated-bound with continuation complete-page-set",
       "refused, or at least not labelled complete-page-set", admit(g2), slot=index, hostContinuation=s["hostProjection"]["continuation"])

g3 = copy.deepcopy(doc)
s = g3["panels"]["graph"]["data"]["slots"][index]
relabel_complete(s)
s["response"]["context"]["countBasis"] = "exact"
s["response"]["items"] = s["response"]["items"][:1]
g3["panels"]["graph"]["data"]["subjectIndex"] = M.subject_index(g3["panels"]["graph"]["data"]["slots"], g3["panels"]["graph"]["data"]["subjectResolution"])
record("G3-control-sliced-exact", "control: same slice with countBasis exact", "J-GRAPH-COUNT", admit(g3))

# --- S: graph slot selection escape through host-asserted descriptor-not-retained
s1 = base("audit-full")
data = s1["panels"]["graph"]["data"]
resolved = [i for i, r in enumerate(data["subjectResolution"]) if r["state"] == "resolved"]
first = resolved[0]
data["subjectResolution"][first] = {"subjectId": data["subjectResolution"][first]["subjectId"], "state": "descriptor-not-retained"}
env = s1["envelope"]
anchor = env["run"]["runId"]
plan = M.plan_slots(data["subjectResolution"], env["projectId"], anchor)
new_slots = []
for i, planned in enumerate(plan):
    request = copy.deepcopy(planned["request"])
    request["page"] = {"size": 100}
    response = ctx.owner.execute(request)
    new_slots.append({"ordinal": i, "purpose": planned["purpose"], "anchorSubjectIds": planned["anchorSubjectIds"], "request": request, "response": response,
                      "hostProjection": {"continuation": "not-embedded" if "nextCursor" in response["context"] else "complete-page-set", "pageSizeCause": "ladder-first"}})
data["slots"] = new_slots
data["slotsProjection"] = {"total": len(plan), "omitted": 0, "omissionCause": "none"}
data["subjectIndex"] = M.subject_index(new_slots, data["subjectResolution"])
record("S1-descriptor-not-retained-reselects-plan", "host marks the first retained subject descriptor-not-retained and re-plans slots from the remaining subjects",
       "accept only as disclosed host assertion; plan identity then depends on an unverifiable host claim", admit(s1),
       originalPlanPurposes=[x["purpose"] for x in fixture["bases"]["audit-full"]["panels"]["graph"]["data"]["slots"]], newPlanPurposes=[p["purpose"] for p in plan])

# --- D: D9 aggregate with a query refusal followed by a renderer failure (root: renderer failure cannot replace query failure)
query_refusal = {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "runId": "run3:" + "1" * 64,
                 "domainDetail": {"code": "QUERY.VIEW_UNKNOWN", "remedy": "select a sealed run"}}
renderer = {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED", "faultCause": "delivery-required", "runId": "run3:" + "1" * 64,
            "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT", "remedy": "re-run", "subject": "run3:" + "1" * 64}}
agg = M.d9_aggregate([{"class": "success", "runId": "run3:" + "1" * 64}, query_refusal, renderer])
record("D1-d9-query-refusal-then-renderer-failure", "reference D9 aggregate over [analysis success, query request-rejected, render operational-failed]",
       "query refusal retained (root decision) or an explicit owned rule stating otherwise", {"aggregateClass": agg["class"], "aggregateDetail": agg.get("domainDetail", {}).get("code")},
       fixtureAggregateCases=[g["id"] for g in fixture["aggregateCases"]])

# --- D2: interrupted step termination (StepTermination admits class interrupted; workflows section 1 cancellation law)
d2 = base("audit-full")
steps = d2["invocationLedger"]["steps"]
target = next(st for st in steps if st.get("recorded") and st["requirement"] == "required")
target["termination"] = {"class": "interrupted", "signal": "SIGINT"}
target["outcome"] = "cancelled"
try:
    ctx.reference.validate({"$ref": C + "StepTermination"}, target["termination"], registry)
    termination_valid = True
except Exception as exc:
    termination_valid = "invalid: " + str(exc)[:120]
record("D2-interrupted-step-in-ledger", "a recorded required step carries an owner-valid interrupted termination", "typed refusal code (never an uncaught exception)", admit(d2),
       terminationOwnerValid=termination_valid)

# --- L: root allowance versus owner-valid ledger termination maxima
wide = "\U0001F600"
consequences = ctx.reference  # placeholder to keep names short
pin_schema = json.loads((ARCH / "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json").read_bytes())["$defs"]["PinnedPurgeDisclosure"]
consequence_const = pin_schema["properties"]["consequences"]["const"]


def pinned_termination(pins):
    return {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "runId": "run3:" + "a" * 64,
            "domainDetail": {"code": "evidence.pinned", "remedy": wide * 1024, "subject": wide * 1024,
                             "purgeDisclosure": {"runId": "run3:" + "a" * 64, "consequences": consequence_const,
                                                 "activePins": sorted([{"pinId": ("%04d" % i) + wide * 252, "kind": "other-authorized"} for i in range(pins)], key=lambda p: p["pinId"].encode())}}}


def owner_ok(value):
    try:
        ctx.reference.validate({"$ref": C + "StepTermination"}, value, registry)
    except Exception as exc:
        return "schema-invalid: " + str(exc).splitlines()[0][:200]
    try:
        ctx.reference.typed(value, 3)
    except Exception as exc:
        return "codec-invalid: " + str(exc)[:120]
    return "valid" if len(M.canonical(value)) <= 4194304 else "over-4MiB"


lo, hi = 1, 4096
while lo < hi:
    mid = (lo + hi + 1) // 2
    if len(M.canonical(pinned_termination(mid))) <= 4194304:
        lo = mid
    else:
        hi = mid - 1
max_termination = pinned_termination(lo)
record("L1-owner-valid-step-termination-maximum", "largest owner-valid StepTermination (evidence.pinned PinnedPurgeDisclosure) within the 4 MiB owner codec",
       "root allowance covers owner-valid ledger maxima or the byte law accounts for root size",
       {"pins": lo, "terminationBytes": len(M.canonical(max_termination)), "ownerValidity": owner_ok(max_termination), "rootAllowanceBytes": ctx.budget["rootAllowanceBytes"],
        "documentMaxBytes": ctx.budget["documentMaxBytes"], "authorWorstRootBytes": owner_builder.worst_root_bytes()})

# L2: try to realise it in an admitted document shape: a required query refusal on the after-commit fit failure base (termination appears in ledger and envelope)
l2 = base("fit-after-commit-query-failure")
env = l2["envelope"]
qstep = next(st for st in l2["invocationLedger"]["steps"] if st["kind"] == "query")
big = pinned_termination(lo // 2)
big["runId"] = env["termination"].get("runId", big["runId"])
big["domainDetail"]["purgeDisclosure"]["runId"] = big["runId"]
qstep["termination"] = copy.deepcopy(big)
env["termination"] = copy.deepcopy(big)
env["errors"] = [copy.deepcopy(big["domainDetail"])]
l2["staticParity"] = builder.static_parity(env, l2["command"]) if hasattr(builder, "static_parity") else l2["staticParity"]
record("L2-large-pinned-termination-in-fit-failure-report", "fit after-commit query failure whose (owner-valid) termination carries a half-maximum pinned disclosure in both envelope and ledger",
       "admits within documentMaxBytes, or a typed boundary", admit(l2), envelopeTerminationBytes=len(M.canonical(big)))

# L3: kind=run analysis report with byte-law-filled panels plus the same pinned termination on a required step
l3 = base("audit-full")
l3_env = l3["envelope"]
record("L3-envelope-kind-run-terminations-admitted", "which termination classes envelope5 admits on kind=run (schema only)",
       "informational", sorted({cls for cls in ["success", "policy-failed", "request-rejected", "indeterminate", "operational-failed", "interrupted"]
                                 if ctx.reference.ExactValidator(documents[chk.ENV5], registry=registry).is_valid(dict(copy.deepcopy(l3_env), exitCode=chk.EXIT[cls], termination=(
                                     {"class": cls, "runId": l3_env["run"]["runId"]} if cls in ("success", "policy-failed") else
                                     {"class": cls, "errorCode": "REQUEST.PRECONDITION_FAILED", "runId": l3_env["run"]["runId"]} if cls == "request-rejected" else
                                     {"class": cls, "reasonCodes": ["VERDICT.INDETERMINATE"], "runId": l3_env["run"]["runId"]} if cls == "indeterminate" else
                                     {"class": cls, "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io", "runId": l3_env["run"]["runId"]} if cls == "operational-failed" else
                                     {"class": cls, "signal": "SIGINT", "runId": l3_env["run"]["runId"]})))}))

# --- H: history determinism
h1 = base("audit-full")
sel = h1["panels"]["history"]["data"]["selection"]
record("H0-audit-history-shape", "audit-full history selection", "informational", {k: sel[k] for k in ("baselineSourceRunId", "priorRunsInSnapshot", "currentCommitSequence")} | {"prior": len(sel["priorRuns"])})
h2 = base("default-run")
sel = h2["panels"]["history"]["data"]["selection"]
if len(sel["priorRuns"]) >= 2:
    dropped = sel["priorRuns"].pop()
    sel["priorRunsInSnapshot"] = len(sel["priorRuns"])
    sel["requestedRunIds"] = [r for r in sel["requestedRunIds"] if r != dropped["runId"]]
    h2["panels"]["history"]["data"]["runs"] = [r for r in h2["panels"]["history"]["data"]["runs"] if r["runId"] != dropped["runId"]]
    record("H1-snapshot-count-understated", "host understates priorRunsInSnapshot and drops the oldest selected prior Run", "accept only as host assertion (count is not document-provable)", admit(h2))

# --- I: integer limits at the u64 commit sequence
i1 = base("audit-full")
i1["panels"]["history"]["data"]["selection"]["currentCommitSequence"] = 2 ** 64 - 1
record("I1-commit-sequence-u64-max", "currentCommitSequence 2^64-1 (schema maximum)", "accept", admit(i1))
raw = M.canonical(base("audit-full")).replace(b'"currentCommitSequence":', b'"currentCommitSequence":1', 0)
i2 = base("audit-full")
i2["panels"]["history"]["data"]["selection"]["currentCommitSequence"] = 2 ** 64
record("I2-commit-sequence-over-u64", "currentCommitSequence 2^64", "typed refusal", admit(i2))

# --- X: independent subject3 (stdlib only, from the documented frame) and static parity (from inventory5 pointers)
def subject3(endpoint):
    body = json.dumps(dict({"schemaVersion": 3}, **endpoint), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "subject3:" + hashlib.sha256(b"opensip.product.v1\x00evaluation-subject\x00" + len(body).to_bytes(8, "big") + body).hexdigest()


mismatch, rows = [], 0
for name, doc in fixture["bases"].items():
    graph = doc["panels"].get("graph", {})
    if graph.get("state") != "present":
        continue
    for row in graph["data"]["subjectIndex"]:
        rows += 1
        if subject3(row["endpoint"]) != row["subjectId"]:
            mismatch.append((name, row["subjectId"]))
record("X1-subject3-independent", "stdlib subject3 over every subjectIndex row of every base", "0 mismatches", {"rows": rows, "mismatches": mismatch})

static = {}
for name, golden in fixture["staticParityGoldens"].items():
    doc = fixture["bases"][name]
    row = next(c for c in ctx.inventory5["commands"] if c["name"] == doc["command"])
    dispatch = row.get("queryDispatch") or row.get("advisoryDispatch")
    lines = []
    if dispatch and doc["envelope"]["kind"] in ("query", "run"):
        for field in row["parityFields"]:
            value = doc["envelope"]
            for token in dispatch["parityPaths"][field].strip("/").split("/"):
                value = value[int(token)] if isinstance(value, list) else value[token]
            lines.append(field + ": " + json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    lines.append("envelope: " + json.dumps(doc["envelope"], ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    text = "".join(l + "\n" for l in lines).encode()
    static[name] = hashlib.sha256(text).hexdigest() == golden["textSha256"] and len(text) == golden["textBytes"] == doc["staticParity"]["textBytes"]
record("X2-static-parity-independent", "independent labelled-canonical-lines recomputation against staticParityGoldens and base staticParity", "all true", static)

fit_lines = [l.split(":")[0] for l in "".join(
    f + ": x\n" for f in next(c for c in ctx.inventory5["commands"] if c["name"] == "fit")["parityFields"]).splitlines()]
record("X3-fit-static-section-fields", "fit static section lines include the four disclosure fields", "includes candidates-truncated/total-items/next-cursor/availability", fit_lines)

# --- C: owned coverage validator masking (check.py compares only the first raised message)
overlay = json.loads((COPY / "owner/implementation-coverage-successor.v1.json").read_bytes())
cov_base = json.loads((ARCH / overlay["base"]["path"]).read_bytes())
applied = copy.deepcopy(cov_base)
for change in overlay["rowChanges"]:
    row = applied["groups"][change["group"]][change["index"]]
    row["source"] = change["source"]
    if "owners" in change:
        row["owners"] = change["owners"]
    row["verification"]["method"] = change.get("verificationMethod", row["verification"]["method"])
for addition in overlay["rowAdditions"]:
    applied["groups"][addition["group"]].append(addition["row"])
sources = {}
for key, pin in cov_base["sources"].items():
    raw_src = (ARCH / pin["path"]).read_bytes()
    sources[key] = json.loads(raw_src) if pin["path"].endswith(".json") else raw_src.decode()
sources_next = dict(sources, commands=ctx.inventory5, **{"workflows-and-surfaces": owner_builder.overridden_text(cov_base["sources"]["workflows-and-surfaces"]["path"])})
inventory_doc = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v3.json").read_bytes())
delivery_groups = ("commands", "queryOperations", "renderers", "capabilityCells", "workflowGoldens")
masked = {}
for label, data_, srcs in (("base", cov_base, sources), ("overlay", applied, sources_next)):
    trial = copy.deepcopy(data_)
    owners = {o for g in delivery_groups for r in trial["groups"][g] for o in r["owners"]}
    first = dict(trial["moduleFirstMilestone"])
    trial["moduleFirstMilestone"] = {o: first.get(o, "M0") for o in owners}
    messages = []
    for _ in range(40):
        try:
            planning.validate_coverage(trial, srcs, inventory_doc)
            messages.append("valid")
            break
        except ValueError as exc:
            msg = str(exc)
            messages.append(msg)
            break
    masked[label] = {"moduleFirstMilestoneKeysAdded": sorted(set(owners) - set(first))[:10], "moduleFirstMilestoneKeysRemoved": sorted(set(first) - set(owners))[:10],
                     "nextValidatorResult": messages[-1]}
record("C1-coverage-validator-beyond-first-failure", "owned validate_coverage re-run after neutralising only the pre-existing module-milestone key-set condition",
       "overlay reaches the same result as base (no new masked violation)", masked)

OUT.write_text(json.dumps(results, indent=1, ensure_ascii=False) + "\n")
print(json.dumps({k: v["observed"] if k not in ("X2-static-parity-independent",) else v["observed"] for k, v in results.items()}, indent=1, ensure_ascii=False)[:12000])
