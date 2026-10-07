# S12 F01 correction, round 18

ACCEPT-DESIGN-UNIT. requiredFindings empty.

Subject manifest `subject.json` is 4578 bytes, sha256 `d9fd0c628ccc9630a3bad15c04cc305f35cc6c6407ae62713c5fbc99e98fd560`. All 25 members match those bytes. Their paths are sorted and unique. This review accepts the law correction only. It accepts no product change, inventory row, or J3b implementation.

`PROPOSAL-r18-S12-F01.md` is 282710 bytes, sha256 `817d7edca75e8a00cb2313b99aa7147e30ee9cb73682af8954b30fb401920cd7`. It keeps the accepted r17 prefix byte for byte: `PROPOSAL-r17-S12.md` is 278697 bytes, sha256 `6b208ccf7d1b0ce5c18ec0329724fbc103de8b18d9abae0b02a6ac0856f397f3`, and the r17 review's `subjectSha256` is that same digest, verdict ACCEPT, requiredFindings empty. The appended correction is 4013 bytes and begins at `## S12 F01 correction, round 18`. X4T r12 is pinned at 79182 bytes, sha256 `cf566db721c0dd3b24aabdbf4613062c59ecbf52d7f64ebed507016f9f9643fb`. `~/Library/Application Support/OpenSIP` is absent. The evidence homes are synthetic scratch captures.

## The two cells

After this successor is accepted and bound, only these existing cells change:

| case | variant | field | r17 | successor |
|---|---|---|---|---|
| F01 | `replay-run-object-missing` | `stateUnchanged` | true | false |
| F01 | `replay-run-descriptor-altered` | `stateUnchanged` | true | false |

Every other field of those rows stays as r17 scores it: `ledgerCarrierUnchanged` true, `ledgerPresent` false, `attemptRows` 0, `sealRows` 0, `carrierAdded` empty, and the same `finalize1` row, delivery phase, remedy, runId, and subject. The other 96 original rows, the four J3b S12 rows, and J3d's later S12-O row stay under their existing law. The correction adds no point, scope, count, order, vocabulary, run-record member, normalization rule, unit selector, or numeric limit. The census prediction stays host 218/271, storage 261/327 after X3c-3, union 323/389. Each old and new row still needs its development check and both exclusive two-target lead repetitions.

The pinned `required-runs.v1.json` is the 98-row file, and both F01 cells there are still `true`. J3b's unaccepted copy appends the four transcribed rows and leaves those 98 rows equal, including both `stateUnchanged` cells. The fixture edit waits until this correction is bound.

## Why the cells move

S12.4's journal account still holds. For these two rows, `prepare_commit` never runs, so no attempt row, SEAL, or ledger is created and no settlement reserve is taken. `refused()` and `finish` append no `REV` or `CLN` because the copy tail is already the candidate child's `REV`. The entry's X3b floor step and `finish`'s end step write the journal floor only when that tail is higher, so they write nothing. `ledgerCarrierUnchanged` stays true.

That account misses SC-TRUST's S4 floor. The finalize child enters through `operation`, which is R12. `operation_handoff::begin` calls `trust_start` at the lease-free point before the journal floor step and before it returns. `trust_start` projects the S4 observation from that read's own opening sample and calls `fenced_operation_read`. On an accepted store, `bootstrapping_first_read` runs `fenced_first_read` and returns that result. The F-absent bootstrap and its confirming admission on the same sample run only when the first admission is `NoAdmittedTimeContext`. The matrix store is already accepted, so this read is a new fenced admission.

X4T r12 item 7 requires a pending S4 change to be published before a decision at that tEval is used, including before a later refusal. `needs_write` admits the publication when the evaluation floor rises, L advances, or the anchor differs. `fenced_first_read` then builds the clock-write successor, publishes it, and confirms `state.v1` before the view returns. X9 r2 item 3's script, as implemented by `scripted_wall`, makes the n-th wall reading of ordinal k equal `E + 3600·k + n`. The pinned epoch is `1791072000` (2026-10-04T00:00:00Z). The candidate child is ordinal 1 and the finalize child is ordinal 2, so every finalize wall second is strictly later than every candidate wall second. The first readings are E+3600 and E+7200, inside the validity window X4T r12 names. The later tEval exceeds the floor the earlier child published, so this read owes a new publication. Replay runs only after `operation` returns and `CommitSession::open` succeeds. The refusal and the journal end step cannot suppress or remove the publication.

X9's normalization is unchanged. `stateUnchanged` is equality of `normalizedSha256` over the logical tree. `trustState` digests the trust files, and `directories` lists the tree. A new publication, records, event, and `state.v1` change those two members, so the digest changes and the cell is false. `ledgerCarrierUnchanged` compares the ledger and carrier apart from that digest, and those stay equal. The false value is that comparison applied to the publication item 7 requires. It is not a value copied off the observed report.

F01's substituted rows do not score `stateUnchanged`. Their scored carrier cell remains the one latched-gate `REV` that S12.4 already names. This correction leaves those cells, and the other 96 original rows, under LD-S12-8.

## Evidence that confirms the derivation

The supplied logs were read. No Cargo, compiler, or test lane was run for this review.

J3b stopped under S12.6 before either lead set. The stop report records 20 completed old-row runs, with the two F01 replay-refused rows failed and the other 18 passed. `old98ExpectedRowsUnchanged` is true. The four transcribed S12 development rows passed: `s12-development-r1.log` is one `x9_6_matrix` test, ok, with seven filtered out. That interrupted set is not qualification. The transcription receipt records qualification false.

The targeted diagnostic reproduces each row's only mismatch: `stateUnchanged` expected `true`, observed `false`. The observed `finalize1` row, delivery phase, remedy, runId, subject, attempt, seal, carrier, ledger, and `ledgerCarrierUnchanged` match the r17 cells.

Each captured before/after pair differs in six raw trust paths: one publication, three records, one event, and `state.v1`. Logical `databases`, `objects`, and `operational` are equal. Logical `directories` and `trustState` differ, and `normalizedSha256` differs. No carrier, witness, ledger, journal, or object path changes.

Census prediction passed for names, counts, and order on both targets. Coverage passed with an empty uncovered set, union 323 and kill set 389. `killedOutsideKillSet` is the two `x3c.object/file-barrier` `#41` points S12.6 already names after X3c-3, so 391 kills are that 389-point set plus those two. `matrixPass` is false because this is not a lead set. The host whole-census JSON differs by fresh ExecutionId payloads and arrival text; the assessment records that the point sequence itself matches.

## Precedence

The appended section supersedes only S12.3's claim that these replay refusals leave the whole post-state unchanged, S12.4's two `stateUnchanged` cells and the "Nothing else is written" / "So" sentence that treats the trust store as untouched, and LD-S12-8's ban on re-transcribing an existing row as applied to those two cells. S12.4's journal-floor, no-ledger, and no-carrier-append reasoning stands. The other 96 original rows keep LD-S12-8. S12.4 and S12.6 still stop J3b on any further contradiction. Keeping the r17 prefix makes that precedence readable.

Replaying before R12 would contradict X5 r4, X7 r7, and J1, and the pinned runner does not do it. Suppressing the pending trust publication would contradict X4T r12 item 7. Dropping `trustState` or publication directories from normalization would weaken the state comparison for every row. Writing any other new expected value, or editing either fixture cell before this correction is bound, would break the stop rule. The evidence reports stay diagnostic.

J3b stays halted until this correction is bound. The lead handles root assent and design verification. No commit or push is part of this review. The record grants no lead set and no product qualification.
