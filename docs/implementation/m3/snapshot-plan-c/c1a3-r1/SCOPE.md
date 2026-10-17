# C1a3 r1: sealing the snapshot (M3-C r8 items 1, 4, 5 and 6)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements C1a3 of the C1a plan: r4 is accepted (Codex `codex-c1a-plan-r4`), amended by r5 and r6, and r6 is accepted (Codex `codex-c1a-plan-r6`). Under r6, C1a3 is **preparatory library work**:
- no `snapshot_profile`, and no production snapshot-ledger claim;
- no production caller (J2b and J2c compose it);
- no census-closure file changed.

**Base:** product main as the subject manifest names, with C1a1 and C1a2 integrated.

## What it changes

| File | Change |
| --- | --- |
| `crates/host/src/snapshot_seal.rs` (new) | **`seal(session, root, report, inputs, registry, work)`, item 6's order:**<br>(1) the walk, which the caller ran: sealing takes only the walk's own report, so every walk refusal precedes it;<br>(2) the read set, empty until C1c (LD-C1A-6);<br>(3) sort and uniqueness: the session's inventory must be strictly ascending by path bytes (a violation is the typed `Internal`); rows, total bytes and the canonical inventory's exact length are counted without allocating; then the **leftover captures** and the **project carrier's join** (LD-C1A3-1);<br>(4) the VCS observation: `kind: none` only for the lending's authenticated `NoRepository` observation with no admitted D15 member, otherwise `SnapshotVcsPending` (LD-C1A-5);<br>(5) the bounds in item 5's order: rows (100,000), the canonical descriptor (4 MiB, `canonical.rs`'s `MAX_BYTES`; its exact length is computed before it is built, so an over-bound descriptor is never built), total bytes (8 GiB, RPP:100), each `SnapshotBound {field, observed, limit}`;<br>(6) `snapshot2` through `IdentityCandidate::from_json(.., IdentityDomain::Snapshot, ..)`, which admits against identity-v3's `$defs/snapshot` and checks the inventory's order.<br>**The encoding.** The canonical inventory and descriptor are written byte for byte as the identity crate's canonical encoder writes them (a test compares them), each charged at its exact length before it is allocated. `sourceInventoryDigest` is the raw SHA-256 of the canonical inventory, which is **retained in candidate custody** under that digest (item 4). `vcsDigest` is the raw SHA-256 of the canonical `vcs-observation` `{schemaVersion: 2, kind: "none", commitId: null, dirty: false, sourceInventoryDigest}`.<br>**`ProjectCarrierObservation {Absent | Present {sha256}}`**, built from B1's `ResolverInputV1` project carrier (`of`), hashing the captured bytes.<br>**The bound inputs** (`SealInputs`): `projectId` (X2's, or J2c's fresh ephemeral draw), B1's `resolvedConfigDigest`, B2's `scopeDigest`, the carrier observation, and the admitted members. The tracking observation is not an input: it is read from the `SnapshotRoot`'s lending, so no caller can assert it. No operational value enters a field (C1-T23). |
| `crates/host/src/snapshot_seal_tests.rs` (new) | 9 tests (below). |
| `crates/host/src/snapshot.rs` | `CaptureSession::custody_mut`, for the inventory blob; the test module made `pub(crate)` for the sealing tests. |
| `crates/host/src/snapshot_tests.rs` | Its harness helpers made `pub(crate)`, and `insert_reached`, a test-only synthetic reached capture for the bound controls. |
| `crates/host/src/lib.rs` | The module (macOS, `allow(dead_code)`: library only). |
| `crates/security/src/snapshot_source.rs` | **`SnapshotTracking {NoRepository, Repository, Unobserved}`** and `SnapshotRoot::tracking()` (LD-C1A3-2). `from_operation` records the operation's own `member_precondition()`: the `NoRepository` proof over this very retained chain, or none. `from_released_read`, the ephemeral route, records `Unobserved` until J2c brings its observation. |
| `crates/security/src/snapshot_walk.rs` | **`SnapshotWalkReport.carrier: CarrierEntry {Absent, Regular, Directory, Symlink, Special, Excluded}`** and `PROJECT_CARRIER` (LD-C1A3-3): the root listing's `opensip.json` as the walk classified it. The three exclusions (pruned trees, `ignorePaths`, an admitted boundary) are now judged as one predicate, in the same order and with the same charge, before any kind-dependent step; the carrier is classified from that predicate and its observed kind, with no charge. |
| `tools/security/snapshot_ledger_model.py` | The walk's `KIND_FREE_BOUNDARY` anchor re-anchored on the combined exclusion; no charge term changes. |
| `crates/security/src/snapshot_ledger_vectors.json`, `crates/host/src/snapshot_session_vectors.json` | Regenerated: the model pins the edited files whole. No predicted charge changes. |

## Lead decisions

- **LD-C1A3-1. The leftover captures and the carrier join sit in step 3.** Both concern the inventory the walk produced, so they follow the sort and uniqueness check and precede the VCS observation. Item 1's leftover rule refuses when "any resolved input depends on such a capture". Every pre-walk capture is made for a resolved input (B2's and C2's reads are `CaptureSession::capture`'s only use), so every leftover refuses `LeftoverCapture {path}`.
- **LD-C1A3-2. The tracking observation is the lending's.** LD-C1A-5 needs an *authenticated* `NoRepository` observation, so `seal` reads it from the `SnapshotRoot`, which records it from the operation's own proof. The ephemeral route has no such observation yet, so it seals nothing (`VcsPending`) until J2c.
- **LD-C1A3-3. The walk reports the carrier entry.** The join needs to know whether the root listing held `opensip.json` and how it classified it. The inventory alone cannot say so for a directory, a link, a special file or an excluded entry. The report says it, at no charge.
- **LD-C1A3-4. Sealing's working set.** The inventory, the VCS record, the descriptor and the id are charged at their exact lengths before allocation. Identity admission's own allocation is bounded by the 4 MiB descriptor and the schema budget (64 MiB of evaluator work, as B1's configuration admission uses), like every other identity admission.
- **LD-C1A3-5. C1A-T6's controls.** The plan names an over-8-GiB synthetic tree of sparse files. Reading one would still write more than 8 GiB through custody, so the controls are split:
  - the order is structural: sealing takes only the walk's own `Ok` report, so a later read failure, change or custody failure refuses before any bound;
  - the test holds an over-8-GiB inventory in the session and shows a later read failure refusing first;
  - a source pin shows that neither the session nor the walk names the bound, so the walk never stops at it;
  - the 8 GiB bound itself is exercised at step 5 with synthetic reached captures (exactly 8 GiB admits; one byte more refuses).

## The tests

- **The record (C1-T17):** the sealed descriptor equals the identity crate's canonical encoding of the six-member record, built independently; `sourceInventoryDigest` is the canonical inventory's SHA-256, and its custody blob holds those bytes; the VCS record admits as identity-v3's `vcs-observation`; `snapshot2` is identity-v3's snapshot id of the descriptor; the carrier stays in the inventory. The lending's tracking is `NoRepository`.
- **The encoders:** strings with quotes, backslashes, control characters and multibyte text, decimals, and rows, each byte-equal to the canonical encoder's, with their counted lengths.
- **C1-T26, the carrier join:** one case per table row, each change made after X2's capture and before the walk: present and stable admits; absent and stable admits; a changed digest refuses `digest`; removal refuses `present-absent`; creation refuses `absent-present`; replacement by a directory, a symlink or a FIFO refuses `type`; an `ignorePaths` exclusion refuses `excluded`, and the carrier is not inventoried.
- **Leftovers:** a capture under `ignorePaths` refuses `LeftoverCapture`.
- **C1A-T4:** a `NoRepository` root with an admitted member refuses `SnapshotVcsPending`.
- **C1-T18 to C1-T21:** 100,001 rows refuse `rows`, and 100,000 rows pass the row bound (to be refused by the descriptor); a descriptor of exactly 4 MiB admits and 4 MiB + 1 refuses `descriptor`, though its inventory alone fits; exactly 8 GiB admits and one byte more refuses `totalBytes`. Each refusal carries its field, observed value and limit, and nothing is minted, not even the inventory blob.
- **C1A-T6 (LD-C1A3-5):** a later read failure refuses before the bounds, with an over-8-GiB inventory already held; and the walk names no total.
- **C1-T11 (with C1a1):** two trees differing only in a pruned `target/` and unread `node_modules` seal to the same `snapshot2`.
- **C1-T23's source pin:** the builder names no request or execution id, process id, clock, host spelling or environment.

## Checks

Lane r1, attempt 2, `evidence/c1a3-checks-r1/` (the lane of record), on main as the subject names (v216's lock commit, lock-only after the attempt-1 base):
- **Attempt 1** (`evidence/c1a3-checks-r1-attempt1/`) passed every check and all eleven mutations except the operability source census: its mint audit counted three `usize::from(..)` calls in `snapshot_seal.rs`'s encoders, which the audited exceptions do not list. They are now `as usize` casts of a `bool` and two nibbles, with no behaviour change.

The checks:
- **the suites,** at base and candidate, with equal failure sets (isolated reruns for any differing test): host (9 new passing tests) and security (none new);
- **rustfmt** on the new and base-clean edited files, and warning-denied all-targets Clippy on the two crates;
- **the focused tests:** sealing, the session and custody, and the walk and its source;
- **the model's `--check`** (both outputs), and the T2 census `--check` over the lead-readable cache;
- **repository checks:** FW-01, the environment exceptions, the operability source census, the census-closure check (no closure file changed, so the blind receipt stays current) and verify_design;
- **eleven mutations,** each failing the sealing tests: the carrier digest unchecked; an excluded carrier admitted; an absent-then-present carrier admitted; leftovers ignored; the members ignored; the row bound off by one; the descriptor bound unchecked; the total bound refusing at the bound; the inventory not retained; the walk's carrier unclassified; and the tracking not the lending's.

## Not delivered

- **The read set and the layout** (item 3): C1c.
- **Git and D15 members** (item 4, VCS-1): C1b. C1a3 seals `kind: none` only.
- **The ephemeral route's tracking observation:** J2c.
- **The caps and `snapshot_profile`:** C1a4, gated on M3-C r9.
- **Composition:** J2b and J2c call `seal`, with B1's resolver input and B2's scope descriptor.

## Not claimed

- No caller, no ledger profile and no cap.
- No qualification; C1a's completion is not claimed.

## Inventory

New paths: `crates/host/src/snapshot_seal.rs` and `crates/host/src/snapshot_seal_tests.rs`.
