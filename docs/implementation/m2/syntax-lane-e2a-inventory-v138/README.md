# E2a inventory138 (SYN-LANE)

Adds exactly twenty-two rows to inventory137 (unit J2a). They belong to unit **E2a**, the grammar closure lane SYN-LANE of law M3-E1 r4 (`docs/implementation/m3/syntax-e/PROPOSAL-r4.md`, accepted; items 4 to 6, 19 and 20). E0 selected native tree-sitter linked in the host (`native-linked-v1`), and under that branch item 20 says E2a "shrinks to the definition records over the crate archives".

**Parent: inventory137, not yet integrated.** The lead assigned E2a inventory138 on J2a's inventory137 (`host-invocation-j2a-inventory-v137/`, built on inventory136, which the lock at d2c00a9 selects). J2a's README states its file set is final. Until J2a is integrated, every script here applies J2a's staged entry in memory from J2a's own `evidence/verify_scratch.py` (its SCRATCH-J2A placeholders), exactly as J2a stages it. Only inventory137's candidate, record and projected meanings are used, and those do not depend on J2a's review pins. If J2a's candidate changes, this one must be rebuilt.

All twenty-two rows are in the existing `tooling` package (path `tools`):
- **`tools/grammar/grammar_lane.py`** (entrypoint), the lane, and **`tools/grammar/lane.json`** (registry), its pins: the tree-sitter runtime v0.27.0 and the rust v0.24.2, typescript v0.23.2 and javascript v0.25.0 grammar releases at E0's commits, each with its crates.io archive checksum, size and VCS record; every retained member at its upstream path by role, sha256, length and git blob; the eight grammar rows; and the six SYN-NS members.
- **`tools/grammar/upstream/tree-sitter-typescript/LICENSE`** (documentation): the one pinned member a crate archive omits, from the release tag.
- **Eight generated definition records**, `tools/grammar/closure/opensip-interface/grammar/<grammarId>/definition.v1.json` (registry, generated): four code rows (javascript, rust, tsx, typescript) and four data-document format definitions (json, markdown, toml, yaml).
- **Four generated `SymbolTableV1` records**, `tools/grammar/symbol-tables/<grammarId>.v1.json` (registry, generated).
- **Six SYN-NS members**, at their closure tree paths under `tools/grammar/closure/` (registry, not generated): `normalizer.v1.json`, the IE map and its four level files, byte-identical to the candidates of the SYN-NS successor the lock binds.
- **`tools/tests/test_grammar_lane.py`** (test).

It keeps all 973 existing rows of inventory137 by value, along with the packages and their edges, the pending decisions and the carried unresolved obligations, for 995 planned files.

**Planned row changed.** `tools/README.md` gains a "Grammar closure lane (SYN-LANE)" section. Its row ("Publish supported maintenance/build commands, their inputs, outputs and ownership ...") stays true, so no description successor is needed.

**No new edge, crate or dependency.** The rows are in `tooling`, which declares no dependencies. No manifest, `Cargo.lock` or dependency policy changes: the lane reads the four pinned crate archives as lane inputs and links nothing. SYN-DEP (unit E2b) selects and links the crates. The builder asserts that every added path is new and every changed path is planned.

**Order.** `evidence/build_v138.py`:
- takes the lock (by default the product checkout's), applies J2a's staged entry in memory while that lock selects inventory136, and requires the result to select inventory137 with J2a's successor record;
- checks every meaning the lock binds to the parent before carrying it;
- writes only its two paths;
- refuses tracked paths, and refuses while a lock selects inventory138.

Reruns reproduce the same bytes, whether J2a is staged in memory or integrated, because only inventory137's candidate, record and meanings enter them. **At integration,** after J2a's: rerun the builder and verifiers against the real lock (they then use it directly), re-stage E2a's entry on it, and replace E2a's two placeholder pins.

**Projection: one hundred and three rows.** Once inventory138 is selected, inventory137 becomes an ancestor, and every description meaning a lock selecting inventory137 binds to it is inherited by stable file path: its one hundred and three inheritance rows, as inventory137 projected them (inventory136's one hundred, and the three direct overrides of `read-endpoint-x3a2-descriptions` on inventory136: `installation_records.rs`, `installation_selection.rs` and `native_marker.rs`). No bound contract successor has a passage override or supersession on inventory137, and none is folded. One projected row, sorted after the inserted paths, moves.

- `verify_projection.py` is inventory137's helper with its comment updated for this parent, and it applies J2a's staged entry in memory when the given lock selects inventory136. Against the real lock at d2c00a9: PASS, 103 rows, 518 corruptions refused.
- `evidence/stage_lock_e2a.py` stages the lock change in the E2a worktree, as X3a-2 staged inventory136: HEAD's `design-lock.json` plus J2a's inventory137 entry exactly as J2a stages it, then the inventory138 entry, with the one hundred and three inheritance rows re-parented to inventory138. The parent, candidate, record and subject pins are real. E2a's review and assent pins are `SCRATCH-E2A/` placeholders, which integration replaces with the accepted review and the completed unit record. E2a has no contract successor.
- `evidence/verify_scratch.py` checks the staged lock (or, on an unstaged worktree, applies the same change in memory). It requires the staged lock to equal HEAD's plus exactly those entries and that inheritance, serves synthetic reviews and assents for J2a's and E2a's placeholders, runs the worktree's real `verify_design` on HEAD's lock, the lock with inventory137 and the lock with inventory138, and requires verify_design's own projected inheritance to equal the record's. It also checks that plain `verify_design` refuses the staged lock at the first placeholder (`SCRATCH-J2A/review.json` while J2a is staged), as it must until integration.
- `evidence/drift_scratch_e2a.py` runs the worktree's real public generator (`generate_contracts.generate`, the selected rebuild-02 generator, write false) with the same synthetic reviews and assents served in memory, as I1-a's drift gate did. It must pass with `changed: []`: E2a changes no generation input.
- `evidence/check_e0_pins.py` cross-checks the lane against E0's accepted record, independently of the lane. Every upstream tag and commit equals E0's `PINS.txt`, and the runtime crate's checksum equals E0's harness lock. All 72 retained members equal E0's per-file tag pins (sha256, length and git blob). All four `SymbolTableV1` records carry E0-REPORT's P3 digest prefixes and are byte-identical to the tables E0 recomputed from the natively linked `Language` and decoded from its modules. The SYN-NS members and the manifest normalizer equal SYN-NS's materialization map. Its output is `evidence/e0-crosscheck.json`.
