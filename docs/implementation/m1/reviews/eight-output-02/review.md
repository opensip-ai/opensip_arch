# Review: m1-eight-output-subject-02

- **Verdict:** ACCEPT-TRIAL-UNIT
- **Required findings:** none
- **Subject manifest:** `/tmp/opensip-implementation/m1-eight-output-subject-02.json`, SHA256 `ffafa677fb0db256ae62323989a312239c34fe18bf18fb349bd5490cb3e3856e` (63 files)
- **Scope:** acceptance of the generator transformation algorithms only, over the 28-schema/589-ref trial input.

This review does not approve:
- M1 completion;
- registry or tool closure, or a hermetic lane;
- full TS2/Rust3 protocol translation or current-root selection (three superseded Native2 handshake definitions remain among the targets);
- control or report owner resolution;
- effect, lane or product integration;
- any semantic conformance.

## Inherited finding dispositions

### review01 RF-1: RESOLVED

- **Projection:** the Rust projection no longer contains `contains`. It has no `not:{}` and no empty `allOf` branches.
- **Output and guard:** output-e has no empty enums, and the generator now asserts that every enum has variants.
- **Guard control:** running the generator on subject01's projection, which still has `contains`, panics with `uninhabited generated enum Handshake1RustCapabilitiesV3`.
- **Review01 cases:** the sorted capability array and the minimal `TypeScriptHelloV2` now roundtrip.
- **Coverage:** all 1343 witnesses, covering 589/589 refs, and all 1781 reviewer mutants roundtrip.

### review01 RF-2: RESOLVED

- **Carrier:** both sites now use `Integer(ExactInteger)`. It stores an i128 that can only be built from i64 or u64 deserialize calls.
- **Boundary cases:** I built targeted cases that Python accepts:
  - FindingParameters at -2^63, -2^63+1, -1, 0, 2^63-1, 2^63, 2^64-1, plus a mixed map;
  - Sarif `message.properties` at -2^63, 2^63, 2^64-1, plus mixed and empty maps.

  All are valid in TS02, roundtrip in Rust and are assignable in TS. The metadata-v2 codec rejects 2^64 and -2^63-1.
- **Subject integer probe:** reproduced, covering 7 boundaries, 10 invalid forms, and normalized equality and ordering.
- **Mutation corpus:** 307 integer-boundary mutants, across 43 refs that accept values above i64::MAX, all pass.
- **Remaining `i64`:** only the FieldFilter branches, which are bounded to [0, 1000000].

### review01 RF-3: RESOLVED

The AST audit uses the TypeScript 6.0.3 API, the same one the renderer prints with.
- **report.ts:** exports exactly the 589 table names. Its other exports are only the verbatim subject02 runtime plus `createTrialReportShapeRegistry`.
- **protocol.ts:** exports 45 names plus `Json`. That covers all 13 roots, including `FactBatch3Root`, and equals an independently computed `$ref` closure.
- **Naming:** no title-derived or numeric-dedupe names, and no type references outside the table.
- **Negative type controls:** all 6 fail as expected under tsc 7.0.2 and 6.0.3.

### review01 advisories

| review01 advisory | Disposition |
|---|---|
| ADV-1 (`not:{}`) | resolved |
| ADV-2 (duplicate map keys; value-level roundtrip) | carried |
| ADV-3 (inert over-acceptance) | carried by design; TS02 rejects those values |
| ADV-4 (rustfmt command) | resolved; README records `--edition 2024` |
| ADV-5 (stale shared cargo target) | resolved as a documented procedure |
| ADV-6 (`prepare.py` keyword allowlist) | carried |
| ADV-7 (hardcoded paths) | carried |
| ADV-8 (provider root selection and supersession) | carried open |
| ADV-9 (report runtime integration) | reconfirmed verbatim |

## Advisories

1. **Unsupported keywords can narrow TS types.** The renderer ignores keywords it doesn't support instead of refusing them. For example, `{type:'array', prefixItems:[{type:'string'}], items:false}` renders `never[]`, which rejects valid `["x"]`. This doesn't occur in the current input or output, and TS02 refuses such schemas at admission. Before integration, share a keyword allowlist with `schema.ts` and `prepare.py`.
2. **The exactness audit misses numeric literal types.** `enum [{a:1}]` renders a JS-number literal type, and `prepare.py` only adds a `tsType` for top-level integer enum members. There are 0 such nodes in the projection and 0 numeric literal types in the output. Extend the audit.
3. **The integer collapse also widens const/enum integers.** 207 projection nodes become `ExactInteger`, including `schemaVersion` consts and edition enums. That is fine for inert carriers, but the Rust types no longer express those closed sets, so admission must govern them.
4. **Output written outside FRESH_OUTPUT.** `generate-ts-v2.cjs` rewrites `ts-exports.json` beside the script. The rewrites were identical on both fresh runs.
5. **Two TypeScript versions are in use:** 6.0.3 for the renderer and 7.0.2 for compiling. Both pass here; pin one.
6. **The witness checker writes into its origin directory** (`witness_common.OUT`). I ran it in a copy with that path redirected, and the results equal the frozen files.
7. **Positive evidence is bounded.**
   - Witness strings are minimal, one ref's only witness is `{}`, and 15 refs have exactly one witness.
   - For 263 refs, no single-point mutant was valid.
   - -2^63 was valid only at the targeted sites.
   - Rust checks compare values.

   Representability of every valid instance is not proved.

## Executed evidence (copy, isolated cargo targets)

- **Pins:** identical before and after for subject02 (63/63), runtime02, 44 external inputs and the witness origin files.
- **Code:** read the README and every changed or new source file.
- **`prepare.py` (unmodified):** all four outputs byte-identical.
- **Rust probes:**
  - metadata 12/12;
  - harvested 64,091 rows, 0 failures;
  - `integer_probe` passes;
  - `review_probe` output equals the frozen results;
  - witness `carrier_probe` 1343 rows, 0 failures;
  - both frozen differentials identical.
- **Regeneration:** two fresh runs match output-e and `drift-v2.json` on all 8 files.
- **TS compile:** provider, report and witness-check compile under tsc 7.0.2 and 6.0.3.
- **Witness checker (`check.py`, run in a copy):** 589/589 refs, 1343 cases, passed; its `result.json` and `manifest.json` equal the frozen files.
- **TS02 runtime on originals:** 1343/1343 witnesses and 1781/1781 mutants valid, with 0 disagreements against Python.
- **My own TS concrete assignments** (plain keys, `strict` + `exactOptionalPropertyTypes`): 3,434 statements with 0 errors on both compilers. Extended diagnostics confirm 48,257 types were checked.
- **Mutation corpus:** 1781 mutants that Python accepts under the original schemas, across 326 refs; Rust 1781/1781.
- **Targeted `ExactInteger` sites:** FindingParameters, Sarif and edition, including one TS type-rejection control.
- **TS AST audit:** 0 number, any, unknown, object, never, numeric-literal or empty types; the provider closure matches exactly.
- **Static Rust scan:** no floats, sets or empty enums; every struct has `deny_unknown_fields`.
- **Fail-closed controls:** the generator's empty-enum guard fires; the renderer refuses numeric enums, `number`, bare `const`, and unflattened or missing refs.

Scripts and logs are in `work/`.
