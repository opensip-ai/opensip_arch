# CODEX2 Review — CLI creator source-guard repair r3

## Verdict

**ACCEPT-UNIT**

## Finding dispositions

`CLI-GUARD-R2-RF-1` is resolved. `logging_adapter_is_single_top_level` removes from its working copy only complete lines exactly equal to one of the four accepted built-in attributes, then rejects every residual `#` byte. Every Rust attribute contains that token, so whitespace, newline, line-comment, block-comment, and multiline separation between `#` and `[` cannot evade the fence. Extra exact occurrences of the four allowed attributes do not introduce name generation: they only apply the existing `cfg` or `allow` behavior to source that remains visible to the other textual checks. Residual occurrences of the accepted prefix identifiers `cfg`, `allow`, `forbid`, `doc`, and `compile_error` are also refused, preventing a later item from rebinding the pinned prefix macro or reusing those spellings outside the accounted lines.

The new controls exercise space-, newline-, line-comment-, and block-comment-separated attribute forms, the existing contiguous `macro_use` form, and a later `compile_error` import. The residual-hash mutation compiles and is caught at the earlier `#[macro_use]` assertion. This is sufficient even though the witness precedes the separated forms: disabling the only residual-hash condition admits that contiguous unapproved attribute, proving the condition is observed, while the positive source independently executes every separated-form assertion.

`CLI-GUARD-R1-RF-1` remains resolved. The exception still requires exactly one complete adapter at the offset after the exact accepted comment-stripped top-level prefix and immediately before the next known export, and removes only that occurrence. The remainder refuses further `opensip_operability` identifiers, glob tokens, macro tokens, and unapproved attributes. The locked offline Cargo metadata predicate still follows the intended host resolve node, requires exactly one dependency binding named `opensip_operability`, and binds the selected operability package, its manifest and library source, and the host manifest and library source to the intended canonical worktree paths. Duplicate, nested, alias, module, glob, macro, missing-binding, same-name bridge, renamed-binding, alternate-root, altered-adapter, raw-identifier, and appended-storage controls remain present.

## Authority ruling

Existing X11 and accepted S-OP-2 PROPOSAL-r6 remain sufficient. X11 requires creator, ordinary-writer, gate, pack-admission, recovery, and storage-commit authority to remain absent from the CLI and host ingress. S-OP-2 separately authorizes the accepted optional-logging finalizer. This test-only predicate distinguishes those existing duties and selects no new creator, storage, logging, command, or production behavior.

## Frozen subject and evidence

The requested `subject.json` SHA-256 is exact: `de6cecb4163c62382417cb3586ef95faebe6a70a5bb01e9a68dc6c9d461cda11`. All 174 declared members are present, every declared byte count and SHA-256 matches, and there are no extra frozen subject files. The full rejected r2 package, including rejected r1, is preserved by value. The candidate is byte-identical to the named worktree file, its parent is `ca6f5be9ded80c50a143b2f219258c95c80db2e6`, and that worktree has only the declared existing test-file change. The architecture checkout is at the declared `278d1a27b4cea095b37eed09e7109d8a98be7696`. All frozen product and architecture authority files equal their corresponding live pinned files. `product-map.json` records one existing path, zero new paths, no production changes, and candidate SHA-256 `094bd17bf38bc771ebec281d78bce52e6791cf82121dddfd4ab643c154ac00b9`.

Fresh owning-r7 records both affected exact tests and all-target CLI Clippy passing. Each of the three mutations compiled and failed at its declared runtime witness; after each mutation the candidate hash was restored and both controls passed freshly. The r6 driver failure is accurately preserved as a witness-expectation mismatch after the guard had already caught the mutant, and r7 reruns the same source with the corrected expected witness. No compilation failure is counted as a catch.

The original six command/refusal/catalogue/effect bodies, other forbidden-name checks, and security ownership and visibility assertions remain parent-exact. This acceptance covers only the frozen test-only source unit. It does not establish integration, inventory/hash binding, status reconciliation, full CLI or workspace qualification, product qualification, or any Rust3 work.

## Required findings

None.

## Non-blocking observations

None.
