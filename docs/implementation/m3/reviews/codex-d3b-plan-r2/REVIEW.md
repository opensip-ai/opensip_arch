# D3B-PLAN-r2 review

**Verdict: REQUIRED-FINDINGS.** The four round-1 findings are addressed at plan level. One new required finding concerns the added clock-failure policy. No non-blocking observations.

## Subject verification

Verified the 566-byte manifest, SHA-256 `5f9f519d739e4cc65871c24461dbb7341b0eca7a17e919dcca0ad5b77f2dc9c9`, and both members:

- `d3b/PLAN-r2.md`: 47,535 bytes, `0e11a70a2c9d669838874c8e9b0826c1370a31d11de06eb661bb2e714fd58144`.
- Historical `d3b/PLAN-r1.md`: 32,980 bytes, `4f0d8cb0b0e57abead364a615d40d8df43e2d6fc81d4b75ed21f43b3f7fdd6c9`, unchanged from the reviewed round-1 subject.

Used product `d704ed4551d65da8be18faf69f4aeed26be369c2` for the revised interfaces. Git confirms crates/platform is unchanged from 5de9fd4. Reviewed the revised plan against the prior findings/rulings, M3-D's descendant/cancellation rules, M3-L's two cancellation planes, S6's clock/mark standing and the existing registry field shapes. D2b-3b remains composition context, not an accepted replacement authority.

## Round-1 findings and ruling conditions

**D3BPLAN-R1-RF-1: noncompletion addressed.** The pending/satisfied/missed/inapplicable states, deadline and impossibility disclosures, terminal resolution at settlement and no duplicate after later completion cover the original missing-action problem. Provider/tool applicability is explicit. Failed/closed/refused/blocked control writes, abandoned roots and all retained-scratch reasons now have controls. The newly added elapsed fallback needs the separate correction below.

**D3BPLAN-R1-RF-2: addressed.** killed now counts observed successful by-pid sends only, with one count per PID. Group results are reported separately; no stale snapshot membership proves delivery. The plan adds typed outcomes, failed-call handling, distinct snapshot status, late joiners and controls for exits, group changes, failed identity checks, failed group calls and repeated confirms. This preserves macOS's platform limitation and makes no whole-tree or death guarantee.

**D3BPLAN-R1-RF-3: addressed.** Gate admission is now the shared linearization point. Queued triggers and the first two signals have stamps, and the loop merges them at its existing bounded consumption point. Queue FIFO/capacity/refusal behavior and atomic close are preserved. The specified interleavings, full-queue and close-race controls cover the missing ordering cases. Implementation must also define stamp exhaustion without wraparound or silently coalescing distinct ordered entries.

**D3BPLAN-R1-RF-4: addressed.** The timestamp-order filter is withdrawn. Equality at the send remains the best-effort identity check. The owned Child method supplies protected-root context and refuses root, pid 1, host PID and post-reap calls. The below-root numeric timestamp and changed-identity controls exercise both sides of the correction.

The Q3 conditions are now explicit: positive root-exit observation, singleton confirmation, complete snapshot and no failed group SIGKILL call. Earlier walk/listing failures cannot be erased by a later singleton. Alive-root versus held-zombie controls are separate. Q4's seam now includes completion, request closure and abandon_input. Q5's no-fabricated-record rule is retained with typed leg evidence. Q6 follows the common ordering, including a second signal during normal-exit grace. Q8 correctly counts three event names and one literal table, with Project-only tool counterparts. Q9's protected-root capability is explicit.

## D3BPLAN-R2-RF-1 — Complete the clock-failure policy (P2)

**Location:** `d3b/PLAN-r2.md:242`, read with LD-D3B-9's elapsed definition.

The plan converts S6 observation-relative deadlines to Instant using a measured arming lag, then says any failed clock read emits the arming lag plus Instant elapsed as a lower bound. Failure of the initial arming read leaves no measured lag, so that fallback is undefined. A later clock failure has a different information state and needs a distinct rule.

There is also a record-level meaning mismatch: elapsed is defined as the measured observation-to-determination duration, but the fallback is only a lower bound. Settlement-only RevocationEvidence does not label an independently emitted revocation.missed event. A consumer cannot infer the quality of that required numeric field from the event itself.

**Required change:** specify initial and later read failures separately. An initial failure must fail closed for applicable pending marks without inventing the missing lag, resetting the observer reference or blocking the kill ladder. Define the available timing evidence and expose its quality/availability in the proposed ordinary event registration, or provide a distinct lawful clock-failure disclosure. A lower bound must be named and labelled as a lower bound rather than silently taking the exact elapsed field's meaning. Existing SafeField kinds suffice; no new kind or profile is requested.

**Controls:** failure of the first arming read, failure after successful arming, repeated failure through settlement and recovery after disclosure. Verify emitted fields, no invented duration, no timer restart and exactly-once miss accounting.

## X-D3B-1 and new text

The inband correction is right and belongs in D3b-2, the unit joining the two cancellation planes. At d704ed4, the registered SupervisionCancelSent event requires inband, while RecordFact lacks it and supplies() says it is always true for D3a's T-1. That is wrong for fault teardown, which sends no in-band Cancel. Adding the boolean to the fact, making T-1 false and making cooperative cancellation depend on actual completion removes the ambiguity before J2b emits it. The mutation and write-completion controls should pin both true and false cases.

The mark states, KillOutcome, TreeEvidence, CancelProgress and stamps are internal mechanism/evidence vocabulary, not invented public protocol members. RevocationMark's five literal members and bounds remain S6's; the three event registrations use existing kinds and the appropriate identity sets. The proposed conservative miss policy does not make an observation failure proof of an actual elapsed-time overrun; that distinction is why RF-1 matters.

The two-anchor reap interpretation and macOS/Linux scope remain as ruled. No complete Linux or real-codec qualification is claimed. The no-cgroup check is a structural guard; the implementation lane must cover newly added candidate production files as well as tracked existing files, and verify that exclusions cannot hide a production inclusion.

## New rulings

**Q10:** Accepted. Keep the existing three-field tree.swept shape, with killed explicitly counting distinct successful identity-checked by-pid sends rather than group delivery or deaths. Typed TreeEvidence may carry the snapshot outcome, group-call results, by-pid outcome counts and deduplicated late-joiner counts. No new event field is required for this unit. Keep raw orphan PIDs out of operational records, and make any later J2 projection an explicit reviewed registration. The code unit must bound internal deduplication storage as well as the listing buffers.

**Q11:** Accepted. Abandoning unfinished cooperative input means no further data-plane frame is completed. It does not prohibit the control plane's one teardown announcement. On escalation, drop the pending in-band write and close fd0; queue the not-yet-queued control cancel through the existing ControlSession only, and append its typed outcome. Do not duplicate an in-flight/written cancel or restart either grace. The cancellation reason must follow the cause: user for user-driven forcing; supervisor-fault for an observer/fault-driven T-1 when no prior cancel exists, as LD-D3B-10 states. Preserve validated sequence order and do not fabricate a sent fact.

**Q12:** Accepted as the declared conservative disclosure policy. A provider whose normal end already closed fd3 cannot complete a new protocol-cancel leg; marking it missed-by-impossibility, rather than silently treating every closed control channel as inapplicable, is safe and explicit. The evidence must retain that normal shutdown had already completed and no cancel was writable. It neither authorizes another control write nor changes a clean local admission result or the existing revocation/interruption projection. A tool remains inapplicable because it never had that protocol leg.

No repository, worktree or control file was edited. Only REVIEW.md and review.json were written in the requested directory. No Cargo, rustc, build, lane, network, prohibited private material, held tree, T2 store/cache, pane or delegation was used. This is a plan review, not implementation or product qualification.
