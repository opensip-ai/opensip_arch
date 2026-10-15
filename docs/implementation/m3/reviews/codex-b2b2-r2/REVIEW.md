# B2-B2-r2 review

**Verdict: ACCEPT-UNIT.** B2B2-1 is resolved. No required findings; one nonblocking documentation observation below.

## Subject and bases

Rehashed the 6,944-byte manifest, SHA-256 `5b2f87759dc0993b6563ca05bdba12574bbdba7a55eac0ce10c516c90bab02a5`, and all 31 members. Every size and digest matches. Verified all authority pins and the product-lock pin. Every product-map candidate matches the archived and worktree bytes; existing parent pins match the product base and the four new paths are absent at base. The candidate contains exactly the six mapped paths.

Product and worktree HEADs remain `f51769f885dc786168e487033645ad1a4e0ae699`; architecture HEAD is `588e3e847379e871d9b86d73c4b86a27f08f9998`. Main product and architecture tracked states are clean. Inventory remains v191 and contract successors remain 164.

## Finding closure and implementation

`reference_order` fixes B2B2-1 without changing the legacy judgment. It supplies neutral linkage/size values only to the pure shared check, so kind, owner, mode and the real captured ACL are judged first. It then checks the original file metadata for one link and the existing S3 size limit. The original observation is not modified. Directory judgments are unaffected by file linkage/size. The legacy entry point continues to call the shared judge with no waiver and retains its original refusal order.

Eight new bound-reference vectors cover ACL-write and unreadability combined with hard linkage and oversize, clean-ACL linkage/size failures, and waived chains whose foreign-owned marker remains refused. The side-by-side test explicitly distinguishes discovery's ACL-first result from legacy linkage/size-first behavior. The new `links-and-size-before-acl` mutation reproduces the original mismatch and is caught by both this test and the vector replay. This is substantive regression coverage, not merely a new assertion mirroring the corrected helper.

The remainder of the core preserves the reviewed finish flow: nested boundaries, exclusive unit source, exact roots and JOIN details, automatic enumeration through the shared rule, ordered custody/depth exclusions, post-exclusion cap and D9 mappings. The ObservedAcl interface faithfully carries normalized readable captures or unreadability, including premise-admitted empty ACLs. The typed waiver reaches only directory chains in the core and skips owner alone; markers always receive no waiver.

Pending provenance still has no production serializer, implementation/completion method or declaration type. The complete boundary inventory has the sole production JSON projection, rejects non-accepted results, converts locators and ordering correctly and drops exclusions already explained by nested boundaries. No walker, descriptor observation, ledger, caller, public-row mapping, environment read or export is added.

## Vectors and evidence

Inspected the generator, metadata/ACL/VCS conversion and Rust result dispatch. Pinning and package-closure checks remain intact. All **79 vectors** regenerate from successor 164: 45 finish-reaching discovery cases and 34 controls, yielding 65 accepted and 14 refused results. The 19 pre-finish refusal cases remain explicitly listed for B2-b3, whose upward selection owns them. Every pending field and each accepted inventory is compared against the reference.

Independently ran only the three permitted offline checks:

- Source census: passed, 114 rows, no findings.
- Environment-exception check: 10 checks passed.
- Discovery-scan vector check: exact regeneration passed.

Inspected the remaining evidence without executing its driver or compiler. Security has equal named failure sets (14), with 1078 → 1086 passing tests; host retains the same eight failures and 336 passing tests. Suite counts agree. These are unchanged-failure comparisons, not fully green suites. Locked/offline all-targets Clippy for host/security with warnings denied is recorded passing. Rustfmt covers the base-clean/new Rust files; `project_chain.rs` remains explicitly base-dirty and excluded. Configuration-table checks are recorded passing. Parsed design verification passes with inventory v191 and 164 successors.

All nine mutation logs contain the stated failing tests rather than compilation failures. The planted environment read fires `disallowed_methods`, for **10 caught controls** overall. The new mutation log shows exactly the original ACL-versus-linkage mismatch, establishing that the added regression controls detect it.

## Nonblocking observation

**NBO-1:** SCOPE.md's r2 introduction correctly says 79 vectors and lane r3, but the paths table and Tests introduction still say 71, and the inherited Check lanes paragraph still calls lane r2 current. Update those statements or label the older lane paragraph historical. The actual vectors, assertions and evidence have the correct current values.

## Boundaries and remaining work

Used permitted read-only inspection, hashing, JSON parsing, Git queries and the three offline checks. Ran no Cargo, rustc, builds, lane or additional tests; used no network, other panes or delegation; accessed no private fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, worktree, stage nor control files were edited. Wrote only `REVIEW.md` and `review.json` in this directory.

Acceptance covers this exact sub-unit. Lead assent, architecture publication, the product code commit and separately reviewed inventory v192 remain subsequent actions. The walker, T2 census/all-entry margin, readers, production composition and qualification remain outstanding; the entire plan is not complete.
