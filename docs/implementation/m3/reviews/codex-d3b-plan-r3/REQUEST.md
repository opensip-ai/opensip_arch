# Review request: D3B-PLAN-r3 (tree kill, cancellation, revocation and harness coexistence, M3-D items 18, 19 and 23), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3b-plan-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing, diffing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3b-plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 752 bytes, SHA-256 `857527305a3e6eab16748fb6e360e8b8df123e7f6c857ba6648a4b87b67b8522`. Rehash it. Its 3 members are:
  - `d3b/PLAN-r3.md`, the subject;
  - `d3b/PLAN-r2.md`, history, unchanged from round 2 (SHA-256 `0e11a70a…`);
  - `d3b/PLAN-r1.md`, history, unchanged (SHA-256 `4f0d8cb0…`).
- **Bases:** product main `d704ed4551d65da8be18faf69f4aeed26be369c2` and architecture HEAD `9415426c053c8e2b287022f5db4dd380024d120a`. Both are unchanged since round 2.
- **r3 is narrow.** Diff `PLAN-r2.md` against `PLAN-r3.md`. The changes are the header, a new "r3 changes" table, LD-D3B-9's `revocation.missed` schema, LD-D3B-10's measurement bullet, LD-D3B-13's table count, the RF-1 clock controls in §3 and four mutations. Every other line is r2's.

## Round 2

- **Review:** `/tmp/opensip-implementation/reviews/codex-d3b-plan-r2/` (REVIEW.md, review.json): REQUIRED-FINDINGS, one RF and no NBO. Q10, Q11 and Q12 were accepted.
- **The lead's disposition:**

| Item | Round 2 | Disposition in r3 | Where |
| --- | --- | --- | --- |
| D3BPLAN-R2-RF-1 | The arming-read failure was undefined, and the fallback's quality was invisible in the event | **Fixed.**<br>**Separate paths.** Path A is a successful arming read, with a measured lag and `Instant`-domain timers. Path B is an arming-read failure, which fails closed: every applicable pending mark is missed once, at arming, with `elapsed_status: unavailable` and no `elapsed`. No lag is assumed, no timer is armed, the reference is never reset, and the ladder is unaffected.<br>**Later failures.** A later-read failure in Path A gives a labelled `lower-bound`: the lag plus `Instant` elapsed, which excludes sleep. A successful read gives `measured`.<br>**Valid reads.** A read is valid only with `Ok`, an equal `boot_id`, and no regression below the reference. The reference is the observation's `monotonic_before`, and a read uses its `monotonic_after`.<br>**The event's own status.** `revocation.missed` gains `elapsed_status` (K1, new registry-literal `ElapsedStatus`: `measured`, `lower-bound`, `unavailable`). `elapsed` is optional, present exactly for `measured` and `lower-bound`, behind three typed builders. Only existing kinds are used.<br>**Accounting.** It stays exactly-once, and recovery never revises or repeats an earlier miss.<br>**Controls:** the four requested ones, plus no `measured` without a valid read and no `elapsed` with `unavailable`. Four mutations pin them. | r3 changes; LD-D3B-9; LD-D3B-10 (Measurement); LD-D3B-13; §3 |
| Q10 | Accepted | Carried unchanged to the code units, including the bounded deduplication storage. | (code units) |
| Q11 | Accepted | Carried unchanged: the reason follows the cause, with no duplicate cancel and no fabricated fact. | (code units) |
| Q12 | Accepted | Carried unchanged: the evidence keeps that normal shutdown had completed. | (code units) |
| Review text (RF-3 stamps; no-cgroup check) | Stamp exhaustion must not wrap or coalesce. The check must cover new candidate files and exclusions must not hide production inclusions. | Carried to the D3b-2 and D3b-1 code units as stated in the review. r3 does not reopen those sections. | (code units) |

## Authority

As in round 2, especially:
- SL S6 (`docs/v2/contracts/product-v1/security-and-lifecycle.md`:466-497; the clock at :472-473; the marks at :492-494);
- `crates/platform/src/clock.rs` on main (`ClockObservation`, `monotonic_before`, `monotonic_after`, `boot_id`; `observe_clock` at :68);
- S-OP-2 r6 items 3 to 5 and 23, for kinds, optionality and ordinary registrations;
- D3a-3's typed-builder precedent for `supervision.scratch.retained` (`crates/operability/src/kinds/registry.rs` on main).

## What to review

1. **The fix.** Is R2-RF-1 fixed as required: separate arming and later failure paths; a fail-closed arming failure with no invented lag and no reset reference; the event's own measurement status; a labelled lower bound; the kill ladder and exactly-once accounting preserved?
2. **The schema.** Are `ElapsedStatus`, the optional `elapsed` and the three builders lawful ordinary registrations with existing kinds?
3. **The controls and mutations.** Are the four requested controls, and the mutations, adequate?
4. **Narrowness.** Does r3 change anything outside RF-1's sections?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3BPLAN-R3-RF-n` / `D3BPLAN-R3-NBO-n`.
