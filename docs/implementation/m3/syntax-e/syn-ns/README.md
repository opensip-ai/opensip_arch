# SYN-NS — the syntax normalizer specification (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r2, PROPOSED, not accepted.** It is a design unit: it adds new design files to arch, and changes no product file, contract passage, schema or public code. It needs `ACCEPT-DESIGN-UNIT` from an independent reviewer and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-E1 r3** (`../PROPOSAL-r3.md`, `d71031ff…`) names successor **SYN-NS** in item 19 (E1:693): "The identity-bearing normalization bytes (items 13 and 14)". It covers:
- `normalizer.v1.json`, the native normalizer, a member named by the bundle manifest;
- IE's normalization map, the closure tree's second root;
- the four level specifications, reached only through the map's rows;
- `near-v1`.

E1 item 20 says that E2c implements these bytes and that "SYN-NS, accepted before its fixtures freeze". This unit writes the bytes now, so that E2c implements an accepted specification rather than inventing one.

**The rule r2 follows.** Where the pinned grammar cannot prove that a transform preserves meaning, the transform is not applied. A missed clone costs little. A false equality would mint an identifier-insensitive or lexical fact identity for bodies that differ, which is a correctness defect.

**The bytes are the closure members.** The candidates under `closure/` are canonical JSON (foundation `canonical.py`'s rule) at their exact closure tree paths. E2a's lane places them in the `kind=grammar` closure unchanged.

| Tree path (E1 item 4) | Bytes | sha256 | Bound by |
|---|---|---|---|
| `opensip-interface/grammar/normalizer.v1.json` | 43,373 | `e4a648f0…` | the manifest's `normalizer.specificationDigest` |
| `opensip-interface/normalization/specification-map.v1.json` | 549 | `e5d65586…` | its fixed path, the tree's second root (A3, A6) |
| `opensip-interface/normalization/levels/L0-verbatim.v1.json` | 2,315 | `506a30e0…` | the map's L0 `specificationDigest` |
| `opensip-interface/normalization/levels/L1-lexical.v1.json` | 4,540 | `4b36eeec…` | the map's L1 row |
| `opensip-interface/normalization/levels/L2-comment-insensitive.v1.json` | 6,628 | `0762f542…` | the map's L2 row |
| `opensip-interface/normalization/levels/L3-identifier-insensitive.v1.json` | 27,540 | `6b060a83…` | the map's L3 row |

`materialization-map.json` and `evidence/kinds-report.json` give the full digests. `readable/` has the same six documents pretty-printed, for review; they are not normative.

**The branch.** These bytes are the same under both execution models; E1 item 4 says "Both branches carry the same map and level files". E0 chose `native-linked-v1` (`../E0-REPORT.md`, `c1011e83…`). There, step A12's symbol tables are recomputed from the linked `Language` rather than decoded from a module. The names checked are the same either way.

**Product.** Main at `218465f` (SYN-1 bound at `682991f`, SYN-1F at `218465f`; 91 contract successors), read only. The record is built against `design-lock.json@218465f`.

## r2 changes and review responses

CODEX2 reviewed r1 (subject `35f1a60c…`; `docs/implementation/m3/reviews/codex2-syn-ns-r1/`) and returned REQUIRED-FINDINGS: six required findings and two observations. The r1 bytes of every member are in `docs/implementation/m3/reviews/codex2-syn-ns-r2/r1-members/`.

| Finding | The rule chosen |
|---|---|
| **RF-SYNNS-1** (ASI line terminators) | **The lead's simple rule.** A JavaScript-family row (javascript, tsx, typescript; so `.js`, `.jsx`, `.ts`, `.tsx`, `.d.ts` and the rest) has `lineTerminators: significant`.<br>- At L1 and above, a whitespace gap that holds a CR or LF becomes **one `opensip:line-break` token** (value `0x0A`), never dropped. Spaces, tabs, VT and FF alone are still dropped.<br>- At L2, a non-directive comment whose text holds a line terminator (U+000A, U+000D, U+2028 or U+2029) becomes one line-break token instead of being removed; ECMAScript counts such a comment as a line terminator. Runs of line-break tokens then merge into one.<br>- Rust rows keep `lineTerminators: insignificant`, since Rust has no automatic semicolon insertion.<br>**Rejected:**<br>- An "ASI-could-apply" rule, such as marking statements that end without an explicit `;`. It needs a per-grammar proof that every newline-sensitive production leaves a visible trace (restricted productions, TypeScript's `[no LineTerminator here]` modifiers, class-member ASI). That proof is not available now (LD-NS18).<br>- CODEX2's keep-the-comment variant. It would make L2 sensitive to the comment's text, where only the line terminator matters.<br>Fixtures: `asi-return-newline` (CODEX2's `return item;` against `return\nitem;`), `asi-comment-newline`, and a positive control. |
| **RF-SYNNS-2** (Rust identifier patterns) | **Bindings only by explicit binding forms** (LD-NS8, rewritten).<br>- An identifier binds only as `ref x`, `mut x` (also `ref mut x`), `x @ p`, `let mut x` or a `mut x: T` parameter.<br>- A shorthand field binds only as `S { mut a }` or `S { ref a }`.<br>Each is structural in the pinned grammar: `ref_pattern`, `mut_pattern`, `captured_pattern`, a `mutable_specifier` child, or the anonymous `ref` token. Rust's grammar never applies a binding mode or `@` to a path.<br>Every other identifier inside a pattern is an **ambiguous pattern identifier**. That includes plain `let x`, plain parameters, plain closure and `for` patterns, all match-arm, `if let`, `while let` and let-else identifiers, `r#X`, and primitive-type names. Such an identifier binds nothing, and at L3 its name is non-renamable (R4).<br>The same pattern law serves declares extraction, so plain locals and parameters get no declares fact. That precision loss is stated in the pattern law's `statedLimit`. |
| **RF-SYNNS-3** (macro token trees) | **`token_tree` is an atomic kind at L1, L2 and L3.** It is one token with its exact bytes: no gap dropping, comment deletion or renaming inside it (NE:2596-2598). That covers macro invocations, `macro_rules!` bodies and attribute arguments.<br>**A Rust body containing any `macro_invocation`, `attribute_item` or `inner_attribute_item` gets no L3 renaming at all.** That is the safe statement the lead asked for: an unexpanded macro, or an attribute or derive macro, can introduce names this reading cannot see. The visible-name and format-capture disqualifiers, now redundant, are removed. Fixture: `macro-token-tree-atomic`. |
| **RF-SYNNS-4** (flow-node traversal) | `CONTROL_FLOW_LAW` now states, in order:<br>- **Lists.** `List(L)` with and without a field; a `switch_case` value is never a statement.<br>- **Selection.** The role tables are the single authority. It gives each role's exact selected children, reads a Rust `expression_statement` through its effective expression node (identity, order and anchor stay the wrapper's), and unwraps an `else_clause` to its first non-comment named child. A selected list is transparent; any other selected node is a single statement, which is how *singleStatement* is now defined. Nothing unselected is entered, and **opacity takes precedence over a role**.<br>- `first`, `next` and the edges.<br>The `unsafe_block` role is removed from the Rust table: an unsafe block is a body of its own, so it is opaque and simple in the enclosing graph. That resolves the clash between opacity and role expansion.<br>The TypeScript and Rust `roleLaw` texts are rewritten to match. |
| **RF-SYNNS-5** (do…while) | A new **posttest entry** rule: `enter(X)` is `enter(first(body of X))` for a posttest loop with a non-empty body, and every edge target passes through `enter`. The two edges that reach the test do not: the end of the body, and a `continue` that targets the loop.<br>Rule 6 is restated:<br>- entry reaches the body;<br>- the body's end reaches the test as `loop`;<br>- the test's true edge goes back to the body as `branch-true`;<br>- its false edge goes to the next statement;<br>- `continue` targets the test (rule 15).<br>Fixture: `cf-do-while`, with a `continue` inside the body. |
| **RF-SYNNS-6** (control-flow identities) | **Identities.** P is the body owner's **full** subject chain: its container chain, then the owner's own segment. entry and exit are `P/entry:@0` and `P/exit:@0`. A flow node is P plus a stmt segment per enclosing flow node, then its own. Ordinals count within the graph. The owner's own segment is unique under the subject law, so no two graphs share an identity.<br>Fixture: `cf-two-functions` (CODEX2's example). Under r1's strict-ancestor reading the two graphs collide, and the checker shows it. |
| **NB-SYNNS-1** (binding-site resolution) | Taken as suggested: a binding-site occurrence resolves directly to its own binding, and only reference occurrences use the scope lookup (`L3_LAW[3]`). |
| **NB-SYNNS-2** (moving HEAD) | Taken: the record is built and verified against `design-lock.json@218465f`, read with `git show`. The request pins that lock and says the live checkout may move. |

**Also changed in r2:**
- **The IDS parent** is now the **selected** identity copy, SYN-1F's `design/foundation/identity-schemas.v3.json` (bound at `218465f`), instead of the frozen `foundation/identity-schemas.v3.json` that I1-L, CRC-1 and SYN-1F have superseded. The `normalization-specification-map` definition the map is validated against is byte-identical in both (LD-NS16).
- **Fixtures.** `evidence/fixtures.json` (hand-written trees and expectations) and `evidence/reference_syn_ns.py` (a small oracle that reads these documents' own tables) are new. The check runs them, and it re-runs r1's rules to show that each finding's defect reproduces.
- **`evidence/verify_scratch.py`.** SYN-NS's copy now skips units the lock already binds, so its `--chain` works at `218465f`. SYN-1's and SYN-1F's bound copies keep their bytes.
- **The builder** now emits the lead's draft unit record, with review path `codex2-syn-ns-r2/review.json`.

## Short names

E1, E0, NE and NES are as in SYN-1's README. The other names:
- **IE:** `docs/v2/contracts/product-v1/identity-and-evidence.md`.
- **FIP:** `docs/coop/artifacts/fact-identity-policy.v2.json`, the inherited body recipe IE names as normative, with its `canonicalisationSchema/byteGrammar` and `normalisationLadder`.
- **IDS:** the selected identity schema, `docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json`, whose `#/$defs/normalization-specification-map` and `x-opensip-digest-domains.normalizationSpecificationLaw` define the map.
- **RPS:** `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json`, which holds the declares, literal and control-flow payloads.
- **The grammars:** E0's pins, tree-sitter-rust `v0.24.2` (`77a37472…`), tree-sitter-typescript `v0.23.2` (`f975a621…`, the `typescript` and `tsx` grammars) and tree-sitter-javascript `v0.25.0` (`44c892e0…`). Each pinned file is in `../e0-probe/pins/*.pins.tsv`, and the bytes are in E0's SCRATCH.

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `closure/opensip-interface/…` | the six closure members (generated, canonical) |
| `readable/*.json` | the same six, pretty-printed (generated, not normative) |
| `materialization-map.json` | generated: tree path, candidate path, bytes and sha256 per member; the manifest's `normalizer` object |
| `successor.json` | the record: five parents, no passage override, twenty-one candidates |
| `evidence/spec_syn_ns.py` | the documents, as data |
| `evidence/build_syn_ns.py` | builds the members, the record, the subject and (outside the subject) the draft unit record |
| `evidence/check_syn_ns.py` | read-only checks: grammar pins, the symbol census, every reference, canonical bytes, the map, consistency and the fixtures |
| `evidence/kinds-report.json` | generated by the check: the census, every kind, anonymous token and field named, each verified, and the fixture results |
| `evidence/reference_syn_ns.py` | (r2) the fixture oracle: the token and comment laws for every row, and the JavaScript-family statement-level control flow (lists, selection, identities, `first`, `next`, posttest entry and edge rules 1 to 6, 11, 12, 14 and 15) |
| `evidence/fixtures.json` | (r2) six fixtures: hand-written source and trees, and hand-derived expected streams and graphs |
| `evidence/verify_scratch.py` | the real verify_design with a synthetic review and assent |
| `../syn-ns-subject.json` | the subject manifest (generated) |
| `../syn-ns-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW` (generated); not part of the subject |

## What the documents say

### `normalizer.v1.json`: the native normalizer

It has one row per code grammar (`javascript`, `rust`, `tsx`, `typescript`); the four data rows have none, because they are never parsed. Every law is stated once at the top, and every table is per row.

- **`parameters`.** NE §6.2's values, copied: `minOccurrences` 2, `minBodyBytes` 64, `minTokens` 20 for levels and 50 for near, `nearThreshold` 800,000, and the two group bounds. The check compares them with NE's text.
- **`bodies`.** NE §6.3's function, method, closure or lambda, impl item and block bodies, each as a (kind, field or child) pair:
  - **JavaScript family:** function, generator and arrow functions, methods, and class static blocks.
  - **Rust:** `function_item` (a method in an impl or trait), closures, `impl_item` bodies, and unsafe, async, const, try and gen blocks.
  - **Import-only bodies are excluded** as candidates. Such a body is a statement container whose named children are all import-only kinds or comments. A kept body is hashed verbatim.
- **`subjects`.** The `SubjectIdV1` text is `syntax:` + esc(path) + `#` + `/`-joined segments of the form `tag:esc(name)@ordinal`.
  - tag is the declarationKind, or a containers rule's tag for an anonymous container, or `stmt`, `entry` or `exit` in control flow.
  - esc percent-encodes every byte outside `0x21` to `0x7E`, and `% # / @ :`. It is injective, and its output is ASCII, so NFC.
  - ordinal counts earlier same-tag, same-name segments under the same parent chain.
  - No offset or line enters the text, so E2-T19 (a blank line above a declaration changes nothing) holds. A text over 4,096 characters makes the file `truncated:nodes` (E1 item 11).
- **`declares`.** Per row, which node declares what and under which `declarationKind`. Each rule is a name rule, a names rule or a pattern-bindings rule, under a pattern law. The rows cover:
  - functions, methods, types (class, interface, alias, enum, struct, union, trait, associated type), namespaces and modules;
  - fields (class fields, property signatures, TypeScript enum members, Rust struct fields and enum variants);
  - variables (declarators, `for…in`/`of` with a binding kind, consts, statics);
  - parameters (formal parameters, arrows' single parameter, catch parameters).

  **Rust pattern bindings** (let, parameter, closure, match, `if let`/`while let`, `for`) are declared only for explicit binding forms (RF-SYNNS-2). Imports declare nothing: they are the `imports` capability.
- **`literals`.**
  - **The kinds.** `string`, `template_string`, `number`, `true`, `false`, `null` and `regex` in the JavaScript family. In Rust, string, raw string and char literals, integer and float literals, and `boolean_literal`.
  - **The valueText rule.** Control characters become `\uXXXX`; the text is put in NFC; and a text over 4,096 characters becomes its first 3,996 characters, `…`, `sha256:` and the digest of the whole.
- **`controlFlow`.** One statement-level graph per function, method, lambda or block body, with entry and exit nodes. The law's sections, in order:
  - lists, and selection by the role tables;
  - identities, under the owner's full subject;
  - `first` and `next`;
  - posttest entry;
  - sixteen numbered edge rules:
    - fallthrough, branch-true/false, loop, return, throw and exception, for if, the loops, switch, match, try, labeled statements, break, continue, return and throw;
    - Rust's `?` as an early-return edge.

  Three simplifications are stated: finally interposition; no decomposition inside expressions; and no decomposition of a let-else alternative. Per row, the role table is the single authority for which nodes are flow nodes and what they select.
- **`near`.** `near-v1` takes 5-token shingles of the L3 stream, encoded as framed tokens, and decides similarity by an integer Jaccard test against 800,000 millionths. Groups are connected components within one body language, so they are never `typescript+javascript`. They are `CloneCandidateGroupV2` records with sorted members and sorted `matchedEdges`, and `similarityMillionths` is the minimum member's best edge.

### The four level specifications

Each one is complete for its level (LD-NS2). Each states FIP's byte grammar for its payload, its transform order, and its rows.

- **L0-verbatim:** the payload is `u32be len ‖ the exact span bytes`, with no tokenisation.
- **L1-lexical, the token law:**
  - Token nodes are the visible leaves of the body's subtree. A node of the row's `atomicKinds` is one token and is not entered. Those kinds are strings, regexes and comments; in Rust also raw strings, chars and **macro token trees**.
  - Bytes covered by no token form gaps. A gap of spaces, tabs, VT and FF is dropped. A whitespace gap holding CR or LF is dropped in Rust, and is **one `opensip:line-break` token** in the JavaScript family. Any other gap is one `opensip:gap` token with its exact bytes.
  - A kind id is `n:` or `a:` plus the symbol name. Values are exact bytes.
- **L2-comment-insensitive:** L1, minus comment tokens that are not directives.
  - **JavaScript-family directives:** triple-slash directives, `@ts-` pragmas and JSX pragmas, by anchored patterns.
  - A JavaScript-family comment holding a line terminator becomes a line-break token, and runs of line-break tokens merge.
  - **Rust directives:** doc comments, recognised by their doc-marker child.
- **L3-identifier-insensitive:** L2, with the occurrences of renamable local names replaced by `{kind: "opensip:local", value: "<n>"}`, numbered by first occurrence. A name is renamable only when:
  - **R1:** it has a local binding site;
  - **R2:** it has no non-renamable one (a class, enum, named function expression, block-nested function declaration, Rust item or `use` name);
  - **R3:** every occurrence resolves, under the row's scope law, to a local binding inside the body's boundary (a binding-site occurrence resolves to its own binding);
  - **R4:** it has no disqualifying occurrence (a shorthand property or field, a JSX tag name, or, in Rust, an ambiguous pattern identifier);
  - **R5:** the body has no `with` or direct `eval`, or, in Rust, no glob `use`, macro invocation or attribute.

  The rows carry the scope kinds, binding rules, barriers, non-occurrences, disqualifiers and pattern laws.

### The map

The map is `{"levels":[{L0…},{L1…},{L2…},{L3…}],"normalizerId":"opensip.syntax.normalizer","schemaVersion":1}` in canonical bytes. Its levels are strictly ascending, and each `specificationDigest` is its level file's sha256. It validates against IDS's `#/$defs/normalization-specification-map` with the design's `ExactValidator`, and its `normalizerId` is the manifest's (E1 item 5). So A3 and A6's map checks, and IE's Run-closure joins (IE:1074-1080), are satisfiable by construction.

## Lead decisions

Each decision is made under the owner's standing direction to decide on the lead's recommendation, and names the alternatives it rejects. The owner may reverse any of them.

**LD-NS1. One unit covers all of items 13 and 14, written now against E0's pins.**
- The declares, literal and control-flow tables live in `normalizer.v1.json`, one closure member, so they cannot be split from the body and near tables into another unit.
- The grammars are pinned (E0), so every name can be checked now.
- **Rejected:**
  - **Leaving item 13's tables for E2c to write and SYN-NS to review alongside** (E1 item 13's wording). The specification would then be drafted inside a code unit, against its own fixtures.
  - **Deferring control flow.** Item 12's `syntax` cell would be unproducible.

**LD-NS2. Each level specification is self-contained and carries its own node-kind tables. A12 covers them too.**
- FIP's `levelVersionDefinition`, which IE adopts as normative, defines a level's version as the digest of "the canonical level specification, **including** per-language lexical boundary rules, canonical token-kind registry, directive classification, transform order, and replacement byte rules".
- FIP's BH-1 says "Changing L2's comment grammar does not touch L1 identities."
- E1 item 14 put the comment, directive and local-binding tables in `normalizer.v1.json`, but then a level's digest would not commit to its own rules. So the tables a level uses are in the level file:
  - `atomicKinds` and `lineTerminators` in L1, L2 and L3;
  - the comment kinds and directives in L2 and L3;
  - the scope and binding tables in L3.
- `normalizer.v1.json` keeps what is not a level's transform: bodies, subjects, declares, literals, control flow and near.
- The one shared law, the pattern law, is stated in both `normalizer.v1.json` (for declares bindings) and L3 (for renaming), and the check asserts the two copies are equal.
- **Consequence:** step A12 (`native.syntax-normalizer-kind-unknown`) must check the level files' names as well as the normalizer's. SYN-1's route row and key table say so (SYN-1 E-7). CODEX2 accepted this reading in r1 (judgment 1).
- **Rejected:**
  - **The tables in `normalizer.v1.json` only, with level files that reference them by digest.** Every level's digest would then change with any normalizer change, including the syntax-fact tables.
  - **Per-sub-table digests.** That adds an admission join E1 does not have.

**LD-NS3. The grammar pins are E0's.**
- Every name is checked against tree-sitter-rust `v0.24.2`, tree-sitter-typescript `v0.23.2` and tree-sitter-javascript `v0.25.0`, with runtime `v0.27.0`.
- E1 item 6's selection rule ("the newest upstream release, as of E2a") is therefore read as of this unit. A later upstream release is item 6's "updating a grammar": a new closure, a dependency-policy row, and a SYN-NS successor. A12 refuses a drifted name at admission in any case.
- **Rejected:** re-selecting the grammars at E2a's start, which could invalidate an accepted specification without review.

**LD-NS4 (r2). Tokens are visible leaves plus atomic kinds, plus gap tokens and, in the JavaScript family, line-break tokens.**
- Some grammars cover bytes with hidden tokens. tree-sitter-rust's raw string delimiters `_raw_string_literal_start` and `_end` are an example. A leaves-only stream would lose those bytes and could make different bodies equal, which would be a false identity. The gap rule makes the stream lossless except for dropped whitespace.
- **Line terminators.** In the JavaScript family, a line terminator decides automatic semicolon insertion and the restricted productions, which FIP:726-728 marks significant. So it is never dropped; it is canonicalised to one line-break token (RF-SYNNS-1). In Rust no whitespace is significant between tokens, so whitespace is dropped.
- **JSX.** The pinned scanner makes every significant JSX whitespace run a `jsx_text` token (`scan_jsx_text`). That covers a run without a newline, and a run with text on a line. So a gap inside JSX children is only newline-led indentation, which JSX itself removes; the line-break token keeps even that.
- Atomic kinds make each literal, each comment and each Rust macro token tree one token, so its inner structure stays in one exact value.
- **Rejected:**
  - **Leaves only.** It would lose hidden-token bytes.
  - **The grammar's own whitespace set,** which includes Unicode spaces. Dropping those would equate bodies that differ by a non-ASCII space.
  - **Dropping JavaScript-family newlines** (r1). That equates `return item;` and `return\nitem;` (RF-SYNNS-1).

**LD-NS5. Kind ids are symbol names; replaced locals use the kind `opensip:local`.**
- FIP forbids numeric ordinals. Symbol names are the grammar's canonical identifiers, and the `n:` and `a:` prefixes separate a named `identifier` from an anonymous token spelled the same way.
- A replacement must never equal a source token. JavaScript allows `$1` as an identifier, so `$1` as a value under `n:identifier` would collide. A distinct kind id cannot. The same holds for `opensip:line-break` and `opensip:gap`.
- **Rejected:**
  - **A cross-grammar canonical token registry.** Identities never cross grammars anyway: dialect is in `languageVersion`.
  - **`$N` values under `n:identifier`.** They can collide with real identifiers.

**LD-NS6. Directives: NE §6.3's two, plus every triple-slash directive and the JSX pragmas. Rust doc comments are recognised by their marker child.**
- `/// <amd-module>` and `@jsx` pragmas direct the compiler as much as `/// <reference>` does. Keeping more comments makes L2 narrower, never wrongly equal.
- rustc's own doc-comment rule (`///` but not `////`; `/**` but not `/***` or `/**/`) is what tree-sitter-rust's scanner encodes in the marker child.
- **Rejected:**
  - **NE's two directives literally.** Other compiler directives would then be removed.
  - **Lexeme regexes for Rust.** They would duplicate the grammar's classification.

**LD-NS7. L3 renames a name only when every occurrence of it in the body is bound inside the body (R1 to R5).**
- **The soundness argument.** Two bodies with equal L3 streams then differ only by a one-to-one renaming of names that are bound inside. Free names, properties and kept names are identical. That is NE's identifier-insensitive identity. It holds only if binding classification and scope lookup are right. r2 therefore removes every heuristic classification (LD-NS8) and every case where an unseen expansion can bind (LD-NS9). A doubtful name is kept, never guessed.
- **Rejected:**
  - **Renaming a name wherever it is bound somewhere in the body.** It is unsound: a free reference that shares a local's name would be renamed with it.
  - **Per-binding renaming with exact shadowing.** It has more recall, but needs a complete scope implementation per language, and a mistake there is a false identity.
  - **Renaming under `with` or a direct `eval`,** which can read locals by name.

**LD-NS8 (r2). Rust pattern bindings: explicit binding forms only.**
- **The forms.** An identifier binds only as `ref x`, `mut x` (also `ref mut x`), `x @ p`, `let mut x` or a `mut x: T` parameter. A shorthand field binds only as `S { mut a }` or `S { ref a }`.
- **Why these.** Each form is visible in the pinned grammar's structure: `ref_pattern`, `mut_pattern`, `captured_pattern`, a `mutable_specifier` child, or `field_pattern`'s anonymous `ref`. Each is a binding by Rust's grammar, because a binding mode or `@` cannot apply to a path.
- **The lead's list, read under its condition.** The lead named "let patterns, function and closure parameters, for patterns, and identifier @ bindings, if the pinned grammar marks them structurally". The pinned grammar marks the *position* of a plain `let x`, `fn f(x: T)`, `|x|` or `for x in`, but not the identifier's binding-ness. Rust resolves such an identifier as a unit struct or a single-valued constant pattern when one is in scope, and the reading cannot see the items in scope. So only the forms above qualify.
- **Everything else is ambiguous.** Any other identifier in a pattern binds nothing. That includes every bare identifier in a match arm, `if let`, `while let` or let-else; `r#X`; and a primitive-type name the grammar spells as an identifier. At L3 an ambiguous pattern identifier's name is non-renamable (R4), so a path or constant is never renamed.
- **Precision loss, stated in `statedLimit`.**
  - Ordinary unmodified Rust locals and parameters are neither renamed at L3 nor declared by declares extraction.
  - With LD-NS9 (no renaming in a body with a macro or attribute), Rust L3 renames little in practice.
  - Syntax-only Rust is the fallback for code with no Rust unit; Cargo projects go through the Rust provider (M3-L).
- **Rejected:**
  - **The r1 case rule** (an initial capital means a constant in a refutable position). `r#LEFT` against `r#RIGHT` defeats it, and lowercase constants are legal (CODEX2's counterexample).
  - **Stripping `r#` and keeping the case rule.** That leaves the lowercase-constant hole.
  - **All plain identifiers in irrefutable positions.** That leaves the unit-struct and single-valued-constant hole the lead's guiding rule forbids.
  - **A different pattern law for declares than for L3.** A declares fact that names a constant as a declared variable is also false.

**LD-NS9 (r2). Macros and attributes: atomic token trees, and no renaming in their presence.**
- `token_tree` is an atomic kind at L1, L2 and L3, so macro invocation token trees are verbatim at every level (NE:2596-2598). That covers whitespace and comments too, and also `macro_rules!` bodies and attribute arguments.
- A Rust body containing any `macro_invocation`, `attribute_item` or `inner_attribute_item` gets **no L3 renaming at all**. An unexpanded macro, or an attribute or derive macro, can introduce names (an inner `const item`, say) that this reading cannot see. No claim about which names an expansion introduces is needed.
- A glob `use` also disables renaming for the body (unchanged).
- **Rejected:**
  - **The r1 visible-name and format-capture guards.** They miss names an expansion introduces that do not appear in its token tree (CODEX2's `make!()` case).
  - **Disqualifying only macro invocations and not attributes.** Attribute and derive macros expand to items as well.

**LD-NS10. Bodies.**
- A "block body" is a class static block, or a Rust unsafe, async, const, try or gen block. It is never the block of an if, a loop or a function, which would duplicate their enclosing body.
- An import-only body is a statement container of import-only kinds and comments. A comment-only body counts, since NE lists headers and licence comments.
- **Rejected:**
  - **Every block as a body.** That gives overlapping noise.
  - **Keeping comment-only bodies.** They hold no code to clone.

**LD-NS11. Subjects.**
- Segment tags are declarationKinds, not node kinds, so subjects read the same across the JavaScript-family grammars.
- esc is injective byte escaping, with no NFC applied to names.
- The ordinal is per tag and name under one parent chain.
- **Control-flow identities (r2)** are prefixed by the owner's full subject chain (RF-SYNNS-6).
- **Rejected:**
  - **NFC-normalizing names.** Two different identifiers could then share a subject.
  - **Node-kind tags,** which churn with grammar versions.
  - **Offsets** (finding-key2 excludes them).
  - **File-global flow-node ordinals.** They would make a node's identity depend on unrelated functions earlier in the file.

**LD-NS12. The declares coverage.** It covers every declaration RPS's `DeclarationKindV1` can express. TypeScript enum members and Rust enum variants are `field`, and catch parameters are `parameter`.
- **Not declared:** imports, `macro_rules!`, tuple-struct positional fields (no kind or no name for them) and, in r2, Rust pattern bindings that are not explicit binding forms (LD-NS8).

**LD-NS13. The `valueText` representation.**
- A long literal keeps a digest-suffixed prefix, rather than being dropped or silencing the file.
- **Rejected:**
  - **Dropping the fact.** That would put a hole under a `complete` Coverage.
  - **`truncated:nodes` for the file.** One embedded blob would silence every fact in the file.

**LD-NS14 (r2). Statement-level control flow, traversed only through the role tables.**
- **Rejected:**
  - **Expression-level control flow.** That needs an evaluation-order law per language, which is much larger and adds risk.
  - **Leaving control flow unspecified.** The cell is SUPPORTED-DESIGN (NCM:269).
  - **Keeping the `unsafe_block` block role.** It contradicted the opacity of the unsafe block, which is a body of its own (RF-SYNNS-4).
  - **Entering a do...while at its test** (r1, RF-SYNNS-5).

**LD-NS15. near-v1.**
- Shingles compare as exact framed-token strings, not hashes, so there are no collisions.
- `.ts` and `.tsx` bodies may pair, since both are body language `typescript`. JavaScript never pairs with TypeScript in this mode (`cross-tsjs` is not selected).
- The order of members and edges is fixed, so a group digest is deterministic.

**LD-NS16 (r2). The parents are NE, IE, FIP, the selected IDS copy and RPS: the accepted inputs the documents implement.**
- There is no copy and no override.
- The IDS parent is SYN-1F's copy, which is the selected identity text now that SYN-1F is bound. Its `normalization-specification-map` definition is byte-identical to the frozen file's.
- **Rejected:**
  - **The frozen IDS.** It is no longer the selected text.
  - **E1's snapshot as a parent.** It would order SYN-NS after SYN-1 for no content reason.

**LD-NS17. `readable/` is in the subject.** Canonical bytes are one line each, so a pretty-printed twin makes review practical. The build derives it, and it is not normative.

**LD-NS18 (r2). Fixtures as design evidence: a small oracle over hand-written trees.**
- The lead asked for CODEX2's ASI case and two-function case as fixtures. Running a parser is outside this docs-only lane. So each fixture states its source and the visible tree tree-sitter yields for it.
- `reference_syn_ns.py` applies these documents' own tables to those trees. The check compares the result with hand-derived expectations, and also applies r1's rule to show each finding's defect.
- The oracle covers the token and comment laws for every row, and JavaScript-family control flow for the roles the fixtures use. L3 renaming, switch, try, throw, match and the Rust graph are outside it. E2c's fixtures run the real parser and should include these six cases.
- **Rejected:**
  - **No fixtures.** The lead required two.
  - **Running E0's harness to get trees.** That is a parser run outside this lane.
- **On the ASI rule.** An exact "ASI cannot apply" rule was considered, for example marking statement nodes that end without an explicit `;`. It would have to be proven complete for every newline-sensitive production of three grammars, and that proof is not available. So the lead's simple rule is used.

## Deviations from E1 r3 (record items for E1's next revision)

- **E-7** (shared with SYN-1, accepted there). A12 covers the level specifications' names and the anonymous tokens the tables name (LD-NS2).
- **E-9.** Item 14's placement of the comment, directive and local-binding tables moves into the level specifications (LD-NS2).
- **E-10.** Item 6's selection rule is evaluated as of SYN-NS, at E0's pins (LD-NS3).
- **E-11.** Item 13's "What E2c fixes, inside `normalizer.v1.json`, which SYN-NS reviews" becomes: SYN-NS fixes it, and E2c implements and tests it (LD-NS1).
- **E-12 (r2).** NE §6.3's Rust L3 list ("local let bindings, parameters, closure parameters, pattern bindings") is narrowed to explicit binding forms, and to bodies without a macro or attribute (LD-NS8, LD-NS9). This is a recall limit, not a change to what L3 means.

## Cross-law items and obligations

- **E2a (SYN-LANE).** Places the six members at their tree paths unchanged. Writes the manifest's `normalizer` object exactly as `materialization-map.json` gives it, and pins the grammars at E0's commits (LD-NS3).
- **E2b.** A12 checks every name in `normalizer.v1.json` and in the four level files, including the anonymous tokens (now also `ref`), against the linked `Language`'s `SymbolTableV1` (under T-native).
- **E2c.** Implements bodies, subjects, declares, literals, control flow, the four levels and near-v1. Its fixtures freeze after this unit's acceptance, and should include `evidence/fixtures.json`'s six cases run on real trees. It should also add a test per stated limit, and a soundness test per L3 condition, R1 to R5.
- **H.** The syntax join admits the candidates these tables produce: one anchor each; subjects as defined here.
- **C, CRC-1, J1.** None.

## Points for the reviewer

- **R1 (RF-SYNNS-1).** Is the line-break rule sound for every JavaScript-family row, at L1, L2 and L3? Is the L2 comment rule right?
- **R2 (RF-SYNNS-2, -3).** Do the explicit binding forms and the macro and attribute disqualifiers close every case where a Rust path, constant or macro-introduced name could be renamed?
- **R3 (RF-SYNNS-4, -5, -6).** Is the traversal now complete and unambiguous, with the role tables the only authority? Is the posttest entry rule right? Are the identities injective across graphs?
- **R4 (fixtures).** Do the fixtures' trees match the pinned grammars for these sources? Do they discriminate the r1 defects?
- **R5 (NB-SYNNS-1, -2; the IDS parent).** Are the observations resolved? Is the IDS parent change right?

## Binding

After `ACCEPT-DESIGN-UNIT`:
1. Copy the accepting review to `docs/implementation/m3/reviews/codex2-syn-ns-r2/review.json`. r1's REQUIRED-FINDINGS review is kept in `codex2-syn-ns-r1/`.
2. Complete `syn-ns-unit.json`, which the builder emits with that review path.
3. Append the entry. It has no ordering dependency.
4. Run plain verify_design.

The binding changes no product byte. E2a and E2c consume the bytes later.

## Evidence runs

All runs used `python3.14 -I -B` at `nice -n 19`, read-only.
- **`build_syn_ns.py`:** run, then `--check` twice; the bytes were identical.
- **`check_syn_ns.py --deps <offline jsonschema 4.25.1>`:** passes.
  - All four grammars' `parser.c` and `node-types.json` equal their E0 pins.
  - Every kind, anonymous token and field named resolves: 106, 115, 133 and 127 distinct references for javascript, rust, tsx and typescript.
  - Every member re-encodes canonically with the real `canonical.py`.
  - The map validates with the design's `ExactValidator` against the selected IDS copy.
  - The parameters equal NE §6.2.
  - All six fixtures match. r1's rules reproduce the defects of RF-SYNNS-1 (both ASI fixtures), RF-SYNNS-3 and RF-SYNNS-6 on the same inputs.
  - Negative probes confirm the walk refuses a wrong kind, a wrong field, a field not on its kind, an unchecked key, an anonymous token named as a named kind, and a hidden supertype.
- **`verify_scratch.py --rev 218465f`:** binds, 91 → 92. `--chain` skips the bound SYN-1 and SYN-1F and gives the same result. The selected inventory and the inheritance projection are unchanged.

## Not claimed

- No parser, normalizer or corpus was run. The tables are checked for names and structure, and the fixtures run a small oracle over hand-written trees. E2c's fixtures on real trees are the executable evidence.
- The L3 soundness argument is a design argument. Its premises (binding classification, scope lookup and no unseen binders) are now made true by construction, at a cost in recall.
- No semantic equivalence is claimed by any level or by near-v1 (NE §6.1).
- No Python, data-format or `cross-tsjs` content is included.
