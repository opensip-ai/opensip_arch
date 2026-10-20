# D4-3 request classifier source preflight r2

**Verdict: PREFLIGHT-CLEAR**

**Subject manifest SHA-256:** `9b5b5077d781521d09d3ed1916a787c23b66751258fd1d4bc4f161c6ab9ab783`

The 1,711-byte manifest and all eleven declared members match their recorded sizes and SHA-256 digests. The production `candidate-invocation.rs` is byte-identical to r1 at `81143ba4146990a9bc0d90e7bab4dcb59a29de702a9c732cf5be40c28e724db9`. The only r2 candidate change is the constructor-control addition in `candidate-invocation_tests.rs`; the prior field, mode, format, request-variant, classification-order, and effect-absence controls remain intact. I1 and I2 remain permitted as ruled in r1.

## Prior finding disposition

### D4-3-PRE-R1-RF-1 — RESOLVED

The new assertion hashes the complete production `invocation.rs` bytes and its expected byte array exactly equals SHA-256 `81143ba4146990a9bc0d90e7bab4dcb59a29de702a9c732cf5be40c28e724db9`. The reviewed module contains one `impl AdmittedRequest`, one fresh `Self { ... }` construction in that impl, and the existing order proof requires validation, that construction, `request_excluded_form(&admitted)`, and `Ok(admitted)` in that sequence. The added scoped count requires exactly one `Self {` in the reviewed impl.

The full-module pin closes the weakness identified in r1. A second `Self` construction, a type alias, a macro or alternate spelling, an added impl, a production child module, or even a comment or whitespace change alters the module bytes and fails the pin. The test therefore does not need to parse arbitrary future Rust: updating the digest is an explicit review action. The current module has no alias, construction macro, unsafe/transmute route, `Default`, conversion, or deserialization implementation for `AdmittedRequest`. Its fields are private, so sibling modules cannot construct it. Its only child module is under `cfg(test)`; adding a production child changes the pinned bytes. Derived `Clone` preserves every field of an already classified value and does not create a different request state.

The retained literal `AdmittedRequest {` count is still only a spelling check, but it is now a secondary diagnostic beneath the exact full-source pin. It no longer carries the constructor-inventory proof by itself.

## Non-blocking observations

### D4-3-PRE-R2-NBO-1 — Final evidence remains outstanding

This is source preflight only. The runtime mutation that adds an internal `Self` constructor bypass, the complete owning evidence, and final unit review remain pending. This verdict grants no unit, production-composition, integration, inventory, or qualification acceptance.

No tests, builds, cargo commands, lanes, network access, private data access, other panes, delegation, or repository changes were used during this review.
