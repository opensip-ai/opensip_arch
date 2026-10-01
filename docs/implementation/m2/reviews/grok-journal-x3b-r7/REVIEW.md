# Law X3b r7 — grant-generation rollover

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `journal-x3b/PROPOSAL.md` is 52076 bytes, sha256 `b9aad8f68fd150ca5245378a7c3925b7f80e8b282fde0a772b35c7d3c948c3c5`, matching `hashes.txt`. Preserved r6 is `PROPOSAL-r6.md`, 25772 bytes, sha256 `4ee7e465e790fa3bc04ddd40c6e07e96e00e08a1487e0f10049b57dec4a72765`, equal to the accepted r6 `subjectSha256`. The diff is five hunks: the r7 header, item 3's last floor-table row, item 4, item 5's `TERMINAL` bullet, and items 5a through 13 with the forbidden substitutes and the not-claimed list. The journal files were read at `9dbefb918aa2fb10848e6203fb0cb79338c7ce2f`.

## What holds

X7 r3 item 6's dependency is defined in the end step. Item 13 runs under the fence that step already holds, on this invocation's one gate admission. `EXCLUSIVE` is `writer.lease` then `readers.lease`, both `LOCK_EX|LOCK_NB`, which is X2 item 7. A busy lock releases anything already taken and returns `Skipped`. The `TERMINAL` is cause `grantGenerationClosure`, through item 5's level-3 then level-4 protocol, and only inside item 5a's window. Opening g+1 writes no carrier row: the witness is `COMMITTED (g+1, 0, null)` under the lease, and the floor `(g+1, 0, null)` is the end step's copy after the lease is released. The crash table matches that order. Item 9 reserves the rollover once, on the attempt ledger X1 item 5 already separates from the gate ledger, before the lease is taken, and an exhausted reserve is a rollover failure that leaves the attempt's outcome as it was.

The `SEAL` ceiling is the right width. A `SEAL` at tail `9007199254740987` takes seq `9007199254740988` and leaves `9007199254740989` and `9007199254740990` for the one `REV` and one `CLN` X3d item 7 appends. The trigger, effective tail open and `t ≥ 9007199254740988`, is exactly `seal_fits` false. Superseding X3d item 3's `≥ 9007199254740990` with that predicate is the threshold that keeps those two ordinary slots. v2 §5.4's close when the tail reaches `9007199254740990` stays the latest close; r7 closes earlier only where no `SEAL` fits, with the same cause `grantGenerationClosure`, and `gj3_append_laws` already admits `TERMINAL` at any seq. The single reserved slot, `TERMINAL` only at seq `9007199254740991`, is what lets a `SEAL` take `9007199254740990` and strand that `REV`.

Item 4a's successor rule matches the frozen `reconcile_observations` at that commit. The function quarantines a generation mismatch, so the caller selects the tail first. A witness that names G+1 is reconciled against the successor's empty tail `(G+1, 0, none)`: `COMMITTED 0` with a null hash is OK, `PENDING 1` is REVERT, and every other state is QUARANTINE. Any other witness is reconciled against the `TERMINAL` row, and there OK or ADVANCE is OPEN, writing only `COMMITTED (G+1, 0, null)`, while REVERT is QUARANTINE because the DDL refuses a row after a `TERMINAL`. The witness and floor decoders admit seq 0 with a null hash. Seq 1 of G+1 chains from `genesis_previous(N, G+1)`, the v2 §5.4 genesis, with N as item 2's key text. The copy tail is `(G+1, 0, null)` only when that witness is `COMMITTED 0`; on OPEN the floor step copies the closing `TERMINAL`. The predecessor check is the gap the DDL does not enforce: `gj3_append_laws` refuses a superseded generation and an append after `TERMINAL`, and it does not require the previous generation to be closed. The crash rows are the next writer's floor step and start, and each one has an item 4a result. Whole-generation `REV` closure is explicitly unclaimed.

Item 13 writes no floor under the lease, waits on no lock, takes no second gate, and takes no fence of its own. The `operationRef` is `op-` plus the lowercase hex of 16 CSPRNG bytes, length 35, drawn once per attempt and required to differ from the released operation's ref. `wallClockData` is one UTC sample `YYYY-MM-DDTHH:MM:SSZ`. Both match `terminal_body` and the carrier CHECK. The r7 rows reuse the busy row, the quarantine row, the invariant row, and `HOST.IO_FAILURE`. No new code, subject, or remedy is introduced.

## RF-1

Item 5a's admission table admits `RA`, `REV`, and `CLN` when the committed tail `t` is `≤ 9007199254740990`. At that tail the next seq is `9007199254740991`.

carrier-format.v3 §5 and `gj3_append_laws` reserve seq `9007199254740991` for `TERMINAL`. X3b-2 at `9dbefb9` refuses a non-`TERMINAL` when `tail.seq >= LAST_ORDINARY_SEQ` (`9007199254740990`), so an ordinary record is admitted only for `t ≤ 9007199254740989`, and the appended seq is at most `9007199254740990`. The same item's `GenerationFull` bullet, and the item 11 test, refuse `RA`, `REV`, and `CLN` at `t = 9007199254740990` on the busy row. That tail has two results, and the admitting result is the one the carrier aborts.

Required: the `RA`, `REV`, and `CLN` row admits them when `t ≤ 9007199254740989`. `GenerationFull` at `t = 9007199254740990` stays the busy row. The `SEAL` ceiling, the `TERMINAL` window, and the trigger stay as written.

## RF-2

Item 13 carries X3d's `{grantGeneration: G, provenTailSeq}`, and the attempt reached rollover because that seq was at least `9007199254740988`. The decision table appends `TERMINAL` whenever the observed open tail is still inside `9007199254740988` through `9007199254740990`. It treats a tail below what the attempt proved as loss only when the tail is below the window.

A restore can leave the committed tail at `9007199254740988` or `9007199254740989` while `provenTailSeq` is `9007199254740990` and the floor is still behind both. Item 3's floor regression does not fire. The in-window row then appends `TERMINAL` over the missing records.

Required: an observed open tail below `provenTailSeq` refuses before any write. The floor being ahead of that tail is floor regression; otherwise it is `uncertainTailLoss`. That includes a tail that is still inside the window. The `TERMINAL` row runs only when the observed tail is in the window and is at least `provenTailSeq`.

## RF-3

Item 8's no-successor row, generation `9223372036854775807`, writes nothing and appends no `TERMINAL`. It rejects appending `TERMINAL`, because the carrier would then have no open generation. Item 4a applies that refusal to OPEN when the last row is already a `TERMINAL` at that generation.

Item 13's table has no row for an open generation at that maximum. When that generation is open and the tail is in the window, the table writes the REVERT or ADVANCE witness and then runs steps 4 to 6. Those steps append the `TERMINAL` before OPEN. OPEN then refuses, and the `TERMINAL` is already durable.

Required: when the open generation is `9223372036854775807`, the observation refuses on item 8's invariant row before any write, and no `TERMINAL` is appended.

## Verdict

REQUIRED-FINDINGS. RF-1, RF-2, and RF-3.
