# CI-A3 r2: the launch member, a pinned entrypoint recheck (amendment to CI r5)

**Lead amendment, 2026-10-17. Proposed; it needs Codex review (round 2).** The law is "component release installation and tree custody" (`PROPOSAL.md`: r5 under its acceptance note, with CI-A1; r5's bytes are `PROPOSAL-r5.md`, cited here by line). The lead owns it as DR-103's delivery owner. CI-A3 has the shape of CI-A1 and CI-A2: it quotes each current LAW sentence or row, and gives its replacement or insertion. **It is a standalone amendment.** Accepting it changes LAW only as stated here, and until then LAW stands as written.

**Bases:**
- product main `d704ed4`;
- architecture `b1f80423` (the D4 plan r2 published);
- **CI-2/CI-3's candidate** (worktree `opensip-ci2`, proposing CI-A2 in its `SCOPE.md` §4; not yet reviewed). CI-A3 is written against r5 + CI-A1 + CI-A2 **as proposed**. If CI-A2 changes in its review, CI-A3 is rebased in a new round, and nothing here depends on CI-A2's text beyond its index rows (CI-A2-b, CI-A2-c).

## r2 changes (answering `codex-ci-a3-r1`)

| Item | Disposition | Where |
| --- | --- | --- |
| **CIA3-R1-RF-1** (content length versus path length; every owned native-name representation) | **Fixed.** `B_launch` now uses distinct symbols: `c` (the final row's authenticated content length) for the read envelope; `p` (the final row's path byte length), `b` (its basename length) and `k` (its component count) for the path's representations and descents; `h` (symlink hops actually followed) and `h + 1` lookups; `q_i` (each hop's joined-path length); `L` (the store path's length). Every owned native spelling is priced, with its terminator: the file open's NUL-terminated basename `b + 1`, each descent's name (already inside `desc(k)`'s `k + 1`), and one shared NUL-terminated launch-path buffer of `P + 1` bytes, used for the binding's status read and then reused, without reallocation, as the result's path. The store-path record is charged once, at the store's opening (CI-A3-d), never per launch. `Directory("")` has no lookup, no hop, no descent and no negative count. A separate conservative pre-bound `B̂_launch` replaces each actual count by a stated maximum over the TreeCommitment. CI-T28 adds the requested shapes and independent enumeration. | CI-A3-b; CI-A3-d; CI-T28 |
| **CIA3-R1-NBO-1** (the absolute-path identity observation) | **Addressed.** CI-3L adds two platform primitives in `component_tree.rs`, owned by the platform owner: `path_status_no_follow(&CStr, work) -> Result<PathStatus, WorkFailure<PathStatusError>>` (`lstat`, charged `st` before the call; `PathStatus {kind, mode, device, inode}`; `PathStatusError {Absent, NotDirectory, Io}`), and `directory_identity(&RetainedDirectory, work)` (`fstat` of a retained directory, charged `st`). Neither exists in CI-2's candidate. The r1 sentence "It adds no platform primitive" is withdrawn. | CI-A3-a; Interaction |
| **Q1** (accepted) | The entrypoint is taken from the same authenticated selected-platform association the capability holds, never from the caller. The bounded rule (at most `S + 1` lookups) replaces security's seen-set, with no allocation for it. | CI-A3-a |
| **Q2** (accepted, with the seam's outcomes explicit) | The binding's outcomes are partitioned at the seam: `Absent` and `NotDirectory` from the path observation, a non-matching kind, a symlink final component or different `(device, inode)` are `Binding`; any other native error is `Io`; a refused charge is `Budget`. | CI-A3-a |
| **Q3** (no D1a amendment) | The r1 suggestion that D1a "may narrow the window" is withdrawn. M3-D item 2 already places the recheck and discloses the same-user window; CI-A3 claims to close it neither by the pin nor by a repeated sample. | CI-A3-a; Not claimed |
| **Q4** (accepted, with wording) | A directory member's identity, mode and binding, with the retained pin, are sufficient here. The text now says that a directory inode or `flock` does not attest unchanged descendant bytes against a same-user writer. Files named individually by a launch spec get their own re-hash. | CI-A3-a |
| **Q5** | Answered by RF-1's rewrite. | CI-A3-b |
| **Q6** (accepted) | CI-3L covers CI-A3-a to CI-A3-f, including `Binding` and the controls, and the two platform primitives. | CI-A3-f |
| Review notes on CI-A3-c | The operation's explicit ownership of the capability through child settlement is stated as the operative rule; the borrow is a guard, not the mechanism, since D1a's values are owned and clonable. The sole production factory path and lifetime controls enforce it. | CI-A3-c |

## Why

D4's session factory must make "the closure owner's recheck, 'descriptor/identity/open-handle or digest recheck binding verification to spawn' (CPC:251)" immediately before D1 (M3-D r5 item 2, `supervisor-d/PROPOSAL-r5.md`:212; item 26, :852-878). The spawner accepts only a `VerifiedLaunch`, which holds a `ClosureRecheck {member, device, inode, sha256}` and a `LaunchSpec` with an **absolute executable path** (`crates/platform/src/process.rs`:177-183, :335-358). macOS has no `execveat`, so D1a spawns by path (`posix_spawn`).

CI r5's capability offers two operations:
- **opening** (item 6), which verifies the whole tree;
- **`transfer`**, which copies one verified file into a retention sink.

Neither yields a launch path joined to a rechecked member identity. (Round 1 is `CI-A3-r1.md`, reviewed REQUIRED-FINDINGS in `codex-ci-a3-r1`.) `codex-d4-plan-r1` Q7 accepted the architecture "subject to … CI-A3 acceptance before D4-4", and required that CI-A3 "define the entrypoint resolution, retained lifetime/path binding, exact prices and typed failures. The launch path, rechecked member identity and selected entrypoint must be joined, and the pin must remain alive through spawn."

## The amendment

### CI-A3-a: item 6 gains the launch-member operation

**Current** (`PROPOSAL-r5.md`, item 6, after the transfer bullet ending "this law supplies only the verified bytes", :295-300): there is no third operation.

**Insertion, after the transfer bullet:**

> - **The launch member (CI-A3).** `RetainedTree::launch_member(&mut self, request: MemberRequest<'_>, work: &mut WorkScope) -> Result<LaunchMember<'_>, TreeReadFailure>`. It is the only operation that yields a path to spawn.
>   - **The request.** `MemberRequest::Entrypoint` names the selected platform row's `entrypoint` (CMS `platforms[].entrypoint`), **taken from the same authenticated selected-platform association the capability holds**, never from the caller (Q1). `MemberRequest::File(path)` names a regular-file row, and `MemberRequest::Directory(path)` a `dir` row, including `""` for `tree/` itself. The caller names a path; the capability decides what it resolves to.
>   - **Resolution, lexical only.** The member is found in the capability's retained index (CI-A2-b) by binary search. A `symlink` row is followed **over the TreeCommitment, never on the filesystem**, by the security owner's rule (`crates/security/src/component_manifest.rs`:313-331). The target text is joined to the link's parent path, and the result is looked up again. At most `S + 1` lookups are made, `S` being the tree's symlink count; that bound replaces security's seen-set, so nothing is allocated for cycle detection. The analyzer manifest's validation already proved that chain acyclic and ending in an executable `file` row (:334-379, the entrypoint check at :366-379). The launch member is the **final** row, so no link is traversed at spawn. `Entrypoint` and `File` must end at a `file` row, and `Directory` at a `dir` row. Any other result, a lookup that finds no row, or more than `S + 1` lookups is `Association`.
>   - **Observation from the retained base.** From the retained `tree/` handle, the member's parent chain is descended one component at a time, no-follow, as `transfer` does (none for a root-level member). Then:
>     - a **file** member is opened no-follow with its kind check. Its type, its installed mode (LD-CI-10's function of the authenticated mode) and its length are compared with its row, and its bytes are read in full through the retained buffer and hashed, as `transfer` reads them, with no sink;
>     - a **directory** member is entered with the same descent, its handle's status is read (`directory_identity`), and its type and installed mode are compared with its row. Its contents are not re-hashed: the capability's open verified them, and the pin keeps the generation from lawful removal. **A directory's inode or `flock` does not attest unchanged descendant bytes against a same-user writer** (item 5's custody limits); files a launch spec names individually are each requested as `File` members and re-hashed. `Directory("")` is `tree/` itself: no lookup, no descent, and `directory_identity` on the retained `tree/` handle.
>
>     The failures are `Absent`, `Type`, `Mode`, `Length` and `Digest`, as item 6's checks define them. The observed `(device, inode)` comes from the opened handle's status: the file open's kind-check status, or `directory_identity`.
>   - **The path binding.** The launch path is composed **once**, as one owned NUL-terminated byte buffer, `<storePath>/<closure2-hex>/tree` followed by `/<member path>` unless the member is `tree/` itself. `<storePath>` is the store's recorded absolute location (item 5; CI-A3-d). The buffer is re-observed by **`path_status_no_follow`** (`lstat`: it does not follow the final component), and then becomes the result's path without reallocation (its NUL is dropped in place). The seam's outcomes are explicit (Q2):
>     - the observation names a regular file (a directory, for `Directory`) with the handle's `(device, inode)`: bound;
>     - `PathStatusError::Absent` (`ENOENT`), `PathStatusError::NotDirectory` (`ENOTDIR` along the path), a symlink or other kind at the final component, or a different `(device, inode)`, even with identical bytes: **`Binding`**, a new typed failure (CI-A3-e);
>     - any other native error: `Io {call: "lstat", …}`;
>     - a refused charge: `Budget`, before the call.
>   - **The result.** `LaunchMember<'c>` borrows the capability (`'c`). It holds the owned launch path, `(device, inode)`, the row's SHA-256 (files) and the row index. Only `launch_member` constructs one. Because it borrows the capability, it cannot outlive the pin.
>   - **What it is not.** It does not spawn, it is not a retention transfer, and it is not authority for the tree. It records nothing in the store, and it changes no mode.
>   - **The residual window (stated, not closed).** Between the path binding and the spawner's own path resolution, the path is re-resolved by the kernel. The store's custody excludes other principals, but not the invoking user's own processes or root (item 5, "Exactly what custody excludes"), so the law claims **no** exclusivity in that window. The binding proves the path named the verified member at the instant of its re-observation. A later substitution needs a same-principal write to a private, write-bit-free, pinned generation, which is an ambient trusted-TCB act (PPBS EE-5b's "not admission-enforced"), not an admitted path, and M3-D item 2 already discloses the same-user window between recheck and exec. **CI-A3 does not claim to close it**, either by the pin (which prevents lawful GC, not same-principal writes) or by any repeated sample. No D1a change is made (round 1, Q3).

### CI-A3-b: item 4 gains `B_launch`

**Current** (item 4, after the `B_transfer(f)` table and its sentence "The sink commits only when the final length and digest verify.", :199-207): no recipe for a launch member.

**Insertion, after it:**

> - **`B_launch(m)`, one `launch_member` of member `m`** (CI-A3), from the capability's retained index and retained `tree/` handle. **The quantities** (all from the TreeCommitment or the store record, all in bytes or counts, and all distinct):
>   - `n`: the tree's entry count; `S`: its symlink count;
>   - `h`: the symlink rows actually followed by the resolution (`0 ≤ h ≤ S`); the lookups made are `h + 1`, or `0` for `Directory("")`;
>   - `q_i` (`1 ≤ i ≤ h`): the byte length of the `i`-th joined path (the link's parent path, `/` unless the parent is the root, and the target text);
>   - for the final row: `p`, its path's byte length (`0` for `tree/` itself); `k`, its component count (`0` for `tree/` itself); `seg_j`, its components; `b = len(seg_k)`, its basename's length (files only); `c`, its authenticated content length (files only);
>   - `L`: the byte length of the store's recorded absolute path (CI-A3-d);
>   - `P = L + 1 + 64 + 1 + 4`, plus `1 + p` when `p > 0`: the launch path's byte length without its terminator.
>
>   | Operation | Count | Price |
>   |---|---|---|
>   | lexical resolution: a lookup in the retained index | `h + 1` (`0` for `Directory("")`) | at most `⌈log₂ n⌉ + 1` comparisons, one edge each (CI-A2-c's price) |
>   | each hop's joined path, an owned temporary dropped before the next lookup | `h` | objects 1, bytes `q_i` |
>   | descent along the final row's parent chain from the retained `tree/` handle | `k − 1` (`0` when `k ≤ 1`) | `desc(len(seg_j))` each, which includes each name's NUL-terminated copy |
>   | **file:** the basename's NUL-terminated native spelling | 1 | objects 1, bytes `b + 1` |
>   | **file:** the open, with its kind-check status | 1 | `fopen` |
>   | **file:** read attempts through the retained buffer | `env(c)` | `rd` each |
>   | **directory (`k ≥ 1`):** the final descent | 1 | `desc(len(seg_k))` |
>   | **directory:** its handle's status (`directory_identity`; on the retained `tree/` handle for `Directory("")`) | 1 | `st` |
>   | the launch path's one NUL-terminated buffer, shared by the binding and the result | 1 | objects 1, bytes `P + 1` |
>   | the binding's no-follow-final status read (`path_status_no_follow`) | 1 | `st` |
>   | the result record | 1 | one object of `LM` bytes (the record's size, a compile-time property of the code) |
>
>   The read buffer is `B_open`'s, and the SHA-256 state is a fixed-size stack value (item 4), so neither is charged again. Handles opened are dropped at return. Every row is charged before its operation, with checked arithmetic. An exhausted charge is `Budget`, with no observation and no path produced.
> - **The conservative pre-bound `B̂_launch(request)`**, for a caller funding the operation in advance. Each actual count is replaced by a maximum computed from the TreeCommitment:
>   - `h` by `S`;
>   - each `q_i` by `Q̂`, the largest joined-path length over the tree's symlink rows;
>   - the final row's `p`, `k`, `b`, `c` and segment lengths by their maxima over rows of the requested kind (files for `Entrypoint` and `File`, dirs for `Directory`), or by the named row's own values when the request names a row directly and no hop is possible.
>
>   `B̂_launch` dominates `B_launch` componentwise. It is never substituted for the actual charges, which are made as the operation runs.

### CI-A3-c: item 7's lifetime covers the launch

**Current** (item 7, "Pin acquisition and continuity", the second bullet, :308): "The pin is a shared `flock`, so it survives the fence-to-lease handoff (SL S7: leases follow the fence). The operation holds it through R11 and every later step, until the operation ends or, for a Run, until the Run releases it."

**Replacement:** that sentence, followed by: "**Every spawn of a closure member happens while the operation holds that closure's pin** (CI-A3). **The operation owns the capability through the spawned child's settlement**: it obtains a path from `launch_member` only while its `LaunchMember` borrows the pinned capability, and it keeps the capability open until every child spawned from that closure has settled. The borrow is a guard, not the mechanism: the launch values D1a receives are owned and clonable, so the sole production path to a `VerifiedLaunch` (M3-D item 2) and the lifetime controls enforce the rule. A Run that releases its pin after its retention (below) does so only after every child spawned from that closure has settled."

### CI-A3-d: item 5 records the store's absolute location

**Current** (item 5, "Location (LD-CI-7, kept)", :265): "`<installRoot>/components/`, created by installation provisioning as a private `0700` directory. The lifecycle locations owner (`crates/lifecycle/src/locations.rs`) gains it."

**Replacement:** that text, followed by: "**The store keeps the absolute path it was opened at** (CI-A3), as the locations owner gives it: the installation root's admitted absolute path joined with `components`, `L` bytes. **It is charged once, at the store's opening**: `ComponentStore::open_in` (and the fixture constructor) take the caller's `WorkScope` and charge objects 1, bytes `L` before copying the path, on the operation's ledger that opens the store. No launch charges it again. It is used only to compose launch paths, and it confers nothing: every read stays descriptor-relative and no-follow from the retained store directory, and a launch path is used only after `launch_member`'s binding."

### CI-A3-e: item 6's and item 8's typed failures gain `Binding`

**Current** (item 6, "The other typed failures", :293): "`NotInstalled` (no `<closure2-hex>`), `Pin` (r3), `Budget`, `Io{call, errno}`."

**Replacement:** "`NotInstalled` (no `<closure2-hex>`), `Pin` (r3), `Binding` (CI-A3: the composed launch path does not name the verified member), `Budget`, `Io{call, errno}`."

**Current** (item 8, :333): "**`Absent`, `Length`, `Digest`, `Type`, `Mode`, `LinkTarget`, `Extra`, `Association`, `Pin` and `Custody`** are a promised tree's own corruption."

**Replacement:** "**`Absent`, `Length`, `Digest`, `Type`, `Mode`, `LinkTarget`, `Extra`, `Association`, `Pin`, `Custody` and `Binding`** are a promised tree's own corruption." The rest of the bullet is unchanged. So `Binding` routes operational-failed 4, `HOST.IO_FAILURE`, `DELIVERY.CLOSURE_BYTES_CORRUPT` durably, and the same with no detail ephemerally. No code is added. `Io` and `Budget` keep their existing routes (:334).

### CI-A3-f: item 9's units and controls

**Current** (item 9, the CI-3 unit, :340): "**CI-3, the retained-tree capability:** lifecycle. It covers item 6 and item 7's pin. **C2a-3 binds CI-3**; C2a-4's wiring waits for it (`codex-c2a-plan-r2` Q6)."

**Replacement:** that text, followed by: "**CI-3L, the launch member (CI-A3):** lifecycle, after CI-3, with two platform primitives (`path_status_no_follow`, `directory_identity`). It covers CI-A3-a to CI-A3-f: the operation, `B_launch` and `B̂_launch`, the store-path record, `Binding`, and CI-T27 and CI-T28. **D4-4 binds CI-3L** (`codex-d4-plan-r1` Q7; `codex-d4-plan-r2` NBO-1): CI-A3's acceptance alone does not supply the operation."

**Insertion, after CI-T26 (:391-397):**

> - **CI-T27 (CI-A3, the launch member):**
>   - **Resolution:** a root-level file entrypoint; a nested one; an entrypoint that is a symlink row to a file row, and one through two links. The result is the final file row, and the spawned path contains no link. A link chain longer than `S + 1` lookups, and a request resolving to a row of the wrong type, refuse `Association`.
>   - **Observation:** a changed byte refuses `Digest`; a truncated file `Length`; a changed mode `Mode`; a file replaced by a directory `Type`; a removed file `Absent`. Each comes from the retained base, with no multi-component `openat`.
>   - **Binding:** a launch path whose final component is replaced by a symlink to an identical copy, and one whose store path names a different directory, each refuse `Binding`.
>   - **Directory members:** `Directory("")` and a nested `dir` row give `(device, inode)` and a mode check, with no content read.
>   - **Lifetime:** a `LaunchMember` cannot outlive its capability (a compile-fail probe); GC under the fence retains a generation whose capability a test holds across a spawn of its member.
> - **CI-T28 (CI-A3, work):**
>   - **The shapes:** a zero-length file under a long path; a large file under a short path; a nested member reached through two hops whose joined-path lengths differ from each other and from the final path; a nested `dir` member; `Directory("")`.
>   - **Independent enumeration:** an independently written enumerator lists, from a recorded call log, every charged call and every owned representation of the run: each lookup's comparisons, each hop temporary, each descent and its name copy, the basename's NUL-terminated spelling, the open, the read attempts, the directory status, the shared launch-path buffer with its terminator, the binding's status read and the result record. Separately, it lists the store opening's one path record. It computes each expected size from the TreeCommitment and the store path themselves, not from the module's cost functions.
>   - **Bounds:** the run's charges equal `B_launch(m)` for the actual counts, and are at most `B̂_launch(request)`.
>   - **Exhaustion:** a scope one unit short before each allocation, read attempt and status operation refuses `Budget`, with nothing allocated or observed past it and no path produced.
>   - **Partition:** an injected I/O failure in the member's read refuses `Io`, not `Digest`; an injected `EIO` from `path_status_no_follow` refuses `Io`, not `Binding`; `ENOENT` and `ENOTDIR` from it refuse `Binding`.

## Interaction with CI-2/CI-3 (in progress, with CI-A2)

- **Not folded into CI-2/CI-3's review.** CI-2/CI-3's package is one unit with CI-A2, already built in its worktree (`opensip-ci2`: `crates/lifecycle/src/retained_tree.rs`, `installation.rs`). CI-A3 does not change that unit's subject or reset its review. Its code lands as **CI-3L**, a separate unit after CI-2/CI-3 integrate, on their main.
- **CI-3L touches CI-3's files.** It changes `retained_tree.rs` (the operation, `B_launch`, `Binding`) and `installation.rs` (`ComponentStore` records its absolute path, CI-A3-d; `open_in` and `fixture` gain the path). So CI-3L's lane starts only after CI-2/CI-3 are on main, and its integrate script refuses if main changed one of its paths since its lane base.
- **Reused machinery.** CI-3L reuses CI-3's `charged_find` (CI-A2-c), `descend` and `descend_cost`, `open_regular_no_follow` and `read_verified`. CI-2's `open_regular_no_follow` builds its NUL-terminated basename itself and leaves copied names to the caller's records (`component_tree.rs`'s header). CI-3L therefore charges `b + 1` before calling it, as `B_launch`'s row states.
- **New platform primitives (NBO-1), owned by the platform owner, added by CI-3L in `crates/platform/src/component_tree.rs`.** CI-2's candidate has neither: its `entry_status` takes one slash-free component relative to a retained directory and returns `{kind, mode, length}` with no identity, and its `sample_identity` observes an opened file, not a spelling.
  - `path_status_no_follow(path: &CStr, work) -> Result<PathStatus, WorkFailure<PathStatusError>>`: one `lstat` of an absolute spelling, charged `status_read_cost()` before the call. `PathStatus` is `{kind: EntryKind, mode, device, inode}`, and `PathStatusError` is `{Absent, NotDirectory, Io(io::Error)}`. The caller owns and charges the spelling.
  - `directory_identity(directory: &RetainedDirectory, work) -> Result<PathStatus, WorkFailure<io::Error>>`: one `fstat` of a retained directory handle, charged `status_read_cost()`.
  - Both refuse `Unsupported` off macOS before charging, as their siblings do. Both use P-7's published price, so no new price is introduced.
- **The CI fork's in-flight candidate** already partitions `TreeReadFailure` (`retained_tree.rs`:40-65). `Binding` is a new member there, added by CI-3L, so CI-3's own controls are unchanged. `NotInstalled` and `Pin` cannot arise from `launch_member`, since the capability is already open and pinned.
- **If CI-A2 changes in review,** CI-A3's `B_launch` row that cites CI-A2-c's search price is rebased in a new round. No other dependency exists.

## Not claimed

- No spawn.
- No D1a change (round 1, Q3): no second sample before `posix_spawn`.
- No D4 code.
- No new public code or route.
- No closure of the same-principal window (CI-A3-a's residual).
- No Linux.
- No qualification.

## Questions for the reviewer

Round 1's Q1 to Q6 are ruled (`codex-ci-a3-r1`). For this round:

- **Q1 (RF-1).** Are `B_launch`'s quantities now distinct and complete, with every owned native spelling, terminator, the shared launch-path buffer and the one-time store-path record priced before use? Does `B̂_launch` conservatively dominate it?
- **Q2 (NBO-1).** Are `path_status_no_follow` and `directory_identity`, with their error partition and P-7's price, the right owner and API for the binding's observations?
- **Q3.** Is charging the store-path record at `ComponentStore::open_in`, on the opening operation's ledger, the right charge site? `open_in` takes a `WorkScope` it does not take in CI-2's candidate.
