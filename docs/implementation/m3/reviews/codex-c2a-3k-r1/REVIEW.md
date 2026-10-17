# C2A-3K-r1 review

**Verdict: ACCEPT-UNIT.** No required findings or non-blocking observations. Acceptance covers the pure internal retained-byte verification kernel and its controls. It confers no delivered-custody, component-admission or product-qualification standing.

## Subject verification

Independently verified the 9,340-byte manifest, SHA-256 `c3caf5fb8e818ff89b8f92aaead2813659b2e93f204fff030cbbea39ec2bd5f8`, and all 40 member lengths and SHA-256 values. All match.

The detached worktree is at the exact requested product base `d704ed4551d65da8be18faf69f4aeed26be369c2`. All three product-map parent blobs match that commit, and all three candidate files match their archived reviewed bytes:

- `crates/security/src/component_closure.rs`: 26,357 bytes, SHA-256 `e4d90cc20c320e5e837f68d233b0a8cde944a052b11bb9812c2e3e62f6abedbc`.
- `crates/security/src/component_closure_tests.rs`: 53,538 bytes, SHA-256 `9facc8e1b5d9565c5eefcdb2fc4b5f5829675a4a4d882e56f3db6f228aa79e35`.
- `crates/security/src/trust/trust_bootstrap_tests.rs`: 57,652 bytes, SHA-256 `acb1d4ed86ee85a1b8dcb891620c438f6deb71d28eec89f66cf784a0b317b138`.

Verified source.json's lock pin, five authority pins and two stacked-unit pins. The changed set is exactly the three existing paths; no new path and no lib.rs change. Git confirms the relevant earlier units' files are unchanged through the stated base. The v227 lock and 177-successor context are consistent with the package.

## Kernel correctness and authority

The signature matches C2a plan r4's C2a-3k row: candidate, borrowed map of retained byte slices, borrowed raw body and borrowed WorkScope, returning Result<(), ClosureFailure>. Retention has the closed Missing/Length/Digest causes and is carried through ClosureRefusal without relabelling corruption as absence or not-installed.

The presence walk is correct. Candidate Blobs are already sorted and unique in path-byte order; BTreeMap<&str, _> iteration has the same order. Each comparison is funded immediately before the byte comparison. A smaller retained key advances only the retained iterator; equality consumes that exact slice once; a greater key or exhausted iterator returns Missing. Consequently a later key, a path prefix, trailing slash/space, case variant, directory key or symlink key cannot substitute for a Blob. Neither map lookup with hidden key comparisons nor a new sort is introduced.

For each matching slice the length comparison precedes hashing. Wrong length returns Length without hashing that slice. Correct-length bytes are hashed and compared with the Blob's lowercase SHA-256 via the existing fixed stack hex array. Only after every Blob verifies does the kernel hash the supplied raw body and compare its binary digest with candidate.manifest_digest. The envelope is not a substitute for the raw body. Each first failure returns its actual typed cause; a failed charge remains the ledger's Budget failure.

The production diff adds no allocation, slice copy, file operation, custody handle, manifest parser, candidate constructor or admitted constructor. raw_sha256 and hex_digits are existing helpers; the latter returns a fixed array. The existing C2a-1 allocation pin still covers the extended production module and its five original allocation sites. Returning unit does not upgrade the ClosureCandidate or permit context/Plan/selection/worker use.

## Pricing and explicit rulings

**Q-C2A3K-1: accepted.** Passing over keys that are no candidate Blob's is correct for this kernel. Its contract establishes retention of the candidate's required regular-file bytes and manifest body. It does not admit the delivered directory's exact path set. Extra supplied slices, including those keyed by dir/symlink delivery rows, are never accepted in a required file's place, and their contents are not hashed. Delivery-law verification and C2a-3 remain responsible for rejecting extra delivered files; no unapproved Extra variant or successful component admission is introduced. A trailing extra need not be examined after all required Blobs have matched.

**Q-C2A3K-2: accepted.** The plan's explicit rule that each comparison and digest is charged first includes presence-key and digest-equality comparisons as well as the length checks listed in its summary. Each uses the existing COMPARISON_COST, one edge. Each hash uses the existing digest_cost(len), ceil(len/64)+1 edges, immediately before computation. The digest price's padding allowance is not reused as the equality charge. With an exact map, the successful cost is the sum over Blobs of three comparison edges plus digest_cost(slice length), then digest_cost(body length) plus one body comparison. Each extra key passed before a required Blob adds one comparison edge. Nothing allocates, so no new object or byte charge is justified.

The source has four charged comparison sites and two charged hash sites. The exact-price controls cover all roles and empty-file retention; every smaller positive edge allowance representable by the test ledger refuses within its allowance. The aggregate test uses the same ledger across two component verifications and exhausts partway through the second, without a reset. The source-order pin separately checks that charges precede work; exact-total tests alone would not establish that ordering. A zero-edge with_limits scope is not asserted by the loop starting at one, and is not needed to infer additional test coverage.

## Signed-chain and mutation controls

C2-T6's new kernel leg reuses the existing ordinary-reader helper for default and escapable synthetic trees of all five roles. The chain goes through the existing initial-core/acceptance setup, signed catalog and component association, ordinary metadata preparation and C2a-1 candidate production before entering this same kernel with the authenticated body and supplied tree slices. Flipping a supplied byte at unchanged length produces Retention(Digest). The two C2a-2 tests retain their previous paths and assertions, passing false to the new helper flag; the new flag adds kernel checks rather than a fixture-only admission path.

The eight module tests cover every-role success, missing/lookalike slices, short/long/empty-file length errors, changed bytes and wrong bodies, extras before/between/after Blobs, exact funding, aggregate exhaustion and source allocation/charge order. The original C2a-1 controls remain present. The new trust test supplies the ninth test. Existing public test-only signing infrastructure is reused; no new key, root, signing role, feature or key-file read is added.

Independently inspected the mutation definitions and all 13 log outcomes. Every mutation reaches failing tests rather than a compile error. They cover removed presence/end/later-Blob/length/tree-digest/body-digest checks, relabelled failures, an uncharged comparison, hash charged after computation, an underpriced hash, a copied slice and a retained iterator not advanced on equality. Source pins supply the decisive failures for the allocation and charge-order mutations, alongside the functional/accounting controls.

## Lane evidence and live check

The packaged results and underlying logs agree:

- Security: 1,248 to 1,257 passing tests, nine new passing names, the same 14 pre-existing failures on both sides.
- Host: 412 to 412 passing tests, no new passing names, the same eight pre-existing failures on both sides.
- Focused run: 32 passed, zero failed, including the explicitly selected existing ordinary-catalog test in addition to the unit groups.
- All three edited files are recorded base-clean and candidate-clean under rustfmt. The exact edited-set control passes.
- Recorded warning-denied all-targets security Clippy, workspace all-targets check, scenario-fixtures/crash-matrix checks and security release build finish successfully.
- Recorded environment-exception tests pass; census closure has 19 files with no changed-path intersection; verify_design reports passed with productQualification false and inventory v227.

These suite comparisons are not all-green full suites: the listed base failures remain. No isolated flaky adjustment was needed. The lane's private 0700 temporary directory, nice level and ownership are recorded evidence, not a lane I acquired or reran.

Ran only the expressly permitted live checker in the candidate: `python3 -I -B tools/check_operability.py source --repository .`. It returned passed, 114 rows and no findings. Its mint audit remains satisfied; the candidate changes no mint-audit or census-closure source. The production/test diff adds no environment read, let-underscore discard, new mint call, public API, production caller, constant/cap or feature. Existing source inclusion in the source-pin test is not a key read.

## Remaining boundary and inventory

No inventory successor is required for this unit's three existing paths. Their realization does not create AdmittedClosure::Component: C2a-3 still owes delivered custody, its production constructor and the applicable CI interface. C2a-4 still owes D4/J1 placement, profile and composition gates. Retention kernel success is neither custody evidence nor completion of successful context admission, end-to-end placement or product qualification.

Only REVIEW.md and review.json were written in the requested directory. Neither repository, worktree nor control file was edited. No Cargo, rustc, build, test or lane was run, and the lane lock was not taken. No network, prohibited private fixture/key/installation material, held trees, T2 store/cache, other pane or delegation was used.
