# B2-b4a r2: what the candidate delivers (M3-B unit B2-b4, sub-unit B2-b4a: the T2 census instrument and record)

**Lead scope record, 2026-10-15. Unreviewed candidate.** It implements section 1 of the accepted B2-b4 plan r2 (`config-discovery-b/b2-b4/PLAN-r2.md`; Codex `codex-b2b4-plan-r2`, after round-1 findings B2B4PLAN-R1-RF-1 to RF-3). Its base is product `02fd45c`: B2-b0 to B2-b3 are bound, inventory is v195, and there are 164 contract successors.

## r2 changes (Codex `codex-b2b4a-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2B4A-R1-RF-1:** workspace integrity checked member identities, not the overlay record or the mounts | **`verified_workspace`.** The overlay root must be a directory (a symlink root refuses before traversal). The record must be exactly the manifest's canonical `overlay` (FETCH-SPEC section 2), with SHA-256 equal to `overlayDigest`, and byte-equal to the archived acquisition copy. The mounts must be exactly the record's. Each mount must link to its own entry's store path, through the guarded `store_path`, with the entry's digest equal to the record's. Controls: a renamed mount (to `node_modules`), swapped mount targets, an altered record and a symlink root each refuse; a pinned overlay passes. |
| **B2B4A-R1-RF-2:** gitlink placeholders skipped the 0555 check | A placeholder must be an empty 0555 directory. Controls (synthetic gitlink pins computed independently): a valid placeholder passes; a writable, a non-empty and a symlink placeholder each refuse. |
| **B2B4A-R1-RF-3:** the walk-vector soundness test accepted an incomplete walk | Both soundness tests now go through `soundness`, which refuses a walk that did not complete (a typed discovery refusal is a completed result). All 52 vectors and 4 composed workspaces complete. New control `an_aborted_native_measurement_never_passes_as_soundness`: a vector on a 10-object ledger stops early, is charged less than the prediction, and is refused. |
| **NBO-1:** the tightness wording | Corrected below: 46 of 56 exact. |

The census figures are unchanged. The evidence is lane r3.

## The outcome: the census fails the margin, and the caps return to the law

The integrity-verified census covers the 39 lead-readable repositories and the 5 workspaces (as composed checkouts). **Three fail the 2× objects margin. One of them exceeds the discovery profile's object cap itself.**

| Entry | Objects | Edges | Object margin | Edge margin | 2× |
| --- | --- | --- | --- | --- | --- |
| `rs-very-large-aws-sdk-rust` | 2,611,910 | 1,007,224 | 0.401 | 2.082 | **no** |
| `mr-ts-very-large-smithy-sdk` (workspace) | 572,330 | 439,389 | 1.832 | 4.772 | **no** |
| `ts-very-large-aws-sdk-js-v3` | 540,986 | 403,655 | 1.938 | 5.195 | **no** |
| `ts-very-large-aws-cdk` | 388,491 | 182,836 | 2.699 | 11.470 | yes |
| `poly-large-rspack` | 381,347 | 302,096 | 2.749 | 6.942 | yes |
| `py-very-large-home-assistant` | 332,508 | 119,895 | 3.153 | 17.491 | yes |

The limits are 2^20 objects and 2^21 edges. Every other entry passes; the lowest passing object margin is 2.699.

**Edges pass everywhere. Objects fail.**
- `aws-sdk-rust` lists 25,746 directories and 270,995 names.
- The walker charges eight objects per listed name: the raw name, the owned name with its path and validator copy (three), the spelling, the by-name observation, the scope entry, and the observation slot.
- So the walk would refuse with `WORK.BUDGET_EXHAUSTED` long before completing.

By M3-B r5 item 12 and the plan (section 1.6, LD-B2B4-5), the record states `caps: returned-to-law`, and **no test claims the margin**. B2-b4b (plan section 2) is the item-12 amendment. The held-out margin stays outstanding. B2-b is not complete.

**The model is an upper bound, and often exact (r2, NBO-1).**
- On the 52 walk vectors and 4 composed workspaces, the native walker's objects and edges equal the model's prediction exactly in 46 of 56 cases.
- The model over-counts in the other ten:
  - where custody refuses before or after a capture;
  - where a capture records ACL entries rather than taking the filesystem branch;
  - where a `.git` read is shorter than its envelope (`nested-gitdir-file-repository`: 440 edges against 475 predicted).
- For the T2 entries, the claim is the upper bound. Exactness is shown only for the three stores the lead probe walked.
- The `census-soundness` lines in `evidence/test-census-soundness.log` list every ratio.

**Confirmed on real stores (lead probe, supporting evidence only).**
- **Setup.** A throwaway worktree of the base raised the discovery limits (to 2^24 objects, 2^23 edges and 2^34 bytes) and added one ignored test, which walked four lead-readable stores natively. It was never committed, and its diff is `evidence/lead-probe-tree.diff`.
- **Objects and edges.** For `aws-cdk`, `aws-sdk-js-v3` and `aws-sdk-rust`, the native charges equal the census exactly (`evidence/lead-probe-real-stores.log`).
- **Bytes (not censused here).** `aws-sdk-rust` used **639,480,718 bytes**, with a 134-byte root spelling, against the 2^30 byte cap. That is a 1.68× margin, and it grows with the root path. Item 12 (r2 NBO-1) says bytes are bounded by other means. For the walker's own charged storage, this evidence says otherwise. B2-b4b's amendment must take bytes up too. The census does not model bytes (plan r2), so this is recorded, not claimed.

## Paths

| Path | Change |
| --- | --- |
| `tools/security/discovery_census.py` | **New.** Integrity, the population cross-check, the cost model, the composed workspaces, both outputs, `--check` and `--write`. |
| `crates/security/src/custody/discovery_census.json` | **New, generated.** The census record. |
| `crates/security/src/custody/discovery_census_vectors.json` | **New, generated.** The model's predictions for the 52 walk vectors and 4 composed-workspace vectors (with their trees). |
| `crates/security/src/custody/discovery_census_tests.rs` | **New.** The soundness control and the margin record control. |
| `crates/security/src/custody.rs` | Declares `discovery_census_tests` (`cfg(all(test, target_os = "macos"))`, `include!`), the file's own pattern. No other change. |
| `tools/tests/test_discovery_census.py` | **New.** The census-tool controls. |

## The tool (plan r2 sections 1.1 to 1.5)

**Integrity.**
- Each lead-readable store is walked with `os.lstat` and `os.scandir` only.
- The Git tree object (gitlinks from `submodulePolicy`, as empty 0555 placeholders) and the QD-22 `treeDigest` (with the blob count) are recomputed from the stored bytes and must equal the manifest's pins. All 39 match.
- These refuse:
  - a directory not 0555;
  - a file not 0444 or 0555, or with more than one link;
  - a non-regular object;
  - an extra object;
  - a `.git` path component.
- `store_path` is the only join of a digest to the store. It refuses a held-out entry before any filesystem call. Workspace overlays are read no-follow. Their member symlinks are resolved only against lead-readable store paths, and the members must equal the manifest's `memberIds`.

**Population (LD-B2B4-1).** Every modeled walk (vector, store and composed workspace) is compared with the bound B2-b0 reference's `walker_population` over the same tree, through the walk-vector tool's adapter and pins. They are equal everywhere, and a difference refuses.

**The cost model.**
- `Model` mirrors `discovery_walk.rs` step for step: `walk`, `named_root`, `subtree`, `enter`, `list`, `observe`, `directory_passes`, `capture_markers`, the probe and `gitdir_target`.
- Unknowns are taken at their dearer branch:
  - every judgment captures and passes;
  - every capture takes the dearer of the ACL-entry record and the filesystem premise;
  - every listing returns `.` and `..`;
  - a regular `.git` file is read at the uninterrupted envelope, min(L, ceiling) + 1 attempts.
- Interrupted retries are excluded. The margin is structural (RF-2). No T2 walk reads.

**The closure (RF-3).**
- 15 files are pinned whole: plan r2's 14 plus `custody.rs`, which holds the `.git` read limit, `MAX_CONFIG_BYTES`.
- 23 anchors read every constant. Each must match exactly once.
- The delegated `status_read_cost` is read from `path_binding.rs` and added to `open_child_directory_cost`'s own term.

**Workspaces (RF-1).** A workspace is censused as the composed checkout: the overlay root's own entries, with each member's verified tree as a directory at its mount name. It goes through the same model and population check.

## The controls

**Native (`discovery_census_tests.rs`).**
- `the_cost_model_bounds_the_native_walker_on_every_walk_vector`: each of the 52 vectors is materialized and run through `discover_downward` on a fresh `discovery_profile` ledger. The walk must complete (r2), and its `used()` must not exceed the prediction. It also checks that the predictions pin the current walk vectors.
- (r2) `an_aborted_native_measurement_never_passes_as_soundness`.
- `the_cost_model_bounds_the_native_walker_on_composed_workspaces`: the same over 4 composed workspaces:
  - units at several depths;
  - a member that is a boundary, and one that is a repository;
  - pruned segments in a member;
  - a member 253 segments deep.
- `the_census_pins_the_cost_closure_as_compiled`: both records' closure pins equal the compiled files' bytes.
- `the_census_margin_is_classified_against_the_profile_limits_and_never_claimed_for_a_failing_entry`:
  - each entry's `passes2x` equals whether a fresh discovery ledger admits twice its cost (the code's limits, never the record's copy);
  - `failingEntries` and `caps` follow from it;
  - the ten held-out rows are outstanding;
  - the record's limits are exactly the profile's.
- The helpers repeat the closed walk tests' own, which stay unmodified.

**The census-tool controls (`test_discovery_census.py`, 16 tests; r2 adds the gitlink-placeholder and workspace controls).** These cover:
- the pinned constants;
- delegated-cost drift (`status_read_cost` edges changed, the caller untouched) refusing;
- a planted charge outside every anchor refusing;
- an anchor that stops matching refusing, even with the pin bypassed;
- the read envelope at L = 0, 1, 4,095, 4,096, ceiling − 1, ceiling and beyond;
- a verified synthetic store;
- a `.git` component refusing;
- an extra file refusing;
- the held-out guard: a planted held-out digest directory is never touched (every `lstat`, `scandir`, `listdir`, `readlink` and `open` recorded).

**The model mutations (the lane).** Each patches the tool, regenerates the predictions, and must make the native soundness tests fail:
- `observation-charge-dropped`
- `capture-edges-dropped`
- `dot-entries-forgotten`
- `workspace-member-sum` (the r1 formula)

## Check lanes

The evidence is lane r3, over the r2 candidate. Lanes r1 and r2 (the r1 candidate; r1 had no `--nocapture` soundness step) are kept in the work directory. See `evidence/checks.json`. The rows are:
- the security suite at base and candidate, with equal failure sets and at least five new passing tests;
- warning-denied all-targets Clippy on host and security;
- rustfmt on base-clean and new edited files;
- the environment pin, the three existing vector checks, the FW-01 pin, the configuration tables, the operability census and verify_design;
- the census controls;
- the census `--check` over the T2 cache;
- the four model mutations.

## Not claimed

- No margin for any failing entry, and none for the held-out entries.
- No cap change (B2-b4b, after the item-12 amendment).
- No production caller, no byte census and no qualification.

B2-b is not complete.
