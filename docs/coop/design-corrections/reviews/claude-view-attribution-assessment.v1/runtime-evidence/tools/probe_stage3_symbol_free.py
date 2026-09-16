"""Stage 3: (a) is stage 2's PAYLOAD_RECORD closed-run failure a BASELINE property of the symbol
worlds (unmutated)?  (b) the stage-2 C discriminators rebuilt in symbol-free maintained worlds whose
unmutated closed Runs are known to run (stage 2 D0 / A0)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_mutation as X  # noqa: E402

R = X.Recorder()
KW_SYM = dict(symbol_rows=[{"nativeSubjectId": "x"}])
KW_ASYM = dict(multiple_universes=True, symbol_rows=[{"nativeSubjectId": "x"}], symbol_only_second_program=True)

# (a) baseline: unmutated symbol worlds through the maintained full_run driver
R.closed_only("S0a-baseline-closed-run-symbol-rows-unmutated", X.build(**KW_SYM),
              note="same kwargs as maintained check-execution-inputs partial controls, but complete")
R.closed_only("S0b-baseline-closed-run-symbol-only-second-program-unmutated", X.build(**KW_ASYM))
R.closed_only("S0c-baseline-closed-run-default-unmutated", X.build())

# (b1) unsupported references@U0 row: a coverage-less FOREIGN-universe scope on its returned view
KW_UM = dict(unsupported_cell="required", multiple_universes=True)


def refs_view_plus_scope(scope_uni_role):
    G = X.build(**KW_UM)
    U0 = X.binding_universe(G, "references")
    U1 = X.other_universe(G, U0)
    v_ref = X.single_view(G, "references", U0)
    rv = G["objects"][v_ref][1]
    extra = X.mint_scope(G, "declares", "syntactic", U0 if scope_uni_role == "U0" else U1, [])
    nv = X.mint_view(G, rv["scopeIds"] + [extra], rv["facts"], rv["coverageIds"])
    X.replace_views(G, [v_ref], [nv])
    return G


R.world("F1-control-unsupported-view-plus-coverage-less-declares-scope-same-U", refs_view_plus_scope("U0"))
R.world("F1-unsupported-view-plus-coverage-less-declares-scope-foreign-U", refs_view_plus_scope("U1"),
        note="references@U0 row names a view whose second scope is at U1; no Coverage, no fact on it")


# (b2) same-scope discriminator on the unsupported row: U on one scope, relation on another
def refs_split_scopes(foreign):
    G = X.build(**KW_UM)
    U0 = X.binding_universe(G, "references")
    U1 = X.other_universe(G, U0)
    s_decl = X.mint_scope(G, "declares", "syntactic", U0, [])
    s_ref = X.mint_scope(G, "references", "resolved-binding", U1 if foreign else U0, [])
    v = X.mint_view(G, [s_decl, s_ref], [], [])
    X.replace_views(G, [], [v])
    return G, v


G, v = refs_split_scopes(False)
R.world("F2-control-references-relation-and-U-on-same-scope", G,
        note="declares@U0 + references@U0 (coverage-less): both recipes attribute to references@U0")
G_f2, v_f2 = refs_split_scopes(True)
R.world("F2-references-relation-and-U-on-different-scopes", G_f2,
        note="declares@U0 + references@U1 (coverage-less): separate booleans attribute to references@U0; "
             "a same-scope recipe attributes to no row (no references binding at U1)")


def _f2_same_scope(kw):
    row = X.row_by_cap(kw, "references")
    row["viewDigests"] = [h for h in row["viewDigests"] if h != X.K.hx(v_f2)]


R.world("F2y-host-alt-same-scope-encoding", G_f2, host_edit=_f2_same_scope,
        note="view stays captured in receipt + selectedRefs, attributed to no row")


# (b3) supported-available rows, two bound universes of the same capability
def inv_split_scopes(foreign):
    G = X.build(multiple_universes=True)
    U0 = X.binding_universe(G, "inventory", 0)
    U1 = X.binding_universe(G, "inventory", 1)
    s_ref = X.mint_scope(G, "references", "resolved-binding", U0, [])
    s_pkg = X.mint_scope(G, "package", "manifest-declared", U1 if foreign else U0, [])
    v = X.mint_view(G, [s_ref, s_pkg], [], [])
    X.replace_views(G, [], [v])
    return G, v


G, v = inv_split_scopes(False)
R.world("F3-control-inventory-U-and-relation-on-same-scope", G,
        note="references@U0 + package@U0 (coverage-less, the same package scope id as the owner's)")
G_f3, v_f3 = inv_split_scopes(True)
R.world("F3-inventory-U-and-relation-on-different-scopes", G_f3,
        note="references@U0 + package@U1 (coverage-less): separate booleans name it on inventory@U0 AND "
             "inventory@U1; a same-scope recipe names it on inventory@U1 only")


def _f3_same_scope(kw):
    row = X.row_by_cap(kw, "inventory", 0)
    row["viewDigests"] = [h for h in row["viewDigests"] if h != X.K.hx(v_f3)]


R.world("F3y-host-alt-same-scope-encoding", G_f3, host_edit=_f3_same_scope,
        note="identical graph; only inventory@U0 drops the view")


# (b4) supported rows: coverage-bearing U0 file view + coverage-less foreign references scope
def file_view_plus_foreign_scope():
    G = X.build(multiple_universes=True)
    U0 = X.binding_universe(G, "inventory", 0)
    U1 = X.binding_universe(G, "inventory", 1)
    v_file = X.single_view(G, "file", U0)
    fv = G["objects"][v_file][1]
    extra = X.mint_scope(G, "references", "resolved-binding", U1, [])
    nv = X.mint_view(G, fv["scopeIds"] + [extra], fv["facts"], fv["coverageIds"])
    X.replace_views(G, [v_file], [nv])
    return G


R.world("F4-supported-file-view-plus-coverage-less-foreign-references-scope", file_view_plus_foreign_scope(),
        note="inventory@U1 reaches the U0 file Coverage only because its U1 match is a references scope "
             "and its relation match is the U0 file scope")


# (b5) the lawful split construction for stage-2 D1
def split_reference_views():
    G = X.build(**KW_UM)
    U0 = X.binding_universe(G, "references")
    U1 = X.other_universe(G, U0)
    s_b = X.mint_scope(G, "references", "resolved-binding", U1, [])
    c_b = X.mint_coverage(G, s_b, U1)
    vb = X.mint_view(G, [s_b], [], [c_b])
    X.replace_views(G, [], [vb])
    return G


R.world("F5-lawful-split-construction-for-D1", split_reference_views(),
        note="contract 5: 'Splitting the selected evidence into one view per universe is the lawful construction'")

R.report("receipts/stage3-symbol-free.json")
