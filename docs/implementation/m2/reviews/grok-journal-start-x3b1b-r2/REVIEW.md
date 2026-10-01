# X3b-1b r2 — journal start

Verdict: ACCEPT-UNIT. Inventory v97: ACCEPT.

Worktree `/Users/sb/code/opensip-ai/opensip-x3b1` at `859089a74a6fecf8137471ff49b555e20e1f9887`. `hashes.txt` recomputed 16/16. The OpenSIP support directory is absent. `product.diff` is `git diff HEAD`: 37333 bytes, sha256 `4e39856ab64b58a3130ccb9916d1557d32e0efebf144716320ea6989309687b3`, 4 `diff --git` headers, 690 insertions, 57 deletions. `design-lock.json` at this HEAD selects inventory v94.

Law is accepted X3b r6 items 4 and 5, and accepted X3d r3 item 7. The carrier start, the end step, and `reconcile_after_uncertain` are a macOS child of `carrier_floor` (`#[path = "carrier_start.rs"]`). `lib.rs` does not export them.

## RF-1 closed

On `WitnessProposal::Initialize`, `reconcile_after_uncertain` calls `write_committed_witness` with the classified tail, the same function `carrier_start` uses, then returns `Initialize`. An empty journal's committed tail is `first_generation`, sequence 0, body absent. A fresh carrier's `carrier_format` row requires `first_generation` 1. `witness_bytes` encodes `bodySha256` null and state `COMMITTED`. `Initialize` is its own variant, so `end_step(Uncertain(None))` returns `NotCopied` before the lease probe and before any floor read.

`reconciliation_after_an_uncertain_outcome_copies_only_ok_revert_or_advance` removes the witness on a created carrier, reads the floor, and checks that reconciliation returns `Initialize`, the witness is generation 1, sequence 0, body absent, `COMMITTED`, the end step is `NotCopied`, and the floor bytes are the bytes read before the call. A second reconciliation returns `Copyable(ReconciledTail(CommittedTail::init()))`.

`QUARANTINE` returns `Quarantined` and leaves the witness absent. `Unavailable` and a carrier that classifies as absent return `Err` (`Unreadable`, `TailChanged`) before that write. The floor copy stays off on this end step.

## Judgment calls that still hold

1. The start classifies the carrier once, reads the witness, and confirms that tail against `floor_step_observed` before any write. A mismatch returns `TailChanged` with the witness and the floor unchanged.

2. `TailChanged` takes `LedgerCorrupt`. A missing carrier at start takes that variant and writes nothing.

3. A Certain end whose carrier classifies as absent returns `Quarantine(UncertainTailLoss)` while the probe is still held, before the floor is read or written.

4. The functions take a `CarrierLocation` only. Taking and releasing the fence and the operation lease stays with X3b-3. The end step probes `writer.lease` without waiting, reads the tail it will copy while that probe is held, drops the probe, and then writes the floor. A busy probe is `Skipped`.

5. `carrier_start`, `reconcile_after_uncertain`, and `end_step` are `pub(crate)` inside the child module.

6. The inherited `carrier_floor.rs` sentence still says the carrier start's witness writes, the end step, and the append are later units. The row is equal to v96. The new `carrier_start.rs` row records this unit, and the v97 README defers that inherited sentence to a description-only successor, the same deferral accepted at r1. The `carrier_floor_tests.rs` sentence stays true: the diff is `pub(super)` on the existing fixture.

`reconcile_witness` returns `Initialize` only for an absent witness and sequence 0. `CommittedTail::init` is generation 1, sequence 0, no body.

## Inventory v97

`repository-file-inventory.v97.json` is 340214 bytes, sha256 `5e4269c50e07590c1cc8e56d1cf302f51f227e034f71fb3395f5467a174848a7`. Parent v96 is 337478 bytes, sha256 `e8a868cc9abd2c57ef19d55215b00f121ac8af3b9da1bdff8beaf8ecd78cd4d5`. Successor `journal-start-inventory-v97/successor.json` is 20186 bytes, sha256 `976dc1f03331791cb2a5cd6d069053080a7ef09d280ea8b2f710ec02eab74443`. Subject manifest `journal-start-inventory-v97-subject.json` is 2283 bytes, sha256 `680965fa4067451f948c2c1df76650b362c8514b53b721853dec3f112722a19c`.

Rows 770 to 772. Added exactly `carrier_start.rs` (index 280, composition, `opensip-security`, proposed) and `carrier_start_tests.rs` (index 281, test). Zero inherited row changes. Paths sorted. Packages, dependencies, pending decisions, and schema version unchanged. The standing sentence is this unit's own. The sixteen projection rows stay bound by file path to inventory96. Each `before` equals the v96 description, the candidate description equals that `before`, and both selectors name those indexes.

The `carrier_start.rs` description matches the code: the start writes the witness on REVERT, ADVANCE, and INIT; `reconcile_after_uncertain` writes the witness on those three and yields a copyable tail on OK, REVERT, and ADVANCE, with INIT left non-copyable; the end step runs under the fence with no project lock.

## Replay

Reviewer's own, Rust 1.95.0. `opensip-security` lib `carrier_floor`: 30 passed, 0 failed, 659 filtered out. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed. The cargo target was removed.

## Verdict

ACCEPT-UNIT. Inventory v97 ACCEPT.
