# J3b cancellation and finalization r1

ACCEPT-UNIT. requiredFindings empty. inventoryCandidateAssessment ACCEPT. matrixPass true. productQualification false.

Subject manifest `docs/implementation/m2/j3b-inventory-v167-subject.json` is 16398 bytes, sha256 `7ea2d3026615ee406c42a41b9fe43b575e81a233a9713b70d0ecff0a13d141fb`. All 74 members match the stage bytes. Their paths are sorted and unique. The evidence tar was streamed and not extracted: 1028 file members, no missing or extra names, and every member hash matches `matrix-evidence-members.json`.

## Commit and trees

Candidate HEAD `43d89894095537b33ffa7ea0ddf62c76eb81c71d` is that commit and its worktree is clean. Against product base `26ee168adc0676f6c3b9a05f462ef815ff009cfc` the commit changes 22 paths and adds 7. Nothing is removed. The delta is exactly the 29 paths in `source.json`. Stage copies, the candidate worktree, and `git show` of the commit agree on those bytes.

Main product HEAD is that base and its porcelain is empty. Architecture HEAD is `5e238cecc5aa41f7be4549447ab79c035ec5cb0b`, tracked-clean, with the existing untracked drafts left untouched. `~/Library/Application Support/OpenSIP` is absent. No scratch database and no private 413 fixture was read.

`qualification-input.json` records the explicit owner authorization, "User: this is okay, in reply to isolated temporary qualification commit explanation", `pushed: false`, and the same two bases. Commit `fe428199184fbf0b0d50be4cd1ccaa9e8826c603` stays the refused trailing-LF attempt. It is not this qualification. The current `qualification.json` is the run record used below. Historical source snapshots predate it.

The ten authority pins match the architecture base, including S12 F01 r2 `PROPOSAL-r18-S12-F01.md` at 283040 / `a7c09266e78fcbfb7cd0c65d057252de2772b7cc95cf7489411b5d6c4bbb4803` and its review at 159 / `cd1700d6a3ed67b192b793bed375815a528e0c3ff2bd4ab75f3fd91e54a5a92a`. Those accepted units stay closed.

## Latch, gate, and window

`CancellationLatch` is a security-owned tuple around the operation's stop handle. Its field is private. `take_cancellation_latch` returns the token once and then `None`. `latch` consumes the token. The six refusal cases reject `Clone`, `Default`, a literal, reuse after `latch`, and serde serialize and deserialize, under the existing `x8_misuse` harness. The macOS export sits beside the other session exports. `LatchOutcome` and `D9Signal` are the separate security exports this unit was allowed to add.

The gate word is four bits: `ADMITTED` 1, `LATCHED` 2, `WINDOW_OPEN` 4, `WINDOW_CLOSED` 8. `admit` and `cancel` are strong `compare_exchange` loops. Each stores `word | bit` and retries on the observed word. Bits are only set, so a conflicting update is finite. `open_window` and `close_window` are `fetch_or` and cannot clear a state bit. `cancel` returns `OutsideWindow` when the window is closed or was never opened, `AlreadyStopped` when `LATCHED` is already set, and otherwise `BeforeAdmission` or `AfterAdmission` from the bit it observed. The cause lock records `StopCause::Operator { signal }` only on that successful transition, through `get_or_insert`, and then runs the existing `x4.gate.latch.after` point outside the lock. A lost race does not replace the first cause.

`open_window` runs only after `admit_attempt` returns success, before object publication. `Ok(PreparedCommit)` has no `Drop` that closes the window. A latch taken on that value and before `publish` is `BeforeAdmission`. A latch after `publish` returns is `OutsideWindow`. Every `StoppedSession` stores `admitted_at_close` from `close_window`'s pre-or sample. Both uncertain classifications, attempt `COMMIT` and seal `COMMIT`, take that sample and then forfeit the reserve. `finish` appends nothing when the reserve is already gone.

## Host order

`open_finalization` opens the session at R12 and keeps the one token. `finalize` replays inside that session. A signal already decided at the P2 check ends the session through `refused` and `finish` without arming. A signal that arrives while prepare is in progress stays pending. Successful prepare is the only arm point. `arm` classifies that pending signal at `AttemptAdmitted` and latches it. Prepare's refusal paths never arm; the pending signal stays phase A until the one P5 decision.

`publish` samples the close, and `returned` runs before `finish`. An unlatched `Committed` enters phase D. Every other publish return uses the close sample: admitted is C, otherwise B. `decide_output` runs once, then the operational hook, then one required render and write. A later signal is O until `settled`, then E. `CommitUndetermined` projects `DURABILITY.COMMIT_FAILED` and is left in place. A commit latched after admission projects the F39 renderer-failed row, with the published runId, and is also left in place. Any other decided signal becomes `Interrupted` at exit 130. A renderer failure before a byte is replaced by the failure envelope, including the F16 runId witness when a `PublishedCommit` exists. A write failure after bytes changes the outcome to exit 4 and does not emit a second envelope. The optional effect runs only after a successful authoritative output. The runner calls the operation entry once.

The harness admits only `SIGINT`, `SIGTERM`, and `SIGHUP` on the existing control channel. One registration owns the input thread. The product thread sends; that thread alone calls the source. The parent waits for the `signalled` acknowledgement and only then resumes the held thread. Drop closes the channel and joins the thread. An unknown name, or a signal with no registration, is a harness error.

The diff adds no crash-barrier point name and no feature flag. The new `cfg` uses are the existing test interference seam and the existing refusal harness. No operability path, mint list, pattern list, or exceptions file is in the delta. J4a and the O1a tree are outside it. J3d, native signal delivery, end-to-end and operability wiring, and S12-O remain owed. The checker vocabulary admits the names `J3b` and `J3d` and refuses them to `check-unit`. The host fixture has no J3d row.

## Fixture

Storage `required-runs.v1.json` is byte-identical to the base, 209604 bytes. Host clock epoch stays `1791072000`. The file has 102 rows and no trailing newline. The original 98 rows match the base except `stateUnchanged` on `F01` `replay-run-object-missing` and `replay-run-descriptor-altered`, both now `false`. Their other expected cells, including `ledgerCarrierUnchanged`, stay put. The four appended rows are S12-B `F38` `signal-after-staging`, S12-C `F39` `signal-after-admission-delivery`, S12-U `F40` `signal-fail-after-evidence-commit`, and S12-D `F15` `signal-x3d-finish-end-step-after-1`. Each script, label, unit `J3b`, and expected cell matches the bound S12.5 table. S12-O is absent.

## Qualification

The qualification log for the serial feature-library command records host 193 passed, platform 248 passed and 1 ignored, security 1062 passed and 2 ignored, and storage 178 passed. That is 1681 active and 3 ignored. The checker log records 28 tests, OK. The four pinned Clippy logs finish the dev profile with no warning and no error. The earlier unfrozen logs on rust-clippy 1.95.0 show those same checks were denied by `-D warnings`. Clippy was not rerun.

The r3 census files are host 18020 / `b1e4b157a64aaf90c349d25056d294ba811b0d42a60bd70ab7beac854666823c` and storage 21527 / `b4c6553fe04f5f7e089a947d4a407437dee6e507fb7716edeabe2e6378fd5958`. Those bytes also match the attempt2 and unfrozen census files. Host has 218 sorted unique names. Its three part traces are contiguous and their names and occurrence counts equal that census. Storage has 261 sorted unique names. Its trace has 2617 records in two contiguous parts, and the same name and occurrence equality. Both trace digests match the census records the checker reports. Release absence is 665 / `19e21a668fd4ad52b8f4e70dcc7cdbd06e9be5751712c719c58bfe56e4835dad`, `passed` true, and the two release-guard builds exited 101.

The two exclusive lead logs are storage 2126.70s and 2126.37s, host 775.67s and 776.27s, each one passed and exit 0. The published matrix check is 59851 / `b9b3e0af838e793ee73698d042fed3565d28e3cb18ec62fb08ad9012013fb7ea`. I reran that checker read-only, at nice 10, with the pinned Python `-I -B`, against the published r3 outputs. The new output is byte-identical. It reports commit `43d89894…`, `matrixPass` true, `passed` true, `productQualification` false, `repetitionsAgree` true, 505 rows in the union (host 102 and storage 403), kill set 389, 391 killed points, and `killedOutsideKillSet` exactly `x3c.object/file-barrier.after#41` and `x3c.object/file-barrier.before#41`. The two repetitions are the 1010 complete rows. This is not a product qualification.

## Inventory

v167 is 618550 / `718cde32c35771b11527e45715a662c0850228d82b7bf611bfca541553bbbf2b`. Parent v166 at the architecture base is 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. v167 has 1074 sorted unique rows and is a strict superset of the 1067 parent rows. Every inherited row is equal by value. `packages`, `pendingDecisions`, `schemaVersion`, and the standing sentence are unchanged. The seven added rows are the new cancellation source and the six refusal cases, and each path is present in the commit.

`successor.json` is 308006 / `ee9f259cd12ca87ecceb8d59d60816374671b5eea6919759f52706685a1fa575`. Its 103 description projections are the same paths, `before` text, and `effectiveDescription` text as the bound v166 successor `docs/implementation/m2/rust-g2-body-dialect-inventory-v166/successor.json`. Each selector names that path. Candidate indexes move only by the seven insertions, at indexes 121 and 213 through 218. There is no new override path. The two carried v54 pending decisions stay unresolved. No design-lock edit is in this unit.
