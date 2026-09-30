Grok review: 458c-b1, the observation session, and inventory v78. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-read-observation458cb-r1.

Law: `docs/implementation/m2/read-premise-458c/PROPOSAL.md` r5 (accepted), items 5, 6, 7 (non-doctor part) and 11. Consumer migration (item 8) is split out as 458c-b2 and is not in this subject.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-458cb`, based on 42ffa91. Its diff is product.diff in your output directory.
- **Arch:** `repository-file-inventory.v78.json`, `read-observation-inventory-v78-subject.json`, and `read-observation-inventory-v78/`.

## What it does

- **Session.** `custody/installation_session.rs`:
  - `ObservationSession::begin()` allows one per process, with a ledger at the owner's caps.
  - `observe(&mut self, &mut ReadPremiseReceipt)` latches on every outcome.
- **Shared step 0 and step 1.** They are shared with the write gate by refactoring `installation_admission.rs` into `ChainPolicy`, `walk_chain`, `open_fence` and `recheck_chain(.., files)`. The gate's 11 tests pass unchanged. One unreachable branch now returns `Latched` instead of `Absent`.
- **Positive absence.** `Walked::Absent(Suffix)` is returned only for `MissingAncestor`, `FinalNameAbsent` or `ENOENT` on the no-follow open of I.
- **Wait.**
  - 201 × `LOCK_COST` is reserved in one effect.
  - The new `FileLock::try_acquire_retaining` returns the same descriptor on busy, so there is no reopen.
  - Attempts are paced at 25 ms through an injectable `WaitClock`, stopping at 5 s or 201 attempts.
  - `Err` goes to host I/O, and running out goes to Busy.
- **Step 2.** The receipt's rechecks (`ReadPremiseReceipt::split`), then `recheck_chain` with the fence.
- **Step 3.**
  - The fixed members are charged up front, and each node before its own read.
  - Missing, undecodable or misbound members are findings.
  - Open, custody and read failures are kept as values (the new `read_bounded_observed`), so step 4 still runs.
- **Step 4.** `recheck_chain` over every captured file by identity, then the receipt's rechecks. If both a read and the recheck fail, the earlier failure is reported.
- **Result.** `InstallationObservation` offers `findings`, `is_complete`, `complete` (the incomplete row for non-doctor callers) and `release`.
- **Mapping.** `session_refusal` maps `Absent` to `NotInitialized` and `Gate(g)` to exactly 468c's `gate_refusal(g)`.
- **New platform primitives.** `try_acquire_retaining` and `read_bounded_observed`. `try_acquire` delegates to the first and keeps its behavior.

## Judgment calls: please rule on each, against the law

1. **The b1/b2 split.**
2. **ACL-capture errors latch immediately.** A native ACL-capture error in step 3 latches the ledger at once, so step 4 cannot run after it, because `capture_descriptor_acl_accounted` has no non-latching form. Law item 5 step 4 says the recheck also runs after any read failure. Is this a violation that needs a non-latching capture? Or is a latched-and-refused session an acceptable reading, since no bytes are admitted?
3. **Clock failure.** A failed clock sample during the wait goes to host I/O.
4. **Oversized members.** A member over its read cap is a failure (the incomplete row), not a doctor finding. For doctor (458c-c, item 12), is an oversized member a structural defect that must be a finding?
5. **Member order.** Fence, registry, pair, marker, state, then nodes.
6. **Stale description.** The inherited description of `read_premise.rs` ("no read path uses it yet") is stale. The plan is a later contract-successor override. Is that acceptable?
7. **Row type.** `GateRefusal` is reused as the session's row type.

## Tests and checks

There are 13 session tests: the success path, positive absence per suffix versus a file, symlink or custody failure, a missing H, the busy wait end to end, busy then free, `Err` in the wait, the reservation making budget unreachable mid-wait, an owner, mode or link change before step 4, an incomplete I, and a deep home.

Results:
- Gate: 11/11, unchanged.
- Workspace: 1119/0, on two runs. Clippy and fmt are clean.
- `check_package_edges --lane host` passes.
- `verify_scratch` passes with v78.

## Decide

- Does it implement those items exactly, and is the gate's behavior preserved?
- Rule on the judgment calls.
- Are v78 and the inheritance right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of read-observation-inventory-v78-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v78, parent (the v77 pin), successorRecord (the pin of read-observation-inventory-v78/successor.json)}.

Write REVIEW.md and review.json. Do not commit.
