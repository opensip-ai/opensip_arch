# Review request: B-S10 round 2 (design unit: configuration schema admission materialization)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b-s10-r2/`).

## Boundaries

Do not edit either repository, the worktree, the stage or control files. Do not run Cargo, tests, builds, generators or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries over:
- the product (`/Users/sb/code/opensip-ai/opensip`, clean at `95279fa8ae086f98bd221cd827f6c0efc156c0c5`);
- the candidate worktree (`/Users/sb/code/opensip-ai/opensip-b-s10`, detached at that commit, with the B-S10 changes uncommitted);
- the architecture repository (`/Users/sb/code/opensip-ai/opensip_arch`, at `54e336d81911a0e0eaeb815163e25ea992026e54`);
- the work directory (`/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/b-s10`, including its `attempt0`-`attempt3` history).

You may run the read-only `review-support/verify_scratch_b_s10.py`. It reads both repositories and writes only `verify-scratch.json` beside its own copy. If you run it, point its output elsewhere, or report instead of writing.

## Subject

- **Stage.** `/tmp/opensip-implementation/b-s10-r2-stage`
- **Subject file.** `docs/implementation/m3/config-discovery-b/b-s10-subject.json`: 28620 bytes, SHA-256 `96807b6d7852e00c57ba0022e94ea3677e38c61691266a8bb8fa4bbd3936317e`, 125 members. Rehash every member.
- **Unit.** B-S10, a contract successor in the materialization form of `docs/implementation/m3/native-publication/rust3-identity-materialization-r1`. It is the B1-a prerequisite the accepted B1-a plan names (`docs/implementation/m3/config-discovery-b/b1-a/PLAN-r2.md` §2; your `codex-b1a-plan-r2` ACCEPT and its NBO-01).

## Round 2

Round 1 (`/tmp/opensip-implementation/reviews/codex-b-s10-r1`, your REQUIRED-FINDINGS) raised RF-01, the stale recipe `optionsSha256`, and NBO-01, the README's report-lane wording. Confirm:
- **RF-01, the re-pin.** The recipe's `optionsSha256` equals the candidate `options.json`, and the closure, registry and recipe provenance are consistent.
- **RF-01, the evidence path.** The generation runner now runs the standard recipe admission (`tools/contracts/admission.py` `registry()`) before `pipeline.run`. That admission at once caught a second stale fact, an unsorted `registry.json` source row (attempt 4 history). PCS's row is now in source-path order.
- **NBO-01.** The README states that the scratch verification runs only `verify_design.verify`. The actual report lane and the standard `generate_contracts.py` check (no `--write`) run at integration, with the bound lock.
- **History.** Attempts 4 and 5 are retained under the work directory and in the package history. The candidate was rebuilt from scratch.

## What to review

1. **The admission-registry copy.** Is it exactly the parent registry plus the two rows, with `$id`, bytes and SHA-256 matching the selected sources, sorted by schema ID?
2. **The profiled preview copy (lead decision).** Does it differ from the accepted carrier only by removing the one top-level `$comment` member, with every validating keyword unchanged? Check that `crates/identity/src/schema.rs` admits no `$comment`. Is rejecting a profile widening right?
3. **Product copies.** Is `product/` exactly the worktree's changed and added files, and complete? In particular:
   - PCS in `registry.json`, `source-map.json` and `options.json` (namespace `ProductConfiguration2`, module `invocation`) and in admission;
   - the preview carrier in admission only;
   - `SOURCE_PINS` and the host and storage `SOURCES` in schema-ID order;
   - the generator closure row and re-pins, and the registry recipe re-pin;
   - the 48→50 test update.
4. **Generation.** Do the generation evidence and the two regenerated outputs follow from the pinned generator, as in the precedent?
5. **Checks.** Are checks r8 sound?
   - The base/candidate `--no-fail-fast` comparison, with equal failure sets (host 8, storage 33), as evidence that nothing regressed.
   - The pre-existing conditions are disclosed and not changed: the stale identity dependency policy; host and identity not rustfmt-clean at base.
   - The report lane needs the binding.
6. **Scratch verify.** Does `review-support/verify-scratch.json` show the base lock refusing the candidate tree, and B-S10 appended passing (41 generation sources, 50 admission sources)?
7. **Scope.** Is it true that there are no resolver semantics, no law change and no binding?

## Output

`review.json` must carry:
- `verdict` (`ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{
  "verdict": "ACCEPT-DESIGN-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "96807b6d7852e00c57ba0022e94ea3677e38c61691266a8bb8fa4bbd3936317e",
  "rf01RecipeOptionsRepinnedAndStandardAdmission": true,
  "admissionRegistryCopyExact": true,
  "profiledPreviewCopyOnlyDropsComment": true,
  "pcsGenerationAndAdmission": true,
  "previewAdmissionOnly": true,
  "productCopiesExactAndComplete": true,
  "generationEvidenceSound": true,
  "checksAndBaseComparisonSound": true,
  "scratchVerifyPasses": true,
  "preExistingConditionsDisclosed": true,
  "resolverSemanticsAdded": false,
  "lawChanged": false,
  "bindingMade": false,
  "productQualification": false
}
```

After an ACCEPT, the lead gives its own assent, publishes the package to architecture, and binds B-S10 with its own product commit: the exact product copies plus the design-lock contract-successor entry, with fresh verification. Nothing is pushed.
