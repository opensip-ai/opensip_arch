# B3-B3A1 inventory v208 review

Verdict: **ACCEPT-UNIT**. Inventory candidate assessment: **ACCEPT**.

Required findings: none. Non-blocking observations: none.

The subject manifest independently matches 704 bytes and SHA-256 `62a77af1e4e8df88d9d552be02005c298556e2cb22ea0b5931d00d1bb5c32ebf`. All three members match their declared sizes and hashes. Product main is clean at `3f8c60c0937286f3314268dfa7302c829457f281`; architecture is at `f04118f7206d0e578ea6105c18a3a533b5554d5b`. Integrated product files match the accepted B3-b3a1 product map. This review does not reopen the accepted code review.

## Added and inherited content

Exactly two rows are added, neither replacing an inherited planned row:

| Path | Package / role | Assessment |
| --- | --- | --- |
| `crates/security/src/custody/workspace_census_tests.rs` | `opensip-security` / `test` | `generated: false`. Accurately describes the accepted composition and worst-case controls, real scratch Git members, three synthetic root lengths, measurement after item 6a and comparison against the modeled charges. |
| `tools/security/discovery_member_model.py` | `tooling` / `builder` | `generated: false`. Accurately describes the D15 model, its closure/anchor relationship, native observations and item-6b ceiling costs, composition ordering, disjoint terms and explicit regular-file read envelope. |

Neither description claims workspace-margin acceptance, blind-mode completion or qualification. The model row does not repeat the accepted code review's non-blocking wording issue about all reads being no-follow.

The candidate has 1282 sorted, unique rows, a strict superset of the parent's 1280. Every inherited row is equal by value. All other top-level content is unchanged, including the 20 packages and nine pending decisions. All 1184 tracked product paths are covered. The other 98 rows are exactly the still-absent inherited planned paths, retained unchanged without implementation claims. The successor's `addedFiles` and `inheritedPlannedFilesRetained` lists equal the independently computed sets.

The six changed-path descriptions remain true, though incomplete:

- `discovery_census.json` still contains the described verified census pins, populations, modeled costs and classifications; the new D15 fields add information.
- `discovery_census_tests.rs` retains the described walker soundness, compiled closure and entry-classification controls; its additional sizes and full-ledger assertions do not invalidate them.
- `discovery_census_vectors.json` retains the described walker and composed-workspace predictions and closure, alongside the new composition predictions.
- `workspace_discovery_tests.rs` retains the described composition and race controls after the measurement/helper extraction and additional include.
- `discovery_census.py` retains the described ordinary store verification, walker population/model and composed census paths; the new model extends that functionality.
- `test_discovery_census_blind.py` retains the described synthetic confidentiality, receipt, lifecycle and ordinary-mode access controls; copying/stubbing the additional model does not change those claims.

None requires a new description override because of this unit. Keeping those inherited rows equal is appropriate for an additive successor.

## Census and pins

The expressly permitted source operability command passed with 114 rows and no findings. The exceptions document has 439 mint-audit rows. Both the checker and exceptions file match the integration-census pins and are byte-identical to the accepted unit's product base `e367d7f465d8d0a74819cad5010a58b8641e4c7a`. Source checking includes the mint-audit comparison. No mint authority is added; the lexical audit is not authority.

Independently verified successor bindings:

- Parent v207: 704710 bytes, `c811fe3f2ebf0d46c84754b71511f35e7f35a9a561f3a45176f709d0f6b46812`.
- Candidate v208: 706443 bytes, `3ba67e2d955c7c2a89e6d2cbfb12d69a322fbc865f1327cbbbc75b9742350a31`.
- Successor record: 5483 bytes, `5a930beea7a228270fea28c3c95306974f120589d3ad4ebcec667dc2b97cb7e0`.
- Accepted code review: 759 bytes, `7c55ae9c75cd317f1543ff7614af3680d4e875ce10d9ce6489d19a6ad90c6c46`, verdict `ACCEPT-UNIT`, no required findings.
- Accepted code subject: 18195 bytes, `ffe3c284165b8a816450213a59797f8be3350aa8e1c1fc95b21e44d49fd9d92d`, matching that review's subject binding.
- Integration census: 737 bytes, `bebae6ab0e16fda35e82961011a14ea487d1672a050fd18c2ddc1016a8dfe20d`, with the exact integrated product commit, source result and mint count.

No qualification is claimed. Lead assent, architecture publication, the separate inventory lock binding and fresh verify_design remain integration work.

Only `REVIEW.md` and `review.json` are written. Neither repository, stage nor control files were edited. No compiler, Cargo, tests, lane, network, private fixture, installation directory, signing keys, held trees, other panes or delegation were used. Nothing was pushed.
