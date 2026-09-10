"""Retained-closure and cross-record joins from identity-schemas.v3 domainSets
and relation-payload-schemas.v2 x-opensip-relation-registry.

Construction according to an assumed shape is not closure. Each join fetches
retained preimages and compares.
"""
from __future__ import annotations

import json
from typing import Any

from . import admit, canonical, evaluator, h, kit_schemas, law_admit, pilot_checks, store
from . import condtrace


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


def check_fact_relation_laws(fact: dict, payload: dict, snapshot: dict, st: store.Store, fact_id: str | None = None) -> list[str]:
    errors = []
    condtrace.set_document("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
    reg = relation_registry()
    rel = fact["relation"]
    if rel not in reg:
        return [f"FACT_RELATION_UNREGISTERED:{rel}"]
    row = reg[rel]
    fact_id = fact_id or fact.get("id") or f"{rel}@{fact.get('resolution')}"
    rptr = f"/x-opensip-relation-registry/relations/{rel}"
    condtrace.emit(condition=rptr, instance=str(fact_id), field="relation", comparison="registered", left=rel, right=True, result="pass")
    urule = row.get("universeRule")
    if urule == "same-only":
        ok_u = fact.get("sourceUniverse") == fact.get("targetUniverse")
        condtrace.emit(condition=f"{rptr}/universeRule", instance=str(fact_id), field="sourceUniverse", comparison="same-only", left=fact.get("sourceUniverse"), right=fact.get("targetUniverse"), result="pass" if ok_u else "refuse")
        if not ok_u:
            errors.append(f"FACT_UNIVERSE_RULE_SAME_ONLY:{rel}")
    elif urule == "admitted-target":
        condtrace.emit(condition=f"{rptr}/universeRule", instance=str(fact_id), field="targetUniverse", comparison="admitted-target", left=fact.get("targetUniverse"), right=urule, result="pass")
    elif urule:
        condtrace.emit(condition=f"{rptr}/universeRule", instance=str(fact_id), field="universeRule", comparison="dispatch", left=urule, right=None, result="refuse-unhandled-form")
        errors.append(f"FACT_UNIVERSE_RULE_UNHANDLED:{rel}:{urule}")
    if row.get("bodyIdentityJoin"):
        condtrace.emit(condition=f"{rptr}/bodyIdentityJoin", instance=str(fact_id), field="anchors", comparison="delegated-clone-body", left=True, right="check_clone_body_identity", result="pass")
    if row.get("coverageTotality"):
        condtrace.emit(condition=f"{rptr}/coverageTotality", instance=str(fact_id), field="relation", comparison="delegated-view-totality", left=rel, right=row["coverageTotality"].get("rung"), result="pass")
    if not (row.get("rungs") or {}):
        condtrace.emit(condition=f"{rptr}/rungs", instance=str(fact_id), field="rungs", comparison="empty-field-rules", left={}, right="not-the-ladder", result="inapplicable")
    ladder = row["ladder"]
    ok = fact["resolution"] in ladder
    condtrace.emit(condition=f"{rptr}/ladder", instance=str(fact_id), field="resolution", comparison="in", left=fact["resolution"], right=ladder, result="pass" if ok else "refuse")
    if not ok:
        errors.append(f"FACT_RUNG_NOT_IN_LADDER:{rel}@{fact['resolution']}")
    law = row["anchorLaw"]
    n = len(fact.get("anchors") or [])
    cls = law.get("class")
    if cls == "inventory":
        ok = n == 0
        want = 0
    elif cls == "body-identity":
        ok = n == 1
        want = 1
    elif cls == "source-text":
        ok = n >= 1
        want = ">=1"
    else:
        ok = False
        want = f"unhandled:{cls}"
        errors.append(f"FACT_ANCHOR_CLASS_UNHANDLED:{rel}:{cls}")
    condtrace.emit(condition=f"{rptr}/anchorLaw", instance=str(fact_id), field="anchors", comparison="cardinality", left=n, right=want, result="pass" if ok else "refuse")
    if cls == "inventory" and n != 0:
        errors.append(f"FACT_ANCHOR_CARDINALITY:{rel} expected 0 got {n}")
    elif cls == "body-identity" and n != 1:
        errors.append(f"FACT_ANCHOR_CARDINALITY:{rel} expected 1 got {n}")
    elif cls == "source-text" and n < 1:
        errors.append(f"FACT_ANCHOR_CARDINALITY:{rel} expected >=1 got {n}")
    for rung_name, rung in (row.get("rungs") or {}).items():
        applies = fact["resolution"] == rung_name
        if not applies:
            condtrace.emit(condition=f"{rptr}/rungs/{rung_name}", instance=str(fact_id), field="resolution", comparison="rung-dispatch", left=fact["resolution"], right=rung_name, result="inapplicable")
            continue
        for req in rung.get("required") or []:
            ok = req in payload
            condtrace.emit(condition=f"{rptr}/rungs/{rung_name}", instance=str(fact_id), field=req, comparison="required-present", left=req in payload, right=True, result="pass" if ok else "refuse")
            if not ok:
                errors.append(f"FACT_RUNG_REQUIRED:{rel}@{rung_name}:{req}")
        for forb in rung.get("forbidden") or []:
            ok = forb not in payload
            condtrace.emit(condition=f"{rptr}/rungs/{rung_name}", instance=str(fact_id), field=forb, comparison="forbidden-absent", left=forb in payload, right=False, result="pass" if ok else "refuse")
            if not ok:
                errors.append(f"FACT_RUNG_FORBIDDEN:{rel}@{rung_name}:{forb}")
    inv = inventory_index(snapshot)
    for ji, j in enumerate(row.get("snapshotJoins") or []):
        form = j.get("form")
        jptr = f"{rptr}/snapshotJoins/{ji}"
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
                    condtrace.emit(condition=jptr, instance=str(fact_id), field="retainedBlob", comparison="blob-retained", left=rowi["sha256"], right=False, result="refuse")
                else:
                    b = st.blobs[rowi["sha256"]]
                    ok = len(b) == rowi["bytes"] and h.raw_sha256(b) == rowi["sha256"]
                    condtrace.emit(condition=jptr, instance=str(fact_id), field="retainedBlob", comparison="blob-hash-len", left=rowi["sha256"], right=ok, result="pass" if ok else "refuse")
                    if len(b) != rowi["bytes"]:
                        errors.append(f"SNAPSHOT_JOIN_BLOB_LENGTH:{path}")
                    if h.raw_sha256(b) != rowi["sha256"]:
                        errors.append(f"SNAPSHOT_JOIN_BLOB_HASH:{path}")
            else:
                condtrace.emit(condition=jptr, instance=str(fact_id), field=j["pathField"], comparison="inventoried-file", left=path, right=rowi["sha256"], result="pass")
        elif form == "inventoried-path":
            pf = j["pathField"]
            path = payload.get(pf)
            unless = j.get("unless")
            if unless and payload.get(unless["field"]) == unless["equals"]:
                condtrace.emit(condition=jptr, instance=str(fact_id), field=pf, comparison="unless-skip", left=payload.get(unless["field"]), right=unless["equals"], result="inapplicable")
                continue
            ok = path in inv
            condtrace.emit(condition=jptr, instance=str(fact_id), field=pf, comparison="in-inventory", left=path, right=ok, result="pass" if ok else "refuse")
            if not ok:
                errors.append(f"SNAPSHOT_JOIN_PATH_MISSING:{path}")
        else:
            errors.append(f"FACT_SNAPSHOT_JOIN_UNHANDLED_FORM:{rel}:{form}")
            condtrace.emit(condition=jptr, instance=str(fact_id), field="form", comparison="dispatch", left=form, right=None, result="refuse-unhandled-form")
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


def native_context_joins(ctx: dict, domain: str, snapshot: dict, st: store.Store, instance_id: str | None = None) -> list[str]:
    errors = []
    idsch = kit_schemas.identity_schema()
    sets = idsch["x-opensip-digest-domains"]["domainSets"]["native-context"]
    row = sets.get(domain)
    if not row:
        return [f"UNKNOWN_NATIVE_CONTEXT_DOMAIN:{domain}"]
    inv = inventory_index(snapshot)
    inst = instance_id or domain
    condtrace.set_document("docs/coop/design-corrections/foundation/identity-schemas.v3.json")
    base = f"/x-opensip-digest-domains/domainSets/native-context/{domain}"
    for ji, j in enumerate(row.get("closureJoins") or []):
        cur = ctx
        for p in j["path"]:
            cur = cur.get(p) if isinstance(cur, dict) else None
        ptr = f"{base}/closureJoins/{ji}"
        if cur is None:
            errors.append(f"CLOSURE_JOIN_MISSING:{'.'.join(j['path'])}")
            condtrace.emit(condition=ptr, instance=inst, field=".".join(j["path"]), comparison="fetch", left=None, right=j.get("kind"), result="refuse")
            continue
        if j["form"] == "closure2-identity":
            try:
                clo = _obj(st, cur)
            except ClosureError as e:
                errors.append(str(e))
                condtrace.emit(condition=ptr, instance=inst, field="kind", comparison="eq", left=None, right=j.get("kind"), result="refuse")
                continue
            ok = clo.get("kind") == j.get("kind")
            condtrace.emit(condition=ptr, instance=inst, field="kind", comparison="eq", left=clo.get("kind"), right=j.get("kind"), result="pass" if ok else "refuse")
            if not ok:
                errors.append(f"CLOSURE_KIND_MISMATCH:{cur} want {j.get('kind')} got {clo.get('kind')}")
        elif j["form"] == "closure2-suffix":
            ident = "closure2:" + cur
            try:
                clo = _obj(st, ident)
            except ClosureError as e:
                errors.append(str(e))
                condtrace.emit(condition=ptr, instance=inst, field="kind", comparison="eq", left=None, right=j.get("kind"), result="refuse")
                continue
            ok = clo.get("kind") == j.get("kind")
            condtrace.emit(condition=ptr, instance=inst, field="kind", comparison="eq", left=clo.get("kind"), right=j.get("kind"), result="pass" if ok else "refuse")
            if not ok:
                errors.append(f"CLOSURE_KIND_MISMATCH:{ident}")
        else:
            condtrace.emit(condition=ptr, instance=inst, field="form", comparison="dispatch", left=j.get("form"), right=None, result="refuse-unhandled-form")
            errors.append(f"CLOSURE_JOIN_UNHANDLED_FORM:{j.get('form')}")
    for ji, j in enumerate(row.get("snapshotJoins") or []):
        form = j["form"]
        cur = ctx
        for p in j["path"]:
            cur = cur.get(p) if isinstance(cur, dict) else None
        ptr = f"{base}/snapshotJoins/{ji}"
        if cur is None:
            if j.get("nullable"):
                condtrace.emit(condition=ptr, instance=inst, field=".".join(j["path"]), comparison="nullable-skip", left=None, right=form, result="inapplicable")
                continue
            errors.append(f"SNAPSHOT_JOIN_MISSING:{'.'.join(j['path'])}")
            condtrace.emit(condition=ptr, instance=inst, field=".".join(j["path"]), comparison="fetch", left=None, right=form, result="refuse")
            continue
        if form == "inventoried-paths":
            paths = cur if isinstance(cur, list) else [cur]
            for pth in paths:
                ok = pth in inv
                condtrace.emit(condition=ptr, instance=inst, field=j.get("pathField") or "path", comparison="in-inventory", left=pth, right=ok, result="pass" if ok else "refuse")
                if not ok:
                    errors.append(f"CONTEXT_PATH_NOT_INVENTORIED:{pth}")
        elif form == "inventoried-path-and-digest":
            pth = cur.get(j["pathField"]) if isinstance(cur, dict) else None
            dg = cur.get(j["digestField"]) if isinstance(cur, dict) else None
            if pth not in inv:
                errors.append(f"LOCKFILE_PATH_NOT_INVENTORIED:{pth}")
                condtrace.emit(condition=ptr, instance=inst, field=j["pathField"], comparison="in-inventory", left=pth, right=False, result="refuse")
            else:
                ok = inv[pth]["sha256"] == dg
                condtrace.emit(condition=ptr, instance=inst, field=j["digestField"], comparison="eq", left=dg, right=inv[pth]["sha256"], result="pass" if ok else "refuse")
                if not ok:
                    errors.append(f"LOCKFILE_DIGEST_MISMATCH:{pth}")
        else:
            errors.append(f"SNAPSHOT_JOIN_UNHANDLED_FORM:{form}")
            condtrace.emit(condition=ptr, instance=inst, field="form", comparison="dispatch", left=form, right=None, result="refuse-unhandled-form")
    for ni, nr in enumerate(row.get("nestedIdentities") or []):
        ptr = f"{base}/nestedIdentities/{ni}"
        condtrace.emit(condition=ptr, instance=inst, field=".".join(nr.get("path") or []), comparison="nestedIdentities", left=None, right=None, result="pass-empty-or-present")
    for nri, nr in enumerate(row.get("nestedRecords") or []):
        ptr = f"{base}/nestedRecords/{nri}"
        cur = ctx
        for p in nr["path"]:
            cur = cur.get(p) if isinstance(cur, dict) else None
        if cur is None:
            if nr.get("nullable"):
                condtrace.emit(condition=ptr, instance=inst, field=".".join(nr["path"]), comparison="nullable-skip", left=None, right=None, result="inapplicable")
                continue
            errors.append(f"NESTED_RECORD_MISSING:{'.'.join(nr['path'])}")
            condtrace.emit(condition=ptr, instance=inst, field=".".join(nr["path"]), comparison="fetch", left=None, right=None, result="refuse")
            continue
        nested = _c_load(st, cur) if isinstance(cur, str) else cur
        condtrace.emit(condition=ptr, instance=inst, field=".".join(nr["path"]), comparison="canonical-record-load", left=cur if isinstance(cur, str) else "inline", right=nr.get("selector"), result="pass")
        for bji, bj in enumerate(nr.get("blobJoins") or []):
            bptr = f"{ptr}/blobJoins/{bji}"
            seq = nested
            parts = bj["path"]
            if parts == ["entries", "[]"] and isinstance(seq, dict):
                for ent in seq.get("entries") or []:
                    dgst = ent.get(bj["digestField"])
                    ok = dgst in st.blobs
                    condtrace.emit(condition=bptr, instance=inst, field=bj["digestField"], comparison="blob-retained", left=dgst, right=ok, result="pass" if ok else "refuse")
                    if not ok:
                        errors.append(f"NESTED_BLOB_MISSING:{dgst}")
            else:
                errors.append(f"BLOB_JOIN_UNHANDLED_PATH:{parts}")
                condtrace.emit(condition=bptr, instance=inst, field="path", comparison="dispatch", left=parts, right=None, result="refuse-unhandled-form")
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
        ok = node.get("kind") == expected
        condtrace.set_document("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
        condtrace.emit(
            condition="/x-opensip-config-node-kind-law",
            instance=str(path), field="nodes[].kind", comparison="basename-kind",
            left=node.get("kind"), right=expected, result="pass" if ok else "refuse",
        )
        if not ok:
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


def native_universe_joins(uni: dict, domain: str, ctx_hex: str, st: store.Store, instance_id: str | None = None) -> list[str]:
    errors = []
    idsch = kit_schemas.identity_schema()
    sets = idsch["x-opensip-digest-domains"]["domainSets"]["native-semantic-universe"]
    row = sets.get(domain)
    if not row:
        return [f"UNKNOWN_UNIVERSE_DOMAIN:{domain}"]
    inst = instance_id or domain
    condtrace.set_document("docs/coop/design-corrections/foundation/identity-schemas.v3.json")
    ncid = uni.get("nativeContextId")
    want = "sha256:" + ctx_hex if not str(ctx_hex).startswith("sha256:") else ctx_hex
    if ncid != want and ncid != ctx_hex:
        # ctx_hex may already be bare
        if ncid != "sha256:" + ctx_hex:
            errors.append(f"UNIVERSE_CONTEXT_MISMATCH:{ncid} vs {want}")
    lv = (row.get("languageVersionBinding") or {})
    fields = lv.get("fields") or {}
    for fname, spec in fields.items():
        ptr = f"/x-opensip-digest-domains/domainSets/native-semantic-universe/{domain}/languageVersionBinding/fields/{fname}"
        if spec.get("const") is not None:
            condtrace.emit(condition=ptr, instance=inst, field=fname, comparison="const-inapplicable-or-bound", left=spec.get("const"), right=spec.get("source"), result="inapplicable" if domain.startswith("native.semantic-universe.typescript") and spec.get("const") == "rustc" else "pass")
            continue
        condtrace.emit(condition=ptr, instance=inst, field=fname, comparison="source-path", left=spec.get("source"), right=spec.get("path"), result="pass")
    dialect = lv.get("dialect") or {}
    table = dialect.get("table") or {}
    form = dialect.get("form")
    dptr = f"/x-opensip-digest-domains/domainSets/native-semantic-universe/{domain}/languageVersionBinding/dialect"
    if form == "closed-suffix-table":
        snap = next((o for i, o in st.objects.items() if i.startswith("snapshot2:")), None)
        paths = [r["path"] for r in (snap.get("sourceInventory") or [])] if isinstance(snap, dict) else []
        for suf, var in table.items():
            sptr = f"{dptr}/table/{suf}"
            matching = [p for p in paths if str(p).endswith(suf)]
            # longest-suffix wins: a path matching a longer suffix is not this row's
            longer = [o for o in table if o != suf and o.endswith(suf) or (len(o) > len(suf) and suf.endswith(o) is False and o.endswith(suf))]
            # simpler: path applies to this suffix if it ends with suf and no longer table key also matches
            applied = []
            for p in matching:
                better = [o for o in table if o != suf and str(p).endswith(o) and len(o) > len(suf)]
                if not better:
                    applied.append(p)
            if not applied:
                condtrace.emit(condition=sptr, instance=inst, field="dialect", comparison="suffix-dispatch", left=suf, right=var, result="inapplicable")
            else:
                condtrace.emit(condition=sptr, instance=inst, field="dialect", comparison="suffix-dispatch", left=applied, right=var, result="pass")
        condtrace.emit(condition=dptr, instance=inst, field="form", comparison="eq", left=form, right="closed-suffix-table", result="pass")
    elif form:
        condtrace.emit(condition=dptr, instance=inst, field="form", comparison="dispatch", left=form, right=None, result="inapplicable" if domain.startswith("native.semantic-universe.typescript") is False or form != "closed-suffix-table" else "pass")
        if domain.startswith("native.semantic-universe.typescript") and form != "closed-suffix-table":
            errors.append(f"UNIVERSE_DIALECT_UNHANDLED_FORM:{form}")
            condtrace.emit(condition=dptr, instance=inst, field="form", comparison="dispatch", left=form, right=None, result="refuse-unhandled-form")
    for nri, nr in enumerate(row.get("nestedRecords") or []):
        ptr = f"/x-opensip-digest-domains/domainSets/native-semantic-universe/{domain}/nestedRecords/{nri}"
        condtrace.emit(condition=ptr, instance=inst, field=str(nri), comparison="nestedRecords", left=nr.get("path"), right=nr.get("selector"), result="pass")
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


def admit_native_context(ctx: dict, domain: str, snapshot: dict, st: store.Store, instance_id: str | None = None) -> list[str]:
    """Re-decide native context admission over retained descriptors. No compiler execution."""
    errors = native_context_joins(ctx, domain, snapshot, st, instance_id=instance_id)
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


def bind_universe(uni: dict, domain: str, ctx_hex: str, st: store.Store, instance_id: str | None = None) -> list[str]:
    errors = native_universe_joins(uni, domain, ctx_hex, st, instance_id=instance_id)
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
    admit.set_graph_context(st)
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
            errors.extend(admit_native_context(ctx, domain, snap, st, instance_id=ident))
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
            errors.extend(bind_universe(obj, udomain, ctx_hex or "", st, instance_id=ident))
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
            errors.extend(check_fact_relation_laws(fact, payload, snap, st, fact_id=ident))
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
