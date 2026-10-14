# B-S10 configuration schema materialization review

Verdict: **REQUIRED-FINDINGS**

Subject manifest: `1db99bf72fddf01fc88706bac4b7a57fda1cfbbddad6896171424483ad0d9f37` (19010 bytes; 84 members). Rehashed every member; all sizes and hashes match. The three successor parents and 83 candidates also match their pins.

## Required finding

**B-S10-R1-RF-01 — The recipe options pin is stale.**

Location: `product/schemas/registry.json:338`, the contracts-v1 recipe.

The recipe's optionsSha256 remains the base value:

`7b2bf5ee38ec390564856efbea16c9e43d6ad4de7bd1cc7f49b154709d60d753`

The actual selected options file, including ProductConfiguration2, hashes to:

`c3481af1bbc9f5c2ec90fff05d1a298452f8901dce5536dd399a1f5fce404af5`

The generator closure correctly pins the latter. The standard entry point calls contracts/admission.registry, whose recipe processing checks the options bytes against optionsSha256 (`tools/contracts/admission.py:269`). It therefore refuses these candidate bytes even if B-S10's architecture selection is supplied.

The supplied generation runner verifies closure pins and the recipe source set, then calls pipeline.run directly. It never checks the recipe options hash. Its actual generated outputs match their captured hashes, but this bypass leaves the selected recipe inconsistent. Scratch verify_design checks generation/admission source selection rather than this recipe condition, so its PASS does not resolve the finding.

Re-pin the recipe to the exact options bytes, refresh affected product copies and package pins/provenance, and include the standard recipe-admission check in the evidence path. Refresh generation evidence as needed for the corrected registry provenance. No resolver, schema-profile or law widening is required.

## Independent checks that passed

The admission registry preserves every parent row and alias exactly and adds precisely the PCS and profiled-preview rows, sorted by schema ID. Both new IDs, lengths and hashes match the selected full schema documents. The profiled preview differs textually only by removing the top-level $comment and its preceding comma; parsed documents are equal after dropping that member. Every validating keyword remains unchanged. The identity schema-profile implementation is unchanged and has no admitted $comment keyword. Refusing to widen the profile for a prose annotation is appropriate.

All 14 files under product/ are byte-identical to the candidate worktree and exactly cover its changed/added file set. PCS is in generation and admission, with ProductConfiguration2Root in invocation and its source-map/options ownership. Preview is admission-only, resolving the plan's NBO-01. The 50 identity source pins match every registry ID, length, hash and ordering; host and storage source lists exactly match the same 50 rows. The test/comment changes are limited to 48→50. No resolver source or semantics are added.

All 350 generator-closure file pins match the worktree. The closure adds only PCS and re-pins the source map/options; the recipe closure and source-set pins are updated. All eight captured output hashes match the candidate files, with only invocation.rs and report.ts changed. The stale recipe options hash is the remaining generation-provenance defect.

Recomputed the retained base/candidate comparison from the four raw logs. Host has 310 passed and eight failed in both trees, across three suites. Storage has 137 passed and 33 failed in both trees, across two suites. Failed test-name sets equal the comparison JSON, and the runners use --no-fail-fast with lane ownership, priority 10 and private TMPDIR recorded. Identity/contracts tests and warning-denied all-target Clippy are recorded as passing. These are retained results, not tests rerun by this review; equal failure sets support no observed regression, not a clean host/storage suite.

The dependency-policy source-census failure is disclosed as pre-existing and identical at base/candidate. The prior formatting failures and narrowed edited-file check are retained; neither the stale policy nor unrelated formatting is changed. The report-lane log accurately records refusal at the unbound admission preflight.

## Scratch verification

The support script's work-directory architecture package is byte-identical to all subject members and the subject manifest. Independently ran the expressly permitted helper in report-only mode by suppressing its single write_text expression in memory. It wrote no file. The result matches the supplied JSON:

- Base lock with candidate tree: refusal because the admission source is not selected.
- Synthetic B-S10 append: PASS, 162 contract successors and 83 candidates.
- Generation sources: 41; admission sources: 50; aliases: 15.
- No generator/runtime code executed and productQualification false.

This proves structural selectability with synthetic review/assent records, not actual acceptance, binding or a TypeScript-lane pass.

## Non-blocking observation

**B-S10-R1-NBO-01:** README line 32 says the report TypeScript lane runs in scratch verification. Clarify that only its design/admission preflight is exercised there; the actual lane remains to run after real acceptance/assent and selection. The logs and helper already expose this distinction accurately, so this wording issue is non-blocking.

## Scope and boundaries

Verified the requested architecture base `54e336d81911a0e0eaeb815163e25ea992026e54` and clean product checkout. Candidate changes remain uncommitted materialization copies. No binding, law change, resolver semantics or product qualification is established.

Used permitted read-only file/source reading, hashing, JSON parsing and Git queries, plus the expressly permitted scratch helper with its output write suppressed. No Cargo, tests, builds, generators or lane were run. No network, panes or delegation were used. Private fixtures, installation, signing keys and held trees were not read. Neither repository, worktree, stage nor control files was edited. Only this directory's REVIEW.md and review.json were written.
