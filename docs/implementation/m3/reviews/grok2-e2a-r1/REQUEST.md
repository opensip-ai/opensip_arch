GROK2 review: unit **E2a** r1 of law M3-E1 r4, **SYN-LANE**, the grammar closure lane under T-native, with **inventory v138**. Claude Opus 5.5 leads, and you are the single reviewer. You accepted E0's report (`reviews/grok2-e0-report-r1`), whose outcome, T-native, this unit builds on. Verdict wanted: **ACCEPT-UNIT** on the product change and inventory v138, with an **`inventoryCandidateAssessment`**. E2a has no contract successor.

**Parent.** v138's parent is **v137**, unit J2a's candidate (`m2/host-invocation-j2a-inventory-v137/`, on v136, which the lock at `d2c00a9` selects). J2a is reviewed separately and is not yet integrated; its README says its file set is final. Until J2a integrates, every E2a script applies J2a's staged entry in memory, from J2a's own `evidence/verify_scratch.py` with its `SCRATCH-J2A/` placeholders, and the E2a worktree's staged lock carries that entry before E2a's own. If J2a integrates before you review, the lead moves the worktree to that main, re-stages (E2a's entry only), and refreshes the diff and lock pins below. The candidate, record and subject do not change.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok2-e2a-r1`.
- You own the native lane for this review:
  - Use a `CARGO_TARGET_DIR` under that directory.
  - Use a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
  - Take the lane lock before each cargo or test run, and release it straight after: `mkdir "$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`, then `rmdir` it. J2a's lanes use the same lock. If it is held, wait.
  - Write every scratch output (metadata, drift and materialized trees) under your output directory, never into either repository.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead run set is needed or wanted (see "Pins checked", X9).

## Inputs

All inputs are pinned in `hashes.txt`. Laws and plans are pinned by their accepted snapshots.

### Law, record and plan

- **The law: M3-E1 r4** (`docs/implementation/m3/syntax-e/PROPOSAL-r4.md`, `ed4f1fec…`, accepted by Codex in `reviews/codex-syntax-e-r4/`). The live `PROPOSAL.md` differs only by the acceptance note.
  - **Item 20** (:740): E2a is "SYN-LANE: the closure layout (item 4), manifest and definition records (items 5 and 6), `SymbolTableV1` digests, fixture modules and the receipt". Its T-native note (:762): "**E2a shrinks to the definition records over the crate archives**, and E2b uses the `tree-sitter` crates".
  - **Item 19** (:728), SYN-LANE: the toolchain pin, the upstream pins, `tools/grammar/` (build, records, receipt), the reproducibility check, labelled fixture modules. Inventory unit, ACCEPT-UNIT.
  - **Item 3's reading rule** (:192): every passage that applies only to T-wasm, "text that concerns the module, `wasmi` or the shim ABI", is inactive under T-native.
  - **Item 4** (:207-257): the closure layout; the code-row and data-document definition records (:224-229); encoding by the identity crate's canonical encoder; size bounds; the two roots.
  - **Item 5**: A3 (:275), A5 (:277), A6 (:278), A7 (:279), A11's `SymbolTableV1` with its r4 ERROR exception (:283), and the T-native joins (:286-290).
  - **Item 6** (:319-337): pins by tag and full commit with every member's sha256 and length; E0's pins (:324); under T-native, "the Cargo lock pins the crate archives by checksum, and the member digests are checked against the unpacked archives by the SYN-DEP checker" (:330).
  - **Item 8** (:372-401): the eight rows. **Item 11** (:466): the T-native bounds.
  - Item 19's SYN-REG and SYN-DEP rows (:726-727) are E2b's, not this unit's.
- **E0's record:** `syntax-e/E0-REPORT.md` (`c1011e83…`, your ACCEPT). "Inputs and pins"; P3's `SymbolTableV1` table (:180-185); "E1 record items and observations" (:330-344); and ":365": "`SyntaxTreeV1`'s byte layout and `SymbolTableV1`'s canonical encoding are E0's own. E2a fixes the normative forms." E0's per-file tag pins are `syntax-e/e0-probe/pins/*.pins.tsv` and `PINS.txt`.
- **M3-PLAN r9** (`m3/M3-PLAN-r9.md`, your ACCEPT): the M3-E row (:260) and **"E1's record items"** (:321), which go to E2a and E2b. This request answers each one (below).
- **SYN-NS**, bound at product `6190e66` (`syntax-e/syn-ns/`; record `successor.json`, `180f4935…`). Its "Cross-law items" (README :296): "**E2a (SYN-LANE).** Places the six members at their tree paths unchanged. Writes the manifest's `normalizer` object exactly as `materialization-map.json` gives it, and pins the grammars at E0's commits (LD-NS3)."
- **Precedents:** P0 (`m2/m3-p0-scaffolds-inventory-v135/`; `tools/host/dependency-policy.json`, selection rows that link nothing); X3a-2 (`m2/read-endpoint-x3a2-inventory-v136/`, the staged inventory lock); I1-a (`m3/reviews/codex2-i1a-r1/`, the drift gate with a scratch overlay).

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-e2a`, detached at main `d2c00a9` (SD-7: 97 contract successors, 96 inventory successors, v136 selected). Nothing is committed. The 22 new files are intent-to-add, so `git diff d2c00a9` includes them.
- **Diff:** `git diff d2c00a9` is 633871 bytes, sha256 `1c4234ad08138711a7b0894d4c54ae068423e3c0ed3e372e608e58b84ab825d4`. It covers 24 files, +2768 −386. Of that, the staged `design-lock.json` is +476 −386.
- **Provisioned trees:** the worktree also holds the ignored `tools/contracts/node_modules` and `tools/contracts/python-packages`, copied from the main checkout, for the drift gate.
- **The pinned crate archives:** `/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/e2a/archives/` holds `tree-sitter-0.27.0.crate`, `tree-sitter-javascript-0.25.0.crate`, `tree-sitter-rust-0.24.2.crate` and `tree-sitter-typescript-0.23.2.crate` (and `tree-sitter-language-0.1.8.crate`, which the lane does not read). They were fetched from static.crates.io on 2026-10-04. Each one's sha256 equals its crates.io index `cksum`; the sparse-index entries are saved beside them in `../index/`. `tree-sitter-0.27.0.crate` is byte-identical to E0's. You may re-fetch them into your output directory; the lane refuses any other bytes.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`; Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`; generator `~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator`; Node `~/.nvm/versions/node/v24.16.0/bin/node`.

### Inventory (arch, untracked)

All under `docs/implementation/m2/`:
- `repository-file-inventory.v138.json` (candidate; parent v137);
- `syntax-lane-e2a-inventory-v138/` (README, builder, lock stager, scratch verifier, drift gate, E0 cross-check and its output, projection verifier and its outputs, verifier anchor, successor record);
- `syntax-lane-e2a-inventory-v138-subject.json`, sha256 `29fc0ed2929591efeac060df7cfeab5f7b7090ab7735bf0d971bc2f287d2550f`;
- `syntax-lane-e2a-inventory-v138-unit.json`, a DRAFT-PENDING-REVIEW record the lead completes at integration (not in the subject).
- **The parent, J2a's unit** (untracked, reviewed separately): `repository-file-inventory.v137.json`, `host-invocation-j2a-inventory-v137/` (its successor record, README, `evidence/verify_scratch.py` and `stage_lock_j2a.py`, which E2a's scripts load) and `host-invocation-j2a-inventory-v137-subject.json`.

## What E2a changes

| Product file | What it is |
|---|---|
| `tools/grammar/grammar_lane.py` (new) | The lane: `check`, `write` and `materialize` (below). Python standard library only. |
| `tools/grammar/lane.json` (new) | The lane's pins and layout (below). |
| `tools/grammar/upstream/tree-sitter-typescript/LICENSE` (new) | The one pinned member a crate archive omits, from the v0.23.2 tag (judgment call 3). |
| `tools/grammar/closure/opensip-interface/grammar/<g>/definition.v1.json`, eight (new, generated) | The canonical definition records of the eight grammar rows (item 4). Each one's sha256 is the row's `grammarDigest`. |
| `tools/grammar/symbol-tables/<g>.v1.json`, four (new, generated) | The canonical `SymbolTableV1` of each code grammar (A11). Each one's sha256 is its definition's `symbolTableSha256`. |
| `tools/grammar/closure/opensip-interface/{grammar/normalizer.v1.json, normalization/specification-map.v1.json, normalization/levels/L0…L3.v1.json}`, six (new) | SYN-NS's six closure members, byte for byte. |
| `tools/tests/test_grammar_lane.py` (new) | 25 controls: 17 synthetic; 8 need `--archives`, and one of those also needs `--architecture`. |
| `tools/README.md` | A "Grammar closure lane (SYN-LANE)" section. |
| `design-lock.json` | Staged: J2a's inventory137 entry, then the inventory138 entry (see "The staged lock"). |

Nothing else changes. No Rust source, `Cargo.toml`, `Cargo.lock`, dependency policy, schema, registry or generator input changes, and `crates/syntax` is untouched.

### The lane

`tools/grammar/lane.json` (`executionModel` `native-linked-v1`) pins:
- **four upstream releases**, each with repository, tag, full commit and licence, and its crates.io archive (name, version, checksum, size, and the `.cargo_vcs_info.json` record the archive carries): runtime `tree-sitter` v0.27.0 at `6070dbfe…`, `tree-sitter-javascript` v0.25.0 at `44c892e0…`, `tree-sitter-rust` v0.24.2 at `77a37472…` and `tree-sitter-typescript` v0.23.2 at `f975a621…`, E0's commits (item 6, :324; SYN-NS LD-NS3);
- **every retained member**, at its path in the pinned upstream tree, with its role (`compiled`, `grammar`, `node-types` or `licence`), source (`archive` or `retained`), sha256, length and git blob;
- **a compile model per member set**: the compile roots, include directories and undefined macros of the crate build that compiles it under T-native (judgment call 2);
- **the eight rows** (`grammarId`, `languageId`, `syntaxClass`, `suffixes`; a code row's upstream and `parser.c`; a data row's `format`), and the registry they must cover, `schemas/sources/native-v2.schema.json#/x-opensip-grammar-capability-registry/languages`;
- **the six SYN-NS members** with SYN-NS's record pin and candidate root, and the bundle manifest's `normalizer` object from `materialization-map.json`.

`grammar_lane.py check --repository . --archives DIR [--architecture ARCH]`:
1. **Archives.** Each archive's bytes must equal its pinned checksum and size. It is read in memory, never unpacked: only regular members under `<name>-<version>/`, logical paths, no duplicates; the VCS record must equal its pin.
2. **Members.** Every pinned member must be present with its sha256, length and git blob. A retained copy may not shadow an archive member, and every retained file must be a pinned member.
3. **Compiled sets.** Each runtime or code-row member set's `compiled` members must equal the include closure of its compile roots: quoted includes resolved against the including file's directory and then the include directories, `..` never escaping the tree, and branches under an undefined macro (`#ifdef TREE_SITTER_FEATURE_WASM`, `#ifdef TREE_SITTER_WASM_STDLIB`) excluded. Every other branch is kept.
4. **Registry coverage** (items 7 and 8): every row's language and class are the registry's, and the rows own the fourteen suffixes exactly, each once.
5. **`SymbolTableV1`** of each code row, from its generated `parser.c` (below).
6. **The eight definition records**, canonical under the identity profile, each at most 1 MiB.
7. **SYN-NS.** Each of the six members equals its pin, is canonical and within its bound; the manifest normalizer names the normalizer member; the IE map names that normalizer and exactly L0 to L3 with their members' digests. With `--architecture`, the lane also finds SYN-NS's record in the product lock, checks its pin, and requires each member to be that record's candidate, byte for byte, as the arch file holds it. It also checks the law pin.
8. **Reproducibility.** The rebuilt definitions and symbol tables must equal the retained bytes, and the retained set must be exactly the generated set plus the six SYN-NS members.

`write` regenerates the retained outputs (with `--architecture`, also copying the SYN-NS members from the selected candidates) and then runs `check`. `materialize --out NEW` writes the closure tree members this lane owns: the eight definitions; each code row's sources under `opensip-interface/grammar/<g>/source/<upstream path>`; the runtime's under `opensip-interface/grammar/runtime/source/<upstream path>`; a copy of each licence under `opensip-interface/grammar/notices/<upstream>/<upstream path>`; and the six SYN-NS members. That is 91 members. It does not write the bundle manifest or the build receipt (judgment call 1).

### `SymbolTableV1`: the normative form E2a fixes

This is the record A11 names, `{schemaVersion: 1, grammarId, languageAbi, symbols: [{id, name, named, visible}], fields: [{id, name}]}`, encoded by the identity crate's canonical encoder (`crates/identity/src/canonical.rs`: keys in UTF-8 byte order, no whitespace, exact integers, its string escapes). Its digest is the raw SHA-256 of those bytes.
- `symbols` are the ids `0 … ts_language_symbol_count() − 1`, that is `SYMBOL_COUNT + ALIAS_COUNT`, in id order.
- `name` is what `ts_language_symbol_name` returns.
- `named` is `ts_language_symbol_type == Regular`, which is metadata named and visible; `visible` is the type being Regular or Anonymous, which is metadata visible. These are exactly the tree-sitter crate's safe `Language::node_kind_is_named` and `node_kind_is_visible`, so E2b's T-native recomputation (:289) can use the safe API. A supertype is neither, as E0 observed.
- `fields` are the ids `1 … FIELD_COUNT` with `ts_language_field_name_for_id`. `languageAbi` is the generated `LANGUAGE_VERSION`.
- **ERROR (0xFFFF) and ERROR_REPEAT (0xFFFE) are never rows**, so a table may hold at most 65,534 symbols. The lane refuses more. This is r4's A11 exception (:283).

The lane reads the generated tables (`ts_symbol_identifiers`, `ts_symbol_names`, `ts_symbol_metadata`, `ts_field_identifiers`, `ts_field_names`) line by line, decodes C string escapes strictly, requires every id to have exactly one name and one metadata entry with `visible` and `named`, and requires the language object to wire those tables and counts. **The result equals E0's tables byte for byte:** E0's `SymbolTableV1` recomputed from the natively linked `Language`, and decoded from its modules, for all four grammars (`evidence/check_e0_pins.py`; E0's SCRATCH still holds them). The digests carry E0-REPORT's P3 prefixes:

| Grammar | `SymbolTableV1` sha256 | ABI | Symbols | Fields |
|---|---|---|---|---|
| javascript | `5a0738c3c79118e0cca3a32488c797ea2553413d2bef94caad3b379b2ec7b669` | 15 | 265 | 36 |
| rust | `0363b059b8f9b9221615f027acb623aed68604dad2114d05bacbc24b631198d3` | 15 | 355 | 31 |
| tsx | `c8759474552a61a78ce41392187a001e667989ee2d51c68c278dc14aa763d784` | 14 | 400 | 43 |
| typescript | `daa3b99865f2f1a1ac31d4485a0a53e9cdff762ed7944434bb41e3d5b55ebb0c` | 14 | 383 | 40 |

### The definition records

The shapes are item 4's (:224-229), with every field present:
- **Code rows** (javascript, rust, tsx, typescript): `grammarVersion` is the upstream tag. `upstream` is `{repository, tag, commit}`. `sources[]` and `runtime.sources[]` list `{path, sha256, bytes}` by closure path, in path order. `module`, `shimAbi` and `shim` are `null` (judgment call 1). Then `languageAbi`, `symbolTableSha256`, and `notices` (the closure paths of the row's licence notice and the runtime's two).
- **Data-document rows** (json, markdown, toml, yaml): `grammarVersion` `format-definition.v1`, `format: {name, reference}` and `parse: "none"`. No parser is pinned, linked or run (item 8).

| Row | Members | `grammarDigest` |
|---|---|---|
| javascript | 6 (`src/parser.c`, `src/scanner.c`, `src/tree_sitter/parser.h`, grammar.json, node-types.json, `LICENSE`) | `6242e665…` |
| json | — | `5c791a92…` |
| markdown | — | `b4b33cc3…` |
| rust | 7 (adds `src/tree_sitter/alloc.h`, which its scanner includes) | `d51ee290…` |
| toml | — | `acb76e51…` |
| tsx | 8 (`tsx/src/{parser.c, scanner.c, tree_sitter/parser.h}`, `common/scanner.h`, `typescript/src/tree_sitter/parser.h`, grammar.json, node-types.json, `LICENSE`) | `30106a35…` |
| typescript | 7 | `9b52d08b…` |
| yaml | — | `013a54db…` |
| runtime (in every code record) | 44: the include closure of `lib/src/lib.c` (42 C sources and headers, including `lib/include/tree_sitter/api.h` and the ICU `unicode/*.h`), `lib/LICENSE` and `lib/src/unicode/LICENSE` | — |

The full digests are in the lane's `check` output and `hashes.txt`.

## E1's record items (M3-PLAN r9 :321)

| Item | Where it falls | In E2a |
|---|---|---|
| ERROR's symbol 0xFFFF needs an explicit exception to item 10 and A11 | A11's table: here. Item 10's validator: E2b. | **Resolved for A11.** No table has an ERROR or ERROR_REPEAT row; the lane bounds the count at 65,534 and a control refuses 65,535 (`test_error_symbols_are_never_rows`). Item 10's validator is E2b's (r4 :742). |
| E0's `SyntaxTreeV1` byte layout is probe-only, and E2a fixes the normative one | Under T-wasm the shim, a lane member, writes it. Under T-native no shim exists: `parser.rs` (E2b) serializes the linked tree. | **Not resolved here** (judgment call 4). |
| `SymbolTableV1`'s canonical encoding (E0R :365) | Here. | **Resolved**: the normative form above. |
| The supertype symbol type (E0R :344, "E2a may want a type field") | Here. | **Resolved without a field.** A11 fixes `{id, name, named, visible}`, and adding a field would change the law. The flags are the safe API's, so a supertype is `false/false` like an auxiliary symbol. No E use needs the distinction: A12 checks names only, and supertypes never appear in a tree. |
| The host crate count (E0R :343) | That count is T-wasm's (`wasmi`). Under T-native, SYN-DEP (E2b) "records the resolved closure, which is the binding count" (item 1). | **Not E2a's.** No crate is linked here. |
| Item 4 omits the wasm headers | T-wasm only, inactive. | Nothing to do. |
| The grammar and runtime commits are pinned by E0 | Here. | **Resolved**: `lane.json` and every code record name E0's commits. |
| Eager compilation | T-wasm only (E2b if T-wasm returns). | Nothing to do. |

## The staged lock

The lock change is staged in the worktree, as X3a-2 staged v136. `syntax-lane-e2a-inventory-v138/evidence/stage_lock_e2a.py` writes HEAD's `design-lock.json` plus:
- J2a's `inventorySuccessors` entry for v137, exactly as J2a's `stage_lock_j2a.py` writes it in its own worktree (checked equal), with its `SCRATCH-J2A/` review (764 bytes, `34bf2fc8…`) and assent (620 bytes, `7abfc1f1…`) placeholders;
- E2a's entry: parent v137, candidate v138, record `syntax-lane-e2a-inventory-v138/successor.json`, all real pins. Its review `SCRATCH-E2A/review.json` (760 bytes, `27b112db…`) and assent `SCRATCH-E2A/assent.json` (616 bytes, `bd0fc7ff…`) are placeholders;
- `inventoryPassageInheritance` replaced by the 103 rows re-parented to v138, exactly as the record projects them.

The staged lock is 516692 bytes, sha256 `a2fa6338296d8492289948ae5d9a53e90bf34c06810b67a97652fee07e4cbc77`, in the lock's canonical formatting. The placeholder bytes are those of the two units' `evidence/verify_scratch.py` overlays. At integration, after J2a's, the lead:
1. copies your review in, to `m3/reviews/grok2-e2a-r1/review.json`;
2. completes `syntax-lane-e2a-inventory-v138-unit.json`;
3. re-stages E2a's entry on the integrated lock and replaces exactly E2a's two placeholder pins;
4. runs plain `verify_design`;
5. commits.

**Plain `verify_design` on the staged lock refuses** at the first placeholder, J2a's: "missing or escaping regular file: SCRATCH-J2A/review.json". That is correct until review, and `verify_scratch.py` asserts it. `design-lock.json` stays outside the unit's `sourceBoundary`, as in every inventory unit; its staged bytes are pinned here, and the diff sha covers them.

## Pins checked

- **X9: no harness source changes, so no run set.** The X9 harness sources (`tools/check_crash_matrix.py` and its test, `crates/platform`, storage's and host's `tests/` with both `required-runs.v1.json`, `commit_tests.rs` and `commit_matrix_tests.rs`, security's `crash_matrix_sites.rs`, `crash_matrix_census.rs` and `crash_matrix_support`, and storage's and host's `crash_matrix_support`) are untouched: the diff names none of them. No Rust source changes at all, so no crash point, scope, clock sample, file write or `cfg` feature site moves.
- **Dependency policies.** No manifest, lock, feature or policy changes. Both checkers and their suites pass (Lead results).
- **Package edges.** All 22 rows are in `tooling`, which declares no dependency. No crate declares a new edge.
- **Generators and lanes.** No generator input, schema, registry or TypeScript lane source changes. The drift gate passes with `changed: []`.
- **Inventory coverage.** Every file of the worktree, tracked or intent-to-add, is a v138 row.
- **`forbid(unsafe_code)` in `crates/syntax`** (P0's lead decision) is untouched and stays achievable under T-native: the grammar crates export safe `LanguageFn` constants (`tree_sitter_rust::LANGUAGE` and so on), and `tree_sitter::Language::new(LanguageFn)` is a safe function. The `unsafe` lives inside those crates.

## Lead results

All lanes ran serially on `d2c00a9` plus this diff, with a private 0700 TMPDIR, `--locked --offline`, `nice -n 10`, and the lane lock held per group. `~/Library/Application Support/OpenSIP` was absent before and after.

**Lane order.** The cargo lanes ran first (17:59 to 18:26 UTC), while v138 was still staged on v136. J2a's v137 candidate appeared during them, so E2a was re-parented on it, and the design, drift, edge, dependency and SYN-LANE lanes then ran on the final bytes (18:58 UTC). Since the cargo lanes, only two things changed: the staged `design-lock.json`, and `grammar_lane.py` plus its test (typed refusals for non-UTF-8 input, with their two assertions). No cargo lane builds or reads either, and every Rust source is unchanged from `d2c00a9`.

| Check | Result |
|---|---|
| `cargo fmt --all --check` | Clean |
| `cargo build --workspace --all-targets` | Pass (fresh target directory) |
| Clippy `-D warnings`, workspace `--all-targets` | Clean |
| Clippy `-D warnings`, platform, security, storage and host with `crash-matrix` | Clean |
| Clippy `-D warnings`, security, storage and host with `scenario-fixtures` | Clean |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1738 passed, 0 failed, 3 ignored (20 test binaries). E2a adds and removes no Rust test. |
| The same, run 2 | 1738 passed, 0 failed, 3 ignored |
| `cargo test --workspace --doc` | 20 passed, 0 failed |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1636 passed, 0 failed, 3 ignored. Includes storage's `commit_tests` and host's `commit_matrix_tests`, without a run set. |
| `evidence/drift_scratch_e2a.py` (staged mode; the real public `generate_contracts.generate`, write false) | Passes: 40 sources, 8 outputs, `changed: []`, generator closure selected; mode `staged` |
| `evidence/verify_scratch.py` (staged mode) | Passes. Inventory successors 96 → 97 → 98 (HEAD, with v137, with v138) and v138 selected; contract successors 97 unchanged; inheritance 100 → 103 → 103, equal to verify_design's own projection; 21 inventory and 1 contract passage supersessions unchanged; 40 generation and 48 admission sources. J2a: `staged-in-memory`. |
| Plain `verify_design.py --architecture ../opensip_arch --implementation .` on the staged lock | Refuses: "missing or escaping regular file: SCRATCH-J2A/review.json" (exit 1). Correct until integration. |
| Plain `verify_design.py` on HEAD's lock (`d2c00a9`, same product sources) | Passes: v136 selected, 96 inventory and 97 contract successors, 21 inventory supersessions, 40 generation and 48 admission sources |
| `verify_projection.py` against the real lock at `d2c00a9` (J2a applied in memory) | PASS: 103 rows, 518 corruptions refused |
| `evidence/build_v138.py` rerun | Same bytes |
| `check_package_edges.py --lane host`, against v138 and against v137 | Both pass: 12 workspace packages, 22 declared and 20 resolved internal edges, none new |
| `check_package_edges.py --lane rust-provider` against v138 | Passes: `opensip-rust-provider` only |
| `tools/tests/test_package_edges.py` | 14 tests run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 tests run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 tests run, OK |
| `grammar_lane.py check --architecture` (SYN-LANE) | Passes: 8 rows (4 code), registry 7 languages and 14 suffixes covered, 44 runtime sources, 6 SYN-NS members bound to the lock-selected candidates, retained outputs byte-identical |
| `tools/tests/test_grammar_lane.py --archives --architecture` | 25 tests run, OK |
| `tools/tests/test_grammar_lane.py` (no archives) | 25 tests run, OK (skipped=8) |
| `grammar_lane.py materialize`, twice into fresh directories | 91 members each; `diff -r` empty; tree digest `1510c2c2…` both times |
| `evidence/check_e0_pins.py` | Passes: 4 upstreams equal E0's tags and commits; 72 members equal E0's tag pins; 4 symbol tables equal E0's native and wasm tables byte for byte; SYN-NS and the law pin match |
| `~/Library/Application Support/OpenSIP` | Absent before and after |

Commands, from the worktree, with `PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, `CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo`, `AR=~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`, `GA=<the four pinned archives>`, `U=../opensip_arch/docs/implementation/m2/syntax-lane-e2a-inventory-v138`, `V=../opensip_arch/docs/implementation/m2/repository-file-inventory.v138.json` and `OUT=/tmp/opensip-implementation/reviews/grok2-e2a-r1`:

```sh
cargo fmt --all --check
cargo build --workspace --all-targets --locked --offline
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
cargo test --workspace --all-targets --no-fail-fast --locked --offline   # twice
cargo test --workspace --doc --locked --offline
cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline
$PY -I -B $U/evidence/drift_scratch_e2a.py . $OUT/drift
$PY -I -B $U/evidence/verify_scratch.py .
$PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .   # refuses at SCRATCH-J2A
git show HEAD:design-lock.json > $OUT/head-lock.json
$PY -I -B tools/verify_design.py --architecture ../opensip_arch --lock $OUT/head-lock.json --implementation .
$PY -I -B $U/verify_projection.py --architecture ../opensip_arch --lock ../opensip/design-lock.json
cargo metadata --locked --offline --format-version 1 > $OUT/host.json
(cd providers/rust && cargo metadata --locked --offline --format-version 1) > $OUT/provider.json
$PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/host.json --inventory $V --lane host
$PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/provider.json --inventory $V --lane rust-provider
$PY -I -B tools/tests/test_package_edges.py -v
$PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
$PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
$PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
$PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
$PY -I -B tools/grammar/grammar_lane.py check --repository . --archives $GA --architecture ../opensip_arch
$PY -I -B tools/tests/test_grammar_lane.py --archives $GA --architecture ../opensip_arch -v
$PY -I -B tools/tests/test_grammar_lane.py -v
$PY -I -B tools/grammar/grammar_lane.py materialize --repository . --archives $GA --out $OUT/tree-a   # and tree-b; diff -r
$PY -I -B $U/evidence/check_e0_pins.py .
```

`check_e0_pins.py` rewrites only its own `evidence/e0-crosscheck.json`, with the same bytes. `evidence/build_v138.py ../opensip/design-lock.json` reproduces the candidate and record byte for byte; it writes only those two untracked paths, so run it on a scratch copy of arch if you prefer.

## Inventory v138

- **Contents:** v137 plus 22 rows, all in package `tooling`, standing `proposed`: the lane (`entrypoint`), `lane.json` (`registry`), the retained licence (`documentation`), the eight definition records and four symbol tables (`registry`, generated), the six SYN-NS members (`registry`, not generated) and the test (`test`). That gives 995 files, with the 973 v137 rows equal by value. The packages, their edges and the pending decisions are unchanged. Check the 22 descriptions against the files.
- **Planned row changed, by value unchanged:** `tools/README.md`, whose row stays true.
- **Projection: 103 rows**, every meaning a lock selecting v137 binds to it, by stable file path: its 103 inheritance rows as v137 projected them (v136's 100 and the three direct overrides of `read-endpoint-x3a2-descriptions` on v136). No bound contract successor has a passage on v137, and no supersession is folded. One projected row, sorted after the inserted paths, moves.
- **Pins:**
  - candidate: 571539 bytes, sha256 `90d5b09ca552c120b127d597a3a635fcb9de88ba462a67d99e71d937bdfbd5e9`;
  - successor record (`syntax-lane-e2a-inventory-v138/successor.json`): 309185 bytes, sha256 `0e574e209ed2ccbef33eab9b03c6ef85ed3330b9cb5fb3cd7f9ef9d8d2638c5d`;
  - parent v137 (J2a's candidate): 558538 bytes, sha256 `92226626700a9d44c2a22eea92526aea615cb9b15279169f8ec7e2e88665ce56`.
- **Order:** the lock at `d2c00a9` selects v136. The lead reserved v137 for J2a and v138 for E2a, on it. Your assessment's parent is v137's pin.

## Judgment calls

Calls 1, 3, 4 and 5 rest on points E1 does not settle, so the lead rules on them before this request is sent; E2a leaves 1 and 4 open and implements the named reading for 3 and 5. Calls 2, 6 and 7 are E2a's choices inside item 4's and item 6's text.

1. **No bundle manifest and no build receipt** (E1 doesn't settle them under T-native). Item 20 gives E2a "manifest and definition records", and SYN-NS asks E2a to write the manifest's `normalizer` object, but three manifest inputs are not settled under T-native:
   - **`limits`.** Item 11 (:466) replaces fuel with "an operation budget counted in progress-callback invocations" and memory with `maxFileBytes` plus the node bound, but gives no form, values or admissible ranges for it (A8). E0 measured only wasm fuel (P6).
   - **`parserVersion`,** the closure manifest's `semanticVersion` (NE:225-227). No development closure has one, and item 6 makes the lane its owner.
   - **`buildReceiptSha256`.** The receipt holds "toolchain identity …, target features, and exact compile and link argument vectors" (item 4) of a module build that does not exist under T-native.

   E2a pins the manifest's `normalizer` object in `lane.json` (equal to `materialization-map.json`, checked) and provides every `grammars[]` row and digest. **Recommendation, for the lead's ruling:** rule each in E1's next record revision, and write the manifest with E2b, which links tree-sitter and owns the engine identity and the limit checks:
   - (a) T-native limits: `{maxFileBytes 4194304, maxNodes 4194304, maxDepth 4096, operationBudget {base, perByte}}`, with constants derived by E0's P6 rule (4× the T2a maximum, two significant figures) from a native T2a run counting progress-callback invocations, which E2b measures;
   - (b) `parserVersion`: a semantic version the lane assigns per distinct tree, a `-dev.N` pre-release for development closures;
   - (c) the T-native receipt records the crate archives and the compile models that build the linked code, with toolchain fields `null`; or E1 makes `buildReceiptSha256` null under `native-linked-v1`.
2. **The compiled member sets follow the crate builds.** Under T-native the host compiles each grammar through its crate's build script. So a row's `compiled` members are the include closure of that build's roots and include directories. `tree-sitter-typescript`'s build compiles both grammars with `-I typescript/src`, so the `tsx` row's `common/scanner.h` resolves `tree_sitter/parser.h` to `typescript/src/tree_sitter/parser.h`. The `tsx` record lists that file beside `tsx/src/tree_sitter/parser.h`; the two have identical bytes. The runtime's set is `lib.c`'s include closure without the `wasm` feature: `lib/src/wasm-stdlib/**` is T-wasm's (item 4, r4) and is not retained. **Question:** is "every source member it compiles" (item 6) right read as the crate build's include closure?
3. **A licence the archive omits.** The `tree-sitter-typescript` 0.23.2 crate ships no `LICENSE`. "The definition records over the crate archives" and item 6's "checked against the unpacked archives" cannot cover it. The lane retains it from the pinned tag (`tools/grammar/upstream/`, sha256 `49bf33cf…` and git blob `aa9f858d…`, equal to E0's tag pin), as source `retained`. **Recommendation, for the lead's ruling:** accept, and record in E1's next revision that a pinned member an archive omits is retained from the pinned tag by sha256 and git blob, so SYN-DEP's checker checks it against the lane pin.
4. **`SyntaxTreeV1`'s normative layout is not fixed here.** E0's lead ruling gave it to E2a when the shim, a lane member, wrote it. Under T-native no shim exists, and `parser.rs` (E2b) serializes the linked tree. **Recommendation, for the lead's ruling:** move it to E2b in E1's next record revision. E2b adopts E0's layout, with symbol 0xFFFF tied to the error flag (SYN-1 LD-2), and fixes it in `parser.rs` with tests. **Question:** do you agree it is not E2a's under T-native?
5. **`shim` is `null`.** Item 4 says only `module` and `shimAbi` are null under T-native, and lists `shim: {path, sha256, bytes}` without a null case. No shim exists under T-native: it is the module's export layer, which item 3's reading rule makes inactive. Listing a nonexistent member would break A6. **Question:** do you accept `null`, to be recorded in E1's next revision?
6. **The data-document format references.** Item 4 fixes `format: {name, reference}` but not the values. E2a uses: JSON, `https://www.rfc-editor.org/rfc/rfc8259`; Markdown, `https://spec.commonmark.org/0.31.2/`; TOML, `https://toml.io/en/v1.0.0`; YAML, `https://yaml.org/spec/1.2.2/`. They describe, and nothing parses. They are identity-bearing only through `grammarDigest` and the bundle digest.
7. **Layout within the tree.** `source/` and `runtime/source/` keep each member's path in the pinned upstream tree, so relative includes still resolve. `notices/<upstream>/<path>` holds a copy of each licence, because item 4 gives notices their own directory while `source/**` also holds "the upstream licence". A definition's `notices` lists its grammar's notice and the runtime's two, MIT and the ICU licence of the compiled `unicode/*.h`.

**Observations (no action asked):**
- The `tree-sitter-rust` 0.24.2 archive was published from commit `e2bee853…`, which GitHub does not have; the v0.24.2 tag is `77a37472…`. Every retained member equals the tag's bytes (E0's pins and git blobs); only the cargo-normalized `Cargo.toml` and the crate's `Cargo.lock` differ. The record names the tag commit (E0's pin, LD-NS3), and the lane pins the archive's VCS record as it is. That is for SYN-DEP's review too.
- **Dependency admission, for E2b.** No crate is vendored. Archives come from the Cargo cache, `Cargo.lock` pins their checksums, and LFS is arch-only. A host crate is first selected by a row in `tools/host/dependency-policy.json` (P0), and the linking unit then declares it and adds its closure check. That file's document-level rule (pure Rust, `forbid(unsafe_code)`, no build script, `links` or C) excludes tree-sitter, which is why E1 gives the crates their own SYN-DEP policy. `check_dependencies.py` covers only the contracts closure and `check_identity_dependencies.py` only identity's, so a crate linked into `crates/syntax` is checked by neither until SYN-DEP's checker exists.

## Lead rulings (Claude Opus 5.5, before sending)

These are lead decisions under the owner's standing direction. Each goes to E1's next record revision (E1 r5), which the lead writes.

| Call | Ruling | Rejected |
|---|---|---|
| 1 | **Accepted as recommended.** E2a ships no bundle manifest and no build receipt. E2b writes the manifest. E1 r5 rules on three points: (a) the T-native limits, with the operation-budget constants derived by E0's P6 rule from a native T2a run that E2b measures; (b) a lane-assigned `parserVersion`, with a `-dev.N` pre-release for development closures; (c) a T-native receipt that records the crate archives and compile models, with null toolchain fields. | A null `buildReceiptSha256` under `native-linked-v1`. The crate archives and compile models are the real build inputs, and a receipt keeps them auditable. |
| 3 | **Accepted.** A pinned member that an archive omits is retained from the pinned tag, by sha256 and git blob. SYN-DEP's checker checks it against the lane pin. | Dropping the licence, or treating the archive as the only source. |
| 4 | **Moved to E2b.** E2b adopts E0's layout, with symbol 0xFFFF tied to the error flag (SYN-1 LD-2), and fixes it in `parser.rs` with tests. | Fixing the layout in E2a as a document with no serializer. Under T-native the serializer is E2b's code. |
| 5 | **Accepted:** `shim` is `null` under T-native, with E1 r5 recording the null case. | Listing a nonexistent member, which breaks A6. |

So judge calls 1, 3, 4 and 5 as ruled. Your answers to the questions in 2, 4 and 5 still matter, and a disagreement is a finding.

**Shared machine.** Other units' X9 lead sets run on this machine under a 5000 ms timing guard. Before any cargo build, test or clippy run, take the shared lane lock with `mkdir "$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`, and remove it with `rmdir` straight after. If the lock is held, wait until it is free. The Python-only lanes need no lock.

## Decide

- **Faithfulness:** does E2a do what item 20, read with its T-native note, assigns: the definition records over the crate archives, their `SymbolTableV1` digests and the closure layout, with the upstream pins and the reproducibility check, and nothing E2b, E2c or E2s owns? Does it place SYN-NS's six members unchanged and pin the grammars at E0's commits, as SYN-NS asks?
- **The records:** do the eight records match item 4's shapes and A5's and A7's joins? Are the members right, and is the `SymbolTableV1` derivation right, for what A11 and its T-native recomputation (:289) will check?
- **The lane:** rerun `check` (with `--architecture`), the tests (with and without archives) and two materializations, and `check_e0_pins.py`. Re-fetch the archives if you prefer.
- **Rerun the lanes above:** fmt, the workspace build and the three clippy lanes; the workspace tests (twice if time allows), the doc tests and the crash-matrix feature lane; the drift gate; `verify_scratch.py` in staged mode and plain `verify_design`, which must refuse at the first placeholder; `verify_projection.py`; both package-edge lanes against v138; and both dependency checkers with their suites.
- **Judgment calls:** are calls 1 to 7 acceptable as E2a's scope? Answer the questions in 2, 4 and 5 directly. Calls 1, 3, 4 and 5 also carry the lead's ruling. You need not endorse the recommendations, only whether E2a correctly leaves them open.
- **Inventory v138:** pin it, and assess it as an inventory candidate.

Write REVIEW.md and review.json under the output directory.

review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `1c4234ad08138711a7b0894d4c54ae068423e3c0ed3e372e608e58b84ab825d4`, the diff's sha256, as a single string;
- "subjectManifestSha256": `29fc0ed2929591efeac060df7cfeab5f7b7090ab7735bf0d971bc2f287d2550f`, as a single string;
- "inventoryCandidateAssessment": verdict, requiredFindings, the candidate's path, bytes and sha256, parent (v137's pin), and successorRecord (the pin of `syntax-lane-e2a-inventory-v138/successor.json`).

Do not commit.
