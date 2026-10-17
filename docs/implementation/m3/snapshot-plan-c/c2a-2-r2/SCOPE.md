# C2a-2 r2: the shared synthetic component fixtures

**Standing:** UNREVIEWED CANDIDATE. Test-support only: no production code, no public API, no qualification.

**Authority:**
- the C2a plan r4 (`c2a/PLAN-r4.md`; `codex-c2a-plan-r4`, ACCEPT), sub-unit C2a-2, LD-C2A-6 and the Q4 ruling;
- law M3-C r8 item 8 (`PROPOSAL-r8.md`:451-466), with C2-T6, C2-T7 and C2-T8's label half.

**Candidate base:** product main `50f1ac1`. That is the v225 lock, over v223 (the combined C1c-0 and C2a-1 inventory), D2b-3a, v224 and CI-1, on C2a-1's integration at `e770404`. The worktree `opensip-c2a2` moved from `e770404` to `01769e9` by hand. The lane runner then followed main inside the lock, through `feb7739` to `50f1ac1`, because main's changes touch none of the candidate's paths.

**Round 2** answers `codex-c2a-2-r1` (REQUIRED-FINDINGS, `C2A2-R1-RF-1`), whose Q rulings are adopted:
- **RF-1: JSON-escape the supplied paths and entrypoints.** `body` no longer interpolates any supplied string into JSON text.
  - Every directory row, file row, the entrypoint and the platform row are built as JSON values. They are encoded by the identity crate's canonical encoder, so every lawful path is escaped exactly as `canonical.rs` escapes it, quotes, controls and non-ASCII included.
  - `release_row` is built the same way. The pre-existing literal was already the canonical encoding, so its `p1` bytes are unchanged; the byte-preservation control still compares them with that literal.
  - Paths are not narrowed: no ASCII-only restriction is imposed.
- **New controls:**
  - `c2a2_escapable_supplied_paths_are_encoded_exactly_and_admitted`. Every role's body over `ESCAPABLE_FILES` round-trips through the canonical encoder and carries the canonical escapes. The supplied paths are a quote in the first-file entrypoint and in its directory prefix, U+0001, a tab, a newline, DEL, U+001F and non-ASCII names, including a non-ASCII directory. Each body decodes to exactly the supplied paths, entrypoint, directories, lengths and digests, and passes the real body validation. A backslash path is encoded and decoded exactly, and is refused by the validator's own path rule (`Error::Path`), not by the generator.
  - `c2a2_escapable_paths_admit_through_the_ordinary_reader_into_a_candidate`. The whole C2-T6 chain runs over those bodies: the signed release, the InitialCore, acceptance, the full ordinary reader, and C2a-1's bridge and candidate. Each candidate's Blobs are exactly the supplied paths in path-byte order, so C2a-1's hand encoder escapes them as `$defs/closure` admits them.
- **New mutations:** a file path's quote dropped, the entrypoint escaped twice, and a directory prefix's quote dropped.
- **Q-C2A2-1 and Q-C2A2-2 were ruled "not a finding"** (r1 REVIEW.md), and are kept as decided.

## 1. The change

| Path | Change |
| --- | --- |
| `crates/security/src/trust/component_fixtures.rs` (new) | The shared module, `core_authentication::tests::components`. It holds `LABEL` (`"synthetic"`, `scenario.rs`'s label), CR-1's five `ROLES`, a `Synthetic` component (its role, version, declaration, `{os, arch}` and supplied files), and `body`: a role-valid canonical body with C2PM-1's `closureProtocolMajor` and a tree built from the supplied bytes. `release` gives the envelope and the release row, every artifact carrying `LABEL`; `release_row` is the same with an explicit artifact profile; `every_role` gives one body per role. |
| `crates/security/src/trust/component_fixtures_tests.rs` (new) | 6 controls (§3). |
| `crates/security/src/trust/core_authentication.rs` (base-dirty; hand-edited, not reformatted) | The module is included inside the existing `tests` module, so it adds no predicate site. `Spec` gains `components` (bodies by index, default empty). `signed_release` uses a listed body and its labelled row, and otherwise the pre-existing `component_body` and `component_release`. `component_release` now goes through `release_row` with the pre-existing `p1` profile, byte for byte. |
| `crates/security/src/trust/trust_bootstrap_tests.rs` | C2-T6's C2a-2 leg over the default and the escapable trees (§3). |

There are eight new tests: six in the fixtures module and two in `trust_bootstrap_tests.rs`. The latter share one helper, over the default and the escapable trees.

## 2. Lead-decision candidates

- **LD-C2A2-1. The module's place and predicate.**
  - It is included inside `core_authentication.rs`'s `tests` module, the existing home of the signed-release builders and the public test-only signers.
  - It is therefore compiled under exactly that module's `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`, as the Q4 ruling requires.
  - It adds no predicate site: the crash-matrix site census (`crash_matrix_sites.rs`, `every_test_feature_site_is_on_the_pinned_list`) is unchanged.
- **LD-C2A2-2. Signers and root.** Signing goes only through the existing `sign`, with `COMPONENT_SIGNER` (and the catalog's `INDEX_SIGNER`), under the existing synthetic root. No key, seed, root or feature is introduced. The module names none (a source pin).
- **LD-C2A2-3. Existing bytes.**
  - `component_body`, `component_release` and an empty-`components` `signed_release` keep every byte. A control compares `component_release` with the literal it wrote before.
  - The pre-existing rows keep `archiveProfileId` `p1`. `LABEL` is on every row the new module writes (C2-T8's label half): "every artifact" is read as every artifact the generator produces, and existing fixture bytes stay unchanged.
- **LD-C2A2-4. Role validity.**
  - The bodies are `COMPONENT_MANIFEST` with the role, version and declaration set.
  - For every role but the analyzer, commands are removed and capabilities and permissions are empty (CR-1, as `component_manifest.rs`'s `cr1_body`).
  - Major 1 is each non-analyzer role's supported major, and equals the analyzer's `providerProtocol` (C2PM-1's shared rule).
  - The tree's regular files are exactly the supplied bytes, with their lengths and digests. Directory rows cover every proper prefix, every file is `0755`, and the entrypoint is the first file.
- **LD-C2A2-5. C2-T6 is shared.**
  - C2a-2's leg drives the whole lawful chain short of retention: the signed release, the InitialCore, acceptance onto a P0 installation, the full ordinary reader over the accepted store (each body validated under its host context), C2a-1's bridge, and C2a-1's candidate for every role. The analyzer runs under a test-selected subprotocol (LD-C2A1-3).
  - C2a-3's verifier completes C2-T6, and nothing here claims retention or admission.

## 3. Controls

| Plan control | Test |
| --- | --- |
| LD-C2A-6: role-valid bodies with C2PM-1's declaration and supplied trees | `c2a2_every_role_body_is_role_valid_with_its_declaration_and_tree` |
| C2-T8's label half; the signers | `c2a2_release_rows_carry_the_label_and_join_their_bodies` |
| LD-C2A-6: existing bytes unchanged | `c2a2_pre_existing_builders_keep_their_bytes`, with the existing suites (equal failure sets) |
| the signed release of every role | `c2a2_signed_release_of_every_role` |
| C2-T7: the source pin over the predicate | `c2a2_the_fixtures_exist_only_under_the_joint_predicate`, the unchanged crash-matrix site census, and the lane's release build of security |
| C2-T6's C2a-2 leg | `c2a2_every_role_admits_through_the_ordinary_reader_into_a_candidate` |
| C2A2-R1-RF-1: escapable paths, encoded, decoded and validated | `c2a2_escapable_supplied_paths_are_encoded_exactly_and_admitted` |
| C2A2-R1-RF-1: escapable paths through the signed reader and candidate | `c2a2_escapable_paths_admit_through_the_ordinary_reader_into_a_candidate` |

## 4. Mutations

Twelve, each run against the focused tests, which must fail:
- the label dropped (`p1` on new rows);
- the pre-existing rows' bytes changed (`LABEL` on `component_release`);
- the declaration dropped;
- the analyzer's command rules applied to every role;
- the supplied file bytes ignored in the tree digests;
- `Spec.components` ignored;
- a non-fixture signer (the root's keys signing a manifest);
- the TR-INDEX signer signing the components;
- **(r2) a file path's quote dropped;**
- **(r2) the entrypoint escaped twice;**
- **(r2) a directory prefix's quote dropped;**
- the fixtures compiled outside the joint predicate (`debug_assertions` added to it).

## 5. The lane

`evidence/run_c2a2_checks.py`, as r1's with the three r2 mutations, ran at `50f1ac1`. Its results are in `evidence/c2a2-checks-r2/`. Every row passed, and all twelve mutations were caught.
- **Suites:** security 1240 → 1248 (+8) and host 412 → 412, with 14 and 8 pre-existing failures, equal on both sides.
- **Static checks:** warning-denied all-targets Clippy, rustfmt (`core_authentication.rs` base-dirty, not reformatted), the workspace check, the feature checks and the release build.
- **Tests:** the focused tests, including the crash-matrix site census.
- **Censuses and design:** the environment exceptions, operability (mint audit unchanged), the census closure and verify_design.

**Attempt history.** Attempt 1 (`/tmp/opensip-implementation/c2a2-checks-r2-void-attempt1/`, not packaged) ran on the same product bytes and passed every row but one mutation. `entrypoint-escaped-twice` was written with a malformed Rust literal, so it failed to compile rather than being caught. Its literal was corrected, and the corrected mutant was checked to compile and fail the two escapable-path controls. The lane was then rerun on the same product bytes.

**Rules held:** no environment read, no `let _ =`, and no signing or private test key read. The module signs only through the existing `sign` with the public test-only seeds. No new key, root, role or feature is introduced.

## 6. Open questions

None new. r1's two were ruled "not a finding".

## 7. Inventory

There are two new paths and two changed ones, whose rows stay true. The successor is numbered at integration from the lock's last plus one, after the combined C1c-0 and C2a-1 v223. v224 and v225 are bound since, so it is v226 or later. Its draft is `/tmp/opensip-implementation/prepare_c2a2_inventory.py`.
