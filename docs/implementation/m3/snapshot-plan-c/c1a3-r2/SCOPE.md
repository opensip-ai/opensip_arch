# C1a3 r2: sealing the snapshot (M3-C r8 items 1, 4, 5 and 6)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 2.**

## Round 2

Round 1 (`codex-c1a3-r1`, subject `00a182bd…`) returned REQUIRED-FINDINGS. Both findings are accepted and fixed:
- **C1A3-R1-RF-1 (uncharged hex temporaries).** `push_row`, `none_observation` and the VCS digest each called the identity crate's `digest_hex`, which allocates a 64-byte `String`, uncharged. Sealing now writes the hex from a stack `[u8; 64]` (`hex_digits`), directly into the precharged inventory, VCS record and descriptor buffers, and the descriptor takes the VCS digest as that array. `digest_hex` is no longer imported by production code. **The charged terms are unchanged**; sealing simply makes no allocation beyond them. A new control, `sealing_allocates_only_what_it_charges`, checks three things: `hex_digits` equals `digest_hex`; the production source names no allocating conversion (`digest_hex`, `format!`, `to_string`, `String::`, `vec!`, `collect`, `Box::`, `clone()`, `concat`, `join(`, `to_vec`); and each of its five allocation sites follows, as its nearest preceding charge, a charge of its own exact length. Two new mutations (a swapped nibble, and a `digest_hex` temporary reintroduced) must fail it.
- **C1A3-R1-RF-2 (C1A-T6's mixed-error controls).** `walk_refusals_come_before_the_bounds` now goes through the walk-then-seal composition (`over_bound_then_walk`). It preloads a synthetic reached capture over 8 GiB, walks, and seals only on the walk's `Ok`. It covers four cases:
  - the control, with no injection, reaches sealing and refuses `totalBytes`;
  - a later read I/O failure refuses `Read {z.txt}`;
  - a change during a later read (an append before the second read call) refuses `ChangedDuringRead(z.txt)`;
  - a later custody write failure refuses `Custody`.

  In each refusal case, sealing never runs. The no-total source pin and the step-5 bound controls are kept. LD-C1A3-5 is reworded: the report's provenance is a **composition precondition**, not a structural proof (see NBO-1 under *Not delivered*).

The r9 law work (M3-C r9) pins `snapshot_seal.rs` and is re-pinned to this round's file.

It implements C1a3 of the C1a plan: r4 is accepted (Codex `codex-c1a-plan-r4`), amended by r5 and r6, and r6 is accepted (Codex `codex-c1a-plan-r6`). Under r6, C1a3 is **preparatory library work**:
- no `snapshot_profile`, and no production snapshot-ledger claim;
- no production caller (J2b and J2c compose it);
- no census-closure file changed.

**Base:** product main as the subject manifest names, with C1a1 and C1a2 integrated.

## What it changes

| File | Change |
| --- | --- |
| `crates/host/src/snapshot_seal.rs` (new) | **`seal(session, root, report, inputs, registry, work)`, item 6's order:**<br>(1) the walk, which the caller ran: the caller seals only on the walk's `Ok` report, so every walk refusal precedes sealing (a composition precondition: LD-C1A3-5);<br>(2) the read set, empty until C1c (LD-C1A-6);<br>(3) sort and uniqueness: the session's inventory must be strictly ascending by path bytes (a violation is the typed `Internal`); rows, total bytes and the canonical inventory's exact length are counted without allocating; then the **leftover captures** and the **project carrier's join** (LD-C1A3-1);<br>(4) the VCS observation: `kind: none` only for the lending's authenticated `NoRepository` observation with no admitted D15 member, otherwise `SnapshotVcsPending` (LD-C1A-5);<br>(5) the bounds in item 5's order: rows (100,000), the canonical descriptor (4 MiB, `canonical.rs`'s `MAX_BYTES`; its exact length is computed before it is built, so an over-bound descriptor is never built), total bytes (8 GiB, RPP:100), each `SnapshotBound {field, observed, limit}`;<br>(6) `snapshot2` through `IdentityCandidate::from_json(.., IdentityDomain::Snapshot, ..)`, which admits against identity-v3's `$defs/snapshot` and checks the inventory's order.<br>**The encoding.** The canonical inventory and descriptor are written byte for byte as the identity crate's canonical encoder writes them (a test compares them), each charged at its exact length before it is allocated; digest hex is written from a stack array straight into those buffers, so sealing makes no uncharged temporary (r2). `sourceInventoryDigest` is the raw SHA-256 of the canonical inventory, which is **retained in candidate custody** under that digest (item 4). `vcsDigest` is the raw SHA-256 of the canonical `vcs-observation` `{schemaVersion: 2, kind: "none", commitId: null, dirty: false, sourceInventoryDigest}`.<br>**`ProjectCarrierObservation {Absent | Present {sha256}}`**, built from B1's `ResolverInputV1` project carrier (`of`), hashing the captured bytes.<br>**The bound inputs** (`SealInputs`): `projectId` (X2's, or J2c's fresh ephemeral draw), B1's `resolvedConfigDigest`, B2's `scopeDigest`, the carrier observation, and the admitted members. The tracking observation is not an input: it is read from the `SnapshotRoot`'s lending, so no caller can assert it. No operational value enters a field (C1-T23). |
| `crates/host/src/snapshot_seal_tests.rs` (new) | 10 tests (below). |
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
- **LD-C1A3-4. Sealing's working set.** The inventory, the VCS record, the descriptor, the id and a refused leftover's path are charged at their exact lengths before allocation, and sealing allocates nothing else: digest hex is written from a stack array (r2). Identity admission's own allocation is bounded by the 4 MiB descriptor and the schema budget (64 MiB of evaluator work, as B1's configuration admission uses), like every other identity admission.
- **LD-C1A3-5. C1A-T6's controls.** The plan names an over-8-GiB synthetic tree of sparse files. Reading one would still write more than 8 GiB through custody, so the controls are split:
  - the order is the composition's: the caller seals only on the walk's own `Ok` report. `seal` takes the report as a separate argument, and its type (public, `Default`, `Clone`) does not prove that it is this session's successful walk. That is an **explicit composition precondition**, which J2's production composition must bind (NBO-1);
  - the test holds an over-8-GiB inventory in the session, then walks and seals through that composition: a later read I/O failure, a change during a later read and a later custody write failure each refuse with their own refusal, and sealing never runs; with no injection, the same composition reaches step 5 and refuses `totalBytes`;
  - a source pin shows that neither the session nor the walk names the bound, so the walk never stops at it;
  - the 8 GiB bound itself is exercised at step 5 with synthetic reached captures (exactly 8 GiB admits; one byte more refuses).

## The tests

- **The record (C1-T17):** the sealed descriptor equals the identity crate's canonical encoding of the six-member record, built independently; `sourceInventoryDigest` is the canonical inventory's SHA-256, and its custody blob holds those bytes; the VCS record admits as identity-v3's `vcs-observation`; `snapshot2` is identity-v3's snapshot id of the descriptor; the carrier stays in the inventory. The lending's tracking is `NoRepository`.
- **The encoders:** strings with quotes, backslashes, control characters and multibyte text, decimals, and rows, each byte-equal to the canonical encoder's, with their counted lengths.
- **C1-T26, the carrier join:** one case per table row, each change made after X2's capture and before the walk: present and stable admits; absent and stable admits; a changed digest refuses `digest`; removal refuses `present-absent`; creation refuses `absent-present`; replacement by a directory, a symlink or a FIFO refuses `type`; an `ignorePaths` exclusion refuses `excluded`, and the carrier is not inventoried.
- **Leftovers:** a capture under `ignorePaths` refuses `LeftoverCapture`.
- **C1A-T4:** a `NoRepository` root with an admitted member refuses `SnapshotVcsPending`.
- **C1-T18 to C1-T21:** 100,001 rows refuse `rows`, and 100,000 rows pass the row bound (to be refused by the descriptor); a descriptor of exactly 4 MiB admits and 4 MiB + 1 refuses `descriptor`, though its inventory alone fits; exactly 8 GiB admits and one byte more refuses `totalBytes`. Each refusal carries its field, observed value and limit, and nothing is minted, not even the inventory blob.
- **C1A-T6 (LD-C1A3-5):** with an over-8-GiB inventory already held, through the walk-then-seal composition: a later read I/O failure, a `ChangedDuringRead` and a custody write failure each refuse first, and sealing never runs; the uninjected control refuses `totalBytes`; and the walk names no total.
- **The allocation pin (r2, RF-1):** `hex_digits` equals the identity crate's hex; the production source names no allocating conversion; each of the five allocation sites follows its own exact-length charge.
- **C1-T11 (with C1a1):** two trees differing only in a pruned `target/` and unread `node_modules` seal to the same `snapshot2`.
- **C1-T23's source pin:** the builder names no request or execution id, process id, clock, host spelling or environment.

## Checks

Lane r2, `evidence/c1a3-checks-r2/` (the lane of record), on main as the subject names (v216's lock commit), passed every check (`allPassed`):
- **the suites,** at base and candidate, with equal failure sets after isolated reruns:
  - host: 8 failures each side, and 10 new passing tests;
  - security: no new tests. `custody::git_tracking::tests::every_member_refusal_has_its_subject` failed at base only; it passed all six isolated runs, so it is classed as flaky and not as a difference (its record is in the evidence);
- **rustfmt** on the new and base-clean edited files, and warning-denied all-targets Clippy on the two crates;
- **the focused tests:** sealing (10), the session and custody, and the walk and its source;
- **the model's `--check`** (both outputs), and the T2 census `--check` over the lead-readable cache;
- **repository checks:** FW-01, the environment exceptions, the operability source census, the census-closure check (no closure file changed, so the blind receipt stays current) and verify_design;
- **thirteen mutations,** each failing the sealing tests: round 1's eleven, plus r2's two (a hex nibble swapped, and a `digest_hex` temporary reintroduced, which the allocation pin catches).

Round 1's lane (`c1a3-r1/evidence/`) is history.

## Not delivered

- **The read set and the layout** (item 3): C1c.
- **Git and D15 members** (item 4, VCS-1): C1b. C1a3 seals `kind: none` only.
- **The ephemeral route's tracking observation:** J2c.
- **The caps and `snapshot_profile`:** C1a4, gated on M3-C r9.
- **Composition:** J2b and J2c call `seal`, with B1's resolver input and B2's scope descriptor. Codex C1A3-R1-NBO-1 is carried there: the production composition binds the walk's provenance, with a session-bound completion token or a single walk-then-seal helper, and considers freezing the session against later reads.

## Not claimed

- No caller, no ledger profile and no cap.
- No qualification; C1a's completion is not claimed.

## Inventory

New paths: `crates/host/src/snapshot_seal.rs` and `crates/host/src/snapshot_seal_tests.rs`.
