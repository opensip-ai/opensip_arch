# CODEX2 Review — CLI creator source-guard repair r2

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### CLI-GUARD-R2-RF-1 — Make the post-adapter attribute fence recognize Rust token separation

`logging_adapter_is_single_top_level` does not enforce its stated rejection of every unapproved attribute below the adapter. At `apps/cli/tests/creator_commands_tests.rs:514-525`, it trims each line and examines only lines whose text starts with the contiguous bytes `#[`. Rust attributes are tokenized as `#` followed by `[` and permit whitespace or comments between those tokens. Consequently, valid forms such as `# [path = "bridge.rs"]` and `#/**/[some_attribute]` are skipped by the filter. If the remaining text contains no literal `opensip_operability`, `!`, or `*`, the exception predicate still returns true and removes the adapter's sole `finalize` occurrence.

This is the same class of generated or unscanned bridge risk the r2 disposition says must fail closed. A separated `path` attribute can select an otherwise unscanned source file, and a separated procedural attribute can generate a binding or item without spelling it in the guarded source. The Cargo-resolution check constrains the external `opensip_operability` dependency but does not prohibit other present or future attribute-macro dependencies, so it does not close this lexical route. The existing `#[macro_use]` control exercises only the contiguous spelling and therefore passes without observing the hole.

Reject every post-adapter attribute token sequence unless it is one of the exact permitted built-ins, regardless of whitespace or comments between `#` and `[`. A bounded implementation may conservatively reject any `#` sequence left after accounting for the permitted exact attributes; a token-aware equivalent is also sufficient. Add negative controls for at least whitespace-separated and comment-separated unapproved attributes, then freeze fresh affected evidence that observes the corrected fence.

## R1 finding and authority ruling

The successor otherwise addresses `CLI-GUARD-R1-RF-1`. It requires one exact adapter occurrence after the pinned comment-stripped host prefix and immediately before the known next export, removes only that occurrence, rejects later literal `opensip_operability`, glob and macro spellings, and fails closed when the binding check is false. The metadata predicate follows the intended host resolve node, requires one dependency named `opensip_operability`, and binds the selected package, manifest, host library source, and operability library source to the intended canonical paths. Its same-name bridge, renamed binding, and alternate source-root controls exercise those decisions.

Existing X11 and accepted S-OP-2 authority remains sufficient for this test-only repair. X11 requires the creator, writer, gate, pack admission, recovery, and storage commit path to stay out of the CLI and host ingress, while S-OP-2 authorizes the existing optional-logging finalizer. Tightening the predicate that distinguishes those two accepted duties needs no new creator, storage, or logging selection.

## Frozen-subject and evidence assessment

The requested `subject.json` SHA-256 is exact: `ffa56833c1e0291157032ebe0911623e4ab3d34d271735775a04d19e5a2a1b94`. All 87 declared members are present, with no extra frozen subject files, and every declared byte count and SHA-256 matches. The candidate is byte-identical to the named worktree file; the worktree parent is `ca6f5be9ded80c50a143b2f219258c95c80db2e6`, its only diff path is the declared existing test file, and the architecture checkout is at the declared `278d1a27b4cea095b37eed09e7109d8a98be7696`. The full rejected r1 package and verdict are preserved by value.

The fresh r5 evidence records both affected tests and all-target CLI Clippy passing. Both weakening mutations compiled and failed at their named witnesses, the exact candidate bytes were restored after each, and both controls then passed freshly. The package accurately limits that evidence to source guards and offline Cargo metadata; it claims no CLI execution, private-fixture access, full matrix, production behavior, or product qualification. Those results establish the exercised branches but do not cover `CLI-GUARD-R2-RF-1`.

The six command/refusal/catalogue/effect test bodies and the other forbidden-name and security-owner checks remain unchanged. Inventory/hash binding and status reconciliation remain out of scope until a corrected unit is independently accepted. Rust3 is not reviewed here.

## Non-blocking observations

None.
