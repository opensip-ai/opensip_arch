# Pilot recheck — syntax-code positive and logical-result-tamper

**Outcome: `PILOT_ADMITS`**

Independent kit-only review of another actor’s newly corrected syntax-code pilot and its whole logical-result-tamper export. This is **not** a new origin, **not** independent acceptance of this reviewer’s own authored workflow work, and **not** whole-consumer ACCEPT. Consumer `PILOT_READY_FOR_INDEPENDENT_RECHECK` and prior helper grades are not oracles.

Snapshot-manifest `33507ddb3d006027834dd4c3552ec33193717b97cfc37e19644dd274e01cad1d` **264/264 PASS**. Kit 80/80 `ea2fa750…`. Requirements `855a1464…`. Snapshot bytes were not reminted.

## Exports

| Exhibit | Store SHA-256 | Run | Proof |
|---|---|---|---|
| Positive | `8c3b68ab6d7b8823e59c30ce7432f51416e0ef8bd6bc9718ba33713f360b0158` (889354 B, 90 blobs) | `run3:d7b78defeb7524066df48934bbd65cd8e8c3edd7dd083272d0631a86e4bbc6fd` | `proof3:0388fb9721ce4140ab291f8591795e2f59dc600118be51331e3bca141a94760a` |
| Tamper | `c9c1be48d0e7b3b1b315fb7ae5640c9bba9588201e55fb294f38e68b7a8b9f8e` (889474 B, 90 blobs) | `run3:5d2ee6759163d735640ae160d08d7524812d5a7f80c7c08848bbd8db09123ed8` | `proof3:94c139961110a4277276b573b1dabdc589df017e2b3d3720f3c234f3b9f463c8` |

Plan `plan2:61407daf…` and `executionInputsDigest` `d72fb03c…` are the same selected-input bytes on both graphs.

## Positive export

**First refused boundary: none.** Structural admission passed, then complete semantic replay passed.

Independently reconstructed expected proof from retained selected inputs only (plan, execution-inputs `selectedRefs`, view/facts/coverage/inventories, policy/rule-program). Consumer `compose_proof` was not an oracle.

- `evaluationInputRefs` (12) equals `selectedRefs` (11) plus the execution-inputs manifest. No `rule-program` / `policy` extras.
- `none` over `file@enumerated` filtered to `hello.rs` is **false** (known file fact + complete Coverage).
- No findings; gating rule outcome pass; sealed verdict **pass**.
- Complete proof C SHA-256 `8764a0ac48eb8b3bb26a423606f271c8f6e7ac906b37223d44825558d1bcb85a` equals the claimed proof C. H identity equals `proof3:0388fb97…`.
- Evaluator `closure2:a8a0903d…` is in `plan.semanticClosures`. Grammar artifacts sit in the `kind=grammar` closure tree. L0/L1 FACT-IDENTITY frames are retained (custody).

## Tamper export

**First refused boundary (semantic, after structural admission):** complete proof C/H inequality against the independently derived expected proof from the same selected inputs.

Structural admission of the replacement graph passed first (schema, blob rehash, H frames, `evaluationInputRefs` equality, plan/snapshot/evaluator joins, reminted enclosing identities). Semantic replay was not reported before that.

Fresh derivation remains verdict=`pass`, atom=`false`, expected proof `proof3:0388fb97…`. Claimed tamper verdict=`fail`, atom=`true`. Enclosing proof/evidence/seal/run identities reminted. This is a result-tamper, not a stale-hash digest flip.

## Limits

| Item | Disposition |
|---|---|
| L1 token-stream tokenisation judgment | **notReached** — frame/custody retained; tokenisation is level-spec freedom |
| `component-manifest-schemas.v11` stock inhabitance | **notReached / CANDIDATE-NOT-APPLIED** — prose field contract, not an executable stock schema; no invented validator |
| Other four Run stores | out of this scoped recheck; hashes verified unchanged |
| ROOT-ADMISSION / whole-consumer | not performed |
| Real OS/compiler/crypto | future qualification |

Executed applicable checks: 129 pass / 0 fail (`diagnostics/pilot_recheck_probes.py`). Probe counts are not whole-charter conformance counts.

Existing-law implementation misses on these two exports: **none** among executed applicable laws. Absent/contradictory norms: **none**.

Reproduction:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-recheck.v3/output/diagnostics/pilot_recheck_probes.py
```
