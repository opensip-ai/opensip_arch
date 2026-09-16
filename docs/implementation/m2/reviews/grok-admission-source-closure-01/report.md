# Independent Grok advisory: M2 admission source closure (48) and API boundary

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement. Not the separate reference-profile session.
**Kind:** Bounded source/API boundary review. **Not acceptance.** Not runtime selection. Not M2 complete.
**Work tree:** `/tmp/opensip-implementation/m2-grok-source-closure-review-01/review`. Live, frozen, and history were not edited.

## Standing

The live **40** `schemas/registry.json` rows are the **generation** selection. Selected identity-v3 `x-opensip-payload-registry` / digest annotations name additional **foundation record documents**. A complete M2 shape helper that compiles identity payload/parameter rows needs those documents as **admission-only** sources, not as a silent URI→bytes guess. Source-selection-v2 README (bound through v3): current producer uses selected schema **bytes**; historical readers use the retained exact descriptor; an old URI or major alone never authorizes a new interpretation.

## Census (independent check)

Exploratory census `m2-admission-source-closure-01/result.json` SHA `c9ab0337e180320adec40c47831461c4053186d7443c4687c9bf90b69d2c2c1c` / 16963. Script SHA `d958e0d91ba9804c52732ae6d064c702db747e53edc42522f3b1bea9e2a91ad8`.

| Claim | Verified |
| --- | --- |
| 40 generation sources | yes (`schemas/registry.json`) |
| 15 unique `document` paths in live identity-v3 | yes |
| 8 additional foundation files, `$id` not in the 40 | yes; `$ref` among those 8 + 40 ids: **no unresolved foreign ids** |
| 72 patterns, 3 new | yes (CanonicalText / control-char text / `SubjectIdV1`) |
| New `x-opensip-*` vs engine-01 ignore-list | **11** extra annotations (plus existing semantic `x-opensip-order`) |

Live identity-v3: 197480 bytes, SHA `311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f`. Base `identity-schemas.v3.json`: 196987 / `a76c9e2f…db21`. Different bytes (recognition overlay). Do not hash-substitute base for selected.

## Exact alias map (logical document → accepted **current** bytes)

Admission `payloadSchemaDigest` is SHA-256 of the **exact full document file** named by the row. Pins must be current selected producer bytes, not same-`$id` historical files.

| Logical `document` | `$id` | Current bytes (authority) | Classification |
| --- | --- | --- | --- |
| `foundation/enumeration-plan.schema.v1.json` | `opensip.product.enumeration-plan.1` | foundation 19975 / `10627cb6…197c` | **new** admission source |
| `foundation/evaluator-emission-plan.schema.v1.json` | `urn:opensip:product-v1:evaluator-emission-plan:1` | 3055 / `ac9ae438…198e` | **new** |
| `foundation/execution-inputs.schema.v1.json` | `opensip.product.execution-inputs.1` | 39910 / `604bd941…00e9` | **new** |
| `foundation/import-source-context.schema.json` | `urn:opensip:product-v1:import-source-context` | 842 / `51cdca8b…6518` | **new** |
| `foundation/incoming-search.schema.v1.json` | `opensip.product.incoming-search.1` | 13724 / `accb597a…b8a1` | **new** |
| `foundation/relation-payload-schemas.v2.json` | `opensip.product.relation-payload.2` | 57623 / `53380a24…be9a` | **new** |
| `foundation/subject-inventory.schema.v1.json` | `opensip.product.subject-inventory.1` | 16861 / `6ab46925…ee33` | **new** |
| `foundation/target-attribution.schema.v2.json` | `opensip.product.target-attribution.2` | 23086 / `bd938f11…1d53` | **new** |
| `native/native-evidence.schemas.v2.json` | `urn:opensip:product-v1:native:evidence-schemas:v2` | **selected** `schemas/sources/native-v2.schema.json` 280357 / `e5834d37…7773` | **explicit current vs historical** (hist 277967 / `2d37b810…6043`, **same `$id`**) |
| `workflows/schemas/policy-document.v2.schema.json` | `urn:opensip:product-v1:policy-document:2` | **selected** `policy-v2.schema.json` 26534 / `b221b5ed…9b55` | **explicit current vs historical** (hist 27863 / `c8b0a907…3595`, **same `$id`**) |
| `workflows/schemas/common.schema.json` | common v1 | selected 55042 / `b7b25d5e…d39c` | exact existing |
| `workflows/schemas/imported-evidence.schema.json` | imported v1 | 46315 / `edce21a3…4b9e` | exact existing |
| `workflows/schemas/policy-document.schema.json` | policy v1 | 20724 / `012505da…2e18` | exact existing |
| `workflows/schemas/test-execution.schema.json` | test-execution | 13672 / `a6f7c2d8…d54b` | exact existing |
| `foundation/framework-recognition-plan.schema.v1.json` | `opensip.product.framework-recognition-plan.1` | **already in the 40**: `schemas/sources/framework-recognition-plan-v1.schema.json` 10188 / `49aacd86…f822` | **census listed unlocated**; foundation file is absent. Not a 9th new file. Alias to **current selected 40** bytes. |

**Unsafe substitutions (refuse):** historical native `2d37b810…` or policy-v2 `c8b0a907…` as current `payloadSchemaDigest`; base identity `a76c9e2f…` as live identity-v3 `311c1feb…`; inventing a foundation path for recognition instead of the selected 40 file; using `$id`/major without the file SHA.

Candidate count **48** = 40 generation + 8 new. Recognition is inside the 40, not an extra document.

## Patterns and annotations

Three new closed predicates are required (Python `re.search` / selected `$` law):

- `^[\^\u0000-\u001f\u007f-\u009f]*(?![\\s\\S])` and `+` (CanonicalText / detail)
- `^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\\s\\S])` (`SubjectIdV1`)

Engine-01 ignore-list must **gain** these shape-only annotations (do not execute as keywords):  
`x-opensip-kind-derivation`, `x-opensip-file-membership-extent-law`, `x-opensip-new-internal-faults`, `x-opensip-derived-carrier-law`, `x-opensip-external-joins`, `x-opensip-applicability-precedence`, `x-opensip-identity`, `x-opensip-law`, `x-opensip-relation-registry`, `x-opensip-subject-language-table`, `x-opensip-join-law`.  
Keep `x-opensip-order` semantic; keep `x-maxUtf8Bytes` ignored at generic shape.

## Report-root codec vs identity parser (do not mix)

Selected report codec profile 6 (`source-selection-v2/report-codec-profile.json` SHA `9f516661…b6d1`, standing **proposed**): `documentMaxBytes` **27829365**, `maxContainerDepth` **39**, report root `urn:opensip:product-v1:workflows:evaluator3:report-projection:1#`, schema SHA `bbb5ca92…cc97`.

Generic identity C parser: **4 MiB / depth 32**.

The 48-pin `from_sources` helper may **compile** the report **schema document** (161357 bytes, under 4 MiB). It must **not** be presented as report-root **instance** admission. Feeding a 27 MiB / depth-39 report through identity parse would fail as `Json`/byte-limit — the wrong error, and a silent M4 waiver if MAX_BYTES were raised.

**Recommendation (no schedule waiver):** M2 identity registry **explicitly refuses** report-root (and any other non-C codec) with a dedicated unsupported-codec / not-this-profile outcome, not `Mismatch` and not a 4 MiB parse accident. **M4 / reporting** implements the fixed report profile. Do **not** add a generic identity exception to 27 MiB/39 now. Owner: reporting, not identity.

## Ownership, provider, inventory

- **Identity** stays `no_std` + contracts-only DAG. Inventory v10: 20 packages; identity files today are Cargo.toml, canonical, canonical_tests, closure, descriptors, digests, lib — **no** `schema.rs` yet. Adding `schema.rs` / `schema_patterns.rs` / `schema_registry.rs` / `schema_tests.rs` is an inventory **file** successor, not a 21st package.
- **Contracts stay a leaf.** Do not generate carriers for the 8 admission-only documents unless a later unit needs them. Do not put the pin table in `crates/contracts`.
- **Host (future) is the source provider:** embed or load the 48 raw files in pin order; call `from_sources`. Identity holds **pins** (id/path/len/SHA), not necessarily `include_bytes!` of ~0.7 MiB+ JSON.
- **Two maps:** keep `schemas/registry.json` + generation source-map at **40** (Typify/namespaces). Add `schemas/admission-registry.json` + `admission-source-map.json` for the **48** admission closure and aliases. Eight new `schemas/sources/*` filenames (hyphen-vN, matching current style). Generator options unchanged.

`from_sources(&[u8; 48])` compiling **only exact pins** is a useful M2 helper. It is not report-root admission and not descriptor/replay.

## Model overlay when porting

`identity_model.proposed.v3.py` (157728 / `5ba92896…5369`) vs base `identity-model.v3.py` (157684 / `a6dc5f99…803dc`): **2189 lines, only line 60 differs** — adds `framework-recognition-plan.schema.v1.json` to the local HERE list. Both still load **foundation filenames** (`identity-schemas.v2.json`, `target-attribution.schema.v1.json`, …), not `schemas/sources/*`. Porting must overlay:

- SCHEMA → selected identity-v3 `311c1feb…`
- recognition plan → selected 40 file `49aacd86…`, not a missing foundation path
- native/policy-v2 → selected current SHAs, not historical
- do **not** treat model `target-attribution.schema.v1.json` / `identity-schemas.v2.json` as extra current admission documents unless identity-v3 payload rows name them (they do not)

HERE-relative execution of the proposed copy is not product authority.

## Remaining boundaries (not M2 complete)

1. Write the alias map with **current SHAs**; refuse same-`$id` historical bytes.
2. Fix census “unlocated” recognition → alias into selected 40.
3. Extend pattern table + ignore-list before compiling 48.
4. Inventory successor for 8 sources + 2 maps + 4 identity modules; 20-package DAG unchanged.
5. Host source-provider unit (embed/load); identity stays pure.
6. Explicit M2 refuse of report-root codec; M4 implements profile 6.
7. `Program` export still not a product wrapper for untrusted schemas (trial-02 E0451 lesson).
8. Descriptor joins / ReplayedRun remain later. Independent profile-oracle correction is a separate review.

## Limits

- Advisory only. Did not install sources, did not edit live/frozen, did not read the other Grok profile-correction conversation.
- Did not re-run schema-engine 486k corpora.
- Did not accept source-selection-v2/v3 as installed lock (v3 is binding-order correction; source still not in product lock).
