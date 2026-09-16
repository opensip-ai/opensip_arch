"""Deterministic report-projection reference model (author-04). Design/reference only; no product authority.

Pure functions shared by the owner builder, fixture builder and checker:
- subject3 minting from the composition-contract frame and governed per-operation GraphEndpoint pointers;
- the query projection table rows used by the slot plan;
- the finding-subject slot plan and the history selection policy;
- a mock graph owner answering every (re-)issued first-page request over complete fact rows with owner ordering, the produced-item
  and page laws (query-projection-contract.v3 section 5: complete = traversalCoverage complete AND countBasis exact; a produced prefix
  with owed work is countBasis lower-bound), reference cursors, and optional reference test bounds;
- the fit first-page cursor, the owned D9 step aggregate with the invocation cancellation law, per-renderer outcome goldens,
  ledger missing-child disclosure, the static parity text and the byte law against an effective budget.
"""
import copy
import hashlib
import json
from collections import deque

LADDER = [100, 50, 25, 12, 6, 3, 1]
MAX_SLOTS = 6
MAX_PLANNED_SUBJECTS = 64
EXPLORATION_CAP = 4194304
PROJECTION_PRIORITY = ["comparison", "catalog", "evidence", "graph", "history"]
PLACEHOLDER_DELTA = 999999999
TABLE = {
    ("calls", "resolved-callee"): {"source": {"symbol"}, "target": {"symbol"}},
    ("references", "resolved-binding"): {"source": {"symbol"}, "target": {"symbol"}},
    ("imports", "resolved-target"): {"source": {"symbol"}, "target": {"file", "symbol", "package"}},
    ("control-flow", "syntactic"): {"source": {"symbol"}, "target": {"symbol"}},
    ("reachability", "from-resolved-calls"): {"source": {"symbol"}, "target": {"symbol"}},
}
SEVERITY_RANK = {"error": 0, "warning": 1, "note": 2}
D9_ORDER = ["operational-failed", "request-rejected", "policy-failed", "indeterminate", "success"]
STATIC_FORMAT = "labelled-canonical-lines.2"


class ModelRefusal(Exception):
    def __init__(self, code, text=""):
        super().__init__(code + (": " + text if text else ""))
        self.code = code


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def subject_id(endpoint):
    """subject3 = prefix:hex(SHA256("opensip.product.v1"||00||"evaluation-subject"||00||u64be(len C(X))||C(X)))."""
    raw = canonical(dict({"schemaVersion": 3}, **endpoint))
    return "subject3:" + sha(b"opensip.product.v1\x00evaluation-subject\x00" + len(raw).to_bytes(8, "big") + raw)


def endpoint_tuple(endpoint):
    return tuple(x.encode() for x in (endpoint["universe"], endpoint["kind"], endpoint["nativeSubjectId"], endpoint.get("packageManifestPath", "")))


ENDPOINT_POINTERS = {
    "graph.neighbors": ["request/params/endpoint", "response/items/*/source", "response/items/*/target"],
    "graph.path": ["request/params/start", "request/params/target", "response/items/*/start", "response/items/*/target",
                   "response/items/*/nodes/*", "response/items/*/edges/*/source", "response/items/*/edges/*/target"],
    "graph.reach": ["request/params/start", "response/items/*/endpoint"],
}


def slot_endpoints(slot):
    out = []
    def walk(value, tokens):
        if not tokens:
            out.append(value)
            return
        head, rest = tokens[0], tokens[1:]
        if head == "*":
            for child in value:
                walk(child, rest)
        elif isinstance(value, dict) and head in value:
            walk(value[head], rest)
    for pointer in ENDPOINT_POINTERS[slot["request"]["operation"]]:
        walk(slot, pointer.split("/"))
    return out


def subject_index(slots, resolution):
    rows = {}
    for row in resolution:
        if row["state"] == "resolved":
            rows[canonical(row["endpoint"])] = {"subjectId": subject_id(row["endpoint"]), "endpoint": copy.deepcopy(row["endpoint"])}
    for slot in slots:
        for endpoint in slot_endpoints(slot):
            rows[canonical(endpoint)] = {"subjectId": subject_id(endpoint), "endpoint": copy.deepcopy(endpoint)}
    return sorted(rows.values(), key=lambda r: r["subjectId"].encode())


def page_law(context, item_count, size, bounds):
    """Owner page/count law for one first page (query-projection-contract.v3 sections 5-6). bounds: effective maxItemsPerOperation/maxVisitedNodes.
    Returns None when lawful, else the violated clause. Owed work (countBasis lower-bound) only arises when a produced or visited cap was reached."""
    coverage, basis, cursor = context["traversalCoverage"], context["countBasis"], context.get("nextCursor")
    total, produced, visited = context["totalItems"], context["producedItems"], context["visitedNodes"]
    capped = produced == bounds["maxItemsPerOperation"] or visited == bounds["maxVisitedNodes"]
    if context["truncated"] != (coverage == "truncated-bound"):
        return "truncated iff truncated-bound"
    if produced > bounds["maxItemsPerOperation"] or visited > bounds["maxVisitedNodes"]:
        return "counts exceed effective caps"
    if item_count > size or item_count > total or item_count > produced:
        return "embedded rows exceed page size or counts"
    if coverage == "complete":
        if basis != "exact" or cursor is not None or total != item_count:
            return "complete requires countBasis exact, no cursor and totalItems equal to the embedded rows"
    if basis == "lower-bound" and not capped:
        return "lower-bound without a reached produced/visited cap"
    if basis == "exact" and coverage == "truncated-bound":
        return "truncated-bound owes work: countBasis must be lower-bound"
    if coverage == "truncated-page":
        if cursor is None or item_count != size or total <= item_count:
            return "truncated-page requires a cursor, a full page and more counted rows"
    if coverage == "truncated-bound":
        if cursor is None and total != item_count:
            return "last page without cursor must embed every produced row"
        if cursor is not None and item_count != size:
            return "continued truncated-bound page must be full"
    return None


def continuation_for(context):
    """Host continuation derived only from the owner answer: a page set is complete only for an exact complete answer."""
    if "nextCursor" in context:
        return "not-embedded"
    if context["traversalCoverage"] == "complete" and context["countBasis"] == "exact":
        return "complete-page-set"
    return "operation-truncated-no-continuation"


# ---------------------------------------------------------------------------
# slot plan (finding-subject-slot-plan.1)

def policy_subjects(envelope, command):
    ordered = []
    if envelope["kind"] == "run":
        findings = sorted(envelope.get("findings", []), key=lambda f: (SEVERITY_RANK[f["severity"]], f["findingId"].encode()))
        ordered = [f["subjectId"] for f in findings]
    elif envelope["kind"] == "query" and command == "candidates":
        for candidate in envelope["queryRecord"]["candidates"]:
            ordered += [o["subjectId"] for o in candidate.get("occurrences", [])]
    seen, out = set(), []
    for sid in ordered:
        if sid not in seen:
            seen.add(sid)
            out.append(sid)
    return out[:MAX_PLANNED_SUBJECTS]


def plan_slots(resolution, project_id, run_id):
    resolved = [r["endpoint"] for r in resolution if r["state"] == "resolved"]
    symbols = [e for e in resolved if e["kind"] == "symbol"]
    packages = [e for e in resolved if e["kind"] == "package"]
    files = [e for e in resolved if e["kind"] == "file"]
    base = {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": project_id, "view": {"runId": run_id}, "completeness": "best-effort"}
    plan = []
    def add(purpose, anchors, operation, params):
        plan.append({"purpose": purpose, "anchorSubjectIds": [subject_id(a) for a in anchors], "request": dict(copy.deepcopy(base), operation=operation, params=copy.deepcopy(params))})
    for endpoint in symbols[:2]:
        add("neighborhood", [endpoint], "graph.neighbors", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": endpoint})
    if packages:
        add("package-coupling", [packages[0]], "graph.neighbors", {"relation": "imports", "minResolution": "resolved-target", "direction": "incoming", "endpoint": packages[0]})
    if files:
        add("neighborhood", [files[0]], "graph.neighbors", {"relation": "imports", "minResolution": "resolved-target", "direction": "incoming", "endpoint": files[0]})
    if symbols:
        add("reach", [symbols[0]], "graph.reach", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": symbols[0], "maxDepth": 2, "includeStart": False})
        partner = next((e for e in symbols[1:] if e["universe"] == symbols[0]["universe"]), None)
        if partner is not None:
            add("path", [symbols[0], partner], "graph.path", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": symbols[0], "target": partner, "maxDepth": 8})
    assert len(plan) <= MAX_SLOTS
    return plan


def graph_cursor(request, position):
    params = copy.deepcopy(request["params"])
    if request["operation"] == "graph.reach":
        params.setdefault("includeStart", False)
    order = {"graph.neighbors": "neighbor-tuple", "graph.reach": "endpoint-tuple", "graph.path": "fact2-sequence"}[request["operation"]]
    binding = {"projectId": request["projectId"], "runId": request["view"]["runId"], "operation": request["operation"], "params": params, "order": order}
    return "q3." + request["view"]["runId"][5:] + "." + sha(canonical(binding)) + "." + str(position)


def fit_cursor(project_id, run_id, position=100):
    binding = {"projectId": project_id, "runId": run_id, "operation": "candidate.list", "params": {"includeSuppressed": False}, "order": "candidateId"}
    return "q3." + run_id[5:] + "." + sha(canonical(binding)) + "." + str(position)


class MockGraphOwner:
    """First-page answers over complete fact rows. test_bounds may only lower maxItemsPerOperation (query contract section 5 reference controls)."""

    def __init__(self, facts, context_template, max_items_per_operation=100000):
        self.facts = sorted(facts, key=lambda f: f["factId"].encode())
        self.template = context_template
        self.max_items = max_items_per_operation
        self.calls = []

    def _hops(self, rows, vertex, direction):
        key = canonical(vertex)
        out = []
        for f in rows:
            if direction in ("outgoing", "both") and canonical(f["source"]) == key:
                out.append((f["factId"], f["target"]))
            if direction in ("incoming", "both") and canonical(f["target"]) == key:
                out.append((f["factId"], f["source"]))
        return sorted(out, key=lambda hop: hop[0].encode())

    def execute(self, request):
        assert "cursor" not in request["page"], "first pages only"
        self.calls.append(copy.deepcopy(request))
        op, params, size = request["operation"], request["params"], request["page"]["size"]
        rows = [f for f in self.facts if f["relation"] == params["relation"] and f["resolution"] == params["minResolution"]]
        visited = 1
        if op == "graph.neighbors":
            key, direction = canonical(params["endpoint"]), params["direction"]
            selected = [f for f in rows if (direction in ("outgoing", "both") and canonical(f["source"]) == key) or (direction in ("incoming", "both") and canonical(f["target"]) == key)]
            units = [{"factId": f["factId"], "relation": f["relation"], "resolution": f["resolution"], "source": f["source"], "target": f["target"]} for f in selected]
            units.sort(key=lambda r: (endpoint_tuple(r["source"]), endpoint_tuple(r["target"]), r["factId"].encode()))
        elif op == "graph.reach":
            start, depth_cap = params["start"], params["maxDepth"]
            seen = {canonical(start): (0, None)}
            queue = deque([start])
            while queue:
                vertex = queue.popleft()
                depth = seen[canonical(vertex)][0]
                if depth >= depth_cap:
                    continue
                for fact_id, nxt in self._hops(rows, vertex, params["direction"]):
                    if canonical(nxt) not in seen:
                        seen[canonical(nxt)] = (depth + 1, fact_id)
                        queue.append(nxt)
            visited = len(seen)
            units = []
            for raw, (depth, via) in seen.items():
                if depth == 0 and not params.get("includeStart", False):
                    continue
                row = {"endpoint": json.loads(raw), "depth": depth}
                if via is not None:
                    row["viaFactId"] = via
                units.append(row)
            units.sort(key=lambda r: endpoint_tuple(r["endpoint"]))
        else:
            start, target, depth_cap = params["start"], params["target"], params["maxDepth"]
            parent = {canonical(start): None}
            queue = deque([(start, 0)])
            found = canonical(start) == canonical(target)
            while queue and not found:
                vertex, depth = queue.popleft()
                if depth >= depth_cap:
                    continue
                for fact_id, nxt in self._hops(rows, vertex, params["direction"]):
                    if canonical(nxt) not in parent:
                        parent[canonical(nxt)] = (canonical(vertex), fact_id)
                        if canonical(nxt) == canonical(target):
                            found = True
                            break
                        queue.append((nxt, depth + 1))
            visited = len(parent)
            units = []
            if found:
                nodes, edges, cursor = [target], [], canonical(target)
                while parent[cursor] is not None:
                    prev, fact_id = parent[cursor]
                    edges.append({"factId": fact_id, "source": json.loads(prev), "target": json.loads(cursor)})
                    nodes.append(json.loads(prev))
                    cursor = prev
                nodes.reverse()
                edges.reverse()
                units = [{"hopCount": len(edges), "start": start, "target": target, "nodes": nodes, "edges": edges}]
        produced = units[:self.max_items]
        owed = len(units) > len(produced)
        page = produced[:size]
        more_pages = len(produced) > len(page)
        context = copy.deepcopy(self.template)
        if more_pages:
            coverage = "truncated-page"
        elif owed:
            coverage = "truncated-bound"
        else:
            coverage = "complete"
        context.update(projectId=request["projectId"], resolvedView={"runId": request["view"]["runId"]}, totalItems=len(produced),
                       countBasis="lower-bound" if owed else "exact", traversalCoverage=coverage, truncated=coverage == "truncated-bound",
                       visitedNodes=visited, producedItems=len(produced))
        context.pop("nextCursor", None)
        if more_pages:
            context["nextCursor"] = graph_cursor(request, len(page))
        return {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": op, "context": context, "items": page}


# ---------------------------------------------------------------------------
# history selection (baseline-source-then-prior-commit-sequence.1)

def history_selection(current_sequence, receipts, baseline_source_run, baseline_id, max_runs):
    """receipts: committed authoritative analysis receipts of the namespace in one consistent ledger snapshot [{runId, commitSequence}].
    The baseline source Run, when present, is listed first and is excluded from the prior-sequence candidates."""
    limit = max_runs - (1 if baseline_source_run else 0)
    prior = sorted((r for r in receipts if r["commitSequence"] < current_sequence and r["runId"] != baseline_source_run), key=lambda r: -r["commitSequence"])
    chosen = prior[:limit]
    return {"policy": "baseline-source-then-prior-commit-sequence.1", "currentCommitSequence": current_sequence,
            "baselineId": baseline_id, "baselineSourceRunId": baseline_source_run,
            "priorRuns": [{"runId": r["runId"], "commitSequence": r["commitSequence"]} for r in chosen],
            "priorRunsInSnapshot": len(prior),
            "requestedRunIds": ([baseline_source_run] if baseline_source_run else []) + [r["runId"] for r in chosen]}


# ---------------------------------------------------------------------------
# D9 aggregate with the invocation cancellation law (workflows-and-surfaces section 1)

def d9_aggregate(step_terminations):
    """Owned ordering over required step terminations: operational-failed > request-rejected > policy-failed > indeterminate > success;
    ties keep the first termination carrying domain detail in step order, else the first. Interrupted is not in this ordering."""
    if not step_terminations:
        return None
    for termination in step_terminations:
        if termination["class"] not in D9_ORDER:
            raise ModelRefusal("J-LEDGER-CANCELLATION", "interrupted step termination outside a before-settle cancellation")
    rank = min(D9_ORDER.index(t["class"]) for t in step_terminations)
    tied = [t for t in step_terminations if D9_ORDER.index(t["class"]) == rank]
    with_detail = [t for t in tied if "domainDetail" in t]
    return (with_detail or tied)[0]


def invocation_aggregate(steps, cancellation):
    """steps: [{kind, requirement, recorded, outcome?, termination?, analysisRunId?}] in step order.
    before-settle: some required step not terminal; remaining steps cancelled; aggregate interrupted(130) naming a Run committed by an earlier step.
    after-settle or no cancellation: the settled aggregate stands (never reclassified)."""
    if cancellation is not None:
        if cancellation["requested"] != (cancellation["phase"] != "none"):
            raise ModelRefusal("J-LEDGER-CANCELLATION", "requested and phase disagree")
        if cancellation["phase"] == "before-settle":
            required = [s for s in steps if s["requirement"] == "required"]
            if all(s["recorded"] and s["outcome"] != "cancelled" for s in required):
                raise ModelRefusal("J-LEDGER-CANCELLATION", "before-settle but every required step settled")
            for step in steps:
                if step["recorded"] and step["outcome"] == "cancelled" and step["termination"] != {"class": "interrupted", "signal": cancellation["signal"]}:
                    raise ModelRefusal("J-LEDGER-CANCELLATION", "cancelled step termination does not name the signal")
            committed = [s["analysisRunId"] for s in steps if s["recorded"] and s.get("analysisRunId") and s["outcome"] == "completed"]
            out = {"class": "interrupted", "signal": cancellation["signal"]}
            if committed:
                out["runId"] = committed[-1]
            return out
    if any(s["recorded"] and s["outcome"] == "cancelled" for s in steps):
        raise ModelRefusal("J-LEDGER-CANCELLATION", "cancelled step without a before-settle cancellation")
    if cancellation is not None and cancellation["phase"] == "after-settle":
        if not all(s["recorded"] for s in steps if s["requirement"] == "required"):
            raise ModelRefusal("J-LEDGER-CANCELLATION", "after-settle while a required step is not terminal")
    terminations = [s["termination"] for s in steps if s["recorded"] and s["requirement"] == "required"]
    return d9_aggregate(terminations)


EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}


def renderer_failure(run_id):
    """Owned required-delivery detail law (common:3 StepTermination): after a committed Run name it; otherwise forbid runId."""
    if run_id:
        return {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED", "faultCause": "delivery-required", "runId": run_id,
                "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT", "remedy": "re-run the command; the committed Run is unchanged", "subject": run_id}}
    return {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED", "faultCause": "delivery-required",
            "domainDetail": {"code": "DELIVERY.REQUIRED_PROJECTION_FAILED", "remedy": "re-run the command"}}


def failure_envelope(template, aggregate):
    env = {k: copy.deepcopy(template[k]) for k in ("schemaFamily", "schemaMajor", "requestId", "projectId")}
    env.update(kind="failure", termination=copy.deepcopy(aggregate), exitCode=EXIT[aggregate["class"]],
               errors=[copy.deepcopy(aggregate["domainDetail"])] if "domainDetail" in aggregate else [])
    return env


def delivery_outcome(fmt, prior_steps, render, template, run_id, command_row=None, cancellation=None):
    """One renderer selection over already-recorded steps (their terminations are never rewritten).
    render: None when no rendering is selected (no render attempt) or {requirement, result: written|failed|cancelled}.
    The owned D9 aggregate then applies to the render step like any other step: a required operational renderer failure dominates a
    request rejection; an equal-rank tie keeps the first termination with domain detail; an optional render failure never changes it.
    A signal during a required render is before-settle: the render is cancelled, the aggregate is interrupted (130) naming the committed Run,
    and the envelope is the run envelope (envelope5 admits interrupted on kind=run); no artifact is delivered."""
    steps = copy.deepcopy(prior_steps)
    render_record = None
    if render is not None:
        result = render["result"]
        termination = {"class": "success"} if result == "written" else ({"class": "interrupted", "signal": cancellation["signal"]} if result == "cancelled" else renderer_failure(run_id))
        render_record = {"kind": "render", "requirement": render["requirement"], "recorded": True,
                         "outcome": {"written": "completed", "failed": "failed", "cancelled": "cancelled"}[result], "termination": termination}
        steps.append(render_record)
    aggregate = invocation_aggregate(steps, cancellation)
    if aggregate["class"] == "interrupted" and template.get("kind") == "run" and aggregate.get("runId") == template["run"].get("runId"):
        envelope = dict(copy.deepcopy(template), termination=copy.deepcopy(aggregate), exitCode=EXIT["interrupted"])
    else:
        envelope = failure_envelope(template, aggregate)
    delivered = None
    if render is not None and render["result"] == "written":
        delivered = {"envelopeSha256": sha(canonical(envelope))}
        if fmt == "html":
            text = static_parity_text(envelope, command_row, document_disclosures({})).encode()
            delivered["staticParity"] = {"format": STATIC_FORMAT, "textSha256": sha(text), "textBytes": len(text)}
    return {"format": fmt, "renderAttempts": 0 if render is None else 1,
            "renderStep": None if render_record is None else {"requirement": render["requirement"], "outcome": render_record["outcome"], "termination": render_record["termination"]},
            "priorStepTerminations": [s["termination"] for s in prior_steps], "cancellation": cancellation, "aggregate": aggregate, "exitCode": EXIT[aggregate["class"]],
            "envelope": envelope, "delivered": delivered}


def effective_exploration_budget(budget, envelope, ledger, root_keys):
    """Bytes left for panels after the canonical envelope, the canonical ledger and the derived maxima of every other root member."""
    overhead = 2 + sum(len(canonical(k)) + 1 for k in root_keys) + (len(root_keys) - 1)
    remaining = budget["documentMaxBytes"] - overhead - len(canonical(envelope)) - len(canonical(ledger)) - budget["rootMemberMaxBytes"]
    return min(budget["explorationMaxCanonicalBytes"], remaining)


def missing_children(steps):
    out = []
    for step in steps:
        if not step["recorded"]:
            out.append({"stepId": step["stepId"], "missing": "render-in-progress" if step["kind"] == "render" else "step-result-not-recorded"})
        elif not step["attempts"] and step["outcome"] != "skipped":
            out.append({"stepId": step["stepId"], "missing": "attempts-not-recorded"})
    return out


def document_disclosures(panels):
    """Static disclosure counts: host-asserted retention/snapshot inputs are exposed, never promoted to verified completeness."""
    graph = panels.get("graph", {})
    history = panels.get("history", {})
    out = {"graphUnresolvedSubjects": None, "graphPlannedSubjects": None, "historyPriorRunsInSnapshotHostAsserted": None}
    if graph.get("state") == "present":
        resolution = graph["data"]["subjectResolution"]
        out["graphPlannedSubjects"] = len(resolution)
        out["graphUnresolvedSubjects"] = sum(1 for r in resolution if r["state"] != "resolved")
    if history.get("state") == "present":
        out["historyPriorRunsInSnapshotHostAsserted"] = history["data"]["selection"]["priorRunsInSnapshot"]
    return out


def static_parity_text(envelope, command_row, disclosures):
    """Script-independent section: owned human labelled canonical-JSON parity lines, disclosure lines, then the exact json envelope."""
    lines = []
    dispatch = command_row.get("queryDispatch") or command_row.get("advisoryDispatch")
    if dispatch is not None and envelope["kind"] in ("query", "run"):
        for field in command_row["parityFields"]:
            value = envelope
            for token in dispatch["parityPaths"][field].strip("/").split("/"):
                value = value[int(token)] if isinstance(value, list) else value[token]
            lines.append(field + ": " + canonical(value).decode())
    for key in sorted(disclosures):
        lines.append("disclosure." + key + ": " + canonical(disclosures[key]).decode())
    lines.append("envelope: " + canonical(envelope).decode())
    return "".join(line + "\n" for line in lines)


# ---------------------------------------------------------------------------
# byte law (contract section 9) against an effective exploration budget

def project_exploration(sources, provenance, applicable, budget_bytes, resolution=None, owner=None, plan=None):
    omitted = {"state": "omitted", "reason": "exploration-budget-exceeded"}
    panels = {name: dict(omitted) for name in applicable}
    cap = budget_bytes

    def size():
        return len(canonical(panels))

    def settle(name, rejected_size, build_with):
        delta = PLACEHOLDER_DELTA
        for _ in range(4):
            panels[name] = build_with(delta)
            nxt = rejected_size - size()
            if nxt == delta:
                break
            delta = nxt
        panels[name] = build_with(delta)
        assert rejected_size - size() == delta and size() <= cap
        return delta

    def prefix(name, count, item_cap, build):
        limit = min(count, item_cap)
        def cause(n):
            return "none" if n == count else ("item-cap" if n == item_cap else "byte-budget")
        panels[name] = build(0, PLACEHOLDER_DELTA if cause(0) == "byte-budget" else None)
        if size() > cap:
            panels[name] = dict(omitted)
            return
        lo, hi = 0, limit
        while lo < hi:
            mid = (lo + hi + 1) // 2
            panels[name] = build(mid, PLACEHOLDER_DELTA if cause(mid) == "byte-budget" else None)
            if size() <= cap:
                lo = mid
            else:
                hi = mid - 1
        if cause(lo) == "byte-budget":
            panels[name] = build(lo + 1, PLACEHOLDER_DELTA if cause(lo + 1) == "byte-budget" else None)
            rejected = size()
            settle(name, rejected, lambda d: build(lo, d))
        else:
            panels[name] = build(lo, None)

    def projection(total, n, item_cap, delta):
        cause = "none" if n == total else ("item-cap" if n == item_cap else "byte-budget")
        out = {"total": total, "omitted": total - n, "omissionCause": cause}
        if cause == "byte-budget":
            out["rejectedByteDelta"] = delta
        return out

    for name in PROJECTION_PRIORITY:
        if name not in panels:
            continue
        if name in ("comparison", "catalog"):
            panels[name] = {"state": "present", "data": sources[name]}
            if size() > cap:
                panels[name] = dict(omitted)
        elif name == "evidence":
            src = sources["evidence"]
            entries, item_cap = src["entries"], src["cap"]
            prefix(name, len(entries), item_cap, lambda n, d: {"state": "present", "data": {"coverageId": src["coverageId"], "entries": entries[:n],
                                                                                             "entriesProjection": projection(len(entries), n, item_cap, d), "provenance": provenance["evidence"]}})
        elif name == "graph":
            def panel(slots, stop_delta):
                proj = {"total": len(plan), "omitted": len(plan) - len(slots), "omissionCause": "none" if len(slots) == len(plan) else "byte-budget"}
                if proj["omissionCause"] == "byte-budget":
                    proj["rejectedByteDelta"] = stop_delta
                return {"state": "present", "data": {"policy": "finding-subject-slot-plan.1", "subjectResolution": resolution, "slots": slots,
                                                     "slotsProjection": proj, "subjectIndex": subject_index(slots, resolution), "provenance": provenance["graph"]}}

            def slot_for(planned, ordinal, page_size, delta):
                request = copy.deepcopy(planned["request"])
                request["page"] = {"size": page_size}
                response = owner.execute(request)
                host = {"continuation": continuation_for(response["context"]), "pageSizeCause": "ladder-first" if page_size == LADDER[0] else "byte-budget-reduced"}
                if page_size != LADDER[0]:
                    host["rejectedByteDelta"] = delta
                return {"ordinal": ordinal, "purpose": planned["purpose"], "anchorSubjectIds": planned["anchorSubjectIds"], "request": request, "response": response, "hostProjection": host}

            slots, stopped = [], False
            for planned in plan:
                placed, rejected_size = False, None
                for page_size in LADDER:
                    slot = slot_for(planned, len(slots), page_size, PLACEHOLDER_DELTA)
                    panels["graph"] = panel(slots + [slot], PLACEHOLDER_DELTA)
                    if size() <= cap:
                        if page_size == LADDER[0]:
                            slots.append(slot)
                        else:
                            final_slots = list(slots)
                            def with_delta(d, final_slots=final_slots, chosen=page_size, planned=planned):
                                return panel(final_slots + [slot_for(planned, len(final_slots), chosen, d)], PLACEHOLDER_DELTA)
                            settle("graph", rejected_size, with_delta)
                            slots = panels["graph"]["data"]["slots"]
                        placed = True
                        break
                    rejected_size = size()
                    if slot["response"]["context"]["traversalCoverage"] != "truncated-page":
                        break  # a smaller page cannot drop rows from an answer whose page is not full
                if not placed:
                    stopped = True
                    break
            if stopped:
                panels["graph"] = panel(slots + [slot_for(plan[len(slots)], len(slots), LADDER[-1], PLACEHOLDER_DELTA)], PLACEHOLDER_DELTA)
                rejected = size()
                settle("graph", rejected, lambda d: panel(slots, d))
            else:
                panels["graph"] = panel(slots, None)
            if size() > cap:
                panels["graph"] = dict(omitted)
        elif name == "history":
            src = sources["history"]
            rows, item_cap = src["runs"], src["cap"]

            def build_h(counts, deltas):
                runs = []
                for i, (row, n) in enumerate(zip(rows, counts)):
                    if row["state"] != "present":
                        runs.append({k: row[k] for k in ("state", "runId", "availability", "detail") if k in row})
                        continue
                    runs.append({"state": "present", "runId": row["runId"], "commitSequence": row["commitSequence"], "run": row["run"], "findings": row["findings"][:n],
                                 "findingsProjection": projection(len(row["findings"]), n, item_cap, deltas[i])})
                return {"state": "present", "data": {"selection": src["selection"], "runs": runs, "provenance": provenance["history"]}}

            counts = [0] * len(rows)
            deltas = [PLACEHOLDER_DELTA] * len(rows)
            panels[name] = build_h(counts, deltas)
            if size() > cap:
                panels[name] = dict(omitted)
                continue
            for i, row in enumerate(rows):
                if row["state"] != "present":
                    continue
                total = len(row["findings"])
                lo, hi = 0, min(total, item_cap)
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    trial = list(counts)
                    trial[i] = mid
                    panels[name] = build_h(trial, deltas)
                    if size() <= cap:
                        lo = mid
                    else:
                        hi = mid - 1
                counts[i] = lo
                if lo < min(total, item_cap):
                    trial = list(counts)
                    trial[i] = lo + 1
                    panels[name] = build_h(trial, deltas)
                    rejected = size()
                    def with_delta(d, i=i):
                        local = list(deltas)
                        local[i] = d
                        return build_h(counts, local)
                    deltas[i] = settle(name, rejected, with_delta)
                panels[name] = build_h(counts, deltas)
    return panels
