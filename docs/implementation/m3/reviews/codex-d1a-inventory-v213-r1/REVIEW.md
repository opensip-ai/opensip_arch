# D1a inventory v213 review

**Verdict: ACCEPT-UNIT.** Inventory candidate assessment: ACCEPT. No required findings or non-blocking observations. Product qualification is false.

## Subject and bindings

The staged subject manifest is 680 bytes, SHA-256 `80e66bb99a1b4a1892051cdf95ad5d6136b682ef4f048644d57e7bfb5023c414`. Independently rehashed all three members: candidate inventory, integration census and successor record; every size and digest matches.

Verified pins:

- Parent v212: 716,592 bytes, `b42e7f5f8555aeb8096d6cb29f337efcd7e591e3c06399e6423d65a6a166be17`. Architecture bytes also match its committed HEAD parent artifact.
- Candidate v213: 717,619 bytes, `00fd49c70d6aa3afbf78000868544acbde22206281d2a25e3901a2b4d1f5073a`.
- Successor record: 5,422 bytes, `a940b39ec45fbc2860dfd16fe3a9fb437436801e39218745beec39f0a33fd1ef`.

Product main is clean at `e4e715845d2d0579060709898892d3d5fd93e49e`; architecture HEAD is `907b8998da143b7012beca7083329af50d860c7c`. The successor's accepted-code review pin matches the 185-byte ACCEPT-UNIT review, whose subjectManifestSha256 matches the exact 8,995-byte accepted D1a r4 manifest. The three integrated product-map files match the accepted code bytes. This was a byte-binding check, not a code re-review.

## Inventory assessment

The candidate has 1,296 sorted, unique file rows against the parent's 1,295. It is a strict superset with exactly one added path: `crates/platform/src/process_tests.rs`. Every inherited row is equal by value. The 20 packages, nine pending decisions and other inherited top-level fields are unchanged. All 1,199 tracked product paths are covered. The remaining 97 rows are exactly the successor's inheritedPlannedFilesRetained list; every one is still absent on disk.

The new row correctly assigns opensip-platform, role test and generated=false. Its description identifies the accepted macOS D1a fixture/control coverage and mechanism tests without claiming production supervision, Linux execution or qualification. addedFiles is exact.

`crates/platform/src/process.rs` is exactly the one newly realized planned path. Its inherited adapter description remains an accurate statement of the module's mechanism role: launch, process-group signalling and reap support already authorized operations. D1a does not thereby claim the D3 cancellation policy or tree-supervision work complete. No description override is needed. The inherited public-api description of lib.rs also remains accurate.

## Census and succession

The permitted live operability source check passes with zero findings and 114 rows. The checker compares the live mint inventory with mintAudit.rows as part of source_check; the unchanged exceptions record has exactly 439 mint rows. Checker and exceptions bytes match the integration-census pins and the pre-D1a base. This confirms the recorded census without adding mint authority.

All parent, candidate, accepted-review, accepted-subject and integration-census pins in successor.json match. addedFiles, realizedPlannedFiles and inheritedPlannedFilesRetained match the independently computed sets. The record and census explicitly disclaim qualification.

For the later bind, verified that contract successor 173 has four passage overrides anchored to exact v212 bytes. Their referenced before descriptions remain present unchanged in the corresponding v213 rows. Carrying their accepted meaning through inventoryPassageInheritance is subsequent lock-binding work, along with lead assent, architecture publication and fresh verify_design. Those actions have not been performed or inferred by this review.

No repository, stage or control file was edited. No compiler, Cargo, tests, lane, network, delegation, other-pane access or restricted fixture/installation/key/held-tree access occurred. Only REVIEW.md and review.json were written in the requested review directory.
