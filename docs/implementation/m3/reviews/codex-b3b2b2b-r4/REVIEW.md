# B3-B2B2B-r4 review

**Verdict: REQUIRED-FINDINGS.** One P2 storage-bound finding remains.

Manifest: 21,093 bytes, SHA-256 `e20a637d387a33b7c3b35eed9ed002a43f6629ebc310c7b1e4ae19d483f0a02b`. All 86 members rehashed successfully. All 21 product-map candidate/archive rows and mapped parents, authority pins and the product-lock pin match. The unchanged r3 manifest and all 194 of its members also match their reviewed pins. Product main is clean at `92624ae00f242d9a56e4305146e1d69665e2ecc5`; candidate HEAD matches; architecture HEAD is `271d7eee4759799e9a731c34ff1d2517f2862727`.

## Previous findings first

**R3 RF-1 is resolved.** copy_kept inspects the borrowed cached outcome and charges owned(len) before the clone. The test-only copy event follows the charge. The insufficient-budget control checks that it is not reached, the ample-budget control checks the charged cost, and both missing-charge and copy-before-charge mutations are caught. Validated repeated reads retain their established semantics.

**R3 RF-2 is partly resolved.** The new optional collector correctly removes identity-record construction and its new charges from observe/observe_members. Identified observation now charges before constructing each path and inserting its record. Prefix lengths and Git-label final lengths are computed correctly, and the legacy-versus-identified comparison accounts for repeated shared prefixes. However, identity_cost is not a sound bound on the requested allocations, as detailed below.

**R3 NBO-1 is resolved.** SCOPE now states that attempt 2 also failed formatting.

## B3B2B2B-R4-RF-1 — The identity charge does not bound the buffers its builders allocate (P2)

R3 RF-2 is only partly resolved. Identity collection is now opt-in and a charge precedes each build, but identity_cost prices final path length plus one tuple slot plus owned’s 128-byte allowance. This does not bound the actual requested buffers. First, an initially empty MemberIdentities grows through Vec::push: the pinned Rust 1.95 RawVec allocates at least four slots for an element of this size. Let S be the tuple size. The first one-byte identity is charged S + 129 bytes, but the list buffer alone requests 4*S bytes. DescriptorMetadata plus Vec makes S greater than 128/3, so even the raw slot allocation exceeds the whole record allowance. Second, label_in_git starts with member.to_vec() and extends it. For a long member spelling of length L, adding /.git grows the path buffer to about 2*L on this toolchain, while the charge uses only L plus the short suffix and fixed overhead. The debug assertion checks length, not capacity or requested growth. The new controls compare charges to identity_cost itself and prove ordering, but cannot detect these under-sized charges.

**Required change:** Fund the list capacity and path-buffer allocation/growth that the identified path actually requests, before those allocations. One option is to charge and reserve a known bounded identity-list capacity up front, then build Git labels once at their computed final capacity. Alternatively account each explicit buffer growth using a reviewed bound. Keep collection opt-in and preserve the legacy observe/observe_members charge path. Do not rely on the fixed 128-byte record allowance to absorb path-length-dependent growth or the initial multi-slot Vec allocation.

**Validation:** Add independent requested-storage controls for the first identity in an empty list, a list growth boundary, and a long member spelling producing .git/config/index labels. Assert the actual requested capacities fit the precharged bound, including the tight-budget case. Retain charge-order, legacy equality and identity-binding controls, and add an under-sized-cost mutation rather than only missing/reordered-charge mutations.

This is a requested-storage accounting issue, not an allocator/RSS claim. The local pinned toolchain source establishes the relevant growth: alloc/src/raw_vec/mod.rs:158 selects a minimum capacity of four for these moderate-sized elements, and :521-522 doubles existing capacity. The identity list uses ordinary push; the Git-label builder uses to_vec followed by extensions. No Rust code was compiled or executed to establish the finding. The later B3-b3a census derivation does not replace the current obligation to fund these allocations before requesting them.

## Other round-three judgments

Only four product files differ from the reviewed r3 archive: git_tracking.rs, git_tracking_member_tests.rs, workspace_observation.rs and workspace_discovery_tests.rs. The other seventeen mapped product files are byte-identical. The accounting changes preserve the prior functional identity comparisons and reference-derived behavior.

The accepted A4/r4 flow remains: array size, global grammar, placement/volume rules, member cap, per-candidate custody and item 6b, then the single member/gitlink-aware walk. Branch-A links run only after acceptance; walk refusals clear member/config rows and retain the pre-link declaration rows. Gate paths remain raw, source-specific size details and D9 mappings are retained, and the no-members walk supplies provenance without replacing the gate verdict.

The shared binding table, no-follow traversal, custody-bound descriptor reads and full-status/ACL postchecks are unchanged. The independent ancestor/member/Git-evidence controls still detect changes inside item 6b before admission. The complete V3 serializer remains the emittable result; keeping the pending core as an internal partial remains acceptable.

The 41 composition cases, 189 member-vector cases, walker-trace gitlink assertions, gate controls, paired unlistable-subtree case, repeated-provider cases and member-configuration refusal control remain. walk and sixB pin the reference seams; forbiddenReads and forbidden preserve the distinct access prohibitions; the short-circuit tripwire is scoped to custody/6b. The two non-string reference arrays remain explicitly excluded by id because product arrays contain strings. The scenario still derives its precondition and custody premises from the operation's retained subject/root.

Read-only JSON comparison confirms that both census files change only bytes/SHA fields at closure indices 0, 4 and 6. No census execution or held-out access was performed. The full-ledger bound and later margins remain outstanding as stated.

## Verification and evidence

All three expressly permitted fresh checks pass:

- Operability source: 114 rows, no findings.
- workspace_discovery_vectors.py --check against bound B3-b0 r4.
- workspace_member_vectors.py --check against bound B3-b0 r4.

The pinned lane records the same 14 base/candidate failures and fourteen new passes. Library passes increase 1,145 to 1,159, with five ignored at each subject; including six documentation tests, totals increase 1,151 to 1,165. This remains equal-failure-set evidence rather than a green full suite. The composition run has twelve passing tests, focused discovery/member checks ninety-two, and host discovery_flag_tests seven. Both warning-denied Clippy configurations, formatting, all vector checks, census controls/check, operability, environment checks and verify_design are recorded passing.

All thirty-four mutation logs show successful compilation followed by failing tests, and the pinned control summary records all caught. The four new mutations establish presence and ordering of charges. They do not establish the independent size bound identified above.

No Cargo, rustc, tests, builds, lane or census tool was run in this review. No network, other panes or delegation was used. No private fixture, installation directory, signing key, held tree or T2 held-out entry/store/overlay was read. Only REVIEW.md and review.json in the requested directory were written; neither repository, worktree nor any control file was edited. T2/joint controls, B3-b3a/b/c, J1 and qualification remain separate work.
