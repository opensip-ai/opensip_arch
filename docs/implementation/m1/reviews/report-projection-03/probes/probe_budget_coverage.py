"""RPR3 follow-up probes reusing probe_rpr3.py's rebuilt admission context (reviewer-authored).
B1: mandatory root metadata (ledger) of an owner-valid, join-consistent failure report versus documentMaxBytes.
C2: which overlay commands row drifts under the owned validator; report-feature rows for the F obligations."""
import copy, json, runpy
from pathlib import Path
g = runpy.run_path(str(Path(__file__).with_name("probe_rpr3.py")))
ctx, M, chk, builder, base, admit, pinned_termination = g["ctx"], g["M"], g["chk"], g["builder"], g["base"], g["admit"], g["pinned_termination"]
out = {}

audit = base("audit-full")
fitfail = base("fit-after-commit-query-failure")
steps = audit["invocationLedger"]["steps"]
recorded = [s for s in steps if s["recorded"]]
run_id = next(s["analysisRunId"] for s in steps if s.get("analysisRunId"))

def build(pins, big_steps):
    doc = copy.deepcopy(audit)
    env = copy.deepcopy(fitfail["envelope"])
    env["requestId"] = doc["envelope"]["requestId"]
    env["projectId"] = doc["envelope"]["projectId"]
    T = pinned_termination(pins)
    T["runId"] = run_id
    T["domainDetail"]["purgeDisclosure"]["runId"] = run_id
    env["termination"] = copy.deepcopy(T)
    env["errors"] = [copy.deepcopy(T["domainDetail"])]
    env["exitCode"] = chk.EXIT["request-rejected"]
    for i, step in enumerate(s for s in doc["invocationLedger"]["steps"] if s["recorded"]):
        step["termination"] = copy.deepcopy(T) if i < big_steps else {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"}
    doc["envelope"] = env
    doc["panels"] = {k: {"state": "unavailable", "reason": "no-admitted-result"} for k in doc["panels"]}
    doc["staticParity"] = builder.static_parity(env, doc["command"])
    return doc, T

lo, hi = 1, 4096
while lo < hi:
    mid = (lo + hi + 1) // 2
    doc, T = build(mid, 1)
    if len(M.canonical(doc["envelope"])) <= ctx.budget["envelopeMaxCanonicalBytes"]:
        lo = mid
    else:
        hi = mid - 1
control, T = build(lo, 1)
three, _ = build(lo, len(recorded))
out["B1-ledger-mandatory-metadata-vs-document-cap"] = {
    "claim": "audit failure report: every recorded required step rejected with an owner-valid evidence.pinned termination; envelope at its 4 MiB boundary; panels all no-admitted-result",
    "expectedIfSound": "admits (mandatory envelope + ledger bounded by documentMaxBytes), or the byte law/allowance is derived from these maxima",
    "pinsPerTermination": lo, "terminationBytes": len(M.canonical(T)), "envelopeBytes": len(M.canonical(control["envelope"])),
    "recordedRequiredSteps": len(recorded),
    "controlOneLargeStep": admit(control),
    "allRecordedStepsLarge": dict(admit(three), ledgerBytes=len(M.canonical(three["invocationLedger"])), panelsBytes=len(M.canonical(three["panels"]))),
    "rootAllowanceBytes": ctx.budget["rootAllowanceBytes"], "documentMaxBytes": ctx.budget["documentMaxBytes"],
}

planning, applied, sources_next = g["planning"], g["applied"], g["sources_next"]
expected = planning.expected_groups(sources_next)
drift = []
for row in applied["groups"]["commands"]:
    _, _, value = expected["commands"][row["id"]]
    fields = [f for f in ("requestClass", "authorizationClass", "formats", "parityFields") if row[f] != value[f]]
    if fields:
        drift.append({"id": row["id"], "fields": fields, "overlayRow": {f: row[f] for f in fields}, "inventory5": {f: value[f] for f in fields}})
out["C2-overlay-command-row-drift"] = drift
overlay = json.loads((Path(__file__).resolve().parent.parent / "probe-copy/owner/implementation-coverage-successor.v1.json").read_bytes())
feature_rows = {}
for grp, rows in applied["groups"].items():
    for row in rows:
        if any(t in json.dumps(row) for t in ("R03", "R05", "R06", "R07", "R08", "R12", "R14", "R23")) and grp not in ("commands",):
            feature_rows.setdefault(grp, []).append({k: row.get(k) for k in ("id", "milestone", "owners", "verification", "reviewIssues")})
out["C3-report-feature-rows"] = {k: v[:12] for k, v in feature_rows.items()}
out["C3-overlay-change-ids"] = [(c["group"], c["id"]) for c in overlay["rowChanges"]] + [("add", a["group"], a["row"]["id"]) for a in overlay["rowAdditions"]]
Path(__file__).with_name("probe_budget_coverage.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
print(json.dumps(out, indent=1, ensure_ascii=False)[:9000])
