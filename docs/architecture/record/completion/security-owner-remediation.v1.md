# Delegated owner disposition of the failed security repair confirmation

Status: PROPOSED, not operative until independent consent and recording.
Author: Codex lead. Independent procedural reviewer: Claude, who authored none
of this decision text. This is a decision about further remediation, not a
security acceptance verdict.

## Authority and exact exception

The user's instruction delegates all design decisions to Codex and Claude,
including previously owner-reserved choices. Adopted D-367 records that
standing delegation. The pair receives the terminal CONTESTED security result
as the delegated owner; it does not ask the author or reviewer to pretend that
the failed repair passed.

For this security unit only, explicitly supersede D-368 clause 4's sentence:
“After UPHOLD, the adjudicator performs one bounded confirmation of the repair
diff against the upheld finding, outside the three-exchange budget; failed or
inconclusive confirmation returns the unit to CONTESTED without a fourth
exchange.” The failed result remains CONTESTED. Authorize exactly one additional
corrective successor and one additional bounded confirmation by the same
independent adjudicator, on the terms below. All other units retain D-368's
existing limits. This is a prospective, explicit owner exception to the
single-confirmation limit, never an ordinary fourth exchange or a count reset.

## Decision and required evidence

1. Preserve security v1–v4, all three ordinary exchanges, the independent
   UPHOLD ruling and the failed first bounded confirmation byte-for-byte.
   Their counts remain **three ordinary exchanges plus one failed bounded
   confirmation**. The final history may say CONTESTED-CORRECTED only after
   the additional confirmation accepts the actual repairs. It must retain
   this exception and both confirmation results.
2. Claude may author security v5 solely to repair the surviving SEC3-M1,
   SEC3-M3, SEC3-M4 and SEC3-M5 failures identified by the frozen confirmation.
   SEC3-M2 and SEC3-M6 retain their confirmed dispositions; the separately
   accepted SEC-POLICY-N1 and cap clarification remain intact. Retain each
   exact failed probe as a negative, with legal positive controls and an
   exact v4-to-v5 diff manifest. No unrelated feature or scope expansion.
3. Apply the systemic repair at every changed admission boundary: validate
   the complete closed shape and strict types of every consumed input record
   before comparing values or returning authority or bytes. Validate
   bindings, contexts, witness states, sequence numbers and permission modes;
   malformed inputs produce the owning refusal, never uncaught exceptions.
   A wrapper type or constructor is not a trust anchor. Envelope verification
   rechecks the complete root admission boundary on the value it receives.
   Recovery admits only the existing journal vocabulary and lawful record
   ordering; missing outcome evidence never proves a revert or non-performance.
4. Freeze v5 and its exact diff before dispatch. The same independent
   adjudicator, who authored none of the repair bytes, receives the failed
   confirmation, this recorded owner decision, the corrective successor and
   retained probes. Perform one bounded confirmation of the four surviving
   IDs and any inseparable regressions introduced by their repairs. Preserve
   the two confirmed IDs. No self-certification, synthetic acceptance,
   waived SHOULD-FIX or weakened technical criterion is permitted.
5. Acceptance requires zero surviving MUST-FIX and SHOULD-FIX and a pinned
   per-ID repair disposition. This only releases the corrected security unit
   for the independent integrated architecture review. It supplies no row
   grade, register edit, implementation authorization or product qualification.
6. If the additional confirmation fails or is inconclusive, retain CONTESTED
   and escalate the exact unresolved decision to the user as the exceptional
   issue contemplated by D-367. The pair may not authorize another confirmation
   under this exception. Independent work on other units may continue.

## Alternatives, consequence and reversal

Stopping all work for the user to adjudicate these reproducible technical
failures would leave delegated work unfinished. Dismissing the findings or
restarting the ordinary exchange count would misrepresent the evidence.
A single explicit extension preserves independent challenge while requiring a
systemic repair and retaining an actual terminal limit.

The consequence is one extra bounded confirmation beyond D-368's default;
it creates no precedent for other units. Reversal cancels the extra authority
before confirmation and leaves security CONTESTED. No prior verdict or source
byte is erased. The live readiness register remains unchanged.

## Frozen evidence and recording

The recording must bind this decision, Claude's independent procedural verdict,
the frozen failed confirmation, security v4 freeze, and D-368's adopted text.
The following exact input bytes govern this case:

| Input | SHA-256 |
|---|---|

| `D-368-workflow-proposal.v3.md` | `92febaf2329b767a272ee173a3691a254e7200ca6443ef658d2523ffc92d3f74` |
| `security-freeze.v4.json` | `6219340d84c390e4667ec16b40e1e813974155bd865f49768c322100239e8bb9` |
| `security-repair-confirmation.v1.json` | `4c7f3c29e5bd58b4b4530a838cb71293a60071fa432d3f262a9fd3cc17014497` |
| `security-repair-confirmation.v1.md` | `905ade7e33c4de4f3c600c392d65554e066b0404e5fa7068876d4ea939a1199a` |
| `security-policy-cap-supplement-review.v1.json` | `065d44c5506d2fe6eab5811cda78e48e6f6997a212f24d76e1236d2c7db27550` |
