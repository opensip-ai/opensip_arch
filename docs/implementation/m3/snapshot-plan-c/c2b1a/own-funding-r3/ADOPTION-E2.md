# Adoption receipt: FUNDING-r4 §3.7 erratum E-2, v4 (the OBJECT entry width is the type's size), 2026-10-30

**Decision LD-COORD-E2 (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1, after R3 review.**

`FUNDING-R4-S37-ERRATUM-E2-v4.md` is adopted as an additive correction to FUNDING-r4 §3.7 (funding-r3), beside E-1.
- **Entry widths:** every own B-tree insert's entry width is `size_of::<K>() + size_of::<T>()`; the retained objects
  map is 72, not the stale constant 64.
- **Per-insert effect:** `+88(h+1)` allocation bytes and `+168h` pass bytes, `256h+88` in total.
- **Per-pass and per-call bounds:** per call they carry an explicit pass count p and the accounting interval at
  dbe4955. The object-domain k bounds are necessary-domain bounds, not feasible maxima.
- **Withdrawn:** the earlier fit-margin and refusal-order claims.

No M1a rule, BOUND-1 term or cap changes. The insert's formula is unchanged; only its width input becomes the type's
size.

| Artifact | sha256 |
|---|---|
| **The subject, `FUNDING-R4-S37-ERRATUM-E2-v4.md`** (the reviewed bytes, never edited) | `5439f215830e78301d74ee47eacc27c6e432ddd9932a266020ded4fd19a13d29` |
| **The request, `review/REQUEST-r9-design.md`** | `42bf4d50c3d606c41875645f720967fcf041a0751cec190d0a9c6c8e003f0a2f` |
| **R3 review r9-design, `review/REVIEW-r9-design.md`** (verdict line `C2B1A-E2: ACCEPT`) | `ef8bf57cbd0f4045c5610fe57649bf6ca532c1775dbcaa2a476ba198f46825b1` |

- **The reviewer:** the C2b-1a own-funding Codex reviewer, gpt-6-astra/high, R3-FRONTIER. It is a different vendor from
  the Claude author (w25:p3, Fable 5.1 high).
- **What this does not accept,** as the review states: "the frozen correction and its bounded accounting claims". It
  does not accept the product implementation. E-2 v1 to v3 are superseded and are not adopted.
- **Binding:** with C2b-1a's binding, beside funding-r3, E-1 and E-3.
- **Owner notification:** flagged as an owner-delegated adoption. It changes no cap or price law.
