# Independent adjudication r2 — recovery record owner decisions (six versus eleven)

Reviewer: Claude (actual independent reviewer; Codex owns the decision). 2026-09-18.
Standing: **adjudication of a proposed, unselected decision**; no model or code is approved. r1 stays
unchanged. No frozen/selected/product edit, commit, push or delegation.

## 1. Exact bytes reviewed
`recovery-record-owner-decisions-r2-20260918.md`, 3,080 bytes, SHA-256
`49a2bf3ce15686edb8761adfc542552c5f4d8c023040298eeddcbeb6f0382fe3` (copy in `claude-out/`). Owners as pinned
in r1 (reference 122 model `60b14495…939b`, schemas `79a1b38d…9e91`), plus
`security/trust-clock-cases.v1.json` (122) and the frozen-124 Rust fixtures `trust-clock-cases.ndjson` and
`recovery-cases.ndjson`, read for `claude-out/checks.py`.

## 2. Verdict
**Your correction of my r1 is right, and the refined placement is coherent.** I inferred the wrong owner
for one of my three insertion points. With that fixed, complete-record admission stays compatible with
poisoned-floor recovery and with an expired but well-shaped pending challenge. Three things to settle in
the text before authoring (C-1 to C-3).

### The wrong owner inference (mine)
r1 §5.1 said to validate `TrustClockRecordV1` "at the head of `clock_decision`". Checked: `clock_decision`
reads exactly six members (`evalHighWater`, `lastAccepted`, `anchor`, `revocationIssuedAt`,
`catalogExpiresAt`, `rootExpiresAt`); **0 of the 11 records in the reference clock cases validate under the
eleven-member schema**, and all 1,856 Rust clock-fixture records carry exactly those six keys and nothing
else. My change would have refused every lawful clock input. The eleven-member schema owns the *retained
state* (decoder, recovery challenge, recovery apply); the clock kernel owns a *six-member projection*. Two
owners, as you say.

### What I checked about the refined decision
| Claim in r2 | Result (`claude-out/checks.json`) |
|---|---|
| Schema validation alone is not enough; validate calendar semantics | **Confirmed and necessary**: `2026-02-30…`, month 13, hour 24, year 0000, second 60 are all **valid under the schema** and all rejected by `ts()`. Schema-only admission would admit a record that still bricks the clock — the very defect r1 found, one layer down. |
| Poisoned but well-formed floors remain recoverable | valid |
| Floor set with `lastAccepted` null stays legal | valid — and it should: the clock raises `RECORD_LAST_ACCEPTED_REQUIRED` on it for ever, and recovery is what repairs it (it writes both). Keep this out of `RECORD_SHAPE` explicitly. |
| All nullable members null (fresh) | valid |
| Expired but well-shaped pending (exact 24 h window, long past) | valid under the schema and `_pending_shape` — replaceable by a new challenge |
| Pending window not exactly 24 h | valid under the schema, `PENDING_SHAPE` semantically — so **pending-before-full-record precedence is what preserves the existing detail**, exactly as you order it |
| "No missing consumed field defaults to null" is compatible with existing inputs | Rust fixture: **0 of 1,856** records miss a consumed member. Reference cases: see C-1. |

The orderings are right. Challenge: nonce → observation → report-only → new-window overflow → full record
(including the old pending's semantic shape) → digest/entropy/persistence. Apply: epoch shape →
observation → present pending (`PENDING_SHAPE`) → complete record (`RECORD_SHAPE`) → root admission →
authority → freshness → binding → counters → time. No signature domain or bound-member change is needed,
and none is proposed.

## 3. To settle before authoring

- **C-1 — the reference clock cases are written as overlays.** 5 of the 11 case records are `$from`
  overlays that, as written, lack consumed members (`('$from','anchor','evalHighWater')` ×4). If
  materialisation always yields all six, "no missing consumed field defaults to null" costs nothing; if
  any materialised record still relies on `.get()` returning `None`, the new rule will refuse a lawful
  existing input — the same trap you just caught me in. Run the rule over the *materialised* corpus and the
  mandatory monotone sweep's generated records before writing the sentence, and say in the text that the
  check is on the materialised six.
- **C-2 — `RECORD_SHAPE` replaces existing details for malformed *bound* members.** Today a malformed
  `evalHighWater`/`lastAccepted` reaches the reference as a `Reject` and leaves as
  `RECOVERY.REFUSED:CONTEXT_SHAPE` (challenge) or through the apply wrapper; Rust says
  `Input("RECORD_SHAPE")`. Moving the reference to `RECORD_SHAPE` is the right direction — it removes a
  standing reference/Rust class split — but it changes recorded expectations. List the affected existing
  cases in the successor, and add the record rule to `diagnostic-map.json` beside the observation rule so
  the mapping stays a class rule.
- **C-3 — say what a malformed old pending means at challenge time.** "Reject malformed old state" makes a
  malformed `pendingRecoveryChallenge` block the issue of a *new* challenge, although a challenge replaces
  the pending wholesale and the pending is not digest-bound. I agree with refusing — it is the same
  judgement as the malformed `anchor`: storage corruption, not something recovery silently overwrites —
  but the consequence is that such an installation has **no recovery path at all**, only restore. That
  belongs in the text next to "no storage restoration implemented or implied", so that it is a stated
  limit and not discovered later.

## 4. Agreed without comment
`AdmittedTrustRecord` owning the full eleven-member state and exposing only an immutable six-member clock
projection (built in a child module with private fields, per my 123 F-1); unknown extra members on the
full projection refuse; anchor observation validated semantically, not only by schema; the clock kernel
claims no storage authority and does not admit enclosing fields; bound members, signature domain and
challenge digest unchanged.

## 5. Bounded verdict
**r2 accepted as a coherent owner decision: eleven-member admission at decoder and recovery, six-member
semantic validation at the clock, pending before full record, calendar semantics in addition to the
schema. My r1 placement at `clock_decision` was wrong and is withdrawn. Carry C-1 (materialised reference
cases), C-2 (affected existing expectations and the class mapping) and C-3 (malformed pending = no
recovery path) into the successor.** Approves no model or code.

Evidence: `claude-out/checks.py`, `checks.json`, `hashes.txt`.
