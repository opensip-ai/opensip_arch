# D2b-3b r2 review

**Verdict: ACCEPT-UNIT.** No required findings or non-blocking observations. D2B3B-R1-RF-1 is resolved. Product qualification is false.

## Subject verification

Verified the 12,431-byte subject manifest, SHA-256 `9c5fd9b424c375b3e4cee1a47507717e61094f3e02b849305b7f390de191e129`, and all 53 members against their sizes and hashes. All authority pins and the pinned round-1 review match. The six product-map rows match the candidate and archived bytes; existing-file parent pins match Git. Candidate HEAD is the declared product base `d113fa735225c416e3c9e903e706aec3a2a435fd`, with exactly the three edited and three new paths recorded. The declared architecture base is `87657afb8c9edba63780f9a0018691b2d21265de`.

## Round-1 disposition

`realize_next` now wraps private `realize` and calls `refuse` on every returned error. This closes the transient source-error path for direct realization and for `send_next`, including short reads and other realization errors. `cancel()` also latches its before-Hello refusal. The other public fallible sender operations use the same irreversible refusal guard; the observation accessors do not reopen it.

The four source-restoration cases cover first and later chunks through both entry points. They check that next_slot and cancel_payload disappear; realize_next, send_next, admit, cancel and admit_cancel return AfterRefusal; and the source read counter does not advance. The existing failed-source case and before-Hello Cancel case now check the ended transcript. Both new latch mutations fail the relevant controls.

## Builders, schedule and sender

The unchanged builder and planner portions remain consistent with the carriers, handshake/startup schemas, DLV and trial-07 reference:

- The seven host frame families use the prescribed closed checks. Hello carries selection tokens without repair and schema-sourced limits/identity versions. Unsupported census selection remains refused pending D2b-3c.
- OpenUniverse recomputes universeKey from resolvedInputs under the prescribed domain. Manifest and seal use the supplied sealed inventory, its canonical manifest digest and checked aggregate counts.
- Analyze projects stages in selection order with Analyze-relative ordinals, empty absent dependencies, the six-dimensional budget projection and range, manifest-order file subject scope, Plan-supplied keys, verified producer version and prescribed commitment domains.
- The planner checks entry bounds before manifest construction, measures envelope payloads without the prefix, uses closed-form greedy chunk sizes without materializing chunk bytes, hashes chunk payloads without bytes and binds each final chunk to its entry digest. It reserves the maximal Cancel at the last possible sequence and uses the carriers' refusal route. TS2 has no request-total limit.
- The sender independently walks the request and supplied snapshot bytes. Before advancing sent state it checks sequence, family, chunk coordinates, seal count, closed schema, exact envelope payload length, payload digest and final entry content digest. Refusals end the transcript.
- Cancel remains once only, after Hello, at the next sequence, with user-interrupt and deterministic-CBOR equality to the exact sent correlation, within the reserved bound. No subsequent frame can be admitted.

The context/request constructor joins the receiver's checked values to the actual request: Hello values, OpenUniverse identifiers, manifest digest/files, seal totals and stage correlation/budgets/keys with the context's providerBuildId. The T2O gate uses a copied run and the same host event as sent(), rather than duplicating table policy.

## Participant and supervisor rebase

The participant retains one pending frame and performs at most one pipe write or one bounded pipe read per call. Admitted transitions alone generate progress and admitted-byte accounting. WouldBlock/Interrupted do not fault; zero-byte pending writes and other host pipe failures are HostFault. Faulted participants send nothing further and reject cancellation.

The supervisor diff on the D3a-3 base is limited to ParticipantStatus::HostFault and its transition arm triggering Cause::HostFault. The existing terminal, fault, accounting and boundary handling is preserved.

Each admitted FactBatch contributes its received payload bytes to the spool in admission order. A refused frame is not appended. The spool moves into the terminal output at its single mint; take_terminal_output hands it out once, and discard drops both retained spool and output. TransferStarted follows manifest acceptance; TransferEnded follows admitted SnapshotAccepted; ContextVerified follows NativeContextVerified or pre-Analyze Unavailable. The session controls check spool bytes, discard and these boundaries. The three D3a-4 boundary variants are explicitly deferred because that seam is not consumed by this subject.

D2b-3a's historical base clarification is retained. Its depth-witness observation is addressed with a lawful depth-7 Coverage frame admitted in a session, plus a depth-8 reader refusal. No new issue arises from either disposition.

## Validation and limits

Independently ran the two permitted commands: operability source passed with 114 rows and no findings; the duty-table checker passed with 30 rows, all 55 carrier ids listed once, and all 19 TS2 builder/sender rows named. The source/reference comparisons above supplement that lexical duty check.

Reviewed the pinned lane evidence without rerunning builds or tests. Components pass at base/candidate with 145/164 passing tests, identity 72/72, contracts 0/0, and empty failure sets throughout. The fixture runner records each side's own supervisor fixture path/hash before its suites. All six Rust files are new or base-clean and recorded format-clean. Warning-denied all-targets Clippy, 35 focused TS2 tests, environment checks, census-closure check and verify_design pass; verify_design reports 52 admission sources and no product qualification. All 17 mutation logs contain failing tests rather than compilation failures.

The disclosed limits remain: no supervisor-level control drives the new HostFault arm; no real TS2 child session runs here; C4 Plan production, C1/D4 source custody and session composition, D3b cancellation integration, D3a-4 boundaries, FA-2/replays in D2b-3c and the inventory successor remain separate work. Acceptance does not claim those deliveries or D2b completion.

Only REVIEW.md and review.json were written. Neither repository, worktree nor control files were edited. No Cargo, rustc, builds, generators, lanes, network, other panes or delegation were used. No forbidden private fixture, installation, signing key, held tree, T2 store or cache was read.
