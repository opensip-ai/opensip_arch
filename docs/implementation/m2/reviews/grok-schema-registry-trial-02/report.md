# Independent Grok advisory: M2 schema-engine trial 02 (owning exact-source registry)

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement. Not the separate normative-oracle session.
**Kind:** Advisory technical review. **NOT ACCEPT-DESIGN-UNIT.** Not runtime selection, not descriptor/digest/domain/replay authority, not full M2.
**Work tree:** `/tmp/opensip-implementation/m2-grok-schema-registry-trial-review-02/review`. Frozen 01/02, live repos, and prior review reports were not edited.
**Engine 01 review:** archived; this unit is the owning-registry follow-on, not a re-litigation of the interpreter kernel.

## Standing

`RegisteredSchemas` is an opaque wrapper whose only constructor takes the exact 40 complete raw documents in `source_requirements()` order. Length then SHA-256 then `$id` then owned `Program` preflight. `schema(id, selector)` yields `SchemaHandle` (full-document SHA + exact selector). `admit_json` consumes the handle and returns read-only `ShapeValue` on complete shape success. Generic `Program` remains publicly constructible for trial oracles and **cannot** mint registry/handle/shape wrappers (private fields; external E0451). Production export should narrow. Resource caps remain exploratory. `x-maxUtf8Bytes` stays a later control-owner law.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 17473 | `ae181b48d00a4ba6b822c23b13bfc748e1bba1653817f5d3448262d6c43f63f2` |
| Archive | 472480 | `761fd031f5db84d51b40cab0581464ff92e4018584ac667cadc92a2cb22b9e22` |
| `probe/src/registry.rs` | 5436 | `edd7d6f6e14c1e21b32f057e5064ff2f43f2aa46e8be6ac9b59a5f3e854bb623` |
| `probe/src/registry_pins.rs` | 10633 | `a165471a266aa6ba0586e301ea2ca9533569287f19a3a033cceb4a6c929ebfef` |
| `check-profile-oracle.py` | 5035 | `9e8330774fc0050f7ccc955e84aa25ce325c9f109e6ff9bd5a979f7a5c98a5d5` |
| `probe/tests/registry.rs` | 3675 | `2afa0eafda3d2727aa57e4464aa6783c062bfd945313c7c4956669eba06bd4d7` |
| Identity source pins | 1025 | `dd06fbb65f7fe30159488488b8a5de5d2aea6414fa1ea96426860a91c64124b9` |
| Schema source pins | 6683 | `a19c4f9aee1c4b58f7ddfd1c2255d3c254f28e22985ee2689f3c2d05830cb14d` |
| Registry pins JSON | 9259 | `0ecfc8ec588eb89fd06995e48c159aff61c15ddf11a8be84bd896022d7fc226c` |
| Pattern census | 99068 | `9bbb8de3f2c99d6e7e2803a1e7f9de630e91b8b9780c8124bc1107a13a782e4f` |

Schema source pins match engine 01. Previous-trial.json pins frozen 01 subject `b5dfe136…75b6` / archive `01368a74…01d0` — unchanged.

Original `/tmp/opensip-implementation/m2-schema-engine-trial-02` **101/101**. Private copy rewrote **both** `probe/Cargo.toml` and `consumer-probe/Cargo.toml` to included identity + private probe. Not live. Identity six files match pins (includes descriptors.rs). `registered-cases.jsonl` and `owning-probe.stdout` verified in place.

## API and ownership

`Program` now **owns** `BTreeMap<String, JsonValue>`. `compile(Vec<Value>, entries, budget)` copies documents in. `RegisteredSchemas { program }` is private. `from_sources(&[&[u8]])`:

1. `sources.len() == SOURCE_PINS.len()` else `SourceSet`
2. Positional zip: `len != pin.bytes` or `raw_sha256 != pin.sha256` → `SourceBytes` (length **before** hash)
3. Parse; root `$id` must equal `pin.id`
4. Entries = `{id}#` plus each direct `$defs` key with `~` / `/` JSON-pointer escape
5. `Program::compile` preflight of that closure (budget 200 000 000, exploratory)

Caller buffers can be zeroed and dropped; the owned AST remains. No filesystem/network/resolver in the library. Fixture binaries take an **explicit** source-root argument. `document_sha256()` on a handle is the **pin-table** digest of the whole raw document, not a subschema hash.

`schema(id, selector)`: unknown id → `SourceSet`; selector must be the exact stored pointer (`""` for root, `"/$defs/HostRelease"` for a def). `"#/$defs/HostRelease"` and missing defs → `UnselectedEntry`. No version fallback. 839 = 40 roots + direct `$defs` only.

`admit_json(self, raw, budget)` consumes the handle: `Ok(value)` → `ShapeValue`; `Ok(None)` → `Mismatch`; parse/limit/schema/ref faults stay `AdmissionError::Schema(Error::…)`. Limit is not mismatch. `into_value()` drops the shape account by design.

`ShapeValue` / `SchemaHandle` / `RegisteredSchemas` have no `Default`/`Deserialize`/public fields. Extracting `JsonValue` is inert.

This is **not** descriptor admission, digest domain, custody, or ReplayedRun.

## Independent reproduction

Private copy, reconstructed identity:

| Check | Result |
| --- | --- |
| `cargo fmt --check` | exit 0 |
| `clippy --all-targets -D warnings` | exit 0 |
| `cargo test --locked --offline` | **8/8** (5 kernel + 3 registry) |
| `cargo build --bins` | exit 0 |
| External `public-reader` (`source_requirements().len()`) | exit 0 |
| External `private-authority-forgery` (struct-literal `ShapeValue` / `RegisteredSchemas`) | exit 101, **E0451** private fields |
| 40 pin rows vs included files vs `registry_pins.rs` vs `schema-source-pins.json` | all match |
| Root + direct `$defs` | **839** |
| Frozen 01 subject SHA | still `b5dfe136…75b6` |

Did not re-run 486986 owning replay or 487156 oracle cases. Archived claims: owning stdout byte-equal to engine 01; 25170 non-synthetic cases through `registered` binary byte-equal to prior reference output. Those inherit engine 01’s `$ref`-wrapper oracle limits.

## Proposed profile-stable oracle (code review, not acceptance)

`check-profile-oracle.py` does **not** edit frozen `canonical.py` (`d47f25db…b442`). It `validators.extend(ExactValidator)` and replaces `evolve` so retrieved Draft 2020-12 resources keep the **same class** (custom keywords + integer type checker). Direct resolved node + `registry.resolver(base_uri=owner)`.

Independent control, same as archived `profile-oracle-result.json`:

| Adapter | `[1, true]` + `x-opensip-order: numeric` |
| --- | --- |
| Direct `ExactValidator(schema)` | false |
| `ExactValidator({"$ref": id})` (stock evolve) | **true** (defect) |
| `Stable({"$ref": id})` (proposed evolve) | false |

That is the engine-01 finding, closed in the **adapter**, not by claiming the old wrapper was fine. Archived 13 `direct-original` vs rust/stable differences are **only** synthetic `urn:exact-ref-order#` / `urn:exact-conditional#` (cross-document `$ref` / `if`). Rust matches the stable adapter (0 mismatches claimed on 487156). The 13 are original-dispatch defects, not selected-instance disagreements.

The adapter is **proposed**. It uses jsonschema `evolve` / `_resolver` internals. A separate session is auditing whether this becomes normative; this review does not accept it as profile law. Next production tests should keep **direct** ExactValidator on the resolved node **and** a profile-stable `$ref` path, including `[1, true]` numeric.

## Security / error / resource

- Missing/extra → `SourceSet`; reorder/tamper/truncate → `SourceBytes`; wrong id after hash → `Schema`.
- Unknown schema id → `SourceSet`; bad selector → `UnselectedEntry`; shape fail → `Mismatch`; `budget=0` → `Limit`; invalid JSON → `Json`.
- Empty `Program::compile(vec![], &[], …)` would succeed if `RegisteredSchemas.program` were public. **E0451 is load-bearing.** Production must not export a public `Program` constructor that can be wrapped, or must keep those fields private forever.
- Compile budget and eval depth 128 remain experimental, not M6.
- No I/O in the `no_std` library.

## Blockers before production selection

1. **Export surface.** Trial still `pub use schema::{Error, Program}` with public `compile`. Narrow to `RegisteredSchemas` / `SchemaHandle` / `ShapeValue` / `AdmissionError` / `SourcePin` (or `pub(crate)` Program) before treating this as a product API.
2. **Source provider.** Host/build must embed or supply the 40 raw documents in pin order. Not done here.
3. **Oracle law.** Profile-stable adapter is not yet an accepted replacement for frozen canonical.py dispatch. Do not select runtime on the 487156 figure alone.
4. **Descriptor/replay.** `ShapeValue` is shape-only. Joins, digest domains, and ReplayedRun remain later.
5. **Resource.** Do not freeze 200 000 000 / 128 as selected M6 law.
6. **Selector set.** 839 root+direct defs only; nested pointers are `UnselectedEntry` by design until a later unit says otherwise.

The owning pin table is the correct next architecture versus engine 01’s borrowed caller documents. It is not by itself a complete M2 admission stack.

## Limits

- Advisory only. Not ACCEPT-DESIGN-UNIT, not runtime selection, not M2 complete.
- Did not re-run 486986 / 25170 / 487156 corpora; did not execute original tmp `run` scripts against original trees.
- Did not read the separate normative-oracle session.
- Did not implement `control_protocol.rs` or source embedding.
- Private Cargo path rewrites are review-only.

## Evidence

- `review/results/probes.json` — SHA `cbffaf7fca57b25ec8332811aaeeb3940e40138b6f68222d69f63e8f902e5ebf`
- `review/copy/identity-source/`, `review/copy/probe/`, `review/copy/consumer-probe/`
- `review/probes/run_probes.py`
