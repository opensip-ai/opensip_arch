"""source45 (runtime consumer-b.v24-source45.v1) corrections to this origin's own helpers. They continue HC-1..HC-58: the source42, source43 and source44
records remain in tools/hc_source42.py, tools/hc_source43.py and tools/hc_source44.py, and apply unchanged.

Each entry names the original failure and where its bytes or results are retained, the source45 kit selector that answers it, and the correction with
its re-execution. The exact source44.v1 final bytes are preserved at preserved/s44-final/ (manifest.json; results-manifest.json).
"""
HC = {
    "HC-59": ("Runtime adaptation for source45.v1, no law change. output/preserve_s44_final.py ran before any rebind or execution. It copied the exact source44.v1 "
              "final bytes of 138 files (every helper *.py, the review, requirement status, checkpoints, notes, traces, custody reports and selfcheck files) "
              "to preserved/s44-final/, and hashed all 546 result files (104 stores) in preserved/s44-final/results-manifest.json. output/rebind_s45.py "
              "then rebound the copied executable code from the source44.v1 root (output/rebind-s45-manifest.json: 113 files, 132 occurrences). It exited "
              "1 only on runtime label text in four files. Two are source44 records left as history (tools/hc_source44.py, tools/result_diffs_s44.py); "
              "tools/finalize_review.py and vectors/phase0_custody.py were edited for source45. tools/run_unchanged_s44.py runs the source44 phase-3 scripts "
              "against the source45 kit after checking that every helper they import equals preserved/s44-final with the root mapped back. Custody "
              "expectations in vectors/phase0_custody.py and tools/final_custody.py now assert the supplied source45 hashes (manifest 70771536..., parent "
              "8b4efbb0...). output/reconcile_s44_arithmetic.py re-derives my source44 result-comparison numbers from retained files "
              "(selfcheck/s45-s44-arithmetic-reconciliation.json)."),
    "HC-60": ("Pre-Analyze host conversion closedWorld. The source44 helper, ref/provider_wire.py pre_analyze_conversion(requests, closed_world), took a "
              "caller-chosen closedWorld, because source44 published none (my M-s44-1). The source44 startup vectors measured four candidates as "
              "undetermined, and the source44 traces minted reading A (exportsClosed unknown, dynamicDispatch not-applicable, reasons []). Measured unchanged "
              "on the source45 kit (logs/s45-original.1 and .2, outputs preserved/s45-original/traces/), both runs exited 0. The startup vectors still "
              "reported a determinacy gap, and the traces still minted reading A, which is not the published value because its reasons are [] instead of "
              "['no-manifest']. Neither run detected the change. Selectors: native-evidence.md s9.7 closedWorld bullet (lines 3241-3261); "
              "native/provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion and hostConversionClosedWorld. "
              "Correction: provider_wire reads the published value from both owners and checks that they agree. pre_analyze_conversion(requests) takes no "
              "closedWorld, and admit_minted_entry refuses cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED for any other value. The startup vectors measure owner "
              "agreement, ClosedWorldV2 admission and identity stability, and check that each source44 candidate refuses. The traces mint and check the "
              "published value. Re-executed: logs/s45-p3.*."),
}
PHASE = {0: ["HC-59"], 3: ["HC-60"], 9: ["HC-59"]}
CARRIED = ("HC-1..HC-58 (consumer-b.v24, source39.v1-v3, source41.v1, source42.v1-v3, source43.v1, source44.v1) remain in the helper code as prior "
           "corrections. The source42, source43 and source44 records are tools/hc_source42.py, tools/hc_source43.py and tools/hc_source44.py; earlier "
           "records are preserved inside preserved/. Source45 execution re-exercises them without re-making them.")


def for_phase(n):
    return [f"{k}: {HC[k]}" for k in PHASE.get(n, [])]


def all_entries():
    return [f"{k}: {v}" for k, v in HC.items()]
