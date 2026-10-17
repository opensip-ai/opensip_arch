# C2a-2 r1: the shared synthetic component fixtures

**Standing:** UNREVIEWED CANDIDATE. Test-support only: no production code, no public API, no qualification.

**Authority:**
- the C2a plan r4 (`c2a/PLAN-r4.md`; `codex-c2a-plan-r4`, ACCEPT), sub-unit C2a-2, LD-C2A-6 and the Q4 ruling;
- law M3-C r8 item 8 (`PROPOSAL-r8.md`:451-466), with C2-T6, C2-T7 and C2-T8's label half.

**Candidate base:** product main `e770404`, which holds the integrated C2a-1 r1 (`codex-c2a-1-r1`, ACCEPT-UNIT). C2a-2 was built in the worktree `opensip-c2a2` on C2a-1 r1's exact candidate bytes, and moved onto main once C2a-1 landed there.

## 1. The change

| Path | Change |
| --- | --- |
| `crates/security/src/trust/component_fixtures.rs` (new) | The shared module, `core_authentication::tests::components`. It holds `LABEL` (`"synthetic"`, `scenario.rs`'s label), CR-1's five `ROLES`, a `Synthetic` component (its role, version, declaration, `{os, arch}` and supplied files), and `body`: a role-valid canonical body with C2PM-1's `closureProtocolMajor` and a tree built from the supplied bytes. `release` gives the envelope and the release row, every artifact carrying `LABEL`; `release_row` is the same with an explicit artifact profile; `every_role` gives one body per role. |
| `crates/security/src/trust/component_fixtures_tests.rs` (new) | 5 controls (§3). |
| `crates/security/src/trust/core_authentication.rs` (base-dirty; hand-edited, not reformatted) | The module is included inside the existing `tests` module, so it adds no predicate site. `Spec` gains `components` (bodies by index, default empty). `signed_release` uses a listed body and its labelled row, and otherwise the pre-existing `component_body` and `component_release`. `component_release` now goes through `release_row` with the pre-existing `p1` profile, byte for byte. |
| `crates/security/src/trust/trust_bootstrap_tests.rs` | One control: C2-T6's C2a-2 leg (§3). |

There are six new tests: five in the fixtures module and one in `trust_bootstrap_tests.rs`.

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

## 4. Mutations

Nine, each run against the focused tests, which must fail:
- the label dropped (`p1` on new rows);
- the pre-existing rows' bytes changed (`LABEL` on `component_release`);
- the declaration dropped;
- the analyzer's command rules applied to every role;
- the supplied file bytes ignored in the tree digests;
- `Spec.components` ignored;
- a non-fixture signer (the root's keys signing a manifest);
- the TR-INDEX signer signing the components;
- the fixtures compiled outside the joint predicate (`debug_assertions` added to it).

## 5. The lane

`evidence/run_c2a2_checks.py`, adapted from C2a-1's, ran at `e770404`. Every row passed, and all nine mutations were caught.
- **Suites:** security 1212 → 1218 (+6) and host 412 → 412, with 14 and 8 pre-existing failures, equal on both sides.
- **Static checks:**
  - warning-denied all-targets Clippy on security;
  - rustfmt on the base-clean files (`core_authentication.rs` is base-dirty and hand-edited, not reformatted);
  - the workspace all-targets check;
  - the `scenario-fixtures` and `crash-matrix` checks;
  - a release build of security.
- **Tests:** the focused tests, which include the crash-matrix site census.
- **Censuses and design:**
  - the environment exceptions;
  - operability with an unchanged mint audit;
  - the census closure, unchanged;
  - verify_design.

**Rules held:** no environment read, no `let _ =`, and no signing or private test key read. The module signs only through the existing `sign` with the public test-only seeds. No new key, root, role or feature is introduced.

## 6. Open questions

- **Q-C2A2-1:** is LD-C2A2-3's reading of "every artifact carries `LABEL`" right, with the pre-existing `p1` rows unchanged?
- **Q-C2A2-2:** is placing the module inside the existing `tests` module the right way to meet "under exactly" the joint predicate, rather than a new pinned site?

## 7. Inventory

There are two new paths and two changed ones, whose rows stay true. The successor is numbered at integration from the lock's last plus one, after the combined C1c-0 and C2a-1 v223, so it is v224 or later. Its draft is `/tmp/opensip-implementation/prepare_c2a2_inventory.py`.
