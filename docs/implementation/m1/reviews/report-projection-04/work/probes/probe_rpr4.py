"""Reviewer admission probes for author-04 (review-04). Rebuilds check.py main() context steps 0-1 (no hook/regeneration) from the probe copy,
then applies reviewer mutations and records exact outcomes. Results: probe_rpr4.json (written by the shell via stdout capture)."""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
W = Path("/tmp/opensip-implementation/m1-report-projection-review-04/work")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
COPY = W / "probe-copy"
def load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
chk = load("chk", COPY / "check.py")
sys.setrecursionlimit(20000)
from jsonschema import Draft202012Validator
from referencing import Resource
from referencing.jsonschema import DRAFT202012
ctx = chk.Ctx()
cm = chk.load("check_metadata", ARCH / "docs/implementation/m1/metadata-v2/check_metadata.py")
ctx.reference, registry, documents = cm.load(ARCH)
ctx.qsp = chk.load("query_surface_projection", ARCH / "docs/coop/design-corrections/workflows/query_surface_projection.v3.py")
ctx.M = M = chk.load("report_model", COPY / "report_model.py")
owner = chk.load("build_owner", COPY / "build_owner.py")
builder = chk.load("build_fixtures", COPY / "build_fixtures.py")
ctx.builder = builder
for name in ("owner/command-envelope.v5.schema.json", "owner/command-inventory.v5.schema.json", "report-projection.schema.json"):
    d = ctx.reference.parse((COPY / name).read_bytes())
    documents[d["$id"]] = d
    registry = registry.with_resource(d["$id"], Resource(contents={k: v for k, v in d.items() if k != "$schema"}, specification=DRAFT202012))
ctx.registry, ctx.documents, ctx.schema = registry, documents, documents[chk.RID]
ctx.budget = {k: v["const"] for k, v in ctx.schema["$defs"]["BudgetProfileV1"]["properties"].items()}
ctx.derivations = json.loads((COPY / "owner/budget-derivations.v1.json").read_bytes())
ctx.inventory5 = json.loads((COPY / "owner/command-inventory.v5.json").read_bytes())
fixture = json.loads((COPY / "fixtures.json").read_bytes())
try:
    ctx.material = builder.material()
    ctx.owner = M.MockGraphOwner(ctx.material["facts"], ctx.material["template"])
except Exception as exc:
    print("material setup failed", exc, file=sys.stderr)
R = {}
def admit(doc):
    raw = M.canonical(doc)
    try:
        chk.admit_document(ctx, raw); return {"outcome": "accept", "bytes": len(raw)}
    except chk.Refused as exc:
        return {"outcome": exc.code, "detail": str(exc)[:200], "bytes": len(raw)}
    except Exception as exc:
        return {"outcome": "UNCAUGHT-" + type(exc).__name__, "detail": str(exc)[:200], "bytes": len(raw)}
def refresh(doc):
    out = builder.refresh(doc)
    return out if out is not None else doc
def base(n):
    return copy.deepcopy(fixture["bases"][n])
def rec(pid, claim, expected, observed, **extra):
    R[pid] = dict({"claim": claim, "expectedIfSound": expected, "observed": observed}, **extra)

rec("P0-bases", "all author bases admit in rebuilt context", "accept", {n: admit(base(n))["outcome"] for n in fixture["bases"]})
bounds = ctx.budget["graphPublicBounds"]
R["P0-graphPublicBounds"] = bounds

def graph_mutation(fn):
    d = base("audit-full")
    data = d["panels"]["graph"]["data"]
    slot = data["slots"][0]
    fn(slot)
    slot["hostProjection"] = {"continuation": M.continuation_for(slot["response"]["context"]), "pageSizeCause": slot["hostProjection"]["pageSizeCause"]}
    data["subjectIndex"] = M.subject_index(data["slots"], data["subjectResolution"])
    return refresh(d)

def g4(slot):  # truncated-bound, lower-bound via produced cap, no cursor, totalItems=items=1 (99,999 produced rows neither embedded nor continuable)
    c = slot["response"]["context"]; c.pop("nextCursor", None)
    slot["response"]["items"] = slot["response"]["items"][:1]
    c.update(traversalCoverage="truncated-bound", truncated=True, countBasis="lower-bound", producedItems=bounds["maxItemsPerOperation"], totalItems=1)
rec("G4-truncated-bound-produced-cap-total-understated-sliced", "slot0 cut to 1 row; context truncated-bound/lower-bound; producedItems at public cap; totalItems forged to 1; no cursor",
    "refused: owner lower-bound totalItems is the produced prefix (query-projection-contract.v3.md:136,146); rows produced but neither embedded nor continuable", admit(graph_mutation(g4)))

def g5(slot):  # same, capped via visitedNodes; producedItems 50 > embedded 1 and totalItems 1
    c = slot["response"]["context"]; c.pop("nextCursor", None)
    slot["response"]["items"] = slot["response"]["items"][:1]
    c.update(traversalCoverage="truncated-bound", truncated=True, countBasis="lower-bound", visitedNodes=bounds["maxVisitedNodes"], producedItems=50, totalItems=1)
rec("G5-truncated-bound-visited-cap-produced-exceeds-total", "slot0 cut to 1 row; visited cap reached; producedItems 50, totalItems 1, no cursor",
    "refused: producedItems > totalItems contradicts a lower-bound produced-prefix count and 49 produced rows vanish", admit(graph_mutation(g5)))

def g6(slot):  # complete exact with producedItems > totalItems
    c = slot["response"]["context"]; c.pop("nextCursor", None)
    slot["response"]["items"] = slot["response"]["items"][:1]
    c.update(traversalCoverage="complete", truncated=False, countBasis="exact", producedItems=1000, totalItems=1)
rec("G6-complete-exact-produced-exceeds-total", "slot0 cut to 1 row labelled complete/exact/total 1 but producedItems 1000",
    "refused: a complete exact answer produced exactly totalItems units", admit(graph_mutation(g6)))

def g7(slot):  # control: exact complete sliced
    c = slot["response"]["context"]; c.pop("nextCursor", None)
    slot["response"]["items"] = slot["response"]["items"][:1]
    c.update(traversalCoverage="complete", truncated=False, countBasis="exact", producedItems=1, totalItems=107)
rec("G7-control-complete-total-mismatch", "control: complete/exact with totalItems 107 but 1 row", "J-GRAPH-COUNT", admit(graph_mutation(g7)))

def g8(slot):  # positive: capped lower-bound truncated-bound continued full page with valid cursor
    c = slot["response"]["context"]
    c.update(traversalCoverage="truncated-bound", truncated=True, countBasis="lower-bound", producedItems=bounds["maxItemsPerOperation"], totalItems=bounds["maxItemsPerOperation"])
    c["nextCursor"] = M.graph_cursor(slot["request"], len(slot["response"]["items"]))
rec("G8-positive-capped-truncated-bound-full-page-cursor", "slot0 100 rows, truncated-bound lower-bound at produced cap with valid cursor", "accept", admit(graph_mutation(g8)))

# --- cancellation inside a delivered document
for pid, canc in (("K1-after-settle-claimed-in-document", {"requested": True, "signal": "SIGTERM", "phase": "after-settle"}),
                  ("K2-before-settle-in-document", {"requested": True, "signal": "SIGINT", "phase": "before-settle"})):
    d = base("audit-full")
    d["invocationLedger"]["cancellation"] = canc
    if canc["phase"] == "before-settle":
        rid = d["envelope"]["run"]["runId"]
        d["envelope"]["termination"] = {"class": "interrupted", "signal": "SIGINT", "runId": rid}
        d["envelope"]["exitCode"] = 130
    rec(pid, "delivered report document carrying cancellation %s" % canc["phase"], "J-LEDGER-CANCELLATION (report is projected inside the in-progress required render)", admit(refresh(d)))

# --- maximal document: boundary envelope + reviewer 6-byte maximal pinned terminations + panels filled to the effective budget
common = documents["urn:opensip:product-v1:workflows:evaluator3:common:3"]["$defs"]
pin_def = common["PinnedPurgeDisclosure"]
CTRL = [chr(c) for c in range(1, 32)]
def ctrl(n, index=None):
    head = ""
    if index is not None:
        ds = []
        for _ in range(3):
            ds.append(CTRL[index % 31]); index //= 31
        head = "".join(reversed(ds))
    return head + CTRL[0] * (n - len(head))
def pinned_term(n, run_id):
    pins = sorted([{"pinId": ctrl(256, i), "kind": "repair-prerequisite"} for i in range(n)], key=lambda p: p["pinId"].encode())
    return {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "authority": "authoritative", "runId": run_id, "executionId": "exec1_" + "f" * 32,
            "coverageId": "coverage2:" + "f" * 64, "domainDetail": {"code": "evidence.pinned", "remedy": ctrl(1024), "subject": ctrl(1024),
            "purgeDisclosure": {"runId": run_id, "activePins": pins, "consequences": pin_def["properties"]["consequences"]["const"]}}}
d = base("audit-full")
env = d["envelope"]
rid = env["run"]["runId"]
recorded = [s for s in d["invocationLedger"]["steps"] if s["recorded"]]
lo, hi = 1, 4096
while lo < hi:
    mid = (lo + hi + 1) // 2
    trial = dict(copy.deepcopy(env), termination=pinned_term(mid, rid), exitCode=2)
    if len(M.canonical(trial)) <= ctx.budget["envelopeMaxCanonicalBytes"]:
        lo = mid
    else:
        hi = mid - 1
T0 = pinned_term(lo, rid)
TMAX = pinned_term(4096, rid)
env["termination"] = copy.deepcopy(T0); env["exitCode"] = 2
recorded[0]["termination"] = copy.deepcopy(T0)
for s in recorded[1:]:
    s["termination"] = copy.deepcopy(TMAX)
entries = d["panels"]["evidence"]["data"]["entries"]
seed = copy.deepcopy(entries[0])
def with_entries(doc, n):
    rows = []
    for i in range(n):
        r = copy.deepcopy(seed); r["key"]["subjectScopeCommitment"] = "sha256:" + hashlib.sha256(b"rv04-%d" % i).hexdigest(); rows.append(r)
    doc["panels"]["evidence"]["data"]["entries"] = rows
    doc["panels"]["evidence"]["data"]["entriesProjection"] = {"total": n, "omitted": 0, "omissionCause": "none"}
    return doc
budget_bytes = M.effective_exploration_budget(ctx.budget, env, d["invocationLedger"], ctx.schema["required"])
overhead = 2 + sum(len(M.canonical(k)) + 1 for k in ctx.schema["required"]) + (len(ctx.schema["required"]) - 1)
indep_remaining = ctx.budget["documentMaxBytes"] - overhead - len(M.canonical(env)) - len(M.canonical(d["invocationLedger"])) - ctx.budget["rootMemberMaxBytes"]
lo2, hi2 = 1, ctx.budget["maxEvidenceEntries"]
while lo2 < hi2:
    mid = (lo2 + hi2 + 1) // 2
    if len(M.canonical(with_entries(d, mid)["panels"])) <= budget_bytes:
        lo2 = mid
    else:
        hi2 = mid - 1
full = refresh(with_entries(copy.deepcopy(d), lo2))
over = refresh(with_entries(copy.deepcopy(d), lo2 + 1)) if lo2 < ctx.budget["maxEvidenceEntries"] else None
rec("B2-maximal-kind-run-audit-document", "kind=run audit: envelope at 4 MiB boundary (step0 pinned termination), steps 1-2 reviewer 6-byte 4096-pin terminations, evidence filled to the effective budget",
    "accept within documentMaxBytes 27,827,964; J-LEDGER-BOUND holds", admit(full),
    envelopeBytes=len(M.canonical(full["envelope"])), ledgerBytes=len(M.canonical(full["invocationLedger"])), auditLedgerBound=ctx.derivations["perCommand"]["audit"]["ledgerMaxBytes"],
    panelsBytes=len(M.canonical(full["panels"])), effectiveBudget=budget_bytes, independentRemainingBeforeMin=indep_remaining, evidenceEntries=lo2,
    rootMemberMaxBytes=ctx.budget["rootMemberMaxBytes"], documentMaxBytes=ctx.budget["documentMaxBytes"])
if over is not None:
    rec("B2b-one-entry-over-effective-budget", "same with one more evidence entry", "J-BUDGET-BYTES", admit(over))

# --- disclosures / static section wording
d = base("audit-full")
row = next(c for c in ctx.inventory5["commands"] if c["name"] == "audit")
text = M.static_parity_text(d["envelope"], row, d["disclosures"])
R["X1-static-section-disclosure-lines"] = [l for l in text.splitlines() if l.startswith("disclosure")]
R["X1-document-provenance"] = d["documentProvenance"]
R["X1-graph-provenance"] = d["panels"]["graph"]["data"]["provenance"]
sys.stdout.write(json.dumps(R, indent=1, ensure_ascii=False) + "\n")
