# B1-B-r3 review

Verdict: **REQUIRED-FINDINGS**

One required finding remains in the environment exception checker. Round-2 RF-02 is resolved. The custody fixes, optional-parent fixes, base compatibility evidence and format classification remain valid. No non-blocking observations.

Verified the 12,046-byte subject manifest, SHA-256 `4d4b0bc303525ec2734b2f2ff09a098c0e95207cb4eedfbdfb35e89ce49394f5`, and all 53 members. All 27 product-map files match their candidate worktree and archived bytes. Parent pins match product base `c0151bc6b7fdb6db9157124fa068c8be5061f5d4`, and new paths are absent there. The map equals the complete changed/untracked path set. Source authorities match architecture base `b98932720200253f671814d9cb728ba0615c1085`. Product and candidate HEADs match the product base; the main product is clean. The lock is byte-identical to base: inventory 188 and 162 contract successors remain unchanged.

## Required finding

**B1B-R3-RF-01: Apply production-include confinement to integration-test files too**

Severity: medium. Location: tools/tests/test_environment_exceptions.py:123-136,169. Prior finding: B1B-R2-RF-01 / B1B-R1-RF-03.

The revised include analysis rejects mixed test/production inclusions of src files such as installation_routing_tests.rs, but exempts every path containing /tests/ before examining its incoming edges. whole_test initializes these files to True and the fixed-point loop skips them forever. Thus a production include edge to crates/host/tests/admission_tests.rs leaves rustc_path (RUSTC), nested_cargo (CARGO) and the X8 helpers classified test-only, even while their existing item-level Clippy allowances remain. Their call and allowance sets do not change, so the pin cannot reject this production reachability. This contradicts the stated rule that one production-reachable inclusion makes a file production. The new negative control exercises a src/custody target, not this still-exempt target class.

Required correction: Treat integration-test entry-point status as a test root, not an unconditional exemption from production reachability. Reject production-reachable include edges into those files and propagate that status through their includes; retain ordinary test-target classification when no production inclusion exists. Add a negative control introducing a real production include of an allowed tests/ file while preserving its integration-test role, and require the existing exception pin to reject it. Keep the successful src-file mixed-include and comment/literal controls.

Evidence:

- whole_test = {rel: '/tests/' in rel for rel in codes}
- if whole_test[rel]: continue prevents checking incoming production edges for these targets
- test_only[key] uses whole_file_test unconditionally
- The accepted r5 list requires all non-Git exceptions to remain test-only, including the host integration-test helpers

The current candidate does not itself add a production inclusion of those integration tests. This is a defect in the required structural guard: it cannot establish continued test confinement for the entire enumerated list. The current call-site list is exact, hence environmentListExactPerR5 is true, while r2Rf01IncludeConfinementExact is false. r1FindingsStayResolved is false only because the original RF-03 structural-check requirement remains partly unresolved.

## Round-2 resolutions

RF-01 is substantially improved: real literal-path include edges are extracted from blanked code, comment/literal text creates no edge, and all incoming edges participate in the fixed-point analysis for non-tests/ files. The new src-file mixed-inclusion control passes. Constant values and attached allowances remain pinned. The required finding identifies the remaining unconditional tests/ exemption.

RF-02 is resolved. LOCAL_LOOKUPS is test-only and thread-local, incremented at local_directory, the current entry to local capture/recheck. The control resets it, runs both admission phases, asserts zero in CI and two interactively. The new mutation explicitly calls and ignores local_directory in CI and is caught by the archived failing test.

The host composition test now invokes the real resolver and X12 pack admission on bytes captured by security's writer-gate first phase. A refused project-layer other.pack:1 prevents the second phase; a bundled-pack case admits it. The scenario result checks a byte-identical registry, unchanged installation/project member sets and sizes, and a new writer opening after release. This establishes no RESERVED row, new lease, journal or marker for the refusal. The composition seam is inside the existing doc-hidden scenario-fixtures module and dev-dependency feature path. It adds test-seam exports, not an ordinary production public API or CLI caller.

## Whole-unit assessment

The prior custody repairs are retained byte-for-byte in the relevant capture and optional-parent logic. Selection and local judgment retain their successful sample; the 4 MiB charged read requires equality to it before and after capture. Descriptor retention prevents name-based redirection of the byte read. Captured samples and explicit project/local absence observations join the held-fence recheck. CI's non-interactive branch never invokes local capture.

Optional global capture shares the judged private walk and settlement with required capture. Existing parents receive private custody, exact-name and filesystem admission; their original samples and the absent component are rechecked. Wrong-custody, changed, replaced and detached parents refuse. No global file or directory is created.

The carrier/registry split retains the required order, and legacy admission remains non-capturing with unchanged reads, charges, refusals, rechecks and latching. The archived base/candidate core-admission probe has five equal charge/classification states; the legacy session/gate wrapper bodies retain their original behavior. J1 production composition remains deferred.

InvocationModeV1 remains unified with invocation.rs. Its rule is the conjunction of stdin/stderr terminal observations; the observation uses IsTerminal, reads no environment and has no production caller. The single added operability stdio row is correctly owned by output and terminal.

The two crate-local Clippy configurations target the four prohibited methods. The current 13 item-level allowances cover exactly r5's 17 existing sites and actual variable names, with current non-Git reads confined to test code. LD-B1B-4's crate split now compares complete stable resolver/provenance output under cleared/hostile environments, alongside capture facts; the allowed Git refusal is separately asserted. LD-B1B-5 soundly leaves the unused child-marker allowance unused. New refusal variants map to existing public codes. No discovery, member carriers, production wiring, inventory successor, qualification or project completion is claimed.

## Checks and evidence

Independently ran exactly the permitted offline checks:

- `python3 -I -B tools/tests/test_environment_exceptions.py`: nine tests passed, including constant, moved-helper, src-file mixed-inclusion and comment/literal controls.
- `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip-b1b`: passed, no findings, 114 rows.

All nine archived mutation/planted logs match controls.json: seven mutations have the named failing tests, and both planted production reads trigger disallowed_methods with compilation failure. The new ignored-local-lookup mutation is among those caught. The five legacy probe lines match both raw archived probe logs and one another.

The submitted full-suite comparison records equal failure-name sets and suite counts: security retains 14 failures, with passes increasing from 1,046 to 1,062; host retains eight failures, with passes increasing from 330 to 336. Full-suite raw transcripts are not subject members, so these results are supported by the submitted comparison and runner rather than an independent replay or raw-suite reconstruction. Archived evidence supports warning-denied all-targets Clippy, tools checks, the 114-row census and design verification selecting inventory 188/contracts 162. All 23 mapped Rust files are format-classified; all 13 new/base-clean files are checked and the remaining ten have declared base-dirty exclusions. The fresh pinned checks-r5 evidence is used; historical wording and failed earlier attempts are not acceptance evidence.

No Cargo, rustc, builds, other tests, lane or network was run by this review. No private fixture, installation directory, signing keys, held trees, other panes or delegation were used. Neither repository, the candidate worktree, stage, control files nor prior reviews was edited. Persistent review writes are limited to this directory's REVIEW.md and review.json; the permitted checker creates and cleans its own temporary copies.
