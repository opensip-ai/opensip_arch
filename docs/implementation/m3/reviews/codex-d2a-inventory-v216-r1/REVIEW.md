# D2A inventory v216 review

Verdict: **ACCEPT-UNIT**. Inventory candidate assessment: **ACCEPT**. No required findings or non-blocking observations. Product qualification: false.

## Exact subject and successor path

Independently rehashed the 680-byte subject manifest and all three staged members:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Subject manifest | 680 | `d765d00b2f200561765f5866cfdc5ea7211117dca39946343b6e31acddc26508` |
| Candidate inventory v216 | 726771 | `436062c470091d15729e6472b2d9a646c479ba629df1919af07538cf24de13ae` |
| Integration source census | 737 | `3a37502e3c1d80d7c99bf0e9e84c64badd5372be7ee0a6b60e793d59b43043c5` |
| Successor record | 5503 | `71f921112b58dd3fd3d20c3fbf6d8aea8c201f88e4e9f54f67a37b559af50d22` |

The candidate is at `docs/implementation/m2/repository-file-inventory.v216.json` in the stage. Both its manifest member and successor record name v216, distinct from the v215 parent. No replacement v215 file is present in the stage. The architecture parent remains 725,221 bytes, SHA-256 `a2d3fb7d87f484168352dd8a93f8cad843bcfa3d3c42b1cf9f2e8199a7dd140a`.

Clean product main is `a9a84a6fd369e7ca10689d6ab432bead3ad7eef2`; architecture HEAD is `1649a041df87555d682b4a5c30aeda67b16c6d97`. Both match the request.

## Inventory assessment

The candidate is a sorted, unique strict superset: 1,311 file rows versus the parent's 1,308. Exactly three rows are added:

| Path | Package | Role | Generated |
| --- | --- | --- | --- |
| `crates/components/src/control_protocol_tests.rs` | opensip-components | test | false |
| `crates/components/tests/data/control-completion.cases.v5.json` | opensip-components | fixture | false |
| `crates/components/tests/data/control-completion.rf5-proof.v2.json` | opensip-components | fixture | false |

The test description accurately covers the accepted corpus replay, matrix, prefix classifications, nonrecursive probes, fixed production policy, encoder and session sending controls, and schema closure. It does not claim stream acquisition or supervisor integration. Both fixture descriptions correctly identify retained reference evidence, not generated product artifacts or qualification. Independently compared the fixture bytes with their architecture CC v5 originals: both are exact copies.

Every inherited file row is equal by value, with no deletion or description override. All 20 packages, all 9 pending decisions and other inherited top-level values are unchanged. The inherited API, package manifest and dependency-lock descriptions remain accurate for the accepted changes to `lib.rs`, `Cargo.toml` and `Cargo.lock`.

`crates/components/src/control_protocol.rs` alone realizes an existing planned codec row. Its unchanged description, “Encode and validate common control frames without translating provider semantics,” remains true of the accepted module. No override is needed and no provider codec or supervision completion is implied.

All 1,216 tracked product paths are covered. The 95 inherited paths still absent from product remain unchanged and are exactly the successor's `inheritedPlannedFilesRetained` list. `addedFiles` equals the computed three-path difference and `realizedPlannedFiles` equals the single codec path. Retaining absent planned rows makes no implementation claim.

## Acceptance and integration census

Verified the successor's accepted-code review pin: 1,535 bytes, SHA-256 `aa1e5cd567d58a4af6b69494d17a36d1d4b5cb24527c4a6ca85df76928ed7f49`. It records ACCEPT-UNIT, no required findings, and the existing non-blocking privacy-mutation evidence observation. Its subject hash matches the independently verified 9,929-byte D2a-r2 subject manifest, SHA-256 `1b633d2db9cfac5294715407f73215085dbb8b30a44e5851f647b5830409cb2a`. All seven integrated product files match the accepted product-map candidate pins. This is an integration-identity check, not a code re-review; the inventory does not erase or expand that accepted review.

The integration census names the actual product commit and exact checker/exception bytes. Independently ran only the permitted source command:

`python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`

It passed with 114 rows and no findings, matching the staged result. The mint-audit record is unchanged from the product parent and contains 439 rows. The source check also compares that record with the actual lexical mint census. No mint authority is added.

The integration's changed paths have an empty intersection with the discovery census's 19 pinned closure files. There is no closure change from this unit to invalidate the blind receipt. The successor's parent, candidate, accepted review, accepted subject and integration-census pins are exact. No qualification is claimed.

Acceptance covers this staged additive inventory successor. Lead assent, architecture publication and the separate lock commit re-pointing inherited passages to v216, with fresh verify_design, remain subsequent steps. Their completion is not inferred here.

## Boundaries

No compiler, Cargo, tests, generator or lane was run. No network, other pane, delegation, private fixture, installation, signing key or held tree was accessed. Neither repository, the stage nor control files were edited. Only the requested REVIEW.md and review.json were written.
