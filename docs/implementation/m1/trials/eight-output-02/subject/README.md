# Eight-output algorithm correction trial 02

Standing: algorithm trial only. Source registry, hermetic recipe/tool closure, complete TS2/Rust3 wire mapping, control/report source ownership and product integration remain separate. No M1 completion claim. The 28 original schema documents and 589 trial entrypoints remain unchanged; actual current registry must omit three superseded Native2 handshake definitions and use metadata-v2 source paths.

Corrections for actual Claude review01:
- RF1: remove contains from inert Rust projection, eliminate resulting empty intersections/not:{}, and reject empty generated enums. Original-schema runtime retains contains/not/allOf and all other shape constraints.
- RF2: ExactInteger with private i128 storage represents [-2^63,2^64-1] with normalized equality/order, signed/unsigned serialization and integer-only deserialization. Mixed integer domains use this carrier. Original-schema bounds/enums still govern admission.
- RF3: own explicit type-alias renderer using the TypeScript6.0.3 AST printer. Every selected ref has exactly its configured name; schema titles do not rename exports. Provider has45 exports (13 roots plus closure), report589; AST rejects number/any nodes.

All optional Rust fields retain FieldPresence semantics from predecessor. Carriers are inert and do not perform lexical/shape/semantic admission. Their equality roundtrip checks are serde_json value checks, not a claim of byte-canonical encoding. Runtime originals remain in the accepted TS02 shape registry.

Evidence: independent actual Claude original-schema-only witnesses cover589/589refs,1343cases. They all pass exact-codec/original-schema validation, Rust typed value roundtrip, and TS concrete typed assignments. Witness corpus origin/limitations are in witness provenance. Also64091 prior harvested positive rows pass, seven exact integer boundaries and ten invalid forms pass, normalized signed/unsigned equality/order passes. Targeted review01 TS/Rust capability, Hello, mixed-range integer and parser errors=[] regressions pass. Positive examples do not prove all valid instances are representable.

output-e is the tested frozen output. Two fresh runs output-f/output-g are identical across all8 files and to output-e (drift-v2.json). Rust formatting uses /opt/homebrew/bin/rustfmt --edition 2024. The generator remains an explicitly path-bound engineering trial, not selected product tooling. No product source changed.

Reproduce: python3 -B prepare.py; cargo run --offline --locked --manifest-path generator/Cargo.toml -- SUBJECT FRESH_OUTPUT; rustfmt --edition 2024 FRESH_OUTPUT/crates/contracts/src/generated/*.rs; node generate-ts-v2.cjs FRESH_OUTPUT. The preparation and TS runtime imports still reference earlier pinned trials documented in review01. Use separate Cargo targets for mutated/copied probes to avoid stale same-package reuse. compile-rust source points relatively into output-e.
