Grok review law 463 r4, an amendment to your accepted 463 r3. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-core463-r4. Law review; no product cargo. Do not read or print the private 413 UUID fixture.

Subject: docs/implementation/m2/initial-core-launch-463/PROPOSAL.md r4 (pin in hashes.txt). `diff` it against PROPOSAL-r3.md. r4 appends the section "r4 amendment" and a header note. Everything accepted in r3 is unchanged. It closes gaps found while planning the code:

1. **Inventory locator.** The inventory pair had no locator. r4 allows only `inventory.json` and `inventory.sig.json`, law 229's reserved top-level names, under the tree root.
2. **Anchor.** The anchor node is built in memory from the five pairs and served to `core_anchor::capture` through an attempt-charged in-memory store.
3. **Platform id.** Before installation it comes from the compiled target. r3's "from the authenticated anchor" is circular when the producer builds that anchor.
4. **Signatures.** TR-CORE on the inventory and TR-BUNDLE on the manifest are verified under the final root after revocation. Today `capture` only parses carriers and `authenticate` only checks root-chain quorums, so K and the flags would be unsigned.
5. **Revocation order.** The embedded chain is authenticated, then the embedded revocation is verified under the final root, then every quorum is re-filtered. No caller-supplied set is accepted.
6. **K and flags.** Both are signed per-row members of `CoreInventoryV3` (unit 463b): `stateWriter` and `requiredCodeSigningFlags`. This explicitly supersedes owner.md §1a step 3's "adds no metadata member".
7. **Custody predicate.** A new core-tree predicate: any owner or root; no group or other write; no ACL write to anyone else, counting inherit-only allows; omission and the sentinel refuse.

Code context:
- core_anchor.rs:108–130, 139–148, 177–290
- core_authentication.rs:43–88
- core_inventory.rs:105–108, 236–321
- admitted_revocations.rs:18
- verified_envelopes.rs:319, 505
- law 229 in reviews/claude-trust-distribution229-author-20260919-r1/REVIEW.md:22–29
- owner.md:23

## Decide

- Is each item a sound, minimal completion of r3 that stays consistent with law 229, owner.md and security-completion v8 §3.3?
- Item 3: is the compiled-target platform id acceptable, given that InitialPlatform refuses a mismatch?
- Item 4: does verifying TR-CORE conflict with law 229's "TR-CORE's signature is never an input", given r4's scoping to pre-installation authentication?
- Item 5: is the revocation order sound (no window where a revoked key counts)?
- Item 6: is superseding the owner.md sentence acceptable as an owner amendment under D-367's delegation, and is the inventory (not the profile set) the right home for the flags?
- Is anything missing?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" (id, title, failureScenario) and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
