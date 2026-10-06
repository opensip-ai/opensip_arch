# Rustflags reference exact-value and end anchors r1

ACCEPT-DESIGN-UNIT. requiredFindings empty.

This is a separate reference-source copy. It does not reopen the closed B-S9 unit. Subject manifest `docs/implementation/m3/native-g/rustflags-reference-r1-subject.json` is 1762 bytes, sha256 `eb2e56ab9c4c57a2d57bf5476a3c9c6bcf353524800054a4933b9c104447145e`. All eight members match. Successor `docs/implementation/m3/native-g/rustflags-reference-r1/successor.json` is 2139 bytes, sha256 `1b3b4be7655bf3b63eb257a310545b579e3c5d376363ef0648cb6911a40d8601`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Candidates are the other seven members, with the manifest pins. Standing: "PROPOSED separate Rustflags reference-source exact cap-lints value and terminal-anchor follow-up; no complete projector/product qualification".

Product HEAD `610941f33ceb68b7ce9aca4340b59003364a397d` and architecture HEAD `c2f5d11a09595dc8783e96383b6ef7a1700b369a` are the pinned bases and are tracked-clean. The new reference path is not tracked. Product source and inventory v166 are unchanged. Inventory v166 remains 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, the last inventory successor.

## Parents

Both parents are already accepted, and the architecture bytes match the pins.

- `docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py`, 319894 / `4f800faaf75c36ffd38fa9ae0f3618bee1bedbe586026e280326b0d7d73ebca8`, is a candidate of the bound b-s9 successor. That accepted file is still those bytes.
- `docs/v2/contracts/product-v1/native-evidence.md`, 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`, is a design-lock input. Section 3.3 is the rustflags allowlist.

The candidate copy is `docs/implementation/m3/native-g/rustflags-reference-r1/reference/native_evidence_model.v2.py`, 320103 / `4c3f78a9c43102ed391430a9ec8fd84f0d31535a2e0beb366035c14887a8907e`. Reversing the four sites in `evidence/prepare.py` reproduces the parent bytes exactly. `prepare.py` was not run.

## Four source sites

Native evidence §3.3 honors `--cap-lints` only for `allow`, `warn`, `deny`, and `forbid`, cfg values with identifier syntax and no spaces, lint names `[a-z0-9_:]+`, and eight codegen options whose values match `[A-Za-z0-9_+,.=-]`. The projection carries `executableSelected=false`.

The parent inline branch honored every `--cap-lints=` suffix. The candidate separates that branch from the attached `-A`/`-W`/`-D`/`-F` lint branch. The suffix must be one of those four strings. Any other suffix, including empty, `other`, `ALLOW`, and `allow` plus a trailing newline, is stripped with the existing reason `cap-lints-value`. The split `--cap-lints` form already used that tuple and that reason, and it is unchanged.

`_CFG_RE`, `_LINT_RE`, and `_ALLOWED_C_VALUES` keep their character classes and change only the terminal `$` to `\Z`. In Python, `$` also matches before one trailing newline; `\Z` matches only the end of the string. A trailing newline on a cfg value, a split lint name, or a codegen value now fails the existing syntax or allowlist reason. An attached lint whose body fails `_LINT_RE` still falls through to the existing `not-allowlisted` reason. `_ALLOWED_C` stays the eight names `target-feature`, `target-cpu`, `opt-level`, `debuginfo`, `panic`, `overflow-checks`, `debug-assertions`, and `strip`.

No other line differs. The copy does not add a pattern family, option, reason, schema, wire member, or numeric limit. The accepted B-S9 file is not rewritten.

The inherited cfg class `[^"\\]*` still matches a space inside quotes. Section 3.3 says cfg values have no spaces. That interior-space behavior is unchanged on purpose: both the parent and the candidate honor `--cfg` `feature="a b"`. Long attached lint spellings and verified-path or carrier admission stay outside this copy. The whole inherited model is carried with these four edits. This review did not import or execute the module; sibling helpers are not claimed runnable, and the copy is not a full rustflags conformance claim.

## Controls

`evidence/check.py` was not run. It writes `controls.json`, and it loads `native_evidence_model.v2.py` beside itself. That sibling is absent. The candidate is the `reference/` copy. An independent read-only AST execution of the same five declarations — `_CFG_RE`, `_LINT_RE`, `_ALLOWED_C`, `_ALLOWED_C_VALUES`, and `rustflags_projection` — from the parent file and from that candidate reproduced every stored row.

`evidence/controls.json` is 20561 / `a3de82883daae41eb25a3ac3f2cda2e165c1c53574d4dcbf53fdcde6d299c939`. It records 39 controls, 11 parent counterexamples, `passed` true, `fullRustflagsConformance` false, `productCodeUnchanged` true, and `qualification` false. The 11 changes are the four invalid inline cap-lints values, the six trailing-newline cfg, lint, and codegen values, and the ordered disclosure whose `--cap-lints=other` is now `cap-lints-value`. Named cap-lints values, invalid split forms, ordinary cfg, lint, and codegen syntax, response files, unknown flags, dangling arguments, verified remap membership, and `executableSelected: false` stay as the parent behaved. The interior-space control remains honored and unchanged.

`~/Library/Application Support/OpenSIP` is absent. Integration is exact architecture-source assent and `verify_design`, then an architecture commit and a separate product lock commit. Nothing is pushed. The record does not grant Coverage, `NativeContextVerified`, a provider launch, Plan, Run, or product qualification.
