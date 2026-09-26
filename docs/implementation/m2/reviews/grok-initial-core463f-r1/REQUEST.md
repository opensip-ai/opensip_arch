Grok review 463f-3 (the InitialCore producer) and 463g (its tests), r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-core463f-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/initial-core-launch-463/PROPOSAL.md, r3 plus amendment items 1–12 (all accepted), and owner.md §1a step 3. Product HEAD 8e7eb49, with inventory69 selected; it already plans initial_core.rs and initial_core_tests.rs. The files are pinned in hashes.txt: two new, and four modified (root_payload.rs includes initial_core on macOS; retained_metadata_index.rs gets the `ReadRequest::digest()` accessor; core_authentication.rs has the synthetic builder generalised into `Spec`/`signed_release` in a `pub(super)` test module; macos_image.rs adds the item-11 live-join test).

## Producer (initial_core.rs)

`produce_initial_core(attempt)` runs everything in one `attempt.run`, so any failure latches. The step comments F0–F21 mark each step:
- F0: embedding admission before any native call. The development build refuses `EmbeddedRootAbsent` with only the lineage charged.
- F1: the running image.
- F2: the exact leaf name.
- F3: the tree root. With n entrypoint components and C retained parents, refuse unless n ≤ C; the root is r = C−(n−1). Each directory i in r..=C is judged, and for i > r its name must equal `entrypoint[i−r−1]`.
- F4: the executable's ACL on the image's own descriptor.
- F5: `inventory.json` and `inventory.sig.json`.
- F6: the bootstrap directories.
- F7: the payload pair.
- F8: the locator.
- F9: member opens under judged directories, memoized, with a 16 MiB cap. Then item 9: the one-to-one envelope pairing by carrier stored digest. Deviation from the design: item 9 runs after F9, because the stored digests need the envelope bytes. An extra listed envelope is therefore read, within the cap, before it is refused. It is never stored or used.
- F11: the anchor record, with the binding from the EMBEDDED root.
- F10: the store: exactly item 2 plus the revocation pair.
- F12: `authenticate_embedded_release` on the borrowed budget.
- F13: the bootstrap path.
- F14: K and the flags.
- F15: the entrypoint row's path and its sha256/length against the image.
- F17: item 8, via a pure helper.
- F18: flags.
- F19: K.
- F20: the closing recheck.
- F21: the receipt.

`InitialCore` is private and non-Clone. It has accessors and `recheck(attempt)`, which refuses on a foreign attempt and latches.

## Tests

- Security: 11 new tests on a signed on-disk tree, with explicit ACLs and an injected image (law item 11). The positive tests check the closure, K Stage1 and Stage2, the lineage, and recheck. Every negative the design lists is covered; the helper reports the variants. The live dev path refuses at F0.
- Platform: the live join. The copied test binary is executed, and its kernel cdhash equals the parent's. sha256, length, CS_VALID, and `Entries(≥1)` on both the file and its directory are checked.

## Lead's replay

Workspace `cargo test --all-targets`: 979 passed, 0 failed. Clippy `-D warnings` and fmt pass. One positive production costs about 244 objects, 5,695 edges and 570 KB on the ledger; a recheck adds about 93 objects, 2,115 edges and 158 KB.

## Known gaps, for your judgement

- The live Running image through the whole producer is only in the split form, per item 11.
- Item 8 is tested on the helper only, per item 12.
- Multi-component member paths are untested.
- Budget exhaustion mid-production is untested.
- Parse charges are an allowance, not a proven bound.
- MAX_IMAGE_BYTES is 96 MiB, while the platform observation bound in the live test is 64 MiB. The law fixes no size cap for the real core binary.
- The closing recheck requires unchanged metadata for every judged directory. That is not stated in the law but fits a committed tree.

## Decide

Does the producer implement r3 and items 1–12 exactly, in a safe order? Is any fact admitted before authentication? Is every allocation charged? Is the tree-root derivation (F3 indexing) correct, with the ancestors above the root not judged (item 10)? Does item 9 hold even though envelopes are read first? Is the store exactly item 2? Are custody refusal order, symlinks (ELOOP) and case variants handled? Do the tests genuinely exercise each refusal? Is anything missing? Replay the security and platform libs, workspace clippy and fmt.

review.json must contain top-level "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS) and "requiredFindings". Write REVIEW.md and review.json. Do not commit.
