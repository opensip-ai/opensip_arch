# CI-3L r1: the launch member, a pinned entrypoint recheck (law CI r5 with amendment CI-A3)

**Unreviewed candidate, 2026-10-17. It needs Codex review.** It implements unit CI-3L, the launch member: amendment CI-A3 r4's CI-A3-a to CI-A3-f. The law is "component release installation and tree custody" (`../PROPOSAL.md`: r5 under its acceptance note, with CI-A1, CI-A2 and CI-A3), and CI-A3 r4 (`../CI-A3-r4.md`) was accepted by `codex-ci-a3-r4` with no findings. **D4-4 binds CI-3L** (`codex-d4-plan-r1` Q7; `codex-d4-plan-r2` NBO-1). It follows CI-2 + CI-3 (accepted in `codex-ci-2-r2`, integrated at `d113fa7`) and changes their files. CI-3L proposes no law amendment.

**Product base:** main at the lane's start, as `source.json` and `checks.json` record it (product `d113fa7` when drafted). **Worktree:** `/Users/sb/code/opensip-ai/opensip-ci3l`. **Changed:** see `product-map.json`. No new path.

## Self-review (the lead's pre-submission checklist, `/tmp/opensip-implementation/PRE-SUBMISSION-CHECKLIST.md`)

1. **Charge before work, and prove the order.**
   - **The order oracle.** `ci_t28_a_scope_one_unit_short_before_each_actual_charge_refuses_budget_there` computes CI-A3-b's rows in execution order, independently, for a file reached through two hops, a one-chunk file, a nested directory and `tree/` itself. For each row it runs the launch on a ledger one unit short of that row. Each run must refuse `Budget` with the ledger's `used` equal to the prefix before the row exactly, so nothing charged past the stop and nothing made before its charge. The binding's `lstat` must have run only when the stop is the result record. Moving any charge relative to its operation changes some prefix.
   - **Source-order guards.**
     - `ci_t28_charges_precede_their_operations_in_source_order` covers four orderings: the kind check before resolution, each hop temporary's charge before its allocation, the launch-path buffer's charge before its allocation, and the result record's charge before its construction.
     - CI-2's funded-allocation guard gains this unit's three allocation sites (the store path, the hop temporary and the launch-path buffer), each immediately preceded by its funding charge. Its construct counts are updated, and it now counts `String::with_capacity(`.
     - Platform's `every_primitive_charges_before_its_native_call` gains `path_status_no_follow` and `directory_identity`.
   - **Copies.** The basename's NUL-terminated spelling is `open_regular_no_follow`'s stack copy (CI-A2-h; no allocation, no charge). `path_status_no_follow` borrows the caller's `&CStr` and copies nothing. Platform's counting allocator shows both new primitives allocate nothing on success and on an unfunded refusal.
   - **Mutations moving work ahead of its charge:** `hop-allocated-before-charge`, `result-charged-before-binding` and `lstat-before-charge`.
   - **Not priced, as before:** in-memory checks against an already funded status read (kind, mode, length, `(device, inode)`), and the SHA-256 state. The `CStr` terminator scan over the composed buffer is also an in-memory check, like `StackName`'s NUL scan.
2. **Exact charges vs bounds (E ≤ B ≤ B̂).**
   - `check_work` runs each request on a fresh scope. It requires the actual charge to equal `E_launch` exactly, enumerated independently:
     - lookups by the test's own segment-list order and binary search;
     - read attempts as `⌈c / 64 KiB⌉ + 1`, also counted at the read seam;
     - each hop temporary, descent, open, status read, the `P + 1` buffer and `LM`, each computed from the TreeCommitment and the store path.
   - It then checks `E ≤ B` and `B ≤ B̂` separately. `B` replaces each `s_j` by `⌈log₂ n⌉ + 1` and the read attempts by `env(c)`. `B̂` is enumerated independently and must also equal the module's `launch_pre_bound`.
   - The shapes are:
     - an empty file, a one-chunk file, a 300,000-byte file under a short path, and a zero-length file under a 76-byte path;
     - a member reached through two hops (joined lengths 8 and 14);
     - nested directories and `Directory("")`;
     - a miss, and the no-`dir` tree refusing at the kind check after one edge;
     - lookups matching at several search depths (the test asserts at least three distinct depths).
   - Nothing is precharged. The mutations `reads-precharged` and `store-path-charged-per-launch` are caught.
3. **System-call conventions.** `lstat` and `fstat` return 0 or −1. `errno` is read with `last_os_error()` only on −1, immediately after the call, and nothing is called in between. `ENOENT` is `Absent` and `ENOTDIR` is `NotDirectory`; anything else is `Io` with its errno.
4. **Pinned-source equality.** No table is taken from a schema or generated source. `P-7`'s price is the published `status_read_cost()`, whose expression CI-2's source pin already checks against the filesystem's.
5. **Immutable context pins.** The law is the accepted `CI-A3-r4.md`, with its review subject pinned in `source.json`. The base product files are main's accepted CI-2/CI-3 bytes, and their parent pins are in `product-map.json`.
6. **Time and measurement.** No duration is reported.
7. **Failure latching.**
   - Every failure of `launch_member`, `Budget` included, latches the capability, and `Binding` joins the latched causes.
   - A later `launch_member` or `transfer`, on any scope, refuses with the latched cause before any charge or observation. A latched `Budget` gives `Budget(Closed)`.
   - `ci_t27_every_failure_latches_across_launch_and_transfer` covers three cases:
     - a launch after a failed transfer;
     - a transfer after a failed launch;
     - a launch exhausted on one scope, then a launch and a transfer on a fresh funded scope, each refusing `Budget(Closed)` with zero charge and no read or `lstat`.
   - Mutations: `launch-latch-skipped`, `budget-not-latched`.
8. **Disclosure.** See §6, "Not exercised".
9. **Mutations.** 19, each required to fail a test and not a compile (§6).

## Carried: CI2-R2-NBO-1's qualification (from the `codex-ci-2-r2` assent)

The allocation-free statement covers **names, paths and link targets**. Every native spelling a primitive copies goes into `StackName`'s fixed stack buffer. `path_status_no_follow` copies nothing, and the launch path is an owned heap buffer charged at `P + 1`.

**Error carriers are a separate convention.** After a refusal, an error value may allocate. Examples are `invalid_input` and `supported_io`'s message-carrying `io::Error`s, and `io_failure`'s formatted carrier in `retained_tree.rs`. Such a value funds no admitted work and is not an owned record.

**What the controls cover.** The counting-allocator controls cover successful name-bearing calls and the budget and over-capacity refusals they name. They do not cover every error path, and this SCOPE claims no more than that. The next CI law note states the same qualification (lead decision; `codex-ci-2-r2` NBO-1).

## 1. What changes

- **`crates/platform/src/component_tree.rs`** (the platform owner's; CI-A3's NBO-1 primitives):
  - `path_status_no_follow(&CStr, work) -> Result<PathStatus, WorkFailure<PathStatusError>>`: one `lstat`, charged `status_read_cost()` first.
  - `directory_identity(&RetainedDirectory, work) -> Result<PathStatus, WorkFailure<io::Error>>`: one `fstat`, charged the same.
  - `PathStatus {kind, mode, device, inode}`; `PathStatusError {Absent, NotDirectory, Io}`.
  - Off macOS both refuse `Unsupported` (as `Io`) before charging, as their siblings do.
- **`crates/lifecycle/src/installation.rs`:**
  - `ComponentStore` keeps its absolute path (CI-A3-d). `open_in(install_root, install_root_path, uid, work)` joins the admitted root's absolute path with `components`. `fixture(directory, path, uid, work)` takes the store's own path. Each charges `{objects 1, bytes L}` before the copy and refuses a relative or NUL-bearing spelling before any charge. Both now return `Result<Self, WorkFailure<io::Error>>`.
  - `Tree` gains `links` (`S`) and `entrypoint` (the selected row's `platforms[].entrypoint`).
  - `read_verified` gains a test-only `"read"` seam.
- **`crates/lifecycle/src/retained_tree.rs`** (CI-A3-a, -b, -e):
  - `MemberRequest::{Entrypoint, File(path), Directory(path)}`.
  - `RetainedTree::launch_member(&mut self, request, work) -> Result<LaunchMember<'_>, TreeReadFailure>`.
  - `LaunchMember` exposes `path()`, `device()`, `inode()`, `sha256()` and `row()`.
  - `RetainedTree::launch_pre_bound(request) -> Option<WorkCost>` returns `B̂_launch`.
  - `TreeReadFailure::Binding`, and `Latched::Binding`.
  - The capability keeps the generation's name for the launch path.
- **Tests:**
  - `retained_tree_tests.rs`: CI-T27, CI-T28 and CI-A3-d;
  - `installation_tests.rs`: the fixture store's new constructor call, and the funded-allocation guard's new sites;
  - `component_tree_tests.rs`: the two primitives.

## 2. Lead decisions

None new. CI-A3 r4 is applied as accepted.

## 3. Implementation decisions (ID-CI3L-n)

1. **`B̂_launch` always uses the maxima.** CI-A3-b allows the named row's own values "when the request names a row directly and no hop is possible". Using the maxima over the requested kind's rows is never smaller, so `launch_pre_bound` depends only on the request's kind (and `""`). The control checks that `B̂` equals an independent enumeration of this choice.
2. **Hop temporaries.** Each joined path is charged `{objects 1, bytes q_i}` immediately before its allocation and dropped right after the lookup it funds, so at most one is live.
3. **The owned-record price.** The store path, each hop temporary and the launch-path buffer are charged as CI-A3's table gives them, `{objects 1, bytes x}`. That is not `owned_record(x)`, which adds the custody walk's record overhead, because CI-A3-b's rows are exact and `E_launch` must equal the actual charges.
4. **The store path's spelling.** `open_in` joins with one `/` unless the root already ends with one. The path is never normalized: the binding, not the spelling, establishes what the path names. A store path naming another directory refuses `Binding` (CI-T27).
5. **The borrow.** `launch_inner` returns a `LaunchMember<'static>` so that the latch can be written on failure. `launch_member`'s signature then ties the result to `&mut self`, so the result cannot outlive the capability. The `compile_fail,E0505` doctest on `LaunchMember` is the lifetime probe, with a passing twin.
6. **Routes the law leaves implicit.**
   - `TreeOpenError::Name` maps to `Association` (CI-A3's Interaction).
   - A NUL found in the composed buffer is `Binding`. It is unreachable, since the store path is refused with a NUL at opening and committed paths hold none.
   - A missing `entrypoint` maps to `Association`.
   - A directory member's mode is `installed_mode(row)` (`0500`), and `tree/`'s is `0500` (LD-CI-10).
7. **Test seams.** Both are compiled only into the crate's tests.
   - `"read"` sits before each verified read attempt.
   - `"lstat"` sits after the real observation, and an injected error replaces its result. It maps `NotFound` to `Absent`, `NotADirectory`/`ENOTDIR` to `NotDirectory`, and anything else to `Io`.

## 4. Interfaces

- **`launch_member(request, work)`.** The caller funds it on its own scope, optionally in advance from `launch_pre_bound(request)`. On success it returns the bound launch path, which names no link at its final component, together with `(device, inode)`, the file's SHA-256 and the row. On failure it returns one of `Association`, `Absent`, `Type`, `Mode`, `Length`, `Digest`, `Binding`, `Budget` or `Io {call, error}`. `NotInstalled`, `Pin`, `Custody`, `Extra` and `LinkTarget` cannot arise from it.
- **D4-4's `ClosureRecheck`** needs `{member, device, inode, sha256}`. It takes `device` and `inode` from the result, `sha256` as hex from `sha256()`, and the path from `path()`. The member name is D4's.

## 5. Census and receipts

No census-bound file changes. The changed files are in neither receipt's bound set. The lane's `census-closure-unchanged` and `receipt-inputs-unchanged` checks confirm it, with the receipt files byte-equal to base.

## 6. Controls

- **CI-T27 (`retained_tree_tests.rs`):**
  - **Resolution.**
    - Root-level and nested entrypoints.
    - Installed link chains, one link (`latest` → `bin/entry`) and two (`again` → `latest` → `bin/entry`), requested as `File` members, which follow links by the same rule. Each result is the final file row, with no link at any component below the store.
    - An `Entrypoint` that is a two-link chain, over a hand-built TreeCommitment: it resolves to the file row with two one-byte hop temporaries. An installed fixture can't carry one. A validated toolchain's entrypoint must name its file row directly (`component_manifest.rs`'s entry check), and C2a-1's candidate refuses the analyzer variant of the fixture body (`Protocol { key: Unsupported, origin: AuthenticatedReleaseDeclaration }`).
    - Over a hand-built TreeCommitment (unreachable through validation): a two-link cycle refuses `Association` after exactly `S + 1 = 3` lookups and three one-byte hop temporaries.
    - Wrong-kind and missing requests refuse `Association`.
  - **Observation from the retained base.** A changed byte, a truncation, a changed mode, a file replaced by a directory and a removal refuse `Digest`, `Length`, `Mode`, `Type` and `Absent`, each with no binding read. A source pin over the launch code forbids every path-based filesystem call.
  - **Binding.** Each of these refuses `Binding`:
    - the final component replaced by a symlink to an identical copy, by moving `tree/` aside under the retained handles;
    - an identical regular copy at the spelling;
    - a store path naming an identical copy elsewhere;
    - a store path naming nothing (`ENOENT`);
    - a store path naming a regular file (`ENOTDIR`).
  - **Directory members.** `Directory("")`, `Directory("a/b/c")` and `Directory("lib")` give the spelled path's `(device, inode)` and read no content. A changed mode refuses `Mode`, and for `tree/` it is `Mode { row: None }`.
  - **Lifetime.**
    - The `compile_fail,E0505` doctest (lane row `lifetime-doctest`).
    - GC's exclusive probe is busy before and after a spawn of the member while the capability lives, and free once it drops.
  - **Latching:** as listed in the Self-review, item 7.
- **CI-T28:** exact work and bounds over the shapes (Self-review, item 2); the kind check; exhaustion before each actual charge (Self-review, item 1); and the partition:
  - an injected read failure is `Io { call: "read" }`, not `Digest`;
  - an injected native error from the binding is `Io { call: "lstat" }`;
  - `NotFound` and `NotADirectory` are `Binding`;
  - real `ENOENT` and `ENOTDIR` are covered under Binding above.
- **CI-A3-d:** `open_in` records `<root>/components` and charges exactly `{1, 0, L}`. A relative spelling refuses with no charge.
- **Platform:** both primitives are no-follow, charged first, partition their errors, and allocate nothing.
- **Mutations (19).** Each must fail its crate's focused tests and not a compile:
  - lifecycle:
    - kind-check and lookup rules: `kind-check-uncharged`, `kind-check-skipped`, `lookup-bound-loosened`;
    - work and its charges: `hop-uncharged`, `hop-allocated-before-charge`, `reads-precharged`, `store-path-charged-per-launch`, `store-path-uncharged-at-open`, `result-charged-before-binding`, `pre-bound-hops-dropped`;
    - binding and the partition: `binding-identity-unchecked`, `lstat-io-as-binding`, `absent-path-as-io`, `directory-mode-unchecked`;
    - latching: `launch-latch-skipped`, `budget-not-latched`;
  - platform: `lstat-before-charge`, `lstat-follows-final`, `directory-identity-uncharged`.
- **Not exercised here, by design:**
  - an end-to-end spawn through D1a's `VerifiedLaunch` (D4-4's);
  - an installed `Entrypoint` that is a symlink chain (no admitted fixture carries one; resolved over a hand-built TreeCommitment instead);
  - the residual same-principal window CI-A3-a discloses, which is claimed closed by nothing;
  - a real `EIO` from `lstat` (injected by seam);
  - a basename beyond `NAME_CAPACITY`, which no committed path can reach (CI-T5 caps paths at 100 bytes);
  - off-macOS refusals, since the lifecycle modules are macOS-only;
  - CI-T11's signed half, which still waits for C2a-2's profile-1 fixtures.

## 6b. The lane

`evidence/ci3l-r1-checks/` (`run_ci3l_checks.py`, adapted from CI-2 r2's): one lane hold, nice 10, a private 0700 TMPDIR, and the worktree follows main under the lock when main changed no candidate path. **Not yet run.**

## 7. Not delivered

- D4-4's session factory and its `VerifiedLaunch` construction.
- CI-4's command and terminations, including `Binding`'s route into CI-T16 (CI-A3-e: the corruption row).
- X-CI-1-a's sourced profile.
