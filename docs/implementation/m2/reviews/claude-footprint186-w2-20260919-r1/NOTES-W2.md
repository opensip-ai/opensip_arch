# NOTES-W2 — my 186 W-2 "fails closed" argument was wrong; the limitation, measured

Separate from `REVIEW.md` in this directory, which is unchanged (its `hashes.txt` still verifies). Written 2026-09-19 after the owner sent an executed counterexample (`/tmp/opensip-implementation/reviews/footprint186-w2-owner-counterexample.json`, copied as read to `claude-out/w2/`). Not a new frozen review and not approval of anything.

## 1. What I claimed, and why it was wrong

In 186 W-2 I wrote that an unbound `transitionExecutionId` is tolerable because "a wrong id makes every real binding look foreign → carrier present ⇒ QUARANTINE; the only ABORT cells need an absent/own carrier and no own fence, **which cannot coexist with a real post-fence state**. So a wrong id fails closed."

The bold clause is the error. It reasons only over *lawful crash prefixes* of the stated write order. But the whole point of the quarantine cells is *damaged* states — observations the write order never produces. "Carrier absent although this execution has fenced the source" is exactly such a state, it is observable, and with the true id the selector correctly answers QUARANTINE. With a wrong id the true fence is read as "an earlier execution's fence" (`fence = other`), the absent carrier is read as "nothing was created", and the pre-fence cells apply. I assumed away damage while arguing about the component whose job is to detect damage. The owner's objection is correct in full.

## 2. Reproduction and extent (`claude-out/w2/w2_sweep.py` → `w2_sweep.txt`)

On the frozen 186 bytes, through the real `recover_transition_journal`:

- **Owner's case reproduced exactly**: `PREPARED` forward, source fenced by the true execution, carrier and target observed absent, `selected=from` → true id **QUARANTINE**, wrong id **ABORT** (`journalStateAfter: ABORTED`).
- **Extent.** Holding the physical truth fixed (fence, carrier binding and image all bound to the true execution) and varying only the supplied id over 864 states (2 cases × 6 journal states × fenced/unfenced × 6 carriers × 3 selections × target present/absent): the outcome changes in 34.
  - **12 are dangerous** — the source *is* fenced by the true execution and the wrong id yields a progress action:
    - 9 × QUARANTINE → **ABORT** (`LEASED`, `PREPARING`, `PREPARED`; forward with target present or absent; ancestor);
    - 3 × QUARANTINE → **RELEASE-ONLY** (`ABORTED` journal) — this one the owner did not list: it goes on to **retire the active slot** over a fenced source, destroying the evidence, and through `sequence` it would then be eligible for Phase C.
  - All 12 have `carrier = absent` and `selected = from`; none is a lawful crash prefix. That is the precise shape of the hole: *true fence + missing carrier + wrong id*.
  - The other 22 changes fail in the safe direction (ABORT/RESUME-COMMIT/RELEASE-ONLY → QUARANTINE), which is the part of my argument that was right and is why the 4,320-state sweep and my phase probe saw nothing: every state there was evaluated with the true id.

My 186 sweep therefore does not cover this at all; it varied the *observed* attribution (none / other / mine / mine-wrong-intent) but never the *supplied* identity against a fixed truth. The verdict sentence "never aborts past this execution's fence" is true only under a correct `transitionExecutionId`; it should be read with that qualifier.

## 3. Assessment of the proposed correction

Owner proposal: an explicit **coherent active-slot execution/journal binding prerequisite before the model is invoked**; do not claim wrong caller assertions always fail closed; no new public journal member; product host binding remains owed.

I agree, and I think it is the only honest option at this layer:

1. **It cannot be fixed inside the selector.** The selector's notion of "mine" *is* the supplied id. Any rule of the form "be suspicious when a foreign fence exists" would break the legitimate repeated-intent / pre-existing-fence case that 186 exists to handle (a retained root really can carry an earlier execution's fence). The two situations are observationally identical to the selector; only an authenticated id separates them.
2. **So the id must stop being a caller assertion and become an admitted observation**, with the same standing as the slot observation: read from the active-slot carrier as one coherent revision with the exact journal reference, admitted under custody, and `unavailable` (→ unknown-custody, model not called) when it cannot be read or does not cohere. That is a Phase A prerequisite in 181's terms, which is where it belongs — before registry/lease/footprint, because everything after depends on it.
3. **What the reference can and cannot show.** It can show ordering (the model is not invoked without an admitted binding; a missing or incoherent binding stops unknown-custody; the spy shows no footprint read first) and it can carry the counterexample as a *documented limit* vector. It cannot show that a host binds correctly. The text should say exactly that, replacing any "fails closed" language — including mine.
4. **Wording I would avoid:** "the execution id is verified". Nothing here verifies it; the carrier binding is itself an observation under custody. "Admitted from the active-slot carrier as a coherent revision with the journal reference; never supplied by the invocation" is accurate.
5. **One thing to add that the proposal does not mention:** the `ABORTED → RELEASE-ONLY` flip. Because it leads to slot retirement, the prerequisite must gate terminal handling too, not only the ABORT/RESUME cells. A regression should pin it.
6. **Tests worth having in the successor:** the owner's case and the three RELEASE-ONLY cases as explicit "limit" vectors asserting the *documented* wrong-id behaviour (so the limitation cannot silently change); binding `unavailable` and binding-present-but-journal-ref-mismatch → stop before any footprint read; and a sweep like mine (truth fixed, supplied id varied) reporting the dangerous count, so the size of the hole is tracked rather than argued.

## 4. Effect on my 186 review

- W-2 should be read as: **the unbound execution id is a real limitation, not a tolerable one; with a wrong id the selector can ABORT, or release and retire, over a source the true execution has fenced, in 12 damaged states.** Severity: I would now place it with the findings rather than the low-severity notes — not because the reference is wrong for a correct id (it is not), but because my review said the opposite of the truth about a wrong one.
- 181 F-1/F-2 closure, the 4,320-state result, the Phase C stops and T-1 are unaffected: all were measured with the true id.
- The mistake is mine, not the owner's text: the protocol already listed the coherent active-slot revision as a host obligation and never claimed fail-closed behaviour. I added that claim.

## 5. Limits of this note

Same synthetic model and assumptions as the review. The 864-state comparison fixes the truth to "everything real is bound to the true execution"; mixed-truth damage (e.g. a carrier bound to a third execution) was not enumerated. No draft of any successor was inspected.
