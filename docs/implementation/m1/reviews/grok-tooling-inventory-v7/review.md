# Independent Grok review: tooling inventory v7 (two-path additive layout)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/tooling-inventory-v7-subject.json`
**Manifest SHA-256:** `d6d8f771409001ede14dfac0fb449f0d4ccff6417acf82c6beba4f8fa49173ce`
**Members:** 3
**Verdict:** **ACCEPT-UNIT**

Additive file-inventory layout only. It reserves two test paths under the existing `tooling` owner. It does not install those files, approve checker09 bytes, approve the generic TypeScript orchestration wrapper, select bootstrap/policy, or settle M1. Filename approval is not implementation acceptance. Checker09 ACCEPT-UNIT and its evidence were not altered; S1 remains a separate successor10.

## Custody

3/3 subject members match architecture bytes before and after. Paths are POSIX-sorted unique.

Parent inventory v6 is architecture-accepted and **installed** in the live product lock:

- candidate `docs/implementation/m1/repository-file-inventory.v6.json` `52e75edc8a30aa304d2f3e42f541a5ece1c00d9e1f21435651ac29776d0b81c1` / 118433
- Grok review `docs/implementation/m1/reviews/grok-tooling-inventory-v6/review.json` `a18ed3a0ba9f764226921b10d92ff571b0f1da523b75a5d2955ab37dd80b61e3` / 2793
- root unit `ACCEPTED-UNIT`, `rootSubstantiveAssent: true`, `requiredUnitFindings: []`
- live lock `inventorySuccessors` includes that v6 candidate; `inventoryPassageInheritance` already parents v6 `/files/7/description`

This unit is not in the live lock. Inventory v6 subject SHA-256 `3f0e683d88795ef8bb8667106c567deeb2a3106480c02a0286fd5594fa59be2f` is unchanged. This review does not rewrite that verdict.

## Additive layout

Parent v6 has 324 files and 20 packages. Candidate v7 has 326 files. **324 inherited rows are byte-equal by value.** Removed paths: none. Added paths, matching `successor.json` `addedFiles`:

- `tools/tests/test_typescript_check.py`
- `tools/typescript-boundary/tests/generated-outputs.test.mjs`

All inventory keys other than `standing`/`files` (`schemaVersion`, `packages`, `pendingDecisions`) are unchanged, including the 20 package definitions. Candidate file paths are sorted unique. No `node_modules` or `python-packages/` first-party rows.

## Naming and responsibility

Both new rows are `package: tooling` (most-specific prefix `tools`), `role: test`, `generated: false`.

| Path | Convention | Responsibility |
| --- | --- | --- |
| `tools/tests/test_typescript_check.py` | Python underscore `test_*.py`, same directory as existing `tools/tests/test_design_binding.py` | Orchestration/wrapper path-pin and process-group cleanup regressions. Does **not** approve unimplemented `tools/check_typescript.py` behavior. |
| `tools/typescript-boundary/tests/generated-outputs.test.mjs` | Hyphenated `*.test.mjs`, same tree as `amd-loaders.test.mjs` / `boundary.test.mjs` | Checker compile/check-cycle regressions. Does **not** re-approve checker09 implementation (already a separate ACCEPT-UNIT; S1 is successor10). |

Neither path is present in the live product tree (same class of reservation as `tools/check_typescript.py`). Synthetic fixture pins named in descriptions are mechanics only.

## CLI passage inheritance

`apps/cli/src/bootstrap.rs` remains `files[7]` with the identical v6 row. Metadata-v2 passage inheritance can continue through v7 by stable row path. This unit does not settle root package-manager or report bundler descriptions.

## Must-fix / should-fix

None in this additive-layout scope. Required findings remain empty.

## Remaining

Selecting this inventory into the live lock, materializing the two test files, checker09 product install, orchestration-wrapper implementation, bootstrap/policy, M1, and release are separate.
