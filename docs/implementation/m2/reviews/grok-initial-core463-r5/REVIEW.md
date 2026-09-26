# Review: initial core launch 463 r5

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review of `docs/implementation/m2/initial-core-launch-463/PROPOSAL.md` after 463 r4. No repository edits. No product cargo.

The proposal is 13792 bytes, sha256 `35e1b63d34fb5e456147b00fd73ee24fb6a05b495d94a10925d80b13e12e3b45`, matching `hashes.txt`. `PROPOSAL-r4.md` is the r4 bytes: 12846 bytes, sha256 `1c66458d24d36cffd43d6d7263fe3dd2690dd01f78b7046ae8cb6f0bac38d3f7`. The diff is the header plus amendment items 2 and 5.

## Verdict

**ACCEPT.**

## Answers

RF-1 is closed. Step 3 re-filters, with the set the revocation establishes, every chain-link quorum, the TR-CORE quorum, the TR-BUNDLE quorum, and the revocation document's own quorum, and each must still be met. `filtered_again` only removes keys. A key named in the list is removed from the quorum that established the list, so that key cannot be what makes the revocation effective. If the remaining signers fall below threshold, the producer refuses and does not fall back to the empty initial set. No fact is admitted before step 3 completes. The chain, the inventory, and the manifest are under the same pass, so a revoked key does not remain in any admitted quorum.

RF-2 is closed. The attempt-owned store holds exactly three groups, every allocation charged to the attempt ledger:

- the constructed `CoreAnchorNodeV1` record in the records collection, which is what `capture` loads through `anchor_ref`;
- the three `DocRef` pairs: inventory, bootstrap payload, and the index-0 root;
- every later `rootChain` member the manifest declares, from the no-follow opens r3 already permits, keyed the way `EmbeddedCapture` loads them.

The index-0 root is the third `DocRef`. `capture` checks that reference equal to the tree row `EmbeddedCapture` builds for that member (`sha256` and length), so the pair is the index-0 object load. Later members are the additional objects. A chain-walk request outside that set refuses. Nothing is read from I or any record store, and nothing else is stored.

The r4 answers on the inventory names, the compiled-target platform id, the TR-CORE and TR-BUNDLE quorums, the inventory home for K and the flags, and the core-tree custody predicate stand. The diff does not reopen them.

Do not commit.
