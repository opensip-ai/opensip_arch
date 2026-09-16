"""Stage 4: contract 5's "lawful construction" for the stage-2 D1 shape, made closable.

F5 (stage 3) showed that the maintained host-capture builder only captures ATTRIBUTED views, so a
per-universe references view at a universe with no references binding is dropped from the receipt and
selectedRefs while the Run's evidence still names it (EVALUATION_VIEW_ROOTS). Contract 1 says the
stage-produced refs are the union of complete receipt outputRefs, and contract 5 says a captured view
no selected binding resolves is not restricted. This host encoding captures it in the receipt and in
selectedRefs (with its Coverage) and attributes it to no row, then runs admission and the maintained
closed-run driver. Standing as stage 2/3."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_mutation as X  # noqa: E402

R = X.Recorder()
KW_UM = dict(unsupported_cell="required", multiple_universes=True)

G = X.build(**KW_UM)
U0 = X.binding_universe(G, "references")
U1 = X.other_universe(G, U0)
s_b = X.mint_scope(G, "references", "resolved-binding", U1, [])
c_b = X.mint_coverage(G, s_b, U1)
vb = X.mint_view(G, [s_b], [], [c_b])
X.replace_views(G, [], [vb])


def _capture_unattributed(kw):
    ei = kw["execution_inputs"]
    vh, ch = X.K.hx(vb), X.K.hx(c_b)
    for rc in ei["hostCapture"]["stageReceipts"]:
        if "view" in rc["outputDomains"]:
            rc["outputRefs"] = X.K.canon_refs(rc["outputRefs"] + [{"domain": "view", "digest": vh}])
    ei["selectedRefs"] = X.K.canon_refs(ei["selectedRefs"] + [{"domain": "view", "digest": vh},
                                                              {"domain": "coverage", "digest": ch}])


R.world("F5x-lawful-split-unattributed-view-captured", G, host_edit=_capture_unattributed,
        note="U0 references view on the unsupported row; separate U1 references view captured, attributed to no row")
R.report("receipts/stage4-lawful-split.json")
