# Independent Grok advisory: retained-payloads-05

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Frozen-trial advisory. **Not runtime selection. Not M2 complete. Not ACCEPT-DESIGN-UNIT. Not native ADMIT.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-retained-payloads-review-05/review`. Live product, frozen trial, architecture history, and commits were not edited.
**Prior:** records04 advisory archived (`c30809b9…ede5`). Recognition-derived reference `619d6e3c…c141e6` is separately **ACCEPT-DESIGN-UNIT** and live lock **9 inventory / 14 contract**. This trial does not install that unit; it uses the now-selected identity-model as the restricted oracle. No fresh blindness claimed.

## Standing

Subject: restricted registered **parameter/coverage** payload prototype; no full closure/native/replay authority. Copied product lock is predecessor **9 inventory / 12 contract** (last exact-schema-profile). Live last contract is `docs/implementation/m2/recognition-derived-reference-selection-v1/successor.json` and does **not** install payloads05.

`registered_payload` is closed to `parameter` and `coverage`. Relation/import stay `Unsupported("payload-class owner joins")`. `resolvedThrough` domain recipes are not payload roots (`GraphError::Law`). Coverage shape-valid input proceeds to `MissingObject(scope)` and is **not** native-semantic admission.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 41647 | `1fcb79f28a805384b81062bb413630e02786491b31da4d7ad4088484b6f1e856` |
| archive / archive-pin `subject.tar.gz` | 5214458 | `32864d57decf927841817f527cecf7d5ec525386d96a08c1c2848181bd5778e4` |
| Unpacked files | 232 | 0 missing / 0 mismatch / 0 extra (private `subject/` and `from-archive/`) |
| `identity/src/closure.rs` | 42278 | `b16d165067fde871098733c9cad8d6fc950c7481ff4b2a27bfe15a62ae614c4d` |
| `host/src/schema_sources.rs` | 43863 | `68c141689171524869c409208023b9658db5d81c7aa7c41505430d7d8a4c629b` |
| `harness/src/main.rs` | 3330 | `c626416d788874247c7b617b2f97e1d5186cce5e3e8e1ed7f86c696eceb5ec55` |
| `payload-requests.ndjson` | 36596181 | `d3f63eadce842977674e7a04b4f283831097d7a66d2ed82cb8e41abb50ac2a2e` |
| `payload-expected.txt` / frozen `payload-actual.txt` | 35655 | `264527c8ab2bd729803f3624bc23b8ff02f79652044de25fb72a5da13f65b79d` |
| `digests.rs` / `schema_registry.rs` / `lib.rs` | — | **unchanged vs records04** (`a19ede27…`, `bc6b9143…`, `920321ed…`) |

Records04 subject `f786c3e2…7fb78` (46850, 265 files). Shared product files that changed: `closure.rs`, `schema_sources.rs`, `harness/src/main.rs`, README, clippy/test logs, dependency pins.

## Payloads05 delta (on records04)

- **Class gate:** `payloadClass` not in `{parameter, coverage}` → `Unsupported("payload-class owner joins")` before any registry row. `resolvedThrough` → `Law`.
- **Parameter row:** keyed by cited `schemaDigest`. Matches closed `x-opensip-payload-registry.classes.parameter.rows` whose **full document** SHA (`current_record_schema(document, "").document_sha256()` = `SOURCE_PINS[index].sha256`) equals the cited digest. 0 matches → `PayloadRegistryRow`; >1 → `AmbiguousPayloadRegistryRow`. Not a subschema hash, URI, or major.
- **Coverage row:** keyed by `payload.schemaVersion` string/int → registered key (`"3"` only). No default row.
- **Cited schema document:** selected row handle SHA must equal cited digest (`PayloadSchemaDocument` otherwise). Exact full bytes must be retained and rehashed (`MissingBlob` / `BlobDigest`).
- **Selector:** `admit_json` uses the row selector (`#` → root; `#/$defs/CoverageResultV3` → that entry). Not a caller-chosen registry: `RegisteredSchemas::from_sources` still refuses length/pin mismatch.
- **Admission before memo:** every reference re-runs row selection + schema-document check + `admit_json`. There is **no** payload-admission memo. `foreign_record` may reuse `(sha, document, selector)` only **after** that per-reference admission. Shared payload + second unregistered `schemaDigest` → `PayloadRegistryRow`.
- **Foundation recurse:** `parameter` and `document` starts with `foundation/` → `foreign_record` (shape + foundation digest-law walk). Coverage’s native document does **not** recurse; shape success is not native proof.
- **Python decode memo vs Rust:** selected model memos only parsed canonical bytes (`payload-decode`). Rust re-canonicalizes every time. Admission context is not skipped in either.

`StructuralChecks` still expose `object_count` / `blob_count` / `record_count` only. Independent parameter success: records=2, blobs=3, objects=0. Those counts are not Plan tokens.

## Oracle-input-order account (preserved, not a runtime change)

Initial oracle (1921 cases, records + parameter/coverage extras, **no** 2520 local) built coverage dictionaries in Python insertion order (`scopeId` before `payloadDigest`). Rust parsed canonical/sorted instance keys (`payloadDigest` first). Cases with **both** missing scope and invalid payload disagreed on first failure (`unavailable` vs `invalid`): **118 mismatches**, first `coverage:17910:current`.

Correction: round-trip each request through selected `C.canonical` / `C.parse` before **both** implementations. Neither identity-model nor Rust `registered_payload` changed for that. Preserved: `payload-result.initial-oracle-order.json` (`8bf07355…9a6c`), `payload-expected.initial-oracle-order.txt` (`5ef9a1ec…8801`), `oracle-input-order-account.json`. This does **not** establish fault precedence for arbitrary in-memory insertion orders. Walk still follows instance key order (Python dict after canonical parse; Rust `BTreeMap`), matching the selected `walk`.

Current corpus is 4441 = 1738 record + 2520 local + 63 parameter + 120 coverage.

## Independent reproduction

Trusted rustc/cargo **1.95.0**, `--offline`, private `CARGO_TARGET_DIR` under the review tree.

| Check | Result |
| --- | --- |
| 232-file pin verify (copy + archive) | match |
| Dependency pins (records04, unit `5c84dad9…`, identity-model `619d6e3c…`, records04 advisory, admission-work-map) | match |
| Overlay `foundation/import-source-context.schema.json` and product `import-source-context-v1.schema.json` | both `51cdca8b…6518` |
| Overlay/product `native-v2` / `native-evidence.schemas.v2.json` | both `e5834d37…7773` |
| `retained_input_tests` | **16/16** |
| `cargo test --workspace --all-targets` | **77 passed**, 0 failed |
| Clippy `--workspace --all-targets -D warnings` | exit 0 |
| Harness replay `payload-requests.ndjson` vs `payload-expected.txt` | **4441 = expected**, 0 mismatch |
| Outcomes | 205 ok / 3948 invalid / 280 unavailable / 8 unsupported |
| Independent negatives | **ALL_PASS** |

Archive `focused-final.stdout` is the 16-test log. Archive `retained-tests.stdout` lists 15 (captured before the coverage focused test); not used as the passing claim.

Of 205 ok: 2 are parameter `retained-schema` (valid ImportSourceContextV1). **0 coverage cases are ok.** 8 unsupported are inherited (stage-output / evaluation-subject / run), not a relation/import ADMIT.

## Independent probes

- Subschema SHA of canonical `$defs/CoverageResultV3` ≠ full native-v2 document (`0d1beefc…` vs `e5834d37…`); citing it as `payloadSchemaDigest` → `PayloadSchemaDocument`.
- `RegisteredSchemas::from_sources(&[b"{}"])` → `SourceSet` (no caller-chosen registry).
- Parameter: missing schema blob → `MissingBlob`; exact retained full document → ok; corrupt bytes under same digest → `BlobDigest`.
- Shared payload, second `schemaDigest=f*64` → `PayloadRegistryRow` (no memoized second-context success).
- Coverage shape-valid → `MissingObject(scope)` (not native ADMIT); wrong document SHA → `PayloadSchemaDocument`; schemaVersion `"2"` → `PayloadRegistryRow`; `{schemaVersion:3}` only → `Schema(Mismatch)`.
- Fact `payloadClass=relation` → `Unsupported("payload-class owner joins")`.
- Import object/role check succeeds without payload bytes; walk does not return ok (here `MissingBlob` on an earlier auxiliary digest, before the class gate). Same class gate as relation.

## Findings

**Required:** none relative to the trial’s stated prototype standing.

**Should-fix:** none new for this freeze.

**Not findings**

- Coverage first-failure among simultaneous payload+scope faults follows canonical instance key order; original failed expected vector is preserved; runtime/reference were not changed to invent a precedence law.
- `atMostOnePerSpec` / `admit_parameter_selection` is pre-Plan / `close_run`, not this inspect surface. Byte-identical duplicate parameter entries still fail `uniqueItems`.
- Implementing parameter/coverage registry rows does not admit relation/import/native/full Run and does not select a caller registry.
- Diagnostic `StructuralChecks` counts are not selected-Plan evidence.
- Archive clippy log includes a pre-fix `collapsible_if`; `clippy-clean` and independent `-D warnings` pass.

## Limits

- Advisory only. Not acceptance of payloads05, records04, frames03, graph02, A04/A05, M2, or release.
- Did not re-run original tmp overlay `check-oracle.py` in place (it binds `/tmp/opensip-implementation/m2-retained-graph-trial-05` and overlay paths); reproduced from the frozen archive + private copy.
- Did not execute `close_run`, native `admit_*`, compiler, or complete evaluator replay.
- Relation/import/native/fullRun owner joins remain Unsupported or later. Root continues that work with the other Grok boundary review.
- Copied product `design-lock.json` is historical 9/12 and does not authorize these prototype sources.
- 4441 matching the restricted selected reference is not full closure comparison and is not native proof.

## Conclusion

Payloads05 is a bounded registered **parameter/coverage** increment on records04: exact closed-row selection by full schema-document SHA, retained schema blob, row selector, per-reference admission before any foreign memo, and foundation-only parameter recurse. Coverage positives are shape-then-missing-scope. Relation/import stay Unsupported. Original oracle-order mismatch is preserved as a harness-input account, not a silent runtime change.

**Verdict: NOT ACCEPTANCE.** Prototype matches its standing. Root continues relation/import owner work separately.
