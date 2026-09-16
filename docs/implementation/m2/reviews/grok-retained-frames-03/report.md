# Independent Grok advisory: retained-frames-03

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Frozen-trial advisory. **Not runtime selection. Not M2 complete. Not ACCEPT-DESIGN-UNIT.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-retained-frames-review-03/review`. Live product, frozen trial, architecture history, and commits were not edited.
**Prior work:** Fixture-composition advisory is archived (`report.json` `6a4806af…e8bd`). Graph02 remains a separate review. This review inspects the frame03 delta on graph02 only. No new blindness is claimed.

## Standing

Subject standing: current retained frame/shape and payload-schema membership prototype; **no native/closure/replay authority**. Copied product `design-lock.json` is predecessor **9 inventory / 12 contract** (last exact-schema-profile-selection-v1). Live lock remains **9/13** with admission-runtime-selection-v1; this trial is not installed.

`parse_hash_preimage` / `digests.rs` is byte-identical to graph02 (`a19ede27…b0ef`). Identity stays `no_std`, `forbid(unsafe_code)`, contracts-only `sha2-const-stable`. Host still embeds the 48 sources. No compiler/native qualification and no Rust replay of a Run.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 41127 | `9fd2f3eb992cda32551688904f4995f49a8f0e8a1468c5ee881c5b8f56f02667` |
| `subject.tar.gz` / archive-pin | 1970976 | `74ce71a08e145520f58efd00f74c97c7ec9878bd8e175348e62ad4dc19aca6c3` |
| Unpacked files | 229 | 0 missing / 0 mismatch / 0 extra |
| `identity/src/closure.rs` | 28165 | `28918388…db4e` |
| `identity/src/lib.rs` | 1415 | `920321ed…74f4` |
| `identity/src/schema_registry.rs` | 26808 | `bc6b9143…c511` |
| `host/src/schema_sources.rs` | 29754 | `e2f96c2b…fdd0` |
| `harness/src/main.rs` | 2962 | `5648f562…9da9` |
| `digests.rs` (unchanged vs graph02) | 3830 | `a19ede27…b0ef` |

Graph02 identity `closure.rs` `15f786ca…7608a` / 22991. Frame03 adds `NativeFrameSet`, `FramedCandidate`, `frame_candidate`, `registered_schema_blob`, walker membership, and `GraphError::{Frame, UnregisteredFrameDomain, UnregisteredSchemaDocument}`.

## Frame03 delta (on graph02)

**`frame_candidate(sha, set, budget)`**

1. Retained blob digest/length (missing → `MissingBlob`; corrupt → `BlobDigest`).
2. Frame prefix `opensip.product.v1\0`, nonempty ASCII domain, then **closed** identity-v3 `domainSets[set]` membership (`native-context` / `native-semantic-universe` / `native-nested`; **12** domains).
3. Reuses accepted **`parse_hash_preimage`** for expected-domain, u64BE length, C(payload)==payload.
4. `current_record_schema(document, selector)` — logical alias → **current** 48-pin bytes. No URI/major historical fallback (`SourceBytes` / `SourceSet`).
5. ExactValidator `admit_json` of the current row selector.
6. Recomputed `hash_canonical_value(domain, shape) == sha`.

`FramedCandidate` fields are **private**. Read-only getters (`digest`, `domain`, `domain_set`, `descriptor`, `schema`, `registry_row`) expose shape/row. Independent compile probe: all five fields `E0616`. `FramedCandidate` does not implement `Debug`. There is no native ADMIT / universe-bind / snapshot-join method.

**`registered_schema_blob(sha)`**

Derives the document set from selected identity-v3 `x-opensip-payload-registry` **rows** (not a caller set). Resolves each logical path through current aliases and compares full-document pin SHA. **9** members. The other **39** of **48** available sources, including current identity-v3 and policy-v2, refuse `UnregisteredSchemaDocument`. Historical native `2d37b810…` and historical policy-v2 `c8b0a907…` (same `$id`) refuse as current.

**Walker**

Graph02 `raw-artifact` + `artifactClass` → `Unsupported("registered schema membership")`.
Frame03: blob, then if `artifactClass == registered-schema-document` call `registered_schema_blob`. Frozen **2520** local-walk outcomes are **byte-identical** to graph02 (`expected.txt` / `actual.txt` `97e2d1a7…`). Those 9 `unsupported` cases are candidate corpus labels (`coverage` / `evaluation-subject` / `run`), not schema-membership hits. `view.schemaDigests` is the annotation that would exercise membership; a view walk visits `planId` first and the referenced plan still `Unsupported("capability derivation")`. Membership is implemented; the frozen 2520 corpus does not reach it.

## Independent reproduction

Trusted Cargo/rustc **1.95.0**. Offline. Private `CARGO_TARGET_DIR`. Unpacked copy only.

| Check | Result |
| --- | --- |
| Harness `cargo build --offline --locked` | exit 0 |
| Replay `requests.ndjson` vs `expected.txt` | **2520/2520**, 87 ok / 246 unavailable / 2178 invalid / 9 unsupported |
| Replay `frame-requests.ndjson` vs `frame-expected.txt` | **794/794**, 23 ok / 12 unavailable / 759 invalid, **0 mismatch** |
| 12 domain positives in 794 | all 12 native context/universe/nested domains have ≥1 `ok` |
| 9 payload-registry documents in 794 | enumeration, emission, recognition, import-source-context, imported-v1, native-v2, policy-v1, relation, test-execution |
| `cargo test -p opensip-host --lib retained_input_tests` | **9/9**, 11 filtered |
| `cargo clippy --workspace --all-targets -- -D warnings` | exit 0 |
| Independent negatives crate | **ALL_PASS** |
| External private-field access | **E0616** × 5 |

794 `ok` breakdown (independent labels): 12 domain `schema:29` frames + extra `dependency-file-manifest` `schema:16` + empty-array payload + 9 schema-membership files = 23. Oracle is selected `parse_h_frame` plus workflow/current-overlay schema admission, **not** native `admit_*`.

## Independent negatives (review-only)

- All **48** `source_requirements` pins match product files (length+SHA).
- Exactly **9** of 48 `registered_schema_blob` succeed; identity-v3 and policy-v2 do not.
- Historical same-`$id` native/policy refuse as current.
- Missing schema blob → `MissingBlob`; corrupt digest → `BlobDigest` (not `UnregisteredSchemaDocument`).
- Wrong `NativeFrameSet` → `UnregisteredFrameDomain`.
- Raw C bytes → `FramePrefix` (`parse_hash_preimage` also fails). Truncation/length mismatch → `FrameLength` / `Frame`, not unavailable.
- Missing frame blob → `MissingBlob`.
- Getters return current native document row `native/native-evidence.schemas.v2.json`, not a historical alias.
- No caller-supplied membership set exists on the API.

## Findings

**Required:** none relative to the trial’s stated prototype standing.

**Should-fix (latent; not hit by 2520/794):** graph02 treated every `artifactClass` as `Unsupported`. Frame03 implements membership only for `registered-schema-document` and maps any other class to `GraphError::Law`. Selected identity-model.v3 special-cases only `registered-schema-document` and otherwise retains the blob; `producer-interface-stage-output-schema` remains a later owner join. Trial README: “Other owner obligations remain explicit Unsupported.” `Law` here is the wrong category if a stage-spec `outputSchemaDigest` is ever walked. Prefer `Unsupported("stage output schema owner join")` (or blob-only, matching the Python digest field). Do not treat this as permission to add native ADMIT.

**Not findings**

- Getters are not authority. Independent compile and API surface agree.
- Current-only aliases are correct. Historical bytes must not become current via `$id`.
- `current_record_schema` is `pub(crate)`; external code cannot pass a chosen schema set.
- Incomplete nested blob (focused test) can coexist with a valid `FramedCandidate`. That is the stated shape/frame boundary, not a missing native join in this unit.

## Limits

- Advisory only. Not acceptance of frames03, graph02, A04/A05, M2, or release.
- Did not run full workspace 68 tests (belongs to graph02). Nine focused tests + Clippy only, as the trial states.
- Did not execute original `/tmp/opensip-implementation/m2-retained-graph-trial-03` checkers in place; reproduced from the frozen archive.
- Did not run `close_run`, native `admit_*`, compiler, or Rust Run replay.
- Walker membership is code-complete but not exercised by the frozen 2520 vector.
- Copied design-lock is predecessor authority only.
- Root remains independently working the annotation walker. This trial is not that walker’s completion.

## Conclusion

Frame03 is a bounded, current-profile increment on graph02: H-frame parse/recompute via accepted `parse_hash_preimage`, closed 12-domain sets, current alias schema selection, and a 9-document payload-registry membership check that does not treat the 48 sources as registered. Reproduction matches the frozen 794 and 2520 corpora. Private fields do not leak construction. Native ADMIT and context joins remain later owners.

**Verdict: NOT ACCEPTANCE.** Prototype is consistent with its standing. One latent owner-class classification should be fixed in a successor if stage-output schema walks are added. No live/frozen edits.
