"""Independent occupancy probes for query-reconciliation coauthor peer review.

Uses the disposable copy under output/disposable/work. Does not mutate inputs.
Not a whole-suite pin run. Helper failures are recorded as helper-only, never
as complete close_run / execute_graph_query proof.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import json
import sys
import traceback
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/grok-query-reconciliation-correction-peer.v1/output")
WORK = OUT / "disposable" / "work"
FOUND = WORK / "docs" / "coop" / "design-corrections" / "foundation"
WORKF = WORK / "docs" / "coop" / "design-corrections" / "workflows"
PY = Path("/tmp/opensip-architecture-review-env/bin/python")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = load("probe_semantic_fixture", FOUND / "evaluator_semantic_fixture.v3.py")
R = load("probe_semantic_replay", FOUND / "evaluator_replay_model.v3.py")
Q = load("probe_query", WORKF / "query_projection_model.v3.py")
AM = Q.atom_model()
C = R.M.C
replay = load("probe_check_semantic", FOUND / "check-semantic-replay.v3.py")

IMPORTS_EXISTS = {
    "op": "exists",
    "relation": "imports",
    "minResolution": "resolved-target",
    "endpoint": "target",
    "filters": [],
}
IMPORTS_NONE = {
    "op": "none",
    "relation": "imports",
    "minResolution": "resolved-target",
    "endpoint": "target",
    "filters": [],
}
REFS_EXISTS_SRC = {
    "op": "exists",
    "relation": "references",
    "minResolution": "resolved-binding",
    "endpoint": "source",
    "filters": [],
}

ROWS = []


def rec(cid, ok, **extra):
    row = {"id": cid, "ok": bool(ok)}
    row.update(extra)
    ROWS.append(row)
    return bool(ok)


def host_obs(**kw):
    body = {"requestId": "req1_" + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
    body.update(kw)
    return body


def ep(universe, kind, nid, manifest=None):
    row = {"universe": universe, "kind": kind, "nativeSubjectId": nid}
    if manifest is not None:
        row["packageManifestPath"] = manifest
    return row


def request(operation, project, view, params, *, completeness="required", size=100):
    return {
        "completeness": completeness,
        "operation": operation,
        "page": {"size": size},
        "params": params,
        "projectId": project,
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "view": view,
    }


def neighbors(run, objects, blobs, actual, relation, min_res, direction, endpoint, host=None):
    used = host if host is not None else host_obs(latestRunId=actual["runId"])
    if "requestId" not in used:
        used = dict(host_obs(), **used)
    return Q.execute_graph_query(
        request(
            "graph.neighbors",
            run["projectId"],
            {"runId": actual["runId"]},
            {
                "relation": relation,
                "minResolution": min_res,
                "direction": direction,
                "endpoint": endpoint,
            },
        ),
        run,
        objects,
        blobs,
        host=used,
    )


def proof_of(run, objects):
    return objects[objects[run["evaluationSealId"]][1]["proofBundleId"]][1]


def subject_values(run, objects):
    out = {}
    for p in proof_of(run, objects)["predicateProofs"]:
        if p["predicateId"] == "p":
            out[p["subjectId"]] = {
                "value": p["value"],
                "witnessDigest": p["witnessDigest"],
                "operation": p["operation"],
                "subjectId": p["subjectId"],
            }
    return out


def witness_of(run, objects, blobs, subject_id):
    pred = subject_values(run, objects)[subject_id]
    w = C.parse(blobs[pred["witnessDigest"]])
    return pred, w


def by_native(items, nid, path=None):
    hits = [
        i
        for i in items
        if i["row"]["nativeSubjectId"] == nid and (path is None or i["row"]["path"] == path)
    ]
    if len(hits) != 1:
        raise AssertionError("lookup %s path=%s count=%d" % (nid, path, len(hits)))
    return hits[0]


def file_items(graph, universe=None):
    items = [i for i in graph["inputs"]["population"].values() if i["kind"] == "file"]
    if universe is not None:
        items = [i for i in items if i["universe"] == universe]
    return items


def symbol_items(graph, universe=None):
    items = [i for i in graph["inputs"]["population"].values() if i["kind"] == "symbol"]
    if universe is not None:
        items = [i for i in items if i["universe"] == universe]
    return items


def imports_scope_subjects(objects):
    found = []
    for key, (domain, rec) in objects.items():
        if domain != "subject-scope":
            continue
        if rec.get("relation") == "imports":
            found.append({"id": key, "subjects": list(rec.get("subjects") or [])})
    return found


def close_mode(occupancy, subject_kind, atom=None):
    g = S.build_ts_semantic_graph(
        atom=atom or IMPORTS_EXISTS,
        subject_kind=subject_kind,
        has_declares=False,
        has_references_fact=False,
        second_partition=False,
        imports_occupancy=occupancy,
    )
    run, objects, blobs, actual = replay.close_positive(g)
    return g, run, objects, blobs, actual


def inspect_signatures():
    recon = inspect.signature(AM._reconcile_attribution)
    eph = inspect.signature(AM._ephemeral_target)
    rec(
        "coord-reconcile-signature",
        list(recon.parameters) == ["fact", "spec", "inputs"],
        signature=str(recon),
        parameters=list(recon.parameters),
    )
    rec(
        "coord-ephemeral-signature",
        list(eph.parameters) == ["fact", "spec", "inputs"],
        signature=str(eph),
        parameters=list(eph.parameters),
    )
    rec(
        "coord-atom-admission-error-key",
        hasattr(AM.AtomAdmissionError("TARGET_ATTRIBUTION_SCHEMA_VERSION"), "key"),
        key_sample=AM.AtomAdmissionError("TARGET_ATTRIBUTION_SCHEMA_VERSION").key,
    )
    rec(
        "coord-query-imports-private-reconcile",
        "atom_model._reconcile_attribution" in (Q.__doc__ or ""),
        note="query model still names the private helper in its module docstring; contract cites atom §2",
    )


def census_default_mapped_file():
    g, run, objects, blobs, actual = close_mode("mapped-file", "file")
    scopes = imports_scope_subjects(objects)
    subjects = sorted({s for row in scopes for s in row["subjects"]})
    rec(
        "census-default-imports-scope-includes-foo-and-bar",
        subjects == sorted([g["foo"], g["bar"]]),
        subjects=subjects,
        foo=g["foo"],
        bar=g["bar"],
        note="author claimed default mapped-file fixture unchanged; imports source census is foo+bar",
    )
    rec(
        "census-default-mapped-file-payload-still-file-a-ts",
        True,
        occupancy="mapped-file",
    )
    a_ts = by_native(file_items(g, g["u1"]), "a.ts")
    pred, w = witness_of(run, objects, blobs, a_ts["subjectId"])
    rec(
        "mapped-file-atom-a-ts-true-with-matching-facts",
        pred["value"] == "true" and len(w.get("matchingFactIds") or []) >= 1,
        value=pred["value"],
        matchingFactIds=w.get("matchingFactIds"),
        uncertainFactIds=w.get("uncertainFactIds"),
        verdict=actual["verdict"],
        findingCount=actual["findingCount"],
    )
    q = neighbors(
        run,
        objects,
        blobs,
        actual,
        "imports",
        "resolved-target",
        "incoming",
        ep(g["u1"], "file", "a.ts"),
    )
    items = q["items"]
    rec(
        "mapped-file-query-incoming-a-ts-inventory-spelling",
        len(items) == 1
        and items[0]["target"]["nativeSubjectId"] == "a.ts"
        and items[0]["target"]["kind"] == "file"
        and "file:a.ts" not in items[0]["target"]["nativeSubjectId"]
        and items[0]["source"]["nativeSubjectId"] == g["foo"],
        items=items,
    )
    rec(
        "mapped-file-query-fact-is-atom-matching-fact",
        items and items[0]["factId"] in (w.get("matchingFactIds") or []),
        queryFact=items[0]["factId"] if items else None,
        matchingFactIds=w.get("matchingFactIds"),
    )
    rec(
        "mapped-file-target-universe-equals-fact-target",
        items and items[0]["target"]["universe"] == g["u1"],
        universe=items[0]["target"]["universe"] if items else None,
        u1=g["u1"],
    )
    return g, run, objects, blobs, actual


def exact_id_agreement():
    g, run, objects, blobs, actual = close_mode("exact-id-symbol", "symbol")
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    pred, w = witness_of(run, objects, blobs, foo["subjectId"])
    q = neighbors(
        run,
        objects,
        blobs,
        actual,
        "imports",
        "resolved-target",
        "incoming",
        ep(g["u1"], "symbol", g["foo"]),
    )
    items = q["items"]
    rec(
        "exact-id-atom-foo-true-matching-facts",
        pred["value"] == "true" and len(w.get("matchingFactIds") or []) >= 1,
        value=pred["value"],
        matchingFactIds=w.get("matchingFactIds"),
        uncertainFactIds=w.get("uncertainFactIds"),
        verdict=actual["verdict"],
        findingCount=actual["findingCount"],
    )
    rec(
        "exact-id-query-incoming-foo-from-bar",
        len(items) == 1
        and items[0]["source"]["nativeSubjectId"] == g["bar"]
        and items[0]["target"]["nativeSubjectId"] == g["foo"]
        and items[0]["target"]["kind"] == "symbol",
        items=items,
    )
    rec(
        "exact-id-query-fact-is-atom-matching-fact",
        items and items[0]["factId"] in (w.get("matchingFactIds") or []),
        queryFact=items[0]["factId"] if items else None,
        matchingFactIds=w.get("matchingFactIds"),
    )
    rec(
        "exact-id-no-sidecar-selected",
        not any(
            r.get("domain") == "target-attribution"
            for r in proof_of(run, objects).get("evaluationInputRefs") or []
        ),
        refs=[r for r in proof_of(run, objects).get("evaluationInputRefs") or [] if r.get("domain") == "target-attribution"],
    )
    return g, run, objects, blobs, actual


def unknown_sidecar_agreement():
    g, run, objects, blobs, actual = close_mode("unknown-sidecar-symbol", "symbol")
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    pred, w = witness_of(run, objects, blobs, foo["subjectId"])
    forged = dict(host_obs(latestRunId=actual["runId"]), targetAttributions={"forged": True}, cache={"edges": ["lie"]}, standing={"graph": True})
    q = neighbors(
        run,
        objects,
        blobs,
        actual,
        "imports",
        "resolved-target",
        "incoming",
        ep(g["u1"], "symbol", g["foo"]),
        host=forged,
    )
    items = q["items"]
    rec(
        "unknown-sidecar-atom-foo-true-matching-facts",
        pred["value"] == "true" and len(w.get("matchingFactIds") or []) >= 1,
        value=pred["value"],
        matchingFactIds=w.get("matchingFactIds"),
        uncertainFactIds=w.get("uncertainFactIds"),
        verdict=actual["verdict"],
        findingCount=actual["findingCount"],
    )
    rec(
        "unknown-sidecar-does-not-erase-exact-id-query",
        len(items) == 1 and items[0]["target"]["nativeSubjectId"] == g["foo"],
        items=items,
    )
    rec(
        "unknown-sidecar-query-fact-is-atom-matching-fact",
        items and items[0]["factId"] in (w.get("matchingFactIds") or []),
        queryFact=items[0]["factId"] if items else None,
        matchingFactIds=w.get("matchingFactIds"),
    )
    rec(
        "host-cache-standing-attributions-do-not-change-occupancy",
        len(items) == 1,
        items=items,
    )
    return g, run, objects, blobs, actual


def unmapped_honest_omission():
    g, run, objects, blobs, actual = close_mode("unmapped-file", "file")
    a_ts = by_native(file_items(g, g["u1"]), "a.ts")
    pred, w = witness_of(run, objects, blobs, a_ts["subjectId"])
    out = neighbors(
        run,
        objects,
        blobs,
        actual,
        "imports",
        "resolved-target",
        "outgoing",
        ep(g["u1"], "symbol", g["foo"]),
    )
    inc = neighbors(
        run,
        objects,
        blobs,
        actual,
        "imports",
        "resolved-target",
        "incoming",
        ep(g["u1"], "file", "a.ts"),
    )
    lims = out["context"]["evidence"]["resolutionLimitations"]
    rec(
        "unmapped-atom-a-ts-not-known-true",
        pred["value"] != "true",
        value=pred["value"],
        matchingFactIds=w.get("matchingFactIds"),
        uncertainFactIds=w.get("uncertainFactIds"),
        verdict=actual["verdict"],
        findingCount=actual["findingCount"],
    )
    rec(
        "unmapped-atom-is-unknown-not-false-none",
        pred["value"] == "indeterminate",
        value=pred["value"],
        note="findingCount 0 is not a known miss; occupancy unknown must not become payload-inequality nomatch",
    )
    rec(
        "unmapped-query-outgoing-unprojectable-not-edge",
        out["items"] == [] and any(x.get("kind") == "unprojectable-fact" for x in lims),
        items=out["items"],
        limitations=lims,
    )
    rec(
        "unmapped-empty-incoming-is-not-negative-proof",
        inc["items"] == [] and inc["termination"]["class"] == "success",
        items=inc["items"],
        termination=inc["termination"],
        note="zero neighbors is not native none; atom value remains indeterminate",
    )
    rec(
        "unmapped-no-sidecar-selected",
        not any(
            r.get("domain") == "target-attribution"
            for r in proof_of(run, objects).get("evaluationInputRefs") or []
        ),
    )
    return g, run, objects, blobs, actual


def single_kind_unknown_still_projects():
    g = S.build_ts_semantic_graph(
        atom=REFS_EXISTS_SRC,
        subject_kind="symbol",
        has_declares=False,
        has_references_fact=True,
        second_partition=True,
        references_resolved=True,
        target_sidecar=False,
    )
    run, objects, blobs, actual = replay.close_positive(g)
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    pred, w = witness_of(run, objects, blobs, foo["subjectId"])
    q = neighbors(
        run,
        objects,
        blobs,
        actual,
        "references",
        "resolved-binding",
        "outgoing",
        ep(g["u1"], "symbol", g["foo"]),
    )
    rec(
        "single-kind-references-atom-foo-true",
        pred["value"] == "true" and len(w.get("matchingFactIds") or []) >= 1,
        value=pred["value"],
        matchingFactIds=w.get("matchingFactIds"),
    )
    rec(
        "single-kind-unknown-or-absent-sidecar-still-projects-payload-id",
        len(q["items"]) >= 1 and q["items"][0]["source"]["nativeSubjectId"] == g["foo"],
        items=q["items"],
        note="single-kind table kind is the target kind; unknown occupancy still projects payload native id",
    )
    if q["items"]:
        rec(
            "single-kind-query-fact-is-atom-matching-fact",
            q["items"][0]["factId"] in (w.get("matchingFactIds") or []),
            queryFact=q["items"][0]["factId"],
            matchingFactIds=w.get("matchingFactIds"),
        )
    return g, run, objects, blobs, actual


def isolated_package_not_absence():
    g, run, objects, blobs, actual = close_mode("mapped-file", "file")
    pkgs = [i for i in g["inputs"]["population"].values() if i["kind"] == "package"]
    if not pkgs:
        rec("isolated-package-present", False, note="no package inventory row")
        return
    item = pkgs[0]
    q = neighbors(
        run,
        objects,
        blobs,
        actual,
        "imports",
        "resolved-target",
        "incoming",
        ep(item["universe"], "package", item["row"]["nativeSubjectId"], item["row"]["path"]),
    )
    rec(
        "isolated-package-empty-neighbors-not-absence",
        q["items"] == [] and q["termination"]["class"] == "success",
        items=q["items"],
        package=item["row"]["nativeSubjectId"],
        path=item["row"]["path"],
    )
    try:
        neighbors(
            run,
            objects,
            blobs,
            actual,
            "imports",
            "resolved-target",
            "incoming",
            ep(item["universe"], "package", item["row"]["nativeSubjectId"]),
        )
        rec("package-missing-manifest-path-ambiguous-or-malformed", False, note="expected QueryRefusal")
    except Q.QueryRefusal as exc:
        rec(
            "package-missing-manifest-path-ambiguous-or-malformed",
            exc.detail in ("QUERY.ENDPOINT_AMBIGUOUS", "QUERY.PARAMS_MALFORMED"),
            error=exc.error_code,
            detail=exc.detail,
        )


def v1_helper_vs_fullrun():
    g, run, objects, blobs, actual = close_mode("mapped-file", "file")
    proof = proof_of(run, objects)
    plan = objects[run["planId"]][1]
    evidence = objects[run["evidenceId"]][1]
    views = evidence.get("viewIds") or []
    table = Q.projection_table()[("imports", "resolved-target")]
    occupancy_inputs = Q.occupancy_inputs_from_retained(proof, plan, objects, blobs)
    sidecars = occupancy_inputs.get("targetAttributions") or {}
    rec("v1-probe-has-selected-v2-sidecar", bool(sidecars), count=len(sidecars))
    # Helper path: replace sidecar with schemaVersion=1 in occupancy inputs only.
    helper_inputs = copy.deepcopy(occupancy_inputs)
    v1_map = {}
    for fid, sc in helper_inputs["targetAttributions"].items():
        v1 = dict(sc)
        v1.pop("evaluationNativeId", None)
        v1["schemaVersion"] = 1
        v1_map[fid] = v1
        helper_inputs["targetAttributions"][fid] = v1
    helper_catch = None
    helper_occ = None
    fid = next(iter(v1_map))
    fact = dict(objects[fid][1])
    payload = Q._blob_payload(blobs, fact["payloadDigest"], fid)
    fact["payload"] = payload
    fact["factId"] = fid
    try:
        helper_occ = Q._reconcile_fact_occupancy(fact, helper_inputs)
        helper_kind = "returned"
    except AM.AtomAdmissionError as exc:
        helper_kind = "AtomAdmissionError"
        helper_catch = {"type": type(exc).__name__, "key": exc.key, "msg": str(exc)}
    except Exception as exc:
        helper_kind = type(exc).__name__
        helper_catch = {"type": type(exc).__name__, "msg": str(exc)}
    rec(
        "helper-v1-sidecar-raises-atom-admission",
        helper_kind == "AtomAdmissionError" and (helper_catch or {}).get("key") == "TARGET_ATTRIBUTION_SCHEMA_VERSION",
        helper_kind=helper_kind,
        helper_catch=helper_catch,
        helper_occ=helper_occ,
        standing="helper-only; not complete close_run proof",
    )
    projected, limits, _, _ = Q.collect_projected_edges(views, objects, blobs, table, helper_inputs)
    v1_omitted = [x for x in limits if x.get("kind") == "unprojectable-fact" and "TARGET_ATTRIBUTION_SCHEMA_VERSION" in str(x.get("note"))]
    rec(
        "helper-collect-projected-edges-downgrades-v1-to-unprojectable",
        bool(v1_omitted) and projected == [],
        projectedCount=len(projected),
        v1_omitted=v1_omitted,
        limitations=limits,
        standing="helper-only defensive branch inside collect_projected_edges",
    )
    # Public execute_graph_query + complete close_run: mutate selected sidecar bytes to V1
    # at a new digest and rewrite proof evaluationInputRefs. close_run must refuse; query
    # must not return omitted-edge success.
    mutated_objects = copy.deepcopy(objects)
    mutated_blobs = copy.deepcopy(blobs)
    mutated_run = copy.deepcopy(run)
    proof_key = mutated_objects[mutated_run["evaluationSealId"]][1]["proofBundleId"]
    mutated_proof = copy.deepcopy(mutated_objects[proof_key][1])
    new_refs = []
    replaced = 0
    for ref in mutated_proof.get("evaluationInputRefs") or []:
        if ref.get("domain") != "target-attribution":
            new_refs.append(ref)
            continue
        raw = mutated_blobs[ref["digest"]]
        sc = C.parse(raw)
        v1 = dict(sc)
        v1.pop("evaluationNativeId", None)
        v1["schemaVersion"] = 1
        v1_raw = C.canonical(v1)
        v1_digest = hashlib.sha256(v1_raw).hexdigest()
        mutated_blobs[v1_digest] = v1_raw
        new_refs.append({"domain": "target-attribution", "digest": v1_digest})
        replaced += 1
    mutated_proof["evaluationInputRefs"] = new_refs
    mutated_objects[proof_key] = ("proof-bundle", mutated_proof)
    rec("fullrun-v1-mutation-replaced-sidecar-refs", replaced >= 1, replaced=replaced)
    public_kind = None
    public_detail = None
    public_error = None
    public_items = None
    public_lims = None
    try:
        pub = Q.execute_graph_query(
            request(
                "graph.neighbors",
                mutated_run["projectId"],
                {"runId": actual["runId"]},
                {
                    "relation": "imports",
                    "minResolution": "resolved-target",
                    "direction": "incoming",
                    "endpoint": ep(g["u1"], "file", "a.ts"),
                },
            ),
            mutated_run,
            mutated_objects,
            mutated_blobs,
            host=host_obs(latestRunId=actual["runId"]),
        )
        public_kind = "success-body"
        public_items = pub.get("items")
        public_lims = (pub.get("context") or {}).get("evidence", {}).get("resolutionLimitations")
    except Q.QueryRefusal as exc:
        public_kind = "QueryRefusal"
        public_error = exc.error_code
        public_detail = exc.detail
        term = exc.termination()
        rec(
            "fullrun-v1-query-refusal-termination",
            True,
            termination=term,
            klass=term.get("class"),
        )
    except Exception as exc:
        public_kind = type(exc).__name__
        public_error = str(exc)[:300]
    rec(
        "fullrun-v1-cannot-reach-omitted-edge",
        public_kind == "QueryRefusal" and public_detail != "unprojectable-fact",
        public_kind=public_kind,
        public_error=public_error,
        public_detail=public_detail,
        public_items=public_items,
        public_lims=public_lims,
        note="complete close_run refuses selected V1; public query must not emit unprojectable-fact success",
    )
    rec(
        "fullrun-v1-is-admission-failure-not-success-omission",
        public_kind == "QueryRefusal"
        and public_error == "HOST.IO_FAILURE"
        and public_detail in ("evidence.corrupt", "evidence.missing"),
        public_kind=public_kind,
        public_error=public_error,
        public_detail=public_detail,
    )
    # Direct close_run on mutated closure.
    close_kind = None
    close_msg = None
    try:
        Q.identity3().close_run(mutated_run, mutated_objects, mutated_blobs)
        close_kind = "ADMIT"
    except Exception as exc:
        close_kind = type(exc).__name__
        close_msg = str(exc)[:400]
    rec(
        "fullrun-close-run-refuses-selected-v1",
        close_kind != "ADMIT",
        close_kind=close_kind,
        close_msg=close_msg,
    )
    rec(
        "v1-helper-downgrade-is-not-fullrun-behavior",
        bool(v1_omitted) and public_kind == "QueryRefusal" and close_kind != "ADMIT",
        note="preserve helper failure; do not treat collect_projected_edges catch as whole-Run proof",
    )


def occupancy_inputs_ignore_unselected_and_host():
    g, run, objects, blobs, actual = close_mode("exact-id-symbol", "symbol")
    proof = proof_of(run, objects)
    plan = objects[run["planId"]][1]
    occ = Q.occupancy_inputs_from_retained(proof, plan, objects, blobs)
    rec(
        "occupancy-inputs-keys",
        set(occ) == {"enumerationPlan", "inventories", "targetAttributions", "closures"},
        keys=sorted(occ),
    )
    rec(
        "occupancy-inputs-no-host-cache-key",
        "cache" not in occ and "standing" not in occ,
        keys=sorted(occ),
    )
    rec(
        "exact-id-occupancy-inputs-have-inventories-no-sidecar",
        bool(occ.get("inventories")) and not occ.get("targetAttributions"),
        inventoryCount=len(occ.get("inventories") or []),
        attributionCount=len(occ.get("targetAttributions") or {}),
    )


def extra_graph_kinds_absent():
    table = Q.projection_table()
    rec(
        "no-extra-graph-kinds-or-aliases",
        set(table)
        == {
            ("calls", "resolved-callee"),
            ("references", "resolved-binding"),
            ("imports", "resolved-target"),
            ("control-flow", "syntactic"),
            ("reachability", "from-resolved-calls"),
        },
        table=sorted("%s@%s" % k for k in table),
    )


def none_atom_mapped_file_false_on_hit():
    g, run, objects, blobs, actual = close_mode("mapped-file", "file", atom=IMPORTS_NONE)
    a_ts = by_native(file_items(g, g["u1"]), "a.ts")
    pred, w = witness_of(run, objects, blobs, a_ts["subjectId"])
    rec(
        "mapped-file-none-atom-a-ts-false",
        pred["value"] == "false" and len(w.get("matchingFactIds") or []) >= 1,
        value=pred["value"],
        matchingFactIds=w.get("matchingFactIds"),
        verdict=actual["verdict"],
        findingCount=actual["findingCount"],
    )


def main():
    steps = [
        inspect_signatures,
        extra_graph_kinds_absent,
        census_default_mapped_file,
        exact_id_agreement,
        unknown_sidecar_agreement,
        unmapped_honest_omission,
        single_kind_unknown_still_projects,
        isolated_package_not_absence,
        occupancy_inputs_ignore_unselected_and_host,
        none_atom_mapped_file_false_on_hit,
        v1_helper_vs_fullrun,
    ]
    for fn in steps:
        try:
            fn()
        except Exception as exc:
            rec(
                "probe-exception:" + fn.__name__,
                False,
                error=type(exc).__name__ + ": " + str(exc)[:400],
                traceback=traceback.format_exc()[-2000:],
            )
    failed = [r for r in ROWS if not r["ok"]]
    report = {
        "standing": (
            "independent occupancy probes over disposable copy; public execute_graph_query "
            "and complete close_run distinguished from helper-only collect_projected_edges / "
            "_reconcile_fact_occupancy; not pin-gated global suite; not compiler qualification"
        ),
        "passed": not failed,
        "count": len(ROWS),
        "failedCount": len(failed),
        "failed": failed,
        "checks": ROWS,
    }
    dest = OUT / "receipts" / "independent-probes.json"
    dest.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"passed": report["passed"], "count": report["count"], "failedCount": report["failedCount"], "failedIds": [r["id"] for r in failed]}, indent=2))
    if failed:
        raise SystemExit(1)
    return report


if __name__ == "__main__":
    main()
