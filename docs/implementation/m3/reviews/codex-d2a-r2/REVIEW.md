# D2A-r2 review

Verdict: **ACCEPT-UNIT**. No required findings; one non-blocking observation about the precision of the privacy-mutation evidence.

Subject manifest: `docs/implementation/m3/supervisor-d/d2a-r2-subject.json`, 9,929 bytes, SHA-256 `1b633d2db9cfac5294715407f73215085dbb8b30a44e5851f647b5830409cb2a`. Independently rehashed all 44 members with no mismatch. The detached candidate is at `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`; all seven product-map entries match the candidate and architecture archive, and the mapped parent files match the base. The old integration-test path is absent.

## Prior findings and revised behavior

- **D2A-R1-RF-1 resolved.** `encode` checks host direction before creating the writer. All eight component-only variants return `ComponentMessage`; their body-writer branch is unreachable. The sixteen-type control checks all eight host outputs against the receiver and refuses all eight component inputs.
- **D2A-R1-RF-2 resolved.** Outgoing bodies pass strict parsing, the integer-domain walk, the closed schema member without identity substitution, and the UTF-8 byte-bound walk. This addresses the character-count versus byte-count nonce, oversized generated integers, refusal conditionals, and constructible invalid identity values. Nullable optional carriers explicitly refuse instead of disappearing. `bounded` admits exactly 65,536 body bytes and refuses one over. `ControlSession::send` additionally enforces policy identities, platform, frame offer and tuples, then checks the current session verdict. Every error path returns before `apply`; only acceptance advances state and sequence. No further constructible-invalid escape was identified through this sending boundary.
- **D2A-R1-RF-3 resolved.** `ControlContext.policy` and every `ControlPolicy` field are private. Public policy accessors return values or shared references. `for_session` fixes the bound and offer at 65,536 and supplies exactly one admitted tuple; the arbitrary reference constructor is test-only and crate-private. Moving the corpus tests in-crate does not expose that constructor to production. `observations_mut` exposes observations without mutable policy access. The three documentation examples address policy construction, mutation of a clone, and context reassembly. The evidence qualification below does not change the source-level privacy conclusion.
- **Prior NBOs addressed.** Schema loading now closes root keywords, with a corresponding negative control. SCOPE accurately reserves bounded stream acquisition for D3a: complete-frame classification and `body_buffered: false` do not establish how many transport bytes were acquired.

The receiver's precedence-sensitive processing remains intact: strict reader behavior, opaque future-major hello handling, sequence sentinel and identity substitution for schema validation, UTF-8 checking of received values, deferred sequence faults, and session/direction stopping. The corpus, matrix, deep nesting, long integer, duplicate-key and stopped-direction controls support the lack of regression.

## Evidence and rules

Reviewed the archived lane rather than executing Cargo, rustc, builds or the lane. Base and candidate have the same two suites and empty failure sets; the candidate adds 13 passing unit tests and three passing compile-fail documentation tests. The corpus/proof bytes match the architecture copies. Both architecture-side CC v5 source pins also match live hashes. The tests retain the byte-for-byte 480-case replay, full 16 × 8 × 2 matrix, prefix classification and bounded-stack probes.

All 16 recorded mutations are caught. Fifteen fail unit assertions; the privacy mutation fails a compile-fail documentation test because its example now compiles. The logs contain actual test failures, not compiler-error substitutes. The archived warning-denied all-targets Clippy, rustfmt classifications, package-edge check, ten environment-exception tests, operability check and verify_design all pass. Package edges are exactly the contracts dependency and identity dev-dependency. The runner's zero-new-suites constant agrees with the two-suite comparison.

Independently ran only the permitted operability source command: passed, 114 rows, no findings. Source inspection found no prohibited calls, environment reads or `let _ =` in the changed Rust files. Independently checked the 19-file census closure against changed/untracked paths: no intersection.

Inventory scope is correct: `control_protocol.rs` realizes its existing proposed codec row; the new inventory paths are the in-crate test module and the two vendored data files. The removed round-one integration-test path is not an addition.

## D2A-R2-NBO-1 — Narrow the privacy-mutation evidence claim

SCOPE says making the fields public makes all three documentation examples compile and cites `policy-made-public`. The runner changes only `ControlContext.policy` to public, leaving `ControlPolicy` fields private. Its log therefore shows two compile-fail tests still passing and only the context-reassembly example at line 953 compiling successfully. `controls.json` marks the mutation caught correctly, but its `failed` list is empty because the extraction omits documentation-test names.

Narrow the stated evidence to the reassembly example, or add a separate policy-field mutation for the other two examples. Include the failed documentation-test identity in the summary. This is non-blocking: production privacy holds on inspection, the three original documentation tests pass, and the recorded mutation genuinely detects the context privacy breach.

Acceptance covers this codec unit only. It does not establish D3a transport acquisition or caller integration, D2 completion, provider-protocol implementation, or product qualification. No repository, worktree or control file was edited; only the two requested review artifacts were written.
