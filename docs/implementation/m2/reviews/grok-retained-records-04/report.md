# Independent Grok advisory: retained-records-04

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Frozen-trial advisory. **Not runtime selection. Not M2 complete. Not ACCEPT-DESIGN-UNIT.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-retained-records-review-04/review`. Live product, frozen trial, architecture history, and commits were not edited.
**Prior:** frames03 advisory archived (`dd597e51…d758`). Fixture-composition archived. Graph02 remains separate. Root continues the next slice separately.

## Standing

Subject: restricted cross-document records prototype; **proposed** recognition-reference dependency; no runtime/closure/replay authority. Copied product lock is predecessor **9/12**. This trial does not select `recognition-derived-reference-selection-v1` and does not claim full graph replay.

Live lock at this review: **9 inventory / 14 contract**, last row `docs/implementation/m2/recognition-derived-reference-selection-v1/successor.json`. That is a **separate** unit. It does not install records04, and this advisory does not accept either as complete M2.

The Rust recognition branch implements the already-selected **feature** recipe `J-FRP-ID` (`native_h("native.framework-recognition.v1", recognition)` → `sha256:`+H). Matching inline hash does not prove feature inventory/entry/evidence/summary joins and is not native ADMIT.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 46850 | `f786c3e2a584e823bf2e155666763261184ffd603caeeaeb14ef1a2c9797fb78` |
| archive / archive-pin | 2030940 | `5080767f…6d99` |
| Unpacked files | 265 | 0 missing / 0 mismatch / 0 extra |
| `identity/src/closure.rs` | 38164 | `3ea33820…ac9f` |
| `host/src/schema_sources.rs` | 36928 | `feb9253f…ea2c` |
| `harness/src/main.rs` | 3155 | `d61f3c15…cf61` |
| `digests.rs` / `schema_registry.rs` / `lib.rs` | — | **unchanged vs frames03** |

Frames03 `closure.rs` `28918388…db4e` / 28165. Local/frame corpora byte-identical to frames03 (`97e2d1a7…`, `b6a41249…`).

## Records04 delta (on frames03)

- **Owner-aware walk:** `walk` / `deref` / `carries_digest` / `branch_matches` take the owner schema id. Root-then-branch overlay keeps the owner document’s root assertions (including `x-opensip-*`), matching the selected reference discriminator.
- **`inspect_identity_record(sha, kind)`** / **`inspect_current_record(sha, document, selector)`:** structural inspection only. Comments and `StructuralChecks` counts are not Plan-selected tokens. Memo: local `(sha, kind)`; foreign `(sha, document, selector)`; foundation digest-law once per document.
- **Foreign canonical records:** rehash, C(value), `current_record_schema` (current alias, no URI/major fallback), exact admit. **Foundation** documents then run the bare-hex annotation coverage sweep and recursively walk digest annotations. **Non-foundation** (native/workflow) stop after shape, like model `foreign_payload`. Owner semantic joins are not implemented here.
- **Bare-digest coverage:** definition-wide hex `$defs` are not a blanket exemption; each field/branch/items/property that is a bare 64-hex pattern must carry `x-opensip-digest` (`UnannotatedFoundationDigest`). Identity/relation bundles keep their own sweeps.
- **Frames03 should-fix:** `producer-interface-stage-output-schema` is `Unsupported("stage output schema owner join")` **after** the retained blob check. Focused test: present blob → Unsupported; missing blob → `MissingBlob` first. Other unknown `artifactClass` remains `Law` (no generic bypass). Registered-schema-document still uses the nine-document membership set.
- **Recognition:** closed branch for `h-identity` domain `native.framework-recognition.v1` with `retention=derived` and `form=sha256-text`; compare `sha256:`+`hash_canonical_value` of sibling `recognition`. No CAS frame required. Mismatch → `DerivedIdentity`. Not a generic derived skip or form dispatcher.

Remaining `Unsupported`: payload-class records, fragment/owner-retained, capability derivation, registered H-frame domain sets, stage-output owner join.

## Original 1736 is not a pass

Selected identity-model.v3 (no recognition branch): `PREFIX['native.framework-recognition.v1']` → **`KeyError('native.framework-recognition.v1')`**. Frozen `recognition-reference-fault.json` and `record-result.json` preserve that fault (index 209, `schema:8369`, UnitRecognitionV1).

Independent replay of `record-requests.ndjson` vs `record-expected.txt`: **not equal**. Sole mismatch: expected `reference-fault`, harness `invalid`. Not relabelled pass.

## Independent reproduction

Trusted rustc/cargo **1.95.0**, offline, private target dirs.

| Check | Result |
| --- | --- |
| Local 2520 vs frames03 expected | match |
| Frame 794 vs frames03 expected | match |
| Records 1738 vs `records-expected.txt` / `proposed-record-actual.txt` | match (116 ok / 1605 invalid / 16 unavailable / 1 unsupported) |
| Original 1736 | **not pass** (1 `reference-fault` vs `invalid`) |
| `retained_input_tests` | **13/13** |
| `cargo test --workspace` | **74 passed**, 0 failed |
| Clippy `--workspace --all-targets -D warnings` | exit 0 |
| Independent probes | ALL_PASS |

1738 is the narrowly **proposed** record oracle (pending separate reference review). It is not a claim that the Python successor is this trial’s selected runtime law.

## Independent probes

- Cross-document foundation: emission-plan `policyDigest` → current policy-v2; counts 2 records / 2 blobs / 0 objects (not a Plan token).
- Second inspect of the same `(sha, document, selector)` is stable (memo).
- Native-v2 `DependencyFileManifestV1`: shape-only; nested `contentSha256` blob may be missing. Not a generic foundation walk of native form/preimage metadata.
- Coverage `payloadDigest` (`payloadClass`) → `Unsupported("payload-class record")`.
- Correct recognition hash inspects without the derived H frame present; object_count 0 (not feature/native ADMIT).

## Findings

**Required:** none relative to the trial’s stated prototype standing.

**Should-fix:** none new. Frames03 stage-output `Law` classification is corrected and covered by a focused test that distinguishes missing blob.

**Not findings**

- Implementing `J-FRP-ID` in Rust does not select the Python identity-model successor and does not admit a world/feature/native closure.
- Broad native-v2/form dispatch is absent; non-foundation foreign records are shape-only.
- Diagnostic counts are not selected-Plan evidence.

## Limits

- Advisory only. Not acceptance of records04, the recognition-reference unit, frames03, graph02, A04/A05, M2, or release.
- Did not re-run original tmp overlay checkers in place; reproduced from the frozen archive.
- Did not execute `close_run`, native `admit_*`, compiler, or complete evaluator replay. README’s retained syntax graph/RunId is not re-claimed here.
- 1738 matching the proposed reference is not a substitute for that reference unit’s own review.
- Remaining payloadClass/context, fragment/owner-retained, capability, and native semantic joins stay `Unsupported`.

## Conclusion

Records04 is a bounded cross-document inspection increment on frames03: owner-aware refs, current-alias foreign shape, foundation annotation coverage, inspect APIs that return counts, and an exact `J-FRP-ID` inline hash check. Predecessor 2520/794 are unchanged. Original 1736 KeyError is preserved as a non-pass. Stage-output owner join is explicit Unsupported after blob check.

**Verdict: NOT ACCEPTANCE.** Prototype matches its standing. Root continues the next slice separately.
