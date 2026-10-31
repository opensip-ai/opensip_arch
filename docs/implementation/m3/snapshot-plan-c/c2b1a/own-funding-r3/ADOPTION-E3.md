# Adoption receipt: M1a erratum E-3 (destruction is funded by the allocation charge), 2026-10-30

**Decision LD-COORD-E3 (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1, after R3 review.**

`FUNDING-M1A-ERRATUM-E3.md` is adopted as an additive paragraph to M1a
(`docs/implementation/m3/snapshot-plan-c/c2b/law-revision-r4/PLAN.md`, the M1a paragraph). It says that freeing a value's
storage is covered by the charges of the charged operations that allocated its storage or wrote its elements: both
construction and later charged growth, with a reallocation's free of the old buffer assigned to the growth charge. It
is not charged again. The amortization premise and the scope are stated in the erratum. It changes no price, no cap, no
BOUND-1 term and no published figure.

| Artifact | sha256 |
|---|---|
| **The subject, `FUNDING-M1A-ERRATUM-E3.md`** (the reviewed bytes, never edited) | `4d84cf2d3f11840d0d1abde69983475c69b04a1ccdcd6844edac844d2fffb6b1` |
| **The request, `review/REQUEST-r7-design.md`** | `da47cc546baec2e40c4f02b211765f10cf060a32e05c6b63dcfaf1f806f89a6a` |
| **R3 review r7-design, `review/REVIEW-r7-design.md`** (verdict line `C2B1A-E3: ACCEPT`) | `a5499d69ca4bd33c4bb4ef5d76d7468eff336a4a680cadcee0568c4aaa445319` |

- **The reviewer:** the C2b-1a own-funding Codex reviewer, gpt-6-astra/high, R3-FRONTIER. It is a different vendor from
  the Claude authors: the base text by w11:p1, Opus; the version frozen by w25:p3, Fable 5.1 high.
- **What this does not accept,** as the review states: E-3 is "the separate, explicitly premise-limited law rule". It
  does not establish its premises for the r7 design. R7D-6, owned `impl Fn*` captures with arbitrary destructors, shows
  the premise is not yet met. So R6D-5 stays open for the design until a design revision meets the premise.
- **Binding:** with C2b-1a's binding, beside funding-r3's accepted derivation and E-1.
- **Owner notification:** flagged as an owner-delegated law adoption. It changes no cap or price law.
