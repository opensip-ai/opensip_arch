# Adoption receipt: X9-SUCCESSOR-CADENCE r3 (the census run's observer cadence), 2026-11-01

**Decision LD-COORD-X9-CADENCE (coordinator, session 9ce22ffd, under OD-AUTO-1; a law change; flagged to the owner).**

**Adopted:** the exact bytes `x9-cadence/X9-SUCCESSOR-CADENCE-r3.md`, sha256 `12e9b8d12ec06739b174d0f8e5eed01a8b3697d7f2f65beeb470248a400cb85a`, mode 0444 (re-hashed at signing with the reviewer idle). X9's accepted text is not edited; this successor supplies the rule that X9 r3 (:54-58) owed to "this law's next revision", and supersedes r16's "no rule is needed" (:815) as the record states.

**Substance (the record controls):**
- In census runs, the unarmed observer's cadence is scripted: no timed tick, so `x4.observer.tick` occurs once per guard. Production keeps X4 r7 item 5's 5 s.
- X4's 10 s bound stays on the native clock and is sampled at reads. The load limit therefore moves; it does not disappear. A census over it stays red as a HARNESS-ERROR, with no retry.
- The record states the effect on the three census consumers (storage commit_tests, security's pinned CENSUS, host commit_matrix_tests).

**Basis, bound by value (R3 different-vendor review, Codex gpt-6-astra/high, w3A):** `x9-cadence/review/r2/REVIEW-r2.md`, sha256 `0734091426da295df5accb8de233b4bcdc6cb2798cd0a9391452ff69c5355d90`: `X9-CADENCE: ADOPTABLE`, no required findings. `review/REVIEW-r1.md` (`ebb2df7d…`, REJECT of r2) is history. Coordinator rulings LD-Q-232, 233, 235, 236, 237.

**Confirmed:** S8 item 5's reconciliation of LD-Q-236 with RF-1 (the class "Positioned, not reproduced"). Requiring at least 3 Reproduced is accepted on the reviewer's conditions: every attempt and class stays reported, no rate is computed from the reproduced subset, and the selected three are not presented as the whole experiment.

**Carried notes (the reviewer's, non-blocking):**
- NB-1: read S4's "Clean" as "no additional cadence-induced refusal, assuming the other checks succeed", and "Their points stay equal" as "normally completed post-rule repetitions retain these points".
- NB-2: the unstalled arm does not prove the stall caused a particular tick.
- NB-3: the measurement's caveats stay with the implementation evidence.

**Separate from this adoption (owed):** the implementation and its independent review (FLAKE7-FIX-1), C1-C6 evidence, current-workload validation, inventory and integration, LT-4's install. Carry CP-X9-ARMED-TIMER stays open. LD-Q-236's LT-4 decision is an operational selection that keeps red outcomes and escalation, not a quantitative guarantee: its margins are proxies. No qualification is established.
