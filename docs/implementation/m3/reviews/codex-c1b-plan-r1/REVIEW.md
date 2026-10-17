# C1B plan r1 review

**Verdict: REQUIRED-FINDINGS.** Two required corrections and two non-blocking clarifications. Rulings on Q1–Q4 are below. This is a plan review, not implementation acceptance.

Manifest SHA-256: `427ba6eeca4ea1e0fc85ac2f1ea7add3bc30f9bb7211286d054c438d159b5888` (383 bytes). Its sole member, PLAN-r1.md, matches its 19,717-byte length and SHA-256 `72e8a3a80826f3d925be52ed7f4795c1e994bd3ecea0e5722fa8401118cb81de`. The recorded bases are product `23b3871269c6553c96097084dd412b3aa95dec68` and architecture `3b4171a8d887a926c5952937a854b822bb07d5e8`.

## Required findings

### C1BPLAN-R1-RF-1 — C1b-1 also changes the census closure

**Location:** PLAN-r1.md:52, :87–89 and :152.

C1b-1 explicitly appends helpers to custody/git_tracking.rs. That file is already pinned whole in discovery_census.py's CLOSURE at the declared product base (:87). receipt_bindings includes those pins. Append-only helpers change its hash just as other edits do. The current plan refreshes after C1b-0, then integrates C1b-1, but claims census checks remain current outside C1b-0's refresh. In fact C1b-1 requires another closure re-pin and makes the freshly written discovery receipt stale.

LD-C1B-6 also changes the snapshot recipe by adding the VCS term. The companion snapshot validation must describe that final recipe; an earlier C1a4 result is not automatically evidence for additional VCS work.

**Required correction:** allocate the C1b-1 closure re-pin, affected regenerated census records, stale interval and reviewed blind validation/refresh, including the snapshot companion receipt's final recipe binding. Either refresh after this integration or specify an expressly reviewed combined integration batch with all final inputs frozen before its refresh. Preserve pre-run/post-run reviews and the obligation to refresh before another lane relies on a current census. Update the split, ordering, checks and Q3 accordingly.

### C1BPLAN-R1-RF-2 — The ref grammar admits invalid Git names

**Location:** PLAN-r1.md:69.

The declared closed Git-valid subset forbids whole `.` and `..` segments, but does not forbid `..` inside a segment or a ref name ending in a dot. For example, `refs/heads/a..b` and `refs/heads/topic.` pass its listed checks. A reader following that list could resolve such a custody-valid file as HEAD's ref target.

**Required correction:** explicitly reject double-dot substrings anywhere and a trailing dot. Apply the same rule to HEAD's target and names in packed-refs. Add these exact negative cases, distinct from the existing whole-segment and .lock tests, and refuse them as malformed rather than unborn.

## Other assessments

The three-way split is reasonable: first merge/materialize S4 and its consumer joins, then security's Git reads, then host sealing. C1b-1 may be prepared independently of materialization, but its ledger evidence must wait for C1a4's accepted final profile/model; the table's C1a dependency is not proof that the currently open C1a4 step is complete. C1c owns a different sealing step and is not a semantic dependency; the second edit must rebase and preserve the accepted sealing order.

LD-C1B-1 correctly requires a proof derived from the operation's own TrackingObservation and never-reused chain identity, selecting the innermost observed repository rather than accepting a caller's path or rescanning upward. The NoRepository and unobserved routes remain distinct.

LD-C1B-3's admitted member record is the right direction, subject to an explicit same-root composition join (NBO-1). LD-C1B-4 preserves per-read no-follow/custody obligations and an enclosing .git evidence recheck. LD-C1B-5 correctly reuses item 6b's positive marker placement and same-volume reach, rather than calling MemberSession::begin and accidentally re-reading global/environment sources. Member per-read custody remains necessary despite admission at discovery.

The one snapshot ledger, fixed r9 caps and stop-for-law-revision rule are correct. The VCS bound must include path traversal, custody captures, read buffers and parsing/retained data, not just three raw-file lengths. No source supplied a separate unlimited VCS ledger. LD-C1B-8 may leave public routing with J2; equal subject spelling is not route authority. LD-C1B-10's constant Git dirty=true agrees with item 4 and VCS-1, while none/null/false remains the no-repository value.

S4 materialization is correctly assigned to C1b-0: merge the fragment rather than replacing unrelated schema definitions, regenerate carriers, re-pin registries, retain the top-level VCS_KIND_JOIN, and add member joins. Schema 3 applies exactly to a nonempty admitted member set, ordered by path, with the none/null/false workspace top level. The inventory digest remains one whole-inventory digest; no per-member digest or correspondence is introduced. Single-root preservation should be compared before/after S4 for each fixed input (NBO-2).

C1-T15's six observation cases, loose precedence, unborn refusal, custody and evidence-change controls, exact charge tests, C1-T16/17, canonical encoders, S4 negatives and mutations provide a useful implementation gate. Add the malformed-name cases from RF-2 and the complete closure/recipe validation from RF-1. The implementation must preserve budget-before-effect ordering and distinguish failed/malformed reads from true absence. No Git object, environment or global configuration read is authorized by this plan.

## Non-blocking observations

**C1BPLAN-R1-NBO-1 — Bind the member record to this root** (PLAN:75). AdmittedBoundaries has a private constructor but carries a selected_root and may describe another discovery result. State which owner joins it to the exact lent subject/discovery observation, with W2/NoRepository for a nonempty member set. Add a cross-root record control there. Replacing strings with a typed record alone does not prove this association.

**C1BPLAN-R1-NBO-2 — Correct the byte-preservation comparison** (PLAN:118). B-S2 requires identical single-root bytes before versus after S4 for each fixed tracking observation, not identical snapshot2 across different Git/no-repository observations. Compare the schema-2 VCS bytes/digest and full snapshot bytes/ID on both sides with all inputs fixed; separately test the expected kind/commitId/dirty and derived digest changes across observation kinds.

## Open-question rulings

- **Q1:** Accept the explicitly reviewed reuse of the sourced 4 MiB record ceiling for each Git file, with exact-cap/one-over and typed oversize controls and bounded parsing/allocation. It is a new application of an existing ceiling, not an assertion that the index rule already covers these files. C1b-1 must add its complete VCS term and satisfy r9's rule; otherwise a law-record successor is required before proceeding.
- **Q2:** Leave projection with J2's reviewed composition. Do not infer PROJECT.ROOT_CUSTODY_REFUSED from shared subject spelling. Preserve the exact subject, distinguish work exhaustion/I/O and establish the phase-appropriate no-Plan/no-Run route under its owning law.
- **Q3:** One physical blind run can serve a reviewed batch of final inputs and write the required current receipts. It cannot retroactively cover subsequent C1b-1 edits, or silently waive immediate-refresh sequencing. Include C1b-1's closure/recipe change, freeze all inputs, review the batch's ordering and blind mode beforehand, and complete post-review before any dependent lane relies on a current census. Otherwise refresh each intervening stale state as required.
- **Q4:** Accept one symbolic level as an explicit conservative supported layout, with symbolic loose refs/cycles refusing without further traversal. Do not justify it as a universal property of Git. No Git object reader or symbolic-chain implementation is required.

Only read-only hashing, JSON inspection, source/document reading and Git queries were performed. No compiler, Cargo, builds, tests or lanes ran. No prohibited fixtures, installation, keys, held trees or T2 stores/cache were accessed. Neither repository, worktree nor control files was edited. Only the requested REVIEW.md and review.json were written.
