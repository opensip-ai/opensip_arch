"""Retained-closure and cross-record joins from identity-schemas.v3 domainSets
and relation-payload-schemas.v2 x-opensip-relation-registry.

Construction according to an assumed shape is not closure. Each join fetches
retained preimages and compares.
"""
from __future__ import annotations

import json
from typing import Any

from . import admit, canonical, evaluator, h, kit_schemas, law_admit, pilot_checks, store


class ClosureError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.firstRefusal = code


class EvidenceUnavailable(Exception):
    """Identity §6: missing promised bytes are not schema refusal."""

    def __init__(self, ref: str):
        super().__init__(f"evidence.missing:{ref}")
        self.code = "HOST.IO_FAILURE"
        self.faultCause = "host-io"
        self.domainDetail = "evidence.missing"
        self.classification = "operational-failed"
        self.ref = ref
        self.firstRefusal = "evidence.missing"


def _c_load(st: store.Store, digest: str) -> Any:
    bare = digest.split(":")[-1] if digest.startswith("sha256:") else digest
    raw = st.blobs.get(bare) or st.blobs.get(digest)
    if raw is None:
        raise EvidenceUnavailable(digest)
    # canonical-record: UTF-8 C(X). h-identity: framed preimage.
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        try:
            _domain, cx = h.parse_h_frame(raw)
            return json.loads(cx.decode("utf-8"))
        except Exception:
            return raw


def _obj(st: store.Store, ident: str) -> Any:
    if ident in st.objects:
        return st.objects[ident]
    bare = ident.split(":")[-1]
    for k, v in st.objects.items():
        if k.endswith(bare):
            return v
    raise EvidenceUnavailable(ident)


def obj_or_none(st: store.Store, ident: str | None) -> Any:
    if not ident:
        return None
    try:
        return _obj(st, ident)
    except EvidenceUnavailable:
        return None


def inventory_index(snapshot: dict) -> dict[str, dict]:
    idx = {}
    for row in snapshot.get("sourceInventory") or []:
        idx[row["path"]] = row
    return idx


def relation_registry() -> dict:
    rel = kit_schemas.relation_schema()
    return rel["x-opensip-relation-registry"]["relations"]


def check_fact_relation_laws(fact: dict, payload: dict, snapshot: dict, st: store.Store) -> list[str]:
    errors = []
    reg = relation_registry()
    rel = fact["relation"]
    if rel not in reg:
        return [f"FACT_RELATION_UNREGISTERED:{rel}"]
    row = reg[rel]
    ladder = row["ladder"]
    if fact["resolution"] not in ladder:
        errors.append(f"FACT_RUNG_NOT_IN_LADDER:{rel}@{fact['resolution']}")
    law = row["anchorLaw"]
    n = len(fact.get("anchors") or [])
    if law.get("class") == "inventory":
        if n != 0:
            errors.append(f"FACT_ANCHOR_CARDINALITY:{rel} expected 0 got {n}")
    elif law.get("class") == "body-identity":
        if n != 1:
            errors.append(f"FACT_ANCHOR_CARDINALITY:{rel} expected 1 got {n}")
    elif law.get("class") == "source-text":
        if n < 1:
            errors.append(f"FACT_ANCHOR_CARDINALITY:{rel} expected >=1 got {n}")
    inv = inventory_index(snapshot)
    for j in row.get("snapshotJoins") or []:
        form = j.get("form")
        if form == "inventoried-file":
            path = payload.get(j["pathField"])
            if path not in inv:
                errors.append(f"SNAPSHOT_JOIN_PATH_MISSING:{path}")
                continue
            rowi = inv[path]
            if payload.get(j["digestField"]) != rowi["sha256"]:
                errors.append(f"SNAPSHOT_JOIN_DIGEST_MISMATCH:{path}")
            if payload.get(j["lengthField"]) != rowi["bytes"]:
                errors.append(f"SNAPSHOT_JOIN_LENGTH_MISMATCH:{path}")
            if j.get("retainedBlob"):
                if rowi["sha256"] not in st.blobs:
                    errors.append(f"SNAPSHOT_JOIN_BLOB_MISSING:{path}")
                else:
                    b = st.blobs[rowi["sha256"]]
                    if len(b) != rowi["bytes"]:
                        errors.append(f"SNAPSHOT_JOIN_BLOB_LENGTH:{path}")
                    if h.raw_sha256(b) != rowi["sha256"]:
                        errors.append(f"SNAPSHOT_JOIN_BLOB_HASH:{path}")
        elif form == "inventoried-path":
            pf = j["pathField"]
            path = payload.get(pf)
            unless = j.get("unless")
            if unless and payload.get(unless["field"]) == unless["equals"]:
                continue
            if path not in inv:
                errors.append(f"SNAPSHOT_JOIN_PATH_MISSING:{path}")
    return errors


def coverage_totality_and_partition(view: dict, st: store.Store, snapshot: dict) -> list[str]:
    errors = []
    facts_by_id = {i: o for i, o in st.objects.items() if i.startswith("fact2:")}
    scopes = []
    for sid in view.get("scopeIds") or []:
        scopes.append((sid, _obj(st, sid)))
    # partition: same (snapshotId, relation, resolution, sourceUniverse, targetUniverse) subjects disjoint
    groups: dict[tuple, list] = {}
    for sid, sc in scopes:
        key = (sc["snapshotId"], sc["relation"], sc["resolution"], sc["sourceUniverse"], sc["targetUniverse"])
        groups.setdefault(key, []).append((sid, set(sc.get("subjects") or [])))
    for key, members in groups.items():
        seen = set()
        for sid, subj in members:
            overlap = seen & subj
            if overlap:
                lowest = sorted(overlap, key=lambda s: s.encode("utf-8"))[0]
                errors.append(f"SUBJECT_SCOPE_PARTITION_OVERLAP:{key[1]}@{key[2]}:{lowest}")
            seen |= subj
    # totality: file@enumerated complete Coverage owes a fact per inventoried subject in that scope
    inv = set(inventory_index(snapshot))
    cov_by_scope = {}
    for cid in view.get("coverageIds") or []:
        cov = _obj(st, cid)
        cov_by_scope[cov["scopeId"]] = (cid, cov)
    view_facts = [facts_by_id[f] for f in view.get("facts") or [] if f in facts_by_id]
    for sid, sc in scopes:
        if sc["relation"] != "file" or sc["resolution"] != "enumerated":
            continue
        pair = cov_by_scope.get(sid)
        if not pair:
            continue
        cid, cov = pair
        payload = _c_load(st, cov["payloadDigest"])
        entry = payload.get("entry") or {}
        if entry.get("coverage") != "complete":
            continue
        # Native §1.2: complete file@enumerated is total over the snapshot inventory.
        owed = sorted(inv)
        have = set()
        for f in view_facts:
            if f.get("relation") != "file":
                continue
            pl = _c_load(st, f["payloadDigest"])
            if isinstance(pl, dict) and pl.get("path") in owed:
                have.add(pl["path"])
        for path in owed:
            if path not in have:
                errors.append(f"COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:{path}")
    return errors


def native_context_joins(ctx: dict, domain: str, snapshot: dict, st: store.Store) -> list[str]:
    errors = []
    idsch = kit_schemas.identity_schema()
    sets = idsch["x-opensip-digest-domains"]["domainSets"]["native-context"]
    row = sets.get(domain)
    if not row:
        return [f"UNKNOWN_NATIVE_CONTEXT_DOMAIN:{domain}"]
    inv = inventory_index(snapshot)
    for j in row.get("closureJoins") or []:
        cur = ctx
        for p in j["path"]:
            cur = cur.get(p) if isinstance(cur, dict) else None
        if cur is None:
            errors.append(f"CLOSURE_JOIN_MISSING:{'.'.join(j['path'])}")
            continue
        if j["form"] == "closure2-identity":
            try:
                clo = _obj(st, cur)
            except ClosureError as e:
                errors.append(str(e))
                continue
            if clo.get("kind") != j.get("kind"):
                errors.append(f"CLOSURE_KIND_MISMATCH:{cur} want {j.get('kind')} got {clo.get('kind')}")
        elif j["form"] == "closure2-suffix":
            ident = "closure2:" + cur
            try:
                clo = _obj(st, ident)
            except ClosureError as e:
                errors.append(str(e))
                continue
            if clo.get("kind") != j.get("kind"):
                errors.append(f"CLOSURE_KIND_MISMATCH:{ident}")
    for j in row.get("snapshotJoins") or []:
        form = j["form"]
        cur = ctx
        for p in j["path"]:
            cur = cur.get(p) if isinstance(cur, dict) else None
        if cur is None:
            if j.get("nullable"):
                continue
            errors.append(f"SNAPSHOT_JOIN_MISSING:{'.'.join(j['path'])}")
            continue
        if form == "inventoried-paths":
            paths = cur if isinstance(cur, list) else [cur]
            for pth in paths:
                if pth not in inv:
                    errors.append(f"CONTEXT_PATH_NOT_INVENTORIED:{pth}")
        elif form == "inventoried-path-and-digest":
            if cur is None and j.get("nullable"):
                continue
            pth = cur.get(j["pathField"]) if isinstance(cur, dict) else None
            dg = cur.get(j["digestField"]) if isinstance(cur, dict) else None
            if pth not in inv:
                errors.append(f"LOCKFILE_PATH_NOT_INVENTORIED:{pth}")
            elif inv[pth]["sha256"] != dg:
                errors.append(f"LOCKFILE_DIGEST_MISMATCH:{pth}")
    for nr in row.get("nestedRecords") or []:
        cur = ctx
        for p in nr["path"]:
            cur = cur.get(p) if isinstance(cur, dict) else None
        if cur is None:
            if nr.get("nullable"):
                continue
            errors.append(f"NESTED_RECORD_MISSING:{'.'.join(nr['path'])}")
            continue
        nested = _c_load(st, cur) if isinstance(cur, str) else cur
        for bj in nr.get("blobJoins") or []:
            # path entries[] digestField contentSha256
            seq = nested
            parts = bj["path"]
            # walk to array
            if parts == ["entries", "[]"] and isinstance(seq, dict):
                for ent in seq.get("entries") or []:
                    dgst = ent.get(bj["digestField"])
                    if dgst not in st.blobs:
                        errors.append(f"NESTED_BLOB_MISSING:{dgst}")
    return errors


CONFIG_NODE_KIND_BY_BASENAME = {
    "tsconfig.json": "tsconfig",
    "jsconfig.json": "jsconfig",
}


def check_typescript_config_graph(graph: dict) -> list[str]:
    """native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law plus graph reachability."""
    errors = []
    nodes = graph.get("nodes") or []
    by_path = {}
    for node in nodes:
        path = node.get("path")
        if path in by_path:
            errors.append(f"CONFIG_GRAPH_DUPLICATE_PATH:{path}")
        by_path[path] = node
        basename = str(path).rsplit("/", 1)[-1]
        expected = CONFIG_NODE_KIND_BY_BASENAME.get(basename, "other")
        if node.get("kind") != expected:
            errors.append(f"native.config-graph-kind-contradicts-path:{path}")
    entry = graph.get("entryConfigPath")
    if entry is not None and entry not in by_path:
        errors.append(f"CONFIG_GRAPH_ENTRY_MISSING:{entry}")
        return errors
    for path, node in by_path.items():
        for edge in node.get("extendsResolved") or []:
            if edge not in by_path:
                errors.append(f"CONFIG_GRAPH_EDGE_UNNAMED:{path}->{edge}")
    if entry is None:
        return errors
    # reachability from entry; acyclicity on directed extends edges
    seen = set()
    stack = [entry]
    visiting = set()

    def visit(p):
        if p in visiting:
            errors.append(f"CONFIG_GRAPH_CYCLE:{p}")
            return
        if p in seen:
            return
        visiting.add(p)
        seen.add(p)
        node = by_path.get(p)
        if node:
            for edge in node.get("extendsResolved") or []:
                if edge in by_path:
                    visit(edge)
        visiting.discard(p)

    visit(entry)
    for path in by_path:
        if path not in seen:
            errors.append(f"CONFIG_GRAPH_UNREACHABLE:{path}")
    return errors


def native_universe_joins(uni: dict, domain: str, ctx_hex: str, st: store.Store) -> list[str]:
    errors = []
    idsch = kit_schemas.identity_schema()
    sets = idsch["x-opensip-digest-domains"]["domainSets"]["native-semantic-universe"]
    row = sets.get(domain)
    if not row:
        return [f"UNKNOWN_UNIVERSE_DOMAIN:{domain}"]
    ncid = uni.get("nativeContextId")
    want = "sha256:" + ctx_hex if not str(ctx_hex).startswith("sha256:") else ctx_hex
    if ncid != want and ncid != ctx_hex:
        # ctx_hex may already be bare
        if ncid != "sha256:" + ctx_hex:
            errors.append(f"UNIVERSE_CONTEXT_MISMATCH:{ncid} vs {want}")
    if domain == "native.semantic-universe.typescript.v2":
        ghash = uni.get("tsconfigGraphHash")
        if ghash:
            graph = _c_load(st, ghash)
            if isinstance(graph, dict):
                errors.extend(check_typescript_config_graph(graph))
                recomputed = h.raw_sha256(canonical.encode(graph))
                if recomputed != ghash:
                    errors.append(f"TSCONFIG_GRAPH_HASH_MISMATCH:{ghash} vs {recomputed}")
    return errors


def admit_native_context(ctx: dict, domain: str, snapshot: dict, st: store.Store) -> list[str]:
    """Re-decide native context admission over retained descriptors. No compiler execution."""
    errors = native_context_joins(ctx, domain, snapshot, st)
    hx = h.h_digest(domain, ctx)
    frame = st.blobs.get(hx)
    if frame is None:
        errors.append(f"native.native-context-closure-unretained:{hx}")
        return errors
    try:
        parsed_domain, cx = h.parse_h_frame(frame)
    except ValueError as e:
        errors.append(f"H_FRAME_ADMISSION:{e}")
        return errors
    if parsed_domain != domain:
        errors.append(f"H_FRAME_DOMAIN_MISMATCH:{parsed_domain}!={domain}")
    restated = canonical.encode(ctx)
    if cx != restated:
        errors.append("H_FRAME_C_MISMATCH")
    if domain == "native.context.typescript.v2":
        libs = (ctx.get("toolchain") or {}).get("libSelection") or []
        folded = [s.lower() for s in libs]  # ASCII lib names: full default lowercase == this
        if len(folded) != len(set(folded)):
            errors.append("native.native-context-field-mismatch:duplicate-lib-selection")
        honored = (((ctx.get("configProjection") or {}).get("honoredOptions") or {}).get("lib")) or []
        if honored and {x.lower() for x in libs} != {x.lower() for x in honored}:
            errors.append("native.native-context-field-mismatch:libSelection")
    return errors


def bind_universe(uni: dict, domain: str, ctx_hex: str, st: store.Store) -> list[str]:
    errors = native_universe_joins(uni, domain, ctx_hex, st)
    ncid = uni.get("nativeContextId")
    want = "sha256:" + ctx_hex
    if ncid not in (want, ctx_hex):
        errors.append(f"native.universe-context-binding-mismatch:{ncid}")
    return errors


def _complete_replay(st: store.Store, run: dict, plan: dict, proof: dict) -> list[str]:
    """Identity §4 public close_run: independently derive complete proof from retained inputs."""
    errors = []
    replay = evaluator.replay_from_retained(st)
    cmp = replay["comparison"]
    if cmp.get("refused"):
        errors.append(f"REPLAY_PROOF_MISMATCH:{cmp.get('reason') or cmp}")
    for extra in replay.get("outputMismatches") or []:
        errors.append(f"REPLAY_OUTPUT_PREIMAGE:{extra}")
    return errors


def close_run(st: store.Store) -> dict:
    """Public close_run: owner joins + native re-admission + complete evaluator3 replay."""
    runs = [(i, o) for i, o in st.objects.items() if i.startswith("run3:")]
    if len(runs) != 1:
        raise ClosureError("RUN_CARDINALITY", f"expected 1 run3, got {len(runs)}")
    run_id, run = runs[0]
    errors = []
    # acyclic field presence
    plan = _obj(st, run["planId"])
    snap = _obj(st, run["snapshotId"])
    evid = _obj(st, run["evidenceId"])
    seal = _obj(st, run["evaluationSealId"])
    proof = _obj(st, evid["proofBundleId"])
    if "evidenceId" in proof or "runId" in proof:
        errors.append("PROOF_EVIDENCE_CYCLE")
    if run["snapshotId"] != plan["snapshotId"]:
        errors.append("RUN_PLAN_SNAPSHOT_MISMATCH")
    if run["planId"] != evid["planId"] or run["planId"] != seal["planId"] or run["planId"] != proof["planId"]:
        errors.append("PLAN_ID_JOIN_MISMATCH")
    if run["capabilityManifestId"] != plan["capabilityManifestId"]:
        errors.append("CAPABILITY_MANIFEST_ID_JOIN")
    cap_bytes = st.blobs.get(plan["capabilityManifestBytesDigest"])
    if not cap_bytes:
        errors.append("CAPABILITY_MANIFEST_BYTES_MISSING")
    else:
        recomputed = h.capability_manifest_id(cap_bytes)
        if recomputed != plan["capabilityManifestId"]:
            errors.append(f"CAPABILITY_MANIFEST_RECOMPUTE:{recomputed}!={plan['capabilityManifestId']}")
    # native contexts named by plan
    for hx in plan.get("nativeContextDigests") or []:
        ident = "sha256:" + hx
        if ident not in st.objects and not any(k.endswith(hx) for k in st.objects):
            errors.append(f"PLAN_CONTEXT_UNRETAINED:{hx}")
            continue
        ctx = st.objects.get(ident) or _obj(st, ident)
        # classify domain
        domain = None
        if isinstance(ctx, dict) and "languageMode" in ctx and "toolchain" in ctx and "compilerName" in (ctx.get("toolchain") or {}):
            domain = "native.context.typescript.v2"
        elif isinstance(ctx, dict) and "grammarBundle" in ctx:
            domain = "native.context.syntax.v2"
        elif isinstance(ctx, dict) and "targetTriple" in ctx:
            domain = "native.context.rust.v2"
        if domain:
            errors.extend(admit_native_context(ctx, domain, snap, st))
            recomputed_hex = h.h_digest(domain, ctx)
            if recomputed_hex != hx:
                errors.append(f"CONTEXT_H_MISMATCH:{hx} vs {recomputed_hex}")
    # native semantic universes retained as sha256 objects
    for ident, obj in list(st.objects.items()):
        if not ident.startswith("sha256:") or not isinstance(obj, dict):
            continue
        udomain = None
        ctx_hex = None
        if obj.get("schemaVersion") == 2 and "tsconfigGraphHash" in obj:
            udomain = "native.semantic-universe.typescript.v2"
            ctx_hex = str(obj.get("nativeContextId") or "").split(":")[-1]
        elif obj.get("schemaVersion") == 2 and "crateRootPaths" in obj:
            udomain = "native.semantic-universe.rust.v2"
            ctx_hex = str(obj.get("nativeContextId") or "").split(":")[-1]
        elif obj.get("schemaVersion") == 2 and "selectedGrammarIds" in obj:
            udomain = "native.semantic-universe.syntax.v2"
            ctx_hex = str(obj.get("nativeContextId") or "").split(":")[-1]
        if udomain:
            errors.extend(bind_universe(obj, udomain, ctx_hex or "", st))
            recomputed = h.h_digest(udomain, obj)
            bare = ident.split(":")[-1]
            if recomputed != bare:
                errors.append(f"UNIVERSE_H_MISMATCH:{bare} vs {recomputed}")
            plan_hexes = set(plan.get("nativeContextDigests") or [])
            if ctx_hex and ctx_hex not in plan_hexes:
                errors.append(f"UNIVERSE_CONTEXT_NOT_IN_PLAN:{ctx_hex}")
    # facts
    for ident, fact in list(st.objects.items()):
        if not ident.startswith("fact2:"):
            continue
        payload = _c_load(st, fact["payloadDigest"])
        if isinstance(payload, dict):
            errors.extend(check_fact_relation_laws(fact, payload, snap, st))
            if fact.get("relation") == "imports":
                errors.extend(pilot_checks.check_imports_rungs(fact, payload))
            if fact.get("relation") == "clones":
                uni = None
                ctx = None
                uhex = fact.get("sourceUniverse")
                for iid, rec in st.objects.items():
                    if iid.startswith("sha256:") and isinstance(rec, dict) and rec.get("schemaVersion") == 2 and "tsconfigGraphHash" in rec:
                        if iid.endswith(str(uhex)):
                            uni = rec
                            ctx_id = rec.get("nativeContextId")
                            ctx = st.objects.get(ctx_id) or obj_or_none(st, ctx_id)
                            break
                if uni is not None and ctx is not None:
                    errors.extend(pilot_checks.check_clone_body_identity(fact, payload, snap, uni, ctx, st))
                else:
                    errors.append(f"CLONE_UNIVERSE_OR_CONTEXT_UNRETAINED:{ident}")
            try:
                admit.admit_relation_payload(payload, fact["relation"], st, ident)
            except admit.AdmitError as e:
                errors.append(f"{e.code}:{e.message}")
    # views
    for ident, view in list(st.objects.items()):
        if ident.startswith("view2:"):
            errors.extend(coverage_totality_and_partition(view, st, snap))
            errors.extend(pilot_checks.check_file_totality_match_on(view, st, snap))
            if view.get("planId") != run["planId"]:
                errors.append(f"VIEW_PLAN_MISMATCH:{ident}")
    # Plan.budget equals resolved semantic configuration analysis.budget
    try:
        cfg = _c_load(st, plan["resolvedConfigDigest"])
        want = (cfg.get("analysis") or {}).get("budget")
        if want is not None and plan.get("budget") != want:
            errors.append(f"PLAN_BUDGET_NE_ANALYSIS_BUDGET:{plan.get('budget')}!={want}")
    except EvidenceUnavailable:
        raise
    errors.extend(pilot_checks.check_all_h_identity_frames(st))
    spec = _c_load(st, plan["analysisSpecDigest"])
    errors.extend(pilot_checks.check_analysis_spec_parameters(spec, st))
    from . import builder as _builder
    ep_d = next(p["payloadDigest"] for p in spec["parameters"] if p["schemaDigest"] == _builder.ENUM_PLAN_DIGEST)
    enum_plan = _c_load(st, ep_d)
    mem = _c_load(st, enum_plan["membershipDigest"])
    errors.extend(pilot_checks.check_u4_membership(mem, snap))
    errors.extend(pilot_checks.check_enumeration_plan_joins(plan, spec, enum_plan, mem, st))
    ei = _c_load(st, proof["executionInputsDigest"])
    errors.extend(pilot_checks.check_expected_inventories(enum_plan, ei, st))
    errors.extend(pilot_checks.check_cell_outcome_totality(enum_plan, ei))
    law = law_admit.run_all(st)
    for lid, rec in law.items():
        for e in rec.get("errors") or []:
            errors.append(f"{lid}:{e}")
    try:
        errors.extend(_complete_replay(st, run, plan, proof))
    except EvidenceUnavailable:
        raise
    if errors:
        raise ClosureError("CLOSURE_REFUSED", " | ".join(errors))
    return {"closed": True, "runId": run_id, "errors": [], "replayed": True}
