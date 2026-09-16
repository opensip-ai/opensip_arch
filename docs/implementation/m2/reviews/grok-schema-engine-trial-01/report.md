# Independent Grok advisory: M2 schema-engine trial 01

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement. Not fresh consumer B.
**Kind:** Advisory technical review. **NOT ACCEPT-DESIGN-UNIT.** Not runtime selection, not registered descriptor admission, not ReplayedRun authority.
**Work tree:** `/tmp/opensip-implementation/m2-grok-schema-engine-trial-review-01/review`. Frozen trial, live repos, and prior 01–03 pattern/engine history were not edited.
**Prior closed-pattern 03 / addenda:** archived; not reopened.

## Standing

Exploratory `no_std` + `alloc` exact-schema interpreter. `Program` borrows caller-supplied documents, preflights selected entry closures, and evaluates instances. It grants **no** registry authority. Resource meters are experimental, not M6 proof. `x-maxUtf8Bytes` is an ignored annotation at this generic shape boundary (ExactValidator does not implement it); the 21 control sites remain a later `control_protocol.rs` owner law.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 13290 | `b5dfe136de8e3fb3bb986252a7240f1fd65fbbad4b2c7b09db062e60f30475b6` |
| Archive | 2732135 | `01368a74cebf6f0fb47c0085bf2bf4b04c9b87d315e58af125d7b63b4e7e01d0` |
| `probe/src/schema.rs` | 20110 | `378b9b77c194bfc50d255c2948e94b7edb52d1a549bc3636ffd308c062d17d5c` |
| `probe/src/patterns.rs` | 8364 | `cf6438544160c78445db3a84135dd9a4f9a05d434bfd420e6996bd63df81467c` |
| `probe/src/table.rs` | 6047 | `216fa6b9e04106a14147948f9f0d0ce45b11a7d9e58a0c14722ff99cb73875c9` |
| Complete pattern census | 99068 | `9bbb8de3f2c99d6e7e2803a1e7f9de630e91b8b9780c8124bc1107a13a782e4f` |
| Identity source pins | 1025 | `dd06fbb65f7fe30159488488b8a5de5d2aea6414fa1ea96426860a91c64124b9` |
| Schema source pins | 6683 | `a19c4f9aee1c4b58f7ddfd1c2255d3c254f28e22985ee2689f3c2d05830cb14d` |
| `result.json` | 505 | `f109be3553ef34be6010925397766e3b55c5b09b4bb93806172049f102283c1c` |

Original `/tmp/opensip-implementation/m2-schema-engine-trial-01` matches the manifest **75/75**. Archive matches `archive-pin.json`. `cases.jsonl` / `initial.json` / `probe.stdout` verified in place, not duplicated.

Private `Cargo.toml` was rewritten to `review/copy/identity-source` (included pins). It was **not** pointed at live identity. Identity files match pins (Cargo.toml, canonical.rs, canonical_tests.rs, **descriptors.rs** 17536 / `868d7c37…97d3`, digests.rs, lib.rs 876 / `da6f4bdc…3eb7`). That is the frozen combined staged identity (ArrayOrder + LogicalPath present, parser still `no_std`). Lock: identity + `sha2-const-stable` only.

Forty included `selected-sources` match `schema-source-pins.json`. Census standing: pattern **values and** `patternProperties` keys; **69** strings including `^.+$`.

Tooling: Cargo/rustc 1.95.0 Homebrew; isolated CPython 3.14.6; jsonschema 4.25.1; canonical.py `d47f25db…b442`.

## What the program is (and is not)

`Program<'a>` holds `BTreeMap<&'a str, &'a V>` and a set of selected entry strings. Compile requires unique `$id` (no `#` in the id), `$schema` = Draft 2020-12, then preflights each entry’s `$ref` closure. Unknown keywords refuse (`Error::Schema`). Unselected pattern strings refuse (`Error::Pattern`). `%` / array-index pointers / `~2` refuse (`Error::Reference`). Duplicate `$id` refuses.

Evaluation is typed JSON (`JsonValue` has no float; `integer` is not `boolean`). `$ref` applies **and then siblings**. `prefixItems` then `items` for the tail (2020-12). `not` / `if` / `anyOf` propagate `Error::Limit` with `?` — cyclic `$ref` is Limit, never success. Boolean schemas are `true`/`false`. `x-maxUtf8Bytes` and the closed `x-opensip-*` annotation list are ignored at evaluate. `x-opensip-order` is semantic via `ArrayOrder::parse`/`verify`.

This is a **shape program**. A successful `Ok(true)` is not descriptor admission, not a digest, not a ReplayedRun.

## Archived claim vs independent work

Archived: 40 sources, 839 root+direct-`$defs` entries, 228 synthetic, 486986 cases, 0 mismatches vs `canonical.ExactValidator` / jsonschema 4.25.1; 5 focused tests; clippy/fmt/build. Initial preflight refused omitted `^.+$` (`first-failure.txt` preserved).

This review did **not** re-run 486986 cases. Private copy: `fmt --check`, `clippy -D warnings`, `test` (**5/5**), `build` — all exit 0 against reconstructed identity.

Bounded probes (20 instance rows + compile/cyclic/budget): const `1` admits `1` and refuses `true`/`false`; `type: integer` refuses `true`; `prefixItems` + `items` string tail and `items: false` extra match Draft 2020-12; `uniqueItems` treats `{a:1,b:2}` and `{b:2,a:1}` as duplicates; `^.+$` admits `a`, `a\n`, `\r` and refuses `\n`, `a\nb`; `x-maxUtf8Bytes:1` with `maxLength:1` still admits `😀`; patternProperties `^.+$` admits `"a\r"` and refuses empty key. Compile refuses unknown keyword, `type: number`, `.*`, empty `allOf`, unknown order, `#/0`, `#/%61`, `#/~2`. Unselected `urn:probe` vs `urn:probe#` is `UnselectedEntry`. Cyclic `not`/`anyOf`/`if` `$ref: "#"` are `Limit`. Budget 0 is `Limit` not false.

Those instance rows also match **direct** `ExactValidator` except as noted next.

## Findings (strategy, not frozen03 re-litigation)

**Bool/int.** No hidden JSON-schema-style bool-as-int leak in the Rust evaluator. Identity `Value::Bool` vs `Integer`, `kind()`, and `type(v) is int` in canonical.py agree. `-0` is `Error::Json` at parse (crate test).

**`x-opensip-order` through a `$ref` oracle.** Direct `ExactValidator(schema).validate([1, true])` with `numeric` **refuses**. Rust refuses. `ExactValidator({"$ref": "urn:probe#"}, registry=...)` **admitted** in this environment — custom `x-opensip-order` did not apply on the retrieved resource, while `type`/`const` still did. The trial’s 486986 comparison used that `$ref` wrapper. Treat the zero-mismatch corpus as **not** a proof that order-on-bool was cross-checked. Next registry tests must oracle **direct** `ExactValidator` on the resolved node, including `[1, true]` against `numeric`.

**Prefix/items.** 2020-12 tail `items` after `prefixItems`; extra elements with `items: false` fail; missing `items` leaves extras unconstrained. Selected 40 sources have 9 `prefixItems`, 0 `unevaluated*`, 0 `exclusiveMinimum`, 0 `minContains`. Empty `allOf`/`prefixItems` compile as `Schema` (stricter than vacuous JSON Schema); unused in the 40.

**Unknown keyword / ref preflight.** Closed keyword + annotation allowlists. Unreferenced nested `$defs` are not walked except as selected entries (839 = each document + its direct `$defs`). Nested unused `$defs` with unknown keywords would not fail compile until referenced. Low for these 40; the owning registry should still preflight the full selected AST.

**Cyclic Limit.** `not` / `if` / `anyOf` cannot invert Limit into success. Depth 128. Fail-closed. `anyOf`/`oneOf`/`contains` stop on Limit without trying remaining branches — acceptable for Limit≠false; resource-order dependent.

**Resource meter.** Experimental: `spend(1)` per node, string bytes, canonical bytes for `uniqueItems`, compile vs eval budgets separate. Integers/bools cheap. Pattern CPU not separately metered. Parsing still identity 4 MiB / depth 32; eval depth 128. `Error::Limit` is not `Ok(false)`. Not M6.

**Ownership.** Borrowed `&V` documents are immutable for the `Program` lifetime in safe Rust, but **the caller chooses the bytes and `$id`s**. A caller can present a document whose `$id` impersonates a selected schema. That is the trial’s explicit non-authority. Schema AST is the parsed identity `Value`, not a compiled opcode image.

**Annotation vs semantic law.** `x-maxUtf8Bytes` ignored (emoji admitted). `x-opensip-order` enforced. Other `x-opensip-*` on the allowlist ignored. Digest/path/ownership annotations are **not** executed here — correctly, because this is shape, not join/replay.

## Next step: owning pin table, not caller schema as authority

Root’s next replacement — **owning immutable registry + compiled exact 40-source pin table** — is the right direction. Do not select this borrowed `Program` as a product runtime that accepts arbitrary caller schemas.

Required for that unit:

1. Store the 40 source bytes (or their exact SHA-256 pins from `schema-source-pins.json`) as the only compilable documents. Reject any other `$id`.
2. Own the parsed AST (`Box`/`Arc`, not a caller borrow of untrusted `V`).
3. Entries = the registered 839 (plus only test-only synthetics). `UnselectedEntry` for anything else.
4. Keep Limit ≠ false ≠ Json ≠ Schema ≠ Pattern ≠ Reference ≠ UnselectedEntry.
5. Oracle against **direct** ExactValidator on the resolved node, including order and bool/int.
6. Still ignore `x-maxUtf8Bytes` at this layer; do not port TS trial shape.
7. Still do not mint descriptors or ReplayedRun from `Ok(true)`.
8. Resource policy remains a later M6 unit; do not freeze these meter constants as product law.

A shape program that only compiles pinned selected sources is still **not** complete M2-A03 descriptor admission. Combinators here check JSON shape. Registered descriptor admission additionally binds document hash + selector + identity joins. Replay remains a later owner.

## Limits

- Advisory only. Not ACCEPT-DESIGN-UNIT, not runtime selection, not M2 complete.
- Did not re-run 486986 cases; did not execute original `run-trial.py` against original tmp.
- Did not reopen pattern-trial 03 opinions except to confirm census69 / `^.+$` is now in the table.
- Did not implement or require `control_protocol.rs`.
- Private `Cargo.toml` path rewrite is review-only.

## Evidence

- `review/results/probes.json` — SHA `870ebbed052bc19d4db368d5ae5f569e5cb02ab4e75da5de3382a7c79a025aa8`
- `review/copy/identity-source/` — reconstructed combined identity
- `review/copy/probe/` — engine + rewritten path dep
- `review/probes/run_probes.py`
