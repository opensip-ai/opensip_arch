# B2-c2b description successor (contract successor 173)

**Lead record, 2026-10-16. Proposed; it needs Codex review and root assent.**

This successor refreshes four inventory row descriptions that no longer describe their files. B2-c2b implemented M3-B r10's record bounds for item 14a, and wrote S10b's remedy into the product. The rows B2-c2 wrote still say "as r9 amends it", list only the 32-node and 64 KiB checks, and name S10's native model copy (contract successor 167) as the vector source.

The successor uses passage overrides on the rows of `docs/implementation/m2/repository-file-inventory.v212.json`, the selected inventory. B2-c2b adds no path, so there is no inventory successor to carry new rows, and an override on the selected inventory is the only form.

**Description only.** No inventory row other than these four descriptions changes. Nothing changes in the schema, product, law or any package.

| Row | Why the old text is stale |
| --- | --- |
| `crates/host/src/typescript_config.rs` | It cites item 14a "as r9 amends it" and lists the cycle, 32-node and 64 KiB checks. It now also enforces r10's 64-entry `extends` and 4,096-character path bounds. |
| `crates/host/src/typescript_config_tests.rs` | It omits the schema admission of every replayed graph and the new bounds test. Row 59 now carries S10b's remedy. |
| `crates/host/src/typescript_config_vectors.json` | It names "the S10 native model copy (contract successor 167)". The vectors now come from S10b's copy (172), with r10's controls and S10b's remedy. |
| `tools/host/typescript_config_vectors.py` | It cites item 14a "as r9 amends it" and S10's model copy. It now reads r10 and pins S10b's copy, with S10's registry copy unchanged. |

`successor.json` gives each override's exact before and after text.
