# Review: initial core launch 463 r6

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of the one-entry r6 amendment. No repository edits. No product cargo.

The proposal is 14222 bytes, sha256 `63970ddf1604221a433c7134bf44ac9b94187663e61083acb69e954b5e562a0c`, matching `hashes.txt`. `PROPOSAL-r5.md` is 13849 bytes, sha256 `262bd550232b92e7a31e99c129a15adda8d8a74e420dc8e8b7a986ba2d186f39`. The diff is the header note plus one store bullet.

## Verdict

**ACCEPT.**

## Answer

This is the right and minimal fix. Item 5 step 2 verifies the manifest's embedded revocation. An ordinary payload's `members.revocation` is a required member (`verified_recovery_bundle` and `admitted_payload_paths`), and its envelope is one row of `members.envelopes`. `core_anchor::capture` selects bootstrap files through `EmbeddedCapture`, which loads `{bootstrapDirectory}/{path}` by the tree row's sha256 and length. The r5 store listed the anchor record, the three `DocRef` pairs, and later `rootChain` members. The revocation is not a `rootChain` member, so that list could not serve step 2. r6 adds that member and its envelope, read by the same no-follow opens and keyed the same way.

The rest of the revocation order is already covered. Step 1 uses the index-0 root pair and the later chain members. Step 3 re-filters quorums already obtained from the inventory envelope, the bootstrap payload envelope, the chain envelopes, and, once stored, the revocation envelope. The catalog, other manifests, artifacts, and permission policies are payload members and are not inputs to this order. A request for any of them still refuses.

Do not commit.
