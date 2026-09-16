# Frozen trial review: capability-support-16

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private native syntax-fact support and three Coverage prerequisites. **Not runtime selection. Not Coverage producer admission, full Run, replay, release, or product qualification.** Layout inventory v16 is a separate accepted inventory unit; this source is **not** live-installed.
**Work tree:** `/tmp/opensip-implementation/m2-grok-capability-support-review-16/review`. Live, frozen, and history not edited. No commits.

The archived native-relation-boundary-16 advisory and body-identity-15 source review are **not** acceptance and **not** a fresh-blind of this source.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/capability-support-16/subject.json` | 53521 | `b3d1c76c78cf7d6ae43b4673b90d2458f01c8139bbf818076f2bd88d9a16be28` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 62150830 | `772325a150c0d70a3bf1bd81662bd7105ced78a8b73b7232d1108e59e8040bc5` |
| adjacent `support-result.json` | 359 | `07d99f090898c8ca41755882bd32c78e8c38e1363e58260d9149bf8a6e40e386` |
| adjacent `final-replay-result.json` | 648 | `e89cafc61881ae64d4c62a23a1e22dfd31716e6932d4b6c7a2d587fbc80d5adb` |
| adjacent `oracle-scope-account.json` | 2203 | `16ff2889d27cf027b32ddb9b8deac6fb186b5ddda9eb3dbf546f557a397b2c3a` |
| export | `/tmp/opensip-implementation/m2-capability-support-subject-16` | 301/301 member pins match; tar 301/301; 0 extra; 0 missing |

301 `files[].path` values are unique and string-sorted.

Dependency pins hash-match: body-identity-15 subject `6539a71f…be28`; runtime-v5 unit `597c16f9…2b13`; inventory-v16 subject `6940c86d…1756`; grok native-relation-boundary-16 advisory `caa378f3…7d48`; selected native e678 `e6784aa1…e2b9`; selected identity 619d `619d6e3c…41e6`.

Live lock independently observed **14 inventory / 18 contract** (last inventory **candidate** v16; last contract native-runtime v5). Live tree has body15/`body_identity.rs` from v5 and **no** `capability_support.rs` / `capability-support-registry.json`.

## Source delta vs installed runtime v5

`body_identity.rs` and `body-registry.json` are byte-identical to live v5 / frozen 15. Identity `lib.rs` and identity/evaluator `Cargo.toml` unchanged. External TCB unchanged (`sha2-const-stable=0.1.0`, `tinyvec 1.13.3`, `unicode-normalization=0.1.24`). Identity source policy **110** files independently passed: only local `src/closure.rs` pin `49900/7f6ea3be…` → `50730/72a73d74…`.

| Path | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `product/crates/evaluator/src/capability_support.rs` | syntax-fact + 3 Coverage prerequisite guards | 17797 | `fd330f6943548bc2168f85a34cee84797da498b4400f3b3d7f2aaad9f411e8c0` |
| `product/crates/evaluator/src/capability-support-registry.json` | kebab closed extract | 15937 | `3c30caa66cc1e53deaee4df4eee39784227d30f1b202860fb9eba2c9172ccbd0` |
| `product/crates/evaluator/src/lib.rs` | export `inspect_syntax_fact` / `inspect_coverage_prerequisites` | 1302 | `4ca7bbbfc280cede59a8ffb85c68e28537a3a09b291f342273a776771f814288` |
| `product/crates/identity/src/closure.rs` | `registered_record_shape` | 50730 | `72a73d74b66d857a0f285389bbd5eacbadc41fffe15e505f737d9dd6f0807360` |
| `product/crates/host/src/native_owner_tests.rs` | suffix/empty-view/Limit host cases + pooled blobs | 27887 | `09c4f86958beaa60be1e1ca25d6d706f78721dfb44e9db8ba2fa75895acbca69` |

Closed `grammarCapabilities.languages` equals the live/export native-context-registry table. Adjacent `registry-sources.json` pins identity-v3 / native-v2 / relation-payload-v2 / e678. Not a caller registry.

`registered_record_shape` checks exact selected schema-document digest, retains raw schema bytes, rehashes canonical payload, admits shape, and returns inert JSON (no producer or reference walk). Generic `inspect_relation_sources` still `Unsupported("relation body identity owner")`.

## Law vs selected I (619d) + N helpers (e678)

`inspect_syntax_fact` — walk-time, **before** Plan: crate-private universe frame inputs then actual context owner; compiler universes skip (gates 0); syntax uses **selected grammar row suffixes**; inventory capabilities are exempt; empty path sets are not vacuously supported. No `inspect_plan_native`.

`inspect_coverage_prerequisites` — rehash Coverage/scope/snapshot + `registered_record_shape` (`CoverageResultV3`) then **dialect ownership, syntax, source-variant** in that order. Disclosure is **derived** from the committed universe/ownership/registry, never read as a producer claim. Source-path scopes require **every** subject path; symbol scopes use **any** snapshot inventory path and do not invent symbol-to-path attribution. Empty clones scopes refuse complete (`COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE`). Universe-level missing/partial/ambiguous ownership discloses; uncompiled/unselected individual bodies do not invent universe unavailability (`rust-not-compiled-ownership-missing` stays checked). Distinct complete / undisclosed / deficiency / cause keys.

`NativeSupportChecks.gates_checked` is a private count (1 or 3), not Plan/Run/producer authority. Full Coverage producer is **not** implemented here and, in FullRun, must run **before** these guards. `steps==0`/`depth==0` → `NativeSupportError::Limit` (distinct from Refused). Harness now forwards `steps` (initial 580/6 mismatches were harness ignoring zero-step while the product already returned Limit).

## History (fixtures/harness, not production-limit changes)

- Unsorted anchors failed before corpus; canonical sort.
- Initial 580: six `*-limit` cases expected `limit`, harness returned `checked`; product Limit already correct; harness + Clippy if-collapse fixed.
- Initial 660 ambiguity used invalid `unitId` `other`; corrected to sha256-framed identity; narrow 8 ownership probes then final 660 reach the actual ambiguous guard. Initial660 result preserved (362 checked, 0 mismatch at that fixture).
- Host packets exceeded 4 MiB parser cap; shared body-fixture blob pool (`4158383` < `4194304`). Two failed workspace outputs retained. **No production parser-limit change.**

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- Frozen 660-row actual/expected independently classified: **660/660**, **363 checked**, **0 mismatch**. Separate 8 ownership rows: 0 mismatch.
- Compiler skip: TS/Rust syntax-fact goldens `gates: 0`; syntax-universe golden `gates: 1`. Zero-step cases `result: limit`.
- `cargo test --locked --offline -p opensip-host native_support --lib` on the **export** product: **ok** (selected suffixes, empty-view disclosures, `steps:0` Limit).
- Identity policy independently passed: `sourceFilesVerified: 110`. Frozen workspace.stdout sums to **101**. Final Clippy `-D warnings` compile-only (no diagnostics).
- Prior suites byte-identical: body `8228e14c…93f0` / 965, Plan `340d3bdd…4fcb` / 383, retention `591d2c50…5404` / 304, source `0c08af51…39a6` / 161.

Did not re-pipe 476 MiB `support-requests.ndjson`. Did not re-exec Unicode-15 or 07–12 corpora.

## requiredFindings

None.

## Limits (not required findings)

- Local diagnostics are not Coverage producer admission, Plan selection, inventory totality, complete graph, `close_run`, or ReplayedRun.
- FullRun still owes producer **before** these three guards.
- Gate counts are not a Run token.
- `registered_record_shape` schema-work Limit surfaces as `Record(GraphError::Schema(Limit))`, not `NativeSupportError::Limit`; steps/depth Limit is the owner variant. Not collapsed into Refused.
- Layout inventory v16 names these files; live runtime v5 does not install them.
- Did not re-pipe the 476 MiB request corpus through a rebuilt harness.

## Verdict

No required findings. Private source matches the selected walk-time syntax support and the three Coverage prerequisites (derived disclosure, row-suffix ownership, inventory exemption, compiler skip, empty-scope non-vacuity), with inert `registered_record_shape` and unchanged body15. Not a live/runtime/full-Run selection.
