# Host policy-pack admission inventory109

Adds exactly one file to inventory105 (unit X2c, selected at product 0206ce8):
- crates/host/src/configuration_tests.rs

It keeps all 785 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 786 planned files. The row is unit X12b: law X12 r3 items 1, 5, 7 and 8 on the host side, and item 10's host cases (X12a judgment call 14).

- **configuration_tests.rs (test).** configuration.rs's `cfg(test)` child module, included as doctor_ingress.rs includes its tests. It holds item 10's host cases: NT-1 and NT-2 through `admit_policy_selection`, the selection count, the exhaustive mapping onto generated members, the X12-0 remedy bytes through the shared failure envelope, and the purity and "no evaluation" source pin.

**Existing rows that change in the product, with their descriptions unchanged.**
- `host/src/configuration.rs` is already a planned row ("Resolve admitted configuration layers, registry selections and provenance."). X12b creates it with the M2 slice only: the policy selection is a registry selection, admitted against the bundled pack registry (law item 1). Layers, discovery and provenance arrive with M3 in the same file, so the row stays true and is kept by value.
- `host/src/doctor_ingress.rs`: `doctor_envelope`'s refused arm becomes the shared `failure_envelope`, which the X12 rows use too, and `row_remedy` gains the `CONFIG.INVALID` (X12-0) and `POLICY.IMPERATIVE_KEY_REFUSED` remedies. Doctor's own output is unchanged. "Remedies are the selected golden's where one exists and otherwise one fixed text per row" stays true.
- `host/src/lib.rs` declares the private `configuration` module (`#[allow(dead_code)]`, the security crate's precedent for unwired library modules). "Keep internal modules private" stays true.
- `host/Cargo.toml` moves `opensip-evaluator` from dev-dependencies to dependencies. The host -> evaluator edge is already in the inventory's package row, so the package graph is unchanged; `check_package_edges --lane host` passes against inventory109. Cargo.lock does not change.

**Order.** Its parent is the inventory the real product lock selects: inventory105 (unit X2c) at product 0206ce8. evidence/build_v109.py reads the parent and the successor record that bound the sixteen inherited rows from the lock itself, so it reruns unchanged when v106 or v108 integrates first. Succession is by the lock's parent pin, not by number. It refuses to write over any path git already tracks, and while a lock selects inventory109.

**Projection.** The sixteen effective description overrides bound to inventory105 (carried unchanged back to inventory81) stay bound by stable file path, with parent inventory105. verify_projection.py is inventory105's helper with only its comment generalized. It runs against the real lock at 0206ce8, which selects inventory105. evidence/verify_scratch.py appends inventory109 in memory over the real lock, with a synthetic review and assent.
