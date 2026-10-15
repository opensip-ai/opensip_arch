# B3-A inventory v190 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none. This is an inventory-only acceptance; the accepted B3-a code was not re-reviewed.

Verified the 695-byte subject manifest, SHA-256 `a6f7fd8e66652cfbf042dbdec8ba2f17da03a00318dc6e04ae5dca17fc6a98a1`, and all three members by byte count and SHA-256. The 672,997-byte candidate matches `1c6f17df0eeebc747defcd8b89d08a13b9fafa8965e8609d62139b4a04bd583e`; the 5,543-byte successor record matches `1e004c3600cd13702642d1859247cd4d2df959dbdcd6371b571bf66c52de3eea`.

The parent matches committed v189: 671,444 bytes, SHA-256 `d8b31737f66c0e645d425abf9f7f3f9452d567af23efe2ce1f2c3c5da4abe78d`. All 1,227 inherited file rows are equal by value, including grants.rs and every existing row for a changed product file. Top-level fields, all 20 packages and all nine pending decisions are unchanged.

The candidate has 1,230 sorted, unique rows and is a strict superset. Exactly the three requested paths are added:

| Path | Package | Role | Generated |
|---|---|---|---|
| crates/security/src/grants_tests.rs | opensip-security | test | false |
| crates/security/src/storage_choice_vectors.json | opensip-security | fixture | true |
| tools/security/storage_choice_vectors.py | tooling | builder | false |

Their descriptions accurately identify the accepted invocation-record/choice controls, generated 144-case reference fixture and developer vector tool. They claim no qualification, execution/mutation/recovery grant or additional production capability. The added paths equal the accepted product map's new paths excluding grants.rs, whose planned inventory row already existed.

Keeping grants.rs unchanged is appropriate. Its validator role and description, "Bind and verify exact execution, mutation and recovery permissions.", identify the module's lifetime responsibility, not a declaration that every responsibility is implemented at M3. The accepted B3-a scope remains the invocation records and pure S3.1 choice; execution, mutation and recovery grants remain later work. Presence is established by the committed product path, without rewriting the inherited role description or standing.

All 1,131 tracked product paths at `eea381f5736ae9fef2f280f9c6b36a12d69d8f3b` are covered. grants.rs is now tracked/present. The remaining 99 candidate paths are exactly inheritedPlannedFilesRetained, are absent from the tracked product tree and retain their parent rows without new implementation claims. addedFiles is exact.

The accepted-code review and code-subject pins match committed architecture bytes at `8597ffe8e2beece34c8bbbcd48ee91054d315a0a`. The review is ACCEPT-UNIT with no required findings and binds the same subject hash. All seven accepted product-map candidate pins match committed product bytes; this verifies integration identity without re-reviewing code. Both repository HEADs match the request and the product is clean.

The integration census member and its checker/exception pins match the committed product. Independently ran the expressly permitted `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`: passed, no findings, 114 rows. The exception document is unchanged by value from the pre-B3-a product, including all 439 mint-audit rows. No mint authority is added; the census remains lexical evidence.

The successor record pins the exact parent, candidate, accepted review, accepted code subject and integration census. It claims no product qualification. Lead assent, architecture publication and the separate inventory lock binding with fresh design verification remain subsequent steps.

Review used only read-only hashing, JSON parsing, Git queries and the expressly permitted source-census command. No compiler, Cargo, other tests, lane, network, private fixture, installation directory, signing keys, held trees, other panes or delegation were used. Neither repository, the stage, controls nor prior reviews was edited. Only this directory's REVIEW.md and review.json were written.
