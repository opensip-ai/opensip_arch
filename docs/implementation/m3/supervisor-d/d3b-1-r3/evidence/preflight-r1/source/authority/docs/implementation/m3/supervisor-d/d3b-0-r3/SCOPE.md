# D3b-0 r3: the macOS descendant mechanisms, rebased onto D3a-4 (M3-D r5 items 4, 8, 16 and 18; D3b plan r3, sub-unit D3b-0)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 3: a rebase-only round.**

Round 2 (`codex-d3b-0-r2`, subject `c1fd5c30…`) was accepted by Codex with ACCEPT-UNIT and no findings. The lead held its integration (LD-ORD-1) until D3a-4 integrated, because D3a-4 also edits `crates/platform/src/lib.rs`'s `process` re-export list. D3a-4 is now integrated at `4e475c7`. This round re-applies the accepted r2 candidate onto that main and changes nothing else. The r2 package (`../d3b-0-r2/`) is the accepted substance and is unchanged; its SCOPE, self-review and untested-path disclosure stand as written.

**Base:** the product main that the lane of record ran on, recorded as `productBase` in `evidence/d3b0-checks-r3/checks.json` (`4e475c7`, unless the lane records a disjoint move in its own `rebased.json`).

## Delta against the accepted r2

D3a-4 changed all three candidate paths on main: `TerminatingSignal` in `process.rs`, its test in `process_tests.rs`, and its export in `lib.rs`. So the r3 files cannot be byte-identical to r2's. What is identical is **D3b-0's own change**: the added and removed lines of each file's diff against its base.

| File | r2 (on `f16f50d`) | r3 (on `4e475c7`) | Delta |
| --- | --- | --- | --- |
| `crates/platform/src/process.rs` | D3b-0's hunks | the same hunks; `git apply --3way` applied them cleanly | **None** in D3b-0's change. The `+`/`-` lines of the two diffs are identical (SHA-256 of the line set `b5605969…`, equal for both). The file also holds D3a-4's `TerminatingSignal`, unchanged. |
| `crates/platform/src/process_tests.rs` | D3b-0's hunks, appended after D1a's and D3a-0's tests | the same hunks. The append conflicted with D3a-4's appended `terminating_signals_map_by_their_libc_constants`, and was resolved by keeping D3a-4's test whole, then D3b-0's section | **None** in D3b-0's change: the `+`/`-` lines are identical (`ab69fa46…` for both). |
| `crates/platform/src/lib.rs` | the `process` re-export list gains `KillOutcome`, `Listing`, `ProcessIdentity`, `Protected`, `child_processes`, `group_members_bounded` and `process_identity` | the same seven names, merged into the list that D3a-4 extended with `TerminatingSignal` | **The one re-based hunk.** The list is the union of D3a-4's names and r2's, in rustfmt's order. No name is added or removed beyond r2's seven. |

The rustfmt classification of all three files is base-clean and candidate-clean. The product map pins each file's parent at `4e475c7` and its candidate bytes.

## Takeover packaging note

Codex recovered this draft and its already completed lane after taking over implementation. Candidate code was not edited or rerun. The additive rebase proof in `evidence/rebase-equivalence.json` independently compares added/removed diff lines (joined by LF, without a final LF) and verifies the export union. The digest labels above use that explicit representation; the original draft used another unspecified representation. The source record's inventory base is refreshed to v231 from the unchanged candidate lock. This remains an unreviewed rebase-only package.

## Checks of record

`evidence/run_d3b0_checks.py` is r2's runner, unchanged except for its labels. Its rows are:
- the platform suite on base and candidate, serial, with equal failure sets and **nine** new passing tests, as in r2;
- rustfmt;
- warning-denied all-targets Clippy;
- the workspace check;
- the focused D3b-0 tests;
- the environment exceptions;
- the operability source census;
- the census-closure check;
- verify_design;
- r2's eleven mutations, each of which must fail a test and not compilation.

## Self-review

r2's self-review (`../d3b-0-r2/SCOPE.md`, "Self-review") applies unchanged, since D3b-0's change is unchanged. For this round, the lead checked:
- **item 5 (immutable pins):** the subject pins round 1's and round 2's submitted subjects and reviews, both rounds now closed, and the accepted r2 package;
- **item 8 (disclosure):** the conflict resolutions above are the only hand edits.

## Not claimed

The same as r2. No walk, confirm, tree report or record (D3b-1); no cancellation (D3b-2); no Linux; no production caller.

## Question for the reviewer

- **Q1.** Is r3 a faithful rebase of the accepted r2? Check three things: D3b-0's diff lines are identical in `process.rs` and `process_tests.rs`; `lib.rs`'s re-export list is the union of D3a-4's and r2's names; and nothing else changed.
