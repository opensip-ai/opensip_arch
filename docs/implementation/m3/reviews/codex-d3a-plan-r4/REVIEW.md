# D3A-PLAN-r4 review

**Verdict: ACCEPT.** No required findings; one nonblocking clarification. This accepts PLAN-r4 and its narrowly stated M3-D amendment LD-D3A-17 together, as the request specifies. It accepts a plan and amendment, not an implementation or completed D3.

## Exact subject

Verified the 938-byte manifest SHA-256 `42ebdeeaa565c6861b0613b60d6aa6c5315e663cdf6655ab338eaffa8d314a29` and all four members:

| Member | Bytes | SHA-256 |
|---|---:|---|
| PLAN-r4.md | 54,973 | 793d6f02c1a0a353da663d16fb1d17cd42a699ebdf84bbaa7c3a05de723dd6c0 |
| PLAN-r3.md | 52,932 | 63cfd25a805d0a855aa2072eeb9437a9b503eb04a03909438d3d63530c8bc2e9 |
| PLAN-r2.md | 46,262 | 63fa40da2e5d4766f92227d74a013d17791cb85765e2f3cf811730ca435776c1 |
| PLAN-r1.md | 26,606 | 9b2d051d242667b669c2e04d313b7769c8348b23fabd61c4af854df9bae5b454 |

The three historical revisions remain unchanged. Product HEAD is the manifest's `e937dac74c8e529fee3efb6f84439d05280e48ea`; architecture HEAD is its `24fbf182c3d3144d8a159bee7d9d2a0e6418996c`. Reviewed the r3-to-r4 changes against the prior review and the retained plan, including the applicable M3-D and S-OP-2 authority.

## Corrections and amendment

**R3-RF-1 resolved.** LD-D3A-10, LD-D3A-17's replacement item 21 passage and the D3a-3 C-2 controls now consistently specify numeric P0 **K2 Errno**, with the failing call's actual raw_os_error value. The required reason remains **K1 ScratchRetainedReason**, with literal members io-failure and work-exhausted. Errno is present exactly for io-failure and absent for work-exhausted. The typed settlement, conditional descriptor, required-field inventory and tests agree. No new kind or synthetic errno is authorized.

**LD-D3A-17 accepted as a whole.** Its replacements are confined to item 12's scratch fate, item 20's cleanup disclosure and item 21's scratch-retention registration/table. Finite removal work can be exhausted without a syscall failure; the amendment represents that case explicitly rather than inventing an errno. The closed settlement distinguishes Removed, Retained(IoFailure(Errno)) and Retained(WorkExhausted). Removal failure or exhaustion leaves admission unchanged and retains the scratch for item 6's sweep. Measurement exhaustion remains a scratch-bound cause, distinct from removal exhaustion after settlement work.

The event uses existing K1 and K2 kinds and registry-literal provenance, fitting S-OP-2 item 3's ordinary-registration rule. It adds no privacy class, sink, provenance class or SafeField kind and does not alter S-OP-2 item 23's common role/universe or Project/Plan/Execution requirements. The controls cover both valid reason/errno shapes and prohibit both invalid combinations, with C-2 checking kinds and conditional presence. The plan's acceptance gate remains explicit; acceptance here satisfies that plan/amendment review gate only, while the implementation units still require their own checks and reviews.

**R3-NBO-1 substantially resolved.** The build-and-run lane owns the handoff lifecycle, deletes a prior file before building, selects the fixture from the current build's compiler-artifact record, writes its path and content SHA-256, runs the tests and deletes the file. Tests require the handoff and matching bytes. This avoids directory ambiguity and artifact timestamp assumptions, works with reused build artifacts, and introduces no environment read. The harness-free fixture still exits silently with no behavior argument. The outside-lane claim needs the minor qualification below; content matching alone is not proof of an active build invocation.

## Regression assessment and retained scope

The revision changes only the reviewed kind correction, fixture handoff and revision bookkeeping. No regression was identified in the prior plan resolutions: participant-owned incremental provider acquisition, retained pending writes and the one-I/O-call yield contract; normal shutdown separate from the fault ladder; nonblocking reap and custody-preserving abandonment; separate finite no-follow measurement/removal walks; exact required operational fields or explicit blockers; raw fixture byte equality without filtering; pre-write tool materialization accounting; typed payload accounting and one-shot opaque TerminalOutput; and single-owner, exactly-once settlement.

The qualified D3-T3 controls remain consistent: killable/removable fixtures leave no child or scratch, while ceiling/exhaustion fixtures disclose unreaped/retained outcomes, preserve custody and make no later signal or blocking reap. The four-subunit order, D2b-1/-2 integration gates, unresolved event-table blockers, provisional scratch-work policy and X-D3A-1 remain intact. D3b, Linux, C3 materialization, J2 projection/composition and D5 real-codec reruns remain assigned to their respective owners. This review accepts no in-flight D2b implementation, no production caller, no completed item 21 while blocked, and no product qualification.

## Nonblocking observation

### D3APLAN-R4-NBO-1 — Qualify the outside-lane failure claim after an interrupted lane

`docs/implementation/m3/supervisor-d/d3a/PLAN-r4.md:138`

The lane-owned delete/build/write/run/delete sequence and digest comparison establish the intended fixture binding for a normally executed lane, including reused build artifacts. They do not establish that every invocation outside the lane finds no file: the plan itself permits a path file to remain after a killed lane. A direct test invocation before the next lane can read that file and pass the digest check if the fixture bytes are unchanged. The next lane deletes it and restores its own binding. This does not block the lane-scoped fixture design or the scratch amendment.

Describe direct Cargo invocation as unsupported and guaranteed to fail when the handoff file is absent, rather than universally rejected. Explicitly retain the interrupted-lane exception; if rejection outside an active lane is desired, add a separate active-invocation binding in the implementation.

## Boundaries

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, rustc, build, lane, network, other pane or delegation was used. No private 413 fixture, installation directory, signing key, held tree, T2 store or T2 cache was read. Only this REVIEW.md and review.json were written; neither repository, worktrees nor control files were edited.
