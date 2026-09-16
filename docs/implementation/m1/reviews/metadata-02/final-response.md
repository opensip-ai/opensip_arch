**Verdict: ACCEPT-DESIGN-UNIT**, with no required findings. Only this RF-01 design/reference correction is accepted. Product implementation, binding the successor into the design-lock, the tests, the M1 gates, and runtime/release qualification (including the M6 release producer) all remain required.

**Integrity and checker**
- Subject-02's manifest hash (`1b456017…`) and all 10 files matched before and after the review. Subject-01 is also unchanged.
- The four schema/inventory files are byte-identical to v1. The other diffs contain only the stated corrections.
- The frozen checker passed: exit 0, 28 schemas, 43 cases.

**Prior findings (all closed)**
- **RF-A, coverage routing:** help/version now target envelope4, `metadata:1`, the fixed selectors and parser-refusal tests. The M1 development-only and single-channel negatives are there too. The named owners (`assets.rs`, `projection_tests.rs`, `startup_tests.rs`) already exist in the design-locked M1 inventory v3, so no product files are added.
- **RF-B, successor binding:** 9 members, 9 parents and 4 passage overrides are pinned, and the parents match the accepted v46 overlay or the design-lock. On temporary copies, the checker refused every tampering I tried: an extra or changed member, a changed parent, altered override text or pointer, a dropped override and a dropped candidate. Outside review folders, the old wording remains only in the superseded M1 inventory v2.
- **RF-C, one build channel:** all channel disagreements and invalid records are refused.

**The `$schema` validator bug**
- **Reproduced independently.** With the v1 registry, the custom ordering check never ran when validation followed a whole-document `$ref`. Keeping `$schema` while declaring the dialect explicitly still lost it. Only the v2 adapter keeps it.
- **Differential.** Across all 43 cases, only `unsorted-help` and `duplicate-help-name` change, matching the reported TypeScript disagreements. I did not rerun the TypeScript trial itself.
- **Also affected:** reversed release closure IDs in a version envelope, which the old registry accepted.
- **Adapter is safe for these 28 documents.** Each registry entry equals the original minus top-level `$schema`, and none of the schemas has nested `$schema`, embedded `$id` or dynamic refs. Mutations that revert the adapter, drop help ordering or drop the development-closure rule are all caught.

**Correction to my review-01:** its ordering and uniqueness conclusions never showed enforcement across documents. Its A-05 advisory blamed semantic "masking" when the envelope path simply never checked ordering. Its other conclusions are unaffected.

**Advisories (nonblocking)**
- **N-01:** removing the version `closureIds` ordering rule is not caught by the checker. A reversed-closure envelope case would fix that.
- **N-02:** three older cross-document refs (envelope3 to `baseline:2` and `invocation:3`, fact-batch to occupancy-companion) may have lost these checks in earlier Python evidence. That needs its own root-level item; I did not requalify it.
- **N-03 to N-07 (smaller):**
  - the `assets.rs` inventory description doesn't mention its new channel role;
  - `projection_tests.rs` is named as an owner only in the method text;
  - the schema still allows an empty diagnostic string;
  - the checker doesn't verify `previousCandidate`;
  - the superseded inventory v2 keeps the old wording.

I ran 47 independent probes, all as expected. Files are in `/tmp/opensip-implementation/m1-metadata-review-02`:
- review.md
- review.json
- checker-output.json
- probes.py
- probe-results.json
- root-refs.json
