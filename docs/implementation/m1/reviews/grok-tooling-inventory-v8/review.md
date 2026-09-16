# Independent Grok review: tooling inventory v8 (two-path additive layout)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/tooling-inventory-v8-subject.json`
**Manifest SHA-256:** `68c3855e6e12e0b5a02e734d8b9775a99d5e51ca8c9dc5f8199544d98e507b7c`
**Members:** 3
**Verdict:** **ACCEPT-UNIT**

Additive file-inventory layout only. It reserves two paths under the existing `tooling` owner. It does not install those files, approve Cargo checker02 runtime/purity, approve bootstrap, or settle M1. Filename approval is not implementation acceptance. Checker10 and inventory v7 archives were not altered.

## Custody

3/3 subject members match architecture bytes before and after. Paths are POSIX-sorted unique.

Parent inventory v7 is architecture-accepted and **archived**, not live-installed:

- candidate `docs/implementation/m1/repository-file-inventory.v7.json` `763a5431ebd0aac23dfdd2bb95bacc5ae930dc50763c147a97b93fd8be91e111` / 119227
- Grok review `docs/implementation/m1/reviews/grok-tooling-inventory-v7/review.json` `4b9bd97745fc4bc60fd960ee9ebeaec7c75123e0b7a154e383cedbf12a853bb2` / 4368
- root unit `ACCEPTED-UNIT`, `rootSubstantiveAssent: true`, `requiredUnitFindings: []`
- live lock still selects inventory v6 (`52e75edc…0b81c1`); v7 and v8 are absent

Inventory v7 subject SHA-256 `d6d8f771409001ede14dfac0fb449f0d4ccff6417acf82c6beba4f8fa49173ce` is unchanged. This review does not rewrite that verdict.

Separately, `docs/implementation/m1/package-boundaries-unit.v1.json` records Cargo checker02 as Claude `ACCEPTED-UNIT` with `integrationApproved: false` and a remaining obligation to add tool paths through reviewed additive inventory. That code unit is **not** this layout verdict. This review did not rerun those 14 tests or Cargo metadata.

## Additive layout

Parent v7 has 326 files and 20 packages. Candidate v8 has 328 files. **326 inherited rows are byte-equal by value.** Removed paths: none. Added paths, matching `successor.json` `addedFiles`:

- `tools/check_package_edges.py`
- `tools/tests/test_package_edges.py`

All inventory keys other than `standing`/`files` (`schemaVersion`, `packages`, `pendingDecisions`) are unchanged, including the 20 package definitions. Candidate file paths are sorted unique. No `node_modules` or `python-packages/` first-party rows.

## Naming and responsibility

Both new rows are `package: tooling` (most-specific prefix `tools`), `generated: false`.

| Path | Role | Convention | Responsibility |
| --- | --- | --- | --- |
| `tools/check_package_edges.py` | `entrypoint` | Underscore `check_*.py`, same directory as reserved `tools/check_typescript.py` | Cargo manifest/locked-offline-metadata DAG check entry. Does **not** approve checker02 bytes or bootstrap wiring. |
| `tools/tests/test_package_edges.py` | `test` | Underscore `test_*.py`, same directory as `tools/tests/test_design_binding.py` / reserved `test_typescript_check.py` | Isolated Cargo boundary regressions. Does **not** re-approve checker02 tests. |

Neither path is present in the live product tree (same reservation class as `tools/check_typescript.py`).

## CLI passage inheritance

`apps/cli/src/bootstrap.rs` remains `files[7]` with the identical v7 row. Metadata-v2 passage inheritance can continue through v8 by stable row path. This unit does not settle root package-manager, report bundler, or bootstrap selection.

## Must-fix / should-fix

None in this additive-layout scope. Required findings remain empty.

## Remaining

Selecting inventory v7 then v8 into the live lock, materializing the two files, checker02 product install, bootstrap, M1, and release are separate.
