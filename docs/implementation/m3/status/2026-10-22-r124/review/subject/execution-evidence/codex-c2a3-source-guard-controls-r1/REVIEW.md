# Review: C2a3 draft source binding guard test append r1

**Verdict: SOURCE-AUDIT**

**Scope:** `uncompiled-test-source-only`

The frozen subject manifest SHA-256 is `c8989ffe332ab790436015651f947946aa69eba634973145caf43392ac0b3538`. All 10 declared members are ordinary files and match their declared byte counts and SHA-256 values.

No required findings.

The test change is append-only: the complete 38,765-byte before-file is an exact prefix of the 40,537-byte after-file. The suffix adds one private helper and exactly two `#[test]` functions, bringing this module from 22 to 24 test functions without changing existing test text or production source.

The positive guard is internally coherent:

- `include_str!("component_admission.rs")` names the production source beside the included test source and therefore binds the intended sibling file.
- `opensip_identity::RawSha256` is publicly re-exported by the frozen identity library. Its consuming `update` accepts the source bytes, returns a debuggable length error suitable for `expect`, and `finish` returns `[u8; 32]`.
- The embedded 32-byte constant is exactly `1233e3076ab94fa41750f1cb0874693a10601148aea596774bc16fad9ee37811`, which matches the frozen production source digest and the manifest.

The text controls are also coherent. Each of the five anchors occurs exactly once in the frozen source and each replacement is nonidentical. They cover payload-header insertion, payload reservation, Blob-count scanning, chunk copying, and the current `8E` callback coefficient. Any such replacement changes the bytes supplied to the same digest helper, so the pinned equality is refused. The test intentionally binds comments and formatting as well as executable text.

No evident Rust source error was found in the appended helper or tests. The fully qualified identity API needs no new import, the source length is far below `RawSha256`'s domain limit, and the helper's result type agrees with the 32-byte expected value.

The stated limits are accurate. These tests are exact-byte identity controls, not semantic analysis, a security boundary, runtime mutation tests, or proof that the guarded implementation satisfies M. The frozen source still uses coefficient `8`; an accepted `128E` implementation would change the source digest and must receive a separately reviewed pin update. The old queued compiler image excludes these controls and supplies no execution evidence for them.

The tests were neither compiled nor executed. Full source and operand bounds, ABI and native evidence, debit and cleanup behavior, export and lifetime controls, meaningful runtime mutations, complete M, unit acceptance, integration, and product qualification remain open.
