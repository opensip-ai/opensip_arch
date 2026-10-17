# D3a-4 r2 review

**Verdict: ACCEPT-UNIT.** D3A4-R1-RF-1, RF-2, RF-3 and NBO-1 are resolved. No new required findings or non-blocking observations.

## Subject verification

Verified the 21,571-byte subject manifest, SHA-256 `454d5eeb6a96260ed56f7dd208ae96f0fec56f6e86db18146acc79719229b1fa`, and all 91 members against their sizes and hashes. Authority, base-unit and prior-round pins match. All 16 product-map entries match candidate, archived and parent bytes. Candidate HEAD is the declared `7a4be0b0402341481ae388c0cd46877f328de6c2`, with exactly the 16 edited paths and none new. Git confirms the final f16f50d-to-7a4be0b base move changes only design-lock.json.

## Round-1 dispositions

### RF-1 — resolved

AbsenceClock separates the last admitted transition from the last report. Only SelectAck/admitted progress advances progress; report advances only reported. Both the report condition and wake-up scheduling use due(), an interval after the later timestamp. Reports therefore retain a growing since value without repeatedly scheduling an expired transition deadline. A later real transition resets the effective span and schedule.

The fixed-instant control proves reports at 200, 410 and 610 ms measure from the original transition, then a 700 ms transition resets the next due time to 900 ms and its span to 200 ms. The slow-long fixture checks multiple increasing reports. Both absence-report-resets-the-span and absence-schedule-ignores-the-report are caught, alongside the zero-span mutation.

### RF-2 — resolved

reach_terminal sets the first terminal_observed before the existing-cause early return. teardown_span prefers that observation over teardown_from and uses the first trigger only when no terminal exists. terminal_at remains the normal-exit grace timer; the existing-cause return still prevents normal shutdown/grace actions. The first cause, teardown ladder and single stage-terminal fact are preserved.

The controlled case invokes the real reach_terminal after a trigger placed at least 150 ms earlier, checks the new observation and 250 ms terminal-based span, preserves HostFault and leaves terminal_at absent. The real facts-then-hang case proves the no-terminal trigger fallback within labelled lower/upper time bounds and records one crash terminal. Both terminal-time-only-without-a-cause and teardown-without-its-trigger-fallback are caught. Replacing a timing-dependent real fault-before-terminal fixture with this controlled ordering is appropriate.

### RF-3 — resolved

The new source-equality control independently parses the carrier/startup/native schemas and compares table members in order:

- StageKind against the TS2 and Rust3 operator sources;
- ProviderReason against the sorted, deduplicated union of pre-Analyze, TS2 and Rust3 Unavailable reasons;
- StageTerminal against the native evidence enum.

The generated enums are exhaustively matched, with Display spellings compared where available. ProviderState retains its independent P3T/T2O check. Registry provenance and reference checks remain in place, and no dependency is added by this revision.

The same-cardinality provider-reason substitution changes registry.rs and both references together. Its registry tests, including drift, still pass (33 tests; passesExitCode 0), while the independent source control fails. The analogous stage-kind substitution has the same result. Source-side reason, terminal and provider-state additions are also caught at runtime. These controls now detect the synchronized drift the prior review identified.

### NBO-1 — resolved

LD-D3A4-3 explicitly distinguishes an admitted pre-Analyze Unavailable from a synthetic crash. The unavailable-early fixture records one unavailable terminal with native-context-mismatch, no fact/coverage frames and zero analysis duration. No crash is synthesized; signal-death still records no stage terminal before Analyze. The pre-analyze-terminal-dropped mutation is caught.

## Regression and self-review

Comparison with round 1 preserves the previously accepted event descriptors, builders, reader descriptors, emission/budget registrations, references, C-2 inventory, signal mapping and record projections. The additional unrelated-base content is CI-2's component_tree declaration and D2b-3b's HostFault variant/arm; both remain intact. The seam remains additive: real codec adoption of Phase, AnalyzeSent and Unavailable stays explicitly carried.

The rules hold: no new mint call outside operability, runtime environment read, let _ = or dependency. The new test's env!(CARGO_MANIFEST_DIR) is a compile-time source location. The permitted operability command independently passes with 114 rows and no findings.

The self-review appropriately excludes ledger charging and syscall error handling for the new clock/record logic. Its measurement boundaries and zeros are disclosed: zero analysis when Analyze was never sent, and a debug-asserted unreachable teardown fallback when both boundaries are absent. The stated untested real codec boundaries, remaining reason/terminal end-to-end cases, out-of-table signal death and real fault-before-terminal ordering are not claimed covered. Production emission, participant adoption and qualification remain separate work.

## Lane evidence and attempt history

Reviewed the pinned final lane evidence without executing builds/tests. All rows pass: components 164 to 176, operability 99 to 100 and platform 343 to 344, with no failures. The serial supervisor record reports base 66/66 and candidate 78/78; only the candidate is the runner's gate. Fixture records, formatting, warning-denied all-targets Clippy, workspace check, focused tests, package/fixture-scope checks, environment check, unchanged census closure and verify_design pass. verify_design reports 52 admission sources and no product qualification.

All 18 mutation logs contain failed tests rather than compilation failures. Inspected the disclosed earlier attempts: attempts 1 and 3 have empty check directories and overlap failures naming platform/lib.rs and components/supervisor.rs respectively. Attempt 2 fails only mutation-controls, with stage-kind-substituted-with-references uncaught; its serial supervisor runs pass. The final runner/control changes address that mutation defect, and the final evidence supersedes it.

Only REVIEW.md and review.json were written. Neither repository, worktree nor control files were edited. No Cargo, rustc, build, lane, network, other pane or delegation was used. No forbidden fixture, installation, signing key, held tree, T2 store or cache was read.
