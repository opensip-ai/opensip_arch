# CODEX2 review — M3 unit plan r3

**Verdict: REQUIRED-FINDINGS.** M5-EX resolves C2-M3-R2-02. The main DAG repairs resolve most of C2-M3-R2-01, but the exit formula still omits O2 work selected by its own successor rule. One narrow required scheduling correction remains.

Subject: `docs/implementation/m3/M3-PLAN.md`, 43,170 bytes, SHA-256 `7ef4f0d1147ce8311c49e375c83caf9b5d80895cd77b5e152b9c21799a019c2b`. Product baseline `eb0d503`. This reviews the planning record and does not decide O7 or approve any successor law.

## r2 finding resolution

| ID | Resolution | Reason |
|---|---|---|
| C2-M3-R2-01 | partially-resolved | The missing K1/producer/operability joins, confinement probe, code-versus-launch split and bounded branch account are repaired. The host chain adds to 26 days, and the unsupported whole-M3 total is removed. One required exit join remains absent from the timing formula: O2 parts whose successors have been accepted. |
| C2-M3-R2-02 | resolved | M5-EX explicitly names and gates all three contract joins: native admission/model and human/JSON disclosure; WS test-execution schema and disclosure; and the measured permission truth-table profile. It changes only measured cells, assumes no unnecessary native carrier major, and preserves M3's imported preparation and the excluded untrusted-component scope. |

The graph repairs are at [m3/M3-PLAN.md:149](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:149); [m3/M3-PLAN.md:154](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:154); [m3/M3-PLAN.md:158](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:158); [m3/M3-PLAN.md:163](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:163); [m3/M3-PLAN.md:192](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:192); [m3/M3-PLAN.md:231](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:231). The M5-EX package is at [m3/M3-PLAN.md:337](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:337), with its three successor joins at lines 338–340 and preserved boundaries at 344–347.

All three r2 nonblocking observations are addressed: the preliminary spike launch boundary, the explicit confinement-control extension and the complete worker-prohibition citation.

## C2-M3-R3-01 — Include selected O2 completion in the exit formula

**Location:** [m3/M3-PLAN.md:164](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:164); related lines 166, 214, 217, 223 and 229.

The O2 rule makes each part with an accepted successor an M3-X prerequisite. The unit row includes those parts, but the timing row omits them and gives X = max(M3-M, R, 23) + 2. Their finishes are explicitly successor-gated/unbounded. That formula can therefore put X before a required O2 part finishes, and K2 alone cannot determine the critical path.

**Evidence:**

- [m3/M3-PLAN.md:164](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:164): X requires every O2 part whose successor is accepted by then; only unaccepted parts may be carried to M4.
- [m3/M3-PLAN.md:166](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:166): The exit unit explicitly includes O2 parts under that rule.
- [m3/M3-PLAN.md:214](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:214): O2 has no finite implementation finish bound.
- [m3/M3-PLAN.md:217](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:217): The X timing row lists no O2 dependency and omits its finish from the maximum.
- [m3/M3-PLAN.md:223](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:223): The discussion conditions the 26-day chain on K2 and compares only the bounded branches.
- [m3/M3-PLAN.md:229](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:229): K2 is called the critical path whenever it runs past day 21, without accounting for a later selected O2 branch.

**Counterexample:** Assume K2 finishes at day 21 and a required, successor-accepted O2 part finishes at day 30. M finishes at day 24 and R at day 23. The displayed formula predicts X at day 26, but X must wait for O2 and finishes no earlier than day 32 under the same two-day exit assumption. This is an illustrative dependency counterexample, not a measured result.

**Fix:** Define O2_selected_finish as the latest finish of the O2 parts required under the O-row rule (use a nonbinding value when none are selected). Add it to X's dependencies and maximum. State that X can finish at day 26 only when K2 finishes by 21 and every selected O2 part finishes by 24, in addition to the existing day-zero/branch assumptions. Qualify the statement that K2 becomes the critical path when late. The 26-day host-chain arithmetic and leaving the whole-M3 total uncomputed can remain.

## Nonblocking observations

**C2-M3-R3-N01 — Separate primitive implementation from enforcement-claim readiness.** The unit row correctly requires CF-1 before D1's enforcement claim. The finish table places primitive implementation at day 2 and G2-v validation at day 3, while CF-1 may complete at day 5. Label those early completions as implementation/validation readiness, and give the enforcement claim its max(D1, CF-1) readiness. The existing gate can stay; this clarification need not lengthen the host chain. Sources: [m3/M3-PLAN.md:154](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:154); [m3/M3-PLAN.md:199](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:199); [m3/M3-PLAN.md:205](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:205).

**C2-M3-R3-N02 — Remove the stale operability review-status bullet.** The source abbreviation correctly identifies OPP r3 as accepted and pins its preserved bytes. The risks section still says operability r3 is under review. Update that copied status; it does not change the substantive successor gates. Sources: [m3/M3-PLAN.md:7](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:7); [m3/M3-PLAN.md:380](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:380).

## Other checks

- The K1→M edge, CF-P→D-law acceptance, CF-1→D5/enforcement claim, and D1→provider launch are explicit. G2 authoring is separate from G2-v launch/validation.
- The shown bounded arithmetic checks: C4=12, H=15, I2=17, J2/J3/J4=18/21/23, G4=18, E3=7, F4=12, O1/O3=4/13 and CF-2≤7. R=max(15,K2)+2 and M=max(21,K2)+3.
- The 26-day host chain is a valid bounded subgraph calculation under the stated day-zero assumptions. It is not a whole-M3 or unconditional exit estimate.
- O2's carry rule is confined to successor-dependent additions. O1/O3, CF-2 and the J1/S-OP-12 join remain hard obligations; accepting OPP as a plan does not itself accept any successor.
- M5-EX's new native, reference-model, WS/test-schema and worker-prohibition citations support the described handoff. The corrected policy.rs admission citations match the pinned eb0d503 source.
- The inherited L gate, preview-pack split, G14 preparation/M5 installation boundary, no repository-code execution at M3 and M6 qualification boundary remain sound. O7 remains the owner's pending decision.

M5-EX's cited constraints were checked against [product-v1/native-evidence.md:2440](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:2440), [product-v1/native-evidence.md:2483](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:2483), [product-v1/workflows-and-surfaces.md:1075](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:1075), [native/native_evidence_model.v2.py:2170](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native_evidence_model.v2.py:2170) and [schemas/test-execution.schema.json:7](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/schemas/test-execution.schema.json:7). The O2 schedule remains conditional under [operability/PLAN-r3.md:379](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN-r3.md:379) and [operability/PLAN-r3.md:388](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN-r3.md:388); the finding concerns the missing selected-work dependency, not a demand to move every pending O2 successor into M3.

## Verification boundary

The requested subject size/hash and preserved OPP r3 hash were verified. Only static reads and pinned source inspection were performed, with read-only supporting inspectors. No product build, run, test, spike, benchmark or project script executed. The real runtime home and 413 fixture were not accessed. No commit was made. Only these two review artifacts were written under `/tmp/opensip-implementation/reviews/codex2-m3-plan-r3/`.
