# M3-P0 inventory135

Adds exactly one file to inventory134 (unit L1, selected at product 2967905 and still at cd5958b, where no later unit has an inventory successor):
- tools/host/dependency-policy.json

It keeps all 968 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 969 planned files.

The row belongs to unit M3-P0, the package scaffolds of the accepted M3 plan (`docs/implementation/m3/M3-PLAN-r6.md:208`).

- **tools/host/dependency-policy.json (registry, package `tooling`).** The host-workspace selection policy. Its first rows are law M3-C r7 item 12's pure-Rust inflater (`snapshot-plan-c/PROPOSAL-r7.md`, CRATE-ARCHIVE-1 rule 1 and the rejected tar-crate reader): miniz_oxide 0.9.1 and its one dependency, adler2 2.0.1. Consumer `opensip-host`; linking unit C3a. A row links nothing. No manifest names either crate, and `Cargo.lock` gains no registry package.

**Planned rows realized or changed.** Every row is kept by value. Each description stays true.
- **`crates/components/Cargo.toml`, `crates/components/src/lib.rs`, `crates/syntax/Cargo.toml`, `crates/syntax/src/lib.rs`** (new bytes). Each crate has a manifest and a doc-only `lib.rs`: no dependency, module or public item. The modules come from their laws' units: M3-E1 r3 item 20 for syntax (E2b, E2c), M3-D r3 for components (D2a, D2b, D3a, D3b, D4).
- **`Cargo.toml`** adds both crates to `members`. **`Cargo.lock`** gains their two path-package entries and nothing else.

**No new edge.** The added row is in the `tooling` package, which declares no dependencies. Neither scaffold declares an internal or external dependency, so the host lane's package-edge check passes against inventory134 and inventory135 alike. The packages `opensip-syntax` and `opensip-components`, and their permitted edges, were already in the parent. The builder asserts these facts.

**Order.** Its parent is the inventory the real product lock selects: inventory134 (unit L1) at product cd5958b. Succession is by the lock's parent pin. `evidence/build_v135.py`:
- reads the parent from the lock;
- checks every meaning the lock binds to the parent before carrying it;
- writes only its two paths;
- refuses tracked paths, and refuses while a lock selects inventory135.

Reruns reproduce the same bytes.

**Projection: one hundred rows.** Once inventory135 is selected, inventory134 becomes an ancestor, and every description meaning the lock binds to inventory134 is inherited by stable file path:
- the fifty-five inheritance rows (the sixteen carried from inventory81 onward and D1's thirty-nine, with D2's four supersessions already folded);
- contract successor D3's forty-five direct overrides on inventory134 (`description-batch-d3/successor.json`).

D3's seventeen supersessions on inventory134 each name an inherited row's current meaning and are folded into its effective description (law VD1). No other bound contract successor has a passage on inventory134. Only one projected selector moves, by one: `tools/tests/test_check_crash_matrix.py`, the one projected row sorted after the inserted path.

- `verify_projection.py` is inventory134's helper, with its row count (100) and comment updated for this parent. It runs against the real lock at cd5958b: PASS, 100 rows, 503 corruptions refused.
- `evidence/stage_lock_v135.py` stages the lock change in the P0 worktree, as F8b staged its binding: HEAD's `design-lock.json` plus the inventory135 entry and the one hundred inheritance rows re-parented to inventory135. The parent, candidate and record pins are real. The review and assent pins are `SCRATCH-P0/` placeholders, which integration replaces with the accepted review and the completed unit record. The lock has no separate selected-inventory field.
- `evidence/verify_scratch.py` checks the staged lock (or, on an unstaged worktree, applies the same change in memory). It requires the staged lock to equal HEAD's plus exactly that change, serves a synthetic review and assent for the two placeholders, runs the worktree's real `verify_design` on the locks without and with inventory135, and requires verify_design's own projected inheritance to equal the record's. It also checks that plain `verify_design` refuses the staged lock at `SCRATCH-P0/review.json`, as it must until integration.
