# Existing-root diagnostics and wording — contract successor 468a

2026-09-27. Claude Opus 5.5, implementation lead. This is the contract successor that law 468 r3 requires in items 6 and 8. Grok accepted the law in 468 r3 on 2026-09-27. The three new codes are an owner decision made the same day. The unit is PROPOSED and needs independent review and root assent before selection.

## Three new domain details

The unit appends three codes to the current common4 `DomainDetailCode` enum, the same way the owner-selection unit appended `INSTALLATION.NOT_INITIALIZED`. The schema ID stays the same, and all 319 existing enum positions keep their places. No other schema byte changes.

| Detail | Class, exit | D9 error code | Fault cause |
|---|---|---|---|
| `CORE.NO_EMBEDDED_RELEASE` | request-rejected, 2 | `REQUEST.PRECONDITION_FAILED` | none |
| `INSTALLATION.ACCOUNT_REFUSED` | request-rejected, 2 | `REQUEST.PRECONDITION_FAILED` | none |
| `WORK.BUDGET_EXHAUSTED` | operational-failed, 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` | host-invariant |

- `reference/public-detail-registry.json` gives the owner-selection registry three new records, in sorted order, for 322 records in all.
- `diagnostic-routes.json` is law 468 item 6's complete routing table. The owner-selection routes are unchanged.
- No existing code, class or exit changes.

## Product materialization

`materialization-map.json` maps 10 product files, based on product b230250. Every other tracked file stays unchanged.

- **Schema source:** `schemas/sources/common-v4.schema.json`, whose bytes equal `schemas/common.v4.schema.json` here.
- **Generation maps and the closure:**
  - `schemas/source-map.json` and `schemas/registry.json`, which carry the source digest, the recipe's closure digest and its source set;
  - `tools/contracts/generator-closure.json`, where only two rows change: `source-map.json` and `common-v4`.
- **Admission maps:** `schemas/admission-registry.json`, whose bytes equal `schemas/admission-registry.json` here, and `schemas/admission-source-map.json`, which carries the common4 and registry architecture pins.
- **Native source pin:** the common4 length and digest in `crates/identity/src/schema_registry.rs`.
- **Generated outputs:**
  - `crates/contracts/src/generated/evidence.rs` gains three `Common4DomainDetailCode` variants, with their `Display` and `FromStr` arms;
  - `apps/report/src/generated/report.ts` gains the TS union members and the embedded common4 bytes. Its two provenance comments change.
- **Test:** `crates/host/src/schema_sources.rs` extends the existing test so that each new code is admitted by current common4 and the generated Common4 enum, and refused by common1, common3 and their generated enums.

The builder, generator binary, toolchain, build receipt and options are unchanged. The generator's executable is the existing `contracts-generator-rebuild-01` pin.

## Generation evidence

`evidence/run_generation468a.py` drives the selected pipeline on the prepared worktree. The public entry point cannot run yet, because the new architecture source is not selected. Before running, the script checks all 349 closure pins, the registry recipe joins and the build receipt.

- The pipeline passed with 40 sources and 8 outputs.
- Only `evidence.rs` and `report.ts` differ.
- Before these changes, a baseline run of the public entry point on the unmodified product reported no drift.
- `evidence/verify_scratch.py` runs the real `verify_design` with this unit appended. The review and assent are synthetic and exist only in memory, under `SCRATCH-468A/` paths. It passes with 40 generation sources, 48 admission sources and 69 contract successors.
- `evidence/drift_scratch.py` runs the real public `generate_contracts` entry point with the same in-memory assent, and it reports no drift. Neither script writes to either repository, and neither is review or assent.
- The live `verify_design` correctly refuses this candidate until it is selected, with "generation source is not selected by accepted design".
- After selection, a fresh drift check through the public entry point must pass.

## Passage overrides

The overrides are text only.

- **Law 468 item 8, in all three accepted command inventories** (coop v3, metadata-v2 v4 and the composed-owners proposal):
  - golden 37, `analyze-backup-choice-required-in-ci`, drops "or an admitted storage-policy record" from its situation and "or select another admitted root" from its remedy;
  - golden 0, `default-first-use-durable`, records that the account-derived installation root and "backup status unknown" were disclosed.
- **Inventory v74 descriptions**, which were stale:
  - `crates/security/src/initial_installation.rs` now describes the intent, storage and disclosure of law 464 and 465;
  - `crates/security/src/private_access.rs` now describes the charged private creation helpers;
  - `crates/identity/src/store_lineage.rs` now describes the one shared node spelling `LineageKey::relative_components` (product b230250).

## Limits

- Nothing emits these codes yet. Units 468b and 468c route them, and they must match exhaustively.
- No CLI, creator enablement, envelope field or doctor change.
- Development builds on macOS arm64 only.
