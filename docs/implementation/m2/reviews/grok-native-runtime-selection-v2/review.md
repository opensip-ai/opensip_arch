# Independent Grok review: native-runtime-selection v2

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Verdict: ACCEPT-DESIGN-UNIT**
**subjectManifestSha256:** `6a761425a60f1e6145a8b4f9edb60af0ac40468f0514cb19397c4ad05dfa0a97`
**requiredFindings:** none

Bounded composed runtime unit: retained 01–06 primitives, CVE1/capability/source-policy 07, Plan + Rust/syntax contexts 08, TypeScript + Unicode 15 FULL default lowercase 09, plus explicit identity production TCB. **Not** complete M2, native execution, universe/Plan/Run/replay, Syntax-10, custody/publication, or release. Root assent and private activation remain required before install. Live lock **10/15** does not itself accept these 35 inputs.

## Custody

| Manifest | Bytes | SHA-256 | Members |
| --- | ---: | --- | ---: |
| Selection `native-runtime-selection-v2-subject.json` | 25067 | `6a761425…0a97` | **110/110** |
| Implementation `trials/native-runtime-02/subject.json` | 46356 | `68a9e7b6…9d08` | **254/254** |
| Implementation archive | 1959435 | `7e735189…7bff` | pin match |

Successor parents (sorted) pin admission-runtime `0a3c2694…`, capability-totality `6421e727…`, exact-schema-profile `fe1ebd49…`, inventory-v12 successor `00089f89…`, recognition-derived `4b771e6e…`, inventory v12 `dd2ad2da…`. Successor candidates **109** = subject files minus `successor.json`. Materialization map **35/35** exact vs selection product and implementation product. All **21** inventory-12 added paths are among those 35; the other 14 are modified existing files.

Live lock **10 inventory / 15 contract** (last inventory `native-owners-inventory-v12/successor.json`, last contract `capability-totality-reference-selection-v1/successor.json`). Frozen 09 was **9/15**. Candidate `design-lock.json` **byte-equals live** `e1282724…9f0d` and is **not** a code accept. Generation `registry.json` 40 and `source-map.json` byte-equal live. Admission registry **48** sources / **15** aliases verified by `verify_design` on the candidate product against the live 10/15 lock (`executedRuntimeCode: false`).

Work stayed under `/tmp/opensip-implementation/m2-grok-native-runtime-selection-v2-review/review`. Frozen/live/history not edited. Isolation receipts keep original `/tmp/...-isolation-02` paths; this review used a private copy and checked receipt source pins against that copy.

Archived 09 advisory `17370708…4f5d` (requiredFindings none) is pinned. Inventory-12 `aa458656…` is already accepted (369 files, 20 packages, 21 new paths). Syntax-10 is not in this unit.

## Scope (code, not packaging)

Identity remains `#![no_std]` + `forbid(unsafe_code)`. Public surface is retained candidates and diagnostic `StructuralChecks` / framed candidates over supplied immutable objects/blobs. Immutable **48** sources and **15** aliases unchanged. Generation **40** unchanged. General graph relation/import/capability-owner joins remain `Unsupported` (`payload-class owner joins`, `capability derivation`, `relation body identity owner`) in `closure.rs` **byte-identical** to 08/09 (`a6dc8b89…`).

Evaluator is pure and depends only on identity. `CapabilityManifest` fields are private (compile-fail doctest). `admit_plan_capability` checks `CAPABILITY_BYTES_JOIN` **before** selected `e678` gates; malformed bytes + wrong ID is `BytesJoin` (independently reproduced; golden identity `508f24c7…`). `inspect_native_context` covers Rust, syntax, and TypeScript over **closure descriptors** only: identity/kind/tools/grammars/lib. One retained frame blob is not member-blob proof. Caller ADMIT is not authority. Host production graph is unchanged; evaluator is **dev-only**. Provider remains honest `native analysis is not implemented`.

Product vs frozen 09: **226/226** overlapping product files byte-identical **except** `design-lock.json` (9/15 → live 10/15). `Cargo.lock` is unchanged (`4aae31ea…`). Live tree still lacks `unicode_case.rs` (not installed).

## Identity production TCB (explicit accept)

Requested exact production closure, independently re-checked (not inferred from advisories):

| Crate | Version | Features | Archive SHA-256 |
| --- | --- | --- | --- |
| `sha2-const-stable` | 0.1.0 | `[]` | `5f179d4e…1ed9` |
| `unicode-normalization` | 0.1.24 | `[]` (default-features=false, UCD **16**) | `5033c97c…d956` |
| `tinyvec` | 1.13.3 | `[alloc, default]` with **empty** default | `fd3ca314…f0ee` |

`check_identity_dependencies.py` + `dependency-policy.json` (`58399e31…4520`) pin versions, resolved features, crate archives, extracted source census, and 13 local identity sources: **110** files. No build/links/proc-macro/unlisted targets/deps. **8** host/provider × 4 target profiles all `sourceFilesVerified: 110`. Independently refused extra features, unlisted dep, Unicode 0.1.25 policy mismatch, checksum change, extra local source, root extra feature.

`tinyvec_macros` **package absent** from cargo metadata. 1.13.3 retains an empty feature of that name and no longer depends on the crate (changelog; `Cargo.toml` has no `tinyvec_macros` dependency). Earlier false proc-macro claim remains corrected history (`followup-account.json`), not rewritten.

Guarded Hangul `char::from_u32_unchecked` in pinned `unicode-normalization-0.1.24` `src/normalize.rs` **8074** `e6bb470e…fbb6`: syllable `AC00..D7A3` (not the looser D7AF block comment); L `1100..1112`, V `1161..1175`, T `11A8..11C2`; LV ≤ `D788`; LVT ≤ `D7A3`; every output **< D800**. Own-crate `forbid(unsafe_code)` is not transitive and is **not** a memory-safety proof. This unit’s accept is those exact bytes/features as bounded pure external TCB.

Unicode **15** FULL default lowercase is a **separate** owned evaluator table (`6012d5ee…`, generator `--check` reproduced from three official UCD15 pins + LICENSE). Final_Sigma on the original string; Case_Ignorable precedence; no tailoring/casefold/NFC/std17. Selected `e678` `UNICODE_CASE_DATA_VERSION = "15.0.0"` is **not** rebound. Distinct from NFC16 and rustc std17 (U+1C89 identity here; std lowercases it).

## Historical freeze accounts (preserved, not defects)

`freeze-preparation-account.json`: first selection-manifest attempt used the wrong inventory-12 successor filename; **no frozen member changed**; continuation used accepted `native-owners-inventory-v12/successor.json`.

`frozen-source-check.json`: an extra provider test was run against frozen 09 source; new target/logs moved out; **all 270 frozen 09 members unchanged**. Isolation exports are separate.

Isolation harnesses retain original absolute `/tmp` paths. This review did not mutate them.

## Reproduction (private copy)

Trusted rustc/cargo **1.95.0**, `--offline`. Python reference env `-I -B`. Did **not** rerun 07 CVE1 77998, 08 Plan 783 / 1197, or 09 1 112 064-scalar corpora: those sources are byte-identical and already independently reviewed.

| Check | Result |
| --- | --- |
| 110-file selection + 254-file implementation + archive | match |
| 09 product vs this unit except `design-lock.json` | **226/226** identical |
| generator `--check` | 0 |
| `cargo test --workspace --all-targets` | **93** |
| evaluator compile-fail doctest | **1** → **94** |
| Clippy `--workspace --all-targets -D warnings` | 0 |
| identity policy 8×4 profiles | 110 sources each |
| 7 independent policy refusals | all refused |
| package edges host + rust-provider | passed; evaluator→identity; host **dev**→evaluator |
| `verify_design` live 10/15 | passed; generation 40; admission 48 / aliases 15 |
| contracts `check_dependencies` | passed (separate lane) |
| composition probe | **ALL_PASS** (TS/Rust/syntax one-blob, Plan BytesJoin, Unicode15 vs std17, Unsupported literals) |
| CLI help/version | success; help catalogue unchanged |
| host isolation receipt 108 sources / 18 archives vs copy | 0 missing / 0 mismatch |
| provider isolation receipt 25 / 14 vs copy | 0 missing / 0 mismatch |
| Hangul range + `tinyvec_macros` absent | pass |

## Limits (not waived)

Not complete M2. Not native execution / universe binding / Plan selection / full Run / evaluator replay / `ReplayedRun`. Not every closure member blob. Not Syntax-10. Not A06 custody/publication or M3–M6. Isolation exports are development-lane evidence with trusted compiler/SDK/loader, not hermetic OS qualification. Hangul accept is bounded TCB, not a memory-safety proof. After root assent, private activation must materialize the **35** map files; do not treat live 10/15 preflight as that install.

## requiredFindings

[]
