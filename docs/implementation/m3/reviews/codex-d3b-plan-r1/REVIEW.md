# D3B-PLAN-r1 review

**Verdict: REQUIRED-FINDINGS.** Four required findings; no non-blocking observations.

## Subject verification and scope

Verified the 380-byte manifest, SHA-256 `d601b12770366661eca0ea3e68e8123a9771aa7d7cb6df90798d214d599d30f4`, and its sole member `d3b/PLAN-r1.md`: 32,980 bytes, SHA-256 `4f0d8cb0b0e57abead364a615d40d8df43e2d6fc81d4b75ed21f43b3f7fdd6c9`.

Judged the plan against product `5de9fd4740ea17018d0bd3fbff9496c94ddacda9`, using Git reads for the platform, clock and supervisor mechanisms. Subsequent D3a-3 and D2b-3b work was treated as named composition context, not as a replacement base. Read the relevant M3-D, M3-L, SL S6, D3a/D2b and S-OP-2 provisions. No implementation or test acceptance is inferred from this plan review.

The split is coherent: D3b-0 supplies bounded mechanisms, D3b-1 implements the macOS descendant policy, and D3b-2 implements user cancellation and observer-triggered teardown. The macOS snapshot/group-kill/identity-check/confirm/reap order, root hold, truthful platform limitation, and Linux deferral align with the law in outline. D3b should reuse the existing trigger gate, table-owned Cancel, normal-end join and D3a-3 records. C4/D4/D2b remain the codec/context producers, J1 delivers signals, SL owns the observer, J2 owns composition/routes, and D5 owns G21 qualification.

## Required findings

### D3BPLAN-R1-RF-1 — Disclose revocation marks whose action never completes (P2)

**Location:** `docs/implementation/m3/supervisor-d/d3b/PLAN-r1.md:162-169`.

The marks are checked only at their completion events. A failed or permanently blocked fd3 cancel has no last byte; an abandoned root has no reap; retained scratch may have no successful cleanup. These are precisely cases in which a required mark is missed, but the proposed event-only checks can emit no miss. The mark-delay control covers late completion, not noncompletion.

**Required change:** Define pending, satisfied, missed and inapplicable marks, with exactly-once miss disclosure when a deadline passes or settlement/abandonment makes completion impossible. Later completion must not duplicate the miss. Define tool applicability explicitly, since a tool has no protocol-cancel leg. Preserve work-bounded scratch removal and do not invent a completion timestamp.

**Control:** Include failed/blocked control writes, an unreaped root, retained scratch and late completion after an already recorded miss, for provider and tool contexts as applicable.

### D3BPLAN-R1-RF-2 — Do not infer per-process signal delivery from snapshot group membership (P2)

**Location:** `docs/implementation/m3/supervisor-d/d3b/PLAN-r1.md:109-111`.

The killed count promises pids to which SIGKILL was sent, but identifies group delivery by pgid at the earlier snapshot. A pid may exit or leave the group before killpg, an identity check may then fail, or the group signal itself may fail. Counting the snapshot member still claims delivery without evidence. Conversely, a process joining the group after the snapshot may receive the signal without appearing in that count. The macOS law expressly distinguishes membership at the moment of the signal from the non-atomic snapshot.

**Required change:** Define an auditable meaning for killed and the exact outcomes used to increment it. Do not describe stale membership as proof of individual delivery or imply confirmed death. If the intended count is snapshot targets covered by an attempted group signal, state that narrower meaning and handle failed calls explicitly; if it is actual successful identity-checked sends, count those outcomes and distinguish group attempts. Keep the existing registered field shape unless a separately reviewed field is needed.

**Control:** Add controls for a snapshot member exiting, changing group, failing its identity recheck, and a failed group-signal call. Repeated confirms must not double-count a target.

### D3BPLAN-R1-RF-3 — Specify the shared ordering of counted user signals and queued triggers (P2)

**Location:** `docs/implementation/m3/supervisor-d/d3b/PLAN-r1.md:127-129`.

A user_signals count beside the queue preserves multiplicity but carries no relative order with faults, revocation or other pending triggers. A signal/fault/signal interleaving and two signals followed by a fault can leave identical count-plus-queue state, while the plan claims firstCause and stage-1/fault escalation follow the earlier merged event. No rule defines how these two stores are merged. The planned burst test only proves the second signal is not dropped.

**Required change:** Define the common linearization and deterministic merge rule for signal arrivals and queued triggers. If gate admission establishes order, retain bounded ordinal metadata for the first and second user signals relative to queued triggers; later signals can remain aggregate counts. Preserve atomic close and exact late accounting. Avoid silently changing the existing queue ordering or losing an admitted later cause.

**Control:** Add deterministic signal/fault/signal, fault/signal/signal and signal/signal/fault interleavings, plus races with settlement close, checking firstCause, later causes, userInterrupted, force timing and late counts.

### D3BPLAN-R1-RF-4 — Do not assume the identity timestamps order descendant creation (P2)

**Location:** `docs/implementation/m3/supervisor-d/d3b/PLAN-r1.md:85-86`.

Item 18 uses pbi_start_tvsec/pbi_start_tvusec for equality at the identity recheck. The cited law does not establish that these start-time values are a monotonic ordering across processes. The new pre-root filter instead treats a lower value as proof of PID reuse and drops the target. Without a platform guarantee covering clock adjustments, this can exclude a legitimate snapshotted descendant from the mandated identity-checked kill. A stricter eligibility filter is not automatically a stronger fulfillment of the kill obligation.

**Required change:** Remove the pre-root timestamp-order filter, or provide a pinned platform guarantee establishing the required monotonic cross-process ordering and address clock adjustment. Keep same-start-time equality, the protected root/pid-1/host guards and the explicitly best-effort macOS standing. Do not promote the timestamp heuristic into proof of ancestry.

**Control:** Cover a legitimate snapshot identity whose numeric timestamp is below the root timestamp in the seam, and separately a target whose identity changes between snapshot and send. The former must not be discarded without the sourced guarantee; the latter must never be signaled.

## Rulings

**Q1:** Accepted in structure. The platform/sweep/cancellation split and D3a-3 dependency are appropriate. Linux stays D3b-L after D1a-L; D5 owns G21 and real-codec qualification. Platform functions must remain caller-bounded mechanisms, with class counts and ladder/report policy in components. Resolve RF-2 and RF-4 before finalizing the mechanism contract.

**Q2:** The two-anchor reading is acceptable under the existing texts: item 14 explicitly gives the abandon ceiling after KILL, while S6 measures its qualification marks from the revoking observation. Keep both visible; a reap after the observation-plus-5-second mark is a disclosed miss, not timely S6 completion. RF-1 must also cover a reap or cancel that never occurs. Observer-fail-stop and revoked remain distinct causes; neither restarts an earlier applicable deadline.

**Q3:** Accepted as an explicit scheduling choice. Reusing the 250 ms cadence for repeated group enumeration is bounded by the existing reap ceiling and creates no new law constant. Continue serving channels/triggers, stop all group signals at reap/abandonment, and require positive root-exit observation plus singleton enumeration before claiming the zombie-root result. A bounded walk/listing failure must remain incomplete even if a later group listing is singleton.

**Q4:** Accepted. Complete the admitted in-band frame, close fd0, then queue the control cancel. The grace starts at the stage-1 transition, not successful I/O, so stalled writes cannot extend it. Escalation must abandon unfinished cooperative writes without completing new frames afterward. The participant seam must carry both cancellation completion and request-side closure semantics, rather than only adding the bool method.

**Q5:** Accepted. A control cancel.sent fact must describe a fully written control frame, with inband true only after the in-band leg completed. If the control leg cannot be sent, do not fabricate control_reason or emit a reduced instance of the registered event. Preserve separate typed leg-attempt/failure observations and any applicable revocation miss under RF-1.

**Q6:** Accepted in policy, subject to RF-3 ordering. Tools have no cooperative protocol leg and may enter TERM/KILL directly. Fault/revocation during stage 1 may force the fault ladder without inventing a ForceTrigger member. Later user signals always set userInterrupted; an already-running fault ladder is not replaced. A second signal during normal-exit grace must still force stage 2 as the plan states.

**Q7:** Accepted. After a verified terminal, leave item 20's literal local admissibility test intact and preserve userInterrupted. J's cancellation latch, interrupted route and FinalGate own whether anything can be published. This is not permission to release cancelled partial output or produce a Run after interruption.

**Q8:** The event/table additions are ordinary registrations using existing kinds and identity sets. There are three event names: tool.tree.swept and the provider/tool revocation.missed pair. RevocationMark is a permissible literal projection of the five S6 marks. Prefer the proposed reduced records plus settlement evidence over settlement-only disclosure, but define applicability and noncompletion as RF-1 requires. The tool variant needs Project only; provider/supervision variants retain their registered common identities. No new mint authority is implied.

**Q9:** Equal identity at the send and exclusion of the supervised root, pid 1 and host pid are appropriate safeguards. The generic platform API must receive enough protected-root context or an owned-child capability to enforce the promised root check; components chooses eligible descendants. The pre-root ordering heuristic is not accepted without the additional guarantee in RF-4. Equality is a best-effort identity check, not proof of complete macOS tree settlement.

## Bounds, records and verification requirements

Four times the class process count gives the proposed walk bounds of four and sixty-four. Caller-sized buffers with an explicit overflow result can implement that bound without unbounded doubling. The implementation must distinguish reaching the walk limit from proving a complete list, account for every inspected/queued PID, and keep the sampler's overflow typed as process-count breach rather than a complete memory sample. No extra ledger is inherently required for a fixed, sourced syscall/space bound.

The plan covers all eight item-23 dispositions: no cgroup mechanism, inherited leaf membership, Linux subreaper deferral, per-child settlement with host-wide joining in J2, unchanged descriptor custody, confinement with O7/K1c/D5, bounded waits, and macOS's explicit limitation. The fixed-list source control must cover every relevant production module, including production inclusions; its own forbidden-token literals and test code must not cause false positives. A compile-time source scan is a structural guard, not Linux harness qualification.

The proposed tests and behavioral mutations cover the main ladder, tree ordering, output/cause separation, exact cancellation writes and platform limitations. Add the four findings' missing cases before the corresponding code unit is accepted. Retain a distinction between root still alive and root dead but deliberately held unreaped, and verify no group signal after the latter is reaped or abandoned. For each descendant action, report syscall outcomes conservatively; neither successful killpg nor a singleton list establishes an atomic whole-tree guarantee on macOS.

The cited 1 s escalation, protocol-specific stage-1 graces, post-KILL ceilings and S6 observation-relative marks are existing authorities. Reusing the 250 ms sample cadence is an explicit implementation decision, not a claim that item 18 itself prescribes it. RevocationMark spells a reviewed literal projection of S6, rather than a new protocol enum. The heading “two ordinary registrations” describes two families but lists three event names; code-unit inventories and drift checks must count the actual names.

No repository, worktree or control file was edited. Only REVIEW.md and review.json were written in the requested directory. No Cargo, rustc, build, lane, network, prohibited private material, T2 material, pane or delegation was used.
