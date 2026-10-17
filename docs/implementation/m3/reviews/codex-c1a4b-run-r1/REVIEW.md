# C1A4-BLIND-RUN-r1 review

**Verdict: ACCEPT-UNIT.** No required findings or non-blocking observations.

Subject manifest: `0f1ad1a777af56504804a5ac938b93a04347ff2c4adf129236101955d3fa5a6f` (7,271 bytes). All 25 members and all six gate pins match their declared lengths and SHA-256 values.

## Authorized run

The pinned gate review is ACCEPT-UNIT with `runAuthorized: true`. The archived run record, stdout/stderr files, driver log and reviewed script support one discovery invocation followed by one companion invocation, each successful with empty stderr. The companion is conditional on discovery succeeding, producing its receipt and emitting no stderr. There is no retry path or second invocation in the recorded execution.

The script checks the pinned post-run checker before proceeding, then checks the executable freeze, detached clean worktree, repository identity, five tools in main and the worktree, five architecture inputs and absence of a companion receipt before removing only the stale discovery receipt. Lane ownership, nice 10, private 0700 TMPDIR and the specified PATH are enforced in the reviewed script; the run record reports the lane and private temporary directory. These historical execution conclusions rely on the pinned execution evidence and lead record; I did not rerun either blind mode.

Live Git queries independently confirm product main and the detached run worktree at `3742822e2823c3a7624aca3fea11220a46cffa16`, architecture at `4088af763254018d6a3e70ef7b95c58b17ae8cc9`, clean product main, and exactly the four expected worktree changes. The gate commit is the sole commit after `b7538549b727e13013f36d3b7c2e2917e767f3f2`, with exactly the gate-map paths and candidate bytes. All four run-map parent/new-path assertions, candidate hashes and archived copies match.

## Receipts and census records

Both receipts have the closed top-level and measured-row shapes, unique matching ids, all ten rows measured, true integrity/population verdicts, integer object/edge/byte per-mille margins, and consistent `passes2x` and `holds (blind census)` states. There are no error or over-item-5 held-out rows.

Discovery's rows are exactly equal to the committed old receipt's. Its only changed bindings are `closure`, `reference` and `tool`: exactly `work_ledger.rs` and `discovery_rule.rs` in the closure, and `tools/contracts/generator-closure.json` in the reference list. The other five bindings remain equal. The companion has exactly the seven expected bindings, including discovery's complete current bindings. Public file pins were independently rehashed against current product/architecture bytes; all five tools and five architecture inputs also match the gate.

The companion caps are exactly 2^21 objects, 2^24 edges and 2^33 bytes. Its minimum held-out margins are 12,020‰ objects, 65,452‰ edges and 144,238‰ bytes, all above 2,000‰. Discovery's minimum margins remain 68,010‰, 38,712‰ and 73,050‰ respectively. These are receipt margins, not disclosed raw costs.

Discovery's census changes only `entries` and `heldOutMargin`; the companion changes only `heldOutEntries` and `heldOutMargin`. Every readable row and workspace row remains unchanged, and both records compose their held-out rows exactly from their respective receipts. Discovery has `failingEntries: []` and `caps: recorded-margin-holds`; the companion has `failing2x.snapshotProfile: []` and `capsStatus: recorded-margin-holds`.

I ran only the two expressly permitted ordinary `--check` commands, using the exact pinned Python interpreter, flags, arguments and run worktree. Both exited 0. Discovery also verified its vectors. These checks recompute the ordinary records and current receipt bindings without opening held-out stores.

The existing readable/workspace rows independently agree with their recorded caps and margin arithmetic: 39 measured rows pass, with minimum margins 3,960‰, 11,274‰ and 39,040‰. Five over-item-5 rows claim no margin and are excluded as the law requires.

## Post-run checks and disclosure

The pinned post-run checker and its archived results agree: eight composed-record Rust tests passed, 21 companion blind controls passed, 25 discovery blind controls passed, and verify_design reports `passed: true` with `productQualification: false`. I inspected these records; I did not execute those tests or the checker.

The independent gate-identity script compares both HEADs to the completed run record's `productBase`, checks detachment, the frozen parent and one-commit distance, and repeats exact gate-map path/hash comparisons. Its archived result passes. Independent live Git/hash queries in this review confirm the same facts. This satisfies C1A4B-R2-NBO-1.

No reviewed receipt or execution evidence discloses held-out tree paths, file names, contents or raw object/edge/byte counts. The held-out outputs stay within ids, verdicts and per-mille margins; the aggregate execution summaries are the gate's reviewed summaries. Public source-binding metadata and lead-readable pricing logs are not held-out content.

## Outcome

The lead may assent and commit exactly the four files in this run's product map. The one inventory successor, v222, must then cover the new companion receipt and the gate's controls under LD-C1A4B-5. Neither action was performed by this review.

C1a plan r6 RF-3's C1a4 blind-validation requirement is satisfied: both receipts are current at the frozen inputs, every T2 entry within item 5 passes at 2×, and the frozen caps stand. The failure branch does not arise. Product integration and inventory binding remain pending; this does not declare all of C1a or product qualification complete. Any later bound-input change, including C1b-0's generator-closure change, makes the affected receipts stale and requires its own correctly composed records.

No repository, worktree or control file was edited. No blind mode, run script, post-run checker, Cargo command or test was executed during this review. Only REVIEW.md and review.json were written in the requested directory.
