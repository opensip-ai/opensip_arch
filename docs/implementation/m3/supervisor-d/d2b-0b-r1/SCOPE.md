# D2b-0b r1: the successor schemas' generation (D2b plan r3 amendment A1, LD-D2B0-A)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1.**

**Authority.** D2b-0b is the sub-unit that D2b plan r3 amendment A1 (`supervisor-d/d2b/PLAN-r3-A1.md`) creates. A1 was accepted with D2b-0 r2 (`codex-d2b-0-r2`, `amendmentLDD2B0A` ACCEPT). It owes:
- the generator's pattern-profile extension (`SubjectIdV1`'s pattern, with `pattern-profile.json`, as a reviewed generator-input change);
- the source-map, generation-registry and options rows, re-making D2b-0's deferred LD-D2B0-1 to 4, including the Root and root-law-annotation question;
- the regenerated carriers;
- the reviewed blind refresh.

**What it serves.** M3-D item 10 (`PROPOSAL-r5.md`:381) and both accepted materialization maps (FA-2's and RUST3-LIM's `materialization-map.json`) stand unamended. This unit does their generation part: the two schemas' source-map rows, the registry re-pin, and the regenerated carriers.

**What it does not include.** The reviewed blind refresh is **not** in this package. It follows as a separate unit (a pre-run Codex review of the blind mode, the lead's mechanical blind run, a post-run review). The lead plans one refresh covering C1a4 and D2b-0b together, if timing allows. D2b-0b must be integrated before D2b-3 or D2b-4 consumes either successor payload (A1).

It is a contract successor: the generator closure, options, source map and runtime pattern files change, and `tools/generate_contracts.py` requires the closure's bytes to be an accepted design input.

**Base:** product main as the subject manifest names: `3d1d771`, the v221 lock on C1a4's `57e5c48`, with D2b-0 bound as contract successor 174.

## What it changes

| File | Change |
| --- | --- |
| `tools/contracts/runtime/pattern-profile.json` | **The pattern profile extended by its own method** (LD-D2B0b-5). Two sources are added: FA-2's `symbol-census-v1` and RUST3-LIM's `rust-subject-scope-v1`, at their accepted architecture paths, in path order (28 to 30). The patterns are re-collected over all the sources and translated by the M1 method, giving 67 rows from 66. The only new row is `SubjectIdV1`'s `^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])`. Its translation is the identity, because it has no unescaped `.` or `$` outside a class. Every existing row is unchanged. |
| `tools/contracts/runtime/patterns.ts` | The table, rendered by the method's own template: 70 entries from 69. The new entry is added in sorted position, and every existing entry is unchanged. |
| `schemas/source-map.json` | Two rows: `opensip.product.rust-subject-scope.1` and `opensip.product.symbol-census.1` (LD-D2B0b-1, 2), pinned to the accepted FA-2 and RUST3-LIM candidates (41 to 43). |
| `schemas/registry.json` | Two source rows; the recipe's `sourceSha256s`, `generatorClosureSha256` and `optionsSha256` re-pinned. |
| `tools/contracts/options.json` | Two `owners` rows (LD-D2B0b-1), two `sourceMappings` rows (LD-D2B0b-2), and 25 `entryPoints`: every `$def` of each schema, with no Root (LD-D2B0b-3). `providerEntryPoints` and `deniedRefs` are unchanged (LD-D2B0b-4). |
| `tools/contracts/generator-closure.json` | The two schema sources added (in path order), and four inputs re-pinned: the source map, the options and the two runtime pattern files. |
| `crates/contracts/src/generated/protocol.rs` | Regenerated: 919 lines added, none removed. The new `SymbolCensus1*` and `RustSubjectScope1*` carriers. |
| `tools/operability/exceptions.json` | The mint-audit census row for the regenerated `crates/contracts/src/generated/protocol.rs`, `into` calls, from 99 to 110 (LD-D2B0b-8). |
| `apps/report/src/generated/report.ts` | Regenerated: 110 lines added, 4 replaced. The new types are additive. **The expected generated-output movement** is the four replaced lines: the two header digests (registry and closure), and the embedded `selectedSchemaBytes` and `selectedSchemaEntryPoints` arrays, which now include the two schemas. The embedded runtime pattern table gains the one entry. No existing type definition changes. |

**Unchanged:**
- the other six generated outputs, including `providers/typescript/src/generated/protocol.ts`, because no provider entry point is added;
- `schemas/wire/native-carriers-v1.json`;
- the admission registry and its source map, the identity pins and the embeddings (D2b-0's);
- every census-closure file, the census tools and their records;
- the blind receipt;
- the Cargo manifests and lock.

## Lead decisions

These are D2b-0's deferred LD-D2B0-1 to 4, made again here, as A1 requires.

- **LD-D2B0b-1. The namespaces (a lead naming decision).** `SymbolCensus1` and `RustSubjectScope1`, module `protocol`.
  - **Basis:** the existing namespaces are the PascalCase schema stem plus the major (`Handshake1` from `provider-handshake.1`, `Startup1`, `FactBatch3`), though not mechanically (`Dispatch1`, `RecognitionPlan1`, `Inventory6`).
  - Both pass the adapter's name rule and its no-prefix-overlap rule.
- **LD-D2B0b-2. The source mappings (a lead placement decision).**
  - `declaredMajor` 1, from each `$id`;
  - profile `opensip-exact-schema-reference-1`;
  - semantic owner `crates/components/src/provider_protocol.rs`, the handshake's and startup's owner, and the codec D2b-3 and D2b-4 complete;
  - the source-map standing text that the existing generator rows share, verbatim.
- **LD-D2B0b-3. The entry points: every `$def`, with no Root (a lead decision by precedent).** `typeName` is the namespace plus the definition name. Every existing owner follows this rule, with three exceptions, and they settle the Root question:
  - **common-v4 and graph-query-v4** have no Root entry point: their roots are `$defs`-only containers;
  - **native-v2** omits exactly its three denied definitions.

  Each new schema's root is a `$defs`-only container whose one root keyword is a law annotation (`x-opensip-symbol-census-law`, `x-opensip-subject-scope-law`). That keyword is outside the generator runtime's closed annotation set (`runtime/schema.ts`:17). Following common-v4 and graph-query-v4, neither root is an entry point. So `prepare.py` never converts either root, and the annotation question needs no generator change: `runtime/schema.ts` is unchanged. Every other keyword in either schema is in the selected set (D2b-0's walk, which Codex confirmed in `codex-d2b-0-r1`).
- **LD-D2B0b-4. No `providerEntryPoints`.** No TypeScript provider consumes either payload yet. The TypeScript codec unit adds them when it needs them, under its own review. So the TypeScript provider's generated output is unchanged.
- **LD-D2B0b-5. The pattern profile is extended by the M1 method, not by hand.**
  - **The method** is `trials/ts-runtime-02/subject/pattern-profile.py`: its `visit()` collects every `pattern` and `patternProperties` key, its `translate()` rewrites only an unescaped `.` (to `[^\n]`) and `$` (to `(?=\n?(?![\s\S]))`) outside a class, and it renders the table by its template. `grok-schema-pattern-trials-01` reviewed exactly this adaptation: 68 patterns, 74,528 cases, no mismatches.
  - **The prepare** (`evidence/prepare_d2b0b.py`) carries those three functions verbatim. It asserts that:
    - the existing profile reproduces from its own 28 sources;
    - the existing `patterns.ts` is the template's rendering of its table;
    - adding the two accepted successor documents as sources adds exactly one pattern;
    - no existing row or entry changes.
  - **The differential** (`evidence/check_d2b0b_patterns.py`, `pattern_differential.mjs`) records the Python `re.search` reference result for every profile row over a value set. The set is the M1 method's own values (prefixes, the six line terminators, path segments and identity endings), plus `SubjectIdV1`'s targeted values: C0, DEL and C1 controls, NBSP, an emoji, an uppercase or digit prefix, an underscore, an empty side and `::`. Node's `u`-flag `RegExp` over the translations must agree on every comparison.
  - **A pre-existing inconsistency, recorded as is.** `patterns.ts` holds three entries that `pattern-profile.json` does not list: `^RP-DO-[0-9]{2}(?![\s\S])`, `^owner1:[0-9a-f]{64}(?![\s\S])`, and one control-and-bidi-excluding class. They have been there since `generator-selection-v1`; the profile and table were selected together, with that difference. This unit changes neither: the three entries stay in the table, and the profile stays the reproducible record of its own sources.
- **LD-D2B0b-8. The mint-audit census follows the regenerated carriers (a lead placement decision by precedent).** The new carriers add 11 generated `into(..)` calls to `protocol.rs`. The operability source census then differs from its audited exceptions; lane attempt 2 failed there. The count is re-pinned as B-S10 re-pinned its regenerated `invocation.rs` (`c019e9e`: `into` 135 to 150).
  - **How:** `evidence/repin_d2b0b_mint_audit.py` measures the count with `check_operability.py`'s own `mint_inventory()`, never by hand. It asserts that the census rows are otherwise identical, and that this one count is the only difference.
  - **What it is:** generated code's conversions, not a hand-written mint authority.
- **LD-D2B0b-6. The successor record.**
  - **Parents:** the five accepted generator inputs it re-pins (the closure, `s10-tsc`'s copy; the options, `b-s10`'s; the source map, `s10-tsc`'s; the pattern profile and table, `generator-selection-v2`'s), and FA-2's and RUST3-LIM's successor records.
  - **Candidates:** this package. Its `product/tools/contracts/generator-closure.json` is the accepted input `generate_contracts.py` requires after binding.
  - The binding adds the next contract successor. The inventory is unchanged: no new product path.
- **LD-D2B0b-7. The census and the stale receipt (the C1a4 rule).**
  - **The rule:** no census output embeds the generator-closure digest. `discovery_census.py` binds it only into the blind receipt's `reference` bindings (`receipt_bindings`), and renders a receipt bound to other inputs as stale rows. So the discovery census, workspace ledger and snapshot census `--check`s **pass** with no regeneration, and their records are byte-equal to the base's.
  - **The stale receipt is recorded separately, from public fields only** (`check_d2b0b_census_stale.py`):
    - **the binding change:** recomputed by the tool's own `receipt_bindings()`, the candidate's bindings differ from the base's in exactly one row, the generator closure's reference pin (the base's, then the candidate's);
    - **already stale on the base:** the receipt was already stale on the base, in its `closure` and `tool` bindings (C1a4);
    - **the receipt:** byte-equal to the base's;
    - **the census record's rendered held-out rows:** all 10 are `outstanding: held-out (blind receipt stale)`, and `heldOutMargin` is `outstanding`.
  - No held-out store or content is read. The refresh is the separate unit.

## Checks

Lane r1, attempt 3, `evidence/d2b0b-checks-r1/` (the lane of record), on product `3d1d771`. allPassed.

**Order of preparation** (all scripted, in `evidence/`): `prepare_d2b0b.py`, then `run_d2b0b_generation.py` (write), then `repin_d2b0b_mint_audit.py`.

**Void history** (kept, not acceptance evidence):
- **Attempt 1** was stopped after three suites, when the census rule was corrected to the C1a4 rule.
- **Attempt 2** failed in three places:
  - the operability mint audit, the regenerated `protocol.rs`'s `into` count, now LD-D2B0b-8;
  - a mutation's expected reason (the namespace change is refused first by `validate_options`, "entrypoint ownership or unique name mismatch");
  - the generator TypeScript lane, which refuses identically on the base.

The checks:
- **The suites,** at base and candidate, with equal failure sets and no new or differing test:

  | Suite | Failed | Passed |
  | --- | --- | --- |
  | contracts | 0 | 0 (it compiles the regenerated `protocol.rs`) |
  | components | 0 | 43 |
  | identity | 0 | 72 |
  | host | 8 | 409 |
  | storage | 33 | 137 |
  | evaluator | 0 | 47 |

  The failure counts are the same on both sides, and every failure is pre-existing on the base.
- **Lints:** warning-denied all-targets Clippy on contracts and components. No hand-edited Rust file.
- **Generation determinism:** the selected pipeline re-run over the pinned closure (43 sources, 883 entry points) reproduces all eight outputs byte for byte.
- **The pattern-profile check:**
  - the table is the profile's rendering plus the three pre-existing entries, with one entry added: 70 entries, 67 profile rows;
  - the differential: 89,512 comparisons of Python `re` against Node's `u` flag, **no mismatch**.
- **The design preflight:**
  - verify_design passes on the candidate, with 43 generation sources and 52 admission sources;
  - the public `generate_contracts.py` refuses for exactly one reason, "generator closure is not selected by an accepted design unit", until the binding.
- **The TypeScript lanes:**
  - the report lane passes;
  - the generator lane refuses on the base and the candidate alike ("tool policy input pinned bytes differ: tools/contracts/package.json"). This is a pre-existing refusal, recorded, not a D2b-0b change.
- **The census (LD-D2B0b-7):**
  - the discovery census, workspace ledger and snapshot census `--check`s pass;
  - the stale receipt is recorded separately: the candidate's only binding change is the closure's reference pin; the receipt was already stale on the base (`closure`, `tool`); the receipt and the census record are byte-equal to the base's; and all 10 held-out rows render stale, with `heldOutMargin` outstanding.
- **Repository checks:** FW-01, the environment exceptions, the operability source census (114 rows, no findings) and the census-closure check (no closure file changed).
- **Four mutations,** each caught by its named detector with its expected reason:
  - the new pattern entry removed (generation: `validate` refuses);
  - a non-M1 translation dropping the C1 controls (the pattern differential mismatches);
  - a namespace differing from its owner's (generation: "entrypoint ownership or unique name mismatch");
  - an entry point omitted (generation: `prepare` refuses the unowned reference).

## Not delivered

- **The reviewed blind refresh:** the separate unit, possibly together with C1a4's.
- **The codecs** and any consumer of the new carriers: D2b-3 and D2b-4.
- **Provider entry points:** the TypeScript codec unit (LD-D2B0b-4).

## Not claimed

- No codec, no semantic admission, no caller.
- No qualification; D2b's completion is not claimed.
