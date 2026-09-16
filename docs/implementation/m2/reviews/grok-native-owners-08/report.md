# Independent Grok advisory: native-owners-08

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Frozen-trial advisory. **Not runtime selection. Not ACCEPT-DESIGN-UNIT. Not M2 complete. Not full native closure. Not ReplayedRun.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-native-owners-review-08/review`. Live product, frozen history, and commits were not edited.
**Prior:** capability-codec-07 advisory `eac98220…a8b4`. Boundary-02 `b1768ea5…386d` (DAG + `CAPABILITY_BYTES_JOIN` before ADMIT). Unicode-case-owner-01 `96de4c76…5ae2` (fold bound **15.0.0**, no rebind). Lock remains **9/15**; this candidate is not a lock successor.

## Standing

Private Plan-capability join and Rust/syntax native-context owner on reviewed07. Identity/deps unchanged. Evaluator orchestrates identity primitives; identity does not depend on evaluator/host. Host **dev-depends** on evaluator for four boundary tests only. Context checks do **not** require all closure member blobs and do **not** claim universe/Plan/Run/replay. TypeScript is explicit `Unsupported("Unicode15 full lowercase owner")` until a FULL default-lowercase owner exists for selected native constant **15.0.0**, distinct from NFC **16** and rustc std **17**. Graph relation/import/capability-manifest-id remain Unsupported.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 47606 | `daf557729e5e8ea24471825eab873a1d9800df643b071465b3ad8cc4250c016b` |
| `subject.tar.gz` | 1650604 | `48a5dbdcbaa40d580e23e673d2e7e8a9721f1a0d370c83e9b40e3810b2bf4104` |
| Files | 267 | 0 missing / 0 mismatch (targets excluded) |
| `native_context.rs` | 10896 | `a5a916c8243ddc750ad820686aef872667ff7b9b46b9e4d1432730168688bc21` |
| `plan_capability.rs` | 2711 | `0954ea49d1885bd8e175ba3674e4724835ba8ef3c584f5fd43f2c73871645d77` |
| `native_context_registry.json` | 2592 | `269f25c1eb66f6cf31fc244c00ba3ee6f06b895d6b2e8ce1e4052071e1c7dd0a` |
| `host/src/native_owner_tests.rs` | 7595 | `bb4bf0adcd40c503d8d4934f5eef08453b91fb1f464c6f13386c8dec6f93af11` |
| identity `capability_codec.rs` / `closure.rs` / `relations.rs` / checker | — | **byte-identical to 07** |

Copied product lock **9/15**.

## Plan capability join

`admit_plan_capability` recomputes Plan identity, rehashes retained capability bytes, then:

1. **`CAPABILITY_BYTES_JOIN`** — `SHA256(UTF8("opensip.capability-manifest.v1") \|\| 0x00 \|\| bytes)` vs Plan `capabilityManifestId` **before** gates
2. selected `e678` `admit_capability_manifest`
3. `CAPABILITY_MANIFEST_IDENTITY` vs opaque result

Malformed bytes + mismatched ID → `BytesJoin`, not a codec/manifest hide. Matching ID on `0xff` reaches `Manifest` after the join. Missing blob → `Input(MissingBlob)`. Per-Plan: a second Plan with wrong ID does not reuse the first.

## Native context owner

`inspect_native_context` rehashes/shape-admits the registered H-frame, then Rust/syntax branches over **closure descriptors** (not member blobs). Causes stay distinct: `unretained` vs `identity-mismatch` vs `kind-mismatch` vs `malformed`; budget `Limit` does not collapse into unretained. Syntax class/suffix/body-language law uses the embedded registry (no caller-chosen table). Re-framing JSON `syntaxClass=code` refuses `…json:declared=code:registered=data-document`. TypeScript arm is Unsupported **15**, not NFC16 and not std17. Selected `UNICODE_CASE_DATA_VERSION = "15.0.0"` was **not** rebound. Running Python `unicodedata` here is 16.0.0; 08 does not call `lib_name_fold`.

## Registry extraction (independent)

`native_context_registry.json` equals:

- `grammarCapabilities` / suffixes / syntaxClass from **current** product `native-v2.schema.json` `e5834d37…7773` (`x-opensip-grammar-capability-registry`)
- `bodyLanguages` `["typescript","javascript","rust"]` from foundation `identity-schemas.v2.json` `c5667985…67d5` (same enum in product identity-v3)
- `bundledGrammars` exact selected `BUNDLED_GRAMMARS` literal

Zero mismatches. Oracle-composition used this current native schema, not the older coop pin `2d37b810…` listed among dependency-pins.

## DAG

evaluator → identity only. host production graph unchanged; evaluator is **dev-dependency**. identity has no evaluator/host edge. Matches boundary-02.

## Initial fixtures (preserved, test-only)

Extra executable on closure tree (invalid `{path,sha256,bytes}`) and H-frame missing 8-byte payload length: both caught; `initial-frame-length-native-context-result.json` is all-invalid (`checked: 0`). TypeScript Unsupported label 16→15 after case-owner audit; Clippy on final source. No production fix for those harness errors.

## Independent reproduction

Trusted rustc/cargo **1.95.0**, `--offline`. XZ streamed; no 07 CVE1/375273 rerun.

| Check | Result |
| --- | --- |
| 267-file pin + archive | match |
| `cargo test --workspace --all-targets` | **91** |
| evaluator compile-fail doctest | **1** → **92** |
| Clippy `--workspace --all-targets -D warnings` | exit 0 |
| Native-context xz | **1197**, 143 checked, 73 native-refused, SHA `7de8296e…3c49` |
| Plan-capability xz | **783**, 81 ADMIT / 694 REFUSE / 2 BytesJoin (+ other join errors), SHA `fe7e7777…c79a` |
| Independent negatives | **ALL_PASS** |

## Independent negatives

- Syntax positive with **one** retained frame blob (no member-blob proof)
- `work=0` → Limit, not unretained
- Missing closure → `…unretained…`; changed descriptor → `…identity-mismatch…`; rekeyed `kind=provider` → `…kind-mismatch…` without unretained
- JSON data grammar cannot promote to `code`
- Plan golden identity `508f24c7…`; malformed+wrong ID → BytesJoin; malformed+matching ID → Manifest after join
- Graph relation still `Unsupported("payload-class owner joins")`

## Findings

**Required:** none relative to the trial’s stated private-candidate standing.

**Should-fix:** none new for this freeze.

**Not findings**

- Context diagnostics without member blobs are the stated subset, not full native ADMIT.
- TypeScript Unsupported is the 08 owner boundary; Unicode 15 tables are a later slice, not a silent 16/17 fold.
- Older coop native-evidence pin `2d37b810…` is not the extraction source; current `e5834d37…` is.

## Limits

- Advisory only. Not acceptance of 08, 07, native ADMIT, M2, or release.
- Did not execute `close_run`, universe binding, body identity, TypeScript fold, or complete replay.
- Graph owner joins remain Unsupported.
- Root proceeds TypeScript Unicode **15** tables separately; no rebind of `15.0.0`.

## Conclusion

08 adds Plan `CAPABILITY_BYTES_JOIN` before selected capability gates, and a Rust/syntax native-context owner over registered frames and closure descriptors, with distinct unretained/identity/kind/Limit causes. Identity/deps unchanged from 07. Vectors and Clippy reproduce.

**Verdict: NOT ACCEPTANCE.** Prototype matches its standing.
