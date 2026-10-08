# O1-b additive inventory v170 r1

ACCEPT-UNIT. requiredFindings empty. inventoryCandidateAssessment ACCEPT. productQualification false. This subject closes the additive inventory only. The accepted O1-b code review stays closed on its own subject.

Subject `docs/implementation/m3/operability/o1b-inventory-v170-subject.json` is 1024 bytes, SHA-256 `caa55911be0925995abbb8275eb75a69f52d686abdb5f80fff954e2902c0db95`. Its three members are sorted and unique, and each matches the stage bytes:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/repository-file-inventory.v170.json` | 639076 | `6f6b43a8f6f75587864f87705482f7fa5db25e362276fa5fe0cb82e1c0db96ef` |
| `docs/implementation/m3/operability/o1b-inventory-v170/source-census.json` | 722 | `459a2a3d910e694e675a9e0eac1c24d86fd4108d76193a3f22d31eab92de0445` |
| `docs/implementation/m3/operability/o1b-inventory-v170/successor.json` | 5626 | `80583fdb76cfda28ef7893890f2114dc7b7c33358b094ab94df331cd7597bc87` |

The successor names the same candidate and the selected parent `docs/implementation/m2/repository-file-inventory.v169.json`, 637990 bytes, SHA-256 `0b5c57f04f6a40a7ed770e474be44c14710aa2e7e76957c83541bdf9c36118c3`. That parent file on architecture `a808f5807058ecf8ac053713e458eb68e2d30493` matches the pin. `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`, `packagesUnchanged`, and `pendingDecisionsUnchanged` are true. `rawPackagesUnchanged` is true on the subject.

## Code join

Product main is `fa7c68742dabc0bb3d52ce0be492b37b68c82f77`, whose parent is `790153f929f16823591be725686cc7e5ef86600b`. Architecture `docs/implementation/m3/reviews/grok-o1b-whole-unit-r2/review.json` is 312 bytes, SHA-256 `3c9234f64e8af94b90c34d337f4a995770372487b6843b8156a7228f3c5e24e1`, verdict ACCEPT-UNIT, with `fullO1bCodeAccepted` true, `inventoryAuthored` false, and subject `def506bb4f139c16b4b472b2ac3de99f4a16369cea8390308ad7fe9d1f9d9487`. That subject is `docs/implementation/m3/reviews/grok-o1b-whole-unit-r2/subject.json`, 5095 bytes and the same hash. All 28 pins match the blobs at the product commit. The commit changes those 28 paths and no others: 4 additions and 24 modifications. `design-lock.json` is the same blob as at `790153f929f16823591be725686cc7e5ef86600b`. The lock is schemaVersion 4, 590236 bytes, with 129 inventory successors and 140 contract successors. The last inventory candidate is v169. v170 is absent from the lock and from architecture HEAD. `tools/verify_design.py` is the same blob at that base and at this product commit, 43946 bytes, SHA-256 `7b313de629f2c958a1e62538b909d6f01545be2519238ba9b3d86ab7e7ba3326`, so the five-pin additive profile is unchanged. Bound O1-PKG remains the independent package policy. This inventory does not re-measure that policy.

## Inventory

v169 has 1148 sorted unique file rows. v170 has 1152. The path list is sorted and unique, nothing is removed, and every inherited row is equal by value. The 4 additions are exactly the successor `addedFiles` set:

- `crates/operability/src/harness_writer.rs`
- `crates/operability/src/harness_writer_tests.rs`
- `crates/operability/src/phase.rs`
- `crates/operability/src/phase_clock.rs`

Each new row has only `description`, `package`, `path`, and `role`. The package is `opensip-operability`. `harness_writer_tests.rs` has role `test`. The other three have role `rust-source`, the same role as the existing operability sources. Each description names the accepted O1-b unit and states no qualification claim. Each added path is tracked at the product commit. The 24 modified code paths were already v169 rows, and those rows are unchanged.

`schemaVersion`, `packages`, and `pendingDecisions` match v169. The package list remains the same 20 ids. `opensip-operability` is not added there. Pending decisions remain 9. The candidate standing sentence is the only other top-level change. It records a proposed additive inventory of the O1-b phase and harness files, unchanged inherited rows, packages, and pending decisions, and no qualification.

The successor `inheritedPlannedFilesRetained` list is the same 100 unique paths as the v169 successor. Each of those rows remains equal by value, with `standing` `proposed` and `generated` false. None of the 100 is tracked. The product tree has 1052 tracked paths, every tracked path is in v170, and those 100 planned paths are exactly the inventory paths absent from the tree. No path contains `SCRATCH`.

## Census

`source-census.json` records product `fa7c68742dabc0bb3d52ce0be492b37b68c82f77`, checker `tools/check_operability.py` 14464 / `7fb837009a5cf1d286997f64e8f414548f97a57fb341402501f7845e52d069ba`, and `tools/operability/exceptions.json` 82174 / `b0a4da39fec2df0da25aed0085e55d089b65594f3dab1e575ac1dbad419a1a46`. Both blobs match the product commit. The exceptions document has 113 source rows and 431 mint-audit rows. The mint-audit standing is “Conservative lexical call census and complete owner-file definitions; not receiver type inference or mint authority.” The census records source check passed, findings empty, `lexicalAuditGrantsNoMintAuthority` true, `private413Read` false, and `realInstallationRead` false. The tracked tree has no mint-list file. `productQualification` is false on the subject, the successor, and the census.

Root assent, the five closed pins, and the projected inherited passage coordinates are verified by `tools/verify_design.py --architecture` and `--lock` before a separate lock commit. S-OP-2-P, S-OP-2-R, and S-OP-2b are already bound and closed. O1-c, O1-S, Q0, and strict M6 remain separate. This acceptance does not qualify the product or complete the plan. This review does not push.
