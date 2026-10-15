# B2-b3a r2: what the candidate delivers (M3-B unit B2-b3, sub-unit B2-b3a: selection provenance and lending)

**Lead scope record, 2026-10-15. Unreviewed candidate.** It implements the B2-b3a row of the accepted B2-b3 plan r2 (`config-discovery-b/b2-b3/PLAN-r2.md`; Codex `codex-b2b3-plan-r2`): LD-B2B3-1, LD-B2B3-7 and LD-B2B3-9. Its base is product `3b3ab6e`: B2-b2 is bound, inventory is v192, and contract successors are 164.

## r2 changes (Codex `codex-b2b3a-r1`, REQUIRED-FINDINGS)

**B2B3A-R1-RF-1: the `.git` file is read only under S3 file custody.**
- **The defect.** r1's `gitdir_target` checked identity, one link and size, but not owner, other and group write or the ACL. Its LD-B2B3A-3 dropped those checks because the target is data. That deviated from plan r2 LD-B2B3-7, which reads the value "under S3 file custody", without acceptance.
- **The fix.** LD-B2B3A-3 is withdrawn. `gitdir_target` now takes the invoking uid and the chain policy (the receipt's premise and the authorized groups). On the opened, identity-matched descriptor it runs the configuration-file judgment, `judge_project_object_ordered(ConfigurationFile, waiver None, CustodyOrder::Reference)`. A custody refusal (`Root`, or an omitted ACL no premise admits) keeps the boundary with a null target. Its sample must equal the opened one, and the status after the read must equal the judged one. Any change, host I/O and exhaustion still refuse the whole operation. The owner waiver never reaches the `.git` file.
- **The adapter.** The vector tool no longer decides custody. It asks the bound model's own `_file_custody` over the `.git` file's `fs` entry, with no waiver, and decides only the line grammar.
- **New vectors:**
  - ACL grants to another user and to another group; other-writable; group-writable; each has no target;
  - group-writable with the group authorized, and owner-only, each with its target;
  - a waived foreign explicit root whose `.git` file is never waived.

  `vcs-git-file-foreign-acl-still-read` is renamed and inverted: it is now `vcs-git-file-acl-grant-to-another-user-has-no-target`.
- **New native controls,** in the renamed `a_gitdir_file_is_judged_by_custody_and_a_change_or_exhaustion_is_never_a_null_target`: a foreign invoking uid, and an omitted ACL with no premise, each with no target, beside the admitted read.
- **New mutation.** `gitdir-custody-ignored` reads the file whatever custody says, and is caught.

**NBO-1: a bare `\r`.** `gitdir_value` strips only `\n` or `\r\n`, so `gitdir: /a\r` has no target, as the scope says. There is a new vector (`vcs-gitdir-file-bare-cr`) and a new mutation (`gitdir-bare-cr-stripped`). The tool's grammar is the same.

**NBO-2: the stage guard.** The mapping is now `UpwardRecord::discovery_refusal(&refusal, explicit) -> Option<(code, detail, path)>`. It maps only when selection named the refusal's object. Selection names the object of every refusal it makes, and clears the pre-open name once the open succeeds. A refusal from a later step, such as the chain walk, has no named object, so it maps to `None` even where its variant is one selection also uses. The variant mapping itself is now private (`selection_refusal`).
- **New test.** `a_refusal_after_selection_is_never_mapped_as_a_selection_refusal`: synthetic `PathInvalid(NotFound)` and `Symlink` refusals with no named object, and a real analysis admission whose selection accepts the home and whose chain walk refuses it (`OutsideHome`), each map to `None`. A named object maps.
- **New mutation.** `selection-guard-dropped`, caught.

There are now 59 vectors (24 refused, 17 of them reference cases; 35 accepted) and 17 mutations: three are new, and r1's `gitdir-hard-link-read` is retired because the link bound is custody's now, which `gitdir-custody-ignored` covers. The evidence is lane r4. Lane r3 stopped at a stale mutation anchor (`vcs_evidence` gained its custody arguments) before any product byte was mutated, and is kept in the work directory.

## Paths

| Path | Change |
|---|---|
| `crates/security/src/custody/project_admission.rs` | The upward record (`UpwardRecord`, `UpwardRow`, `Candidate`, `RowBoundary`), recorded by `select` on the analysis path. VCS evidence (`vcs_evidence`, `gitdir_target`). The waiver through selection. The discovery refusal mapping (`UpwardRecord::discovery_refusal`, r2). `ProjectRootAdmission::recheck_waived`. |
| `crates/security/src/custody/project_chain.rs` | `walk_project_chain_waived`, `ProjectChain::recheck_waived` and `applicable_waiver`. `CustodyOrder` with `judge_project_object_ordered` and `check_project_object_ordered` (the reference order, moved here from B2-b2's core). `DiscoveryRoot`. |
| `crates/security/src/custody/installation_read.rs` | `ReadSession::release` and `ReleasedRead::discovery_root`. The analysis phases take the waiver and the record. |
| `crates/security/src/custody/operation_handoff.rs` | `ProjectOperation::discovery_root`. |
| `crates/security/src/custody/first_registration.rs`, `ordinary_writer.rs` | The write gate's analysis phases take the waiver and the record. |
| `crates/security/src/custody/discovery_scan.rs` | `reference_order` calls the moved `check_project_object_ordered`; `DiscoveryRefusal::ConfigCustodyRefused` (`CONFIG.CUSTODY_REFUSED`, D9 `CONFIG.INVALID`). |
| `crates/security/src/scenario.rs` | The existing seam passes no waiver and a fresh record. |
| `crates/security/src/custody/project_admission_upward_tests.rs` | **New.** The controls below. |
| `crates/security/src/custody/discovery_upward_vectors.json` | **New, generated.** 59 current-reference vectors. |
| `tools/security/discovery_upward_vectors.py` | **New.** The vector tool. |
| `project_admission_carrier_tests.rs`, `discovery_scan_tests.rs`, `operation_handoff_tests.rs` | Call sites, and one write-path lending test. |

## What it does

**The upward record (LD-B2B3-7).** `select` takes an optional record. The legacy `select_project_root` passes none and is the same selection: the same opens, charges and refusals. The B1-b legacy admission probe, run at base and candidate, gives equal lines. On the analysis path (`admit_project_root_for_analysis`, on the read session and on the write gate) the record is always kept:
- **Rows** follow SLM's walk. Each examined directory gets one row with its spelling, `PASS` or the custody reason, the candidate (`ABSENT`, `PRESENT`, `REFUSED`, `NOT_EXAMINED`) and the boundary (`EXPLICIT`, `VCS`, `HOME`, `FS_ROOT`, `MOUNT` or the bare custody reason). A custody failure above the launch is a `NOT_EXAMINED` row. A config refusal leaves its row `REFUSED`. A mount is back-patched onto the child's row.
- **The refusal's object.** A selection refusal names its object (SLM's refusal `path`): the launch, the explicit path, the config file, or the directory where the depth bound fell. A failed open closes the work scope, so the path an open may refuse is named and charged before the open and cleared after it.
- **Charges.** Each row's spelling and the refusal path are charged as owned copies. Turning the record into strings (`rows`, `provenance`) is uncharged formatting, and returns `None` for a spelling that is not UTF-8, which the caller refuses.
- **`provenance(&Selected)`** gives the upward half of `DiscoveryProvenanceV3`: mode, `configPath`, rows, stop reason (`CUSTODY:<why>` from the last row), `vcs`, and `explicitPathWasSymlink`.
- **`UpwardRecord::discovery_refusal(&refusal, explicit)`** (r2) maps a selection refusal to the discovery result's code and detail: the launch's custody and an absent or non-directory launch (`PROJECT.ROOT_CUSTODY_REFUSED`); an absent or non-directory explicit path (`PROJECT.EXPLICIT_PATH_INVALID`); the depth bound (`WALK_DEPTH_EXCEEDED`); config custody (`CONFIG.CUSTODY_REFUSED`). Anything else (host I/O, budget, and any refusal whose object selection did not name, which covers every later admission step) maps to `None`.

**VCS evidence (LD-B2B3-7, LD-B2B3-8).** On the analysis path, `vcs_evidence` observes `.git`, `.hg`, `.svn` and `.jj` in that order, by one charged no-follow status read each (`observe_child_accounted`, the same cost as the legacy absence probe). The first present one decides:
- a marker directory is `directory`;
- a regular `.git` file is `indirection` with its `gitdir:` value (below);
- anything else is `indirection` with no target, and is never opened or followed.

`gitdir_target` opens the `.git` file no-follow from its parent and compares it with the observation (`ChildObservation::matches`). A change, or an open that finds it gone, a link or another kind, refuses the whole operation (`Changed`). So do exhaustion and host I/O. The descriptor is then judged by S3 file custody as a configuration file is (r2): owner, other and group write, the ACL under this invocation's premise and authorized groups, one link and at most 4 MiB, in SLM's order, with no owner waiver. A refused file keeps its boundary and has no target. An admitted file's bytes are read once from the judged descriptor, whose status must be unchanged before and after the read. One `gitdir: <path>` line, with an optional `\n` or `\r\n`, is the target. Anything else gives no target.

**Order (LD-B2B3-7).** On the analysis path the config is judged in SLM's refusal order (`CustodyOrder::Reference`: kind, owner, mode, ACL, then links and size). The legacy path keeps the shared order. The order changes only which reason is reported, never whether the config passes, and the capture and charges are the same. The function is B2-b2's `reference_order`, moved to the chain module as `check_project_object_ordered`; B2-b2's core calls it unchanged, and its 79 vectors still reproduce.

**The waiver (LD-B2B3-9).** `--trust-project-owner` with `--project` reaches exactly three judgments, and only when the waiver names the root's spelling byte for byte (`applicable_waiver`):
- the explicit directory's custody in `select`;
- its `opensip.json` (SLM:636, 665);
- the chain walk's root judgment (`walk_project_chain_waived`), and its recheck (`ProjectChain::recheck_waived`, through `ProjectRootAdmission::recheck_waived` in phase 2).

The chain remembers whether its walk waived the root (`owner_waived`). Its recheck waives again only then; otherwise the root is judged unwaived. The waiver never reaches an ancestor, the marker, `.opensip`, the local carrier, a mode or an ACL. Walk mode never has one.

**Lending (LD-B2B3-1).** `DiscoveryRoot<'a>` lends the admitted chain's retained root and spelling, the ACL omission premise, and the check that a filesystem is H's. It lends nothing else: no ledger, fence, registry or receipt. Its constructors are `pub(super)`, called only by the two lendings:
- **Read path.** `ReadSession::release(self) -> Result<ReleasedRead, SessionRefusal>` is the read session's equivalent release (MB item 12). It unlocks the fence and closes every retained installation handle (`InstallationObservation::release`), drops the ledger and captures, and keeps only the read receipt. A latched or failed session still releases its fence and returns `Latched`. A fence release error is the lock I/O row. `ReleasedRead::discovery_root(&admission)` builds the view.
- **Write path.** `ProjectOperation::discovery_root()` builds it from the subject's chain (eligible or registered) and the write receipt, after the handoff released the fence.

## Lead decisions (implementation; within plan r2)

- **LD-B2B3A-1. Four-marker evidence at a config or explicit root.** Plan r2 LD-B2B3-7 says a config or explicit root needs "one extra by-name `.git` observation". The candidate observes the same four markers, in the same order, as the walk does at any level, stopping at the first present one. With `.git` alone, a `.hg`, `.svn` or `.jj` root would record no `vcs`. That contradicts LD-B2B3-8's four markers and SLM, whose `vcs` is the directory's own evidence. The cost is at most three more status reads at the selected root.
- **LD-B2B3A-2. A non-directory `.hg`, `.svn` or `.jj` is `indirection` with no target.** Plan r2 names only `.git`'s other kinds. These three markers have no file form to read, so they are treated like `.git`'s other kinds: still X2b's boundary, never opened.
- **LD-B2B3A-3. Withdrawn in r2** (Codex B2B3A-R1-RF-1). The `.git` file is judged by S3 file custody, as plan r2 LD-B2B3-7 requires.
- **LD-B2B3A-4. A mount is the child's boundary, decided before the parent's depth.** On the analysis path, the device of each level is read before its depth is judged, as SLM does (its mount check reads the parent's `dev` from the child's iteration). The legacy order (depth, then device) is unchanged. A scratch tree cannot hold a mount, so no native control exists. The reference's own cases hold it.
- **LD-B2B3A-5. An explicit path is never resolved through a link.** X2 refuses a link anywhere in a spelling (no-follow opens). So `explicitPathWasSymlink` is always `false`, and a link in the spelling refuses as `PROJECT.ROOT_CUSTODY_REFUSED` with `SYMLINK`. SLM instead follows a harness-supplied `explicitResolved`. X2's stricter rule stands.
- **LD-B2B3A-6. The retained-path bound precedes the walk's depth bound.** X2 item 9 bounds the retained path from `/` at 256 components. A launch deeper than that refuses at its open (`Chain(PathInvalid)`), before any level, and `UpwardRecord::discovery_refusal` does not map it. The walk's own 256-level bound is therefore reachable only from a 256-component launch outside H. It maps to `WALK_DEPTH_EXCEEDED`.
- **LD-B2B3A-7. The analysis path's charges change; the legacy path's do not.** The analysis path now also spends on its evidence probes after a config, on `gitdir:` custody captures and reads, and on row copies. Every existing analysis caller passes no waiver and a fresh record. The legacy probe pins the legacy admission.

## Tests

- **`the_analysis_selection_reproduces_the_current_reference_on_native_trees`.** All 59 vectors are built under a scratch home and selected over natively, with `/H` for the home. They pin the reference's path and SHA-256. Rows compare for every case, refused or not.
  - **Accepted cases:** mode, `configPath`, stop reason, `vcs` kind and target, `explicitPathWasSymlink` and the selected root.
  - **Refused cases:** code, detail and the named path.
  - **The cases:**
    - 17 of SLM's upward-only discovery cases, by their reference ids, with their reference code and detail checked by the tool;
    - 7 further refusals: an absent launch; a FIFO and a directory as the config; three order controls (ACL before a hard link, ACL before oversize, and a hard link before oversize); and a waived foreign root whose config ACL grant still refuses;
    - 35 accepted selections: the home boundary, from below and as the launch; a config at an ancestor; a config beside a VCS directory and beside a `gitdir:` file; each of the four VCS directories; 17 `.git` file, symlink and FIFO forms, six of them new in r2 (five custody cases and a bare `\r`); a non-directory `.hg`; marker order; custody boundaries from mode and from an ACL grant; an authorized group; explicit roots with and without config; a waived foreign explicit root; and a waived foreign explicit root whose `.git` file is never waived (r2).
- **`every_upward_only_reference_case_a_scratch_tree_can_hold_is_a_vector`.** B2-b2's vectors list 19 upward-only cases. All are here except two, each with its own control: a waiver without `--project` is unconstructible (`grants_tests`), and an unreadable ACL is the next test.
- **`an_unreadable_acl_on_the_launch_refuses_custody`.** With no premise, an omitted ACL gives `ACL_UNREADABLE`, naming the launch.
- **`the_legacy_selection_records_nothing_and_selects_the_same_roots`.** For every accepted non-foreign vector, the legacy selection's `Selected` equals the recorded one.
- **`a_gitdir_file_is_judged_by_custody_and_a_change_or_exhaustion_is_never_a_null_target`.** A mismatched observation refuses `Changed`. A foreign invoking uid and an unadmitted omitted ACL each give no target (r2). A ledger one byte short refuses as budget, through `gitdir_target` and through `vcs_evidence`.
- **`a_refusal_after_selection_is_never_mapped_as_a_selection_refusal`** (r2, NBO-2).
- **`the_owner_waiver_reaches_only_its_explicit_root`.** The waiver applies only to its exact spelling, never to `home/./checkout`. A foreign owner passes only when waived, and the waiver never admits other-write.
- **`the_chain_walk_remembers_a_waiver_only_for_its_root`.**
- **`a_launch_beyond_the_retained_path_bound_refuses_at_its_open_with_no_row`.**
- **`a_released_read_session_frees_the_fence_and_lends_only_the_discovery_root`.** On a published scratch installation: the fence is held before `release` and free after it. The view's spelling and inode are the admission root's, and its premise is lent. The upward provenance is the repository's.
- **`a_latched_read_session_still_releases_its_fence_and_lends_nothing`.**
- **`the_operation_lends_the_discovery_root_after_the_fence_is_released`.** For an eligible root and a fresh registration.

## Check lanes

The evidence is lane r4, over the r2 candidate. Lane r2 was the reviewed r1 candidate's evidence. Lane r1 (kept in the work directory) passed every row but one, `legacy-admission-spend-equal`. The fault was in the lane's extractor, not the product: the probe's first line, `no-config`, follows the test harness's `test ... ` prefix on the same line, so a start-of-line match captured four lines where five were expected. Lane r1's logs show all five lines equal at base and candidate. Lane r2 matches the lines anywhere in the output. No product byte changed.

See `evidence/checks.json`. The rows are:
- the security and host suites at base and candidate, with equal failure sets;
- the legacy admission spend probe at base and candidate, with equal lines;
- warning-denied all-targets Clippy;
- rustfmt on base-clean and new edited files;
- the environment pin, both vector checks, the configuration tables, the operability census and verify_design;
- 17 code mutations, each caught (three new in r2, one retired).

## Not claimed

- No walker, listing, downward observation or FW-01 pin (B2-b3b).
- No seam or flag rows (B2-b3c).
- No production caller (J1).
- No public row and no rendering.
- No T2 census (B2-b4).
- No qualification.
