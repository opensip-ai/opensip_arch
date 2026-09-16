"""Stage 2: view-attribution discriminators on runtime-only mutated copies of maintained worlds.

Every world starts from `evaluator_graph_fixture.v3.build_file_inputs(atom_override=NONE_ATOM, ...)`
exactly as the maintained `full_run_case` driver does, mutates a PRIVATE deep copy (new scopes /
coverage / views minted with the checker's own `_mint` and the native owner's admitted
`coverage_result`), and is then measured twice:

  admission  - `admit_execution_inputs` over the shared host-capture builder's rows. The builder
               reuses the reference model, so ADMIT is reference self-consistency only.
  closed-run - the maintained `check-execution-inputs.v1.full_run` driver (owner ADMIT -> R.derive
               -> seal -> IDENTITY.close_run). Recorded only when it actually ran; an exception is
               recorded verbatim and never re-labelled.

Host-alternative encodings (a row whose `viewDigests` differs from the builder's) are hashed into
the graph the same way `attach_host_capture` does, so the closed-run column shows whether the Run
itself decides between the encodings.
"""
import copy
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_common as P  # noqa: E402

K, M, F = P.K, P.M, P.F
C = M.C
NH = F.fixture_helpers()
COV_SCHEMA = NH.N.schema_document_digest(NH.N.NATIVE_SCHEMA_DOC)


def build(**kwargs):
    return F.build_file_inputs(atom_override=K.NONE_ATOM, **kwargs)


def views_of(G):
    return {k: v for k, (d, v) in G["objects"].items() if d == "view" and k in G["viewIds"]}


def sc(G, sid):
    return G["objects"][sid][1]


def single_view(G, relation, uni):
    for k, v in views_of(G).items():
        scopes = [sc(G, s) for s in v["scopeIds"]]
        if len(scopes) == 1 and scopes[0]["relation"] == relation and scopes[0]["sourceUniverse"] == uni:
            return k
    raise LookupError("no single-scope view " + relation + "@" + str(uni))


def binding_universe(G, capability):
    for cell in G["enumerationPlan"]["cells"]:
        if cell["capabilityId"] == capability:
            return cell["programBindings"][0]["universe"]
    raise LookupError(capability)


def provider(G):
    return next(iter(views_of(G).values()))["producerClosure"]


def rel_schema(G):
    return next(d for d in next(iter(views_of(G).values()))["schemaDigests"] if d != COV_SCHEMA)


def mint_scope(G, relation, resolution, uni, subjects):
    return K._mint(G["objects"], "subject-scope", {
        "snapshotId": G["inputs"]["plan"]["snapshotId"], "sourceUniverse": uni, "targetUniverse": uni,
        "relation": relation, "resolution": resolution, "enumeratorClosure": provider(G),
        "subjects": M.canon_str_list(subjects),
    })


def mint_coverage(G, sid, uni):
    paths = [r["path"] for r in G["snapshot"]["sourceInventory"]]
    scope = sc(G, sid)
    payload = NH.coverage_result(scope, uni, True, G["blobs"], paths)
    admitted = NH.N.admit_coverage_result_v3(payload, scope, [], COV_SCHEMA)
    if admitted.get("result") != "ADMIT":
        raise RuntimeError("native owner refused probe coverage: " + str(admitted))
    pd = K._blob(G["blobs"], payload)
    return K._mint(G["objects"], "coverage", {"scopeId": sid, "payloadSchemaDigest": COV_SCHEMA, "payloadDigest": pd})


def mint_view(G, scope_ids, facts, coverage_ids):
    return K._mint(G["objects"], "view", {
        "planId": G["inputs"]["planId"], "scopeIds": M.canon_str_list(scope_ids),
        "facts": M.canon_str_list(facts), "coverageIds": M.canon_str_list(coverage_ids),
        "producerClosure": provider(G), "schemaDigests": M.canon_str_list([rel_schema(G), COV_SCHEMA]),
    })


def replace_views(G, retire, add):
    """Retire/add views on the graph's own view census and evaluation refs (pre-attach only)."""
    retire = set(retire)
    G["viewIds"] = M.canon_str_list([v for v in G["viewIds"] if v not in retire] + list(add))
    refs = [r for r in G["inputs"]["evaluationInputRefs"]
            if not (r["domain"] == "view" and "view2:" + r["digest"] in retire)]
    refs += [{"domain": "view", "digest": K.hx(a)} for a in add]
    G["inputs"]["evaluationInputRefs"] = K.canon_refs(refs)
    live = [G["objects"][v][1] for v in G["viewIds"]]
    G["coverageIds"] = M.canon_str_list([c for v in live for c in v["coverageIds"]])
    G["scopeIds"] = M.canon_str_list([s for v in live for s in v["scopeIds"]])
    G["inputs"]["coverageCount"] = len(G["coverageIds"])
    if G.get("viewId") in retire:
        G["viewId"] = add[0]


def row_by_cap(kw, capability, program=0):
    return next(r for r in kw["execution_inputs"]["cellOutcomes"]
                if r["capabilityId"] == capability and r["programOrdinal"] == program)


def closed_run(G):
    try:
        result, proof = K.full_run(copy.deepcopy(G))
    except Exception as exc:  # noqa: BLE001 - recorded verbatim
        return {"standing": "closed-run", "ran": False, "exception": type(exc).__name__ + ":" + str(exc)[:600]}
    return {
        "standing": "closed-run", "ran": True, "verdict": result.get("verdict"), "runId": result.get("runId"),
        "executionCauses": sorted(d["cause"] for d in proof.get("executionDeficiencies") or []),
        "executionInputsDigest": proof.get("executionInputsDigest"),
    }


def attach_manifest(G, manifest):
    """Mirror `attach_host_capture` for a host-alternative manifest (no admission short-cut)."""
    digest = M.raw_digest(manifest)
    G["blobs"][digest] = C.canonical(manifest)
    G["inputs"]["executionInputsDigest"] = digest
    G["inputs"]["evaluationInputRefs"] = K.canon_refs(
        list(manifest["selectedRefs"]) + [{"domain": "execution-inputs", "digest": digest}])
    G["executionInputs"] = manifest
    G["executionInputsDigest"] = digest
    return G


RESULTS = {}
ORDER = []


def world(name, G, *, host_edit=None, run_closed=True, note=None):
    ORDER.append(name)
    entry = {"note": note}
    try:
        kw = K.manifest_from_owner(copy.deepcopy(G))
        if host_edit is not None:
            host_edit(kw)
            promised = M.promised_pointers(kw["execution_inputs"], kw["plan"], kw["execution_plan"],
                                           kw["enumeration_plan"], objects=kw["objects"], blobs=kw["blobs"])
            kw["store_pointers"] = promised["store_pointers"]
        entry["describe"] = P.describe(kw)
        entry["admission"] = P.admit_summary(kw)
        if run_closed:
            GG = copy.deepcopy(G)
            if host_edit is not None:
                attach_manifest(GG, kw["execution_inputs"])
            entry["closedRun"] = closed_run(GG)
            if entry["closedRun"].get("ran"):
                entry["closedRun"]["digestEqualsAdmission"] = (
                    entry["closedRun"]["executionInputsDigest"] == entry["admission"]["executionInputsDigest"])
    except Exception as exc:  # noqa: BLE001 - a failed attempt is preserved, not hidden
        entry["probeError"] = type(exc).__name__ + ":" + str(exc)[:600]
        entry["traceback"] = traceback.format_exc()[-2000:]
    RESULTS[name] = entry


# ---------------------------------------------------------------- A: unsupported-typed selected U
G_uns = build(unsupported_cell="required")
world("A0-control-unsupported-required", G_uns,
      note="maintained world; builder names the returned references view on the UNSUPPORTED-TYPED row")


def _uns_row_empty(kw):
    row_by_cap(kw, "references")["viewDigests"] = []


world("A1-host-alt-unsupported-row-names-no-view", G_uns, host_edit=_uns_row_empty,
      note="same captured receipt/selectedRefs/coverage; only the unsupported row's viewDigests is []")


def _uns_capture_nothing(kw):
    ref_view = row_by_cap(kw, "references")["viewDigests"][0]
    view = kw["objects"]["view2:" + ref_view][1]
    covs = {K.hx(c) for c in view["coverageIds"]}
    ei = kw["execution_inputs"]
    row_by_cap(kw, "references")["viewDigests"] = []
    for rc in ei["hostCapture"]["stageReceipts"]:
        rc["outputRefs"] = [r for r in rc["outputRefs"] if r["digest"] != ref_view]
    ei["selectedRefs"] = [r for r in ei["selectedRefs"]
                          if not (r["domain"] == "view" and r["digest"] == ref_view)
                          and not (r["domain"] == "coverage" and r["digest"] in covs)]


world("A1b-host-alt-unsupported-returned-view-not-captured-at-all", G_uns, host_edit=_uns_capture_nothing,
      run_closed=False,
      note="contract 5 says the answered Coverage stays in stage capture and selectedRefs; law-refused shape")


def _inv_adds_refs_view(kw):
    ref_view = row_by_cap(kw, "references")["viewDigests"][0]
    row = row_by_cap(kw, "inventory")
    row["viewDigests"] = M.canon_str_list(row["viewDigests"] + [ref_view])


world("A2-host-alt-inventory-row-also-names-references-view", G_uns, host_edit=_inv_adds_refs_view,
      note="a same-U same-producer view that carries no inventory matrix relation, named on the inventory row")

# ---------------------------------------------------------------- B: one shared view, several relations
G = build()
U0 = binding_universe(G, "inventory")
v_file, v_pkg = single_view(G, "file", U0), single_view(G, "package", U0)
fv, pv = G["objects"][v_file][1], G["objects"][v_pkg][1]
shared = mint_view(G, fv["scopeIds"] + pv["scopeIds"], fv["facts"] + pv["facts"], fv["coverageIds"] + pv["coverageIds"])
replace_views(G, [v_file, v_pkg], [shared])
world("B1-shared-view-file+package-one-cell", G,
      note="one provider view carrying both inventory relations' partitions replaces the two split views")

G = build(symbol_rows=[{"nativeSubjectId": "x"}])
U0 = binding_universe(G, "inventory")
v_file, v_decl = single_view(G, "file", U0), single_view(G, "declares", U0)
fv, dv = G["objects"][v_file][1], G["objects"][v_decl][1]
shared2 = mint_view(G, fv["scopeIds"] + dv["scopeIds"], fv["facts"] + dv["facts"], fv["coverageIds"] + dv["coverageIds"])
replace_views(G, [v_file, v_decl], [shared2])
G_b2 = G
world("B2-shared-view-file+declares-two-cells", G_b2,
      note="one view carries an inventory partition and a syntax partition at the same U")


def _syntax_omits_shared(kw):
    row = row_by_cap(kw, "syntax")
    row["viewDigests"] = [h for h in row["viewDigests"] if h != K.hx(shared2)]


world("B2x-host-alt-syntax-row-omits-shared-view", G_b2, host_edit=_syntax_omits_shared,
      note="the shared view stays captured and named by the inventory row only")

# ---------------------------------------------------------------- C: universes of NAMED scopes
KW_ASYM = dict(multiple_universes=True, symbol_rows=[{"nativeSubjectId": "x"}], symbol_only_second_program=True)


def with_extra_scope_on_file_view(scope_universe_role):
    G = build(**KW_ASYM)
    U0, U1 = binding_universe(G, "inventory"), binding_universe(G, "syntax")
    uni = U0 if scope_universe_role == "U0" else U1
    v_file = single_view(G, "file", U0)
    fv = G["objects"][v_file][1]
    extra = mint_scope(G, "references", "resolved-binding", uni, [])
    nv = mint_view(G, fv["scopeIds"] + [extra], fv["facts"], fv["coverageIds"])
    replace_views(G, [v_file], [nv])
    return G


world("C1-control-file-view-plus-coverage-less-references-scope-same-U", with_extra_scope_on_file_view("U0"),
      note="lawful control: every named scope of the inventory@U0 view is at U0")
world("C1-file-view-plus-coverage-less-references-scope-foreign-U", with_extra_scope_on_file_view("U1"),
      note="inventory@U0 names a view one of whose scopes is at U1 (no Coverage, no fact); contract 3 "
           "'each named scope sourceUniverse vs binding U'")


def same_scope_discriminator(foreign):
    G = build(**KW_ASYM)
    U0, U1 = binding_universe(G, "inventory"), binding_universe(G, "syntax")
    s_ref = mint_scope(G, "references", "resolved-binding", U0, [])
    s_pkg = mint_scope(G, "package", "manifest-declared", U1 if foreign else U0, [])
    v = mint_view(G, [s_ref, s_pkg], [], [])
    replace_views(G, [], [v])
    return G, v


G_c2ctrl, v_c2ctrl = same_scope_discriminator(False)
world("C2-control-U-and-relation-on-same-scope", G_c2ctrl,
      note="references@U0 + package@U0 (both coverage-less): both recipes attribute to inventory@U0")
G_c2, v_c2 = same_scope_discriminator(True)
world("C2-U-and-relation-on-different-scopes", G_c2,
      note="references@U0 + package@U1 (both coverage-less): model's separate booleans attribute to "
           "inventory@U0; a same-scope recipe attributes to no cell")


def _c2_same_scope_encoding(kw):
    row = row_by_cap(kw, "inventory")
    row["viewDigests"] = [h for h in row["viewDigests"] if h != K.hx(v_c2)]


world("C2y-host-alt-same-scope-recipe-encoding", G_c2, host_edit=_c2_same_scope_encoding,
      note="the view stays captured in the receipt and selectedRefs but is attributed to no row")

# ---------------------------------------------------------------- D: one view, two universes' Coverage
G = build(unsupported_cell="required", multiple_universes=True)
UA = binding_universe(G, "references")
UB = next(b["universe"] for c in G["enumerationPlan"]["cells"] for b in c["programBindings"] if b["universe"] != UA)
v_ref = single_view(G, "references", UA)
rv = G["objects"][v_ref][1]
s_ref_b = mint_scope(G, "references", "resolved-binding", UB, [])
c_ref_b = mint_coverage(G, s_ref_b, UB)
two_u = mint_view(G, rv["scopeIds"] + [s_ref_b], rv["facts"], rv["coverageIds"] + [c_ref_b])
G_d0 = build(unsupported_cell="required", multiple_universes=True)
world("D0-control-unsupported-two-universe-world-unchanged", G_d0,
      note="maintained combination, no mutation")
replace_views(G, [v_ref], [two_u])
world("D1-unsupported-row-view-carries-two-universes-coverage", G,
      note="contract 5: 'forbids exactly one thing: making a SINGLE view carry two universes' Coverage and "
           "then attributing that view to a cell/program binding fixed at one of them'")

G = build(multiple_universes=True)
UA = binding_universe(G, "inventory")
UB = next(b["universe"] for c in G["enumerationPlan"]["cells"] for b in c["programBindings"] if b["universe"] != UA)
va, vb = single_view(G, "file", UA), single_view(G, "file", UB)
av, bv = G["objects"][va][1], G["objects"][vb][1]
merged = mint_view(G, av["scopeIds"] + bv["scopeIds"], av["facts"] + bv["facts"], av["coverageIds"] + bv["coverageIds"])
replace_views(G, [va, vb], [merged])
world("D2-contrast-supported-rows-view-carries-two-universes-coverage", G,
      note="same forbidden shape on supported-available rows, where account derivation loads the Coverage")

# ---------------------------------------------------------------- E: candidate-only relation filter
try:
    owner = K.manifest_from_owner(build())
    o = copy.deepcopy(owner)
    base = o["enumeration_plan"]["cells"][0]["programBindings"][0]
    prov = base["enumerator"]["closureId"]
    o["enumeration_plan"]["cells"].append({
        "capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".", "required": False,
        "kinds": [], "programBindings": [{
            "ordinal": 0, "provenance": "default-unit", "enumerator": {"status": "selected", "closureId": prov},
            "nativeContextDigest": base["nativeContextDigest"], "universe": base["universe"],
            "programEntry": None, "extents": [], "candidateSourcePaths": ["src/index.ts"]}]})
    spec = copy.deepcopy(o["analysis_spec"])
    spec["requestedCapabilities"] = list(spec["requestedCapabilities"]) + [
        {"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".", "required": False}]
    o["analysis_spec"] = spec
    o["plan"] = dict(o["plan"], analysisSpecDigest=M.raw_digest(spec))
    o["execution_inputs"]["analysisSpecDigest"] = M.raw_digest(spec)
    o["execution_inputs"]["enumerationPlanDigest"] = M.raw_digest(o["enumeration_plan"])
    rebuilt = K.rebuild_after_object_mutation(o, dict(o["objects"]), dict(o["blobs"]))
    ORDER.append("E1-standalone-candidate-cell-beside-native-views")
    RESULTS["E1-standalone-candidate-cell-beside-native-views"] = {
        "note": "STANDALONE admission observation: Plan/spec not reminted through closure; not a Run",
        "describe": P.describe(rebuilt), "admission": P.admit_summary(rebuilt)}
except Exception as exc:  # noqa: BLE001
    ORDER.append("E1-standalone-candidate-cell-beside-native-views")
    RESULTS["E1-standalone-candidate-cell-beside-native-views"] = {
        "probeError": type(exc).__name__ + ":" + str(exc)[:600], "traceback": traceback.format_exc()[-2000:]}

digest = P.write_json("receipts/stage2-attribution.json", {"order": ORDER, "worlds": RESULTS})
for name in ORDER:
    e = RESULTS[name]
    print("==", name)
    if "probeError" in e:
        print("   PROBE ERROR", e["probeError"])
        continue
    a = e["admission"]
    print("   admission", a["result"], a["refusals"])
    cr = e.get("closedRun")
    if cr:
        print("   closed-run", cr.get("verdict") if cr.get("ran") else "NOT RUN: " + cr.get("exception", "")[:300],
              cr.get("executionCauses"), "digest==admission", cr.get("digestEqualsAdmission"))
    for c in e["describe"]["cells"]:
        print("   row", c["cell"], c["capabilityId"], "U", c["universe"], c["rowState"], "viewDigests", c["viewDigests"])
    for v in e["describe"]["views"]:
        if len(v["scopes"]) > 1 or v["coverageCount"] != 1:
            print("   view", v["view"], v["scopes"], "cov", v["coverageCount"], "receipt", v["inReceipt"], "selected", v["inSelected"])
print("receipt sha256", digest)
