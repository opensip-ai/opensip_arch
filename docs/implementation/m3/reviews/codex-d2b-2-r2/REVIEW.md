# D2B-2-r2 review

**Verdict: ACCEPT-UNIT.** D2B2-R1-RF-1 and D2B2-R1-RF-2 are resolved. No required findings or non-blocking observations.

Subject manifest SHA-256: `758e7035b4f51a24c04f967b79b6c24e1b7821d1eea8ec22c603df794e0abd3a` (9,203 bytes). All 40 members match their pinned lengths and hashes. Verified product-map candidates against the worktree and archives, the existing file's parent pin, authority/prior-round pins, and the package-base lock. The candidate is detached at `4ece8495b3a599dbd1f14009458c94b60d1836c8` with the declared seven paths, six new.

## Findings resolved

**RF-1:** Loading now checks the complete singleton stageDependentTransitions mapping: the expected key and its protocol-specific prose value. P3_STAGE and T2_STAGE equal the respective published table texts exactly. A missing, changed or non-text value cannot pass the value comparison; unsupported content refuses Law. The engine's existing increment-and-resolve behavior is unchanged.

The new test changes the increment text and substitutes null under both protocols. Independently checked the repinning substitutions: all four altered inputs have correct carrier-owned SHA-256 and length pins, so the test exercises content validation rather than an earlier Pin refusal. The recorded stage-law-value-unchecked mutant fails this test specifically.

**RF-2:** check_no_overlay admits exactly base, overlay and unavailableSelection. Unknown members refuse Law; all three supported members are required by their subsequent checks. The base is a two-member object with pin ts2order and the textual rule count derived from the loaded T2O rules. Its exact no-overlay declaration and payload-selection note match the current carriers. Altered values, nulls, wrong metadata and unsupported executable members cannot be silently ignored.

The new control covers changed/null declarations, added stateUpdateAdditions and stateAdditions, a changed selection note, and wrong base rule count/pin. The two corresponding mutations—open TS2 members and an unchecked declaration—fail that control. The engine still consumes the host-derived unavailablePayload observation; payload selection and per-frame contextual admission remain outside this engine with the codecs. No wire admission duty moves into table matching.

## Evidence and regression assessment

Compared the round-two product archive with round one. Only table.rs and table_tests.rs change, implementing these guards and two loading tests. The module declaration, vendored tables and reference-vector bytes are unchanged. Both vendored documents equal their architecture sources and match their carrier source pins. The previously reviewed first-match, pre-match, overlay, total-fallback, stage resolution and process-observation behavior therefore carries over.

The permitted live vector --check completes successfully with `current []`, reproducing the reference vectors byte for byte. The permitted live operability source check passes with 114 rows and no findings. No compiler, Cargo, build or lane was run for this review.

The recorded round-two lane reports 35 base versus 43 candidate components passes, zero failures, equal suite counts and eight new tests, with no differing/flaky cases. All eight table tests pass. Formatting and warning-denied all-targets Clippy pass. Vector check, vendored-byte comparison, package-edge policy, ten environment-exception tests, operability, unchanged-closure check and verify_design pass as recorded. Components' internal dependencies remain contracts and identity.

All eleven mutations produce table-test failures rather than compilation failures. The three new mutants are caught by their new loading controls; the eight original interpreter mutants remain caught. The census closure's 19 paths have no intersection with the seven changed paths. No new mint-census call, environment read or prohibited discard is introduced by this revision.

The lane base is `2b24f319882d41fa4688a6a55bc1ed431fdfb78c`. Git confirms the package base adds exactly the v219 inventory-lock commit and changes only design-lock.json. Carrying the lane across this lock-only rebase is sufficient for the unchanged table implementation; no fresh package-base lane or design-verification execution is inferred.

This accepts the table engine library only. Complete codecs, contextual admission, process supervision, callers, the six-path inventory successor and product qualification remain outside this acceptance. Neither D2b nor M3 completion is claimed.

Only read-only inspection, hashing, JSON parsing, Git queries and the two expressly permitted checks were performed. Neither repository, worktree nor control files was edited. Only the requested REVIEW.md and review.json were written.
