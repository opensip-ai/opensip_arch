# C1a1 r3: the snapshot root, its pre-walk opener, the extent walk and its charge model (M3-C r8 items 1 and 2)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 3.**

## r3 changes (Codex `codex-c1a1-r2`, REQUIRED-FINDINGS)

| Finding | Resolution | Controls and mutants |
| --- | --- | --- |
| **C1A1-R2-RF-1:** the pre-walk path validator allocated before any charge | `SnapshotRoot::open` now charges `owned(path.len())` first, then runs the shared grammar (`LogicalPath::parse`). It keeps the validated `LogicalPath`'s own string as the `SourceFile` path (`into_string`), so there is no second copy, and the old trailing charge and `to_owned` are gone. The grammar is called, never copied.<br>**The same rule elsewhere:** `SnapshotExtent::new` now takes the `WorkScope` and charges each `ignorePaths` entry's validator copy before parsing it.<br>**The model now covers the opener:** the validator's copy, the root's sample and custody, then per directory component its key, observation, open, sample and custody, then the leaf's observation, open and sample, and a marker's custody. | `the_pre_walk_opener_charges_exactly_the_models_prediction`: a root-level file, a nested file and a nested marker, each equal to the model exactly (the model's `openers`). `an_ignore_path_that_is_not_a_logical_path_is_refused` now also asserts the extent's exact validation charge. Mutants `opener-validator-uncharged`, `extent-validation-uncharged` and model mutant `model-opener-validator-free`. |
| **NBO-1:** the triples were not in the log | The runner's focused step runs with `--nocapture`, so `snapshot-walk-tests.log` holds the 35 `soundness` lines, the summary and the three `opener` lines. | — |

**Base (r3):** the candidate worktree now sits on product main `e4e715845d2d0579060709898892d3d5fd93e49e` (D1a's integrated commit, a fast-forward from `808ad64`; it touches only platform files). The lane's base is that commit. The r2 package (`../c1a1-r2/`) is history.

**The allocation audit, r3 rows** (added to the table below):

| Allocation | Charged by |
| --- | --- |
| The opener's validated path (kept as the `SourceFile` path) | `owned(path.len())`, before `LogicalPath::parse` |
| Each `ignorePaths` entry's validator copy | `owned(path.len())` in `SnapshotExtent::new`, before `LogicalPath::parse` |

## r2 changes (Codex `codex-c1a1-r1`, REQUIRED-FINDINGS)

| Finding | Resolution | Controls and mutants |
| --- | --- | --- |
| **C1A1-R1-RF-1:** the walk stat'ed the `.opensip` anchor before pruning it | `enter` lists the directory with the unchanged `ListingConversion`, so every name is still validated. It then asks the shared rule (`classify_path`, charged as a classification) about each `.opensip` name only. An exact `opensip-custody-state` anchor, at the root or an admitted D15 member, is removed from the listing before any child is observed. It is never stat'ed, opened or listed. An ordinary nested `.opensip` is not an anchor and is walked. The observation slots are charged for the remaining children only. | `the_exact_opensip_anchors_are_never_observed_even_when_they_vanish_or_change`: a test-only hook runs before each child observation, logging every observed path. After the root's listing, the hook removes the root's anchor and turns the member's into a file. The walk succeeds, and the log holds `a/.opensip` but neither anchor. Model case `opensip-anchors-root-and-member`. Mutant `opensip-anchor-observed`; model mutant `model-anchor-classification-free`. |
| **RF-2:** a boundary was enforced only when its entry was a directory | `is_boundary` now runs for every entry kind, after the pruned-tree and `ignorePaths` checks and before the kind is dispatched. A boundary that is now a file, a symlink or a FIFO is neither handed nor reported. The marker-custody row is still marker-specific, in the file branch. The model mirrors this, and its boundary lookup now reproduces the shared rule exactly: `at_or_below`, repositories before projects, then the first covering custody row. Before, the model treated a root anchor `''` as covering everything. | `a_boundary_that_is_now_a_file_a_link_or_a_fifo_is_never_handed_or_reported`: nested repositories that are a file, a link and a FIFO; a `DIRECTORY_CUSTODY` row that is a file; a `DEPTH` row that is a file. Model case `boundaries-replaced-by-non-directories`. Mutant `boundary-for-directories-only`. |
| **RF-3:** the pre-walk opener did not judge the retained root | `judge_root`, shared by the walk and the opener, takes one status sample of the lent descriptor, then runs `judge_opened`: S3 directory custody, with the waiver for directories only. `SnapshotRoot::open` calls it before any component is observed, and a failure refuses terminally with `Custody` at `""`. | `the_pre_walk_opener_judges_the_retained_root_before_any_capture`: a root-level capture (`a.txt`) and a nested one (`src/main.rs`) are opened from a root lent at 0755. They refuse after the root becomes 0777, open again when it is restored, and refuse again after a `group:everyone allow add_file` ACL entry. Mutant `opener-root-not-judged`. |
| **RF-4:** native path and boundary copies were outside the charges | **Copies removed.** A child's path and observation move out of their frame (`mem::take`, `mem::replace`). Its parent and name are borrowed views of it (`rsplit_once`, `last_segment`). The opener's components are borrowed from `path`, so there is no `Vec`. `SnapshotExtent` borrows `ignorePaths`. The root's spelling is built only inside the terminal name refusal, as in the discovery walk.<br>**Boundary lookups copy nothing.** `AdmittedBoundaries` (`discovery_export.rs`, outside the census closure) builds the rule-form custody rows once, at construction. The new `boundary_anchor` borrows its anchor, and `is_boundary`, `boundary_hit` and `excluded_prefixes` all use it.<br>**Root frame.** The root frame's slot is now charged, as every other frame's is.<br>**`classify_cost` is counted from the shared rule's source,** instead of reusing the discovery walk's form: the segment list; one prefix per `target` segment; up to three anchors (dependency or VCS, Cargo build output, and custody state), each at most `rel`; and each non-empty D15 member root's segment list. The model mirrors each term. | Model cases `long-deep-and-many-custody-rows` (three 200-byte names deep, about 640 bytes of path, plus 24 custody rows, 12 marker and 12 directory, consulted for every entry) and `opensip-anchors-root-and-member` (one member root). Model mutants `model-root-frame-free` and `model-member-lists-free`.<br>**The allocation audit** below is the independent justification. Each heap allocation the walk and the opener make is listed with its charge. |
| **NBO-1:** route controls | Kept for C1a2, with the obligation unchanged: the same-tree durable and released-read inventory comparison, and the no-lease, no-fence released-read control with its scenario helper, before production use. | — |
| **NBO-2:** upper bound against exact | The model now marks a case `exact` only when every capture in it takes the branch the model charges. That means no captured object carries an ACL entry, so on the APFS scratch each capture takes the premise branch, and the premise branch must be the dearer one; the model checks both. The native test still asserts the upper bound on every case, asserts equality on each `exact` case, and prints every case's native and predicted triples. All 35 cases are `exact`, because no vector captures an object with an ACL entry list. That is the only branch at which native can fall below the model. The model mutants are evidence for the term each one removes, not a proof that every undercount fails. | The lane log `snapshot-walk-tests.log` (35 `soundness` lines). |
| **NBO-3:** stale metadata | This record cites plan r6 as accepted (`codex-c1a-plan-r6`, published `cde73773`). `source.json` records `publicApiAdded: true`. The runner's stale serial-suite comment is gone (the security suite runs in parallel, as before). | — |

**One lead change beside the findings (for C1a2):** the walk's visitor now also receives the walk's own `WorkScope` (`FnMut(SourceFile, &mut WorkScope) -> Result<(), E>`), so the host's read in C1a2 is charged to the same snapshot ledger before each step. Nothing in the walk's own charges changes, and the tests' visitors charge nothing.

## The allocation audit (RF-4)

Every heap allocation in `walk_snapshot`, `enter`, `custody_state_anchor`, `judge_root`, `judge_opened`, `open_directory`, `open_regular` and `SnapshotRoot::open`, and in the shared calls they make, with what charges it. Terminal refusal details (`format!`, `to_owned` inside a returned refusal) are built only when the walk stops, as in the discovery walk.

| Allocation | Charged by |
| --- | --- |
| The listing's paths and the validator's copy, the `Vec` slots, and an invalid name's bytes | `ListingConversion::accept` (the discovery walk's, unchanged) |
| The observation `Vec` | `owned(paths.len() × size_of::<ChildObservation>())`, before it is built, for the children left after the anchor is dropped |
| Each child's observation | `observe_child_accounted` (platform) |
| A frame (`levels` slot), root included | `owned(0)` before each push |
| A Cargo root key (`known.insert(rel.clone())`) | `key_cost(rel, "")` |
| `classify_path`'s segment list, target prefixes, anchors and member lists | `classify_cost(rel, members)`, before each call, the anchor check included |
| A reported link's or special file's path slot | `owned(rel.len())` |
| A directory open, a regular open and their status samples | `open_child_directory_cost`, `open_regular_cost` and `STATUS`, through `work.run` |
| An ACL capture and its premise sample | `capture_descriptor_acl_accounted` and `premise.admits` (their owners) |
| An ACL entry list | `owned(count × size_of::<CapturedAclEntry>())` |
| The opener's `rel` per component | `key_cost(rel, part)` (its final path: the r3 row above) |
| `boundary_anchor`, `is_boundary`, `ignored`, `last_segment`, `rsplit_once`, `judge_entry` | Nothing to charge: they borrow, or copy plain-old-data `DescriptorMetadata` |

## Lead observation for the discovery walk (routed, not changed here)

Counting `classify_path` from its source shows that the discovery walk's own `classify_cost` (`custody/discovery_walk.rs:99-110`, a census-closure file) prices one anchor and no member lists. The rule can build up to three anchors, and one segment list per non-empty D15 member root (`custody_state`), and the discovery walk passes its admitted members. A workspace with many members may therefore be undercharged in discovery.

This unit does not touch that file: a change there reopens the census and the blind receipt. The snapshot walk does not reuse that form. It is routed to the status board as an open discovery accounting item, for a closure-changing unit with its own census refresh.

## Base and earlier round

The r1 package (`../c1a1-r1/`) is history.

It implements C1a1 of the C1a plan as amended: r4 is accepted (Codex `codex-c1a-plan-r4`), r5 and r6 amend it, and r6 is accepted (Codex `codex-c1a-plan-r6`, published `cde73773`). Under r6, C1a1 is **preparatory library and model work**. It adds no `snapshot_profile`, makes no production snapshot-ledger claim, has no production caller, and changes no census-closure file. C1a4's caps wait for an M3-C r9 law record.

**Base:** product main `e4e7158` (D1a; inventory v212, 173 contract successors). Rounds 1 and 2 were on `808ad64`.

## What it changes

| File | Change |
| --- | --- |
| `crates/security/src/snapshot_source.rs` (new) | **`SnapshotRoot`**, with one constructor per lawful lending: `from_operation(&ProjectOperation)` (durable; the writer handoff's `DiscoveryRoot`) and `from_released_read(&ReleasedRead, &ProjectRootAdmission)` (ephemeral with I complete; crate-internal until J2c). The I-absent root is join E-1, later.<br>**`SnapshotCustody`:** the invoking uid, the authorized groups and the owner waiver. The waiver applies to directories, never to markers.<br>**`SourceFile`:** a logical path, an open descriptor, its pre-open observation and a marker flag. It is never read here.<br>**`SnapshotRoot::open`**, the pre-walk capture opener (plan r2 RF-1): **(r2)** the retained root judged first by the shared `judge_root`, then a root-relative component walk with `fstatat(AT_SYMLINK_NOFOLLOW)` and `O_NOFOLLOW` opens, each directory compared with its observation and judged under S3 directory custody, the final regular file opened and compared, and config-file custody for a marker.<br>**Shared helpers:** `judge_opened`, the metadata-only judgment, then one premise-applied ACL capture of the same object and the full judgment, through the existing `judge_entry`; and `open_directory` and `open_regular`, which open relative to the given parent and compare.<br>**`SnapshotRefusal`:** `Name`, `ListingBound`, `Changed`, `Custody`, `MarkerCustody`, `NotARegularFile`, `Capture`, `Premise` and `HostIo`. None is retried.<br>A test-only `set_before_open` hook drives the swap controls. |
| `crates/security/src/snapshot_walk.rs` (new) | **`SnapshotExtent`**, built from B2's `AdmittedBoundaries`, the admitted D15 member roots and validated `ignorePaths`.<br>**`walk_snapshot`**, the extent walk:<br>• the root's sample and custody first;<br>• it descends holding each directory's retained descriptor;<br>• it lists each directory once with the discovery walk's own `ListingConversion` (names refuse exactly as there) and observes every child relative to its enumerating parent;<br>• **(r2)** it drops each exact `.opensip/` anchor from its listing before observing any child;<br>• it skips the shared rule's pruned trees (through `classify_path`), `ignorePaths`, admitted boundaries of any entry kind, and a marker-custody row's own marker;<br>• it opens each directory and regular file from that same parent and compares it (plan r3 RF-2), judging each directory entered and each marker;<br>• it counts symlinks and special files in the walk report and never opens them;<br>• it hands each regular file, open, to the visitor.<br>**Charges:** made before every step, at the discovery walk's prices (`LISTING`, `STATUS`, `owned`, its listing conversion) and with `classify_cost`'s form. The walk changes no file the census pins. |
| `crates/security/src/snapshot_walk_tests.rs` (new) | 16 tests (below; r2 adds three, r3 one). |
| `crates/security/src/discovery_export.rs` | **(r2, RF-4)** `AdmittedBoundaries` keeps its custody rows in the rule's form, built once, and adds `boundary_anchor`, a borrowing lookup that `boundary_hit`, `is_boundary` and `excluded_prefixes` use. Behaviour is unchanged, and the file is not in the census closure. |
| `crates/security/src/lib.rs` | `pub mod snapshot_source` and `pub mod snapshot_walk` (macOS), beside `discovery_export`. This file is not in the census closure. |
| `tools/security/snapshot_ledger_model.py` (new) | **The charge model.** It imports `discovery_census.py` unchanged, so its `costs` verifies the census's whole cost closure and reads every shared constant by anchor; it also brings the size inventory, `Tree`, the vector tree reading and the B2-b0 reference rule. The snapshot modules' own charge shapes are pinned by anchor, and both files are pinned whole. `SnapshotModel` mirrors `walk_snapshot` charge for charge, with ACL captures at their dearer branch. It writes or checks `snapshot_ledger_vectors.json`. |
| `crates/security/src/snapshot_ledger_vectors.json` (new) | The model's predictions for 35 trees, each with its `exact` flag: the 28 accepted automatic discovery walk vectors, with their boundaries and invocation, and 7 generated shapes. Four are from r1: wide long names, a wide pruned listing, a 64-deep chain, and markers with a pruned tree, a boundary and a link. Three are new in r2: the anchors at the root and at a member, boundaries that are not directories, and long names three deep under 24 custody rows. |

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
- **(r2) The anchors, boundaries of any kind and the opener's root judgment:** the three controls in the r2 table.
- **(r3) The opener's accounting:** a root-level file, a nested file and a nested marker are each charged exactly the model's prediction.
- **The soundness control:** on all **35** trees, the native walk's ledger charge never exceeds the model's prediction. It must equal the prediction on each tree the model marks `exact`, which is all 35 here. Each case's triples are printed.

## Not delivered (plan r6)

- **The capture session, candidate custody and the read:** C1a2. It also extends the model with the read, retention and custody charges.
- **Sealing:** C1a3.
- **The caps, their T2 margins and `snapshot_profile`:** C1a4, gated on M3-C r9.
- **The ledger.** No snapshot ledger yet: the walk takes the caller's `WorkScope`, and the tests use the discovery profile.
- **The route controls C1A-T2 and C1A-T3** (durable and released-read routes walking one tree to one inventory; the ephemeral route holding no lease and no fence). They need a real `ProjectOperation` and `ReleasedRead`, which security's scenario fixtures build. They land with C1a2, whose host tests enable `opensip-security`'s `scenario-fixtures` in their dev-dependencies, as storage's already do.
- **C1APLAN-R4-NBO-1** (the 1024-byte injected name control) lands with the model's envelope controls in C1a4. No native stream yields such a name.

## Checks

Lane r3, `evidence/c1a1-checks-r3/` (the lane of record), on base `e4e7158`. Round 2's lanes are in `../c1a1-r2/evidence/`:
- **Round 2, attempt 1** failed one check. The soundness control could not create the generated long-path tree, then four 200-byte names deep: under the lane's longer private TMPDIR its absolute path passed macOS's 1,024-byte path limit (ENAMETOOLONG; symlink aliases do not help, because the limit applies after expansion). The case is now three deep, about 640 bytes of path, and round 2's attempt 2 reran every check.
- **Supplementary** (round 2, `../c1a1-r2/evidence/supplementary/`): `discovery_export.rs` is an FW-01-covered file, so FW-01 and the environment-exceptions tests were run on the candidate. Both pass, and `discovery_export.rs` is unchanged in r3.

The checks:
- **the security suite** at base and candidate, with equal failure sets (isolated reruns for any differing test) and 16 new passing tests;
- **rustfmt** on the new files and `discovery_export.rs` (clean at base and candidate; security `lib.rs` is not clean at base and is not reformatted), and warning-denied all-targets Clippy on `opensip-security`;
- **the snapshot walk tests,** and the model's `--check`;
- **the T2 census `--check`** over the lead-readable cache, so the census records are unchanged;
- **repository checks:** the operability source census, the census-closure check (no closure file changed, so the blind receipt stays current) and verify_design;
- **mutations:**
  - **thirteen walk mutations,** each failing the walk tests: a pruned tree entered, `ignorePaths` skipped, a boundary entered, directory custody ignored, a regular open not compared, a directory open not compared, a marker-custody row ignored, a symlink not reported, (r2) an exact anchor observed, a boundary enforced for directories only, the opener's root not judged, and (r3) the opener's validator uncharged and the extent's validation uncharged;
  - **seven model undercounts,** each regenerated and each failing the soundness or opener control: the classification dropped, name copies made free, the directory capture dropped, (r2) the anchor classification made free, the root frame made free, member lists made free, and (r3) the opener's validator made free.

## Not claimed

- No caller, no ledger profile and no cap.
- No read, custody or seal.
- No Linux claim and no qualification.
- C1a's completion is not claimed.

## Inventory

The changed existing path `crates/security/src/discovery_export.rs` and `crates/security/src/lib.rs` keep their rows. New paths for the inventory after acceptance:
- `crates/security/src/snapshot_source.rs`;
- `crates/security/src/snapshot_walk.rs`;
- `crates/security/src/snapshot_walk_tests.rs`;
- `crates/security/src/snapshot_ledger_vectors.json`;
- `tools/security/snapshot_ledger_model.py`.
