# CI-A3 r3: the launch member, a pinned entrypoint recheck (amendment to CI r5)

**Lead amendment, 2026-10-17. Proposed; it needs Codex review (round 3).** The law is "component release installation and tree custody" (`PROPOSAL.md`: r5 under its acceptance note, with CI-A1; r5's bytes are `PROPOSAL-r5.md`, cited here by line). The lead owns it as DR-103's delivery owner. CI-A3 has the shape of CI-A1 and CI-A2: it quotes each current LAW sentence or row, and gives its replacement or insertion. **It is a standalone amendment.** Accepting it changes LAW only as stated here, and until then LAW stands as written.

**Bases:**
- product main `114d2ac`;
- architecture `339d9dc56`;
- **CI-A2 as proposed in CI-2/CI-3's review subject `codex-ci-2-r2`** (lead decision LD-CIA3-R3): the exact bytes of `docs/implementation/m3/component-install/ci-2-r2/SCOPE.md` (37,281 bytes, SHA-256 `d79e838a4c63383a22e3090290d6feb309b776187afd3ab0f3fa0e49f7e2c4b8`), as that review's subject manifest `docs/implementation/m3/component-install/ci-2-r2-subject.json` (SHA-256 `988d53cc816e76523ac3a72299ef04f3b5c137e89e0ed64c06eb14dc099f452e`) pins them. That subject is immutable once packaged, unlike the live working `ci-2-r1/SCOPE.md`, which round 2 pinned and which has since changed. CI-A3 is written against r5 + CI-A1 + CI-A2 **as proposed there**, and is not accepted ahead of it. It depends on CI-A2's text only through its index rows (CI-A2-b, the retained component index; CI-A2-c, the search price, at most `⌈log₂ n⌉ + 1` comparisons, one edge each), rechecked against those bytes (CI-A2-c's row there reads "at most `⌈log₂ n⌉ + 1` … one edge each"). A byte copy of them is CI-A3's own immutable context member, `docs/implementation/m3/component-install/ci-a3-r3/context/ci-2-r2-SCOPE.md`. If CI-A2 changes in its review, CI-A3 is rebased in a new round.

## r3 changes (answering `codex-ci-a3-r2`)

| Item | Disposition | Where |
| --- | --- | --- |
| **CIA3-R2-RF-1** (the CI-A2 context pin) | **Rebased (LD-CIA3-R3).** The subject now pins CI-A2 from the immutable `codex-ci-2-r2` review subject's exact bytes, not the live working file. Round 2's pin of the live file is history: those bytes are gone from the live path and are not reconstructed. An intermediate pin to the `codex-ci-2-r1` subject, never submitted, was dropped when that review changed CI-A2. The CI fork's files are not touched. The two CI-A2 rows CI-A3 uses are rechecked against the pinned bytes. | Bases; Interaction |
| **CIA3-R2-RF-2** (exact executed charges versus bounds) | **Fixed.** Three expressions now: **`E_launch(m)`**, the exact executed charge, in independently observed counts (`s_j`, the comparisons the `j`-th lookup actually made; `a`, the read attempts actually made, one EOF attempt for an empty file); **`B_launch(m)`**, the per-member conservative bound, with `⌈log₂ n⌉ + 1` per lookup and `env(c)` reads; and **`B̂_launch(request)`**, the request pre-bound. `E ≤ B ≤ B̂` componentwise. No unused comparison is precharged and no extra read is made: each comparison and read attempt is charged immediately before it is made. CI-T28 now requires the actual charges to equal `E_launch` exactly, and the two inequalities separately, with an empty file, a one-chunk file and lookups matching at different depths. | CI-A3-b; CI-T28 |
| **Round 2 Q1's conditions** (the maxima) | Each maximum over an empty set is `0`. `Directory("")` is a stated special case, with no lookup or descent. Every final-path segment length is bounded by the largest segment over the requested kind's rows. All sums and products are checked before any allocation they fund. | CI-A3-b |
| CI-A2's revision in CI-2 r2 (CI-A2-h, copied names) | `B_launch`'s basename row no longer charges `b + 1`. CI-2's primitive copies the basename into a fixed stack buffer, which CI-A2-h makes no allocation and no charge, so charging it would precharge unused work. CI-A2-e's reservation semantics concern the installer's single debit and do not change `launch_member`, which charges each operation on the caller's scope as it runs. | CI-A3-b; Interaction |
| Round 2 Q2, Q3 | Accepted as written. Off-macOS unsupported outcomes are represented through the declared error types before charging, and the opening owner's model carries the one-time store-path term. | CI-A3-a, -d |

## Self-review (the lead's pre-submission checklist, `/tmp/opensip-implementation/PRE-SUBMISSION-CHECKLIST.md`, items 2 and 5)

- **Item 2, exact charges vs bounds.** `E_launch(m)` is the exact executed charge, in observed counts (`s_j`, the comparisons each lookup made; `a`, the read attempts made). `B_launch(m)` is the per-member bound, which replaces those counts with `⌈log₂ n⌉ + 1` and `env(c)`. `B̂_launch(request)` is the request pre-bound, a maximum over the TreeCommitment. `E ≤ B ≤ B̂` holds componentwise. Each comparison and read attempt is charged immediately before it is made, at its actual count. Nothing is precharged, and no read is made to fill an envelope. No feasibility is claimed from a subtotal: CI-T28 checks equality to `E_launch` and each inequality separately, over the stated shapes.
- **Item 5, immutable context pins.** The CI-A2 context is the SCOPE.md bytes pinned by the CI-2 review subject of `codex-ci-2-r2`, a submitted subject, byte-copied into CI-A3's own context path. The CI fork's live working file is not pinned. The law (`PROPOSAL-r5.md`) and CI-A3's own prior rounds are published or submitted bytes.

## r2 changes (answering `codex-ci-a3-r1`; history)

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

> - **The launch member's work, as three expressions** (CI-A3): the exact executed charge `E_launch(m)`, the per-member bound `B_launch(m)` and the request pre-bound `B̂_launch(request)`, with `E_launch ≤ B_launch ≤ B̂_launch` componentwise. **Every charge is made immediately before its operation, at the operation's actual count**: no unused comparison is precharged and no read is made to fill an envelope. An exhausted charge is `Budget`, before the operation it would fund. Funded observations already made stay made, and no path is produced.
>
>   **The quantities** (all from the TreeCommitment, the store record or the run itself, all in bytes or counts, and all distinct):
>   - `n`: the tree's entry count; `S`: its symlink count;
>   - `h`: the symlink rows actually followed by the resolution (`0 ≤ h ≤ S`). The lookups made are `h + 1`, or `0` for `Directory("")`;
>   - `s_j` (`1 ≤ j ≤ h + 1`): **the comparisons the `j`-th lookup actually made**, observed (`charged_find` charges one edge immediately before each). `0 ≤ s_j ≤ ⌈log₂ n⌉ + 1` (CI-A2-c's bound);
>   - `q_i` (`1 ≤ i ≤ h`): the byte length of the `i`-th joined path (the link's parent path, `/` unless the parent is the root, and the target text);
>   - for the final row:
>     - `p`, its path's byte length (`0` for `tree/` itself);
>     - `k`, its component count (`0` for `tree/` itself);
>     - `seg_j`, its components;
>     - `b = len(seg_k)`, its basename's length (files only);
>     - `c`, its authenticated content length (files only);
>   - `a`: **the read attempts actually made** for a file member, observed (`read_verified` charges one `rd` immediately before each, until the end of file is observed). `1 ≤ a ≤ env(c)`: an empty file is one attempt, the one that observes the end; a one-chunk file is two when each read returns its maximum. More than `env(c)` attempts is `Length` (item 6), never a further read;
>   - `L`: the byte length of the store's recorded absolute path (CI-A3-d);
>   - `P = L + 1 + 64 + 1 + 4`, plus `1 + p` when `p > 0`: the launch path's byte length without its terminator.
>
>   **`E_launch(m)`, the exact executed charge**, is the sum of these rows at their actual counts:
>
>   | Operation | Count | Price |
>   |---|---|---|
>   | lexical resolution: the `j`-th lookup in the retained index | `h + 1` lookups (`0` for `Directory("")`) | `s_j` edges, one before each comparison |
>   | each hop's joined path, an owned temporary dropped before the next lookup | `h` | objects 1, bytes `q_i` |
>   | descent along the final row's parent chain from the retained `tree/` handle | `k − 1` (`0` when `k ≤ 1`) | `desc(len(seg_j))` each, which includes each name's NUL-terminated copy |
>   | **file:** the basename's NUL-terminated native spelling, copied by the primitive into its fixed stack buffer (CI-A2-h; `NAME_CAPACITY` 1,024 bytes plus its NUL) | 1 | **no charge**: no allocation, so no owned record (CI-A2-h) |
>   | **file:** the open, with its kind-check status | 1 | `fopen` |
>   | **file:** read attempts through the retained buffer | `a` | `rd` each |
>   | **directory (`k ≥ 1`):** the final descent | 1 | `desc(len(seg_k))` |
>   | **directory:** its handle's status (`directory_identity`; on the retained `tree/` handle for `Directory("")`) | 1 | `st` |
>   | the launch path's one NUL-terminated buffer, shared by the binding and the result | 1 | objects 1, bytes `P + 1` |
>   | the binding's no-follow-final status read (`path_status_no_follow`) | 1 | `st` |
>   | the result record | 1 | one object of `LM` bytes (the record's size, a compile-time property of the code) |
>
>   A run that stops early (a refusal or `Budget`) has executed only the rows before its stop, at their actual counts.
>
>   **`B_launch(m)`, the per-member bound,** is `E_launch(m)` with each observed count replaced by its bound: each `s_j` by `⌈log₂ n⌉ + 1`, and `a` by `env(c)`. Every other row is already exact for a given member. So `E_launch(m) ≤ B_launch(m)`.
>
>   The read buffer is `B_open`'s, and the SHA-256 state is a fixed-size stack value (item 4), so neither is charged again. Handles opened are dropped at return. Every sum and product is computed with checked arithmetic before the allocation or operation it funds, and an overflow is the same refusal as exceeding the allowance.
> - **`B̂_launch(request)`, the request pre-bound,** for a caller funding the operation in advance. It is `B_launch` with each member-dependent quantity replaced by a maximum from the TreeCommitment. **A maximum over an empty set is `0`.**
>   - `h` by `S`, and the lookups by `S + 1`;
>   - each `q_i` by `Q̂`, the largest joined-path length over the tree's symlink rows (`0` when `S = 0`);
>   - the final row's `p`, `k`, `b` and `c`, and each `len(seg_j)`, by their maxima over the rows of the requested kind (files for `Entrypoint` and `File`, `dir` rows for `Directory`), or by the named row's own values when the request names a row directly and no hop is possible. Each segment length is bounded by the largest segment length over those rows.
>   - **`Directory("")`** is the stated special case: no lookup, hop or descent, one `st` on the retained `tree/` handle, the launch-path buffer at `p = 0`, the binding's `st` and the result record.
>   - A request whose kind has no rows can only refuse `Association` at its first lookup. Its pre-bound is that lookup, at `⌈log₂ n⌉ + 1` edges.
>
>   So `B_launch(m) ≤ B̂_launch(request)` for every member the request can resolve to. `B̂_launch` is never charged in place of the actual charges.

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
>   - **Latching:** a launch after a failed transfer, and a transfer after a failed launch, each refuse with the latched cause, with no charge and no observation.
> - **CI-T28 (CI-A3, work):**
>   - **The shapes:** a zero-length file under a long path; a large file under a short path; a nested member reached through two hops whose joined-path lengths differ from each other and from the final path; a nested `dir` member; `Directory("")`.
>   - **Independent enumeration:** an independently written enumerator lists, from a recorded call log, every charged call and every owned representation of the run: each lookup's comparisons, each hop temporary, each descent and its name copy, the basename's stack spelling (recorded, with no charge and no allocation), the open, the read attempts, the directory status, the shared launch-path buffer with its terminator, the binding's status read and the result record. Separately, it lists the store opening's one path record. It computes each expected size from the TreeCommitment and the store path themselves, not from the module's cost functions.
>   - **Exact executed work:** the run's actual charges equal `E_launch(m)` computed from the independently observed counts: each lookup's comparisons, recomputed by the enumerator's own search over the retained index, and the read attempts, recomputed from the file's length and the recorded read returns. This must hold when they are strictly below the envelopes. The enumerator includes an **empty file** (one EOF attempt, charged once; no second attempt), a **one-chunk file**, and **lookups that match at different search depths** (the first probe, an intermediate one, the last, and a miss).
>   - **Bounds, separately:** `E_launch(m) ≤ B_launch(m) ≤ B̂_launch(request)` componentwise, for every shape above, including `Directory("")` and a request whose kind has no rows.
>   - **Exhaustion:** a scope one unit short before each **actual** allocation, comparison, read attempt and status operation refuses `Budget`, with nothing allocated or observed past it and no path produced. Earlier funded observations may already have occurred.
>   - **Partition:** an injected I/O failure in the member's read refuses `Io`, not `Digest`; an injected `EIO` from `path_status_no_follow` refuses `Io`, not `Binding`; `ENOENT` and `ENOTDIR` from it refuse `Binding`.

## Interaction with CI-2/CI-3 (in progress, with CI-A2)

- **Not folded into CI-2/CI-3's review.** CI-2/CI-3's package is one unit with CI-A2, already built in its worktree (`opensip-ci2`: `crates/lifecycle/src/retained_tree.rs`, `installation.rs`). CI-A3 does not change that unit's subject or reset its review. Its code lands as **CI-3L**, a separate unit after CI-2/CI-3 integrate, on their main.
- **CI-3L touches CI-3's files.** It changes `retained_tree.rs` (the operation, `B_launch`, `Binding`) and `installation.rs` (`ComponentStore` records its absolute path, CI-A3-d; `open_in` and `fixture` gain the path). So CI-3L's lane starts only after CI-2/CI-3 are on main, and its integrate script refuses if main changed one of its paths since its lane base.
- **Reused machinery.** CI-3L reuses CI-3's `charged_find` (CI-A2-c; one edge before each comparison it actually makes), `descend` and `descend_cost`, `open_regular_no_follow` and `read_verified` (one `rd` before each attempt it actually makes, refusing `Length` once `env(c)` attempts are spent). CI-2's `open_regular_no_follow` copies the basename NUL-terminated into its fixed stack buffer (`StackName`, `NAME_CAPACITY` 1,024), which under CI-A2-h is no allocation and carries no charge. So `B_launch` charges nothing for it, and precharges nothing (round 2's `b + 1` row is withdrawn). A basename longer than the buffer refuses before any charge (`TreeOpenError::Name`). The archive profile already caps a tree path at 100 bytes (CI-T5), so a committed member cannot reach that refusal, and CI-3L maps it to `Association`. The launch-path buffer stays an owned heap record of `P + 1` bytes, because it is the result's path and may exceed the stack buffer. `path_status_no_follow` borrows it as `&CStr` and copies nothing.
- **New platform primitives (NBO-1), owned by the platform owner, added by CI-3L in `crates/platform/src/component_tree.rs`.** CI-2's candidate has neither: its `entry_status` takes one slash-free component relative to a retained directory and returns `{kind, mode, length}` with no identity, and its `sample_identity` observes an opened file, not a spelling.
  - `path_status_no_follow(path: &CStr, work) -> Result<PathStatus, WorkFailure<PathStatusError>>`: one `lstat` of an absolute spelling, charged `status_read_cost()` before the call. `PathStatus` is `{kind: EntryKind, mode, device, inode}`, and `PathStatusError` is `{Absent, NotDirectory, Io(io::Error)}`. The caller owns and charges the spelling.
  - `directory_identity(directory: &RetainedDirectory, work) -> Result<PathStatus, WorkFailure<io::Error>>`: one `fstat` of a retained directory handle, charged `status_read_cost()`.
  - Both refuse `Unsupported` off macOS before charging, as their siblings do. Both use P-7's published price, so no new price is introduced.
- **Failure latching (CI-2 r2).** The capability latches its first transfer failure, so every later `transfer` refuses with the same cause. `launch_member` obeys the same latch. On a capability that has latched, it refuses with the latched cause before any charge or observation. Its own first failure (any typed failure other than `Budget`, which the ledger latches itself) latches the capability in the same way, so no later launch or transfer of that capability proceeds. CI-T27 gains the matching control: a launch after a failed transfer, and a transfer after a failed launch, each refuse with the latched cause and make no observation.
- **The CI fork's in-flight candidate** already partitions `TreeReadFailure` (`retained_tree.rs`:40-65). `Binding` is a new member there, added by CI-3L, so CI-3's own controls are unchanged. `NotInstalled` and `Pin` cannot arise from `launch_member`, since the capability is already open and pinned.
- **CI-A2's pinned bytes** are those of the `codex-ci-2-r2` subject (Bases). If CI-A2 changes in that review, CI-A3's lookup rows, which cite CI-A2-b's index and CI-A2-c's search bound, are rebased in a new round. No other dependency exists. The CI fork's live working files (`ci-2-r1/SCOPE.md`, `ci-2-r2/SCOPE.md`) are theirs, and CI-A3 neither pins nor edits it.

## Not claimed

- No spawn.
- No D1a change (round 1, Q3): no second sample before `posix_spawn`.
- No D4 code.
- No new public code or route.
- No closure of the same-principal window (CI-A3-a's residual).
- No Linux.
- No qualification.

## Questions for the reviewer

Rounds 1 and 2 are ruled (`codex-ci-a3-r1`, `codex-ci-a3-r2`). For this round:

- **Q1 (RF-2).** Do `E_launch`, `B_launch` and `B̂_launch` now separate exact executed work from the envelopes, with `E ≤ B ≤ B̂` and with every charge at its actual operation?
- **Q2 (RF-1).** Is pinning CI-A2 from the immutable `codex-ci-2-r2` subject, with round 2's live-file pin kept as history only, the right rebase? Do CI-A3's lookup rows agree with CI-A2-b and CI-A2-c in those bytes?
- **Q3 (CI-A2's revision).** Do `B_launch`'s rows agree with CI-A2-h's stack-buffer convention (no charge for the basename; the heap launch-path buffer kept) and with CI-A2-e's reservation semantics, and is the capability's failure latch correctly extended to `launch_member`?
