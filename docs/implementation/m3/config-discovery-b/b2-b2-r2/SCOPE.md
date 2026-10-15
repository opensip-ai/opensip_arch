# B2-b2 r1: what the candidate delivers (M3-B unit B2-b, sub-unit B2-b2: the pure discovery core)

**Lead scope record, 2026-10-15. Unreviewed candidate.** It implements section 1.2 of the accepted B2-b plan r4 (`config-discovery-b/b2-b/PLAN-r4.md`; Codex `codex-b2b-plan-r4`). Its base is product `f51769f`: B2-b1 is bound, B2-b0 is contract successor 164, and inventory is v191.

## r2 changes (Codex `codex-b2b2-r1`, REQUIRED-FINDINGS)

**B2B2-1: the order of a marker's file judgment.**
- **The defect.** The shared judge checks a file's link count and size before its captured ACL. SLM `_file_custody` checks the ACL first. A marker failing both therefore reported `HARD_LINKED` or `TOO_LARGE` where the reference reports `WRITABLE_BY_ACL` or `ACL_UNREADABLE`.
- **The fix.** The core now judges through `reference_order`: kind, owner, mode and the real ACL first, through `check_project_object_waived` with one link and no size standing in; then links and size against S3's own bounds.
- **The legacy judge keeps its order,** which is accepted for its existing callers. A test shows both orders side by side.
- **New vectors.** Eight current-reference vectors: ACL write or unreadable ACL combined with a hard link or oversize, each alone, and two waived explicit chains whose foreign-owned marker is still refused.
- **New mutation.** `links-and-size-before-acl` restores the shared order and is caught.

There are now 79 vectors (65 accepted, 14 refused). The evidence is lane r3.

## Paths

| Path | Change |
|---|---|
| `crates/security/src/custody/discovery_scan.rs` | **New.** The pure core. |
| `crates/security/src/custody/discovery_scan_tests.rs` | **New.** Its controls. |
| `crates/security/src/custody/discovery_scan_vectors.json` | **New, generated.** 71 current-reference vectors. |
| `tools/security/discovery_scan_vectors.py` | **New.** The vector tool. |
| `crates/security/src/custody/project_chain.rs` | `check_project_object_waived(..., waiver: Option<&ProjectOwnerWaiver>)`. `check_project_object` now calls it with `None`, so the legacy path is the same judgment. |
| `crates/security/src/custody.rs` | Declares `#[cfg(target_os = "macos")] #[allow(dead_code)] pub(crate) mod discovery_scan` in the `include!` form. No export. |

## The core (plan 1.2)

`discover(scope, root, upward, invocation) -> DiscoveryResultPending` is SLM `finish` (SLM:753-841) as the bound current reference runs it, over an `ObservedScope`. The scope is what the walker (B2-b3) observed, keyed by absolute spelling:
- `DescriptorMetadata`;
- `ObservedAcl::{Entries, Unreadable}`, where a premise-admitted omission is an empty list;
- for a probed directory, `ObservedVcs`.

**Steps, in SLM's order:**
1. Nested repositories (directories with VCS evidence below the root).
2. Nested projects (`opensip.json` outside nested repositories and pruned trees).
3. The exclusive unit source:
   - **explicit joins and config roots** (`_explicit_units`): the 4096 bound; `JOIN_PATH_GRAMMAR`; `JOIN_CROSSES_NESTED_REPOSITORY`; `JOIN_CROSSES_NESTED_PROJECT`; `JOIN_INSIDE_PRUNED_TREE:<reason>:<anchor>`; chain custody, where ABSENT or NOT_A_DIRECTORY gives the explicit-path row and anything else the root-custody row; markers; and the marker-less warning;
   - **automatic:** the shared rule's `enumerate_units` with observed directories, the basis and unreadable anchors; then exclusions in order (`INSIDE_NESTED_REPOSITORY`, `INSIDE_NESTED_PROJECT`, `DEPTH` beyond 256, `DIRECTORY_CUSTODY:<why>` at the failing directory, `MARKER_CUSTODY:<marker>:<why>`); then the cap counted after exclusions.

**Custody** runs through the product's own judge (`check_project_object_waived`), so the vocabulary is `Refusal::code()`'s SLS spelling. For files it runs in the reference order (`reference_order`; r2). The typed waiver (LD-B2B-9):
- reaches only the root-to-unit directory chains;
- never reaches a marker;
- skips only the owner comparison. Mode, ACL, links and size still apply.

**Records (LD-B2B-3).**
- **`DiscoveryProvenancePending`** is V3 without `workspaceDeclarations`. It has no serializer, no `impl` and no completion, and no `WorkspaceDeclaration*` type exists: a source pin holds all of that.
- **`DiscoveryResultPending`** carries the refusal code and its D9 (SLM `D9`; `DiscoveryD9V1`).
- **`boundary_inventory(&result)`** gives the complete `AdmittedBoundaryInventoryV3`, with members empty until B3-b. `BoundaryInventory::to_json` is its closed record. A non-accepted result is `InventoryRefusal::NotAccepted`.
- **Upward provenance** is selection's (B2-b3) and passes through.
- **Not mapped here:** no public row and no rendering.

## Tests

- **`every_current_reference_vector_is_reproduced`.** The vectors pin the reference's path and SHA-256. All 71 reproduce:
  - 45 discovery cases that reach `finish`;
  - 34 controls (26 of the reference checker and 8 of the marker judgment order, r2) (the four pruned reasons with hidden repositories and VCS annotations, Cargo-`target` joins through both sources, the ordinary `target`, crossing order, nested-in-nested, explicit and config siblings, markers below anchors, and units, config and VCS boundaries at depths 256, 257 and 258).

  Every partial-provenance field compares, `workspaceDeclarations` excluded, with 65 accepted and 14 refused. Every accepted result's boundary inventory equals the reference's byte for byte. The 19 cases that refuse before `finish` are upward selection and are listed by id in the vectors; they are B2-b3's.
- **`the_waiver_skips_only_the_owner_comparison`.** For directories and config files: foreign owner refused without the waiver and admitted with it; others-write and ACL write still refused under it; the legacy judge equals the waived judge with `None`.
- **`the_waiver_reaches_the_explicit_chain_and_never_a_marker`.** A foreign-owned explicit chain refuses without the waiver. With it, the unit is admitted while its foreign-owned `package.json` is `MARKER_CUSTODY:package.json:FOREIGN_OWNER`.
- **`the_pending_provenance_cannot_be_emitted_or_completed`,** a source pin.
- **`a_boundary_inventory_needs_an_accepted_result`.**
- **`the_core_is_pure`,** a source pin: no filesystem, I/O, environment, process, network, retained descriptor, work scope or `unsafe`.
- **`the_inventory_drops_units_already_explained_by_a_nested_boundary`.** Added after lane r1. Units inside a nested repository and a nested project are excluded as `INSIDE_NESTED_*` in the provenance, and the boundary inventory does not repeat them as custody exclusions.

## Check lanes

The evidence is lane r2. Lane r1 (kept in the work directory) passed every row but one control: the mutation `inventory-keeps-inside-nested` was NOT CAUGHT.
- **Cause.** A real test gap. No vector's accepted result carries an `INSIDE_NESTED_*` exclusion, so nothing checked the inventory's filter.
- **Fix.** r2 adds the test above. No product byte changed.

## Not claimed

- No walker or observation, no upward provenance capture, no ledger, no CI or scope trace and no public row (B2-b3).
- No T2 census (B2-b4).
- No readers, members or `workspaceDeclarations` (B3-b).
- No export (B2-c).
- No qualification.
