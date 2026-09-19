# Independent adjudication r3 — storage D2, resolutions of r2 G-1 to G-4

Reviewer: Claude (actual independent reviewer; Codex owns the decisions). 2026-09-18.
Standing: **design adjudication of unselected choices**; no text, model or code is approved, and the
frozen 111 review remains a separate later step. My r1 and r2 reviews and evidence are unchanged; no
frozen, selected or product byte was touched; no commit, push or delegation.

## 1. Exact bytes reviewed

`storage-D2-owner-decisions-r3-20260918.md`, 4,591 bytes, SHA-256
`1ce53b08ab491850ff3c7da2e0a520f477b0eba0d4e219828ec0e761139fddc9`
(copy: `claude-out/decisions-r3-as-reviewed.md`). Read against the r2 decisions `ed101e67…02e9`, the
addendum `c834b676…0e27` and the owners pinned in r1. Additionally read for this round:
`carrier-format.v3.md` §8.1 "Interrupted state and stale custody" and §12 note on `witnessMalformed`
(same file hash as r1, `2c3e465d…5a7f`).

## 2. Verdict

**G-1, G-2, G-3 and G-4 are resolved as design choices, and G-4's replacement is better than what I
recommended in r1.** I have no remaining objection to the direction. Two things must be written down
before the normative text is frozen, because r3 makes them load-bearing (H-1, H-2), and one cheap
scheduling rule recovers almost all of the availability r3 gives up (H-3).

| r2 | r3 resolution | Assessment |
|---|---|---|
| G-1 marker no-progress | marker(G) ⇒ already quarantined; never re-insert, never append/ADVANCE/REVERT in G; valid same-project witness naming G is continuation-*eligible* regardless of its relation to the tail; absent witness only with `witnesslessRestore`; malformed/unreadable/foreign stay refusals; malformed marker authorizes nothing; later journal generations still win | **Resolved**, see H-1. "Regardless of its relation to the tail" is necessary, not merely permissive: after a namespace rollback caught by the start-of-operation floor comparison the witness is perfectly *consistent* with the rolled-back tail, so eligibility cannot depend on the witness looking adverse. |
| G-2 empty base / inherited table | highest generation ranges over inherited **and** v3 rows; predecessor closure considered before the empty-base rule; act C requires the same-project `COMMITTED` witness at the inherited TERMINAL seq/digest after a witnessed act A, resume reconciles first; no grandfathering of unwitnessed experimental migrations | **Resolved**, see H-2 for one precedence sentence. Refusing a retained development carrier with no in-place repair is the right call for a prospective format. |
| G-3 superseded `k > t` | two valid same-project later witnesses select historical scope even when `k > t`; F22/floor condition keeps its candidate and Step 4; otherwise `unknown-custody`; one-sided observations retry once | **Resolved.** Model: X3 `(1,2)` is `unknown-custody:superseded-k-beyond-tail` (r2 rule: `busy`); X2 remains `F22-lower-tail`. |
| G-4 end-copy scope | **anchored-floor rule**: copy only the generation the witness names, only when reconciliation establishes `COMMITTED` at that generation's exact tail; once W has left G its floor is final; no remembered list, no later authority | **Resolved, and I withdraw my r1 F-5 recommendation in its favour.** This is the principled version of what I was reaching for: a floor is only ever raised to a tail the witness currently anchors, so the floor never records something weaker than the witness did. It also removes process memory and the undefined authority in one move. |

## 3. Evidence for G-3/G-4 (reviewer model, not law)

`claude-out/probes/d2_model_r4.py` → `d2-model-r4.json` (the r2 model with the anchored copy `Hanch`
and the G-3 rule; five separately timed reads per capture; addendum witness rule).

| Schedule | Evaluations (association × placement of the 10 reads) | Lawful quarantine | Last SEAL of gen 1, `(1,2)` |
|---|---|---|---|
| S1 closure **and** first gen-2 SEAL in one operation | 2,571,804 | 0 | never confirmed (36,209 `hist-floor-insufficient`) — floor final at the operation's start |
| S2 closure is the **final append** of its operation | 8,078,954 | 0 | **confirmed** (116,886) — ordinary end copy, W still `COMMITTED(1,TERMINAL)` |
| S3 crash after TERMINAL, no end copy; next operation's **start** copy | 4,625,438 | 0 | **confirmed** (67,824) — no remembered state needed, as r3 says |
| S4 crash at `PENDING(2,1)` → REVERT → `COMMITTED(2,0)` | 13,743,405 | 0 | never confirmed (515,340) |

S4 is worth stating in the text: **W leaves G at the moment `PENDING(G+1,1)` is published, even if
that append never becomes durable.** After the REVERT the witness is `COMMITTED(G+1,0)`, the anchored
rule (correctly) refuses to raise G, and G's floor is final although generation G+1 is still empty.

## 4. What still has to be written down

### H-1 (must state) — which v8 QUARANTINE rows write a marker, and with which reason

r3 G-1 makes *marker presence* the gate for continuation eligibility. But the durable vocabulary is
two values — `CHECK (reason IN ('uncertainTailLoss','witnesslessRestore'))` — and
`carrier-format.v3.md` §8.1/§12 says a writer refusal "writes no marker, because
`carrier_quarantine.reason` keeps its inherited enum" and that `witnessMalformed` "deliberately is not
a durable reason". v8 §5.4 has ten QUARANTINE rows; v2 maps only some ("tail > witness → treated as
`uncertainTailLoss`"). So today it is not determinable, per row, whether a carrier ends up
*quarantined-with-marker* (continuation-eligible) or *refused-without-marker* (fail closed for ever,
re-detected at each open). Both are defensible; they are very different outcomes for an operator.

Needed: one table, row → {marker reason | no marker}. My reading of what r3 intends: marker
`uncertainTailLoss` for `COMMITTED n > tail`, equal-seq/different-hash (both states), tail > witness,
non-adjacent PENDING, and the start-of-operation floor conditions; marker `witnesslessRestore` for a
definitely absent witness over a non-empty journal; **no marker** for malformed, foreign-project and
"names another generation" outside the lawful next-generation states. If that is right, say so, and
say explicitly that the no-marker rows have **no continuation path in this profile** (a corrupted
witness file is then a permanently closed carrier until some future owner defines recovery) — r3
already says "intentionally fail closed"; it should also be listed with the §3 selected limits.

### H-2 (should state) — precedence between the carrier open dispatch and the witness dispatcher

"Highest journal generation ranges over inherited and v3 rows" is safe only after
`carrier-format.v3.md` §8 steps 1–3 have run: F51 (an inherited generation at or above
`first_generation`), a v3 row below `first_generation`, and an incomplete footprint are decided
there. State that the witness dispatcher runs only on a carrier those steps accepted, so that "highest
generation" can never be an F51 row, and that on the lawful `{A}`/`{A,B}` prefixes the only lawful
witness is `COMMITTED` at the inherited TERMINAL (which is exactly act C's new precondition).

### H-3 (recommendation) — make closure the final append of its operation

S1 vs S2 is the whole availability cost of G-4, and it is avoidable without touching the rule: if an
operation that closes a generation appends nothing after `TERMINAL`, its ordinary end copy (or, after
a crash or a skipped lease re-acquisition, the next operation's start copy) runs while W is still
`COMMITTED(G, TERMINAL)` and covers the whole closed generation. Migration already has this shape
(act A, then B and C, no v3 append). Whole-generation REV and the uint53 rollover can adopt it. With
it, "above-final-floor SEALs remain `unknown-custody` permanently" applies only to the crash window
S4 and to a process that violates the scheduling rule — and r3's cautious sentence about a skipped
lease becomes stronger than it needs to be: under the anchored rule the next writer's start copy
*does* cover the closed generation whenever W still names it, which restores the v8 handoff argument
("that writer's start recorded a tail at or above ours") for exactly the case r2 had to disclaim.
I recommend stating it as SHOULD with the S1/S4 limit disclosed, not as MUST, because a reader's
correctness never depends on it.

### H-4 (minor)

- A start copy with `W = COMMITTED(G+1,0)` names an empty generation: state that no floor record is
  written for `lastSeq = 0` (my model writes none), or that one is and is harmless — either, but say
  which, since item 3 forbids lower/equal-different overwrites and a `(G+1, 0, null)` record followed
  by `(G+1, 1, h)` is a raise.
- G-3: "one-sided generation observations retry, then ordinary final rules" — fine; add that a
  *valid, same-project* W2 lower than W1 is the `lowerWitnessGeneration` candidate (r2 G-5 note).
- The r2 required-evidence list still names "end-copy success and skipped-reacquisition paths" and
  "every generation this operation appended to"; re-word for the anchored rule and add S2, S3, S4.

## 5. Bounded verdict

**D2 r3: G-1 to G-4 resolved as sound design choices; nothing here blocks authoring the normative
successor, provided H-1 (marker/reason table and the no-continuation limit) and H-2 (dispatch
precedence) are written into it; H-3 is a recommendation.** No lawful false diagnosis in 29,019,601 modelled
evaluations across S1–S4. This is not approval of private 111, of any frozen text, model or code,
and says nothing about D3–D6.
