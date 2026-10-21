# CODEX2 review — D2b-4b descriptions r1

## Verdict

**ACCEPT-DESIGN-UNIT**

## Independent assessment

I independently rehashed subject manifest `47fc57d66da79b9d6fcdf142ee24586ca895637a78d57c99f9e2fde2418b45b1` and its three declared members. The frozen stage contains exactly the manifest, README, source record, and successor record. The outer review subject's pins resolve to those exact frozen bytes.

The live product and architecture heads match `c12e63063e09ce25e07028b60414d8d2a5b5dae3` and `cc95944033afb016921fd455a6543b8ec3be99df`. The current product lock, inventory v237, accepted D2b-4b code subject/review/root assent, accepted inventory v237 subject/review/root assent, prior contract184, and all 24 current source pins match the source record's byte counts and SHA-256 values. The current product bytes remain identical to the accepted D2b-4b source pins.

The current lock contains 197 inventory successors, 184 contract successors, and 145 inventory-passage inheritance entries. The source record preserves all 145 inheritance entries by value. Resolving those entries against their pinned inventories yields exactly one current meaning among the six paths in this contract: the accepted contract184 passage for `provider_protocol.rs`. The other five paths have no inherited or current-direct meaning.

The successor therefore has the correct shape: five raw-inventory passage overrides and one explicit passage supersession. Each override points into inventory v237, resolves to its declared physical path, and has a `before` value equal to the raw inventory description. The supersession's `before` value equals contract184's accepted effective passage, and its `supersedes` reference exactly pins that record, inventory v236, and `/files/48/description`. No existing supersession targets the same reference, so there is no collision or double supersession. Replacing that one meaning and adding five direct meanings produces the declared 150-meaning next-inventory projection; a future projection must fold the supersession rather than retain the stale contract184 passage.

The six `after` passages accurately describe the integrated implementation:

- `provider_protocol.rs` now exposes the D2b-4b host builders, request/sender, and participant, while its accumulator query reports only the next prefix, digest, or body-fragment length for pre-allocation charging. The passage preserves the base receiver role and does not grant identity, worker-admission, or universal allocation-free authority.
- `rust3.rs` exports the scoped D2b-4a receiver/context surface together with the D2b-4b plan, projection, request, schedule, sender, source, and participant surface. Reference-scope host construction is available at all counts under the selected token, while receive-side census/reference admission remains gated to 4c.
- `receive.rs` transfers the original admitted candidate buffers exactly once and only after DONE, and clears candidates on discard or fault paths.
- `receive_tests.rs` covers original-buffer identity, one-time DONE handoff, completion, invalidation, and the shared host/participant fixture surface without turning test support into production authority.
- `schema_work.rs` retains the exact 52-source derivation and expands its explicit root set from 16 to 18 solely for `RustSubjectScopeV1` and `StageRequestV3` host construction.
- `tools/operability/exceptions.json` preserves all 115 accepted ownership rows and all 453 parent lexical constructor rows, adding exactly nine ordinary send-module rows for a total of 462. The description correctly treats this as a mechanical census change with no mint authority.

The 18 new inventory-v237 rows remain byte-exact and retain their accepted raw descriptions. The contract changes no raw inventory, inventory binding, prior contract, inheritance, source, registry, schema, alias, receipt, or runtime bytes. It grants no FA-2/reference worker admission, trial07 replay, C4/H authority, production factory/caller, source39, qualification, or project completion. Binding contract185, root assent, status reconciliation, and the later 150-meaning inventory projection remain separate work.

## Findings

None.
