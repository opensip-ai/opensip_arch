# Bundled policy-pack admission inventory104

Adds exactly five files to inventory101 (unit X3b-2, selected at product 9dbefb9):
- crates/evaluator/src/pack-registry.json
- crates/evaluator/src/policy_pack_tests.rs
- crates/evaluator/tests/fixtures/policy-pack-plan-fixture.json
- crates/evaluator/tests/fixtures/policy-pack-test-fixture.policy.json
- crates/evaluator/tests/fixtures/policy-pack-test-registry.json

It keeps all 778 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 783 planned files. No crate or dependency edge is added: the evaluator already depends only on identity. The rows are unit X12a, law X12 r3 items 2 to 7 and 9 (evaluator side), and item 10's evaluator cases.

- **pack-registry.json (registry).** The bundled release registry, compiled in with `include_bytes!`. Zero rows in M2.
- **policy_pack_tests.rs (test).** policy.rs's `cfg(test)` child module `pack_tests`, holding item 10's evaluator cases and the synthetic test registry.
- **Three fixtures.** The synthetic test registry, its one policy document (the golden-typescript policy blob of plan-policy-fixtures.json), and a corpus Plan with its analysis-spec for `check_plan_pack`.

**Changes to existing rows.**
- `evaluator/src/policy.rs` gains the pack registry reader, `PackSource`, `SuppliedProvenance`, `AdmittedPack`, `PackDefect`, `PackRefusal`, `admit_pack`, the imperative classifier, `PlanPackChecks` and `check_plan_pack`. Its private traversal counter moves into a `Meter`, so the rule and atom laws run without retained inputs; the three existing inspectors behave the same. It includes three pinned schema sources (policy-v2, common-v1, imported-v1) for the classifier. Its description ("Admit and compile the closed declarative policy language; own the pure portable glob predicate …") stays true.
- `evaluator/src/lib.rs` exports the new names. Its description stays true.

No other existing source changes.

**Order.** Its parent is the inventory the real product lock selects: inventory101 (unit X3b-2) at product 9dbefb9. It was first built on inventory102 at 920941b; X3b-2 integrated before review, so evidence/build_v104.py rebuilt it on inventory101 with the same five rows (one more parent-map entry). The builder reads the parent from the lock, and maps inventory102 and inventory101 to the successor records that bound their sixteen rows. The number 104 sits above its parent's 101 and above 102; succession is by the lock's parent pin, not by number. It refuses to write over any path git already tracks, and while a lock selects inventory104.

**Projection.** The sixteen effective description overrides bound to inventory101 (carried unchanged from inventory97 back to inventory81) stay bound by stable file path, with parent inventory101. verify_projection.py is inventory102's helper with only its comment corrected. It runs against the real lock at 9dbefb9, which selects inventory101. evidence/verify_scratch.py appends inventory104 in memory over the real lock, with a synthetic review and assent.
