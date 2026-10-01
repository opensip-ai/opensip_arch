# X3b-1b r1 — journal start

Verdict: REQUIRED-FINDINGS. Inventory v92: ACCEPT.

Worktree `/Users/sb/code/opensip-ai/opensip-x3b1` at `7e676a93567bfb5030e01cc11b56de6831f8d19c`. `hashes.txt` recomputed 15/15. The OpenSIP support directory is absent. `product.diff` is `git diff HEAD`: 36664 bytes, sha256 `83a225d6e9ffe6c64e99fb209d644b73b8863c81f9190280aee38ba5019fa232`, 4 `diff --git` headers, 674 insertions, 57 deletions. `design-lock.json` at this HEAD selects inventory v91.

Law is accepted X3b r6 items 4 and 5, and accepted X3d r3 item 7. The carrier start, the end step, and `reconcile_after_uncertain` are a macOS child of `carrier_floor`. `lib.rs` does not export them.

## Judgment calls

1. The start classifies the carrier once, reads the witness, and confirms that tail against `floor_step_observed` before any write. `reconcile_witness` then uses that same tail. A mismatch returns `TailChanged` with the witness and the floor unchanged. Accepted.

2. `TailChanged` takes `LedgerCorrupt`. Item 4 names the confirmation and names no row. The same arm already carries the other structural carrier refusals. A missing carrier at start takes that variant and writes nothing. Accepted.

3. An INIT outcome of `reconcile_after_uncertain` is `Initialize`, which is not `Copyable`. `end_step(Uncertain(None))` returns `NotCopied` and runs no probe and no floor write. The missing witness write is RF-1.

4. A Certain end whose carrier classifies as absent returns `Quarantine(UncertainTailLoss)` while the probe is still held, before the floor is read or written. Accepted.

5. The functions take a `CarrierLocation` only. The module states that taking and releasing the fence and the operation lease belongs to X3b-3. The end step probes `writer.lease` without waiting, reads the tail it will copy while that probe is held, drops the probe, and only then writes the floor. A busy probe is `Skipped`. Accepted.

6. `carrier_start`, `reconcile_after_uncertain`, and `end_step` are `pub(crate)` inside the child module. No crate re-export. Accepted.

7. The inherited `carrier_floor.rs` sentence still says the carrier start's witness writes, the end step, and the append are later units. The start and the end step now live in the child module, so that clause is stale. An additive successor leaves the row equal to v91. The new `carrier_start.rs` row records what this unit does, and the README defers the inherited sentence to a description-only successor. The `carrier_floor_tests.rs` sentence stays true: the diff is `pub(super)` on the existing fixture. Accepted.

`reconcile_witness` and `quarantine_kind` are the floor step's decision moved out unchanged. `floor_step` is `floor_step_observed` with the tail dropped. `CommittedTail::init` is generation 1, sequence 0, no body.

## RF-1

`reconcile_after_uncertain` returns `Initialize` for an empty journal with no witness and writes nothing. `reconciliation_after_an_uncertain_outcome_copies_only_ok_revert_or_advance` asserts the witness stays absent. Item 4's reconciliation writes the witness on REVERT, ADVANCE, and INIT. Item 5 and X3d r3 item 7 step 1 run that reconciliation in this writer while the lease is held. The carrier start already performs that INIT write. This path must too.

The floor copy stays off. INIT is not OK, REVERT, or ADVANCE, so the outcome stays non-copyable and `end_step` copies nothing. QUARANTINE and a failed reconciliation still write nothing and leave the floor untouched.

Required: on `WitnessProposal::Initialize`, write the witness `COMMITTED` at generation 1, sequence 0, `bodySha256` null, by the same file protocol the start uses, then return `Initialize`.

## Inventory v92

`repository-file-inventory.v92.json` is 330904 bytes, sha256 `c95759480bd925487b309dfdd4e64c50540425da1b007d38db3093beb5bca2e0`. Parent v91 is 328245 bytes, sha256 `c36f00e5e72744f56f60ef2cd21a2e6c2b028596463daa43efc94f73583ba1b4`. Successor `journal-start-inventory-v92/successor.json` is 20186 bytes, sha256 `1bee30cbb3ac8326b321f4f20a3b10f08513ca2105420a2a574c91fd427200b3`. Subject manifest `journal-start-inventory-v92-subject.json` is 2070 bytes, sha256 `ecd2b0a52b7b143ecca56983cd74db8ab0a8b294bc0333a82629d31088e32e7a`.

Rows 763 to 765. Added exactly `carrier_start.rs` and `carrier_start_tests.rs`. Zero inherited row changes. Paths sorted. Packages, dependencies, and pending decisions unchanged. The standing sentence is this unit's own. The sixteen projection rows stay bound by file path to inventory91. Each `before` equals the v91 description, and the candidate description equals that `before`.

## Replay

Reviewer's own, Rust 1.95.0. `opensip-security` lib `carrier_floor`: 30 passed, 0 failed, 642 filtered out. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed. The cargo target was removed.

## Verdict

REQUIRED-FINDINGS. Inventory v92 ACCEPT.
