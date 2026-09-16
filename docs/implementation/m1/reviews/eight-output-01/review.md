# Review: m1-eight-output-subject-01

- **Verdict:** CHANGES-REQUIRED
- **Subject manifest:** `/tmp/opensip-implementation/m1-eight-output-subject-01.json`, SHA256 `15e9f02b414f541fd5c543c51f44625b53c5f22f29d76bcf573d4745cbd87629`
- **Scope:** a bounded review of the eight-output generator algorithm trial. It does not approve M1 completion, production generator or dependency selection, a hermetic lane, owner decisions (protocol, control, report), current-root selection, or semantic conformance.

## Summary

Most of the trial reproduces. `prepare.py` regenerates its four inputs byte for byte. All eight outputs regenerate byte for byte. Both TS outputs compile. The 12 metadata roundtrips and 64,091 harvested roundtrips pass in my copy.

The FieldPresence adapter is necessary, and the mutation control confirms it: with the adapter disabled, `errors: []` is dropped again. Every Rust struct has `deny_unknown_fields`, and the output contains no `f64`, set types or defaults module.

The report runtime is the accepted subject02 code, unchanged apart from removed import lines. On the original schemas it gives the expected result for all 43 metadata fixtures and every control.

Three transformation defects block using this as the next integration candidate. None of them shows up in the harvested corpus.

## Required findings

### RF-1: `contains` produces uninhabited Rust carriers for the TS provider handshake

`rust-projection.json` keeps `allOf: [{contains: {const: ...}} x4]` on `Handshake1TypeScriptCapabilitiesV2` and `Handshake1RustCapabilitiesV3`. typify turns both into empty enums:
- `protocol.rs:1883 pub enum Handshake1TypeScriptCapabilitiesV2 {}`
- `protocol.rs:1663 pub enum Handshake1RustCapabilitiesV3 {}`

Because these are required fields, 6 of the 589 targets can never be constructed: the two capability arrays, `TypeScriptHelloV2`, `TypeScriptHelloAckV2`, `HelloV3` and `HelloAckV3`. None of these has a harvested witness.

Small cases:

| case | TS runtime (original schema) | Rust carrier |
|---|---|---|
| `["coverage-v3","fact-identity-fact2","plan-identity-plan2","source-identity-snapshot2"]` as `…provider-handshake.1#/$defs/TypeScriptCapabilitiesV2` | shape-valid | refused (`expected value at line 1 column 1`) |
| minimal `TypeScriptHelloV2` (see `work/control-cases.json`) | shape-valid | refused |

Required correction:
- Drop `contains` in the Rust inert projection, the same way `pattern` and `if`/`then`/`else` are dropped; admission enforces it.
- Make the generator refuse empty enums or uninhabited selected targets.
- Add a runtime-valid synthetic witness roundtrip for every selected entrypoint that has no harvested witness.

I tested the first step: removing the 8 contains-only branches in a work copy leaves 0 empty enums.

### RF-2: integer carriers are narrower than the schema and codec range

The exact codec admits integers in [-2^63, 2^64-1]. Two carriers use `i64`:
- **`Identity3FindingParameters`:** the parameter value declares `minimum -9223372036854775808, maximum 18446744073709551615`, but generates `Integer(i64)` (`identity.rs:2947`).
- **`Sarif2Result`:** the `message.properties` value is an unbounded `integer` and also generates `Integer(i64)` (`output.rs:9564`).

A value of `9223372036854775808` or `18446744073709551615` is shape-valid in the TS runtime and refused by the Rust carrier. This is a refusal, not silent loss, but admitted, digest-bearing records cannot be carried. Every other integer node is bounded within i64 or u64, or is a const/enum in [0, 9663676416].

Required correction:
- Use an exact carrier that covers the full codec range (for example a checked i128 or an explicit signed/unsigned representation).
- Add boundary witnesses at -2^63, 2^63-1, 2^63 and 2^64-1, plus a codec refusal at 2^64.

### RF-3: TS outputs ignore the explicit stable name table

json-schema-to-typescript names types after `title` and adds numeric suffixes to deduplicate.

- **report.ts:** 28 of the 589 table names are missing. That is 24 namespace roots (such as `Dispatch1Root`, `FactBatch3Root`, `Metadata1Root`) plus 4 `$ref` aliases. Title-derived names appear instead, such as `CommandInventorySchemaMajor4TypedHelpVersionParity`.
- **protocol.ts:** the selected entrypoint `FactBatch3Root` is not exported. `TrialSelectedProviderPayload` references a title-derived name and `Handshake1TypeScriptProtocolLimitsV11`. A separate, identical `…ProtocolLimitsV1` is also exported.
- **Dedupe suffixes:** 16 in report.ts and 5 in protocol.ts, such as `CapabilitiesV21/V22/V23`. These can't be told apart from version numbers.

The type probe (`work/ts-type-probe`) confirms these names are absent.

Required correction: control TS naming explicitly. Every selected target must be exported under its table name, and generation must fail if any other name is exported besides declared helpers. Stripping titles alone is not enough: I tried it, and 5 names were still missing with 17 dedupe names remaining.

## Advisories

1. **`not: {}` in the Rust projection.** Dropping `pattern` turns LogicalPath's `not:{pattern}` into `not:{}` (four definitions), which matches nothing. typify 0.8.0 ignores `not`, so nothing is lost today. A tool that honours `not` would refuse every path. Drop a `not` once its body is empty.
2. **Duplicate keys and roundtrip evidence.** The Rust carrier collapses duplicate map keys, keeping the last one; the TS codec refuses them. The roundtrip checks compare serde_json values without `preserve_order`, so they ignore key order and are not byte-level. Feed the Rust carriers only bytes that have passed admission.
3. **Expected over-acceptance.** Rust carriers accept values that violate `pattern`, `propertyNames`, `if`/`then`, `x-opensip-order` or `not`. They also accept a present `null` on non-nullable optional members. The TS runtime rejects all of these.
4. **rustfmt command.** `rustfmt --edition2024` is rejected by rustfmt 1.9.0; `--edition 2024` reproduces output-b. Record the exact command and version.
5. **Stale cargo artifacts.** The environment's shared `CARGO_TARGET_DIR` plus identical package and bin names made the first mutant run reuse a stale binary and falsely pass. Drift and mutation checks need isolated target dirs.
6. **Keyword allowlist.** `prepare.py` silently ignores keywords it does not traverse. None occur in the current input, but it should refuse anything outside the runtime's known and annotation sets.
7. **Absolute paths.** The trial scripts hardcode absolute paths, which matches the README's no-hermetic claim.
8. **Provider closure.** The provider subset has 13 entrypoints and emits no Rust, HelloV3, HelloAckV3 or ProtocolLimitsV3 declarations. Root selection and exclusions remain open.
9. **Report runtime integration.** The runtime code matches subject02 apart from removed imports. The `sources.json` pins are checked, and the 28 embedded `$id`s equal the `owners.json` set. Report owner selection and minimal closure remain open.

## Executed checks (all inside a copy)

- **Frozen pins before and after:** 37/37 subject files, the manifest SHA and the 37 runtime02 files are unchanged, with no extra files. The 44 external input pins are unchanged.
- **`prepare.py` (unmodified):** placed beside a copied `m1-full-generator-trial-01`. All four outputs are byte-identical.
- **Metadata roundtrip binary:** 12/12. **`carrier_probe`:** 64,091 rows, 0 failures, and the differential is byte-identical.
- **Both `tsc` projects:** exit 0.
- **Regeneration with `rustfmt --edition 2024`:** all 8 outputs are byte-identical to output-b and `drift.json`.
- **FieldPresence mutant (isolated target dir):** reproduces the `errors: []` omission.
- **Static Rust scans:** listed in `review.json`.
- **Report runtime on original schemas:** 43/43 fixtures, plus the control matrix (`work/logs/control-matrix.json`).
- **Rust raw-byte control probe:** results in the same control matrix.
- **TS type-level probe:** confirms bigint limits and the missing names.
- **Correction experiments:** no-`contains` and no-`title`.

## Limitations

- No synthesized witnesses for the 479 refs without witnesses beyond these controls. The uninhabited-type scan is regex-based.
- I did not re-validate the carrier-case selection or the flattened input's fidelity.
- I did not re-review the closed R1/R2 runtime findings.
- Toolchain is whatever is installed; there is no hermetic or no-network claim.
- No semantic validation, protocol conformance or M1 completion is inferred.
