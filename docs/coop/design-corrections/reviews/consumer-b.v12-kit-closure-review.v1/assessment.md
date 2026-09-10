I’ll treat this as a bounded structural-admission review of the corrected syntax-code Run: verify the 147-file snapshot, then walk kit closure laws independently.Snapshot hashes matched. Next I’ll inventory kit closure laws, then walk the syntax-code store against those laws rather than the consumer’s helper claims.I’ll implement an independent structural walker from the kit registries, then run it against the corrected syntax-code store.I’ll write an independent structural walker from those kit laws and run it against the syntax-code store.**Verdict: `SCOPED_CLOSURE_REFUSED`**

This is structural admission of the corrected syntax-code Run only — not whole-consumer acceptance, semantic-proof evaluation, or root admission. 63 passing checks are not full admission.

Snapshot **147/147** PASS (`f0339fa8345a5c7ce929a6a7ccd54239469d9862ce7d7e76700ded7a4ba65511`). Independently reminted run `run3:f2542b3afb9c5042438370893f9932830b4b6b1ac17f16299d35ed55d49db918`.

### Refusal (existing law, not a new design gap)
`identity-schemas.v3.json` `closureMembership.direct`: `evaluation-seal.evaluatorClosure` must be in `plan.semanticClosures`.

- Plan selects provider `closure2:00ec14d1…` and grammar `closure2:2951220e…`
- Evaluator `closure2:2a9cfd9286fa5f4fb752a8f8d8e42792fe471d9c71e0abcd69ce27e59129ccec` is retained (`kind=evaluator`) and proof=seal, but **is not Plan-selected**

### What was walked
C/H remint, acyclic proof/evidence/seal/run joins, capability-manifest derived id, relation ladders and anchor cardinalities, file inventory path/digest/length/blob, clones L0 recompute from syntax languageVersionBinding, RC-6, coverage totality/partition, digest preimages, syntax grammar-only context. TS/Rust nested joins and import payloads are **NOT_APPLICABLE** on this graph.

### NOT_REACHED
Semantic proof evaluation, root admission, full `derive_outcome`, L1 token-stream framing judgment.

Reproduce:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-closure-review.v1/output/probes/structural_admit.py
```

Deliverables: `closure-review.md`, `closure-review.json` (73 laws: 63 PASS / 1 REFUSED / 6 N/A / 3 NOT_REACHED).
