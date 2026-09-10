I'll work only in the six owned files: direction-specific sufficiency, current-source dependency partitions, multi-provider same-U bindings, owner exception classes, and v8 output.I'll apply the five owner-law fixes next: direction-specific sufficiency, current-source deps, per-provider same-U bindings, native exception classes, and v8-only output.Incoming scopes without coverage should be covered by a per-provider attestation when no S→U Coverage exists. I’ll make that pairing explicit.v8 of the six owned atom files is finished. Bounded unit checks passed; this is not Run acceptance.

`/tmp/opensip-architecture-review-env/bin/python -I -B …/check-atoms.v1.py --output /tmp/opensip-design-corrections/grok-atom-contract.v8` → **50/50 ok** (the previous 44 plus 6 direction/partition/provider/carrier probes). Default is stdout only; v6 receipts were not rewritten. Root’s 25 frozen/exported replay controls remain a separate qualification.

### Corrections (owner law, not withdrawals)

1. **Direction-specific sufficiency.** Native `sufficiency_v2` `target_exported` / `target_affected` apply only to `endpoint=target`. Unknown external-consumer closure is unknown *incoming* use of an exported target. Outgoing source-partition RC-2 already counts that partition’s referrers; it does not decide whether this source made an outgoing edge. Paired controls: outgoing `none` on an exported source with complete local search stays true with `exportsClosed=open`; incoming `none` on the same closed-world is `external-consumers-unknown` / `target-export-unknown`. Resolution-incomplete is unchanged.

2. **DEPENDS_ON current-source pairing.** Owner: `reachability → calls@resolved-callee`, `clones → declares@syntactic`. Same `sourceSubjectKind` (both symbol): pair dep Coverage to scopes containing the current native ids. Different kind would owe whole-source *(S,T)* search. Never `covs[0]`; never AND unrelated partition B into A’s outgoing view. Incoming still owes every *S* partition. Attestation of whole *S* owes all dep partitions of *(S,T)*.

3. **Per-(U, provider) contributors.** Enumeration-plan does not forbid two selected enumerators on one *U* across workspace cells. Bindings are no longer collapsed to the first PC. Program identity remains *U* (expected IDs union by *U*). Incoming `scopeRefs` / inventory locators are that provider’s owned set. Uniqueness stays `(planId, providerClosure, S, T, relation, minResolution)`. Unavailable bindings carry cell family; foreign-family unavailable work discloses `cross-family-edge-not-owed` and does not poison a TS closure.

4. **Owner AdmissionError.** `_validate_incoming_rc_law` and `_derive_scope_commitment` catch native’s separately loaded `AdmissionError` (and jsonschema `ValidationError`), not this file’s `C.AdmissionError`. Invalid typed carriers refuse `ATOM_NATIVE_CARRIER` / `INCOMING_SEARCH_SCHEMA`; they are not coerced to unknown. Incomplete descriptors (missing subject-scope2 fields) still mean metadata absent.

5. **Checker output.** `--output DIR` writes the current report. No default write to v6.

### Standing

These 50 cases are synthetic admitted-map probes that assume native owner admission. They are not a full independent Run and not compiler qualification. Root’s 25 full controls (21 ADMIT + 4 reminted semantic REFUSE) live in `reviews/evaluator3-replay-controls.v1`.

### Owned-file SHA-256 (v8)

| file | sha256 | bytes |
|---|---|---|
| `evaluator-projection-registry.v1.json` | `e77be0dd65f431f94cc3c70153ec90509fb886d699755499e9a8237724ce5609` | 58836 |
| `target-attribution.schema.v1.json` | `788bd9d000fb1da830ef368d14c119f441f7b60e8a56f8da3467ef0fbf0ed90e` | 13480 |
| `atom-evaluation-contract.v1.md` | `c101c71509a9e9fccf68ba22820038b778a5e13e9190c2e7e8e3e01f6a2c7cf9` | 17574 |
| `atom_model.v1.py` | `e033b6584a623b7186893c32fa652f3e5247bc334497f0b0cb3594a4ccefdbf4` | 83760 |
| `check-atoms.v1.py` | `c61cb59eecd4de8ae2b817fa23fbee0e0891c54b7f478187f837447d78694f18` | 68590 |
| `incoming-search.schema.v1.json` | `e1a84b8a3de6672eab0646f9174feec514d50d3d23e82b7b9b2f85d2cb923e0a` | 12310 |
