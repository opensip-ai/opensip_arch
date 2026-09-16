# Independent Grok advisory: capability-codec-07

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Frozen-trial advisory. **Not runtime selection. Not ACCEPT-DESIGN-UNIT. Not M2 complete. Not native ADMIT. Not ReplayedRun.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-capability-codec-review-07/review`. Live product, frozen history, and commits were not edited.
**Prior:** relations06 portable-bound advisory `9a0b1f31…ba53`. Lock is now **9 inventory / 15 contract**; last contract is capability-totality reference `e6784aa1…e2b9` (other Grok `ACCEPT-DESIGN-UNIT` `bc9d694d…efff`, unit `f9c3c13a…cfbb`). That selects the **reference**, not this candidate implementation.

## Standing

Private CVE1 codec, evaluator capability-encoding owner, and proposed pure-identity source/dependency policy. `CapabilityManifest` fields are private; compile-fail doctest refuses independent construction. Integer `schemaVersion` values and provider/language/version strings are **OPEN**. Encoding `windows-x86_64-msvc` (or musl) is registry membership, **not** product platform custody. Graph relation/import remains `Unsupported("payload-class owner joins")`; `capability-manifest-id` remains `Unsupported("capability derivation")`.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 46373 | `a415bb72f37578a5424e020f2d0fde6ff9d0ec07423d03927af5a6f8b0497d09` |
| `subject.tar.gz` | 2350558 | `2ff78c8c8b50d0507a6487f771620538034f6f5e1ca85bd1b3f67657ebd07cad` |
| Unpacked / copied files | 261 | 0 missing / 0 mismatch / 0 extra (targets excluded) |
| `identity/src/capability_codec.rs` | 9297 | `f0c81e353e431239ac448bbc2bdc884c59d4c8e976cd59f2481a167c54e74db9` |
| `evaluator/src/capabilities.rs` | 15116 | `d4928454d0153cba66bf067204f07ac56f46eeebcf03351daf3f14c7aed080cb` |
| embedded `capability_registry.json` | 16522 | `1456ae1476dfe1b0f3b1134c9d7a36e35890e45e20f57e7bbc2b7ada2144aef6` |
| `check_identity_dependencies.py` | 7630 | `655ecea7af9b0bfe389ebd1f9387e377c40e6c7ae8269afd7851ef50302cacd1` |
| `tools/identity/dependency-policy.json` | 21165 | `58399e317983558f9a35a1b5c8566f2a0d634e5de4494f173309d90619c94520` |
| `closure.rs` / `relations.rs` | — | **byte-identical to relations06** (`a6dc8b89…`, `af375b0d…`) |

Copied product lock is **9/15**. Candidate code is not a lock successor.

## Delta vs relations06

- **CVE1:** eight tags, exact integer ranges, NFC Unicode 16, unsigned UTF-8 map order, depth 64 / count 1048576, truncation/trailing/duplicate/unknown-tag refuse. Values inert. Encoder also stays inside decoder bounds. **Not** the JSON-C profile (depth 32).
- **Capability owner:** `admit_capability_manifest` over exact retained CVE1 bytes, embedded registry pin `1456ae14…` (byte-identical to coop `capability-manifest-domains.v2.json`). Gates ADM-TYPE / CLOSED / DOMAIN / ORDER. Identity `SHA256(UTF8("opensip.capability-manifest.v1") \|\| 0x00 \|\| committedBytes)`. Golden `508f24c7…8881b`.
- **Source policy:** dedicated identity checker, independent of contracts `check_dependencies.py`. Three deps: `sha2-const-stable 0.1.0`; `unicode-normalization 0.1.24` `default-features=false` / features `[]`; `tinyvec 1.13.3` resolved features `["alloc","default"]` with **empty default**. `tinyvec_macros` absent (follow-up: ordinary `macro_rules`, not a proc-macro).

Checked against selected `e6784aa1…`: `cve1_encode` / `cve1_decode` / `_cve1_read` **AST-identical** to historical `7d1c0acf…` (77998 oracle). `admit_capability_manifest` matches **selected** totality (non-dict early return, `strict_unique` skips non-strings, `relationIds[]` type), not the historical function. 774-case `capability-result.json` still records `referenceIsSelected: false`; `reference-selection-binding.json` authenticates the same `e678` bytes later selected at 9/15. History was not rewritten.

## Unicode / Hangul TCB (proposed, not live)

Did **not** rerun the pinned 375273-case Unicode 16 conformance (`f437176a…c33a`, matched). Independently inspected `unicode-normalization 0.1.24` `src/normalize.rs`: three `#[allow(unsafe_code)]` Hangul paths using `char::from_u32_unchecked` after `is_hangul_syllable` / Jamo range checks (`S_BASE=AC00`, `S_COUNT=11172` → **AC00..D7A3**). L/V/T bases match the policy `rangeArgument`. Comments mention block end U+D7AF; the **predicate** is the tighter UAX #15 syllable range. No FFI/OS. Identity itself remains `forbid(unsafe_code)`. Policy records this as **proposed bounded TCB**; this advisory does not convert that into live acceptance or a memory-safety proof.

## Original CVE1 harness depth (preserved)

`codec-oracle-separation-account.json`: initial typed-value hash used OpenSIP **C** canonical encoding, whose lower nesting bound rejected valid CVE1 depths 63/64 and panicked the harness (`initial-json-depth-cve1-result.json`, 11973 mismatches, exit 101). Correction is **test-only** `serde_json` typed serialization. Production codec unchanged. Original failure preserved.

## Independent reproduction

Trusted rustc/cargo **1.95.0**, `--offline`, private `CARGO_TARGET_DIR`. XZ streamed line-by-line (no 27MB/1.2MB buffer of the uncompressed relation-scale kind).

| Check | Result |
| --- | --- |
| 261-file pin + archive | match |
| `cargo test --workspace --all-targets` | **87** passed |
| `cargo test --doc -p opensip-evaluator` (compile-fail) | **1** passed |
| Combined workspace claim | **88** |
| Clippy `--workspace --all-targets -D warnings` | exit 0 |
| CVE1 xz replay | **77998** lines, 5699 accept / 72299 reject, exact text, SHA `d71926c3…5dad` |
| Capability xz replay | **774** parsed JSON, 81 ADMIT / 693 REFUSE, SHA `61e74e0d…09f6` |
| Identity policy 8 profiles × 4 targets | all passed |
| 21 dependency/source bypass probes | all refused |
| Independent codec/capability/graph negatives | **ALL_PASS** |

Did not rerun 375273 NFC conformance.

## Independent negatives

- CVE1: tag 3 vs 7, NFC refuse decomposed, depth 64 ok / 65 bound (not JSON-C 32), trailing/unknown tag, no repair
- Golden identity `508f24c7…`
- OPEN `schemaVersion=99`, language `cobol`, platform `windows-x86_64-msvc` **admit** (not custody)
- Boolean `schemaVersion` → `capability.adm-type:CapabilityManifestV1.schemaVersion`
- Graph fact `payloadClass=relation` still Unsupported
- Policy bypasses: extra features, local substitute, native links, custom-build/proc-macro, root extra feature, Unicode 0.1.25, path escape, unlisted dep, lock checksum, mutated local/extracted sources, symlink, changed archive — all refused

## Findings

**Required:** none relative to the trial’s stated private-candidate standing.

**Should-fix:** none new for this freeze.

**Not findings**

- OPEN scalars and inherited platform-id membership are not product support or release custody.
- Hangul `unsafe` is recorded proposed TCB, not proven memory-safe and not live-selected.
- `tinyvec` version remains a lock+policy pin of upstream `"1"`; policy+lock checksums are the closure used here.
- Selected reference tree does not ship a sibling `capability-manifest-domains.v2.json`; this candidate embeds the pinned `1456ae14…` document. Not a codec defect.
- Diagnostic `StructuralChecks` / framed candidates are not native admission.

## Limits

- Advisory only. Not acceptance of this candidate, Unicode crate live use, M2, or release.
- Did not execute `close_run`, native universe/context, body join, compiler, or complete evaluator replay.
- Graph relation/import/capability-manifest-id remain Unsupported.
- Other Grok continues native-owner integration; root advances the next slice.

## Conclusion

07 adds a bounded CVE1 codec, a private-field capability encoding owner on the selected totality reference, and an exact identity source-policy checker. Vectors and Clippy reproduce. Predecessor relation/closure bytes are unchanged. Lock 9/15 selects `e678`, not this Rust.

**Verdict: NOT ACCEPTANCE.** Prototype matches its standing.
