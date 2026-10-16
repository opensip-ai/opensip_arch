# B3-b description successor (contract successor 170)

**Lead record, 2026-10-17. Proposed; it needs Codex review and root assent.**

This successor refreshes three inventory row descriptions that no longer describe their files. B3-b2b2b r3 restructured the D15 decision core's branch A under plan amendment A4 and regenerated its member vectors from B3-b0 r4 (contract successor 169). The rows B3-b2b1 wrote still describe the removed trial walk and B3-b0 r3 (successor 168).

The successor uses passage overrides on the rows of `docs/implementation/m2/repository-file-inventory.v206.json` (the v206 candidate). An additive inventory successor must keep every inherited row equal by value, so v206 cannot change these rows itself.

**Description only.** No inventory row other than the three descriptions changes. Nothing changes in the schema, product, law or any package. It binds in the same lock commit as v206.

| Row | Why the old text is stale |
| --- | --- |
| `crates/security/src/custody/workspace_declarations.rs` | It says "two phases around the trial walk" and "no consumer yet". Since B3-b2b2b r3, branch A is the array gate, then the member decisions, then the caller's one walk, with links after it. Item 6b's outcome carries gitlinks. The composition consumes it. |
| `crates/security/src/custody/workspace_member_vectors.json` | It names B3-b0 at contract successor 168 and a `trial` field. The vectors now come from B3-b0 r4 (169), with `walk`, `sixB`, `forbiddenReads`, the gate's and walk's refusal kinds, and the non-string arrays listed by id. |
| `crates/security/src/custody/workspace_declarations_tests.rs` | It says the core touches "none of the checker forbidden paths". Since B3-b2b2b r3, the checker's unread paths may be looked up where placement passes them, and must only never be read. The tests also compare branch A's walk members and gitlinks, and item 6b's consultations, exactly. |

`successor.json` gives each override's exact before and after text.
