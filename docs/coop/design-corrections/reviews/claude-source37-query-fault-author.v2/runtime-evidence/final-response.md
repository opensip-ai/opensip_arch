RC37-01 and RC37-A1 are corrected in my proposal, and every focused check has finished in the foreground. check-evaluator-faults.v3 is the one failing check, and it already fails the same way on the original overlay. This is coauthor work, not independent acceptance. No pins or planning were rebound, nothing was frozen or committed, and all product gates and recovery cases remain unperformed.

**v1 ended incomplete.** It exited while claiming to wait on two background checker batches that were stopped at teardown, and it wrote no review. I didn't count any v1 result as a pass. v2 copied the v1 trees, checked them against the manifests and v1's edit hashes, and reran everything here. v1 is byte-identical before and after (25,832 files).

**RC37-01.** Before the fix, the four reminted false-result Runs, the structural refusal and four simulated host bugs all came out as `evidence.corrupt`. Every refusal was a class from a separately loaded copy of the identity model. So the query's `isinstance` test never matched, and the `EVIDENCE_UNAVAILABLE` string prefix was what actually routed missing bytes. The fix:
- **Identity model:** a new condition-only `CompleteReplayMismatch`, which carries the exact comparison key but no route or origin. `close_run` converts its replay stack's declared outcomes into its own classes by exact class object, keeping the message and the original error. Anything else passes through unchanged. `restore` maps the mismatch to the existing `RegenerationMismatch`.
- **Replay and composition models:** the comparisons raise that mismatch with unchanged keys.
- **Query model:** it routes by type only.
  - Missing bytes → `evidence.missing`.
  - Replay disagreement → the existing retained-regeneration route (`HOST.IO_FAILURE` / `evidence.regeneration-mismatch`, subject the refused RunId), copied from the identity carrier.
  - Other admission refusals → `evidence.corrupt`.
  - Any other exception → the existing host-invariant route (`SYSTEM.OUTCOME.ILLEGAL_STATE` / `HOST.INVARIANT_VIOLATED`).
  - The exact error text is kept privately and never picks the route; no prefix parsing remains.
- **Query contract §7:** the paragraph that allowed `evidence.corrupt` is replaced. A live evaluator contradicting itself keeps the host-internal route at its own boundary.

Results:
- The query checker has 31 new controls: 162 → 193 checks, 0 failed.
- Structural, missing, replay-mismatch and host-bug cases land on four distinct routes.
- The three maintained RunIds are unchanged.
- The evaluator fault routes and details are identical across frozen37, the original overlay and my edited tree.
- The new condition-only class is refused as an owner carrier, so it can't skip origin assignment.

**RC37-A1.** `ReferenceCallPrecondition` stays the right signal for the reference entry point, where the observation is a call argument. The contract now also says:
- A product host adapter's own invalid observation goes to the host-invariant route when a valid RequestId exists. Without one, the precondition is re-raised.
- A malformed or wrong-Run retained availability record is `evidence.corrupt`.

No new public code was added, and both laws have passing controls.

**Effect of the foundation changes.** They change exception classes, not decisions or messages. One behavior change: `restore` now raises `RegenerationMismatch` for a Run whose replay disagrees, where before a generic refusal escaped. The other 11 affected checkers produce the same output on the original and edited trees, apart from tree names in file paths. That includes check-identity (1596 passed), check-workflow-projection (493 passed), and check-replay, semantic, execution and candidate replay. No registered schema changed.

**New findings:**
- **QF-I1 (existing failure, for root):** check-evaluator-faults.v3 exits 1 on both the original overlay and my edited tree, but passes on frozen37. The root overlay's StepTermination pair law now rejects one mutated test envelope at schema validation, before the parity check the control expects. The checker then aborts before its carrier rows. The bad envelope is still refused, so this breaks the test, not the safety. The checker isn't one of my six files, so I didn't edit it. A probe that runs each of its rows separately shows every other row as expected.
- **QF-I2 (pins, not rebound):** all six files are pinned in the five source-pins files. The three foundation files are newly stale. The three query files were already stale from the root overlay.

**Limitations.** The list of known refusal classes is closed and explicit: a new refusal class would show up as host-invariant until it is added. Atom, enumeration and native refusals weren't individually triggered through `close_run`. Host bugs were simulated with in-process monkeypatches.

The six changed files, hash before → after:

| File | Before | After |
|---|---|---|
| `identity-model.v3.py` | `204e0f00…` | `9376aaae…` |
| `evaluator_replay_model.v3.py` | `59d3fc33…` | `26e88580…` |
| `evaluator_composition_model.v3.py` | `c2e7f58f…` | `cceeb42b…` |
| `query_projection_model.v3.py` | `0d4433ae…` | `bb9de8f7…` |
| `query-projection-contract.v3.md` | `f7b2e7ca…` | `6a504eb5…` |
| `check-query-projection.v3.py` | `cfe85f88…` | `82eddd74…` |

The root successor still has the original bytes for all six, so they don't overlap its integration.

Files are in /private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v2:
- review.md
- review.json (sha `6b235dd9…`; full hashes and all 30 run receipts)
- proposed-edits.diff (sha `8167db3b…`, identical to v1's)
