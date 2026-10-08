# O1-a additive inventory v168 r1

ACCEPT-UNIT. requiredFindings empty. inventoryCandidateAssessment ACCEPT. productQualification false. This subject closes the additive inventory only. The accepted O1-a code review stays on its own subject.

Subject `docs/implementation/m3/operability/o1a-inventory-v168-subject.json` is 1024 bytes, SHA-256 `b59b3c639b2c2521bbb84554326208437c467ccc40b6ef416aeeabe26199481c`. Its three members are sorted and unique, and each matches the stage bytes:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/repository-file-inventory.v168.json` | 637019 | `196f38b89c164c0c6062f7d0678bd9bff10b4b7f37482c0b38ad82f225dbd781` |
| `docs/implementation/m3/operability/o1a-inventory-v168/source-census.json` | 753 | `539ae707ecd575a9d2e24bcab642dec4e0cdaef4117a9fe02f8ea044d3192aa0` |
| `docs/implementation/m3/operability/o1a-inventory-v168/successor.json` | 9602 | `6bbe541a687e11d9401812e10f75428b02c54e994288afd11f752f39fa2fb84b` |

The successor names the same candidate and the selected parent `docs/implementation/m2/repository-file-inventory.v167.json`, 618550 bytes, SHA-256 `718cde32c35771b11527e45715a662c0850228d82b7bf611bfca541553bbbf2b`. That parent file on architecture `cea283d5b1b92ec9d2f50877638837d562386786` matches the pin. `parentArtifactBytesUnchanged` and `inheritedRowsEqualByValue` are true.

## Code join

Product main is `31ac89a9276571e559d40619e659f84b134b2b90`. Architecture `docs/implementation/m3/reviews/grok-o1a-whole-unit-r1/review.json` is 246 bytes, SHA-256 `85d0bb7b2114544d7b221c1384b5e14f11387863b43accfd3436bf607ff6b2c9`, verdict ACCEPT-UNIT, with `fullO1aCodeAccepted` true, `inventoryAuthored` false, and subject `17f1dbe4842bc5177bb3ceade3101d4d9059baf6f2722ce9720ba878b563edc5`. That subject is 14846 bytes and the same hash. All 80 pins match the blobs at the product commit. The commit changes those 80 paths and no others: 71 additions and 9 modifications. `design-lock.json` is byte-identical to `bf9561a4c280a141ba4cf14d7acf535e6dbb5bd0`. The lock still has 127 inventory successors, and the last candidate is v167. `tools/verify_design.py` is the same blob at that base, at this product commit, and at HEAD, so the five-pin additive profile is unchanged.

## Inventory

v167 has 1074 sorted unique file rows. v168 has 1145. The path list is sorted and unique, nothing is removed, and every inherited row is equal by value, including description, generated, package, role, and standing. The 71 additions are exactly the successor `addedFiles` list and exactly the paths v167 does not cover in the product tree. Each of those paths is tracked at the product commit. The nine modified code paths were already v167 rows, and those rows are unchanged.

`schemaVersion`, `packages`, and `pendingDecisions` match v167. The package list remains the same 20 ids. `opensip-operability` is not added there. Bound O1-PKG `package-policy.json` is still 7741 bytes, SHA-256 `0961c2fd544f1288c72f1a0eda2dd581df85d10f3cb45e902503b1a754af8463`. Sixty-six new rows use package `opensip-operability`; the five tooling rows use `tooling`. Roles are manifest, rust-source, test, and validator. Each description names the accepted O1-a code unit. The candidate standing sentence records a proposed additive inventory, unchanged raw package policy, separate effective permissions, and no qualification.

The parent’s 100 planned paths are still absent from the product tree. v168 keeps each of those rows equal by value, all `standing` `proposed` and `generated` false. No planned path was removed or rewritten as implemented. After the 71 additions, the product tree has 1045 tracked paths, every tracked path is in v168, and the only inventory paths absent from the tree are those 100 planned rows. No path contains `SCRATCH`.

## Census

`source-census.json` records product `31ac89a9…`, checker `tools/check_operability.py` 14448 / `72cdf111a74e494f9b7b3852707afbd6f97c615f9e604768dcb5750a5c3d69ad`, and `tools/operability/exceptions.json` 44504 / `09506587717478fdb0e79a016dec4c3db97582446923b492e6ce2d4a3eeedc4d`. Both blobs match the product commit. The exceptions document has 113 source rows and 176 mint-audit rows. The census records source check passed, findings empty, and no mint authority from the lexical audit. The tracked tree has no mint-list file. `productQualification` is false on the subject, the successor, and the census.

Root assent and the verified lock commit follow this acceptance. S-OP-2-P, then S-OP-2-R, then S-OP-2b, follow an O1-a bind. This review does not push.
