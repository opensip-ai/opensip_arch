# C1a1 r1: the snapshot root, its pre-walk opener, the extent walk and its charge model (M3-C r8 items 1 and 2)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements C1a1 of the C1a plan as amended: r4 is accepted (Codex `codex-c1a-plan-r4`), r5 and r6 amend it, and r6 is in review. Under r6, C1a1 is **preparatory library and model work**. It adds no `snapshot_profile`, makes no production snapshot-ledger claim, has no production caller, and changes no census-closure file. C1a4's caps wait for an M3-C r9 law record.

**Base:** product main `808ad64` (inventory v212, 173 contract successors).

## What it changes

| File | Change |
| --- | --- |
| `crates/security/src/snapshot_source.rs` (new) | **`SnapshotRoot`**, with one constructor per lawful lending: `from_operation(&ProjectOperation)` (durable; the writer handoff's `DiscoveryRoot`) and `from_released_read(&ReleasedRead, &ProjectRootAdmission)` (ephemeral with I complete; crate-internal until J2c). The I-absent root is join E-1, later.<br>**`SnapshotCustody`:** the invoking uid, the authorized groups and the owner waiver. The waiver applies to directories, never to markers.<br>**`SourceFile`:** a logical path, an open descriptor, its pre-open observation and a marker flag. It is never read here.<br>**`SnapshotRoot::open`**, the pre-walk capture opener (plan r2 RF-1): a root-relative component walk with `fstatat(AT_SYMLINK_NOFOLLOW)` and `O_NOFOLLOW` opens, each directory compared with its observation and judged under S3 directory custody, the final regular file opened and compared, and config-file custody for a marker.<br>**Shared helpers:** `judge_opened`, the metadata-only judgment, then one premise-applied ACL capture of the same object and the full judgment, through the existing `judge_entry`; and `open_directory` and `open_regular`, which open relative to the given parent and compare.<br>**`SnapshotRefusal`:** `Name`, `ListingBound`, `Changed`, `Custody`, `MarkerCustody`, `NotARegularFile`, `Capture`, `Premise` and `HostIo`. None is retried.<br>A test-only `set_before_open` hook drives the swap controls. |
| `crates/security/src/snapshot_walk.rs` (new) | **`SnapshotExtent`**, built from B2's `AdmittedBoundaries`, the admitted D15 member roots and validated `ignorePaths`.<br>**`walk_snapshot`**, the extent walk:<br>• the root's sample and custody first;<br>• it descends holding each directory's retained descriptor;<br>• it lists each directory once with the discovery walk's own `ListingConversion` (names refuse exactly as there) and observes every child relative to its enumerating parent;<br>• it skips the shared rule's pruned trees (with `.opensip/` through `classify_path`), `ignorePaths`, admitted boundaries, and a marker-custody row's own marker;<br>• it opens each directory and regular file from that same parent and compares it (plan r3 RF-2), judging each directory entered and each marker;<br>• it counts symlinks and special files in the walk report and never opens them;<br>• it hands each regular file, open, to the visitor.<br>**Charges:** made before every step, at the discovery walk's prices (`LISTING`, `STATUS`, `owned`, its listing conversion) and with `classify_cost`'s form. The walk changes no file the census pins. |
| `crates/security/src/snapshot_walk_tests.rs` (new) | 12 tests (below). |
| `crates/security/src/lib.rs` | `pub mod snapshot_source` and `pub mod snapshot_walk` (macOS), beside `discovery_export`. This file is not in the census closure. |
| `tools/security/snapshot_ledger_model.py` (new) | **The charge model.** It imports `discovery_census.py` unchanged, so its `costs` verifies the census's whole cost closure and reads every shared constant by anchor; it also brings the size inventory, `Tree`, the vector tree reading and the B2-b0 reference rule. The snapshot modules' own charge shapes are pinned by anchor, and both files are pinned whole. `SnapshotModel` mirrors `walk_snapshot` charge for charge, with ACL captures at their dearer branch. It writes or checks `snapshot_ledger_vectors.json`. |
| `crates/security/src/snapshot_ledger_vectors.json` (new) | The model's predictions for 32 trees: the 28 accepted automatic discovery walk vectors, with their boundaries and invocation, and 4 generated worst-case shapes (wide long names, a wide pruned listing, a 64-deep chain, and markers with a pruned tree, a boundary and a link). |

## The tests

- **The extent:** every regular file outside the pruned trees, boundaries and `ignorePaths` is handed, and only those:
  - `target/` is pruned beside `Cargo.toml` and kept elsewhere (C1-T9);
  - `node_modules`, `.git` and `.opensip/` are pruned (SX-1);
  - a nested repository is never read (C1-T10);
  - the symlink and the FIFO are reported, never opened (C1-T5, C1-T6);
  - the bytes handed are the file's (C1-T1's first half).
- **An `ignorePaths` entry that is not a logical path is refused.**
- **Custody:**
  - a 0777 directory refuses `Custody`;
  - a hard-linked marker refuses `MarkerCustody` (C1-T8), unless B2's marker-custody row excludes exactly that marker;
  - a marker over 4 MiB refuses.
- **Names (C1-T7):** a backslash name and a staging-prefix name refuse the whole walk, with the parent spelled.
  - The non-UTF-8 and 256-scalar cases cannot be created on APFS (EILSEQ, ENAMETOOLONG).
  - They go through the same unchanged `ListingConversion`, whose own controls are `discovery_walk_tests.rs::listed_names_are_validated_as_logical_paths`.
- **Changes (C1-T4, C1A-T5):**
  - a file swapped between its observation and its open refuses `Changed`;
  - a directory replaced between its listing and its open refuses `Changed`;
  - an ancestor replaced by path after it is entered never redirects the walk: the original bytes are read through the retained descriptors.
- **The pre-walk opener:**
  - its observation equals the walk's;
  - after an ancestor is replaced, the walk's observation is another object, so the host's comparison refuses (C1-T24 and C1A-T5);
  - it refuses a symlinked component and a custody failure.
- **The oracle cross-check:** all **28** accepted automatic discovery walk vectors, from B2-b0 (contract successor 164), hand exactly the reference's regular files outside every exclusion.
- **The soundness control:** on all **32** trees, the native walk's ledger charge never exceeds the model's prediction. On every tree it is exactly equal, so any undercount in the model fails.

## Not delivered (plan r6)

- **The capture session, candidate custody and the read:** C1a2. It also extends the model with the read, retention and custody charges.
- **Sealing:** C1a3.
- **The caps, their T2 margins and `snapshot_profile`:** C1a4, gated on M3-C r9.
- **The ledger.** No snapshot ledger yet: the walk takes the caller's `WorkScope`, and the tests use the discovery profile.
- **The route controls C1A-T2 and C1A-T3** (durable and released-read routes walking one tree to one inventory; the ephemeral route holding no lease and no fence). They need a real `ProjectOperation` and `ReleasedRead`, which security's scenario fixtures build. They land with C1a2, whose host tests enable `opensip-security`'s `scenario-fixtures` in their dev-dependencies, as storage's already do.
- **C1APLAN-R4-NBO-1** (the 1024-byte injected name control) lands with the model's envelope controls in C1a4. No native stream yields such a name.

## Checks

Lane r1, `evidence/c1a1-checks-r1/`:
- **the security suite** at base and candidate, with equal failure sets (isolated reruns for any differing test) and 12 new passing tests;
- **rustfmt** on the new files (security `lib.rs` is not clean at base and is not reformatted) and warning-denied all-targets Clippy on `opensip-security`;
- **the snapshot walk tests,** and the model's `--check`;
- **the T2 census `--check`** over the lead-readable cache, so the census records are unchanged;
- **repository checks:** the operability source census, the census-closure check (no closure file changed, so the blind receipt stays current) and verify_design;
- **mutations:**
  - **eight walk mutations,** each failing the walk tests: a pruned tree entered, `ignorePaths` skipped, a boundary entered, directory custody ignored, a regular open not compared, a directory open not compared, a marker-custody row ignored, and a symlink not reported;
  - **three model undercounts,** each regenerated and each failing the soundness control: the classification dropped, name copies made free, and the directory capture dropped.

## Not claimed

- No caller, no ledger profile and no cap.
- No read, custody or seal.
- No Linux claim and no qualification.
- C1a's completion is not claimed.

## Inventory

New paths for the inventory after acceptance:
- `crates/security/src/snapshot_source.rs`;
- `crates/security/src/snapshot_walk.rs`;
- `crates/security/src/snapshot_walk_tests.rs`;
- `crates/security/src/snapshot_ledger_vectors.json`;
- `tools/security/snapshot_ledger_model.py`.
