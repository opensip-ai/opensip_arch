"""source42.v1 helper corrections of this origin's own ported helpers (continuing HC-1..HC-46, which remain history and stay in the
ported code: HC-1..HC-13 consumer-b.v24, HC-14..HC-32 source39.v1, HC-33..HC-38 source39.v2/v3, HC-39..HC-46 source41.v1).

Each entry names the original failure and where its bytes or results are retained, the source42 kit selector that answers it, and the
correction with its re-execution. The unchanged ported helper state is preserved at preserved/s42-original-state/ (exact bytes) and is
re-executable at preserved/pre-s42/ (tools/make_pre_s42.py, root rebinding only).
"""
HC = {
    "HC-47": ("ref/enumeration.py and builders/{ts,rust,syntax}_runs.py - the enumeration binding programEntry law. Selectors: "
              "foundation/enumeration-contract.v1.md s1 lines 20-21 (provenance=default-unit: at most one per cell, ordinal 0; a syntax-only default "
              "binding is backed by the U-9 fallback unit) and lines 24-47 (an available default-unit binding has programEntry null, never the U-1 "
              "marker; a non-null value refuses ENUMERATION_BINDING_PROGRAM_ENTRY; TS/JS entry derived and compared to "
              "TypeScriptConfigGraphV1.entryConfigPath: tsconfig/jsconfig marker -> that markerPath, package.json -> null with nodes [], "
              "explicit-plan-selection -> programEntry); foundation/enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/"
              "programEntry/description ('U-1 default uses null; admission derives the actual U-1 marker/synthesized entry and compares it to retained "
              "TypeScriptConfigGraphV1.entryConfigPath'), a schema description unchanged since source41. Original failure: the unchanged ported "
              "helpers admit all 27 positives (logs/s42-original.7.from_scratch.log) whose retained enumeration plans carry programEntry "
              "'tsconfig.json' (ts-*, cmp-*) or 'Cargo.toml' (rust-*) on default-unit bindings and label the U-9 syntax default "
              "explicit-plan-selection; those stores have run ids identical to all 27 source41 exports "
              "(preserved/source41-v1/blind-review.json), so the source41 exports carried the defect and the source41 admission omitted the published "
              "description. Correction: program_entry_faults (null rule; derived entry vs retained entryConfigPath; explicit entry) and the "
              "default-unit cardinality check (no published key: cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY); builders emit programEntry null and the "
              "syntax default as default-unit. Re-executed: logs/s42-hc47-probe.*, logs/s42-hc47-probe2.*, logs/s42-fin-build.*, "
              "logs/s42-fin-mut.0.replay_all.log (ts-pass~default-unit-program-entry and rust-mixed~default-unit-program-entry refuse "
              "ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:default-unit-non-null; ts-pass~explicit-entry-not-graph-entry refuses "
              "ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:explicit-entry); the cardinality control after HC-50."),
    "HC-48": ("ref/execinputs.py - candidate views for s3 attribution. Selector: foundation/execution-inputs-contract.v1.md s3 line 53 (the candidate "
              "views are the view outputRefs of complete receipts, which s1 makes exactly the view members of selectedRefs; a view on selectedRefs "
              "but on no complete receipt refuses EXECUTION_INPUTS_SELECTED_COVER; relation-column membership, the resolution playing no part) and s8 "
              "build_manifest row. Original: the source41 HC-42 helper also drew candidates from the claimed selectedRefs, so such a view was attributed "
              "and refused only indirectly (unchanged-helper column of selfcheck/s42-prepost-matrix.json#/controls for "
              "syntax-code~selected-view-not-on-receipt). Correction: candidate_views reads complete receipts only; admission refuses a selectedRefs "
              "view on no complete receipt with EXECUTION_INPUTS_SELECTED_COVER before any derivation. Re-executed: logs/s42-fin-mut.0.replay_all.log "
              "(syntax-code~selected-view-not-on-receipt refuses EXECUTION_INPUTS_SELECTED_COVER:view-not-on-receipt)."),
    "HC-49": ("Runtime adaptations of ported tools, no law change: tools/discovery_vectors.py loaded its unchanged-helper comparison module from the "
              "source41 layout (original failure logs/s42-original-disc.0.discovery_vectors.log: FileNotFoundError "
              "preserved/s41-original-state/ref/membership.py) and now loads preserved/s42-original-state; tools/retention_negatives.py pre column "
              "-> preserved/pre-s42; vectors/phase0_custody.py and tools/final_custody.py assert the supplied source42 hashes; tools/prepost_s42.py, "
              "tools/provenance_s42.py and tools/make_pre_s42.py replace their source41 counterparts; checkpoint and finalize tools cite s42 logs."),
    "HC-50": ("Own control construction error in builders/syntax_runs.py: the first syntax-code~second-default-unit-binding added the second binding "
              "without a stage observation, so the synthetic capture wrote stageOrdinal null for it and closure refused SCHEMA_REFUSED:execution-inputs "
              "(/cellOutcomes/1/stageOrdinal) before enumeration admission ran, masking the cardinality law under test "
              "(logs/s42-fin-mut.0.replay_all.log). Correction: the second binding gets a lawful observation (stage 0, its attributed views). "
              "Re-executed: logs/s42-fin2.*."),
}
PHASE = {0: ["HC-49"], 5: ["HC-47", "HC-48", "HC-50"], 7: ["HC-47", "HC-49"], 9: ["HC-48", "HC-49", "HC-50"]}
CARRIED = ("HC-1..HC-46 (consumer-b.v24, source39.v1-v3, source41.v1) remain in the ported code as prior corrections; their records are preserved at "
           "preserved/source41-v1/tools/hc_source41.py and the histories preserved inside preserved/source41-v1/, and were re-exercised, not re-made, by "
           "this runtime's source42 re-execution.")


def for_phase(n):
    return [f"{k}: {HC[k]}" for k in PHASE.get(n, [])]


def all_entries():
    return [f"{k}: {v}" for k, v in HC.items()]
