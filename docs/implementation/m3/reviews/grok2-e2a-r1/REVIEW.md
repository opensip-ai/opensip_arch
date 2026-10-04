# E2a r1 — ACCEPT-UNIT

Unit E2a r1 of law M3-E1 r4 (SYN-LANE, the grammar closure lane under T-native) and inventory v138 are accepted. There are no required findings.

The subject is the worktree diff at `/Users/sb/code/opensip-ai/opensip-e2a`, detached at `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1`. Its sha256 is `1c4234ad08138711a7b0894d4c54ae068423e3c0ed3e372e608e58b84ab825d4`. The subject manifest sha256 is `29fc0ed2929591efeac060df7cfeab5f7b7090ab7735bf0d971bc2f287d2550f`. `~/Library/Application Support/OpenSIP` was absent before the lanes and after them.

## What this unit does

Item 20's T-native note is the operating branch: E2a is the definition records over the crate archives, the SymbolTableV1 digests, the closure layout of those records, the upstream pins, and the reproducibility check. The lane places SYN-NS's six members at their tree paths unchanged and pins the four grammars at E0's tag commits. `tools/grammar/grammar_lane.py` reads the four pinned crate archives in memory, never unpacks them, and never executes upstream code.

The lane leaves the bundle manifest and the build receipt unproduced. `materialize` reports both paths in `notProduced`, and `productQualification` is false. E2b owns the manifest, the receipt, `grammar.rs`, `parser.rs`, SYN-REG, SYN-DEP, and the admission recomputation of SymbolTableV1 from each linked `Language`. E2c owns the normalizer implementation. E2s is later. `crates/syntax` is untouched. No Rust source, Cargo.toml, Cargo.lock, dependency policy, schema, registry, or generator input changes. The X9 harness sources are outside the diff, so this review ran no crash-matrix lead set.

## Judgment calls

**Call 1.** E2a correctly leaves the bundle manifest and the build receipt unwritten. Item 11's limits stay with E2b, under the lead's accepted reading: the T-native limit object comes from a native T2a run that E2b measures, development closures use a lane-assigned `parserVersion` with `-dev.N`, and the T-native receipt records the crate archives and compile models with null toolchain fields. `lane.json` pins the manifest's normalizer object, and that object equals SYN-NS `materialization-map.json`: `opensip.syntax.normalizer`, version `1`, specification path `opensip-interface/grammar/normalizer.v1.json`, digest `e4a648f015945b0749af6314b83d62a51df94031457a0cad6b0f54f2718b5867`. E2b writes the manifest that carries it.

**Call 2.** "Every source member it compiles" (item 6) is the crate build's include closure. The tree-sitter 0.27.0 `binding_rust/build.rs` compiles `lib/src/lib.c` with include directories `lib/src`, `lib/src/wasm`, and `lib/include`, and it defines `TREE_SITTER_FEATURE_WASM` only when the wasm feature is set. `lib/src/lib.c` guards `wasm-stdlib` with `#ifdef TREE_SITTER_WASM_STDLIB`. The lane's undefined macros are those two names, and an `#ifdef` of an undefined macro drops that branch. The only `TREE_SITTER_FEATURE_WASM` guard in the crate sources is `#ifdef` in `wasm_store.c`, which `lib.c`'s closure does not pull in. `lib/src/wasm-stdlib/**` stays out. The check reports 44 runtime sources.

The typescript 0.23.2 crate compiles both grammars with `-I typescript/src`, and it reruns on `common/scanner.h`. The tsx record therefore lists `typescript/src/tree_sitter/parser.h` beside `tsx/src/tree_sitter/parser.h`. Both files are 7039 bytes and sha256 `a1f6ef161fba…`. The javascript and rust crates compile `parser.c` and `scanner.c` with the grammar `src` directory on the include path, and rust's scanner also pulls `src/tree_sitter/alloc.h`. That is the compiled set the lane requires.

**Call 3.** A pinned member the archive omits stays, taken from the pinned tag by sha256 and git blob. `tools/grammar/upstream/tree-sitter-typescript/LICENSE` is 1080 bytes, sha256 `49bf33cf78ef5897e4e161ce1517df7de1ae5042a65b6bcfd44401e0fc606559`, git blob `aa9f858db5722d9576104726471b11cc0e31f131`. The 0.23.2 crate archive contains no `LICENSE`. The member's source is `retained`, and the lane refuses a retained copy that shadows an archive member. SYN-DEP checks it against the lane pin.

**Call 4.** SyntaxTreeV1's layout is E2b's. E2b adopts E0's layout, ties symbol `0xFFFF` to the error flag (SYN-1 LD-2), and fixes it in `parser.rs` with tests. E2a has no serializer. Leaving the layout open here is correct.

**Call 5.** `shim` is null under T-native. Item 4's code-row shape lists `shim` as `{path, sha256, bytes}` and says `module` and `shimAbi` are null under T-native. Under T-native the closure has no shim source. The eight code records carry `shim`, `module`, and `shimAbi`, each null, and `test_definition_records` requires that triple. A path to a file that does not exist would fail A6. E1 r5 records the null case.

**Call 6.** The data-document format references are identity-bearing only through `grammarDigest`. The records use JSON `https://www.rfc-editor.org/rfc/rfc8259`, Markdown `https://spec.commonmark.org/0.31.2/`, TOML `https://toml.io/en/v1.0.0`, and YAML `https://yaml.org/spec/1.2.2/`. Each data row has `grammarVersion` `format-definition.v1` and `parse` `none`. No parser is pinned, linked, or run.

**Call 7.** `source/` and `runtime/source/` keep each member's path in the pinned upstream tree, so a relative include still resolves. `notices/<upstream>/<path>` holds a copy of each licence. A code definition's `notices` list is that grammar's licence plus the runtime's MIT licence and the ICU licence of the compiled `unicode/*.h` headers.

## Records and SymbolTableV1

The code rows are javascript, rust, tsx, and typescript. Each record carries `grammarVersion` as the upstream tag, `upstream` as repository, tag, and commit, `sources` and `runtime.sources` as `{path, sha256, bytes}` in path order, the null module triple, `languageAbi`, `symbolTableSha256`, and `notices`. The data rows are json, markdown, toml, and yaml. Canonical records stay within the 1 MiB bound. Grammar digests from this review's check:

| Row | Digest | Sources | ABI |
|---|---|---|---|
| javascript | `6242e6654e9219c789c8742ee3cce21d62282ee03740a0d83dba8bd1b3d33a74` | 6 | 15 |
| rust | `d51ee290721d644a5e09bbd4eb9eb2ed9fc2bda7b88db7aae61013ab78031422` | 7 | 15 |
| tsx | `30106a35bf4d36c90960f88f04155c33d87ca1ce6a0e6ae8dfbd1102a47e256d` | 8 | 14 |
| typescript | `9b52d08bd438bf5926128a3d405a5d3212fa1f571e2f293ef650286243797d1b` | 7 | 14 |
| json | `5c791a92bb21136a3d812e7774e5e8afb29fa4cadbe148dafe4f3d9b74fb99b5` | — | — |
| markdown | `b4b33cc31f3ae5b3742b9239c90f804110595ee11df21aac1a88019ec4f63697` | — | — |
| toml | `acb76e51576580e866a25b3bbe72650988b0eeb407a0b2edd9002fbed41d9f09` | — | — |
| yaml | `013a54dbf26ce65ea077ceec23c19e37d1b7243244d28cb9ca7ecd3376d52d55` | — | — |

SymbolTableV1 is `{schemaVersion: 1, grammarId, languageAbi, symbols: [{id, name, named, visible}], fields: [{id, name}]}`, encoded with the identity crate's canonical profile: UTF-8 key order, the same string escapes, depth 32, and the same integer bounds. `named` is `metadata.named and metadata.visible`, which is `Language::node_kind_is_named`. `visible` is `metadata.visible`, which is `node_kind_is_visible`. A supertype is false/false. Symbol ids are `0 … count−1`. Field ids are `1 … FIELD_COUNT`. ERROR (`0xFFFF`) and ERROR_REPEAT (`0xFFFE`) are never rows. The lane refuses a table above `0xFFFE` symbols, which is r4's A11 exception. The four tables equal E0's native recomputation and E0's wasm decode byte for byte:

| Grammar | Digest | Symbols | Fields | ABI |
|---|---|---|---|---|
| javascript | `5a0738c3c79118e0cca3a32488c797ea2553413d2bef94caad3b379b2ec7b669` | 265 | 36 | 15 |
| rust | `0363b059b8f9b9221615f027acb623aed68604dad2114d05bacbc24b631198d3` | 355 | 31 | 15 |
| tsx | `c8759474552a61a78ce41392187a001e667989ee2d51c68c278dc14aa763d784` | 400 | 43 | 14 |
| typescript | `daa3b99865f2f1a1ac31d4485a0a53e9cdff762ed7944434bb41e3d5b55ebb0c` | 383 | 40 | 14 |

The upstream commits are E0's: tree-sitter `v0.27.0` `6070dbfefd326bd735e5683eb128cc1b57dad0c0`, javascript `v0.25.0` `44c892e0be055ac465d5eeddae6d3e194424e7de`, rust `v0.24.2` `77a3747266f4d621d0757825e6b11edcbf991ca5`, typescript `v0.23.2` `f975a621f4e7f532fe322e13c4f79495e0a7b2e7`. The registry coverage is 7 languages and 14 suffixes. The six SYN-NS members match the materialization map and the product copies. `check_e0_pins.py` passed: 72 members equal E0's tag pins, the law pin is `PROPOSAL-r4.md` sha256 `ed4f1fec5a7e11293f48724e349afc0ca8bf9b7b2e46e761efac25a4f7d8764c`. The script rewrote `evidence/e0-crosscheck.json` with the same bytes (`38f7b5d8521816b6152627697694eb6b066d38be79701daa262682e098458a71`); the original file was restored.

## Lanes rerun

Grammar `check --architecture` passed (8 rows, 4 code, 44 runtime sources, 6 normalization members, 91 tree members). `test_grammar_lane.py` with the pinned archives and `--architecture` was 25 OK. Without archives it was 25 OK, 8 skipped. Two materializations each wrote 91 members. `diff -rq` was empty. Both tree digests are `1510c2c220fe6a29800e3578b9fa7459fdeed29d2eefc99cecc6274845dee5d9`.

Drift passed in staged mode: 40 sources, 8 outputs, `changed: []`, write false. `verify_scratch.py` passed in staged mode with J2a staged in memory: inventory successors 96, then 97, then 98; contract successors 97; inheritance 100, then 103, then 103; 21 inventory and 1 contract passage supersession; 40 generation sources and 48 admission sources; v138 selected. Plain `verify_design` on the staged lock exited 1 with `missing or escaping regular file: SCRATCH-J2A/review.json`. Plain `verify_design` on HEAD's lock passed and selects v136 (555473 bytes, sha256 `ba124e21d23c8cd100eb2031203fd5c04fd8aeaab056872af54d1fa8c92bacea`): 96 inventory successors, 97 contract successors, 100 inheritance rows, 21 inventory supersessions, 40 generation sources, 48 admission sources. `verify_projection.py` passed: 103 rows, 518 corruptions refused.

Package edges against v138 and against v137 are the same host graph: 12 workspace packages, 22 declared internal edges, 20 resolved. The rust-provider lane passes with `opensip-rust-provider` only (2 declared, 2 resolved). `test_package_edges.py` was 14 OK. `check_dependencies.py` was 11 dependencies and 8 local sources. `check_identity_dependencies.py` was 8 dependencies and 305 sources. Their suites were 9 OK and 5 OK.

Under the lane lock, with `CARGO_TARGET_DIR` in this review directory: `cargo fmt --all --check` was clean. `cargo build --workspace --all-targets --locked --offline` finished in 24.41s. Clippy workspace (20.17s), crash-matrix (9.89s), and scenario-fixtures (already fresh from the workspace `--all-targets` check, which follows host's dev-dependency) were clean under `-D warnings`. Workspace tests ran twice, each 1738 passed, 0 failed, 3 ignored, 20 binaries. Doctests were 20 passed. The crash-matrix feature lane was 1636 passed, 0 failed, 3 ignored, including storage `commit_tests` and host `commit_matrix_tests`, with no `OPENSIP_X9_RUN_SET`.

`build_v138.py` was rerun against a scratch clone of the architecture tree, with J2a staged in memory. It reproduced the candidate and the successor byte for byte (995 files, 22 added, 103 projection rows, 103 inherited, 0 direct, 0 supersessions folded, 1 selector moved). The clone was removed.

## Inventory v138

Accepted. The candidate is `docs/implementation/m2/repository-file-inventory.v138.json`, 571539 bytes, sha256 `90d5b09ca552c120b127d597a3a635fcb9de88ba462a67d99e71d937bdfbd5e9`. Its parent is v137, 558538 bytes, sha256 `92226626700a9d44c2a22eea92526aea615cb9b15279169f8ec7e2e88665ce56`. The successor record is `docs/implementation/m2/syntax-lane-e2a-inventory-v138/successor.json`, 309185 bytes, sha256 `0e574e209ed2ccbef33eab9b03c6ef85ed3330b9cb5fb3cd7f9ef9d8d2638c5d`.

v138 is v137 plus 22 tooling rows, all standing `proposed`. 973 inherited file rows are equal by value. Nothing was removed. Packages, edges, and pending decisions are unchanged. The document standing is this candidate's own statement of the grammar closure lane. `tools/README.md` remains a planned row whose description stays true. The 22 descriptions match the files: the lane and `lane.json`, the retained typescript licence, eight definition records, four symbol tables with the counts and ABIs above, six SYN-NS members, and the lane test. The projection is the 103 meanings a lock selecting v137 binds, re-parented to v138 by stable file path.

J2a is still unintegrated. The staged lock is HEAD's lock plus J2a's v137 entry, exactly as J2a's `stage_lock_j2a.py` writes it, and then E2a's v138 entry. Plain `verify_design` refuses at J2a's placeholder, which is the state until integration.

## Observations

These are for later owners. They do not affect this verdict.

The tree-sitter-rust 0.24.2 archive's VCS record is commit `e2bee853694a1d3e0f6ef308fe3674542fec95d7`. E0's tag commit, which the definition record names, is `77a3747266f4d621d0757825e6b11edcbf991ca5`. `check_e0_pins.py` reports `crateFromTagCommit: false` for that one upstream. Every retained member equals the tag's bytes. The lane pins the archive's VCS record as the archive carries it. SYN-DEP's review is the place that checker meets this pin.

No crate is vendored. `check_dependencies.py` covers the contracts closure and `check_identity_dependencies.py` covers identity's. A crate linked into `crates/syntax` is checked by neither until SYN-DEP exists. `crates/syntax` is untouched in this diff. `forbid(unsafe_code)` in that crate stays available under T-native because the grammar crates export safe `LanguageFn` constants and `tree_sitter::Language::new(LanguageFn)` is safe.
