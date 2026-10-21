# CODEX2 Review — D2b-4a Rust3 schema-work budget preflight r1

## Verdict

**PREFLIGHT-CLEAR**

## Required findings

None.

## Frozen-subject integrity

The requested `subject.json` SHA-256 is exact: `735529138b443e1a57bfbfa043cf9ddb0199d4b87f341a1e552691326741eaa4`. All 120 declared members are present, there are no extra files in the frozen `subject/` tree, and every declared byte count and SHA-256 matches. The 14 context pins match both the frozen product copy and the named D2b-4a worktree. Product main and the worktree are both at parent `ca6f5be9ded80c50a143b2f219258c95c80db2e6`; the architecture checkout is at `278d1a27b4cea095b37eed09e7109d8a98be7696`.

The five-path delta is limited to the new schema-work derivation, its Rust3 module exposure, the replacement of Rust3's old fixed-budget extern call, routing nested Rust3 carrier externs through the same path, and making the existing immutable embedded-source slice crate-visible in production. TS2 continues to use its existing JSON/CAN admission helper and fixed budget. The registry's 52-source list, ordering, bytes, pin check, aliases, constructor, selected entries, schema evaluator, and identity JSON profile are unchanged.

## Meter-bound assessment

The derivation matches the frozen evaluator's actual `Meter` charges. With `W(value)` equal to one per value node plus UTF-8 string and object-key bytes:

- the initial `admit_value` walk costs exactly `W`, and a strict byte-free Rust3 CBOR encoding is at least `W` bytes;
- each evaluator call's base credit and string scan are covered; `$ref` siblings and the complete `allOf`/`anyOf`/`oneOf`/`not`/`if` closure are conservatively added;
- `const` and every attempted `enum` member include both the received-value walk and the fixed literal walk, with fixed work safely amortized because `W >= 1`;
- array item evaluation uses the maximum applicable prefix/item coefficient per item, while `contains` is added over the same total item weight;
- object member scanning, `propertyNames`, the maximum single named property, every pattern scan and matching child, and the unmatched `additionalProperties` branch are all covered; fixed required-name lookup charges are included;
- `uniqueItems` includes the extra item walk and a conservative canonical-output allowance. The 32-times-weight allowance exceeds the frozen exact-integer, escaped-string/key, scalar and container encodings. The selected reachable uniqueness sites also bound each item far below the separate canonical byte limit;
- `x-opensip-order` includes its complete input walk and fixed order literal. Operational canonicalization failures remain errors and cannot become successful schema mismatches.

Using `max(array, object, 1)` for mutually type-specific local work is sound; all non-type-specific work is added outside that maximum. Checked additions reject coefficient or fixed-literal overflow. Reference memoization preserves the evaluator's document-owner rule, JSON-pointer decoding and reference-sibling behavior; cycles, missing documents, malformed pointers and arithmetic overflow fail closed. The registry is successfully obtained before the same immutable source slice is reparsed, and `OnceLock` performs the full derivation once.

An independent carrier-graph walk found exactly the 13 Rust3 frame extern roots plus the three direct piecewise-item roots listed in `ROOTS`, with no missing or extra selection. The independently archived factors range through the maximum complete-admission factor 936. At the full 67,108,864-byte frame limit, the largest budget is 62,813,896,704 credits, which fits `usize` on the selected macOS/Linux arm64/x86_64 platform set; conversion and multiplication are checked before the received value is copied into the identity model. Unknown roots refuse rather than fall back.

The accepted D2b duties are sufficient authority for this mechanism. They require strict transport-bounded decoding followed by the selected closed-schema check and prohibit inventing an unrelated payload cap. Deriving a conservative meter budget from the already selected schema and received encoded length implements that requirement without choosing a new schema, entry, evaluator, protocol limit or semantic authority. No further design selection is required for this five-path source slice.

## Evidence and scope

The preserved real red demonstrates the defect at the intended boundary: a schema-legal 33,554,433-byte NFC key produces a 33,556,921-byte strict-CBOR payload below 64 MiB but exhausts the borrowed 64 Mi-credit meter. The final evidence records 291 component tests, 86 identity tests, 16 Rust3 mechanism tests and component Clippy passing. The separately compiled fixed-cap mutation fails at the large-positive runtime assertion, then all 14 pins are restored and a freshly compiled positive passes. The earlier round-one compile failure is correctly retained as a failure and is not treated as runtime evidence.

The public binding record reports both recomputations equal, both existing held receipt bindings current, and no blind invocation. The structural depth research is only an upper-bound analysis; the required actual receiver deepest-valid and one-over witness remains open.

This is a limited source preflight. It does not accept D2b-4a, the 14 unaccepted context paths, or any complete Rust3 receiver. Contextual admission, provenance, counters, typed conversion, complete owning controls and mutations, integration, inventory, and product qualification remain required. The derived credit budget also does not establish wall-clock or allocation qualification; those checks stay with the complete receiver and release gates.

## Non-blocking observations

None.
