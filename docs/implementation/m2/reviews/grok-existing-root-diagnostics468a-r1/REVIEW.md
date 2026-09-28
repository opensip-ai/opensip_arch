# Review: existing-root diagnostics 468a

Grok is the single reviewer. Claude Opus 5.5 leads. Review of the diagnostic contract successor for law 468 r3 items 6 and 8. No repository edits.

Subject `docs/implementation/m2/existing-root-diagnostics-468a-subject.json`, 5152 bytes, sha256 `b813e2f2efca543bad37e5772abbc9669373017f66bc539637c1875944ffacdb`. All 25 pins match, including `product.diff` (3606532 bytes, sha256 `e63a8e889406de0715d3c8dde52b28cb2dade0cade1ada6b0222c710bfec500c`). The worktree `/Users/sb/code/opensip-ai/opensip-468a` is `b2302506f3b43cd79f9e64e99ae01b5e78f09970`. Its diff is that file, and the ten changed files match the archived copies and `materialization-map.json`.

## Verdict

**ACCEPT-DESIGN-UNIT.**

## Law 468 items 6 and 8

`DomainDetailCode` grows from 319 to 322 by appending `CORE.NO_EMBEDDED_RELEASE`, `INSTALLATION.ACCOUNT_REFUSED` and `WORK.BUDGET_EXHAUSTED`. The preceding 319 entries are unchanged, and no other schema byte changes. The registry has the same 319 records plus these three, in code order. Their selectors state the r3 terminations:

- the first two are request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`;
- `WORK.BUDGET_EXHAUSTED` is operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, fault cause `host-invariant`.

`diagnostic-routes.json` is the item 6 table, including `LEDGER.BUSY_TIMEOUT` with detail `PROJECT.BUSY` and fault cause `ledger-busy`, `HOST.IO_FAILURE` with fault cause `host-io` and no new detail, and continuation for `LostRace`, `NotPristine` and `Published`. The owner-selection route file is an unchanged parent.

The twelve overrides resolve to the parent text. In all three command inventories, golden `analyze-backup-choice-required-in-ci` drops "or an admitted storage-policy record" and "or select another admitted root", and golden `default-first-use-durable` records the account-derived installation root and "backup status unknown".

## Regeneration

The closure has 349 files. Only `schemas/source-map.json` and `schemas/sources/common-v4.schema.json` change. The recipe's source set and closure digest follow those bytes. The saved pipeline output `assembly/output` matches the candidate `evidence.rs` and `report.ts`. The enum, the Rust `serde` names, and the TypeScript union are the same 322 codes in the same order. `Display` and `FromStr` gain the three arms. The report provenance comments are the new registry digest `cde02c13…` and closure digest `7fcfa104…`. The host test admits the three codes on current common4 and refuses them on common1 and common3.

## Descriptions at b230250

The three inventory rows are `initial_installation.rs`, `private_access.rs` and `store_lineage.rs`. At that commit the first mints and rechecks the actor, classifies storage as `Unknown`, applies the backup choice, writes the disclosure, and consumes one intent at StepId 0. `private_access.rs` judges the private ACL, creates the private file and directory, appends the zero-rights allow, observes a private directory, and spends the reserved OpenSIP sample. `store_lineage.rs` exposes `relative_components` as `transitions/lineage/S/G/K.node`.
