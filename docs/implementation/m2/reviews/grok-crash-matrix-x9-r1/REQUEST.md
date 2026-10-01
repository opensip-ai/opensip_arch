Grok review: law X9 r1, the crash, lock and revocation matrix (the unit that gates M2 completion). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r1. This is a law review: run no product cargo. The lead keeps the native lane. Product HEAD is main f1b8321 (X3d-0 integrated).

Subject: docs/implementation/m2/crash-matrix-x9/PROPOSAL.md r1 (sha256 and bytes are pinned in hashes.txt). Context:
- `EXIT-PLAN.md`: the X9 row, "Choices left open by the design" (crash injection) and the release gates;
- the build plan (`docs/v2/architecture/implementation-boundaries-and-build-plan.md`): line 886 (M2), the failure matrix F00–F53 (lines 524–587), the required checks (lines 591–613), and the tooling row at line 1072;
- the accepted laws X2 r8, X3a r5, X3b r10, X3c r7, X3d r6, X4 r7, X4T r9 (item 7's whole-file `state.v1` restore limit), X6 r2 and X7 r3;
- in product f1b8321:
  - the `cfg(test)` hooks in `security/src/journal_store/carrier_append.rs` (`AppendStep`, `Fault`, lines 273–366) and `storage/src/ledger_store/project_commit.rs` (`ObjectStep`, `simulate_crash`, `with_commit_hook`);
  - the platform primitives in `platform/src/filesystem.rs` (`PublicationOps` lines 945–1033, `replace_with`, `publish_new_regular`) and `platform/src/locks.rs`;
  - `carrier_floor.rs` `publish_private_file`;
  - the re-exec precedent at `security/src/journal_store.rs` line 1289;
  - the Cargo manifests (no features exist) and `tools/check_package_edges.py`.

## Decide

- **The structural premise.** `cfg(test)` is set only for the crate under test, so neither `crates/storage/tests/commit_tests.rs` nor another crate's tests can reach security's `cfg(test)` fixtures (X4T-0, the injected InitialCore image, the synthetic profiles). Is that right, and does it force a feature-gated surface?
- **Items 1 and 2: the mechanism.**
  - Is this the right choice: a `crash-matrix` Cargo feature, named points through `crash_barrier!` and `crash_scope!`, and a re-executed test binary held at the point and killed by the parent? The rejected options are `cfg(test)` only, a harness binary, `fork`, a debugger and an SQLite VFS.
  - Do the four guards keep every point out of every release build? They are: `compile_error` without `debug_assertions`; no manifest edge, with `required-features` on the two test targets only; an unchanged edge checker; and release-absence evidence.
- **Item 3: the protocol.**
  - Does the `held` record, followed by a blocking stdin read and a parent `SIGKILL` checked by the signal status and the trace, prove the child died exactly at the point?
  - Is the protocol free of sleep-and-hope? The only timed wait is a watchdog that can only record `HARNESS-ERROR`.
- **Item 4: point kinds.** Are the injected stand-ins (`fail-before`, `fail-after`, `torn`, `inject-id`) faithful to the existing `cfg(test)` `Fault::Fail` semantics, and honestly labelled?
- **Item 5: the census-derived kill set and the scope table.** Who places points: X9-1 for integrated units, and each later unit for its own.
- **Item 6: the synthetic support surface.** It produces inputs on disk only, with no authority type, and with a pinned list of `cfg(any(test, feature))` sites. Is it a production seam under any accepted law?
- **Items 7 and 8: the evidence.**
  - The run record, the raw and logical post-state, and the normalized digest.
  - The R1 to R4 recovery ladder.
  - Where the evidence lives, and the checker.
  - Your own rerun as the determinism check.
- **Item 9: the matrix.** Check every row against its build-plan row and its owning law: the unit, the status (exec, inj, mut, elsewhere or LIMIT) and the expected values. In particular check:
  - F43 (argued not to be a lawful process race under X6's ledger-first order);
  - F44 and F45 (built on F39's end-path `REV`, because a later writer's floor step would raise the floor);
  - C5 (the sweep's admission under a revoked view, left open as G5).
- **Item 10: the limits L1–L10.** L4 records X4T r9's limit without asserting either refusal or admission. Is any limit actually executable here, or any executed row actually a limit?
- **Item 11: F30 and live revocation.** The deterministic holds, the gated observer tick, and the 2 s timing guard.
- **Item 12: the units X9-0 to X9-6 and their dependencies.** These include X3d-1/2, X4a, X2e, X5a, X6a/b/c, X7a/b and VD1.
- **Cross-law corrections G1–G6.** Are they real? G1 in particular: X3d r6 item 12, X6 r2 item 11 and X7 r3 item 10 rely on another crate's `cfg(test)` fixtures.
- Is anything else wrong or missing?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" (an array; empty on ACCEPT) and "subjectSha256" (the sha256 of the subject as pinned in hashes.txt). Write REVIEW.md and review.json. Do not commit.
