# GROK2 review: M2 completion record, r1

**Verdict: REQUIRED-FINDINGS.**

Subject `docs/implementation/m2/M2-COMPLETE.md`, 53199 bytes, sha256 `957d300264d4f3cee3173f6d8fd6e06df01f028fc7fc4481561a19949c4935cf`. EXIT-PLAN `docs/implementation/m2/EXIT-PLAN.md`, 32329 bytes, sha256 `edf062eed3c6a712cfec55af54cc9fca36964d34b927ddbb2fbe7ff37ec16083`. Both match `hashes.txt`. Product main is `3e64266aa8729160cd22509dcfff95a3bb09fcea` (2026-10-04 01:09:37 -0700). Matrix commit C is `3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f` (2026-10-03 23:46:08 -0700). `git diff --stat 3d2d5b5 3e64266` is the three files §6 names (`design-lock.json`, `tools/contracts/dependency-policy.json`, `tools/identity/dependency-policy.json`; +58 −6). `~/Library/Application Support/OpenSIP` was absent. No cargo, tests, or crash-matrix run. `verify_design` was re-run at `nice -n 19` on the product checkout and matched §6.

The crash-matrix evidence, the 62-row inventory chain, the 19 law-acceptance rows, the L1–L11 owners, and the `verify_design` counts are right. The record was marked COMPLETE while several of its own sentences, and the EXIT-PLAN status cells, still describe the rerun and the four lead decisions as unfinished. Those sentences are required findings.

## What holds

**§1, except claim 5's relationship to §3.3.** BP:886 is the M2 row: admission and durable publication; the demonstration is opaque API refusal tests and the crash/lock/revocation matrix, with synthetic fixtures labelled and not compiler qualification. Gate execution is M6 (BP:895). `productQualification` is false in `check.json` and in `verify_design`. X8 r5 "Not claimed" excludes every toolchain other than rustc 1.95.0. D-372 condition 4 and the implementation-authorization sentence match the quoted text. The six M2 gates in §2.5 are the six EXIT-PLAN release-gate rows (DR-G07, G09, G11, G19, G24, G27).

**§2.1.** X8 r5 sha256 `ba6915b9…` matches. Fixture files at `3e64266`: 108 under `crates/host/tests/refusal/cases/` (security 58, storage 21, host 10, platform 10, evaluator 9) and 8 under `refusal/selftest/`. `admission_tests.rs` names `synthetic_b0_…` through `synthetic_b8_…` (two B3 cases). The fixture-adding commits are the seven §2.1 names. X8c's REQUEST.md:131–133 records workspace 1726 passed twice, crash-matrix 1611, and the scenario-fixtures lane 1139.

**§2.2 numbers.** Evidence directory at arch `5c703071d`: 490 files, 22,699,067 bytes. `hashes.txt` is 66611 bytes, sha256 `97f8367e…`, 491 pin lines (489 evidence files, `hashes.txt` itself unpinned, plus both product `required-runs.v1.json`) and a trailer line naming commit C. `check.json` matches the lead table, including both census traces (`e9add21e…` / 1379 records, `93d0922a…` / 1195 records). All 479 run records are verdict PASS, labelled `synthetic` and `scripted-clock`: process-death 320+81, mutation 40+77, injected 12+7. Each states macOS 27.0 (26A428), arm64, filesystem `apfs`, fixture `synthetic-signed-v2`, profile `BASELINE-ATTESTED`, rustc 1.95.0, feature `crash-matrix`, and `worktreeClean: true`. Storage required runs are 381 and host 98. The singular `unit` field marks 46 storage runs and 4 host runs as X9-6. The earlier reviews state X9-2 231, X9-3 57, X9-4 47, and X9-5 94, so 231+57+47+46 = 381 and 94+4 = 98. X9-2 through X9-5 `review.json` scopes match the agreement claims, including the shared release binary 6315264 / `b32604fe…`. X9-6 r1 is ACCEPT-UNIT and its REVIEW.md "Rerun timing" defers the two full sets to C. `release-absence.json` sha256 `538a10c4…` matches the binary, the empty `found` list, 26 strings, and `featureBuildRefused: true`. Lead durations 1959 s, 1921 s, 811 s, and 801 s are in `OVERNIGHT-2026-10-03.md`.

The rerun values that were filled match `/tmp/opensip-implementation/reviews/grok-crash-matrix-x96-r2/review.json` and that review's REVIEW.md: verdict ACCEPT, required findings empty, reviewer pair, mixed pair, and lead pair all true, 479 equal and 0 differing in all five pairings, evidence sha `97f8367e…`, release binary 6315264 / `b32604fe…`, both feature builds refused. Arch `50047b7ed` (2026-10-04 03:00:23 -0700) records that review. Its `status.json` is ACCEPTED.

**§2.4.** Line counts at `3e64266`: `replay.rs` 335, `fact_admission.rs` 180, `commit.rs` 808, `recover.rs` 482, `finalization.rs` 571. The four named owner paths are absent. `installation_lineage.rs:68` is `capture_descendant`; the file's last change is `b230250`.

**§3.1.** All 19 rows: the named arch commit's date matches, `status.json` is ACCEPTED, and the review verdict is ACCEPT (split reviews under `x3b/`, `x3d/`, `x6/`, `x7/`, `x9/`, `ec1/`; EC1 is ACCEPT-DESIGN-UNIT; 463 r9 and X4B r5 are both ACCEPT; VD1 law and tooling are both ACCEPT).

**§3.2.** `d4239a5..3e64266` is 62 commits, in the table's order, each once. At every commit the inventory cell matches the `design-lock.json` delta (new inventory version, selected version where the cell says `none (vN)`, and each named contract successor). Where a row adds an inventory or contract successor, the bound review path contains the named review directory.

**§4.1 owners.** L1–L11 `owner` strings are identical in `storage/matrix.json`, `host/matrix.json`, and both `lead-2` copies, and they match the "Recorded owner" column verbatim. L11's three families match X9 r16 item 10. `MAX_LINEAGE_NODES` is 64. Law 464 returns backup classification `UNKNOWN`.

**§6 counts.** v134 is 552176 bytes, sha256 `626cd719…`, 968 planned files. Main tracks 861 files. `verify_design` at `3e64266`: passed true, productQualification false, 76 contract successors (69 at `d4239a5`, plus 461b, X10b, X12-0, D1, D2, EC1, D3), 94 inventory successors (55 at `d4239a5`), inheritance 55, supersessions 21, inputsVerified 46, application manifest `dab6e00f…`, selected inventory v134. The X9-6 pre-integration lane table matches `grok-crash-matrix-x96-r1/REQUEST.md` "Lanes". EXIT-PLAN is absent from product `design-lock.json` and from `application-subject.v46.json`.

**§8, the parts that are real.** The ten EXIT-PLAN git dates are 2026-10-01, not the 2026-10-03/04 dates in the bullets. The cited law headers do carry the later dates (X9 r2/r3, X3d r7, X7 r6, X11 r1, VD1 r1, X8 r4's "2026-10-04" against an acceptance note of 2026-10-02). The listed missing `status.json` files are absent. The listed stale `status.json` values match. `grok-crash-matrix-x96-r1/status.json` still has a `pending` member naming the final lead sets, the evidence record, and the rerun. `staged-notes.patch` has 11 hunks: README, 02, 05, 08 ×5, 10 ×2, 12. Arch `1648ceb7e` accepted F8b r2; that review's `status.json` is ACCEPTED.

## Required findings

### RF-1. The rerun is accepted, and the record still says it is pending

`reviews/grok-crash-matrix-x96-r2/review.json` is verdict ACCEPT with `requiredFindings: []`. Arch `50047b7ed` copied it in on 2026-10-04. The status line says COMPLETE.

These sentences still say the opposite:

- The preamble (lines 7–12) still says that until the rerun returns the record claims nothing beyond the lead's evidence, and it still describes finalization as future work.
- The token table's `[[RERUN:date]]` and `[[RERUN:arch-record]]` expected values are still `—`. §2.2 already states 2026-10-04 and `50047b7ed`. §9 allows the token names to remain inside that table; these two cells were not filled.
- §2.2's rerun heading is still "PENDING."
- §3.2 row 60 still says the rerun is PENDING.
- §5 row 1 still says "owned, in progress" and "M2 completes on its acceptance."
- §9 is still a checklist of work the lead has not done ("When Grok's rerun returns", "Change the status line to COMPLETE", "On GROK2's acceptance").
- EXIT-PLAN's X9 status cell still says the rerun is PENDING and that M2 completes on its acceptance.

### RF-2. "No deferral record" is false inside this same record

§3.3 says the record of deferral is **None** for X3a-2, X4b, and X4T-c. §8 item 4 repeats "never built, with no deferral record."

§1 claim 5 and §5 rows 13–16 are those deferral records: lead decisions dated 2026-10-04, each with a rejected alternative. X3a-2 is deferred to a post-M2 unit before M3-C1. X4b is deferred to M3-B3 and M5-EX. X4T-c is scheduled after F8b. X4 F-1 is deferred to X4-F1. M3-PLAN r6 does schedule them (M3-PLAN.md:160 and the carry-in table).

EXIT-PLAN's refreshed X3a, X4, and X4T cells still say there is no deferral record and that each needs a lead decision. That was the draft's wording. The finalized record's §5 has the decisions, and the finalize commit `3e6c40ad` did not update those cells.

### RF-3. The M3 citations say there is no unit row, and they point at the wrong lines

Accepted M3-PLAN r6 names the owners:

- The resume/repair writer is J-RW and J4 (M3-PLAN.md:158, the M3-J row, and the carry-in row at line 238).
- The X3c re-commit successor is X3c r8 and X3c-3 (line 159, and the carry-in row at line 239).
- X12d is C4b (lines 157 and 212), not C4.
- J1 is named at line 149 and in the M3-J row.

The completion record says otherwise:

- §4.1 L11 "When" cites `m3/M3-PLAN.md:112` and says no M3 unit row names it (M3-PLAN:156–173). Line 112 is "No command. Every analysis command is M4 or later." Lines 156–173 include line 158, which names J-RW and J4. This "When" cell is not marked as an inference.
- §5 row 10 cites M3-PLAN:112 and says "No unit row yet."
- §5 row 11 cites M3-PLAN:113 and M3-PLAN:255 and says "No unit row yet." Line 113 is the quality-plan heading. Line 255 is "J-RW and J4 apart from J3." Line 159 names X3c r8 and X3c-3.
- §5 row 7 gives the owner as M3-J1 at M3-PLAN:170. Line 170 is the `configuration.rs` product-state row. The owner name J1 is right; the line is not.
- §5 row 9, §3.3, and §2.5 call X12d "M3-C, unit C4" and cite M3-PLAN:208. Line 208 is the M3-L row. The M3-C row (line 212) says **C4b = X12d**.
- §5 row 9 also says `snapshot-plan-c/PROPOSAL.md` item 19 is r1 and that CODEX2 returned 4 required findings (`codex2-snapshot-plan-c-r1`, arch `7615a496b`). That r1 result is real: status REQUIRED-FINDINGS, four findings, and `7615a496b` is the arch commit. The current proposal is r5, and `codex2-snapshot-plan-c-r5/status.json` is ACCEPTED (the law's own gate still waits on M3-L and X12 r4). The row does not record r2–r5.

### RF-4. §6 both denies a lane at `3e64266` and then states one

§6 says "No cargo lane is recorded at `3e64266`" and then says the lead ran workspace 1744 passed, 0 failed, 3 ignored, and the crash-matrix lane 1624 passed, 0 failed, 3 ignored, on main on 2026-10-04, with clippy, fmt, and `verify_design` clean.

`OVERNIGHT-2026-10-03.md` records the main run as "workspace 1744/0, crash-matrix 1624/0, clippy, fmt and `verify_design` all clean." It does not state 3 ignored. Those ignored counts are the pre-integration worktree lanes in `grok-crash-matrix-x96-r1/REQUEST.md`, which §6 already reports in the lane table. The main-run sentence has no citation, and its ignored counts are not in the overnight sentence.

### RF-5. §5 omits X4-F2 and F9

EXIT-PLAN lines 209–211, added at arch `ebfb0f12` (2026-10-04 02:08), record two open follow-ups found by X4-F1: X4-F2 (fenced-read expiry flags computed and not applied) and F9 (X4T-0 fixture dates refuse native-clock lanes from 2026-12-30). The overnight log schedules X4-F2 before J2 and F9 by 2026-12-01. M3-PLAN r6 schedules both (line 160 and the carry-in table). §5 has no row for either. §5 row 16 covers X4 F-1 only.

### RF-6. §8 item 7. F8b's status line is not "DRAFT r2"

§8 item 7 says `generator-closure-f8b/PROPOSAL.md` still reads "Status: **DRAFT r2 for review**". At the finalize commit `3e6c40ad`, and now, the status line reads "Status: **r2 ACCEPTED by CODEX2 (2026-10-04); execution pending.**" `codex2-generator-closure-f8b-r2/status.json` is ACCEPTED. Arch `1648ceb7e` is that acceptance. The discrepancy as written is not in the file.

### RF-7. §8 item 5. The X9 r16 status hash is not a 12-character prefix

§8 says `grok-crash-matrix-x9-r16/status.json` records a 12-character subject prefix `f08efe95deba`, while `review.json` has the full value. `status.json` `subjectSha256` is the full `f08efe95deba681f2940a043c80c91b4faae4e4c804ca5865c024e0e083c0a85`. `review.json` has the same full value.

### RF-8. The EXIT-PLAN status refresh does not match the finalized record

The commit that lands the finalized record is `3e6c40ad`. Its parent is `494092761`. That commit does not change EXIT-PLAN. The status-column edit is the earlier commit `5df50f35` (parent `28e46fec5`). That diff changes only the status cells, pads X4T-0, X4T, X4B, and X12 from four cells to six, and adds one note line after the table.

Current EXIT-PLAN also contains `ebfb0f12`'s new follow-up bullet (X4-F2 and F9). §7 says no other section changed and that the dated follow-up bullets were left as they were. That is true of the `5df50f35` diff and false of the current file against the pre-record parent.

Status cells that are wrong now:

- X9: rerun PENDING (RF-1).
- X3a, X4T, and X4: "no record defers it" / "needs a lead decision" (RF-2).
- X2: "X2 r9, drafted inside M3-B r1". X2 r9 was accepted at `494092761` (2026-10-04 03:17:53 -0700), the parent of the finalize commit. The cell still says drafted.
- X12: "X12d is now M3-C, unit C4". The accepted plan's unit is C4b (RF-3).

§7 says the column was refreshed to match §3 and §5 in the same change as this record. The finalize commit did not touch EXIT-PLAN, and the cells above do not match the finalized decisions.

## Non-blocking observations

- Several §3.2 "(review)" cells name the accepting re-review (461a r2, X3a-1 r2, X2a r2, X3b-1a r2, X2b-1 r3, X3c-1 r3). Those REQUEST files do not restate the law revision; an earlier round's request does. The revisions agree with §3.1. 461b's commit message does not say "461 r3"; the accepted law at that point is 461 r3. VD1's message says "VD1"; the review request says VD1 r1. EC1's message does not say "X3d r8"; the combined review request does.
- "23 MB" is 22,699,067 bytes. The host field is `filesystem: "apfs"`, which §2.2 writes as APFS.
- `[[` occurs only in the token table. §9 allows the names to stay there once the table is marked filled. RF-1 is the two unfilled expected-value cells and the leftover PENDING prose, not the retained names.
- EXIT-PLAN's earlier file-presence table still says `finalization.rs` is missing. That table was outside the status-column diff.
- §5 row 21 still says the EXIT-PLAN record pass is due before or with finalization. The row correctly marks the pass open. Finalization landed without it, which is why the date bullets §8 lists are still undated.
- One storage required run (F14) also carries singular `unit: "X9-4"`. The 47-run X9-4 count used in the arithmetic is the X9-4 review's transcribed-row count, not that tag. Totals still add up.
- M3-PLAN.md line 7 still says M2 completion waits on PENDING-RERUN. That is the plan citing an earlier draft of this record. It is stale, and it is not a sentence of M2-COMPLETE.md.

## Rows checked

| Section | Rows checked |
|---|---|
| §3.1 | 19 |
| §3.2 | 62 |
| §4.1 | 11 |
| §5 | 22 |
