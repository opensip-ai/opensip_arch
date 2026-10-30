VERDICT: ACCEPT-DESIGN-UNIT

Independent Codex review, round 2, 2026-10-29, R1-BALANCED, gpt-6.1-sol/medium. Unit C2B-M5-DESCRIPTIONS-r1. Required findings: none. B-RF-1 and B-RF-2 are resolved for exactly the subject manifest da17f38b01d08300a91da22ad43fe3ede0eede9cdc2fab5524df331fb36b90a8. The independently accepted inventory review is unchanged.

## Authority and verification

Read the round-2 REQUEST.md and ran its preflight before substantive review:

```text
python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/tools/agent_model_route.py check --provider codex --plan /Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/c2b-m5/review-binding/REQUEST.md
ROUTE-OK R1-BALANCED codex gpt-6.1-sol/medium
```

Applied round 1's retained limits. Rechecked the live M5 plan/route selection and Git standing: product main is clean at f61b0cbfdb2ff9f6e6606993daa59e00a0e8111e; architecture remains 6f28e1067242a53d4ffe5522b06e7bd69ebe8a52. All eleven round-2 request-table byte/hash pins match. The round-1 description review archive matches reviews-r1/, and its review.json names the frozen stage-r1 subject.

Verification used public source/JSON/Git reads, hashing, exact staged-tree/record comparisons, AST extraction of the staging script's literal replacement data, and the unmodified product design verifier on the existing lead dry-run candidate. The staging script was inspected, not executed. No product/architecture/lock edit, commit, push, root assent, build, product test, census, refresh or store access occurred. No private413, real home, keys, installs, T2 cache or held-out store was read. All new scratch stays under review-binding/scratch/; only this descriptions unit's REVIEW.md and review.json are rewritten.

## Findings

### B-RF-1 — Resolved: the current shared-rule relationship is accurate

v241 /files/770/description selects crates/security/src/discovery_export.rs. The replacement removes only the obsolete unchanged-file parenthetical, preserves the one shared rule being called rather than copied, and retains the security-owned construction and boundary authority text. The appended sentence accurately names the changes present at f61b0cb: the shared rule's crate-private excluded_path and crate-visible DEPENDENCY_TREE_SEGMENT, and AdmittedBoundaries' crate-private custody_rows and scan_shape read-only queries for snapshot-side pricing.

Checked the visibility and implementation of each named item in discovery_rule.rs and discovery_export.rs. No constructor is exposed, no new authority is claimed, and the correction changes the row's current descriptive meaning rather than accepted law or product source. Its before text is the exact raw/current v241 passage. The old replacement text occurs exactly once, and after equals that one replacement plus the specified tail.

### B-RF-2 — Resolved: the layout primitives and content-read boundary are explicit

v241 /files/818/description selects crates/security/src/snapshot_read_set.rs. The replacement accurately distinguishes the new primitives from open_pruned:

- reach_directory uses no-follow descriptor-relative traversal and S3 directory custody above the first node_modules segment, or throughout a first-party path, with descriptor discipline at and below the dependency segment.
- list_directory uses the walk's charged listing conversion, drops dot names and observes other names no-follow; observe_entry and reached_dependency_cargo_root are observations.
- read_link calls the charged platform readlinkat through the held descriptor and returns only stored symlink text, never following it; non-UTF-8 text yields None.
- layout_exclusion charges before the extent/shared-rule predicates; resolve_link and its cost helper describe lexical resolution, with no open or follow.

The revised content statement distinguishes the symlink-text read from regular-file source contents, which remain captured by crates/host/src/snapshot.rs. All preceding open_pruned dependency-path, no-follow and custody restrictions and the trailing charged-first/library-only/no-production-caller text remain exact. This is the requested local correction; it does not grant a read-set implementation, production caller, link-following capability or native authority.

The old no-content substring occurs once. The new after text is exactly its replacement, with no other change to that inherited description. The primitive descriptions were checked against their implementation and the platform link-read mechanism.

### B-NBO-1 — The round-2 delta is complete and preserves prior accepted bytes

Compared the entire stage/ file set with stage-r1/: path sets are identical; exactly three files change, the descriptions README, successor record and subject manifest. Inventory v241, its successor and subject, and evidence/m5-summary.json are byte-identical.

The successor has exactly four unique overrides, numerically ordered 770, 815, 818, 1387. The original two overrides at rows 815 and 1387 are equal to round 1 as complete JSON objects, including parent pins and before/after text. Outside passageOverrides, only standing and the README candidate pin change; schemaVersion, parent pins, summary candidate pin and empty passageSupersessions remain unchanged. The README now names four rows and the two resolved findings without adding an execution or qualification claim.

The subject contains exactly README, summary and successor, sorted and pinned to their actual bytes. review.json.subjectManifestSha256 is the new subject's digest, not the candidate inventory's digest. Neither the existing inheritance projection nor current direct meanings alter any of the four selected raw v241 passages, so no supersession link is needed and supersededPassages remains empty.

The entire 41-file source population from the round-1 effective-description completeness sweep was rehashed against its retained audit pins; every file is unchanged. Its earlier conclusions remain applicable, with both identified false meanings now corrected. The inventory review's REVIEW.md and review.json are byte-identical to their round-1 archives. References there to the companion's round-1 findings are retained history, not rewritten acceptance evidence.

### B-NBO-2 — The unchanged summary retains its bounded evidence standing

Rechecked the eight referenced review pins/verdict lists, six committed receipt pins, refresh-log pin and final-lane report pin. They still match the unchanged summary. Its accepted frozen M5d result remains execution at 5327e75 under the reviewed expected-failure/ignore/flake policy; it is not a wholly passing workspace run at f61b0cb. The separate source/fix/receipt reviews and final lane retain their own subjects and meanings. No M5d replay, L8b2 production execution, production caller, native authority, push or product qualification follows.

### B-NBO-3 — Exact binding remains gated on real assent and final verification

Re-ran the unmodified product tools/verify_design.py against binding/dryrun and its r2 candidate lock. It exited 0 and reported passed=true, 201 inventory successors, 189 contract successors and productQualification=false. Confirmed that the candidate lock selects the exact current r2 description record/subject, not round 1. Inheritance remains 180, carrying the prior 169 meanings and the S4 current overrides/supersession tails; none conflicts with the four new direct overrides.

The dry-run reviews and root assents are placeholders, so this result is structural evidence only. make_assents.py and bind_lock.py are unchanged from round 1. Their gates continue to bind accepting review verdicts with empty requiredFindings to the exact subject manifests, candidate/record pins and root assents; bind_lock.py then derives inheritance and invokes the unmodified verifier. This acceptance permits the lead to proceed through those separate gates for exactly the reviewed bytes. It is not root assent, final live-lock verification, integration, a push or product qualification.

## Reviewed bytes

L = /Users/sb/code/.opensip-implementation-cache/lead-2026-10-25; P = /Users/sb/code/opensip-ai/opensip. L paths below are relative to L. The retained round-1 audit carries the 41 source pins rechecked this round; audit-r2.json records the exact staged delta and unchanged inventory-review pins.

| Subject | Bytes | SHA-256 |
|---|---:|---|
| c2b-m5/binding/stage/docs/implementation/m3/snapshot-plan-c/c2b/m5/descriptions-r1-subject.json | 716 | `da17f38b01d08300a91da22ad43fe3ede0eede9cdc2fab5524df331fb36b90a8` |
| c2b-m5/binding/stage/docs/implementation/m3/snapshot-plan-c/c2b/m5/descriptions-r1/successor.json | 9883 | `7daab8230dd2d9ec585f082f51403b7daaff40bb0b6a59ac2df082fe6f0bab51` |
| c2b-m5/binding/stage/docs/implementation/m3/snapshot-plan-c/c2b/m5/descriptions-r1/README.md | 1072 | `1328a3ae555e858648bef4fca00f61809c8d38d50e1980d061617883cc485dbc` |
| c2b-m5/binding/stage/docs/implementation/m3/snapshot-plan-c/c2b/m5/descriptions-r1/evidence/m5-summary.json | 5204 | `6e0589553e75b85a8ee6861637294dc3cfbe6ac15d09012f68f1bda5c44ce15a` |
| c2b-m5/binding/stage/docs/implementation/m2/repository-file-inventory.v241.json | 822071 | `77f298a1181f8250f576192e37e587ed2041e3d9c22f0392170acd45be818197` |
| c2b-m5/binding/stage_binding.py | 8313 | `f5bdc274e39bcdcc0f1df7e5673553be534566471517c37d6ee808f9059bd40f` |
| c2b-m5/binding/stage_binding-r1.py | 5441 | `b3bfb2d08d81b3c11e6c37472bb8e88b0abc27865b1973a11abfccc825712ec8` |
| c2b-m5/review-binding/REQUEST-r1.md | 8505 | `a0064ce248b3e57cdd9ea223b06a8a8b25046d1313454c690b2a908cd5c860b8` |
| c2b-m5/review-binding/REVIEW-descriptions-r1-r1.md | 12331 | `c50f52324989f30b279880f49aa328a3634a69aba8d263c90658632706a9757e` |
| c2b-m5/review-binding/REVIEW-inventory-v241-r1-r1.md | 9067 | `62c3170c8e1e55831bcfd64f3840095118b69b93b90e6f9901ee1b522a7b90d1` |
| c2b-m5/binding/dryrun/design-lock.json | 808686 | `2b09525ed5c17a3d3906cbb5a7bd4db6fac1382a6e06f7ab96da8e65ad08fae0` |
| P/crates/security/src/discovery_export.rs | 10760 | `c78c4d95bdf9a271c3536858769fd6a56b74a84b194ff722864455eeeb0ed879` |
| P/crates/security/src/custody/discovery_rule.rs | 25668 | `c935f17f570fdc02705fefb19d503788d34a9fd3bd1da3b2afd37b3c76657f65` |
| P/crates/security/src/snapshot_read_set.rs | 31113 | `8eadd3522db9f3c6402e4f6728c0e04ccb4e18ec87e67f53ff17d83ca25b0043` |
| P/crates/platform/src/link_target.rs | 5307 | `249a4c0d897fb15d982b02cdac688f73df409b6fd7adc2b201c550f013bcadf4` |
| P/crates/host/src/snapshot.rs | 33734 | `e281f3b6ee18dab7a8b8a7235fcde79131c3b1033fe3c9cc2656d5a105d88731` |
| P/tools/verify_design.py | 43946 | `7b313de629f2c958a1e62538b909d6f01545be2519238ba9b3d86ab7e7ba3326` |
| c2b-m5/binding/bind_lock.py | 3707 | `1adf7d89e32bf91a1b137ee4e5d51e0369fea28cbd23fb94f11e49e36571951a` |
| c2b-m5/binding/make_assents.py | 4061 | `7c146c992b44d62502f1fa32f129510fcf0c83f9c0588f7e8076d20d27630f89` |
| c2b-m5/binding/stage/docs/implementation/m3/snapshot-plan-c/c2b/m5/inventory-v241-r1-subject.json | 488 | `c9834ab6e168eb2cdadd5b82e83903c260edcb4c558c1157b612d1c613fff871` |
| c2b-m5/review-binding/scratch/audit.json | 39744 | `739a41af97ffe0f5faa0677c14d970a7d0b65210a4602b586f9367bbe37e11c4` |
| c2b-m5/review-binding/scratch/audit-r2.json | 3814 | `e9a34b8017212c802b856e11e2a78a3f1d67b131b017d50355a53bb1056bad38` |
| c2b-m5/review-binding/scratch/dryrun-r2-verification.json | 2391986 | `422161a743d7296ed93d2e002f2c7b0c86de7db69fd026548a737eb3b3de5dc7` |
| c2b-m5/review-binding/REQUEST.md | 5076 | `4b7b71d83866836f99ac092f3ef5dcbf980837e870038739c838dfa4bf0fd5f8` |
