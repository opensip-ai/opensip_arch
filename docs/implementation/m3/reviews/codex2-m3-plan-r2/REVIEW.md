# CODEX2 review — M3 unit plan r2

**Verdict: REQUIRED-FINDINGS.** Four r1 required findings are resolved; the critical-path finding is partially resolved. Two required method fixes remain: a complete and internally consistent dependency/finish account, and an explicit contract handoff for O7's proposed M5 repository-execution enforcement.

Subject: `docs/implementation/m3/M3-PLAN.md`, 35,300 bytes, SHA-256 `add49e2508816defdcc033a3720359fa8a639d8fcb94191950b91e8f5df8c841`. Product baseline `eb0d503`. This reviews the planning record; it approves neither O7 nor any successor law.

## r1 finding resolution

| ID | Resolution | Reason and evidence |
|---|---|---|
| C2-M3-R1-01 | resolved | The L acceptance gate now requires S-M, complete T2, Q0, D3, D13, the D2 draft, the vocabulary draft and O1/O7. The SDK record join is explicitly part of the L law/successor scope. Pre-law work has priority. [m3/M3-PLAN.md:135](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:135); [m3/M3-PLAN.md:139](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:139); [m3/M3-PLAN.md:221](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:221); [analysis-quality/PLAN.md:480](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:480) |
| C2-M3-R1-02 | resolved | S-P is a preliminary feasibility probe without a Q6 claim. S-M requires T2a, the Q0 envelope and D13; Q6-labelled samples require D12. The recommended start prioritizes Q0. [m3/M3-PLAN.md:137](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:137); [m3/M3-PLAN.md:228](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:228); [analysis-quality/PLAN.md:534](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:534) |
| C2-M3-R1-03 | resolved | I1 owns the frozen preview IR, contract/conditional policy-language successors, bundled bytes, registry row and self-checks, with no H dependency. C4 and J require I1/X12d. I2 separately owns the non-authoritative draft catalog. [m3/M3-PLAN.md:145](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:145); [m3/M3-PLAN.md:142](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:142); [m3/M3-PLAN.md:149](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:149); [m3/M3-PLAN.md:150](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:150) |
| C2-M3-R1-04 | resolved | O7 is explicitly a hard prerequisite to L and provider launch. D waits for CF, and F4/G2 use the selected O7 profile. The owner decision remains pending; reviewing this plan does not decide it. [m3/M3-PLAN.md:139](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:139); [m3/M3-PLAN.md:143](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:143); [m3/M3-PLAN.md:263](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:263); [operability/PLAN-r3.md:378](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN-r3.md:378) |
| C2-M3-R1-05 | partially-resolved | The displayed host-chain arithmetic is correct and now includes B/C3/C4/H. However, the subunit table still does not account for all required joins or establish that the host chain determines exit. K1 is missing from M's dependencies, CF timing is unaccounted for, and the D-law/day-zero premise conflicts with the placement of D1's feasibility trial. [m3/M3-PLAN.md:151](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:151); [m3/M3-PLAN.md:152](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:152); [m3/M3-PLAN.md:168](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:168); [m3/M3-PLAN.md:179](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:179); [m3/M3-PLAN.md:187](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:187); [m3/M3-PLAN.md:300](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:300) |

All four r1 nonblocking observations are addressed: C3 names the complete prepared-output checks and recipe; M completes an exploratory report despite pending labels; FW-14/U-8/U-9 are explicit; OPP r3 and S-OP-12 are incorporated.

## C2-M3-R2-01 — Complete and reconcile the DAG before identifying the critical path

**Location:** [m3/M3-PLAN.md:143](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:143); related lines 151, 152, 168, 170, 187, 198, 300.

The shown host chain sums to 26 days, but the table does not establish a longest path through all M3 obligations. Several required branches have no duration or completion bound. There is also a missing executable-harness dependency and an inconsistent law/trial timeline. Calling the estimate provisional does not repair these omissions.

**Evidence:**

- [m3/M3-PLAN.md:151](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:151): K1 is the harness core and determinism driver; K2 is the T1 fixture work. M's unit and timing rows name K2 but omit K1.
- [m3/M3-PLAN.md:152](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:152): M's unit row requires E3 and O1, while the timing row at 187 omits both. I2 and K2 also have no timing rows or finish bounds.
- [m3/M3-PLAN.md:143](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:143): D requires CF; the timing row at 179 starts D immediately without a CF finish bound or an explicit pre-day-zero CF completion assumption.
- [m3/M3-PLAN.md:168](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:168): The model assumes B/C/D/E/H/J laws accepted before day zero.
- [m3/M3-PLAN.md:300](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:300): D1's Seatbelt trial decides feasibility before D law is accepted, while the table places D1 during days 0–2.
- [m3/M3-PLAN.md:155](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:155): X depends on all units, yet B3, D4/D5, E, F4, J4, K, I2, O, R and CF are not fully accounted for in the finish model.
- [m3/M3-PLAN.md:181](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:181): G2's four days are assigned before L, but the prelude at 196 does not show its joins or the prerequisites to execute it under the O7 profile.
- [m3/M3-PLAN.md:198](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:198): The 33-day total relies on the incomplete day-zero assumptions and exit graph.

**Fix:** Add K1 to M's prerequisites. Give every M/X prerequisite a duration or an explicit finish bound, and reconcile those joins across the unit and timing tables. Account for CF and split an earlier confinement feasibility probe from D1 implementation, or move D-law acceptance to its actual position. Distinguish code authoring from lawful provider-launch/demonstration readiness when placing G2 and the producer subunits. Recompute the longest path and total, or call 26 days only the conditional host-chain duration and leave the whole-M3 total uncomputed until the missing branches are bounded.

## C2-M3-R2-02 — Name the repository-execution contract joins required by O7 item 4

**Location:** [m3/M3-PLAN.md:272](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:272); related lines 284, 286, 290, 298.

The proposed confined/container-only repository execution is carried into M5, but the successor account names only SL S10/S6, AQ, DR-128 and a provider-result disclosure carrier. Native preparation and test execution independently pin effect admission, schemas and pre-execution disclosures to the current unconfined truth-table profile. An SL matrix change and an implementation task do not by themselves replace those other accepted contracts.

**Evidence:**

- [m3/M3-PLAN.md:272](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:272): O7 item 4 requires repository-code execution to run inside confinement or a container.
- [m3/M3-PLAN.md:286](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:286): CF-1 names SL/AQ/DR-128 successors; CF-2 is a provider-ran-unconfined output carrier.
- [m3/M3-PLAN.md:298](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:298): M5 execution.rs is to enforce item 4 for native-prepare and test-run, but no native/test-execution successor package is named.
- [product-v1/native-evidence.md:2440](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:2440): AuthorizedExecutionV2 effects are pinned to the v9 security table, and stronger claims are refused.
- [product-v1/native-evidence.md:2483](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:2483): Native preparation mandates a human/JSON pre-execution sentence saying OpenSIP does not prevent network or other effects.
- [product-v1/workflows-and-surfaces.md:1075](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:1075): Measured platform enforcement explicitly requires a successor truth-table profile and test-execution schema; the current pre-spawn sentence also describes unconfined execution.
- [schemas/test-execution.schema.json:7](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/schemas/test-execution.schema.json:7): The closed test-execution vocabulary excludes ENFORCED-PLATFORM and expressly requires a measured-profile/schema successor to admit it.
- [native/native_evidence_model.v2.py:2170](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native_evidence_model.v2.py:2170): The reference admission checks the selected table and constructs the existing unconfined disclosure at 2181–2182.

**Fix:** Extend CF-1's successor account, or name an explicitly gated M5 successor package, for the native §5.2 admission/model and human/JSON disclosure join, the WS §7/test-execution schema join, and the selected permission truth-table profile. These must be accepted before M5 execution claims the selected enforcement. This review does not require a new native carrier major where its existing vocabulary suffices; change only measured platform/effect cells and preserve the repository-code worker prohibition and excluded untrusted-component scope. No repository-execution implementation is added to M3.

## Nonblocking observations

**C2-M3-R2-N01 — State the launch boundary of the pre-law spike.** The outside-product harness makes S-M a possible lawful pre-law prototype, so this review does not establish a dependency cycle. Still, state what launches its compiler/runtime processes: separately reviewed throwaway tooling under the O7 decision, an existing external confinement mechanism, or another explicitly limited probe. Routing S-M through the production D unit would conflict with L requiring S-M while D requires L. Preserve the owner-decision gate and keep preliminary samples distinct from qualified or production claims. Sources: [m3/M3-PLAN.md:137](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:137); [m3/M3-PLAN.md:139](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:139); [m3/M3-PLAN.md:143](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:143); [m3/M3-PLAN.md:263](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:263).

**C2-M3-R2-N02 — Identify confinement escape controls as an extension.** Network, write-outside-scratch and environment escape controls are sensible additions. OPP r3 §10 contains privacy, correlation, custody, bounds, outcome, crash, capacity, cancellation, liveness and overhead cases; it does not itself specify those confinement escape cases. Label D5's cases as the proposed CF/S-OP-11 extension rather than implying they are already supplied by that citation. Sources: [operability/PLAN-r3.md:420](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN-r3.md:420); [m3/M3-PLAN.md:295](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:295).

**C2-M3-R2-N03 — Tighten the worker-prohibition citation.** The cited rule is correct. Its exact field/value statement spans NE:2534–2535; NE:2533–2534 does not include the constant false value. Use the complete span or cite line 2535. Sources: [product-v1/native-evidence.md:2534](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:2534).

## Other checks

- The explicit L acceptance gate matches the accepted AQP pre-protocol obligations and the OPP O1/O7/vocabulary/SDK joins.
- I1 is the mandatory preview pack; I2 remains an exploratory catalog. The earlier empty-registry handoff is repaired.
- CF correctly treats O7 as pending, distinguishes enforced hardening from opening untrusted native/WASM/plugin scope, and names the security, platform and output work rather than claiming existing confinement.
- The cited confinement disclaimers match SL:497/1113, AQ:344, NE:2554 and REG:317/366. Those sources do not themselves approve the pending O7 recommendation or demonstrate primitive availability.
- The inherited M3 scopes, G14 preparation/M5 installation split, D15 successor, imported inert prepared sets, no public CLI/repository execution at M3, and M6 qualification boundaries remain sound.

The recomputed 26-day host-chain arithmetic is correct. The required graph finding concerns missing prerequisites, completion bounds and sequencing, not the addition itself. No further hard missing M3 implementation unit was established beyond the harness join and successor handoff described above.

## Verification boundary

The exact subject size/hash matched the request. The accepted AQP r4 and preserved OPP r3 hashes were verified. OPP's live file gained an acceptance note; this review uses `PLAN-r3.md` for its stable cited bytes.

Only static reads and source inspection were performed, with read-only supporting inspectors. No product build, run, test, spike, benchmark or project script executed. The real runtime home and 413 fixture were not accessed. No commit was made. Only the two requested review artifacts were written under `/tmp/opensip-implementation/reviews/codex2-m3-plan-r2/`.
