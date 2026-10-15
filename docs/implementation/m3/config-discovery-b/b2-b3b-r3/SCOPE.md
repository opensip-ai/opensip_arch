# B2-b3b r3: what the candidate delivers (M3-B unit B2-b3, sub-unit B2-b3b: the S3 downward walker)

**Lead scope record, 2026-10-15. Unreviewed candidate.** It implements section 3 of the accepted B2-b3 plan r2 (`config-discovery-b/b2-b3/PLAN-r2.md`; Codex `codex-b2b3-plan-r2`), with LD-B2B3-2 to LD-B2B3-6, LD-B2B3-8, LD-B2B3-11 and LD-B2B3-13, and the plan's R2-NBO-1. It also takes Codex B2B3A-R2-NBO-1 (the `gitdir:` race controls). Its base is product `f3384b5`: B2-b3a is bound, inventory is v193, and contract successors are 164.

## r3 changes (Codex `codex-b2b3b-r2`, REQUIRED-FINDINGS)

**B2B3B-R2-RF-1: pruning before custody when a pruned prefix is not a directory.**
- **The fix.** Before any custody judgment of a join, `named_root` now classifies the whole join with the chain's Cargo roots, as the core does, whatever the chain stopped on. A join through a pruned prefix that is a file, or absent, refuses before custody, so nothing on its chain is captured. The population is unchanged.
- **New vectors**, for both sources: `a/node_modules/x` with `node_modules` a file, and absent.
- **New control.** The oracle test now asserts that any join refused before custody (detail `JOIN_*`) has no capture in its trace.
- **New mutation.** `pruned-join-custody-judged`.

**B2B3B-R2-RF-2: every owned copy charged before it is made.**
- **Moved, not cloned.** A child's owned name and path are moved out of its level when visited (each child is visited once), never cloned.
- **The validator's copy.** The listing's charge now prices the validator's copy of the root-relative path that `LogicalPath::parse` builds: three copies per name.
- **The shared rule's temporaries.** Each classification is charged first (`classify_cost`): its segment list, one prefix copy per `target` segment, and the anchor's path.
- **Charged first.** The remaining uncharged copies are charged before they are made: the named chain's root spelling and the walk's root spelling.
- **Exempt.** A refusal's own record (its path or escaped name) is one terminal allocation at the refusal and is not charged. Charging it could replace the refusal with a budget row.
- **New controls,** with exact marginal costs:
  - **File children:** four prefix copies per file child (the listing's two, the spelling and the scope record);
  - **Directory children:** ten per ordinary directory child and five per pruned one, each copy enumerated in the test;
  - **Specs:** the spec control gains the first join's whole-path classification.
- **New mutations:** `classification-uncharged`, and `listed-path-uncharged` aimed at the validator's copy.

**B2B3B-R2-RF-3: the depth policy at a named root.**
- **The fix.** `subtree` applies the depth policy to its start. A named root of more than 256 segments is never listed; only its four marker names are observed, as the reference's `subtree` does.
- **New vectors:** explicit joins at depths 256, 257 and 260, and config roots at 257, each with a marker and an arbitrary child.
- **New control.** `a_named_root_beyond_the_listing_depth_is_never_listed`, for both sources.
- **New mutation.** `named-start-listed`.

There are now 52 vectors and 23 mutations. The evidence is lane r4.

## r2 changes (Codex `codex-b2b3b-r1`, REQUIRED-FINDINGS)

**B2B3B-R1-RF-1: capture only where the core's judgment reaches the ACL.**
- **The defect.** r1 captured every unit chain and every regular marker of a candidate, even past a directory the core refuses by its mode or owner, or past an ancestor's refusal. Named chains were captured before the crossing and pruned checks that refuse first.
- **The fix.** The core and the walker now judge with one function, `discovery_scan::judge_entry`. It returns `Passed`, `Refused(reason)`, or `NeedsAcl` when the metadata-only rejection passed and the ACL is uncaptured. The core's `custody` and the walker both call it. `discover_observed`'s fault is the core's `NeedsAcl`. The walker follows the core's order:
  - **Directories on a unit chain** (`directory_passes`, memoized per directory, with the waiver as the core applies it) are judged; a directory is captured only on `NeedsAcl` and then judged again. The chain stops at the first refusal.
  - **Markers** are judged only for a unit whose chain passed. A marker is opened and captured only on `NeedsAcl`. A marker its kind, owner or mode refuses is never opened.
  - **Explicit and config modes** judge each join, in order, right after its chain is walked:
    - a pruned prefix or a boundary refuses before any custody;
    - otherwise the root (for `.`) or each chain directory is judged, from the root down;
    - a component that is not a directory refuses by its kind;
    - only a reached root whose chain passed has its markers judged.

    Once a join refuses, or the specs exceed the cap, or a spec fails the grammar, the core judges nothing further, so later joins are walked for the population but never captured.
- **New controls:**
  - `a_metadata_rejection_captures_nothing_past_it_and_opens_no_marker`: a 0777 unit and a foreign owner each capture nothing, and a marker its mode refuses is never opened beside one that is;
  - `an_ancestor_refused_by_its_acl_stops_the_chain_there`: exactly one capture;
  - `a_crossing_join_captures_nothing_and_later_joins_are_not_judged`: no capture at all, while the later join is still listed.
- **New mutations:** `capture-ungated`, `chain-not-stopped-at-refusal`, `marker-ungated` and `judgment-continues-past-a-refused-join`.

**B2B3B-R1-RF-2: a path seen twice is one object.**
- **The fix.** `observe` compares every repeated observation with the scope's entry: the same device, inode and kind, and still present. Otherwise it refuses `Changed`. A new descriptor is never paired with an earlier entry's capture.
- **New control.** `a_shared_prefix_replaced_between_named_roots_refuses`: roots `a/u` and `a/v` share `a`. Between the two chains, `a` is replaced by a new directory holding the old children, their identities kept. The second chain refuses `Changed`, for both explicit joins and config roots.
- **New mutation.** `revisit-identity-unchecked`.

**B2B3B-R1-RF-3: owned storage is charged before it is allocated.**
- **The model.** Every owned record is charged as one object plus its bytes plus `RECORD`, a conservative 128-byte allowance for the allocation header, a map or set node and a vector slot. This covers:
  - each raw listed name, in the visitor;
  - each owned name and its root-relative path;
  - each child's spelling;
  - each new scope entry, with its key;
  - each observed-children slot, frame, listed-set entry, Cargo root, verdict, spec and normalized spec;
  - each captured ACL's entries.

  The Cargo roots on the path are now one set, with entries inserted and removed, instead of a per-directory copy.
- **New control.** `owned_paths_are_charged_with_their_length_under_deep_prefixes`, with exact marginal costs so that per-directory costs cancel:
  - The marginal cost of 64 more children, under an 8-level prefix of 100-byte names and under a short one, differs by exactly three prefixes per child: the child's spelling, its scope record and its parent's path in the listing.
  - 200 specs of 208 bytes against 200 of 8 differ by exactly five copies per spec: the spec, its normalized path, its spelling, its chain path, and the platform's own by-name observation of its name.
- **New mutations:** `spelling-uncharged`, `scope-record-path-uncharged`, `listed-path-uncharged` and `spec-uncharged`.

**NBO-1.** The vector count is 44 (35 accepted, 9 refused), not 46.

**NBO-2.** B2-b3a's `vcs_evidence` and `gitdir_target` now take the directory's spelling, for the trace only. They trace each by-name observation, the `.git` open, its capture and its read (`trace_child`, which builds nothing outside tests). New control: `the_evidence_probe_is_traced_and_a_gitdir_target_is_never_followed`.

**NBO-3.** Descriptor accounting now distinguishes a subtree (the frames on the current path, at most the root and depths 1 to 256) from a named chain (one per segment, up to 2,048 under the grammar, dropped before the named root's subtree).

**Also changed: no recursion.** The subtree walk is now an explicit stack of levels (`enter` and `subtree`) instead of recursion. The deeper r2 frames overflowed a 2 MiB test-thread stack at 257 levels, and the walk must not depend on stack size. Its order and observations are unchanged.

The evidence is lane r3. Lane r2 (kept in the work directory) caught 14 of the 20 mutations, and lane r3 resolves the other six:
- `metadata-only-rejection-skipped` did not compile, an error in the lane's replacement text.
- The revisit control swapped `a` inside the second chain's open, where the open's own identity comparison caught it first; it now swaps after the first chain's marker open, before the second chain observes `a`.
- The storage controls compared totals that carry per-directory costs, so each single charge had slack; they now assert exact marginal costs.

No product byte changed between lanes r2 and r3; only the walker's tests. There are 20 mutations: 11 of r1's carried over with new anchors, 9 new. r1's `unit-chain-not-captured`, `explicit-root-not-captured`, `named-chain-not-captured` and `non-regular-marker-opened` are replaced by the gated forms above.

## Paths

| Path | Change |
|---|---|
| `crates/security/src/custody/discovery_walk.rs` | **New.** The walker: `walk`, `discover_downward`, `WalkRequest`, `WalkRefusal`. |
| `crates/security/src/custody/discovery_walk_tests.rs` | **New.** Its controls. |
| `crates/security/src/custody/discovery_walk_vectors.json` | **New, generated.** 52 current-reference vectors. |
| `tools/security/discovery_walk_vectors.py` | **New.** The vector tool. |
| `tools/tests/test_discovery_fw01.py` | **New.** The FW-01 structural pin (LD-B2B3-11). |
| `crates/security/src/custody/discovery_scan.rs` | `ObservedAcl::NotObserved`, the metadata-only early rejection, `UnobservedAcl` and `discover_observed`. `discover` keeps its signature. |
| `crates/security/src/custody/project_admission.rs` | `VCS_MARKERS`, `vcs_evidence` and `gitdir_target` are visible to the walker. A test-only hook (`GitdirStep`, `set_gitdir_hook`) for the race controls. |
| `crates/security/src/custody/project_chain.rs` | A test-only `DiscoveryRoot::for_tests` over a scratch root with a test premise. |
| `crates/security/src/custody.rs` | Declares `#[cfg(target_os = "macos")] #[allow(dead_code)] pub(crate) mod discovery_walk` in the `include!` form. No export. |

## The walker (plan section 3)

`walk(&DiscoveryRoot, &WalkRequest, work) -> ObservedScope` charges the caller's one discovery ledger before every step. `discover_downward(root, upward, invocation, work)` walks, then runs B2-b2's core through `discover_observed`.

**Automatic mode** lists the root depth first, with each ancestor's descriptor retained on the frame stack. For each listed directory:
1. charge the listing (2 objects, 3 edges, 1,024 bytes), then each name before it is copied (1 edge plus its bytes); the platform's per-directory ceilings refuse as `ListingBound`, never truncation; the stream is closed before any child is observed;
2. discard exactly `.` and `..`; every other name must be one platform component (UTF-8, at most 1,023 bytes, no `/`, `\` or NUL, not `.opensip-stage-*`) whose root-relative path is a `LogicalPath` (each segment at most 255 scalars, at most 4,096 in all), or the whole walk refuses with `NAME_UNREPRESENTABLE:<parent>:<escaped bytes>`;
3. observe each name by one no-follow status read; a name gone by then refuses (`Changed`);
4. record a `Cargo.toml` file as a Cargo root for the subtree;
5. for each child directory, in name order:
   - a pruned anchor (`classify_entry` with the path's Cargo roots) is its own entry only, never opened;
   - a 257-segment directory is opened, compared with its observation, and only its four marker names are observed;
   - otherwise the child is opened and compared, then probed by name: its VCS evidence (B2-b3a's `vcs_evidence`, with the `gitdir:` value under S3 file custody) and its `opensip.json`; with either, it is a boundary and is never listed; otherwise it is listed.

The root's own VCS evidence comes from its listed children, the same four markers in the same order.

**Explicit and config modes** walk each named root once (duplicates once; a spec the grammar refuses, or beyond the 4,096 bound, is not walked and is the core's refusal). The root's `Cargo.toml` and `opensip.json` are observed by name. Then the chain runs parent-first, as the reference's chain walk does. Each chain directory is observed, then:
- **it stops** at a non-directory or a pruned prefix;
- **otherwise it is opened and compared,** its `Cargo.toml` and `opensip.json` are observed, it is probed for VCS evidence, and it is captured;
- **it stops** at a boundary.

At a reached named root, its four markers are observed by name and captured, then its subtree is listed by the automatic rule.

**Captures (LD-B2B3-3, LD-B2B3-6; r2).** Only objects whose judgment reaches their ACL are captured, as the r2 changes describe, each by one premise-applied capture, normalized to readable entries, an admitted omission (an empty list) or unreadable. The capture must be the object observed: device, inode and kind. Its sample then replaces the entry's metadata, so custody judges one capture's metadata and ACL. The captured objects:
- **automatic mode:** for each listed directory holding a regular-file marker, the chain from below the root to that directory, and its markers;
- **explicit and config modes:** the root, each named chain directory, and each reached named root's markers.

A marker that is a FIFO, socket, device or link is never opened. It keeps `NotObserved`, and its reason comes from its kind.

**The core (LD-B2B3-3).** An entry with `NotObserved` is judged by a metadata-only early rejection in the reference order: kind, owner, mode. Its reason is final. If it passes, the judgment needs the ACL. `discover_observed` then reports the instrument fault `UnobservedAcl` instead of a result, and `discover_downward` refuses with `WalkRefusal::Unobserved`. `discover` keeps its accepted signature for B2-b2's vectors, whose scopes are fully captured.

**Descriptors (LD-B2B3-4, R2-NBO-1; r2 NBO-3).** Retained: in a subtree, the frames on the current path (the root and depths 1 to 256); on a named chain, one per segment, dropped before its subtree. Temporary: one for a 257-segment directory or a marker (or the `.git` file under B2-b3a's read), and the listing stream, which closes before any child is observed. Running out refuses as host I/O.

**Refusals.** `WalkRefusal::discovery_refusal` maps only `NameUnrepresentable` to a discovery refusal (`PROJECT.ROOT_CUSTODY_REFUSED`). Every other refusal keeps its own row, mapped by B2-b3c's seam:
- `ListingBound` is the budget row;
- `Changed`, `Evidence`, `Capture` and `Premise` are a change or host I/O;
- `HostIo`;
- `Unobserved` is an instrument fault.

**The trace (LD-B2B3-13).** A test-only thread-local log of every `observe`, `open`, `list`, `probe` and `capture`. Production carries nothing.

## Lead decisions (implementation; within plan r2)

- **LD-B2B3B-1. A listed name gone by its observation refuses.** It is a change between listing and status read, never skipped.
- **LD-B2B3B-2. A capture is compared by identity, then its metadata stands.** A full-metadata comparison with the by-name observation would refuse ordinary directory time churn on active trees. The identity comparison (device, inode, kind) keeps the swap control.
- **LD-B2B3B-3. A listed directory's VCS evidence comes from its listing.** Only the root can be listed while holding it. A child is probed by name before it is listed, so a boundary's interior is never listed.
- **LD-B2B3B-4. Automatic mode does not capture the root.** The core never judges the root's custody there. Explicit and config modes capture it, since an explicit unit at `.` judges it.
- **LD-B2B3B-5. Escaping.** Graphic ASCII except `%` and `:` stays; every other byte is `%XX`.
- **LD-B2B3B-6. Test-only seams.** `DiscoveryRoot::for_tests`, the walker's `set_before_open` and B2-b3a's `set_gitdir_hook` exist under `#[cfg(test)]` only.

## Tests

- **`every_walk_vector_matches_the_reference_population_evidence_and_records`.** All 52 vectors are built under a scratch root and walked natively, with `/h/w` for the root. They pin the reference's path and SHA-256. For each:
  - **The population:** exactly the reference's paths, with their kinds.
  - **Custody inputs, with the r2 projection:**
    - owner for every entry;
    - mode for directories, files and FIFOs (a link's or socket's mode is set by the platform and never judged beyond its kind);
    - for captured entries only, the link count and the ACL's write grants in the reference's spelling.

    A `NotObserved` entry is compared by kind, owner and mode only.
  - **The evidence:** VCS presence, kind and target on exactly the probed directories.
  - **No-open traces** for every FIFO, socket and link.
  - **The core over the native capture:** status, refusal, path and detail; every downward provenance field, `workspaceDeclarations` excluded; and the boundary inventory byte for byte.

  The cases cover:
  - units at and below the root;
  - all four pruned reasons, and a repository hidden under a pruned anchor;
  - `target` with and without a Cargo root;
  - nested repositories (directory, `gitdir:` file, `gitdir:` file under an ACL grant, `.hg` file) and nested projects;
  - `.opensip` as a directory and as a file;
  - depth 256, and 257 hiding a repository and a config;
  - explicit joins and config roots, including `.`, a missing marker, a Cargo `target` join through both sources, crossings, absence, a file, grammar, `node_modules`, and a large sibling;
  - FIFO, socket and symlink markers, alone and beside a valid marker, in both source modes;
  - mode, group, authorized-group and ACL failures on chains and markers, hard links and the ACL-first order;
  - the waiver reaching the explicit chain and never a marker.
- **`listed_names_are_validated_as_logical_paths`.**
  - Segments of 255 and 256 scalars.
  - 255 two-byte scalars.
  - Bytes that are not UTF-8, a backslash, a staging name and NUL.
  - Complete paths of 4,096 and 4,097 scalars.
  - The detail's escaping.
- **`native_names_refuse_the_whole_walk_and_an_ordinary_listing_succeeds`.** A backslash name and a staging name each refuse natively with their detail. A 255-scalar name is admitted.
- **`complete_paths_of_4096_scalars_are_walked_and_4097_refuse`.** Native trees, built and walked by relative steps.
- **`the_ci_trace_touches_opensip_only_by_its_parents_observation`.** `.opensip` as a file is no row and no source.
- **`an_explicit_root_never_touches_a_large_sibling_and_needs_only_its_own_budget`.** A ledger sized to the explicit walk succeeds, where automatic mode exhausts it.
- **`a_same_kind_swap_between_observation_and_open_refuses`.** A chain directory and a marker.
- **`a_gitdir_file_changed_after_its_opening_or_its_judgment_refuses`.** B2B3A-R2-NBO-1: one race control for each full-metadata comparison in `gitdir_target`.
- **`a_read_only_tree_gives_identical_records_and_a_canary_is_never_touched`.** FW-01.
- **`exhaustion_refuses_as_budget_and_never_truncates`.** Each limit, one short.
- **`an_uncaptured_acl_the_core_reaches_is_an_instrument_fault`.** A metadata-only refusal needs no ACL.
- **`tools/tests/test_discovery_fw01.py`** (LD-B2B3-11).
  - **What it covers:** the production code, and its production `include!` closure, of `crates/host/src/configuration.rs`, `discovery_rule.rs`, `discovery_scan.rs`, `discovery_walk.rs` and `grants.rs`.
  - **What it forbids:** spawn, socket, filesystem write, create, rename and remove names, and the platform's create, publish and write primitives.
  - **Planted negatives:** a spawn, a socket and a write in every covered file, and a platform publication. A forbidden name inside a test module is not production. A production include is covered.
  - The host's `discovery.rs` must not exist yet; its owning unit (B2-c) adds it.

## Check lanes

See `evidence/checks.json`. The rows are:
- the security and host suites at base and candidate, with equal failure sets;
- the B1-b legacy admission spend probe, with equal lines;
- warning-denied all-targets Clippy;
- rustfmt on base-clean and new edited files;
- the environment pin;
- all three vector checks;
- the FW-01 pin;
- the configuration tables, the operability census and verify_design;
- 23 code mutations, each caught.

## Not claimed

- No seam and no flag rows (B2-b3c), and no public row mapping beyond `NAME_UNREPRESENTABLE`.
- No production caller (J1).
- No T2 census (B2-b4).
- No readers or members (B3-b).
- No export (B2-c).
- No qualification.
