# C1a1 r2 review

**Verdict: REQUIRED-FINDINGS.** One remaining allocation-accounting finding and one non-blocking evidence observation.

## Verified subject and boundaries

Manifest `docs/implementation/m3/snapshot-plan-c/c1a1-r2-subject.json`: 18,305 bytes, SHA-256 `ac8c281a1b826e175cf39d8312f4cc9abd83922bdd2706f7fb4e4259af5fe760`, 77 members. Every member was rehashed successfully. All seven product-map rows match candidate/archive bytes; existing-file parents match Git base. The candidate is detached at `808ad6476fb848f84e732ee233a47229370081f4` and has only the seven declared changed/new paths.

Product main is clean at `e4e715845d2d0579060709898892d3d5fd93e49e`. Its delta from the candidate base is exactly the three D1a platform paths named in the request, disjoint from this candidate. The recorded lane comparison is against 808ad64; this review does not treat it as an integrated-main verification. Identical-byte integration and fresh verify_design remain later work.

Applied accepted C1a plan r4 as amended by r6 and M3-C r8 items 1–2. Only the two permitted checks were executed in the candidate: snapshot_ledger_model.py --check passes and operability source passes with zero findings, 114 rows. No Cargo, rustc, build, lane, network, delegation, other-pane access, private fixture, installation, keys, held trees, T2 store or T2-cache access occurred. T2 and runtime results below are archived evidence only.

## Required finding

### C1A1-R2-RF-1 (P2): The pre-walk path validator still allocates before any charge

`crates/security/src/snapshot_source.rs:400,472-474; crates/identity/src/descriptors.rs:31-61; SCOPE.md allocation audit`

SnapshotRoot::open calls LogicalPath::parse(path).is_err() before charging work. On every valid path, that parser constructs LogicalPath(String::from(value)); is_err then discards the allocated string. The later owned(path.len()) charge covers the distinct final SourceFile path copy, after custody and opens have already happened. It cannot cover both copies or retroactively charge the validator before allocation. This is a successful-path allocation omitted from the supposedly complete independent audit, including for a root-level file. The 35-case soundness test exercises walk_snapshot, not this opener, so it cannot expose the omission. C1A1-R1-RF-4 is therefore not fully resolved.

**Required:** Account for the validator allocation before invoking the allocating parser, or retain/reuse its owned validated path as the eventual SourceFile path with the charge made first. Preserve the existing shared grammar and do not copy validation rules. Update the allocation audit, source pins/generated vectors as needed, and add a focused pre-walk accounting control covering root-level and nested valid paths. The full read/custody model may still remain with C1a2 as planned.

## Round-1 findings and observations

- **RF-1 resolved.** ListingConversion still validates every name. Before any child observation, enter classifies each .opensip name using the shared rule and removes the exact custody-state anchor. The observation slots and subsequent observations cover only remaining paths. Root and admitted-member anchors are consequently neither stat-ed, opened nor listed by the walk; ordinary nested .opensip remains source. The observation hook removes the root anchor after listing and changes the member anchor to a file; neither enters the observation log, while a/.opensip does. The anchor-observed mutant fails.
- **RF-2 resolved.** The non-marker boundary check now precedes entry-kind dispatch, after shared pruning and ignorePaths, so an admitted boundary excludes a replacement regular file, link or FIFO as well as a directory. The native control also covers directory-custody and depth rows. Marker custody still excludes only its matching marker. The Python model now reproduces shared at_or_below, including its root-anchor behavior, and the repository/project/custody lookup precedence. The new borrowed boundary_anchor preserves existing boundary_hit results.
- **RF-3 resolved.** Both the walk and opener call judge_root before traversal/observation. It samples the retained descriptor and applies the existing metadata-first, ACL-aware S3 directory judgment, with the directory-only waiver. Root-level and nested captures refuse Custody at the root after 0777 mode or the injected unauthorized write ACL; restoration is also checked. The root-judgment mutant fails.
- **RF-4 substantially corrected but still open as above.** Paths/observations move from frames; parent/name views and opener component iteration borrow; ignorePaths borrows; the root spelling is deferred to a terminal name refusal; each frame including the root is charged. Boundary lookup now borrows cached rule-form rows rather than copying them on each call. The revised classifier charge covers a segment list, each target-prefix string, up to three anchors, and each nonempty member-root segment list. Its anchored model reproduces those terms. These are independent source-level justifications for the charged walk operations, but the audit is incomplete for the allocating pre-walk validator.
- **NBO-1 disposition remains acceptable.** C1A-T2/T3 stay explicitly owed by C1a2: same-tree durable/released-read inventory comparison and the released-read no-lease/no-fence control with its scenario helper before production use. Current test roots do not discharge them.
- **NBO-2 equality correction is implemented.** The model marks exact only when filesystem-premise costs dominate the bounded ACL-entry branch and no captured object has supplied ACL entries. All 35 vectors are marked exact; the native test asserts both the componentwise upper bound and equality on these cases. This is a finite regression control, not a proof that every possible undercount fails. The six regenerated model mutants supply evidence for their own omitted terms. The remaining log discrepancy is NBO-1 below.
- **NBO-3 metadata is principally corrected.** The accepted plan status, public API addition and parallel security command are described correctly. Attempt 1 has two failed check rows (suite comparison and focused tests), both arising from the one long-path materialization failure; attempt 2 is the completed lane of record.

## Other requested assessments

Passing the same WorkScope to the visitor is consistent with item 2: C1a2 can charge each read/retention step to the invocation's existing ledger without recreating it. Current visitors charge nothing; this model remains walk-only, and C1a2 must extend it for reader, retention and custody costs. The same-parent observations/opens and identity comparisons, lawful root lendings, crate-internal released-read constructor, marker policy and no-retry behavior remain intact. The non-test security modules open/observe but do not read source content; the test visitors are separate.

The discovery accounting issue is an acknowledged, separate closure-changing obligation. Reading classify_path confirms additional anchor/member-list allocations beyond discovery_walk.rs's old pricing form. This candidate uses its own corrected form and leaves the pinned discovery files untouched. Unchanged pins mean the blind receipt remains bound to its inputs; they do not resolve the separately routed discovery undercharge. No snapshot profile, production caller, cap acceptance, law-r9 decision or completed-snapshot claim is supplied by this preparatory unit.

## Lane and rules

- Attempt 2 has identical sets of 14 security failures at base and candidate, with no differing failures. Across two suites, passes increase from 1,167 to 1,182: 15 new passes. Each lib suite retains seven ignored tests. This is an equal-failure-set lane, not an all-green security suite.
- The focused snapshot suite passes all 15 tests. Its oracle still asserts 28 exact automatic reference cases and zero custody refusals. The model check passes on 35 cases, all marked exact.
- All eleven walk mutation logs contain real failed tests without compilation failures. All six model mutants regenerate and fail the native soundness/equality control. controls.json reports all seventeen caught.
- Warning-denied all-targets Clippy passes. New Rust files and discovery_export.rs are rustfmt-clean; existing lib.rs is dirty at base and candidate and excluded under the recorded policy. Supplementary FW-01 (8 tests) and environment exceptions (10 tests) pass.
- Archived model check, T2 census --check, operability, closure-unchanged and verify_design pass. verify_design selects inventory v212 and 173 contract successors. Independently rehashed all 19 census-closure files and compared them with candidate Git base; all match. The census tool itself is unchanged.
- The new Rust and changed boundary surface contain no actual prohibited from/into/pid/line/issue call. No new non-test environment read or Linux claim was identified. No census-closure file changed.
- Five new inventory paths remain: crates/security/src/snapshot_source.rs, snapshot_walk.rs, snapshot_walk_tests.rs, snapshot_ledger_vectors.json, and tools/security/snapshot_ledger_model.py. Existing discovery_export.rs and security lib.rs retain their inventory rows.

## Non-blocking observation

### C1A1-R2-NBO-1: The recorded soundness log does not expose the claimed triples

The test now correctly asserts equality for each exact case and emits the triples with eprintln!, but the runner invokes the successful test without --nocapture or --show-output. The pinned snapshot-walk-tests.log contains the 15 passing test rows and no soundness triples or summary. Thus the equality assertions are supported by the passing test, while SCOPE.md's claim of 35 soundness lines in that log is inaccurate. In the next lane capture successful-test output, or narrow that evidence statement. This is a reporting observation, not a defect in the new equality assertions.
