# D3A-3-r2 review

**Verdict: ACCEPT-UNIT.** Both round-1 required findings are resolved. No new required findings or non-blocking observations.

Subject: `docs/implementation/m3/supervisor-d/d3a-3-r2-subject.json`, 22,221 bytes, SHA-256 `ad3da9c24123ade090e4e645f7ab5c9446cee22615893d0d783b7ac7689c6484`.

## Subject verification

Independently rehashed all 92 manifest members. Verified all 15 candidate files against both their worktree and archived pins, all 14 existing parent pins against product base `5de9fd4740ea17018d0bd3fbff9496c94ddacda9`, and the source record's five authority pins, four base-unit/review pins, three prior-round pins and product-lock pin. The candidate is detached at that exact base, and its dirty/untracked paths match the map: 15 files, with only `crates/components/src/supervisor_records.rs` new.

Compared each archived round-1 product file with the round-2 worktree. The changes are the two requested fixes, their tests, the six associated registrations/readers/renderings/budget slots, and the registry-owner mint-audit recount. `Cargo.toml` and `Cargo.lock` are byte-identical to round 1. The previously reviewed components-to-operability normal dependency remains; round 2 adds no dependency.

## D3A3-R1-RF-1: resolved

The six new ordinary registrations are `tool.limit.breached`, `tool.sample.incomplete`, `tool.wait.expired`, `tool.teardown.started`, `tool.scratch.retained` and `tool.child.settled`. All require Project only and omit provider role and universe. The scratch event exposes the three typed constructors, with actual errno only for `io-failure`; the general constructor remains crate-private. Each registration has its reader descriptor, C-2 inventory entry, committed reference rendering, export setting and `EmitOn<ProjectScope>` implementation. Budget slots 23–28 are distinct, within `BUDGET_EVENTS = 29`.

Every supervisor-produced fact goes through the central class-aware `fact` method. On tool paths, `RecordFact::for_tool` maps the common limit, sample, wait, teardown, scratch and settlement facts to the new tool variants, preserves tool spawn/reap, and suppresses provider-only facts. `RecordFact::requires()` agrees with their registered identity sets. Provider paths retain the Project/Plan/Execution requirement. No Plan, Execution, provider role or universe is fabricated for a tool.

The new class-identity control checks normal, timed-out, output-bound, sample-failing and scratch-retaining tool runs against the registry's actual identity requirements and requires all eight tool event names to be produced. It separately checks provider facts. The two round-2 tool-routing mutations fail that control. Event-field completeness and the registry inventory checks include the six additions.

## D3A3-R1-RF-2: resolved

`PendingWrite` now carries the optional record associated with completion. `send_deferred` attaches `CancelSent` after the session accepts and queues its cancel frame; it does not emit the fact. `service_control_write` retains the annotation and offset over short writes, `WouldBlock` and interrupted writes. Once the complete frame has been written, taking the pending value consumes its annotation and emits the fact once. A fatal write error clears the pending value and closes fd3 without recording it. Settlement closes the descriptors and subsequent loop turns stop, so an abandoned pending frame cannot later produce a sent fact.

`ControlSession::send`, validation, sequence advancement and deferred-frame ordering remain unchanged. The internal `ControlSent` observer notification remains a queue notification, as before; it is distinct from the operability `CancelSent` fact corrected here.

The new completion control asserts zero facts while queued, zero after a partial write with a three-byte allowance, and one after full completion. The failed-write control first proves the cancel was queued, then injects `EPIPE` on that write and checks that no sent fact exists. It also retains the early-closing child-reader case. Both premature-emission mutations fail actual test assertions.

## Carried obligations and regression scope

The eight entries in `carried-obligations.json` cover the four unresolved tables, the settlement-name correction, actual event construction/emission, D3b's forced-cancel/tree-sweep producers, and D5's real-codec rerun and handshake timing. Their proposed owners are reasonable and explicitly remain subject to coordinator confirmation at assent. The D5 entry's twelve flaky tests refers to round 1; the current comparison has nine.

The previously accepted gate, whole-spool discard, one-shot output release, scratch-removal behavior, route distinctions, reduced liveness provenance and incomplete-sampling disclosure remain intact. D3A1-R2-NBO-1 and D3A2-R1-NBO-1 remain discharged by the existing reduced facts and controls. The four blocked events are still blocked rather than registered with missing fields. `supervision.child.settled` remains the explicit name-only cross-law correction. This unit does not claim M3-D item 21 complete.

## Validation

Independently ran only the permitted `python3 -I -B tools/check_operability.py source --repository .` in the candidate: passed, 114 rows, no findings. The registry-owner exception recount is accepted; no new mint call outside operability is introduced. The revised components production code adds no environment read or `let _ =`.

Inspected the pinned lane logs and controls without running Cargo, rustc, builds or the lane. Components has 101 base passes and nine handshake-related failures versus 127 candidate passes and zero failures. Each of the nine differing tests passes all six recorded isolated runs; adjusting the comparison for these established timing failures gives 17 new tests. This does not establish a passing parallel base suite or eliminate the timing concern carried to D5. Operability rises from 95 to 99 passes with no failures. Focused supervisor tests pass 66/66 and focused registry/readback tests pass 32/32.

All 19 mutations have nonempty actual test-failure results, with no mutation timeout or reliance solely on compilation failure. Independently read the historical attempt-1 controls: the failed-write mutation was indeed uncaught. The added queued-cancel EPIPE control addresses that missing exercise; the lane of record catches it. Later base-assertion stops are history, not substitute validation.

Recorded warning-denied all-targets Clippy, scoped rustfmt, workspace all-targets check, package-edge policy, test-fixture feature scope, environment exceptions, unchanged census closure and verify_design all pass. Package edges remain contracts, identity, operability and platform, all normal; test-fixture stays confined to the components dev dependency. verify_design explicitly reports no product qualification.

Acceptance is for this library unit and these exact bytes. Production composition/emission and persisted readback remain J2b's obligations, producer additions remain D3b's, real-codec qualification remains D5's, and the one new file still needs its separately reviewed inventory successor. No repository, worktree or control file was edited; no network, private fixture, installation, held tree or T2 material was accessed, and no delegation occurred.
