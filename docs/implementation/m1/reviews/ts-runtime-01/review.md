# Review: OpenSIP TS runtime trial (m1-ts-runtime-subject-01)

- **Verdict:** CHANGES-REQUIRED
- **subjectManifestSha256:** `48089c1e4daa161dd5a18deebcd396514901a290d4ac0ac80a89fd2cbacf8ba3`
- **Scope:** the trial exact-JSON codec and shape interpreter only. This review does not qualify a generator, public API, Rust carriers, build/tool selection or M1/release.

Machine-readable form: `review.json`. Probes and outputs: `work/probes/`. The copied and compiled subject is in `work/subject/`.

## Summary

The lexical/canonical codec holds up well. All frozen checks reproduce, 25 extra adversarial lexical probes refuse correctly, and I found no canonical-encoding defects. The interpreter agrees with the Python metadata-v2 adapter on:
- the 11191 retained generic cases;
- my own reproduction of the 43 metadata cases;
- 2680 targeted ordering cases;
- 1,472,500 harvested real-value rows (64,091 valid).

Two defects block acceptance. Both sit in areas the corpus structurally cannot reach.

## Required findings

### R1: The regex dialect is unpinned, and TS is more permissive on pinned path patterns
`schema.ts:35` compiles every pattern as a JS `u` RegExp. In JS, `.` excludes `\r`, U+2028 and U+2029, and `$` matches only at the end. In the Python reference, `.` excludes only `\n`, and `$` also matches before a final `\n`.

Across the 66 pinned patterns with line-terminator edge strings, 428 of 68,640 rows differ, spread over 4 patterns. On the real registry, TS returns **true** and Python returns **false** for:

| Schema | Input |
|---|---|
| `evidence-schemas:v2#/$defs/CanonicalPath` | `"a\r/../../etc/passwd"`, `"a /../../x"`, `"..\n"`, `"a/..\n"` |
| `workflows:common#/$defs/LogicalPath`, `identity:v3#/$defs/LogicalPath` | `"..\n"`, `"a/..\n"` |

The CanonicalPath lookahead pattern appears at 34 pinned locations. `^.+$` (sarif `messageStrings`) accounts for 362 of the mismatching rows.

**Required:**
- Pin one normative dialect and record who owns that decision.
- Make TS, the Python reference and Rust agree, either by rewriting patterns to be terminator-explicit or by translating in the runtime.
- Retain a line-terminator edge corpus over every pinned pattern.

### R2: The inert-data check is not bound to the evaluated value
`matches()` calls `canonical(value)` (`schema.ts:91`), throws the result away, and then evaluates the live caller object. `canonical()` does not check array prototypes (`exact-json.ts:115`) and cannot observe Proxies. Demonstrated:
- An array with a custom prototype whose `every()` returns true: `[1n,2n]` matches `items:{type:string}` → **true**.
- An `Array` subclass behaves the same way.
- A Proxy over `{a:5n}` with a `get` trap returning `"x"` matches `{a:string}` → **true**.
- Proxy `ownKeys` traps run 3× inside `canonical()`, so the no-effects claim does not hold for Proxies.

**Required:**
- Evaluate an owned snapshot (`parseExact(canonical(value))`), as the registry constructor already does, or accept only bytes.
- Require `Array.prototype` for arrays.
- Reject Proxies where the host allows it, or scope the claim explicitly.
- Add regression tests.

## Advisories
- **A1:** `ordered()` throws `SchemaError` for instance-dependent faults such as wrong item types or missing `by` keys, where the reference returns invalid. Inside `not`/`anyOf`/`if` this aborts evaluation. It also accepts integers under `utf8`/field orders and strings under `numeric`/`candidateOrdinal`. This is not reachable on current pins (0/2680 mismatches over all 134 non-sequence nodes), because same-node `items` runs first. `allOf` runs before `items`, though, so a different schema layout would expose it.
- **A2:** `checkEntryPoints` does not type keyword values. A non-array `enum`/`required` fails open, a bigint `pattern` or string `minimum` gets coerced, a non-string `$ref` throws `TypeError`, and `type:"number"` never matches. The pins are clean on all of these (static scan).
- **A3:** Non-productive `$ref` cycles surface as `ShapeLimit` rather than a static `SchemaError`. Pinned recursion (Predicate) consumes instance depth, and deep valid-structure probes did not hit a limit.
- **A4:** `schema-probe.mjs` uses metadata-v1 and compares nothing, and no frozen script produces `schema-differential-02.json`. My independent reproduction matches, but the producing script should be frozen.
- **A5:** The default work limit (1e6) raises `ShapeLimit` on a parsable ~2M-element array. canonical, regex and enum equality are unmetered but size-bounded. 4 MiB parse/canonical timings are ≤0.71 s.
- **A6:** Uint8Arrays backed by SharedArrayBuffer are accepted, and cross-realm Uint8Arrays are refused. Document the accepted input class.

## Confirmed without findings
- Integer bounds -2^63..2^64-1 hold as bigint, and overlong digits are refused before BigInt allocation.
- `-0`, floats and exponents are refused. So are BOM, duplicate decoded keys, lone and reversed surrogate escapes, and UTF-8-encoded surrogates.
- Byte limits (4 MiB) and the 32-container depth limit work in both the parser and canonical.
- Canonical output is compact and UTF-8-key-sorted (supplementary characters after U+FFFF), preserves arrays, and round-trips `__proto__`/`constructor` keys.
- Accessors, holes, hidden or symbol properties, boxed primitives, Numbers and cycles are refused.
- The registry snapshots documents, refs resolve only to exact registered IDs (URN and non-URN), and JSON Pointer unescaping order is correct.
- `if/then/else`, `not`, `oneOf` counting, `contains`, `propertyNames` and `uniqueItems` (canonical-based) are correct.
- Unsupported keywords refuse. The pins have no nested `$id`, and no relative, percent-encoded or array-index refs.

## Executed checks
1. Verified the manifest and all 12 file hashes before and after the review.
2. Compiled a copy with tsc 7.0.2 on Node 24.16.0: clean.
3. Frozen scripts: boundaries 34 passed; corpus 14000 (4490/9510); shape differential 11191 with 0 mismatches.
4. Reproduced the 43 metadata cases on my own (0 mismatches; the v1 adapter differs on 2).
5. Static scan of the 28 pins and ref graph over the 589 entrypoints.
6. Lexical, ownership, keyword and cycle probes (`own.mjs`, `toctou.mjs`).
7. Ordering differential (`order-*.{py,mjs,json}`).
8. Regex differential and end-to-end path probes (`regex-*`).
9. Harvested differential: 2500 real values × 589 refs, 0 mismatches (`harvest*.{py,mjs}`, `harvest-diff.json`).
10. Deep Predicate recursion probes (`deep.mjs`) and 4 MiB performance / work-limit timing (`perf.mjs`).

## Limitations
- The Python adapter is a comparator, not an authority, and R1 partly hinges on which dialect is normative.
- Rust was not executed, and Rust regex behaviour on line terminators was not measured.
- Only 110 of 589 refs have any valid-case differential witness.
- No coverage-guided lexer fuzzing. No evaluation of Proxy detection options or non-Node runtimes. No regex backtracking analysis.
- The 589-entrypoint selection was taken as given.
