# Law X8 r2, the opaque API refusal suite

Verdict: **REQUIRED-FINDINGS**.

r1's RF-1 is closed. Item 4b is one site list, X9-1's pin extended by name, with one joint predicate on exactly the sites both surfaces call. r1's RF-2 is not closed. Item 5a names a helper process, and the invocation it names does not run that helper.

## Subject

`docs/implementation/m2/refusal-suite-x8/PROPOSAL.md` is 39753 bytes, sha256 `829a70e547ef766317893a0ddf479289846b6004fcf9a1ec814aa35221b2bafd`. `PROPOSAL-r1.md` matches the r1 subject, 32723 bytes, sha256 `1fa3fa80fe3859115a05d5527c0de58ed96e879728d9a8670460d092a697c125`. The r1 review files match `hashes.txt`. Accepted X9 r1 matches its pin, 50057 bytes, sha256 `8ef294d241a1bf3c1324ddf6ef2d2a23dc883269e01ada695b0fe17955f827e4`. The diff against r1 is the header cites, the r2 note, items 4b, 4c, 4f and 4g, the synchronization and item 5a, the B6 and B7 rows, the unit dependencies, and the forbidden substitutes. Items 1 to 3, B0 to B5, B8 and item 6 are unchanged. No new public code, row or detail. `TRUST.COMPONENT_REVOKED_DURING_OPERATION` is already in the public detail registry.

## RF-1 from r1

Closed.

Item 4b has one list and no second pin: `Image::Injected`, `HomeSource::Fixture` and its match arm, X4T-0, and the fenced `state.v1` publisher. Each of those is `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. A site is on the list only when both support surfaces call it. `AppendStep`, `ObjectStep` and the ledger commit hook stay `cfg(test)`, and `scenario` does not name them. `scenario-fixtures` stays a separate feature, enabled from storage's and host's `[dev-dependencies]`. `crash-matrix` stays X9 item 2: no manifest names it, only the matrix targets' `required-features` reach it, and a release build fails at `compile_error!`. `crash_matrix_support` still returns no authority type. `scenario` is compiled only under `scenario-fixtures`, and `operation` returns the production `ProjectOperation`. Item 4f says that with neither feature every shared site is `cfg(test)` only, so X9 item 2's release-absence evidence still covers them. Item 4g tells X3d r7 to name this same list for both the ordinary lane and the matrix rows.

The recorded wording change matches X9 and leaves its outcome in place. X9 item 6's sentence that a `cfg(test)` site becomes `cfg(any(test, feature = "crash-matrix"))` is restated, for the shared sites only, as the joint predicate. X9's forbidden substitute that bars a `cfg(any(test, feature = "crash-matrix"))` site from a build reached without `--features crash-matrix` excepts those shared sites when they are reached through `scenario-fixtures`, and they stay absent from every release build. No barrier point, `crash_matrix_support` item, row or outcome of X9 changes. X9's proposal file is not edited.

## RF-1. The helper invocation exits successfully without publishing

Item 5a tells the test to re-execute `std::env::current_exe()` with `--exact` on one `#[ignore]`d helper test, then to wait for that process to exit with success before `prepare_commit` and `publish`.

The Rust test harness treats an ignored test as not run. On this host, rustc 1.95.0 `--test` with `--exact helper` on an ignored test printed `test helper ... ignored` and exited 0 (`0 passed; 0 failed; 1 ignored`). The same binary with `--ignored --exact helper`, and with `--include-ignored --exact helper`, ran the body. Item 5a does not pass `--ignored` or `--include-ignored`. The success exit it waits for is the exit of a process that did not publish. B6 and B7 then call `prepare_commit` against the trust view the handoff already held.

X9 item 3 does not use `#[ignore]`. Its child is an ordinary `#[test]` that returns at once unless `OPENSIP_X9_CHILD` is set, spawned as `current_exe() --exact <child entry>`. That entry runs under `--exact` alone.

The publisher call has the same hole. X9 item 6 places the fenced publisher inside `crash_matrix_support`, and that module exists only under `crash-matrix`. Item 4b keeps the modules separate and keeps X9 item 2, so the host test binary, which enables `scenario-fixtures` from `[dev-dependencies]`, does not compile `crash_matrix_support`. Item 4c withdraws `publish_revocation` and lists no publication function on `scenario`. Item 4b also says a shared site is on the list only if both support surfaces call it, and that under `scenario-fixtures` the site is reachable through `scenario`. The helper is a host test. As item 5a and item 4c are written, that test has no compiled publisher to call.

B3, B4 and B5 stay on the test thread. B3 and B5 replace project files, B4 plants a ledger row, and none of them takes the fence or writes trust state. That part of r1's RF-2 is met. The observer-tick sentence is also right for these two rows: the helper is required to finish before `prepare_commit`, so the published `state.v1` is already in place, and X4 r7 items 5, 7 and 8 make either the checkpoint or the 5 s observer a revoking observation of that view (gate `0 → 2`, `TRUST.COMPONENT_REVOKED_DURING_OPERATION` for B6; unrelated drift and `Committed` for B7). X9 item 11 holds the observer only so a matrix script can choose which party latches. B6 and B7 assert the row, not the party.

Required: the re-executed process runs the fenced publisher before it exits 0, in a process that never ran `operation` and holds no operation lease. The harness arguments must select that entry; an ignored test needs the flag that runs ignored tests, or the entry follows X9 item 3 and is an ordinary test that publishes only when the helper environment is set. Success means the publication happened. The publisher is callable from that host test under `scenario-fixtures` alone, through `scenario`, and `crash-matrix` stays off that build. The test thread still waits for the process to exit, then calls `prepare_commit` and `publish`, with no sleep.

## Rest of the amendment

The withdrawal of in-process `publish_revocation`, the separate process, the fence being free after the handoff, and the rejection of a helper thread in the lease-holding process match X4 r7 item 2 and X2 r8 item 7a. B6 and B7 name item 5a. X8c's dependency on X9-1's publisher matches. The new forbidden substitutes match the joint predicate, the separated features, and the ban on a trust write from the lease holder.
