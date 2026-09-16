"""Read-only sweep: how does the maintained host-capture builder treat the explicit returned views of
maintained graph constructors?  Measures, per graph, with the builder of VA_TREE:

  explicitViews        graph['viewIds'] plus view refs on inputs.evaluationInputRefs present in objects
  droppedExplicit      explicit views on no receipt outputRefs (and so not on selectedRefs)
  droppedSameProducer  of those, the ones whose producerClosure IS a stage producer (a real stage return)
  selectedNotOnReceipt selectedRefs views on no complete receipt
  refsOnly / idsOnly   views named by only one of the two explicit inputs

No Run is closed here; this bounds the impact of a builder/model capture correction on maintained graphs.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pc  # noqa: E402

K, H, S = pc.K, pc.H, pc.K.S
ATOM = lambda rel, rung, op="exists": {"op": op, "relation": rel, "minResolution": rung, "filters": []}  # noqa: E731

GRAPHS = [
    ("file:default", lambda: pc.F.build_file_inputs()),
    ("file:none-atom", lambda: pc.build()),
    ("file:missing-required-package", lambda: pc.F.build_file_inputs(complete_required_native=False)),
    ("file:multiple-universes", lambda: pc.F.build_file_inputs(multiple_universes=True)),
    ("file:unsupported-required", lambda: pc.F.build_file_inputs(unsupported_cell="required")),
    ("file:unsupported-optional+optional-unselected", lambda: pc.F.build_file_inputs(unsupported_cell="optional", optional_unselected_cell=True)),
    ("file:symbol-rows-x", lambda: pc.F.build_file_inputs(symbol_rows=[{"nativeSubjectId": "x"}])),
    ("file:symbol-only-second-program", lambda: pc.F.build_file_inputs(multiple_universes=True, symbol_rows=[{"nativeSubjectId": "x"}], symbol_only_second_program=True)),
    ("file:package-coverage-unknown", lambda: pc.F.build_file_inputs(package_coverage_unknown=True)),
    ("file:census-subjects", lambda: pc.F.build_file_inputs(file_coverage_subjects=["README.md"])),
    ("semantic:file", lambda: S.build_ts_semantic_graph(atom=ATOM("file", "enumerated"), subject_kind="file")),
    ("semantic:package", lambda: S.build_ts_semantic_graph(atom=ATOM("package", "manifest-declared"), subject_kind="package")),
    ("semantic:declares", lambda: S.build_ts_semantic_graph(atom=ATOM("declares", "syntactic"))),
    ("semantic:references", lambda: S.build_ts_semantic_graph(atom=ATOM("references", "resolved-binding"))),
    ("semantic:references-full", lambda: S.build_ts_semantic_graph(atom=ATOM("references", "resolved-binding"), second_partition=True, second_universe=True, target_sidecar=True, incoming_search=True, incoming_complete=True, has_references_fact=True)),
    ("semantic:references-b-target-u2", lambda: S.build_ts_semantic_graph(atom=ATOM("references", "resolved-binding"), second_universe=True, partition_b_target="u2")),
    ("semantic:imports", lambda: S.build_ts_semantic_graph(atom=ATOM("imports", "resolved-target"))),
    ("semantic:package-graph", lambda: S.build_package_graph()),
]

out = {"tree": str(pc.TREE), "graphs": {}}
for name, make in GRAPHS:
    try:
        g = make()
        n = H.normalize_graph(g)
        objects = n["objects"]
        ids = [v for v in n["view_ids"] if v in objects]
        refs = ["view2:" + r["digest"] for r in n["evaluation_input_refs"] if r.get("domain") == "view" and "view2:" + r["digest"] in objects]
        explicit = list(dict.fromkeys(ids + refs))
        manifest, _d = H.build_manifest(copy.deepcopy(g))
        exec_plan = objects[n["execution_plan_id"]][1]
        specs = H._stage_specs(exec_plan, n["blobs"])
        stage_producers = {s.get("producerClosure") for s in specs.values()}
        receipt = {r["digest"] for rc in manifest["hostCapture"]["stageReceipts"] if rc["state"] == "complete" for r in rc["outputRefs"] if r["domain"] == "view"}
        selected = {r["digest"] for r in manifest["selectedRefs"] if r["domain"] == "view"}
        attributed = {h for row in manifest["cellOutcomes"] for h in row["viewDigests"]}
        dropped = [v for v in explicit if K.hx(v) not in receipt]
        out["graphs"][name] = {
            "explicitViews": len(explicit), "receiptViews": len(receipt), "selectedViews": len(selected),
            "droppedExplicit": [[pc.short(v), [objects[s][1]["relation"] for s in objects[v][1]["scopeIds"]]] for v in dropped],
            "droppedSameProducer": [pc.short(v) for v in dropped if objects[v][1]["producerClosure"] in stage_producers],
            "selectedNotOnReceipt": sorted(pc.short(h) for h in selected - receipt),
            "attributedNotOnReceipt": sorted(pc.short(h) for h in attributed - receipt),
            "refsOnly": [pc.short(v) for v in refs if v not in ids], "idsOnly": [pc.short(v) for v in ids if v not in refs],
            "manifestDigest": pc.M.raw_digest(manifest),
        }
    except Exception as exc:  # noqa: BLE001
        out["graphs"][name] = {"error": type(exc).__name__ + ":" + str(exc)[:400]}

label = sys.argv[1] if len(sys.argv) > 1 else "base"
path = pc.RUNTIME / "receipts" / ("sweep-builder-" + label + ".json")
if path.exists():
    raise SystemExit("refusing to overwrite " + str(path))
raw = json.dumps(out, indent=2).encode() + b"\n"
path.write_bytes(raw)
for name, v in out["graphs"].items():
    print(name, {k: v[k] for k in v if k != "manifestDigest"})
print("receipt", path.name, hashlib.sha256(raw).hexdigest())
