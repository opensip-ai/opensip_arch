# Review: native-owner complete materialization unit r1

**Verdict: REQUIRED-FINDINGS**

Subject-manifest SHA-256: `b1fcfe05e05ad1a0ac7cff4ee1459511bf6879c784c662f8771213c1690ab841`

## Required findings

### OWNPAT-UNIT-R1-RF-1 — The corrected path forms escape the native-owner interpreter boundary

The bound generator profile keeps the inherited Rust interpreter at 72 forms, classifies the two corrected complete-relative-path literals as newly recognized native-owner forms, and requires foreign targets and `patternProperties` to retain the inherited table. The candidate instead inserts both literals into the shared `TABLE` in `crates/identity/src/schema_patterns.rs` and implements them as `Kind::CompleteRelativePath`. The generic `matches()` function therefore accepts them.

This changes behavior outside the three selected native owners. `Program::pattern_matches` sends every foreign resolved owner to `matches()`, while schema compilation and evaluation send every `patternProperties` key directly to `matches()` regardless of owner. Consequently, a foreign schema using either corrected literal as `pattern`, or any schema using it as a `patternProperties` key, is now admitted and evaluated where the predecessor returned `Error::Pattern`. Strict construction of the present 52-source registry limits current registered reachability, but it does not preserve the reviewed interpreter boundary: `Program::compile_registered_native_owners` accepts constructed document sets, and the candidate's own isolation tests exercise that interface with foreign documents.

The archived controls do not cover this expansion. The inherited differential iterates only `original::selected_patterns()`, so the reported 72-form comparison never calls the candidate with the two newly added shared-table forms. The foreign and `patternProperties` tests use other literals, and `native-dispatch-leaks-to-foreign` mutates owner dispatch rather than the shared table.

Keep the two corrected complete-relative-path literals out of the inherited `TABLE` and evaluate them within the native-owner path, or obtain a separately accepted expansion of the inherited interpreter profile. Add controls proving that each literal is accepted with the intended semantics under the selected native `pattern` owners, refused as a foreign `pattern`, and refused as a `patternProperties` key. The inherited-profile control must also establish that the candidate's shared selected-form set remains exactly the predecessor's 72 forms. Freeze and rerun the affected source, identity/host, differential, mutation/restoration, formatting, and complete owning evidence on the repaired bytes.

## Independent checks

- Rehashed all 363 declared manifest members and confirmed the only staged file outside that membership is the subject manifest itself. Its bytes match the requested SHA-256. The 42-row product map is unique and exact: 27 archived parents match the pinned product base, all archived candidates match their mapped hashes, and all 15 new paths are absent from that base.
- Confirmed the live product and architecture heads match the pinned bases, and the archived authority copies bind accepted designs 179, 180, and 181 through exact record, subject-manifest, review, and assent bytes. The final source maps remain 43 generator sources, 52 admission sources, and 15 aliases, with no added dependency, entrypoint, semantic source, or package owner.
- Confirmed the final schema edits are exactly the declared 34 plus one pattern-literal substitutions, with all other bytes unchanged. The three selected resolved documents contain 137 pattern nodes and exactly 26 forms. The generated-output audit accounts for eight outputs, 43 embedded documents, 73 registry controls, and 886 entrypoints; seven outputs are byte-exact and the report is the sole changed output. Ordinary generation records zero drift, and all three TypeScript owning lanes bind loader policy 181.
- Confirmed the historical 41-path preflight is not used as acceptance of the final image. R2 covers that 41-path image and retains only the three host integration failures. R3 adds only `crates/host/tests/admission_tests.rs`, keeps the preceding 41 source bytes exact, and reruns the complete host suite and all-target warning-denied Clippy successfully. R4 changes only rustfmt layout in `native_owner_tests.rs` and `admission_tests.rs`, keeps the other 40 paths exact, and reruns the full host suite and Clippy on the final 42 hashes. Its formatting classification is clean.
- Confirmed the ordinary storage release check succeeds and the crash-matrix feature refuses release compilation at its intended source guard. The added host fixture reader selects the rebuilt replay corpus. The manifest guard adds only lifecycle fixture forwarding allowed by CI PLAN-r3 LD-CIP-3 and preserves default and dependency-route refusals.
- Confirmed all 14 compiled mutation records are runtime test failures rather than compile failures, and each restores its exact original pin. The unchanged-main distinctions and prior failures remain preserved rather than waived.
- Independently checked the 15 companion additions and their retained predecessors. The correspondence accounts for all 9,127 object and 4,580 blob occurrences, preserves deliberate malformed status and opaque bytes, and maps all 116 indexed native selections exactly. The two runtime registry companions make only the declared three native-SHA substitutions.
- Compared the 526 full-walk cases after inverse identity mapping. Exactly 12 request populations retain the declared 14 existing base facts, while the other 514 selections are exact and every intended mutant remains selected. Exactly two typed negative results change for the documented malformed `FilePayloadV1` schema refusal and foreign-view `REFERENCE_PLAN_JOIN`; the other 524 verdicts are equal. The rejected foreign-FACT change is absent and remains `invalid` / `REFERENCE_SOURCE_JOIN`.
- Confirmed the security companion is the exact flat current subset with 23 objects and 46 blobs, and that only test/debug storage helpers select it. Production storage admission remains outside those fixture-selection edits.

## Boundary

The additive 15-path inventory and retained-predecessor descriptions remain post-integration obligations. The blind receipt is still `STALE` / `PENDING`; no census-dependent claim was reviewed. This review does not establish integration, current blind margin, D4/CI4, or whole-project qualification.
