# CI-A3 r1: the launch member, a pinned entrypoint recheck (amendment to CI r5)

**Lead amendment, 2026-10-17. Proposed; it needs Codex review.** The law is "component release installation and tree custody" (`PROPOSAL.md`: r5 under its acceptance note, with CI-A1; r5's bytes are `PROPOSAL-r5.md`, cited here by line). The lead owns it as DR-103's delivery owner. CI-A3 has the shape of CI-A1 and CI-A2: it quotes each current LAW sentence or row, and gives its replacement or insertion. **It is a standalone amendment.** Accepting it changes LAW only as stated here, and until then LAW stands as written.

**Bases:**
- product main `d704ed4`;
- architecture `9415426c`;
- **CI-2/CI-3's candidate** (worktree `opensip-ci2`, proposing CI-A2 in its `SCOPE.md` §4; not yet reviewed). CI-A3 is written against r5 + CI-A1 + CI-A2 **as proposed**. If CI-A2 changes in its review, CI-A3 is rebased in a new round, and nothing here depends on CI-A2's text beyond its index rows (CI-A2-b, CI-A2-c).

## Why

D4's session factory must make "the closure owner's recheck, 'descriptor/identity/open-handle or digest recheck binding verification to spawn' (CPC:251)" immediately before D1 (M3-D r5 item 2, `supervisor-d/PROPOSAL-r5.md`:212; item 26, :852-878). The spawner accepts only a `VerifiedLaunch`, which holds a `ClosureRecheck {member, device, inode, sha256}` and a `LaunchSpec` with an **absolute executable path** (`crates/platform/src/process.rs`:177-183, :335-358). macOS has no `execveat`, so D1a spawns by path (`posix_spawn`).

CI r5's capability offers two operations:
- **opening** (item 6), which verifies the whole tree;
- **`transfer`**, which copies one verified file into a retention sink.

Neither yields a launch path joined to a rechecked member identity. `codex-d4-plan-r1` Q7 accepted the architecture "subject to … CI-A3 acceptance before D4-4", and required that CI-A3 "define the entrypoint resolution, retained lifetime/path binding, exact prices and typed failures. The launch path, rechecked member identity and selected entrypoint must be joined, and the pin must remain alive through spawn."

## The amendment

### CI-A3-a: item 6 gains the launch-member operation

**Current** (`PROPOSAL-r5.md`, item 6, after the transfer bullet ending "this law supplies only the verified bytes", :295-300): there is no third operation.

**Insertion, after the transfer bullet:**

> - **The launch member (CI-A3).** `RetainedTree::launch_member(&mut self, request: MemberRequest<'_>, work: &mut WorkScope) -> Result<LaunchMember<'_>, TreeReadFailure>`. It is the only operation that yields a path to spawn.
>   - **The request.** `MemberRequest::Entrypoint` names the selected platform row's `entrypoint` (CMS `platforms[].entrypoint`, the TreeCommitment's own platform). `MemberRequest::File(path)` names a regular-file row, and `MemberRequest::Directory(path)` a `dir` row, including `""` for `tree/` itself. The caller names a path; the capability decides what it resolves to.
>   - **Resolution, lexical only.** The member is found in the capability's retained index (CI-A2-b) by binary search. A `symlink` row is followed **over the TreeCommitment, never on the filesystem**, by the security owner's rule (`crates/security/src/component_manifest.rs`:313-331). The target text is joined to the link's parent path, and the result is looked up again, at most `S + 1` lookups, `S` being the tree's symlink count. The analyzer manifest's validation already proved that chain acyclic and ending in an executable `file` row (:334-379, the entrypoint check at :366-379). The launch member is the **final** row, so no link is traversed at spawn. `Entrypoint` and `File` must end at a `file` row, and `Directory` at a `dir` row. Any other result, a lookup that finds no row, or more than `S + 1` lookups is `Association`.
>   - **Observation from the retained base.** From the retained `tree/` handle, the member's parent chain is descended one component at a time, no-follow, as `transfer` does (none for a root-level member). Then:
>     - a **file** member is opened no-follow with its kind check. Its type, its installed mode (LD-CI-10's function of the authenticated mode) and its length are compared with its row, and its bytes are read in full through the retained buffer and hashed, as `transfer` reads them, with no sink;
>     - a **directory** member is entered with the same descent, and its type and installed mode are compared with its row. Its contents are not re-hashed, since the open already verified them, and the pin keeps the generation from removal.
>
>     The failures are `Absent`, `Type`, `Mode`, `Length` and `Digest`, as item 6's checks define them. The observed `(device, inode)` comes from the opened handle's status.
>   - **The path binding.** The launch path is composed as `<storePath>/<closure2-hex>/tree/<member path>`, where `<storePath>` is the store's absolute location as the locations owner admitted it when the store was opened (item 5; CI-A3-d). The composed path is then re-observed by one status read that does not follow its final component. It must name a regular file (or a directory, for `Directory`) with the same `(device, inode)` as the handle. Any other result, or a status-read failure other than an I/O failure, is **`Binding`**, a new typed failure (CI-A3-e).
>   - **The result.** `LaunchMember<'c>` borrows the capability (`'c`). It holds the owned launch path, `(device, inode)`, the row's SHA-256 (files) and the row index. Only `launch_member` constructs one. Because it borrows the capability, it cannot outlive the pin.
>   - **What it is not.** It does not spawn, it is not a retention transfer, and it is not authority for the tree. It records nothing in the store, and it changes no mode.
>   - **The residual window (stated, not closed).** Between the path binding and the spawner's own path resolution, the path is re-resolved by the kernel. The store's custody excludes other principals, but not the invoking user's own processes or root (item 5, "Exactly what custody excludes"), so the law claims **no** exclusivity in that window. The binding proves the path named the verified member at the instant of its re-observation. A later substitution needs a same-principal write to a private, write-bit-free, pinned generation, which is an ambient trusted-TCB act (PPBS EE-5b's "not admission-enforced"), not an admitted path. D1a's spawner may narrow the window further by re-observing `(device, inode)` at the executable path immediately before `posix_spawn`; that is D1a's to decide (Q3).

### CI-A3-b: item 4 gains `B_launch`

**Current** (item 4, after the `B_transfer(f)` table and its sentence "The sink commits only when the final length and digest verify.", :199-207): no recipe for a launch member.

**Insertion, after it:**

> - **`B_launch(m)`, one `launch_member` of member `m`** (CI-A3), from the capability's retained index and retained `tree/` handle:
>
>   | Operation | Count | Price |
>   |---|---|---|
>   | lexical resolution: a lookup of each path in the retained index | `h ≤ S + 1` | at most `⌈log₂ n⌉ + 1` comparisons, one edge each (CI-A2-c's price) |
>   | each symlink hop's joined path, an owned temporary dropped before the next lookup | `h − 1` | owned, the joined path's length |
>   | descent along the final row's parent chain, one component at a time, from the retained `tree/` handle | `k(m) − 1` | `desc(len(seg_i))` each |
>   | **file:** the open, with its kind check | 1 | `fopen` |
>   | **file:** read attempts through the retained buffer | `env(len(m))` | `rd` each |
>   | **directory:** the final descent, and its status | 1, 1 | `desc(len(name))`, `st` |
>   | the composed launch path | 1 | owned, `len(storePath) + 1 + 64 + 1 + 4 + 1 + len(m)` bytes |
>   | the path binding's status read | 1 | `st` |
>   | the result record | 1 | one object of `LM` bytes (the record's size, a compile-time property of the code) |
>
>   For `Directory("")`, `tree/` itself, there is no descent: one `st` on the retained handle, and the path is `<storePath>/<closure2-hex>/tree`. `h`, `k(m)` and `len(m)` are the **final** row's; a caller computing the bound in advance uses `S + 1` lookups and the largest joined-path length. The handles opened are dropped at return; the buffer is `B_open`'s. Every row is charged before its operation. An exhausted charge is `Budget`, with no observation or path produced.

### CI-A3-c: item 7's lifetime covers the launch

**Current** (item 7, "Pin acquisition and continuity", the second bullet, :308): "The pin is a shared `flock`, so it survives the fence-to-lease handoff (SL S7: leases follow the fence). The operation holds it through R11 and every later step, until the operation ends or, for a Run, until the Run releases it."

**Replacement:** that sentence, followed by: "**Every spawn of a closure member happens while the operation holds that closure's pin** (CI-A3). The spawner receives a path from `launch_member` only while its `LaunchMember` borrows the pinned capability, and the operation keeps the capability open until the spawned child has settled. A Run that releases its pin after its retention (below) does so only after every child spawned from that closure has settled."

### CI-A3-d: item 5 records the store's absolute location

**Current** (item 5, "Location (LD-CI-7, kept)", :265): "`<installRoot>/components/`, created by installation provisioning as a private `0700` directory. The lifecycle locations owner (`crates/lifecycle/src/locations.rs`) gains it."

**Replacement:** that text, followed by: "**The store keeps the absolute path it was opened at** (CI-A3), as the locations owner gives it: the installation root's admitted absolute path joined with `components`. It is an owned record of its length, made once when the store is opened, and used only to compose launch paths. It confers nothing: every read stays descriptor-relative and no-follow from the retained store directory, and a launch path is used only after `launch_member`'s binding."

### CI-A3-e: item 6's and item 8's typed failures gain `Binding`

**Current** (item 6, "The other typed failures", :293): "`NotInstalled` (no `<closure2-hex>`), `Pin` (r3), `Budget`, `Io{call, errno}`."

**Replacement:** "`NotInstalled` (no `<closure2-hex>`), `Pin` (r3), `Binding` (CI-A3: the composed launch path does not name the verified member), `Budget`, `Io{call, errno}`."

**Current** (item 8, :333): "**`Absent`, `Length`, `Digest`, `Type`, `Mode`, `LinkTarget`, `Extra`, `Association`, `Pin` and `Custody`** are a promised tree's own corruption."

**Replacement:** "**`Absent`, `Length`, `Digest`, `Type`, `Mode`, `LinkTarget`, `Extra`, `Association`, `Pin`, `Custody` and `Binding`** are a promised tree's own corruption." The rest of the bullet is unchanged. So `Binding` routes operational-failed 4, `HOST.IO_FAILURE`, `DELIVERY.CLOSURE_BYTES_CORRUPT` durably, and the same with no detail ephemerally. No code is added. `Io` and `Budget` keep their existing routes (:334).

### CI-A3-f: item 9's units and controls

**Current** (item 9, the CI-3 unit, :340): "**CI-3, the retained-tree capability:** lifecycle. It covers item 6 and item 7's pin. **C2a-3 binds CI-3**; C2a-4's wiring waits for it (`codex-c2a-plan-r2` Q6)."

**Replacement:** that text, followed by: "**CI-3L, the launch member (CI-A3):** lifecycle, after CI-3. It covers CI-A3-a to CI-A3-d. **D4-4 binds CI-3L** (`codex-d4-plan-r1` Q7)."

**Insertion, after CI-T26 (:391-397):**

> - **CI-T27 (CI-A3, the launch member):**
>   - **Resolution:** a root-level file entrypoint; a nested one; an entrypoint that is a symlink row to a file row, and one through two links. The result is the final file row, and the spawned path contains no link. A link chain longer than `S + 1` lookups, and a request resolving to a row of the wrong type, refuse `Association`.
>   - **Observation:** a changed byte refuses `Digest`; a truncated file `Length`; a changed mode `Mode`; a file replaced by a directory `Type`; a removed file `Absent`. Each comes from the retained base, with no multi-component `openat`.
>   - **Binding:** a launch path whose final component is replaced by a symlink to an identical copy, and one whose store path names a different directory, each refuse `Binding`.
>   - **Directory members:** `Directory("")` and a nested `dir` row give `(device, inode)` and a mode check, with no content read.
>   - **Lifetime:** a `LaunchMember` cannot outlive its capability (a compile-fail probe); GC under the fence retains a generation whose capability a test holds across a spawn of its member.
> - **CI-T28 (CI-A3, work):** an independently written enumerator lists every charged call and owned representation of a `launch_member` run from a recorded call log. The run's charges are at most `B_launch(m)`, and every non-zero row appears. A scope one unit short before each row's operation refuses `Budget`, with no observation and no path. An injected I/O failure in the member's read refuses `Io`, not `Digest`.

## Interaction with CI-2/CI-3 (in progress, with CI-A2)

- **Not folded into CI-2/CI-3's review.** CI-2/CI-3's package is one unit with CI-A2, already built in its worktree (`opensip-ci2`: `crates/lifecycle/src/retained_tree.rs`, `installation.rs`). CI-A3 does not change that unit's subject or reset its review. Its code lands as **CI-3L**, a separate unit after CI-2/CI-3 integrate, on their main.
- **CI-3L touches CI-3's files.** It changes `retained_tree.rs` (the operation, `B_launch`, `Binding`) and `installation.rs` (`ComponentStore` records its absolute path, CI-A3-d; `open_in` and `fixture` gain the path). So CI-3L's lane starts only after CI-2/CI-3 are on main, and its integrate script refuses if main changed one of its paths since its lane base.
- **Reused machinery.** CI-3L reuses CI-3's `charged_find` (CI-A2-c), `descend` and `descend_cost`, `open_regular_no_follow` and `read_verified`. It adds no platform primitive: the binding's status read is `st` (P-7's published `status_read_cost`). If P-7's exposure has not landed with CI-2, CI-3L waits for it.
- **The CI fork's in-flight candidate** already partitions `TreeReadFailure` (`retained_tree.rs`:40-65). `Binding` is a new member there, added by CI-3L, so CI-3's own controls are unchanged. `NotInstalled` and `Pin` cannot arise from `launch_member`, since the capability is already open and pinned.
- **If CI-A2 changes in review,** CI-A3's `B_launch` row that cites CI-A2-c's search price is rebased in a new round. No other dependency exists.

## Not claimed

- No spawn.
- No D1a change: whether the spawner re-observes before `posix_spawn` is Q3.
- No D4 code.
- No new public code or route.
- No closure of the same-principal window (CI-A3-a's residual).
- No Linux.
- No qualification.

## Questions for the reviewer

- **Q1.** Is lexical resolution over the TreeCommitment, by the security owner's rule and ending at the final file row, the right entrypoint resolution, so that the spawner never traverses a link?
- **Q2.** Is the path binding sound: one no-follow-final status read of the composed absolute path, compared by `(device, inode)` with the handle, and refusing `Binding`, routed as corruption? Is the residual window honestly stated under item 5's custody limits?
- **Q3.** Should D1a's spawner re-observe `(device, inode)` at the executable path immediately before `posix_spawn`, as a D1a amendment? Or is CI-A3's binding, under the pin, the whole required "recheck binding verification to spawn" (CPC:251)?
- **Q4.** Is a directory member, identity and mode only with no content re-hash, sufficient for a launch spec's directory argument such as Rust3's `--toolchain-root`, given that the capability's open verified the tree and the pin holds it?
- **Q5.** Are `B_launch`'s rows complete and conservative, including the hop temporaries and the full re-hash of a file member at every launch?
- **Q6.** Is CI-3L, a separate unit after CI-2/CI-3 rather than a change to that in-flight unit, the right ordering?
