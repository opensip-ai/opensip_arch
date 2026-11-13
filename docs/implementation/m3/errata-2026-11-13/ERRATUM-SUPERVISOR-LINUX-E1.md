# Erratum SUPERVISOR-LINUX-E1: "the Linux code is built" was never true (author draft, 2026-11-13)

Status: **PROPOSED.** It implements lead decision LD-DEC-10 item 2 and its addendum "Item 2 resolved"
(`LC/decisions/LD-DEC-10-platform-scope/DECISION.md`, `LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`),
on the facts and wording of `BOTH-LANES-CHECK.md` sections 5 and 6. It is **additive**: the accepted bytes stay frozen.
It is an erratum, not a breach: no unit was accepted on a Linux claim (`BOTH-LANES-CHECK.md` §2, §5).

Corrects two accepted texts:
1. **Law M3-D r5** (the supervisor and common control law), accepted 2026-10-04 by Grok: `docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`,
   209,266 bytes, sha256 `224b9228e9d7c0bc11c848c88cd2ed7fa7da8734208c45d70fbb678a97afec6d`. The live `PROPOSAL.md`
   (209,670 bytes, sha256 `36c26161…`) is r5 plus an acceptance note; its line numbers are r5's plus 2. The same two
   sentences were already in the accepted r3 (`PROPOSAL-r3.md:299`, `:301`, per `BOTH-LANES-CHECK.md` §1).
2. **The M3 unit plan r10**, accepted 2026-10-04 by Codex: `docs/implementation/m3/M3-PLAN-r10.md`, 226,011 bytes, sha256
   `ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964`. A "Planning record: not law, not code, not a contract
   successor" (`M3-PLAN-r10.md:3`). The live `M3-PLAN.md` (226,459 bytes, sha256 `af4f835c…`) is r10 plus an acceptance note;
   its line numbers are r10's plus 2.

**Which record form applies (checked against the product's `design-lock.json` at main `1bd328f3`).** Neither
`supervisor-d/PROPOSAL*.md` nor `M3-PLAN*.md` appears in the design lock. So no passage successor applies.
- The law takes an erratum with an adoption receipt (`ADOPTION-SUPERVISOR-LINUX-E1.md`, not yet written), as
  `../snapshot-plan-c/c2b1a/own-funding-r3/ADOPTION-E1.md` did.
- The plan is corrected the way this repository corrects an accepted plan revision: the accepted `M3-PLAN-r10.md` is never
  edited; findings go into the next revision as record notes. The live `M3-PLAN.md:3` does this for r10's own review:
  "Its two P3 observations go to r11 as record notes: NB-01 … and NB-02 …". So `M3-PLAN-r10.md` is corrected by **a note
  carried into the successor revision r11**, citing this erratum. No r11 exists yet (`docs/implementation/m3/` has
  `M3-PLAN-r1.md` to `M3-PLAN-r10.md` and the live copy).

## SLE1.1 The accepted sentences (verified at architecture main `3dbe61503`)

| # | Where | Accepted text |
|---|---|---|
| 1 | Live `supervisor-d/PROPOSAL.md:347` (r5 `:345`), item 8 | "- **Platform scope at M3:** run and claim only this host's macOS family. The Linux code is built and exercised only on Linux lanes (M3P:472). Windows is outside the population (SL:722-723; CPC:258)." |
| 2 | Live `supervisor-d/PROPOSAL.md:349` (r5 `:347`), item 8 | "- **Controls:** every D1 and D3 test runs on both platform families' lanes. A Linux row that cannot run on this host is reported "not run", never "passed"." |
| 3 | Live `M3-PLAN.md:746` (r10 `:744`), "Choices left open, with lead recommendations" (`:721`) | "- **Platform scope (M3-X).** Recommendation: run and claim only this host's macOS family (NE:157-160). The Linux confinement code is built but exercised only on Linux lanes." |
| 4 | Live `M3-PLAN.md:781` (r10 `:779`), D1b's Linux bullet | "… CF-P's desk check confirms the reading (CFP:293-297). It is built at M3 and exercised on Linux lanes." |

## SLE1.2 Why (evidence)

At product main `1bd328f3` there is no Linux spawn, scratch or confinement code:
- `crates/platform/src/lib.rs:416-418`: `#[cfg(all(test, target_os = "macos"))] mod process_tests;`; `:437-439` the same for
  `confinement_tests`; `:419-420` `#[cfg(all(test, not(target_os = "macos")))] mod unsupported_tests;`.
- `crates/platform/src/process.rs:2545-2640` are refusing stubs; no `pidfd_open`, `PR_SET_CHILD_SUBREAPER`, Landlock or
  seccomp appears in `crates/` or `apps/` (`BOTH-LANES-CHECK.md` §3; I re-read the `lib.rs` lines, not the search).
- The Linux lane compiles 183 gated D1 and D3 tests away (50 spawn, 9 confinement, 124 supervisor; LD-DEC-10 addendum).
  The later measurement (LD-DEC-10, "The measured gap", from `LC/linux/NOT-RUN-HANDOFF.md`) counts 2,031 macOS tests not
  run on Linux in all (2,017 absent from the Linux build, 14 printed "skipped (macOS only)"); the 183 are inside it.
- Every unit deferred its Linux half by name: D1a-L, D1b-L, D3b-L, D5-L (`BOTH-LANES-CHECK.md` §2, with the plan and
  review lines).

## SLE1.3 The amendment

**1. Law, sentence 2 of live `:347` (r5 `:345`).** Before: "The Linux code is built and exercised only on Linux lanes
(M3P:472)." After:

> The Linux halves are owed (D1a-L, D1b-L, D3b-L, D5-L); off macOS the build compiles typed refusals and tests them, and nothing Linux is exercised (M3P:472; erratum SUPERVISOR-LINUX-E1).

Sentences 1 and 3 are unchanged.

**2. Law, live `:349` (r5 `:347`).** Both sentences stay as written. One sentence is added after them:

> Until the Linux halves of D1 and D3 land (D1a-L, D1b-L, D3b-L, and D3a's Linux half, which waits for D1a-L), the first sentence is an open obligation of those units, not a met control, and the Linux lane must report each macOS-gated D1 and D3 row "not run" (erratum SUPERVISOR-LINUX-E1).

The control itself stays. The added sentence is prescriptive: its "not run" half is unmet today because the lane drops the gated rows silently; LD-DEC-10's
addendum fixes that in lane tooling (a not-run count and the names, from the difference between the two lanes' test
lists at one head). That tooling is not this erratum.

**3. Plan, live `:746` (r10 `:744`), record note for r11.** Before: "The Linux confinement code is built but exercised
only on Linux lanes." After:

> The Linux confinement code is owed (D1b-L); no Linux confinement code exists at r10, and nothing Linux is exercised (erratum SUPERVISOR-LINUX-E1).

**4. Plan, live `:781` (r10 `:779`), record note for r11.** Before: "It is built at M3 and exercised on Linux lanes."
After:

> It is owed (D1b-L); no Linux confinement code exists at r10 (erratum SUPERVISOR-LINUX-E1).

## SLE1.4 Owed with the Linux halves (listed, not reworded)

`BOTH-LANES-CHECK.md` §6, verified here:
- Live `supervisor-d/PROPOSAL.md:629` (item 18): "Each case runs on both families' lanes, and macOS rows report their
  expected limitation, never a pass of a guarantee macOS lacks." Owed by D3b-L and D5-L.
- Live `supervisor-d/PROPOSAL.md:913` (D5): "**Where they run.** Ordinary test lanes on both platform families." Owed by D5-L.
- Live `supervisor-d/PROPOSAL.md:1094`: "**Where they run:** this host's macOS family, and Linux lanes (Ubuntu 24.04;
  AL2023 on its 6.1, 6.12 and 6.18 kernels, through DR-126's successor)." The one Linux lane is Ubuntu 26.04
  (`LC/linux/README.md:1`: "Ubuntu 26.04"), and no AL2023 lane exists. Owed with the Linux halves; the distribution
  versions are not reworded here.

These are controls of the `:349` kind, not claims that code exists. LD-DEC-10's addendum says: no rewording beyond
listing them.

## SLE1.5 What this does not change

- No control is removed. `:349`, `:629`, `:913`, `:919` ("a control that passes by not running on a platform" is
  forbidden) and `:1094` stand.
- No unit's scope, gate or acceptance. No product code. No Linux implementation is decided or scheduled; when Linux is
  built is the owner's (LD-DEC-10 item 4).
- `:347`'s cite "(M3P:472)" is kept in the new sentence. It is true as a cite: line 472 of `M3-PLAN-r6.md` is the
  "Platform scope (M3-X)" recommendation (in later revisions it moved: r10 `:744`, live `:746`). That line carries the
  same "is built" sentence, which item 3 corrects in its current place.

## SLE1.6 Review and binding owed

- **Law (items 1 and 2): two fresh reviewers.** M3-D is security-boundary law (confinement, cancellation): OD-PACE-1
  rule 4 (`OD-PACE-1.md:30-31`) and OD-REVIEW-1 item 4 (`OD-REVIEW-1.md:51-58`); LD-DEC-10 addendum.
- **Plan (items 3 and 4): one independent review** (OD-PACE-1 rule 2; the plan is a planning record). The same reviewers
  can carry it.
- **Binding owed:** the lead's receipt `ADOPTION-SUPERVISOR-LINUX-E1.md` pinning this file's sha256; and, when M3-PLAN r11
  is drafted, its two record notes (items 3 and 4) citing this erratum. No design-lock entry.
