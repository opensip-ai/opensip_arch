# Independent review — frozen `trust-role-machine-checkpoint-208`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 208 product bytes — a **private, pure, per-role event interpreter** over the incorporated v14 machine plus the CORE/INDEX/COMPONENT continuation join (`security/src/trust/role_machine.rs`, new; one module declaration in `trust.rs`). It is conditional logic over **asserted** inputs: no document, signature, time, custody, admission, persistence, audit or capability claim, no operational caller, and "State token not whole record". I review it as exactly that, against the machine **as incorporated** — including the original refusal of `EV-REVOKE` from `ST-UNBOOTSTRAPPED`. My unaccepted 209 proposal is not applied to it anywhere below. No release or cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `9dfb0ae0915335ff2d2d16058c867873d3a19373bdbc76de77a1f7d72d873e35`, 4,410,276 B = request = `archive-pin.json` |
| Members | 433, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 355/355, none unpinned |
| Parent | equals **my own verified 207 extraction**; one changed (`security/src/trust.rs`), one added (`security/src/trust/role_machine.rs`) |
| Owner inputs | 5/5 rehash equal `owner-inputs.json`; v14 = `039a570244441709…6715` = the v1/v2 incorporation pin and byte-identical to the file I read for my 206 note |
| Host receipt 128 | 235 sources all equal product pins; no failed command |

## 2. Owner checks re-run (fresh scratch, offline, locked)
security 167/167; strict workspace Clippy clean.

## 3. Independent exhaustive check against the incorporated machine

**Oracle** (`probes/oracle208.py`): a table interpreter that reads `machine.transitions`, `fallbackByEvent`, `fallbackDefault`, each member's `whenInactive/whenActiveFailure/whenActiveSuccess` objects, the abort `toFunction`, and `offlineRunningPolicy.totalDecision` **from the archived v14 JSON**, and applies `outcomeBranchDiscipline.evaluationOrder` (applicability → whenInactive → whenActiveFailure → whenActiveSuccess → otherwise `fallbackByEvent`). Source-state sets, targets and refusal reasons are therefore the file's, not mine; only the guard *predicates* that v14 states in prose are hand-encoded, each beside the sentence it implements. It shares no code and no table with the Rust.
**Kernel dump** (`probes/matrix208_probe.rs.txt`, scratch copy): every state × every event variant × every guard value — 7 × 44 = **308 decision cells**, each compared on *next state*, *outcome/refusal reason* and *ceremony-termination target*; and all 7³ = **343 continuation triples**.

| Comparison | Result |
|---|---|
| 308 decision cells | **0 disagreements** |
| 343 continuation triples | **0 disagreements**; none unmatched in v14's ordered table (294 core-refuse, 28 index-refuse, 18 component-refuse, 2 `ExistingOnly`, 1 install-gate) |
| Oracle sensitivity (v14 tables perturbed in memory, `io/oracle_sensitivity.txt`) | unperturbed 0; drop `ST-RECOVERY` from `EV-REVOKE` sources → 1; `EV-QUORUM-OBSERVE` fallback made refused → 16; abort order reversed → 11; `ST-REVOKED` added to the ordinary-heal member → 2; `ST-UNBOOTSTRAPPED` added to the quorum-loss member → 1. The oracle is not vacuous |

Points the request singled out, each confirmed cell-by-cell:
- **Applicability before activation.** Ordinary PRESENT from `ST-REVOKED`/`ST-RECOVERY` is `PAYLOAD-NOT-ADMISSIBLE` for *every* entry observation, including `Inactive` — never `ENVELOPE-INACTIVE` (v14 `normativeExclusion`: the inactive branch belongs only to an applicable named member). Recovery PRESENT has no TRUSTED-entry branch at all; its only input is staging validity.
- **Concurrent revocation.** `QuorumObserve{below, revocation_also_holds:true}` is the *accepted stay* fallback from TRUSTED/EXPIRED/STALE/RECOVERY ("If both, the EV-REVOKE rank wins and this guard is false"), and the code comment states the host obligation to dispatch the admitted `EV-REVOKE` first. From `ST-RECOVERY`, a valid `EV-REVOKE` and a below-threshold observation both leave the ceremony, as v14 names them.
- **Accepted-fallback semantics.** `EV-CLOCK` and `EV-QUORUM-OBSERVE` fall back to *accepted* stay; `EV-REVOKE`, PRESENT, INSTALL, RECOVER-BEGIN/COMMIT/ABORT fall back to *refused* with their own reasons; `NO-MATCHING-GUARD` is unreachable because all nine events have a `fallbackByEvent` entry — correctly absent from the kernel's `Refusal`.
- **Sticky behaviour.** `EV-CLOCK` never moves QUORUM-LOST/REVOKED/RECOVERY; restored quorum stays QUORUM-LOST and an ordinary admissible payload heals it; nothing but RECOVER-COMMIT leaves REVOKED toward TRUSTED; abort returns the first still-true of REVOKED, QUORUM-LOST, EXPIRED, STALE, else UNBOOTSTRAPPED, never TRUSTED, and proposes the termination target without writing anything.
- **ACTIVE failure without a declared branch.** INSTALL from TRUSTED with a rejected entry yields `INSTALL-NOT-TRUSTED` and ordinary PRESENT from TRUSTED yields `PAYLOAD-NOT-ADMISSIBLE`: v14 gives those members no `whenActiveFailure`, so `defaultTransition` sends them to the event fallback — the kernel matches that reading; RECOVER-COMMIT, which does declare one, yields `RECOVERY-COMMIT-REFUSED` and stays in ceremony.

## 4. Mutation (owner tests as judge; 21 mutants, all compiled; `io/mutation208.json`)
**20 killed**: CLOCK preempting RECOVERY; stale-over-expired precedence; REVOKE from UNBOOTSTRAPPED; REVOKE refused from RECOVERY; restored quorum healing; quorum ignoring concurrent revocation; ordinary PRESENT healing REVOKED; recovery PRESENT staging from TRUSTED; RECOVER-BEGIN from TRUSTED / without inputs; abort rank swap; abort → TRUSTED; abort without termination; inactive INSTALL mis-reasoned; INSTALL from EXPIRED; RECOVER-COMMIT outside ceremony; three continuation mutants; CONTINUE refusal reported accepted.
**1 survived — T-1 (low):** *`ST-QUORUM-LOST` reachable from `ST-UNBOOTSTRAPPED`* (adding `Unbootstrapped` to the quorum-loss source set) passes all six kernel tests. v14 excludes it (member 12's sources are TRUSTED, EXPIRED, STALE-REVOCATION, RECOVERY; from UNBOOTSTRAPPED the event is the accepted-stay fallback) and my matrix catches it (1 cell). It matters more than its size suggests: QUORUM-LOST is a *sticky* state, so the mutant would let a quorum observation on a never-bootstrapped role manufacture retained restrictive history. One assertion — `decide(Unbootstrapped, QuorumObserve{below:true, revoked:false}) == accepted(Unbootstrapped)` — closes it; better, a table-driven test over the source sets of each named member would close the whole class (the owner tests are example-based, which is why a single missing example survives).

## 5. Findings
No behavioural defect: the kernel is cell-for-cell the incorporated machine. Beyond T-1:

### W-1 (low) — `Event::Continue` carries a caller-asserted `Continuation` unrelated to the three role states
`continuation(core, index, component)` is correct for all 343 triples, but `decide(state, Event::Continue(c))` accepts or refuses purely on the supplied `c`; nothing ties `c` to the triple it was computed from, nor `state` to one of those three roles. For an assertion-driven kernel that is consistent with the README, and v14 routes `EV-CONTINUE` "from `*` … See offlineRunningPolicy.totalDecision". But it is the one event whose decisive input is a *precomputed verdict* rather than an observation, so a future caller can pass `InstallGateRequiredForNewProcess` while the role is `ST-REVOKED` and get an accepted decision. Before a caller exists, prefer `Event::Continue { core, index, component }` computed inside `decide` (or make `Continuation` constructible only by `continuation()`), so the join cannot be bypassed by construction.

### N-1 — vocabulary coverage
v14's 13 reasons vs the kernel's 10: `NO-MATCHING-GUARD` unreachable (above); `CONTINUE-UNMATCHED-COMBINATION` unreachable because the join is total (343/343 classified); `CONTINUE-REPLAY-NOT-DESIGNED` out of scope by the README ("Replay remains governed by its current separate owner"). Correct omissions; worth one comment in the enum so a later reader does not "complete" it.

### N-2 — what the kernel deliberately does not know
`Conditions` for abort, `revocation_also_holds`, `newer_and_byte_valid`, the `EntryObservation` and the clock booleans are all asserted. In particular abort's `still_true.revoked/quorum_lost` can only be truthful if the caller retained that history across the ceremony — the module header says so ("The caller must retain sticky observation and ceremony evidence across events"). That is the open capsule work, not a 208 defect.

### N-3 — roles
The kernel is per-role and role-agnostic; the continuation join names CORE/INDEX/COMPONENT only, as v14's install-surface policy does. `TR-BUNDLE`, `TR-REPAIR`, `TR-PROFILE` have no join semantics here; nothing claims otherwise.

### N-4 — owner inputs vs reference
The README states that 201 omitted v14/v2 from its physical snapshot and that "a reference successor must pin and reconcile them". Agreed; until then the machine this kernel implements is pinned by *this product candidate's* owner-inputs only.

## 6. Limits and disclosure
macOS; probes and mutants only in `build208-*`/`target208-*` scratch copies created after asserting absence, restored from frozen bytes; nothing deleted; no compile failure occurred. The oracle's guard predicates are my reading of v14 prose — a shared misreading by owner and reviewer would not be detected by this differential; I mitigated by reading tables from the JSON and by the sensitivity run. `honestyRepairs*`, fixture classes and `g06/g08` of v14 were not read. Later supersessions (clock rule v8 §4.2, thresholds, component revocation) affect how the *asserted inputs* are produced, not this dispatch table; I did not review that production. My first sensitivity script failed on a Python f-string syntax error before running anything; fixed and re-run. Host isolation not re-run (receipt verified).

## 7. Verdict (bounded)
**Against an independent interpreter driven by the archived v14 tables, the kernel agrees on all 308 state×event×guard cells — next state, outcome or refusal reason, and ceremony termination — and on all 343 continuation triples; the oracle demonstrably reacts to table perturbations. Applicability precedes activation, recovery staging is separate from TRUSTED-entry, CLOCK never preempts RECOVERY, concurrent revocation makes the quorum guard false with the dispatch obligation stated, and sticky states behave as incorporated. Twenty of 21 mutants are killed; the survivor (QUORUM-LOST from UNBOOTSTRAPPED, T-1) needs one assertion. W-1 asks that the continuation verdict not be a caller-supplied event payload before a caller exists.** No approval of persistence, admission, audit, continuity, installation or cumulative readiness.
