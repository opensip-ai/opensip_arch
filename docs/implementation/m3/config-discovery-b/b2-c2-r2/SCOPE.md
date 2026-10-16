# B2-c2 r2: the JSONC reader and effective `allowJs` (M3-B unit B2-c, sub-unit B2-c2)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 2.** It implements section 2.2 of the accepted B2-c plan r2 (Codex `codex-b2c-plan-r2`) under accepted law **M3-B r8 item 14a** (`../PROPOSAL-r8.md:567-680`, Codex `codex-m3b-r8-r3`), as accepted **M3-B r9** amends its reading grammar (`../PROPOSAL-r9.md`, Codex `codex-m3b-r9-r1`).

## r2 changes (Codex `codex-b2c2-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2C2-R1-RF-1:** accepting an empty document needs an accepted law change | **The law is amended.** M3-B r9 was drafted, and Codex accepted it with no findings (`codex-m3b-r9-r1`; published at arch `a06251386`). Item 14a's grammar now says: a file holding only whitespace and comments reads as an empty object, and the root value and `compilerOptions` must be objects, `null` included as the wrong type. The reader's behaviour is unchanged. LD-B2C2-2(a) and (h) now cite r9 instead of standing as lead decisions. The tool pins `PROPOSAL-r9.md`, and the code cites r9. **New vectors (r9's controls):** an empty base and a comment-only `jsconfig.json` base, each read as an empty object. |
| **B2C2-R1-RF-2:** the Python oracle conflated a JSON `null` with an empty document | `parse_jsonc` now returns a distinct `EMPTY` sentinel for a whitespace-and-comments document, so a parsed `null` reaches the object check and is `malformed`, as the Rust is. **New vectors:** a `null` root, a `null` root with comments, a `null` `jsconfig.json` root, and a `null` base. **Mutations:** `null-root-as-empty` (Rust) and `reference-null-as-empty` (tool). |
| **B2C2-R1-RF-3:** inherited options were evaluated without a cache, so the work was exponential over repeated edges | **Postorder evaluation, in both implementations.** A node's inherited `allowJs` and `checkJs` are computed once, when the node is done. Every base is done by then, because the graph is acyclic, so each base's value is read and never recomputed. Each edge is merged once, repetitions included. The result carries `Work { node_evaluations, edge_merges }`. The Rust tests assert, for every case, that the work equals the node count and the total edge count, and equals the reference's recorded counts; the reference asserts the same of itself. No wall-clock timing is involved. Repeated edges stay in the graph, and declaration-order precedence is unchanged. **New vectors:** a 32-node chain with 64 repeated edges per file (32 evaluations, 1,984 merges), and shared bases repeated 32 times (4 evaluations, 192 merges). **Mutation:** `edge-merge-uncounted`. |

**Evidence.** Lane r2 (`evidence/checks-r2/`). Lane r1 was round 1's, kept in the r1 package.

**Authorities:**
- **The law:** M3-B r8 item 14a, the pre-Plan TypeScript configuration graph, with r9's reading grammar. It fixes the grammar, the bounds, the specifier grammar, normalization, candidate order, graph identity, custody, the derivation, the four refusals and their public termination, and the controls.
- **The public record:** successor S10, design unit S10-TSC (Codex `codex-s10-tsc-r1`, ACCEPT-DESIGN-UNIT; contract successor 167, product lock `1f70dba`). It provides the public detail `native.typescript-config-unresolved`, its four alias rows, its D9 row, its remedy, the product vocabulary and `REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED`.
- **The matrix row:** M3-J1 r7 item 10 row 59 (Codex `codex-host-pipeline-j-r7`, ACCEPT; arch `a35987d70`). It places this refusal in the host outcome matrix. S10-TSC's LD-4 left the row and its observation to this unit.
- **The meaning:** NE:527-545 (effective `allowJs`) and NE:1330-1345 (`TypeScriptConfigGraphV1`).

**Base.** Product `1f70dba` (167 contract successors, inventory v201); architecture `a06251386` (M3-B r9 published).

## What changes

| Path | Change |
| --- | --- |
| `crates/host/src/jsonc.rs` | **New: the first-party JSONC reader** that C2 will share. It parses RFC 8259 JSON plus `//` and `/* */` comments and one trailing comma per container. A duplicate key keeps its last value at its first position. The parser is **iterative over an arena**, so no input recurses, either while parsing or while dropping the result. It returns the whole document (values, number lexemes, strings), so C2 can read more fields than this unit does. It is pure. |
| `crates/host/src/typescript_config.rs` | **New: item 14a.**<br>• The closed specifier grammar (`classify`), with lexical normalization and containment.<br>• The candidate lists, for path and package specifiers.<br>• `ConfigSource`, the custody trait (C1's; a test tree until then).<br>• `effective_allow_js(entry, source)`: the graph walk in declaration order, cycle and 32-node checks on canonical node identities, the 64 KiB check, and NE:527-545's inheritance, evaluated once per node in postorder (r2; its `Work` counts are returned). It returns the effective `allowJs` and `checkJs` and the `TypeScriptConfigGraphV1` value (each node's path, content SHA-256, kind and every edge).<br>• The four internal keys (`ConfigRefusalKey`) and the refusal's subject.<br>• `TYPESCRIPT_CONFIG_ALIASES`, the four S10 alias rows, and `public_detail`.<br>• `observe_effective_allow_js`, the composition with U-1 (LD-B2C2-6).<br>Pure: it has no I/O of its own. |
| `crates/host/src/outcomes.rs` | **Row 59:** `Observation::TypescriptConfigUnresolved(ConfigRefusal)` projects to request-rejected 2, `CONFIG.INVALID`, detail `native.typescript-config-unresolved`, S10's remedy and the bounded subject `<internal key>:<path>`, with no runId, executionId or operational key. The remedy's doc comment names the row. |
| `crates/host/src/invocation.rs` | `commit_evidence`'s exhaustive match: row 59 carries no commit evidence, like every other pre-Plan refusal. |
| `crates/host/src/outcomes_tests.rs` | The item-10 matrix gains row 59. The coverage set becomes rows 2 to 59, without 41, 45, 48 and 50 (as before) and without 58. Row 58, SYN-1's syntax backend fault, still has no observation in the product; that gap predates this unit and is disclosed here. |
| `crates/host/src/typescript_config_tests.rs` | **New. Eight tests:**<br>• every law control replays with its whole result: the options, the graph in canonical bytes, or the refusal's key and path, plus every path the reader asked the source for, in order, and (r2) linear evaluation work;<br>• the seven units cases from configuration bytes;<br>• the composition reads only surviving configuration markers, and a refused discovery reads nothing;<br>• an entry the source does not hold is an internal fault;<br>• the alias map is S10's registry rows, and unknown keys refuse;<br>• row 59 projects S10's termination, with a long path and a non-ASCII path bounded as the model bounds them;<br>• deep nesting at the 64 KiB bound neither overflows nor refuses;<br>• duplicate-key position and value. |
| `crates/host/src/typescript_config_vectors.json` | **New, generated** by the tool below. |
| `tools/host/typescript_config_vectors.py` | **New: the vector tool** (`--check` / `--write`), with an independent Python reading of item 14a (LD-B2C2-8). |
| `crates/host/src/lib.rs` | `mod jsonc;`, `mod typescript_config;` (library only, `#[allow(dead_code)]`), and the macOS test module. |
| `tools/tests/test_discovery_fw01.py` | FW-01 covers both new files. A new purity check finds no filesystem, environment, I/O, process, network, platform or `libc` name in either file, with planted negatives. |

## Lead decisions

**LD-B2C2-1. Two modules, the discovery instrument untouched.** `jsonc.rs` is the reader C2 shares (item 14a: "one first-party function"). `typescript_config.rs` is the graph. `discovery.rs`, which B2-c1 bound, is unchanged: U-1 still reads `allowJs` from the marker observation, and LD-B2C2-6 supplies that observation from bytes. **Rejected:**
- a crate, which item 14a rejects (a dependency-policy row for a small grammar);
- folding this into `discovery.rs`, which would reopen a reviewed file and its vectors for no behavioural need.

**LD-B2C2-2. What "JSONC data" means where item 14a is silent.** Item 14a says: JSON with `//` and `/* */` comments and trailing commas, and duplicate keys last-wins. The rest is strict RFC 8259:
- **(a) An empty document** (only whitespace and comments) reads as an empty object. **(r2) This is now law: M3-B r9.** Round 1 made it a lead decision, citing TypeScript's design, which says a `tsconfig.json` "is permitted to be completely empty" (microsoft/TypeScript PR #1692). Codex required a law change (B2C2-R1-RF-1), and r9 is that change.
- **(b) A leading UTF-8 byte order mark is ignored,** as RFC 8259 §8.1 permits a parser to do.
- **(c) A line comment ends at LF or CR,** JSON's own line-ending whitespace. U+2028 and U+2029 are ordinary characters inside a comment.
- **(d) A `\u` escape of a lone surrogate is malformed:** it names no Unicode scalar.
- **(e) Strict elsewhere:** RFC numbers (no leading zero, `+`, `NaN` or hex), the three literals, and RFC escapes. No single quotes, no unquoted keys, and no raw control character inside a string. The input must be UTF-8.
- **(f) One trailing comma per container,** after its last member. `[,1]`, `{,}` and `,,` are malformed.
- **(g) No depth bound.** The reader is iterative, so the 64 KiB file bound is the only bound, and no refusal beyond item 14a's four exists. A test parses 32,768 nested arrays on a test thread's stack.
- **(h) Types (r2: M3-B r9 states the object requirements).** The root must be an object. `compilerOptions`, where present, must be an object. `allowJs` and `checkJs` must be booleans, so `null` is the wrong type. `extends` must be a string or an array of strings. Anything else is `malformed`, as the remedy text states.

**LD-B2C2-3. Resolution where item 14a's list needs an operational reading:**
- **(a) A link on any candidate's path refuses at once** (`extends-unresolved`), even when a later candidate is a regular file. Skipping it would silently choose a file that C1's custody might not choose. Item 14a: "a link is unresolved".
- **(b) Containment is decided per candidate spelling,** before any file is consulted. If either spelling of a path specifier rises above the root, the specifier is unresolved.
- **(c) A candidate that normalizes to the root** (`""`, for example `./a/..`) is the project directory, never a file. It is skipped without asking the source. Its `.json` spelling is still a candidate (`a/...json`).
- **(d) The law's lists are taken literally.** A non-empty package subpath ending in `.json` still has the `P.json` candidate (`pkg/strict.json` then `pkg/strict.json.json`). At E = a `node_modules` directory, the list probes `node_modules/node_modules/N`, which is harmless.
- **(e) A candidate below a regular file** (`a/b` where `a` is a file) is not a file.

**LD-B2C2-4. Walk order and the refusal's subject.**
- **The order.** The walk is depth-first, in `extends` declaration order. A file's fields are read before any of its edges are resolved. For a new node, the 32-node check comes first, then the 64 KiB check, then JSONC and types.
- **The subject** is the internal key and a path:
  - for a malformed or unresolvable specifier, a cycle, or the 33rd node, the file whose `extends` holds the edge;
  - for an oversized, non-JSONC or wrongly typed file, that file itself.

  So the first refusal is deterministic, and both implementations agree on it.

**LD-B2C2-5. The entry.** The entry is a marker path from the admitted marker inventory.
- **A link** at or above the entry refuses `extends-unresolved` with the entry's path (before C1, item 14a).
- **A non-canonical path, or one the source does not hold as a regular file,** is an internal composition fault with no public detail: the inventory and the source disagree, which only a host defect produces.

**LD-B2C2-6. The composition with U-1** (`observe_effective_allow_js`):
- **Two passes.** Discovery runs once with the raw marker observations. Then, for each surviving `tsjs` unit whose marker is `tsconfig.json` or `jsconfig.json` (U-1's first present marker), the effective value is read from bytes and set on that marker, and discovery runs again.
- **Why it is sound.** Discovery alone decides which directories survive, and `allowJs` changes only U-1's mode. So the second pass gives the same units with their modes decided. For the seven units cases, the result equals the reference's discovery over the case's trusted observation.
- **What is read.** A refused discovery reads nothing, and a marker inside a pruned tree is never read. The first refusal in unit order wins. J1 calls this composition, so its function has no production caller here.

**LD-B2C2-7. Row 59, as M3-J1 r7 places it.** The projection is item 14a's three steps:
- the alias to `native.typescript-config-unresolved`;
- that detail's D9 row: request-rejected 2, `CONFIG.INVALID`, no fault cause;
- S10's remedy, keyed by the detail and never `CONFIG.INVALID`'s.

The subject is bounded by NES `subjectBoundLaw` through the existing `bounded_subject`.

**LD-B2C2-8. The oracle is the law, checked three ways.**
- **(1) The tool's case table** writes each of item 14a's controls with the result the law gives it, by hand: 121 cases, 71 of them refusals (r2). An independent Python reading of item 14a must give every one, or generation fails (mutation `law-expectation-altered`). That check caught one error while the table was being written: an expected value that the law's "a written `allowJs` wins after inheritance" contradicts. The expectation was corrected to the law.
- **(2) The model admits every graph.** It validates as `TypeScriptConfigGraphV1` in the S10 native model copy, with no `typescript_config_graph_faults`, each kind from the model's `config_node_kind`, and the origin from `typescript_config_origin`.
- **(3) The B2-c0 reference runs the units cases.** The vectors record every read, so the Rust must consult the same candidates in the same order.

**Rejected:** a separate reference design unit before the code. Plan r2 names none for B2-c2, and the law already fixes every result the controls test.

**LD-B2C2-9. A duplicate key is not recorded.** Plan r2 §2.2 said a duplicate key "is recorded". Accepted item 14a, which came later, says only that it "keeps its last value", and `UnitDiscoveryV3` is closed, so no record could carry it. The law governs.

## Open items (recorded, not resolved)

- **O-1, `extendsResolved` has a 64-entry bound that item 14a lacks.** `TypeScriptConfigGraphV1.nodes[].extendsResolved` has `maxItems: 64`. Item 14a bounds file bytes and graph nodes, but not edges per node. A single file whose `extends` array holds more than 64 entries, repetitions included, gets a correct effective `allowJs` here, but its graph value has no admissible `TypeScriptConfigGraphV1` record. **Routed to the lead, for C2:** before C2 emits graphs, either item 14a gains an edge bound under `native.typescript-config-bound`, or C2 decides otherwise. B2-c2 emits no record and claims nothing for that case.
- **O-2, the read set.** The graph's nodes are exactly the files read. C1 enters them in the snapshot inventory, as `host-ignore-convention` rows under a pruned tree (NE:735-741).
- **O-3, production custody.** The `ConfigSource` implementation is C1's, and J1 composes it. Until then every link refuses.

## Checks

Lane r2 (`evidence/checks-r2/checks.json`):
- the host suite at base and candidate, with equal failure sets and eight new passing tests;
- rustfmt on the new and base-clean edited files;
- warning-denied all-targets Clippy;
- the TypeScript configuration vectors `--check`, and the B2-c1 unit vectors `--check`, which are unchanged;
- FW-01 with its planted negatives;
- the host TypeScript configuration and outcome tests;
- the operability source census;
- verify_design.

**Mutations.** Each must make the host tests (product) or the vector check (tool) fail:
- `jsconfig` default dropped;
- later `extends` loses;
- own loses to base;
- `checkJs` derivation dropped;
- the `.json` candidate first;
- nearest `node_modules` last;
- a link skipped;
- the node bound off by one;
- the file bound off by one;
- an escape clamped;
- an upper-case name admitted;
- an empty document refused;
- cycles unchecked;
- an alias row altered;
- duplicate keys first-wins;
- a lone low surrogate accepted;
- a BOM refused;
- row 59's remedy dropped;
- a law expectation altered;
- the reference's candidate order swapped;
- (r2) a `null` root read as empty, in the Rust and in the reference;
- (r2) an edge merge left uncounted.

## Inventory

New paths, for inventory v202:
- `crates/host/src/jsonc.rs`;
- `crates/host/src/typescript_config.rs`;
- `crates/host/src/typescript_config_tests.rs`;
- `crates/host/src/typescript_config_vectors.json`;
- `tools/host/typescript_config_vectors.py`.

## Not claimed

- No production caller or custody source (J1, C1).
- No C2 projection, and no graph record emission (O-1).
- No compatibility with TypeScript's full resolver beyond item 14a's candidates: no `exports` conditions, no `package.json` `tsconfig` field.
- No qualification.

B2-c is not complete until inventory v202 binds, and B2-b is not complete until B3-b.
