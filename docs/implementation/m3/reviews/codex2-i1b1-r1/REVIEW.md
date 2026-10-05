CODEX2 review: I1-b1 r1

**ACCEPT-UNIT.** No required findings and no new non-blocking observations.

Reviewed the exact 16,054-byte diff against `0765f8cd0c778e15adf713bd9607fd198230bfa6` in `/Users/sb/code/opensip-ai/opensip-i1b1`, sha256:

`4371f9dfa2aba740747ac5ea887fa95b0ec53acac2305196f9f920725d13e822`

All 28 input pins, the two changed-file before/after pins, and the unchanged final diff match. The authority is M3-I1 r3 `PROPOSAL-r3.md` (`204f8ee834da5340ddcfe315a70da29a05a57b6109941d44d9dd60f0494dd86c`), item 2.2, UNITS-r2's I1-b1 row, I1-L §4a, and X12 r3's admission/row-4 law.

The diff implements the op law exactly for `cycle-representative`: whole rule emitWhen, imports at resolved-target, filters exactly [], literal absence of endpoint and evidence, and policy subjectKind file. The policy walk passes depth==1; the program walk marks only the whole emitWhen as root and makes every boolean operand non-root. A violation returns POLICY.UNKNOWN_RULE before the evidence-use join and becomes the existing bundled HostInvariant/PackDefect::RuleLaw row. The shared registry relation, ladder, endpoint, plane and filter checks still run. Only this op skips the source-kind membership check; every other op retains its old path.

| Judgment call | Answer |
|---|---|
| 1 — Kind in the program pass | **Yes.** RuleProgramV2 carries no subjectEnumeration. The policy pass checks file kind first. admit_from and compile_plan_policy compile from that policy; inspect_policy_program requires its exact compilation digest before checking the laws. Accept None for the program kind while enforcing all its carried conjuncts. This meets the joined both-passes requirement. |
| 2 — Shared law | **Accept.** Require the op law first, then the shared law, replacing only the source-kind check for this op. |
| 3 — Explicit endpoint source | **Yes, it is a violation.** Absent is literal. The schema's default source does not permit an explicit member prohibited by item 2.2. |
| 4 — Evidence | **Accept.** Declared and undeclared evidence both give UNKNOWN_RULE before evidence-use joining. |
| 5 — Root bit and direct program tests | **Yes.** Carry root at the two traversal callers. Direct check_program_laws tests isolate the private program pass, whose violations public owners otherwise reject in the policy pass or compilation join. They do not assert public acceptance of divergent programs. |
| 6 — Synthetic pack | **Accept.** A one-row cfg(test) pack meets this unit's test requirement; its emitWhen equals I1-P's document. Shipping the full document, release row and self-checks remains I1-c's. |
| 7 — Inventory | **Accept.** Only two existing evaluator files change, with their descriptions still true. No inventory, contract successor, or contract review file is needed. |

The first test admits the file-subject test pack through real bundled admission and checks identity, policy/program digests and determinism. Its exists controls retain file refusal and symbol acceptance at root and under not. The second test covers 17 schema-admissible violations with exact row-4 RuleLaw UNKNOWN_RULE assertions: boolean nesting, wrong registered relations/rungs, lower imports rung, two nonempty filters, both explicit endpoints, evidence declared and undeclared, and all three non-file kinds. The n control remains a Schema refusal. The third isolates 13 emitWhen violations in the program pass and checks lawful file and rejected symbol policy/program pairs. The fourth verifies each conjunct independently with Some(file) and None. No schema-admissible conjunct is missing; missing required fields and null optional members remain schema failures.

The pinned mutation evidence is sufficient: unmutated control passes; all 12 semantic mutants compile and fail the expected controls. Standalone checks are necessary because today's registry independently masks removal of relation and evidence conjuncts; M2 and M6 are killed there. M11 and M12 separately detect incorrect root propagation in policy and program. The historical base failure with the first three tests and the base compile failure after the helper test are distinct, as disclosed. I inspected and checked this evidence against the pinned source; I did not run mutations or edit the worktree.

Every earlier pack test body and expectation is byte-identical. The release source pin still has seven include_bytes sites, one PackRegistry construction, two RELEASE_PACKS selections and no forbidden runtime/test references. Evaluation still returns structural ATOM_OP until I1-b2. No I1-b2 semantics or I1-c row/document is added, and no manifest, lock, feature, schema, generated source, registry, fixture, crash point, or design selection changes. No crash-matrix lead run set is needed or was run.

I agree that **I1A-NB-1 is outside I1-b1**, with the Lead's routing. Admission does not use scanner reference metadata; the consumer search finds only the registry metadata itself. This unit does not maintain it, no law selects a replacement locator, and the unchanged bytes equal I1-a's accepted materialization. Carry it to the next unit that edits atom-registry.json for its own reasons, or a record-maintenance follow-up. It remains a historical locator and must not be cited as current fixture-byte verification.

I independently reran all requested lanes, including two workspace runs:

| Lane | Result |
|---|---|
| Workspace fmt | PASS |
| Explicit rustfmt of the path test module | PASS |
| Workspace all-targets build | PASS |
| Workspace clippy | PASS |
| Crash-matrix clippy | PASS |
| Scenario-fixtures clippy | PASS |
| Workspace all-targets tests, run 1 | 1742 passed, 0 failed, 3 ignored |
| Workspace all-targets tests, run 2 | 1742 passed, 0 failed, 3 ignored |
| Workspace doc tests | 20 passed, 0 failed, 0 ignored |
| Crash-matrix feature tests, no lead set | 1636 passed, 0 failed, 3 ignored |
| Generator drift | PASS: 40 sources, 8 outputs, changed: [] |
| Plain design verification | PASS |
| Host package edges against v136 | PASS |
| Rust-provider package edges against v136 | PASS |
| Package-edge tests | 14 tests, OK |
| Dependency policy | PASS |
| Identity dependency policy | PASS |
| Dependency-policy tests | 9 tests, OK |
| Identity dependency tests | 5 tests, OK |

All four new tests and the unchanged release source pin pass in both workspace runs. Metadata outputs, copied checksum-verified dependency archives, generator outputs and logs are under this review directory. Product cargo lanes used locked/offline mode and the review-local target/cache, with private 0700 Darwin TMPDIR and a synthetic HOME. The requested Python suites resolve changed disposable fixture manifests with offline-only metadata; checks on unchanged lock graphs use locked/offline metadata. No offline-only resolver runs against the product worktree. Each cargo or cargo-invoking lane acquired the shared mkdir lock and released it immediately after completion, only when its mkdir had succeeded. The waiting process argv names only the Python script, containing no cargo text. The generator process check was clear before the drift lane, which also held the shared lock. All owned locks are released. The controller was continued after completed tests to ensure the package-edge suite's internal cargo metadata calls also hold the lock; completed native checks were preserved.

Acceptance covers the reviewed pre-integration bytes. The Lead reports main moved to b7b87b7 through changes outside evaluator and owns rebase/integration. I made no repository edit, commit, push or delegation and did not access the real OpenSIP home or the private 413 fixture. This is macOS arm64 development validation.

Evidence: [native-results.json](native-results.json), [source-audit.json](source-audit.json), [pin-audit.json](pin-audit.json), [lock-log.jsonl](lock-log.jsonl), and [drift/selection-result.json](drift/selection-result.json).
