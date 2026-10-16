# B2-C1-r1 review

Verdict: **REQUIRED-FINDINGS**

Three required findings block acceptance. One non-blocking metadata observation.

## Subject and verification

Rehashed the 9526-byte subject manifest, SHA-256 `7f3f7b8db7d3e027b7c3609905ce0061839727d041141fbe18c3d4dc0fee8613`, and all 43 members; every size and digest matches. Confirmed clean product main `b0154f08f9193bbf3ca368420c2dae2006c11661` and architecture HEAD `b6e42226f103642306e8c0cd1ac2ddc1b633587a`. All source authority and product-lock pins match. The ten product-map paths exactly equal candidate changes; archived/candidate/parent pins agree.

Independently ran only the permitted commands in the candidate worktree: source check (114 rows, passed, no findings), FW-01 (7 tests passed) and discovery-unit-vectors --check (verified). Read the Rust implementation, security export, scenario admission, generator/tests and recorded evidence. Additional inputs were evaluated only through the expressly permitted bound Python reference; candidate mismatches below are established by source inspection, not an unauthorized Rust run.

## Required findings

### B2C1-R1-RF-1 — Production can omit the boundary inventory

`crates/host/src/discovery.rs:343` exposes a production `pub(crate)` function taking `Option<&AdmittedBoundaries>`. Passing None succeeds through the standalone lane. Membership and scope likewise accept None in production. No operational require_admitted_boundaries entry or test-only standalone gate exists.

The opaque security type correctly prevents construction of a forged Some value outside security, but cannot prevent passing None. The selected NE U-8 and plan r2 require that authoritative composition structurally require the inventory; future J1 composition must not rely on a convention to remember it. SCOPE.md's claim that the type system forces this is therefore incorrect, and the named missing-inventory internal refusal has no implementation.

Provide production entry points requiring a boundary reference, or an operational checked wrapper that refuses missing input with the selected internal key. Restrict optional standalone functions to the existing test/scenario seam. Verify that production composition cannot bypass the check. The JSON unforgeability field remains true for actual boundary values; it does not mean absence is prevented.

### B2C1-R1-RF-2 — Unicode bounds differ from the selected schemas

`canonical_relative_dir` at line 304 uses `path.len() <= 4096`; scope text checks similarly use `t.len()`. These count UTF-8 bytes, while the selected reference's schema maxLength counts Unicode characters. Scenario V3 admission repeats this mismatch.

Synthetic reference probe: take a valid discovered tsjs unit and replace its root with 2049 NFC `é` characters, updating markerPath accordingly. The root has 2049 characters and 4098 bytes. Bound-reference root admission, membership of its a.js and scope construction all succeed. The candidate rejects the root at the byte-length guard. With an ordinary short-root unit, using that same string as an exclusion prefix also succeeds in reference scope construction and is rejected by the candidate's scope text guard. Every recorded vector is ASCII.

Match the selected character bounds in all new schema-equivalent guards, including member roots, scope strings and scenario admission. Add multibyte positive/negative vectors around the published bounds. A new byte limit would require separate authority; it is not exact reproduction.

### B2C1-R1-RF-3 — Generated default requests are not vocabulary-closed

`default_capability_selection` at line 1103 only admits the release registry, then derives requests by treating any pair absent from not_selected as selected. It does not reject an unknown unit mode. The unit field is a String, so this input is representable.

Synthetic reference probe: copy a normal discovered unit, set languageMode to unknown-mode and pass an empty registry. The bound reference refuses `native.requested-capability-mode-unregistered:calls:unknown-mode`. Candidate source instead emits every matrix capability for that unknown mode, then returns success after its ownership and cardinality checks.

Validate the generated rows or source modes against the selected matrix before returning the default analysisSpec, with the reference's refusal. Add this negative vector. Full admission of externally supplied specs can remain deferred; that decision does not justify omitting the constraints required to keep internally generated defaults closed.

## Positive findings and evidence limits

The security export is a thin mirror calling the shared rule, with private fields and a crate-private constructor for AdmittedBoundaries. Record admission is in the existing feature-gated scenario seam. The shared rule and custody.rs bytes remain unchanged; every file pin in the recorded census cost closure still matches the candidate. No held-out store was accessed to establish this. The matrix copy is byte-identical to its architecture source. Alias pairs match the closed registry map, and unknown aliases refuse.

The implementation covers the recorded discovery branches: LD-B2C0-1, full custody/depth boundary handling, subset/member checks, explicit workspace folding, cap, modes, fallback and ordering. Scope ordering, digest construction and boundary disclosure follow the reference apart from RF-2. FW-01 covers both new production files. No production caller, environment read or law change is added.

Cargo workspace status as an input is faithful to the oracle; later composition can use identity's existing parser. UnitMembershipV1 has no membershipDigest field in the reference; deferring its binding to the Plan stage avoids inventing a field. These scope decisions are reasonable. Inventory v201 remains owed for six new paths.

Recorded security suites have identical 14-failure sets and 1128 passes at base/candidate. Recorded host suites have identical 8-failure sets, with passes increasing from 343 to 347. The focused four discovery tests pass in the recorded log. Clippy's recorded command covers host/security with --all-targets and -D warnings, and finishes successfully. All eight mutation logs contain actual failing tests rather than compilation errors. These are inspected recorded results, not reviewer reruns. They do not cover the three findings above.

Non-blocking **B2C1-R1-NBO-1:** source.json says contractSuccessorsUnchanged=164 despite the pinned 166-contract base, and publicApiAdded=false despite introducing the explicit public Rust discovery_export surface. Correct these descriptive fields without implying a user-facing production caller.

## Boundaries

Wrote only REVIEW.md and review.json in the requested directory. Neither repository, worktree, stage nor control files were edited. No Cargo, rustc, builds, lane, network, other panes or delegation were used. Execution was limited to the expressly permitted Python checks and bound-reference synthetic probes. No private fixture, installation directory, signing keys, held trees or T2 held-out entry was accessed. No qualification or plan completion is granted.
