**Verdict: ACCEPT-TRIAL-UNIT** for manifest `ffafa677…3856e`, with no required findings. I wrote `review.json` and `review.md` in `m1-eight-output-review-02/`; my scripts and logs are under `work/`. Pins were identical before and after for all 63 subject files, runtime02, the 44 external inputs and the witness origin files. I ran everything in a copy with separate cargo target directories.

**Review01 findings:**
- **RF-1 resolved.**
  - Rust has no empty enums left, and the generator now refuses one: fed subject01's projection, which still has `contains`, it stops with `uninhabited generated enum Handshake1RustCapabilitiesV3`.
  - The capability array and HelloV2 cases from review01 now roundtrip.
  - Witnesses for all 589 refs roundtrip in Rust (1343 cases), as do all 1781 of my own variants.
- **RF-2 resolved.** Both sites now use `ExactInteger`.
  - I built boundary values Python accepts at FindingParameters and at the Sarif `message.properties` map: -2^63, 2^63, 2^64−1 and mixed maps.
  - All are valid in the TS runtime, roundtrip in Rust and assign in TS; the codec rejects 2^64 and −2^63−1.
  - The subject's integer probe reproduces.
  - 307 integer-boundary variants across 43 refs also pass.
- **RF-3 resolved.** An AST audit found:
  - `report.ts` exports exactly the 589 table names, plus the unchanged runtime.
  - The provider exports 45 names, including `FactBatch3Root`. That set equals a `$ref` closure I computed separately.
  - There are no title-derived or numeric-suffix names, and no `number`, `any`, `never` or numeric-literal types.
  - 6 negative type controls fail as intended on both TS 6.0.3 and 7.0.2.
- **Review01 advisories:** `not:{}`, the rustfmt command and stale cargo artifacts are resolved. Duplicate keys, expected over-acceptance, the keyword allowlist, hardcoded paths and root selection are carried forward.

**What I ran to check this independently:**
- The witness checker (in a copy, with its output path redirected) matches its frozen results.
- The TS runtime on the original schemas agrees with Python on all 1343 witnesses and 1781 variants.
- My own TS assignments (3,434 statements, strict with `exactOptionalPropertyTypes`) have 0 errors on both compilers. I first confirmed the compile was really checking types, because it finished suspiciously fast.
- Two fresh regenerations match output-e and `drift-v2.json` on all 8 files.
- `prepare.py` reproduces its inputs byte for byte, and the harvested 64,091 rows and the review probes pass.

**Advisories:**
1. **Unknown keywords:** the renderer ignores keywords it doesn't support instead of refusing them, so an array with `prefixItems` + `items:false` renders `never[]`. This case isn't in the current input.
2. **Nested numeric enums:** the renderer's type audit doesn't catch a JS-number literal nested in an object enum. None occur in the current projection.
3. **Integer const/enum widening:** the integer rule turns 207 const/enum nodes into `ExactInteger`. That's fine for inert carriers, but those closed sets are no longer in the Rust types.
4. **Side effect:** `generate-ts-v2.cjs` writes `ts-exports.json` beside the script, outside the fresh output directory.
5. **Two TypeScript versions** are in use (6.0.3 for rendering, 7.0.2 for compiling); pin one.
6. **Witness checker output path:** `witness_common.py` hardcodes the origin directory, so the checker writes there unless redirected.
7. **Evidence limits:** witness strings are minimal, and 263 refs got no valid variants. Every valid value being representable is still not proven.

The review makes no claim about the registry or tool closure, protocol translation, owner decisions, integration, or M1 completion.
