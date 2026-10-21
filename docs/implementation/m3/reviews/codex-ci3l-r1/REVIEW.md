# CI-3L r1 review

**Verdict: ACCEPT-UNIT.** No required findings or non-blocking observations.

## Subject and provenance

Verified the 50,317-byte subject manifest at SHA-256 `94d1ce759253f65d182aadb4ca7a49a379490ca3e35040cb253c46e81853cf97` and independently rehashed all 207 declared members. The stage contains exactly those members plus the manifest. All 14 architecture-authority pins match architecture base `5e0ee62da9fe4078bfb99c163b40d5cdbdedb802`, all seven product-authority pins match product base `f2be09731e015ec30002addd8bda6227fa07b71e`, and the 711,307-byte product lock matches its declared digest.

The product map has exactly seven existing paths. Each parent matches the product base, and each frozen candidate matches its archive: lifecycle installation, installation tests, retained tree and retained-tree tests; platform component tree and its tests; and the operability exceptions file. The base-to-candidate diff has no other path. There is no new path, dependency or production caller. The protected drafts remain unchanged.

## Implementation assessment

The implementation satisfies CI-A3 r4's accepted a–f duties on the reviewed bytes. `ComponentStore` retains and charges its admitted absolute store path once. Installed trees retain the generation/tree handles, authenticated tree structure, pin and selected entrypoint. Launch resolution uses only retained rows and handles, charges the kind check before lookup, permits at most `S+1` lookups and `S` link strings, refuses the last permitted link before another hop allocation, and reports joined-length overflow as `Budget(Arithmetic)`.

Regular files are reopened no-follow through the retained parent and checked for mode, length, digest and identity. Directories descend through retained handles and bind their final identity without reading content. The final lexical path is formed once in a charged NUL buffer; a no-follow status observation binds kind, device and inode before the allocation-free `Vec`-to-`PathBuf` conversion. The launch record is charged before construction. Platform status and directory-identity helpers reject unsupported hosts before charge, charge before exactly one native observation, retain errno immediately and do not retry or fall back. Missing/non-directory paths, other I/O, binding failures and budget failures remain distinct.

Every launch failure is latched. Later launch or transfer calls return the latched class before further charge or observation, with budget failures projecting to Closed as specified. `LaunchMember` owns the path and binding data while its lifetime remains tied to the retained tree. The controls cover root, nested, link, empty, large and directory cases; wrong kinds, misses, excessive and cyclic links; mode, size, digest, type, absence and identity changes; source-path replacement; final symlinks; directory identity; one-unit-short stops at every charge; overflow; transfer/launch latching; and pin retention through an actually spawned member until capability drop. The documented same-principal residual window remains a qualification boundary rather than a claim closed by this unit.

The CI-T28 reference oracle computes status, regular-open, descent, search and resolution prices independently of production cost helpers. Its cyclic case requires the exact repeated lookup trace and charges, and its final-hop model refuses before constructing another temporary. The overflow control checks both the arithmetic class and subsequent latch.

The operability exceptions file preserves every ordinary field and prior mint row by value and adds exactly two sorted funded lexical-conversion rows: `OsString::from_vec` in lifecycle `installation.rs` and `retained_tree.rs`. Those are the two reviewed, charged `PathBuf` constructions. They confer no identity or provenance mint authority.

## Frozen validation evidence

The final native ABI evidence uses the frozen four-line C probe containing `sizeof(struct stat)` and records measured and reference sizes of 144 with equality true. This closes source-preflight observation NBO-1 on the final source.

The corrected owning lane records all 27 checks passing, including exact base comparisons, scoped formatting, warning-denied Clippy, workspace and feature checks, release/fixture symbol controls, the lifetime doctest, package edges, environment and operability checks, unchanged census closure and receipt inputs, and design verification. Lifecycle rises from 81 to 97 library tests with zero failures. Platform rises from 292 to 295 library tests with zero failures and retains its one separately explained reporter ignore. The accepted SECURITY-BASELINE-r1 and bound inventory v233 precede this lane; both fresh security base and candidate runs record 1,291 passed, zero failed and the same seven unwaived ignored controls, plus six passing documentation tests. The earlier 14 failures are therefore repaired by the accepted baseline rather than waived or replaced with superseded-r1 evidence.

All 24 final mutation records were checked against their frozen patches, build artifacts and runtime logs. Every patch changes exactly its reported source file, every relevant executable compiler artifact has `fresh:false`, all 24 binary digests are distinct, every run exits 101 with a failing test set exactly matching the report, and none relies only on compilation failure. The set includes the three independent price undercharges, reference last-hop regression and overflow-class regression in addition to the original behavior and charge-order mutations. After restoration, the exact focused lifecycle and platform suites pass 16/16 and 15/15. The report and the complete-lane control record are byte-identical. This closes source-preflight observation NBO-2.

## Scope and carried obligations

Acceptance is limited to this CI-3L code unit and these exact bytes. It does not accept D4 or CI4 composition, a production caller, platform qualification or project qualification. D4-4 still owns production composition and pin lifetime through settlement; CI4 owns command, termination and profile behavior. The separate Linux, private-data, T2, clock and other qualification lanes remain open.

After exact accepted integration, the CI description successor is required under `CI2INV230-R1-NBO-1`; it must describe allocation-free retained names, paths and link targets while preserving the allowance for allocated error carriers. This acceptance does not itself bind that successor.

Review used only read-only file reading, hashing, JSON parsing, Git queries and source inspection. No build, test, Cargo command, lane, network access, other pane, private fixture/data access or delegation was used. Neither repository, any worktree, the frozen stage, controls nor evidence was edited. Only `REVIEW.md` and `review.json` were written in the requested directory.
