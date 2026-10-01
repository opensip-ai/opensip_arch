# Stale inventory descriptions after 458c — contract successor 461b

2026-09-30. Claude Opus 5.5, implementation lead. Unit 461b of law 461 r3 item 8. Description-only: no schema, registry, generated code, product file or inventory successor changes.

## What it does

Eight text overrides on rows of the selected inventory, `repository-file-inventory.v80.json`. Each replaces a description made untrue by units 458c-b1, 458c-b2 and 458c-c (product 0ce4c72, 417d443 and d4239a5). Every new description was written against the committed code at d4239a5.

| Row | File | What was stale |
|---|---|---|
| 236 | `crates/security/src/custody/installation_fence.rs` | Described only the fence acquire. It now defines the `HeldFence` view, which the read session implements for production readers, and the old supplied and native fence remain for supplied-root tests only. |
| 240 | `crates/security/src/custody/installation_publication_tests.rs` | Said reads go "through the existing installation fence"; they go through the read session. |
| 247 | `crates/security/src/custody/installation_session.rs` | "no consumer uses it yet" is false. |
| 250 | `crates/security/src/custody/read_premise.rs` | "no read path uses it yet" is false. |
| 259 | `crates/security/src/installation_observation.rs` | "under a native installation fence" is false. It is now the production reader API over the read session. |
| 316 | `crates/security/src/trust/native_census.rs` | "retained native fence" is now a borrowed held-fence view. |
| 320 | `crates/security/src/trust/native_read_session.rs` | "borrowed native fence" is now the borrowed `InstallationReadFence` and its one ledger. |
| 321 | `crates/security/src/trust/native_record_capture.rs` | "retained native fence" is now a borrowed held-fence view. |

## Scope checks

- Every file changed between product 26d3d92 (inventory74) and d4239a5 was reread against its v80 description. Rows not listed above were found accurate, or carry an inherited override that this unit does not touch.
- The eight overrides are direct overrides on the final selected inventory, so `inventoryPassageInheritance` stays at its 8 rows. When a later inventory successor is made, these rows must be carried by value and these meanings projected, as 468a's were.
- None of the touched rows is an inherited row. A direct override on an inherited row would conflict with its projection.
- **461a independence.** None of the v80 descriptions of the 19 files changed by 461a mentions `possible_acl_writers`, an empty writer list, or omission meaning no writers. So no 461a override is needed, and this unit does not depend on 461a landing first.

## Evidence

`evidence/verify_scratch.py` runs the product checkout's real `verify_design` with this binding appended and an in-memory review and assent, without writing either repository.
