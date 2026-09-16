**Verdict: CHANGES-REQUIRED** for manifest `15e9f02b…87629`. I wrote `review.md` and `review.json` in `m1-eight-output-review-01/`; my working files and logs are under `work/`. The frozen pins matched before and after, and I ran everything in a copy.

**What reproduces:**
- `prepare.py`, unmodified, regenerates its 4 inputs byte for byte.
- All 8 outputs regenerate byte for byte, and both `tsc` projects compile.
- The 12 metadata and 64,091 harvested Rust roundtrips pass.
- FieldPresence is necessary: with it disabled, the parser-refusal case loses `errors: []` again, matching `carrier-roundtrip-01.log`.
- Every Rust struct rejects unknown members, and there is no `f64`, no set type and no defaults module.
- The report runtime is subject02's code with only the import lines removed. On the original schemas it gives the expected result for all 43 metadata fixtures. It also rejects every control case: pattern, `if`/`then`, `x-opensip-order`, `not`, float, out-of-range integer and duplicate keys.

**Required findings.** The harvested corpus can't catch any of these:
1. **Some Rust carriers can never hold a value.** The `allOf`/`contains` branches become empty enums (`protocol.rs:1883` for `TypeScriptCapabilitiesV2`, `protocol.rs:1663` for `RustCapabilitiesV3`). As a result, 6 targets refuse every value, including the selected TS provider entrypoints `TypeScriptHelloV2` and `TypeScriptHelloAckV2`. A sorted capability array and a minimal HelloV2 both pass the TS runtime and are refused by Rust. Removing `contains` from a copy of the Rust projection leaves no empty enums.
2. **Integer carriers are too narrow.** `Identity3FindingParameters` declares integers from −2^63 to 2^64−1, and a Sarif message-property value is unbounded, but both generate `Integer(i64)`. Values from 2^63 up to 2^64−1 pass the TS runtime and are refused by Rust.
3. **TS outputs don't use the stable name table.** Names come from schema titles and get numeric suffixes like `…V11` or `…V21`. `report.ts` is missing 28 of the 589 table names, and the provider doesn't export `FactBatch3Root`. Stripping titles alone still leaves 5 names missing and 17 suffixed names.

**Advisories:**
- **`not: {}`:** dropping `pattern` from LogicalPath's `not` leaves a `not: {}`, which matches nothing. typify ignores it today, so nothing is lost yet.
- **Duplicate keys:** Rust keeps only the last duplicate map key.
- **Evidence strength:** the roundtrips compare values, not bytes or key order.
- **Commands:** `rustfmt --edition2024` from your instructions fails on rustfmt 1.9.0; `--edition 2024` is the working form.
- **Stale builds:** the shared `CARGO_TARGET_DIR` let cargo reuse a stale binary, so my first mutant run falsely passed. A separate target directory fixed it.
- **Keywords:** `prepare.py` silently skips schema keywords it doesn't know.

The review approves no owner decisions, root selection, tool selection, hermetic claim or M1 completion. One limitation: apart from these control cases, I didn't create test values for the 479 refs that have no harvested examples, and my scan for types that can't hold any value is regex-based.
