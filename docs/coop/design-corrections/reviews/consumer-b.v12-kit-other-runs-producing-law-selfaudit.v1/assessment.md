I'll continue the same kit-only origin: copy the checker first, then audit whether the Rust/syntax-data FULL_ADMIT and complete-bundle claims actually cover the producing laws.I'll freeze the original checker as source, copy it for edits, then read the four producing-law contracts in full.Checker is frozen. Next I’ll read the four producing-law contracts in full and map each required join against what the original checker actually executed.I'll add producing-law checks the original FULL_ADMIT skipped: independently derived extents, membership coverage, selectedRefs totality, and complete proof C-equality.**Successor scoped verdict remains `FOUR_RUNS_REFUSED`.** The original Rust `FOUR_RUN_FULL_ADMIT` is withdrawn. Original findings are not waived. This is not whole-consumer acceptance.

COMPLETE49’s “full-bundle comparison” was a selected-field projection (`verdict`, `witnessDigest`, sorted cause pairs) and it copied claimed proof locators into the computed proof. Composition §7 requires `C` of the complete proof plus reminted evidence/seal/run. Enumeration never independently derived membership snapshot cover or file extents; claimed `KindExtentV1` certified itself.

| Run | Original | Successor first refusal | producing | semantic | proof `C` |
|---|---|---|---|---|---|
| TypeScript | REFUSED import producer=`adapter` | **preserved** | notReached | DIAGNOSTIC | true (diagnostic) |
| Rust complete | **FULL_ADMIT withdrawn** | membership rows miss `#/Cargo.toml`, `#/a/Cargo.toml`, `Cargo.lock`; inventory file extent is only `lib.rs` vs four snapshot paths | REFUSED | DIAGNOSTIC | **true** (not admission) |
| Syntax data | FULL_ADMIT *basis* withdrawn | none on successor C-path | PASS | PASS | **true**, reminted `run3:ab1d6fc4…` matches |
| Rust partial | REFUSED rule outcome | **earlier** same membership/extent producing join; diagnostic `C(ruleResults)` still mismatches | REFUSED | DIAGNOSTIC | false |

Rust diagnostic proof-`C` equality with a matching reminted Run ID is the trap the producing laws forbid: a matching proof over unadmitted extents/membership.

Syntax-data is re-admitted only after reconstructing `selectedRefs`, deriving clones-fact `partial` from unknown Coverage, and putting cell inventory digest `3148550880…` on `executionDeficiencies.inputRefs`. The original method would have hidden that field.

Deliverables under the self-audit output: `other-runs-producing-law-selfaudit.md`/`json`, successor `other-runs-full-review.md`/`json`, `inventory/`, frozen `checker-original/` + `history/checker-pathdiff.txt`.
