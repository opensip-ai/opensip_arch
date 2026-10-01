REVIEWER review: X3b-1b, the journal carrier start, the reconciliation after an uncertain outcome, and the end step, with inventory v92. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. If you build, use a CARGO_TARGET_DIR under it.

Law: X3b r6 item 4 (start and end) and item 5's uncertain-outcome rule, with X3d r3 item 7.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x3b1`, based on 7e676a9 (X3b-1a integrated). Save the diff as product.diff and report its sha256.
- **Arch:** v92 (parent v91), `journal-start-inventory-v92-subject.json` and `journal-start-inventory-v92/`. v92 will be rebuilt on the then-current parent before integration, because X2b-1's v93 lands first.

## What it adds

The new `journal_store/carrier_start.rs` is a child of `carrier_floor.rs`.
- **`carrier_start`** runs under the fence and the lease:
  - classifies the carrier and its N binding;
  - confirms the tail equals the floor step's observed tail, or refuses `TailChanged`;
  - runs `reconcile_witness`: OK writes nothing; REVERT, ADVANCE and INIT write only the witness, by the file protocol; QUARANTINE refuses;
  - never writes the floor.
- **`reconcile_after_uncertain`** runs under the lease. It writes only the witness on REVERT or ADVANCE, and returns `Copyable(ReconciledTail)` only for OK, REVERT or ADVANCE. `ReconciledTail` is opaque.
- **`end_step`** runs under the fence with no project lock:
  - `Uncertain(None)` does nothing;
  - otherwise it probes `writer.lease` without waiting (busy gives Skipped) and fixes the tail while the probe is held;
  - it checks the floor binding, then copies forward only;
  - floor missing gives `floorLost`; floor above the tail gives regression.
- **`carrier_floor.rs`** gains `floor_step_observed`. `reconcile_witness` and `quarantine_kind` are factored out with no behavior change.

## Judgment calls: please rule on each

1. The tail is confirmed before the witness write, from the same single read.
2. `TailChanged` takes `LedgerCorrupt`. The law names no row.
3. An INIT after an uncertain outcome gives no copy.
4. A Certain end with no carrier but a present floor is `uncertainTailLoss`.
5. The lease and fence are the caller's documented preconditions, composed by X3b-3.
6. No crate re-export yet; X3b-3 adds it.
7. The v91 `carrier_floor.rs` description is stale and goes to the D1 description batch.

## Checks

- Carrier tests: 30/30.
- Workspace: 1249/0 on one run. Another run had two failures from known cross-process interference (F3, whose fix is in review). Both tests passed alone.
- Clippy and fmt are clean. `check_package_edges` and verify_scratch (v92) pass.

## Decide

- Does it implement those items exactly?
- Rule on the judgment calls.
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of journal-start-inventory-v92-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v92, parent (the v91 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
