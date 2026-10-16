# B3-B2B2B-r5 review

**Verdict: ACCEPT-UNIT.** No required findings or nonblocking observations.

Manifest: 39,004 bytes, SHA-256 `70e1024afbd4ca80ce72f3e7e2ab865567daed417149a391044187aca07cdccf`. All 156 members rehashed successfully. All 21 product-map candidate/archive rows and mapped parents, authority pins and the product-lock pin match. The r3 and r4 manifests and every member of those packages remain at their reviewed bytes. Product main is clean at `92624ae00f242d9a56e4305146e1d69665e2ecc5`; candidate HEAD matches that base; architecture HEAD is `271d7eee4759799e9a731c34ff1d2517f2862727`.

## Previous finding

**B3B2B2B-R4-RF-1 is resolved.** The identity collector no longer relies on per-record slack to absorb implicit Vec growth.

- **List:** reserve_identities charges owned((segments + 3) * slot_size) before allocated creates the list. member_layout records one identity per opened member-path component, plus at most three present layout samples: .git, config and index. The exact label matches restrict those layout records to the intended three. Thus the reserved capacity bounds all pushes, including the first, without growth. With at most 256 member-path components, the slot count is at most 259. Early refusals or an absent index can leave paid capacity unused; they cannot exceed it. The 128-byte owned allowance is now overhead beyond the fully priced list buffer, rather than a substitute for unfunded slots.
- **Paths:** push_identity computes the sum of its parts without constructing a path, charges owned(len), and allocates one buffer at that capacity. The directory-prefix iterator and the three-part Git-label iterator concatenate exactly that total. No to_vec-then-extend or prefix join allocates an intermediate identity buffer, and extension cannot exceed the preallocated length. owned(len) therefore covers the requested path buffer plus the existing conservative overhead allowance.
- **Allocation order and legacy path:** every added identity list/path allocation goes through allocated after its charge. The counter is at that allocation, so an allocation moved before a refusing charge is observable. Collection remains opt-in; observe and observe_members do not reserve a list or build identity paths, retaining their established charge path. Cached-read copies still charge before cloning.

The revised flow control derives requested storage from actual list and path capacities, rather than reusing the cost function as its oracle. It covers shared prefixes, long Git-label paths and filling the reserved lists to their capacity. The tight-ledger control verifies that neither list nor path allocation occurs after a refused charge. The seven identity mutations cover underpriced buffers, growth, missing charges and allocation ordering. This addresses both the size and order gaps from the previous review. These are requested-storage bounds, not allocator/RSS claims.

## Other judgments retained

Only git_tracking.rs and git_tracking_member_tests.rs differ from the reviewed r4 mapped product bytes; the other nineteen product files are identical. The functional boundary, custody, binding and composition judgments remain applicable.

Branch A still follows accepted A4 and bound B3-b0 r4: array size, global grammar, placement/volume rules, member cap, custody and item 6b per candidate, then one member/gitlink-aware walk. Links follow only an accepted branch-A walk. Gate paths remain raw, D9 and source-specific details remain correct, and a no-members walk supplies refusal provenance without replacing the selected gate verdict. Walk refusals clear member/config rows and preserve the specified declaration rows.

The shared object bindings include reopened ancestors and member Git evidence before the member verdict reaches the core. No-follow traversal, positive marker lookups, listing conversion, retained custody-captured reads and post-read full-status/ACL checks remain. Repeated providers use the validated-read cache. The complete V3 record remains the emittable result with the pending core internal.

The 41 composition and 189 member-vector cases, walker-trace non-entry assertions, gate and short-circuit controls, preserved-inode identity races, repeated-provider controls and member-configuration refusal case remain. The walk/sixB seams and distinct forbidden-read/forbidden-lookup checks retain their prior meaning. Non-string reference arrays remain explicitly excluded because the product arrays are typed as strings. The scenario still uses the operation's own precondition and retained-root custody premises.

Read-only comparison independently confirms that each census JSON file differs from base only at the bytes/SHA fields of closure indices 0, 4 and 6. No census or held-out operation was performed.

## Verification and evidence

All three permitted fresh checks pass:

- Operability source: 114 rows, no findings.
- workspace_discovery_vectors.py --check against bound B3-b0 r4.
- workspace_member_vectors.py --check against bound B3-b0 r4.

The final archived lane records identical 14-failure base/candidate sets and fourteen new passing tests. Library passes increase 1,145 to 1,159, with five ignored at both subjects; including six documentation tests, totals increase 1,151 to 1,165. This is equal-failure-set evidence, not a green full suite. The composition run has twelve passes, focused discovery/member checks ninety-two, and host discovery_flag_tests seven.

Both warning-denied Clippy configurations, formatting, all vector checks, census controls/check and equality projection, operability, environment checks and verify_design are recorded passing. All thirty-nine mutation logs show successful compilation followed by failing tests; the control summary records all caught. The archived first r5 attempt shows the two allocation-order survivors, and the final allocation-site counter and lane resolve them.

No Cargo, rustc, tests, builds, lane or census tool was run during this review. No network, other panes or delegation was used. No protected fixture, installation directory, signing key, held tree or T2 held-out data was read. Only REVIEW.md and review.json in the requested directory were written; neither repository, worktree nor any control file was edited.

This acceptance covers the requested native observation/composition unit. Its inventory integration, B3-b2b2c's T2/joint controls, B3-b3a/b/c's bound and margins, J1 and qualification remain separate work as the plan states.
