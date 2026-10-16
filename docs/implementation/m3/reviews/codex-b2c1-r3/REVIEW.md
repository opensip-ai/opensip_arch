# B2-C1-r3 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none. All earlier findings are resolved.

## Exact subject and scope

Rehashed the 10448-byte subject manifest, SHA-256 `7c43d5d56cdc65f423c267818287b67a9edcbfb603dcd6a59da29816e7880bf9`, and all 47 members; every size and digest matches. Confirmed clean product main `b0154f08f9193bbf3ca368420c2dae2006c11661` and architecture HEAD `b6e42226f103642306e8c0cd1ac2ddc1b633587a`. All source authority and product-lock pins match. All ten product-map paths match candidate/archive bytes and existing-parent pins; the candidate's changed/untracked paths equal that map exactly.

Reviewed r3 against the prior rounds and the bound reference. The semantic implementation remains the previously inspected instrument; this round removes the incomplete Python repr formatter and explicitly records a narrow internal diagnostic normalization.

## Prior findings and grammar-key decision

**Round-1 RF-1 remains resolved.** Production discovery, membership and scope entries require &AdmittedBoundaries; private implementations retain the optional form, and standalone wrappers are cfg(test)-only. The missing-inventory gate returns the selected internal key. The source control and recorded mutation enforce this separation. Private security fields and its crate-private constructor prevent production callers outside security from forging an admitted inventory; raw-record admission remains in the existing scenario seam.

**Round-1 RF-2 remains resolved.** Schema-equivalent root/scope/scenario bounds count characters. Vectors cover a 2049-character root occupying 4098 bytes, a 4096-character exclusion, and 4097-character root/member/prefix refusals. Length keys retain the reference's exact field, selector, count and bounds.

**Round-1 RF-3 remains resolved.** Generated default requests undergo the matrix capability/mode/NOT-SELECTED checks after cardinality admission. The unknown-mode vector preserves the reference refusal. The earlier source metadata observation is also corrected.

**Round-2 RF-1 resolved by the explicit reviewed lead decision.** Grammar faults now retain their internal class, field and selector, ending in `:grammar`. The vector generator applies the same transformation only to NATIVE_UNIT_ROOT_REPRESENTATION grammar faults; it leaves the `length=` form and unrelated keys untouched. It does not convert successes to failures, suppress failures, change public routing or alter records/digests.

This is a sound implementation-level diagnostic choice: the reference's Python repr spelling is not a public detail or identity input, while coupling the product diagnostic spelling to Python's Unicode printability tables would introduce an unnecessary runtime-version dependency. The normalization is declared in SCOPE.md and code, not hidden in the tests. The eight new unit/member grammar vectors exercise U+0085, U+2028, dot segments and trailing slashes; the new grammar-key mutation is caught.

The exact-reproduction assessment in review.json means exact canonical records and selected refusals under this explicitly accepted grammar-key normalization. It does not assert that raw Python repr diagnostic strings are retained.

## Instrument and security assessment

The reviewed algorithm implements the bound reference's LD-B2C0-1 anchor filter, full custody/depth boundary handling, subset test, member consistency, exact explicit-root selection/workspace folding, cap, effective-mode input, fallback, ordering, membership, scope descriptor and default selection. The public security mirror calls the shared rule; it does not duplicate pruning/enumeration policy. Its aliases match the registry and unknown keys refuse. The embedded capability matrix equals the architecture's bytes.

The rule file and custody.rs are byte-unchanged. Every pin in the existing receipt's modeled cost closure matches the candidate; no corpus store was opened for this check. Scope bounds/digest/disclosure and default selection's matrix obligation versus release availability remain sound. Full external-spec admission remains the later Plan stage's responsibility.

Cargo workspace status as an input is faithful to the oracle; J1 can use identity's existing TOML parser over C1 bytes. The reference membership record contains no membershipDigest field, so later Plan binding remains appropriate. FW-01 covers the host instrument and security export.

## Verification and evidence limits

Independently ran only the permitted checks:

- Source census: 114 rows, passed, no findings.
- FW-01: 7 tests passed.
- Discovery-unit-vectors --check: generated record verified against the accepted reference.

Independently replayed the 15 targeted grammar, multibyte and unknown-mode calls through the bound reference and compared their recorded outcomes, applying only the explicit grammar normalization. All agree. The complete vector record contains 135 steps.

Inspected recorded suite comparisons: security has the same 14 failures and 1128 passes at base/candidate; host has the same 8 failures and passes increase from 343 to 348. Recorded Clippy covers host and security with --all-targets and -D warnings and passes. All twelve mutation logs contain actual failing tests and no compilation errors. These Rust/lane results are recorded evidence, not reviewer reruns.

## Remaining work and boundaries

Lead assent/publication, product code integration and then inventory v201 remain subsequent steps. The inventory must cover the six new paths. No production caller, environment read, law change, qualification or entire-plan completion is claimed. B2-c2, later composition and workspace full-ledger obligations remain outside this acceptance.

Wrote only REVIEW.md and review.json in the requested directory. Neither repository, worktree, stage nor control files were edited. No Cargo, rustc, builds, lane, network, other panes or delegation were used. Execution was limited to the expressly permitted Python checks and read-only bound-reference probes. No private fixture, installation directory, signing keys, held trees or T2 held-out entry was accessed.
