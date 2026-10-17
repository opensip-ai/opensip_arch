# D3a-3 r1 review

**REQUIRED-FINDINGS: two P2 findings.** The supplied lane passes, but the tool-record identity path and cancel-write timing need correction before unit acceptance. No non-blocking observations are added.

## Required findings

### D3A3-R1-RF-1 — Tool facts require unavailable provider identities

**Location:** crates/components/src/supervisor.rs:2792; also the shared fact production in append, breached, sample_incomplete and retained-scratch recording.

A normal tool emits ToolSpawned and ToolReaped, but settle_records then unconditionally emits RecordFact::Settled. That fact names supervision.child.settled. The descriptor requires Project, Plan and Execution, plus role and universe fields; emit.rs permits only PlanAttemptScope. Tool execution precedes PlanId and law item 21 explicitly gives its events Project only. ProviderRole contains only TypeScript and Rust providers. J2b cannot supply these missing identities lawfully.

This also affects tool timeout, output-bound, sampling, teardown and retained-scratch paths, which use the common supervision facts. Existing tool tests check the two tool events and absence of provider stderr, but allow the un-emittable supervision facts. The field-name completeness test does not establish that the producing class has the required identities.

**Required:** make tool-produced facts correspond to Project-only registrations. Restrict provider/supervision facts requiring provider identities to provider paths and explicitly register any needed tool-specific records. Do not fabricate a provider role, universe, Plan or Execution. Cover normal and failing tool paths and check every resulting fact against the context actually available.

### D3A3-R1-RF-2 — Queued cancel is recorded as written

**Location:** crates/components/src/supervisor.rs:2280.

send_deferred records CancelSent as soon as send_control succeeds. send_control only queues the encoded frame in control_out at offset zero. Actual writes occur later in write_control. A partial write, WouldBlock, reader closure or abandoned pending frame can therefore yield a cancel.sent fact even though the cancel was never fully written. The write-error branch clears the pending buffer without correcting the earlier fact.

**Required:** associate the cancel reason with the pending frame and emit the fact exactly once at full write completion. Preserve it across partial writes/WouldBlock, and drop it without a sent fact on failure or abandonment. Test the queued, partial, complete and failed-write cases. This concerns record timing; preserve control-session validation and sequence semantics.

## Subject and boundaries

Independently rehashed the 20,842-byte subject manifest (`a6e9a3c5f0a6490af9e82ce04ea910af317ede511c43b689251c243e779985dd`) and all 86 members, with a final rehash. Verified all fifteen candidate/archive product-map pins, edited parents, exact changed-file scope, candidate base f05c5d5cda5f68aec607cdc8731c277e4e29491b, authority pins and integrated base-unit pins. The new path is supervisor_records.rs.

Only read-only inspection, hashing, JSON parsing, Git queries and the expressly permitted operability source census were used. No Cargo, rustc, builds, tests, lane, network, other panes or delegation. No prohibited private fixture, installation, signing key, held tree, T2 store or cache was read. Neither repository, worktree nor control files were edited. Only the two requested review outputs were written.

## Gate, registry and scope assessment

The output capability now owns the non-Clone spool, with private fields and no public mint. Settlement::release checks clean cause, terminal, zero exit, EOF and terminal output, and releases it once. Non-admissible settlements invoke Participant::discard; release drops any rejected terminal output. The supplied D3-T22/T23/T24, bad-commitment and absent-output controls exercise those gates and preserve admission despite removal failure. They remain fixture-scoped; D5 must rerun with the real codecs.

Reviewed the seventeen event registrations, code-table provenance, optional and asserted fields, privacy classes, identity sets, export flags, reader descriptors, emission scopes and per-name slots. The tool domain and Project identity set are ordinary registrations. All seventeen slots are distinct, extending BUDGET_EVENTS from 6 to 23. The macro keeps fields typed and optional fields absent in projections; typed scratch builders enforce the three reason/errno shapes, and typed liveness builders enforce the two provenance shapes. Asserted resource fields are labelled in both references and are not used as progress. The transcribed C-2 inventory and planted missing/extra/optionality/class/event changes are meaningful descriptor controls, but do not detect RF-1.

The three protocol-enum tables are checked against their protocol definitions, including exhaustive generated-enum matches where applicable. The mint-audit delta is confined to registry.rs, an existing mint-owner file: 439 to 444 rows, with the documented new builder definitions and changed macro call/definition counts. All non-owner audit rows and other exceptions remain unchanged. Components gains the permitted normal operability edge; Cargo.lock adds that internal dependency only. No new third-party dependency is introduced.

The four blocked table names are not resolved as authoritative record tables by the inspected pinned contracts, carriers, M3-L or S-OP-2. The existing phase sets, one-member stage vocabularies, terminal-reason enums and sent-signal constants do not designate the required combined tables. Blocking provider.stage.changed, provider.stage.terminal, provider.process.reaped and supervision.progress.absent rather than inventing or omitting fields follows LD-D3A-10. Item 21 is correctly not claimed complete. The three-segment supervision.child.settled registration addresses the documented name-grammar conflict; its required provider identities must still be respected on tool paths.

RecordFact itself contains reduced host-held values and closed codes, with no free text, paths, nonce or environment value. The field-supply control covers the fifteen represented fact variants; the registered cancel.forced and tree.swept runtime observations relate to the later cancellation/descendant work and are not demonstrated by that control. J2b still owns construction and emission with lawful mints. This split is coherent subject to RF-1 and RF-2.

## Values, sampling and routes

Breach values use the observed count/bytes or larger asserted memory value, with the appropriate unit. An unfinished scratch walk does not invent a numeric observed value; the event/cause still records the failure. Wait facts use configured bounds. Participant boundary observations supply ready/start/transfer spans, while asserted resource reports remain separate from progress.

Sampling distinguishes ESRCH from other failures, reports failed listings and unsampled members, suppresses repeated identical incomplete shapes, resets after a complete sample and treats a partial sum above the ceiling as a lower-bound breach. The injected ESRCH, EPERM and listing controls address D3A2-R1-NBO-1. The LivenessMiss mapping preserves window-expiry versus nonce-mismatch and the refusal family, addressing D3A1-R2-NBO-1 without recording nonce bytes.

The outcome helpers separate host pre-spawn/spec/I/O failures from provider-caused routes, check userInterrupted first and preserve tool and zero-fit routes. Actual J1 code projection remains J2's. The C-4 fixture places a canary in stderr and control-fault detail; the supplied control checks its absence, and its digest's absence, from facts/events/settlement. Detail is reduced to byte length. Persisted emitter/read-back composition is explicitly later work.

## Evidence assessment

Independently matched the raw suite logs and comparison records. Components records 98 base passes with 12 failures versus 124 candidate passes with zero failures. All twelve base failures show HandshakeDeadline under load, and every isolated record contains six successful runs, three on each checkout. Treating these as the documented pre-existing timing instability is reasonable for this comparison: the normalized increase is fourteen new tests, not twenty-six new implementations. It is not proof that the base parallel suite passed, and the timing margin remains a D5 concern. Operability records 95 to 99 passes with no failures.

All fifteen mutation logs contain the expected behavioral test failures, rather than compilation failures. Attempt 1's record shows eleven caught mutations; the four uncaught controls correspond to the stale package selection for three registry mutations and the absent-output test gap. The lane of record fixes both and catches all fifteen. Neither mutation set exercises RF-1 or RF-2.

Recorded warning-denied Clippy, workspace check, focused supervisor/registry tests, package edges, fixture scope, rustfmt, ten environment-exception tests, closure check and verify_design pass. Every edited Rust file checked is base-clean/new and candidate-clean. The nineteen-file census closure has no changed-file intersection. The permitted live operability source census passes 114 rows without findings. These checks support the candidate but do not resolve the two semantic findings.

No Linux or product qualification is established. One inventory row, J2b composition, the four blocked events, later cancellation/descendant work and real-codec qualification retain their own owners and gates.
