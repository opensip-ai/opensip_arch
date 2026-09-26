Grok review law 463 r8, which adds items 9 to 12. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-core463-r8. Law review. You may read code and run read-only probes; do not run product cargo. Do not read or print the private 413 UUID fixture.

Subject: docs/implementation/m2/initial-core-launch-463/PROPOSAL.md r8 (pin in hashes.txt). `diff` it against PROPOSAL-r7.md. The items came from designing the producer.

- Item 9: `Data::build` in retained_metadata_index.rs (about lines 566–596) loads every `members.envelopes` path before selection, and item 2's store holds nothing else. So the listed envelope set must be exactly one per root-chain body plus the revocation.
- Item 10: custody scope. From the tree root down. The ancestors above it are the retained, name-rechecked, symlink-free locator, not judged by the predicate, because `/` carries no ACL. Qualifying the install location is a separate signed qualification.
- Item 11: test shape. The security unit-test binary is about 620 MB, above the 256 MiB ledger cap (work_ledger.rs:8). So the live join is a platform-crate copied-binary child test, and the producer end to end uses a signed on-disk tree with a test-only injected image. Production has only the live observation.
- Item 12: item 8 never fires in practice, because the closure commits to the revocation file's digest. It stays as a defensive check.

Decide: is each item a sound, minimal completion consistent with r3 to r7, owner.md and security-completion v8 §3.3? For item 10, is not judging the ancestors above the tree root an acceptable stated limit, or does r3 require something stronger? For item 11, does the injected image in tests weaken anything production relies on? Is anything missing?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
