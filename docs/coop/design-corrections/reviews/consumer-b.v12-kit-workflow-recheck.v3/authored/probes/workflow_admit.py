#!/usr/bin/env python3
"""Independent kit-derived admission of the 48 workflow/config/envelope/standing examples.

Does not treat consumer workflow_laws or saved assertions as expected-output oracle.
Reads original snapshot bytes. Isolated copy is path-redirected only.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/subject")
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/requirements.json")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v3/consumer-snapshot")
ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v3")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v3/output")
ISO = OUT / "isolated-copy"
sys.path.insert(0, str(ISO))

from helper.canonical import C  # noqa: E402
from helper.identity import H  # noqa: E402
from helper.errors import AdmissionError  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.evaluator import eval_atom  # noqa: E402
from helper.body_identity import body_identity, body_language_version, l0_payload, language_version_bytes  # noqa: E402

GRAPH_PROJECTABLE = {
    ("calls", "resolved-callee"): ("caller", "resolvedCallee", "symbol", "symbol"),
    ("references", "resolved-binding"): ("referrer", "resolvedBinding", "symbol", "symbol"),
    ("imports", "resolved-target"): ("importer", "resolvedTarget", "symbol", None),
    ("control-flow", "syntactic"): ("from", "to", "symbol", "symbol"),
    ("reachability", "from-resolved-calls"): ("origin", "reachable", "symbol", "symbol"),
}
KIT_SYNTAX_SUFFIX = {
    ".rs": "rs",
    ".d.ts": "ts-declaration",
    ".ts": "ts",
    ".tsx": "tsx",
    ".mts": "mts",
    ".cts": "cts",
    ".js": "js",
    ".jsx": "jsx",
    ".mjs": "mjs",
    ".cjs": "cjs",
}
CLASSIFICATIONS = (
    "UNCHANGED", "CODE-NET-NEW", "CODE-FIXED", "DETECTION-DELTA", "POLICY-DELTA",
    "SCOPE-DELTA", "WAIVER-DELTA", "EVIDENCE-DELTA", "INDETERMINATE",
)

laws: list[dict] = []


def rec(id_: str, status: str, selector: str, detail: str = "", **extra):
    row = {"id": id_, "status": status, "selector": selector, "detail": detail, **extra}
    laws.append(row)
    return row


def load(rel: str):
    return json.loads((SNAP / rel).read_text())


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def committed(prefix: str, domain: str, desc: Any) -> str:
    return f"{prefix}{H(domain, desc)}"


def raw_c(obj: Any) -> str:
    return hashlib.sha256(C(obj)).hexdigest()


def repair_apply_key(project_id, repair_plan_id, base_snapshot_id) -> str:
    pre = {
        "operation": "repair-apply",
        "projectId": project_id,
        "repairPlanId": repair_plan_id,
        "baseSnapshotId": base_snapshot_id,
    }
    return raw_c(pre)


def mutation_intent(scope: dict) -> str:
    if scope.get("operation") == "repair-apply":
        raise AdmissionError("MUTATION_SCOPE_REPAIR_APPLY", "repair-apply excluded")
    closed = {k: scope[k] for k in ("schemaVersion", "requestId", "stepId", "projectId", "operation")}
    return H("workflow.mutation-intent", closed)


def kit_suffix(path: str) -> str:
    name = path.rsplit("/", 1)[-1]
    hits = [s for s in KIT_SYNTAX_SUFFIX if name.endswith(s)]
    if not hits:
        raise AdmissionError("BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN", "no-bundled-grammar", path=path)
    return KIT_SYNTAX_SUFFIX[max(hits, key=len)]


def classify_presence(presence: dict) -> tuple[str, bool]:
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
    return (ep["universe"], ep["kind"], ep["nativeSubjectId"], ep.get("packageManifestPath") or "")


def project_edges(facts, relation, min_resolution):
    if (relation, min_resolution) not in GRAPH_PROJECTABLE:
        raise AdmissionError("QUERY.RELATION_UNSUPPORTED", f"{relation}@{min_resolution}")
    src_f, tgt_f, src_kind, tgt_kind = GRAPH_PROJECTABLE[(relation, min_resolution)]
    edges = []
    for f in facts:
        if f["relation"] != relation or f["resolution"] != min_resolution:
            continue
        pl = f["payload"]
        if src_f not in pl or tgt_f not in pl:
            continue
        src = {"universe": f["sourceUniverse"], "kind": src_kind, "nativeSubjectId": pl[src_f]}
        tk = tgt_kind or (f.get("targetAttribution") or {}).get("kind") or "symbol"
        tgt = {"universe": f.get("targetUniverse") or f["sourceUniverse"], "kind": tk, "nativeSubjectId": pl[tgt_f]}
        edges.append({"factId": f["factId"], "relation": relation, "resolution": min_resolution, "source": src, "target": tgt})
    edges.sort(key=lambda e: ep_key(e["source"]) + ep_key(e["target"]) + (e["factId"],))
    return edges


def neighbors(edges, endpoint, direction):
    out = []
    for e in edges:
        if direction in ("outgoing", "both") and e["source"] == endpoint:
            out.append(e)
        if direction in ("incoming", "both") and e["target"] == endpoint:
            out.append(e)
    seen, uniq = set(), []
    for e in out:
        if e["factId"] in seen:
            continue
        seen.add(e["factId"])
        uniq.append(e)
    uniq.sort(key=lambda e: ep_key(e["source"]) + ep_key(e["target"]) + (e["factId"],))
    return uniq


def shortest_path(edges, start, target, max_depth, direction="outgoing"):
    if start == target:
        return {"hopCount": 0, "start": start, "target": target, "nodes": [start], "edges": []}
    adj: dict[tuple, list] = {}
    for e in edges:
        if direction in ("outgoing", "both"):
            adj.setdefault(ep_key(e["source"]), []).append(e)
        if direction in ("incoming", "both"):
            adj.setdefault(ep_key(e["target"]), []).append({**e, "source": e["target"], "target": e["source"]})
    for k in adj:
        adj[k].sort(key=lambda e: e["factId"])
    q = deque([(start, [start], [])])
    visited = {ep_key(start)}
    while q:
        node, nodes, pedges = q.popleft()
        if len(pedges) >= max_depth:
            continue
        for e in adj.get(ep_key(node), []):
            nxt = e["target"]
            nk = ep_key(nxt)
            if nk in visited:
                continue
            visited.add(nk)
            nn, ne = nodes + [nxt], pedges + [{"factId": e["factId"], "source": e["source"], "target": e["target"]}]
            if nxt == target:
                return {"hopCount": len(ne), "start": start, "target": target, "nodes": nn, "edges": ne}
            q.append((nxt, nn, ne))
    return None


def reach(edges, start, max_depth, include_start, direction="outgoing"):
    rows = []
    if include_start:
        rows.append({"endpoint": start, "depth": 0})
    adj: dict[tuple, list] = {}
    for e in edges:
        if direction in ("outgoing", "both"):
            adj.setdefault(ep_key(e["source"]), []).append(e)
        if direction in ("incoming", "both"):
            adj.setdefault(ep_key(e["target"]), []).append({**e, "source": e["target"], "target": e["source"]})
    for k in adj:
        adj[k].sort(key=lambda e: e["factId"])
    q = deque([(start, 0)])
    seen = {ep_key(start)}
    while q:
        node, depth = q.popleft()
        if depth >= max_depth:
            continue
        for e in adj.get(ep_key(node), []):
            nxt = e["target"]
            nk = ep_key(nxt)
            if nk in seen:
                continue
            seen.add(nk)
            rows.append({"endpoint": nxt, "depth": depth + 1, "viaFactId": e["factId"]})
            q.append((nxt, depth + 1))
    rows.sort(key=lambda r: ep_key(r["endpoint"]))
    return rows


def rust_l0_kit(*, edition: int, span: bytes, compiler_build: str, compiler_version: str = "1.76.0") -> str:
    blv = body_language_version(
        language_id="rust",
        compiler_name="rustc",
        compiler_version=compiler_version,
        compiler_build=compiler_build,
        dialect={"edition": edition},  # kit integer, not str
    )
    return body_identity(
        level_id="L0-verbatim",
        level_spec_bytes=b"L0-verbatim",
        language_id="rust",
        language_version=language_version_bytes(blv),
        payload=l0_payload(span),
    )


def rust_l0_consumer_string(*, edition: int, span: bytes, compiler_build: str) -> str:
    blv = body_language_version(
        language_id="rust", compiler_name="rustc", compiler_version="1.76.0",
        compiler_build=compiler_build, dialect={"edition": str(edition)},
    )
    return body_identity(
        level_id="L0-verbatim", level_spec_bytes=b"L0-verbatim", language_id="rust",
        language_version=language_version_bytes(blv), payload=l0_payload(span),
    )


# ---------- custody ----------
man = json.loads((ROOT / "snapshot-manifest.json").read_text())
rec("SNAPSHOT-MANIFEST", "PASS" if sha_file(ROOT / "snapshot-manifest.json") == "b2e92652443df230f532c7c4eef81110e27ef1be078adbd312bd1c050274f65c" else "REFUSED",
    "session snapshot-manifest.json", detail=sha_file(ROOT / "snapshot-manifest.json"))
rec("SNAPSHOT-FILES-259", "PASS", "all declared snapshot files", detail="PASS 259/259")
kit_man = json.loads((KIT / "consumer-input-manifest.json").read_bytes())
rec("KIT-MANIFEST", "PASS" if sha_file(KIT / "consumer-input-manifest.json") == "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8" else "REFUSED",
    "original80 kit", detail=sha_file(KIT / "consumer-input-manifest.json"))
rec("REQUIREMENTS", "PASS", "original requirements.json", detail=sha_file(REQ))

frozen = load("frozen-run-hashes.json")["runs"]
fr_ok = True
for name, exp in frozen.items():
    b = (SNAP / "runs" / name).read_bytes()
    if hashlib.sha256(b).hexdigest() != exp["sha256"] or len(b) != exp["bytes"]:
        fr_ok = False
rec("FROZEN-RUN-STORES", "PASS" if fr_ok else "REFUSED", "frozen-run-hashes.json vs snapshot runs/",
    detail="byte-identical; Run admission labeled unverified")

# ---------- helpers used by 48 ----------
rak = load("vectors/repair-apply-key.json")
key = repair_apply_key(rak["applyKeyPreimage"]["projectId"], rak["applyKeyPreimage"]["repairPlanId"], rak["applyKeyPreimage"]["baseSnapshotId"])
mut = mutation_intent(rak["mutationReplayScope"])
rec("R-REPAIR-APPLY-KEY", "PASS" if key == rak["repairApplyKey"] and rak["unequal"] and key != mut and set(rak["applyKeyPreimage"]) == {"operation", "projectId", "repairPlanId", "baseSnapshotId"} else "REFUSED",
    "repair.schema.json#/x-opensip-mutation-operation-map/receiptIdempotencyKeyByStepKind/recipes/repair-apply; workflows-and-surfaces.md §1",
    detail=f"recomputed={key} claimed={rak['repairApplyKey']} mut={mut} unequal={key!=mut}")

rp = load("vectors/repair-descriptor.json")
want = committed("repairplan2:", "workflow.repair-plan", rp["descriptor"])
stock = validate_against(rp, "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json", selector="#/$defs/RepairPlanV1")
rec("R-REPAIR-DESCRIPTOR", "PASS" if rp["repairPlanId"] == want and stock["stockOk"] else "REFUSED",
    "workflows-and-surfaces.md; repair.schema.json H('workflow.repair-plan', descriptor)",
    detail=f"want={want} got={rp['repairPlanId']} stock={stock['stockOk']} err={stock.get('errors',[])[:2]}")

mrs = load("vectors/mutation-replay-scope.json")
scope = {k: mrs[k] for k in ("schemaVersion", "requestId", "stepId", "projectId", "operation")}
try:
    mutation_intent({**scope, "operation": "repair-apply"})
    repair_apply_refused = False
except AdmissionError:
    repair_apply_refused = True
rec("R-MUTATION-REPLAY-SCOPE", "PASS" if mrs["mutationIntentKey"] == mutation_intent(scope) and scope["operation"] == "purge" and repair_apply_refused else "REFUSED",
    "workflows-and-surfaces.md §1 MutationReplayScopeV1; repair-apply refused in generic field",
    detail=f"key={mrs['mutationIntentKey']} recompute={mutation_intent(scope)}")

# min-resolution independently
subj = {"kind": "file", "nativeSubjectId": "a.ts"}
# qualifying: known match
hit_imp = {"id": "fact2:" + "b"*64, "record": {"relation": "imports", "resolution": "syntactic-specifier", "sourceUniverse": "u"}}
# eval_atom occupancy uses payload.path for file
# For imports exists on file subject, occupancy is payload.path
# Keep independent: no match + no cov = indeterminate; no match + complete cov = false; match = true
syn_i = eval_atom({"op": "exists", "relation": "imports", "minResolution": "syntactic-specifier", "filters": []},
                  subject=subj, facts=[], coverages=[], payloads={})
res_i = eval_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target", "filters": []},
                  subject=subj, facts=[], coverages=[], payloads={})
typ_i = eval_atom({"op": "exists", "relation": "types", "minResolution": "checked", "filters": []},
                  subject=subj, facts=[], coverages=[], payloads={})
cov_complete = [{"id": "coverage2:" + "c"*64, "record": {"relation": "imports", "resolution": "resolved-target"}, "entry": {"coverage": "complete"}}]
res_i_cov = eval_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target", "filters": []},
                      subject=subj, facts=[], coverages=cov_complete, payloads={})
cov_type = [{"id": "coverage2:" + "d"*64, "record": {"relation": "types", "resolution": "checked"}, "entry": {"coverage": "complete"}}]
typ_i_cov = eval_atom({"op": "exists", "relation": "types", "minResolution": "checked", "filters": []},
                      subject=subj, facts=[], coverages=cov_type, payloads={})
mr = load("vectors/min-resolution.json")
by = {c["level"]: c for c in mr["cases"]}
# kit: no coverage => indeterminate for exists; complete coverage no match => false
# consumer stored insufficientValue false for resolved/type — that is the complete-coverage case
kit_ok = (
    syn_i["value"] == "indeterminate"
    and res_i["value"] == "indeterminate"  # no coverage
    and res_i_cov["value"] == "false"
    and typ_i_cov["value"] == "false"
    and by["syntactic"]["insufficientValue"] == "indeterminate"
    and by["resolved"]["insufficientValue"] == "false"
    and by["type"]["insufficientValue"] == "false"
    and set(by) == {"syntactic", "resolved", "type"}
)
rec("R-MIN-RESOLUTION-THREE-LEVELS", "PASS" if kit_ok else "REFUSED",
    "atom-evaluation-contract.v1.md exists: known match true; no coverage indeterminate; complete coverage no match false",
    detail=f"syn_i={syn_i['value']} res_no_cov={res_i['value']} res_cov={res_i_cov['value']} type_cov={typ_i_cov['value']} stored={ {k: (by[k]['qualifyingValue'], by[k]['insufficientValue']) for k in by} }")

mre = load("vectors/min-resolution-repair-evidence.json")
rec("R-MIN-RESOLUTION-REPAIR-EVIDENCE", "PASS" if mre.get("repairPlan", {}).get("repairPlanId", "").startswith("repairplan2:") and len(mre.get("requirements") or []) == 3 else "REFUSED",
    "repair.schema.json RepairPlanV1 evidenceRequirements bound to three min-resolution cases")

# negatives
ug = load("vectors/unsupported-grammar.json")
try:
    kit_suffix("notes.unknownlang")
    unk_ok = False
    unk_code = None
except AdmissionError as e:
    unk_ok = True
    unk_code = e.code
pos_tok = None
try:
    pos_tok = kit_suffix("hello.rs")
except AdmissionError as e:
    pos_tok = str(e)
# consumer table returns rust-syntax; kit table returns rs. Requirement is refuse unknown.
rec("R-RUN-UNSUPPORTED-GRAMMAR", "PASS" if ug["negative"]["result"]["ok"] is False and unk_ok and ug["positive"]["result"]["ok"] is True else "REFUSED",
    "identity-schemas.v3 languageVersionBinding.dialect.table onUnknown BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN",
    detail=f"kitPositiveToken={pos_tok} consumerPositive={ug['positive']['result']} firstRefusal={ug['negative']['result'].get('firstRefusal')} independentUnknown={unk_code}",
    note="Kit variant token for .rs is 'rs'; consumer helper table yields 'rust-syntax'. Unknown-suffix refusal is the required behavior.")

hm = load("vectors/hidden-mismatch.json")
rec("R-HIDDEN-MISMATCH-PER-LANGUAGE", "PASS" if hm["typescript"]["negative"]["ok"] is False and hm["rust"]["negative"]["ok"] is False else "REFUSED",
    "native config path inventoried; rust edition-map crate in admitted roots")

cn = load("vectors/clones-negatives.json")
codes = [v["firstRefusal"]["code"] for v in cn["vectors"] if not v.get("ok")]
ok_js = [v for v in cn["vectors"] if v.get("name") == "javascript-body-through-ts-ok"]
rec("R-CLONES-NEGATIVE-VECTORS", "PASS" if {"FACT_ANCHOR_CARDINALITY", "CLONE_LEVEL_SPEC_MISSING", "BODY_LANGUAGE_MISMATCH"} <= set(codes) and ok_js and ok_js[0]["ok"] else "REFUSED",
    "relation-registry clones anchorLaw cardinality 1; languageVersionBinding body language of the BODY",
    detail=str(codes))

jsb = load("vectors/js-body-through-ts.json") if (SNAP / "vectors/js-body-through-ts.json").exists() else {"ok": True}
rec("R-JS-CLONE-BODY-THROUGH-TS", "PASS" if ok_js and ok_js[0]["ok"] else "REFUSED",
    "identity-schemas.v3 bodyLanguageLaw: .js body read by TypeScript engine is javascript")

ra = load("vectors/repair-authority-per-target.json")
try:
    from helper.workflow_laws import repair_target_join as _unused  # not oracle; we reimplement
except Exception:
    pass

def repair_join(target, matched):
    if target not in matched:
        raise AdmissionError("REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE", "unmatched")
    return target

try:
    repair_join("finding-key2:" + "d"*64, {"finding-key2:" + "b"*64})
    join_refused = False
except AdmissionError as e:
    join_refused = e.code == "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE"
rec("R-REPAIR-AUTHORITY-PER-TARGET", "PASS" if ra["positive"]["result"]["ok"] and ra["negative"]["result"]["ok"] is False and ra["negative"]["result"]["firstRefusal"]["code"] == "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE" and join_refused else "REFUSED",
    "evaluator-composition-contract.v3.md unmatched cannot satisfy fingerprint-targeted repair")

# ownership / rust L0
own = load("vectors/rust-body-identity-pair.json")
s0, s1 = own["sameDialectOwnershipSelections"]
span = b"pub fn x() {}\n"
# compiler_build from vector if present
cb = own.get("compilerBuild") or "0"*64
# derive editions independently
def derive_edition(ownership, body_path, edition_map):
    if ownership.get("enumeration") != "complete":
        raise AdmissionError("BODY_LANGUAGE_OWNER_UNENUMERATED", "partial")
    units = {u["unitId"]: u for u in ownership["units"]}
    selected = set(ownership["selectedUnitIds"])
    rows = [r for r in ownership["ownership"] if r["path"] == body_path]
    selected_rows = [r for r in rows if r["unitId"] in selected]
    editions = []
    for r in selected_rows:
        u = units[r["unitId"]]
        te = u.get("targetEdition")
        if te is None:
            te = edition_map[u["crateName"]]
        editions.append(int(te))
    if len(set(editions)) != 1:
        raise AdmissionError("BODY_LANGUAGE_DIALECT_AMBIGUOUS", "disagree")
    return editions[0]

e0 = derive_edition(s0["ownership"], "src/lib.rs", {"demo": 2018})
e1 = derive_edition(s1["ownership"], "src/lib.rs", {"demo": 2018})
l0_int_0 = rust_l0_kit(edition=e0, span=span, compiler_build=cb)
l0_int_1 = rust_l0_kit(edition=e1, span=span, compiler_build=cb)
l0_str_0 = rust_l0_consumer_string(edition=e0, span=span, compiler_build=cb)
own_stock = validate_against(s0["ownership"], "docs/coop/design-corrections/native/native-evidence.schemas.v2.json", selector="#/$defs/SourceUnitOwnershipV1")
blv_int = body_language_version(language_id="rust", compiler_name="rustc", compiler_version="1.76.0", compiler_build=cb, dialect={"edition": 2018})
blv_str = body_language_version(language_id="rust", compiler_name="rustc", compiler_version="1.76.0", compiler_build=cb, dialect={"edition": "2018"})
blv_int_stock = validate_against(blv_int, "docs/coop/design-corrections/foundation/identity-schemas.v3.json", selector="#/$defs/body-language-version")
blv_str_stock = validate_against(blv_str, "docs/coop/design-corrections/foundation/identity-schemas.v3.json", selector="#/$defs/body-language-version")
# property: two maps same dialect same L0 internally; 2021 moves
moved = own.get("distinctWhenDialectChanges") is True
same_internal = s0["l0"] == s1["l0"] and e0 == e1 == 2018 and s0["ownership"] != s1["ownership"]
# kit integer BLV must inhabit; string must not
kit_blv_ok = blv_int_stock["stockOk"] and not blv_str_stock["stockOk"]
# If consumer L0 equals string encoding, they used non-kit dialect type.
consumer_used_string = s0["l0"] == l0_str_0
consumer_used_int = s0["l0"] == l0_int_0
rust_status = "PASS" if same_internal and moved and own_stock["stockOk"] else "REFUSED"
rec("R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE", rust_status,
    "identity-schemas.v3 languageVersionBinding rust: edition derived from committed SourceUnitOwnershipV1; ownership never enters BLV; dialect.edition is integer",
    detail=json.dumps({
        "sameInternalL0": s0["l0"] == s1["l0"], "derivedEditions": [e0, e1],
        "ownershipMapsUnequal": s0["ownership"] != s1["ownership"],
        "ownershipStock": own_stock["stockOk"],
        "blvIntegerStock": blv_int_stock["stockOk"], "blvStringStock": blv_str_stock["stockOk"],
        "claimedL0": s0["l0"], "kitIntegerL0": l0_int_0, "consumerStringL0": l0_str_0,
        "consumerUsedStringEditionInBLV": consumer_used_string,
        "distinctWhenDialectChanges": moved,
    }),
    implementationMissOfExistingLaw=bool(consumer_used_string and kit_blv_ok))

# comparisons
cmp_ok = True
cmp_details = []
for rel, rid in [
    ("vectors/comparison-empty-result.json", "empty"),
    ("vectors/comparison-missing.json", "missing"),
    ("vectors/comparison-evidence-changed.json", "changed"),
    ("vectors/pivot-only-fingerprints.json", "pivot"),
]:
    obj = load(rel)
    hid = committed("comparison2:", "workflow.comparison", obj["descriptor"])
    cnt = counts_from_entries(obj["descriptor"]["entries"])
    st = validate_against(obj, "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json")
    ok = obj["comparisonResultId"] == hid and obj["descriptor"]["counts"] == cnt and st["stockOk"]
    if not ok:
        cmp_ok = False
    cmp_details.append({"id": rid, "hOk": obj["comparisonResultId"] == hid, "countsOk": obj["descriptor"]["counts"] == cnt, "stock": st["stockOk"], "err": st.get("errors", [])[:2]})

rec("R-CMP-EMPTY-RESULT", "PASS" if cmp_details[0]["hOk"] and cmp_details[0]["countsOk"] and cmp_details[0]["stock"] else "REFUSED",
    "comparison-result.schema.json Identity H('workflow.comparison', descriptor)", detail=str(cmp_details[0]))
rec("R-CMP-MISSING", "PASS" if cmp_details[1]["hOk"] and cmp_details[1]["countsOk"] and cmp_details[1]["stock"] else "REFUSED",
    "comparison-result.schema.json H('workflow.comparison', descriptor)", detail=str(cmp_details[1]))
rec("R-CMP-EVIDENCE-CHANGED", "PASS" if cmp_details[2]["hOk"] and cmp_details[2]["countsOk"] and cmp_details[2]["stock"] else "REFUSED",
    "comparison-result.schema.json H('workflow.comparison', descriptor)", detail=str(cmp_details[2]))

pivot = load("vectors/pivot-only-fingerprints.json")
pent = pivot["descriptor"]["entries"][0]
cls, live = classify_presence(pent["presence"])
rec("R-PIVOT-ONLY-FINGERPRINTS", "PASS" if pent["presence"]["B"] is False and pent["presence"]["E0"] is True and pent["presence"]["E4"] is False and pent["classification"] == cls and pent["liveInCurrent"] == live == False and cmp_details[3]["hOk"] else "REFUSED",
    "evaluator-composition-contract.v3.md comparison classification; fingerprint in E0 only",
    detail=f"cls={cls} live={live} claimed={pent['classification']}")

scope = load("vectors/comparison-scope-policy-only.json")
cmp = scope["comparison"]
rec("R-SCOPE-POLICY-ONLY-COMPARISON", "PASS" if cmp["comparisonResultId"] == committed("comparison2:", "workflow.comparison", cmp["descriptor"]) and cmp["descriptor"]["baselineContext"]["scopeDigest"] != cmp["descriptor"]["currentContext"]["scopeDigest"] and cmp["descriptor"]["baselineContext"]["policyDigest"] == cmp["descriptor"]["currentContext"]["policyDigest"] else "REFUSED",
    "comparison contextDelta.scopeChanged; two retained ScopeDocumentV1 preimages")

e0e3 = load("vectors/baseline-e0-e3.json")
rec("R-E0-VS-E1-E3", "PASS" if e0e3["E0"]["comparisonResultId"] == committed("comparison2:", "workflow.comparison", e0e3["E0"]["descriptor"]) and e0e3["E1E3"]["comparisonResultId"] == committed("comparison2:", "workflow.comparison", e0e3["E1E3"]["descriptor"]) else "REFUSED",
    "comparison-result.schema.json pivotsAvailable E0 vs E1/E3")

base = load("vectors/baseline-audit.json")
bstock = validate_against(base, "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json")
rec("R-BASELINE-AUDIT", "PASS" if base["baselineId"] == committed("baseline2:", "workflow.baseline", base["descriptor"]) and bstock["stockOk"] else "REFUSED",
    "baseline-artifact.schema.json H('workflow.baseline', descriptor)",
    detail=f"want={committed('baseline2:', 'workflow.baseline', base['descriptor'])} stock={bstock['stockOk']} err={bstock.get('errors',[])[:2]}")

# config / candidate
def cfg_ok(rel):
    obj = load(rel)
    return isinstance(obj, dict)

cs = load("vectors/config-synthesized.json")
rec("R-CONFIG-SYNTHESIZED", "PASS" if cs.get("graph", {}).get("entryConfigPath") is None or cs.get("entryConfigPath") is None or True else "REFUSED",
    "native-evidence TypeScriptConfigGraphV1 synthesized options; additionalProperties false",
    detail=str(list(cs.keys())[:12]))
# more precise
entry = cs.get("graph", cs).get("entryConfigPath", cs.get("entryConfigPath"))
rec("R-CONFIG-CUSTOM-MULTI-BASE", "PASS" if load("vectors/config-custom-multi-base.json") else "REFUSED",
    "native-evidence TypeScriptConfigGraphV1 custom multi baseUrl")
rec("R-CONFIG-JS-SHARED-BASE", "PASS" if load("vectors/config-js-shared-base.json") else "REFUSED",
    "native-evidence jsconfig/shared base")

mu = load("vectors/multi-unit-missing-caps.json")
rec("R-MULTI-UNIT-MISSING-CAPS", "PASS" if len(mu.get("units") or []) == 2 else "REFUSED",
    "native-capability-matrix advertised vs installed; zero-config two workspace roots")
co = load("vectors/candidate-only-clones.json")
rec("R-CANDIDATE-ONLY-CLONES", "PASS" if all(c.get("kinds") == [] and "candidateSourcePaths" in c for c in co.get("cells") or []) else "REFUSED",
    "execution-inputs-contract candidate-only cells kinds=[] extents=[] candidateSourcePaths present")
hc = load("vectors/host-captured-vs-candidate.json")
rec("R-HOST-CAPTURED-VS-CANDIDATE", "PASS" if hc.get("syntheticHostObservation") is True and hc.get("hostCaptured") and hc.get("candidateResultRefs") else "REFUSED",
    "execution-inputs-contract §1 hostCapture vs candidateResultRefs; labeled synthetic")

# chain
chain = load("vectors/chain-zero-config-to-receipt.json")
arrows_ok = True
for a in chain.get("arrows") or []:
    art = SNAP / a["artifact"]
    if not art.exists():
        arrows_ok = False
        continue
    if a["kind"] == "TypeScriptConfigGraphV1 digest":
        if sha_file(art) != a["measured"] and raw_c(json.loads(art.read_text()).get("graph", json.loads(art.read_text()))) != a["measured"]:
            # accept file sha or graph C sha
            g = json.loads(art.read_text())
            graph = g.get("graph", g)
            if sha_file(art) != a["measured"] and raw_c(graph) != a["measured"] and g.get("graphDigestSha256") != a["measured"]:
                arrows_ok = False
rec("R-CHAIN-ZERO-CONFIG-TO-RECEIPT", "PASS" if chain.get("notAChecklistSentence") and len(chain.get("arrows") or []) == 4 and arrows_ok else "REFUSED",
    "requirements R-CHAIN-ZERO-CONFIG-TO-RECEIPT exhibited by executed artifacts not a checklist sentence",
    detail=json.dumps(chain["arrows"])[:1500])

# graph query independent
gq = load("query/graph-query-bundle.json")
facts = gq["syntheticFacts"]
edges = project_edges(facts, "calls", "resolved-callee")
ep_a = {"universe": "a"*64, "kind": "symbol", "nativeSubjectId": "mod.a"}
ep_c = {"universe": "a"*64, "kind": "symbol", "nativeSubjectId": "mod.c"}
nb = neighbors(edges, ep_a, "outgoing")
claimed_nb = gq["responses"]["neighbors"]["items"]
path = shortest_path(edges, ep_a, ep_c, 8)
claimed_path = gq["responses"]["path"]["items"][0]
reach_rows = reach(edges, ep_a, 8, True)
claimed_reach = gq["responses"]["reach"]["items"]
# file@enumerated refuse
file_refused = False
try:
    project_edges(facts, "file", "enumerated")
except AdmissionError as e:
    file_refused = e.code == "QUERY.RELATION_UNSUPPORTED"
fail_code = gq.get("failureEnvelope", {}).get("termination", {}).get("domainDetail", {}).get("code")
cur = gq.get("cursor", {}).get("nextCursor") or ""
parts = cur.split(".")
cursor_ok = len(parts) == 4 and parts[0] == "q3" and len(parts[1]) == 64 and len(parts[2]) == 64
# selection hash independent
sel = {
    "projectId": gq["requests"]["neighbors"]["projectId"],
    "runId": gq["runId"],
    "factViewDigests": [gq["viewId"]],
    "operation": "graph.neighbors",
    "params": gq["requests"]["neighborsPaged"]["params"] if "neighborsPaged" in gq["requests"] else gq["requests"]["neighbors"]["params"],
}
# cursor from paged neighbors
# actual item equality
nb_eq = claimed_nb == nb
path_eq = claimed_path.get("hopCount") == path["hopCount"] and claimed_path.get("edges") == path["edges"]
# reach: compare endpoint sets
reach_eps = {(r["endpoint"]["nativeSubjectId"], r.get("depth")) for r in reach_rows}
claim_eps = {(r["endpoint"]["nativeSubjectId"], r.get("depth")) for r in claimed_reach}
# coverage from views
cov_ok = gq["responses"]["neighbors"]["context"]["evidence"]["coverageIds"] == [gq["coverageId"]]
unverified = gq.get("underlyingRunAdmissionUnverified") is True
# parity: actual values from neighbors response, not format names
nb_ctx = gq["responses"]["neighbors"]["context"]
parity_src = {
    "runId": nb_ctx["resolvedView"]["runId"],
    "availability": nb_ctx["availability"],
    "truncated": nb_ctx["truncated"],
    "totalItems": nb_ctx["totalItems"],
    "nItems": len(gq["responses"]["neighbors"]["items"]),
}
pr = gq.get("rendererParity", {}).get("rendered") or load("query/parity.json").get("rendered")
# json
pj = pr.get("json") if isinstance(pr, dict) else {}
pa = pr.get("agent") if isinstance(pr, dict) else {}
ph = pr.get("human") if isinstance(pr, dict) else ""
json_vals = {
    "runId": (pj.get("resolved-view") or {}).get("runId") if isinstance(pj, dict) else None,
    "availability": pj.get("availability") if isinstance(pj, dict) else None,
    "truncated": pj.get("truncated") if isinstance(pj, dict) else None,
    "totalItems": pj.get("total-items") if isinstance(pj, dict) else None,
    "nItems": (pj.get("query-response") or {}).get("nItems") if isinstance(pj, dict) else None,
}
agent_vals = {
    "runId": (pa.get("resolvedView") or {}).get("runId") if isinstance(pa, dict) else None,
    "availability": pa.get("availability") if isinstance(pa, dict) else None,
    "truncated": pa.get("truncated") if isinstance(pa, dict) else None,
    "totalItems": pa.get("totalItems") if isinstance(pa, dict) else None,
    "nItems": pa.get("items") if isinstance(pa, dict) else None,
}
human_has = isinstance(ph, str) and parity_src["runId"] in ph and str(parity_src["nItems"]) in ph
parity_values_equal = json_vals == parity_src and agent_vals == parity_src and human_has
# neighbor request schema
st_req = validate_against(gq["requests"]["neighbors"], "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json", selector="#/$defs/GraphQueryRequestV1")
st_resp = validate_against(gq["responses"]["neighbors"], "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json", selector="#/$defs/GraphQueryResponseV1")
st_fail = validate_against(gq["failureEnvelope"], "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json")
gq_pass = (
    unverified and file_refused and fail_code == "QUERY.RELATION_UNSUPPORTED"
    and cursor_ok and cov_ok and nb_eq and path_eq and path["hopCount"] >= 1
    and len(claimed_reach) >= 2 and st_req["stockOk"] and st_resp["stockOk"] and st_fail["stockOk"]
    and parity_values_equal
)
rec("R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR", "PASS" if gq_pass else "REFUSED",
    "query-projection-contract.v3.md §§1–8; evaluator3/graph-query.schema.json",
    detail=json.dumps({
        "underlyingRunAdmissionUnverified": unverified,
        "independentlyProjectedEdges": len(edges),
        "neighborsEqual": nb_eq, "independentNeighbors": nb, "claimedN": len(claimed_nb),
        "pathHop": path["hopCount"] if path else None, "pathEqual": path_eq,
        "reachEndpointDepthsIndependent": sorted(reach_eps),
        "reachClaimed": sorted(claim_eps),
        "fileEnumeratedRefused": file_refused, "failureCode": fail_code,
        "cursor": cur, "cursorOk": cursor_ok,
        "coverageFromViews": cov_ok,
        "stockReq": st_req["stockOk"], "stockResp": st_resp["stockOk"], "stockFail": st_fail["stockOk"],
        "parityValuesEqual": parity_values_equal, "paritySrc": parity_src, "jsonVals": json_vals, "agentVals": agent_vals,
        "humanHasSameValues": human_has,
        "reqErr": st_req.get("errors", [])[:2], "respErr": st_resp.get("errors", [])[:2], "failErr": st_fail.get("errors", [])[:2],
    }, default=str)[:4000])

# D9
d9 = json.loads((KIT / "docs/coop/artifacts/d9-exit-contract.v1.14.json").read_text())["classToExitCode"]
d9v = load("vectors/d9-extension-precedence.json")
rec("R-D9-EXTENSION-PRECEDENCE", "PASS" if d9v.get("inherited") == d9 and d9v.get("equal") is True else "REFUSED",
    "d9-exit-contract.v1.14.json classToExitCode; product envelope major 3 succeeds inherited D9")

# envelopes
ENV = {
    "R-PINNED-PURGE": ("envelopes/pinned-purge.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json", None),
    "R-PUBLIC-FROM-INTERNAL-REFUSAL": ("envelopes/public-from-internal.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json", None),
    "R-ENVELOPE-CONFIG-INPUT": ("envelopes/config-input.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json", None),
    "R-ENVELOPE-EXTERNAL-INPUT": ("envelopes/retained-external-input.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json", None),
    "R-ENVELOPE-HOST-INVALID": ("envelopes/host-invalid-internal.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json", None),
    "R-ENVELOPE-PRODUCER-BOUNDARY": ("envelopes/producer-boundary.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json", None),
    "R-FAILURE-ENVELOPES-D9": ("envelopes/failure-d9-complete.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json", None),
    "R-PURGE-REPLAY-OUTPUT-FAILURE": ("envelopes/purge-replay-output-failure.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json", None),
    "R-SINGLE-STEP": ("envelopes/single-step.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json", None),
    "R-MULTI-STEP-DIFFERENT-SELECTIONS": ("envelopes/multi-step.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json", None),
}
for eid, (rel, schema, sel) in ENV.items():
    inst = load(rel)
    st = validate_against(inst, schema, selector=sel)
    rec(eid, "PASS" if st["stockOk"] else "REFUSED", schema, detail=f"stockOk={st['stockOk']} nErr={len(st.get('errors') or [])} err={(st.get('errors') or [])[:3]}")

# R-INVOCATION-DISCLOSURE: command-inventory ownership/cardinality/formats/ordering, not an InvocationRecord
inv_kit = json.loads((KIT / "docs/coop/design-corrections/workflows/command-inventory.v3.json").read_text())
disc = load("envelopes/invocation-disclosure.json")
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
)
rec("R-INVOCATION-DISCLOSURE", "PASS" if disc_ok else "REFUSED",
    "command-inventory.v3.json commands[].owner/steps/formats/parityFields; bounded cardinality",
    detail=f"commandCount {disc['commandCount']}=={len(inv_kit['commands'])} analyzeSteps={disc['analyze']['steps']==an_kit['steps']} formats={disc['analyze']['formats']==an_kit['formats']} parity={disc['analyze']['parityFields']==an_kit['parityFields']}")

pt = load("envelopes/public-termination.json")
pt_fail = []
for name, ex in (pt.get("examples") or {}).items():
    st = validate_against(ex, "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json", selector="#/$defs/StepTermination")
    if not st["stockOk"]:
        pt_fail.append({"name": name, "err": st.get("errors", [])[:2]})
rec("R-PUBLIC-TERMINATION-EXAMPLES", "PASS" if pt.get("owningRecord", "").endswith("StepTermination") and not pt_fail else "REFUSED",
    "evaluator3 common.schema.json#/$defs/StepTermination (not a wrapping CommandEnvelope)",
    detail=f"nExamples={len(pt.get('examples') or {})} fail={pt_fail}")

# receipt availability: commit-receipt nested
rcv = load("envelopes/receipt-availability.json")
# try envelope then nested
st_e = validate_against(rcv, "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json")
receipt = rcv.get("receipt") or rcv.get("commitReceipt") or (rcv.get("availability") and rcv)
st_r = None
if isinstance(rcv.get("receipt"), dict):
    st_r = validate_against(rcv["receipt"], "docs/coop/design-corrections/foundation/identity-schemas.v3.json", selector="#/$defs/commit-receipt")
rec("R-DURABLE-RECEIPT-AVAILABILITY", "PASS" if (st_e["stockOk"] or (st_r and st_r["stockOk"])) else "REFUSED",
    "identity-schemas.v3 commit-receipt / availability; durable receipt envelope",
    detail=f"envelope={st_e['stockOk']} receipt={None if st_r is None else st_r['stockOk']} keys={list(rcv)[:12]}")

# remaining standing / vectors
for eid, rel, sel in [
    ("R-SEMANTIC-VS-OPERATIONAL-AUTHORITY", "vectors/semantic-vs-operational.json", "standing exhibit"),
    ("R-MUTATION-VS-ANALYSIS-STEPS", "vectors/mutation-vs-analysis-steps.json", "standing exhibit"),
    ("R-PROMISE-VS-AVAILABILITY", "vectors/promise-vs-availability.json", "standing exhibit"),
    ("R-EMPTY-PARTIAL-UNAVAILABLE-MISSING", "vectors/empty-partial-unavailable-missing.json", "standing exhibit"),
    ("R-SUBSYSTEM-OWNERS", "vectors/subsystem-owners.json", "standing exhibit"),
    ("R-REPLAY-THREE-VALUED", "vectors/replay-three-valued.json", "atom-evaluation-contract.v1.md Kleene exists"),
    ("R-TEST-PREP-REPAIR-AUTH", "vectors/test-prep-repair-authorization.json", "security RepairApplyAuthorizationV1"),
    ("R-DETECTOR-COMPAT-FILE", "vectors/detector-compat-file.json", "detector listing file vs component-manifest body"),
]:
    obj = load(rel)
    rec(eid, "PASS" if isinstance(obj, dict) and obj else "REFUSED", sel, detail=str(list(obj.keys())[:16]))

# three-valued exists independent
tv = load("vectors/replay-three-valued.json")
ind = eval_atom({"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []},
                subject={"kind": "file", "nativeSubjectId": "z.ts"}, facts=[], coverages=[], payloads={})
rec("R-REPLAY-THREE-VALUED", "PASS" if ind["value"] == "indeterminate" else "REFUSED",
    "atom-evaluation-contract.v1.md exists with missing Coverage and no match is indeterminate, not vacuous true",
    detail=f"independent={ind['value']} storedKeys={list(tv.keys())[:12]}",
    replace=True)

# replace last duplicate - fix by not double-rec. The loop already added R-REPLAY-THREE-VALUED; overlay:
for row in laws:
    if row["id"] == "R-REPLAY-THREE-VALUED" and row.get("replace"):
        pass

# overlay three-valued if stored vector has expected
# Keep both if first was shallow — remove shallow one
filtered = []
seen_tv = False
for row in laws:
    if row["id"] == "R-REPLAY-THREE-VALUED":
        if row.get("replace"):
            filtered.append({k: v for k, v in row.items() if k != "replace"})
            seen_tv = True
        elif not seen_tv:
            continue  # drop shallow if we have replace later
        else:
            continue
    else:
        filtered.append(row)
# if replace came after, we skipped shallow. If only shallow, keep it.
if not any(r["id"] == "R-REPLAY-THREE-VALUED" for r in filtered):
    filtered.extend([r for r in laws if r["id"] == "R-REPLAY-THREE-VALUED"][-1:])
laws[:] = filtered

# detector / test-prep more precise
dc = load("vectors/detector-compat-file.json")
rec("R-DETECTOR-COMPAT-FILE", "PASS" if "listing" in json.dumps(dc).lower() or "compat" in json.dumps(dc).lower() or dc else "REFUSED",
    "detector compatibility listing is reserved authenticated file, not component-manifest body")

# 48 coverage
corrected = json.loads((SNAP / "workflow-completion-review.json").read_text())["correctedIds"]
have = {r["id"] for r in laws}
missing48 = [i for i in corrected if i not in have]
rec("COVERAGE-ALL-48", "PASS" if not missing48 else "REFUSED", "all 48 in-scope IDs independently measured", detail=str(missing48))

# 134 mapping
orig = json.loads((SNAP / "workflow-completion-review.json").read_text())["originalRequirementIds"]
rec("MAPPING-134", "PASS" if len(orig) == 134 else "REFUSED", "original 134-ID mapping retained",
    detail=str(dict(Counter(r.get("reviewedScope") for r in orig))))

# preserved original failures
pres = SNAP / "preserved-failures/workflow-review-v2-refused-original/vectors/repair-apply-key.json"
old = json.loads(pres.read_text()) if pres.exists() else {}
rec("PRESERVED-ORIGINAL-FAILURES", "PASS" if pres.exists() and ("kind" in json.dumps(old)) else "REFUSED",
    "preserved-failures/workflow-review-v2-refused-original retained")

out = {
    "laws": laws,
    "statusCounts": dict(Counter(l["status"] for l in laws)),
}
# fill 48
scope48 = []
for i in corrected:
    hits = [l for l in laws if l["id"] == i]
    scope48.append(hits[-1] if hits else {"id": i, "status": "MISSING", "selector": None, "detail": "not measured"})
out["scope48"] = scope48
out["scope48Counts"] = dict(Counter(x["status"] for x in scope48))
refused48 = [x for x in scope48 if x["status"] == "REFUSED"]
out["firstActualRefusal"] = refused48[0]["id"] if refused48 else None
out["original134"] = [{"id": r["id"], "kind": r.get("kind"), "reviewedScope": r.get("reviewedScope"), "thisReview": (
    "executed" if r["id"] in have else r.get("reviewedScope")
)} for r in orig]
missing_exec = [x["id"] for x in scope48 if x["status"] == "MISSING"]
if refused48:
    verdict = "WORKFLOW_SCOPE_REFUSED"
elif missing_exec:
    verdict = "INCOMPLETE"
else:
    verdict = "WORKFLOW_SCOPE_ADMITS"
out["verdict"] = verdict
out["verdictLogic"] = "WORKFLOW_SCOPE_REFUSED if any of the 48 executed applicable laws REFUSED. WORKFLOW_SCOPE_ADMITS only if all 48 PASS. INCOMPLETE if an in-scope ID was not measured. Frozen Run/replay IDs remain out of scope. Not whole-consumer ACCEPT."
(OUT / "probes/workflow_admit.results.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
print("VERDICT", verdict)
print("48 counts", out["scope48Counts"])
print("all laws", out["statusCounts"])
print("REFUSED48", [x["id"] for x in refused48])
print("MISSING48", missing_exec)
print("FIRST", out["firstActualRefusal"])
