# Independent Grok review: tooling inventory v6 (one-path additive layout)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/tooling-inventory-v6-subject.json`
**Manifest SHA-256:** `3f0e683d88795ef8bb8667106c567deeb2a3106480c02a0286fd5594fa59be2f`
**Members:** 3
**Verdict:** **ACCEPT-UNIT**

Additive file-inventory layout only. It adds the single path `tools/contracts/tsconfig.json`. It does not install that file, approve its bytes, select generator05, select loader policy, activate packages, or settle bootstrap. Filename approval is not implementation acceptance.

## Custody

3/3 subject members match architecture bytes before and after. Paths are POSIX-sorted unique.

Parent inventory v5 is the architecture-accepted inventory (`docs/implementation/m1/repository-file-inventory.v5.json` `ec7292f6545e564bae77a8b56ca34ee51af94b70ab3b7484feaecb6df2f22687` / 118054). That parent has actual Grok ACCEPT-UNIT at `docs/implementation/m1/reviews/grok-tooling-inventory-v5/review.json` `c5607c5fca925515c72079fef24bcade2d22d4ccc3cf8d0a08243cdb15391f93` / 2839 and root unit `docs/implementation/m1/tooling-inventory-v5-unit.json` status `ACCEPTED-UNIT`, `rootSubstantiveAssent: true`, `requiredUnitFindings: []`. This review does not rewrite that verdict.

Live product `design-lock.json` `37169104a3de12db15e9390eadb282eff190d1262f0d0b4c6d70bb66e51dafef` still selects inventory v4 only. A genuine private product chain with inventory5+generator-selection-v1 already passed `verify_design.py` (`/tmp/opensip-implementation/m1-generator-activation-01/verify.stdout`, `passed: true`); live product is not updated. Current live lock still verifies without this unit.

## Additive layout

Parent v5 has 323 files and 20 packages. Candidate v6 has 324 files. **323 inherited rows are byte-equal by value.** Removed paths: none. Added paths: exactly `tools/contracts/tsconfig.json`. All inventory keys other than `standing`/`files` (`schemaVersion`, `packages`, `pendingDecisions`) are unchanged, including the 20 package definitions and dependency lists. Candidate file paths are sorted unique. Successor `addedFiles` equals that one path.

The new row is owned by existing package `tooling` (most-specific prefix `tools/contracts`), role `configuration`, `generated: false`. No `node_modules` or `tools/contracts/python-packages/` first-party rows. No package, lock, wheel, or policy change.

## CLI passage inheritance

`apps/cli/src/bootstrap.rs` remains `files[7]` with the identical v5 row (path, package, role, description, generated, standing). Metadata-v2 passage inheritance can continue through v6 by stable row path. This unit does not silently settle root package-manager or report bundler descriptions.

## Must-fix / should-fix

None in this additive-layout scope. Required findings remain empty.

## Remaining

Selecting this inventory into a lock, materializing `tools/contracts/tsconfig.json`, generator-selection-v2 design acceptance, loader policy, public activation, checker bootstrap, M1, and release are separate. This ACCEPT-UNIT does not accept generator05 code.
