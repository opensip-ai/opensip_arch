# SYN-NS r2 — design-unit review

Reviewer: GROK2. Verdict: **ACCEPT-DESIGN-UNIT**.

CODEX2's r1 review stands. This round judges whether r2 resolves its six findings. No cargo, no parser, no repository edit.

## Subject

- `docs/implementation/m3/syntax-e/syn-ns-subject.json`: 4701 bytes, sha256 `adc20c45caf7c28b4f590ebae7cf38f08d826ba632d592e566db9ad865da85ed`.
- `docs/implementation/m3/syntax-e/syn-ns/successor.json`: 6975 bytes, sha256 `180f49350f5fb243ff535f472df60226928fb46089f978a0e647d49ed0bb3e58`. No passage overrides. The identity parent is SYN-1F's `design/foundation/identity-schemas.v3.json` (200510 bytes, `73645b7633d95f5d7b8e5183d789b8aab028148be0dd158e0b503a4cc3e2bd19`).
- Product HEAD during this review: `218465fb71fd62ca01856d40d26ec822f45233be`. The frozen lock revision is what was verified.
- `~/Library/Application Support/OpenSIP` was absent before and after.

## Findings

All six r1 findings are resolved. There is no new false-equality path in the rules r2 states.

**RF-SYNNS-1.** `line_terminators()` is `significant` for javascript, tsx, and typescript, and `insignificant` for rust. A whitespace gap of only CR/LF plus spaces, tabs, VT, and FF becomes one `opensip:line-break` token of value `0x0A`. A non-directive comment that contains LF, CR, U+2028, or U+2029 becomes one line-break token, and consecutive line-break tokens merge. Spaces, tabs, VT, and FF alone are still dropped. The pinned JSX scanner puts significant JSX whitespace in `jsx_text`, so those bytes stay in that token; a gap inside JSX children is newline-led indentation, which the line-break token keeps. `return item;` and `return\nitem;` stay distinct at L1 and L2. `return /*x*/ item;` and `return /*\n*/ item;` stay distinct at L2. `a(); // note` and `a();` meet at L2. Re-applying r1's insignificant setting collides the two ASI pairs.

**RF-SYNNS-2.** Bindings are the pinned grammar's explicit forms only: `ref x`, `mut x` (and `ref mut x` through the inner `mut_pattern`), `x @ p`, `let mut x`, a `mut x: T` parameter, and `S { mut a }` / `S { ref a }`. A binding mode or `@` is not applied to a path by those rules. Every other identifier in a pattern, including a plain let, parameter, closure parameter, `for` pattern, match arm, `if let`, `while let`, let-else, raw identifier, and a primitive name spelled as an identifier, binds nothing, and R4 makes that name non-renamable. `statedLimit` says ordinary unmodified locals and parameters are neither declared nor renamed. Declares use the same pattern law.

**RF-SYNNS-3.** `token_tree` is atomic, so the fixture values `(left /*one*/ right)` and `(left /*two*/ right)` stay exact and distinct at L1 and L2. Dropping `token_tree` from the atomic set reproduces the r1 L2 collision. A body containing a `use_wildcard`, a `macro_invocation`, an `attribute_item`, or an `inner_attribute_item` gets no L3 renaming. The old visible-name and format-capture guards are not in `disqualifying`.

**RF-SYNNS-4.** `List` is defined with and without a field, so a `switch_case` value is not a statement. Selection names the role-table children, reads Rust role fields on the `expression_statement`'s expression child, unwraps `else_clause`, treats a selected statement list as transparent and any other selected node as one flow node, and gives opacity precedence over a role. `unsafe_block` has no role; the role law calls unsafe, async, const, try, and gen blocks bodies of their own. The pinned JavaScript `try_statement` handler is a `catch_clause` whose `body` is a `statement_block`, and the finalizer is a `finally_clause` with the same `body` field.

**RF-SYNNS-5.** `enter` sends a nonempty posttest loop to its first body statement. The body's end and `continue` are the two edges that reach the test itself. The test's true edge returns to the body as `branch-true`, and its false edge leaves. The do…while fixture's graph matches that: entry arrives at the `if`, `continue` and the end of `work()` arrive at the `do_statement`, and the false edge arrives at `after()`.

**RF-SYNNS-6.** The identity prefix includes the owner's own segment. `entry` and `exit` use ordinal 0, and statement ordinals count inside the graph. `function f` and `function g` produce `syntax:a.js#function:f@0/...` and `syntax:a.js#function:g@0/...`. The checker reports that a strict-ancestor prefix collides those identities.

**NB-SYNNS-1** is in the L3 resolution sentence: a binding-site occurrence resolves to the binding that site introduces. **NB-SYNNS-2** is the frozen `design-lock.json@218465f` check.

## Stated limits

The recall losses are stated and acceptable under the rule that an unproved transform is not applied. Rust L3 and declares cover only the explicit binding forms, and a body that contains a macro or an attribute is not renamed (E-12). JavaScript-family line breaks are kept even where a given production would not use them for ASI. Both miss clones. Neither equates a path, a constant, a macro token tree, or two different statement boundaries.

## Fixtures and the oracle

The six trees were compared by hand with the pinned grammars. No parser was run. Visible leaves and the structure the oracle reads match those grammars: ASI splits `return` from a following item when a line terminator or a line-terminating comment intervenes; a comment without a line terminator stays inside the return; the macro invocation's `token_tree` holds the comment as an extra child; the two functions are ordinary `function_declaration` nodes; the do…while body's `if` has a `continue_statement` consequence. `reference_syn_ns.py` applies the closure tables for tokens, comments, owner chains, and the JavaScript-family roles these fixtures use. Its do…while edges and the two function prefixes match `CONTROL_FLOW_LAW`. The checker compared the hand-derived expectations with that oracle.

## IDS parent and verify_scratch

The `normalization-specification-map` definition in SYN-1F's identity copy is raw-byte identical to the frozen file's definition (2000 bytes). `verify_scratch.py` skips a unit the lock already binds. At `218465f`, `--rev` and `--chain` both pass and both append only SYN-NS, 91 contract successors to 92.

## Evidence

From `docs/implementation/m3/syntax-e`, with `python3.14 -I -B` at `nice -n 19` and jsonschema 4.25.1 offline:

- `check_syn_ns.py --deps <review deps>` passed, `wrote: false`. Distinct references: javascript 106, rust 115, tsx 133, typescript 127. The map validated with `ExactValidator`. All six fixtures matched, and the r1 collisions reproduced.
- `build_syn_ns.py --check` passed and reported the subject and successor hashes above.
- `verify_scratch.py --rev 218465f` and the same command with `--chain` both passed, 91 to 92.

## Observation

**NB-SYNNS-3.** Outer attributes on a Rust item sit outside the body block, so they do not by themselves disable L3 for that block. Detail is in `review.json`. No change is required for acceptance.
