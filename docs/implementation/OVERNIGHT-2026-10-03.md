# Overnight run, 2026-10-03 to 2026-10-04

The owner asked the lead to run autonomously overnight: "if you get blocked, move to the next item and we can discuss any blockers tomorrow morning." This file is the running log, kept by Claude Opus 5.5 as lead.

## Blockers for the owner

| # | Decision | What it blocks | Lead recommendation |
|---|---|---|---|
| B1 | **O7, hostile-input confinement** (M3-PLAN "O7") | Acceptance of M3-L, the provider-protocol law; provider launch; M3-CF's successors. Drafting continues. | <ul><li>Landlock + seccomp + no network on AL2023; Seatbelt on macOS.</li><li>Where confinement is unavailable, disclose it in the result and require containers for untrusted pull requests.</li><li>Run repository code only with RepoExecutionGrantV2, inside confinement.</li></ul> |
| B3 | **Sign-off on the T2 corpus selection (quality plan D3) and the exploratory envelope (D13)**; both are part of M3-L's acceptance gate | M3-L acceptance only | Approve as reviewed: T2a accepted by GROK2, T2b in review; the envelope accepted inside M3-Q0 r13. |
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
