# Review: OpenSIP TS runtime trial, successor (m1-ts-runtime-subject-02)

- **Verdict:** ACCEPT-TRIAL-UNIT
- **subjectManifestSha256:** `f4cb31f4d7144f6c00e47c712da1ba5772aede4404d6f3365da02a1903a79ab9` (37 files)
- **Scope:** the trial algorithms only (`exact-json.ts`, `schema.ts`, `patterns.ts`). This review does not accept product integration, a public API, a production Rust dependency, tool selection or M1 qualification. I did not infer approval from the author's test counts; each conclusion below comes from my own reruns and probes.

Machine-readable form: `review.json`. Work is in `work/subject` (copy), `work/regen` (table regeneration) and `work/probes`.

## Prior findings

### R1: resolved
The runtime looks up each pattern in an exact 66-entry table (`patterns.ts`) and refuses unknown patterns. Six entries are rewritten:
- An unescaped dot outside a class becomes `[^\n]`.
- A bare `$` becomes `(?=\n?(?![\s\S]))`.

These are exactly Python `re` semantics without DOTALL or MULTILINE, and jsonschema 4.25.1 validates `pattern` with `re.search`. All other constructs in the 66 patterns have the same language in ECMA Unicode mode: ASCII classes, `\uXXXX`, `[\s\S]` only as a pair, lookaheads, bounded quantifiers, and `^` without `m`.

Independent evidence:
- **Regeneration:** regenerating from `pattern-profile.py` is byte-identical. The pattern set equals my review-01 extraction, and the sources equal metadata-v2.
- **Exhaustive differential:** 26,790,060 comparisons (405,910 strings: every string up to length 5 over a 13-symbol alphabet that includes LF, CR, U+2028, U+0085, NUL, `\`, `.` and `/`, plus terminator insertion at every position of identity/semver/path seeds). 0 mismatches.
- **Mutation control:** running the unmapped source patterns on the same harness gives 185,478 mismatches, so the harness is sensitive.
- **Review-01 corpus:** 68,640 rows now give 0 mismatches, and the end-to-end path booleans agree.
- **Rust probe:** the regress probe on my copy gives 39,336 comparisons with 0 mismatches.

### R2: resolved
`matches()` evaluates `parseExact(canonical(value))`, and `canonical()` requires `Array.prototype`. My review-01 bypasses now fail:
- A custom array prototype or an Array subclass throws `PLAIN_ARRAY_REQUIRED`.
- The Proxy `get` trap and the Proxy with a fake `every()` both return `false`.
- Cross-realm arrays and objects are refused, and local and growable SAB views are refused.

Proxies are explicitly outside the contract, and even a descriptor-lying Proxy produces a snapshot that is consistent with itself.

### Other prior advisories
- **A1:** resolved. 36,000 random evaluations across 12 annotations, bare and under `not`, against `canonical.py` gave 0 mismatches. The 2680 real-node cases also give 0.
- **A2:** resolved for the selected vocabulary; 12 extra malformations refuse with `SchemaError`.
- **A4:** resolved; 43/43 executable comparison.
- **A3 and A5:** carried limitations, confirmed.

## Finite pattern profile assessment
**Acceptable** as a scoped compatibility mapping for exactly these 66 source patterns in the 28 pinned documents. Root assent is still required before product integration.

Grounds:
- `identity-and-evidence.md` §2 (lines 64–76) explicitly reads a bare `$` as admitting a final LF, and `(?![\s\S])` as the exact end. Preserving that reading is consistent with the product contract.
- Raw schema bytes and historical evidence are unchanged.
- The mapping refuses unknown patterns rather than porting Python `re`.

Conditions:
- Any new or changed pattern, or any new engine, needs a regenerated table, an independent differential and review.
- The generator is a character scanner, not a regex parser. It is acceptable only as a frozen, reviewed output for these inputs.

## Required findings
None.

## Advisories
- **ADV-1: LF-separated traversal is still admitted by CanonicalPath.** Both engines accept `evidence-schemas:v2#/$defs/CanonicalPath` for `"a\n/../../etc/passwd"`, `"a\n/.."` and `"a\r\n/../x"`. The runtime is faithful to the reference and PROFILE.md discloses this. `native-evidence.md:644` does not claim CanonicalPath is canonical or traversal-free. Host component and custody admission must check paths independently, and a successor schema should use `[\s\S]` or `(?![\s\S])`. The LogicalPath variants refuse these inputs.
- **ADV-2: unescaped dots in the `security.repo-execution-grant(s).v2` identity patterns.** Both engines accept `securityXrepo-execution-grantXv2:<hex>`, and the grants variant accepts U+2028 and `/` as separators. These patterns are used in 3 pinned documents. Semantic owners must compare exact digest domain prefixes, and the dots should be escaped in a successor schema.
- **ADV-3: the SAB refusal is realm-local.** A SharedArrayBuffer from another vm realm wrapped in a local `Uint8Array` is accepted. This is low risk and inside the trusted-builtins scope; a `toString` brand check would close it.
- **ADV-4: Rust probe log provenance.** The frozen `rust-pattern-check.log` was produced from `m1-ts-runtime-trial-02`, not the frozen path. My rerun on the copy reproduces its result. Cargo put `target/` under `m1-ts-runtime-review-02/`.
- **ADV-5: carried limits.** Non-productive `$ref` cycles report `ShapeLimit`, and canonical, snapshot and regex work is unmetered (a 4 MiB object takes 523 ms). Integration must set work limits and host timeouts.

## Executed checks
1. Subject pins (manifest plus 37 files) before and after the review.
2. Full reads of the changed sources, the profile, the regressions, the harness notes and the Rust probe, plus the cited contract passages.
3. tsc clean on the copy.
4. All frozen scripts: boundaries 34, regressions 38, pattern differential 39,336/0, schema-probe 43/0, shape 11,191/0, corpus 14,000 (4,490/9,510), canonical differential 0, reviewer regex 68,640/0, Rust 39,336/0.
5. Table regeneration: byte-identical.
6. Exhaustive pattern differential with mutation control.
7. R2/A2 adversarial probes.
8. A1 randomized ordering differential.
9. Reruns of the review-01 order cases (2,680) and harvested rows (1,472,500; 64,091 valid; 0 mismatches).
10. LF-gap and identity-dot probes.

## Limitations
- The reference is a comparator chosen by the root. I accept the profile as faithful, not as the ideal grammar.
- The exhaustive alphabet and length are bounded; wider equivalence rests on construct analysis.
- regress was checked for conformance only.
- No fuzzing, no backtracking or wall-clock analysis, and no non-Node runtimes.
- Only 110 of 589 refs have valid harvested witnesses.
- Proxy, concurrent-mutation and untrusted-builtin inputs are out of contract.
