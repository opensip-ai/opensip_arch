# Independent review — frozen `role-join-checkpoint-211`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 211 product bytes — one file, `security/src/trust/role_machine.rs`: closure of my 208 T-1, W-1 and N-1. The machine law is the retained v14 machine exactly as in 208; the unaccepted 209 reset-context is **not** applied and I do not apply it. Still a private pure kernel over asserted inputs: raw states and their provenance remain host work. No persistence, admission, audit, continuity or cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `adfdbc7333d09cd88195c3ea5fc1078df00a0f81f9be8cbb5d244466c2e5f9af`, 4,218,624 B = request = `archive-pin.json` |
| Members | 391, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 355/355, none unpinned |
| Parent | equals **my own verified 210 extraction**; exactly one file changed |
| Owner inputs | archived v14 = `039a570244441709…` = the incorporation pin (same bytes as in 208) |

## 2. Owner checks re-run (fresh scratch, offline, locked)
security 167/167; strict workspace Clippy clean.

## 3. What changed (diff read in full)
- `Event::Continue(Continuation)` → `Event::Continue { core, index, component }`; `decide` calls `continuation(core, index, component)` itself and maps `Refuse(why)` → refused, `ExistingOnly`/`InstallGateRequiredForNewProcess` → accepted stay. **No `Event` variant carries a `Continuation` any more**, so a precomputed verdict cannot be passed in; the comment says role observations and caller attribution still need host admission.
- A full 7 states × 4 quorum-guard test (expected value computed from the v14 source set), and the 343-triple join test now drives `decide`.
- A comment on `Refusal` records that `NO-MATCHING-GUARD` and `CONTINUE-UNMATCHED-COMBINATION` are unreachable under the total tables and that replay has a separate owner.
- No other production token changed: every non-`Continue` arm is byte-identical to 208.

## 4. Independent checks
**Oracle differential, adapted** (`probes/adapt211.py` derives both files mechanically from my 208 probe and oracle; only the `Continue` input and the hoisting of the oracle's join function differ): the kernel dump now covers 7 × (39 non-continue event/guard variants + 343 continue triples) = **2,674 decision cells**, compared on next state, outcome/refusal reason and ceremony termination against the interpreter driven by the archived v14 tables: **0 disagreements**. The 343 direct `continuation()` triples: **0 disagreements**, same distribution as 208 (294 / 28 / 18 / 2 / 1).
**Mutation** (`io/mutation211.json`; the 208 harness re-used verbatim for every anchor that still exists, plus five join mutants): **25/25 killed**, no compile failures, no missing anchors —
- **208 T-1 survivor (QUORUM-LOST reachable from UNBOOTSTRAPPED): now killed.**
- join refusal reported accepted; core/index swapped; supplied component ignored; supplied core ignored; `ExistingOnly` refused — all killed.
- the other nineteen 208 mutants remain killed.

## 5. Closure
| 208 | Status |
|---|---|
| T-1 missing source-set coverage for quorum loss | **closed** — and closed as a class for that event: the new test is the full state×guard table, not one more example |
| W-1 caller-asserted continuation verdict | **closed** — the verdict is computed inside `decide`; the type no longer admits a precomputed one |
| N-1 vocabulary comment | **closed** |

## 6. Findings
None. Two notes:
- **N-1** `decide(state, Event::Continue{core,index,component})` still takes `state` separately from the triple; the decision's `state` is returned unchanged either way, so an inconsistent pairing cannot alter an outcome — it only means the *audit* subject (which role this attempted event is recorded against) is the caller's choice, which is host work as the comment says.
- **N-2** the class-level fix was applied to `EV-QUORUM-OBSERVE` only. My matrix shows the other events are also correct, and the remaining owner tests did kill every source-set mutant I tried for them; if root wants the same structural guarantee everywhere, the 2,674-cell table is cheap to adopt as a permanent test because it is generated from the state and guard enumerations.

## 7. Limits
macOS; scratch copies only (`build211-*`, `target211-*`, created after asserting absence), restored from frozen bytes; nothing deleted; build targets excluded from `hashes.txt`. The oracle's guard predicates remain my reading of v14 prose (tables are read from the JSON); its sensitivity was demonstrated in the 208 review and the oracle body is unchanged apart from the `Continue` input. No host-isolation run for these bytes by me; none claimed by the owner for 211.

## 8. Verdict (bounded)
**211 closes 208 T-1, W-1 and N-1 without changing the retained machine: 2,674 decision cells and 343 join triples agree with the v14-driven oracle, the continuation verdict can no longer be supplied by a caller, and all 25 mutants — including the 208 survivor — are killed.** No approval of state provenance, persistence, reset/continuity law, installation or cumulative readiness.
