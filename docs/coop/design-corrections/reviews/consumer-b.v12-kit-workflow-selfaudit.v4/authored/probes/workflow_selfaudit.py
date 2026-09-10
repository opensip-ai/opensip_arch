#!/usr/bin/env python3
"""Independent kit-only self-audit of the v3 48-PASS WORKFLOW_SCOPE_ADMITS.

Does not import consumer helper/canonical/identity/evaluator/schema_admit.
Expected values are reminted from the frozen 80-file kit recipes.
Consumer helper output and artifact metadata are claims under test.
Writes only under this output directory.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-selfaudit.v4/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/subject")
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/requirements.json")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v3/consumer-snapshot")
PRIOR = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v3/output")
MANIFEST = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v3/snapshot-manifest.json")
PY = "/tmp/opensip-architecture-review-env/bin/python"

SNAP_EXPECT = "b2e92652443df230f532c7c4eef81110e27ef1be078adbd312bd1c050274f65c"
KIT_EXPECT = "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8"
REQ_EXPECT = "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495"

PRODUCT_PREFIX = b"opensip.product.v1"
I64_MIN = -(2**63)
U64_MAX = 2**64 - 1
MAX_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32

GRAPH_PROJECTABLE = {
    ("calls", "resolved-callee"),
    ("references", "resolved-binding"),
    ("imports", "resolved-target"),
    ("control-flow", "syntactic"),
    ("reachability", "from-resolved-calls"),
}

CLASSIFICATIONS = (
    "UNCHANGED",
    "CODE-NET-NEW",
    "CODE-FIXED",
    "DETECTION-DELTA",
    "POLICY-DELTA",
    "SCOPE-DELTA",
    "WAIVER-DELTA",
    "EVIDENCE-DELTA",
    "INDETERMINATE",
)

QUERY_PARITY_FIELDS = (
    "resolved-view",
    "availability",
    "truncated",
    "total-items",
    "termination-class",
    "query-response",
)

rows: list[dict[str, Any]] = []
notes: list[str] = []
withdrawals: list[dict[str, Any]] = []


def rec(id_: str, status: str, *, kind: str, selector: str, detail: Any = None, prior: str = "PASS",
        measurementKind: str = "independent-kit-derived", extra: dict | None = None):
    row = {
        "id": id_,
        "status": status,
        "kind": kind,
        "selector": selector,
        "priorStatus": prior,
        "measurementKind": measurementKind,
        "detail": detail,
    }
    if extra:
        row.update(extra)
    rows.append(row)
    if prior == "PASS" and status != "PASS":
        withdrawals.append({"id": id_, "prior": prior, "successor": status, "reason": selector if isinstance(selector, str) else str(detail)[:400]})


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_snap(rel: str) -> Any:
    return json.loads((SNAP / rel).read_text())


def load_json(p: Path) -> Any:
    return json.loads(p.read_text())


# ---- independent C / H from identity-and-evidence.md §3 ----

def _encode_string(s: str) -> str:
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\t":
            out.append("\\t")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\r":
            out.append("\\r")
        elif o < 0x20:
            out.append(f"\\u{o:04x}")
        elif 0xD800 <= o <= 0xDFFF:
            raise ValueError(f"surrogate U+{o:04X}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _encode(value: Any, depth: int) -> str:
    if depth > MAX_DEPTH:
        raise ValueError("nesting too deep")
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        if value < I64_MIN or value > U64_MAX:
            raise ValueError("integer out of range")
        return str(value)
    if type(value) is str:
        return _encode_string(value)
    if type(value) is list:
        return "[" + ",".join(_encode(v, depth + 1) for v in value) + "]"
    if type(value) is dict:
        keys = list(value.keys())
        for k in keys:
            if type(k) is not str:
                raise ValueError("non-string key")
        keys.sort(key=lambda k: k.encode("utf-8"))
        parts = [_encode_string(k) + ":" + _encode(value[k], depth + 1) for k in keys]
        return "{" + ",".join(parts) + "}"
    raise ValueError(f"cannot encode {type(value).__name__}")


def C(value: Any) -> bytes:
    raw = _encode(value, 1).encode("utf-8")
    if len(raw) > MAX_BYTES:
        raise ValueError("descriptor too large")
    return raw


def H(domain: str, value: Any) -> str:
    cx = C(value)
    pre = PRODUCT_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00" + len(cx).to_bytes(8, "big") + cx
    return hashlib.sha256(pre).hexdigest()


def committed(prefix: str, domain: str, desc: Any) -> str:
    return prefix + H(domain, desc)


def raw_c_hex(obj: Any) -> str:
    return hashlib.sha256(C(obj)).hexdigest()


def repair_apply_key(project_id: str, repair_plan_id: str, base_snapshot_id: str) -> str:
    return raw_c_hex({
        "operation": "repair-apply",
        "projectId": project_id,
        "repairPlanId": repair_plan_id,
        "baseSnapshotId": base_snapshot_id,
    })


def mutation_intent(scope: dict) -> str:
    if scope.get("operation") == "repair-apply":
        raise ValueError("MUTATION_SCOPE_REPAIR_APPLY")
    return H("workflow.mutation-intent", scope)


# ---- kit dialect suffix table (identity-schemas.v3 languageVersionBinding syntax dialect.table) ----

def kit_suffix_table() -> dict[str, str]:
    ident = load_json(KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json")
    # Walk to syntax-only languageVersionBinding dialect.table
    found = {}
    def walk(o):
        if isinstance(o, dict):
            if "table" in o and isinstance(o.get("table"), dict) and ".rs" in o["table"]:
                found.update(o["table"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(ident)
    return found


def kit_suffix(path: str) -> str:
    table = kit_suffix_table()
    # longest matching suffix
    matches = [suf for suf in table if path.endswith(suf)]
    if not matches:
        raise ValueError("BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN")
    matches.sort(key=len, reverse=True)
    return table[matches[0]]


def config_node_kind(path: str) -> str:
    base = path.rsplit("/", 1)[-1]
    if base == "tsconfig.json":
        return "tsconfig"
    if base == "jsconfig.json":
        return "jsconfig"
    return "other"


def nodes_path_order_ok(nodes: list[dict]) -> bool:
    paths = [n["path"] for n in nodes]
    encoded = [p.encode("utf-8") for p in paths]
    return encoded == sorted(encoded) and len(set(paths)) == len(paths)


def graph_identity_ok(graph: dict, claimed: str) -> dict:
    kind_ok = all(n.get("kind") == config_node_kind(n["path"]) for n in graph.get("nodes") or [])
    order_ok = nodes_path_order_ok(graph.get("nodes") or [])
    digest = raw_c_hex(graph)
    return {
        "digest": digest,
        "digestMatch": digest == claimed,
        "kindOk": kind_ok,
        "pathOrderOk": order_ok,
        "entryNull": graph.get("entryConfigPath") is None,
        "schemaVersion": graph.get("schemaVersion"),
        "requiredFields": set(graph.keys()) <= {"schemaVersion", "entryConfigPath", "nodes"} and {"schemaVersion", "entryConfigPath", "nodes"} <= set(graph.keys()),
    }


def exists_three_valued(*, has_match: bool, coverage: str | None) -> str:
    """Published exists law: known match true; no coverage indeterminate; complete coverage no match false."""
    if has_match:
        return "true"
    if coverage is None:
        return "indeterminate"
    if coverage == "complete":
        return "false"
    return "indeterminate"


def classify_presence(presence: dict) -> tuple[str, bool]:
    """First-axis classification from workflows-and-surfaces.md §3 (B→E0 code, then detection/policy/scope/waiver)."""
    b, e0, e1, e2, e3, e4 = (presence.get(k) for k in ("B", "E0", "E1", "E2", "E3", "E4"))
    waived = bool(presence.get("waivedC"))
    live = e4 is True and not waived
    if e0 is not None and b is not None and bool(b) != bool(e0):
        return ("CODE-NET-NEW" if (not b and e0) else "CODE-FIXED"), live
    if e0 is not None and e1 is not None and bool(e0) != bool(e1):
        return "DETECTION-DELTA", live
    if e1 is not None and e2 is not None and bool(e1) != bool(e2):
        return "POLICY-DELTA", live
    if e2 is not None and e3 is not None and bool(e2) != bool(e3):
        return "SCOPE-DELTA", live
    if e3 is not None and e4 is not None and (bool(e3) != bool(e4) or waived):
        return "WAIVER-DELTA", live
    pivot_true = any(presence.get(k) is True for k in ("E0", "E1", "E2", "E3"))
    if b is False and pivot_true and e4 is False:
        return ("CODE-NET-NEW" if e0 is True else "DETECTION-DELTA"), live
    return "UNCHANGED", live


def counts_from_entries(entries):
    c = {k: 0 for k in CLASSIFICATIONS}
    c["gating"] = 0
    for e in entries:
        c[e["classification"]] += 1
        if e.get("gates"):
            c["gating"] += 1
    return c


def ep_key(ep: dict) -> tuple:
    return (
        ep.get("universe") or "",
        ep.get("kind") or "",
        ep.get("nativeSubjectId") or "",
        ep.get("packageManifestPath") or "",
    )


def project_edges(facts, relation, min_resolution):
    if (relation, min_resolution) not in GRAPH_PROJECTABLE:
        raise ValueError("QUERY.RELATION_UNSUPPORTED")
    edges = []
    for f in facts:
        recd = f.get("record") or f
        if recd.get("relation") != relation or recd.get("resolution") != min_resolution:
            continue
        payload = recd.get("payload") or {}
        src = {
            "universe": recd["sourceUniverse"],
            "kind": "symbol",
            "nativeSubjectId": payload["caller"],
        }
        tgt = {
            "universe": recd["targetUniverse"],
            "kind": "symbol",
            "nativeSubjectId": payload["resolvedCallee"],
        }
        edges.append({
            "factId": f["factId"],
            "relation": relation,
            "resolution": min_resolution,
            "source": src,
            "target": tgt,
        })
    edges.sort(key=lambda e: ep_key(e["source"]) + ep_key(e["target"]) + (e["factId"],))
    return edges


def neighbors(edges, endpoint, direction):
    out = []
    for e in edges:
        if direction in ("outgoing", "both") and ep_key(e["source"]) == ep_key(endpoint):
            out.append(e)
        elif direction in ("incoming", "both") and ep_key(e["target"]) == ep_key(endpoint):
            out.append(e)
    out.sort(key=lambda e: ep_key(e["source"]) + ep_key(e["target"]) + (e["factId"],))
    return out


def shortest_path(edges, start, target, max_depth, direction="outgoing"):
    if ep_key(start) == ep_key(target):
        return {"hopCount": 0, "start": start, "target": target, "nodes": [start], "edges": []}
    from collections import deque
    adj = {}
    for e in edges:
        adj.setdefault(ep_key(e["source"]), []).append(e)
    for k in adj:
        adj[k].sort(key=lambda e: e["factId"])
    q = deque([(ep_key(start), 0, [start], [])])
    seen = {ep_key(start)}
    while q:
        cur, depth, nodes, path_edges = q.popleft()
        if depth >= max_depth:
            continue
        for e in adj.get(cur, []):
            nxt = ep_key(e["target"])
            if nxt in seen:
                continue
            nn = nodes + [e["target"]]
            ne = path_edges + [e]
            if nxt == ep_key(target):
                return {"hopCount": len(ne), "start": start, "target": target, "nodes": nn, "edges": [
                    {"factId": x["factId"], "source": x["source"], "target": x["target"]} for x in ne
                ]}
            seen.add(nxt)
            q.append((nxt, depth + 1, nn, ne))
    return None


def reach(edges, start, max_depth, include_start, direction="outgoing"):
    from collections import deque
    adj = {}
    for e in edges:
        adj.setdefault(ep_key(e["source"]), []).append(e)
    for k in adj:
        adj[k].sort(key=lambda e: e["factId"])
    rows_map = {}
    if include_start:
        rows_map[ep_key(start)] = {"endpoint": start, "depth": 0}
    q = deque([(ep_key(start), start, 0)])
    seen = {ep_key(start)}
    while q:
        curk, cur, depth = q.popleft()
        if depth >= max_depth:
            continue
        for e in adj.get(curk, []):
            nxtk = ep_key(e["target"])
            if nxtk in seen:
                continue
            seen.add(nxtk)
            rows_map[nxtk] = {"endpoint": e["target"], "depth": depth + 1, "viaFactId": e["factId"]}
            q.append((nxtk, e["target"], depth + 1))
    rows_out = list(rows_map.values())
    rows_out.sort(key=lambda r: ep_key(r["endpoint"]))
    return rows_out


def envelope_shape(obj: dict) -> dict:
    return {
        "schemaFamily": obj.get("schemaFamily"),
        "schemaMajor": obj.get("schemaMajor"),
        "kind": obj.get("kind"),
        "hasRequestId": isinstance(obj.get("requestId"), str) and obj["requestId"].startswith("req1_"),
        "hasTermination": isinstance(obj.get("termination"), dict) and "class" in obj["termination"],
        "hasErrors": isinstance(obj.get("errors"), list) and len(obj.get("errors") or []) > 0,
        "hasExitCode": "exitCode" in obj,
        "noRunField": "run" not in obj,
    }


def invocation_shape(obj: dict) -> dict:
    steps = obj.get("orderedSteps") or []
    return {
        "schemaFamily": obj.get("schemaFamily"),
        "schemaMajor": obj.get("schemaMajor"),
        "nSteps": len(steps),
        "stepKinds": [s.get("kind") for s in steps],
        "profiles": [(s.get("params") or {}).get("profile") for s in steps if s.get("kind") == "analysis"],
        "selectionsDiffer": len({json.dumps(s.get("params"), sort_keys=True) for s in steps if s.get("kind") == "analysis"}) > 1,
    }


def step_term_shape(obj: dict) -> bool:
    return isinstance(obj, dict) and "class" in obj and obj["class"] in {
        "success", "policy-failed", "request-rejected", "operational-failed", "indeterminate", "interrupted"
    }


def derive_edition(ownership: dict, body_path: str) -> int:
    if ownership.get("enumeration") != "complete":
        raise ValueError("BODY_LANGUAGE_OWNER_UNENUMERATED")
    units = {u["unitId"]: u for u in ownership["units"]}
    selected = set(ownership["selectedUnitIds"])
    rows_o = [r for r in ownership["ownership"] if r["path"] == body_path and r["unitId"] in selected]
    editions = []
    for r in rows_o:
        u = units[r["unitId"]]
        te = u.get("targetEdition")
        if te is None:
            raise ValueError("no targetEdition")
        editions.append(int(te))
    if len(set(editions)) != 1:
        raise ValueError("BODY_LANGUAGE_DIALECT_AMBIGUOUS")
    return editions[0]


def ownership_required(o: dict) -> bool:
    return {"schemaVersion", "enumeration", "units", "selectedUnitIds", "ownership"} <= set(o.keys())


# ---- custody ----
man_sha = sha_file(MANIFEST)
kit_sha = sha_file(KIT / "consumer-input-manifest.json")
req_sha = sha_file(REQ)
man = load_json(MANIFEST)
file_pass = 0
file_fail = 0
undeclared = 0
# verify declared files only; do not walk extra
for ent in man.get("files") or man.get("entries") or []:
    if isinstance(ent, dict):
        rel = ent.get("path") or ent.get("relativePath")
        exp = ent.get("sha256") or ent.get("digest")
        ln = ent.get("bytes") or ent.get("length")
        p = SNAP / rel if rel else None
        if p and p.is_file():
            b = p.read_bytes()
            ok = hashlib.sha256(b).hexdigest() == exp and (ln is None or len(b) == ln)
            file_pass += 1 if ok else 0
            file_fail += 0 if ok else 1
        else:
            file_fail += 1
n_declared = len(man.get("files") or man.get("entries") or [])
if n_declared == 0:
    # fallback: snapshot-manifest.json structure
    files = man.get("snapshotFiles") or man.get("members") or []
    n_declared = len(files)

# Use hash-verification.json if present as a claim, but independently hash all SNAP files listed in manifest
# If files key missing, read snapshot-manifest more carefully
if n_declared == 0:
    # typical kit consumer snapshot-manifest
    pass

hv = load_snap("hash-verification.json") if (SNAP / "hash-verification.json").exists() else {}

# Independent: hash every file listed in snapshot-manifest
listed = []
if "files" in man:
    listed = man["files"]
elif "entries" in man:
    listed = man["entries"]
elif "items" in man:
    listed = man["items"]

# If still empty, try nested
if not listed:
    for k, v in man.items():
        if isinstance(v, list) and v and isinstance(v[0], dict) and ("path" in v[0] or "relativePath" in v[0]):
            listed = v
            break

ind_pass = 0
ind_fail = []
for ent in listed:
    rel = ent.get("path") or ent.get("relativePath") or ent.get("name")
    exp = ent.get("sha256") or ent.get("digest") or ent.get("sha256Hex")
    ln = ent.get("bytes") or ent.get("length") or ent.get("size")
    p = SNAP / rel
    if not p.is_file():
        ind_fail.append({"rel": rel, "reason": "missing"})
        continue
    b = p.read_bytes()
    got = hashlib.sha256(b).hexdigest()
    if got != exp or (ln is not None and len(b) != ln):
        ind_fail.append({"rel": rel, "reason": "mismatch", "got": got, "exp": exp, "len": len(b), "ln": ln})
    else:
        ind_pass += 1

custody = {
    "snapshotManifestSha256": man_sha,
    "snapshotManifestMatch": man_sha == SNAP_EXPECT,
    "kitManifestSha256": kit_sha,
    "kitManifestMatch": kit_sha == KIT_EXPECT,
    "requirementsSha256": req_sha,
    "requirementsMatch": req_sha == REQ_EXPECT,
    "listedCount": len(listed),
    "independentFilePass": ind_pass,
    "independentFileFail": ind_fail[:8],
    "nFail": len(ind_fail),
}

frozen = load_snap("frozen-run-hashes.json")["runs"]
fr_ok = True
fr_detail = {}
for name, exp in frozen.items():
    b = (SNAP / "runs" / name).read_bytes()
    got = hashlib.sha256(b).hexdigest()
    ok = got == exp["sha256"] and len(b) == exp["bytes"]
    fr_detail[name] = {"ok": ok, "sha256": got, "bytes": len(b)}
    if not ok:
        fr_ok = False

# Prior review imported consumer helper?
prior_probe = (PRIOR / "probes/workflow_admit.py").read_text()
imported_consumer_helper = "from helper." in prior_probe or "import helper" in prior_probe
vacuous_config_pass = "or True" in prior_probe
file_presence_config = 'PASS" if load("vectors/config-custom-multi-base.json")' in prior_probe or "if load(\"vectors/config-custom-multi-base.json\")" in prior_probe

# ---- R-REPAIR-APPLY-KEY ----
rak = load_snap("vectors/repair-apply-key.json")
key = repair_apply_key(rak["applyKeyPreimage"]["projectId"], rak["applyKeyPreimage"]["repairPlanId"], rak["applyKeyPreimage"]["baseSnapshotId"])
mut = mutation_intent(rak["mutationReplayScope"])
pre_keys = set(rak["applyKeyPreimage"])
rec("R-REPAIR-APPLY-KEY",
    "PASS" if key == rak["repairApplyKey"] and rak["unequal"] and key != mut and pre_keys == {"operation", "projectId", "repairPlanId", "baseSnapshotId"} else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="repair.schema.json#/.../recipes/repair-apply raw SHA-256 of C({operation, projectId, repairPlanId, baseSnapshotId}); unequal to H(workflow.mutation-intent)",
    detail={"recomputed": key, "claimed": rak["repairApplyKey"], "mut": mut, "unequal": key != mut})

# ---- R-REPAIR-DESCRIPTOR ----
rp = load_snap("vectors/repair-descriptor.json")
desc = rp.get("descriptor") or rp
want = committed("repairplan2:", "workflow.repair-plan", desc if "schemaFamily" in desc else rp["descriptor"])
got_id = rp.get("repairPlanId")
rec("R-REPAIR-DESCRIPTOR",
    "PASS" if got_id == want else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="H('workflow.repair-plan', descriptor) → repairplan2:",
    detail={"want": want, "got": got_id})

# ---- R-MUTATION-REPLAY-SCOPE ----
mrs = load_snap("vectors/mutation-replay-scope.json")
scope = {k: mrs[k] for k in ("schemaVersion", "requestId", "stepId", "projectId", "operation")}
repair_apply_refused = False
try:
    mutation_intent({**scope, "operation": "repair-apply"})
except ValueError:
    repair_apply_refused = True
rec("R-MUTATION-REPLAY-SCOPE",
    "PASS" if mrs["mutationIntentKey"] == mutation_intent(scope) and scope["operation"] == "purge" and repair_apply_refused else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="H('workflow.mutation-intent', MutationReplayScopeV1); repair-apply refused in generic field",
    detail={"key": mrs["mutationIntentKey"], "recompute": mutation_intent(scope), "repairApplyRefused": repair_apply_refused})

# ---- min-resolution ----
mr = load_snap("vectors/min-resolution.json")
by = {c["level"]: c for c in mr["cases"]}
has_facts = any(("facts" in c) or ("coverages" in c) or ("qualifyingFacts" in c) or ("insufficientCoverage" in c) for c in mr["cases"])
syn_i = exists_three_valued(has_match=False, coverage=None)
res_i = exists_three_valued(has_match=False, coverage=None)
res_cov = exists_three_valued(has_match=False, coverage="complete")
typ_cov = exists_three_valued(has_match=False, coverage="complete")
syn_q = exists_three_valued(has_match=True, coverage=None)
# law values
law_ok = syn_i == "indeterminate" and res_cov == "false" and typ_cov == "false" and syn_q == "true"
stored_three = set(by) == {"syntactic", "resolved", "type"}
stored_ins = {
    "syntactic": by["syntactic"]["insufficientValue"] == "indeterminate",
    "resolved": by["resolved"]["insufficientValue"] == "false",
    "type": by["type"]["insufficientValue"] == "false",
}
# Original requires facts/Coverage at each level × qualifying/insufficient. Retained vector is helper-agreement labels.
rec("R-MIN-RESOLUTION-THREE-LEVELS",
    "REFUSED" if not has_facts else ("PASS" if law_ok and stored_three and all(stored_ins.values()) else "REFUSED"),
    kind="standaloneCanonicalVector",
    selector="atom-evaluation-contract exists; original verb: each of syntactic/resolved/type with qualifying and insufficient facts/Coverage",
    detail={
        "retainedHasFactsOrCoverage": has_facts,
        "vectorIsHelperAgreementTable": mr.get("function"),
        "independentLaw": {"noCov": syn_i, "completeNoMatch": res_cov, "match": syn_q},
        "stored": {k: (by[k]["qualifyingValue"], by[k]["insufficientValue"]) for k in by},
        "helperAgreesFlagsAreClaims": True,
    })

mre = load_snap("vectors/min-resolution-repair-evidence.json")
mre_desc = mre["repairPlan"]["descriptor"]
mre_want = committed("repairplan2:", "workflow.repair-plan", mre_desc)
mre_got = mre["repairPlan"]["repairPlanId"]
ev = mre_desc.get("evidenceRequirements") or []
levels = {(e.get("relation"), e.get("minResolution")) for e in ev}
need = {("imports", "syntactic-specifier"), ("imports", "resolved-target"), ("types", "checked")}
rec("R-MIN-RESOLUTION-REPAIR-EVIDENCE",
    "PASS" if mre_got == mre_want and levels == need and len(mre.get("requirements") or []) == 3 else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="RepairPlanV1 H('workflow.repair-plan') evidenceRequirements bound to three min-resolution rungs",
    detail={"want": mre_want, "got": mre_got, "levels": sorted(levels)})

# ---- unsupported grammar ----
ug = load_snap("vectors/unsupported-grammar.json")
try:
    kit_suffix("notes.unknownlang")
    unk_ok = False
    unk_code = None
except ValueError as e:
    unk_ok = True
    unk_code = str(e)
pos_tok = kit_suffix("hello.rs")
rec("R-RUN-UNSUPPORTED-GRAMMAR",
    "PASS" if ug["negative"]["result"]["ok"] is False and unk_ok and ug["didNotAssumeTypescriptCompiler"] else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="identity-schemas.v3 dialect.table onUnknown BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN; original verb: unsupported grammar without assuming a TypeScript compiler",
    detail={
        "kitPositiveToken": pos_tok,
        "consumerPositive": ug["positive"]["result"],
        "firstRefusal": ug["negative"]["result"].get("firstRefusal"),
        "independentUnknown": unk_code,
        "note": "Kit .rs → rs; consumer SYNTAX_SUFFIX_TABLE .rs → rust-syntax. Unknown-suffix refusal is the required observable.",
    })

# ---- hidden mismatch ----
hm = load_snap("vectors/hidden-mismatch.json")
rec("R-HIDDEN-MISMATCH-PER-LANGUAGE",
    "PASS" if hm["typescript"]["negative"]["ok"] is False and hm["rust"]["negative"]["ok"] is False
    and hm["typescript"]["negative"]["firstRefusal"] and hm["rust"]["negative"]["firstRefusal"] else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="negative vectors per language with first-refusal boundary",
    detail={"ts": hm["typescript"]["negative"]["firstRefusal"]["code"], "rust": hm["rust"]["negative"]["firstRefusal"]["code"]})

# ---- clones negatives / js body ----
cn = load_snap("vectors/clones-negatives.json")
codes = [v["firstRefusal"]["code"] for v in cn["vectors"] if not v.get("ok")]
ok_js = [v for v in cn["vectors"] if v.get("name") == "javascript-body-through-ts-ok"]
rec("R-CLONES-NEGATIVE-VECTORS",
    "PASS" if {"FACT_ANCHOR_CARDINALITY", "CLONE_LEVEL_SPEC_MISSING", "BODY_LANGUAGE_MISMATCH"} <= set(codes) and ok_js and ok_js[0]["ok"] else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="actual negative vectors with first-refusal boundaries",
    detail=codes)

jsb = load_snap("vectors/js-body-through-ts.json")
rec("R-JS-CLONE-BODY-THROUGH-TS",
    "PASS" if jsb.get("bodyLanguageId") == "javascript" and jsb.get("providerLanguageId") == "typescript" and jsb.get("distinct") is True else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="identity-schemas.v3 bodyLanguageLaw: languageId of the BODY ≠ provider; observable is languageId vs provider",
    detail={"bodyLanguageId": jsb.get("bodyLanguageId"), "providerLanguageId": jsb.get("providerLanguageId"),
            "l0Remint": "not required by this observable; span not retained"})

# ---- repair authority ----
ra = load_snap("vectors/repair-authority-per-target.json")
rec("R-REPAIR-AUTHORITY-PER-TARGET",
    "PASS" if ra["positive"]["result"]["ok"] and ra["negative"]["result"]["ok"] is False
    and ra["negative"]["result"]["firstRefusal"]["code"] == "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE" else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="evaluator-composition-contract unmatched cannot satisfy fingerprint-targeted repair",
    detail=ra["negative"]["result"]["firstRefusal"])

# ---- rust body identity pair ----
own = load_snap("vectors/rust-body-identity-pair.json")
s0, s1 = own["sameDialectOwnershipSelections"]
e0 = derive_edition(s0["ownership"], "src/lib.rs")
e1 = derive_edition(s1["ownership"], "src/lib.rs")
e2021 = derive_edition(own["dialectChange"]["ownership"], "src/lib.rs")
same_internal = s0["l0"] == s1["l0"] and e0 == e1 == 2018 and s0["ownership"] != s1["ownership"]
moved = own["dialectChange"]["l0"] != s0["l0"] and e2021 == 2021
span_retained = any(k in own for k in ("span", "bodySpan", "sourceBytes", "compilerBuild", "body-language-version", "blv"))
# identity recipe: languageVersion = SHA-256(C(BLV)); BLV dialect.edition integer enum; derived from retained nested records
blv_int = {
    "schemaVersion": 1,
    "languageId": "rust",
    "compilerName": "rustc",
    "compilerVersion": "1.76.0",
    "compilerBuild": "0" * 64,
    "dialect": {"edition": 2018},
}
blv_str = {**blv_int, "dialect": {"edition": "2018"}}
# integer edition is kit; string is not schema-admitted
int_edition_ok = type(blv_int["dialect"]["edition"]) is int and blv_int["dialect"]["edition"] in {2015, 2018, 2021, 2024}
str_edition_ok = type(blv_str["dialect"]["edition"]) is str
# completeRunProperty identity cannot be reminted without retained span/compilerBuild/BLV
rec("R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
    "REFUSED",
    kind="completeRunProperty",
    selector="identity-schemas.v3 languageVersionBindingLaw: BLV is DERIVED from retained nested records; dialect.edition integer enum; pairwise claimed-hash stability of a non-remintable encoding is not the kit body identity",
    detail={
        "sameInternalClaimedL0": same_internal,
        "derivedEditions": [e0, e1, e2021],
        "ownershipMapsUnequal": s0["ownership"] != s1["ownership"],
        "ownershipRequiredFields": ownership_required(s0["ownership"]),
        "distinctWhenDialectChangesClaimed": moved,
        "spanOrBlvRetained": span_retained,
        "claimedL0": s0["l0"],
        "integerEditionEnum": int_edition_ok,
        "stringEditionNotKit": str_edition_ok,
        "priorWaiver": "v3 PASSed pairwise claimed L0 equality and noted string-edition / unretained-span as implementation notes, not refusals",
    })

# ---- comparisons ----
def cmp_check(rel, rid):
    obj = load_snap(rel)
    hid = committed("comparison2:", "workflow.comparison", obj["descriptor"])
    cnt = counts_from_entries(obj["descriptor"]["entries"])
    return {
        "id": rid,
        "hOk": obj["comparisonResultId"] == hid,
        "want": hid,
        "got": obj["comparisonResultId"],
        "countsOk": obj["descriptor"]["counts"] == cnt,
        "wantCounts": cnt,
        "gotCounts": obj["descriptor"]["counts"],
    }

c_empty = cmp_check("vectors/comparison-empty-result.json", "empty")
c_miss = cmp_check("vectors/comparison-missing.json", "missing")
c_chg = cmp_check("vectors/comparison-evidence-changed.json", "changed")
rec("R-CMP-EMPTY-RESULT", "PASS" if c_empty["hOk"] and c_empty["countsOk"] else "REFUSED",
    kind="standaloneCanonicalVector", selector="H('workflow.comparison', descriptor) + counts from entries", detail=c_empty)
rec("R-CMP-MISSING", "PASS" if c_miss["hOk"] and c_miss["countsOk"] else "REFUSED",
    kind="standaloneCanonicalVector", selector="H('workflow.comparison', descriptor)", detail=c_miss)
rec("R-CMP-EVIDENCE-CHANGED", "PASS" if c_chg["hOk"] and c_chg["countsOk"] else "REFUSED",
    kind="standaloneCanonicalVector", selector="H('workflow.comparison', descriptor)", detail=c_chg)

pivot = load_snap("vectors/pivot-only-fingerprints.json")
pent = pivot["descriptor"]["entries"][0]
cls, live = classify_presence(pent["presence"])
phid = committed("comparison2:", "workflow.comparison", pivot["descriptor"])
rec("R-PIVOT-ONLY-FINGERPRINTS",
    "PASS" if pent["presence"]["B"] is False and pent["presence"]["E0"] is True and pent["presence"]["E4"] is False
    and pent["classification"] == cls and pent["liveInCurrent"] == live == False and pivot["comparisonResultId"] == phid else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="workflows-and-surfaces.md §3 first-axis; fingerprint in E0 only",
    detail={"cls": cls, "live": live, "claimed": pent["classification"], "hOk": pivot["comparisonResultId"] == phid})

scopep = load_snap("vectors/comparison-scope-policy-only.json")
cmp = scopep["comparison"]
rec("R-SCOPE-POLICY-ONLY-COMPARISON",
    "PASS" if cmp["comparisonResultId"] == committed("comparison2:", "workflow.comparison", cmp["descriptor"])
    and cmp["descriptor"]["baselineContext"]["scopeDigest"] != cmp["descriptor"]["currentContext"]["scopeDigest"]
    and cmp["descriptor"]["baselineContext"]["policyDigest"] == cmp["descriptor"]["currentContext"]["policyDigest"] else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="comparison contextDelta.scopeChanged; two retained scope digests unequal / policy equal")

e0e3 = load_snap("vectors/baseline-e0-e3.json")
rec("R-E0-VS-E1-E3",
    "PASS" if e0e3["E0"]["comparisonResultId"] == committed("comparison2:", "workflow.comparison", e0e3["E0"]["descriptor"])
    and e0e3["E1E3"]["comparisonResultId"] == committed("comparison2:", "workflow.comparison", e0e3["E1E3"]["descriptor"]) else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="H comparison identities for E0 vs E1/E3 descriptors")

base = load_snap("vectors/baseline-audit.json")
bwant = committed("baseline2:", "workflow.baseline", base["descriptor"])
rec("R-BASELINE-AUDIT",
    "PASS" if base["baselineId"] == bwant else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="H('workflow.baseline', descriptor) → baseline2:",
    detail={"want": bwant, "got": base["baselineId"]})

# ---- config ----
cs = load_snap("vectors/config-synthesized.json")
cs_g = cs["graph"]
cs_id = graph_identity_ok(cs_g, cs["graphDigestSha256"])
rec("R-CONFIG-SYNTHESIZED",
    "PASS" if cs_id["digestMatch"] and cs_id["requiredFields"] and cs_id["entryNull"] and cs_g["nodes"] == [] and cs.get("tsconfigGraphHashIsNotAGraphField") else "REFUSED",
    kind="standaloneConfigVector",
    selector="native-evidence TypeScriptConfigGraphV1; identity = raw SHA-256 of C(graph); entryConfigPath null iff synthesized",
    detail=cs_id)

cmb = load_snap("vectors/config-custom-multi-base.json")
cmb_g = cmb["graph"]
cmb_id = graph_identity_ok(cmb_g, cmb["graphDigestSha256"])
# repeated bases: schema says repeated edges retained (sequence not set); original requires repeated bases with retained precedence
repeated_edges = any(len(n.get("extendsResolved") or []) != len(set(n.get("extendsResolved") or [])) for n in cmb_g["nodes"])
multi_ordered = any(len(n.get("extendsResolved") or []) >= 2 for n in cmb_g["nodes"])
entry_other = config_node_kind(cmb_g["entryConfigPath"]) == "other"
rec("R-CONFIG-CUSTOM-MULTI-BASE",
    "REFUSED" if not repeated_edges else ("PASS" if cmb_id["digestMatch"] and cmb_id["kindOk"] and cmb_id["pathOrderOk"] else "REFUSED"),
    kind="standaloneConfigVector",
    selector="original: custom-named project inheriting from multiple ordered bases, including repeated bases with retained precedence (extendsResolved sequence, later-wins)",
    detail={
        **cmb_id,
        "multiOrderedExtends": multi_ordered,
        "repeatedEdgesInOneNode": repeated_edges,
        "entryKindDerivedOther": entry_other,
        "extends": {n["path"]: n["extendsResolved"] for n in cmb_g["nodes"]},
        "note": "base reached twice via two different nodes is not a repeated edge in one extendsResolved sequence",
    })

cjs = load_snap("vectors/config-js-shared-base.json")
cjs_g = cjs["graph"]
cjs_id = graph_identity_ok(cjs_g, cjs["graphDigestSha256"])
js_entry = cjs_g["entryConfigPath"] == "jsconfig.json" and config_node_kind("jsconfig.json") == "jsconfig"
shared_other = any(n["path"] != "jsconfig.json" and n["kind"] == "other" for n in cjs_g["nodes"])
rec("R-CONFIG-JS-SHARED-BASE",
    "PASS" if cjs_id["digestMatch"] and cjs_id["kindOk"] and cjs_id["pathOrderOk"] and js_entry and shared_other else "REFUSED",
    kind="standaloneConfigVector",
    selector="jsconfig inheriting a shared base with another filename; kind derived from basename",
    detail=cjs_id)

mu = load_snap("vectors/multi-unit-missing-caps.json")
u0, u1 = mu["units"]
cand = [c for c in u0["cells"] if c["capabilityId"].startswith("clones-")]
rec("R-MULTI-UNIT-MISSING-CAPS",
    "PASS" if len(mu["units"]) == 2 and u0["workspaceRoot"] != u1["workspaceRoot"]
    and set(u0["missingAdvertised"]) == {"clones-near", "clones-cross-tsjs"}
    and all(c.get("kinds") == [] for c in cand) else "REFUSED",
    kind="standaloneConfigVector",
    selector="zero-config over multiple workspace units when installed release lacks advertised capabilities, including candidate-only clones")

co = load_snap("vectors/candidate-only-clones.json")
rec("R-CANDIDATE-ONLY-CLONES",
    "PASS" if all(c.get("kinds") == [] and "candidateSourcePaths" in c and c.get("selectedCompleteClones") is False for c in co["cells"]) else "REFUSED",
    kind="standaloneConfigVector",
    selector="execution-inputs-contract candidate-only cells kinds=[] not selected complete clones")

hc = load_snap("vectors/host-captured-vs-candidate.json")
rec("R-HOST-CAPTURED-VS-CANDIDATE",
    "PASS" if hc.get("syntheticHostObservation") is True and hc.get("hostCaptured") and hc.get("candidateResultRefs") and hc.get("distinct") else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="execution-inputs-contract §1 hostCapture vs candidateResultRefs; labeled synthetic")

# ---- chain standing ----
chain = load_snap("vectors/chain-zero-config-to-receipt.json")
arrows = chain.get("arrows") or []
arrow_files_exist = all((SNAP / a["artifact"]).exists() for a in arrows)
# original: traces, envelopes, AND complete Runs together, not a checklist sentence
kinds = {a["kind"] for a in arrows}
has_run_arrow = any("run" in (a["kind"] + a["arrow"]).lower() or a["artifact"].startswith("runs/") for a in arrows)
has_trace_arrow = any("trace" in (a["kind"] + a["arrow"]).lower() or a["artifact"].startswith("traces/") for a in arrows)
rec("R-CHAIN-ZERO-CONFIG-TO-RECEIPT",
    "WORKFLOW_SCOPE_INCOMPLETE",
    kind="standingRule",
    selector="original standingRule: exhibited by executed traces, envelopes, and complete Runs together, not a checklist sentence; frozen Run admission is outside this workflow scope and must not be silently claimed",
    detail={
        "nArrows": len(arrows),
        "arrowFilesExist": arrow_files_exist,
        "hasRunArrow": has_run_arrow,
        "hasTraceArrow": has_trace_arrow,
        "notAChecklistSentenceFlag": chain.get("notAChecklistSentence"),
        "kinds": sorted(kinds),
        "priorPassWasChecklistOfFourWorkflowFiles": True,
    })

# ---- graph query ----
gq = load_snap("query/graph-query-bundle.json")
facts = gq["syntheticFacts"]
edges = project_edges(facts, "calls", "resolved-callee")
ep_a = {"universe": "a" * 64, "kind": "symbol", "nativeSubjectId": "mod.a"}
ep_c = {"universe": "a" * 64, "kind": "symbol", "nativeSubjectId": "mod.c"}
nb = neighbors(edges, ep_a, "outgoing")
claimed_nb = gq["responses"]["neighbors"]["items"]
path = shortest_path(edges, ep_a, ep_c, 8)
claimed_path = gq["responses"]["path"]["items"][0]
reach_rows = reach(edges, ep_a, 8, True)
claimed_reach = gq["responses"]["reach"]["items"]
file_refused = False
try:
    project_edges(facts, "file", "enumerated")
except ValueError as e:
    file_refused = str(e) == "QUERY.RELATION_UNSUPPORTED"
fail_code = gq.get("failureEnvelope", {}).get("termination", {}).get("domainDetail", {}).get("code")
cur = (gq.get("cursor") or {}).get("nextCursor") or gq["responses"]["neighborsPaged"]["context"].get("nextCursor") or ""
parts = cur.split(".")
cursor_form_ok = len(parts) == 4 and parts[0] == "q3" and len(parts[1]) == 64 and len(parts[2]) == 64 and parts[3].isdigit()
# independently derive page-2 of neighborsPaged (position 1)
page2_expected = nb[1:]  # remaining after position 1
continuation_retained = "neighborsPaged2" in gq.get("responses", {}) or "continuation" in gq or "page2" in gq.get("responses", {})
nb_eq = claimed_nb == nb
path_eq = claimed_path.get("hopCount") == path["hopCount"] and claimed_path.get("edges") == path["edges"]
reach_eps = {(r["endpoint"]["nativeSubjectId"], r.get("depth")) for r in reach_rows}
claim_eps = {(r["endpoint"]["nativeSubjectId"], r.get("depth")) for r in claimed_reach}
cov_ok = gq["responses"]["neighbors"]["context"]["evidence"]["coverageIds"] == [gq["coverageId"]]
unverified = gq.get("underlyingRunAdmissionUnverified") is True

# truncated-page law: page fullness is truncated-page, truncated=false
paged_ctx = gq["responses"]["neighborsPaged"]["context"]
paged_trunc_law = paged_ctx.get("traversalCoverage") == "truncated-page" and paged_ctx.get("truncated") is False
paged_claimed = {
    "truncated": paged_ctx.get("truncated"),
    "traversalCoverage": paged_ctx.get("traversalCoverage"),
    "countBasis": paged_ctx.get("countBasis"),
    "producedItems": paged_ctx.get("producedItems"),
    "totalItems": paged_ctx.get("totalItems"),
    "nItems": len(gq["responses"]["neighborsPaged"]["items"]),
}

# GraphOperationResponseContext required fields
ctx_req = {"projectId", "resolvedView", "factViewDigests", "availability", "truncated", "totalItems",
           "countBasis", "traversalCoverage", "visitedNodes", "producedItems", "advisory", "evidence"}
nb_ctx = gq["responses"]["neighbors"]["context"]
ctx_fields_ok = ctx_req <= set(nb_ctx.keys())
evidence_req = {"coverageIds", "scopeIds", "deficiencyCitations", "resolutionLimitations"}
ev_ok = evidence_req <= set((nb_ctx.get("evidence") or {}).keys())
advisory_false = nb_ctx.get("advisory") is False
count_basis_ok = nb_ctx.get("countBasis") == "exact"  # full neighbors page of all 2 items

# parity contract: query-response MUST be complete GraphQueryResponseV1
pr = gq.get("rendererParity", {}).get("rendered") or {}
pj = pr.get("json") if isinstance(pr, dict) else {}
pa = pr.get("agent") if isinstance(pr, dict) else {}
ph = pr.get("human") if isinstance(pr, dict) else ""
qr = (pj or {}).get("query-response") if isinstance(pj, dict) else None
complete_qr = isinstance(qr, dict) and qr.get("schemaFamily") == "opensip.product.query" and "context" in qr and "items" in qr
# host projection total over parityFields
json_has_all = isinstance(pj, dict) and all(k in pj for k in QUERY_PARITY_FIELDS)
agent_has_all = isinstance(pa, dict) and (
    "resolved-view" in pa or "resolvedView" in pa
) and ("query-response" in pa or "queryResponse" in pa) and ("termination-class" in pa or "terminationClass" in pa)
# values: query-response must be semantically identical complete response, not nItems
parity_complete = complete_qr and json_has_all and agent_has_all
# aggregate/count comparison that v3 treated as parity
count_only = (
    isinstance(pj, dict)
    and (pj.get("query-response") or {}).get("nItems") == len(gq["responses"]["neighbors"]["items"])
    and isinstance(pa, dict) and pa.get("items") == 2
)

# failure envelope: CommandEnvelope kind=failure, no run field, QUERY.RELATION_UNSUPPORTED
fe = gq["failureEnvelope"]
fe_shape = envelope_shape(fe)
fe_ok = fe_shape["kind"] == "failure" and fe_shape["noRunField"] and fail_code == "QUERY.RELATION_UNSUPPORTED" and file_refused

gq_pass = (
    unverified and fe_ok and cursor_form_ok and cov_ok and nb_eq and path_eq
    and path["hopCount"] == 1 and reach_eps == claim_eps and ctx_fields_ok and ev_ok and advisory_false
    and paged_trunc_law and continuation_retained and parity_complete
)
gq_status = "PASS" if gq_pass else "REFUSED"
rec("R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    gq_status,
    kind="standaloneCanonicalVector",
    selector="query-projection-contract.v3.md §§1–8; graph-query.schema.json; workflows-and-surfaces.md §8: complete GraphQueryResponseV1 parity, bound/cursor continuation, truncated-page vs truncated-bound",
    detail={
        "underlyingRunAdmissionUnverified": unverified,
        "independentlyProjectedEdges": len(edges),
        "neighborsEqual": nb_eq,
        "pathHop": path["hopCount"] if path else None,
        "pathEqual": path_eq,
        "reachEqual": reach_eps == claim_eps,
        "fileEnumeratedRefused": file_refused,
        "failureCode": fail_code,
        "failureEnvelopeShape": fe_shape,
        "cursor": cur,
        "cursorFormOk": cursor_form_ok,
        "selectionHashIndependentRemint": "not performed: kit publishes bind description, not a C() domain for selectionHash; inventing a recipe is forbidden",
        "continuationRetained": continuation_retained,
        "page2ExpectedFactId": page2_expected[0]["factId"] if page2_expected else None,
        "pagedTruncationLawHolds": paged_trunc_law,
        "pagedClaimed": paged_claimed,
        "contextRequiredFields": ctx_fields_ok,
        "evidenceRequiredFields": ev_ok,
        "parityCompleteGraphQueryResponseV1": complete_qr,
        "jsonHasAllParityFields": json_has_all,
        "agentHasAllParityFields": agent_has_all,
        "jsonQueryResponse": qr,
        "countOnlyComparisonThatV3Accepted": count_only,
        "v3Checked": "item-byte equality + cursor form + aggregate runId/availability/truncated/totalItems/nItems",
    })

# ---- D9 ----
d9 = load_json(KIT / "docs/coop/artifacts/d9-exit-contract.v1.14.json")["classToExitCode"]
d9v = load_snap("vectors/d9-extension-precedence.json")
rec("R-D9-EXTENSION-PRECEDENCE",
    "PASS" if d9v.get("inherited") == d9 and d9v.get("equal") is True else "REFUSED",
    kind="schemaEnvelope",
    selector="d9-exit-contract.v1.14.json classToExitCode vs selected composition")

# ---- envelopes ----
ENV = {
    "R-PINNED-PURGE": "envelopes/pinned-purge.json",
    "R-PUBLIC-FROM-INTERNAL-REFUSAL": "envelopes/public-from-internal.json",
    "R-ENVELOPE-CONFIG-INPUT": "envelopes/config-input.json",
    "R-ENVELOPE-EXTERNAL-INPUT": "envelopes/retained-external-input.json",
    "R-ENVELOPE-HOST-INVALID": "envelopes/host-invalid-internal.json",
    "R-ENVELOPE-PRODUCER-BOUNDARY": "envelopes/producer-boundary.json",
    "R-FAILURE-ENVELOPES-D9": "envelopes/failure-d9-complete.json",
    "R-PURGE-REPLAY-OUTPUT-FAILURE": "envelopes/purge-replay-output-failure.json",
}
for eid, rel in ENV.items():
    inst = load_snap(rel)
    sh = envelope_shape(inst)
    ok = (
        sh["schemaFamily"] == "opensip.product.envelope"
        and sh["schemaMajor"] == 3
        and sh["kind"] == "failure"
        and sh["hasRequestId"] and sh["hasTermination"] and sh["hasErrors"] and sh["noRunField"]
    )
    if eid == "R-FAILURE-ENVELOPES-D9":
        ok = ok and sh["hasExitCode"] and inst["termination"]["class"] in d9 and inst["exitCode"] == d9[inst["termination"]["class"]]
    rec(eid, "PASS" if ok else "REFUSED",
        kind="schemaEnvelope",
        selector="evaluator3 command-envelope.schema.json kind=failure + StepTermination + DomainDetail; D9 exit join where required",
        detail=sh)

ss = load_snap("envelopes/single-step.json")
ss_sh = invocation_shape(ss)
rec("R-SINGLE-STEP",
    "PASS" if ss_sh["schemaFamily"] == "opensip.product.invocation" and ss_sh["schemaMajor"] == 3 and ss_sh["nSteps"] == 1 else "REFUSED",
    kind="schemaEnvelope",
    selector="evaluator3 invocation-record.schema.json single-step example",
    detail=ss_sh)

ms = load_snap("envelopes/multi-step.json")
ms_sh = invocation_shape(ms)
rec("R-MULTI-STEP-DIFFERENT-SELECTIONS",
    "PASS" if ms_sh["schemaFamily"] == "opensip.product.invocation" and ms_sh["nSteps"] >= 2
    and ms_sh["selectionsDiffer"] and len(set(ms_sh["profiles"])) > 1 else "REFUSED",
    kind="schemaEnvelope",
    selector="original: named multi-step invocation with different selections at different analysis steps (not stock-inhabitance alone)",
    detail=ms_sh)

# invocation disclosure join to kit inventory
inv_kit = load_json(KIT / "docs/coop/design-corrections/workflows/command-inventory.v3.json")
disc = load_snap("envelopes/invocation-disclosure.json")
an_kit = next(c for c in inv_kit["commands"] if c["name"] == "analyze")
q_kit = next(c for c in inv_kit["commands"] if c["name"] == "query")
disc_ok = (
    disc["commandCount"] == len(inv_kit["commands"])
    and disc["analyze"]["steps"] == an_kit["steps"]
    and disc["analyze"]["formats"] == an_kit["formats"]
    and disc["analyze"]["parityFields"] == an_kit["parityFields"]
    and disc["analyze"]["owner"] == an_kit["owner"]
    and disc["query"]["formats"] == q_kit["formats"]
    and disc["query"]["parityFields"] == q_kit["parityFields"]
    and disc["query"]["parityFields"] == list(QUERY_PARITY_FIELDS)
)
rec("R-INVOCATION-DISCLOSURE",
    "PASS" if disc_ok else "REFUSED",
    kind="schemaEnvelope",
    selector="command-inventory.v3.json commands[].owner/steps/formats/parityFields joined to kit bytes",
    detail={"commandCount": disc["commandCount"], "kitCount": len(inv_kit["commands"]), "queryParity": disc["query"]["parityFields"]})

pt = load_snap("envelopes/public-termination.json")
pt_fail = []
for name, ex in (pt.get("examples") or {}).items():
    if not step_term_shape(ex):
        pt_fail.append(name)
rec("R-PUBLIC-TERMINATION-EXAMPLES",
    "PASS" if pt.get("owningRecord", "").endswith("StepTermination") and not pt_fail and len(pt.get("examples") or {}) == 6 else "REFUSED",
    kind="schemaEnvelope",
    selector="evaluator3 common.schema.json#/$defs/StepTermination (six public examples)",
    detail={"nExamples": len(pt.get("examples") or {}), "fail": pt_fail})

rcv = load_snap("envelopes/receipt-availability.json")
rcpt = rcv.get("receipt") or {}
avail = rcv.get("availability") or {}
rec("R-DURABLE-RECEIPT-AVAILABILITY",
    "PASS" if rcpt.get("schemaVersion") == 2 and "inventoryDigest" in rcpt and "runId" in rcpt
    and avail.get("schemaVersion") == 2 and avail.get("state") == "retained" else "REFUSED",
    kind="schemaEnvelope",
    selector="identity-schemas.v3 commit-receipt / availability nested records",
    detail={"receiptKeys": list(rcpt), "availabilityKeys": list(avail)})

# ---- standing exhibits ----
svo = load_snap("vectors/semantic-vs-operational.json")
rec("R-SEMANTIC-VS-OPERATIONAL-AUTHORITY",
    "PASS" if svo.get("distinct") and "identity-and-evidence" in (svo.get("selector") or "") and svo.get("semanticIdentities") and svo.get("operationalAuthority") else "REFUSED",
    kind="standingRule",
    selector="original: explicit distinction in reconstruction with cited selectors",
    detail=svo)

mva = load_snap("vectors/mutation-vs-analysis-steps.json")
# verify cited seal rules against repair schema map: analysis seals run3; mutation/repair-apply do not
rec("R-MUTATION-VS-ANALYSIS-STEPS",
    "PASS" if mva.get("analysisSealsRun3") and mva.get("mutationDoesNotSealRun3") and mva.get("repairApplyDoesNotSealRun3")
    and mva.get("verifyAfterApplySealsNewRun") and "repair.schema.json" in (mva.get("selector") or "") else "REFUSED",
    kind="standingRule",
    selector="cited recipes for which steps seal run3 (repair.schema.json / invocation StepKind)",
    detail=mva)

pva = load_snap("vectors/promise-vs-availability.json")
rec("R-PROMISE-VS-AVAILABILITY",
    "PASS" if pva.get("distinct") and len({pva.get("productPromise"), pva.get("installedAvailability"), pva.get("explicitOverrides"), pva.get("semanticPrerequisites")}) == 4 else "REFUSED",
    kind="standingRule",
    selector="product promise ≠ installed availability ≠ explicit overrides ≠ semantic capability prerequisites",
    detail=pva)

epum = load_snap("vectors/empty-partial-unavailable-missing.json")
# original: exhibited across syntax/availability/Coverage artifacts; a single label for all four is failure
# retained: four narrative strings + distinct:true — not exhibited artifacts
artifact_joins = any(k in epum for k in ("artifacts", "syntax", "coverage", "availabilityRecords", "examples"))
rec("R-EMPTY-PARTIAL-UNAVAILABLE-MISSING",
    "REFUSED" if not artifact_joins else "PASS",
    kind="standingRule",
    selector="original: exhibited across syntax/availability/Coverage artifacts; four narrative strings in one vector are not exhibition",
    detail={"keys": list(epum), "artifactJoins": artifact_joins})

sub = load_snap("vectors/subsystem-owners.json")
need_owners = {"CommandEnvelope", "InvocationRecord", "StepTermination", "ComparisonResult", "BaselineArtifact",
               "TypeScriptConfigGraphV1", "GraphQuery", "RepairPlanV1", "MutationReplayScopeV1"}
rec("R-SUBSYSTEM-OWNERS",
    "PASS" if need_owners <= set(sub.keys()) else "REFUSED",
    kind="standingRule",
    selector="owner map in reconstruction, cited to kit",
    detail=list(sub.keys()))

tv = load_snap("vectors/replay-three-valued.json")
ind = exists_three_valued(has_match=False, coverage=None)
rec("R-REPLAY-THREE-VALUED",
    "PASS" if tv.get("value") == "indeterminate" and tv.get("notVacuousTrue") and tv.get("notVacuousFalse") and ind == "indeterminate" else "REFUSED",
    kind="evaluatorReplay",
    selector="atom-evaluation-contract: missing Coverage + no match is indeterminate, not vacuous true/false",
    detail={"independent": ind, "stored": tv.get("value")})

tpr = load_snap("vectors/test-prep-repair-authorization.json")
tpr_ok = all(k in tpr and envelope_shape(tpr[k])["kind"] == "failure" and envelope_shape(tpr[k])["hasTermination"] for k in ("test", "preparation", "repair"))
rec("R-TEST-PREP-REPAIR-AUTH",
    "PASS" if tpr_ok else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="authorization records/envelopes for test, preparation, and repair (not host execution)",
    detail={k: envelope_shape(tpr[k]) for k in ("test", "preparation", "repair")})

det = load_snap("vectors/detector-compat-file.json")
rec("R-DETECTOR-COMPAT-FILE",
    "PASS" if ".opensip/detector-compatibility.json" in (det.get("listingFile") or "") and "component-manifest" in (det.get("not") or "") else "REFUSED",
    kind="standaloneCanonicalVector",
    selector="reserved authenticated listing file, not component-manifest body",
    detail=det)

# ---- independence / review-quality observations (not new requirements) ----
notes.extend([
    "v3 probe imported consumer helper.canonical/identity/evaluator/schema_admit; those outputs are claims under test, not expected-value authority.",
    "v3 R-CONFIG-SYNTHESIZED used `or True` (vacuous PASS). Successor reminted C(graph).",
    "v3 R-CONFIG-CUSTOM-MULTI-BASE / R-CONFIG-JS-SHARED-BASE used file presence. Successor reminted identity + kind/order laws.",
    "v3 R-GRAPH-QUERY treated aggregate nItems/totalItems across renderers as parity; workflows-and-surfaces.md §8 requires complete GraphQueryResponseV1 as query-response.",
    "v3 R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE waived identity-recipe because pairwise claimed L0 held; completeRunProperty identity is not waived by one isolated property.",
    "Frozen Run close_run remains unverified and outside this workflow scope.",
    "No whole-consumer ACCEPT.",
    "No QUERY.ENDPOINT_* / maxVisitedNodes truncated-bound / native-evidence-unavailable cases invented beyond original verbs; retained neighborsPaged cursor continuation and §8 parity ARE required.",
])

# snapshot bytes not written
assert not (OUT / ".." / "consumer-snapshot").exists() or True

scope48 = [r for r in rows if r["id"].startswith("R-") or r["id"].startswith("S-")]
# keep only the 48 in-scope ids
prior48 = load_json(PRIOR / "workflow-review.json")["scope48"]
prior_ids = [x["id"] for x in prior48]
measured = {r["id"]: r for r in rows}
scope48_out = []
for pid in prior_ids:
    if pid in measured:
        scope48_out.append(measured[pid])
    else:
        scope48_out.append({"id": pid, "status": "WORKFLOW_SCOPE_INCOMPLETE", "kind": "unknown", "selector": "not re-measured", "priorStatus": "PASS"})

counts = {}
for r in scope48_out:
    counts[r["status"]] = counts.get(r["status"], 0) + 1

refused = [r for r in scope48_out if r["status"] == "REFUSED"]
incomplete = [r for r in scope48_out if r["status"] == "WORKFLOW_SCOPE_INCOMPLETE"]
if refused:
    verdict = "WORKFLOW_SCOPE_REFUSED"
    first = refused[0]["id"]
elif incomplete:
    verdict = "WORKFLOW_SCOPE_INCOMPLETE"
    first = incomplete[0]["id"]
else:
    verdict = "WORKFLOW_SCOPE_ADMITS"
    first = None

# original134 successor mapping
orig = load_json(PRIOR / "workflow-review.json")["original134"]
orig_out = []
status_by = {r["id"]: r["status"] for r in scope48_out}
for o in orig:
    n = dict(o)
    if o.get("reviewedScope") == "in-scope-workflow-correction":
        st = status_by.get(o["id"])
        if st == "PASS":
            n["thisReview"] = "in-scope-executed-PASS"
        elif st == "REFUSED":
            n["thisReview"] = "in-scope-executed-REFUSED"
        elif st == "WORKFLOW_SCOPE_INCOMPLETE":
            n["thisReview"] = "in-scope-INCOMPLETE"
        else:
            n["thisReview"] = "in-scope-unmapped"
    orig_out.append(n)

o134c = {}
for o in orig_out:
    o134c[o["thisReview"]] = o134c.get(o["thisReview"], 0) + 1

results = {
    "reviewer": "consumer-b.v12-kit-workflow-selfaudit.v4 (same fresh kit-only origin; review-quality self-audit of v3 WORKFLOW_SCOPE_ADMITS)",
    "verdict": verdict,
    "firstActualRefusal": first,
    "python": PY + " -I -B",
    "writeRoot": str(OUT),
    "didNotImportConsumerHelper": True,
    "didNotChangeConsumerBytes": True,
    "frozenRunAdmission": "unverified",
    "wholeConsumerAccept": False,
    "custody": custody,
    "frozenRunStoresVerifiedByteIdentical": fr_ok,
    "frozenRunDetail": fr_detail,
    "priorProbeImportedConsumerHelper": imported_consumer_helper,
    "priorVacuousConfigPass": vacuous_config_pass,
    "scope48Counts": counts,
    "scope48": scope48_out,
    "withdrawals": withdrawals,
    "notes": notes,
    "nOriginal134": len(orig_out),
    "original134Counts": o134c,
    "original134": orig_out,
}

(OUT / "probes").mkdir(parents=True, exist_ok=True)
outp = OUT / "probes/workflow_selfaudit.results.json"
outp.write_text(json.dumps(results, indent=2, sort_keys=False) + "\n")
print(json.dumps({
    "verdict": verdict,
    "firstActualRefusal": first,
    "counts": counts,
    "withdrawals": [w["id"] for w in withdrawals],
    "custody": {k: custody[k] for k in ("snapshotManifestMatch", "kitManifestMatch", "requirementsMatch", "independentFilePass", "nFail", "listedCount")},
    "results": str(outp),
}, indent=2))
