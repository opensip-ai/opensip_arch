# Independent Grok review: schema inventory04

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-schema-inventory-subject-04`
**Manifest SHA-256:** `6e9145ef1549a467fb9547b50c7b5bfb6a5b33838d2e127b6d67ad12cf0a9c1c`
**Members:** 10
**Verdict:** **ACCEPT-UNIT**

Additive file-responsibility/layout unit only. Extends accepted 202-row inventory3 by 44 owned source paths. Does not select schema IDs, majors, generator, package manager, toolchain, or product files. Does not rewrite inventory3 or names-01.

## Custody

Verified before and after. Frozen subject not executed against. Architecture pins in `input-pins.json` match the architecture checkout and the freeze copies.

| Check | Result |
| --- | --- |
| Manifest | `6e9145ef…9c1c` matches declared |
| Files | 10 listed = 10 walk; no extras, modes, or symlinks |
| Architecture pins | 5/5: parent v3, candidate v4, successor v3, source-map, auxiliary-input-map |
| After | frozen hash unchanged |

## Additive inventory

Parent `docs/implementation/m1/repository-file-inventory.v3.json` (`63027fb6…16ee`, 71497 bytes, 202 rows) is the accepted inventory3 candidate already bound in the product lock. Candidate v4 (`c6c85fb8…84f5`, 87766 bytes, 246 rows) adds exactly the 44 sorted unique paths in `inventory-successor.v3.json`.

Independently:

- 20 packages, package edges, and 9 pending decisions are byte-equal to parent.
- All 202 inherited rows are equal by value, including the four inventory3 tooling exceptions.
- Added set = source-map `implementationPath` (40) ∪ auxiliary `implementationPath` (3) ∪ `{schemas/source-map.json}`. The two maps are disjoint.
- Every added row: package `shared-assets` (most-specific owner of `schemas/`), `generated: false`, standing `proposed`, nonempty description, path under `schemas/`.
- Roles: 40 `schemas/sources/*-vN.schema.json` plus native IDL and native metaschema are `model`; `schemas/source-map.json` is `registry`; `schemas/profiles/report-codec.json` is `configuration`. No new `schema` role.
- Product destinations use `name-vN.schema.json` (and `-meta` for the native metaschema). Architecture sources keep historical `name.vN.schema.json`. Each source-map row maps `*.vN.*` → `*-vN.*` and the architecture bytes/hashes verify.

`check.py` prints `sourceSelectionApproved: false` and `productImplemented: false`. Product `schemas/` is absent. Pending decision “Bind exact schemas…” remains.

## names-01 unaccepted draft

Retained at `docs/implementation/m1/audits/schema-inventory-names-01/` (receipt `ROOT-DRAFT-NAMING-CORRECTION`, `productModified: false`). That draft’s v4 inventory is `9d5a061c…f6de` / 90404 bytes, not this candidate. It uses dot-vN destinations and role `schema` on 42 rows (40 sources + both native wire files). Substituting it for `candidate.json` makes private `check.py` fail. It was never accepted or installed.

## Parent tooling exceptions

The original v1 inventory checker (`docs/operations/check_repository_file_inventory.py`) requires every row `standing == "proposed"` and test names `_tests.rs` / `.test.ts`. Applied to parent or to this full candidate it fails first on `crates/identity/src/canonical_tests.rs` standing `implementation refinement candidate; actual Claude acceptance pending`. The same standing remains on `design-lock.json`, `tools/verify_design.py`, and `tools/tests/test_design_binding.py` (`test` role, Python name). Those four rows are byte-identical to parent. Exempting standing and the Python test name, this candidate’s additions pass the original JSON/role/ownership/folder rules. The exceptions were not rewritten to satisfy the v1-only checker.

names-01, with those exemptions, still fails: unknown role `schema` on `baseline.v2.schema.json`, and after mapping `schema`→`model`, JSON filename `baseline.v2.schema.json`.

## `inventory_successor` binding

Product `tools/verify_design.py` `inventory_successor` requires five closed pins `{parent, candidate, record, review, assent}`. Review vocabulary is `verdict: ACCEPT-UNIT` with empty `requiredFindings`, assessment `verdict: ACCEPT` with empty `requiredFindings`, and the assessment object itself carrying the candidate `path`/`sha256`/`bytes`. Assent is `ACCEPTED-UNIT`. Additive only: packages and policy other than `standing`/`files` unchanged; inherited rows equal by value.

The product lock still selects inventory3 only (`addedFiles: 4`, candidate `63027fb6…16ee`). This v4 is not in the lock. Existing `verify_design.py --architecture opensip_arch` passes; `productQualification` is false. `InventorySuccessorTests` 12/12. Isolated against this freeze: an ACCEPT-UNIT shape with matching pins would close 44 additions; `CHANGES REQUIRED` refuses (`independent inventory acceptance missing or findings remain`); an assessment whose `sha256` is not the candidate refuses (`review candidate names a different subject`). No assent or lock record was written.

## Reproduction (private copy)

- `python -I -B check.py`: exit 0, stdout byte-identical to frozen `check.stdout`.
- Independent probes: **45/45**.
- Author-checker mutants (private copy, not restating the happy path): inherited-row rewrite; package-edge change; pending-decision append; dot-vN filename; `schema` role; `generated: true`; dropping `schemas/source-map.json`; substituting names-01 candidate. All refuse.
- Architecture source-map and auxiliary pins: 40 + 3 hashes/bytes match the architecture checkout. Every `semanticValidatorOwner` is an inherited parent inventory path and is named in the added row description together with the mapped `schemaId`.

## Must-fix / should-fix

None in this inventory-unit scope.

## Remaining

Exact schema bytes, generator, registry, and checked-in generated outputs remain a separate final source review. Chapter 14 is still generated from inventory v1 (198 files); this unit does not regenerate it. Tooling/bootstrap successor remains separate. Not product, milestone, or Claude agreement.
