# E1 r5 — REQUIRED-FINDINGS

M3-E1 r5 is a record revision of the syntax law. Three recordings add a rule, or drop a form, that the cited ruling or accepted review does not state. The rest of the revision matches its sources.

The subject is `docs/implementation/m3/syntax-e/PROPOSAL.md`, 161,442 bytes, sha256 `2c268a07193e1c32c7d7abad4b3573d70fe5ad597b90d4b0655b5cb60e9b3ae2`. The diff base is `PROPOSAL-r4.md`, 133,352 bytes, sha256 `ed4f1fec5a7e11293f48724e349afc0ca8bf9b7b2e46e761efac25a4f7d8764c`. No product build, cargo, test, lane or verifier was run. `~/Library/Application Support/OpenSIP` was absent.

## What holds

The lead's rulings on E2a's calls 1, 3, 4 and 5 are in the items the request names, with the rejected alternatives, apart from the two additions in E-R5-1 and E-R5-2.

- E2a ships no manifest and no receipt. E2b writes both. `buildReceiptSha256` stays non-null under `native-linked-v1`.
- The T-native limits object is `{maxFileBytes: 4194304, maxNodes: 4194304, maxDepth: 4096, operationBudget: {base, perByte}}`. E2b measures the constants on a native T2a run.
- `parserVersion` is lane-assigned, one semantic version per distinct tree, with `-dev.N` on a development closure (items 5 and 6).
- A member an archive omits is retained from the pinned tag by sha256 and git blob. SYN-DEP checks it against the lane pin. The one such member at E0's pins is the typescript `LICENSE`.
- `SyntaxTreeV1`'s layout is E2b's, in `parser.rs`: E0's layout, symbol 0xFFFF tied to the error flag (SYN-1 LD-2), fixed with tests (item 2 and item 20).
- `shim` is null under T-native beside `module` and `shimAbi` (item 4, A7, E2-T25). A non-null shim under `native-linked-v1` refuses.

Calls 2, 6 and 7 match the E2a review. Item 6 reads the compiled set as the crate build's include closure: wasm-stdlib stays out, and the tsx row lists `typescript/src/tree_sitter/parser.h`. Item 4 names the four format URLs and the layout and notices, including the grammar licence plus the runtime's MIT and ICU licences.

The record items match the lane and the E2a review. A11's bound is 65,534 symbols. ERROR (`0xFFFF`) and ERROR_REPEAT (`0xFFFE`) are never rows, so the ids run from 0 to at most 65,533. `grammar_lane.py` sets `MAX_SYMBOLS` to `0xFFFE`. `test_error_symbols_are_never_rows` replaces `SYMBOL_COUNT` with 65534; the fixture's `ALIAS_COUNT` is 1, so the refused table has 65,535 symbols. `SymbolTableV1` is the accepted form: canonical encoding, `named` as named and visible, `visible` as the visible flag, fields from 1 to `FIELD_COUNT`, supertype false/false, and no type field. The host crate count and SYN-DEP's own policy are E2b's. The count of 8 is T-wasm's and inactive. P0's `selectionRule` at product `1799d3d` admits pure Rust with no build script, `links` key or C, and `forbid(unsafe_code)`, which leaves the tree-sitter crates to SYN-DEP. The wasm headers and eager compilation stay inactive.

Item 14b matches C8. X-10 at C8:1272 is the stage reading r5 uses. Membership is a syntax universe or a requested `inventory` cell (C8:510, C2-T13 at C8:545). The TypeScript and Rust negative stops at a use-3 inventory record (C8:539, C2-T13a at C8:546-553). Use 3 is the three inventory relations and the four fields (C8:497-509). Use 2 at C8:488-495 is C r7's use 2 word for word, including the five fields and the syntax-only bound. The syntax stage, its outputs and E's syntax interface stay as r4 has them. The forbidden substitute, E3-T13, E3-T14, the acceptance gate, item 19's X-C1 row, item 20's C4a leg, section G and owner note 4 carry the widening. NB-MC8-1's fix is taken up. Its old line cites are corrected to the r8 snapshot's :510, :545-553 and :1272, as row 8 says.

The C r7 passages r4 cites are unchanged in r8 except the three places the short name names: item 9's core provider closure, C2-T13 and C2-T13a, and the C2a row, which in r8 adds the no-trust-view rule. r5 keeps those citations on C r7.

E2a is accepted, inventory v138, and it integrates after J2a. The rust 0.24.2 archive VCS commit is `e2bee853694a1d3e0f6ef308fe3674542fec95d7`. The tag commit the definition names is `77a3747266f4d621d0757825e6b11edcbf991ca5`. Retained members equal the tag. The lane pins the archive VCS as the archive carries it.

The two rulings on r5's draft are recorded as ruled. Operation-budget exhaustion is `truncated:fuel` in items 5 and 11, and the rejected alternative is a new outcome value. A8's range is an E2b proposal from the native T2a measurement, fixed by E1's next revision before E2b integrates. The law sets no number and mints no outcome.

E-9, E-10 and E-11 are applied. The comment, directive and local-binding tables live in the level specifications. The selection rule is read as of SYN-NS at E0's pins. SYN-NS fixes the declares, literal and control-flow tables, and E2c implements them. Item 19's SYN-NS cell says bound at `6190e66`. Item 20's E2c gate is met. The body no longer marks those items pending. The pending wording remains in r4's header and r4 changes table, which row 13 keeps as history. LD-NS1, LD-NS3, E-7 and E-9 to E-11 say the same in the r2 README as in the retained r1 README. r2's LD-NS2 also puts `lineTerminators` in the level files, and the short name says so (E-R5-NB-1).

Every diff region is one of the fifteen rows, or the questions sentence in E-R5-NB-2. E-R3-NB-01 stays open, as the header says.

## Required findings

### E-R5-1 — the operation-budget formula collapses P6

Item 11 says the operation-budget constants are derived by E0's P6 rule, as `fuelBase` and `fuelPerByte` were (E0R:264-265): 4 × the T2a maximum, rounded up to two significant figures. Row 2 says the same and cites those two lines.

E0R:264 derives `fuelBase` that way: 4 × the maximum fuel over the 23 empty files, rounded up to two significant figures. E0R:265 derives `fuelPerByte` as the ceiling, over non-empty files, of (4 × fuel − base) ÷ bytes, and then rounds that ceiling up to two significant figures. The T-native object has both `base` and `perByte`. A sentence that gives both constants the base formula tells E2b to freeze `perByte` by a rule P6 does not use. The limits are identity-bearing.

The lead ruling on call 1 names E0's P6 rule. The recommendation's parenthetical compresses it. Item 11's colon then treats both cited lines as the base formula.

**Fix.** Keep the derivation as E0's P6 rule, measured by E2b on a native T2a run. State `base` as E0R:264 states `fuelBase`, and `perByte` as E0R:265 states `fuelPerByte`.

### E-R5-2 — the receipt defines a compile model the ruling does not

Item 4 says a compile model is a member set's compile roots, include directories and undefined macros, and it attributes that definition to the lead ruling on E2a's call 1.

The ruling, and the recommendation it accepts, say the T-native receipt records the crate archives and the compile models that build the linked code, with toolchain fields null. They do not list those fields. Item 6 already records call 2: the compiled member set is the include closure of the build's roots and include directories, and branches under an undefined macro drop out. That is the member set. It is not a receipt schema the call 1 ruling fixed.

**Fix.** Record the receipt as the ruling states it. Leave the compile-model fields for a ruling that fixes them.

### E-R5-3 — the E-12 list drops `ref mut x` and the declares half

Item 14 says only these forms rename: `ref x`, `mut x`, `x @ p`, `let mut x`, a `mut x: T` parameter, and `S { mut a }` or `S { ref a }`. A Rust body with a macro invocation or an attribute gets no L3 renaming.

LD-NS8's closed set is `ref x`, `mut x` (also `ref mut x`), `x @ p`, `let mut x`, a `mut x: T` parameter, and `S { mut a }` or `S { ref a }`. The same pattern law serves declares extraction, so a plain local or parameter gets no declares fact. The SYN-NS review's stated limits, which row 14 cites, say Rust L3 and declares cover only the explicit binding forms.

The item 14 list is the operative narrowing. It omits `ref mut x`, and it records the limit for renaming only.

**Fix.** Record LD-NS8's set, including `ref mut x`, and record that declares extraction uses the same forms. Keep LD-NS9's disqualification for a macro or an attribute.

## Non-blocking observations

**E-R5-NB-1.** r2's LD-NS2 places `lineTerminators` in L1, L2 and L3. The short name says so. Item 14's E-9 sentence names the comment, directive and local-binding tables, which is the text of E-9. The bound level files carry `lineTerminators`.

**E-R5-NB-2.** The questions closer adds one `(r5)` sentence: this request asks whether each r5 change is faithful to its source. That sentence is outside the fifteen rows. It decides nothing.
