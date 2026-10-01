# Namespace admission and lease inventory110

Adds exactly two sources to inventory109 (unit X12b, selected at product 6dd7363; first built on inventory105, unit X2c, at product 0206ce8, and accepted there in Grok X2d r1):
- crates/security/src/custody/namespace_lease.rs
- crates/security/src/custody/namespace_lease_tests.rs

It keeps all 786 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 788 planned files. No crate or dependency edge is added: the module uses only `opensip-identity` and `opensip-platform`, which security already depends on. In particular it does not depend on `opensip-lifecycle`, whose private two-lock lease composition it mirrors. The rows are unit X2d: law X2 r8 item 7 (namespace admission and leases, returning `FencedNamespace` with the fence still held), with item 8's rows and item 9's budget for those steps.

- **namespace_lease.rs (composition).** custody.rs's macOS module `namespace_lease`, beside X2c's `first_registration`, so the gate's, the session's, the admission's and the registered project's private types stay crate-private. It holds `NamespaceSubject`, the `FenceHolder` seam that the writer's gate and the read session implement, the namespace confirmation, `NamespaceTarget` (the floor-step seam), the lease, `FencedNamespace` and the refusal rows.
- **namespace_lease_tests.rs (test).** Its `cfg(test)` child module: X2d's cases on scratch homes.

**Changes to existing rows.**
- `custody/ordinary_writer.rs`: `OrdinaryWriteAdmission` gains `admit_namespace` and the `FenceHolder` implementation for the writer's gate (each step on the gate's ledger with the write receipt's premise, then the gate's recheck and the receipt's recheck; any refusal spends the gate). Its description was already out of date after X3a-1 and X2c and stays so; an inventory successor carries rows by value, so the same later description-only contract successor that inventory97, 101, 102 and 105 named must refresh it.
- `custody/installation_read.rs`: `ReadSession` gains `admit_namespace` (SHARED-READ only, through `lease_shared`), `NamespaceSessionRefusal`, and the `FenceHolder` implementation for the session. The description stays true: a shared lease is not a write capability.
- `custody/first_registration.rs`: `ProjectWriteRefusal` gains `Namespace`, `RegistrationRow` gains `Busy` (item 8's busy row), `Step` gains `Lease`, and some owner checks and constants become `pub(super)` for reuse. Its description stays true: that file still takes no lease.
- `custody.rs`: declares the `namespace_lease` module. The description stays true.

No other existing source changes.

**Order.** This successor's parent is the inventory the real product lock selects: inventory109 (unit X12b) at product 6dd7363. evidence/build_v110.py reads the parent from the lock and maps inventory105 or inventory109 to the successor record that bound its sixteen rows; the rebase from inventory105 changed only the parent and the product base, since X12b touched only crates/host and the lock. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory110. inventory106 and 108 are other units' in-flight candidates; none is read or written here.

**Projection.** The sixteen effective description overrides bound to inventory109 (carried unchanged back to inventory81) stay bound by stable file path, with parent inventory109. verify_projection.py is inventory105's helper with only its comment corrected to name its parent. It runs against the real lock at 6dd7363, which selects inventory109. evidence/verify_scratch.py appends inventory110 in memory over the real lock, with a synthetic review and assent.
