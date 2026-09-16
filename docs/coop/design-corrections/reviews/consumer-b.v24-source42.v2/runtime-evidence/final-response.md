The source42 review is complete: the verdict is **ACCEPT-RECONSTRUCTABLE**, with no MUST or SHOULD issues. All 123 requirements and 8 standing rules are executed, none failed, and all checkpoints 0–11 are written. Root admission of the exported bytes is a separate check I haven't seen, and nothing here claims product qualification or acceptance.

**Correction to my own source41 result.** The source41 ACCEPT is superseded. My source41 exports put the marker file name into `programEntry` on default enumeration bindings (`"tsconfig.json"` for 17 TypeScript and cmp Runs, `"Cargo.toml"` for 6 Rust Runs). The schema description has forbidden that since source41, and my admission never checked it. Here the unchanged helpers still admit all 27, with run ids identical to my source41 exports; the corrected code refuses those 23 exact stores.

**What changed in source42.**
- **HC-47:** the enumeration-binding law. Default bindings carry a null `programEntry`, the entry is derived and compared with the retained config graph, and a cell may have only one default binding.
- **HC-48:** only views on complete stage receipts count, and a selected view on no receipt refuses `EXECUTION_INPUTS_SELECTED_COVER`.
- **HC-49:** path and label adaptations, including rebinding the copied code to v2.
- **HC-50:** my first second-default-binding control was masked by a schema fault in my own test setup. Rebuilt, it refuses on the intended law.

**Results.**
- **Positives:** all 27 rebuilt positives pass owning-schema admission, the independent retained closure and replay with byte-equal proofs, and are exported. From-scratch closure, export replay and the admission log were re-run fresh in v2.
- **Stores:** 71 closed; 29 admit (27 positives plus 2 lawful controls) and 42 refuse, including the designed negative.
- **Controls:** all nine refuse on their own laws under the corrected code. The unchanged code admitted three of the new ones.
- **Retention negatives:** 32 constructed, all pass.
- **Custody:** passes at phase 0 and at the end.

**Advisories (non-blocking).** Ten are carried; three are new:
- **A-s42-1:** the one-default-binding rule has no published refusal key.
- **A-s42-2:** the entry-mismatch refusal key is named only indirectly.
- **A-s42-3:** a sole syntax-only binding spelled as an explicit selection is not refused by any published rule, and the two spellings produce different plan identities.

**Continuation.** The v1 process ended before provenance, pre/post comparison, custody, checkpoints or the review ran. Here I:
- verified `output/` byte-identical to v1 (4566 files) and rebound the copied code (100 files) before running anything;
- re-ran all pending steps fresh under `s42v2-*` logs;
- reused v1's builds, tamper, discovery, phases 4–8, graph query, run termination and retention negatives as exact prior measurements, same code and bytes.

My first final-custody run in v2 failed because I ran it before phase 0 had produced its custody file; that log is kept and the re-run passes. No file in the v1 runtime changed.

Everything is in `output/`; start with `blind-review.md` (the JSON form is `blind-review.json`).
