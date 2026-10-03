# GROK2 review: M3 unit plan r3

**Verdict: ACCEPT**

Subject: `docs/implementation/m3/M3-PLAN.md`, 43170 bytes, sha256 `7ef4f0d1147ce8311c49e375c83caf9b5d80895cd77b5e152b9c21799a019c2b`. Previous snapshot `M3-PLAN-r2.md` matches `add49e25…`. Product baseline `eb0d50398035fe3532dadc332f88cf1d8bc4cb69` is a clean worktree. No product build or test was run. `~/Library/Application Support/OpenSIP` is absent.

All four r2 findings are resolved. The added edges are in the unit rows and the timing table, the stated finish days match their starts and durations, and 26 days is only the host chain when K2 finishes by day 21. The M5-EX citations match the native contract, the test-execution contract, and the reference model.

## r2 findings

| ID | Resolved | Where |
|---|---|---|
| RF-1 | yes | K1, CF-P, CF-1, and D1 are edged. Every M and X predecessor is bounded except the three named exceptions. 26 days is conditional. |
| RF-2 | yes | AQP:236 is cited only for too few findings. Closing with adjudication pending is this plan's rule. Later Q2 use cites AQP:228 and AQP:246. |
| RF-3 | yes | OPP §10 is cited for its ten areas. The three escape cases are new D5 and S-OP-11 controls. |
| RF-4 | yes | M5-EX names the native §5.2 join, the WS §7 schema join, and a measured truth-table successor. Repository-code execution stays out of M3. |

RF-1. Day 0 is M3-L's acceptance, so O7 and S-M are done. CF-P (2 days) is pre-day-0 and D-law acceptance is after it. D5 starts after D3 and CF-1 and finishes on day 10. K1 finishes on day 3 and is a predecessor of M3-M. Provider launch is after O7 and D1: G2-v finishes on day 3, and F1's row starts after D3. K2, R (through K2), and O2 are the stated unbounded exceptions. The whole-M3 total is left uncomputed.

The host chain B1 → B2 → C1 → C3 → C4 → H → J2 → J3 → M3-M → M3-X is 2+3+2+3+2+3+3+3+3+2 = 26, with finishes 2, 5, 7, 10, 12, 15, 18, 21, 24, 26 when K2 finishes by day 21. Under that condition M3-M is max(21, K2)+3 = 24 and M3-X is max(24, R ≤ 23, J4 = 23)+2 = 26. G4 finishes on day 18. J4 finishes on day 23. O3 finishes on day 13. CF-2 finishes by day 7. None of those pushes the exit past day 26 while K2 is inside the condition.

RF-2. M3-M says the exploratory report may close with gating or repair-eligible adjudication still pending, and that this is this plan's rule. Strata with too few findings are INSUFFICIENT-EVIDENCE at AQP:236, which is that rule. Later Q2 use cites AQP:228 (every such finding is adjudicated) and AQP:246 (a human expert resolves unclear labels).

RF-3. D5 lists privacy, correlation, custody, bounds, outcomes, crash, capacity, cancellation, liveness, and overhead, and then the three escape controls as an extension that is not in OPP §10. O3 cites the same split.

RF-4. M5-EX must be accepted before `execution.rs` claims confinement or container enforcement. BP:974 is `test-run` and BP:992 is `native-prepare`, both M5, both `crates/host/src/execution.rs`. NE:2440-2444 copies effects from the truth table, refuses a stronger claim, and gives network, subprocess, and filesystem write as `DISCLOSURE-ONLY`. NE:2480-2487 says confinement is never claimed, that only a measured cell moves, and gives the mandatory sentence. NEM:2170-2172 is the reference comparison that refuses a mismatched enforcement value. NEM:2181-2182 is that sentence. WS:1071-1081 is inside §7 (heading at 1046): the step discloses and does not confine, and `ENFORCED-PLATFORM` requires a successor truth-table profile and test-execution schema. TES:7-14 is `EnforcementValue`, whose enum is `DISCLOSURE-ONLY`, `ENFORCED-BY-CONSTRUCTION`, and `ENFORCED-AT-HOST-BROKER`. PTT is `docs/coop/artifacts/permission-truth-tables.v9.json`. The worker prohibition cite is NE:2534-2535. AQ:344 and REG:317 remain the closed untrusted-code scope.

## Non-blocking observations

**NBO-1.** `policy.rs:1087` is the `NotBundled` return. `policy.rs:1401` is the Plan-pack `.find`. The `PLAN_POLICY_PACK_NOT_BUNDLED` refusal is `policy.rs:1402`.

**NBO-2.** The risks section still says operability r3 is in review. The plan header, and `operability/PLAN.md`, record Codex acceptance on 2026-10-03 (`b49035f2…`). The same risk bullet already says M3-O and M3-L follow that accepted revision.

**NBO-3.** G2-v finishes on day 3 from D1. CF-1, which D1's enforcement claim needs, can run until day 5. The stated launch rule is O7 plus the primitive, and G3 is bound by G1a at day 10, so the overlap does not move the host chain. Say that G2-v is not the enforcement claim, or start it after CF-1.

**NBO-4.** Unit C depends on B. C1 starts after B2 and finishes on day 7. B3 finishes on day 8. C4 starts on day 10, after B3, so the conditional 26-day chain is unchanged.

**NBO-5.** AQ:344 names G09 and G30, and M3-CF lists them. BP:1013 is DR-G09 at M2. BP:1034 is DR-G30 at M6. The seven M3 preparation gates are unchanged.
