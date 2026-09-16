I migrated the author constructors to the native-v2 laws and rebuilt the package from inputs against my captured source. All seven positive Runs pass the owner's structural check and full `close_run`, and every control stops where it should. This is author self-checking, not independent review, not acceptance of frozen-candidate39 and not a review of the whole source. The details are in `review.md` and `review.json` at the runtime root.

**Inputs**
- **Captured source:** 12905 files copied to `source/`, with no drift during the copy. File-list hash `e9cb76d5…`; the package's source manifest hash is `8a942a83…`. Compared with source38, 33 files changed and 1 was added. No workflows code changed, only the prose in `workflows-and-surfaces.md`.
- **Package15:** its manifest `6a8d4fec…` and all 335 files verified. At the end I rechecked the original package, my copy and the captured source: all unchanged.
- **Before migration:** all 13 old exports are refused because the registered native schema changed. They stay as historical inputs and were not repaired. The old normalized and Rust-selection constructors fail with `BODY_NORMALIZATION_MAP_MISSING` or `STAGE_OUTPUT_SCHEMA_UNREGISTERED`, which matches what you found about `NAT_DIGEST`.

**What the overlay changes** (11 files, manifest `07c3185f…`, diff in `output/overlay/`)
- **S1:** stages are now registered in the producer closure with the matching schema digest. That covers `analyze` and the finalizers' `author-synthetic-analysis`.
- **S2:** each clone example's own closure now carries the normalization map and level specs: TS (levels L0 and L1), Rust (L0) and syntax-code (L0).
- **S4:** coverage accounts have a null target.
- **U-4b:** membership follows the deterministic ordering and assignment rule.
- **One repair beyond the law changes:** both finalizers now re-sort the analysis-spec parameters into canonical order. The first rebuild failed on this ordering check; that attempt is kept, and the repair diff is quoted in the review.

**Rebuild**
- The new script `rebuild-author-package.v2.py` takes `--source`, `--package`, `--overlay` and `--out` and depends on nothing else in `/tmp`.
- The final build ran from a different working directory. Its exports are byte-identical to the previous passing build; only files containing absolute paths differ.
- Output package manifest: **`b2fca539d71ed03dcb0ebdefe237a954e0bb1cac0b532c1c7d65358b0a0dee45`** (382 files). The old exports and files tied to source38 were moved unchanged into `historical-source38-before-native-v2/`.

**Results on the captured source**
- **Positives:** checkpoint3, the four normalized examples and the two Rust-selection examples pass both checks.
- **Semantic controls:** all three pass the structural check and are refused at `EVALUATOR_COMPLETE_PROOF_REPLAY`, as intended.
- **Binding controls:** the two lawful ones pass both checks; the invalid default entry is refused at `ENUMERATION_BINDING_PROGRAM_ENTRY`.
- **New TS map controls (4):** each is refused structurally at its intended code (map missing, level unmapped, level mismatch, spec not in closure), so `close_run` is correctly never reached.
- **Mapped-clone positives:** they reach full `close_run`. A probe using the owner's own functions confirmed map membership, stage registration, null targets and membership for all 9 lawful Runs.
- **Older probes:** the property and mixed-universe probes give the same results as before.
- **Export IDs:** every ID changed (full table in the review). checkpoint3 still has the same ID as the lawful default binding control.

**Queries:** all 7 query checks pass with unchanged expectations. They load the query projection from the source, and the capture has no workflow-v2 code, so the pending workflow law is untested here and needs your replay.

**Not tested:**
- no map negatives for Rust or syntax (TS only);
- no stage-registration, membership or non-null-target negatives under actual Runs;
- the partial helper still covers only exists/none;
- two-binding qualification is incomplete, and all 30 grades are PENDING;
- files tied to source38, such as the assessment and source-binding files, are not rebound.

I found no conflict with the source law.

**Final-freeze steps for you:**
1. Rerun the rebuild script on package15 plus the overlay with `--source <frozen> --source-manifest <frozen manifest>` and a fresh `--out`. Don't re-pin this package.
2. Require the same outcomes and reason codes. New export IDs are expected if the registered law bytes changed.
3. Classify any refusal as either an author helper limit or a law conflict.
4. Replay the query checks on the source that includes workflow-v2.
5. Rebind the source38-bound files and keep the limits above.
6. Never give this package to a blind consumer.

No background tasks are still running.
