"""Probe B: shared view across TWO capability cells on the SAME program/U, plus a captured view matching
neither cell, on the maintained TypeScript semantic fixture (inventory + syntax at ts-tsconfig, one binding
each at u1, SubjectIdV1 symbol ids, owner-admitted declares/literal/control-flow/file/package Coverage).

Closed Runs use the maintained semantic driver shape (check-semantic-replay.v3.close_positive: seed_seal ->
open_run_closure -> R.derive -> seal_derived -> R.replay -> close_run) and report exactManifest.

Probe P: relation-column vs [relation, resolution]-pair membership, on the file fixture's UNSUPPORTED-TYPED
references@syntax-only row (matrix pair references@resolved-binding; ladder also has syntactic-name-match).
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pc  # noqa: E402

K, H, S, M = pc.K, pc.H, pc.K.S, pc.M
DECLARES = {"op": "exists", "relation": "declares", "minResolution": "syntactic", "filters": []}


def semantic_closed_run(G, manifest):
    want = M.raw_digest(manifest)
    try:
        g = copy.deepcopy(G)
        seed, objects, blobs, _ = S.seed_seal(g)
        _, owner = K.IDENTITY.open_run_closure(seed, objects, blobs)
        i = g["inputs"]
        out = K.R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"], i["evaluationInputRefs"], objects, blobs, owner)
        run, objects, blobs = S.seal_derived(g, out, objects, blobs)
        actual = K.R.replay(run, objects, blobs)
        run_id = K.IDENTITY.close_run(run, objects, blobs)
        if run_id != actual["runId"]:
            raise AssertionError("close_run runId != replay runId")
    except Exception as exc:  # noqa: BLE001
        return {"standing": "closed-run (semantic driver)", "ran": False, "exception": type(exc).__name__ + ":" + str(exc)[:700]}
    proof = out["proof"]
    return {"standing": "closed-run (semantic driver)", "ran": True, "verdict": actual["verdict"], "runId": run_id,
            "executionCauses": sorted(d["cause"] for d in proof.get("executionDeficiencies") or []),
            "proofExecutionInputsDigest": proof["executionInputsDigest"], "exactManifest": proof["executionInputsDigest"] == want}


def semantic_world(R, name, G, *, watch=(), host_edit=None, note=None):
    entry = {"note": note, "tree": str(pc.TREE)}
    try:
        kw = H.admission_kwargs(copy.deepcopy(G))
        manifest = kw["execution_inputs"]
        entry["manifestSource"] = "builder"
        if host_edit is not None:
            host_edit(manifest)
            kw["store_pointers"] = M.promised_pointers(manifest, kw["plan"], kw["execution_plan"], kw["enumeration_plan"],
                                                       objects=kw["objects"], blobs=kw["blobs"])["store_pointers"]
            entry["manifestSource"] = "host-authored (builder output edited)"
        entry["manifestDigest"] = M.raw_digest(manifest)
        entry["rows"] = pc.rows(manifest)
        entry["graphViewIdCount"] = len(G["viewIds"])
        entry["receiptViewCount"] = sum(1 for rc in manifest["hostCapture"]["stageReceipts"] for r in rc["outputRefs"] if r["domain"] == "view")
        entry["selectedViewCount"] = sum(1 for r in manifest["selectedRefs"] if r["domain"] == "view")
        entry["watch"] = {pc.short(v): pc.manifest_facts(manifest, v) for v in watch}
        res = M.admit_execution_inputs(**kw)
        entry["admission"] = {"result": res.get("result"), "refusals": res.get("refusals"),
                              "derivedOutcomeStates": [d.get("state") for d in res.get("derivedOutcomes") or []],
                              "derivedAccountStates": [[d.get("relation"), d.get("accountState")] for d in res.get("derivedAccounts") or []]}
        GG = copy.deepcopy(G)
        if host_edit is not None:
            pc.attach_exact(GG, manifest)
        entry["closedRun"] = semantic_closed_run(GG, manifest)
    except Exception as exc:  # noqa: BLE001
        entry["probeError"] = type(exc).__name__ + ":" + str(exc)[:700]
        entry["traceback"] = pc.traceback.format_exc()[-2500:]
    R.add(name, entry)
    return entry


def capture(view_id):
    def edit(manifest):
        h = K.hx(view_id)
        if not any(r["digest"] == h for rc in manifest["hostCapture"]["stageReceipts"] for r in rc["outputRefs"]):
            for rc in manifest["hostCapture"]["stageReceipts"]:
                if "view" in rc["outputDomains"]:
                    rc["outputRefs"] = K.canon_refs(rc["outputRefs"] + [{"domain": "view", "digest": h}])
        have = {(r["domain"], r["digest"]) for r in manifest["selectedRefs"]}
        add = [{"domain": "view", "digest": h}] + [{"domain": "coverage", "digest": K.hx(c)}
                                                   for c in G_objects[0][view_id][1]["coverageIds"]]
        manifest["selectedRefs"] = K.canon_refs(manifest["selectedRefs"] + [r for r in add if (r["domain"], r["digest"]) not in have])
    return edit


G_objects = []
R = pc.Recorder()

G0 = S.build_ts_semantic_graph(atom=DECLARES)
semantic_world(R, "B0-control-semantic-declares-two-cells-unmutated", G0)


def shared_world(with_neither):
    G = S.build_ts_semantic_graph(atom=DECLARES)
    u1 = G["u1"]
    v_file, v_decl = pc.single_view(G, "file", u1), pc.single_view(G, "declares", u1)
    fv, dv = G["objects"][v_file][1], G["objects"][v_decl][1]
    shared = pc.mint_view(G, fv["scopeIds"] + dv["scopeIds"], fv["facts"] + dv["facts"], fv["coverageIds"] + dv["coverageIds"])
    add = [shared]
    neither = None
    if with_neither:
        s = pc.mint_scope(G, "references", "resolved-binding", u1, [G["foo"]])
        c = pc.mint_coverage(G, s, u1)
        neither = pc.mint_view(G, [s], (), [c])
        add.append(neither)
    pc.set_views(G, retire=[v_file, v_decl], add=add)
    return G, shared, neither


G1, shared1, _ = shared_world(False)
G_objects[:] = [G1["objects"]]
semantic_world(R, "B1-shared-file+declares-view-across-inventory-and-syntax", G1, watch=[shared1],
               note="one provider view carrying an inventory partition (file, facts) and a syntax partition (declares, facts)")


def omit_from_syntax(v):
    def edit(manifest):
        for r in manifest["cellOutcomes"]:
            if r["capabilityId"] == "syntax":
                r["viewDigests"] = [h for h in r["viewDigests"] if h != K.hx(v)]
    return edit


semantic_world(R, "B1x-host-alt-syntax-row-omits-shared-view", G1, watch=[shared1], host_edit=omit_from_syntax(shared1))

G2, shared2, neither2 = shared_world(True)
G_objects[:] = [G2["objects"]]
semantic_world(R, "B2-builder-shared-view-plus-returned-view-matching-neither-cell", G2, watch=[shared2, neither2],
               note="references@resolved-binding view at u1 (owner-admitted Coverage) declared in viewIds and evaluationInputRefs; no references cell")
semantic_world(R, "B2h-host-captures-the-neither-view-exactly", G2, watch=[shared2, neither2], host_edit=capture(neither2),
               note="same graph; host manifest = builder output + that view on the complete receipt and selectedRefs (+ its Coverage)")


def name_neither_on_inventory(v):
    base = capture(v)

    def edit(manifest):
        base(manifest)
        for r in manifest["cellOutcomes"]:
            if r["capabilityId"] == "inventory":
                r["viewDigests"] = M.canon_str_list(r["viewDigests"] + [K.hx(v)])
    return edit


semantic_world(R, "B2y-host-captures-and-names-neither-view-on-inventory-row", G2, watch=[neither2],
               host_edit=name_neither_on_inventory(neither2))

# ---------------- P: relation column vs pair ----------------
UM = dict(unsupported_cell="required")
G = pc.build(**UM)
U0 = pc.binding_universe(G, "references")
s = pc.mint_scope(G, "references", "syntactic-name-match", U0)
try:
    c = pc.mint_coverage(G, s, U0)
    cov = [c]
except Exception as exc:  # noqa: BLE001 - preserved, and the view is then coverage-less
    R.add("P-note-coverage-for-syntactic-name-match", {"probeError": type(exc).__name__ + ":" + str(exc)[:500]})
    cov = []
v_rung = pc.mint_view(G, [s], (), cov)
pc.set_views(G, add=[v_rung])
e = R.world("P1-references-row-view-at-non-matrix-rung", G, watch=[v_rung],
            note="scope references@syntactic-name-match; matrix pair is references@resolved-binding")


def pair_reading(manifest):
    h = K.hx(v_rung)
    for r in manifest["cellOutcomes"]:
        if r["capabilityId"] == "references":
            r["viewDigests"] = [x for x in r["viewDigests"] if x != h]


R.world("P1y-host-alt-pair-membership-encoding", G, watch=[v_rung], host_edit=pair_reading,
        note="same graph and capture; references row omits the non-matrix-rung view")

R.report("receipts/" + (sys.argv[1] if len(sys.argv) > 1 else "probe-B-twocell-base.json"))
