# B2-b4 implementation plan r2 (M3-B unit B2-b, sub-unit B2-b4: the T2 census and margin)

**Lead plan, 2026-10-15. For Codex review.** It refines section 1.4 of the accepted B2-b plan r4 (`config-discovery-b/b2-b/PLAN-r4.md`, LD-B2B-4) and M3-B r5 item 12 (`config-discovery-b/PROPOSAL-r5.md:397`). Product base `02fd45c` (inventory v195, 164 contract successors), architecture `e0fe80bc` (shared r95). B2-b0 to B2-b3 are bound.

## r2 changes (Codex `codex-b2b4-plan-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2B4PLAN-R1-RF-1:** workspace member sums omit the nesting charges | **Replaced.** A workspace is censused as one **composed tree**: the overlay root's own non-symlink entries, plus each member's verified tree mounted as an ordinary directory at its mount name. This is the layout of a real checkout, not the symlink mounts, which the walker never follows. The composed tree goes through the same reference population and the same model as a repository (section 1.5). The native control gains composed-workspace vectors (members nested under a root, including a member that is a boundary, a member under a pruned segment, and members that are units). A new mutation, which falls back to the r1 member-sum formula, must fail it. |
| **B2B4PLAN-R1-RF-2:** a file length does not bound read attempts | **The census claim is split** (section 1.3, read envelope). On the walk, the only charged read is `gitdir_target`'s read of a regular `.git` file. Git rejects a `.git` path component in a tree (fsck `hasDotgit`), and integrity **refuses** any T2 entry with one (fail closed), and **no censused T2 walk performs a charged read.** For the native vectors, which do have regular `.git` files, the model charges the uninterrupted envelope: 1 object, plus min(L, ceiling) + 1 edges (each attempt either returns at least one byte or ends at EOF). `EINTR` retries (`work_reader.rs:183`) are **excluded and stated**: each costs one edge with no bound but the ledger, and exhaustion refuses as `WORK.BUDGET_EXHAUSTED`, never truncation. So the margin is structural. New controls: a planted T2 entry with a `.git` component is refused, and a model unit test checks the envelope for L = 0, 1, 4,095, 4,096 and the ceiling. |
| **B2B4PLAN-R1-RF-3:** the pin closure omits `path_binding.rs` | **The closure is the whole transitive cost code** (section 1.3 and the inventory below). Every file is pinned whole by SHA-256, and each charge's formula is extracted by an anchored match. Any change to any file in the closure refuses, delegated costs included. Two new controls: a copy of the closure with `status_read_cost`'s edges changed (the calling expression in `directory_open.rs` untouched) must refuse; and so must one with a charge added to a pinned file that is outside every anchor. |

## 0. Why a sub-plan

Plan r4 says the census "converts the counts to ledger objects and edges with B2-b3's cost model, which it pins from the code". B2-b3b's accepted walker has no single cost model: it charges at about thirty sites across the walker and the platform primitives it calls, and some charges depend on facts a tree listing does not carry (whether custody reaches an ACL, whether the ACL attribute is returned). This plan fixes how the census models those charges, how the model is shown to be sound against the native walker, and what B2-b4 delivers when the margin fails.

**A pre-census estimate, not evidence.** A no-follow name count of the lead-readable stores (not integrity-verified, no cost model) gives `rs-very-large-aws-sdk-rust` 25,745 directories and 245,250 files. The walker charges at least eight objects per listed name (section 1.2), so its walk costs at least about 2.17 million objects: over the discovery profile's 2^20 objects itself, not only under a 2× margin. `ts-very-large-aws-sdk-js-v3` (56,056 names, at least about 448,000 objects) sits near the 2× line of 524,288. So the expected outcome is that the census fails the margin and, by item 12, **the caps return to the law for revision**. This plan is written for that outcome and for the passing one.

## 1. B2-b4a: the census instrument and record

### 1.1 Integrity (`tools/security/discovery_census.py`)

For each lead-readable repository entry of the T2 manifest (`docs/implementation/m3/corpus/t2-corpus-manifest.draft.json`, the 39 entries with `heldOut: false`), the store `store/<treeDigest.value>/` in the private durable cache named by the acquisition record (`corpus/t2-acquisition-2026-10-06-r1`):
- **No-follow traversal.** `os.lstat` and `os.scandir` only, never following a symlink. A symlink's bytes are its target text (`os.readlink`).
- **Both pins are recomputed from the stored bytes.** The QD-22 `treeDigest` (the manifest's own definition) and the Git `gitTree` (SHA-1 tree objects built from the blobs, the modes and, for gitlinks, the pinned commit from `submodulePolicy.gitlinks`). Either mismatch refuses the entry.
- **The population is exact.** Any file not in the tree, any directory that is neither an ancestor of a tree path nor a gitlink placeholder, any mode other than the store's (directories 0555, files 0444, executables 0555) and any non-regular non-symlink object refuses the entry.
- **Held-out entries are never opened.** The tool reads only the manifest's `heldOut` flag and `id` for them. Its store lookup is guarded so that a held-out digest is never joined to the store path. The ten are written as `outstanding: held-out`.
- No network, no repository code, no subprocess. It runs under `-I -B`.

### 1.2 Population and counts

- **The population is the reference's, not a new rule.** The tool builds SLM's synthetic `fs` from the verified store with the same adapter `tools/security/discovery_walk_vectors.py` uses (its `slm_input` shape: owner 1000, the store's modes, `vcs` from the first present `.git`, `.hg`, `.svn`, `.jj`), selects the store root as an explicit `--project` in automatic mode, and runs B2-b0, the current discovery reference (contract successor 164), at its accepted architecture bytes. `walker_population` gives exactly what the native walker observes; `finish` gives the units.
- **Counts per entry**, all from that population:
  - listed directories and their listed names;
  - visited child directories, pruned anchors (NeverEnter), opened directories and boundaries;
  - per opened directory, how many VCS markers the probe observes (one to four) and whether `opensip.json` is present;
  - Cargo roots; directories whose chain is judged (once each); units whose chain passes; present regular workspace markers in those units;
  - the count of `target` segments in each visited child's path (it scales `classify_cost`);
  - regular `.git` files and their byte length (the `GITDIR` read cost).

### 1.3 The cost model, pinned from the code

The census converts counts to **objects and edges only** (item 12, r2 NBO-1: bytes are bounded separately).

**(r2) The closure.** Every file is pinned whole by SHA-256, and any byte change refuses the census.

| Area | Files |
| --- | --- |
| security, charging | `custody/discovery_walk.rs`, `custody/project_admission.rs` (`vcs_evidence`, `gitdir_target`, its `STATUS`), `custody/project_chain.rs` (`judge_project_object_ordered`), `trust/initial_platform.rs` (the capture's filesystem branch) |
| security, non-charging (pinned to prove they take no `WorkScope`) | `custody/discovery_scan.rs`, `custody/discovery_rule.rs` |
| platform | `filesystem/directory_open.rs`, `filesystem/path_binding.rs` (`status_read_cost`), `filesystem.rs` (`open_regular_cost`), `filesystem/descriptor_acl_capture.rs`, `filesystem/descriptor_filesystem.rs`, `filesystem/directory_entries.rs` (no charge; `EntryLimit`, `NameByteLimit`), `work_reader.rs` (`read_charged`), `work_ledger.rs` (the profile limits; `charge` adds and never refunds) |

**(r2) The inventory, at product `02fd45c`.** `discovery_walk.rs` line numbers. Objects and edges only.

| Charge | Formula (objects, edges) | When |
| --- | --- | --- |
| `owned(b)` | (1, 0) | every owned record, at the sites below |
| `LISTING` | (2, 3) | each listed directory, before its listing (616) |
| each raw name | (1, 1) | each name the listing returns, `.` and `..` included (619) |
| per listed name | (3, 0) + `owned` (spelling, 682→343) + `obs` + `owned` (scope entry, 372, when new) + `owned` (687) | each listed name other than `.` and `..` (649, 682-687) |
| `obs(n)` = `child_absence_observation_cost` | (1, 1) | each by-name observation (`directory_open.rs:45`) |
| `classify_cost(rel)` | (2 + t, 0), where t is the number of `target` segments | each visited child directory (782), named-root segment (878) and judged named root (915) |
| `openDir(n)` = `open_child_directory_cost` | (2, 1 + `status_read_cost`.edges) = (2, 2) | each opened directory (401) (`directory_open.rs:32`, `path_binding.rs:121`) |
| `STATUS` | (0, 1) | the root (1007), each opened directory (417), `gitdir_target` twice |
| probe | 1 to 4 × `obs`, stopping at the first present VCS marker | each opened directory (802; `project_admission.rs:518-540`) |
| `opensip.json` | `owned` + `obs` + `owned` when present | each opened directory (804-805) |
| non-boundary | `owned` | 813 |
| enter | `owned` | 676 |
| Cargo root | `owned` | 702 |
| depth 257 | 4 × (`owned` + `obs` + `owned` when present) | 793-799 |
| judged directory | `owned` (514), plus `CAPTURE` when `NeedsAcl` | first judgment of each chain directory (499-517, memoized) |
| marker capture | 4 × `owned` (532), plus per `NeedsAcl` marker `openReg` (3, 3) + `STATUS` + `CAPTURE` | each unit whose chain passes (525-565) |
| `CAPTURE` | `CAP` (1, 131), then `owned(count·K)` (1, 0), or `FS` (1, 2), or nothing | 432-479 (`descriptor_acl_capture.rs:116`, `descriptor_filesystem.rs:57`) |
| `GITDIR` | `openReg` (3, 3) + `STATUS` + `CAPTURE` + read envelope + `STATUS` + (1, 0) for a parsed target | a regular `.git` file (`project_admission.rs:555-618`) |
| fixed | 4 × `owned` (988, 993, 1011, 1022) + `STATUS` | once per walk |
| named roots | per spec and chain segment, as at 837-960 | explicit and config modes only (vectors only, not T2) |

The implementation turns this table into the tool's anchor list. A site in the closure that the table does not name is a fault: the planted-charge control (r2 changes) shows that it refuses.

**The read envelope (r2, RF-2).** A read of a file of length L, with ceiling c = max + 1, costs 1 object and at most min(L, c) + 1 edges when it is not interrupted. Interrupted retries are excluded, as stated in the r2 changes. No T2 walk reads (integrity refuses a `.git` component).
- **Unknowns are charged at their maximum (an upper bound).**
  - Every judged directory and every present regular workspace marker is assumed to reach the ACL and be captured (`CAP`: 1 object, 131 edges).
  - Every capture is assumed to take the filesystem observation as well (`FS`: 1 object, 2 edges), the dearer of its two branches.
  - Every listing is assumed to return `.` and `..`.
  - A regular `.git` file's read is charged at its uninterrupted envelope (vectors only).
- **No term depends on the root's absolute path.** Objects and edges depend only on counts. Path lengths enter only bytes, which are not censused.

### 1.4 The soundness control (native)

A census whose model under-counts would claim a false margin. So:
- **New security test module** `custody/discovery_census_tests.rs`, `cfg(all(test, target_os = "macos"))`, declared in `custody.rs`. It does not touch the accepted `discovery_walk_tests.rs`. It materializes each of the 52 accepted walk vectors (the same JSON, its own minimal materializer) under a scratch root, walks it with `discover_downward` on a fresh `WorkLedger::discovery_profile()`, and reads `used()`.
- **The census tool emits the model's prediction for every vector** into `custody/discovery_census_vectors.json`, from the same counting and model code it uses for the stores.
- **The test asserts** `used.objects <= model.objects` and `used.edges <= model.edges` for each vector. It also records the ratio, so that an extreme over-count is visible to review.
- **(r2) Composed-workspace vectors.** These are synthetic workspaces whose members are nested trees. Among them: a member that is a boundary (its own `opensip.json`), a member below a pruned segment, members that are units, and a member at depth near the limit. The model's composed-tree prediction must bound the native walk.
- **Mutations** (the lane's). Each must make the native test fail:
  - a model that drops the per-name observation charge;
  - one that drops the capture edges;
  - one that forgets the dot entries;
  - (r2) one that charges workspaces by the r1 member-sum formula.
- **(r2) Census-tool controls** (Python):
  - the delegated-cost drift (`status_read_cost` edges changed);
  - the planted charge outside every anchor;
  - a `.git` component in a T2 entry;
  - the read-envelope unit test;
  - the held-out guard.

  Each must refuse or fail as stated.

### 1.5 Workspaces (r2)

The five overlay workspaces (`workspaces/<id>/`) mount their members as symlinks, which the walker never follows.
- **Not censused:** the overlay's own symlink traversal. It would see only the symlinks.
- **What the census represents:** the **composed checkout**. The overlay root's own non-symlink entries (for example `.cargo/config.toml`, `workspace-overlay.json`) are kept. Each member's integrity-verified tree is placed as an ordinary directory at its mount name.
- **How it is censused.** The composed tree is built as SLM `fs` input and goes through the same population (the bound reference, the store root as the explicit project in automatic mode) and the same model as a repository. So every nesting transition is counted by the model itself: each member's classification, spelling, open, status, probe, `opensip.json` observation, boundary, depth, pruning and unit-chain capture.
- **Checks.** The overlay is checked against its archived `workspace-overlay.json` and its member pins. A member that fails integrity refuses the workspace.

### 1.6 The record and the margin

- **`crates/security/src/custody/discovery_census.json`.** It contains:
  - the manifest pin;
  - the pinned source bytes and the anchors matched;
  - per entry: id, `gitTree`, `treeDigest`, verified, the counts and the modeled objects and edges;
  - the profile limits, read from `work_ledger.rs`'s anchors;
  - the margin (`limit / cost`, per dimension);
  - `passes2x`;
  - the ten `outstanding: held-out` rows.
- **The tool has `--check`** (byte comparison) and `--write`. Like the other vector tools, it is a developer tool. The census JSON is generated evidence, and the product test reads it.
- **The margin test** (`custody/discovery_census_tests.rs`) checks:
  - every censused entry has `2 × objects <= DISCOVERY_OBJECT_LIMIT` and `2 × edges <= DISCOVERY_EDGE_LIMIT`, against the limits in the code, not the JSON's copy;
  - the record's census source pins match the current files;
  - the ten held-out rows are outstanding.
- **If every lead-readable entry passes,** the margin test lands green in B2-b4a. The held-out margin is then raised to the owner (LD-B2B-4).
- **If any entry fails (the expected case),** B2-b4a lands the tool, the vectors, the soundness control and the census record with the failures stated. The margin test lands too, but over the failing rows it asserts the honest state: those rows are recorded as `failsMargin`, the record says `caps: returned-to-law`, and **no test claims the margin**. Nothing is raised, trimmed or skipped. B2-b is not complete.

## 2. B2-b4b: the law revision and the caps (only if the margin fails)

- **The caps return to the law (item 12).** The lead prepares an M3-B amendment of item 12 only, for Codex review. It sets the discovery caps from the census by the law's own rule: the smallest caps that give at least a 2× objects-and-edges margin over every censused entry. It records each failing entry's modeled cost as the basis.
- **The headroom question stays open.** The held-out entries are unread, so the revision cannot prove the margin for them. The amendment states this, and the held-out margin stays outstanding (LD-B2B-4).
- **The amendment also weighs the alternative** of a cheaper walker: the scope retains every listed name, about eight ledger objects each. Each is a real allocation that B2-b3b was required to charge (B2B3B-R1-RF-3), so the census does not discount it. Whether discovery should retain every listed name is a design question for the amendment, not a census choice.
- **After the amendment is accepted,** B2-b4b changes the platform's `DISCOVERY_*_LIMIT` constants to the accepted caps. It updates B2-b1's cap tests (`work_ledger_tests.rs`) through that unit's own review. Then it turns the margin test to the full claim.
- **Owner.** The held-out margin is raised to the owner when B2-b4 reaches it. The cap revision itself is a law amendment under the lead and Codex review, unless it changes a recorded owner decision; the lead will say so if it does.

## 3. Lead decisions

- **LD-B2B4-1. The census reuses B2-b0's adapter and reference** for the population. It adds no new pruning or population rule.
- **LD-B2B4-2. Objects and edges are an upper bound.** The unknowns are taken at their dearer branch. This is shown sound against the native walker on the 52 walk vectors (section 1.4).
  - **Rejected:** a native measurement of the stores themselves. The test would need the store paths at run time, a new environment or argument read (M3-B r5 item 9), and machine-specific inputs in a product test.
- **LD-B2B4-3. Constants are pinned by anchored source matches,** never restated by hand (the K5 lesson: no invented budget constants).
- **LD-B2B4-4 (r2). Workspaces are censused as composed checkouts** through the same model (section 1.5). **Rejected:** the r1 member sum, which misses the nesting charges (B2B4PLAN-R1-RF-1).
- **LD-B2B4-7 (r2). The margin is structural.** Interrupted read retries are excluded and stated. No T2 walk reads. Exhaustion refuses and never truncates (B2B4PLAN-R1-RF-2).
- **LD-B2B4-5. A failing census is still landed.** It is the evidence the law revision needs. The margin is never claimed for a failing row.
- **LD-B2B4-6. The plan's estimate is not evidence.** Only the integrity-verified census counts.

## 4. Checks (B2-b4a lane)

- The census tool's `--check`, run twice: once over the stores, once over the vectors.
- The security suite at base and candidate, with equal failure sets and at least the new census tests passing.
- Warning-denied all-targets Clippy.
- rustfmt on new files.
- The FW-01 pin, the environment pin, the three existing vector checks, the operability census and verify_design.
- The four model mutations, each caught, and the five census-tool controls (section 1.4).
- A held-out guard control: a planted manifest whose held-out entry names a fake digest. The tool must never stat it.

## 5. Not claimed

- No held-out margin.
- No cap change in B2-b4a.
- No production caller.
- No byte census.
- No qualification.

B2-b is complete only when the all-entry margin holds.
