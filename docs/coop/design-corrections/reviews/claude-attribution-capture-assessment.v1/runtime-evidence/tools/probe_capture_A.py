"""Probe A: does the maintained host-capture builder capture the explicit returned views it is given?

Distinguishes three kinds of view presence in the builder INPUT graph:
  store census          - a view object exists in graph['objects'] only
  explicit view ids     - graph['viewIds'] (normalize_graph input; also the Run's semantic-evidence viewIds)
  explicit refs         - inputs.evaluationInputRefs view refs (normalize_graph 'existing evaluationInputRefs')
Then, for the builder's own manifest: receipt outputRefs, selectedRefs, rows, the admission result and the
closed Run through the maintained driver (whose seal step calls attach_host_capture = this same builder).

Also probes the receipts-vs-selectedRefs law on host-authored manifests (labelled as such)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pc  # noqa: E402

R = pc.Recorder()
UM = dict(unsupported_cell="required", multiple_universes=True)

G0 = pc.build(**UM)
R.world("A0-control-maintained-world-unmutated", G0, note="unsupported references@U0 + inventory@U0/U1")


def world_with_unattributed(in_view_ids, in_refs, in_store=True):
    G = pc.build(**UM)
    U0 = pc.binding_universe(G, "references")
    U1 = pc.other_universe(G, U0)
    s = pc.mint_scope(G, "references", "resolved-binding", U1)
    c = pc.mint_coverage(G, s, U1)
    v = pc.mint_view(G, [s], (), [c])
    if in_view_ids or in_refs:
        pc.set_views(G, add=[v], in_view_ids=in_view_ids, in_refs=in_refs)
    return G, v


G, v = world_with_unattributed(True, True)
R.world("A1-explicit-returned-view-in-viewIds-and-refs-no-cell-owns-it", G, watch=[v],
        note="references@U1 view with admitted Coverage; no references binding at U1; declared returned and selected")
G, v = world_with_unattributed(True, False)
R.world("A2-explicit-returned-view-in-viewIds-only", G, watch=[v])
G, v = world_with_unattributed(False, True)
R.world("A3-explicit-selected-view-in-evaluationInputRefs-only", G, watch=[v])
G, v = world_with_unattributed(False, False)
e = R.world("A4-store-census-only-view-object", G, watch=[v],
            note="ambient object: must not be captured and must not change C(ExecutionInputs)")
e["x-digestEqualsA0"] = e.get("manifestDigest") == R.results["A0-control-maintained-world-unmutated"].get("manifestDigest")


def world_with_attributed_extra():
    G = pc.build(**UM)
    U0 = pc.binding_universe(G, "inventory", 0)
    s = pc.mint_scope(G, "file", "enumerated", U0, ["README.md"])
    c = pc.mint_coverage(G, s, U0)
    v = pc.mint_view(G, [s], (), [c])
    pc.set_views(G, add=[v])
    return G, v


G, v = world_with_attributed_extra()
R.world("A5-control-explicit-returned-view-that-a-cell-owns", G, watch=[v],
        note="second file@enumerated partition at U0, one subject, complete Coverage")

# ---- receipts vs selectedRefs (host-authored manifests over the unmutated maintained world) ----
G = pc.build(**UM)
kw0 = pc.K.manifest_from_owner(pc.copy.deepcopy(G))
victim = "view2:" + kw0["execution_inputs"]["cellOutcomes"][0]["viewDigests"][0]


def drop_from_receipt(manifest):
    h = pc.K.hx(victim)
    for rc in manifest["hostCapture"]["stageReceipts"]:
        rc["outputRefs"] = [r for r in rc["outputRefs"] if r["digest"] != h]


R.world("S1-host-attributed-view-on-selectedRefs-and-row-but-on-no-receipt", G, watch=[victim], host_edit=drop_from_receipt,
        note="contract 1: stage-produced selectedRefs == union of complete receipt outputRefs")


def drop_from_selected(manifest):
    h = pc.K.hx(victim)
    manifest["selectedRefs"] = [r for r in manifest["selectedRefs"] if not (r["domain"] == "view" and r["digest"] == h)]


R.world("S2-host-view-on-receipt-and-row-but-not-selectedRefs", G, watch=[victim], host_edit=drop_from_selected)

R.report("receipts/probe-A-capture.json")
