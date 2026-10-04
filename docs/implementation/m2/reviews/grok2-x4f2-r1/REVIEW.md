# GROK2 review: unit X4-F2 r1

**Verdict: ACCEPT-UNIT.** Required findings: none.

Unit X4-F2 implements law X4T r12 (Codex ACCEPT, `reviews/grok2-x4t-f2-r1/`) on product worktree `/Users/sb/code/opensip-ai/opensip-x4f2`, detached at `3f6f9a5a2543b70c0c259e041dc65d7e29164a0d`. The subject is the uncommitted diff against that commit: 10 files under `crates/security/src/`, +620 −42, 47332 bytes, sha256 `ffc4ef1e038199c13b2c1fa0139405239f57f362ee274f46bb26835a3f6835be`. No file is added, removed, or renamed, so there is no inventory successor and no design selection. `subjectSha256` is that diff. This review did not run cargo or a crash-matrix set; the lanes and the X9 evidence are the recorded runs.

The law reviewed is `trust-admission-x4t/PROPOSAL-r12.md`. The live `PROPOSAL.md` carries the acceptance note.

## Law

The fenced arm of `admit_bound` (`current_trust_admission.rs`) keeps the stored-state join before authentication. Its `Ok` standing is discarded. A stored continuation refusal still returns there, before time. After S4's own refusals (payload-future, time range, no context, in-session, beyond-horizon), the arm takes `TimeAdmission.expired` at `evaluation` (tEval), applies `clock_roles`, and joins again.

`clock_roles` is X4-F1's mapping through `role_machine::clock`: root expiry to TR-BUNDLE, TR-COMPONENT and TR-CORE; root or catalog expiry to TR-INDEX; list staleness to all four; TR-PROFILE and TR-REPAIR stay as stored. `clock` is `decide`'s EV-CLOCK: from Trusted or StaleRevocation, expiry yields Expired; from Trusted, staleness alone yields StaleRevocation; expiry is tested first, so it wins when both hold. Nothing is written back into the capsule's roles.

A refused second join is `Admission::Clocked`. It carries the continuation refusal, the floors, the unchanged `TimeAdmission`, and the pending write (absent when the read is report-only). An admitted second join is `Admission::View` with the clocked roles, that standing, and a handoff clock taken from tEval plus the observation's monotonic time and boot. Absent expiry states refuse `TrustRow::HostIo` with cause `expiry`, the same treatment `trust_bootstrap.rs` uses on the accept path. S4's `finish` sets the triple on every admitted evaluation, so that row is unreachable today, and the missing triple is never read as "not expired".

`fenced_first_read` publishes that refusal where r11 returned the view. Check 3 still compares `admission.floors()` and returns `trust-rollback` before any write. When S4 proposes a change, the same floor publication is built and published, the owner advances, and `into_view` runs after that confirmation. When nothing needs writing, the closing fence and owner rechecks run, and `into_view` follows them. A failed build, publish, or recheck returns its own row first. Report-only leaves `pending` empty, so the same clock and join produce the same refusal with no publication.

The reread arm is X4-F1's: it clocks the capsule's stored states at its own instant and a refused join is a plain `Err`, because `standing_of?` runs inside the reread arm. `live_observation.rs` is outside the diff. Its production reread still calls `admit_current_trust`, which converts through `into_view` and writes nothing.

The row is the existing continuation: `CONTINUE-CORE-NOT-TRUSTED`, subject `core:expired` or `core:stale-revocation`. `token` maps those states to those suffixes, and `standing_of` prefixes `core:`. Expiry wins, so both states yield `core:expired`. A catalog expiry alone clocks TR-INDEX to Expired and leaves core and component Trusted, and `standing` admits that as `ExistingOnly`. The diff introduces no `ROOT.FINAL_EXPIRED` row, no new code, and no new subject. It touches no `crash_barrier!`, `crash_scope!`, `observe_clock`, or `native_clock` line.

## Composition, the view, and the hold

Each admission clocks the roles just loaded from that capsule, once. The reread does not take the start view's `role_states`. The floor publication leaves the stored role states as accepted, which the native and handoff tests pin (every carried role stays `ST-TRUSTED` while `evalHighWater` advances). A later reread therefore clocks those stored states again.

`Admission::Clocked` has no standing and no epoch. `into_view` is the only conversion, and it returns `Err(refusal)`. `admit_current_trust` and `admit_native` both end in `into_view`, so neither can return a clocked view. `bootstrapping_first_read` returns any first result other than `NoAdmittedTimeContext` as it stands. A clocked continuation refusal is that other result, so the F-absent acceptance does not run. The native test drives both `fenced_first_read` and `bootstrapping_first_read` (`BootstrapSource::unreached()`) and both refuse `core:stale-revocation` after one confirmed publication.

The production hold is the existing `gate_step`. `trust_start` runs `fenced_operation_read` inside that step. On `Err`, `gate_step` spends the gate and returns `GateStep::Step` without the post-success recheck. `fenced_operation_read` returns the view and the owner's confirmations only on `Ok`, so a clocked refusal drops the local owner after `publish` has already made the new `state.v1` durable. The handoff test pins the observable result: `OperationRow::Installation(TrustContinuation { subject: "core:stale-revocation" })`, the floor advanced to `2026-12-30T00:00:01Z`, stored roles unchanged, no carrier floor, no grant journal, and the monitor samples taken while the fence was held and both leases were free.

## Fixture, and the manifest

The three knobs live on the test-only `Spec` in `accepted_store_fixture`, which is compiled under `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`, the generator's existing gate. Each defaults to `None`. `None` substitutes the previous literals: manifest `issuedAt` `2026-10-01T00:00:00Z`, catalog `expiresAt` `2027-04-01T00:00:00Z`, and the signing root's own `expiresAt`. `produce` and `construct` both sign the substituted values into the manifest, the root, and the catalog. `accepted_store_files`, the matrix builder, calls `generate` with `Spec::default()`, so it passes no knob. The X9 comparison's equal post-state hashes and child traces are the check that those default stores are unchanged.

**Call 6.** The bootstrap manifest's `issuedAt` is the document to move.

`project_times` sets `newest` to the maximum of three issue times: `bundle.proof().payload()`, the catalog, and the revocation list (`ordinary_targets.rs`). `trust_ordinary_inventory.rs` identifies that proof payload as the manifest. Fresh acceptance sets A to the maximum of the root issue time and `newest`, then L to A. The list's issue time is also `revocationIssuedAt`, and staleness is strict `>` of that instant plus 90 days. Raising the list would raise A and the staleness anchor together, and the window between them would stay shut. That is why a default store, whose L is the list's issue time, reaches `beyond-horizon` at the same second the list goes stale.

The catalog's `issuedAt` is one of the three `newest` inputs, and `recovery_catalog.rs` also requires it to precede `expiresAt`. The root's `issuedAt` is the other term of A, `admitted_roots.rs` requires it to precede `expiresAt`, and S4 has a separate payload-future check on the root time. The manifest's `issuedAt` enters the retained time view only through `newest`.

`produce` keeps the acceptance sample at `anchor()`: wall `2026-10-02T00:00:00Z`, boot-1, mono 7. Payload-future refuses when `newest` is strictly after that wall plus 24 hours, so `2026-10-03T00:00:00Z` is the latest issue time that wall admits. A and L become `2026-10-03`, the plausibility bound is `2027-01-01T00:00:00Z`, and the list issued `2026-10-01` stays stale strictly after `2026-12-30T00:00:00Z`. The tests use that two-day window. `construct`, for stores the producer cannot reach, records F and L as `max(2026-10-02, manifest issuedAt)`, which is what that acceptance rule records. The r12 tests assert `produced` and run on the producer path.

## Tests

The five in-memory tests and the two native tests, plus the handoff test, pin the boundaries:

- Strict `>` for staleness: a fenced read at `2026-12-30T00:00:00Z` is admitted `InstallGateRequiredForNewProcess` with trusted carried roles and expiry `(false, false, false)`; one second later is `core:stale-revocation` / `CONTINUE-CORE-NOT-TRUSTED`.
- `>=` for root expiry: `2026-10-31T23:59:59Z` is admitted; `2026-11-01T00:00:00Z` is `core:expired`.
- Expiry wins: with both states available, `2026-12-30T00:00:01Z` is `core:stale-revocation` and `2026-12-31T00:00:00Z` is `core:expired`.
- Catalog expiry alone at `2026-11-01T00:00:00Z` is admitted `ExistingOnly`, TR-INDEX `expired`, the other carried roles `trusted`, S4's triple `(false, true, false)`, and a handoff clock present.
- The mapping test is table-driven through `clock_roles` and `standing_of` at eight instants inside one plausibility window, for report-only and for a writing read. Admitted rows compare standing, role tokens, the triple, and the report flag. Refused rows compare the continuation row.
- The reread test, after an `ExistingOnly` fenced read, reads the same store again at tEval and gets the same standing and role states, with `time()` empty. A later reread, advanced by monotonic time on that boot, refuses `core:stale-revocation` from the stored trusted roles.
- On native files, both entry points publish one floor (F = tEval, anchor = the sample, L unchanged, roles still `ST-TRUSTED`, revision + 1) and then refuse. The second read uses Codex's X4T-R12-NB-01 sample: boot-2, mono 160, wall `2026-12-28T00:00:00Z`, about two days behind the anchor written at `2026-12-30T00:00:01Z` on boot-2 mono 100. Same-boot deviation below −24 h with no excusing witness is `SessionRegression`; S4 keeps the anchor, tEval′ is F, `needs_write` is false, the owner has no confirmation, and `state.v1` and the file count are unchanged.
- Report-only on that store refuses `core:stale-revocation` and writes nothing. A wall of `2027-01-01T00:00:01Z` refuses `beyond-horizon` before the clock, with the same bytes and inode.
- The handoff test is the lease-free termination, as above.

`needs_write` itself is unchanged: it is false for report-only, for an S4 refusal, and when F, L, and the anchor are unchanged.

## Recorded lanes and X9

`evidence/results.json` records the lanes on `3f6f9a5` plus this diff, all exit 0: fmt, the workspace and feature builds, clippy `-D warnings`, 14 passed in the new-and-neighbour test lane, workspace all-targets 1739 passed / 0 failed / 3 ignored on each of two runs (549 s), 18 doctests, and the crash-matrix feature lane 1637 / 0 / 3 ignored (567 s). `verify_design` and the package, dependency, identity, and crash-matrix checker lanes are exit 0. The +8 tests account for 1731 → 1739 and 1629 → 1637. The aborted first lane run stopped on the phase-1 `use` line and is not evidence. I did not re-run these.

X9 is item 13's subset, two sets against the accepted X9-6 evidence at `3d2d5b5`. `evidence/x9/compare.json` has `"identical": true` and `"differences": []`. Storage is 54/54 PASS in both sets (census 259 points, trace 1379 records, `e9add21e…`, kill set 321). Host has no selected row in either set (census 218 points, trace 1195 records, `93d0922a…`, kill set 271). `timingGuardMs` is empty on both targets. `source-pins.txt`, rerun on the final diff, shows zero harness files changed from `3d2d5b5` to `3f6f9a5` or touched by this diff, and zero changes under `crates/security`, `storage`, `host`, and `platform` from `15c0779` to `3f6f9a5`. The diff does touch `accepted_store_fixture.rs`, which is how the matrix stores are built; the equal post-states are the default-knob check.

`waits.txt`: release absence waited 300 s and was clear at 16:19:13Z; `x4f2-1-storage` started with no wait; `x4f2-1-host` then waited 600 s, first on another agent's `cargo test -p opensip-host --lib schema_sources` seen at 16:23:21Z as storage ended, then on the lead's own workspace confirmation; `x4f2-2-storage` and `x4f2-2-host` started clear. `overlap.txt` is the single line `sampler-done`. No selected row carries a timing guard, so the build that appeared as storage ended had no guard to disturb. A full two-target `check` with `matrixPass` needs a clean commit and belongs to integration.

Release absence (`evidence/release-absence.json`): `target/release/opensip` is 6314160 bytes, sha256 `9dd734457effe53f049cd4aad007c23262577292e71a05b629a6fcab13ea458d`, `passed: true`, `found: []` for `OPENSIP_X9_` and the 25 scope names. The crash-matrix release builds of storage and host are refused at the compile guard.

## Judgment calls

1. **Accepted.** `Admission::Clocked` carries floors, the S4 outcome, the pending write, and the refusal. `into_view` yields `Err`. The reread signature stays `Result<AdmittedCurrentTrust, TrustRefusal>`.
2. **Accepted.** Check 3, then the write-ahead when `needs_write`, otherwise the closing rechecks, and the refusal is published at the point where r11 returned the view.
3. **Accepted.** The hold is unchanged `gate_step` code, and the handoff test pins `TrustContinuation` at the lease-free point.
4. **Accepted.** The first join still refuses a stored state that does not continue, before authentication and before the clock. The clock runs only for a store that join admits.
5. **Accepted.** A missing expiry triple is host I/O, cause `expiry`.
6. **Accepted.** The manifest is the issue time to move, for the reasons above.
7. **Accepted.** `construct` applies the same signed knobs and records F and L by the acceptance rule. The r12 tests run on produced stores.
8. **Accepted.** The sticky sample is the same-boot set-back of more than 24 hours that NB-01 asks for, and the second read writes nothing.
9. **Accepted.** The mapping test calls `clock_roles` and `standing_of` instead of restating the table. Refused rows are compared by row, because the clocked states of a refusal are not in a view.
10. **Accepted.** The fixture is touched; the harness pin list is not. Default `None` keeps the old literals, and the X9 post-states match.
11. **Accepted.** Both variants are boxed. The recorded clippy lane is clean under `-D warnings`.
12. **Accepted.** The subject diff gives `write_accepted_trust_issued` its own `use` line. The lanes above ran on that diff.

## Outside this unit

Expiry between reads, native scheduling of the 5 s and 10 s bounds, a recorded EV-CLOCK, F9's fixture date refresh, and Linux remain for their owners. For an X4T-0 store whose L is `2026-10-02`, a fenced read on the native clock now refuses `core:stale-revocation` from `2026-12-30T00:00:01Z`. A default produced store refuses `beyond-horizon` from that second. F9's `2026-12-01` deadline covers both.

`~/Library/Application Support/OpenSIP` was absent. No repository file was edited.
