# Overnight run, 2026-10-03 to 2026-10-04

The owner asked the lead to run autonomously overnight: "if you get blocked, move to the next item and we can discuss any blockers tomorrow morning." This file is the running log, kept by Claude Opus 5.5 as lead.

## Blockers for the owner

| # | Decision | What it blocks | Lead recommendation |
|---|---|---|---|
| B1 | **O7, hostile-input confinement** (M3-PLAN "O7") | Acceptance of M3-L, the provider-protocol law; provider launch; M3-CF's successors. Drafting continues. | <ul><li>Landlock + seccomp + no network on AL2023; Seatbelt on macOS.</li><li>Where confinement is unavailable, disclose it in the result and require containers for untrusted pull requests.</li><li>Run repository code only with RepoExecutionGrantV2, inside confinement.</li></ul><br>**CF-P evidence (2026-10-04, `m3/confinement-cf/CF-P-RECORD.md`):**<ul><li>**macOS 27:** Seatbelt via `sandbox_init_with_parameters` works. Network (TCP, UDP, DNS, unix) is denied, writes outside scratch are denied (19 variants), and fork and foreign exec are denied. Node runs under it. One profile fix is needed (deny `kern.procargs` sysctl). The API is undocumented and deprecation risk is high, so each macOS major needs a check and a missing symbol means disclose.</li><li>**AL2023 (desk check):** kernels 6.12 and 6.18 give Landlock ABI 6 and 7 plus seccomp. Kernels before August 2025 lack Landlock, so they disclose.</li></ul> |
| B3 | **Sign-off on the T2 corpus selection (quality plan D3) and the exploratory envelope (D13)**; both are part of M3-L's acceptance gate | M3-L acceptance only | Approve as reviewed: T2a and T2b accepted by GROK2 (49 repositories, 33 families); the envelope accepted inside M3-Q0 r13. D13 also gates the S-M report. |
| B4 | **OQ-1: what your team's real workspace looks like on disk** (M3-B). That means the package-list file (name and format), whether the root is ever a Git repo, submodules or worktrees, and how Rust and npm packages refer to each other. | Nothing blocks on it; it sharpens D15's admitted shape | M3-B r1 admits a non-repo root with 1–64 disjoint conventional Git member repositories, declared by explicit roots or by Cargo patch and npm `workspaces` readers. |
| B2 | **The gating precision bar** (quality plan D4 revisit; harness design §8) | Q2 acceptance for gating rules. Nothing tonight. | <ul><li>Observed precision ≥ 0.99, plus a 95% cluster-aware lower bound ≥ 0.95 (about 59 independent repository families with zero errors).</li><li>Rules graduate from advisory to gating as evidence from T2 and T3 accumulates.</li></ul> |

## Work log

Times are local.

- **Session restart.** X9-6's lead sets, lanes and release absence had completed: storage 381/381, host 98/98, union 383/383 killed, repetitions agree. The real `check` correctly refuses on the uncommitted worktree.
  - Its review request was pinned and sent to Grok (arch `2c44a5e46`).
  - Lead recommendation: Grok reruns once, on the integrated commit.
- **X9-6 accepted and integrated.** Grok gave ACCEPT-UNIT with no findings, and X9-6 is integrated as product main `3d2d5b5` (commit C). Grok chose to run its full sets once, on C.
- **Final evidence run started on C:** release absence, two full sets across both targets, then the real `check`.
- **Started in parallel, with no machine load:**
  - M3-T2b, corpus completion, for GROK2;
  - M3-I1, the preview-pack IR freeze and contract-successor draft, for CODEX2;
  - M3-L, the protocol law draft. Its acceptance is gated on O7.
- **M3-L r1 drafted and committed, not sent.** Acceptance is gated on S-M, T2b, D3/D13 sign-off, S-OP-2 and O7.
  - **Key finding:** the identity contract binds cache keys to the Plan, and any source edit changes the Plan. So changed-scope reuse (INC-1) needs an identity-contract successor before it can ship. This is consistent with the staged D5 plan; nothing ships at M3.
  - **Rust cancel grace:** 5,000 ms, fixed by Rust3, which differs from the operability plan's provisional 2 s.
- **M3-I1 r1 sent to CODEX2** (arch `bf555155a`). This is the preview pack.
  - **Finding:** the current four predicate ops can't express import cycles, so X12:191's policy-language successor is needed. It adds one atom, `cycle-representative`, with exactly one finding per cyclic component.
  - **The riskiest call (LD-3):** widening the op enums without a new identifier major.
  - **Plan impact:** I1 is larger than M3-PLAN's "M". It splits so that I1-c sits on C4's path and I1-b2 on J2's; this fits the critical path and is to be recorded in the plan.
- **S-OP-2** (safe event vocabulary) is being drafted, for Codex.
- **Release absence on C passed.** The record is byte-identical, and both feature builds were refused.
- **M3-I1:** CODEX2's r1 raised 3 findings: the source-census proof, the authority for widening the enum, and the partial file inventory. r2 fixes all three.
  - **Lead decision:** a two-passage identity-contract successor authorizes the one additive op value under the existing majors.
  - **Rejected:** a major bump, with its cascade listed.
- **S-OP-2 r1 sent to Codex** (arch `42109f80c`).
- **D3 prepared and sent to Grok** (arch `8b9cfc2fe`), while Grok waits for its X9-6 rerun.
  - It refreshes 62 stale rows: 45 overrides and 17 supersessions.
  - `verify_scratch` passes.
  - It includes seven omissions from before D1, and closes X1b with no change.
  - About 20 stale code doc comments are listed for a later code follow-up.
- **M3-T2b sent to GROK2** (arch `06311e94f`).
  - **Size:** 49 repositories, 33 families and 5 workspaces. Every class has at least 2 dev repositories per language.
  - **New very-large entries:** Python has home-assistant and airflow; hand-written Rust has sui.
  - **The aws-cdk workspace was split:** its pinned dependency versions don't resolve against the checkouts.
  - **Open:** only 10 held-out families exist, which bears on B2's gating bar.
  - **Open:** aws-cdk and aws-sdk-rust exceed the 4 MiB canonicalizer limit for the tree digest, so K1a may need a chunked digest.
- **D3 accepted and bound.** Grok gave ACCEPT-DESIGN-UNIT with no findings.
  - It is product main `30c5db1`, on top of C, and touches `design-lock.json` only.
  - `verify_design` passes: 76 contract successors, v134 selected.
  - Main has moved past C. The X9-6 evidence and Grok's rerun stay on C (`3d2d5b5`), in the X9-6 worktree.
- **M3-I1 accepted at r2 by CODEX2,** with no findings. It covers:
  - the frozen preview rule IR;
  - the `cycle-representative` atom;
  - the policy-language and identity successors;
  - the pack contract.

  The product units I1-a, I1-b1, I1-b2 and I1-c are next, after X9-6 finishes.
- **F8 split:**
  - **F8a,** the policy-row refresh, went to Codex. Both dependency checks and both test suites now pass, and every new row was audited.
  - **F8b,** the generator-closure plus TS-lane-registry successor, went to CODEX2 as a proposal. F8b found that `tools/typescript-lanes.json` also pins the `verify_design.py` from before VD1.
  - **The policies went stale on 2026-09-21,** because no unit ran these checks for two weeks. F8a's request recommends adding them to the Python lanes of any unit that touches `crates/contracts` or `crates/identity`.
  - **I1-a regenerates contract code,** so it needs F8b first. Order: F8b, then I1-a.
- **S-OP-2 r1:** Codex raised 7 findings, and it went back for r2 with lead decisions on each.
- **M3-T2b accepted by GROK2,** with no findings. The T2 corpus is complete: 49 repositories, 33 families and 5 workspaces. M3-L's gate item "T2 complete" is met; the owner's D3 sign-off is B3.
- **F8a accepted by Codex and merged.** Product main is now `3e64266`. Both dependency checks pass again.
- **F8b proposal r1:** CODEX2 raised 1 finding. The comparison against rebuild-01 needs a separate equivalence probe, because the selected pipeline refuses any other executable. Sent back for r2.
- **Started drafting M3-B** (configuration and discovery, including the X2 successor for D15 multi-repo workspaces; for GROK2) **and M3-C** (sealed snapshot and Plan; for CODEX2).
- **M2 crash matrix: `matrixPass: true` on clean commit C (`3d2d5b5`).**
  - **Lead sets:** both pass all 479 runs; storage took 1959 s and 1921 s, host 811 s and 801 s.
  - **Kill set:** all 383 union kill-set points are killed, and the two repetitions agree.
  - **Release absence:** byte-identical to the earlier records.
  - **Evidence record:** committed at arch `5c703071d` (`crash-matrix-x9/evidence/3d2d5b5…/`; 490 files, 23 MB).
  - **Next:** Grok's rerun on C (r2, sent). When it agrees, M2's crash/lock/revocation matrix gate is met.
- **The F8b proposal is accepted at r2 by CODEX2.** Its execution runs after Grok's matrix rerun, because it needs the machine:
  - the observed generator rebuild;
  - the separate equivalence probe;
  - the re-pins;
  - the ACCEPT-DESIGN-UNIT review on the frozen manifest.

  M3-I1's product units follow F8b.
- **M3-C r1 drafted and sent to CODEX2.**
  - **Main finding:** `snapshot2`'s 4 MiB descriptor cap limits a snapshot to about 27k files. Five T2 repositories, and likely TS repositories with `node_modules`, exceed it, so an inventory-by-reference successor (S-R) is probably needed after S-M.
  - **Lead decisions, for the owner to know about (reversible):**
    - **O-1:** prepared-mode measurement waits for M5, because it would otherwise execute repository code.
    - **O-2:** every core release is a new detector closure, as EC1 made it for the evaluator.
    - **O-3:** large repositories may hit the cap until S-R lands.
- **M3-B r1 drafted and sent to GROK2.**
  - **D15 shape:** a non-repo root with 1–64 conventional Git members. X2 r9 reuses the closed Git layout for each member.
  - **Findings:**
    - discovery's object and edge caps can't hold large repositories;
    - NE:1750 strips `[patch]`, which needs successor S5;
    - B is about 3 days larger than planned.
  - **OQ-1 added to the blockers as B4.** It is informational.
- **The M2 completion record is drafted** at `m2/M2-COMPLETE.md`, pending Grok's rerun. It has 62 unit rows matched against git, 19 laws, L1–L11 and 22 follow-ups. EXIT-PLAN's status column is refreshed.
  - **It found four M2 law obligations never built or formally deferred.** Lead decisions:
    - **X3a-2** (read-side endpoint adoption): a post-M2 unit, before M3-C1.
    - **X4b** (`admit_repo_execution_grant`): deferred to M3-B3 `grants.rs` and M5-EX, under O7.
    - **X4T-c** (two continuation codes): right after F8b.
    - **X4-F1:** a real defect. Observer rereads don't evaluate expiry as X4T r9 item 6 requires. It is fixed by an X4T-a successor unit before any M3 analysis ships, and disclosed as a known defect at M2 completion.
  - None of the four is among BP:886's M2 criteria, but the owner should know.
- **M3-B accepted at r2 by GROK2.** It covers configuration and discovery, plus D15 multi-repo workspaces through X2 r9. Its successors S1–S9 and the code units come next.
- **M3-C r2 sent to CODEX2.**
  - **Schedule:** the 26-day conditional host chain no longer holds. It is 28 days with the C4 split (recommended) or 29 without, because of C3's units and C4's real size. Flagged as O-4, for the next M3-PLAN revision.
  - **Archive profile:** DS-2 now admits only Cargo's actual package format (gzip, GNU headers, GNU long names), bounded and with no links.
- **X2 r9 and X12 r4 drafted** (M3-B's successors S1 and S2). Lead decisions:
  - **First-use gap.** On the first-use creator route, the creator writes the installation before the write-gate fence, so "pack admission before any effect" can't hold. On that route it reads "before any project-scoped effect". A refused pack there leaves an empty, valid installation, which is disclosed. X11 r1 item 1a's conflict goes to the X11 successor (M3-J1).
  - **X2 ordering.** The placement check and chain walk run before item 3a's config reads.

  Both are queued for Grok after the rerun.
- **X4-F1 written** in worktree `opensip-x4f1` (10 files, +524 −33), not yet compiled.
  - **The fix:** observer rereads evaluate expiry at the handoff time plus monotonic elapsed time. An expired root or stale list fail-stops, with no new codes. No crash-barrier or trace change.
  - **Integration needs:** full lanes plus a rerun of the 43 tick-armed storage rows, X9-4's remaining rows, 13 checkpoint kills, 4 host rows and both censuses.
  - **New follow-ups, lead decisions:**
    - **X4-F2:** the fenced read has the same unapplied-expiry gap.
    - **F9:** test fixture dates expire on 2026-12-30.
- **M3-E1 r1 drafted,** queued for Codex.
  - **Backend lead decision:** tree-sitter grammars compiled to Wasm and run in-host by `wasmi`, with fuel-metered, typed parse failures. Native tree-sitter is the fallback if probe E0 fails.
  - **Owner FYI:** the Wasm route needs a pinned wasi-sdk build toolchain.
- **M3-C r3 sent to CODEX2.** The host chain is now about 31 days at M3-B's estimates; M3-PLAN r5 will carry it.
- **M3-PLAN r5 sent to GROK2.**
  - **Critical path: 33 days** with the C4 split, along B1→B2→C1a→C3→C4a→H→J2→J3→M→X. The earlier "about 31" in this log was the b=8 figure; M3-B's unit table gives b=10.
  - **New owners (lead decisions):**
    - the resume/repair writer gets law J-RW plus unit J4;
    - the X3c re-commit gets X3c r8 plus X3c-3, before J3;
    - X4-F1 and X4-F2 land before J2;
    - F9 by 2026-12-01.
- **M3-J1 r1 drafted,** queued for CODEX2. Lead decisions, reversible by the owner:
  - **No new CLI commands at M3.** A host-library entry serves tests and the harness; the CLI comes at M4 per BP:887. So CLI dogfooding starts at M4, as the quality plan already says.
  - **Steady state now has a lawful route.** A charged presence probe picks an ordinary writer, or the creator act followed by a second attempt.
  - **Producers run twice on first use.**
  - **The ephemeral path is read-only.**

  It also found that six M2 laws need amendments (468, X1, X3a, X4B, X2, 464), and that J units need X9 r17 plus crash-matrix reruns.
- **M3-PLAN r6 accepted by GROK2.** Its critical path is 33 days from M3-L acceptance.
- **M3-C accepted in review at r5 by CODEX2.** It takes effect once M3-L and X12 r4 are accepted. J1 is now with CODEX2.
- **Grok's X9-6 rerun on C was accepted.** All 479 runs agree in every pairing, and `matrixPass` is true for the reviewer, mixed and lead pairs (arch `50047b7ed`). **The M2 crash/lock/revocation matrix gate is MET.** The completion record is being finalized: lanes on main `3e64266` are running, then it goes to GROK2.
- **M3-E1 r2 written,** queued for Codex.
  - **Conflict found:** E1 makes the core provider closure the syntax producer, while M3-C r5 keeps that closure out of `semanticClosures`.
  - **Lead decision:** M3-C r6 widens it and adds the clones-near census (X-C1, X-C2). This gates E3, not E1.
- **X2 r9 and X12 r4 accepted by Grok,** with no findings. These are M3-B's S1 and S2, and X12 r4 includes the first-use clause. M3-C's gate now waits only on M3-L, which waits on O7.
- **M2 COMPLETE (2026-10-04).** `M2-COMPLETE.md` was finalized at arch `3e6c40ad7` and is in GROK2's fact review.
  - **Evidence:** the crash matrix passes on `3d2d5b5` with Grok's rerun agreeing on 479/479.
  - **Lanes on main `3e64266`:** workspace 1744/0, crash-matrix 1624/0, clippy, fmt and `verify_design` all clean.
  - **Open, with owners:** the four obligations X3a-2, X4b, X4T-c and X4-F1.
- **M3-J1 r1:** CODEX2 raised 7 findings. It went back for r2 with lead direction.
- **F8b execution started:** the generator rebuild, the equivalence probe and the re-pins. X4-F1's lanes and X9 row reruns follow it.
- **S-OP-2 r5** is queued for Codex.
- **M3-J1 r2 sent to CODEX2.** Lead decision, reversible by the owner: a signal received during the final required output is recorded and deferred, because the envelope and its exit are already decided. It needs contract successor S18. Rejected: exit 130 beside an already-decided success envelope.
- **CF-P run.** Seatbelt confinement is feasible on macOS 27 with one profile fix. AL2023 is feasible on current kernels (desk check). This is evidence for O7 (B1), and it gates M3-D's acceptance.
  - **Housekeeping for the owner:** the probe's deliberately killed runs left five crash reports in `~/Library/Logs/DiagnosticReports/` (`cfp-2026-10-04-*`, `t_named-*`). They are safe to delete.
- **M3-E1 accepted at r3 by Codex.** The syntax backend is tree-sitter in a fuel-metered Wasm boundary; probe E0 decides between Wasm and the native fallback. X-C1 and X-C2 go to M3-C r6.
- **M3-J1 accepted at r3 by CODEX2,** with no required findings. Its two non-blocking wording observations, the composition citation and post-freeze loss, go into the S18 successor. J-BS and S18 still need their own design-unit reviews.
- **M3-C r6 written and sent to CODEX2.** It applies E1's X-C1 by lead decision: the core provider closure also produces syntax-universe work and is in `semanticClosures` exactly when a syntax universe is selected. It also applies X-C2, the `clones-near` census that C4a builds. Nothing else changed from r5.
- **S-OP-2 accepted at r6 by Codex** (ACCEPT-DESIGN-UNIT, no required findings). It is the safe event vocabulary and sink law. Its one non-blocking observation, a table-cell placement, is applied in the recording text. M3-O's O1 now waits only on P0.
- **Five pre-day-0 drafts started in parallel,** all docs-only, with no machine load:
  - M3-H, the fact-admission law, for Grok;
  - B-S1 (with SX-1) and B-S2, M3-B's contract successors, for GROK2;
  - I1-L and I1-P, the preview pack's contract successors, for CODEX2;
  - J-RW, the resume/repair writer law (P5-1), for Codex;
  - X3c r8, the re-commit law (P5-2), for Codex.
- **F8b accepted and bound.** Grok gave ACCEPT-DESIGN-UNIT with no findings. It is product main `e093e90`, with 77 contract successors, and `verify_design` passes. I1-a and X4T-c are now unblocked on F8b.
- **M2 record r2:** GROK2 raised one required finding. §2.2's storage row cites a singular `unit` field, but the run records carry a plural `units` array. r3 follows.
- **M3-C r6 accepted in review by CODEX2,** with no required findings. Its one stale-wording observation is applied to owner question R1. The law takes effect once M3-L is accepted, which waits on O7 (B1).
- **M2 record r3 sent to GROK2.** It fixes RF-1: the run records carry a plural `units` array of the laws touched, not the X9 sub-unit. It also takes up the four observations and F8b's binding.
- **Lead decision: M3-L gets an early review round.** r1 was never sent and is stale: it cites M3-PLAN r4 and predates S-OP-2, T2b, CF-P, C r6, E1 and J1. It is being refreshed to r2 for Grok. An ACCEPT is recorded as "accepted in review", effective when the gate is met (O7, S-M, D3 and D13), as was done for M3-C. The `⟨SM-n⟩` values and any change that O7 forces go through a delta round. **Rejected:** holding all review until the owner items close, which would serialize the day-0 law behind them.
- **M3-D r2 written,** queued for GROK2 after the M2 record. It answers GROK2's five r1 findings and folds in CF-P:
  - macOS tree kill is best effort, recorded truthfully;
  - the spawn-refusal routes are corrected;
  - the ExecutionId draw follows J1 r3;
  - the Linux fact table is complete.
- **Lead decisions in M3-D r2, reversible by the owner:**
  - **Linux provider scratch moves to `/var/tmp`,** because AL2023's `/tmp` is a tmpfs capped at half of RAM.
  - **A group `SIGSTOP` before the macOS snapshot is deferred to CF-1,** because CF-P didn't measure it.
  - **SD-6:** D's manifest refusals before the ExecutionId draw need a new J1 row, R10a. That amends the accepted J1 r3, so it goes to a J1 r4 delta for CODEX2 once GROK2 has ruled on D r2.
- **The M2 completion record was accepted at r3 by GROK2,** with no required findings. Its two observations, both status cells, are applied as recording text. M2 is complete and the record is final.
- **M3-D r2:** GROK2 resolved all five r1 findings and raised one wording finding. The prohibition must say "no analysis-attempt ExecutionId", because on first use the creation prelude's id already exists. Lead-written r3 fixes that and the four observations, and goes back to GROK2.
- **M3-L r2 written and sent to Grok** for an early soundness review. The gate table is refreshed: G2, G3 and G7 are met; G4, G5 and G9 are owner items; S-M has not started. The S-OP-2 event check found no gap: the 11 provider-boundary needs map to 11 registered events. Its cross-law items go to the next revisions of M3-PLAN, OPP and the citing laws: the early-review rule, "day 0 means L in effect", and the r1 line re-pins. **New lead decisions, reversible by the owner:** stderr is counted and never held; the TypeScript `host-shutdown` cancel reason is never sent at M3.
- **J-RW r1 written and sent to Codex.** This is the resume/repair writer law, P5-1. It covers all 57 refused F00 kill points that L11 leaves. Each kill point is completed inside the next admitted durable write, at its owning law's own step and under that owner's lock. Nothing is deleted or rewritten. Any state that is not exactly a known crash prefix keeps today's refusal. The X9 r17 rows are RW-F00, RW-K1–K9 (crash during repair), RW-N1–N9 (neighbouring states still refuse) and RW-B. **Lead decisions the owner may reverse:**
  - A crashed first registration completes automatically, with no announcement (LD-1, LD-2). The rejected alternative was a repair command, which doesn't exist before M5.
  - The owner's 465 item 5 ACL decision extends to the L11 owners (LD-3).
  - Trust files and ledgers are completed in place: only the missing suffix is written (LD-4, LD-5).
  - **Weakest assumption:** the bare-WAL ledger view at the two WAL kill points comes from SQLite's documentation, not from a run. J4c must pin it by test.
- **M3-D accepted at r3 by GROK2,** with no required findings. This is the supervisor and common control law. Section F, confinement, remains an O7 placeholder, binding only if O7 is decided as recommended. The accepted bytes are `supervisor-d/PROPOSAL-r3.md` (`9679dbc4…`). The acceptance note, and the one history-wording observation, will be added to the live file after Grok's M3-L r2 review, which pins the live bytes. SD-6, the pre-draw row R10a, goes to CODEX2 as a J1 r4 delta.
- **X3c r8 written and sent to GROK2.** This is the re-commit law, P5-2. Codex was busy with J-RW, and the plan names Grok for M2 carry-in laws. A re-commit is a new attempt of the same Run: it adds its own attempt rows and stages no availability or pins. Whether the Run is already committed is read from its own committed rows inside the level-3 transaction, and a half state is `LEDGER.CORRUPT`. There is no DDL change, no new crash point and no new outcome. At C, 18 of the 19 next-writer re-commits change from refused to Committed. The X9 r17 rows are RC-1 to RC-9. **Cross-law item:** X3d's item 4 step 3.8 needs a record restatement (X3d r9).
- **E0 phase 1 is ready.** These are the syntax-backend probe's downloads and harness, with no compiling yet.
  - **Pins:** wasi-sdk-34 (digest verified); tree-sitter v0.27.0; rust v0.24.2, typescript v0.23.2 and javascript v0.25.0; wasmi 2.0.0 (deterministic, validate). T2a has 8,351 selected files, 49.2 MB, all within 4 MiB. Phase 2 waits for X4-F1's lanes and X9 rows to leave the machine.
  - **Lead decisions, made before any data:**
    - P5 uses the strictest reading: the median over non-empty files of bytes ÷ the full per-file cost (fresh instance, parse, copy, validation). Aggregate throughput is reported but not gated.
    - E0's `SyntaxTreeV1` byte layout is probe-only; E2a fixes the normative one.
    - wasmi compiles everything up front, since lazy translation makes fuel depend on file order. This becomes an E2b obligation.
  - **E1 record items** for its next revision or for E2a/E2b:
    - ERROR's symbol 0xFFFF needs an explicit exception to item 10 and A11;
    - item 4's closure layout omits the wasm headers;
    - grammar and runtime commits are now pinned by E0.
- **M3-H r1 written** (fact admission). It is queued for Grok after M3-L r2. Only H5 sits on the host chain (3 days, finishing day 22), so the 33-day figure holds. **Cross-law items:**
  - **X-H1, serious.** No TS2 or Rust3 frame carries a provider's symbol census. Without a native-owner successor (FA-2) and an M3-L revision, no TypeScript or Rust symbol Coverage can be admitted, and the preview cycle rule can never decide on a real Run. **Lead decision:** FA-2 and the matching M3-L r3 are drafted next, before day 0. **Rejected:** deferring symbol Coverage past M3, which would leave G13 and the preview rule without real evidence.
  - **X-H2:** NE's "facts before the terminal" conflicts with the retained selectors. Successor FA-1 resolves it.
  - **X-H3:** inventory records in TS and Rust universes have no lawful producer closure. This goes to C's next revision and CRC-1.
  - **X-H4:** M3-L's no-host-minted-facts rule needs an exception for syntax and inventory facts.
  - **X-H5 and X-H6:** the inventory unit owner, and a typed refusal for the scope bound.
- **I1-L and I1-P written.** These are the preview pack's contract successors. I1-L is with CODEX2 and I1-P follows it. The reference model passes 41 cases and 5 op-law refusals. I1-P's digests, recomputed with the design encoder, equal the law's provisional values.
  - **Lead decision LD-L1:** the four JSON schema changes ship as complete successor copies, carrying their parents' bound overrides, as 468a did. They are not passage overrides, because `verify_design` refuses line selectors on JSON and a pointer override can't append to an enum.
  - **Record items for I1's next revision:**
    - the anchor imprecisions;
    - five more passages that enumerate the closed op set;
    - WS's selected effective copy;
    - item 2.3 and 2.5 choices that fix proof bytes, which I1-L's precisions P0–P7 settle;
    - I1-a's `verify_design` needs: a 468a-form record, re-pointed source maps, and the moved line references.
- **Plan for X-H1:** FA-2 (the provider symbol-census carrier) and M3-L r3 are drafted together once Grok's L r2 verdict is in, so that one L revision answers both.
- **B-S1 and B-S2 drafted.** B-S2, IE `vcs-observation` schema 3, binds on today's `verify_design`. B-S1 found a tooling gate.
  - **The gate:** S9's `CONFIG.INVALID` remedy line is already overridden by X12-0, and `verify_design` refuses a second override of the same line. Its supersession mechanism covers only inventory descriptions.
  - **Lead decision: split S9 out of B-S1 before review.** SX-1 and the D15 passages bind now, and S9 becomes unit B-S9. B-S9's form is checked first as a complete successor copy of the two native-model files, the 468a and I1-L form, which today's tool may admit. VD2, a `verify_design` successor, is the fallback.
  - **Rejected:** going straight to VD2. Changing `verify_design.py` again would make the generator-closure and lane-registry pins stale and force another F8b-style rebuild.
  - **Timing:** B1-a needs S9 by day 0, and SX-1 and D15 are needed by B2-a, C1a and B3-b.
  - **M3-B r2 contradicts itself** on a crossing when the root is inside a repository: item 22 and row 1 say one thing, row 3 another. The drafter follows item 22 and row 1, so projects without D15 keep today's refusal. This is flagged for GROK2.
- **J1 r4 and M3-C r7 written** (SD-6). They are queued for CODEX2 after I1-L.
  - **J1 r4** adds R10a between R10 and R11. It quotes the first-use exception from D, adds ER10a as the last step under the read fence on the ephemeral path, and adds control J-C10b. It also corrects item 11: `repair recover` is the source-repair journal command, not storage repair. CINV:988, WS:1024 and the product's `repair-v2` schema confirm this.
  - **M3-C r7** narrows row 8 to a selection among component manifests admitted at R10a. Core closures are outside the narrowing.
  - **Record items for D's next revision:**
    - D4-T1 and D4-T2 sample at R10a's return;
    - "first use" also covers `LostRace` and `NotPristine`;
    - SD-6's "MC r5" citation;
    - **SD-5,** the public route for R10a's `ExcludedForm` refusal, is not yet written. It must stay distinct from matrix row 27.
- **Pin drift handled.** J-RW (Codex) and X3c r8 (GROK2) pinned live files that later moved to drafts. Both reviewers are told which commits hold the pinned bytes, and the queued M3-H request carries the same note. **Lesson:** requests pin accepted snapshots (`PROPOSAL-rN.md`), not live files.
- **X3c r8 accepted by GROK2,** with no findings or observations. This is the re-commit law, P5-2. X3c-3, the storage code, and its X9 lead set are next, and must land by day 25. X3d r9's record restatement (CL-1) is owed.
- **M3-L r2:** Grok raised one required finding. Item 13's "closed set" of provider-wire identities is wrong: NE's OpenUniverse payloads and HelloAcks carry more members, and J1:192 cites that sentence. Grok also listed exactly which parts depend on O7 and S-M. L r3 follows, together with FA-2 (X-H1) and X-H4.
- **The M3-D live file now carries its acceptance note** (r3 bytes in `PROPOSAL-r3.md`).
- **B-S1, B-S2 and B-S9 ready for GROK2.** B-S9 is S9's `CONFIG.INVALID` remedy, as complete successor copies of the two native-model files, so no VD2 is needed. The capability-totality reference selection is the precedent. The three units bind together on the `e093e90` lock: 77 → 80 successors, no conflict. **Residual hazard (B-S9 LD-4):** a later unit could override a superseded copy's other lines, and only review catches that, as with capability-totality's copy. GROK2 is asked to rule on it. B-S1's and B-S2's M3-C citations are pinned to arch `3590205a9`, since C's live file is now the r7 draft.
