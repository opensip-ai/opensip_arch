Grok review: 458c-a, the read premise receipt, and inventory v77. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-read-premise458ca-r1.

Law: `docs/implementation/m2/read-premise-458c/PROPOSAL.md` r5 (accepted), items 1 to 4 and 10 (458c-a).

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-458ca`, based on 7237f93. Its diff, including new files, is product.diff in your output directory.
- **Arch:** `repository-file-inventory.v77.json`, `read-premise-inventory-v77-subject.json`, and `read-premise-inventory-v77/`, including `evidence/build_v77.py` and `evidence/verify_scratch.py`.

## What it does

The code is in `custody/read_premise.rs`.
- **`ReadPremiseQualification`:** sealed, and only `InitialPlatform` implements it. It lends `is_home_filesystem` and `omission_premise`, with no barrier policy. It is separate from 468b's `DurableBarrierQualification`; both delegate to the same `InitialPlatform` methods.
- **`ReadPremiseReceipt`:**
  - private fields (attempt, actor, core, platform);
  - not Clone, not serializable, with an opaque `Debug`;
  - `qualification()` is its only lending;
  - `recheck(&mut self)` covers the actor, core and platform, mapped through 468c.
- **`produce_read_platform()`:** runs `begin`, `observe_actor`, `produce_initial_core` and `produce_initial_platform`. It takes no command, flag or writer, so no intent can be minted.
- **`produce_on`:** maps refusals through 468c's existing maps, with no new row. A foreign-lineage receipt ends in `Invariant`.
- **Test-only helpers:** `cfg(test)` helpers in trust.
- **Inventory v77:** adds `read_premise.rs` and its tests. The 8 inheritance rows are re-projected.

## Judgment calls: please rule on each

1. **The live dev-build test** uses a test-allocated attempt with the live `observe_actor` and `produce_initial_core`, because 468c's live test already takes the process flag in the same binary. `produce_read_platform` itself is pinned only by signature.
2. **`recheck` on the receipt** is included for 458c-b step 2, a little beyond the listed 458c-a scope. Keep it, or move it to 458c-b?

## Tests and checks

There are 7 tests:
- premise present or absent: absent is admitted, not refused;
- the lent `is_home_filesystem` equals the gate's;
- no effect, and no intent;
- dev build: `NoEmbeddedRelease` before platform runs, and the real OpenSIP stays absent;
- one attempt per process;
- actor, filesystem and budget refusal rows;
- foreign lineage;
- not Clone, and the sealed lending.

Results:
- Workspace: 1106/0, on two runs. Clippy and fmt are clean.
- `check_package_edges --lane host` passes.
- `verify_scratch` passes with v77.

## Decide

- Does it implement 458c r5 items 1 to 4 exactly: the receipt, the sealed lending, the premise scope carried unchanged, the refusal rows, and no intent or effects?
- Can a caller build or widen the qualification?
- Rule on the judgment calls.
- Are v77 and the inheritance right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of read-premise-inventory-v77-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v77, parent (the v76 pin), successorRecord (the pin of read-premise-inventory-v77/successor.json)}.

Write REVIEW.md and review.json. Do not commit.
