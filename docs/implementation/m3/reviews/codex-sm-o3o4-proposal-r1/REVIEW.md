# SM-O3-O4-PROPOSAL-r1 review

Verdict: **ACCEPT**

Required findings: none. Non-blocking observations: none.

Subject manifest: `589ea77eef91179a8ff7e90f16b38af5402f0834da08ae9c708121624931267d` (662 bytes; two members). Rehashed the manifest and both members; all sizes and hashes match. Verified product base `95279fa8ae086f98bd221cd827f6c0efc156c0c5` with a clean checkout and architecture base `f3a753304677365b7344e7ec3bbdcd3151ed4a97`. The held untracked architecture tree was not read or changed.

## Facts

Verified the accepted U-6 round-3 review, its subject hash and all report-subject members. Independently recomputed the proposal's sensitivities from the accepted report data, distinguishing the TS and Rust rows of napi-rs and applying R8's doubled start. The four A-only, ten B and eight C rows match the report.

Without synthetic SM-9, warm F is at most 0.866021 seconds on every row except Lambda. Lambda is 2.091714 seconds, 4.5857% above 2 seconds; its SM-5 is 1.775701 seconds, SM-7 is 0.307326 seconds, and its dependency population is 166417590 bytes. These support the proposal's rounded figures and explanation.

Cold T exceeds 30 seconds only for powertools-lambda, smithy-typescript and umami. All three cease to miss that budget without SM-9; the largest cold T without SM-9 is smithy-typescript at 16.541424 seconds. Warm T exceeds 8 seconds on eight rows; four still exceed it without SM-9:

| Row | Warm analysis, seconds | Warm T without SM-9, seconds |
|---|---:|---:|
| smithy-typescript | 16.295809 | 16.499381 |
| vite | 8.059187 | 8.298093 |
| napi-rs, Rust | 15.802355 | 16.638309 |
| aws-lambda-rust-runtime | 7.715988 | 9.807702 |

Axum's warm T without SM-9 is 7.931936 seconds. Every displayed rounded value matches. The analysis spans dominate the four remaining warm totals; Lambda's non-analysis remainder is also explicitly disclosed.

The 71-source replay is 0.451903 seconds and the 1381-source replay is 62.508591 seconds: 19.4507 times the sources and 138.3231 times the elapsed time. The proposal describes measured growth across D-1 scenarios without establishing a real-workload bound or a complexity law.

AQP §5.2 indeed labels its warm column “Warm (retained evidence), median” and holds the budgets on D12. PLAN-r3 D-7 describes fresh processes following three priming warmups, no OpenSIP state, no reused provider and no declared caches. The proposal accurately distinguishes that measured one-shot warm fixture from retained-evidence work and retains Rust whole-graph dependency coverage. Its lead-host/preliminary and D-1 conditional labels are explicit.

## Options and recommendations

O3-a and O3-b reproduce L's alternatives: await M5 residency for the edit target or change D5 staging. Items 1 and 2 remain one-shot for M3, and the residency/protocol-successor route follows item 9.

O4-a through O4-c are legitimate answers to the owner's budget/staging revisit. O4-a completes the revisit by retaining both, recording the preliminary conditional misses and requiring a D12 re-test with real SM-9 once G3 binds before a later budget or staging change. This is a proposed owner choice, not a claim that the current measurements satisfy the budgets or that D12/G3 gates current L acceptance. O4-b leaves any new values to the owner; none are invented. O4-c presents a staging change as an owner decision.

The recommendations for O3-a and O4-a are reasoned from the synthetic replay dependence, the remaining one-shot analysis costs, the reset distinction and preliminary host standing. They are stated as recommendations and preserve the owner's alternatives. Producer reuse remains subject to INC-1 admission; the proposal grants no reuse authority or present changed-scope implementation.

## Sequence and scope

Section 4 follows L's first delta-round trigger and dependence text: obtain the owner's answers, then draft r7 on r6 with the report's figures at their accepted standing, every outcome and conditionality, the answers and refreshed gate rows. Codex substitution and its reason are recorded consistently with r6's rule allowing an owner- or lead-named replacement when the prior reviewer is unavailable. Acceptance of the subsequent S-M delta round meets L-G1; acceptance of this proposal does not.

The two-part SM-11 through SM-14 rule remains authoritative: r7 carries the report's decomposition, formulas, exact counts and unset owned inputs; the completion round remains after effect. The proposal does not authorize invented completion values. A staging decision remains outside L, and any M3 protocol change still requires the successor item 1 demands.

No owner decision or assent is recorded or inferred here. No placeholder is filled and L is unchanged. Full S-M, L-G1, effective L, native admission/worker, K1 and qualification remain open. ACCEPT means this proposal is accurate and fit to put to the owner; it does not select O3 or O4 for the owner.

## Boundaries

Used only permitted read-only file reading, hashing, JSON parsing and Git queries, followed by writing the requested review artifacts. Did not execute the supplied freeze script or any runner, compiler, Cargo command, test or lane; no network, panes or delegation were used. Private fixtures, installation, signing keys and held trees were not read. Neither repository, the stage nor control files was edited. Only this directory's `REVIEW.md` and `review.json` were written.
