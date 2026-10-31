# Adoption receipt: FUNDING-r4 §8 erratum E-1 (the census implementation-work component), 2026-10-30

**Decision LD-COORD-E1F (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1, after R3 review.**

`FUNDING-R4-S8-ERRATUM-E1.md` is adopted as an additive clarification of the accepted FUNDING-DERIVATION-r4 §8
(funding-r3, `42c24428…`):
- the accepted baseline (B) stays fixed, and the actual census debit becomes (B)+(I);
- the literal-test exception is explicit;
- the source-derived bounds I-ARRAY, I-NAME, I-KEY and I-INT cover the intended work.

It changes no M1a rule, no BOUND-1 term, no cap and no evaluator price.

| Artifact | sha256 |
|---|---|
| **The subject, `FUNDING-R4-S8-ERRATUM-E1.md`** (the reviewed bytes, never edited) | `865204f67f003978ca0b522c18f63cfb8ff948a0ca1740d802924e2e1a3ab4e8` |
| **R3 review r2, `review/REVIEW-r2.md`** (OF-R2-6: "E-1's additive split is acceptable as law text for coordinator adoption") | `0b545c4a66fe26e387b4cc0fe9bd26a385f0d6f1c601ed4279881fb74474ec46` |

- **The reviewer:** codex-c2b1-ownfund-r3, Codex gpt-6-astra/high, R3-FRONTIER. It is a different vendor from the
  Claude author (opensip-c2b1a-ownfund, Opus 5.5 high, w25:p1).
- **What this does not accept,** as the review states: "acceptance of the amendment is not acceptance of its
  implementation evidence". OF-R2-4 and OF-R2-6 (reconciliation on malformed vectors, the remove and move mutants for
  each class, the exhaustion sweep) stay open in the C2b-1a implementation. **AUD-9 may leave PROVISIONAL as to law,**
  but may not freeze until those controls are accepted.
- **Binding:** with C2b-1a's binding, beside funding-r3's accepted derivation.
- **Owner notification:** flagged as an owner-delegated adoption. It changes no cap or price law.
