"""source43 (runtime consumer-b.v24-source43.v1) helper corrections of this origin's own helpers, continuing HC-1..HC-53 (HC-47..HC-53 source42 records
remain in tools/hc_source42.py and apply unchanged).

Each entry names the original failure and where its bytes or results are retained, the source43 kit selector that answers it, and the correction with
its re-execution. The source42.v3 final bytes of every changed file are preserved at preserved/s42-v3-final/ (manifest.json).
"""
HC = {
    "HC-54": ("tools/phase9_graph_query.py against the source43 bytes of docs/coop/design-corrections/workflows/query-projection-contract.v3.md, the "
              "only kit member changed since my source42 custody rows (source42 sha256 923ff32f..., 29699 bytes; source43 30278 bytes). The source42 "
              "bytes are not in my custody, so every law of the current text was re-audited against the helper (vectors/graph-query.json#/source43ReAudit/"
              "lawAudit). The unchanged helper (after the runtime rebind only) still passes its own 53 vectors on source43 "
              "(logs/s43-original.0.phase9_graph_query.log), so its vectors did not discriminate. Executed on the new discriminating source43 vector "
              "inputs, the preserved unchanged helper (preserved/s42-v3-final/tools/phase9_graph_query.py) measured these omissions "
              "(vectors/graph-query.json#/source43ReAudit/prePost): "
              "(s4) graph.path edges carried the stored fact orientation instead of the walked hop nodes[i]->nodes[i+1] under incoming/both; "
              "(s7) availability `missing` and unknown/null/wrong-type observations were silently treated as a grant, no host-adapter "
              "out-of-vocabulary route, no retained availability-record admission; "
              "(s7) close_run refusals were routed by message substring, a complete replay mismatch was reported evidence.corrupt instead of "
              "evidence.regeneration-mismatch, and a non-typed exception escaped the wrapper instead of routing HOST.INVARIANT_VIOLATED; "
              "(s7, evaluator-fault-contract.v3 line 98) loss/regeneration remedies were own text instead of the registered carrier remedies; "
              "(s2) the closed ENDPOINT_AMBIGUOUS refusal was only implicit. Selectors: query-projection-contract.v3.md s2 fault precedence, s4 "
              "graph.path row paragraph, s7 availability/host-adapter/close_run paragraphs and table; foundation/evaluator-fault-observation.schema.v3.json"
              "#/x-opensip-routes (promised-bytes-lost:evidence-store, complete-replay-mismatch:retained-regeneration, input-schema-invalid:host-internal); "
              "foundation/identity-schemas.v3.json#/$defs/availability. Byte arithmetic (net +579 bytes against far more corrected law text) shows at least "
              "part of these laws was already present in the source42 bytes, so my source42.v3 R-GRAPH-QUERY standing rested on a helper that omitted them. "
              "Own tool errors in the corrected tool, both preserved. (1) logs/s43-hc54.0.phase9_graph_query.log asserted that every source43 vector "
              "differs from the unchanged helper, including the positive agreement control availability-retained-observed. (2) logs/s43-hc54b.0."
              "phase9_graph_query.log passed with an asymmetric pre/post comparison: the corrected column was hand-built with fewer fields, so failure "
              "vectors differed by shape alone. availability-out-of-vocabulary-after-malformed-request, where both helpers refuse QUERY.PARAMS_MALFORMED, is "
              "an agreement control. Correction: both columns use the same outcome summary of each helper's execute on identical inputs. Re-executed: "
              "logs/s43-hc54c.0.phase9_graph_query.log."),
    "HC-55": ("Runtime adaptation for source43.v1, no law change. output/rebind_s43.py rebound the root-copied executable code from the source42.v3 root "
              "(output/rebind-s43-manifest.json: 102 files, 121 occurrences; it exited 1 only on runtime labels in tools/finalize_review.py and "
              "vectors/phase0_custody.py, which were then edited). output/preserve_s42v3_final.py copied the source42.v3 final bytes of changed files to "
              "preserved/s42-v3-final/, and output/preserve_s42v3_runs_manifest.py recorded the sha256 of all 404 copied runs/selfcheck/negatives files "
              "before fresh re-execution. Custody expectations in vectors/phase0_custody.py and tools/final_custody.py now assert the supplied "
              "source43 hashes (manifest 6d8912f4..., parent db43ee76...)."),
}
PHASE = {0: ["HC-55"], 9: ["HC-54", "HC-55"]}
CARRIED = ("HC-1..HC-53 (consumer-b.v24, source39.v1-v3, source41.v1, source42.v1-v3) remain in the helper code as prior corrections; the source42 records "
           "are tools/hc_source42.py and earlier records are preserved inside preserved/; they are re-exercised, not re-made, by source43 execution.")


def for_phase(n):
    return [f"{k}: {HC[k]}" for k in PHASE.get(n, [])]


def all_entries():
    return [f"{k}: {v}" for k, v in HC.items()]
