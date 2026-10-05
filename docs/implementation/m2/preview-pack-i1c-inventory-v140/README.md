# I1-c inventory140 (the X12c preview pack's release row)

Adds exactly one row to inventory139 (unit J3a). It belongs to unit **I1-c** of law M3-I1 r3 (`docs/implementation/m3/preview-pack-i1/PROPOSAL-r3.md`, accepted; item 5, with item 7's amendments to X12 r3), which ships the pack contract of the bound contract successor I1-P (`docs/implementation/m3/preview-pack-i1/i1-p/`).

**Parent: inventory139, not yet integrated.** The lead assigned I1-c inventory140 on J3a's inventory139 (`durable-entry-j3a-inventory-v139/`, built on inventory138, which the lock at product `083ad5c` selects): the next number on the highest existing candidate. J3a's candidate is staged and untracked, and its review request is not yet written. Until J3a is integrated, every script here applies J3a's staged entry in memory, from J3a's own `evidence/verify_scratch.py` (its SCRATCH-J3A placeholders), exactly as J3a stages it. Only inventory139's candidate, record and projected meanings are used, and those do not depend on J3a's review pins. **If J3a's candidate changes, or another unit's inventory integrates first, this candidate must be rebuilt** on the new parent, with its record, subject, staged lock and review pins.

The one row is in the existing `opensip-evaluator` package:
- **`crates/evaluator/src/preview-typescript-pack.v1.policy.json`** (registry): the bundled `PolicyDocumentV2` of `opensip.preview.typescript.pack:1`, I1-P's candidate byte for byte (574 bytes, sha256 `96675a5e…`, law item 5.2's block, no trailing newline). `policy.rs` includes it with `include_bytes!` as the one `RELEASE_PACKS.documents` entry, under the name the release row's `policyDocument` gives.

It keeps all 1011 existing rows of inventory139 by value, along with the packages and their edges, the pending decisions and the carried unresolved obligations, for 1012 planned files.

**Planned rows changed.** Four planned rows change bytes (`plannedRowsChanged` in `successor.json`):
- `crates/evaluator/src/pack-registry.json`: I1-P's candidate byte for byte (679 bytes, `d08a85de…`), one row and the standing text I1-P fixes (LD-P1);
- `crates/evaluator/src/policy.rs`: the `RELEASE_PACKS.documents` entry and its doc comment;
- `crates/evaluator/src/policy_pack_tests.rs` and `crates/host/src/configuration_tests.rs`: the flipped X12a and X12b tests and the self-checks S1 to S9.

`policy.rs`'s row stays true. **Three descriptions go out of date**, and an inventory successor carries rows by value, so they are left for the next description-only contract successor, as earlier units left theirs:
- `pack-registry.json`: "Zero rows in M2, with an empty documents table: every named pack is refused as not bundled until the DR-131 row and its content arrive in X12c." X12c has now arrived: the registry has that one row, and its documents table holds the one document.
- `policy_pack_tests.rs`: "opensip.preview.typescript.pack:1 itself, not bundled in M2" and "zero release rows". That ID now admits from the release registry; the registry has exactly one row; and the self-checks S2, S4, S5, S7 and S8 are new tests. The description also predates I1-b1's four op-law tests.
- `configuration_tests.rs`: "over the release registry, which has zero rows" and "opensip.preview.typescript.pack:1 itself" among the row-1 identities. That ID is now admitted (S9), and its exact bytes supplied are row 2.

Suggested texts for that successor, which bind nothing here:
- `pack-registry.json`: replace the "Zero rows in M2 …" sentence with "Exactly one row since X12c (law M3-I1 r3 item 5, contract successor I1-P; unit I1-c): opensip.preview.typescript.pack:1, the DR-131 preview pack, over the sibling preview-typescript-pack.v1.policy.json, the documents table's one entry."
- `policy_pack_tests.rs`: "… and the evaluator's cfg(test) ID) refused as not bundled, while the release row opensip.preview.typescript.pack:1 admits by its exact ID; …; exactly one release row, self-consistent, with its canonical document and the digests I1-P pins (law M3-I1 item 5.6, S1 to S8), its exact bytes supplied as row 2, and check_plan_pack over a release-pack Plan; …; and law M3-I1 item 2.2's cycle-representative op law on synthetic test packs."
- `configuration_tests.rs`: "… over the release registry, whose one row, opensip.preview.typescript.pack:1, admits as the evaluator's AdmittedPack with I1-P's digests and whose exact bytes supplied are row 2 (S9): NT-1 wrong identities (… the empty string, and the evaluator's cfg(test) ID, unreachable from the host) are row 1 …"

**No new edge, crate or dependency.** The row is in `opensip-evaluator`, which declares only `opensip-identity`. No manifest, `Cargo.lock` or dependency policy changes; `include_bytes!` reads a sibling file at compile time. The builder asserts that the added path is new, every changed path is planned, and no added or changed row carries a bound meaning.

**Order.** `evidence/build_v140.py`:
- takes the lock (by default the product checkout's), applies J3a's staged entry in memory while that lock selects inventory138, and requires the result to select inventory139 with J3a's successor record;
- checks every meaning the lock binds to the parent before carrying it;
- writes only its two paths;
- refuses tracked paths, and refuses while a lock selects inventory140.

Reruns reproduce the same bytes, whether J3a is staged in memory or integrated, because only inventory139's candidate, record and meanings enter them. **At integration,** after J3a's: rerun the builder and verifiers against the real lock (they then use it directly), re-stage I1-c's entry on it, and replace I1-c's two placeholder pins.

**Projection: one hundred and three rows.** Once inventory140 is selected, inventory139 becomes an ancestor, and every description meaning a lock selecting inventory139 binds to it is inherited by stable file path: its one hundred and three inheritance rows, as inventory139 projected them (inventory138's, which are inventory136's one hundred and the three direct overrides of `read-endpoint-x3a2-descriptions` on inventory136). No bound contract successor has a passage override or supersession on inventory139, and none is folded. One hundred projected rows, sorted after the inserted path, move.

- `verify_projection.py` is inventory138's helper (E2a's) with its comment updated for this parent, and it applies J3a's staged entry in memory when the given lock selects inventory138. Against the real lock at `083ad5c`: PASS, 103 rows, 518 corruptions refused (`verification.*`, `verifier-anchor.json`).
- `evidence/stage_lock_i1c.py` stages the lock change in the I1-c worktree, as E2a staged inventory138: HEAD's `design-lock.json` plus J3a's inventory139 entry exactly as J3a stages it (checked equal to J3a's own staged worktree lock), then the inventory140 entry, with the one hundred and three inheritance rows re-parented to inventory140. The parent, candidate, record and subject pins are real. I1-c's review and assent pins are `SCRATCH-I1C/` placeholders, which integration replaces with the accepted review and the completed unit record. I1-c has no contract successor.
- `evidence/verify_scratch.py` checks the staged lock (or, on an unstaged worktree, applies the same change in memory). It requires the staged lock to equal HEAD's plus exactly those entries and that inheritance, serves synthetic reviews and assents for J3a's and I1-c's placeholders, runs the worktree's real `verify_design` on HEAD's lock, the lock with inventory139 and the lock with inventory140, and requires verify_design's own projected inheritance to equal the record's. It also checks that plain `verify_design` refuses the staged lock at the first placeholder (`SCRATCH-J3A/review.json` while J3a is staged), as it must until integration.
- `evidence/drift_scratch_i1c.py` runs the worktree's real public generator (`generate_contracts.generate`, the selected rebuild-02 generator, write false) with the same synthetic reviews and assents served in memory, as E2a's drift gate did. It must pass with `changed: []`: I1-c changes no generation input.
