# J3a-o additive inventory v169 r1

ACCEPT-UNIT. requiredFindings empty. inventoryCandidateAssessment ACCEPT. productQualification false. This subject closes the additive inventory only. The accepted J3a-o code review stays closed on its own subject.

Subject `docs/implementation/m3/operability/j3ao-inventory-v169-subject.json` is 1028 bytes, SHA-256 `b6ec8a99503e3e28b57f233fe0a86e1f48ed8cda0e47ac90cb8625ca52517958`. Its three members are sorted and unique, and each matches the stage bytes:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/repository-file-inventory.v169.json` | 637990 | `0b5c57f04f6a40a7ed770e474be44c14710aa2e7e76957c83541bdf9c36118c3` |
| `docs/implementation/m3/operability/j3ao-inventory-v169/source-census.json` | 723 | `c3a453cb20312a84ba3575fea1c829480887404f11414d66c7db05d179dd5550` |
| `docs/implementation/m3/operability/j3ao-inventory-v169/successor.json` | 5703 | `427952ce1bdb95a93431611951a4dbabe8a1257db0578fb40a0db08f35a929e4` |

The successor names the same candidate and the selected parent `docs/implementation/m2/repository-file-inventory.v168.json`, 637019 bytes, SHA-256 `196f38b89c164c0c6062f7d0678bd9bff10b4b7f37482c0b38ad82f225dbd781`. That parent file on architecture `62f91ec79dab3cab1ce7574be95c9f842e18346c` matches the pin. `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`, `packagesUnchanged`, and `pendingDecisionsUnchanged` are true. `rawPackagesUnchanged` is true on the subject.

## Code join

Product main is `92b3b9012ec0aa661861d1f0164f5d37c69498ae`, a descendant of `14e989de220db1d271bb63c716748df5527593f0`. Architecture `docs/implementation/m3/reviews/grok-j3ao-whole-unit-r1/review.json` is 278 bytes, SHA-256 `e723793b7264095f8e36ce85efe82c5c63d636c6bc0177cd9444a838b5d032d9`, verdict ACCEPT-UNIT, with `fullJ3aoCodeAccepted` true, `inventoryAuthored` false, and subject `b716ad14ef9699910803a4fce67b2241c31036913f99e6d4ae34214018833913`. That subject is `docs/implementation/m3/reviews/grok-j3ao-whole-unit-r1/subject.json`, 2344 bytes and the same hash. All 11 pins match the blobs at the product commit. The commit changes those 11 paths and no others: 3 additions and 8 modifications. `design-lock.json` is the same blob as at `14e989de`, object `63e094a43a1b926eff06fe6bf48fd53bac85a39e`. The lock is schemaVersion 4, with 128 inventory successors and 140 contract successors. The last inventory candidate is v168, SHA-256 prefix `196f38b89c164c0c`. v169 is absent from the lock. `tools/verify_design.py` is the same blob at that base and at this product commit, object `afcfa6728164f89a539cfe1bce279820a27b0b4e`, so the five-pin additive profile is unchanged. Bound O1-PKG remains the independent package policy. This inventory does not re-measure that policy.

## Inventory

v168 has 1145 sorted unique file rows. v169 has 1148. The path list is sorted and unique, nothing is removed, and every inherited row is equal by value. The 3 additions are exactly the successor `addedFiles` list, in order:

- `crates/operability/tests/refusal/cases/execution_id_from_unreserved_bytes.rs`
- `crates/operability/tests/refusal/cases/execution_identity_is_not_attempt_admission.rs`
- `crates/operability/tests/refusal/cases/request_scope_from_unowned_bytes.rs`

Each new row has only `description`, `package`, `path`, and `role`. The package is `opensip-operability`, the role is `test`, and the description is “J3a-o owning platform identity conversion and admission compile refusal control; exact accepted code unit, no qualification claim.” Each added path is tracked at the product commit. The eight modified code paths were already v168 rows, and those rows are unchanged.

`schemaVersion`, `packages`, and `pendingDecisions` match v168. The package list remains the same 20 ids. `opensip-operability` is not added there. Pending decisions remain 9. The candidate standing sentence is the only other top-level change. It records a proposed additive inventory of the J3a-o refusal controls, unchanged inherited rows, packages, and pending decisions, and no qualification.

The successor `inheritedPlannedFilesRetained` list is 100 unique paths. Each of those rows remains equal by value, with `standing` `proposed` and `generated` false. None of the 100 is tracked. The product tree has 1048 tracked paths, every tracked path is in v169, and those 100 planned paths are exactly the inventory paths absent from the tree. No path contains `SCRATCH`.

## Census

`source-census.json` records product `92b3b9012ec0aa661861d1f0164f5d37c69498ae`, checker `tools/check_operability.py` 14464 / `7fb837009a5cf1d286997f64e8f414548f97a57fb341402501f7845e52d069ba`, and `tools/operability/exceptions.json` 81203 / `58480de1b8321f2ea1d14971a7d931fff73130ad33bc3251afbf3ff82ba1a237`. Both blobs match the product commit. The exceptions document has 113 source rows and 425 mint-audit rows. The mint-audit standing is “Conservative lexical call census and complete owner-file definitions; not receiver type inference or mint authority.” The census records source check passed, findings empty, `lexicalAuditGrantsNoMintAuthority` true, `private413Read` false, and `realInstallationRead` false. The tracked tree has no mint-list file. `productQualification` is false on the subject, the successor, and the census.

Root assent, the five closed pins, and the projected inherited passage coordinates are verified by `tools/verify_design.py --architecture` and `--lock` before a separate lock commit. S-OP-2-P, S-OP-2-R, and S-OP-2b are already bound and closed. O1-b follows J3a-o binding and is not implemented by this inventory. This acceptance does not qualify the product or complete the plan. This review does not push.
