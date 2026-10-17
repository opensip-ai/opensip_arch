# D3A-2-r1 review

**Verdict: ACCEPT-UNIT.** No required findings; one non-blocking observation. This accepts D3a-2’s library changes at the pinned bytes. It does not re-review D3a-1 or claim production composition, Linux support or qualification.

## Subject and boundaries

The subject manifest is 13,196 bytes, SHA-256 `253eeb316d4e24ad30b16a4dd5dd4456704f6ecd8f4f9dcc6dfb3111fb832be7`. All 56 members match their declared lengths and hashes. The candidate is detached at `72e078799b201709b2545ba58cdce3fcd62a933e` and changes exactly the three product-map files, with no new path. Each parent pin matches HEAD; every candidate pin matches the worktree and archived product copy. Source.json’s authority, accepted base-unit and product-lock pins also match.

Reviewed the candidate’s own diff, the cited law and accepted plan, SCOPE, source controls and archived lane evidence. Only permitted reading, hashing, JSON parsing and Git queries were used, plus the expressly permitted candidate operability source check. That live check exited 0 with 114 rows and no findings. No Cargo, rustc, build, test or lane was run during this review. No network, private fixture, installation directory, key, held tree, T2 store/cache, other pane or delegation was accessed. Neither repository, worktree nor control file was edited. Only the requested REVIEW.md and review.json were written.

## Item 16 and provider behavior

The constants match their law rows: 8 GiB resident memory, 250 ms sampling, one provider process and 16 tool processes, TS2 response 1,073,741,824 bytes, both provider scratch limits 2,147,483,648 bytes, tool output 268,435,456 bytes, and tool materialization 32 GiB plus 1 GiB. The tool wall clock is 300 seconds; Waits::TOOL otherwise preserves the release waits. Public preparation selects Limits::RELEASE; the supervision’s actual limits are private and only tests adjust them. No configuration source substitutes a limit.

The sampler runs while the root has no observed exit/reap and before a teardown cause, and supplies the next sampling deadline to the readiness loop. It counts group members against the class limit and saturating-sums successfully sampled resident sizes. Either that observed total or an accepted resourceReport assertion above the ceiling triggers memory-ceiling; a smaller assertion cannot clear an observed breach. Breaches are marked once. The test-only process-count bypass is confined to the four named D3a-1 member-spawning scripts; production always enforces the class limit. Sampling-error handling is the observation below.

TS2’s response total comes from ParticipantStep’s admitted-payload accounting and refuses strictly above its bound. Accounting is applied before the returned participant state can yield a clean end. Rust3 remains governed by its codec’s totals. The controls test exact and one-past boundaries through typed fixture accounting; they do not pretend to stream a real 1 GiB response through a qualified codec.

Provider scratch is measured after reap, before removal, on a discovery-profile work ledger and with the selected protocol’s byte limit. A byte excess, exhausted measurement ledger or I/O failure fails scratch_within. A clean cause becomes scratch-bound and loses admissibility; an earlier failure retains scratch-bound as a later cause. Removal still runs under its separate bounded ledger and retains its existing failure semantics. An unreaped root keeps its scratch and cannot become admissible. The TS2/Rust3 selection and exact/one-past/exhaustion controls are appropriate.

Both preparation paths reject a memory budget below one release ceiling before Prepared/spawn; neither lowers the ceiling. ToolMaterialization uses checked addition, changes its total only on success and reports the prospective observed total/limit on refusal (u64::MAX on arithmetic overflow). Its 33 GiB limit is distinct from provider scratch. The API is the charge-before-write interface; actual writes and their ordering remain C3’s integration obligation.

## Tool class and provider regressions

The tool uses the same state machine, settlement guard, trigger gate, teardown, reap and scratch-removal machinery. Provider-only selection, participant, protocol waits, control session and reader are Options; the tool’s NoProvider type is uninhabited. A tool enters Running immediately after spawn without control traffic. The class-specific descriptor-set check rejects swapped provider/tool descriptors, and the platform’s existing tool pipe discipline gives fd0 immediate EOF.

The loop reads tool fd1 through a fixed buffer with a bounded per-turn service quantum. Each read is charged to ToolOutput before its bytes are appended. An excess records ToolOutputBound, keeps no additional bytes, closes fd1 and starts byte-bound(tool-output). A tool’s ladder starts at T-2, never a control cancel; stderr retains its existing counted/not-held policy. Timers and the other readiness sources remain serviced between turns.

A tool has no terminal protocol frame. EOF plus its own exit permits clean supervision, with the actual exit preserved; a root death whose fd1 remains held beyond the drain is unexpected-exit. take_tool_output releases bytes once only for clean, zero-exit, EOF-observed, within-bound results. Nonzero or signaled exits release none, leaving adapter routing to C3b/J1. A tool cannot satisfy the provider admissible predicate because it has no provider terminal/output. Tool scratch removal does not substitute the provider measurement for materialization accounting.

The provider’s Option conversions preserve its control, handshake, liveness, normal-exit and data-plane paths. The Delivered append now follows the synchronous participant call and precedes applying its returned step, so nested returned effects remain after delivery in the merged stream. The existing tests retain their behavioral assertions; their changes are the protocol/accounting seam, budget field, Option adaptation and explicit four-script count bypass. No new production mint call, environment read, let-underscore binding or dependency appears in the diff. New numeric policy values are sourced to the law; read-buffer sizes and service quanta are implementation choices, not invented policy limits.

## Lane evidence

The lane of record asserts the candidate and clean main checkout at 72e07879. The earlier local WIP-baseline lane is history, not its acceptance evidence. The pinned lane reports all 13 checks passed at nice 10 under its lane hold/private 0700 TMPDIR:

- Components: 77 to 93 passing tests across equal suite sets, zero failures on both sides, 16 new passing tests. Focused supervisor run: 49 passed.
- All three edited Rust files are clean at base and candidate; warning-denied all-targets components Clippy and workspace all-targets check pass.
- Fixture handoffs are deleted before building, selected from compiler-artifact records, hashed and written beside the actual test executable in both checkouts. The script refreshes the candidate handoff for the focused run and every mutation, restores source bytes after mutation, and deletes both handoffs at the end. Neither handoff remains present.
- Package edges and test-fixture feature scope pass; dependencies are unchanged. Environment exceptions, operability, the 19-file discovery-closure check and verify_design pass. The closure intersection was independently recomputed as empty; the mint census remains 439 rows. verify_design reports passed with productQualification false and inventory v221.
- All 14 mutation logs contain actual failed test results, not compiler failures; all controls report caught with no timeout. All 17 fixture-build logs complete successfully. Mutations cover observed/asserted memory, process count, TS2 response, scratch measurement, refused materialization accounting, zero fit, tool output, handshake, ladder, end-of-output classification, wall clock, tool count and descriptor set.

No new inventory path is needed. Records/discard/admission are D3a-3’s; descendant/cancellation/revocation work is D3b’s; real codecs, adapter/materializer and qualification remain their named owners’ work. The sampled ceiling can miss short spikes, and settlement scratch measurement does not promise to stop disk filling before the deadline.

## Non-blocking observation

**D3A2-R1-NBO-1 — Distinguish sampling failures from a member that disappeared.** supervisor.rs:1503, 1525.

A failed group_members call silently skips the sample, and resident_bytes(...).ok() suppresses every per-member error. The comment accounts for an exited-member race, but does not distinguish other native sampling failures. Repeated failures could leave an observed total partial without a reduced indication. The fixture controls establish successful sampling, not unavailable-sample policy.

Before production composition, the supervision owner should specify how non-disappearance sampling errors are distinguished and surfaced, with focused injected-error controls. Preserve the legitimate exited-member race; do not present an unavailable or partial sample as a complete observed sum. This is not a new policy constant or a measurement claim, and does not block this provisional, fixture-scoped unit’s reviewed normal-path implementation.
