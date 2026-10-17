# D3A-4-r1 review

**REQUIRED-FINDINGS.** Three required findings and one non-blocking observation.

## Subject and verification

The 20,964-byte manifest hashes to `27819282a9b8821dc54d0c8f11f6cc1ced7f94ed4c5e8ea59454261b41051736`. All 86 members rehash exactly. All 16 product-map parent, candidate and archive entries match. The worktree is detached at `2ead5cf1796bb85f363c34fa8ff8fba715462369`, with exactly the mapped changed files and no new path. All ten source.json authority/base-unit pins and the product design-lock pin match.

The permitted operability source check passes live: 114 rows, no findings. I did not run Cargo, rustc, builds, tests or the lane. Other work was read-only reading, hashing, JSON parsing and Git queries. No network, other panes, delegation or prohibited private/store material was used. Only REVIEW.md and review.json in this review directory were written; neither repository nor any worktree/control file was edited.

## Required findings

### D3A4-R1-RF-1 (P2): Keep the last admitted progress time separate from the absence-report timer

Location: `crates/components/src/supervisor.rs:1623-1636, 2378-2385; crates/components/src/supervisor_tests.rs:3344-3363`.

The absence branch computes since from last_progress, then assigns last_progress = now even though no admitted transition occurred. With no intervening progress, reports at approximately I and 2I therefore both claim since approximately I. SOP2:906 and LD-D3A4-4 require time since the last admitted transition, so the second must report approximately 2I. The current control only asserts each span is at least one interval; the mutation replaces the span with zero and does not detect this reset.

Required: Retain the last admitted progress/transition timestamp until actual progress changes it. Use a separate notification/deadline timestamp to rate-limit absence reports without creating a busy loop. Add a deterministic two-or-more-interval control that checks increasing since from the original transition, then checks a real transition resets the span and report schedule.

### D3A4-R1-RF-2 (P2): Capture terminal time even when teardown already has a cause

Location: `crates/components/src/supervisor.rs:2481-2488, 2913-2919`.

reach_terminal records the terminal but returns before setting terminal_at when first_cause is already present. ProcessReaped later uses terminal_at.or(teardown_from), so a terminal admitted after a fault is measured from the earlier trigger instead of that terminal. This is reachable: turn consumes a HostFault trigger before wait_and_service, and service_data_read still admits a participant terminal during teardown. A Complete already in flight can therefore produce a stage terminal while its teardown span includes the pre-terminal interval. M3-L:402 and LD-D3A4-4 select the terminal boundary when there is a terminal; the first-trigger boundary is the fallback when there is none.

Required: Record the actual first-terminal observation time independently of the normal-exit grace timer, or otherwise preserve the existing grace behavior while supplying the correct measurement boundary. Add a controlled fault-before-terminal case with a known intervening interval and a no-terminal case proving the trigger fallback. Keep the first cause, ladder timing and single terminal fact unchanged.

### D3A4-R1-RF-3 (P2): Add the required source equality checks for the new protocol-enum tables

Location: `crates/operability/src/kinds/registry_tests.rs:301-306, 1309-1427; S-OP-2 r6:217, 939; S-OP-2c item 23a`.

The registered literal values match the authorities now, but C-2 does not independently compare all new protocol-enum tables with their pinned sources. ProviderReason is checked only for length 11 and exercised with capability-missing; there is no comparison with the union of PreAnalyzeUnavailableV1, TypeScriptUnavailableV2 and UnavailableV3 reasons. StageKind is compared with a handwritten literal rather than both operator sources, and StageTerminal with a handwritten six-member list rather than its protocol enum. The reference renderings are generated from the registry itself, so synchronized registry/reference drift can pass. ProviderState does have an independent P3T/T2O phase check in components; that does not cover these other tables. S-OP-2 item 3/C-2 and S-OP-2c explicitly require enum/union equality, not just lengths or self-rendering agreement.

Required: Add independent member-by-member checks against the pinned schema/generated enum sources for StageKind, ProviderReason (the full union, in selected order) and StageTerminal. Keep provenance checks and reference equality. Demonstrate that a same-cardinality member substitution or source-enum addition is detected even when registry references are regenerated; do not introduce a new third-party dependency.

## Other conclusions

The five tables' current members and order agree with the selected sources: StageKind has semantic-provider; ProviderState has P3T's 22 phases in order and covers T2O's subset; ChildSignal has the chosen 20 literals; ProviderReason has the exact eleven-member admitted-reason union; StageTerminal matches the six-member native schema enum. I independently parsed the phase lists and reason schemas and checked the JSON reference table members against the registry. The provenance labels are correct. ChildSignal's registry comment incorporates SOP2C-R1-NBO-1's chosen-common-subset wording. Leaving Signal to host.signal.received's owner is consistent with LD-D3A4-1. RF-3 concerns durable C-2 enforcement, not a current incorrect member.

The four event descriptors match SOP2:879-881/:886 as amended: role/universe, kinds, P0/P1 classes, optionality, levels, Project/Plan/Execution requirement and export candidacy are preserved. ProviderStageTerminal's public builders require a reason for unavailable and prevent other() from constructing unavailable. The provider/tool reap builders derive optional signal presence from ReapedExit. ToolProcessReaped's optional ChildSignal is an authorized ordinary field addition. The new PlanAttemptScope registrations occupy unique slots 29–32, and BUDGET_EVENTS is 33. The reader descriptors and public reexports include the new fields/types. The C-2 event inventory and JSON/Markdown references include all four full descriptors and the tool signal field; no reduced event form is introduced.

TerminatingSignal::of compares only the pinned libc constants on macOS/Linux and returns None for other values; unsupported targets map nothing. Its macOS control checks SIGBUS=10, SIGUSR1=30, representative other members, excluded SIGEMT/stop/continue/zero and a count of twenty mapped values. No Linux qualification is implied.

The participant seam is additive: Boundary gains Phase, AnalyzeSent and Unavailable; no trait method, step field or prior variant changes. records::provider_state is an explicit phase-name map, with an unknown-name refusal and independent vendored-table controls. D2b-3b and D2b-4 still must adopt these boundaries. Phase facts suppress repeated phases; counts derive from admitted FactBatch/Coverage progress; terminal facts are single-shot, with crash synthesized only after Analyze when no terminal was recorded. StageKind is semantic-provider, and the new provider/supervision facts require Project/Plan/Execution and are filtered out for tools. The span defects are RF-1/RF-2; pre-Analyze terminal wording is NBO-1.

Item 21's previously blocked four registry descriptors are now complete alongside the existing provider/supervision set. This does not complete production recording: J2b emission, participant adoption and D3b's remaining producers are still carried obligations. No new mint outside operability, runtime environment read, `let _ =`, dependency or inventory path is introduced by the diff. The audited operability definition additions are the two of builders, other and unavailable, and the live mint audit passes. The existing readiness loop, gate, ladder, discard, resource enforcement and tool separation are otherwise retained; the timestamp fixes must preserve those behaviors.

## Lane evidence

The packaged lane reports all 17 check rows passing. Components passed 133 candidate tests versus 105 base passes plus 22 base failures; each of those 22 tests has an archived six-of-six isolated-pass record across base/candidate. That supports the runner's normalization to six new tests, while preserving the disclosed startup-timing limitation. Operability is 99→100 and serial platform 331→332. These are archived results, not a fresh test run by this reviewer.

I checked all eight mutation logs: each has actual failing tests, no compile failure, no timeout, and the controls file reports all caught. They cover repeated phase facts, missing unavailable reason, missing crash, dropped signal, zero since, dropped frame counts, an exited provider given a signal, and a handwritten signal number. They do not cover cumulative since, a fault before a late terminal, or synchronized table/source drift.

The evidence includes the exact fixture artifact/digest records, warning-denied all-targets Clippy, workspace and focused checks, package edges, fixture feature scope, environment exceptions, source/mint census, unchanged closure and verify_design. All 13 Rust formatting rows report base-clean and candidate-clean. Package edges remain contracts/identity/operability/platform, and test-fixture is enabled only from components' dev-dependency. The runner checks main/candidate path disjointness under its lane lock before moving the candidate to main; Git independently confirms 274dccc→2ead5cf changes are disjoint from this subject's paths. The initial stopped wait and the second attempt's compile-only mutation are explicitly disclosed history; the final plain-exit shape control and runtime mutation address that stated gap.

## Non-blocking observation

**D3A4-R1-NBO-1 (P3): Clarify the pre-Analyze unavailable case in the scope record.** The sentence that a provider which never analyzed records no terminal is broader than the implementation: reach_terminal records an admitted pre-Analyze Unavailable too, with zero analysis duration. That terminal is a real protocol possibility, and S-OP-2c explicitly includes PreAnalyzeUnavailableV1 as a reason source. The analyzed-only guard applies to the synthetic crash fallback. Clarify that distinction rather than treating a startup failure and an admitted pre-Analyze terminal as the same case.

Requested: State the intended pre-Analyze Unavailable behavior explicitly and add its fixture control alongside the existing pre-Analyze signal-death/no-terminal case. Preserve the admitted reason and do not synthesize crash for a provider that never analyzed.
