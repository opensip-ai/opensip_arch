# Rustflags attached long lint reference r1

ACCEPT-DESIGN-UNIT. requiredFindings empty.

This is a separate reference-source copy. It does not reopen the closed rustflags-reference r1 unit or B-S9. Subject manifest `docs/implementation/m3/native-g/rustflags-long-lint-r1-subject.json` is 2629 bytes, sha256 `eb242a6c4e1bc587012ca937b3e4137ae11661f50a0844e263f195b5b42d8375`. All 12 members match. Successor `docs/implementation/m3/native-g/rustflags-long-lint-r1/successor.json` is 2979 bytes, sha256 `4c933e3aaf44009807650b27d26e3857df986b8d7f072bc968fe292dd26a2ff5`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Standing: "PROPOSED separate named attached long lint reference-source branch; no full projector/native qualification".

Product HEAD `60fa3a628dd73a6147b81725c574ce15d520aa15` and architecture HEAD `3e8cab12e90a26b9a8709a3c876c29f75b300701` are the pinned bases. Product is tracked-clean. Architecture is tracked-clean. Its untracked S-OP and E2s drafts stay outside this unit. `~/Library/Application Support/OpenSIP` is absent. Product source and inventory v166 are unchanged. Inventory v166 remains 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. The product lock already names rustflags-reference subject `eb2e56ab9c4c57a2d57bf5476a3c9c6bcf353524800054a4933b9c104447145e` and does not yet name this successor.

## Parents

Both parents match the architecture bytes.

- `docs/implementation/m3/native-g/rustflags-reference-r1/reference/native_evidence_model.v2.py`, 320103 / `4c3f78a9c43102ed391430a9ec8fd84f0d31535a2e0beb366035c14887a8907e`, is the accepted r1 copy. Those bytes are still that file.
- `docs/v2/contracts/product-v1/native-evidence.md`, 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. Section 3.3 names `-A/-W/-D/-F <lint>`, the attached `-A<lint>` spelling, and long forms, with lint syntax `[a-z0-9_:]+`, and `--cap-lints` limited to `allow`, `warn`, `deny`, and `forbid`. The projection carries `executableSelected=false`.

The bound B-S9 model remains 319894 / `4f800faaf75c36ffd38fa9ae0f3618bee1bedbe586026e280326b0d7d73ebca8`. This copy does not rewrite it.

## One branch

The candidate copy is `docs/implementation/m3/native-g/rustflags-long-lint-r1/reference/native_evidence_model.v2.py`, 320342 / `51351b14b5b60ddefeb362832203f0a1613a57fbcf11f43ce0231eaa7579280a`. The only difference from the accepted r1 file is one branch, inserted before the existing `--cap-lints=` branch:

`--allow=`, `--warn=`, `--deny=`, and `--forbid=` take the suffix after the first `=`. A suffix matching the existing `_LINT_RE` (`^[a-z0-9_:]+\Z`) is honored. Any other suffix is stripped with the existing reason `lint-syntax`. The branch consumes one flag. Removing those three lines reproduces the accepted r1 bytes exactly.

`_CFG_RE`, `_LINT_RE`, `_ALLOWED_C`, and `_ALLOWED_C_VALUES` are unchanged. The split long forms `--allow`, `--warn`, `--deny`, and `--forbid`, the attached short `-A`/`-W`/`-D`/`-F` forms, the cap-lints value check, cfg, codegen, and remap handling, their reasons, and `executableSelected: false` stay as r1 left them. No option name, allowed value, reason, schema member, or numeric limit is added. `--allows=dead_code` still falls through to `not-allowlisted`.

The inherited cfg class `[^"\\]*` still matches a space inside quotes. Section 3.3 says cfg values have no spaces. The closed r1 control `--cfg` `feature="a b"` stays honored. That interior-space behavior remains unresolved. Verified remap membership, the carrier, the production collector, and projection bounds stay outside this branch. This review executed only the five AST-selected declarations `_CFG_RE`, `_LINT_RE`, `_ALLOWED_C`, `_ALLOWED_C_VALUES`, and `rustflags_projection`. It did not import the module or run a sibling helper.

## Controls and probe

`evidence/check.py` was not run. It writes `controls.json`, and it loads `native_evidence_model.v2.py` beside itself. That sibling is absent. The candidate is the `reference/` copy. An independent read-only execution of those five declarations, from the accepted r1 file and from this candidate, reproduced every stored row.

`evidence/controls.json` is 45382 / `338121da0929263bfb9a5aaaf5781544474b9e39b79b11da88bdf7884fecc63e`. It records 80 controls, 40 changed counterexamples, `passed` true, `fullRustflagsConformance` false, `productCodeUnchanged` true, and `qualification` false. The 39 `r1-` rows are the closed r1 controls in order, with the same flags and expectations, and both copies still agree. Twelve honored rows are `--allow`, `--warn`, `--deny`, and `--forbid` attached to `dead_code`, `clippy::all`, and `unused_variables`. Twenty-four malformed rows are the empty suffix, `Dead_Code`, a trailing newline, an interior space, a hyphen, and `dead_code=extra`, each disclosed as `lint-syntax`. Four ordered rows keep `@args` as `response-file` and still honor the following `--cfg=feature`. The lookalike `--allows=dead_code` stays `not-allowlisted` on both copies.

`evidence/primary-probe.json` is the supplied local record: rustc 1.95.0 Homebrew accepts `--allow=dead_code`, `--warn=dead_code`, `--deny=dead_code`, and `--forbid=dead_code` against the owned public `#![no_std]` source in `public-probe.rs`, each with exit 0. `qualification` is false. This review did not run `primary-probe.py` or rustc. The record is spelling evidence for those four option names. It is not a toolchain, context, or provider qualification.

Integration is exact root assent and `verify_design`, then an architecture commit and a separate product lock commit. Nothing is pushed. The record does not grant Coverage, a provider launch, Plan, Run, or product qualification.
