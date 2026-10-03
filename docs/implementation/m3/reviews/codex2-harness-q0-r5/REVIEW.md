# CODEX2 review — M3-Q0 r5

**Verdict: REQUIRED-FINDINGS.** C2-Q0-R4-01 is resolved. The replacement terminal-counter attribution rule has one new required finding: counting births only within the observation window does not exclude a predecessor born before it.

Reviewed subjects:

- `docs/implementation/m3/harness/DESIGN.md`: 111,807 bytes; SHA-256 `d922f5bdea4a640b1f2723900da8bdadd6e4aa5c1c67acda3667bf467732637f`.
- `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json`: 53,696 bytes; SHA-256 `3f79b9797be80fb06f7981344c6d2bc524a61d615dd451f99d6067316b701800`.

Both match REQUEST.md. Retained r4 subjects match `f7afe2755e21c0f11dfb2fb071d4d8a89d293a1932b1590c1ad385df0fa9adec` and `b6c7d8ae34eb0ac4759a3b9ec330cc6b914c69aee2534932d95c08c9c3fb3006`. ENV below means the reviewed r5 schema.

## R4 finding resolution

**C2-Q0-R4-01 — RESOLVED.** DESIGN:740–744,784–795 replaces the impossible notification interval with exact integer equality of the same `/proc` field-22 key. Equal time namespaces, a usable unique key and retained lifetime history are required. Unresolved host values are retained and make the run incomplete. DESIGN:764,865–871 explicitly includes the start-before-notification case. This fixes the host join independently of the terminal-counter problem below.

Field 22 uses the process's boot-time start with the reader's time-namespace adjustment, converted to clock ticks; comparing the same field avoids the prior comparison with a later notification time. [Linux proc source](https://raw.githubusercontent.com/torvalds/linux/v6.18/fs/proc/array.c).

## Required finding

### C2-Q0-R5-01 — One in-window fork does not prove terminal-counter generation (P1)

**Locations:** DESIGN:739,746–757,794. **Relation:** new error in the replacement for fork-timestamp attribution.

DESIGN:739 counts new-group forks between sentinels and then attributes records for a unique TGID “without any ordering.” That count excludes a process born before the window. Such a predecessor can exit during the window, and its TGID can then be reused for a subtree process. Only the successor's birth is counted, while a delayed predecessor record remains eligible for the TGID-only terminal selection at :748–751. QD-28's start key applies to host joins, not to those taskstats records.

A concrete permitted sequence is:

1. Outside process A, with TGID `p`, is already alive when the pre-launch sentinels run.
2. A exits during the run and emits a low taskstats terminal counter. Its record remains pending in the independent userspace receive path. After A becomes reapable, its TGID can be released; its connector exit notification can still be delayed.
3. Subtree B is created with TGID `p`. B is the only new-group fork(`p`) inside the window, so the declared uniqueness check passes.
4. A's taskstats record is consumed after B's fork and accepted as B's terminal record through `ac_tgid=p` and `AGROUP`.
5. B's actual taskstats report is omitted by kernel allocation failure. B's connector exit and all post-run sentinels arrive. A's connector exit can arrive later than the birth-history fences, so it need not expose the predecessor before completion.
6. B has no host entry, as DESIGN:794 expressly permits. Thus exact host-start equality cannot detect the substituted own counter.

Linux v6.18 can fail taskstats packet allocation before allocating its sequence number, and `taskstats_exit` then returns without reporting. This need not produce a receive `ENOBUFS` or a connector sequence gap. [Taskstats source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/taskstats.c).

The kernel performs taskstats reporting before reaping notification and performs connector exit reporting afterward. Therefore the predecessor's counter, reaping, successor birth and delayed connector exit can occur in the order above. The design already acknowledges that connector exits may arrive after post-run sentinels. [Exit source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/exit.c).

There is one accepted terminal record, no duplicate successor counter, and B's required connector exit is present. The stated checks can therefore report complete RSS using A's lower counter. If B's brief peak also falls between concurrent samples, the result can understate RSS and potentially qualify a budget.

**Required change:** establish positive terminal-record identity across the window boundary. One observed birth alone cannot exclude a predecessor. Define how pre-window occupants and delayed outside/pre-opening terminal and exit traffic are excluded or reconciled, or use another generation-safe counter identity. Retaining only traffic already received is insufficient when predecessor notifications may still arrive after completion. Any attribution that cannot be proven must remain incomplete.

Add a design/calibration case covering a pre-window outside predecessor, in-window reuse, delayed predecessor delivery and a missing successor taskstats report. This review did not execute that case.

## Withdrawal and carrier assessment

Withdrawing cross-clock/fork-timestamp attribution is appropriate. Rejecting TGIDs with multiple observed births is conservative and sound. The additional claim that one birth within the window permits attribution without ordering is not established; R5-01 addresses that narrower defect.

The new `host-join-unresolved` reason is admitted at ENV:158 through typed `slotReasons`. DESIGN:824,842–845 maps it to unavailable own high-water sum and peak, retains elapsed/concurrent samples and eligible elapsed aggregates, and keeps the row incomplete and non-Q6. The added acceptance/rejection cases at :866–867 agree with those declared rules. The equality/read/mismatch/namespace examples at :868–871 agree with the host-key method, but do not cover a predecessor born before the window.

These were static checks. No validator or reference implementation was run, and the author's claimed reference execution was not independently reproduced.

## Non-blocking observation

**C2-Q0-R5-N01 — State the PID namespace and proc-view requirement explicitly (DESIGN:740–743,784–785; OI-11 at :1034).** Alongside equal time namespaces, require compatible initial-namespace TGIDs and the corresponding `/proc` view. Connector/taskstats report initial-namespace IDs; namespace-relative host IDs are not interchangeable. “The same pair” can already impose this interface requirement, so this is a clarification rather than a second required finding. [Taskstats source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/taskstats.c), [connector source](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/connector/cn_proc.c).

## Change scope and verification

No substantive changes beyond the table were found. All ten DESIGN diff hunks map to revision metadata/table, lifetime identity and exact host keys, the replacement reuse policy, calibration/reference cases, QD-27's new reason and the QD-28 index. The two schema hunks update its revision/validator description and add `host-join-unresolved`. All 40 object schemas remain closed; no number-typed fields were introduced. R5-01 is within the declared replacement attribution policy.

Review was read-only comparison with retained r4 subjects/review and primary Linux v6.18 source. No product code, tests, builds, validator runs, corpus fetches, benchmarks or runtime-home access; no commits. Only the requested two r5 review artifacts were written.
