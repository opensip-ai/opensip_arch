# Review request: D3B-PLAN-r2 (tree kill, cancellation, revocation and harness coexistence, M3-D items 18, 19 and 23), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3b-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3b-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 566 bytes, SHA-256 `5f9f519d739e4cc65871c24461dbb7341b0eca7a17e919dcca0ad5b77f2dc9c9`. Rehash it. Its 2 members are:
  - `d3b/PLAN-r2.md`, the subject;
  - `d3b/PLAN-r1.md`, history, unchanged from round 1 (SHA-256 `4f0d8cb0…`).
- **Bases:**
  - product main `d704ed4551d65da8be18faf69f4aeed26be369c2`: D3a-3 at `2fbb779`, inventory v227 and S-OP-2c as contract 177;
  - architecture HEAD `9415426c053c8e2b287022f5db4dd380024d120a`.

  `crates/platform` is unchanged since round 1's base `5de9fd4`. r2 re-cites `supervisor.rs` and `supervisor_records.rs` at `d704ed4`.
- **Main may move while you review,** by lock-only inventory commits and by other units' integrations. D2b-3b touches `supervisor.rs`. Judge the plan against `d704ed4`.

## Round 1

- **Review:** `/tmp/opensip-implementation/reviews/codex-d3b-plan-r1/` (REVIEW.md, review.json): REQUIRED-FINDINGS, four RFs and no NBO, with rulings on Q1 to Q9.
- **The lead's disposition:**

| Item | Round 1 | Disposition in r2 | Where |
| --- | --- | --- | --- |
| D3BPLAN-R1-RF-1 | Marks whose action never completes were never disclosed | **Fixed.** Each mark has a state: `pending`, `satisfied`, `missed` or `inapplicable`. Applicability is stated per class: for a tool, `protocol-cancel` is `inapplicable`, and `requests-refused` is structurally satisfied for both classes. A miss is disclosed exactly once, when the deadline timer fires while pending, or when completion becomes impossible. A later completion records nothing. Settlement resolves every mark. Scratch removal stays work-bounded, and `elapsed` is the determination time, never a completion time. The controls cover failed, closed, refused and blocked writes, an unreaped root, each retained-scratch reason, late completion, the tool case and a failed clock reading. | LD-D3B-10's table; LD-D3B-9; §3 |
| D3BPLAN-R1-RF-2 | Delivery was inferred from snapshot membership | **Fixed.** `killed` counts only identity-checked by-pid sends that returned `Sent`, each pid at most once. Step 3 runs once per escalation. Group `SIGKILL` attempts and results, the snapshot outcome, every `KillOutcome` and the late joiners are in the settlement's typed `TreeEvidence`. A failed group call makes the tree `incomplete`. `tree.swept`'s field shape is unchanged (Q10). The controls cover an exit before the send, a group change, a failed recheck, a failed group call, a repeated confirm and a late joiner. | LD-D3B-4; LD-D3B-5; §3 |
| D3BPLAN-R1-RF-3 | User signals and triggers had no shared order | **Fixed.** The gate's critical section is the one linearization point. One stamp counter stamps queued triggers and the first and second signals. Later signals are an unstamped saturating count. The loop merges by stamp at the existing consumption point. The queue's FIFO, capacity and refusal rule are unchanged, and the atomic close counts each entry as late exactly once. Four interleavings are tabulated, and controls cover them, a full queue and the close race. | LD-D3B-8a; §3 |
| D3BPLAN-R1-RF-4 | The start-time ordering filter | **Withdrawn.** Identity is equality only, at the send, with the protected root, pid 1 and host pid. The controls cover a below-root start time that is still killed, and a changed identity that is never signalled. A mutation reintroducing the filter is added. | LD-D3B-4; D3b-0; §3 |
| Q1 | Accepted in structure | Kept. The mechanism contract now reflects RF-2 and RF-4. | §1 |
| Q2 | Two anchors accepted; RF-1 covers noncompletion | Kept. Only the first observer trigger arms the marks, and a later one restarts nothing. | LD-D3B-10 |
| Q3 | Accepted, with conditions | `GroupKilledPlatformLimited` requires a positive root-exit observation, a singleton listing, a `Complete` snapshot and no failed group call. A walk or listing failure stays `incomplete`. Channels and triggers are served throughout, and group signals stop at the reap or abandonment. | LD-D3B-4; LD-D3B-5 |
| Q4 | Accepted, with conditions | `CancelProgress {written, request_closed}` and `Participant::abandon_input()`. The grace runs from the stage-1 transition. Escalation completes no further data-plane frame (see Q11). | LD-D3B-6; LD-D3B-8 |
| Q5 | Accepted | No fabricated `control_reason` and no reduced record. Typed leg events and `Stage1Evidence` are kept. **Found in re-grounding (X-D3B-1):** D3a-3's `CancelSent` fact has no `inband` field, and its doc calls `inband` "always true for D3a's T-1 cancel" (`supervisor_records.rs`:175-176). That contradicts M3-L r7:910 and this ruling. D3b-2 adds the field, and T-1 sets it false. | LD-D3B-8; r2 changes |
| Q6 | Accepted, subject to RF-3 | Each interleaving follows the stamp merge. A second signal in the normal-exit grace forces stage 2. | LD-D3B-8a; LD-D3B-8; LD-D3B-11 |
| Q7 | Accepted | Kept, with the ruling's limits stated. | LD-D3B-8 |
| Q8 | Accepted; three event names | The heading and inventories count three names and one table. `elapsed` and `bound` are defined. | LD-D3B-9 |
| Q9 | Accepted, with protected-root context | `Child::kill_descendant(&self, &ProcessIdentity)`, on the owned child. It refuses the root, pid 1, the host pid, and any call after the reap. | D3b-0 |
| Review text (item 23 control) | Cover every production module; no false positives | The control is a lane check over `git ls-files`. It excludes test files by rule, builds its tokens at run time, and is described as a structural guard only. | LD-D3B-12 |

## Authority

As in round 1:
- **The law.** M3-D r5 (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`):
  - items 18 (:579-628), 19 (:629-663) and 23 (:734-751);
  - item 14 (:479-508);
  - item 4 (:241-264);
  - item 8 (:329-347);
  - item 12 (:419-461);
  - item 22 (:705-733);
  - the units table (:1244-1288).
- **The accepted neighbours:**
  - D3a plan r4 and its review;
  - D2b plan r3 with A1 and A2;
  - M3-L r7 item 16 (`provider-protocol-l/PROPOSAL-r7.md`:942-1013, and its record table at :910);
  - SL S6 (`docs/v2/contracts/product-v1/security-and-lifecycle.md`:466-497);
  - S-OP-2 r6 item 23 (`operability/s-op-2/PROPOSAL-r6.md`:870-905).
- **The product on main `d704ed4`:**
  - `crates/platform/src/process.rs`;
  - `crates/platform/src/clock.rs`;
  - `crates/components/src/supervisor.rs`;
  - `crates/components/src/supervisor_records.rs`;
  - `crates/components/src/control_protocol.rs`;
  - `crates/operability/src/kinds/registry.rs`.
- **In-flight context, not authority:** D2b-3b's candidate in worktree `/Users/sb/code/opensip-ai/opensip-d2b3b`.

## What to review

1. **The four findings.** Is each fixed as required, with its controls?
2. **The rulings' conditions.** Are Q3, Q4, Q5, Q6, Q8 and Q9's conditions applied?
3. **X-D3B-1.** Is the correction of D3a-3's `inband` reading right, and is D3b-2 the right place for it?
4. **New text.** Does the new text introduce any constant, table member, field or claim the law and its sources do not support? In particular: the mark-state table and its applicability, the clock measurement and its failure rule, `TreeEvidence`, and the stamp counter.
5. **The new questions.** Answer Q10, Q11 and Q12 explicitly.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q10": "...", "Q11": "...", "Q12": "..."}}`, with ids `D3BPLAN-R2-RF-n` / `D3BPLAN-R2-NBO-n`.
