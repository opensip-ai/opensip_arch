# Independent Grok advisory: native-case-09

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Frozen-trial advisory. **Not runtime selection. Not ACCEPT-DESIGN-UNIT. Not M2 complete. Not full native closure. Not ReplayedRun. Not inventory-12 acceptance.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-native-case-review-09/review`. Live product, frozen history, and commits were not edited.
**Prior:** native-owners-08 advisory `59443064…7d90` (requiredFindings none). Unicode-case-owner-01 `96de4c76…5ae2` (fold bound **15.0.0**, no rebind). Lock remains **9/15**; this candidate is not a lock successor. Inventory-12 `aa458656…f057` is a separate formal review and is **not** accepted code or deps.

## Standing

Private TypeScript native-context branch plus Unicode **15** FULL default-lowercase owner on reviewed08. Identity codec/closure/relations and `Cargo.lock` are unchanged. Evaluator still depends only on identity; host **dev-depends** on evaluator. Context checks inspect closure **descriptors**, not member blobs, and still do not claim universe/Plan/Run/replay. Selected native `e678` `UNICODE_CASE_DATA_VERSION = "15.0.0"` is **not** rebound. NFC remains unicode-normalization **16.0.0**. rustc 1.95 std lowercases Unicode **17** assignments that UCD15 leaves unassigned.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 48220 | `6290b55b05a4c1a70f3edacf6e4efccc64cd4ad8c49b841b8acb69f9738087d6` |
| `subject.tar.gz` | 2324106 | `e6778f33daa2e087052fd2ed20e5c7a1a7509e6e122dc810e4cc5ccc2e767a5b` |
| Files | 270 | 0 missing / 0 mismatch (targets excluded) |
| `native_context.rs` | 15809 | `c16fe03d2693bf376ca90fabcbf115f986efd6df6e33724f3a074ade3c2e8a2e` |
| `unicode_case.rs` | 2757 | `c04c71a0e7cda370e87f44fb599f743e60fee565330e9f8b333f1d858523d0ab` |
| `generated/unicode_case_tables.rs` | 49680 | `6012d5ee0506a70947418e2ec828506a062e3f23be1b0090432a668d47e13e0a` |
| `native-context-registry.json` | 2592 | `269f25c1eb66f6cf31fc244c00ba3ee6f06b895d6b2e8ce1e4052071e1c7dd0a` |
| `capability-registry.json` | 16522 | `1456ae1476dfe1b0f3b1134c9d7a36e35890e45e20f57e7bbc2b7ada2144aef6` |
| identity `capability_codec.rs` / `closure.rs` / `relations.rs` / checker / `plan_capability.rs` / `Cargo.lock` | — | **byte-identical to 08** |

Copied product lock **9/15**. Archive pin adjacent matches. Frozen root `/tmp/opensip-implementation/m2-native-case-subject-09` 270/270.

## TypeScript native context

`inspect_native_context` still rehashes/shape-admits the registered H-frame, then Rust/syntax **and TypeScript** over retained closure descriptors. 08 returned `Unsupported("Unicode15 full lowercase owner")` for `native.context.typescript.v2`. 09 runs the TS arm:

- stdlib closure analog of rust-dev (`toolchain.typescriptStdlibMerkleRoot`, kind `stdlib`)
- Unicode15 FULL default lowercase of `libSelection` / honored `lib`
- duplicate-fold and unsigned-UTF-8 order
- complete `.d.ts` inventory vs `standardLibraryComponentDigests`
- ambiguous basename, tree digest mismatch, `lib-not-retained`
- compiler/runtime/package membership and manifest version agreement

`work=0` is still `Limit`, not unretained. One retained frame blob is enough for these owner checks; that is **not** member-blob proof. Numeric `libSelection` fails **frame schema** (`Frame(Schema(Mismatch))`), not a typed lib refusal and not `CaseDataUnavailable`.

## Unicode 15 FULL default lowercase

`unicode_case::lowercase` is crate-private. Tables `VERSION = (15,0,0)`. No `std` lowercase, no NFC, no casefold, no locale tailoring, no `unsafe`. Two linear passes over the **original** character sequence:

1. reverse: following non-ignorable Cased, with **Case_Ignorable precedence** on Cased∩Case_Ignorable overlap (267 code points in UCD15, including U+0345)
2. forward: Final_Sigma U+03A3→U+03C2 iff preceding Cased and not following Cased; else sparse FULL `LOWER`; else identity

Generator `tools/generate_unicode_case.py` is offline developer tooling, not `build.rs`. It pins three official Unicode 15.0.0 files, refuses unknown default contexts (only `Final_Sigma` on U+03A3), ignores `tr`/`az`/`lt` (15 tailored rows), and `--check` reproduces the committed tables byte-for-byte.

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `UnicodeData.txt` | 1913704 | `806e9aed65037197f1ec85e12be6e8cd870fc5608b4de0fffd990f689f376a73` |
| `SpecialCasing.txt` | 16832 | `78b29c64b5840d25c11a9f31b665ee551b8a499eca6c70d770fcad7dd710f494` |
| `DerivedCoreProperties.txt` | 1053943 | `d367290bc0867e6b484c68370530bdd1a08b6b32404601b8c7accaf83e05628d` |

LICENSE Unicode V3 retained under `tools/unicode/`. Table-version mismatch is `CaseDataUnavailable` / `NativeContextError::CaseDataUnavailable` — environment failure, not a lib-selection refusal. Distinct from NFC16 and rustc std17: U+1C89 / U+A7CB / U+10D50 identity here; rustc 1.95 `to_lowercase` maps them.

## Packaging-only renames

Kebab JSON, `generated/` tables, and `unicode-v15` data directory. Registry **bytes** equal 08 underscore names (`269f25c1…`, `1456ae14…`). `capabilities.rs` hash changes only because `include_bytes!("capability-registry.json")` (same 15116-byte file, kebab path). Metadata and semantics preserved. Final renamed-source harness output is byte-identical to prior actual for both corpora.

## Initial TypeScript fixture inventory (preserved)

`initial-ts-fixture-inventory.stderr` records `FIXTURE_NATIVE_UNIVERSE:native.universe-path-not-inventoried:a.ts` plus `tsconfig*.json` source-mismatch **before** any owner comparison. Complete `TS_SOURCES+a.ts` inventory was then supplied. Not a runtime fix. Original stderr retained.

## Independent reproduction

Trusted rustc/cargo **1.95.0** Homebrew, `--offline`. Python **3.12.13 / UCD 15.0.0** is the case oracle (`/Users/sb/.local/bin/python3.12`). Ambient Python 3.14.6 / UCD 16.0.0 was not used. XZ streamed with reader-thread drain. No 07 CVE1 / 06 overlay rerun.

| Check | Result |
| --- | --- |
| 270-file pin + archive | match |
| generator `--check` | exit 0, tables identical |
| `cargo test --workspace --all-targets` | **93** |
| evaluator compile-fail doctest | **1** → **94** |
| Clippy `--workspace --all-targets -D warnings` | exit 0 |
| case15 xz | **1112064** scalars digest `a005fb39…de68` + **31434** strings, 0 mismatch, identical to final-actual |
| independent Python 3.12 scalar digest | same `a005fb39…de68` |
| native-context xz | **1867**, 262 checked (TS 103 / syntax 86 / rust 73), 130 native-refused, 0 mismatch, identical to final-actual |
| independent algorithm vs Python 3.12 samples | 0 mismatch (overlap, Final_Sigma, tailoring ignored, unassigned-in-15) |
| independent negatives | **ALL_PASS** |

## Independent negatives

- Final_Sigma on original context (word-final, medial, after digit, before period, U+0345 overlap, long ignorable run)
- FULL mapping of U+0130 → `i`+U+0307, not Turkish `i`; I+acute is not Lithuanian
- ß stays ß (not casefold); U+1E9E → ß (not `ss`); U+FB03 stays the ligature
- U+1C89/U+A7CB/U+10D50 identity vs rustc 17 divergence; U+10400 → U+10428
- TS positive with **one** retained frame blob
- `libSelection` number → frame schema mismatch, not a lib refusal
- compiler digest not in toolchain closure; `scripthost` `lib-not-retained`; extra `.d.ts` `stdlib-inventory-incomplete`; `İ` full-case not retained

## Findings

**Required:** none relative to the trial’s stated private-candidate standing.

**Should-fix:** none new for this freeze.

**Not findings**

- Context diagnostics without member blobs are the stated subset, not full native ADMIT.
- Packaging kebab / `generated/` / `unicode-v15` preserve registry bytes and table semantics.
- Inventory-12 is another review; kebab names here do not accept that successor.
- Initial TS fixture inventory failure is fixture-universe preparation, not a production patch.
- `CaseDataUnavailable` is an environment gate, matching selected `e678` `ReferenceEnvironmentError`.
- rustc std / Python 3.14 UCD16 must not supply the fold; they were shown to diverge and were not used.

## Limits

- Advisory only. Not acceptance of 09, 08, native ADMIT, M2, inventory-12, or release.
- Did not execute `close_run`, universe binding, body identity, complete evaluator replay, or member-blob authority.
- Did not rerun 07 CVE1 77998 or relations-06 giant corpora. 08 Plan 783 remains prior evidence.
- Graph owner joins remain Unsupported (not re-executed this slice).
- Hangul `from_u32_unchecked` remains proposed TCB on the identity NFC16 path, unchanged.
- Root prepares runtime unit selection later. `UNICODE_CASE_DATA_VERSION` stays **15.0.0**.

## Conclusion

09 adds the TypeScript native-context owner and a closed Unicode 15 FULL default-lowercase implementation generated from three pinned official sources. Selected `e678` constant 15 is preserved and kept distinct from NFC16 and std17. Vectors, generator `--check`, 94 tests, and Clippy reproduce. Final renamed-source harness output is byte-identical.

**Verdict: NOT ACCEPTANCE.** Prototype matches its standing.
