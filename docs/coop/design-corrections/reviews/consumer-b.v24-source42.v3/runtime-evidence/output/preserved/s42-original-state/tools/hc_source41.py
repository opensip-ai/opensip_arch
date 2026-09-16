"""source41.v1 helper corrections of this origin's own ported helpers (continuing HC-1..HC-38, which remain history and stay in the
ported code: HC-1..HC-13 consumer-b.v24, HC-14..HC-32 source39.v1, HC-33..HC-38 source39.v2/v3).

Each entry names the original failure and where its bytes or results are retained, the source41 kit selector that answers it, and the
correction with its re-execution. The unchanged ported helper state is preserved at preserved/s41-original-state/ (exact bytes) and is
re-executable at preserved/pre-s41/ (tools/make_pre_s41.py, root rebinding only).
"""
HC = {
    "HC-39": ("ref/membership.py, ref/enumeration.py, ref/closure.py - three source41 native laws the ported helper did not implement. "
              "(a) U-4b.2/U-4b.5: a tsjs unitKind is the projection of its mode (ts-tsconfig -> ts-program; js-allowjs, js-synthesized -> js-program) and "
              "a ts-program/js-program kind on another family refuses ENUMERATION_MEMBERSHIP_ORDER. Original: logs/s41-original-disc.0.discovery_vectors.log "
              "(16 vectors, 0 assertion failures) with preserved/s41-original-state/vectors/discovery-membership.json#u4b-tsjs-unit-kind-not-assigned: "
              "the ts-program spelling of a js-allowjs unit passed every enforcement check. (b) U-1 with s1.2: both configuration markers select the "
              "mode by the effective allowJs (jsconfig-kind nodes supply allowJs=true unless written; own options beat bases; later extends beat "
              "earlier; otherwise checkJs, default false). The unchanged helper assigned js-allowjs to every jsconfig.json and ignored checkJs and "
              "jsconfig-named bases; measured on the unchanged module in vectors/discovery-membership.json#s12-effective-allowjs-mode-selection "
              "(originalHelperDisagreements). (c) U-0: rootPath is '' or a CanonicalRelativeDirV1, member roots are CanonicalRelativeDirV1, decided "
              "before membership, slicing or enumeration binding reads a root (NATIVE_UNIT_ROOT_REPRESENTATION at the host, "
              "ENUMERATION_MEMBERSHIP_UNIT_ROOT through enumeration admission and Run closure). The unchanged helper had no such decision: a '.' root "
              "surfaced as ENUMERATION_MEMBERSHIP_ROW_DERIVATION on another path, and a malformed member root not at all "
              "(vectors/discovery-membership.json#u0-*/originalHelperEnforcementFaults). Selectors: native-evidence.md lines 755-760 and 797-799; "
              "516-531 and 654-659; 626-651; native-evidence.schemas.v2.json #/$defs/InternalUnitRootV1, #/$defs/CanonicalRelativeDirV1, "
              "#/x-opensip-config-node-kind-law. Re-executed: logs/s41-hc39-disc.0.discovery_vectors.log and logs/s41-fin-disc.0.discovery_vectors.log; "
              "Run-closure controls syntax-code~unit-kind-other-family, syntax-code~unit-root-external-sentinel, ts-pass~unit-kind-not-mode-projection "
              "(logs/s41-fin-mut.0.replay_all.log). Unchanged helpers on those controls (selfcheck/s41-prepost-matrix.json#/controls): the two unitKind "
              "controls ADMIT; the external-sentinel root refuses only by generic schema admission (SCHEMA_REFUSED:unit-membership), not by the U-0 decision."),
    "HC-40": ("tools/phase6_vectors.py spelled vector universes with jsAdmittedToProgram = allowJs and jsDiagnosticsEnabled = allowJs AND checkJs, "
              "the law HC-20 had already corrected in closure. Selector: native-evidence.md lines 538-540. No result depended on it: every phase-6 "
              "universe has JS roots or allowJs=false, and checkJs=false. Correction: allowJs AND len(jsRootFiles) > 0; checkJs. Re-executed: "
              "logs/s41-fin-p4to9.2.phase6_vectors.log; unchanged-helper run: preserved/pre-s41/logs/s41-pre-p4to9.2.phase6_vectors.log."),
    "HC-41": ("ref/run_termination.py and tools/run_termination_vectors.py used the reconstruction's own key cb24.RUN_TERMINATION_NOT_AN_OBJECT for a "
              "non-object candidate (source39 advisory A-n3). Source41 publishes it: run-termination-contract.v1.md s6 step 1 (line 173) "
              "RUN_TERMINATION_CANDIDATE_NOT_OBJECT, applied also at s7.6 step 1, which names no key of its own; s3 lines 85-87 now publish _RULE and "
              "_RUN exactly as the helper already spelled them. Original: preserved/pre-s41/logs/s41-pre-p4to9.8.run_termination_vectors.log "
              "(unchanged helper on the source41 kit). Re-executed: logs/s41-fin-p4to9.8.run_termination_vectors.log."),
    "HC-42": ("ref/execinputs.py took each cell row's views from the host-claimed viewDigests and checked only view planId (under "
              "EXECUTION_INPUTS_STAGE_ORDINAL) and view producer (under EXECUTION_INPUTS_STAGE_PRODUCER); it derived no attribution, compared no "
              "EXECUTION_INPUTS_VIEW_TOTALITY, and did not refuse a candidate view of another Plan as EXECUTION_INPUTS_PLAN_JOIN. The builders "
              "(synthetic host capture) put the single stage view on every row. Selectors: execution-inputs-contract.v1.md s3 'View attribution' "
              "(line 53); foundation/execution-inputs.schema.v1.json CellProgramOutcomeV1.viewDigests description and the internal fault list "
              "(EXECUTION_INPUTS_VIEW_TOTALITY). Original failure measured: logs/s41-hc42-probe.0.syntax_runs.log - the corrected admission refuses the "
              "unchanged builder capture of syntax-code EXECUTION_INPUTS_VIEW_TOTALITY:1:0 (the imports row claimed a view carrying no imports scope); "
              "over exact original bytes the corrected closure refuses syntax-code, syntax-data, syntax-mixed-disclosed and syntax-mixed-omitted with that "
              "key while the unchanged closure admitted them (selfcheck/s41-prepost-matrix.json postCode_originalBytes / preCode_originalBytes). "
              "Correction: attributed_views / attribution_map (V attributed iff V.producerClosure = P and one named scope has sourceUniverse = U and "
              "a matrix relation of the capability; candidate-only: U alone); observed row views must equal them; the named-scope universe check "
              "runs on every attributed view; builders observe attributed views. Own follow-on error of the first HC-42 version: the candidate set was "
              "computed only inside derive(), so the direct derive_outcome callers tools/phase4_tables.py and tools/phase8_envelopes.py failed with "
              "KeyError 'candidate_views' (logs/s41-post-p4to9.0.phase4_tables.log, logs/s41-post-p4to9.5.phase8_envelopes.log; phase5_vectors then "
              "lacked vectors/phase4-tables.json, logs/s41-post-p4to9.1.phase5_vectors.log); corrected by one candidate_views(ctx) function used by "
              "both paths. Second follow-on, in my own vector: tools/phase4_tables.py outcome vector two-carriers-first-in-h-order built subject "
              "scopes without relation/resolution (required by identity-schemas.v3 subject-scope), which the attribution law reads (KeyError "
              "'relation', logs/s41-fin-p4to9.0.phase4_tables.log); the mock scopes now spell declares@syntactic like their Coverage keys "
              "(re-executed logs/s41-fin2-p45.*). Re-executed: logs/s41-fin-build.*, logs/s41-fin-mut.0.replay_all.log, logs/s41-fin-p4to9.*; Run-closure control "
              "syntax-code~row-view-omitted (after HC-45)."),
    "HC-43": ("vectors/phase0_custody.py and tools/final_custody.py asserted the source39 manifest and parent hashes (c2f2f88d... / f71a5992...), and "
              "phase0 carried the source39.v3 runtime label, origin text and prior-row path. Found by reading before execution; the unchanged tools "
              "were not run against source41 (phase0_custody.py line 34 would have asserted). Correction: the user-supplied source41 values "
              "31369cc8c3b71e559c50f107104daff4d6d428e20fb75dc1e3914a2acc1ec6dd / eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236; "
              "prior own custody rows are preserved/source39-v3/vectors/phase0-custody.json (orientation only)."),
    "HC-44": ("tools/retention_negatives.py closed its 'pre' column with preserved/pre-hc33 (source39.v1 code), which is not part of this runtime. "
              "Runtime adaptation, not a law change: the pre column is now the unchanged ported helper exactly as it ran on the source41 kit "
              "(preserved/pre-s41/tools/replay_run.py)."),
    "HC-45": ("Own tool error in a new source41 control: builders/syntax_runs.py syntax-code~row-view-omitted first changed only the builder observation, "
              "which XI.build_record re-derives, so the exported store was byte-identical to syntax-code (runId and blobs equal) and ADMITTED "
              "without testing anything (logs/s41-post-mut.0.replay_all.log line 42; builder tail recorded EXECUTION_INPUTS_VIEW_TOTALITY:0:0). "
              "Correction: the retained claimed cellOutcomes[0].viewDigests is emptied after build_record. Re-executed: logs/s41-fin-mut.0.replay_all.log."),
    "HC-46": ("Own tool error in tools/finalize_review.py (source41 version), found by reading its first phase-10 output before phase 11 ran: "
              "the phase-11 checks compared blind-review.md with the phase-10 blind-review.json verdict, which is necessarily CHANGES_REQUIRED "
              "while the five phase-11 IDs are unexecuted (logs/s41-phase10.0.finalize_review.log), so a review stating the verdict its "
              "measured standing derives could never be delivered. Correction: phase 11 judges the review the phase-11 standing would "
              "yield, marks a failing check failed (which forces CHANGES_REQUIRED), and fails R-DELIVER-MD-JSON when the md does not state the "
              "refreshed verdict. No law, measurement or verdict rule changed."),
}
PHASE = {0: ["HC-43"], 5: ["HC-39", "HC-42", "HC-45"], 6: ["HC-40"], 7: ["HC-39", "HC-41"], 8: ["HC-41"], 9: ["HC-42", "HC-44", "HC-45"]}
CARRIED = ("HC-1..HC-38 (consumer-b.v24, source39.v1, source39.v2/v3) remain in the ported code as prior corrections; their records are preserved at "
           "preserved/source39-v3/tools/hc_v2.py and preserved/source39-v3/preserved/source39-v1/tools/hc_source39.py and were re-exercised, not "
           "re-made, by this runtime's source41 re-execution.")


def for_phase(n):
    return [f"{k}: {HC[k]}" for k in PHASE.get(n, [])]


def all_entries():
    return [f"{k}: {v}" for k, v in HC.items()]
