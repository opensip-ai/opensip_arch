# Owner questions O3 and O4 from the S-M report: lead proposal r1

**Lead proposal for an owner decision, 2026-10-14. Not law, and no owner decision is recorded here.** M3-L r6 raises two owner questions on S-M's outcomes:
- **O3** on outcome (B), F > 2 s;
- **O4** on outcome (C), T over a medium budget (`provider-protocol-l/PROPOSAL-r6.md`, "Open questions" and item 9).

The S-M report (`docs/implementation/m3/s-m-report/S-M-REPORT.md`, accepted by Codex in `codex-sm-report-u6-r3`) records both outcomes on several workloads. L's first delta-round trigger fills the `⟨SM-n⟩` placeholders "with every outcome item 9 records, and any owner answer to O3 or O4 that those outcomes trigger". So the S-M delta round, and with it L-G1, needs the owner's answers.

This record sets out the evidence, the options L gives, and the lead's recommendation for each question. The owner decides.

## 1. What the S-M report found

All figures come from the lead's macOS host and are preliminary; the targets are held on the D12 runner. Every F, T and outcome is conditional on D-1, because SM-9 is a synthetic replay scenario with one fact, one finding and one fingerprint per counted source. It is not a bound on any real workload.

| Outcome | Rows where it holds |
|---|---|
| (A) only | express, napi-rs (TS), hyper, serde-json |
| (B) warm F > 2 s | powertools-lambda, smithy-typescript, umami, vite, napi-rs (Rust), aws-lambda-rust-runtime, axum, serde, tokio, the serde/json overlay |
| (C) cold T > 30 s or warm T > 8 s | powertools-lambda, smithy-typescript, umami, vite, napi-rs (Rust), aws-lambda-rust-runtime, axum, tokio |

**What drives (B).**
- **SM-9 dominates F.** Without SM-9, warm F is at most 0.87 s on every row except aws-lambda-rust-runtime, which is 2.092 s. Lambda's remainder is mostly its Rust SM-5 (1.776 s, which reads and hashes 166 MB of dependency sources) plus SM-7 (0.307 s).
- **SM-9 grows faster than linearly.** Across the D-1 scenarios, 71 sources take 0.452 s and 1,381 sources take 62.5 s: ×19.5 sources against ×138 time. Real SM-9 depends on G3's emission recipe, which binds after day 0.

**What drives (C).**
- **Cold T > 30 s.** This holds for powertools-lambda, smithy-typescript and umami only, and only because of SM-9. Without SM-9, the highest cold T is 16.54 s (smithy-typescript), well under 30 s.
- **Warm T > 8 s.** This holds on 8 rows. Without SM-9, 4 rows still exceed 8 s, all because of analysis:

  | Row | SM-2/SM-4 warm | T warm without SM-9 |
  |---|---:|---:|
  | smithy-typescript | 16.30 s | 16.50 s |
  | vite | 8.06 s | 8.30 s |
  | napi-rs (Rust) | 15.80 s | 16.64 s |
  | aws-lambda-rust-runtime | 7.72 s | 9.81 s |

  Axum is just under, at 7.93 s.

**What S-M's "warm" means.** AQP §5.2's budget column is "Warm (retained evidence)". S-M's warm fixture (D-7) is Q0 §9.2's: priming warmups, then a fresh process with no reused provider and no retained evidence. One-shot analysis re-analyses the whole workload on every run. Rust SM-4's whole graph also analyses dependency crates. So the warm comparison holds the measured one-shot, no-reuse cost against a budget whose column names retained evidence.

## 2. O3 (outcome B)

**L's options** (PROPOSAL-r6, O3). The owner confirms one of:
- **O3-a.** The edit target waits for M5 residency, as D5's staging implies.
- **O3-b.** D5's staging changes.

Under either, items 1 and 2 keep TS2 and Rust3 one-shot for M3. L records residency (item 8) or a protocol successor as M4's only route to the edit target.

**Lead recommendation: O3-a.**
- **(B) is almost entirely the synthetic SM-9.** It holds without SM-9 only on aws-lambda-rust-runtime, at 2.09 s. That is 4.6% over the target, on a preliminary host, dominated by dependency-source hashing. Real replay volume is unknown until G3 binds its emission recipe.
- **The replay's growth is a finding for the replay implementation, not a reason to restage.** The superlinear growth of SM-9 across the D-1 scenarios should be raised with the owners of IE's complete replay (IE:1580-1592) and its implementation for measurement once real graphs exist.
- **The evidence does not show that restaging is needed.** Changing D5's staging, for example bringing the resident host forward, is a large re-plan.

## 3. O4 (outcome C)

**L's question** (PROPOSAL-r6, O4). One-shot full analysis misses a medium budget, which is the D4 revisit AQP:372 names ("to be revisited after the first exploratory measurement"). The owner decides whether to revisit the budgets or the staging. This S-M report is that first exploratory measurement, so the revisit is due now.

**Options.**
- **O4-a.** Revisit done: keep the medium budgets (cold ≤ 30 s, warm ≤ 8 s, on D12) and D5's staging. Record (C) as preliminary and conditional on D-1. Re-test on the D12 reference runner, with real SM-9 once G3 binds, before any budget or staging change. Record the warm-fixture note from §1.
- **O4-b.** Revise the medium budgets now, for example a separate one-shot, no-reuse warm budget. The owner would set the values; the lead proposes none.
- **O4-c.** Change D5's staging, for example to bring changed-scope analysis or residency forward.

**Lead recommendation: O4-a.**
- **The cold misses are all synthetic SM-9.** Without SM-9, every row's cold T is at most 16.54 s.
- **The warm misses that remain are no-reuse analysis cost.** They fall on 4 of 14 rows (two TS, two Rust), measured without retained evidence. The budget's own column names retained evidence. INC-1 permits admitted reuse of producer work, and M4's changed scope targets exactly this cost.
- **These are preliminary figures.** They come from the lead's host, not D12. Changing an owner-approved budget, or the staging, on them would be premature.
- **The re-test is a gate, not a deferral.** Under O4-a, any later budget or staging change is decided on the D12 measurement.

## 4. What follows the owner's answers

The lead then drafts the S-M delta round on L (r7, a diff on r6). Its content:
- it fills every `⟨SM-n⟩` from the S-M report;
- it records every outcome with its D-1 conditionality and preliminary standing;
- it records the owner's O3 and O4 answers verbatim;
- it refreshes the gate rows.

L's delta-round rule goes to the same reviewer. Grok is no longer available, so the owner's named reviewer, Codex, takes the round, and the request records why (PROPOSAL-r6, r6 rule). L-G1 is met when that round is accepted.

The answers change no protocol constant, item or outcome. If the owner chooses O3-b or O4-c, D5's staging is the owner's decision, outside L. L would then need a further delta round only to change M3's protocol, which item 1 forbids without a successor.

## 5. Standing

This record fills no placeholder, changes no law and records no owner decision. No owner assent is inferred. Full S-M, L-G1, effective L, native admission and worker, K1 and qualification remain open.
