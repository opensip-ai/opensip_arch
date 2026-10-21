# CODEX2 review — NATIVE-OWNER-COMPANION-FIXTURE-REPAIR-r1

**Verdict: ACCEPT-UNIT**  
**OWNPAT-CBRUN-R1-NBO-1 closure after exact root integration: accepted**  
**Product qualification: no**

The subject manifest is byte-exact at `690c9af13be1db096b13368adac7e90d1f0b7c571905e91cab5fe537129860b8`. All 14 subject members and all eight authority pins rehash exactly. Product main is clean at the accepted receipt integration `91f422b11bedac820d27c52289c2a499cf4c757f`. The detached same-repository repair worktree is at that commit and has exactly one modified existing product path, `tools/tests/test_snapshot_ledger_census_blind.py`; there is no staged or new path. Current architecture is `90f6cff103173f1eb92bd3acf504c46d20801489`.

## Rulings

- **NBO1 closure — ACCEPT.** The candidate adds exactly `paths |= {p for _, p, _ in model.VCS_ANCHORS}` to the existing synthetic `bound_product` fixture constructor. Removing that one line reproduces the parent bytes exactly. Parent, candidate, and archived bytes match every declared pin. Independent AST comparison finds the same 21 test methods in parent and candidate and byte-for-AST equality for every body, assertion, and expected verdict. The model's `VCS_ANCHORS` resolves to exactly `crates/security/src/snapshot_vcs.rs` and `crates/security/src/snapshot_vcs_tests.rs`; neither belonged to the fixture's prior copied sets, and both are present in the accepted companion receipt's current `snapshotSources` binding. The preserved original failure log shows all 21 tests errored in setup at the first absent VCS source, before their assertions, which agrees with this missing-set diagnosis.

  The direct product validation used the candidate file itself, with no adapter. Its frozen logs and report show exactly 21 companion controls passing, exactly 25 discovery controls passing, design verification passing, and the public current-binding comparison passing. No intended control was skipped or filtered. The four integrated receipt/census files rehash identically in clean main and the repair worktree at their accepted pins. The checker records zero real blind invocations, uses synthetic stores, and invokes no census mode. Its source and the one-file Git diff contain no runtime, model, tool, cost, cap, population, disclosure, design-lock, authority, source-registration, production-caller, or qualification change. Independent acceptance here plus substantive root assent and exact integration of this one candidate file is sufficient to close `OWNPAT-CBRUN-R1-NBO-1`.

- **Metadata scope — ACCEPT.** Inventory v234 contains exactly one row for the path, and it is byte-identical to the archived evidence row: package `tooling`, role `test`, `generated: false`. Its description already covers the unchanged hermetic synthetic-store controls, receipt behavior, refusal and lifecycle cases, and the premise that every product path named by the tool and model is bound. Because the repair only makes the fixture satisfy that existing premise while preserving all 21 test meanings, it creates no additive inventory path, new package or role meaning, description override, passage override, inheritance change, or source39 semantic registration. Existing inventory 234, description 182, and 117-entry inheritance scope therefore remain applicable.

## Remaining obligation

- **OWNPAT-CFIX-R1-NBO-1.** After substantive root assent and exact one-file integration, a separately reviewed status reconciliation must record closure of `OWNPAT-CBRUN-R1-NBO-1`. That bookkeeping obligation does not block this code-unit acceptance and grants no broader product or project qualification.

No build, test, Cargo command, lane, census mode, blind mode, private-data access, network access, or repository/worktree/stage/control/evidence edit was performed during this review.
