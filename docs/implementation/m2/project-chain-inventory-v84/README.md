# Project chain inventory84

Adds exactly two sources to inventory83 (unit X3a-1, committed in arch and under review; not yet selected):
- crates/security/src/custody/project_chain.rs
- crates/security/src/custody/project_chain_tests.rs

It keeps all 756 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 758 planned files. No crate or dependency is added. The rows are unit X2a, law X2 r5 items 1 to 3 and 9, and the custody half of item 4.

- project_chain.rs (composition) walks and judges the chain from `/` to a selected project root with charged, retained, no-follow handles, and samples the root's native birth with the existing sampler. It grants nothing. Each refusal names its item 8 row and subject for X2b to project.
- project_chain_tests.rs (test) checks it on scratch homes under the temp directory with a test omission premise.

**Order.** This successor depends on inventory83 (X3a-1), which depends on inventory82, which product 84a8bfd selects together with the X10b contract successor. If X3a-1's review changes inventory83, this inventory is rebuilt. evidence/build_v84.py refuses to write over any path git already tracks.

**Changes to existing rows.** custody.rs gains only the `project_chain` module declaration; its description stays true. No other existing source changes. X2a touches none of the files X3a-1 changes, apart from that one declaration block in custody.rs (X3a-1 adds `store_endpoint` there).

**Projection.** The sixteen effective description overrides bound to inventory83 (carried unchanged from inventory82 and inventory81) stay bound by stable file path, with parent inventory83. verify_projection.py is inventory83's helper with only its comment corrected. Because the real lock selects inventory82, evidence/scratch_lock.py writes a scratch lock (outside both repositories) that selects inventory83, and the helper runs against it. evidence/verify_scratch.py appends inventory83 and then inventory84 in memory over the real lock, with synthetic reviews and assents.
