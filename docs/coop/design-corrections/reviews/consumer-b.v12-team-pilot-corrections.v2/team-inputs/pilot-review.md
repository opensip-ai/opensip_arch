# Pilot review (self-audit successor) — syntax-code positive and logical-result-tamper

**Outcome: `PILOT_REFUSED`**

Independent kit-only re-audit of another actor’s syntax-code pilot positive export and its whole logical-result-tamper replacement graph. This is **not** a new origin, **not** whole-consumer ACCEPT, and **not** ROOT-ADMISSION. Consumer `PILOT_READY_FOR_INDEPENDENT_RECHECK` and the v3 `PILOT_ADMITS` grade are not oracles. The v3 report is preserved unedited.

Snapshot-manifest `33507ddb3d006027834dd4c3552ec33193717b97cfc37e19644dd274e01cad1d` **264/264 PASS**. Kit 80/80 `ea2fa750…`. Requirements `855a1464…`. Snapshot bytes were not reminted.

## Exports

| Exhibit | Store SHA-256 | Run | Proof |
|---|---|---|---|
| Positive | `8c3b68ab6d7b8823e59c30ce7432f51416e0ef8bd6bc9718ba33713f360b0158` (889354 B) | `run3:d7b78defeb7524066df48934bbd65cd8e8c3edd7dd083272d0631a86e4bbc6fd` | `proof3:0388fb9721ce4140ab291f8591795e2f59dc600118be51331e3bca141a94760a` |
| Tamper | `c9c1be48d0e7b3b1b315fb7ae5640c9bba9588201e55fb294f38e68b7a8b9f8e` (889474 B) | `run3:5d2ee6759163d735640ae160d08d7524812d5a7f80c7c08848bbd8db09123ed8` | `proof3:94c139961110a4277276b573b1dabdc589df017e2b3d3720f3c234f3b9f463c8` |

Plan `plan2:61407daf…` and `executionInputsDigest` `d72fb03c…` are the same selected-input bytes on both graphs.

## Positive export

**First refused boundary: none** among executed applicable laws.

Complete graph admission passed: payload-registry document-byte joins and C remainder (relation document `53380a24…`, native document `a87331bc…`); `file@enumerated` coverage totality and partition disjointness; file inventoried-file snapshot joins (path, `contentSha256`, `byteLength`, retained bytes); `anchorLaw` cardinalities; `closureMembership` (view/fact producer kind=provider; evaluator kind=evaluator on proof/exec/seal); grammar artifacts in the `kind=grammar` tree including `normalizer.specificationDigest`; `selectedRefs` exact totality; seal/plan policy digest; evidence coverage/import/finding sets; native coverage-account partition equality; L0 `languageVersionBindingLaw` derivation.

Expected proof, evidence, seal, and Run were reconstructed from Plan, ExecutionInputs, enumeration, policy, and selected view/facts/coverage/inventories. Claimed proof fields were comparison operands only (`usedClaimedProofFields: []`). `none` over `file@enumerated` filtered to `hello.rs` is **false**. Sealed verdict **pass**. Complete C of proof/evidence/seal/run equals the claimed records. Proof C SHA-256 `8764a0ac48eb8b3bb26a423606f271c8f6e7ac906b37223d44825558d1bcb85a`.

That positive equality does not admit the tamper graph.

## Tamper export

**First refused boundary (structural, before semantic replay):** claimed predicate value disagrees with the retained witness.

- Name: `tamper-claimed-predicate-value-agrees-with-retained-witness-matches-0`
- Selector: `evaluator-composition-contract.v3.md` §3 — `none` with a known match is false
- Claimed `value`: `true`
- Retained witness `matchingFactIds`: `fact2:852404c12751162c8a75c1c9e67465d2be7b356602fa2f663e03fa838849a717`
- Derived from those matches: `false`
- Proof H reminted; witness digest still `111728e6…`. Distinct enclosing identities are not the complete required join.

**Later structural refusal:** `tamper-claimed-emitWhen-true-has-finding3-0` — claimed `value=true` with `findingIds=[]`. Composition §4 requires one `finding3` per true `emitWhen`.

**Semantic replay: `notReached`.** A full admitted replacement graph must precede any semantic-tamper claim. v3’s semantic refuse `tamper-complete-proof-C-unequal` is withdrawn as a reached boundary.

Input-side joins on the tamper store (payload registry, totality, snapshot joins, selectedRefs totality, closures) passed; the claimed **output** graph is not a complete composition.

## Existing-law implementation misses on these exports

Consumer corrections against published laws, not design gaps:

1. Tamper proof `predicateProofs[0].value=true` while the retained witness still lists the file fact (`none` ⇒ false). Selector: composition §3.
2. Tamper `emitWhen` claimed true with empty `findingIds`. Selector: composition §4.

`newMustIssues` and `newShouldIssues` are empty because both cite existing owners. No absent or contradictory normative selector blocked the joins.

## Limits

| Item | Disposition |
|---|---|
| L1 token-stream tokenisation judgment | **notReached** — frame/custody retained and prefixes parsed; tokenisation is level-spec freedom |
| `component-manifest-schemas.v11` stock inhabitance | **notReached** — prose field contract; no invented stock validator |
| Tamper semantic replay | **notReached** — replacement graph not fully admitted |
| Other four Run stores | out of this scoped recheck; hashes verified unchanged |
| ROOT-ADMISSION / whole-consumer | not performed |
| Real OS/compiler/crypto | future qualification |

Executed checks: 240 probes, 237 pass, 3 fail (`diagnostics/pilot_selfaudit_probes.py`). Probe counts are not whole-charter conformance counts.

Reproduction:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-selfaudit.v4/output/diagnostics/pilot_selfaudit_probes.py
```
