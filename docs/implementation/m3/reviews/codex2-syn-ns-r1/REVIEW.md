**CODEX2 — SYN-NS r1: REQUIRED-FINDINGS.**

Reviewed subject manifest 35f1a60c0e0b9fb7ba981c0f29cdf8616c891affc217dadecf1d6b688ded0469; successor fab4cf5394db0bfa308e2bbeb2a60183cf08ce3691a61d1d5fe96777e065a864 (6,330 bytes). There are six required findings. The supplied evidence checks all pass; they validate byte provenance, kind/field membership, canonical encoding and successor binding, not the semantic premises of local-name classification or the flow rules.

All 39 request pins and 20 manifest members verified. Closure/map checking and build --check passed. Scratch verify_design passed at 392499e (83 → 84), on its SYN-1/SYN-1F/SYN-NS chain (83 → 86), and at cd5958b (82 → 83). The selected inventory and inheritance projections stay unchanged. The checkout advanced during review; these are frozen-revision checks.

Only read-only commands and the supplied evidence scripts ran at nice -n 19, using the requested isolated Python. Offline dependencies and every output are under this review directory. No cargo, builds, tests, parser execution, crash-matrix operation, repository writes, commits or delegation. No real OpenSIP home or private 413 fixture access.

The concrete source examples below are static design traces, not parser/compiler execution results. Exact full replacement values for spec_syn_ns.py are in [replacement-data.json](replacement-data.json). They are proposed data, not an applied or accepted successor; the conservative alternatives trade recall for a sound boundary.

**RF-SYNNS-1 — The whitespace/comment transforms erase JavaScript-family line terminators even when they determine automatic semicolon insertion. The stream can equate different lexical statement boundaries, contrary to FIP byteGrammar.lineEndings.**

Location: docs/implementation/m3/syntax-e/syn-ns/evidence/spec_syn_ns.py:451-477; TOKEN_LAW[2], L2_LAW[0]; L1/L2/L3 closure specifications.

- FIP:728 permits L1+ line-ending normalization only where the language treats it as insignificant; the golden-corpus requirement at :722 expressly includes adversarial significant whitespace.
- TOKEN_LAW drops every gap containing only its six ASCII whitespace bytes, including CR/LF. For a common padded body ending in return item; versus return\nitem;, visible leaves are the same ordered return, identifier and semicolon tokens, while the hidden automatic semicolon and the significant newline disappear. The latter has a separate expression statement.
- The pinned JavaScript grammar.js:486-490 and :1300 use _automatic_semicolon; scanner.c:62-102 and :110-145 explicitly consider newlines, including inside block comments. L2 also removes the distinction between return /*same line*/ item; and return /*line\nbreak*/ item;.
- This is a static trace from pinned source and the proposed data, not a parser run. It affects javascript, typescript and tsx.

Fix: Keep significant line-break evidence. The supplied conservative replacement retains every JavaScript-family CR/LF gap and any comment containing a line terminator. A more precise independently reviewed ASI-boundary encoding is also possible, but blanket whitespace/comment deletion is not. Exact targets: `TOKEN_LAW[2]`, `L2_LAW[0]`.

**RF-SYNNS-2 — Capitalization and irrefutable position do not prove that a Rust identifier pattern introduces a local. The heuristic can rename a constant/path and mint identifier-insensitive fact equality; the stated lint limitation does not make that safe and misses raw identifiers.**

Location: docs/implementation/m3/syntax-e/syn-ns/evidence/spec_syn_ns.py:286-318; RUST_PATTERN_LAW; LD-NS8; normalizer and L3 patternLaw.

- The pinned Rust grammar.js:1373-1393 represents a bare pattern as identifier; :1648 permits (r#)? prefixes. node-types.json gives that node no binding-versus-item discriminator.
- With ordinary uppercase constants LEFT and RIGHT outside the function, compare identical padded function bodies whose match arms contain r#LEFT => spare + 10 versus r#RIGHT => spare + 10. Both raw identifier texts start with r, so the proposed case rule treats them as match-arm bindings. R1 holds; R2 sees no constant declaration inside the body boundary; R3 resolves each pattern occurrence to the invented match-arm binding; R4/R5 do not stop it. L3 therefore replaces the differing constant paths with the same opensip:local token.
- The raw-identifier case needs no naming-lint violation for the constants. Even without raw identifiers, permitted lowercase constants defeat a naming-convention proof. Irrefutable syntax does not itself disambiguate an identifier from a unit item pattern.
- E1 item 14 forbids L3 renaming of Rust paths, and NE:2596-2598 keeps paths significant. This is a static counterexample, not an executed parser/compiler case.

Fix: Do not infer bindings from case or position alone. Exact conservative pattern-law replacements bind only explicit binding forms and shorthand field bindings, and state the resulting recall limit. This affects both the declares and L3 copies; regenerate both. A broader extractor needs a separately reviewed proof of binding classification. Merely stripping r# before applying the old heuristic leaves the lowercase-constant defect. Exact targets: `RUST_PATTERN_LAW['law']`, `RUST_PATTERN_LAW['statedLimit']`.

**RF-SYNNS-3 — Macro token trees are not retained verbatim at L1-L3, and the declared unseen-item macro limit can rename a macro-introduced name. These conflict with NE’s significant-token and L3 exclusion tables.**

Location: docs/implementation/m3/syntax-e/syn-ns/evidence/spec_syn_ns.py:467, 469-481, 595-656; RUST_ATOMIC, L2_LAW, SCOPE_LAW_RUST, RUST_L3.bodyDisqualifiers; LD-NS9.

- NE:2596-2598 requires macro invocation token trees verbatim at every level and excludes macro-introduced names from L3 renaming.
- RUST_ATOMIC contains literals and comments but not token_tree. TOKEN_LAW therefore descends into a macro tree and drops whitespace gaps; L2_LAW deletes its non-doc comment tokens. Identical padded bodies differing only in m!{left /*one*/ right} versus m!{left /*two*/ right} become equal at L2 despite the verbatim requirement.
- The L3 macro guard disqualifies only names visible in the macro token tree or format capture, plus glob uses. An empty-token-tree statement macro can define an item in an inner block that shadows a parameter. For { common_padding(); { make!(); item } } versus the same body using parameter other, a make!() expansion defining const item is invisible to the proposed scope lookup. It treats item as the parameter, can rename it with other, and overlooks the introduced item. The README explicitly acknowledges this unseen-item case rather than stopping replacement.
- The checker proves symbol/field membership, not expansion visibility or token-tree opacity. No expansion or parser was executed.

Fix: Make Rust token_tree atomic at all token levels, and disable body-wide renaming whenever a macro_invocation occurs. The latter is a conservative recall limit that closes the unseen-introduction hole; the existing visible-name/format checks alone do not. Replace the stated unsafe exception with this explicit conservative rule. Exact targets: `RUST_ATOMIC`, `L2_LAW[0]`, `RUST_L3['bodyDisqualifiers']`, `SCOPE_LAW_RUST[5]`, `SCOPE_LAW_RUST[6]`.

**RF-SYNNS-4 — The flow-node traversal is under-specified and internally inconsistent with the role tables. singleStatement is never defined; field-filtered lists and wrapper unwrapping need explicit rules. Nested-body opacity also conflicts with unsafe-block role expansion.**

Location: docs/implementation/m3/syntax-e/syn-ns/evidence/spec_syn_ns.py:340-436; CONTROL_FLOW_LAW[1:3], TS_CONTROL.roleLaw, RUST_CONTROL.roleLaw.

- Nodes selects each named child of a statementLists node, while TS statementLists includes switch_case with field body. Its named value child is therefore a flow node under the general rule, but TS roleLaw says the list is only the body field nodes.
- No role record has a singleStatement key, and no prose defines which role fields that term denotes. Consequently loop bodies, consequences and other single-statement children have no closed traversal rule.
- The pinned JS and Rust else_clause nodes have no fields and wrap a statement / block-or-if_expression. The tables name alternativeChild but the law only singles out an else holding another branch. For else { right(); }, a literal first(single child) reading can make else_clause a simple flow node and omit right().
- Rust expression_statement gets its child’s role, but the role’s body/consequence/etc. fields are on the child, not the wrapper. That read target is unstated.
- Every selected nested body is said to be opaque; unsafe_block selects a block body of its own but also has a block role that enters the same child. The precedence between these instructions is unstated.

Fix: State the field-filtered List function, the complete role-selected child traversal, wrapper unwrapping, effective Rust field-read node, and opacity precedence. The supplied replacement does so without decomposing expressions or adding node-kind/field keys. Exact targets: `CONTROL_FLOW_LAW[1]`, `CONTROL_FLOW_LAW[2]`, `TS_CONTROL['roleLaw']`, `RUST_CONTROL['roleLaw']`.

**RF-SYNNS-5 — The posttest-loop rule permits entering do...while and taking its false exit before executing the body, and does not represent the test’s true edge as a branch.**

Location: docs/implementation/m3/syntax-e/syn-ns/evidence/spec_syn_ns.py:364-370; CONTROL_FLOW_LAW[5], edge rule (6).

- For do { work(); } while (check()); after();, entry/previous completion reaches the do flow node S. Rule (6) gives S -> first(body) as fallthrough and S -> next(S) as branch-false. Thus the graph contains entry -> S -> after() before work().
- A do...while body must run before its first test. This is a statement-level sequencing issue, covered by neither stated simplification (finally interposition and undecomposed expressions).
- After the body, the same S represents the test, so its body edge is branch-true rather than unconditional fallthrough. continue must target the test, not restart the body before testing.

Fix: Enter a nonempty posttest loop at its body, retain end-of-body/continue edges to S as the test, and give S its true/false test edges. The exact replacement distinguishes those incoming edges and handles empty and nested posttest bodies. Exact targets: `CONTROL_FLOW_LAW[5]`.

**RF-SYNNS-6 — The control-flow identity prefix says body owner’s chain, but the subject law defines a node’s chain as its STRICT ancestors, excluding the owner’s own segment. The graph-specific ordinal wording does not resolve that omission. Injective identities are not established by these bytes.**

Location: docs/implementation/m3/syntax-e/syn-ns/evidence/spec_syn_ns.py:108-141, 346-352; SUBJECTS_LAW[4], CONTROL_FLOW_LAW[1].

- SUBJECTS_LAW explicitly distinguishes a node’s strict-ancestor container chain from its declared subject, which appends its own segment.
- For two top-level functions f and g, both owner ancestor chains are empty. Reading the CF wording literally with graph-local ordinals gives both entry nodes syntax:<path>#entry:@0 and both first return_statement nodes syntax:<path>#stmt:return_statement@0. A different reader may infer a full owner prefix or file-global ordinal allocation; that inference is not specified.
- The percent escaping itself is injective and admissible. The defect is which container sequence is escaped and numbered, so better escaping does not fix it.

Fix: Use the body owner’s FULL subject segment sequence, including its own declaration/container segment; explicitly number flow nodes within that graph and set its entry/exit ordinal to zero. The combined CONTROL_FLOW_LAW[1] replacement also addresses RF-SYNNS-4. Exact targets: `CONTROL_FLOW_LAW[1]`.

**Requested judgments.**

1. Partly sound; required finding RF-SYNNS-1. LD-NS2 follows FIP:730 and IE:1068-1089: each level commits its own boundary/kind/transform rules, rather than only referring to the full normalizer. The payload frame and n:/a: symbol-name registry are correct. Atomic nodes plus non-whitespace gap tokens cover the span without silently losing other bytes. That byte-loss property does not justify erasing significant line terminators. The map validates against ExactValidator and commits each own canonical level file.

2. Not sound for selection; RF-SYNNS-2 and RF-SYNNS-3. R1-R5 have the right whole-name conservative structure, but their proof assumes correct classification and scope lookup. Case heuristics and invisible macro introductions violate that premise; naming lints and a stated semantic limitation cannot authorize free/path-name replacement in an identity-bearing fact level. The supplied conservative fixes reduce recall rather than overclaim identity. NB-SYNNS-1 separately identifies a reference-versus-binding occurrence gap.

3. Incomplete/ambiguous; RF-SYNNS-4, RF-SYNNS-5, RF-SYNNS-6. The selected edge vocabulary fits RPS. Finally interception and expression decomposition are declared syntactic approximations and are acceptable as explicit limitations here, rather than claims of semantic control-flow equivalence. They do not explain the do-while skip path or the unspecified child/identity traversal.

4. Grammar-name/field checks pass; substantive exceptions recorded. Body, declares, literal and role entries are visible named kinds with fields supported by the pinned grammars. JS-family type/member/parameter rows and Rust item/closure/impl/special-block rows otherwise have no additional required finding. The Rust ambiguous-pattern classification and macro handling require changes; the role traversal cannot be discharged by a census alone. Macro_rules and unnamed tuple fields are disclosed omissions, not invented DeclarationKindV1 values.

5. Escaping/literal encoding sound; CF owner prefix needs RF-SYNNS-6. The UTF-8 percent escape separates reserved delimiters, preserves distinct non-NFC source spellings and produces ASCII NFC SubjectIdV1 text. The 4096-character overflow rule refuses the file rather than collapsing identities. Literal valueText escapes C0/C1, normalizes NFC, and uses at most 4068 characters after its digest suffix; raw literal delimiters ensure nonempty text. Its expressly non-injective representation is admissible because exact bytes remain at the anchor.

6. Sound design definition. Near-v1 has exact framed 5-token shingle sets, integer Jaccard threshold/score, same-body-language comparisons, deterministic connected components, sorted member IDs/edges and minimum-member-best-neighbor scoring. It remains candidate-only and delegates retention/envelope law to SYN-1/E1 item 14a. TS/TSX pairing and JS separation match that selection. No normalizer execution is claimed.

7. Accept the disclosed process/placement deviations, subject to required byte fixes. E-7 and E-9 follow self-contained level ownership and A12 must check those tables and anonymous symbols. E-10 may freeze these exact E0 grammar pins now so E2a cannot silently invalidate reviewed specifications; this review verifies the pinned bytes, not a newest-upstream-release claim. E-11 writes reviewable design data before E2c implements/freezes fixtures. No ordering dependency is introduced: five unchanged accepted parents, no passage overrides, nineteen new candidates. LD-NS4/7/8/9/11/14 need the substantive corrections recorded above; other disclosed decisions have no additional blocker.

**Non-blocking observations.**

**NB-SYNNS-1.** Occurrence includes binding-site tokens, but Rust sequential let resolution is stated only for following siblings. Under that literal rule a first let pattern occurrence is free and R3 blocks the whole name, even when every later reference is local. This is a conservative recall loss rather than a false identity, so it is not a separate acceptance blocker. State that binding-site occurrences resolve directly to their introduced binding, then apply sequential lookup only to reference occurrences. An exact optional L3_LAW[3] replacement is supplied in replacement-data.json.

**NB-SYNNS-2.** The request pins main at 392499e. The checkout had already advanced to 5e25d04b when pin evidence was collected, and advanced again during review. The three verify runs intentionally use the requested frozen revisions, not a moving HEAD. All 39 request pins and all 20 subject members verified. Recheck current integration state in the lead’s acceptance/binding lane. This review identifies exact subject bytes and does not attest to a moving product HEAD.

Evidence is retained in pins-verification.json, additional-source-pins.json, deps-install.log, check.log, build.log and the three verify logs. reviewed-subject/ retains the exact reviewed member bytes. No lead negative probe was rerun, and no fixture/corpus qualification is claimed.
