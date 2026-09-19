# Independent review — frozen `store-recovery-protocol-checkpoint-186`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 186 reference bytes. **My 186 proposal, the Q1 report and its rollback addendum were assistance, not acceptance**; the oracle used below is derived from the frozen protocol text, not from my earlier sketches, and I looked for places where the bytes diverge from either. No physical crash, selection, custody, lease/floor-effect, host-wiring, cumulative or product approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `76cad9aae0eaec021df6433f3416cd83a46306c66b8448f4f9dd8ee67369aa90`, 2,225,864 B = request = `archive-pin.json` |
| Members | 1,490, all regular/safe, verified from the tar before extraction; re-verified at end |
| Candidate pins | 1,298/1,298; none unpinned; declared change list equals computed |
| Parent | equals **my own verified 181 extraction** (1,294); 14 modified + 4 added |
| Python | 91: 84 byte-identical to 181, 5 changed, 2 new. `transition-journal-cases.v1.json` byte-identical (retained as historical); successor `…v2.json` added |

## 2. Owner checks re-run

Reference order, `-I -B`, fresh outputs: **all seven lanes exit 0** (integration 1,490 checks, 0 failed). I also ran the two focused modules alone through the host-model loader: 1,064 checks, 0 failed. No bytecode left.

## 3. What I read

All of `store-transition-protocol.v1.md` (151 lines), `store_transition_reference.py` (119), `store_transition_checks.py`, the `StoreTransitionObservationV1` schema, and every delta to the model, host model, three checkers, the lineage companion and S9/S9.2/S9.2.1/S9.3/S15. The model change is small and surgical: `recover_transition_journal` keeps shape → fence → registry → leases, then dispatches on `selection_case(journal)`; same-store keeps the journal-only table; every changed-store case goes to `ST.decide` with the execution id and the observation wrapper. `Unavailable` is an exception, not an action, so no closed output schema moved.

## 4. Independent sweep (`claude-out/probes/sweep.py` → `io/sweep.txt`)

Oracle: crash prefixes generated from the protocol's *stated* durable order for forward and ancestor (not from the selector's code), including abort-in-progress and the forward "renamed but pair not yet selected" point. Every state goes through the **real `recover_transition_journal`**, so precedence and the model join are inside the test. Floors for source and target differ in both directions per field, so `max` is exercised.

Product: 2 cases × 6 journal states × 4 fence attributions (none / earlier execution with the **same intent digest** / this execution / this execution with a wrong intent) × 6 carrier states × 3 selections × 5 image conditions = **4,320 states: 0 disagreements. ABORT with the source fenced by this execution: 0.**

Targeted counterexamples (all as the protocol says):

| Case | Result |
|---|---|
| repeated identical intent: source fenced by an earlier execution, this one at `LEASED`; and at `PREPARED` with its own carrier | ABORT, ABORT (never RESUME) |
| carrier bound to the earlier execution; source observed absent; ancestor target observed absent | QUARANTINE ×3 |
| wrapper `unavailable`; observation `None`; execution id missing | `Unavailable` ×3 |
| observation with an extra member | schema `ValidationError` |
| ancestor partial floor application (some target fields already raised); fully applied before carrier `COMMITTED` | RESUME-COMMIT ×2 (idempotent) |
| ancestor target floor **above** the image | QUARANTINE |
| leases not re-acquired / registry differs / fence not held, each with an unavailable observation | BUSY / QUARANTINE / REFUSE — footprint never consulted first |
| same-store `core-repair`, same-schema `core-update`, same-schema `core-rollback` | journal-only; a context that raises on reading the observation or execution id is never tripped |
| schema-raising `core-update`, `PREPARED`, fenced by this execution, matching image | RESUME-COMMIT; without an observation → `Unavailable` (the 181/Q1 C1 defect is gone) |

**Phase C** (`probes/phasec.py` → `io/phasec.txt`), through the real `sequence` with Phase C inputs that raise if read, for forward, ancestor and schema-raising core-update: unavailable/missing/malformed observation, missing execution id, missing image → `stop=unknown-custody`; ambiguous selection, source absent, contradictory carrier → `stop=MIGRATION.CORRUPT`; in all eight, `retired=False`, `newAdmission=not-attempted`, Phase C inputs never read. The healthy control *does* reach Phase C, so the stop is not an artefact. `installation_recovery_attempt` projects `[PREPARED, ABORTED]` for abort-in-progress, `[COMMITTED, DONE]` for "selection switched, carrier removed", `[PREPARED, COMMITTED, DONE]` for an ancestor resume.

## 5. Mutation (`claude-out/probes/mutation.{py,json,log}`, `rejudge.py` → `io/rejudge.txt`)

21 mutants of the selector in a scratch copy, judged by the owner's focused checks through the loader (not the pinned lane — a pin refusal is not semantic evidence); baseline 1,064/1,064 and my sweep 0/0.
**18 killed by the owner's checks**, including: attribution by digest only; any fence counted as this execution; image not required / missing treated as matching / mismatch tolerated; ancestor compared with source only or target only; foreign-execution image; unchecked target generation; abort-in-progress cell removed; ABORT at `PREPARED` with a `PREPARING` carrier; unconditional terminal release (both terminals); rename-before-selection point removed; unavailable wrapper turned into QUARANTINE; ambiguous selection read as `from`; ABORT naming the retained target.
**3 survive the owner's checks:**

| Mutant | My corpus | Assessment |
|---|---|---|
| carrier binding not checked | detected (targeted counterexample: QUARANTINE → ABORT) | real gap: no owner check presents a carrier bound to another execution |
| ancestor target absence tolerated | detected (QUARANTINE → ABORT) | real gap: owner checks cover an absent *source*, not an absent retained *target* |
| ancestor-`published` early return removed | no difference in 4,320 states | equivalent: the later branches already reject it; the guard is redundant |

(My first pass counted only the sweep's disagreement total and reported the first two as "not detected by either"; re-judging against the full output showed my targeted counterexamples do catch them. Both outputs are kept.)

## 6. Findings

No finding against the recovery logic. Lower-severity items:

### T-1 (test strength) — the two real survivors above
Add: a carrier whose binding names another execution (and one with the right execution but wrong intent) → QUARANTINE; an ancestor observation with `targetPresent=false` at each journal state → QUARANTINE. Both protect the two attribution/retention sentences the protocol leans on most.

### W-1 (low) — "historical" is declared in code comments and prose, not in the artefacts the lane still runs
`migration-cases.v1.json` is still executed by the security lane as model `migration-recover`, its `standing` text says nothing of being historical, and the regenerated report lists those cases alongside current ones. The contract and the function docstring do say "not a current recovery entry". A reader of the report cannot tell. One `standing` sentence in the fixture (or a `historical: true` marker the report carries) would make the consumer classification machine-visible. `transition-journal-cases.v1.json` is no longer consumed by any checker — correct, and worth one line in the README so nobody re-wires it.

### W-2 (low) — `transitionExecutionId` is an unbound assertion in the reference
The journal gains no member (deliberate, stated), so nothing in `recover_installation_transition` ties the supplied execution id to the journal whose identity it *does* verify. I checked the failure direction: a wrong id makes every real binding look foreign → carrier present ⇒ QUARANTINE; the only ABORT cells need an absent/own carrier and no own fence, which cannot coexist with a real post-fence state. So a wrong id fails closed. The protocol names the "coherent active-slot revision" as a host obligation; I would add this failure-direction argument next to it, because it is the reason the unbound input is tolerable.

### N-1 — lifecycle of old fence records is unowned
A retained root re-selected by a rollback still carries the fence record of the earlier forward execution; a later forward migration sees `fence = other` and is handled correctly (tested). Nothing says when such a record is superseded or cleared, or that a store has one fence slot. Harmless to this table; the host will need it.

### N-2 — same-store write order is implicit
"Durable order" is stated "for both changed-store cases". The same-store table (`PREPARED` → ABORT "closure never selected", `COMMITTED` → RESUME) is sound only if `jCOMMITTED` precedes the core-pair publication there too. It almost certainly does; one sentence would make the pair-selection law cover all three cases.

### N-3 — `ambiguous` selection is a contradiction, partial observation is unavailable
Both are stated, and the selector quarantines `ambiguous`. The boundary between "I could not read the pair" and "I read a pair that is neither" is the host's to draw and is the most consequential projection decision it will make; the reference cannot test it.

## 7. Closure of earlier findings — confirmed only where earned

| Finding | Status |
|---|---|
| 181 F-1 (ABORT after RESTORED; `COMMITTED` ignores the footprint) | **Closed at reference level**: 0 post-fence ABORT in 4,320 states; `COMMITTED` and both terminals are footprint-conditional; contradictions quarantine; through `sequence` none reaches retirement or Phase C |
| 181 F-2 (image freshness) | **Closed**: image placed after the last first-pass evaluation and before the fence; S15 reconciled in S15 itself; resume verifies exact equality (forward) / per-field max (ancestor), bound to execution + intent + target generation |
| 181 T-1 | three of four regressions added (absent slot without fence or with an unsorted registry; requested-operation mismatch; each inventory lineage); the fourth (flag tokenisation) honestly reclassified as secondary to policy equality |
| 181 W-1 | docstring corrected; `installation_recovery_attempt` exercised with its projection limit stated |
| 186-proposal Q1 / Q2 / Q3 | O1 adopted (pair-law dispatch; C1–C4 gone); `jCOMMITTED` precedes publication, so `PREPARED + fenced + final` is a contradiction by stated order; S15 recheck is the pre-image act |
| Q1 addendum (rollback carrier, attribution) | adopted and strengthened — execution id + intent digest rather than digest alone, which my sketch had missed |
| 175/178/181 line of findings on recovery authority | unchanged by this checkpoint |

## 8. Limits

A pure reference over asserted observations: no syscalls, no real carriers, markers, floors, selection publication or crash behaviour. My oracle encodes the protocol's stated order; if that order is wrong for a real filesystem, both the selector and my sweep are wrong together. I did not model PS-01 lineage node states as a separate dimension, `old.present` beyond boolean absence (unobservable is the wrapper), or concurrent executions. I did not rebuild the owner's 12 mutants.

## 9. Verdict (bounded)

**The 186 selector agrees with an oracle derived independently from its own protocol on all 4,320 states, never aborts past this execution's fence, distinguishes unavailable from contradictory, handles repeated intents and pre-existing RESTORED roles, keeps same-store journals away from store evidence, and stops before retirement and Phase C on every non-recovering outcome. 181 F-1 and F-2 are closed at the reference level. T-1 names two untested protections; W-1/W-2 are documentation of classification and of a fail-closed argument.** No cumulative, host or product approval.
