# Review: C2a3 callback128E draft implementation and source-guard rebind r1

**Verdict: SOURCE-AUDIT**

**Scope:** `uncompiled-callback-fee-and-guard-rebind-source-only`

The frozen subject manifest SHA-256 is `887ccdd9164fd18acb12a3579d48272ae3709fc493033f3415dc16f7b0e54f78`. All 14 declared members are ordinary files and match their declared byte counts and SHA-256 values.

No required findings.

The accepted-plan binding is exact. The copied plan subject hashes to `d5f89ce6abf6ffdfd6d42fc003d4547713c20848bc4c1ed9d0d4af41ffd2033d`, the accepted review names that same subject manifest and records `ACCEPT-PLAN-ADDENDUM`, and the copied accounting rules, addendum, and call tree match the corresponding member hashes in that manifest.

The production change is exactly the authorized coefficient change in `fund_representation`: `mul(8, envelopes)` becomes `mul(128, envelopes)`. No other production byte differs. Collector behavior, transfer and kernel calls, failure conversion, funding order, fixed and scan charges, object/storage terms, APIs, ABI-facing definitions, and feature surface are unchanged by this delta.

The resulting arithmetic matches the accepted plan:

- `edges = 128 + F*(237 + 23H) + 128E` and `scalar = edges - q`, with `q = 11FH`.
- Relative to the previous `8E` source, the additional cost is exactly `(0, 120E, 7680E)` because the added 120 edges per envelope are scalar and each reserves 64 bytes.
- The initial fixed `128` and scan `12F` charges remain unchanged. Subtracting `prepaid = 128 + 12F` from the final charge still leaves the same `52F` portion of the local `64F` allowance. The callback increase does not consume or duplicate local, scan, comparison, storage, payload-copy, header, or map-bulk categories.

The test change is limited to four corresponding edits:

- The independent expanded `u128` category table changes its callback row from 8 to 128 while retaining the unreduced category calculation.
- Its authority comment names both M-BOUND and the accepted callback-price-r2 category table.
- The exact-source guard embeds `12d82483517c7bb2da9d6bd485566a36000c6bdca0a41ce182d5fe5dc7ada996`, which is the SHA-256 of the new frozen production source.
- The fee-reduction text control now anchors `mul(128, envelopes)?` and replaces it with `mul(1, envelopes)?`.

All five guard anchors occur exactly once in the new production source. The other four anchors and mutation texts remain unchanged, and `include_str!("component_admission.rs")` continues to resolve the sibling production source. The source guard therefore binds the new coefficient-128 bytes rather than relying on the prior coefficient-8 audit.

The larger checked fee can cause an earlier typed Arithmetic or Budget refusal under existing limits. The delta introduces no cap increase, reset, retry, narrowed positive control, or weakened invariant to avoid that result. Existing charge, prefix, latch, and composition test bodies remain otherwise byte-identical. The old queued compiler/native image remains bound to coefficient 8 and excludes these later guard changes, so it cannot qualify this source.

This review is source-only. The supplied 81-case source/hash/arithmetic report was inspected but not executed, and no Rust test or runtime mutation was compiled or run. Complete metadata and operand bounds, primitive contracts, ABI and native allocation/debit/cleanup evidence, executed source guards, feature/privacy/export/lifetime/owner controls, aggregate census and fit, integration, unit acceptance, and product qualification remain open.
