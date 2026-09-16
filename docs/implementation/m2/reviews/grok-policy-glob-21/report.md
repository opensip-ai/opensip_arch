# Frozen trial review: policy-glob-21

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private pure `portable_glob_match`. **Not runtime selection. Not reference-unit acceptance. Not policy admission/compilation, predicate address lookup, Run, or replay.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-policy-glob-review-21/review`. Live, frozen, and history not edited. No commits.

Proposed predicate-matching-reference-selection-v1 (`04bf748e…c463` / 1842) is under **separate** formal review and is **not selected**. This source review does not accept that reference and does not install glob into live runtime.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/policy-glob-21/subject.json` | 50345 | `f478f097dd7b687eab675d61967394d975eefe99bcd17bb72a6231ec17229fd4` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 3817467 | `0b3c10121470204d877364a1e25615c38d9c891ece87a46f26d010ded5ef3224` |
| adjacent `glob-result.json` | 305 | `18075f7113efd50caf2c4f910c0df7e06ab45195106703f0716e03fd192ed891` |
| adjacent `initial-literal-star-law-mismatches.json` | 507 | `2161474bd1a4520a15d050672335bfd0d7d679f03e5ea47ca0cbe90ebb4a9245` |
| export | `/tmp/opensip-implementation/m2-policy-glob-subject-21` | 280/280 member pins match; tar 280/280; 0 extra; 0 missing |

280 `files[].path` values are unique and string-sorted.

Dependency pins hash-match: frozen run-links-19 `4177e1c0…8c74`; proposed reference subject `04bf748e…c463`; proposed `workflows_model.v1.py` `1d5212d5…9874` / 142828; glob-pattern-contract.v1 `9b12ef44…8ba0` / 3946.

Live lock independently **17 inventory / 22 contract** (`7b2e1d8c…eb64` / 51424). Last inventory **candidate** remains v19; last contract is runtime **v9**. Live tree has **no** `crates/evaluator/src/policy.rs`. Proposed predicate-matching successor is **not** a live contract.

## Source delta vs frozen Run-19

**239** prior product files byte-identical to frozen run-links-19, including identity `closure.rs`, identity source-policy, `run_links.rs`, prior runtime bodies, `Cargo.lock`, and `design-lock.json`. No new crate dependency. External TCB unchanged.

Changed: `lib.rs` export only. **New production body:** `policy.rs` only.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `product/crates/evaluator/src/policy.rs` | 4457 | `8fb940c7cd6b20593e6bd99fcd34b286814b35d208ecea71fd4ebe3a2f4a2bf9` |
| `product/crates/evaluator/src/lib.rs` | 1763 | `9c08b56f5817d3f5a6356da402150f7d253c8ebe2f9e8e838a037e91005b2429` |

## Law vs glob-pattern-contract.v1 and proposed `glob_match`

Pure `portable_glob_match(pattern, candidate, work) -> Result<bool, GlobMatchError>`. Schema / LogicalPath / GlobPattern admission remain caller-owned. No I/O, case-fold, Unicode normalization, brace/bracket expansion, or escape syntax. Split on every `/`, preserving empty segments. Ordinary `*`/`?` stay inside one segment (`?` = one Unicode scalar, not a grapheme or byte). A segment that is exactly `**` matches zero or more **whole** segments, including a final filename. `a**b` is ordinary and cannot consume `/`. Brackets and braces are literal. Dotfiles are not excluded. `steps`/`work` exhaustion is `GlobMatchError::Limit`, distinct from `Ok(false)`. Local work is not evaluator full-scan budget.

DP walks pattern segments in reverse; ordinary segments use greedy scalar matching. The `*` equality bug is corrected: a pattern star is **not** consumed as a literal against a candidate `*` before the star-backtrack position is recorded (`pattern[i] != '*' && pattern[i] == candidate[j]`), matching the proposed successor `seg_match` (`1d5212d5…9874`) and the contract that `*` matches zero or more scalars **including** U+002A.

History preserved, not patched: initial selected-reference helper `be37023f…66dc` consumed literal `*` via equality first. Initial corpus **31592** used candidate alphabet `ab/` (no `*`/`?`); it passed the old helper. Root four false negatives independently confirmed (`*a`/`*ba`, `a*b`/`a*xb`, `**a`/`**ba`, `*?`/`*ab`): old `false`, contract/proposed/this source `true`. Initial `policy.rs` / requests / expected / actual / `glob-result.json` remain in the export. Counterexample list is byte-identical to the proposed-reference evidence pin `2161474b…9245`.

This file does **not** admit or compile PolicyDocument, look up predicate addresses, or join a Run. Inventory v19 still describes `policy.rs` as a **compiler**; this trial is the glob predicate only.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- Independent recursive contract law vs extracted proposed `glob_match` AST: **610310** match pairs (length 0..4 over `ab*?/` plus Unicode/literal extras), **0 mismatch**.
- Frozen `glob-expected.ndjson` / `glob-actual.ndjson` vs that same proposed AST: **610313/610313**, including **3** typed `work=0` Limit rows, **0 mismatch**.
- Four root false negatives and **30** normative unit cases (literal-star controls, `**/*.ts`, empty-segment `a//b`, combining-acute `?`, literal `[ab]`/`{a,b}`, trailing slash) match contract + proposed; `cargo test --locked --offline -p opensip-evaluator portable_glob --lib` ok (each unit row also asserts `work=0` → Limit). Extra corners (`***`, `**/**`, `**/` vs `a`, empty strings, NUL/backslash as data) match.
- Identity policy independently passed: `sourceFilesVerified: 110`. Frozen workspace sums to **105**. Independent `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` Finished.

Did not rebuild the retained-graph harness and re-pipe 34 MiB `glob-requests.ndjson`. Did not re-exec Unicode-15 or 07–12 corpora.

## requiredFindings

None.

## Limits (not required findings)

- Local `Ok(true)` is not policy admission, compilation, predicate-address lookup, `close_run`, or ReplayedRun.
- Proposed predicate-matching-reference-selection-v1 is **not selected**; matching it here is not reference-unit acceptance.
- Inventory `policy.rs` compiler/admission work remains unimplemented.
- Local `work` budget is not evaluator full-scan proof budget; Limit ≠ false.
- Pattern/path schema admission is not this function.
- Live runtime v9 does not install these bytes.
- Did not re-pipe the 34 MiB request corpus through a rebuilt harness.

## Verdict

No required findings. Private `portable_glob_match` matches glob-pattern-contract.v1 and the proposed (unselected) `glob_match` successor, preserves the initial literal-star failure history, and does not mint policy, addresses, or a Run. Not a live/runtime/reference selection.
