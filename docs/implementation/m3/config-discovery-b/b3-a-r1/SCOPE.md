# B3-a r1: what the candidate delivers (M3-B unit B3-a, `grants.rs`)

**Lead scope record, 2026-10-14. Unreviewed candidate.** It implements the accepted plan `config-discovery-b/b3-a/PLAN-r1.md` (Codex `codex-b3a-plan-r1`, ACCEPT, no findings) on product `ec70009` (B1-b and inventory v189 bound).

## Paths

| Path | Change |
|---|---|
| `crates/security/src/grants.rs` | **New** (inventory v189's planned-absent row). The four records, `GrantRefusal`, `storage_write_choice`. |
| `crates/security/src/grants_tests.rs` | **New.** Plan section 3's controls. |
| `crates/security/src/storage_choice_vectors.json` | **New.** 144 SLM vectors, generated. |
| `tools/security/storage_choice_vectors.py` | **New.** The vector tool, in the B1-a pattern. |
| `crates/security/src/lib.rs` | A private `#[allow(dead_code)] mod grants;`. No `pub`, no re-export. |
| `crates/security/src/custody/project_chain.rs` | `ProjectChainPolicy::from_grants(premise, home_filesystem, &AuthorizedGroups)`, delegating to the unchanged `new`. |
| `crates/security/src/custody/project_chain_tests.rs` | One test: `from_grants` lends exactly the record's set. |

## Delivered against plan section 1

- **The records (1.1).**
  - `AuthorizedGroups::from_invocation(&[u32])` collapses duplicates, keeps first-occurrence provenance, and refuses more than 64 distinct gids as `TooManyGroups { count }` (LD-B3A-2, LD-B3A-3). It offers `contains`, `provenance` and `as_set`.
  - `ProjectOwnerWaiver::from_invocation(bool, Option<&Path>)`: without the flag it is `Ok(None)`; the flag without a project is `OwnerWaiverWithoutExplicitProject`, whose `termination()` is the existing `InstallationTermination::ProjectExplicitPath` (`PROJECT.EXPLICIT_PATH_INVALID`). The root spelling is carried as given.
  - `BackupCustodyAcknowledgement::from_invocation(bool) -> Option<_>`.
  - `PolicyRecordId::parse` takes exactly 64 lowercase hex digits. `ConsentSource { PreExistingPolicy { record }, InteractiveConsent }` has `workflow()` and `grant_mode()`: `pre-existing-policy`/`policy-record` and `interactive-consent`/`interactive-explicit` (SL:1110).
  - Every record has private fields, so the module's constructor is the only way to build one. Only `Debug`, `PartialEq` and `Eq` are derived.
- **S3.1 (1.2).** `storage_write_choice(backup, ephemeral, Option<BackupCustodyAcknowledgement>, Option<&PolicyRecordId>, ci)` follows SLM `storage_write_admission`'s order. The acknowledgement is taken by value.
  - Its `choice()` returns the reference's spellings.
  - A `Refuse`'s `termination()` is the existing `InstallationTermination::BackupChoiceRequired`, which the host projects to `REQUEST.PRECONDITION_FAILED` / `storage.backup-choice-required` (`crates/host/src/installation_termination.rs:79-83`).
  - `POLICY_FILE_WRITTEN` and `ROOT_IDENTITY_CHANGED` are `false` constants.
- **`--ephemeral` (1.3).** No new type (LD-B3A-1). B1-a's `configuration_leaf(SharedFlag::Ephemeral) == None` already holds, and the new pin also checks that `configuration.rs` and `configuration_tables.rs` name no record and no `Durability`.
- **Unchanged:**
  - `initial_installation::storage_choice`, the installation-creation S3.1 decision under laws 464 and 465;
  - the legacy `ProjectChainPolicy::new`;
  - every host file.

## Tests (plan section 3)

- **The records.** 0, 1, 64 and 65 distinct gids, with duplicates and their provenance order. The waiver's three cases and their rows. The acknowledgement. The record grammar: valid, empty, 63 and 65 digits, uppercase, non-hex, a trailing newline, a leading space, and non-ASCII digits. The SL:1110 mapping.
- **S3.1.** `every_slm_vector_is_reproduced` covers all 144 combinations of SLM's five inputs:
  - three backup classes;
  - ephemeral;
  - the flag;
  - six record inputs: absent, one lawful id and four malformed;
  - CI.

  It checks the choice spelling, admit or refuse, the refusal's row fields and the two `false` facts. It pins SLM's path and SHA-256, and asserts 10 refusals and 2 record admissions. `the_choice_order_is_the_references` pins the order directly.
- **No configuration path.**
  - A compile-time probe asserts that no record implements any of 21 traits. The probe uses two blanket impls; a forbidden impl makes it ambiguous, error E0283. The traits:
    - `Clone`, `Copy`, `Default` and `FromStr`;
    - `From` of `bool`, `u32`, `&[u32]`, `Vec<u32>`, `&str`, `String`, `&Path`, `PathBuf`, the JSON value and a reference to it;
    - `TryFrom` of `bool`, `&[u32]`, `Vec<u32>`, `&str`, `String`, the JSON value and a reference to it.
  - A source pin: the module's code, comments excluded, contains no conversion, default, `Clone`, `Copy` or serde, and its derives are exactly `Debug, PartialEq, Eq`.
  - No other security source has an `impl` line that names a record.
  - The module is private and not re-exported.
  - The crate manifest has no `serde`.
  - The host resolver sources name no record.
- **Purity.** The module's code names no `std::fs`, `std::io`, `std::env`, `std::process`, `std::net`, platform crate or `unsafe`. Its `use` lines are pinned exactly. It is inside B1-b's `disallowed-methods` lint.

## Check lanes

The evidence is lane r2. Lane r1 ran on the same candidate bytes, and every row passed except one control: `foreign-impl` was NOT CAUGHT.
- **Cause.** The control itself was wrong. Its planted line was a function *taking* an `AuthorizedGroups` inside `impl ProjectChainPolicy`. That is not an impl *for* a record, so the pin was right to ignore it.
- **Fix.** r2 plants a real inherent `impl crate::grants::AuthorizedGroups { .. }` in `project_chain.rs`.
- No product byte changed between r1 and r2. r1's log is kept in the work directory, not in the stage.

## Lead decisions in this candidate

**LD-B3A-4, compile check by in-crate probe, not by a rustc snippet.**
- Plan section 3 named the host admission tests' rustc-snippet style. That harness compiles cases against the host crate's public `.rmeta`. `grants` is private to security and reachable from no public surface, so a snippet there could only show "private module" (E0603). That is true by construction, and it would not show that a record lacks a conversion.
- Adding a case to that accepted X8 harness would also change its pinned census.
- The probe runs in the security crate's own test build, on the real types. The check lane's four compile controls show that it fires: deriving `Clone`, deriving `Default`, `impl FromStr`, and `impl From<bool>` each fail the test build with E0283.
- **Rejected:**
  - a host snippet case, for the reasons above;
  - a feature-gated public seam to make the module nameable, which would add surface.

**LD-B3A-5, the record grammar is the schema's, not Python's `$`.**
- SLM checks `HEX64 = ^[0-9a-f]{64}$` with Python `re.match`, whose `$` also matches before a final newline. So SLM admits `<64 hex>\n`.
- The policy-record id's grammar is 64 lowercase hex, and JSON Schema patterns do not have that newline allowance. `PolicyRecordId::parse` refuses the newline.
- The vectors therefore exclude that one spelling (the tool says why), and a product-only test pins the refusal. This matches B1-a's newline-suffixed profile case.
- **Rejected:** copying the Python quirk.

## Not claimed

- No custody consumer: B2-b and B3-b.
- No CLI parsing: M4.
- No S3.1 caller: J.
- No public row for the group bound: M4.
- No execution, mutation or recovery grant.
- No public API and no environment read.
- No law change and no qualification.
