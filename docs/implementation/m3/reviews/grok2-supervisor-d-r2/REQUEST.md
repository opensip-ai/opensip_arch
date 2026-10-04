GROK2 review: **M3-D r2**, OpenSIP's supervisor and common control law, round 2. It answers your five r1 findings (RF-1 to RF-5) and records CF-P's outcome. This is a **law and fact** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-supervisor-d-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs. Run no `cargo`, no tests, no probes and no lead sets. Do **not** re-run CF-P or any Seatbelt or Landlock trial: judge its record as written.
- Never touch the real home. `~/Library/Application Support/OpenSIP` must stay absent. If you run `git` anywhere, redirect `HOME` to a private 0700 scratch directory and turn hooks off.
- Never read the private 413 UUID fixture.
- If you compute digests, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`.
- `docs/implementation/m3/supervisor-d/PROPOSAL.md` (r2) is the subject of `subjectSha256`. It is a law with a unit breakdown.
- `docs/implementation/m3/supervisor-d/PROPOSAL-r1.md` is r1's bytes (`c6ae10de…`, the subject of your r1 review; r1 is tracked at arch `839018434`). Its sha256 must equal your r1 `subjectSha256`.
- Your r1 review is copied at `docs/implementation/m3/reviews/grok2-supervisor-d-r1/`.

**The gate is now met.** CF-P ran on 2026-10-04. Its record is `docs/implementation/m3/confinement-cf/CF-P-RECORD.md` (arch `70ab22c71`; the overnight log's "CF-P evidence" entry is `68be36dc0`), with the probe under `confinement-cf/probe/`. The law cites it as **CFP**. CF-P is a record, not law, and claims nothing as enforced. If you accept r2, D can be accepted.

**O7 is still pending.** Section F stays an O7 placeholder, "binding only once O7 is decided as recommended". Please check again that nothing outside section F depends on O7.

**Records that moved overnight, and how r2 cites them:**
- **Accepted:** M3-J1 r3 (CODEX2, `ad887c90…`), cited by its `host-pipeline-j/PROPOSAL-r3.md` lines; S-OP-2 r6 (Codex, ACCEPT-DESIGN-UNIT, `ce8d3a4b…`), cited by `operability/s-op-2/PROPOSAL-r6.md` lines, every r4 line re-pinned; M3-E1 r3 (Codex), cited by item 17, unchanged; M3-C r5 (CODEX2), cited by its `snapshot-plan-c/PROPOSAL-r5.md` snapshot by item, while r6 is in review.
- **Unchanged since r1:** M3-PLAN r6, the operability plan r3, Q0 r13, the analysis-quality plan r6, M3-L r1 (draft), and every `docs/v2` and `docs/coop` file r1 cited.

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `e093e90`, read-only. That is F8b on top of r1's `3e64266`; F8b changed no file pinned here.

## What r2 changes (the "r2 changes" table has the detail)

1. **RF-1, item 18 (macOS tree kill).**
   - The Guaranteed cell now promises only that `SIGKILL` is **sent** to every group member at each group kill, with no signal to a recycled group id, and that the record is truthful. It no longer says the root is reaped, and it excludes anything alive at the reap ceiling (`exit: unreaped`, or `tree: incomplete`).
   - The confirm is `proc_listpids(PROC_PGRP_ONLY)` listing only the zombie root. A failed call, or another member at the ceiling, records `tree: incomplete`. A `killpg` error is never the confirm, because CF-P found that `killpg(pg, 0)` on a zombie-only group returns `EPERM` (CFP:228).
   - The snapshot is a **recursive** `proc_listchildpids` walk, which returns a pid count (CFP:224).
   - The in-group fork-and-`setsid` window between the snapshot and the group `SIGKILL` is now on the Not guaranteed row.
   - D5-T2 asserts best effort only. D5-T2b covers the window, and D5-T2c covers the confirm. A group `SIGSTOP` that would close the window is rejected for now as unmeasured.
2. **RF-2, items 12, 22 and 26.** `spawn-refused` is split.
   - `closure-recheck-failed` (host-side, pre-spawn) goes to J1 r3 row 28, with `DELIVERY.CLOSURE_BYTES_CORRUPT` (WS:1375).
   - `session-spec-inconsistent` (a host-built spec that no provider spoke) goes to NE:3573's host-invariant route, which is J1 r3 row 2's.
   - Provider-spoken mismatches stay `control-refusal` or `provider-protocol`, on row 30 (NE:3529).
3. **RF-3, items 12, 19 and 22.** The cause is split into `revoked` (SL:1306; X4:120; J1 r3 row 18) and `observer-fail-stop` (SL:1311; X4:121; row 19). Both keep the S6 kill ladder.
4. **RF-4, items 24-26 and the preamble.**
   - Where ExecutionIds are drawn is stated from accepted J1 r3: the durable attempt's at R12, `CommitSession::open`, reserved in `ExecutionIdReservations`; the ephemeral and render attempts' at their starts; the first-use prelude's in `mint_intent`.
   - Manifest-class refusals move to **a new pre-draw row R10a**, after R10's trust read and before R11 and R12. **SD-6** records it as an amendment to J1 r4, and MC row 8 narrows to selection among R10a-admitted manifests.
   - Request-class refusals stay at R1.
   - D4-T1 asserts the reservation registry's state, and that `x3d.session.execution-draw` is never reached.
   - Item 26 is explicitly post-draw and pre-stage.
5. **RF-5, F-8.**
   - The LX table now aims to cover **every** Linux fact the law relies on. The new rows are LX-15 (`no_new_privs` and the layer order), LX-16 (the seccomp filter-mode probe), LX-17 (Landlock `EXECUTE` scope), LX-18 (io_uring), LX-19 (signal-target filtering), LX-20 (`pipe2` and glibc's exec-failure report), LX-21 (`wait4` units) and LX-22 (`flock` release).
   - Each row states its CF-P status: desk-checked, partly, or not in CF-P.
   - F-1, F-2, F-4 and the ordinary items cite them.
6. **CF-P's outcome.**
   - **The gate (G1) is met.**
   - **F-3:**
     - adopts the `kern.procargs` `sysctl-read` deny (MX-5 failed without it), `realpath`-canonical parameters, and `file-link` by name;
     - resolves the symbol with `dlsym`;
     - uses neither mode of `sandbox_init`, because the named mode gets its caller SIGKILLed.
   - **F-1:** the status pipe gains an "applied" byte, because `errno` stays 0 and the library writes to fd 2.
   - **F-7 and F-8:** MX outcomes table.
   - **Item 6:** a fresh, empty scratch per launch, with only copies placed in it, against MX-3's pre-existing hard-link residual. The Linux scratch root moves to `/var/tmp`, because AL2023's `/tmp` is a size-limited tmpfs.
   - **Item 7:** `RLIMIT_CORE` 1 on Linux.
   - **Item 4:** the raw `pidfd_open` syscall on glibc 2.34.
   - **LX-10:** AL2023 kernels 6.1, 6.12 and 6.18, with 6.18 the default since 2026-08-17.
   - **F8 is confirmed.**
7. **NBO-1:** item 17 now says it departs from ML item 12.1's hold. **NBO-7:** pins renewed.

## Decide

1. **Your five findings.** Is each of RF-1 to RF-5 resolved, partly resolved or unresolved? Give evidence.
2. **Facts.** Check r2's new and changed citations, especially:
   - CFP:94-111, :116-229 (the MX sections), :253-264, :276-320, :322-353;
   - J1 r3 `PROPOSAL-r3.md`: :160-180, :293-312, :424-427, :617, :633-634, :643, :645, :661, :664;
   - SL:470-481, :1306, :1311; X4:120-121; NE:3573; WS:81, :1375;
   - the re-pinned SOP2 lines in `PROPOSAL-r6.md`;
   - SDK27 `libproc.h:92`, `:95`.
3. **R1 (RF-1).** Do item 18's macOS cells now match its escalation sentence and recursive walk exactly? Do D5-T2, D5-T2b and D5-T2c test what the cells claim?
4. **R5 (RF-2, RF-3).** Is each split row on its correct existing owner route?
5. **R6 (RF-4).** Is R10a a sound pre-draw placement against accepted J1's order, including the first-use prelude, which has already drawn its own ExecutionId, and the ephemeral path? Is the registry-state assertion the right proof? Is SD-6, an amendment to accepted J1, the right vehicle?
6. **R8 (RF-5).** Is the LX table now complete for every Linux fact the law relies on? Is anything a Linux claim without a row?
7. **R9 (CF-P).** Does r2 record CF-P faithfully, without over-claiming? Are items 6 and 7's changes right?
8. **New errors.** Does anything in r2 contradict an accepted law, contract, plan or the CF-P record, or claim confinement, measurement or qualification?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"priorFindings"`: RF-1 to RF-5, each `resolved`, `partly-resolved` or `unresolved`, with evidence;
- `"subjectSha256"`: r2 PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. SD-2, SD-3 and SD-6 each need their own review, and D's code units need an `ACCEPT-UNIT` with an `inventoryCandidateAssessment`. Do not commit.
