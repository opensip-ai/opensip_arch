# SRH-1 additive inventory v171 r1

ACCEPT-UNIT. requiredFindings empty. inventoryCandidateAssessment ACCEPT. productQualification false. This subject is the additive inventory and the integration census. The accepted SRH-1 code review stays closed on its own subject.

Subject `docs/implementation/m3/snapshot-plan-c/srh-inventory-v171-subject.json` is 688 bytes, SHA-256 `505b8a0edd1dfc11927e12163829448e88ea99cd8b7642c430eb7234fbf0c567`. Its three members are sorted and unique, and each matches the stage bytes:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/repository-file-inventory.v171.json` | 639720 | `d55288037a126716dc106592b10b4090fb5bbd4dddbeccad6eb51c7d90deca3d` |
| `docs/implementation/m3/snapshot-plan-c/srh-inventory-v171/source-census.json` | 723 | `94de974956e58dc79e9661f50173ee2613827dc024adb4227ccfff1fa3e0f7ce` |
| `docs/implementation/m3/snapshot-plan-c/srh-inventory-v171/successor.json` | 5556 | `9912fd06a1508c7a7897176e59025215f426077954f69d3483c25c3b4a3a880d` |

The successor names the same candidate and the selected parent `docs/implementation/m2/repository-file-inventory.v170.json`, 639076 bytes, SHA-256 `6f6b43a8f6f75587864f87705482f7fa5db25e362276fa5fe0cb82e1c0db96ef`. That parent file on architecture `c698b9bffa193cc98691c5bf83fc02060b9fb28c` matches the pin. `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`, `packagesUnchanged`, and `pendingDecisionsUnchanged` are true.

## Code join

Product main is `9bc242c01672f2aa42a74f6c936b667c1038ed64`, clean, with parent `03afbce448918dd97b12bfe121d51e43e2a9cb88`. The commit modifies `crates/identity/src/lib.rs` and adds `crates/identity/src/streaming_digest.rs` and `crates/identity/src/streaming_digest_tests.rs`. Those blobs match the accepted subject pins: `lib.rs` 3357 bytes, SHA-256 `2e00f0ed23c5ba4af52cdd9051d7a30e2adddf191208b3540e9f454c6f76f01a`; `streaming_digest.rs` 2348 bytes, SHA-256 `19d14dda42290815eaa9f2512ce687bb92504eb4000510ce57384432a81a4b52`; `streaming_digest_tests.rs` 4392 bytes, SHA-256 `03a8c632b146ce182acd0a2c3453648fba96ad9beace7aa3bca8b899d9837f4e`. The architecture copies of those three files match the product blobs.

Architecture `c698b9bffa193cc98691c5bf83fc02060b9fb28c`, parent `6e9d5e0d4001c2ba4bfabdbb49ae5a5858b3febe`, records the accepted SRH-1 review. `docs/implementation/m3/reviews/grok-streaming-raw-hash-r1/review.json` is 517 bytes, SHA-256 `e77371f48ef7d5507ba211937cb99ead0885e31985b8895c64e9d1a488a43206`, verdict ACCEPT-UNIT. The accepted subject `docs/implementation/m3/snapshot-plan-c/streaming-raw-hash-r1-subject.json` is 6051 bytes, SHA-256 `80119d1b52141b084e8376dd0e5e25f55bdd58a6a3b875dc5ae1303edefe5830`. v171 is absent from architecture HEAD. An untracked `docs/implementation/m3/syntax-e/e2s/` tree is outside this subject.

`design-lock.json` is unchanged by the product commit: schemaVersion 4, 602547 bytes, SHA-256 `64504dd716f03ad4393b7a322eccf4e593c880c7c580fb7309ea7d2fd235bf9c`, with 130 inventory successors and 152 contract successors. Every inventory successor has the five closed pins `parent`, `candidate`, `record`, `review`, and `assent`. The selected candidate is v170. The lock carries 103 inherited passage coordinates, each naming v170. v171 is absent from the lock. `tools/verify_design.py` at this commit is 43946 bytes, SHA-256 `7b313de629f2c958a1e62538b909d6f01545be2519238ba9b3d86ab7e7ba3326`.

## Inventory

v171 is a sorted unique strict superset of v170: 1154 file rows, 1152 inherited rows equal by value, including the existing `crates/identity/src/lib.rs` row. The two additions are exactly the successor `addedFiles` set:

- `crates/identity/src/streaming_digest.rs`
- `crates/identity/src/streaming_digest_tests.rs`

Each new row has `description`, `generated`, `package`, `path`, `role`, and `standing`. The package is `opensip-identity`. `generated` is false and `standing` is `proposed`, as on the existing identity rows. `streaming_digest.rs` has role `algorithm`, the same role as `crates/identity/src/digests.rs`. Its description is “Compute a bounded constant-space raw SHA-256 digest across byte chunks without framing or read-completion authority.” `streaming_digest_tests.rs` has role `test`. Its description is “Verify raw streaming SHA-256 vectors, chunk boundaries, byte-count refusal and accumulator storage.”

`schemaVersion`, `standing`, `packages`, and `pendingDecisions` match v170. The package list remains the same 20 ids. Pending decisions remain 9. The standing sentence remains the v170 sentence. It records a proposed additive inventory of the O1-b phase and harness files, unchanged inherited rows, packages, and pending decisions, and no qualification. The successor unit is `SRH-1-inventory-v171`.

The successor `inheritedPlannedFilesRetained` list is the same 100 unique paths as the v170 successor. Each of those rows remains equal by value, with `standing` `proposed` and `generated` false. None of the 100 is tracked. The product tree has 1054 tracked paths, every tracked path is in v171, and those 100 planned paths are exactly the inventory paths absent from the tree. No path contains `SCRATCH`.

## Census

`source-census.json` records product `9bc242c01672f2aa42a74f6c936b667c1038ed64`, checker `tools/check_operability.py` 14464 / `7fb837009a5cf1d286997f64e8f414548f97a57fb341402501f7845e52d069ba`, and `tools/operability/exceptions.json` 82174 / `b0a4da39fec2df0da25aed0085e55d089b65594f3dab1e575ac1dbad419a1a46`. Both blobs match the product commit. The exceptions document has 113 source rows and 431 mint-audit rows. The mint-audit standing is “Conservative lexical call census and complete owner-file definitions; not receiver type inference or mint authority.” The census records source check passed, findings empty, `lexicalAuditGrantsNoMintAuthority` true, `private413Read` false, and `realInstallationRead` false. `productQualification` is false on the successor and the census.

The accepted streaming files are the product tree at this commit. Full C3a, read completion, custody, source profile, owner admission, and R3 remain open, with product qualification.

Root substantive assent, the five closed pins, and the 103 inherited passage coordinates are verified by `tools/verify_design.py --architecture` and `--lock` before a separate lock commit. The product code already has its commit. This acceptance leaves product qualification and plan completion open.
