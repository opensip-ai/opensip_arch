**Verdict: CHANGES_REQUIRED.** The review is written to `output/blind-review.md` and `output/blind-review.json`. All 123 requirements and 8 standing rules were executed with measured outputs; none is unexecuted or failed. The three future-qualification items were not performed, and are recorded as future work rather than design omissions.

**What was checked**
- **Kit custody:** the input manifest, its parent hash and all 102 files were re-checked at the end and are unchanged.
- **Complete Runs:** 26 Runs (4 syntax, 3 TypeScript, 6 Rust, 13 same-project comparison Runs) each passed full closure and independent replay in a separate process. The recomputed proofs match the retained proofs byte for byte, and each Run's inputs, witnesses and proof are exported.
- **Tamper and mutation tests:** changing a Run's logical result while keeping its identities valid is always refused on replay. Of the 32 mutation variants, 30 are refused. The other two are deliberate measurement variants that admit: `syntax-code~budget-exhausted` (seals indeterminate) and `syntax-code~stage-output-schema-relation-doc` (the evidence for S1).
- **Graph query:** 53 query vectors over the admitted Runs, 0 failures.
- **Phases 7–8:** envelopes, baseline/comparison, authorization and D9 vectors are all built.

**MUST issues**
- **M1:** under the default profile, a required clones census over non-code files leaves every TypeScript unit, and any syntax unit containing a non-code file, stuck at indeterminate. The same repository shape passes under Rust.
- **M2:** the digest rule for predicate nodes points at the v1 policy schema. Any rule using the newer `endpoint` field makes a valid Run unclosable (measured refusal).
- **M3:** the order of units and rows in unit membership is never published, yet it feeds the PlanId. The kit cites a `discovery-defaults.py` file that is not in the kit.
- **M4:** `detectorId` has no derivation, but it is part of the baseline identity and the exact detector match used in comparisons.
- **M5:** the query command's required `query-response` parity field has no slot in the JSON command envelope; adding one is refused by the schema.

**SHOULD issues**
- **S1:** no fixed list of stage output schemas; two different run identities both admit for the same plan.
- **S2:** the custody link for clone normalization specifications is unnamed.
- **S3:** nothing creates a zero-config syntax-only unit.
- **S4:** the value of `targetUniverse` in coverage accounts is unstated, and it is identity-bearing.
- **S5:** no recipe for `argvDigest` in execution grants.
- **S6:** three failure goldens have no detail code, but a failure envelope requires `errors[]`.
- **S7:** no indeterminate reason fits unknown absence that has neither an evidence nor a pivot cause.

There are also 14 advisories, all listed in `notes/10-gaps.md`.

**Caveats**
- **cb24 choices:** where the kit had no recipe, I made a choice and named it as a `cb24` choice (for example `detectorId = contributionId`, the unit/row order, the `argvDigest` recipe). Those choices mean the exported identities can't be treated as canonical until M3–M5 and S5 are resolved.
- **Root admission:** root admission of the exported bytes is a separate gate I can't observe; the review makes no product qualification claim.
- **Helper corrections:** 13 fixes to my own reconstruction tooling were made from the kit alone, with the failed attempts kept. None of them is counted as a design gap.

To recompute from scratch, run these from `output/`:
```text
/tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py
```
